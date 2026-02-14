#!/usr/bin/env python3
"""MI Pipeline Performance Benchmark.

Benchmarks each stage of the Musical Intelligence pipeline separately:

    Cochlea (mel) -> R3 (128D) -> H3 (sparse) -> Brain C3 (1006D)

Tests multiple audio durations (1s, 5s, 10s, 30s) and reports per-stage
timing, throughput (frames/second), and approximate memory usage.

Usage::

    python Tests/benchmarks/bench_pipeline.py
"""
from __future__ import annotations

import gc
import os
import sys
import time
import tracemalloc
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

DURATIONS = [1, 5, 10, 30]  # seconds
SR = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048

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

def _fmt_mem(bytes_val: int) -> str:
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

def _fmt_throughput(frames: int, seconds: float) -> str:
    if seconds <= 0:
        return "inf"
    fps = frames / seconds
    if fps >= 1_000_000:
        return f"{fps / 1_000_000:.1f}M"
    elif fps >= 1_000:
        return f"{fps / 1_000:.1f}K"
    else:
        return f"{fps:.0f}"


# ---------------------------------------------------------------------------
# Memory measurement
# ---------------------------------------------------------------------------
def measure_memory(func, *args, **kwargs):
    """Run func and return (result, peak_memory_bytes, elapsed_seconds)."""
    gc.collect()
    tracemalloc.start()
    t0 = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak, elapsed


# ---------------------------------------------------------------------------
# Cochlea stage: audio -> mel spectrogram
# ---------------------------------------------------------------------------
def cochlea_stage(y: np.ndarray, sr: int) -> torch.Tensor:
    """Convert raw audio to log-mel spectrogram tensor."""
    import librosa
    mel_np = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS,
    )
    mel_np = np.log1p(mel_np)
    mel_max = mel_np.max()
    if mel_max > 0:
        mel_np = mel_np / mel_max
    return torch.from_numpy(mel_np).unsqueeze(0).float()


