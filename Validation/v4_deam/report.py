"""V4 DEAM — comprehensive report generation with figures."""
from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as sp_stats

from Validation.config.paths import V4_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    correlation_scatter,
    forest_plot,
    save_figure,
    volcano_plot,
)
from Validation.infrastructure.stats import fdr_correction, fisher_z_mean_ci


# Default sample size per annotation (DEAM uses ~15-20 annotators per 2s window)
_DEFAULT_N_PER_SONG = 100  # time-series length proxy


def generate_summary_report(aggregate: Dict, per_song: List[Dict]) -> str:
    """Generate comprehensive V4 DEAM continuous emotion report.

    Includes per-song table, Fisher-z averages, FDR correction,
    arousal-valence comparison, and 6 figures.
    """
    n = aggregate["n_songs"]

    r_a = np.array([s["r_arousal"] for s in per_song])
    r_v = np.array([s["r_valence"] for s in per_song])
    p_a = np.array([s["p_arousal"] for s in per_song])
    p_v = np.array([s["p_valence"] for s in per_song])
    n_samples = np.full(n, _DEFAULT_N_PER_SONG)

    # Fisher-z averaged correlations
    fz_a, fz_a_lo, fz_a_hi = fisher_z_mean_ci(r_a, n_samples)
    fz_v, fz_v_lo, fz_v_hi = fisher_z_mean_ci(r_v, n_samples)

    # FDR correction
    fdr_a_p, fdr_a_reject = fdr_correction(p_a)
    fdr_v_p, fdr_v_reject = fdr_correction(p_v)

    lines = [
        "=" * 78,
        "V4 DEAM CONTINUOUS EMOTION — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        f"  Songs analyzed: {n}",
        "",
        "─── Arousal ───",
        "",
        f"  Mean r:              {aggregate['mean_r_arousal']:.4f}",
        f"  Median r:            {aggregate['median_r_arousal']:.4f}",
        f"  SD r:                {aggregate['std_r_arousal']:.4f}",
        f"  Min / Max r:         {r_a.min():.4f} / {r_a.max():.4f}",
        f"  IQR:                 [{np.percentile(r_a, 25):.4f}, {np.percentile(r_a, 75):.4f}]",
        f"  Fisher-z mean:       {fz_a:.4f}  95% CI [{fz_a_lo:.4f}, {fz_a_hi:.4f}]",
        f"  Uncorrected p<.05:   {aggregate['n_sig_arousal_005']}/{n} "
        f"({aggregate['n_sig_arousal_005']/n:.1%})" if n > 0 else "",
        f"  FDR-corrected q<.05: {int(fdr_a_reject.sum())}/{n} "
        f"({int(fdr_a_reject.sum())/n:.1%})" if n > 0 else "",
        "",
        "─── Valence ───",
        "",
        f"  Mean r:              {aggregate['mean_r_valence']:.4f}",
        f"  Median r:            {aggregate['median_r_valence']:.4f}",
        f"  SD r:                {aggregate['std_r_valence']:.4f}",
        f"  Min / Max r:         {r_v.min():.4f} / {r_v.max():.4f}",
        f"  IQR:                 [{np.percentile(r_v, 25):.4f}, {np.percentile(r_v, 75):.4f}]",
        f"  Fisher-z mean:       {fz_v:.4f}  95% CI [{fz_v_lo:.4f}, {fz_v_hi:.4f}]",
        f"  Uncorrected p<.05:   {aggregate['n_sig_valence_005']}/{n} "
        f"({aggregate['n_sig_valence_005']/n:.1%})" if n > 0 else "",
        f"  FDR-corrected q<.05: {int(fdr_v_reject.sum())}/{n} "
        f"({int(fdr_v_reject.sum())/n:.1%})" if n > 0 else "",
        "",
    ]

    # Arousal vs Valence comparison
    r_diff = r_a - r_v
    diff_mean = float(np.mean(r_diff))
    n_a_better = int(np.sum(r_a > r_v))
    if n > 1:
        sign_stat, sign_p = sp_stats.wilcoxon(r_a, r_v, alternative="two-sided")
    else:
        sign_stat, sign_p = 0.0, 1.0

    lines.extend([
        "─── Arousal vs. Valence Comparison ───",
        "",
        f"  Mean Δ(r_arousal − r_valence): {diff_mean:+.4f}",
        f"  Arousal > Valence: {n_a_better}/{n} songs",
        f"  Wilcoxon signed-rank: stat={sign_stat:.1f}, p={sign_p:.3e}",
        f"  Interpretation: {'Arousal predicted better' if diff_mean > 0 and sign_p < 0.05 else 'No significant difference' if sign_p >= 0.05 else 'Valence predicted better'}",
        "",
    ])

    # Effect size classification
    lines.extend([
        "─── Effect Size Classification ───",
        "",
        "  Arousal:",
    ])
    for label, lo, hi in [("Negligible", 0, 0.1), ("Small", 0.1, 0.3), ("Medium", 0.3, 0.5), ("Large", 0.5, 1.01)]:
        cnt = int(np.sum((np.abs(r_a) >= lo) & (np.abs(r_a) < hi)))
        lines.append(f"    {label:12s} ({lo:.1f}–{hi:.1f}): {cnt}")
    lines.append("  Valence:")
    for label, lo, hi in [("Negligible", 0, 0.1), ("Small", 0.1, 0.3), ("Medium", 0.3, 0.5), ("Large", 0.5, 1.01)]:
        cnt = int(np.sum((np.abs(r_v) >= lo) & (np.abs(r_v) < hi)))
        lines.append(f"    {label:12s} ({lo:.1f}–{hi:.1f}): {cnt}")

    # Full per-song table
    lines.extend([
        "",
        "─── Per-Song Details ───",
        "",
        f"  {'#':>3s}  {'Song':>10s}  {'r_A':>7s}  {'r_V':>7s}  "
        f"{'p_A':>10s}  {'FDR_A':>10s}  {'p_V':>10s}  {'FDR_V':>10s}  {'|r_A|':>5s}",
        f"  {'─'*3}  {'─'*10}  {'─'*7}  {'─'*7}  "
        f"{'─'*10}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*5}",
    ])

    # Sort by arousal r descending
    sorted_idx = np.argsort(r_a)[::-1]
    for rank, idx in enumerate(sorted_idx, 1):
        s = per_song[idx]
        sig_a = "*" if fdr_a_reject[idx] else ""
        sig_v = "*" if fdr_v_reject[idx] else ""
        r_class = "L" if abs(s["r_arousal"]) >= 0.5 else "M" if abs(s["r_arousal"]) >= 0.3 else "S" if abs(s["r_arousal"]) >= 0.1 else "·"
        lines.append(
            f"  {rank:3d}  {str(s['song_id']):>10s}  "
            f"{s['r_arousal']:7.3f}  {s['r_valence']:7.3f}  "
            f"{s['p_arousal']:10.3e}  {fdr_a_p[idx]:10.3e}{sig_a}  "
            f"{s['p_valence']:10.3e}  {fdr_v_p[idx]:10.3e}{sig_v}  "
            f"{r_class:>5s}"
        )

    lines.extend(["", "=" * 78])
    report = "\n".join(lines)

    V4_RESULTS.mkdir(parents=True, exist_ok=True)
    (V4_RESULTS / "v4_summary.txt").write_text(report)
    print(f"[V4] Report saved: {V4_RESULTS / 'v4_summary.txt'}")

    # Generate figures
    try:
        _generate_figures(per_song, r_a, r_v, p_a, p_v, fdr_a_reject, fdr_v_reject)
        print(f"[V4] 6 figures saved to: figures/v4_deam/")
    except Exception as e:
        print(f"[V4] Figure generation failed: {e}")

    return report


