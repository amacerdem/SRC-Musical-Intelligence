from __future__ import annotations
from typing import Dict, List
import math
import torch
from torch import Tensor
import torch.nn.functional as F
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

_FRAME_RATE = 172.27
_LAG_MIN = 34   # 300 BPM
_LAG_MAX = 344  # 30 BPM
_PEAK_THRESHOLD = 0.3
_WIN_FRAMES = 2 * _LAG_MAX    # ~688 frames ≈ 4 s  (full BPM range)
_HOP_FRAMES = _WIN_FRAMES // 8  # ~86 frames ≈ 0.5 s analysis hop


class RhythmGrooveGroup(BaseSpectralGroup):
    GROUP_NAME = "rhythm_groove"
    DOMAIN = "temporal"
    OUTPUT_DIM = 10
    INDEX_RANGE = (41, 51)
    STAGE = 2
    DEPENDENCIES = ("energy",)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
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

    # ── per-window feature extraction ────────────────────────────────

    def _window_features(self, onset: Tensor, mel: Tensor) -> Tensor:
        """Compute 10 rhythm features for a single analysis window.

        onset : (B, W)
        mel   : (B, N, W)
        Returns: (B, 10)
        """
        B, W = onset.shape
        device, dtype = onset.device, onset.dtype
        eps = 1e-8
        out = torch.zeros(B, 10, device=device, dtype=dtype)

        if W < _LAG_MIN + 1:
            return out

        # Onset autocorrelation (Wiener-Khinchin)
        oenv = onset - onset.mean(dim=-1, keepdim=True)
        fft_size = 1
        while fft_size < 2 * W:
            fft_size *= 2
        O = torch.fft.rfft(oenv, n=fft_size, dim=-1)
        R = torch.fft.irfft(O * O.conj(), n=fft_size, dim=-1)[:, :W]
        R0 = R[:, 0:1].clamp(min=eps)
        R = R / R0

        lag_end = min(_LAG_MAX + 1, W)
        R_search = R[:, _LAG_MIN:lag_end]
        if R_search.shape[1] == 0:
            return out

        best_lag_offset = R_search.argmax(dim=-1)
        best_lag = best_lag_offset + _LAG_MIN
        bpm = _FRAME_RATE * 60.0 / best_lag.float().clamp(min=1)
        tempo = ((bpm - 30.0) / 270.0).clamp(0, 1)

        beat_str = torch.zeros(B, device=device, dtype=dtype)
        syncopation = torch.zeros(B, device=device, dtype=dtype)
        metricality = torch.zeros(B, device=device, dtype=dtype)
        isochrony = torch.zeros(B, device=device, dtype=dtype)
        event_density = torch.zeros(B, device=device, dtype=dtype)
        regularity = torch.zeros(B, device=device, dtype=dtype)

        for b in range(B):
            lag = best_lag[b].item()

            # beat_strength
            if lag < W:
                beat_str[b] = R[b, lag].clamp(0, 1)

            # syncopation
            if lag >= 2:
                peaks_mask = (onset[b, 1:-1] > onset[b, :-2]) & (onset[b, 1:-1] > onset[b, 2:])
                peaks_mask = peaks_mask & (onset[b, 1:-1] > _PEAK_THRESHOLD)
                peak_pos = peaks_mask.nonzero(as_tuple=True)[0] + 1
                if len(peak_pos) > 0:
                    off = ((peak_pos.float() % lag) > lag * 0.25) & \
                          ((peak_pos.float() % lag) < lag * 0.75)
                    syncopation[b] = off.float().mean()

                # isochrony + regularity from IOI
                if len(peak_pos) > 2:
                    ioi = (peak_pos[1:] - peak_pos[:-1]).float()
                    if len(ioi) > 1:
                        npvi = 200.0 * ((ioi[1:] - ioi[:-1]).abs() / ((ioi[1:] + ioi[:-1]) / 2 + eps)).mean()
                        isochrony[b] = (1.0 - npvi / 200.0).clamp(0, 1)
                    hist = torch.histc(ioi, bins=16, min=1, max=_LAG_MAX)
                    p = hist / hist.sum().clamp(min=eps)
                    p = p.clamp(min=eps)
                    ent = -(p * p.log()).sum() / math.log(16)
                    regularity[b] = (1.0 - ent).clamp(0, 1)

            # event_density
            n_events = (onset[b] > _PEAK_THRESHOLD).float().sum()
            dur_s = W / _FRAME_RATE
            event_density[b] = (n_events / dur_s / 20.0).clamp(0, 1)

            # metricality
            count = 0
            for mult in [0.5, 1.0, 2.0, 3.0, 4.0, 6.0]:
                check_lag = int(lag * mult)
                if 0 < check_lag < W:
                    if R[b, check_lag] > _PEAK_THRESHOLD:
                        count += 1
            metricality[b] = count / 6.0

        # pulse_clarity
        R_median = R_search.median(dim=-1).values.clamp(min=eps)
        pulse_clarity = torch.sigmoid(beat_str / R_median - 1.0)

        # groove_index
        mt = mel.transpose(1, 2)
        bass_energy = mt[:, :, :16].sum(dim=-1).mean(dim=-1)
        bass_energy = bass_energy / bass_energy.max().clamp(min=eps)
        groove = syncopation * bass_energy * pulse_clarity
        g_max = groove.max().clamp(min=eps)
        groove = groove / g_max if g_max > eps else groove

        out[:, 0] = tempo
        out[:, 1] = beat_str
        out[:, 2] = pulse_clarity
        out[:, 3] = syncopation
        out[:, 4] = metricality
        out[:, 5] = isochrony
        out[:, 6] = groove
        out[:, 7] = event_density
        # 8 = tempo_stability (filled across windows in _compute_from_onset)
        out[:, 9] = regularity
        return out

    # ── sliding-window → per-frame output ────────────────────────────

    def _compute_from_onset(self, onset: Tensor, mel: Tensor) -> Tensor:
        B, T = onset.shape
        device, dtype = onset.device, onset.dtype

        if T < _LAG_MIN + 1:
            return torch.zeros(B, T, 10, device=device, dtype=dtype)

        # Window / hop (shrink window if track is shorter than default)
        win = min(_WIN_FRAMES, T)
        hop = max(1, min(_HOP_FRAMES, (T - win) // 2 + 1)) if T > win else 1

        # Build analysis-point centers
        centers: List[int] = []
        start = 0
        while start + win <= T:
            centers.append(start + win // 2)
            start += hop
        if not centers:                    # track shorter than one window
            centers.append(T // 2)
            win = T

        n_pts = len(centers)
        feats = torch.zeros(B, n_pts, 10, device=device, dtype=dtype)

        for i, c in enumerate(centers):
            s = max(0, c - win // 2)
            e = s + win
            if e > T:
                e = T
                s = max(0, e - win)
            feats[:, i, :] = self._window_features(onset[:, s:e], mel[:, :, s:e])

        # ── tempo_stability: 1 − CV(local_tempo) over 3-window neighborhood
        if n_pts >= 3:
            tempo_vals = feats[:, :, 0]                        # (B, n_pts)
            padded = F.pad(tempo_vals, (1, 1), mode='replicate')
            stacked = padded.unfold(1, 3, 1)                   # (B, n_pts, 3)
            local_mean = stacked.mean(dim=-1).clamp(min=1e-8)
            local_std = stacked.std(dim=-1)
            cv = local_std / local_mean
            feats[:, :, 8] = (1.0 - cv).clamp(0, 1)
        else:
            feats[:, :, 8] = 1.0

        # ── interpolate to full frame resolution (B, T, 10) ─────────
        if n_pts == 1:
            result = feats.expand(B, T, 10).contiguous()
        else:
            result = F.interpolate(
                feats.permute(0, 2, 1),     # (B, 10, n_pts)
                size=T,
                mode='linear',
                align_corners=True,
            ).permute(0, 2, 1)              # (B, T, 10)

        return result.clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "tempo_estimate", "beat_strength", "pulse_clarity",
            "syncopation_index", "metricality_index", "isochrony_nPVI",
            "groove_index", "event_density", "tempo_stability",
            "rhythmic_regularity",
        )
