"""V6 fMRI Encoding — report generation."""
from __future__ import annotations

from typing import Dict

import numpy as np

from Validation.config.constants import REGION_NAMES
from Validation.config.paths import V6_RESULTS
from Validation.infrastructure.figures import brain_regions_plot


def generate_summary_report(results: Dict[str, Dict]) -> str:
    """Generate V6 fMRI encoding summary."""
    lines = [
        "=" * 60,
        "V6 fMRI ROI ENCODING — SUMMARY",
        "=" * 60,
        "",
        f"{'Model':15s}  {'Dim':>5s}  {'Mean R²':>8s}  {'Max R²':>8s}  {'Sig ROIs':>9s}",
        "-" * 55,
    ]

    for name in ["r3", "beliefs", "ram", "neuro", "full"]:
        if name in results:
            r = results[name]
            lines.append(
                f"  {name:13s}  {r['n_features']:5d}  "
                f"{r['mean_r2']:8.4f}  {r['max_r2']:8.4f}  "
                f"{r['significant_rois']:4d}/26"
            )

    if "full" in results:
        lines.extend([
            "",
            "─── Per-Region R² (Full Model) ───",
        ])
        r2s = results["full"]["r2_per_roi"]
        for i, name in enumerate(REGION_NAMES):
            marker = " ***" if r2s[i] > 0.05 else " *" if r2s[i] > 0 else ""
            lines.append(f"  {name:18s}  R² = {r2s[i]:8.4f}{marker}")

        # Generate figure
        brain_regions_plot(
            r2s, list(REGION_NAMES),
            title="fMRI ROI Encoding R² (Full MI Model)",
            name="v6_roi_r2",
        )

    lines.extend(["", "=" * 60])
    report = "\n".join(lines)

    V6_RESULTS.mkdir(parents=True, exist_ok=True)
    (V6_RESULTS / "v6_summary.txt").write_text(report)
    return report
