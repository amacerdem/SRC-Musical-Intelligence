"""EncodeLoss -- Multi-head auxiliary losses for the encode direction.

Four loss terms supervise the encode path at every MI pipeline layer:
- encode_mel: predicted mel vs teacher mel
- encode_r3:  predicted R3 vs teacher R3
- encode_h3:  predicted H3 vs teacher H3
- encode_c3:  predicted C3 vs teacher C3
"""
from __future__ import annotations

from typing import Dict

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class EncodeLoss(nn.Module):
    """Compute encode direction losses at every layer.

    All losses are MSE between predicted and teacher values.
    """

    def forward(
        self,
        cochlea_hat: Tensor,
        r3_hat: Tensor,
        h3_hat: Tensor,
        c3_hat: Tensor,
        mel_target: Tensor,
        r3_target: Tensor,
        h3_target: Tensor,
        c3_target: Tensor,
        mask: Tensor | None = None,
    ) -> Dict[str, Tensor]:
        """Compute encode losses.

        Parameters
        ----------
        cochlea_hat, r3_hat, h3_hat, c3_hat : Tensor
            Predictions from encode forward pass.
        mel_target, r3_target, h3_target, c3_target : Tensor
            Teacher ground truth.
        mask : Tensor, optional
            ``(B, T)`` bool mask for valid frames.

        Returns
        -------
        dict
            Maps ``encode_mel``, ``encode_r3``, ``encode_h3``, ``encode_c3``
            to scalar loss tensors.
        """
        losses = {
            "encode_mel": self._masked_mse(cochlea_hat, mel_target, mask),
            "encode_r3": self._masked_mse(r3_hat, r3_target, mask),
            "encode_h3": self._masked_mse(h3_hat, h3_target, mask),
            "encode_c3": self._masked_mse(c3_hat, c3_target, mask),
        }
        return losses

    @staticmethod
    def _masked_mse(
        pred: Tensor, target: Tensor, mask: Tensor | None
    ) -> Tensor:
        """MSE loss with optional temporal masking."""
        loss = F.mse_loss(pred, target, reduction="none")
        if mask is not None:
            # mask: (B, T) → (B, T, 1) for broadcasting
            mask_expanded = mask.unsqueeze(-1).float()
            loss = (loss * mask_expanded).sum() / mask_expanded.sum().clamp(min=1)
        else:
            loss = loss.mean()
        return loss
