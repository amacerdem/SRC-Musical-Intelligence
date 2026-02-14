"""CycleLoss -- Bidirectional consistency losses.

Ensures encode and decode are true inverses:
- cycle_forward:  Encode(Decode(C3)) ≈ C3
- cycle_inverse:  Decode(Encode(Wav)) ≈ Wav (via mel comparison)

Reference: MI-VISION Section 12.3
"""
from __future__ import annotations

from typing import Dict

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class CycleLoss(nn.Module):
    """Bidirectional cycle consistency losses."""

    def forward(
        self,
        c3_original: Tensor,
        c3_reconstructed: Tensor,
        mel_original: Tensor,
        mel_reconstructed: Tensor,
    ) -> Dict[str, Tensor]:
        """Compute cycle consistency losses.

        Parameters
        ----------
        c3_original : Tensor
            Original C3 teacher output.
        c3_reconstructed : Tensor
            C3 from Encode(Decode(C3_original)).
        mel_original : Tensor
            Original mel spectrogram.
        mel_reconstructed : Tensor
            Mel from Decode(Encode(mel_original)).

        Returns
        -------
        dict
            Maps ``cycle_forward`` and ``cycle_inverse`` to scalar losses.
        """
        return {
            "cycle_forward": F.mse_loss(c3_reconstructed, c3_original),
            "cycle_inverse": F.mse_loss(mel_reconstructed, mel_original),
        }
