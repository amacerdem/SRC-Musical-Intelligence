"""UncertaintyHead -- Per-dimension confidence estimation.

Produces a 1366D uncertainty vector where each dimension indicates
how confident MI-Core is about that particular MI-space dimension.
Output in [0, 1] via sigmoid.
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import MI_SPACE_DIM


class UncertaintyHead(nn.Module):
    """Uncertainty head: hidden → 1366D per-dim confidence.

    Parameters
    ----------
    d_model : int
        Backbone hidden dimension (default 2048).
    mi_space_dim : int
        MI-space dimension (default 1366).
    """

    def __init__(
        self,
        d_model: int = 2048,
        mi_space_dim: int = MI_SPACE_DIM,
    ) -> None:
        super().__init__()
        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Linear(d_model // 2, mi_space_dim),
            nn.Sigmoid(),
        )

    def forward(self, hidden: Tensor) -> Tensor:
        """Estimate per-dimension confidence.

        Parameters
        ----------
        hidden : Tensor
            Shape ``(B, T, d_model)``.

        Returns
        -------
        Tensor
            Shape ``(B, T, mi_space_dim)`` with values in [0, 1].
        """
        return self.proj(hidden)
