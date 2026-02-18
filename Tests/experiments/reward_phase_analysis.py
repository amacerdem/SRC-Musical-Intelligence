#!/usr/bin/env python3
"""Reward Phase-Plane Analysis — Decompose reward into 4 components.

Runs the C³ Kernel on 3 test pieces and decomposes reward into:
  surprise, resolution, exploration, monotony

Key questions answered:
  1. What % of negative reward comes from monotony?
  2. Where is the break-even |PE| for each piece?
  3. How does salience gate (or fail to gate) reward?
  4. Per-horizon component breakdown (multi-scale)

Usage:
    python Tests/experiments/reward_phase_analysis.py
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import time
import numpy as np
import torch
import librosa

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.kernel.scheduler import C3Kernel

# ── Constants ───────────────────────────────────────────────────────
SR = 44100
HOP = 256
N_MELS = 128
DURATION = 30

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
    "Beethoven": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    ),
}

# Reward config (must match RewardConfig defaults — v2.5 surprise-dominant)
W_SURPRISE = 1.5
W_RESOLUTION = 0.8
W_EXPLORATION = 0.5
W_MONOTONY = 0.6


def run_piece(name: str, path: str) -> dict:
    """Run pipeline and capture per-frame reward components."""
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")

    # Load audio
    waveform, sr = librosa.load(path, sr=SR, duration=DURATION, mono=True)
    waveform_t = torch.from_numpy(waveform).unsqueeze(0).float()

    # Mel + R³
    mel_np = librosa.feature.melspectrogram(y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP)
    mel_db = librosa.power_to_db(mel_np, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.from_numpy(mel_norm).unsqueeze(0).float()
    T = mel_t.shape[2]

    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t, audio=waveform_t, sr=SR)
    r3_tensor = r3_out.features
    feature_map = r3_out.feature_map

    # H³
    kernel_tmp = C3Kernel(feature_map)
    demand = kernel_tmp.h3_demands()
    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, demand)
    h3_dict = h3_out.features

    # C³ Kernel + reward decomposition
    kernel = C3Kernel(feature_map)

    # Per-frame traces
    traces = {
        "salience": [], "familiarity": [], "reward": [],
        "pe_cons": [], "pe_tempo": [],
        "pi_pred_cons": [], "pi_pred_tempo": [],
        # Reward components (reconstructed)
        "surprise_cons": [], "resolution_cons": [], "exploration_cons": [], "monotony_cons": [],
        "surprise_tempo": [], "resolution_tempo": [], "exploration_tempo": [], "monotony_tempo": [],
        "reward_pre_fam": [],  # before familiarity modulation
        # Per-horizon (consonance multi-scale)
        "ms_surprise": {}, "ms_resolution": {}, "ms_exploration": {}, "ms_monotony": {},
        "ms_pe": {}, "ms_pi_pred": {},
    }

    t0 = time.time()
    for t in range(T):
        r3_frame = r3_tensor[:, t:t+1, :]
        h3_frame = {k: v[:, t:t+1] for k, v in h3_dict.items() if v.shape[1] > t}

        out = kernel.tick(r3_frame, h3_frame)

        sal = out.beliefs["salience_state"].mean().item()
        fam = out.beliefs["familiarity_state"].mean().item()
        rew = out.beliefs["reward_valence"].mean().item()

        traces["salience"].append(sal)
        traces["familiarity"].append(fam)
        traces["reward"].append(rew)

        # Single-scale PE + precision
        pe_c = out.pe["perceived_consonance"].mean().item()
        pe_t = out.pe["tempo_state"].mean().item()
        traces["pe_cons"].append(pe_c)
        traces["pe_tempo"].append(pe_t)

        pi_c = out.precision_pred["perceived_consonance"].item() if out.precision_pred["perceived_consonance"].numel() == 1 else out.precision_pred["perceived_consonance"].mean().item()
        pi_t = out.precision_pred["tempo_state"].item() if out.precision_pred["tempo_state"].numel() == 1 else out.precision_pred["tempo_state"].mean().item()
        traces["pi_pred_cons"].append(pi_c)
        traces["pi_pred_tempo"].append(pi_t)

        # Reconstruct single-scale tempo components
        pi_norm_t = min(max(pi_t / 10.0, 0.0), 1.0)
        pe_abs_t = abs(pe_t)
        s_t = pe_abs_t * pi_norm_t * (1.0 - fam)
        r_t = max(1.0 - pe_abs_t, 0.0) * pi_norm_t * fam
        e_t = pe_abs_t * (1.0 - pi_norm_t)
        m_t = pi_norm_t ** 2
        traces["surprise_tempo"].append(s_t)
        traces["resolution_tempo"].append(r_t)
        traces["exploration_tempo"].append(e_t)
        traces["monotony_tempo"].append(m_t)

        # Multi-scale consonance components
        ms_pe_cons = out.ms_pe.get("perceived_consonance", {})
        ms_pi_cons = out.ms_precision_pred.get("perceived_consonance", {})

        # Aggregate consonance components across horizons
        n_h = max(len(ms_pe_cons), 1)
        cons_surprise_total = 0.0
        cons_resolution_total = 0.0
        cons_exploration_total = 0.0
        cons_monotony_total = 0.0

        for h, pe_h_tensor in ms_pe_cons.items():
            if pe_h_tensor.dim() < 2:
                continue
            pe_h_val = pe_h_tensor.mean().item()
            pi_h_raw = ms_pi_cons.get(h, torch.tensor(pi_c)).item() if h in ms_pi_cons else pi_c
            pi_h = min(max(pi_h_raw / 10.0, 0.0), 1.0)
            pe_abs_h = abs(pe_h_val)
            w_h = 1.0 / n_h

            s_h = pe_abs_h * pi_h * (1.0 - fam)
            r_h = max(1.0 - pe_abs_h, 0.0) * pi_h * fam
            e_h = pe_abs_h * (1.0 - pi_h)
            m_h = pi_h ** 2

            cons_surprise_total += w_h * s_h
            cons_resolution_total += w_h * r_h
            cons_exploration_total += w_h * e_h
            cons_monotony_total += w_h * m_h

            # Per-horizon trace
            if h not in traces["ms_surprise"]:
                traces["ms_surprise"][h] = []
                traces["ms_resolution"][h] = []
                traces["ms_exploration"][h] = []
                traces["ms_monotony"][h] = []
                traces["ms_pe"][h] = []
                traces["ms_pi_pred"][h] = []
            traces["ms_surprise"][h].append(s_h)
            traces["ms_resolution"][h].append(r_h)
            traces["ms_exploration"][h].append(e_h)
            traces["ms_monotony"][h].append(m_h)
            traces["ms_pe"][h].append(pe_abs_h)
            traces["ms_pi_pred"][h].append(pi_h)

        traces["surprise_cons"].append(cons_surprise_total)
        traces["resolution_cons"].append(cons_resolution_total)
        traces["exploration_cons"].append(cons_exploration_total)
        traces["monotony_cons"].append(cons_monotony_total)

        # Pre-familiarity-mod reward
        weighted_sum = (
            sal * (
                W_SURPRISE * (cons_surprise_total + s_t)
                + W_RESOLUTION * (cons_resolution_total + r_t)
                + W_EXPLORATION * (cons_exploration_total + e_t)
                - W_MONOTONY * (cons_monotony_total + m_t)
            )
        )
        traces["reward_pre_fam"].append(weighted_sum)

    elapsed = time.time() - t0
    print(f"  {T} frames, {elapsed:.1f}s ({T/elapsed:.0f} fps)")

    # Convert to numpy
    for k in ["salience", "familiarity", "reward", "pe_cons", "pe_tempo",
              "pi_pred_cons", "pi_pred_tempo",
              "surprise_cons", "resolution_cons", "exploration_cons", "monotony_cons",
              "surprise_tempo", "resolution_tempo", "exploration_tempo", "monotony_tempo",
              "reward_pre_fam"]:
        traces[k] = np.array(traces[k])
    for component in ["ms_surprise", "ms_resolution", "ms_exploration",
                       "ms_monotony", "ms_pe", "ms_pi_pred"]:
        for h in traces[component]:
            traces[component][h] = np.array(traces[component][h])

    return {"name": name, "T": T, "traces": traces}


def analyze_phase_space(results: list) -> None:
    """Print phase-space decomposition report."""

    print("\n")
    print("=" * 80)
    print("  REWARD PHASE-PLANE ANALYSIS")
    print("=" * 80)

    # ── Section 1: Component Means ────────────────────────────────
    print("\n" + "─" * 80)
    print("  1. REWARD COMPONENT MEANS (weighted)")
    print("─" * 80)

    header = f"  {'Component':<32s}"
    for r in results:
        header += f" | {r['name']:>14s}"
    print(header)
    print("  " + "-" * (32 + 17 * len(results)))

    for label, key_c, key_t, weight in [
        ("w1×surprise", "surprise_cons", "surprise_tempo", W_SURPRISE),
        ("w2×resolution", "resolution_cons", "resolution_tempo", W_RESOLUTION),
        ("w3×exploration", "exploration_cons", "exploration_tempo", W_EXPLORATION),
        ("w4×monotony (SUBTRACTED)", "monotony_cons", "monotony_tempo", W_MONOTONY),
    ]:
        line = f"  {label:<32s}"
        for r in results:
            tr = r["traces"]
            total = weight * (tr[key_c].mean() + tr[key_t].mean())
            line += f" | {total:>14.4f}"
        print(line)

    # Net pre-familiarity
    line = f"  {'NET (pre-fam-mod)':<32s}"
    for r in results:
        tr = r["traces"]
        line += f" | {tr['reward_pre_fam'].mean():>14.4f}"
    print(line)

    # Familiarity mod
    line = f"  {'Familiarity mod multiplier':<32s}"
    for r in results:
        fam = r["traces"]["familiarity"].mean()
        fam_mod = 4.0 * fam * (1.0 - fam)
        mult = 0.5 + 0.5 * fam_mod
        line += f" | {mult:>14.4f}"
    print(line)

    # Final reward
    line = f"  {'FINAL reward mean':<32s}"
    for r in results:
        line += f" | {r['traces']['reward'].mean():>14.4f}"
    print(line)

    # ── Section 2: Monotony Dominance ─────────────────────────────
    print("\n" + "─" * 80)
    print("  2. MONOTONY DOMINANCE ANALYSIS")
    print("─" * 80)

    for r in results:
        tr = r["traces"]
        total_positive = (
            W_SURPRISE * (tr["surprise_cons"].mean() + tr["surprise_tempo"].mean())
            + W_RESOLUTION * (tr["resolution_cons"].mean() + tr["resolution_tempo"].mean())
            + W_EXPLORATION * (tr["exploration_cons"].mean() + tr["exploration_tempo"].mean())
        )
        total_negative = W_MONOTONY * (tr["monotony_cons"].mean() + tr["monotony_tempo"].mean())
        ratio = total_negative / (total_positive + 1e-8) * 100

        print(f"\n  {r['name']}:")
        print(f"    Positive (S+R+E):  {total_positive:.4f}")
        print(f"    Negative (M):      {total_negative:.4f}")
        print(f"    Monotony/Positive: {ratio:.1f}%")
        print(f"    Net balance:       {total_positive - total_negative:+.4f}")

        # Break-even PE
        fam = tr["familiarity"].mean()
        sal = tr["salience"].mean()
        pi_c = min(tr["pi_pred_cons"].mean() / 10.0, 1.0)
        pi_t = min(tr["pi_pred_tempo"].mean() / 10.0, 1.0)

        # For cons (dominant belief): w1*|PE|*pi*(1-f) + w2*(1-|PE|)*pi*f + w3*|PE|*(1-pi) - w4*pi²
        # Break-even: reward_h = 0 → solve for |PE|
        # A*|PE| + B*(1-|PE|) + C*|PE| - D = 0
        # (A+C-B)*|PE| + B - D = 0
        # |PE| = (D - B) / (A + C - B)
        A = W_SURPRISE * pi_c * (1.0 - fam)
        B = W_RESOLUTION * pi_c * fam
        C = W_EXPLORATION * (1.0 - pi_c)
        D = W_MONOTONY * pi_c ** 2
        denom = A + C - B
        if abs(denom) > 1e-8:
            pe_break = (D - B) / denom
            print(f"    Break-even |PE| (cons): {pe_break:.3f}")
            pe_actual = np.abs(tr["pe_cons"]).mean()
            print(f"    Actual mean |PE_cons|:  {pe_actual:.3f}")
            if pe_actual > pe_break > 0:
                print(f"    → ABOVE break-even → consonance reward NEGATIVE")
            elif pe_break > 0:
                print(f"    → BELOW break-even → consonance reward POSITIVE")
            else:
                print(f"    → Break-even negative (resolution always wins)")

        # Same for tempo
        A_t = W_SURPRISE * pi_t * (1.0 - fam)
        B_t = W_RESOLUTION * pi_t * fam
        C_t = W_EXPLORATION * (1.0 - pi_t)
        D_t = W_MONOTONY * pi_t ** 2
        denom_t = A_t + C_t - B_t
        if abs(denom_t) > 1e-8:
            pe_break_t = (D_t - B_t) / denom_t
            pe_actual_t = np.abs(tr["pe_tempo"]).mean()
            print(f"    Break-even |PE| (tempo): {pe_break_t:.3f}")
            print(f"    Actual mean |PE_tempo|:  {pe_actual_t:.3f}")

    # ── Section 3: Salience Gating Effect ─────────────────────────
    print("\n" + "─" * 80)
    print("  3. SALIENCE GATING ANALYSIS")
    print("─" * 80)

    for r in results:
        tr = r["traces"]
        sal = tr["salience"]
        print(f"\n  {r['name']}:")
        print(f"    Salience mean:    {sal.mean():.4f}")
        print(f"    Salience std:     {sal.std():.4f}")
        print(f"    Salience range:   [{sal.min():.4f}, {sal.max():.4f}]")
        print(f"    Salience < 0.2:   {(sal < 0.2).sum()} / {len(sal)} frames ({(sal < 0.2).mean()*100:.1f}%)")
        print(f"    Salience > 0.5:   {(sal > 0.5).sum()} / {len(sal)} frames ({(sal > 0.5).mean()*100:.1f}%)")

        # What reward would look like if salience were more dynamic
        # Hypothetical: salience_hyp = sigmoid(3 * (salience - mean))
        sal_centered = sal - sal.mean()
        sal_hyp = 1.0 / (1.0 + np.exp(-5.0 * sal_centered))
        print(f"    Hypothetical dynamic salience range: [{sal_hyp.min():.3f}, {sal_hyp.max():.3f}]")
        print(f"    Hypothetical salience std:           {sal_hyp.std():.3f}")

    # ── Section 4: Per-Horizon Decomposition ──────────────────────
    print("\n" + "─" * 80)
    print("  4. PER-HORIZON COMPONENT DECOMPOSITION (consonance)")
    print("─" * 80)

    for r in results:
        tr = r["traces"]
        horizons = sorted(tr["ms_surprise"].keys())
        if not horizons:
            print(f"\n  {r['name']}: No multi-scale data")
            continue

        print(f"\n  {r['name']}:")
        print(f"    {'H':>4s} | {'|PE|':>8s} | {'π_pred':>8s} | "
              f"{'Surpr':>8s} | {'Resol':>8s} | {'Explr':>8s} | {'Monot':>8s} | {'Net':>8s}")
        print(f"    {'-'*74}")

        for h in horizons:
            pe_mean = tr["ms_pe"][h].mean()
            pi_mean = tr["ms_pi_pred"][h].mean()
            s_mean = tr["ms_surprise"][h].mean()
            r_mean = tr["ms_resolution"][h].mean()
            e_mean = tr["ms_exploration"][h].mean()
            m_mean = tr["ms_monotony"][h].mean()
            net = W_SURPRISE * s_mean + W_RESOLUTION * r_mean + W_EXPLORATION * e_mean - W_MONOTONY * m_mean

            print(f"    H{h:>2d}  | {pe_mean:>8.4f} | {pi_mean:>8.4f} | "
                  f"{s_mean:>8.4f} | {r_mean:>8.4f} | {e_mean:>8.4f} | {m_mean:>8.4f} | {net:>+8.4f}")

    # ── Section 5: 5-Second Window Dynamics ───────────────────────
    print("\n" + "─" * 80)
    print("  5. REWARD COMPONENT DYNAMICS (5s windows)")
    print("─" * 80)

    frame_rate = SR / HOP
    window_frames = int(5 * frame_rate)

    for r in results:
        tr = r["traces"]
        T = r["T"]
        n_windows = T // window_frames
        print(f"\n  {r['name']}:")
        print(f"    {'Window':<10s} | {'Sal':>6s} | {'Fam':>6s} | "
              f"{'w×Surpr':>8s} | {'w×Resol':>8s} | {'w×Explr':>8s} | {'w×Monot':>8s} | "
              f"{'Net':>8s} | {'Reward':>8s}")
        print(f"    {'-'*88}")

        for w in range(n_windows):
            s_idx = w * window_frames
            e_idx = (w + 1) * window_frames
            sl = slice(s_idx, e_idx)

            sal_w = tr["salience"][sl].mean()
            fam_w = tr["familiarity"][sl].mean()

            ws = W_SURPRISE * (tr["surprise_cons"][sl].mean() + tr["surprise_tempo"][sl].mean())
            wr = W_RESOLUTION * (tr["resolution_cons"][sl].mean() + tr["resolution_tempo"][sl].mean())
            we = W_EXPLORATION * (tr["exploration_cons"][sl].mean() + tr["exploration_tempo"][sl].mean())
            wm = W_MONOTONY * (tr["monotony_cons"][sl].mean() + tr["monotony_tempo"][sl].mean())

            net = ws + wr + we - wm
            rew = tr["reward"][sl].mean()

            t_start = s_idx / frame_rate
            t_end = e_idx / frame_rate
            print(f"    {t_start:.0f}-{t_end:.0f}s    | {sal_w:>6.3f} | {fam_w:>6.3f} | "
                  f"{ws:>8.4f} | {wr:>8.4f} | {we:>8.4f} | {wm:>8.4f} | "
                  f"{net:>+8.4f} | {rew:>+8.4f}")

    # ── Section 6: Key Findings ───────────────────────────────────
    print("\n" + "─" * 80)
    print("  6. KEY FINDINGS")
    print("─" * 80)

    # Calculate overall monotony percentage
    all_positive = []
    all_negative = []
    for r in results:
        tr = r["traces"]
        pos = (
            W_SURPRISE * (tr["surprise_cons"].mean() + tr["surprise_tempo"].mean())
            + W_RESOLUTION * (tr["resolution_cons"].mean() + tr["resolution_tempo"].mean())
            + W_EXPLORATION * (tr["exploration_cons"].mean() + tr["exploration_tempo"].mean())
        )
        neg = W_MONOTONY * (tr["monotony_cons"].mean() + tr["monotony_tempo"].mean())
        all_positive.append(pos)
        all_negative.append(neg)

    avg_pos = np.mean(all_positive)
    avg_neg = np.mean(all_negative)
    monotony_pct = avg_neg / (avg_pos + 1e-8) * 100

    print(f"\n  Average across all pieces:")
    print(f"    Positive reward components (S+R+E): {avg_pos:.4f}")
    print(f"    Monotony tax (M):                   {avg_neg:.4f}")
    print(f"    Monotony as % of positive:          {monotony_pct:.1f}%")
    print(f"    Net reward (pre-fam-mod):            {avg_pos - avg_neg:+.4f}")

    # Salience impact analysis
    sal_means = [r["traces"]["salience"].mean() for r in results]
    sal_stds = [r["traces"]["salience"].std() for r in results]
    print(f"\n  Salience analysis:")
    print(f"    Mean across pieces:   {np.mean(sal_means):.4f}")
    print(f"    Std across pieces:    {np.mean(sal_stds):.4f}")
    print(f"    → Salience IS active but low-variance → weak gating effect")

    print(f"\n  Implications for salience enhancement:")
    print(f"    If salience ranged [0.1, 0.8] instead of current narrow range:")
    print(f"    → Quiet passages: monotony × 0.1 = {avg_neg * 0.1:.4f} (vs {avg_neg:.4f})")
    print(f"    → Dynamic passages: monotony × 0.8 = {avg_neg * 0.8:.4f}")
    print(f"    → Net effect: quiet passages contribute ~0 reward instead of negative")

    print("\n" + "=" * 80)
    print("  END OF ANALYSIS")
    print("=" * 80)


def main() -> None:
    results = []
    for name, path in PIECES.items():
        if not os.path.exists(path):
            print(f"  SKIP: {name} — file not found: {path}")
            continue
        results.append(run_piece(name, path))

    if not results:
        print("No audio files found!")
        return

    analyze_phase_space(results)


if __name__ == "__main__":
    main()
