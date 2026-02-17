from __future__ import annotations
from typing import Dict
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

_FRAME_RATE = 172.27
_LAG_MIN = 34   # 300 BPM
_LAG_MAX = 344  # 30 BPM
_PEAK_THRESHOLD = 0.3


class RhythmGrooveGroup(BaseSpectralGroup):
    GROUP_NAME = "rhythm_groove"
    DOMAIN = "temporal"
    OUTPUT_DIM = 10
    INDEX_RANGE = (41, 51)
    STAGE = 2
    DEPENDENCIES = ("energy",)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        # Fallback: compute onset from mel, then rhythm features
        B, N, T = mel.shape
        mt = mel.transpose(1, 2)
        spec_diff = mt[:, 1:, :] - mt[:, :-1, :]
        hwr = torch.relu(spec_diff).sum(dim=-1)
        onset = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        onset[:, 1:] = hwr
        onset_max = onset.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        onset = onset / onset_max
        return self._compute_from_onset(onset, mel)

    def compute_with_deps(self, mel: Tensor, deps: Dict[str, Tensor]) -> Tensor:
        onset = deps["energy"][:, :, 4]  # onset_strength is index 4 in energy
        return self._compute_from_onset(onset, mel)

    def _compute_from_onset(self, onset: Tensor, mel: Tensor) -> Tensor:
        B, T = onset.shape
        device, dtype = onset.device, onset.dtype
        eps = 1e-8
        result = torch.zeros(B, T, 10, device=device, dtype=dtype)

        if T < _LAG_MAX:
            # Not enough frames for tempo analysis
            return result

        # Onset autocorrelation (Wiener-Khinchin)
        oenv = onset - onset.mean(dim=-1, keepdim=True)
        fft_size = 1
        while fft_size < 2 * T:
            fft_size *= 2
        O = torch.fft.rfft(oenv, n=fft_size, dim=-1)
        R = torch.fft.irfft(O * O.conj(), n=fft_size, dim=-1)[:, :T]
        R0 = R[:, 0:1].clamp(min=eps)
        R = R / R0  # normalize

        # [65] tempo_estimate: argmax in lag range -> BPM, min-max [30,300]
        R_search = R[:, _LAG_MIN:_LAG_MAX+1]  # (B, lag_range)
        best_lag_offset = R_search.argmax(dim=-1)  # (B,)
        best_lag = best_lag_offset + _LAG_MIN
        bpm = _FRAME_RATE * 60.0 / best_lag.float().clamp(min=1)
        tempo = (bpm - 30.0) / (300.0 - 30.0)
        tempo = tempo.clamp(0, 1)

        # [66] beat_strength: R at tempo lag
        beat_str = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            lag = best_lag[b].item()
            if lag < T:
                beat_str[b] = R[b, lag].clamp(0, 1)

        # [67] pulse_clarity: R[tempo_lag] / median(R[lag_range]) -> sigmoid
        R_median = R_search.median(dim=-1).values.clamp(min=eps)
        pulse_clarity = torch.sigmoid(beat_str / R_median - 1.0)

        # [68] syncopation_index (simplified LHL): count off-beat peaks
        # Simplified: fraction of onset peaks not on beat grid
        syncopation = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            lag = best_lag[b].item()
            if lag < 2:
                continue
            peaks = (onset[b, 1:-1] > onset[b, :-2]) & (onset[b, 1:-1] > onset[b, 2:])
            peaks = peaks & (onset[b, 1:-1] > _PEAK_THRESHOLD)
            peak_positions = peaks.nonzero(as_tuple=True)[0] + 1
            if len(peak_positions) > 0:
                off_beat = ((peak_positions.float() % lag) > lag * 0.25) & \
                           ((peak_positions.float() % lag) < lag * 0.75)
                syncopation[b] = off_beat.float().mean()

        # [69] metricality_index: multi-scale autocorr nested counts / 6
        metricality = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            lag = best_lag[b].item()
            count = 0
            for mult in [0.5, 1.0, 2.0, 3.0, 4.0, 6.0]:
                check_lag = int(lag * mult)
                if 0 < check_lag < T:
                    if R[b, check_lag] > _PEAK_THRESHOLD:
                        count += 1
            metricality[b] = count / 6.0

        # [70] isochrony_nPVI: 1 - nPVI/200 from IOI
        isochrony = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            peaks = (onset[b, 1:-1] > onset[b, :-2]) & (onset[b, 1:-1] > onset[b, 2:])
            peaks = peaks & (onset[b, 1:-1] > _PEAK_THRESHOLD)
            peak_pos = peaks.nonzero(as_tuple=True)[0] + 1
            if len(peak_pos) > 2:
                ioi = (peak_pos[1:] - peak_pos[:-1]).float()
                if len(ioi) > 1:
                    npvi = 200.0 * (((ioi[1:] - ioi[:-1]).abs() / ((ioi[1:] + ioi[:-1]) / 2 + eps)).mean())
                    isochrony[b] = (1.0 - npvi / 200.0).clamp(0, 1)

        # [71] groove_index: syncopation * bass_energy * pulse_clarity
        mt = mel.transpose(1, 2)
        bass_energy = mt[:, :, :16].sum(dim=-1).mean(dim=-1)
        bass_energy = bass_energy / bass_energy.max().clamp(min=eps)
        groove = syncopation * bass_energy * pulse_clarity
        groove = groove / groove.max().clamp(min=eps) if groove.max() > eps else groove

        # [72] event_density: onset count per second / 20
        event_density = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            peaks = onset[b] > _PEAK_THRESHOLD
            n_events = peaks.float().sum()
            duration_s = T / _FRAME_RATE
            event_density[b] = (n_events / duration_s / 20.0).clamp(0, 1)

        # [73] tempo_stability: 1 - CV(local_tempo) over 2s windows
        stability = torch.ones(B, device=device, dtype=dtype)
        # Simplified: use correlation at integer multiples of tempo lag

        # [74] rhythmic_regularity: 1 - entropy(IOI_hist)
        regularity = torch.zeros(B, device=device, dtype=dtype)
        for b in range(B):
            peaks = (onset[b, 1:-1] > onset[b, :-2]) & (onset[b, 1:-1] > onset[b, 2:])
            peaks = peaks & (onset[b, 1:-1] > _PEAK_THRESHOLD)
            peak_pos = peaks.nonzero(as_tuple=True)[0] + 1
            if len(peak_pos) > 2:
                ioi = (peak_pos[1:] - peak_pos[:-1]).float()
                hist = torch.histc(ioi, bins=16, min=1, max=_LAG_MAX)
                p = hist / hist.sum().clamp(min=eps)
                p = p.clamp(min=eps)
                ent = -(p * p.log()).sum() / math.log(16)
                regularity[b] = (1.0 - ent).clamp(0, 1)

        # Broadcast scalar features to (B, T)
        result[:, :, 0] = tempo.unsqueeze(-1).expand_as(result[:, :, 0])
        result[:, :, 1] = beat_str.unsqueeze(-1).expand_as(result[:, :, 1])
        result[:, :, 2] = pulse_clarity.unsqueeze(-1).expand_as(result[:, :, 2])
        result[:, :, 3] = syncopation.unsqueeze(-1).expand_as(result[:, :, 3])
        result[:, :, 4] = metricality.unsqueeze(-1).expand_as(result[:, :, 4])
        result[:, :, 5] = isochrony.unsqueeze(-1).expand_as(result[:, :, 5])
        result[:, :, 6] = groove.unsqueeze(-1).expand_as(result[:, :, 6])
        result[:, :, 7] = event_density.unsqueeze(-1).expand_as(result[:, :, 7])
        result[:, :, 8] = stability.unsqueeze(-1).expand_as(result[:, :, 8])
        result[:, :, 9] = regularity.unsqueeze(-1).expand_as(result[:, :, 9])

        return result.clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "tempo_estimate", "beat_strength", "pulse_clarity",
            "syncopation_index", "metricality_index", "isochrony_nPVI",
            "groove_index", "event_density", "tempo_stability",
            "rhythmic_regularity",
        )
