"""
R³ Group E: Cross-Layer Interactions (24D) [25:49]

"How do features relate?"

Pairwise interactions between spectral groups that capture
cross-feature coupling effects.
  x_l0l5 (8D) [25:33]: Energy × Consonance
  x_l4l5 (8D) [33:41]: Derivatives × Consonance
  x_l5l7 (8D) [41:49]: Consonance × Timbre
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSpectralGroup


class InteractionsGroup(BaseSpectralGroup):
    GROUP_NAME = "interactions"
    OUTPUT_DIM = 24
    INDEX_RANGE = (25, 49)

    @property
    def feature_names(self) -> List[str]:
        return [
            # x_l0l5: Energy × Consonance (8D)
            "x_amp_roughness", "x_amp_sethares",
            "x_amp_helmholtz", "x_amp_stumpf",
            "x_vel_roughness", "x_vel_sethares",
            "x_vel_helmholtz", "x_vel_stumpf",
            # x_l4l5: Derivatives × Consonance (8D)
            "x_flux_roughness", "x_flux_sethares",
            "x_flux_helmholtz", "x_flux_stumpf",
            "x_entropy_roughness", "x_entropy_sethares",
            "x_entropy_helmholtz", "x_entropy_stumpf",
            # x_l5l7: Consonance × Timbre (8D)
            "x_roughness_warmth", "x_roughness_sharpness",
            "x_sethares_warmth", "x_sethares_sharpness",
            "x_helmholtz_tonalness", "x_helmholtz_clarity",
            "x_stumpf_smoothness", "x_stumpf_autocorr",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute cross-layer interaction features.

        This method expects the other R³ groups to have already been computed
        and concatenated. Since we compute in order and concatenate after,
        we compute interactions directly from mel spectrogram statistics.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 24) interaction features in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)
        total_energy = mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)

        # Quick proxies for the base features we need
        # Energy proxies
        amp = mel_t.pow(2).mean(dim=-1, keepdim=True).sqrt()
        amp = amp / amp.amax(dim=1, keepdim=True).clamp(min=1e-8)

        vel = torch.zeros_like(amp)
        if T > 1:
            vel[:, 1:] = amp[:, 1:] - amp[:, :-1]
        vel = torch.sigmoid(vel * 5.0)

        # Consonance proxies
        low_q = N // 4
        high_q = 3 * N // 4
        roughness_proxy = mel_t[..., high_q:].var(dim=-1, keepdim=True)
        roughness_proxy = torch.sigmoid(roughness_proxy - 0.5)

        diff = torch.diff(mel_t, dim=-1)
        sethares_proxy = diff.abs().mean(dim=-1, keepdim=True)
        sethares_proxy = sethares_proxy / sethares_proxy.amax(dim=1, keepdim=True).clamp(min=1e-8)

        peak_e = mel_t.max(dim=-1, keepdim=True).values
        helmholtz_proxy = peak_e / total_energy

        low_ratio = mel_t[..., :low_q].sum(dim=-1, keepdim=True) / total_energy
        stumpf_proxy = low_ratio

        # Change proxies
        flux = torch.zeros(B, T, 1, device=mel.device, dtype=mel.dtype)
        if T > 1:
            flux[:, 1:] = (mel_t[:, 1:] - mel_t[:, :-1]).norm(dim=-1, keepdim=True)
        flux = flux / flux.amax(dim=1, keepdim=True).clamp(min=1e-8)

        prob = mel_t / total_energy
        prob = prob.clamp(min=1e-10)
        entropy = -(prob * prob.log()).sum(dim=-1, keepdim=True)
        entropy = entropy / torch.log(torch.tensor(N, dtype=mel.dtype, device=mel.device))

        # Timbre proxies
        warmth_proxy = mel_t[..., :low_q].sum(dim=-1, keepdim=True) / total_energy
        sharpness_proxy = mel_t[..., high_q:].sum(dim=-1, keepdim=True) / total_energy
        tonalness_proxy = helmholtz_proxy

        bin_idx = torch.arange(N, device=mel.device, dtype=mel.dtype)
        clarity_proxy = (mel_t * bin_idx).sum(dim=-1, keepdim=True) / total_energy / N

        irr = torch.diff(mel_t, dim=-1).abs().mean(dim=-1, keepdim=True)
        irr_max = irr.amax(dim=1, keepdim=True).clamp(min=1e-8)
        smoothness_proxy = 1.0 - (irr / irr_max)

        centered = mel_t - mel_t.mean(dim=-1, keepdim=True)
        norm = centered.norm(dim=-1, keepdim=True).clamp(min=1e-8)
        normalized = centered / norm
        autocorr_proxy = (normalized[..., :-1] * normalized[..., 1:]).sum(dim=-1, keepdim=True).clamp(0, 1)

        # ═══ Cross-layer products ═══

        # x_l0l5: Energy × Consonance (8D)
        x_l0l5 = torch.cat([
            amp * roughness_proxy, amp * sethares_proxy,
            amp * helmholtz_proxy, amp * stumpf_proxy,
            vel * roughness_proxy, vel * sethares_proxy,
            vel * helmholtz_proxy, vel * stumpf_proxy,
        ], dim=-1)

        # x_l4l5: Derivatives × Consonance (8D)
        x_l4l5 = torch.cat([
            flux * roughness_proxy, flux * sethares_proxy,
            flux * helmholtz_proxy, flux * stumpf_proxy,
            entropy * roughness_proxy, entropy * sethares_proxy,
            entropy * helmholtz_proxy, entropy * stumpf_proxy,
        ], dim=-1)

        # x_l5l7: Consonance × Timbre (8D)
        x_l5l7 = torch.cat([
            roughness_proxy * warmth_proxy, roughness_proxy * sharpness_proxy,
            sethares_proxy * warmth_proxy, sethares_proxy * sharpness_proxy,
            helmholtz_proxy * tonalness_proxy, helmholtz_proxy * clarity_proxy,
            stumpf_proxy * smoothness_proxy, stumpf_proxy * autocorr_proxy,
        ], dim=-1)

        features = torch.cat([x_l0l5, x_l4l5, x_l5l7], dim=-1)  # (B, T, 24)
        return features.clamp(0, 1)
