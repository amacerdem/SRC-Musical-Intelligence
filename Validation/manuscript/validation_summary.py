"""Generate validation summary table for manuscript supplementary materials."""
from __future__ import annotations

from typing import Dict, List


def generate_validation_matrix() -> str:
    """Generate the full validation matrix showing evidence levels.

    Maps each MI component to its validation approach and evidence tier.
    """
    matrix = [
        ("R³ spectral features", "V3 Krumhansl, V5 EEG", "α (direct)", "97D"),
        ("H³ temporal morphology", "V2 IDyOM, V4 DEAM", "α (direct)", "~8,600 tuples"),
        ("C³ belief dynamics", "V1 pharma, V4 DEAM, V5 EEG", "α-β", "131 beliefs"),
        ("F1 Sensory processing", "V5 EEG A1/STG", "α", "17 beliefs"),
        ("F2 Prediction (PE)", "V2 IDyOM convergence", "α", "15 beliefs"),
        ("F3 Attention", "V5 EEG topography", "β", "15 beliefs"),
        ("F4 Memory", "V4 DEAM (familiarity)", "β", "13 beliefs"),
        ("F5 Emotion", "V1 pharma (OPI), V4 DEAM", "α", "14 beliefs"),
        ("F6 Reward", "V1 pharma (DA), V6 NAcc/VTA", "α", "16 beliefs"),
        ("F7 Motor entrainment", "V5 EEG (mu/beta)", "β", "17 beliefs"),
        ("F8 Learning", "V2 IDyOM (training)", "β", "14 beliefs"),
        ("F9 Social cognition", "V6 fMRI (STS/TP)", "γ", "10 beliefs"),
        ("DA neurochemistry", "V1 Ferreri 2019", "α", "1 channel"),
        ("OPI neurochemistry", "V1 Mallik/Laeng", "α", "1 channel"),
        ("26 brain regions", "V6 fMRI ROI encoding", "β", "26 ROIs"),
        ("Ψ³ affect (valence/arousal)", "V4 DEAM continuous", "α", "4D"),
        ("Ψ³ emotion", "V1 Mallik OPI, V4 DEAM", "α-β", "7D"),
        ("Representational structure", "V7 RSA", "β", "131×131"),
    ]

    lines = [
        "=" * 90,
        "MI VALIDATION MATRIX",
        "=" * 90,
        "",
        f"{'Component':35s}  {'Validation':30s}  {'Tier':>6s}  {'Scope':>12s}",
        "-" * 90,
    ]

    for component, validation, tier, scope in matrix:
        lines.append(f"  {component:33s}  {validation:28s}  {tier:>6s}  {scope:>12s}")

    lines.extend([
        "",
        "Evidence Tiers:",
        "  α = Mechanistic (direct causal evidence, published replication)",
        "  β = Integrative (correlational, encoding models)",
        "  γ = Speculative (limited direct evidence, theory-driven)",
        "",
        "=" * 90,
    ])

    return "\n".join(lines)