# ---------------------------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------------------------
def main() -> None:
    import librosa
    from Musical_Intelligence.ear import R3Extractor, H3Extractor
    from Musical_Intelligence.brain import BrainOrchestrator

    print(SEP_HEAVY)
    print("  MI PIPELINE PERFORMANCE BENCHMARK")
    print(SEP_HEAVY)
    print()

    # ------------------------------------------------------------------
    # Load Swan Lake audio (full)
    # ------------------------------------------------------------------
    if not os.path.exists(SWAN_LAKE_PATH):
        print(f"[ERROR] Swan Lake audio not found at:")
        print(f"  {SWAN_LAKE_PATH}")
        print(f"  Place the WAV file in Test-Audio/ to run this benchmark.")
        sys.exit(1)

    print(f"Loading audio: {os.path.basename(SWAN_LAKE_PATH)}")
    y_full, sr = librosa.load(SWAN_LAKE_PATH, sr=SR)
    print(f"  Loaded: {len(y_full)} samples, {len(y_full) / sr:.1f}s @ {sr} Hz")
    print()

    # ------------------------------------------------------------------
    # Initialize extractors
    # ------------------------------------------------------------------
    print("Initializing pipeline components...")
    t0 = time.perf_counter()
    r3_ext = R3Extractor()
    t_r3_init = time.perf_counter() - t0

    t0 = time.perf_counter()
    h3_ext = H3Extractor()
    t_h3_init = time.perf_counter() - t0

    t0 = time.perf_counter()
    brain = BrainOrchestrator()
    t_brain_init = time.perf_counter() - t0

    print(f"  R3Extractor:      {_fmt_time(t_r3_init)}")
    print(f"  H3Extractor:      {_fmt_time(t_h3_init)}")
    print(f"  BrainOrchestrator: {_fmt_time(t_brain_init)}")
    print()

    # Collect brain demand (once)
    demand = brain._mechanism_runner.h3_demand
    for unit in brain._units.values():
        demand |= unit.h3_demand
    print(f"Total H3 demand: {len(demand)} unique 4-tuples")
    print()

    # ------------------------------------------------------------------
    # Benchmark loop over durations
    # ------------------------------------------------------------------
    results = []

    for dur in DURATIONS:
        n_samples = int(dur * sr)
        if n_samples > len(y_full):
            print(f"[SKIP] {dur}s exceeds audio length "
                  f"({len(y_full) / sr:.1f}s)")
            continue

        y = y_full[:n_samples]

        print(SEP_LIGHT)
        print(f"  Duration: {dur}s  ({n_samples:,} samples)")
        print(SEP_LIGHT)

        # -- Cochlea --
        mel, mem_cochlea, t_cochlea = measure_memory(cochlea_stage, y, sr)
        T_mel = mel.shape[2]
        print(f"  Cochlea:  {_fmt_time(t_cochlea):>10s}  "
              f"mem={_fmt_mem(mem_cochlea):>8s}  "
              f"shape={tuple(mel.shape)}")

        # -- R3 --
        r3_out, mem_r3, t_r3 = measure_memory(r3_ext.extract, mel)
        r3_tensor = r3_out.features
        T = r3_tensor.shape[1]
        print(f"  R3:       {_fmt_time(t_r3):>10s}  "
              f"mem={_fmt_mem(mem_r3):>8s}  "
              f"shape={tuple(r3_tensor.shape)}  "
              f"tput={_fmt_throughput(T, t_r3)} f/s")

        # -- H3 --
        h3_out, mem_h3, t_h3 = measure_memory(
            h3_ext.extract, r3_tensor, demand
        )
        print(f"  H3:       {_fmt_time(t_h3):>10s}  "
              f"mem={_fmt_mem(mem_h3):>8s}  "
              f"tuples={h3_out.n_tuples}  "
              f"tput={_fmt_throughput(T, t_h3)} f/s")

        # -- Brain --
        brain_out, mem_brain, t_brain = measure_memory(
            brain.forward, h3_out.features, r3_tensor
        )
        output = brain_out.tensor
        print(f"  Brain:    {_fmt_time(t_brain):>10s}  "
              f"mem={_fmt_mem(mem_brain):>8s}  "
              f"shape={tuple(output.shape)}  "
              f"tput={_fmt_throughput(T, t_brain)} f/s")

        t_total = t_cochlea + t_r3 + t_h3 + t_brain
        print(f"  Total:    {_fmt_time(t_total):>10s}  "
              f"tput={_fmt_throughput(T, t_total)} f/s")
        print()

        results.append({
            "dur": dur,
            "T": T,
            "t_cochlea": t_cochlea,
            "t_r3": t_r3,
            "t_h3": t_h3,
            "t_brain": t_brain,
            "t_total": t_total,
            "mem_cochlea": mem_cochlea,
            "mem_r3": mem_r3,
            "mem_h3": mem_h3,
            "mem_brain": mem_brain,
        })

    # ------------------------------------------------------------------
    # Summary table
    # ------------------------------------------------------------------
    if not results:
        print("[WARN] No benchmarks completed.")
        return

    print()
    print(SEP_HEAVY)
    print("  SUMMARY TABLE")
    print(SEP_HEAVY)
    print()

    # Header
    header = (
        f"{'Dur':>5s}  {'Frames':>7s}  "
        f"{'Cochlea':>9s}  {'R3':>9s}  {'H3':>9s}  {'Brain':>9s}  "
        f"{'Total':>9s}  {'f/s':>7s}"
    )
    print(header)
    print("-" * len(header))

    for r in results:
        fps = r["T"] / r["t_total"] if r["t_total"] > 0 else 0
        print(
            f"{r['dur']:>4d}s  {r['T']:>7d}  "
            f"{_fmt_time(r['t_cochlea']):>9s}  "
            f"{_fmt_time(r['t_r3']):>9s}  "
            f"{_fmt_time(r['t_h3']):>9s}  "
            f"{_fmt_time(r['t_brain']):>9s}  "
            f"{_fmt_time(r['t_total']):>9s}  "
            f"{fps:>7.0f}"
        )

    print()

    # Memory table
    header_mem = (
        f"{'Dur':>5s}  "
        f"{'Cochlea':>9s}  {'R3':>9s}  {'H3':>9s}  {'Brain':>9s}"
    )
    print("  MEMORY (peak per stage)")
    print(header_mem)
    print("-" * len(header_mem))

    for r in results:
        print(
            f"{r['dur']:>4d}s  "
            f"{_fmt_mem(r['mem_cochlea']):>9s}  "
            f"{_fmt_mem(r['mem_r3']):>9s}  "
            f"{_fmt_mem(r['mem_h3']):>9s}  "
            f"{_fmt_mem(r['mem_brain']):>9s}"
        )

    print()
    print(SEP_HEAVY)
    print("  Benchmark complete.")
    print(SEP_HEAVY)


if __name__ == "__main__":
    main()
