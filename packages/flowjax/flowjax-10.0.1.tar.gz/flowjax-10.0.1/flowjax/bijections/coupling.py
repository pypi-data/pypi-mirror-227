"""Implemenetation of Coupling flow layer with arbitrary transformer.
See https://arxiv.org/abs/1605.08803 for more information.
"""
from typing import Callable

import equinox as eqx
import jax.nn as jnn
import jax.numpy as jnp
from jax.random import KeyArray

from flowjax.bijections.bijection import Bijection
from flowjax.bijections.jax_transforms import Batch
from flowjax.utils import Array, get_ravelled_bijection_constructor


class Coupling(Bijection):
    """Coupling layer implementation (https://arxiv.org/abs/1605.08803)."""

    untransformed_dim: int
    dim: int
    transformer_constructor: Callable
    conditioner: eqx.nn.MLP

    def __init__(
        self,
        key: KeyArray,
        transformer: Bijection,
        untransformed_dim: int,
        dim: int,
        cond_dim: int | None,
        nn_width: int,
        nn_depth: int,
        nn_activation: Callable = jnn.relu,
    ):
        """
        Args:
            key (KeyArray): Jax PRNGKey
            transformer (Bijection): Unconditional bijection with shape () to be
                parameterised by the conditioner neural netork.
            untransformed_dim (int): Number of untransformed conditioning variables (
                e.g. dim // 2).
            dim (int): Total dimension.
            cond_dim (int | None): Dimension of additional conditioning variables.
            nn_width (int): Neural network hidden layer width.
            nn_depth (int): Neural network hidden layer size.
            nn_activation (Callable): Neural network activation function.
                Defaults to jnn.relu.
        """
        if transformer.shape != () or transformer.cond_shape is not None:
            raise ValueError(
                "Only unconditional transformers with shape () are supported."
            )

        constructor, transformer_init_params = get_ravelled_bijection_constructor(
            transformer
        )

        self.transformer_constructor = constructor
        self.untransformed_dim = untransformed_dim
        self.dim = dim
        self.shape = (dim,)
        self.cond_shape = (cond_dim,) if cond_dim is not None else None

        conditioner_output_size = transformer_init_params.size * (
            dim - untransformed_dim
        )

        conditioner = eqx.nn.MLP(
            in_size=untransformed_dim
            if cond_dim is None
            else untransformed_dim + cond_dim,
            out_size=conditioner_output_size,
            width_size=nn_width,
            depth=nn_depth,
            activation=nn_activation,
            key=key,
        )  # type: eqx.nn.MLP

        # Initialise last bias terms to match the provided transformer parameters
        self.conditioner = eqx.tree_at(
            where=lambda mlp: mlp.layers[-1].bias,  # type: ignore
            pytree=conditioner,
            replace=jnp.tile(transformer_init_params, dim - untransformed_dim),
        )

    def transform(self, x, condition=None):
        x_cond, x_trans = x[: self.untransformed_dim], x[self.untransformed_dim :]
        nn_input = x_cond if condition is None else jnp.hstack((x_cond, condition))
        transformer_params = self.conditioner(nn_input)
        transformer = self._flat_params_to_transformer(transformer_params)
        y_trans = transformer.transform(x_trans)
        y = jnp.hstack((x_cond, y_trans))
        return y

    def transform_and_log_det(self, x, condition=None):
        x_cond, x_trans = x[: self.untransformed_dim], x[self.untransformed_dim :]
        nn_input = x_cond if condition is None else jnp.hstack((x_cond, condition))
        transformer_params = self.conditioner(nn_input)
        transformer = self._flat_params_to_transformer(transformer_params)
        y_trans, log_det = transformer.transform_and_log_det(x_trans)
        y = jnp.hstack((x_cond, y_trans))
        return y, log_det

    def inverse(self, y, condition=None):
        x_cond, y_trans = y[: self.untransformed_dim], y[self.untransformed_dim :]
        nn_input = x_cond if condition is None else jnp.concatenate((x_cond, condition))
        transformer_params = self.conditioner(nn_input)
        transformer = self._flat_params_to_transformer(transformer_params)
        x_trans = transformer.inverse(y_trans)
        x = jnp.hstack((x_cond, x_trans))
        return x

    def inverse_and_log_det(self, y, condition=None):
        x_cond, y_trans = y[: self.untransformed_dim], y[self.untransformed_dim :]
        nn_input = x_cond if condition is None else jnp.concatenate((x_cond, condition))
        transformer_params = self.conditioner(nn_input)
        transformer = self._flat_params_to_transformer(transformer_params)
        x_trans, log_det = transformer.inverse_and_log_det(y_trans)
        x = jnp.hstack((x_cond, x_trans))
        return x, log_det

    def _flat_params_to_transformer(self, params: Array):
        """Reshape to dim X params_per_dim, then vmap."""
        dim = self.dim - self.untransformed_dim
        transformer_params = jnp.reshape(params, (dim, -1))
        transformer = eqx.filter_vmap(self.transformer_constructor)(transformer_params)
        return Batch(transformer, (dim,), vectorize_bijection=True)
