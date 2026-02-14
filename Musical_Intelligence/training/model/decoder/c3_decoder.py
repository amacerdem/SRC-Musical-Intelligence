"""C3Decoder -- Projects C3 cognitive output into backbone hidden space.

For the decode (synthesis) direction: takes the 1006D C3 teacher output
and projects it into the backbone's hidden dimension, allowing the
shared backbone to process it in the inverse direction.
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import BACKBONE_HIDDEN_DIM, C3_DIM


class C3Decoder(nn.Module):
    """C3 input projection for decode direction: (B,T,1006) → (B,T,d_model).

    Parameters
    ----------
    input_dim : int
        C3 dimension (default 1006).
    d_model : int
        Backbone hidden dimension (default 2048).
    """

    def __init__(
        self,
        input_dim: int = C3_DIM,
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

    def forward(self, c3: Tensor) -> Tensor:
        """Project C3 into backbone space.

        Parameters
        ----------
        c3 : Tensor
            Shape ``(B, T, 1006)`` C3 cognitive output.

        Returns
        -------
        Tensor
            Shape ``(B, T, d_model)``.
        """
        return self.proj(c3)
