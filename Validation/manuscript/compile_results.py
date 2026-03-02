"""Aggregate all V1-V7 validation results into a unified summary."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from Validation.config.paths import RESULTS, VALIDATION_ROOT


def compile_all_results() -> Dict:
    """Read all validation result summaries and compile into unified report.

    Returns:
        Dict with per-module results.
    """
    compiled = {
        "version": "1.0",
        "modules": {},
    }

    # Read each module's summary
    for module in ["v1_pharmacology", "v2_idyom", "v3_krumhansl",
                   "v4_deam", "v5_eeg_encoding", "v6_fmri_encoding", "v7_rsa"]:
        summary_path = RESULTS / module / f"{module.split('_', 1)[0]}_{module.split('_', 1)[1] if '_' in module else module}_summary.txt"
        # Try standard naming
        for pattern in [f"{module.replace('_', '/')}_summary.txt",
                        f"{module}_summary.txt",
                        f"v*_summary.txt"]:
            summaries = list((RESULTS / module).glob("*summary*"))
            if summaries:
                compiled["modules"][module] = {
                    "status": "completed",
                    "summary_file": str(summaries[0]),
                    "summary": summaries[0].read_text() if summaries[0].exists() else "No results yet",
                }
                break
        else:
            compiled["modules"][module] = {
                "status": "pending",
                "summary": "Not yet run",
            }

    return compiled


def generate_manuscript_table(results: Dict) -> str:
    """Generate a manuscript-ready summary table.

    Returns:
        LaTeX-formatted table string.
    """
    lines = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{MI Validation Results Summary}",
        r"\label{tab:validation}",
        r"\begin{tabular}{lllr}",
        r"\toprule",
        r"Module & Test & Metric & Result \\",
        r"\midrule",
        r"V1 & Ferreri 2019 (DA) & Reward ordering & Pass/Fail \\",
        r"V1 & Mallik 2017 (OPI) & Emotion reduction & Pass/Fail \\",
        r"V1 & Laeng 2021 (OPI) & Arousal-valence dissociation & Pass/Fail \\",
        r"V2 & IDyOM convergence & Mean Pearson $r$ & 0.xx \\",
        r"V3 & Krumhansl major & Profile $r$ & 0.xx \\",
        r"V3 & Krumhansl minor & Profile $r$ & 0.xx \\",
        r"V4 & DEAM arousal & Mean $r$ & 0.xx \\",
        r"V4 & DEAM valence & Mean $r$ & 0.xx \\",
        r"V5 & EEG encoding & Mean $R^2$ & 0.xx \\",
        r"V6 & fMRI encoding & Significant ROIs & xx/26 \\",
        r"V7 & RSA beliefs vs. acoustics & Spearman $\rho$ & 0.xx \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ]

    return "\n".join(lines)


def save_compiled_results(results: Dict) -> Path:
    """Save compiled results to JSON."""
    output = RESULTS / "compiled_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    return output
