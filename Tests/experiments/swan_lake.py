#!/usr/bin/env python3
"""Swan Lake Cognitive Analysis Experiment.

Analyzes 30 seconds of Tchaikovsky's Swan Lake through the full MI pipeline,
producing a comprehensive cognitive profile report.

Pipeline stages:
    1. Audio loading and mel spectrogram
    2. R3 spectral feature extraction (128D)
    3. H3 temporal morphology extraction (sparse)
    4. Brain forward pass (1006D)

Analysis:
    - R3 temporal dynamics per group
    - H3 feature sampling at key musical moments
    - Brain cognitive profile per unit over time
    - Peak/trough detection in cognitive activity
    - Inter-unit correlation matrix
    - Musical event detection (energy, timbre, tempo changes)

Output: Tests/reports/swan_lake_report.txt

Usage:
    python Tests/experiments/swan_lake.py
"""
from __future__ import annotations

import os
import sys
import time
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch
from torch import Tensor

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain import BrainOrchestrator
from Musical_Intelligence.brain.orchestrator import UNIT_ORDER, TOTAL_DIM
from Musical_Intelligence.ear.r3.constants import (
    R3_GROUP_BOUNDARIES,
    R3_FEATURE_NAMES,
    R3_DIM,
)
from Musical_Intelligence.ear.h3.constants.horizons import HORIZON_MS, BAND_ASSIGNMENTS
from Musical_Intelligence.ear.h3.constants.morphs import MORPH_NAMES
from Musical_Intelligence.ear.h3.constants.laws import LAW_NAMES


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SWAN_LAKE_PATH = os.path.join(
    _PROJECT_ROOT,
    "Test-Audio",
    "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
    " - Pyotr Ilyich Tchaikovsky.wav",
)
REPORT_DIR = os.path.join(_PROJECT_ROOT, "Tests", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "swan_lake_report.txt")

SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP  # 172.27 Hz


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sep(char: str = "=", width: int = 80) -> str:
    return char * width


def _section(title: str) -> str:
    return f"\n{'=' * 80}\n  {title}\n{'=' * 80}"


def _load_mel(path: str) -> Tensor:
    """Load audio and compute normalised mel spectrogram (1, 128, T)."""
    y, sr = librosa.load(path, sr=SR, mono=True)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=1024,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    return torch.tensor(mel_norm, dtype=torch.float32).unsqueeze(0)


def frame_to_time(frame: int) -> float:
    """Convert frame index to seconds."""
    return frame / FRAME_RATE


def time_to_frame(seconds: float) -> int:
    """Convert seconds to nearest frame index."""
    return int(round(seconds * FRAME_RATE))


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------
def analyze_r3_dynamics(
    features: Tensor,
    interval_s: float = 1.0,
) -> List[Dict]:
    """Compute mean R3 per group at regular time intervals."""
    B, T, D = features.shape
    interval_frames = max(1, time_to_frame(interval_s))
    results = []

    for t_start in range(0, T, interval_frames):
        t_end = min(t_start + interval_frames, T)
        segment = features[0, t_start:t_end, :]  # (frames, 128)
        seg_mean = segment.mean(dim=0)  # (128,)

        row = {
            "time_s": frame_to_time(t_start),
            "frame_start": t_start,
            "frame_end": t_end,
        }
        for g in R3_GROUP_BOUNDARIES:
            row[g.letter] = seg_mean[g.start:g.end].mean().item()
        results.append(row)

    return results


def sample_h3_at_moments(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    moments_s: List[float],
    T: int,
) -> Dict[float, Dict]:
    """Sample H3 feature values at specific musical moments."""
    results = {}
    for moment in moments_s:
        frame = min(time_to_frame(moment), T - 1)
        sample = {}
        for key, tensor in h3_features.items():
            r3_idx, horizon, morph, law = key
            val = tensor[0, frame].item()
            sample[key] = {
                "value": val,
                "r3_name": R3_FEATURE_NAMES[r3_idx] if r3_idx < len(R3_FEATURE_NAMES) else f"r3_{r3_idx}",
                "horizon_ms": HORIZON_MS[horizon] if horizon < len(HORIZON_MS) else 0,
                "morph_name": MORPH_NAMES[morph] if morph < len(MORPH_NAMES) else f"m{morph}",
                "law_name": LAW_NAMES[law] if law < len(LAW_NAMES) else f"l{law}",
            }
        results[moment] = sample
    return results


