"""V5 EEG Encoding — comprehensive report generation with figures."""
from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from Validation.config.paths import V5_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    bar_comparison,
    save_figure,
)

MODEL_ORDER = ["envelope", "spectrogram", "r3", "beliefs", "ram", "neuro", "full"]
MODEL_COLORS = {
    "envelope": "#bdd7e7",
    "spectrogram": "#6baed6",
    "r3": "#2171b5",
    "beliefs": "#238b45",
    "ram": "#74c476",
    "neuro": "#fd8d3c",
    "full": "#cb181d",
}


def generate_summary_report(results: Dict[str, Dict]) -> str:
    """Generate comprehensive V5 EEG encoding report.

    Includes model comparison table, incremental R², Cohen's f²,
    feature efficiency, and 4 figures.
    """
    present = [m for m in MODEL_ORDER if m in results]

    # Baseline
    baseline_r2 = results.get("envelope", {}).get("mean_r2", 0.0)

    lines = [
        "=" * 78,
        "V5 EEG ENCODING MODELS — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        "─── Model Comparison ───",
        "",
        f"  {'Model':18s}  {'Dim':>5s}  {'Mean R²':>8s}  {'Alpha':>8s}  "
        f"{'ΔR²(env)':>9s}  {'%Impr':>7s}  {'f²':>7s}  {'R²/dim':>8s}",
        f"  {'─'*18}  {'─'*5}  {'─'*8}  {'─'*8}  "
        f"{'─'*9}  {'─'*7}  {'─'*7}  {'─'*8}",
    ]

    for name in present:
        r = results[name]
        r2 = r["mean_r2"]
        delta = r2 - baseline_r2
        pct_impr = (delta / baseline_r2 * 100) if baseline_r2 > 0 else 0.0
        f2 = r2 / (1 - r2) if r2 < 1.0 else float("inf")
        eff = r2 / r["n_features"] if r["n_features"] > 0 else 0.0

        lines.append(
            f"  {name:18s}  {r['n_features']:5d}  {r2:8.4f}  {r['best_alpha']:8.1f}  "
            f"{delta:+9.4f}  {pct_impr:+6.1f}%  {f2:7.4f}  {eff:8.6f}"
        )

    # Incremental R² analysis
    lines.extend(["", "─── Incremental R² Analysis ───", ""])
    lines.append("  Each feature set's unique contribution beyond envelope baseline:")

    for name in present:
        if name == "envelope":
            continue
        r2 = results[name]["mean_r2"]
        delta = r2 - baseline_r2
        interp = "negligible" if delta < 0.01 else "small" if delta < 0.05 else "moderate" if delta < 0.1 else "large"
        lines.append(f"    {name:18s}  ΔR² = {delta:+.4f}  ({interp})")

    # Hierarchical contribution
    if "r3" in results and "beliefs" in results and "full" in results:
        r3_r2 = results["r3"]["mean_r2"]
        belief_r2 = results["beliefs"]["mean_r2"]
        full_r2 = results["full"]["mean_r2"]
        lines.extend([
            "",
            "─── Hierarchical Layer Contribution ───",
            "",
            f"  Acoustic (envelope→R³):       ΔR² = {r3_r2 - baseline_r2:+.4f}",
            f"  Cognitive (R³→beliefs):        ΔR² = {belief_r2 - r3_r2:+.4f}",
            f"  Full (all combined):           R²  = {full_r2:.4f}",
            f"  Cognitive adds: {(full_r2 - r3_r2) / full_r2 * 100:.1f}% of total R²" if full_r2 > 0 else "",
        ])

    # Cohen's f² interpretation
    lines.extend(["", "─── Effect Size (Cohen's f²) ───", ""])
    lines.append("  Benchmarks: small=0.02, medium=0.15, large=0.35")
    for name in present:
        r2 = results[name]["mean_r2"]
        f2 = r2 / (1 - r2) if r2 < 1.0 else float("inf")
        interp = "small" if f2 < 0.15 else "medium" if f2 < 0.35 else "large"
        lines.append(f"    {name:18s}  f² = {f2:.4f}  ({interp})")

    # Regularization analysis
    lines.extend(["", "─── Regularization Analysis ───", ""])
    lines.append("  Higher alpha → more regularization → less overfitting risk")
    for name in present:
        r = results[name]
        lines.append(f"    {name:18s}  α = {r['best_alpha']:.1f}  dim={r['n_features']}")

    lines.extend(["", "=" * 78])
    report = "\n".join(lines)

    V5_RESULTS.mkdir(parents=True, exist_ok=True)
    (V5_RESULTS / "v5_summary.txt").write_text(report)
    print(f"[V5] Report saved: {V5_RESULTS / 'v5_summary.txt'}")

    # Generate figures
    try:
        _generate_figures(results, present, baseline_r2)
        print(f"[V5] 4 figures saved to: figures/v5_eeg_encoding/")
    except Exception as e:
        print(f"[V5] Figure generation failed: {e}")

    return report


