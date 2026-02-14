"""BaseExpert -- Base class for MI-aligned expert FFN blocks.

Each expert specialises in one region of MI-space:
- E-Cochlea: [0:128]    mel spectrogram (128D)
- E-R3:      [128:256]  spectral features (128D)
- E-C3:      [256:1262] cognitive models (1006D)
- E-L3:      [1262:1366] semantic language (104D)
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor


class BaseExpert(nn.Module):
    """Base expert FFN block.

    A 2-layer MLP with GELU activation that projects from the
    backbone hidden dimension to the expert's output dimension.

    Parameters
    ----------
    d_model : int
        Backbone hidden dimension (input).
    output_dim : int
        Expert output dimension.
    hidden_mult : float
        Hidden layer multiplier (default 4.0).
    dropout : float
        Dropout rate (default 0.0).
    """

    def __init__(
        self,
        d_model: int,
        output_dim: int,
        hidden_mult: float = 4.0,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.output_dim = output_dim
        hidden_dim = int(d_model * hidden_mult)

        self.net = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, hidden_dim, bias=False),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim, bias=False),
        )

    def forward(self, x: Tensor) -> Tensor:
        """Forward pass.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)``.

        Returns
        -------
        Tensor
            Shape ``(B, T, output_dim)``.
        """
        return self.net(x)
