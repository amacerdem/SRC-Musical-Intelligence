"""FillNet -- Masked autoencoder for C3 completion.

When a performer specifies a few C3 dimensions (e.g., pleasure=0.9,
tension=0.2), FillNet completes the remaining ~1000 dimensions
by learning the correlational structure among 96 cognitive models.

Learned correlations include:
- pleasure ↑ → da_nacc ↑ (r=0.84, Salimpoor 2011)
- tension ↓ → consonance ↑ (BCH model)
- wanting ↑ → da_caudate ↑ (r=0.71, Berridge 2003)
- arousal ↑ → scr ↑, hr ↑ (de Fleurian 2021)

Architecture: Small transformer encoder (4 layers, 512D, 8 heads)
operating on the 1006D C3 space. Independent of the main backbone
to avoid polluting bidirectional representations.

Training: Random masking (10-90% ratio), MSE on masked dims only.

Usage::

    fill_net = FillNet()
    c3_filled = fill_net(c3_masked, mask)
    # c3_filled: (B, T, 1006) with all dimensions completed
"""
from __future__ import annotations

import torch
import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import C3_DIM


class FillNet(nn.Module):
    """Masked autoencoder for C3 completion.

    Parameters
    ----------
    c3_dim : int
        C3 dimension (default 1006).
    hidden_dim : int
        Transformer hidden dimension (default 512).
    n_layers : int
        Number of transformer layers (default 4).
    n_heads : int
        Number of attention heads (default 8).
    dropout : float
        Dropout rate (default 0.1).
    """

    def __init__(
        self,
        c3_dim: int = C3_DIM,
        hidden_dim: int = 512,
        n_layers: int = 4,
        n_heads: int = 8,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self.c3_dim = c3_dim
        self.hidden_dim = hidden_dim

        # Input projection: C3 + mask indicator → hidden
        # Mask is concatenated as an additional 1006D binary indicator
        self.input_proj = nn.Linear(c3_dim * 2, hidden_dim)

        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=n_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=n_layers,
        )

        # Output projection: hidden → C3
        self.output_proj = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, c3_dim),
            nn.Sigmoid(),  # C3 values in [0, 1]
        )

    def forward(self, c3_masked: Tensor, mask: Tensor) -> Tensor:
        """Complete masked C3 dimensions.

        Parameters
        ----------
        c3_masked : Tensor
            Shape ``(B, T, c3_dim)`` with masked dims set to 0.
        mask : Tensor
            Shape ``(B, T, c3_dim)`` binary mask where 1 = KNOWN, 0 = MASKED.

        Returns
        -------
        Tensor
            Shape ``(B, T, c3_dim)`` with all dimensions filled.
        """
        # Concatenate masked values with mask indicator
        x = torch.cat([c3_masked, mask.float()], dim=-1)  # (B, T, 2*c3_dim)
        x = self.input_proj(x)  # (B, T, hidden_dim)

        # Transformer processes temporal context
        x = self.transformer(x)  # (B, T, hidden_dim)

        # Project to C3 space
        c3_filled = self.output_proj(x)  # (B, T, c3_dim)

        # Blend: keep known values, fill masked values
        output = c3_masked * mask + c3_filled * (1 - mask)

        return output

    @staticmethod
    def random_mask(
        c3: Tensor,
        mask_ratio_min: float = 0.1,
        mask_ratio_max: float = 0.9,
    ) -> tuple[Tensor, Tensor]:
        """Create random mask for training.

        Parameters
        ----------
        c3 : Tensor
            Shape ``(B, T, c3_dim)`` complete C3 tensor.
        mask_ratio_min : float
            Minimum fraction of dimensions to mask.
        mask_ratio_max : float
            Maximum fraction of dimensions to mask.

        Returns
        -------
        c3_masked : Tensor
            C3 with masked dimensions zeroed out.
        mask : Tensor
            Binary mask (1 = known, 0 = masked).
        """
        B, T, D = c3.shape

        # Random mask ratio per batch element
        ratios = torch.empty(B, 1, 1, device=c3.device).uniform_(
            mask_ratio_min, mask_ratio_max
        )
        # Mask is per-dimension (same across time for simplicity)
        rand = torch.rand(B, 1, D, device=c3.device)
        mask = (rand > ratios).float().expand(B, T, D)

        c3_masked = c3 * mask
        return c3_masked, mask
