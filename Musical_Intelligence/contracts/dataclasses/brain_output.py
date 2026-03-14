"""BrainOutput dataclass for C³.

BrainOutput is the top-level output of the BrainOrchestrator, containing
three channels: tensor, RAM, and neuro.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


class BrainOutput:
    """Top-level output from the BrainOrchestrator.

    Attributes:
        tensor: ``(B, T, N_ext)`` — concatenated external+hybrid dims from all nuclei.
        ram:    ``(B, T, 26)`` — Region Activation Map.
        neuro:  ``(B, T, 4)`` — neurochemical state [DA, NE, OPI, 5HT].
    """

    __slots__ = ("tensor", "ram", "neuro")

    def __init__(
        self,
        tensor: Tensor,
        ram: Tensor,
        neuro: Tensor,
    ) -> None:
        self.tensor = tensor
        self.ram = ram
        self.neuro = neuro

    @property
    def reward(self) -> Tensor | None:
        """Convenience accessor — reward is the mean of the tensor channel.

        Returns the per-frame mean of the external tensor as a simple
        reward proxy, or None if tensor has 0 dims.
        """
        if self.tensor.shape[-1] == 0:
            return None
        return self.tensor.mean(dim=-1)

    def __repr__(self) -> str:
        return (
            f"BrainOutput("
            f"tensor={tuple(self.tensor.shape)}, "
            f"ram={tuple(self.ram.shape)}, "
            f"neuro={tuple(self.neuro.shape)})"
        )
