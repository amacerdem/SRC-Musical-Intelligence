"""MelEncoder -- Projects mel spectrogram into backbone hidden space.

Transforms the 128D mel spectrogram into the backbone's hidden
dimension for the encode (analysis) direction.
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import BACKBONE_HIDDEN_DIM, COCHLEA_DIM


class MelEncoder(nn.Module):
    """Mel spectrogram encoder: (B, T, 128) → (B, T, d_model).

    Parameters
    ----------
    input_dim : int
        Mel spectrogram dimension (default 128).
    d_model : int
        Backbone hidden dimension (default 2048).
    """

    def __init__(
        self,
        input_dim: int = COCHLEA_DIM,
        d_model: int = BACKBONE_HIDDEN_DIM,
    ) -> None:
        super().__init__()
        self.proj = nn.Sequential(
            nn.Linear(input_dim, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model),
            nn.LayerNorm(d_model),
        )

    def forward(self, mel: Tensor) -> Tensor:
        """Project mel features into backbone space.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, T, 128)`` mel spectrogram (time-first).

        Returns
        -------
        Tensor
            Shape ``(B, T, d_model)``.
        """
        return self.proj(mel)
