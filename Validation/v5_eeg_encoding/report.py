"""V5 EEG Encoding — report generation."""
from __future__ import annotations

from typing import Dict

from Validation.config.paths import V5_RESULTS


def generate_summary_report(results: Dict[str, Dict]) -> str:
    """Generate V5 encoding model comparison report."""
    lines = [
        "=" * 60,
        "V5 EEG ENCODING MODELS — SUMMARY",
        "=" * 60,
        "",
        f"{'Model':20s}  {'Dim':>5s}  {'Mean R²':>8s}  {'Alpha':>8s}",
        "-" * 50,
    ]

    for name in ["envelope", "spectrogram", "r3", "beliefs", "ram", "neuro", "full"]:
        if name in results:
            r = results[name]
            lines.append(
                f"  {name:18s}  {r['n_features']:5d}  {r['mean_r2']:8.4f}  {r['best_alpha']:8.1f}"
            )

    lines.extend(["", "=" * 60])
    report = "\n".join(lines)

    V5_RESULTS.mkdir(parents=True, exist_ok=True)
    (V5_RESULTS / "v5_summary.txt").write_text(report)
    return report
