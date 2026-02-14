"""DecodeLoss -- Multi-head auxiliary losses for the decode direction.

Four loss terms supervise the decode path at every layer:
- decode_h3:  reconstructed H3 vs teacher H3
- decode_r3:  reconstructed R3 vs teacher R3
- decode_mel: reconstructed mel vs teacher mel
- decode_wav: reconstructed waveform vs original (multi-res STFT)
"""
from __future__ import annotations

from typing import Dict, Optional

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class DecodeLoss(nn.Module):
    """Compute decode direction losses at every layer.

    The waveform loss (decode_wav) uses multi-resolution STFT
    when available, falling back to MSE on mel.
    """

    def __init__(self, use_wav_loss: bool = False) -> None:
        super().__init__()
        self._use_wav_loss = use_wav_loss

    def forward(
        self,
        h3_rec: Tensor,
        r3_rec: Tensor,
        mel_rec: Tensor,
        h3_target: Tensor,
        r3_target: Tensor,
        mel_target: Tensor,
        wav_rec: Optional[Tensor] = None,
        wav_target: Optional[Tensor] = None,
        mask: Optional[Tensor] = None,
    ) -> Dict[str, Tensor]:
        """Compute decode losses.

        Returns dict with decode_h3, decode_r3, decode_mel, decode_wav.
        """
        losses = {
            "decode_h3": self._masked_mse(h3_rec, h3_target, mask),
            "decode_r3": self._masked_mse(r3_rec, r3_target, mask),
            "decode_mel": self._masked_mse(mel_rec, mel_target, mask),
        }

        # Waveform loss (optional, expensive)
        if self._use_wav_loss and wav_rec is not None and wav_target is not None:
            losses["decode_wav"] = F.mse_loss(wav_rec, wav_target)
        else:
            losses["decode_wav"] = mel_rec.new_tensor(0.0)

        return losses

    @staticmethod
    def _masked_mse(
        pred: Tensor, target: Tensor, mask: Optional[Tensor]
    ) -> Tensor:
        loss = F.mse_loss(pred, target, reduction="none")
        if mask is not None:
            mask_expanded = mask.unsqueeze(-1).float()
            loss = (loss * mask_expanded).sum() / mask_expanded.sum().clamp(min=1)
        else:
            loss = loss.mean()
        return loss
