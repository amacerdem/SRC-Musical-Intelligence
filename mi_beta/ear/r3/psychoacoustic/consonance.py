"""
R3 Group A: Consonance/Dissonance (7D) [0:7]

"Can this moment be liked?"

Psychoacoustic features that determine whether spectral content
is consonant (pleasant) or dissonant (unpleasant).
"""

from __future__ import annotations

from typing import List, Tuple

import torch
from torch import Tensor

from ....contracts import BaseSpectralGroup


class ConsonanceGroup(BaseSpectralGroup):
    GROUP_NAME = "consonance"
    OUTPUT_DIM = 7
    INDEX_RANGE = (0, 7)

    @property
    def feature_names(self) -> List[str]:
        return [
            "roughness",              # Plomp-Levelt critical band beating
            "sethares_dissonance",    # Timbre-dependent dissonance
            "helmholtz_kang",         # Harmonic template matching
            "stumpf_fusion",          # Tonal fusion
            "sensory_pleasantness",   # Spectral regularity + smoothness
            "inharmonicity",          # Deviation from harmonic series
            "harmonic_deviation",     # Error from ideal harmonics
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute consonance features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 7) consonance features in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)

        # Spectral envelope statistics
        spectral_mean = mel_t.mean(dim=-1, keepdim=True)  # (B, T, 1)

        # R0: Roughness — spectral irregularity (high-freq energy variance)
        high_bins = mel_t[..., N // 2:]
        roughness = high_bins.var(dim=-1, keepdim=True) / (spectral_mean.clamp(min=1e-8))
        roughness = torch.sigmoid(roughness - 0.5)

        # R1: Sethares dissonance — adjacent bin interference
        diff = torch.diff(mel_t, dim=-1)
        sethares = diff.abs().mean(dim=-1, keepdim=True)
        sethares = sethares / sethares.amax(dim=1, keepdim=True).clamp(min=1e-8)

        # R2: Helmholtz-Kang — harmonic template matching
        # Peak at harmonically-related bins indicates consonance
        autocorr = _spectral_autocorrelation(mel_t)
        helmholtz = autocorr.unsqueeze(-1)

        # R3: Stumpf fusion — how well partials fuse into single tone
        low_bins = mel_t[..., :N // 4]
        high_bins_broad = mel_t[..., N // 4:]
        ratio = low_bins.sum(dim=-1, keepdim=True) / (
            mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        )
        stumpf = ratio

        # R4: Sensory pleasantness — spectral smoothness + regularity
        smoothness = 1.0 - sethares
        pleasantness = smoothness * 0.6 + stumpf * 0.4

        # R5: Inharmonicity — deviation from harmonic peaks
        inharmonicity = 1.0 - helmholtz

        # R6: Harmonic deviation — energy away from harmonic bins
        harmonic_dev = sethares * 0.5 + inharmonicity * 0.5

        features = torch.cat([
            roughness, sethares, helmholtz, stumpf,
            pleasantness, inharmonicity, harmonic_dev,
        ], dim=-1)  # (B, T, 7)

        return features.clamp(0, 1)


def _spectral_autocorrelation(mel_t: Tensor) -> Tensor:
    """Compute spectral autocorrelation as harmonicity measure.

    Args:
        mel_t: (B, T, N_MELS)

    Returns:
        (B, T) autocorrelation strength in [0, 1]
    """
    # Normalize per frame
    centered = mel_t - mel_t.mean(dim=-1, keepdim=True)
    norm = centered.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    normalized = centered / norm

    # Autocorrelation at lag=1 (adjacent bin correlation)
    autocorr = (normalized[..., :-1] * normalized[..., 1:]).sum(dim=-1)
    return autocorr.clamp(0, 1)
