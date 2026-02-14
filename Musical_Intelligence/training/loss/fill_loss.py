"""FillLoss -- Masked C3 completion losses.

Two loss terms for the Fill-Net:
- fill_c3:     filled C3 vs teacher C3 (on masked dims only)
- fill_decode: Decode(filled C3) vs teacher intermediate layers

Reference: MI-VISION Section 12.3
"""
from __future__ import annotations

from typing import Dict, Optional

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class FillLoss(nn.Module):
    """Fill-Net completion losses."""

    def forward(
        self,
        c3_filled: Tensor,
        c3_target: Tensor,
        mask: Tensor,
        decode_mel_from_filled: Optional[Tensor] = None,
        mel_target: Optional[Tensor] = None,
    ) -> Dict[str, Tensor]:
        """Compute fill losses.

        Parameters
        ----------
        c3_filled : Tensor
            Shape ``(B, T, 1006)`` filled C3.
        c3_target : Tensor
            Shape ``(B, T, 1006)`` teacher C3.
        mask : Tensor
            Shape ``(B, T, 1006)`` binary (1=known, 0=masked).
        decode_mel_from_filled : Tensor, optional
            Mel reconstructed from filled C3 (for fill_decode loss).
        mel_target : Tensor, optional
            Teacher mel target.

        Returns
        -------
        dict
            Maps ``fill_c3`` and ``fill_decode`` to scalar losses.
        """
        # Loss only on MASKED dimensions
        masked_region = 1.0 - mask  # 1 where masked
        fill_loss = F.mse_loss(
            c3_filled * masked_region,
            c3_target * masked_region,
            reduction="sum",
        ) / masked_region.sum().clamp(min=1)

        # Decode loss from filled C3
        if decode_mel_from_filled is not None and mel_target is not None:
            fill_decode_loss = F.mse_loss(decode_mel_from_filled, mel_target)
        else:
            fill_decode_loss = c3_filled.new_tensor(0.0)

        return {
            "fill_c3": fill_loss,
            "fill_decode": fill_decode_loss,
        }
