#!/usr/bin/env python3
"""H3 Temporal Morphology Benchmark -- per-horizon profiling.

Profiles H3 extraction across the four perceptual bands (micro, meso,
macro, ultra), measuring:

- Time per horizon group (band)
- Morph computation distribution across bands
- Demand density per horizon (tuples per horizon index)

Uses Swan Lake audio for realistic R3 input, sliced to 10 seconds for
reasonable benchmark duration.

Usage::

    python Tests/benchmarks/bench_h3.py
"""
from __future__ import annotations

import gc
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root on sys.path
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(_PROJECT_ROOT))

import numpy as np
import torch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SWAN_LAKE = (
    "Test-Audio/Swan Lake Suite, Op. 20a_ I. Scene "
    "_Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav"
)
SWAN_LAKE_PATH = os.path.join(os.path.abspath(_PROJECT_ROOT), SWAN_LAKE)

DURATION_S = 10  # seconds of audio to use
SR = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048

# Horizon band definitions
BAND_DEFS = {
    "micro": list(range(0, 8)),     # H0-H7
    "meso":  list(range(8, 16)),    # H8-H15
    "macro": list(range(16, 24)),   # H16-H23
    "ultra": list(range(24, 32)),   # H24-H31
}

# Morph names for reporting
MORPH_NAMES = (
    "value", "mean", "std", "median", "max", "range",
    "skewness", "kurtosis", "velocity", "velocity_mean",
    "velocity_std", "acceleration", "acceleration_mean",
    "acceleration_std", "periodicity", "smoothness",
    "curvature", "shape_period", "trend", "stability",
    "entropy", "zero_crossings", "peaks", "symmetry",
)

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
SEP_HEAVY = "=" * 78
SEP_LIGHT = "-" * 78

def _fmt_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f} us"
    elif seconds < 1.0:
        return f"{seconds * 1_000:.1f} ms"
    else:
        return f"{seconds:.3f} s"


# ---------------------------------------------------------------------------
# Demand analysis helpers
# ---------------------------------------------------------------------------
def analyze_demand(demand: set) -> dict:
    """Compute per-horizon and per-morph statistics for a demand set."""
    per_horizon = Counter()
    per_morph = Counter()
    per_band = Counter()
    per_band_morphs = defaultdict(Counter)

    for r3_idx, horizon, morph, law in demand:
        per_horizon[horizon] += 1
        per_morph[morph] += 1
        # Determine band
        for band_name, horizons in BAND_DEFS.items():
            if horizon in horizons:
                per_band[band_name] += 1
                per_band_morphs[band_name][morph] += 1
                break

    return {
        "per_horizon": per_horizon,
        "per_morph": per_morph,
        "per_band": per_band,
        "per_band_morphs": per_band_morphs,
    }


def split_demand_by_band(demand: set) -> dict:
    """Split demand set into per-band subsets."""
    band_demands = {band: set() for band in BAND_DEFS}
    for tup in demand:
        r3_idx, horizon, morph, law = tup
        for band_name, horizons in BAND_DEFS.items():
            if horizon in horizons:
                band_demands[band_name].add(tup)
                break
    return band_demands


