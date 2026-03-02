"""V7 RSA — report generation."""
from __future__ import annotations

from typing import Dict, List

import numpy as np

from Validation.config.paths import V7_RESULTS
from Validation.infrastructure.figures import heatmap


def generate_summary_report(
    comparisons: List[Dict],
    rdms: Dict[str, np.ndarray],
    stimulus_names: List[str],
) -> str:
    """Generate V7 RSA summary report."""
    lines = [
        "=" * 60,
        "V7 RSA — REPRESENTATIONAL SIMILARITY ANALYSIS",
        "=" * 60,
        "",
        f"{'Model':20s}  {'Spearman ρ':>12s}  {'p (perm)':>10s}",
        "-" * 50,
    ]

    for c in comparisons:
        lines.append(
            f"  {c['model_name']:18s}  {c['spearman_rho']:12.4f}  {c['p_permutation']:10.4f}"
        )

    lines.extend(["", "=" * 60])
    report = "\n".join(lines)

    V7_RESULTS.mkdir(parents=True, exist_ok=True)
    (V7_RESULTS / "v7_summary.txt").write_text(report)

    # Generate RDM heatmaps
    for name, rdm in rdms.items():
        labels = [s[:15] for s in stimulus_names]
        heatmap(
            rdm, labels, labels,
            title=f"RDM: {name}",
            cmap="viridis",
            name=f"v7_rdm_{name}",
        )

    return report
