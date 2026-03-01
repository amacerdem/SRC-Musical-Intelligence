"""Base protocol for dimension computation models.

Each model is a pure function: (beliefs, ram, neuro) → (B, T) scalar in [0, 1].
Models are stateless — all state lives in the input tensors.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from torch import Tensor


class DimensionModel(Protocol):
    """Callable protocol for dimension computation functions."""

    def __call__(
        self, beliefs: Tensor, ram: Tensor, neuro: Tensor,
    ) -> Tensor:
        """Compute a single dimension value.

        Args:
            beliefs: ``(B, T, 131)`` — all C³ belief values.
            ram:     ``(B, T, 26)``  — Region Activation Map.
            neuro:   ``(B, T, 4)``   — neurochemical state [DA, NE, OPI, 5HT].

        Returns:
            ``(B, T)`` scalar in [0, 1].
        """
        ...
