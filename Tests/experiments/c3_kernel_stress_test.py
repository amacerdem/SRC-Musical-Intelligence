#!/usr/bin/env python3
"""C³ Kernel Stress Test — 3-Piece Comparative.

Compares C³ Kernel belief dynamics on three contrasting pieces:
  - Swan Lake:            orchestral, tonal waltz, predictable
  - Bach Cello Suite:     solo cello, monophonic, contrapuntal clarity
  - Beethoven Pathétique: solo piano, dramatic Grave→Allegro, harmonic tension

Tests whether the architecture produces meaningfully different dynamics:
  - PE magnitude and variance
  - Reward polarity shift
  - Consonance/tempo dynamic range
  - Prediction accuracy differences

Usage:
    python Tests/experiments/c3_kernel_stress_test.py
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
SR = 44100
HOP = 256
N_MELS = 128
DURATION = 30  # seconds

PIECES = {
    "Swan Lake": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
        " - Pyotr Ilyich Tchaikovsky.wav",
    ),
    "Bach Cello": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    ),
    "Beethoven Pathétique": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    ),
}


def run_pipeline(name: str, path: str) -> dict:
    """Run full Audio → R³ → H³ → C³ Kernel pipeline on a piece."""
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")

    # ── 1. Load audio ──────────────────────────────────────────────
    print(f"\n  [1/4] Loading audio...")
    t0 = time.time()
    waveform, sr = librosa.load(path, sr=SR, duration=DURATION, mono=True)
    waveform_t = torch.from_numpy(waveform).unsqueeze(0).float()
    actual_dur = waveform.shape[0] / SR
    print(f"    Audio: {actual_dur:.1f}s, {sr}Hz")

    # ── 2. Mel + R³ ───────────────────────────────────────────────
    mel_np = librosa.feature.melspectrogram(
        y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP
    )
    mel_db = librosa.power_to_db(mel_np, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.from_numpy(mel_norm).unsqueeze(0).float()  # (1, 128, T)
    T = mel_t.shape[2]

    print(f"  [2/4] R³ extraction...")
    t1 = time.time()
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t, audio=waveform_t, sr=SR)
    r3_tensor = r3_out.features  # (1, T, 128)
    feature_map = r3_out.feature_map
    r3_time = time.time() - t1
    print(f"    R³: {r3_tensor.shape}, {r3_time:.2f}s")

    # ── 3. H³ ─────────────────────────────────────────────────────
    print(f"  [3/4] H³ extraction...")
    t2 = time.time()
    # Build H³ demand set from kernel (beliefs + BCH L0 demands, deduped)
    kernel_tmp = C3Kernel(feature_map)
    demand = kernel_tmp.h3_demands()

    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, demand)
    h3_dict = h3_out.features
    h3_time = time.time() - t2
    print(f"    H³: {len(h3_dict)} tuples, {h3_time:.2f}s")

    # ── 4. C³ Kernel ──────────────────────────────────────────────
    print(f"  [4/4] C³ Kernel belief cycle...")
    t3 = time.time()
    kernel = C3Kernel(feature_map)

    traces = {
        "perceived_consonance": [],
        "tempo_state": [],
        "salience_state": [],
        "familiarity_state": [],
        "reward_valence": [],
        "pe_consonance": [],
        "pe_tempo": [],
        "pe_salience": [],
        "pe_familiarity": [],
    }

    for t in range(T):
        r3_frame = r3_tensor[:, t:t+1, :]
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
        traces["salience_state"].append(
            out.beliefs["salience_state"].mean().item()
        )
        traces["familiarity_state"].append(
            out.beliefs["familiarity_state"].mean().item()
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
        traces["pe_salience"].append(
            out.pe["salience_state"].mean().item()
        )
        traces["pe_familiarity"].append(
            out.pe["familiarity_state"].mean().item()
        )

    c3_time = time.time() - t3
    total_time = time.time() - t0
    print(f"    C³: {T} frames, {c3_time:.2f}s ({T/c3_time:.0f} fps)")
    print(f"    Total: {total_time:.1f}s")

    # Convert to numpy
    for k in traces:
        traces[k] = np.array(traces[k])

    return {
        "name": name,
        "T": T,
        "traces": traces,
        "timing": {
            "r3": r3_time, "h3": h3_time, "c3": c3_time, "total": total_time
        },
    }


def analyze_piece(result: dict) -> dict:
    """Compute statistics for a single piece."""
    tr = result["traces"]
    T = result["T"]
    frame_rate = SR / HOP
    window_frames = int(5 * frame_rate)
    n_windows = T // window_frames

    stats = {
        "name": result["name"],
        "T": T,
        "duration": T / frame_rate,
    }

    for key in ["perceived_consonance", "tempo_state", "salience_state",
                "familiarity_state", "reward_valence",
                "pe_consonance", "pe_tempo", "pe_salience", "pe_familiarity"]:
        arr = tr[key]
        stats[key] = {
            "mean": float(arr.mean()),
            "std": float(arr.std()),
            "min": float(arr.min()),
            "max": float(arr.max()),
            "range": float(arr.max() - arr.min()),
        }

    # Per-window analysis
    windows = []
    for w in range(n_windows):
        s = w * window_frames
        e = (w + 1) * window_frames
        t_start = s / frame_rate
        t_end = e / frame_rate
        windows.append({
            "window": f"{t_start:.0f}-{t_end:.0f}s",
            "cons_mean": float(tr["perceived_consonance"][s:e].mean()),
            "tempo_mean": float(tr["tempo_state"][s:e].mean()),
            "sal_mean": float(tr["salience_state"][s:e].mean()),
            "fam_mean": float(tr["familiarity_state"][s:e].mean()),
            "reward_mean": float(tr["reward_valence"][s:e].mean()),
            "pe_cons_std": float(tr["pe_consonance"][s:e].std()),
            "pe_tempo_std": float(tr["pe_tempo"][s:e].std()),
            "pe_cons_mean": float(np.abs(tr["pe_consonance"][s:e]).mean()),
            "pe_tempo_mean": float(np.abs(tr["pe_tempo"][s:e]).mean()),
            "pe_sal_mean": float(np.abs(tr["pe_salience"][s:e]).mean()),
            "pe_fam_mean": float(np.abs(tr["pe_familiarity"][s:e]).mean()),
        })
    stats["windows"] = windows

    # First 5s vs last 5s (adaptation test)
    first = slice(0, window_frames)
    last = slice(-window_frames, None)
    stats["adaptation"] = {
        "pe_cons_first5s": float(np.abs(tr["pe_consonance"][first]).mean()),
        "pe_cons_last5s": float(np.abs(tr["pe_consonance"][last]).mean()),
        "pe_tempo_first5s": float(np.abs(tr["pe_tempo"][first]).mean()),
        "pe_tempo_last5s": float(np.abs(tr["pe_tempo"][last]).mean()),
        "pe_sal_first5s": float(np.abs(tr["pe_salience"][first]).mean()),
        "pe_sal_last5s": float(np.abs(tr["pe_salience"][last]).mean()),
        "pe_fam_first5s": float(np.abs(tr["pe_familiarity"][first]).mean()),
        "pe_fam_last5s": float(np.abs(tr["pe_familiarity"][last]).mean()),
        "sal_first5s": float(tr["salience_state"][first].mean()),
        "sal_last5s": float(tr["salience_state"][last].mean()),
        "fam_first5s": float(tr["familiarity_state"][first].mean()),
        "fam_last5s": float(tr["familiarity_state"][last].mean()),
        "reward_first5s": float(tr["reward_valence"][first].mean()),
        "reward_last5s": float(tr["reward_valence"][last].mean()),
    }

    return stats


def print_report(stats_list: list) -> None:
    """Print comparative report for all pieces."""
    print("\n")
    print("=" * 80)
    print("  C³ KERNEL COMPARATIVE STRESS TEST REPORT")
    print("=" * 80)

    # ── Section 1: Overview ────────────────────────────────────────
    print("\n" + "─" * 80)
    print("  1. OVERVIEW")
    print("─" * 80)

    header = f"{'Metric':<30s}"
    for s in stats_list:
        header += f" | {s['name']:>18s}"
    print(header)
    print("-" * (30 + 21 * len(stats_list)))

    rows = [
        ("Frames", lambda s: f"{s['T']:>18d}"),
        ("Duration (s)", lambda s: f"{s['duration']:>18.1f}"),
    ]
    for label, fn in rows:
        line = f"{label:<30s}"
        for s in stats_list:
            line += f" | {fn(s)}"
        print(line)

    # ── Section 2: Belief Dynamics ─────────────────────────────────
    print("\n" + "─" * 80)
    print("  2. BELIEF DYNAMICS")
    print("─" * 80)

    for belief in ["perceived_consonance", "tempo_state", "salience_state",
                    "familiarity_state", "reward_valence"]:
        bname = belief.replace("_", " ").title()
        print(f"\n  {bname}:")
        for metric in ["mean", "std", "min", "max", "range"]:
            line = f"    {metric:<26s}"
            for s in stats_list:
                val = s[belief][metric]
                line += f" | {val:>18.4f}"
            print(line)

    # ── Section 3: Prediction Error ────────────────────────────────
    print("\n" + "─" * 80)
    print("  3. PREDICTION ERROR (PE)")
    print("─" * 80)

    for pe_key in ["pe_consonance", "pe_tempo", "pe_salience", "pe_familiarity"]:
        pname = pe_key.replace("_", " ").title()
        print(f"\n  {pname}:")
        for metric in ["mean", "std", "min", "max", "range"]:
            line = f"    {metric:<26s}"
            for s in stats_list:
                val = s[pe_key][metric]
                line += f" | {val:>18.4f}"
            print(line)

    # ── Section 4: Temporal Adaptation ─────────────────────────────
    print("\n" + "─" * 80)
    print("  4. TEMPORAL ADAPTATION (first 5s vs last 5s)")
    print("─" * 80)

    adapt_metrics = [
        ("|PE_cons| first 5s",  "pe_cons_first5s"),
        ("|PE_cons| last 5s",   "pe_cons_last5s"),
        ("PE_cons reduction %", None),
        ("|PE_tempo| first 5s", "pe_tempo_first5s"),
        ("|PE_tempo| last 5s",  "pe_tempo_last5s"),
        ("PE_tempo reduction %", None),
        ("|PE_sal| first 5s",   "pe_sal_first5s"),
        ("|PE_sal| last 5s",    "pe_sal_last5s"),
        ("PE_sal reduction %",  None),
        ("|PE_fam| first 5s",   "pe_fam_first5s"),
        ("|PE_fam| last 5s",    "pe_fam_last5s"),
        ("PE_fam reduction %",  None),
        ("Salience first 5s",   "sal_first5s"),
        ("Salience last 5s",    "sal_last5s"),
        ("Salience drift",      None),
        ("Familiarity first 5s", "fam_first5s"),
        ("Familiarity last 5s",  "fam_last5s"),
        ("Familiarity drift",    None),
        ("Reward first 5s",     "reward_first5s"),
        ("Reward last 5s",      "reward_last5s"),
        ("Reward drift",        None),
    ]

    for label, key in adapt_metrics:
        line = f"    {label:<26s}"
        for s in stats_list:
            a = s["adaptation"]
            if key is not None:
                line += f" | {a[key]:>18.4f}"
            elif "cons reduction" in label:
                f5 = a["pe_cons_first5s"]
                l5 = a["pe_cons_last5s"]
                pct = (f5 - l5) / (f5 + 1e-8) * 100
                line += f" | {pct:>17.1f}%"
            elif "tempo reduction" in label:
                f5 = a["pe_tempo_first5s"]
                l5 = a["pe_tempo_last5s"]
                pct = (f5 - l5) / (f5 + 1e-8) * 100
                line += f" | {pct:>17.1f}%"
            elif "sal reduction" in label:
                f5 = a["pe_sal_first5s"]
                l5 = a["pe_sal_last5s"]
                pct = (f5 - l5) / (f5 + 1e-8) * 100
                line += f" | {pct:>17.1f}%"
            elif "fam reduction" in label:
                f5 = a["pe_fam_first5s"]
                l5 = a["pe_fam_last5s"]
                pct = (f5 - l5) / (f5 + 1e-8) * 100
                line += f" | {pct:>17.1f}%"
            elif "Salience drift" in label:
                drift = a["sal_last5s"] - a["sal_first5s"]
                line += f" | {drift:>18.4f}"
            elif "Familiarity drift" in label:
                drift = a["fam_last5s"] - a["fam_first5s"]
                line += f" | {drift:>18.4f}"
            elif "Reward drift" in label:
                drift = a["reward_last5s"] - a["reward_first5s"]
                line += f" | {drift:>18.4f}"
        print(line)

    # ── Section 5: Window-by-Window ────────────────────────────────
    print("\n" + "─" * 80)
    print("  5. WINDOW-BY-WINDOW (5s windows)")
    print("─" * 80)

    for s in stats_list:
        print(f"\n  {s['name']}:")
        print(f"    {'Window':<10s} | {'Cons':>8s} | {'Tempo':>8s} | "
              f"{'Salin':>8s} | {'Famil':>8s} | {'Reward':>8s} | "
              f"{'|PE_c|':>8s} | {'|PE_t|':>8s} | {'|PE_s|':>8s} | "
              f"{'|PE_f|':>8s}")
        print(f"    {'-'*100}")
        for w in s["windows"]:
            print(f"    {w['window']:<10s} | {w['cons_mean']:>8.4f} | "
                  f"{w['tempo_mean']:>8.4f} | {w['sal_mean']:>8.4f} | "
                  f"{w['fam_mean']:>8.4f} | {w['reward_mean']:>8.4f} | "
                  f"{w['pe_cons_mean']:>8.4f} | {w['pe_tempo_mean']:>8.4f} | "
                  f"{w['pe_sal_mean']:>8.4f} | {w['pe_fam_mean']:>8.4f}")

    # ── Section 6: Diagnostic Verdict ──────────────────────────────
    print("\n" + "─" * 80)
    print("  6. DIAGNOSTIC VERDICT")
    print("─" * 80)

    if len(stats_list) < 2:
        print("\n    Need at least 2 pieces for comparative diagnostics.")
        return

    # ── 6a: Cross-piece comparison table ─────────────────────────
    metrics_to_compare = [
        ("Consonance range",    lambda s: s["perceived_consonance"]["range"]),
        ("Consonance mean",     lambda s: s["perceived_consonance"]["mean"]),
        ("Consonance std",      lambda s: s["perceived_consonance"]["std"]),
        ("Tempo range",         lambda s: s["tempo_state"]["range"]),
        ("Tempo mean",          lambda s: s["tempo_state"]["mean"]),
        ("Salience mean",       lambda s: s["salience_state"]["mean"]),
        ("Salience std",        lambda s: s["salience_state"]["std"]),
        ("Salience range",      lambda s: s["salience_state"]["range"]),
        ("Familiarity mean",    lambda s: s["familiarity_state"]["mean"]),
        ("Familiarity range",   lambda s: s["familiarity_state"]["range"]),
        ("Reward mean",         lambda s: s["reward_valence"]["mean"]),
        ("Reward range",        lambda s: s["reward_valence"]["range"]),
        ("PE_cons std",         lambda s: s["pe_consonance"]["std"]),
        ("PE_tempo std",        lambda s: s["pe_tempo"]["std"]),
        ("PE_sal std",          lambda s: s["pe_salience"]["std"]),
        ("PE_fam std",          lambda s: s["pe_familiarity"]["std"]),
        ("PE_cons adapt %",     lambda s: (
            (s["adaptation"]["pe_cons_first5s"] - s["adaptation"]["pe_cons_last5s"])
            / (s["adaptation"]["pe_cons_first5s"] + 1e-8) * 100
        )),
    ]

    # Determine column width from longest name
    max_name = max(len(s["name"]) for s in stats_list)
    col_w = max(max_name, 12)

    header = f"    {'Metric':<22s}"
    for s in stats_list:
        header += f" | {s['name']:>{col_w}s}"
    print(f"\n{header}")
    print(f"    {'-' * (22 + (col_w + 3) * len(stats_list))}")

    for label, fn in metrics_to_compare:
        line = f"    {label:<22s}"
        vals = [fn(s) for s in stats_list]
        best_idx = vals.index(max(vals))
        for i, v in enumerate(vals):
            marker = " *" if i == best_idx else "  "
            line += f" | {v:>{col_w - 2}.4f}{marker}"
        print(line)

    # ── 6b: Per-piece checks ─────────────────────────────────────
    print(f"\n    CHECKS:")
    checks = []

    for s in stats_list:
        name = s["name"]
        # PE should decrease over time for every piece
        pe_decr = s["adaptation"]["pe_cons_first5s"] > s["adaptation"]["pe_cons_last5s"]
        checks.append((f"PE_cons decreases over time ({name})", pe_decr))

    # Cross-piece: pieces should have distinguishable consonance ranges
    ranges = [s["perceived_consonance"]["range"] for s in stats_list]
    spread = max(ranges) / (min(ranges) + 1e-8)
    checks.append((
        f"Consonance range spread > 1.2x (actual {spread:.2f}x)",
        spread > 1.2,
    ))

    # Cross-piece: PE_cons std should vary across pieces
    pe_stds = [s["pe_consonance"]["std"] for s in stats_list]
    pe_spread = max(pe_stds) / (min(pe_stds) + 1e-8)
    checks.append((
        f"PE_cons std spread > 1.2x (actual {pe_spread:.2f}x)",
        pe_spread > 1.2,
    ))

    # Cross-piece: reward should differ
    rew_means = [s["reward_valence"]["mean"] for s in stats_list]
    rew_spread = max(rew_means) - min(rew_means)
    checks.append((
        f"Reward mean spread > 0.01 (actual {rew_spread:.4f})",
        rew_spread > 0.01,
    ))

    # Cross-piece: tempo should differ
    tempo_ranges = [s["tempo_state"]["range"] for s in stats_list]
    tempo_spread = max(tempo_ranges) / (min(tempo_ranges) + 1e-8)
    checks.append((
        f"Tempo range spread > 1.2x (actual {tempo_spread:.2f}x)",
        tempo_spread > 1.2,
    ))

    # Cross-piece: familiarity should differ (key new check)
    fam_means = [s["familiarity_state"]["mean"] for s in stats_list]
    fam_spread = max(fam_means) - min(fam_means)
    checks.append((
        f"Familiarity mean spread > 0.02 (actual {fam_spread:.4f})",
        fam_spread > 0.02,
    ))

    # Salience should NOT be constant 1.0 (proves it's active)
    sal_ranges = [s["salience_state"]["range"] for s in stats_list]
    sal_active = all(r > 0.01 for r in sal_ranges)
    checks.append((
        f"Salience active (range > 0.01 for all pieces)",
        sal_active,
    ))

    # Salience std should vary across pieces
    sal_stds = [s["salience_state"]["std"] for s in stats_list]
    sal_spread = max(sal_stds) / (min(sal_stds) + 1e-8)
    checks.append((
        f"Salience std spread > 1.2x (actual {sal_spread:.2f}x)",
        sal_spread > 1.2,
    ))

    # Familiarity should NOT be constant 0.5 (proves it's active)
    fam_ranges = [s["familiarity_state"]["range"] for s in stats_list]
    fam_active = all(r > 0.01 for r in fam_ranges)
    checks.append((
        f"Familiarity active (range > 0.01 for all pieces)",
        fam_active,
    ))

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)

    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"      [{status}] {label}")

    print(f"\n    SCORE: {passed}/{total} diagnostic checks passed")

    print("\n" + "=" * 80)
    print("  END OF REPORT")
    print("=" * 80)


def main() -> None:
    results = []
    for name, path in PIECES.items():
        if not os.path.exists(path):
            print(f"  SKIP: {name} — file not found: {path}")
            continue
        result = run_pipeline(name, path)
        results.append(result)

    if not results:
        print("No audio files found!")
        return

    # Analyze all pieces
    all_stats = [analyze_piece(r) for r in results]

    # Print comparative report
    print_report(all_stats)


if __name__ == "__main__":
    main()
