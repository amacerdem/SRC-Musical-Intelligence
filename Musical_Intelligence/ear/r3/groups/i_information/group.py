from __future__ import annotations
from typing import Dict, Optional
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

_EMA_ALPHA = 0.0029  # alpha = 1 - exp(-1 / (2.0 * 172.27))
_WARMUP_FRAMES = 344


class InformationGroup(BaseSpectralGroup):
    GROUP_NAME = "information"
    DOMAIN = "information"
    OUTPUT_DIM = 7
    INDEX_RANGE = (87, 94)
    STAGE = 3
    DEPENDENCIES = ("pitch_chroma", "rhythm_groove", "harmony")

    def __init__(self):
        super().__init__()
        self._mel_avg: Optional[Tensor] = None
        self._mel_var: Optional[Tensor] = None
        self._chroma_avg: Optional[Tensor] = None
        self._transition_counts: Optional[Tensor] = None
        self._frame_count: int = 0

    def reset(self):
        """Reset running statistics for new audio segment."""
        self._mel_avg = None
        self._mel_var = None
        self._chroma_avg = None
        self._transition_counts = None
        self._frame_count = 0

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        return torch.zeros(B, T, 7, device=mel.device, dtype=mel.dtype)

    def compute_with_deps(self, mel: Tensor, deps: Dict[str, Tensor]) -> Tensor:
        B, N, T = mel.shape
        device, dtype = mel.device, mel.dtype
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        chroma_full = deps["pitch_chroma"]  # (B, T, 16)
        chroma = chroma_full[:, :, :12]     # (B, T, 12)
        harmony = deps["harmony"]           # (B, T, 12)

        # Initialize running stats if needed
        if self._mel_avg is None:
            self._mel_avg = mt[:, 0].clone()  # (B, 128)
            self._mel_var = torch.zeros(B, N, device=device, dtype=dtype)
            self._chroma_avg = chroma[:, 0].clone()  # (B, 12)
            self._transition_counts = torch.zeros(B, 12, 12, device=device, dtype=dtype)
            self._frame_count = 0

        result = torch.zeros(B, T, 7, device=device, dtype=dtype)
        alpha = _EMA_ALPHA

        for t in range(T):
            self._frame_count += 1
            confidence = min(1.0, self._frame_count / _WARMUP_FRAMES)

            mel_t = mt[:, t]      # (B, 128)
            chroma_t = chroma[:, t]  # (B, 12)

            # Update EMA
            self._mel_avg = (1 - alpha) * self._mel_avg + alpha * mel_t
            residual = mel_t - self._mel_avg
            self._mel_var = (1 - alpha) * self._mel_var + alpha * residual.pow(2)
            self._chroma_avg = (1 - alpha) * self._chroma_avg + alpha * chroma_t

            # Update transition counts
            if t > 0:
                prev_pc = chroma[:, t-1].argmax(dim=-1)  # (B,)
                curr_pc = chroma_t.argmax(dim=-1)
                for b in range(B):
                    self._transition_counts[b, prev_pc[b], curr_pc[b]] += 1

            # [87] melodic_entropy: entropy of transition distribution
            trans_dist = self._transition_counts.sum(dim=-1)  # (B, 12)
            trans_dist = trans_dist / trans_dist.sum(dim=-1, keepdim=True).clamp(min=eps)
            melodic_ent = -(trans_dist * trans_dist.clamp(min=eps).log()).sum(dim=-1) / math.log(12)
            result[:, t, 0] = melodic_ent.clamp(0, 1) * confidence

            # [88] harmonic_entropy: KL(chroma_t || chroma_avg)
            p = chroma_t / chroma_t.sum(dim=-1, keepdim=True).clamp(min=eps)
            q = self._chroma_avg / self._chroma_avg.sum(dim=-1, keepdim=True).clamp(min=eps)
            kl = (p * (p.clamp(min=eps).log() - q.clamp(min=eps).log())).sum(dim=-1)
            result[:, t, 1] = (1.0 - torch.exp(-kl)).clamp(0, 1) * confidence

            # [89] rhythmic_information_content: from rhythm_groove deps
            # Simplified: use event_density from rhythm_groove
            result[:, t, 2] = deps["rhythm_groove"][:, t, 7] * confidence  # event_density

            # [90] spectral_surprise: KL(mel_t || mel_avg)
            p_mel = mel_t / mel_t.sum(dim=-1, keepdim=True).clamp(min=eps)
            q_mel = self._mel_avg / self._mel_avg.sum(dim=-1, keepdim=True).clamp(min=eps)
            kl_mel = (p_mel * (p_mel.clamp(min=eps).log() - q_mel.clamp(min=eps).log())).sum(dim=-1)
            result[:, t, 3] = (1.0 - torch.exp(-kl_mel)).clamp(0, 1) * confidence

            # [91] information_rate: MI(mel_t; mel_{t-1})
            if t > 0:
                mel_prev = mt[:, t-1]
                h_t = -(p_mel * p_mel.clamp(min=eps).log()).sum(dim=-1)
                p_prev = mel_prev / mel_prev.sum(dim=-1, keepdim=True).clamp(min=eps)
                h_prev = -(p_prev * p_prev.clamp(min=eps).log()).sum(dim=-1)
                p_joint = (p_mel + p_prev) / 2
                h_joint = -(p_joint * p_joint.clamp(min=eps).log()).sum(dim=-1)
                mi = (h_t + h_prev - 2 * h_joint) / math.log(128)
                result[:, t, 4] = mi.clamp(0, 1)

            # [92] predictive_entropy: 0.5 * log(2*pi*e*var) / log(128)
            var_mean = self._mel_var.mean(dim=-1).clamp(min=eps)
            pred_ent = 0.5 * torch.log(2 * math.pi * math.e * var_mean) / math.log(128)
            result[:, t, 5] = pred_ent.clamp(0, 1) * confidence

            # [93] tonal_ambiguity: entropy of key correlations
            key_clarity = harmony[:, t, 0]  # key_clarity from harmony group
            # Use 1 - key_clarity as proxy for ambiguity
            result[:, t, 6] = (1.0 - key_clarity).clamp(0, 1)

        return result.clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "melodic_entropy", "harmonic_entropy",
            "rhythmic_information_content", "spectral_surprise",
            "information_rate", "predictive_entropy", "tonal_ambiguity",
        )
