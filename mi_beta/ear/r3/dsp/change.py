"""Group D: Change — 4D [21:25] temporal change features."""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


class ChangeGroup(BaseSpectralGroup):
    GROUP_NAME = "change"
    DOMAIN = "dsp"
    OUTPUT_DIM = 4

    @property
    def feature_names(self) -> List[str]:
        return [
            "spectral_flux", "distribution_entropy",
            "distribution_flatness", "distribution_concentration",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """(B, 128, T) → (B, T, 4)."""
        B, N, T = mel.shape

        # [0] spectral_flux: norm(mel[t] - mel[t-1]) normalized by max
        flux = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        if T > 1:
            diff = mel[:, :, 1:] - mel[:, :, :-1]
            flux[:, 1:] = diff.norm(dim=1)
            flux_max = flux.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
            flux = flux / flux_max

        # Probability distribution per frame
        prob = mel / mel.sum(dim=1, keepdim=True).clamp(min=1e-8)  # (B, N, T)

        # [1] distribution_entropy: -(prob * log(prob)).sum() / log(N)
        log_prob = torch.log(prob.clamp(min=1e-10))
        entropy = -(prob * log_prob).sum(dim=1) / torch.log(
            torch.tensor(float(N), device=mel.device)
        )
        entropy = entropy.clamp(0.0, 1.0)

        # [2] distribution_flatness: exp(mean(log(prob))) / mean(prob) (Wiener)
        geo_mean = torch.exp(log_prob.mean(dim=1))
        arith_mean = prob.mean(dim=1).clamp(min=1e-10)
        flatness = (geo_mean / arith_mean).clamp(0.0, 1.0)

        # [3] distribution_concentration: sum(prob^2) * N (Herfindahl)
        concentration = ((prob ** 2).sum(dim=1) * N).clamp(0.0, 1.0)

        return torch.stack([
            flux, entropy, flatness, concentration,
        ], dim=-1).clamp(0.0, 1.0)
