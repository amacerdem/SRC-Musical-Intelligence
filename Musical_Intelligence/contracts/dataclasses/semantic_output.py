"""SemanticGroupOutput -- Immutable output container for a single L3 semantic group.

All tensors follow the ``(B, T, D)`` convention:

    B -- batch size
    T -- time frames
    D -- group output dimensionality (OUTPUT_DIM)

Range convention:

    alpha, beta, gamma, delta, epsilon, eta, theta  [0, 1]
    zeta                                             [-1, +1]
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


@dataclass(frozen=True)
class SemanticGroupOutput:
    """Immutable output container for a single L3 semantic group.

    Attributes:
        group_name:      Canonical group name (e.g. ``"alpha"``, ``"theta"``).
        level:           Epistemological level (1-8).
        tensor:          Semantic output tensor, shape ``(B, T, D)``.
        dimension_names: Ordered dimension labels; length must match
                         ``tensor.shape[-1]``.
    """

    group_name: str
    level: int
    tensor: Tensor
    dimension_names: tuple[str, ...]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        dim = self.tensor.shape[-1]
        if len(self.dimension_names) != dim:
            raise ValueError(
                f"SemanticGroupOutput {self.group_name!r}: "
                f"len(dimension_names) must equal tensor.shape[-1] ({dim}), "
                f"got {len(self.dimension_names)}"
            )
