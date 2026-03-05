"""V2 IDyOM — comprehensive report generation with figures."""
from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as sp_stats

from Validation.config.paths import V2_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    correlation_scatter,
    forest_plot,
    save_figure,
    volcano_plot,
)
from Validation.infrastructure.stats import fdr_correction, fisher_z_mean_ci, pearson_with_ci


def _length_interpretation(r_len: float, p_len: float) -> str:
    if p_len >= 0.05:
        return "No significant length effect"
    direction = "higher" if r_len > 0 else "lower"
    return f"Longer melodies yield {direction} correlations"


def generate_summary_report(aggregate: Dict, comparisons: List[Dict]) -> str:
    """Generate comprehensive V2 IDyOM validation report.

    Includes full per-melody table, Fisher-z averaged r, FDR correction,
    effect size classification, descriptive stats, and 5 figures.
    """
    n = aggregate["n_melodies"]
    r_vals = np.array([c["pearson_r"] for c in comparisons])
    rho_vals = np.array([c["spearman_rho"] for c in comparisons])
    p_vals = np.array([c["pearson_p"] for c in comparisons])
    n_notes = np.array([c["n_notes"] for c in comparisons])

    # Fisher-z averaged correlation
    fz_mean, fz_ci_lo, fz_ci_hi = fisher_z_mean_ci(r_vals, n_notes)

    # FDR correction
    fdr_p, fdr_reject = fdr_correction(p_vals)
    n_fdr_sig = int(fdr_reject.sum())

    lines = [
        "=" * 78,
        "V2 IDyOM CONVERGENT VALIDITY — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        "─── Aggregate Statistics ───",
        "",
        f"  Melodies analyzed:       {n}",
        f"  Total notes:             {int(n_notes.sum())}",
        "",
        f"  Pearson r:",
        f"    Mean:                  {aggregate['mean_pearson_r']:.4f}",
        f"    Median:                {aggregate['median_pearson_r']:.4f}",
        f"    SD:                    {aggregate['std_pearson_r']:.4f}",
        f"    Min:                   {r_vals.min():.4f}",
        f"    Max:                   {r_vals.max():.4f}",
        f"    IQR:                   [{np.percentile(r_vals, 25):.4f}, "
        f"{np.percentile(r_vals, 75):.4f}]",
        "",
        f"  Fisher-z Averaged r:     {fz_mean:.4f}  "
        f"95% CI [{fz_ci_lo:.4f}, {fz_ci_hi:.4f}]",
        "",
        f"  Spearman ρ:",
        f"    Mean:                  {aggregate['mean_spearman_rho']:.4f}",
        f"    Median:                {float(np.median(rho_vals)):.4f}",
        f"    SD:                    {float(np.std(rho_vals)):.4f}",
        "",
        f"  Significance:",
        f"    Uncorrected (p<.05):   {aggregate['n_significant_005']}/{n} "
        f"({aggregate['proportion_significant']:.1%})",
        f"    FDR-corrected (q<.05): {n_fdr_sig}/{n} "
        f"({n_fdr_sig/n:.1%})" if n > 0 else "",
        "",
    ]

    # Effect size classification
    n_small = int(np.sum((np.abs(r_vals) >= 0.1) & (np.abs(r_vals) < 0.3)))
    n_medium = int(np.sum((np.abs(r_vals) >= 0.3) & (np.abs(r_vals) < 0.5)))
    n_large = int(np.sum(np.abs(r_vals) >= 0.5))
    n_negligible = n - n_small - n_medium - n_large

    lines.extend([
        "─── Effect Size Classification (|r|) ───",
        "",
        f"  Negligible (<0.1):  {n_negligible}",
        f"  Small (0.1–0.3):    {n_small}",
        f"  Medium (0.3–0.5):   {n_medium}",
        f"  Large (≥0.5):       {n_large}",
        "",
    ])

    # Melody-length correlation
    if len(n_notes) > 3:
        r_len, p_len = sp_stats.pearsonr(n_notes, r_vals)
        lines.extend([
            "─── Melody-Length Analysis ───",
            "",
            f"  Correlation (n_notes vs r): r={r_len:.3f}, p={p_len:.3e}",
            f"  Interpretation: {_length_interpretation(r_len, p_len)}",
            "",
        ])

    # Full per-melody table
    lines.extend([
        "─── Per-Melody Details (All Melodies) ───",
        "",
        f"  {'#':>3s}  {'Melody':30s}  {'r':>7s}  {'ρ':>7s}  "
        f"{'p':>10s}  {'FDR-p':>10s}  {'n':>5s}  {'|r|':>6s}",
        f"  {'-'*3}  {'-'*30}  {'-'*7}  {'-'*7}  "
        f"{'-'*10}  {'-'*10}  {'-'*5}  {'-'*6}",
    ])

    # Sort by r value descending
    sorted_idx = np.argsort(r_vals)[::-1]
    for rank, idx in enumerate(sorted_idx, 1):
        c = comparisons[idx]
        r_class = "L" if abs(c["pearson_r"]) >= 0.5 else "M" if abs(c["pearson_r"]) >= 0.3 else "S" if abs(c["pearson_r"]) >= 0.1 else "·"
        sig_mark = "*" if fdr_reject[idx] else ""
        lines.append(
            f"  {rank:3d}  {c['melody_name'][:30]:30s}  "
            f"{c['pearson_r']:7.3f}  {c['spearman_rho']:7.3f}  "
            f"{c['pearson_p']:10.3e}  {fdr_p[idx]:10.3e}{sig_mark:1s}  "
            f"{c['n_notes']:5d}  {r_class:>6s}"
        )

    lines.extend(["", "=" * 78])
    report = "\n".join(lines)

    V2_RESULTS.mkdir(parents=True, exist_ok=True)
    (V2_RESULTS / "v2_summary.txt").write_text(report)
    print(f"[V2] Report saved: {V2_RESULTS / 'v2_summary.txt'}")

    # Generate figures
    try:
        _generate_figures(comparisons, r_vals, rho_vals, p_vals, n_notes, fdr_reject)
        print(f"[V2] 5 figures saved to: figures/v2_idyom/")
    except Exception as e:
        print(f"[V2] Figure generation failed: {e}")

    return report