def _generate_figures(results: Dict, present: list, baseline_r2: float) -> None:
    """Generate all V5 figures."""

    # 1. Model comparison bar
    apply_nature_style()
    names = present
    r2_vals = [results[m]["mean_r2"] for m in names]
    colors = [MODEL_COLORS.get(m, "#999999") for m in names]

    fig, ax = plt.subplots(figsize=(4.5, 3))
    x = np.arange(len(names))
    ax.bar(x, r2_vals, color=colors, edgecolor="black", linewidth=0.5)
    ax.axhline(y=baseline_r2, color="grey", linewidth=0.8, linestyle="--",
               label=f"Envelope baseline ({baseline_r2:.4f})")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=6)
    ax.set_ylabel("Mean R²")
    ax.set_title("EEG Encoding: Model Comparison")
    ax.legend(fontsize=5)
    save_figure(fig, "v5_model_comparison_bar", subdir="v5_eeg_encoding")

    # 2. Incremental R²
    non_baseline = [m for m in names if m != "envelope"]
    if non_baseline:
        deltas = [results[m]["mean_r2"] - baseline_r2 for m in non_baseline]
        delta_colors = [MODEL_COLORS.get(m, "#999999") for m in non_baseline]

        fig, ax = plt.subplots(figsize=(4, 3))
        x = np.arange(len(non_baseline))
        ax.bar(x, deltas, color=delta_colors, edgecolor="black", linewidth=0.5)
        ax.axhline(y=0, color="black", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(non_baseline, rotation=45, ha="right", fontsize=6)
        ax.set_ylabel("ΔR² (vs. envelope)")
        ax.set_title("Incremental R² Over Envelope Baseline")
        save_figure(fig, "v5_incremental_r2", subdir="v5_eeg_encoding")

    # 3. Feature efficiency scatter
    dims = np.array([results[m]["n_features"] for m in names], dtype=float)
    r2s = np.array([results[m]["mean_r2"] for m in names])

    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    for i, m in enumerate(names):
        ax.scatter(dims[i], r2s[i], color=MODEL_COLORS.get(m, "#999999"),
                   s=40, edgecolors="black", linewidth=0.5, zorder=5)
        ax.annotate(m, (dims[i], r2s[i]), fontsize=5, xytext=(3, 3),
                    textcoords="offset points")
    ax.set_xlabel("Number of Features")
    ax.set_ylabel("Mean R²")
    ax.set_title("Feature Efficiency")
    save_figure(fig, "v5_efficiency_scatter", subdir="v5_eeg_encoding")

    # 4. Alpha vs R²
    alphas = np.array([results[m]["best_alpha"] for m in names])

    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    for i, m in enumerate(names):
        ax.scatter(alphas[i], r2s[i], color=MODEL_COLORS.get(m, "#999999"),
                   s=40, edgecolors="black", linewidth=0.5, zorder=5)
        ax.annotate(m, (alphas[i], r2s[i]), fontsize=5, xytext=(3, 3),
                    textcoords="offset points")
    ax.set_xlabel("Best Alpha (regularization)")
    ax.set_ylabel("Mean R²")
    ax.set_title("Regularization vs. Performance")
    ax.set_xscale("log")
    save_figure(fig, "v5_alpha_vs_r2", subdir="v5_eeg_encoding")
