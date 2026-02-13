"""Group B: Energy — 5D [7:12] spectral energy features."""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


class EnergyGroup(BaseSpectralGroup):
    GROUP_NAME = "energy"
    DOMAIN = "dsp"
    OUTPUT_DIM = 5

    @property
    def feature_names(self) -> List[str]:
        return ["amplitude", "velocity_A", "acceleration_A", "loudness", "onset_strength"]

    def compute(self, mel: Tensor) -> Tensor:
        """(B, 128, T) → (B, T, 5)."""
        B, N, T = mel.shape

        # [0] amplitude: sqrt(mean(mel^2)) normalized by max across time
        amp = torch.sqrt((mel ** 2).mean(dim=1))  # (B, T)
        amp_max = amp.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        amplitude = amp / amp_max

        # [1] velocity_A: sigmoid(5.0 * diff(amplitude))
        amp_diff = torch.zeros_like(amplitude)
        amp_diff[:, 1:] = amplitude[:, 1:] - amplitude[:, :-1]
        velocity_A = torch.sigmoid(5.0 * amp_diff)

        # [2] acceleration_A: sigmoid(5.0 * diff(velocity, lag=2))
        vel_diff = torch.zeros_like(velocity_A)
        vel_diff[:, 2:] = velocity_A[:, 2:] - velocity_A[:, :-2]
        acceleration_A = torch.sigmoid(5.0 * vel_diff)

        # [3] loudness: amplitude^0.3 (Stevens' power law), normalized
        loudness = amplitude.pow(0.3)
        loud_max = loudness.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        loudness = loudness / loud_max

        # [4] onset_strength: sum(max(0, diff(mel))) normalized
        mel_diff = torch.zeros_like(mel)
        mel_diff[:, :, 1:] = mel[:, :, 1:] - mel[:, :, :-1]
        onset = torch.relu(mel_diff).sum(dim=1)  # (B, T)
        onset_max = onset.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        onset_strength = onset / onset_max

        return torch.stack([
            amplitude, velocity_A, acceleration_A, loudness, onset_strength,
        ], dim=-1).clamp(0.0, 1.0)
