"""V4 DEAM — report generation."""
from __future__ import annotations

from typing import Dict, List

from Validation.config.paths import V4_RESULTS


def generate_summary_report(aggregate: Dict, per_song: List[Dict]) -> str:
    """Generate V4 DEAM validation summary."""
    lines = [
        "=" * 60,
        "V4 DEAM CONTINUOUS EMOTION — SUMMARY",
        "=" * 60,
        "",
        f"Songs analyzed: {aggregate['n_songs']}",
        "",
        "Arousal:",
        f"  Mean r:   {aggregate['mean_r_arousal']:.4f}",
        f"  Median r: {aggregate['median_r_arousal']:.4f}",
        f"  SD r:     {aggregate['std_r_arousal']:.4f}",
        f"  Significant (p<.05): {aggregate['n_sig_arousal_005']}/{aggregate['n_songs']}",
        "",
        "Valence:",
        f"  Mean r:   {aggregate['mean_r_valence']:.4f}",
        f"  Median r: {aggregate['median_r_valence']:.4f}",
        f"  SD r:     {aggregate['std_r_valence']:.4f}",
        f"  Significant (p<.05): {aggregate['n_sig_valence_005']}/{aggregate['n_songs']}",
        "",
        "=" * 60,
    ]

    report = "\n".join(lines)
    V4_RESULTS.mkdir(parents=True, exist_ok=True)
    (V4_RESULTS / "v4_summary.txt").write_text(report)
    return report