def analyze_brain_profile(
    brain_tensor: Tensor,
    unit_slices: Dict[str, Tuple[int, int]],
    interval_s: float = 5.0,
) -> List[Dict]:
    """Compute unit activation profiles at regular intervals."""
    B, T, D = brain_tensor.shape
    interval_frames = max(1, time_to_frame(interval_s))
    results = []

    for t_start in range(0, T, interval_frames):
        t_end = min(t_start + interval_frames, T)
        segment = brain_tensor[0, t_start:t_end, :]  # (frames, 1006)

        row = {
            "time_s": frame_to_time(t_start),
            "time_end_s": frame_to_time(t_end),
        }
        for unit_name in UNIT_ORDER:
            s, e = unit_slices[unit_name]
            unit_data = segment[:, s:e]
            row[unit_name] = {
                "mean": unit_data.mean().item(),
                "std": unit_data.std().item(),
                "max": unit_data.max().item(),
                "min": unit_data.min().item(),
            }
        # Overall brain activity
        row["overall_mean"] = segment.mean().item()
        row["overall_std"] = segment.std().item()
        results.append(row)

    return results


def detect_peaks(
    brain_tensor: Tensor,
    unit_slices: Dict[str, Tuple[int, int]],
    n_peaks: int = 5,
) -> Dict:
    """Find frames with highest and lowest cognitive activity."""
    B, T, D = brain_tensor.shape
    frame_means = brain_tensor[0].mean(dim=-1)  # (T,)

    # Top peaks
    top_vals, top_idx = torch.topk(frame_means, min(n_peaks, T))
    peaks = []
    for val, idx in zip(top_vals.tolist(), top_idx.tolist()):
        frame_data = brain_tensor[0, idx, :]
        unit_vals = {}
        for unit_name in UNIT_ORDER:
            s, e = unit_slices[unit_name]
            unit_vals[unit_name] = frame_data[s:e].mean().item()
        peaks.append({
            "frame": idx,
            "time_s": frame_to_time(idx),
            "mean_activity": val,
            "per_unit": unit_vals,
        })

    # Bottom troughs
    bot_vals, bot_idx = torch.topk(frame_means, min(n_peaks, T), largest=False)
    troughs = []
    for val, idx in zip(bot_vals.tolist(), bot_idx.tolist()):
        frame_data = brain_tensor[0, idx, :]
        unit_vals = {}
        for unit_name in UNIT_ORDER:
            s, e = unit_slices[unit_name]
            unit_vals[unit_name] = frame_data[s:e].mean().item()
        troughs.append({
            "frame": idx,
            "time_s": frame_to_time(idx),
            "mean_activity": val,
            "per_unit": unit_vals,
        })

    return {"peaks": peaks, "troughs": troughs}


def compute_inter_unit_correlation(
    brain_tensor: Tensor,
    unit_slices: Dict[str, Tuple[int, int]],
) -> Dict[str, Dict[str, float]]:
    """Compute correlation matrix between unit mean activations over time."""
    B, T, D = brain_tensor.shape

    # Compute per-unit mean activation over time: (T,) per unit
    unit_means = {}
    for unit_name in UNIT_ORDER:
        s, e = unit_slices[unit_name]
        unit_means[unit_name] = brain_tensor[0, :, s:e].mean(dim=-1)  # (T,)

    # Compute pairwise Pearson correlation
    corr = {}
    for u1 in UNIT_ORDER:
        corr[u1] = {}
        for u2 in UNIT_ORDER:
            x = unit_means[u1]
            y = unit_means[u2]
            x_centered = x - x.mean()
            y_centered = y - y.mean()
            num = (x_centered * y_centered).sum()
            denom = (x_centered.norm() * y_centered.norm()).clamp(min=1e-8)
            corr[u1][u2] = (num / denom).item()

    return corr


