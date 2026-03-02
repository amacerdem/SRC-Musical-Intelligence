"""V2 IDyOM — report generation."""
from __future__ import annotations

from typing import Dict, List

from Validation.config.paths import V2_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    correlation_scatter,
    save_figure,
)


def generate_summary_report(aggregate: Dict, comparisons: List[Dict]) -> str:
    """Generate V2 IDyOM validation summary."""
    lines = [
        "=" * 60,
        "V2 IDyOM CONVERGENT VALIDITY — SUMMARY",
        "=" * 60,
        "",
        f"Melodies analyzed: {aggregate['n_melodies']}",
        f"Mean Pearson r:    {aggregate['mean_pearson_r']:.4f}",
        f"Median Pearson r:  {aggregate['median_pearson_r']:.4f}",
        f"SD Pearson r:      {aggregate['std_pearson_r']:.4f}",
        f"Mean Spearman ρ:   {aggregate['mean_spearman_rho']:.4f}",
        f"Significant (p<.05): {aggregate['n_significant_005']}/{aggregate['n_melodies']} "
        f"({aggregate['proportion_significant']:.1%})",
        "",
        "─── Per-Melody Details ───",
    ]

    for c in comparisons[:20]:  # first 20
        lines.append(
            f"  {c['melody_name']:30s}  r={c['pearson_r']:.3f}  "
            f"ρ={c['spearman_rho']:.3f}  p={c['pearson_p']:.3e}  n={c['n_notes']}"
        )

    lines.extend(["", "=" * 60])
    report = "\n".join(lines)

    V2_RESULTS.mkdir(parents=True, exist_ok=True)
    (V2_RESULTS / "v2_summary.txt").write_text(report)
    return report
