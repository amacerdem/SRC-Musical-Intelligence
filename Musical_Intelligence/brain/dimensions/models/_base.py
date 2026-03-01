"""Base protocol for dimension computation models.

Each model is a pure function: (beliefs) → (B, T) scalar in [0, 1].
Models are stateless — all state lives in the belief tensor.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from torch import Tensor


class DimensionModel(Protocol):
    """Callable protocol for dimension computation functions."""

    def __call__(self, beliefs: Tensor) -> Tensor:
        """Compute a single dimension value.

        Args:
            beliefs: ``(B, T, 131)`` — all C³ belief values.

        Returns:
            ``(B, T)`` scalar in [0, 1].
        """
        ...
