"""
R³ Group D: Change/Surprise (4D) [21:25]

"Did something unexpected happen?"

Features that detect spectral changes and novelty — the raw
material for prediction error computation.
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSpectralGroup


class ChangeGroup(BaseSpectralGroup):
    GROUP_NAME = "change"
    OUTPUT_DIM = 4
    INDEX_RANGE = (21, 25)

    @property
    def feature_names(self) -> List[str]:
        return [
            "spectral_flux",              # Frame-to-frame spectral change
            "distribution_entropy",       # Shannon entropy of spectrum
            "distribution_flatness",      # Wiener entropy
            "distribution_concentration", # Herfindahl index
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute change/surprise features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 4) change features in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)

        # Spectral flux: L2 norm of frame-to-frame difference
        flux = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        if T > 1:
            diff = mel_t[:, 1:] - mel_t[:, :-1]
            flux[:, 1:] = diff.norm(dim=-1)
        flux_max = flux.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        flux_norm = (flux / flux_max).unsqueeze(-1)

        # Distribution: normalize spectrum to probability distribution
        prob = mel_t / mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        prob = prob.clamp(min=1e-10)

        # Shannon entropy
        entropy = -(prob * prob.log()).sum(dim=-1, keepdim=True)
        max_entropy = torch.log(torch.tensor(N, dtype=mel.dtype, device=mel.device))
        entropy_norm = entropy / max_entropy

        # Spectral flatness (Wiener entropy): geometric mean / arithmetic mean
        log_mean = prob.log().mean(dim=-1, keepdim=True)
        arith_mean = prob.mean(dim=-1, keepdim=True)
        flatness = log_mean.exp() / arith_mean.clamp(min=1e-10)
        flatness = flatness.clamp(0, 1)

        # Spectral concentration (Herfindahl): sum of squared probabilities
        concentration = prob.pow(2).sum(dim=-1, keepdim=True)
        # Invert so high concentration → high value
        concentration = concentration * N  # scale to ~[0,1]
        concentration = concentration.clamp(0, 1)

        features = torch.cat([
            flux_norm, entropy_norm, flatness, concentration,
        ], dim=-1)  # (B, T, 4)

        return features.clamp(0, 1)