# ---------------------------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------------------------
def main() -> None:
    import librosa
    from Musical_Intelligence.ear import R3Extractor, H3Extractor
    from Musical_Intelligence.brain import BrainOrchestrator

    print(SEP_HEAVY)
    print("  H3 TEMPORAL MORPHOLOGY BENCHMARK")
    print(SEP_HEAVY)
    print()

    # ------------------------------------------------------------------
    # Load and prepare audio
    # ------------------------------------------------------------------
    if not os.path.exists(SWAN_LAKE_PATH):
        print(f"[ERROR] Swan Lake audio not found at:")
        print(f"  {SWAN_LAKE_PATH}")
        print(f"  Place the WAV file in Test-Audio/ to run this benchmark.")
        sys.exit(1)

    print(f"Loading audio: {os.path.basename(SWAN_LAKE_PATH)}")
    y, sr = librosa.load(SWAN_LAKE_PATH, sr=SR, duration=float(DURATION_S))
    print(f"  Loaded: {len(y)} samples, {len(y) / sr:.1f}s @ {sr} Hz")
    print()

    # ------------------------------------------------------------------
    # Compute mel + R3
    # ------------------------------------------------------------------
    print("Computing mel spectrogram...")
    mel_np = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS,
    )
    mel_np = np.log1p(mel_np)
    mel_max = mel_np.max()
    if mel_max > 0:
        mel_np = mel_np / mel_max
    mel = torch.from_numpy(mel_np).unsqueeze(0).float()
    print(f"  Mel shape: {tuple(mel.shape)}")

    print("Computing R3 features...")
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel)
    r3_tensor = r3_out.features
    B, T, D = r3_tensor.shape
    print(f"  R3 shape: {tuple(r3_tensor.shape)}")
    print()

    # ------------------------------------------------------------------
    # Collect full demand from brain
    # ------------------------------------------------------------------
    print("Collecting H3 demand from BrainOrchestrator...")
    brain = BrainOrchestrator()
    demand = brain._mechanism_runner.h3_demand
    for unit in brain._units.values():
        demand |= unit.h3_demand
    print(f"  Total demand: {len(demand)} unique 4-tuples")
    print()

    # ------------------------------------------------------------------
    # Demand analysis
    # ------------------------------------------------------------------
    stats = analyze_demand(demand)
    band_demands = split_demand_by_band(demand)

    print(SEP_LIGHT)
    print("  DEMAND DENSITY PER HORIZON")
    print(SEP_LIGHT)
    print()

    header = f"{'Horizon':>8s}  {'Band':>6s}  {'Tuples':>7s}  {'Density':>8s}"
    print(header)
    print("-" * len(header))

    # Theoretical max per horizon = 97 * 24 * 3 = 6984
    THEORETICAL_PER_HORIZON = 97 * 24 * 3

    for h in range(32):
        count = stats["per_horizon"].get(h, 0)
        band = "micro" if h < 8 else "meso" if h < 16 else "macro" if h < 24 else "ultra"
        density = count / THEORETICAL_PER_HORIZON * 100 if count > 0 else 0.0
        if count > 0:
            print(f"    H{h:<4d}  {band:>6s}  {count:>7d}  {density:>7.2f}%")

    print()

    # ------------------------------------------------------------------
    # Demand per band summary
    # ------------------------------------------------------------------
    print(SEP_LIGHT)
    print("  DEMAND PER BAND SUMMARY")
    print(SEP_LIGHT)
    print()

    header_band = (
        f"{'Band':>8s}  {'Tuples':>7s}  {'% of Total':>10s}  "
        f"{'Horizons Used':>14s}"
    )
    print(header_band)
    print("-" * len(header_band))

    for band_name in ("micro", "meso", "macro", "ultra"):
        count = stats["per_band"].get(band_name, 0)
        pct = count / len(demand) * 100 if len(demand) > 0 else 0.0
        active_horizons = sum(
            1 for h in BAND_DEFS[band_name]
            if stats["per_horizon"].get(h, 0) > 0
        )
        total_horizons = len(BAND_DEFS[band_name])
        print(
            f"  {band_name:>6s}  {count:>7d}  {pct:>9.1f}%  "
            f"{active_horizons:>6d} / {total_horizons}"
        )

    print()

    # ------------------------------------------------------------------
    # Morph distribution per band
    # ------------------------------------------------------------------
    print(SEP_LIGHT)
    print("  MORPH COMPUTATION DISTRIBUTION")
    print(SEP_LIGHT)
    print()

    for band_name in ("micro", "meso", "macro", "ultra"):
        morph_counts = stats["per_band_morphs"].get(band_name, Counter())
        if not morph_counts:
            continue
        print(f"  {band_name.upper()} band:")
        # Sort by count descending, show top 10
        for morph_idx, count in morph_counts.most_common(10):
            morph_name = MORPH_NAMES[morph_idx] if morph_idx < len(MORPH_NAMES) else f"M{morph_idx}"
            pct = count / stats["per_band"][band_name] * 100
            bar = "#" * int(pct / 2)
            print(f"    M{morph_idx:<2d} {morph_name:<20s} {count:>5d} ({pct:>5.1f}%) {bar}")
        if len(morph_counts) > 10:
            print(f"    ... and {len(morph_counts) - 10} more morphs")
        print()

    # ------------------------------------------------------------------
    # Per-band H3 extraction timing
    # ------------------------------------------------------------------
    print(SEP_LIGHT)
    print("  PER-BAND H3 EXTRACTION TIMING")
    print(SEP_LIGHT)
    print()

    h3_ext = H3Extractor()

    # Warmup run (full demand)
    print("  Warmup run (full demand)...")
    gc.collect()
    t0 = time.perf_counter()
    h3_full = h3_ext.extract(r3_tensor, demand)
    t_full = time.perf_counter() - t0
    print(f"  Full H3: {h3_full.n_tuples} tuples in {_fmt_time(t_full)}")
    print(f"  Throughput: {T / t_full:.0f} frames/s")
    print()

    # Per-band timing
    band_times = {}

    header_timing = (
        f"{'Band':>8s}  {'Tuples':>7s}  {'Time':>10s}  "
        f"{'f/s':>8s}  {'us/tuple':>10s}"
    )
    print(header_timing)
    print("-" * len(header_timing))

    for band_name in ("micro", "meso", "macro", "ultra"):
        bd = band_demands[band_name]
        if not bd:
            print(f"  {band_name:>6s}  {0:>7d}  {'--':>10s}  {'--':>8s}  {'--':>10s}")
            continue

        gc.collect()
        t0 = time.perf_counter()
        h3_band = h3_ext.extract(r3_tensor, bd)
        t_band = time.perf_counter() - t0

        band_times[band_name] = t_band
        n_tuples = h3_band.n_tuples
        fps = T / t_band if t_band > 0 else 0
        us_per_tuple = (t_band * 1_000_000 / n_tuples) if n_tuples > 0 else 0

        print(
            f"  {band_name:>6s}  {n_tuples:>7d}  "
            f"{_fmt_time(t_band):>10s}  "
            f"{fps:>8.0f}  "
            f"{us_per_tuple:>9.1f}"
        )

    print()

    # ------------------------------------------------------------------
    # Timing breakdown pie
    # ------------------------------------------------------------------
    if band_times:
        total_band_time = sum(band_times.values())
        print("  Time distribution:")
        for band_name in ("micro", "meso", "macro", "ultra"):
            t = band_times.get(band_name, 0)
            pct = t / total_band_time * 100 if total_band_time > 0 else 0
            bar = "#" * int(pct / 2)
            print(f"    {band_name:>6s}  {pct:>5.1f}%  {bar}")
        print()

    # ------------------------------------------------------------------
    # Per-individual-horizon timing (sample 4 horizons, 1 per band)
    # ------------------------------------------------------------------
    print(SEP_LIGHT)
    print("  INDIVIDUAL HORIZON PROFILING (1 per band)")
    print(SEP_LIGHT)
    print()

    # Pick the most-populated horizon from each band
    sample_horizons = {}
    for band_name, horizon_list in BAND_DEFS.items():
        best_h = max(horizon_list, key=lambda h: stats["per_horizon"].get(h, 0))
        if stats["per_horizon"].get(best_h, 0) > 0:
            sample_horizons[band_name] = best_h

    header_single = (
        f"{'Band':>8s}  {'H':>3s}  {'Tuples':>7s}  "
        f"{'Time':>10s}  {'us/tuple':>10s}"
    )
    print(header_single)
    print("-" * len(header_single))

    for band_name in ("micro", "meso", "macro", "ultra"):
        if band_name not in sample_horizons:
            continue
        h = sample_horizons[band_name]
        # Extract demand for just this horizon
        h_demand = {tup for tup in demand if tup[1] == h}
        if not h_demand:
            continue

        gc.collect()
        t0 = time.perf_counter()
        h3_h = h3_ext.extract(r3_tensor, h_demand)
        t_h = time.perf_counter() - t0

        n = h3_h.n_tuples
        us_per = (t_h * 1_000_000 / n) if n > 0 else 0
        print(
            f"  {band_name:>6s}  H{h:<2d} {n:>7d}  "
            f"{_fmt_time(t_h):>10s}  "
            f"{us_per:>9.1f}"
        )

    print()
    print(SEP_HEAVY)
    print("  H3 Benchmark complete.")
    print(SEP_HEAVY)


if __name__ == "__main__":
    main()
