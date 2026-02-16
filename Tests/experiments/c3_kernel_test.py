#!/usr/bin/env python3
"""C³ Kernel Belief-Cycle Test on Swan Lake.

Tests the minimal 3-belief kernel:
  perceived_consonance (SPU) + tempo_state (STU) + reward_valence (ARU)

Pipeline: Audio → Cochlea → R³(128D) → H³(sparse) → C³ Kernel → traces

Expected behavior:
  - First 5s: low familiarity (default), higher PE
  - Theme repeat: rising consonance stability, dropping PE
  - Crescendo: salience spike (default=1), reward spike
  - Repetition: resolution reward increases

Usage:
    python Tests/experiments/c3_kernel_test.py
"""
from __future__ import annotations

import os
import sys
import time

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.kernel.scheduler import C3Kernel


# ── Constants ───────────────────────────────────────────────────────
SWAN_LAKE_PATH = os.path.join(
    _PROJECT_ROOT,
    "Test-Audio",
    "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
    " - Pyotr Ilyich Tchaikovsky.wav",
)
SR = 44100
HOP = 256
N_MELS = 128
DURATION = 30  # seconds


def main() -> None:
    print("=" * 70)
    print("C³ Kernel Belief-Cycle Test — Swan Lake 30s")
    print("=" * 70)

    # ── 1. Load audio ───────────────────────────────────────────────
    print("\n[1/5] Loading audio...")
    t0 = time.time()
    waveform, sr = librosa.load(SWAN_LAKE_PATH, sr=SR, duration=DURATION, mono=True)
    waveform_t = torch.from_numpy(waveform).unsqueeze(0).float()  # (1, N)
    print(f"  Audio: {waveform.shape[0]/SR:.1f}s, {sr}Hz")

    # ── 2. Mel spectrogram ──────────────────────────────────────────
    mel_np = librosa.feature.melspectrogram(
        y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP
    )
    mel_db = librosa.power_to_db(mel_np, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.from_numpy(mel_norm).unsqueeze(0).float()  # (1, 128, T)
    T = mel_t.shape[2]
    print(f"  Mel: (1, {N_MELS}, {T}), {T/SR*HOP:.1f}s at {SR/HOP:.1f} Hz")

    # ── 3. R³ extraction ────────────────────────────────────────────
    print("\n[2/5] R³ extraction...")
    t1 = time.time()
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t, audio=waveform_t, sr=SR)
    r3_tensor = r3_out.features  # (1, T, 128)
    feature_map = r3_out.feature_map
    print(f"  R³: {r3_tensor.shape}, {time.time()-t1:.2f}s")

    # ── 4. H³ extraction ────────────────────────────────────────────
    print("\n[3/5] H³ extraction...")
    t2 = time.time()

    # Build H³ demand set from kernel (beliefs + BCH L0 demands, deduped)
    kernel_tmp = C3Kernel(feature_map)
    demand = kernel_tmp.h3_demands()
    print(f"  Demand: {len(demand)} tuples (incl. BCH L0)")

    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, demand)
    h3_dict = h3_out.features  # Dict[(r3_idx, h, m, l) → (1, T)]
    print(f"  H³: {len(h3_dict)} tuples, {time.time()-t2:.2f}s")

    # ── 5. C³ Kernel ────────────────────────────────────────────────
    print("\n[4/5] C³ Kernel belief cycle...")
    t3 = time.time()
    kernel = C3Kernel(feature_map)

    # Storage for traces
    traces = {
        "perceived_consonance": [],
        "tempo_state": [],
        "reward_valence": [],
        "pe_consonance": [],
        "pe_tempo": [],
    }

    # Run frame-by-frame
    for t in range(T):
        r3_frame = r3_tensor[:, t:t+1, :]  # (1, 1, 128)

        # Extract H³ for this frame (slice all tuples)
        h3_frame = {}
        for key, val in h3_dict.items():
            if val.shape[1] > t:
                h3_frame[key] = val[:, t:t+1]

        out = kernel.tick(r3_frame, h3_frame)

        traces["perceived_consonance"].append(
            out.beliefs["perceived_consonance"].mean().item()
        )
        traces["tempo_state"].append(
            out.beliefs["tempo_state"].mean().item()
        )
        traces["reward_valence"].append(
            out.beliefs["reward_valence"].mean().item()
        )
        traces["pe_consonance"].append(
            out.pe["perceived_consonance"].mean().item()
        )
        traces["pe_tempo"].append(
            out.pe["tempo_state"].mean().item()
        )

    elapsed = time.time() - t3
    print(f"  C³: {T} frames, {elapsed:.2f}s ({T/elapsed:.0f} frames/s)")

    # ── 6. Report ───────────────────────────────────────────────────
    print("\n[5/5] Belief trace analysis...")
    print("=" * 70)

    # Convert to numpy for stats
    for k in traces:
        traces[k] = np.array(traces[k])

    # Time axis
    frame_rate = SR / HOP
    time_axis = np.arange(T) / frame_rate

    # Summary stats per 5-second window
    window_frames = int(5 * frame_rate)
    n_windows = T // window_frames

    print(f"\n{'Window':>8s} | {'Consonance':>11s} | {'Tempo':>7s} | "
          f"{'Reward':>8s} | {'PE_cons':>8s} | {'PE_tempo':>8s}")
    print("-" * 70)

    for w in range(n_windows):
        s = w * window_frames
        e = (w + 1) * window_frames
        t_start = s / frame_rate
        t_end = e / frame_rate

        cons_mean = traces["perceived_consonance"][s:e].mean()
        tempo_mean = traces["tempo_state"][s:e].mean()
        reward_mean = traces["reward_valence"][s:e].mean()
        pe_c_std = traces["pe_consonance"][s:e].std()
        pe_t_std = traces["pe_tempo"][s:e].std()

        print(f"  {t_start:4.0f}-{t_end:2.0f}s | "
              f"  {cons_mean:9.4f} | {tempo_mean:7.4f} | "
              f"{reward_mean:8.4f} | {pe_c_std:8.4f} | {pe_t_std:8.4f}")

    # Global stats
    print(f"\n{'Global':>8s} | "
          f"  {traces['perceived_consonance'].mean():9.4f} | "
          f"{traces['tempo_state'].mean():7.4f} | "
          f"{traces['reward_valence'].mean():8.4f} | "
          f"{traces['pe_consonance'].std():8.4f} | "
          f"{traces['pe_tempo'].std():8.4f}")

    # Dynamic range
    print(f"\n  Consonance range: [{traces['perceived_consonance'].min():.3f}, "
          f"{traces['perceived_consonance'].max():.3f}]")
    print(f"  Tempo range:      [{traces['tempo_state'].min():.3f}, "
          f"{traces['tempo_state'].max():.3f}]")
    print(f"  Reward range:     [{traces['reward_valence'].min():.3f}, "
          f"{traces['reward_valence'].max():.3f}]")

    # Total pipeline timing
    total = time.time() - t0
    print(f"\n  Total pipeline: {total:.1f}s "
          f"(Audio {time.time()-t0:.0f}s, R³ {t2-t1:.1f}s, "
          f"H³ {t3-t2:.1f}s, C³ {elapsed:.1f}s)")

    print("\n" + "=" * 70)
    print("C³ Kernel Test COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
