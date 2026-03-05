"""V6 fMRI Encoding — comprehensive report generation with figures."""
from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from Validation.config.constants import (
    BRAINSTEM_REGIONS,
    CORTICAL_REGIONS,
    REGION_NAMES,
    SUBCORTICAL_REGIONS,
)
from Validation.config.paths import V6_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    bar_comparison,
    brain_regions_plot,
    correlation_scatter,
    heatmap,
    save_figure,
)
from Validation.infrastructure.stats import pearson_with_ci

MODEL_ORDER = ["r3", "beliefs", "ram", "neuro", "full"]
MODEL_COLORS = {
    "r3": "#2171b5",
    "beliefs": "#238b45",
    "ram": "#74c476",
    "neuro": "#fd8d3c",
    "full": "#cb181d",
}


def generate_summary_report(results: Dict[str, Dict]) -> str:
    """Generate comprehensive V6 fMRI ROI encoding report.

    Includes per-model per-ROI tables, anatomical grouping, incremental R²,
    top/bottom ROIs, and 6 figures.
    """
    present = [m for m in MODEL_ORDER if m in results]
    region_names = list(REGION_NAMES)
    n_regions = len(region_names)

    lines = [
        "=" * 78,
        "V6 fMRI ROI ENCODING — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        "─── Model Overview ───",
        "",
        f"  {'Model':13s}  {'Dim':>5s}  {'Mean R²':>8s}  {'Max R²':>8s}  "
        f"{'Sig ROIs':>9s}  {'ΔR²(r3)':>9s}",
        f"  {'─'*13}  {'─'*5}  {'─'*8}  {'─'*8}  {'─'*9}  {'─'*9}",
    ]

    r3_mean = results.get("r3", {}).get("mean_r2", 0.0)
    for name in present:
        r = results[name]
        delta = r["mean_r2"] - r3_mean
        lines.append(
            f"  {name:13s}  {r['n_features']:5d}  "
            f"{r['mean_r2']:8.4f}  {r['max_r2']:8.4f}  "
            f"{r['significant_rois']:4d}/26  {delta:+9.4f}"
        )

    # Anatomical grouping
    lines.extend(["", "─── Anatomical Group Analysis ───", ""])
    lines.append(
        f"  {'Model':13s}  {'Cortical':>10s}  {'Subcortical':>12s}  {'Brainstem':>10s}"
    )
    lines.append(
        f"  {'─'*13}  {'─'*10}  {'─'*12}  {'─'*10}"
    )

    cortical_idx = list(CORTICAL_REGIONS)
    subcortical_idx = list(SUBCORTICAL_REGIONS)
    brainstem_idx = list(BRAINSTEM_REGIONS)

    for name in present:
        r2s = np.array(results[name]["r2_per_roi"])
        c_mean = float(np.mean(r2s[cortical_idx]))
        s_mean = float(np.mean(r2s[subcortical_idx]))
        b_mean = float(np.mean(r2s[brainstem_idx]))
        lines.append(
            f"  {name:13s}  {c_mean:10.4f}  {s_mean:12.4f}  {b_mean:10.4f}"
        )

    # Per-region R² for ALL models
    lines.extend(["", "─── Per-Region R² (All Models) ───", ""])
    header = f"  {'Region':18s}"
    for name in present:
        header += f"  {name:>8s}"
    lines.append(header)
    lines.append(f"  {'─'*18}" + "".join(f"  {'─'*8}" for _ in present))

    for i, reg in enumerate(region_names):
        row = f"  {reg:18s}"
        for name in present:
            r2 = results[name]["r2_per_roi"][i]
            marker = "***" if r2 > 0.05 else " * " if r2 > 0 else "   "
            row += f"  {r2:7.4f}{marker[0]}"
        lines.append(row)

    # Top-5 and Bottom-5 ROIs (full model)
    if "full" in results:
        full_r2 = np.array(results["full"]["r2_per_roi"])
        sorted_idx = np.argsort(full_r2)[::-1]

        lines.extend(["", "─── Top-5 ROIs (Full Model) ───", ""])
        for idx in sorted_idx[:5]:
            lines.append(f"  {region_names[idx]:18s}  R² = {full_r2[idx]:.4f}")

        lines.extend(["", "─── Bottom-5 ROIs (Full Model) ───", ""])
        for idx in sorted_idx[-5:]:
            lines.append(f"  {region_names[idx]:18s}  R² = {full_r2[idx]:.4f}")

    # Incremental R² per ROI
    if "r3" in results and "full" in results:
        r3_per_roi = np.array(results["r3"]["r2_per_roi"])
        full_per_roi = np.array(results["full"]["r2_per_roi"])
        delta_per_roi = full_per_roi - r3_per_roi

        lines.extend(["", "─── Incremental R² per ROI (Full − R³) ───", ""])
        sorted_delta = np.argsort(delta_per_roi)[::-1]
        for idx in sorted_delta:
            arrow = "↑" if delta_per_roi[idx] > 0.001 else "↓" if delta_per_roi[idx] < -0.001 else "─"
            lines.append(
                f"  {region_names[idx]:18s}  ΔR² = {delta_per_roi[idx]:+.4f}  {arrow}"
            )

    lines.extend(["", "=" * 78])
    report = "\n".join(lines)

    V6_RESULTS.mkdir(parents=True, exist_ok=True)
    (V6_RESULTS / "v6_summary.txt").write_text(report)
    print(f"[V6] Report saved: {V6_RESULTS / 'v6_summary.txt'}")

    # Generate figures
    try:
        _generate_figures(results, present, region_names)
        print(f"[V6] 6 figures saved to: figures/v6_fmri_encoding/")
    except Exception as e:
        print(f"[V6] Figure generation failed: {e}")

    return report


