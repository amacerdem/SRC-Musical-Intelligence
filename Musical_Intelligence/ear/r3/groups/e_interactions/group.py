from __future__ import annotations
from typing import Dict
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup


class InteractionsGroup(BaseSpectralGroup):
    GROUP_NAME = "interactions"
    DOMAIN = "cross_domain"
    OUTPUT_DIM = 24
    INDEX_RANGE = (25, 49)
    STAGE = 2
    DEPENDENCIES = ("consonance", "energy", "timbre", "change")

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        # Fallback: compute proxy features from mel directly
        # This path is used when deps are not available
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)
        total = mt.sum(dim=-1).clamp(min=eps)
        quarter = N // 4

        # Proxy base features
        # Roughness proxy
        mel_high = mt[:, :, 3*quarter:]
        roughness = torch.sigmoid(mel_high.var(dim=-1) / mt.mean(dim=-1).clamp(min=eps) - 0.5)

        # Sethares proxy
        spec_diff = torch.diff(mt, dim=-1)
        sethares = spec_diff.abs().mean(dim=-1)
        sethares = sethares / sethares.amax(dim=-1, keepdim=True).clamp(min=eps)

        # Helmholtz proxy (NOTE: known mismatch - uses tonalness, not autocorr)
        helmholtz_proxy = mt.max(dim=-1).values / total

        # Stumpf proxy
        stumpf = mt[:, :, :quarter].sum(dim=-1) / total

        # Amplitude proxy
        amplitude = mt.pow(2).mean(dim=-1).sqrt()
        amplitude = amplitude / amplitude.amax(dim=-1, keepdim=True).clamp(min=eps)

        # Velocity proxy
        amp_raw = mt.pow(2).mean(dim=-1).sqrt()
        diff1 = torch.zeros_like(amp_raw)
        diff1[:, 1:] = amp_raw[:, 1:] - amp_raw[:, :-1]
        velocity = torch.sigmoid(diff1 * 5.0)

        # Flux proxy
        frame_diff = mt[:, 1:, :] - mt[:, :-1, :]
        flux_vals = frame_diff.pow(2).sum(dim=-1).sqrt()
        flux = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        flux[:, 1:] = flux_vals
        flux = flux / flux.amax(dim=-1, keepdim=True).clamp(min=eps)

        # Entropy proxy
        p = mt.clamp(min=eps)
        p = p / p.sum(dim=-1, keepdim=True)
        entropy = -(p * torch.log(p)).sum(dim=-1) / torch.log(torch.tensor(128.0, device=mel.device))

        # Warmth/sharpness/tonalness/clarity/smoothness/autocorr proxies
        warmth = mt[:, :, :quarter].sum(dim=-1) / total
        sharpness = mt[:, :, 3*quarter:].sum(dim=-1) / total
        tonalness = mt.max(dim=-1).values / total
        bins = torch.arange(N, device=mel.device, dtype=mel.dtype)
        clarity = (mt * bins).sum(dim=-1) / total / N
        smoothness = 1.0 - sethares
        m1 = mt[:, :, :-1]; m2 = mt[:, :, 1:]
        m1c = m1 - m1.mean(dim=-1, keepdim=True)
        m2c = m2 - m2.mean(dim=-1, keepdim=True)
        num = (m1c * m2c).sum(dim=-1)
        den = (m1c.pow(2).sum(dim=-1) * m2c.pow(2).sum(dim=-1)).sqrt().clamp(min=eps)
        autocorr = (num / den).clamp(0, 1)

        # Block 1: Energy x Consonance [25:32]
        f25 = amplitude * roughness
        f26 = amplitude * sethares
        f27 = amplitude * helmholtz_proxy
        f28 = amplitude * stumpf
        f29 = velocity * roughness
        f30 = velocity * sethares
        f31 = velocity * helmholtz_proxy
        f32 = velocity * stumpf

        # Block 2: Change x Consonance [33:40]
        f33 = flux * roughness
        f34 = flux * sethares
        f35 = flux * helmholtz_proxy
        f36 = flux * stumpf
        f37 = entropy * roughness
        f38 = entropy * sethares
        f39 = entropy * helmholtz_proxy
        f40 = entropy * stumpf

        # Block 3: Consonance x Timbre [41:48]
        f41 = roughness * warmth
        f42 = roughness * sharpness
        f43 = sethares * warmth
        f44 = sethares * sharpness
        f45 = helmholtz_proxy * tonalness
        f46 = helmholtz_proxy * clarity
        f47 = stumpf * smoothness
        f48 = stumpf * autocorr

        return torch.stack([
            f25, f26, f27, f28, f29, f30, f31, f32,
            f33, f34, f35, f36, f37, f38, f39, f40,
            f41, f42, f43, f44, f45, f46, f47, f48,
        ], dim=-1).clamp(0, 1)

    def compute_with_deps(self, mel: Tensor, deps: Dict[str, Tensor]) -> Tensor:
        """Compute using actual group outputs (preferred path)."""
        B, N, T = mel.shape

        # Extract features from dependency outputs
        con = deps["consonance"]   # (B, T, 7)
        ene = deps["energy"]       # (B, T, 5)
        tim = deps["timbre"]       # (B, T, 9)
        cha = deps["change"]       # (B, T, 4)

        # Base features
        roughness = con[:, :, 0]
        sethares = con[:, :, 1]
        helmholtz = con[:, :, 2]
        stumpf = con[:, :, 3]
        amplitude = ene[:, :, 0]
        velocity = ene[:, :, 1]
        flux = cha[:, :, 0]
        entropy = cha[:, :, 1]
        warmth = tim[:, :, 0]
        sharpness = tim[:, :, 1]
        tonalness = tim[:, :, 2]
        clarity = tim[:, :, 3]
        smoothness = tim[:, :, 4]
        autocorr = tim[:, :, 5]

        # Block 1: Energy x Consonance [25:32]
        f25 = amplitude * roughness
        f26 = amplitude * sethares
        f27 = amplitude * helmholtz
        f28 = amplitude * stumpf
        f29 = velocity * roughness
        f30 = velocity * sethares
        f31 = velocity * helmholtz
        f32 = velocity * stumpf

        # Block 2: Change x Consonance [33:40]
        f33 = flux * roughness
        f34 = flux * sethares
        f35 = flux * helmholtz
        f36 = flux * stumpf
        f37 = entropy * roughness
        f38 = entropy * sethares
        f39 = entropy * helmholtz
        f40 = entropy * stumpf

        # Block 3: Consonance x Timbre [41:48]
        f41 = roughness * warmth
        f42 = roughness * sharpness
        f43 = sethares * warmth
        f44 = sethares * sharpness
        f45 = helmholtz * tonalness
        f46 = helmholtz * clarity
        f47 = stumpf * smoothness
        f48 = stumpf * autocorr

        return torch.stack([
            f25, f26, f27, f28, f29, f30, f31, f32,
            f33, f34, f35, f36, f37, f38, f39, f40,
            f41, f42, f43, f44, f45, f46, f47, f48,
        ], dim=-1).clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "amp_x_roughness", "amp_x_sethares", "amp_x_helmholtz", "amp_x_stumpf",
            "vel_x_roughness", "vel_x_sethares", "vel_x_helmholtz", "vel_x_stumpf",
            "flux_x_roughness", "flux_x_sethares", "flux_x_helmholtz", "flux_x_stumpf",
            "ent_x_roughness", "ent_x_sethares", "ent_x_helmholtz", "ent_x_stumpf",
            "rough_x_warmth", "rough_x_sharpness", "seth_x_warmth", "seth_x_sharpness",
            "helm_x_tonalness", "helm_x_clarity", "stumpf_x_smoothness", "stumpf_x_autocorr",
        )
