"""BrainOutput + PsiState -- Complete C³ output structure.

C³ produces FOUR outputs (TERMINOLOGY.md Section 15):
    tensor  (B, T, N_ext)   — external+hybrid dims from 96 nuclei
    ram     (B, T, 26)      — Region Activation Map
    neuro   (B, T, 4)       — neurochemical state [DA, NE, OPI, 5HT]
    psi     (B, T, N_psi)   — Ψ³ cognitive interpretation

PsiState groups Ψ³ dimensions into 6 cognitive domains
(TERMINOLOGY.md Section 16.4).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


@dataclass
class PsiState:
    """Ψ³ cognitive interpretation — grouped into 6 domains.

    Each field is a ``(B, T, N_domain)`` tensor. The ``flat`` property
    concatenates all domains into a single ``(B, T, N_psi)`` tensor.

    Domains (from TERMINOLOGY.md Section 16.4):
        affect:    Core emotional coordinates (valence, arousal, tension, dominance)
        emotion:   Categorical feelings (joy, sadness, fear, anger, awe, ...)
        aesthetic:  Musical judgement (beauty, groove, flow, surprise, ...)
        bodily:    Felt sensations (chills, movement_urge, breathing_change, ...)
        cognitive: Mental states (familiarity, absorption, expectation, ...)
        temporal:  Moment-in-time (anticipation, resolution, buildup, release, ...)
    """

    affect: Tensor
    emotion: Tensor
    aesthetic: Tensor
    bodily: Tensor
    cognitive: Tensor
    temporal: Tensor

    @property
    def flat(self) -> Tensor:
        """All domains concatenated: ``(B, T, N_psi)``."""
        import torch

        return torch.cat(
            [self.affect, self.emotion, self.aesthetic,
             self.bodily, self.cognitive, self.temporal],
            dim=-1,
        )

    @property
    def n_psi(self) -> int:
        """Total number of Ψ³ dimensions across all domains."""
        return (
            self.affect.shape[-1]
            + self.emotion.shape[-1]
            + self.aesthetic.shape[-1]
            + self.bodily.shape[-1]
            + self.cognitive.shape[-1]
            + self.temporal.shape[-1]
        )


@dataclass
class BrainOutput:
    """Complete C³ output — the brain's four output channels.

    Attributes:
        tensor:  ``(B, T, N_ext)`` — external+hybrid dims from all nuclei.
        ram:     ``(B, T, 26)`` — Region Activation Map.
        neuro:   ``(B, T, 4)`` — neurochemical state [DA, NE, OPI, 5HT].
        psi:     Ψ³ cognitive interpretation (PsiState with 6 domains).
    """

    tensor: Tensor
    ram: Tensor
    neuro: Tensor
    psi: PsiState
