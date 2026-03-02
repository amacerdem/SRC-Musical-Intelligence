"""V1 Pharmacology — report generation and figure creation."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np

from Validation.config.paths import V1_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    bar_comparison,
    save_figure,
)
from Validation.v1_pharmacology.simulate import PharmSimResult, PharmacologicalSimulator
from Validation.v1_pharmacology.targets import ALL_TARGETS


def generate_reward_comparison_figure(
    ferreri_results: List[PharmSimResult],
    name: str = "v1_ferreri_reward",
) -> Path:
    """Generate bar chart comparing reward across Ferreri conditions."""
    conditions = ["Levodopa\n(↑DA)", "Placebo", "Risperidone\n(↓DA)"]
    values = [
        ferreri_results[0].reward_mean,
        ferreri_results[2].reward_mean,
        ferreri_results[1].reward_mean,
    ]
    fig = bar_comparison(
        conditions, values,
        ylabel="Mean Reward Signal",
        title="Ferreri et al. 2019 — DA Modulation of Musical Reward",
        colors=["#238b45", "#6baed6", "#cb181d"],
        name=name,
    )
    return V1_RESULTS / f"{name}.pdf"


def generate_neurochemical_figure(
    ferreri_results: List[PharmSimResult],
    name: str = "v1_neurochemical_state",
) -> Path:
    """Generate bar chart of mean DA/OPI levels across conditions."""
    import matplotlib.pyplot as plt

    apply_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(6, 3))

    # DA levels
    da_vals = [r.da_mean for r in ferreri_results]
    labels = [r.target.drug for r in ferreri_results]
    axes[0].bar(range(len(da_vals)), da_vals,
                color=["#238b45", "#cb181d", "#6baed6"],
                edgecolor="black", linewidth=0.5)
    axes[0].set_xticks(range(len(labels)))
    axes[0].set_xticklabels(labels, rotation=45, ha="right")
    axes[0].set_ylabel("Mean DA Level")
    axes[0].set_title("Dopamine State")

    # Reward vs DA scatter (per time point would be better but means are fine for overview)
    reward_vals = [r.reward_mean for r in ferreri_results]
    axes[1].scatter(da_vals, reward_vals, c=["#238b45", "#cb181d", "#6baed6"],
                    s=50, edgecolors="black", linewidth=0.5)
    for i, label in enumerate(labels):
        axes[1].annotate(label, (da_vals[i], reward_vals[i]),
                         fontsize=6, ha="center", va="bottom")
    axes[1].set_xlabel("Mean DA Level")
    axes[1].set_ylabel("Mean Reward")
    axes[1].set_title("DA–Reward Relationship")

    fig.tight_layout()
    paths = save_figure(fig, name, subdir="v1_pharmacology")
    return paths[0]


def generate_summary_report(
    ferreri_results: List[PharmSimResult],
    mallik_results: List[PharmSimResult],
    laeng_results: List[PharmSimResult],
) -> str:
    """Generate a text summary of all V1 validation results.

    Returns:
        Formatted report string.
    """
    lines = [
        "=" * 70,
        "V1 PHARMACOLOGICAL VALIDATION — SUMMARY REPORT",
        "=" * 70,
        "",
        "─── Ferreri et al. 2019 (PNAS) — Dopamine & Musical Reward ───",
    ]

    placebo = ferreri_results[2]
    for result in ferreri_results:
        comp = PharmacologicalSimulator.compare_to_baseline(result, placebo, "reward")
        lines.append(
            f"  {result.target.drug:15s}  "
            f"Reward={result.reward_mean:.4f}  "
            f"DA={result.da_mean:.4f}  "
            f"Δ={comp['delta']:+.4f} ({comp['percent_change']:+.1f}%)  "
            f"Dir={comp['direction']}"
        )

    lines.extend([
        "",
        "─── Mallik et al. 2017 (Neuropsychopharmacology) — Opioids & Emotion ───",
    ])

    m_placebo = mallik_results[1]
    for result in mallik_results:
        comp = PharmacologicalSimulator.compare_to_baseline(result, m_placebo, "emotion")
        lines.append(
            f"  {result.target.drug:15s}  "
            f"Emotion={result.emotion_mean:.4f}  "
            f"OPI={result.opi_mean:.4f}  "
            f"Δ={comp['delta']:+.4f} ({comp['percent_change']:+.1f}%)  "
            f"Dir={comp['direction']}"
        )

    lines.extend([
        "",
        "─── Laeng et al. 2021 — Opioids & Arousal/Valence Dissociation ───",
    ])

    l_placebo = laeng_results[2]
    for result in laeng_results:
        a_comp = PharmacologicalSimulator.compare_to_baseline(result, l_placebo, "arousal")
        v_comp = PharmacologicalSimulator.compare_to_baseline(result, l_placebo, "valence")
        lines.append(
            f"  {result.target.drug:15s}  "
            f"Arousal={result.arousal_mean:.4f} ({a_comp['percent_change']:+.1f}%)  "
            f"Valence={result.valence_mean:.4f} ({v_comp['percent_change']:+.1f}%)"
        )

    lines.extend(["", "=" * 70])

    report = "\n".join(lines)

    # Save to file
    V1_RESULTS.mkdir(parents=True, exist_ok=True)
    report_path = V1_RESULTS / "v1_summary.txt"
    report_path.write_text(report)
    print(f"[V1] Report saved: {report_path}")

    return report
