"""BrainOutput and PsiState dataclasses for C³ cognitive architecture.

BrainOutput is the top-level output of the BrainOrchestrator, containing
four channels: tensor, RAM, neuro, and Psi state.

PsiState holds the 6 cognitive domains produced by the PsiInterpreter.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


class PsiState:
    """Psi-cubed cognitive state — 6 experiential domains.

    Attributes:
        affect:    ``(B, T, 4)`` — valence, arousal, tension, dominance
        emotion:   ``(B, T, 7)`` — joy, sadness, fear, awe, nostalgia, tenderness, serenity
        aesthetic: ``(B, T, 5)`` — beauty, groove, flow, surprise, closure
        bodily:    ``(B, T, 4)`` — chills, movement_urge, breathing_change, tension_release
        cognitive: ``(B, T, 4)`` — familiarity, absorption, expectation, attention_focus
        temporal:  ``(B, T, 4)`` — anticipation, resolution, buildup, release
    """

    __slots__ = ("affect", "emotion", "aesthetic", "bodily", "cognitive", "temporal")

    def __init__(
        self,
        affect: Tensor,
        emotion: Tensor,
        aesthetic: Tensor,
        bodily: Tensor,
        cognitive: Tensor,
        temporal: Tensor,
    ) -> None:
        self.affect = affect
        self.emotion = emotion
        self.aesthetic = aesthetic
        self.bodily = bodily
        self.cognitive = cognitive
        self.temporal = temporal

    def __repr__(self) -> str:
        dims = []
        for name in self.__slots__:
            t = getattr(self, name)
            dims.append(f"{name}={tuple(t.shape)}")
        return f"PsiState({', '.join(dims)})"


class BrainOutput:
    """Top-level output from the BrainOrchestrator.

    Attributes:
        tensor: ``(B, T, N_ext)`` — concatenated external+hybrid dims from all nuclei.
        ram:    ``(B, T, 26)`` — Region Activation Map.
        neuro:  ``(B, T, 4)`` — neurochemical state [DA, NE, OPI, 5HT].
        psi:    ``PsiState`` — Psi-cubed cognitive interpretation.
    """

    __slots__ = ("tensor", "ram", "neuro", "psi")

    def __init__(
        self,
        tensor: Tensor,
        ram: Tensor,
        neuro: Tensor,
        psi: PsiState,
    ) -> None:
        self.tensor = tensor
        self.ram = ram
        self.neuro = neuro
        self.psi = psi

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
            f"neuro={tuple(self.neuro.shape)}, "
            f"psi={self.psi})"
        )
