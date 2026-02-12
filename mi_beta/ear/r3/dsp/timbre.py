"""
R3 Group C: Timbre/Quality (9D) [12:21]

"Does this sound good?"

Timbral features that characterize the spectral quality and
contribute to hedonic evaluation (opioid_proxy, liking).
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts import BaseSpectralGroup


class TimbreGroup(BaseSpectralGroup):
    GROUP_NAME = "timbre"
    OUTPUT_DIM = 9
    INDEX_RANGE = (12, 21)

    @property
    def feature_names(self) -> List[str]:
        return [
            "warmth",                 # Low-frequency balance
            "sharpness",              # High-frequency weighting
            "tonalness",              # Harmonic-to-noise ratio
            "clarity",                # Signal-to-noise definition
            "spectral_smoothness",    # Spectral envelope regularity
            "spectral_autocorrelation",  # Harmonic periodicity
            "tristimulus1",           # Fundamental strength
            "tristimulus2",           # 2nd-4th harmonic energy
            "tristimulus3",           # 5th+ harmonic energy
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute timbre features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 9) timbre features in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)
        total_energy = mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)

        # Warmth: energy in low-frequency bins (bottom quarter)
        low_cutoff = N // 4
        warmth = mel_t[..., :low_cutoff].sum(dim=-1, keepdim=True) / total_energy

        # Sharpness: energy in high-frequency bins (top quarter)
        high_cutoff = 3 * N // 4
        sharpness = mel_t[..., high_cutoff:].sum(dim=-1, keepdim=True) / total_energy

        # Tonalness: ratio of peak energy to total (harmonic-to-noise proxy)
        peak_energy = mel_t.max(dim=-1, keepdim=True).values
        tonalness = peak_energy / total_energy

        # Clarity: spectral centroid normalized
        bin_indices = torch.arange(N, device=mel.device, dtype=mel.dtype)
        centroid = (mel_t * bin_indices).sum(dim=-1, keepdim=True) / total_energy
        clarity = centroid / N

        # Spectral smoothness: 1 - normalized spectral irregularity
        diff = torch.diff(mel_t, dim=-1).abs()
        irregularity = diff.mean(dim=-1, keepdim=True)
        irr_max = irregularity.amax(dim=1, keepdim=True).clamp(min=1e-8)
        smoothness = 1.0 - (irregularity / irr_max)

        # Spectral autocorrelation: periodicity in spectrum
        centered = mel_t - mel_t.mean(dim=-1, keepdim=True)
        norm = centered.norm(dim=-1, keepdim=True).clamp(min=1e-8)
        normalized = centered / norm
        autocorr = (normalized[..., :-1] * normalized[..., 1:]).sum(dim=-1, keepdim=True)
        autocorr = autocorr.clamp(0, 1)

        # Tristimulus: energy distribution across spectral thirds
        third = N // 3
        t1 = mel_t[..., :third].sum(dim=-1, keepdim=True) / total_energy
        t2 = mel_t[..., third:2*third].sum(dim=-1, keepdim=True) / total_energy
        t3 = mel_t[..., 2*third:].sum(dim=-1, keepdim=True) / total_energy

        features = torch.cat([
            warmth, sharpness, tonalness, clarity,
            smoothness, autocorr, t1, t2, t3,
        ], dim=-1)  # (B, T, 9)

        return features.clamp(0, 1)
