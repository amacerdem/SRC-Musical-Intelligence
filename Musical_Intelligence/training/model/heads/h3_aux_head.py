"""H3AuxiliaryHead -- Training-only H3 temporal feature prediction.

Predicts ~5210 H3 temporal features from the backbone hidden state.
This auxiliary head teaches the backbone to internalize temporal
patterns (multi-scale morphology, memory, prediction, integration).

After training, this head is PRUNED. The backbone retains temporal
awareness in its Mamba-2 state without needing explicit H3 computation.

Reference: MI-VISION Section 4.6
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import H3_AUX_DIM


class H3AuxiliaryHead(nn.Module):
    """H3 auxiliary head: hidden → ~5210D temporal features (training only).

    Parameters
    ----------
    d_model : int
        Backbone hidden dimension (default 2048).
    h3_dim : int
        H3 output dimension (default 5210).
    """

    def __init__(
        self,
        d_model: int = 2048,
        h3_dim: int = H3_AUX_DIM,
    ) -> None:
        super().__init__()
        self.h3_dim = h3_dim

        # Larger MLP due to high-dimensional output
        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, h3_dim),
            nn.Sigmoid(),  # H3 values are in [0, 1]
        )

    def forward(self, hidden: Tensor) -> Tensor:
        """Predict H3 temporal features.

        Parameters
        ----------
        hidden : Tensor
            Shape ``(B, T, d_model)``.

        Returns
        -------
        Tensor
            Shape ``(B, T, h3_dim)`` with values in [0, 1].
        """
        return self.proj(hidden)
