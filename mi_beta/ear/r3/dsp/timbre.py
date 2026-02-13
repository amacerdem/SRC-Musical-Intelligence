"""Group C: Timbre — 9D [12:21] spectral timbre features."""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


class TimbreGroup(BaseSpectralGroup):
    GROUP_NAME = "timbre"
    DOMAIN = "dsp"
    OUTPUT_DIM = 9

    @property
    def feature_names(self) -> List[str]:
        return [
            "warmth", "sharpness", "tonalness", "clarity",
            "spectral_smoothness", "spectral_autocorrelation",
            "tristimulus1", "tristimulus2", "tristimulus3",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """(B, 128, T) → (B, T, 9)."""
        B, N, T = mel.shape
        total = mel.sum(dim=1).clamp(min=1e-8)  # (B, T)
        quarter = N // 4
        third = N // 3

        # [0] warmth: sum(mel[:N/4]) / total
        warmth = mel[:, :quarter, :].sum(dim=1) / total

        # [1] sharpness: sum(mel[3N/4:]) / total
        sharpness = mel[:, 3 * quarter:, :].sum(dim=1) / total

        # [2] tonalness: max(mel) / total
        tonalness = mel.max(dim=1).values / total

        # [3] clarity: (mel * bin_idx).sum() / total / N (spectral centroid)
        bin_idx = torch.arange(N, device=mel.device, dtype=mel.dtype).view(1, N, 1)
        clarity = (mel * bin_idx).sum(dim=1) / total / N

        # [4] spectral_smoothness: 1 - (mean_diff / max_diff)
        mel_diff = (mel[:, 1:, :] - mel[:, :-1, :]).abs()
        mean_diff = mel_diff.mean(dim=1)
        max_diff = mel_diff.max(dim=1).values.clamp(min=1e-8)
        spectral_smoothness = 1.0 - (mean_diff / max_diff)

        # [5] spectral_autocorrelation: lag-1 centered autocorrelation [0,1]
        mean_mel = mel.mean(dim=1, keepdim=True)
        centered = mel - mean_mel
        auto = (centered[:, :-1, :] * centered[:, 1:, :]).mean(dim=1)
        var = (centered ** 2).mean(dim=1).clamp(min=1e-8)
        spectral_autocorr = (auto / var).clamp(0.0, 1.0)

        # [6] tristimulus1: energy in [0, N/3)
        trist1 = mel[:, :third, :].sum(dim=1) / total

        # [7] tristimulus2: energy in [N/3, 2N/3)
        trist2 = mel[:, third:2 * third, :].sum(dim=1) / total

        # [8] tristimulus3: energy in [2N/3, N)
        trist3 = mel[:, 2 * third:, :].sum(dim=1) / total

        return torch.stack([
            warmth, sharpness, tonalness, clarity,
            spectral_smoothness, spectral_autocorr,
            trist1, trist2, trist3,
        ], dim=-1).clamp(0.0, 1.0)