def _generate_figures(
    per_song: List[Dict],
    r_a: np.ndarray, r_v: np.ndarray,
    p_a: np.ndarray, p_v: np.ndarray,
    fdr_a_reject: np.ndarray, fdr_v_reject: np.ndarray,
) -> None:
    """Generate all V4 figures."""
    n = len(per_song)
    n_samples = np.full(n, _DEFAULT_N_PER_SONG)

    # 1. Arousal r distribution
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(r_a, bins=20, color="#cb181d", edgecolor="white", linewidth=0.3, alpha=0.7, density=True)
    ax.axvline(x=np.mean(r_a), color="black", linewidth=1, linestyle="--", label=f"Mean={np.mean(r_a):.3f}")
    ax.axvline(x=0, color="grey", linewidth=0.5, linestyle=":")
    ax.set_xlabel("Pearson r (Arousal)")
    ax.set_ylabel("Density")
    ax.set_title("Arousal Correlation Distribution")
    ax.legend(fontsize=5)
    save_figure(fig, "v4_r_distribution_arousal", subdir="v4_deam")

    # 2. Valence r distribution
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(r_v, bins=20, color="#2171b5", edgecolor="white", linewidth=0.3, alpha=0.7, density=True)
    ax.axvline(x=np.mean(r_v), color="black", linewidth=1, linestyle="--", label=f"Mean={np.mean(r_v):.3f}")
    ax.axvline(x=0, color="grey", linewidth=0.5, linestyle=":")
    ax.set_xlabel("Pearson r (Valence)")
    ax.set_ylabel("Density")
    ax.set_title("Valence Correlation Distribution")
    ax.legend(fontsize=5)
    save_figure(fig, "v4_r_distribution_valence", subdir="v4_deam")

    # 3. Arousal vs Valence scatter
    if n > 3:
        r_av, p_av = sp_stats.pearsonr(r_a, r_v)
        correlation_scatter(
            r_a, r_v,
            xlabel="r (Arousal)", ylabel="r (Valence)",
            title="Per-Song: Arousal vs. Valence Prediction",
            r_value=r_av, p_value=p_av,
            name=None,
        )
        save_figure(plt.gcf(), "v4_arousal_vs_valence_scatter", subdir="v4_deam")

    # 4. Forest plot — arousal
    sorted_a = np.argsort(r_a)[::-1]
    labels_a = [str(per_song[i]["song_id"])[:15] for i in sorted_a]
    ci_lo_a = np.empty(n)
    ci_hi_a = np.empty(n)
    for j, idx in enumerate(sorted_a):
        r_clamp = np.clip(r_a[idx], -0.9999, 0.9999)
        z = np.arctanh(r_clamp)
        se = 1.0 / np.sqrt(max(n_samples[idx] - 3, 1))
        ci_lo_a[j] = np.tanh(z - 1.96 * se)
        ci_hi_a[j] = np.tanh(z + 1.96 * se)
    forest_plot(labels_a, r_a[sorted_a], ci_lo_a, ci_hi_a,
                xlabel="Pearson r", title="Per-Song Arousal Correlations",
                name=None)
    save_figure(plt.gcf(), "v4_forest_arousal", subdir="v4_deam")

    # 5. Forest plot — valence
    sorted_v = np.argsort(r_v)[::-1]
    labels_v = [str(per_song[i]["song_id"])[:15] for i in sorted_v]
    ci_lo_v = np.empty(n)
    ci_hi_v = np.empty(n)
    for j, idx in enumerate(sorted_v):
        r_clamp = np.clip(r_v[idx], -0.9999, 0.9999)
        z = np.arctanh(r_clamp)
        se = 1.0 / np.sqrt(max(n_samples[idx] - 3, 1))
        ci_lo_v[j] = np.tanh(z - 1.96 * se)
        ci_hi_v[j] = np.tanh(z + 1.96 * se)
    forest_plot(labels_v, r_v[sorted_v], ci_lo_v, ci_hi_v,
                xlabel="Pearson r", title="Per-Song Valence Correlations",
                name=None)
    save_figure(plt.gcf(), "v4_forest_valence", subdir="v4_deam")

    # 6. Volcano plot (both dimensions)
    all_r = np.concatenate([r_a, r_v])
    all_p = np.concatenate([p_a, p_v])
    all_labels = ([f"A:{s['song_id']}" for s in per_song] +
                  [f"V:{s['song_id']}" for s in per_song])
    volcano_plot(all_r, all_p,
                 labels=all_labels,
                 xlabel="Pearson r",
                 title="DEAM: Effect vs. Significance (A+V)",
                 name=None)
    save_figure(plt.gcf(), "v4_volcano", subdir="v4_deam")