def detect_musical_events(
    r3_features: Tensor,
) -> Dict:
    """Detect musical events from R3 features."""
    B, T, D = r3_features.shape
    events = {}

    # Energy peaks (Group B: [7:12])
    energy = r3_features[0, :, 7:12].mean(dim=-1)  # (T,)
    energy_smooth = torch.nn.functional.avg_pool1d(
        energy.unsqueeze(0).unsqueeze(0), kernel_size=51, stride=1, padding=25
    ).squeeze()
    if energy_smooth.numel() > 2:
        # Simple peak detection: find local maxima above mean
        e_mean = energy_smooth.mean()
        e_std = energy_smooth.std()
        threshold = e_mean + e_std
        peaks = []
        for i in range(1, len(energy_smooth) - 1):
            if (energy_smooth[i] > energy_smooth[i - 1]
                    and energy_smooth[i] > energy_smooth[i + 1]
                    and energy_smooth[i] > threshold):
                peaks.append({
                    "frame": i,
                    "time_s": frame_to_time(i),
                    "value": energy_smooth[i].item(),
                })
        events["energy_peaks"] = peaks[:10]  # Top 10
    else:
        events["energy_peaks"] = []

    # Timbral changes (Group C: [12:21])
    timbre = r3_features[0, :, 12:21].mean(dim=-1)
    timbre_diff = torch.diff(timbre).abs()
    if timbre_diff.numel() > 0:
        top_vals, top_idx = torch.topk(timbre_diff, min(10, len(timbre_diff)))
        events["timbral_changes"] = [
            {"frame": idx.item() + 1, "time_s": frame_to_time(idx.item() + 1),
             "magnitude": val.item()}
            for val, idx in zip(top_vals, top_idx)
        ]
    else:
        events["timbral_changes"] = []

    # Tempo estimate from rhythm group (index 65: tempo_estimate)
    if D > 65:
        tempo = r3_features[0, :, 65]  # (T,)
        # Take stable region (after warmup ~2s)
        warmup_end = min(time_to_frame(4.0), T)
        if warmup_end < T:
            stable_tempo = tempo[warmup_end:]
            events["tempo"] = {
                "mean": stable_tempo.mean().item(),
                "std": stable_tempo.std().item(),
                "min": stable_tempo.min().item(),
                "max": stable_tempo.max().item(),
            }
        else:
            events["tempo"] = {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
    else:
        events["tempo"] = {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}

    # Spectral flux / change (Group D: [21:25])
    change = r3_features[0, :, 21:25].mean(dim=-1)
    events["spectral_change"] = {
        "mean": change.mean().item(),
        "std": change.std().item(),
        "max_frame": change.argmax().item(),
        "max_time_s": frame_to_time(change.argmax().item()),
        "max_value": change.max().item(),
    }

    return events


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------
class ReportWriter:
    """Writes both to stdout and a file simultaneously."""

    def __init__(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self._file = open(filepath, "w", encoding="utf-8")

    def print(self, text: str = "") -> None:
        print(text)
        self._file.write(text + "\n")

    def close(self) -> None:
        self._file.close()


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def main() -> None:
    rw = ReportWriter(REPORT_PATH)
    timings: Dict[str, float] = {}
    t_experiment = time.perf_counter()

    rw.print(_section("SWAN LAKE COGNITIVE ANALYSIS EXPERIMENT"))
    rw.print(f"  Audio: {os.path.basename(SWAN_LAKE_PATH)}")
    rw.print(f"  Frame rate: {FRAME_RATE:.2f} Hz")
    rw.print(f"  Brain output dim: {TOTAL_DIM}")
    rw.print(f"  Report: {REPORT_PATH}")
    rw.print()

    # ==================================================================
    # Stage 1: Load audio
    # ==================================================================
    rw.print(_section("STAGE 1: Audio Loading"))
    if not os.path.exists(SWAN_LAKE_PATH):
        rw.print(f"  ERROR: Audio file not found: {SWAN_LAKE_PATH}")
        rw.close()
        sys.exit(1)

    t0 = time.perf_counter()
    mel = _load_mel(SWAN_LAKE_PATH)
    timings["audio_load"] = time.perf_counter() - t0
    B, N, T = mel.shape
    duration_s = T / FRAME_RATE

    rw.print(f"  Mel spectrogram: ({B}, {N}, {T})")
    rw.print(f"  Duration: {duration_s:.1f}s ({T} frames)")
    rw.print(f"  Time: {timings['audio_load']:.3f}s")

    # ==================================================================
    # Stage 2: R3 extraction
    # ==================================================================
    rw.print(_section("STAGE 2: R3 Spectral Feature Extraction"))
    t0 = time.perf_counter()
    r3_ext = R3Extractor()
    r3_output = r3_ext.extract(mel)
    timings["r3_extraction"] = time.perf_counter() - t0
    r3_features = r3_output.features  # (B, T, 128)

    rw.print(f"  R3 output: {tuple(r3_features.shape)}")
    rw.print(f"  Value range: [{r3_features.min().item():.4f}, "
             f"{r3_features.max().item():.4f}]")
    rw.print(f"  Mean: {r3_features.mean().item():.4f}")
    rw.print(f"  Time: {timings['r3_extraction']:.3f}s")

    # ==================================================================
    # Stage 3: H3 extraction
    # ==================================================================
    rw.print(_section("STAGE 3: H3 Temporal Morphology Extraction"))
    t0 = time.perf_counter()

    # Collect full demand from brain
    brain = BrainOrchestrator()
    all_demand = set()
    for unit in brain._units.values():
        all_demand |= unit.h3_demand
    all_demand |= brain._mechanism_runner.h3_demand

    h3_ext = H3Extractor()
    h3_output = h3_ext.extract(r3_features, all_demand)
    timings["h3_extraction"] = time.perf_counter() - t0

    rw.print(f"  Demanded tuples: {len(all_demand)}")
    rw.print(f"  Computed tuples: {h3_output.n_tuples}")
    rw.print(f"  Time: {timings['h3_extraction']:.3f}s")

    # ==================================================================
    # Stage 4: Brain forward pass
    # ==================================================================
    rw.print(_section("STAGE 4: Brain Forward Pass"))
    t0 = time.perf_counter()
    brain_output = brain.forward(h3_output.features, r3_features)
    timings["brain_forward"] = time.perf_counter() - t0

    brain_tensor = brain_output.tensor  # (B, T, 1006)
    unit_slices = brain_output.unit_slices

    rw.print(f"  Brain output: {tuple(brain_tensor.shape)}")
    rw.print(f"  Value range: [{brain_tensor.min().item():.4f}, "
             f"{brain_tensor.max().item():.4f}]")
    rw.print(f"  Mean: {brain_tensor.mean().item():.4f}")
    rw.print(f"  Unit slices:")
    for unit_name in UNIT_ORDER:
        s, e = unit_slices[unit_name]
        dim = e - s
        unit_data = brain_tensor[0, :, s:e]
        rw.print(f"    {unit_name}: [{s:>4}:{e:>4}] ({dim:>3}D)  "
                 f"mean={unit_data.mean().item():.4f}  "
                 f"std={unit_data.std().item():.4f}")
    rw.print(f"  Time: {timings['brain_forward']:.3f}s")

    # ==================================================================
    # Analysis 1: R3 temporal dynamics
    # ==================================================================
    rw.print(_section("ANALYSIS 1: R3 Temporal Dynamics (1-second intervals)"))
    r3_dynamics = analyze_r3_dynamics(r3_features, interval_s=1.0)

    # Print header
    group_letters = [g.letter for g in R3_GROUP_BOUNDARIES]
    header_parts = [f"{'Time':>6}"] + [f"{l:>7}" for l in group_letters]
    rw.print(f"  {' '.join(header_parts)}")
    rw.print(f"  {'-' * (6 + 8 * len(group_letters))}")

    for row in r3_dynamics:
        vals = [f"{row['time_s']:>5.1f}s"] + [f"{row[l]:>7.4f}" for l in group_letters]
        rw.print(f"  {' '.join(vals)}")

    # ==================================================================
    # Analysis 2: H3 features at key musical moments
    # ==================================================================
    rw.print(_section("ANALYSIS 2: H3 Features at Key Musical Moments"))
    moments = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
    moments = [m for m in moments if m < duration_s]
    h3_samples = sample_h3_at_moments(h3_output.features, moments, T)

    for moment, features_at_t in h3_samples.items():
        rw.print(f"\n  t = {moment:.1f}s (frame {time_to_frame(moment)}):")
        if not features_at_t:
            rw.print(f"    No H3 features available")
            continue
        # Show a sample of features (first 10 by key)
        sorted_keys = sorted(features_at_t.keys())[:10]
        for key in sorted_keys:
            info = features_at_t[key]
            rw.print(f"    ({key[0]:>3}, H{key[1]:>2}, M{key[2]:>2}, L{key[3]})"
                     f"  val={info['value']:.4f}"
                     f"  r3={info['r3_name']:<20}"
                     f"  morph={info['morph_name']:<14}"
                     f"  law={info['law_name']}")
        if len(features_at_t) > 10:
            rw.print(f"    ... and {len(features_at_t) - 10} more features")

    # ==================================================================
    # Analysis 3: Brain cognitive profile
    # ==================================================================
    rw.print(_section("ANALYSIS 3: Brain Cognitive Profile (5-second intervals)"))
    brain_profile = analyze_brain_profile(brain_tensor, unit_slices, interval_s=5.0)

    header_parts = [f"{'Time':>10}"] + [f"{u:>7}" for u in UNIT_ORDER] + [f"{'Overall':>8}"]
    rw.print(f"  {' '.join(header_parts)}")
    rw.print(f"  {'-' * (10 + 8 * len(UNIT_ORDER) + 9)}")

    for row in brain_profile:
        time_str = f"{row['time_s']:>4.0f}-{row['time_end_s']:>4.0f}s"
        vals = [f"{time_str:>10}"]
        for u in UNIT_ORDER:
            vals.append(f"{row[u]['mean']:>7.4f}")
        vals.append(f"{row['overall_mean']:>8.4f}")
        rw.print(f"  {' '.join(vals)}")

    # ==================================================================
    # Analysis 4: Peak/trough detection
    # ==================================================================
    rw.print(_section("ANALYSIS 4: Peak & Trough Detection"))
    peak_info = detect_peaks(brain_tensor, unit_slices, n_peaks=5)

    rw.print(f"  Top 5 peak frames (highest cognitive activity):")
    for i, p in enumerate(peak_info["peaks"]):
        rw.print(f"    #{i + 1}: frame={p['frame']:>5}, t={p['time_s']:>6.2f}s, "
                 f"mean={p['mean_activity']:.4f}")
        top_units = sorted(p["per_unit"].items(), key=lambda x: -x[1])[:3]
        for uname, uval in top_units:
            rw.print(f"         {uname}: {uval:.4f}")

    rw.print(f"\n  Bottom 5 trough frames (lowest cognitive activity):")
    for i, p in enumerate(peak_info["troughs"]):
        rw.print(f"    #{i + 1}: frame={p['frame']:>5}, t={p['time_s']:>6.2f}s, "
                 f"mean={p['mean_activity']:.4f}")

    # ==================================================================
    # Analysis 5: Inter-unit correlation matrix
    # ==================================================================
    rw.print(_section("ANALYSIS 5: Inter-Unit Correlation Matrix"))
    corr = compute_inter_unit_correlation(brain_tensor, unit_slices)

    header_parts = [f"{'':>5}"] + [f"{u:>7}" for u in UNIT_ORDER]
    rw.print(f"  {' '.join(header_parts)}")
    rw.print(f"  {'-' * (5 + 8 * len(UNIT_ORDER))}")
    for u1 in UNIT_ORDER:
        vals = [f"{u1:>5}"]
        for u2 in UNIT_ORDER:
            r = corr[u1][u2]
            vals.append(f"{r:>7.3f}")
        rw.print(f"  {' '.join(vals)}")

    # Identify strongest correlations (excluding self)
    rw.print(f"\n  Strongest inter-unit correlations:")
    pairs = []
    for i, u1 in enumerate(UNIT_ORDER):
        for j, u2 in enumerate(UNIT_ORDER):
            if i < j:
                pairs.append((u1, u2, corr[u1][u2]))
    pairs.sort(key=lambda x: -abs(x[2]))
    for u1, u2, r in pairs[:5]:
        rw.print(f"    {u1}-{u2}: r={r:.4f}")

    # ==================================================================
    # Analysis 6: Musical event detection
    # ==================================================================
    rw.print(_section("ANALYSIS 6: Musical Event Detection"))
    events = detect_musical_events(r3_features)

    rw.print(f"  Tempo estimate (R3 index 65, after 4s warmup):")
    rw.print(f"    mean={events['tempo']['mean']:.4f}, "
             f"std={events['tempo']['std']:.4f}, "
             f"range=[{events['tempo']['min']:.4f}, {events['tempo']['max']:.4f}]")

    rw.print(f"\n  Spectral change profile:")
    sc = events["spectral_change"]
    rw.print(f"    mean={sc['mean']:.4f}, std={sc['std']:.4f}")
    rw.print(f"    max at frame {sc['max_frame']} "
             f"(t={sc['max_time_s']:.2f}s), value={sc['max_value']:.4f}")

    rw.print(f"\n  Energy peaks ({len(events['energy_peaks'])} detected):")
    for i, p in enumerate(events["energy_peaks"][:5]):
        rw.print(f"    #{i + 1}: t={p['time_s']:>6.2f}s, value={p['value']:.4f}")

    rw.print(f"\n  Timbral change events ({len(events['timbral_changes'])} detected):")
    for i, tc in enumerate(events["timbral_changes"][:5]):
        rw.print(f"    #{i + 1}: t={tc['time_s']:>6.2f}s, magnitude={tc['magnitude']:.4f}")

    # ==================================================================
    # Timing summary
    # ==================================================================
    total_time = time.perf_counter() - t_experiment
    rw.print(_section("TIMING SUMMARY"))
    rw.print(f"  Audio loading:       {timings['audio_load']:>8.3f}s")
    rw.print(f"  R3 extraction:       {timings['r3_extraction']:>8.3f}s")
    rw.print(f"  H3 extraction:       {timings['h3_extraction']:>8.3f}s")
    rw.print(f"  Brain forward:       {timings['brain_forward']:>8.3f}s")
    pipeline_time = sum(timings.values())
    rw.print(f"  Pipeline total:      {pipeline_time:>8.3f}s")
    rw.print(f"  Analysis overhead:   {total_time - pipeline_time:>8.3f}s")
    rw.print(f"  Experiment total:    {total_time:>8.3f}s")

    # ==================================================================
    # Final summary
    # ==================================================================
    rw.print(_section("EXPERIMENT SUMMARY"))
    rw.print(f"  Audio: Swan Lake Suite, Op. 20a, Scene I")
    rw.print(f"  Duration: {duration_s:.1f}s ({T} frames)")
    rw.print(f"  R3 features: {tuple(r3_features.shape)} in "
             f"[{r3_features.min().item():.4f}, {r3_features.max().item():.4f}]")
    rw.print(f"  H3 tuples: {h3_output.n_tuples} computed")
    rw.print(f"  Brain output: {tuple(brain_tensor.shape)} in "
             f"[{brain_tensor.min().item():.4f}, {brain_tensor.max().item():.4f}]")
    rw.print(f"  Total time: {total_time:.3f}s")
    rw.print(f"  Report saved: {REPORT_PATH}")
    rw.print(_sep())

    rw.close()
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
