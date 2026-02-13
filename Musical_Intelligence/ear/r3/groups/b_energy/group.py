from __future__ import annotations
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

class EnergyGroup(BaseSpectralGroup):
    GROUP_NAME = "energy"
    DOMAIN = "spectral"
    OUTPUT_DIM = 5
    INDEX_RANGE = (7, 12)
    STAGE = 1
    DEPENDENCIES = ()

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        # [7] amplitude: RMS of mel values, batch max-norm
        amplitude = mt.pow(2).mean(dim=-1).sqrt()  # (B, T)
        amplitude = amplitude / amplitude.amax(dim=-1, keepdim=True).clamp(min=eps)

        # [8] velocity_A: sigmoid(1st derivative * 5)
        # Pad with zero at t=0
        amp_raw = mt.pow(2).mean(dim=-1).sqrt()
        diff1 = torch.zeros_like(amp_raw)
        diff1[:, 1:] = amp_raw[:, 1:] - amp_raw[:, :-1]
        velocity = torch.sigmoid(diff1 * 5.0)

        # [9] acceleration_A: sigmoid(2nd derivative * 5)
        diff2 = torch.zeros_like(amp_raw)
        diff2[:, 2:] = amp_raw[:, 2:] - 2 * amp_raw[:, 1:-1] + amp_raw[:, :-2]
        acceleration = torch.sigmoid(diff2 * 5.0)

        # [10] loudness: amplitude^0.3, max-norm (known double-compression bug)
        loudness = amp_raw.pow(0.3)
        loudness = loudness / loudness.amax(dim=-1, keepdim=True).clamp(min=eps)

        # [11] onset_strength: HWR spectral flux, max-norm
        # Half-wave rectified spectral difference
        spec_diff = mt[:, 1:, :] - mt[:, :-1, :]
        hwr = torch.relu(spec_diff).sum(dim=-1)  # (B, T-1)
        onset = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        onset[:, 1:] = hwr
        onset = onset / onset.amax(dim=-1, keepdim=True).clamp(min=eps)

        return torch.stack([
            amplitude, velocity, acceleration, loudness, onset
        ], dim=-1).clamp(0, 1)  # (B, T, 5)

    @property
    def feature_names(self):
        return ("amplitude", "velocity_A", "acceleration_A", "loudness", "onset_strength")