def _generate_figures(results: Dict, present: list, region_names: list) -> None:
    """Generate all V6 figures."""

    # 1. Brain regions plot (full model)
    if "full" in results:
        brain_regions_plot(
            np.array(results["full"]["r2_per_roi"]), region_names,
            title="fMRI ROI Encoding R² (Full MI Model)",
            name="v6_roi_r2",
        )

    # 2. Heatmap: models × ROIs
    if len(present) > 1:
        matrix = np.array([results[m]["r2_per_roi"] for m in present])
        heatmap(
            matrix, present, region_names,
            title="R² per Model × Region",
            cmap="YlOrRd", vmin=0,
            name=None,
        )
        save_figure(plt.gcf(), "v6_roi_r2_heatmap", subdir="v6_fmri_encoding")

    # 3. Model comparison bar
    apply_nature_style()
    r2_means = [results[m]["mean_r2"] for m in present]
    colors = [MODEL_COLORS.get(m, "#999999") for m in present]

    fig, ax = plt.subplots(figsize=(4, 3))
    x = np.arange(len(present))
    ax.bar(x, r2_means, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(present, rotation=45, ha="right", fontsize=6)
    ax.set_ylabel("Mean R²")
    ax.set_title("fMRI Encoding: Model Comparison")
    save_figure(fig, "v6_model_comparison_bar", subdir="v6_fmri_encoding")

    # 4. Incremental R² brain plot
    if "r3" in results and "full" in results:
        delta = np.array(results["full"]["r2_per_roi"]) - np.array(results["r3"]["r2_per_roi"])
        brain_regions_plot(
            delta, region_names,
            title="Incremental R² (Full − R³)",
            name=None,
        )
        save_figure(plt.gcf(), "v6_incremental_roi", subdir="v6_fmri_encoding")

    # 5. Anatomical group bars
    cortical_idx = list(CORTICAL_REGIONS)
    subcortical_idx = list(SUBCORTICAL_REGIONS)
    brainstem_idx = list(BRAINSTEM_REGIONS)

    fig, ax = plt.subplots(figsize=(5, 3.5))
    n_models = len(present)
    width = 0.8 / n_models
    group_labels = ["Cortical", "Subcortical", "Brainstem"]
    x_groups = np.arange(3)

    for j, name in enumerate(present):
        r2s = np.array(results[name]["r2_per_roi"])
        vals = [
            float(np.mean(r2s[cortical_idx])),
            float(np.mean(r2s[subcortical_idx])),
            float(np.mean(r2s[brainstem_idx])),
        ]
        color = MODEL_COLORS.get(name, "#999999")
        ax.bar(x_groups + j * width, vals, width, label=name,
               color=color, edgecolor="black", linewidth=0.3)

    ax.set_xticks(x_groups + width * (n_models - 1) / 2)
    ax.set_xticklabels(group_labels)
    ax.set_ylabel("Mean R²")
    ax.set_title("R² by Anatomical Group")
    ax.legend(fontsize=5, ncol=2)
    save_figure(fig, "v6_anatomical_group_bar", subdir="v6_fmri_encoding")

    # 6. R³ vs Full scatter per ROI
    if "r3" in results and "full" in results:
        r3_roi = np.array(results["r3"]["r2_per_roi"], dtype=float)
        full_roi = np.array(results["full"]["r2_per_roi"], dtype=float)
        if len(r3_roi) > 3:
            r_val, p_val, ci = pearson_with_ci(r3_roi, full_roi)
            fig = correlation_scatter(
                r3_roi, full_roi,
                xlabel="R³ Model R²", ylabel="Full Model R²",
                title="Per-ROI: R³ vs. Full Model",
                r_value=r_val, p_value=p_val, ci=ci,
                name=None,
            )
            # Add region labels
            ax = fig.axes[0]
            for i, reg in enumerate(region_names):
                ax.annotate(reg[:6], (r3_roi[i], full_roi[i]),
                            fontsize=3, alpha=0.6)
            # Identity line
            lim = max(r3_roi.max(), full_roi.max()) * 1.1
            ax.plot([0, lim], [0, lim], "k--", linewidth=0.5, alpha=0.3)
            save_figure(fig, "v6_roi_scatter_r3_vs_full", subdir="v6_fmri_encoding")