def _generate_figures(
    comparisons: List[Dict],
    r_vals: np.ndarray,
    rho_vals: np.ndarray,
    p_vals: np.ndarray,
    n_notes: np.ndarray,
    fdr_reject: np.ndarray,
) -> None:
    """Generate all V2 figures."""

    # 1. Distribution of Pearson r
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(r_vals, bins=20, color="#2171b5", edgecolor="white", linewidth=0.3, alpha=0.8, density=True)
    # KDE overlay
    if len(r_vals) > 3:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(r_vals)
        x_kde = np.linspace(r_vals.min() - 0.1, r_vals.max() + 0.1, 200)
        ax.plot(x_kde, kde(x_kde), color="#cb181d", linewidth=1)
    ax.axvline(x=np.mean(r_vals), color="#238b45", linewidth=1, linestyle="--", label=f"Mean={np.mean(r_vals):.3f}")
    ax.axvline(x=0, color="grey", linewidth=0.5, linestyle=":")
    ax.set_xlabel("Pearson r")
    ax.set_ylabel("Density")
    ax.set_title("Distribution of MI–IDyOM Correlations")
    ax.legend(fontsize=5)
    save_figure(fig, "v2_r_distribution", subdir="v2_idyom")

    # 2. r vs melody length
    if len(n_notes) > 3:
        r_len, p_len, ci_len = pearson_with_ci(n_notes.astype(float), r_vals)
        correlation_scatter(
            n_notes.astype(float), r_vals,
            xlabel="Melody Length (notes)", ylabel="Pearson r",
            title="Correlation vs. Melody Length",
            r_value=r_len, p_value=p_len, ci=ci_len,
            name=None,
        )
        plt.gcf().set_size_inches(3.5, 3.5)
        save_figure(plt.gcf(), "v2_r_vs_melody_length", subdir="v2_idyom")

    # 3. Pearson vs Spearman
    if len(r_vals) > 3:
        r_ps, p_ps, ci_ps = pearson_with_ci(r_vals, rho_vals)
        correlation_scatter(
            r_vals, rho_vals,
            xlabel="Pearson r", ylabel="Spearman ρ",
            title="Pearson vs. Spearman Agreement",
            r_value=r_ps, p_value=p_ps, ci=ci_ps,
            name=None,
        )
        save_figure(plt.gcf(), "v2_pearson_vs_spearman", subdir="v2_idyom")

    # 4. Forest plot
    sorted_idx = np.argsort(r_vals)[::-1]
    labels = [comparisons[i]["melody_name"][:25] for i in sorted_idx]
    estimates = r_vals[sorted_idx]
    # Fisher-z CI per melody
    ci_lo = np.empty(len(r_vals))
    ci_hi = np.empty(len(r_vals))
    for i, idx in enumerate(sorted_idx):
        n = max(comparisons[idx]["n_notes"], 4)
        r_clamp = np.clip(r_vals[idx], -0.9999, 0.9999)
        z = np.arctanh(r_clamp)
        se = 1.0 / np.sqrt(n - 3)
        ci_lo[i] = np.tanh(z - 1.96 * se)
        ci_hi[i] = np.tanh(z + 1.96 * se)

    forest_plot(
        labels, estimates, ci_lo, ci_hi,
        xlabel="Pearson r", title="Per-Melody Correlations (MI ↔ IDyOM)",
        name=None,
    )
    save_figure(plt.gcf(), "v2_forest_plot", subdir="v2_idyom")

    # 5. Volcano plot
    volcano_plot(
        r_vals, p_vals,
        labels=[c["melody_name"][:15] for c in comparisons],
        xlabel="Pearson r",
        title="MI–IDyOM: Effect Size vs. Significance",
        name=None,
    )
    save_figure(plt.gcf(), "v2_volcano", subdir="v2_idyom")
