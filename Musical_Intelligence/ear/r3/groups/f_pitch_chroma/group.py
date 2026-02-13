from __future__ import annotations
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup


def _build_mel_center_freqs(n_mels: int = 128) -> Tensor:
    """Compute mel-scale center frequencies for n_mels bins."""
    f_min, f_max = 20.0, 8000.0
    mel_min = 2595.0 * math.log10(1.0 + f_min / 700.0)
    mel_max = 2595.0 * math.log10(1.0 + f_max / 700.0)
    mels = torch.linspace(mel_min, mel_max, n_mels)
    return 700.0 * (10.0 ** (mels / 2595.0) - 1.0)


def _build_chroma_matrix(n_mels: int = 128, sigma: float = 0.5) -> Tensor:
    """Build 128x12 Gaussian soft-assignment mel-to-chroma matrix."""
    freqs = _build_mel_center_freqs(n_mels)
    matrix = torch.zeros(n_mels, 12)

    for k in range(n_mels):
        f = freqs[k].item()
        if f < 20.0:
            continue  # unreliable bins
        # Convert to pitch class (continuous)
        midi = 12.0 * math.log2(f / 440.0) + 69.0
        pc_continuous = midi % 12.0  # [0, 12)

        for pc in range(12):
            # Circular distance
            dist = abs(pc_continuous - pc)
            dist = min(dist, 12.0 - dist)
            # Gaussian weight
            matrix[k, pc] = math.exp(-0.5 * (dist / sigma) ** 2)

    # Normalize each mel bin's weights to sum to 1
    row_sums = matrix.sum(dim=1, keepdim=True).clamp(min=1e-8)
    matrix = matrix / row_sums
    # Zero out bins where freq < 20 Hz (already zero from loop)
    return matrix


class PitchChromaGroup(BaseSpectralGroup):
    GROUP_NAME = "pitch_chroma"
    DOMAIN = "tonal"
    OUTPUT_DIM = 16
    INDEX_RANGE = (49, 65)
    STAGE = 1
    DEPENDENCIES = ()

    def __init__(self):
        super().__init__()
        self._chroma_matrix = _build_chroma_matrix()  # (128, 12)
        self._log2_freqs = torch.log2(_build_mel_center_freqs().clamp(min=1.0))  # (128,)
        self._log2_20 = math.log2(20.0)
        self._log2_22050 = math.log2(22050.0)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        chroma_mat = self._chroma_matrix.to(mt.device, mt.dtype)
        log2_freqs = self._log2_freqs.to(mt.device, mt.dtype)

        # [49-60] chroma: mel @ chroma_matrix, L1-normalize
        chroma = torch.matmul(mt, chroma_mat)  # (B, T, 12)
        chroma = chroma / chroma.sum(dim=-1, keepdim=True).clamp(min=eps)

        # [61] pitch_height: weighted mean of log2(freq), min-max normalized
        weights = mt / mt.sum(dim=-1, keepdim=True).clamp(min=eps)
        pitch_h = (weights * log2_freqs).sum(dim=-1)  # (B, T)
        pitch_height = (pitch_h - self._log2_20) / (self._log2_22050 - self._log2_20)
        pitch_height = pitch_height.clamp(0, 1)

        # [62] pitch_class_entropy: Shannon entropy of chroma / log(12)
        log_chroma = torch.log(chroma.clamp(min=eps))
        pc_entropy = -(chroma * log_chroma).sum(dim=-1) / math.log(12)
        pc_entropy = pc_entropy.clamp(0, 1)

        # [63] pitch_salience: (peak - median) / (peak + median)
        peak = mt.max(dim=-1).values
        median = mt.median(dim=-1).values
        salience = (peak - median) / (peak + median).clamp(min=eps)
        salience = salience.clamp(0, 1)

        # [64] inharmonicity_index: 1 - peak/sum
        inharm = 1.0 - peak / mt.sum(dim=-1).clamp(min=eps)
        inharm = inharm.clamp(0, 1)

        return torch.stack([
            chroma[:, :, 0], chroma[:, :, 1], chroma[:, :, 2],
            chroma[:, :, 3], chroma[:, :, 4], chroma[:, :, 5],
            chroma[:, :, 6], chroma[:, :, 7], chroma[:, :, 8],
            chroma[:, :, 9], chroma[:, :, 10], chroma[:, :, 11],
            pitch_height, pc_entropy, salience, inharm,
        ], dim=-1).clamp(0, 1)  # (B, T, 16)

    @property
    def feature_names(self):
        return (
            "chroma_C", "chroma_Db", "chroma_D", "chroma_Eb",
            "chroma_E", "chroma_F", "chroma_Gb", "chroma_G",
            "chroma_Ab", "chroma_A", "chroma_Bb", "chroma_B",
            "pitch_height", "pitch_class_entropy", "pitch_salience",
            "inharmonicity_index",
        )
