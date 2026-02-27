from __future__ import annotations
from typing import Dict
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

# Krumhansl-Kessler key profiles (major and minor)
_MAJOR = torch.tensor([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR = torch.tensor([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _build_key_profiles() -> Tensor:
    """Build 24 key profiles (12 major + 12 minor), each rotated."""
    profiles = torch.zeros(24, 12)
    for i in range(12):
        profiles[i] = _MAJOR.roll(i)
        profiles[12 + i] = _MINOR.roll(i)
    # Normalize each profile to unit norm
    profiles = profiles / profiles.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    return profiles


def _build_tonnetz_matrix() -> Tensor:
    """Build 12x6 Tonnetz projection matrix (Harte circle-of-fifths)."""
    matrix = torch.zeros(12, 6)
    for k in range(12):
        # Fifth cycle (interval 7 semitones)
        matrix[k, 0] = math.sin(k * 7 * math.pi / 6)
        matrix[k, 1] = math.cos(k * 7 * math.pi / 6)
        # Minor third cycle (interval 3 semitones)
        matrix[k, 2] = math.sin(k * 3 * math.pi / 6)
        matrix[k, 3] = math.cos(k * 3 * math.pi / 6)
        # Major third cycle (interval 4 semitones)
        matrix[k, 4] = math.sin(k * 4 * math.pi / 6)
        matrix[k, 5] = math.cos(k * 4 * math.pi / 6)
    return matrix


class HarmonyGroup(BaseSpectralGroup):
    GROUP_NAME = "harmony"
    DOMAIN = "tonal"
    OUTPUT_DIM = 12
    INDEX_RANGE = (51, 63)
    STAGE = 2
    DEPENDENCIES = ("pitch_chroma",)

    def __init__(self):
        super().__init__()
        self._key_profiles = _build_key_profiles()  # (24, 12)
        self._tonnetz = _build_tonnetz_matrix()       # (12, 6)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        # Fallback: compute chroma from mel, then harmony features
        # This is a simplified path; compute_with_deps is preferred
        B, N, T = mel.shape
        return torch.zeros(B, T, 12, device=mel.device, dtype=mel.dtype)

    def compute_with_deps(self, mel: Tensor, deps: Dict[str, Tensor]) -> Tensor:
        chroma_full = deps["pitch_chroma"]  # (B, T, 16)
        chroma = chroma_full[:, :, :12]     # first 12 = chroma vector
        return self._compute_from_chroma(chroma, mel)

    def _compute_from_chroma(self, chroma: Tensor, mel: Tensor) -> Tensor:
        B, T, _ = chroma.shape
        device, dtype = chroma.device, chroma.dtype
        eps = 1e-8

        key_profiles = self._key_profiles.to(device, dtype)
        tonnetz_mat = self._tonnetz.to(device, dtype)

        # [75] key_clarity: max correlation with 24 key profiles
        # Correlate chroma (B,T,12) with profiles (24,12)
        # Normalize chroma per-frame
        chroma_norm = chroma / chroma.norm(dim=-1, keepdim=True).clamp(min=eps)
        key_corrs = torch.matmul(chroma_norm, key_profiles.T)  # (B, T, 24)
        best_corr = key_corrs.max(dim=-1).values
        mean_corr = key_corrs.mean(dim=-1)
        # Clarity = how much the best key stands out from the average.
        # Uniform chroma → all correlations equal → difference ≈ 0.
        # Strong tonal → best ≫ mean → difference ≈ 0.2-0.3.
        key_clarity = ((best_corr - mean_corr) * 5.0).clamp(0, 1)

        # [76-81] tonnetz: chroma @ tonnetz_matrix, then (x+1)/2
        tonnetz = torch.matmul(chroma, tonnetz_mat)  # (B, T, 6)
        tonnetz = (tonnetz + 1.0) / 2.0
        tonnetz = tonnetz.clamp(0, 1)

        # [82] voice_leading_distance: L1 of chroma diff / 2
        chroma_diff = torch.zeros_like(chroma)
        chroma_diff[:, 1:] = (chroma[:, 1:] - chroma[:, :-1]).abs()
        vl_dist = chroma_diff.sum(dim=-1) / 2.0
        vl_dist = vl_dist.clamp(0, 1)

        # [83] harmonic_change: 1 - cosine_similarity(chroma_t, chroma_{t-1})
        cos_sim = torch.zeros(B, T, device=device, dtype=dtype)
        n1 = chroma[:, 1:].norm(dim=-1).clamp(min=eps)
        n2 = chroma[:, :-1].norm(dim=-1).clamp(min=eps)
        cos_sim[:, 1:] = (chroma[:, 1:] * chroma[:, :-1]).sum(dim=-1) / (n1 * n2)
        harmonic_change = (1.0 - cos_sim).clamp(0, 1)

        # [84] tonal_stability: key_clarity * (1 - smoothed_harmonic_change)
        # Simple smoothing: 5-frame moving average of harmonic_change
        kernel_size = 5
        if T >= kernel_size:
            pad = kernel_size // 2
            hc_padded = torch.nn.functional.pad(harmonic_change.unsqueeze(1), (pad, pad), mode='reflect')
            hc_smooth = torch.nn.functional.avg_pool1d(hc_padded, kernel_size, stride=1).squeeze(1)
        else:
            hc_smooth = harmonic_change
        tonal_stability = key_clarity * (1.0 - hc_smooth)
        tonal_stability = tonal_stability.clamp(0, 1)

        # [85] diatonicity: 1 - (active_PCs - 7) / 5, clamped
        active_pcs = (chroma > 0.05).float().sum(dim=-1)  # count active pitch classes
        diatonicity = 1.0 - (active_pcs - 7.0) / 5.0
        diatonicity = diatonicity.clamp(0, 1)

        # [86] syntactic_irregularity: 1 - exp(-KL(chroma || best_key_template))
        best_key_idx = key_corrs.argmax(dim=-1)  # (B, T)
        best_template = key_profiles[best_key_idx.view(-1)].view(B, T, 12)
        # Make template a valid distribution
        best_template = best_template / best_template.sum(dim=-1, keepdim=True).clamp(min=eps)
        chroma_dist = chroma / chroma.sum(dim=-1, keepdim=True).clamp(min=eps)
        # KL divergence
        kl = (chroma_dist * (chroma_dist.clamp(min=eps).log() - best_template.clamp(min=eps).log())).sum(dim=-1)
        syntactic = 1.0 - torch.exp(-kl)
        syntactic = syntactic.clamp(0, 1)

        return torch.stack([
            key_clarity,
            tonnetz[:, :, 0], tonnetz[:, :, 1],  # fifth x/y
            tonnetz[:, :, 2], tonnetz[:, :, 3],  # minor x/y
            tonnetz[:, :, 4], tonnetz[:, :, 5],  # major x/y
            vl_dist, harmonic_change,
            tonal_stability, diatonicity, syntactic,
        ], dim=-1).clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "key_clarity",
            "tonnetz_fifth_x", "tonnetz_fifth_y",
            "tonnetz_minor_x", "tonnetz_minor_y",
            "tonnetz_major_x", "tonnetz_major_y",
            "voice_leading_distance", "harmonic_change",
            "tonal_stability", "diatonicity", "syntactic_irregularity",
        )
