"""Group A: Consonance — 7D [0:7] psychoacoustic features."""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


def _spectral_autocorrelation(mel: Tensor) -> Tensor:
    """Lag-1 centered autocorrelation. (B, N, T) → (B, T)."""
    mean = mel.mean(dim=1, keepdim=True)
    centered = mel - mean
    auto = (centered[:, :-1, :] * centered[:, 1:, :]).mean(dim=1)
    var = (centered ** 2).mean(dim=1)
    result = auto / (var + 1e-8)
    return result.clamp(0.0, 1.0)


class ConsonanceGroup(BaseSpectralGroup):
    GROUP_NAME = "consonance"
    DOMAIN = "psychoacoustic"
    OUTPUT_DIM = 7

    @property
    def feature_names(self) -> List[str]:
        return [
            "roughness", "sethares_dissonance", "helmholtz_kang",
            "stumpf_fusion", "sensory_pleasantness",
            "inharmonicity", "harmonic_deviation",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """(B, 128, T) → (B, T, 7)."""
        B, N, T = mel.shape
        half = N // 2

        # [0] roughness: sigmoid(var(high_bins) / mean - 0.5)
        high = mel[:, half:, :]
        high_var = high.var(dim=1)
        high_mean = high.mean(dim=1).clamp(min=1e-8)
        roughness = torch.sigmoid(high_var / high_mean - 0.5)

        # [1] sethares_dissonance: mean(|diff|) / max
        diff = (mel[:, 1:, :] - mel[:, :-1, :]).abs().mean(dim=1)
        mel_max = mel.max(dim=1).values.clamp(min=1e-8)
        sethares = (diff / mel_max).clamp(0.0, 1.0)

        # [2] helmholtz_kang: lag-1 centered autocorrelation
        helmholtz = _spectral_autocorrelation(mel)

        # [3] stumpf_fusion: low-freq energy ratio
        low = mel[:, :half, :]
        stumpf = low.sum(dim=1) / mel.sum(dim=1).clamp(min=1e-8)
        stumpf = stumpf.clamp(0.0, 1.0)

        # [4] sensory_pleasantness: 0.6 * smoothness + 0.4 * stumpf
        # smoothness = 1 - roughness (proxy)
        smoothness = 1.0 - roughness
        pleasantness = 0.6 * smoothness + 0.4 * stumpf

        # [5] inharmonicity: 1.0 - helmholtz
        inharmonicity = 1.0 - helmholtz

        # [6] harmonic_deviation: 0.5 * sethares + 0.5 * inharmonicity
        harmonic_dev = 0.5 * sethares + 0.5 * inharmonicity

        # Stack: (B, T, 7)
        return torch.stack([
            roughness, sethares, helmholtz, stumpf,
            pleasantness, inharmonicity, harmonic_dev,
        ], dim=-1).clamp(0.0, 1.0)
