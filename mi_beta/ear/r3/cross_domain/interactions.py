"""Group E: Interactions — 24D [25:49] cross-domain product features."""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


class InteractionsGroup(BaseSpectralGroup):
    GROUP_NAME = "interactions"
    DOMAIN = "cross_domain"
    OUTPUT_DIM = 24

    @property
    def feature_names(self) -> List[str]:
        return [
            # Block 1: Energy × Consonance (8D)
            "x_amp_roughness", "x_amp_sethares", "x_amp_helmholtz", "x_amp_stumpf",
            "x_vel_roughness", "x_vel_sethares", "x_vel_helmholtz", "x_vel_stumpf",
            # Block 2: Change × Consonance (8D)
            "x_flux_roughness", "x_flux_sethares", "x_flux_helmholtz", "x_flux_stumpf",
            "x_entropy_roughness", "x_entropy_sethares", "x_entropy_helmholtz", "x_entropy_stumpf",
            # Block 3: Consonance × Timbre (8D)
            "x_roughness_warmth", "x_roughness_sharpness",
            "x_sethares_warmth", "x_sethares_sharpness",
            "x_helmholtz_tonalness", "x_helmholtz_clarity",
            "x_stumpf_smoothness", "x_stumpf_autocorr",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """(B, 128, T) → (B, T, 24).

        Requires prior groups to have been computed and cached.
        This implementation computes proxy features directly from mel.
        """
        B, N, T = mel.shape
        half = N // 2
        quarter = N // 4
        third = N // 3
        total = mel.sum(dim=1).clamp(min=1e-8)

        # ── Consonance proxies ──
        high = mel[:, half:, :]
        roughness = torch.sigmoid(high.var(dim=1) / high.mean(dim=1).clamp(min=1e-8) - 0.5)
        diff_adj = (mel[:, 1:, :] - mel[:, :-1, :]).abs().mean(dim=1)
        sethares = (diff_adj / mel.max(dim=1).values.clamp(min=1e-8)).clamp(0, 1)
        mean_mel = mel.mean(dim=1, keepdim=True)
        centered = mel - mean_mel
        auto = (centered[:, :-1, :] * centered[:, 1:, :]).mean(dim=1)
        var = (centered ** 2).mean(dim=1).clamp(min=1e-8)
        helmholtz = (auto / var).clamp(0, 1)
        stumpf = (mel[:, :half, :].sum(dim=1) / total).clamp(0, 1)

        # ── Energy proxies ──
        amp = torch.sqrt((mel ** 2).mean(dim=1))
        amp_max = amp.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        amplitude = amp / amp_max
        vel = torch.zeros_like(amplitude)
        vel[:, 1:] = amplitude[:, 1:] - amplitude[:, :-1]
        velocity = torch.sigmoid(5.0 * vel)

        # ── Change proxies ──
        flux = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        if T > 1:
            d = mel[:, :, 1:] - mel[:, :, :-1]
            flux[:, 1:] = d.norm(dim=1)
            fm = flux.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
            flux = flux / fm
        prob = mel / mel.sum(dim=1, keepdim=True).clamp(min=1e-8)
        log_prob = torch.log(prob.clamp(min=1e-10))
        entropy = -(prob * log_prob).sum(dim=1) / torch.log(torch.tensor(float(N), device=mel.device))
        entropy = entropy.clamp(0, 1)

        # ── Timbre proxies ──
        warmth = mel[:, :quarter, :].sum(dim=1) / total
        sharpness = mel[:, 3 * quarter:, :].sum(dim=1) / total
        tonalness = mel.max(dim=1).values / total
        bin_idx = torch.arange(N, device=mel.device, dtype=mel.dtype).view(1, N, 1)
        clarity = (mel * bin_idx).sum(dim=1) / total / N
        mel_d = (mel[:, 1:, :] - mel[:, :-1, :]).abs()
        smoothness = 1.0 - mel_d.mean(dim=1) / mel_d.max(dim=1).values.clamp(min=1e-8)
        autocorr = helmholtz  # same computation

        # ── Block 1: Energy × Consonance (8D) ──
        b1 = torch.stack([
            amplitude * roughness, amplitude * sethares,
            amplitude * helmholtz, amplitude * stumpf,
            velocity * roughness, velocity * sethares,
            velocity * helmholtz, velocity * stumpf,
        ], dim=-1)

        # ── Block 2: Change × Consonance (8D) ──
        b2 = torch.stack([
            flux * roughness, flux * sethares,
            flux * helmholtz, flux * stumpf,
            entropy * roughness, entropy * sethares,
            entropy * helmholtz, entropy * stumpf,
        ], dim=-1)

        # ── Block 3: Consonance × Timbre (8D) ──
        b3 = torch.stack([
            roughness * warmth, roughness * sharpness,
            sethares * warmth, sethares * sharpness,
            helmholtz * tonalness, helmholtz * clarity,
            stumpf * smoothness, stumpf * autocorr,
        ], dim=-1)

        return torch.cat([b1, b2, b3], dim=-1).clamp(0.0, 1.0)
