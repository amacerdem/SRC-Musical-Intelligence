"""DecodeHeads -- Output heads for the decode (synthesis) direction.

In decode mode, the backbone processes C3 → hidden, then these heads
reconstruct each intermediate layer: H3, R3, and Mel.

Each head is supervised by the MI Teacher at its corresponding layer.
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import (
    BACKBONE_HIDDEN_DIM,
    COCHLEA_DIM,
    H3_AUX_DIM,
    R3_DIM,
)


class DecodeH3Head(nn.Module):
    """Decode head for H3 reconstruction: hidden → ~5210D."""

    def __init__(
        self,
        d_model: int = BACKBONE_HIDDEN_DIM,
        h3_dim: int = H3_AUX_DIM,
    ) -> None:
        super().__init__()
        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, h3_dim),
            nn.Sigmoid(),
        )

    def forward(self, hidden: Tensor) -> Tensor:
        return self.proj(hidden)


class DecodeR3Head(nn.Module):
    """Decode head for R3 reconstruction: hidden → 128D."""

    def __init__(
        self,
        d_model: int = BACKBONE_HIDDEN_DIM,
        r3_dim: int = R3_DIM,
    ) -> None:
        super().__init__()
        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Linear(d_model // 2, r3_dim),
            nn.Sigmoid(),
        )

    def forward(self, hidden: Tensor) -> Tensor:
        return self.proj(hidden)


class DecodeMelHead(nn.Module):
    """Decode head for Mel reconstruction: hidden → 128D."""

    def __init__(
        self,
        d_model: int = BACKBONE_HIDDEN_DIM,
        mel_dim: int = COCHLEA_DIM,
    ) -> None:
        super().__init__()
        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Linear(d_model // 2, mel_dim),
            nn.Sigmoid(),
        )

    def forward(self, hidden: Tensor) -> Tensor:
        return self.proj(hidden)
