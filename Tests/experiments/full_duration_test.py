#!/usr/bin/env python3
"""Full-Duration C³ Kernel Test — Serial, Memory-Safe.

Processes full-length pieces one at a time on CPU with aggressive
memory cleanup between pieces.  Designed for M2 Air 8GB.

Output: summary metrics only (no raw tensors stored).

Usage:
    python Tests/experiments/full_duration_test.py
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np
import torch
import librosa

torch.set_grad_enabled(False)

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.kernel.scheduler import C3Kernel

# ── Configuration ────────────────────────────────────────────────────
SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP  # 172.27 Hz

PIECES = [
    ("Bach Cello", os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    )),
    ("Swan Lake", os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
        " - Pyotr Ilyich Tchaikovsky.wav",
    )),
    ("Herald of the Change", os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Herald of the Change - Hans Zimmer.wav",
    )),
    ("Beethoven Pathétique", os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    )),
]

WINDOW_SEC = 10  # analysis window size in seconds


def memory_mb() -> float:
    """Current process RSS in MB (macOS/Linux)."""
    try:
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
    except Exception:
        return 0.0


def hard_cleanup() -> None:
    """Aggressive memory cleanup between pieces."""
    gc.collect()
    if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
        try:
            torch.mps.empty_cache()
        except Exception:
            pass
    gc.collect()


def run_single_piece(name: str, path: str) -> dict:
    """Run full Audio → R³ → H³ → C³ pipeline on one piece.

    Returns summary dict with metrics only (no tensors).
    """
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")
    mem_start = memory_mb()

    # ── 1. Load full audio ──────────────────────────────────────────
    print(f"  [1/4] Loading audio (full duration)...")
    t0 = time.time()
    waveform, sr = librosa.load(path, sr=SR, mono=True)  # full duration
    duration_s = len(waveform) / SR
    waveform_t = torch.from_numpy(waveform).unsqueeze(0).float()
    print(f"    Duration: {duration_s:.1f}s ({len(waveform)} samples)")

    # ── 2. Mel + R³ ─────────────────────────────────────────────────
    print(f"  [2/4] Mel + R³ extraction...")
    t1 = time.time()
    mel_np = librosa.feature.melspectrogram(
        y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP,
    )
    mel_db = librosa.power_to_db(mel_np, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.from_numpy(mel_norm).unsqueeze(0).float()
    T = mel_t.shape[2]
    print(f"    Mel: (1, 128, {T})")

    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t, audio=waveform_t, sr=SR)
    r3_tensor = r3_out.features  # (1, T, 97)
    feature_map = r3_out.feature_map
    r3_time = time.time() - t1
    print(f"    R³: {r3_tensor.shape}, {r3_time:.1f}s")

    # Free audio + mel (no longer needed)
    del waveform, waveform_t, mel_np, mel_db, mel_norm, mel_t
    gc.collect()

    # ── 3. H³ ──────────────────────────────────────────────────────
    print(f"  [3/4] H³ extraction...")
    t2 = time.time()
    kernel_tmp = C3Kernel(feature_map)
    demands = kernel_tmp.h3_demands()
    del kernel_tmp

    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, demands)
    h3_dict = h3_out.features
    h3_time = time.time() - t2
    print(f"    H³: {len(h3_dict)} tuples, {h3_time:.2f}s")
    del h3_ext, h3_out
    gc.collect()

    # ── 4. C³ Kernel (frame-by-frame) ──────────────────────────────
    print(f"  [4/4] C³ Kernel ({T} frames)...")
    t3 = time.time()
    kernel = C3Kernel(feature_map)

    # Rolling statistics (no full trace storage)
    window_frames = int(WINDOW_SEC * FRAME_RATE)
    n_windows = max(1, T // window_frames)

    # Per-window accumulators
    windows = []
    # Running accumulators for current window
    w_cons = []
    w_tempo = []
    w_sal = []
    w_fam = []
    w_reward = []
    w_pe_cons = []
    w_pe_tempo = []
    w_pe_sal = []
    w_pe_fam = []

    # Global accumulators (running stats, not full arrays)
    all_reward = []
    all_cons = []
    all_sal = []
    all_fam = []
    all_pe_cons = []

    current_window = 0
    progress_interval = max(1, T // 10)

    for t in range(T):
        r3_frame = r3_tensor[:, t:t+1, :]
        h3_frame = {k: v[:, t:t+1] for k, v in h3_dict.items() if v.shape[1] > t}

        out = kernel.tick(r3_frame, h3_frame)

        # Extract scalars immediately (no tensor accumulation)
        cons_v = out.beliefs["perceived_consonance"].mean().item()
        tempo_v = out.beliefs["tempo_state"].mean().item()
        sal_v = out.beliefs["salience_state"].mean().item()
        fam_v = out.beliefs["familiarity_state"].mean().item()
        rew_v = out.beliefs["reward_valence"].mean().item()
        pe_c = out.pe["perceived_consonance"].mean().item()
        pe_t = out.pe["tempo_state"].mean().item()
        pe_s = out.pe["salience_state"].mean().item()
        pe_f = out.pe["familiarity_state"].mean().item()

        # Window accumulation
        w_cons.append(cons_v)
        w_tempo.append(tempo_v)
        w_sal.append(sal_v)
        w_fam.append(fam_v)
        w_reward.append(rew_v)
        w_pe_cons.append(abs(pe_c))
        w_pe_tempo.append(abs(pe_t))
        w_pe_sal.append(abs(pe_s))
        w_pe_fam.append(abs(pe_f))

        # Global tracking
        all_reward.append(rew_v)
        all_cons.append(cons_v)
        all_sal.append(sal_v)
        all_fam.append(fam_v)
        all_pe_cons.append(abs(pe_c))

        # Window boundary
        if len(w_cons) >= window_frames or t == T - 1:
            t_start = current_window * WINDOW_SEC
            t_end = t_start + len(w_cons) / FRAME_RATE
            windows.append({
                "window": f"{t_start:.0f}-{t_end:.0f}s",
                "t_start": round(t_start, 1),
                "t_end": round(t_end, 1),
                "cons_mean": round(float(np.mean(w_cons)), 4),
                "tempo_mean": round(float(np.mean(w_tempo)), 4),
                "sal_mean": round(float(np.mean(w_sal)), 4),
                "fam_mean": round(float(np.mean(w_fam)), 4),
                "reward_mean": round(float(np.mean(w_reward)), 4),
                "reward_std": round(float(np.std(w_reward)), 4),
                "pe_cons_mean": round(float(np.mean(w_pe_cons)), 4),
                "pe_tempo_mean": round(float(np.mean(w_pe_tempo)), 4),
                "pe_sal_mean": round(float(np.mean(w_pe_sal)), 4),
                "pe_fam_mean": round(float(np.mean(w_pe_fam)), 4),
            })
            w_cons.clear(); w_tempo.clear(); w_sal.clear(); w_fam.clear()
            w_reward.clear(); w_pe_cons.clear(); w_pe_tempo.clear()
            w_pe_sal.clear(); w_pe_fam.clear()
            current_window += 1

        # Progress
        if (t + 1) % progress_interval == 0:
            elapsed = time.time() - t3
            fps = (t + 1) / elapsed
            pct = (t + 1) / T * 100
            print(f"    {pct:5.1f}% ({t+1}/{T}) — {fps:.0f} fps — "
                  f"reward={rew_v:+.4f}, cons={cons_v:.3f}, sal={sal_v:.3f}")

    c3_time = time.time() - t3
    total_time = time.time() - t0
    fps = T / c3_time

    # Convert global accumulators to numpy for stats
    all_reward = np.array(all_reward)
    all_cons = np.array(all_cons)
    all_sal = np.array(all_sal)
    all_fam = np.array(all_fam)
    all_pe_cons = np.array(all_pe_cons)

    # First/last window for adaptation analysis
    first_w = windows[0] if windows else {}
    last_w = windows[-1] if windows else {}

    # Build summary
    summary = {
        "name": name,
        "duration_s": round(duration_s, 1),
        "frames": T,
        "fps": round(fps, 0),
        "timing": {
            "r3_s": round(r3_time, 1),
            "h3_s": round(h3_time, 2),
            "c3_s": round(c3_time, 1),
            "total_s": round(total_time, 1),
        },
        "beliefs": {
            "consonance_mean": round(float(all_cons.mean()), 4),
            "consonance_std": round(float(all_cons.std()), 4),
            "consonance_range": round(float(all_cons.max() - all_cons.min()), 4),
            "salience_mean": round(float(all_sal.mean()), 4),
            "salience_std": round(float(all_sal.std()), 4),
            "salience_range": round(float(all_sal.max() - all_sal.min()), 4),
            "familiarity_mean": round(float(all_fam.mean()), 4),
            "familiarity_std": round(float(all_fam.std()), 4),
            "familiarity_range": round(float(all_fam.max() - all_fam.min()), 4),
        },
        "reward": {
            "mean": round(float(all_reward.mean()), 4),
            "std": round(float(all_reward.std()), 4),
            "min": round(float(all_reward.min()), 4),
            "max": round(float(all_reward.max()), 4),
            "range": round(float(all_reward.max() - all_reward.min()), 4),
            "pct_positive": round(float((all_reward > 0).mean() * 100), 1),
        },
        "adaptation": {
            "pe_cons_first_window": first_w.get("pe_cons_mean", 0),
            "pe_cons_last_window": last_w.get("pe_cons_mean", 0),
            "reward_first_window": first_w.get("reward_mean", 0),
            "reward_last_window": last_w.get("reward_mean", 0),
            "fam_first_window": first_w.get("fam_mean", 0),
            "fam_last_window": last_w.get("fam_mean", 0),
        },
        "windows": windows,
        "memory_mb": round(memory_mb(), 0),
    }

    print(f"\n  Done: {T} frames in {total_time:.1f}s ({fps:.0f} fps)")
    print(f"  Reward: mean={all_reward.mean():+.4f}, "
          f"range=[{all_reward.min():+.4f}, {all_reward.max():+.4f}], "
          f"{(all_reward > 0).mean()*100:.0f}% positive")
    print(f"  Memory: ~{memory_mb():.0f} MB RSS")

    # Cleanup
    del kernel, r3_tensor, h3_dict, r3_ext, r3_out
    del all_reward, all_cons, all_sal, all_fam, all_pe_cons
    hard_cleanup()

    return summary


def print_comparative(summaries: list) -> None:
    """Print comparative table across all pieces."""
    print("\n")
    print("=" * 90)
    print("  FULL-DURATION COMPARATIVE REPORT")
    print("=" * 90)

    # Header
    max_name = max(len(s["name"]) for s in summaries)
    col_w = max(max_name, 12)
    header = f"  {'Metric':<32s}"
    for s in summaries:
        header += f" | {s['name']:>{col_w}s}"
    print(f"\n{header}")
    print(f"  {'-' * (32 + (col_w + 3) * len(summaries))}")

    rows = [
        ("Duration (s)", lambda s: f"{s['duration_s']:>{col_w}.1f}"),
        ("Frames", lambda s: f"{s['frames']:>{col_w}d}"),
        ("FPS", lambda s: f"{s['fps']:>{col_w}.0f}"),
        ("", None),
        ("Consonance mean", lambda s: f"{s['beliefs']['consonance_mean']:>{col_w}.4f}"),
        ("Consonance range", lambda s: f"{s['beliefs']['consonance_range']:>{col_w}.4f}"),
        ("Salience mean", lambda s: f"{s['beliefs']['salience_mean']:>{col_w}.4f}"),
        ("Salience std", lambda s: f"{s['beliefs']['salience_std']:>{col_w}.4f}"),
        ("Familiarity mean", lambda s: f"{s['beliefs']['familiarity_mean']:>{col_w}.4f}"),
        ("Familiarity range", lambda s: f"{s['beliefs']['familiarity_range']:>{col_w}.4f}"),
        ("", None),
        ("Reward MEAN", lambda s: f"{s['reward']['mean']:>{col_w}.4f}"),
        ("Reward std", lambda s: f"{s['reward']['std']:>{col_w}.4f}"),
        ("Reward range", lambda s: f"{s['reward']['range']:>{col_w}.4f}"),
        ("Reward % positive", lambda s: f"{s['reward']['pct_positive']:>{col_w}.1f}"),
        ("", None),
        ("|PE_cons| first window", lambda s: f"{s['adaptation']['pe_cons_first_window']:>{col_w}.4f}"),
        ("|PE_cons| last window", lambda s: f"{s['adaptation']['pe_cons_last_window']:>{col_w}.4f}"),
        ("Reward first window", lambda s: f"{s['adaptation']['reward_first_window']:>{col_w}.4f}"),
        ("Reward last window", lambda s: f"{s['adaptation']['reward_last_window']:>{col_w}.4f}"),
        ("Fam first window", lambda s: f"{s['adaptation']['fam_first_window']:>{col_w}.4f}"),
        ("Fam last window", lambda s: f"{s['adaptation']['fam_last_window']:>{col_w}.4f}"),
    ]

    for label, fn in rows:
        if fn is None:
            print()
            continue
        line = f"  {label:<32s}"
        for s in summaries:
            line += f" | {fn(s)}"
        print(line)

    # Per-piece window trajectory (condensed: first 3, last 3)
    print(f"\n{'─'*90}")
    print(f"  REWARD TRAJECTORY (10s windows)")
    print(f"{'─'*90}")

    for s in summaries:
        wins = s["windows"]
        n = len(wins)
        print(f"\n  {s['name']} ({s['duration_s']:.0f}s, {n} windows):")
        print(f"    {'Window':<14s} | {'Reward':>8s} | {'Cons':>8s} | {'Sal':>8s} | "
              f"{'Fam':>8s} | {'|PE_c|':>8s} | {'|PE_t|':>8s}")
        print(f"    {'-'*72}")

        # Show first 3 + ... + last 3
        show_indices = list(range(min(3, n)))
        if n > 6:
            show_indices.append(-1)  # sentinel for ellipsis
            show_indices += list(range(n - 3, n))
        elif n > 3:
            show_indices += list(range(3, n))

        for i in show_indices:
            if i == -1:
                print(f"    {'...':^72s}")
                continue
            w = wins[i]
            print(f"    {w['window']:<14s} | {w['reward_mean']:>+8.4f} | "
                  f"{w['cons_mean']:>8.4f} | {w['sal_mean']:>8.4f} | "
                  f"{w['fam_mean']:>8.4f} | {w['pe_cons_mean']:>8.4f} | "
                  f"{w['pe_tempo_mean']:>8.4f}")

    # Diagnostic checks
    print(f"\n{'─'*90}")
    print(f"  DIAGNOSTIC CHECKS")
    print(f"{'─'*90}")

    checks = []

    # PE adaptation for each piece
    for s in summaries:
        pe_first = s["adaptation"]["pe_cons_first_window"]
        pe_last = s["adaptation"]["pe_cons_last_window"]
        ok = pe_last < pe_first
        pct = (pe_first - pe_last) / (pe_first + 1e-8) * 100
        checks.append((f"PE_cons adaptation ({s['name']}): {pct:.1f}%", ok))

    # Cross-piece consonance range
    ranges = [s["beliefs"]["consonance_range"] for s in summaries]
    spread = max(ranges) / (min(ranges) + 1e-8)
    checks.append((f"Consonance range spread > 1.2x ({spread:.2f}x)", spread > 1.2))

    # Cross-piece reward differentiation
    rew_means = [s["reward"]["mean"] for s in summaries]
    rew_spread = max(rew_means) - min(rew_means)
    checks.append((f"Reward mean spread > 0.01 ({rew_spread:.4f})", rew_spread > 0.01))

    # Familiarity differentiation
    fam_means = [s["beliefs"]["familiarity_mean"] for s in summaries]
    fam_spread = max(fam_means) - min(fam_means)
    checks.append((f"Familiarity mean spread > 0.02 ({fam_spread:.4f})", fam_spread > 0.02))

    # Salience std spread
    sal_stds = [s["beliefs"]["salience_std"] for s in summaries]
    sal_spread = max(sal_stds) / (min(sal_stds) + 1e-8)
    checks.append((f"Salience std spread > 1.2x ({sal_spread:.2f}x)", sal_spread > 1.2))

    # Reward positive percentage > 20% for at least one piece
    pct_pos = [s["reward"]["pct_positive"] for s in summaries]
    checks.append((f"Any piece > 30% positive reward ({max(pct_pos):.0f}%)", max(pct_pos) > 30))

    # Full-duration familiarity drift
    for s in summaries:
        fam_drift = s["adaptation"]["fam_last_window"] - s["adaptation"]["fam_first_window"]
        checks.append((
            f"Familiarity drift > 0.02 ({s['name']}): {fam_drift:+.4f}",
            abs(fam_drift) > 0.02,
        ))

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)

    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"    [{status}] {label}")
    print(f"\n    SCORE: {passed}/{total}")

    print(f"\n{'='*90}")
    print(f"  END OF REPORT")
    print(f"{'='*90}")


def main() -> None:
    print("=" * 70)
    print("  FULL-DURATION C³ KERNEL TEST")
    print("  CPU-only | no_grad | serial | memory-safe")
    print("=" * 70)
    print(f"  Device: CPU (MPS disabled for stability)")
    print(f"  torch.is_grad_enabled() = {torch.is_grad_enabled()}")
    print(f"  Process RSS at start: {memory_mb():.0f} MB")

    summaries = []
    for name, path in PIECES:
        if not os.path.exists(path):
            print(f"\n  SKIP: {name} — file not found")
            continue

        summary = run_single_piece(name, path)
        summaries.append(summary)
        hard_cleanup()
        print(f"  Memory after cleanup: {memory_mb():.0f} MB")

    if len(summaries) < 2:
        print("Need at least 2 pieces for comparative analysis.")
        return

    print_comparative(summaries)

    # Save JSON
    out_path = os.path.join(_PROJECT_ROOT, "Tests", "experiments",
                             "full_duration_results.json")
    with open(out_path, "w") as f:
        json.dump(summaries, f, indent=2)
    print(f"\n  Results saved to: {out_path}")


if __name__ == "__main__":
    main()
