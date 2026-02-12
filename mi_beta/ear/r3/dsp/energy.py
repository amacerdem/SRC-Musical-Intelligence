"""
R3 Group B: Energy/Dynamics (5D) [7:12]

"Is the music building or releasing?"

Energy-related features that track loudness, dynamics, and
temporal energy patterns.
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts import BaseSpectralGroup


class EnergyGroup(BaseSpectralGroup):
    GROUP_NAME = "energy"
    OUTPUT_DIM = 5
    INDEX_RANGE = (7, 12)

    @property
    def feature_names(self) -> List[str]:
        return [
            "amplitude",          # RMS energy per frame
            "velocity_A",         # dA/dt — rate of energy change
            "acceleration_A",     # d²A/dt² — energy buildup curvature
            "loudness",           # Stevens' law (sone approximation)
            "onset_strength",     # Transient energy
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute energy features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 5) energy features in [0, 1]
        """
        B, N, T = mel.shape

        # Amplitude: RMS energy per frame
        amplitude = mel.pow(2).mean(dim=1).sqrt()  # (B, T)
        amp_max = amplitude.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        amplitude_norm = amplitude / amp_max

        # Velocity: first temporal derivative of amplitude
        velocity = torch.zeros_like(amplitude)
        if T > 1:
            velocity[:, 1:] = amplitude_norm[:, 1:] - amplitude_norm[:, :-1]
        velocity_norm = torch.sigmoid(velocity * 5.0)  # scale to [0,1]

        # Acceleration: second temporal derivative
        acceleration = torch.zeros_like(amplitude)
        if T > 2:
            acceleration[:, 1:-1] = velocity[:, 2:] - velocity[:, :-2]
        acceleration_norm = torch.sigmoid(acceleration * 5.0)

        # Loudness: Stevens' law approximation (sone ~ intensity^0.3)
        loudness = amplitude.pow(0.3)
        loud_max = loudness.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        loudness_norm = loudness / loud_max

        # Onset strength: spectral flux (positive only)
        onset = torch.zeros_like(amplitude)
        if T > 1:
            flux = mel[:, :, 1:] - mel[:, :, :-1]
            onset[:, 1:] = flux.clamp(min=0).sum(dim=1)
        onset_max = onset.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        onset_norm = onset / onset_max

        features = torch.stack([
            amplitude_norm, velocity_norm, acceleration_norm,
            loudness_norm, onset_norm,
        ], dim=-1)  # (B, T, 5)

        return features.clamp(0, 1)
