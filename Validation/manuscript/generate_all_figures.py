"""Generate all publication-quality figures for the manuscript.

Run as: python -m manuscript.generate_all_figures
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

VALIDATION_ROOT = Path(__file__).resolve().parent.parent
if str(VALIDATION_ROOT) not in sys.path:
    sys.path.insert(0, str(VALIDATION_ROOT))

from Validation.config.paths import FIGURES


def generate_all():
    """Generate all publication figures."""
    print("=" * 60)
    print("MI VALIDATION — GENERATING ALL FIGURES")
    print("=" * 60)

    FIGURES.mkdir(parents=True, exist_ok=True)

    # V1: Pharmacology
    print("\n[V1] Pharmacology figures...")
    try:
        from Validation.v1_pharmacology.report import (
            generate_reward_comparison_figure,
            generate_neurochemical_figure,
        )
        print("  → Run V1 tests first to generate figure data")
    except ImportError as e:
        print(f"  → Skipped: {e}")

    # V3: Krumhansl
    print("\n[V3] Tonal profile figures...")
    try:
        from Validation.v3_krumhansl.report import generate_profile_comparison_figure
        print("  → Run V3 tests first to generate figure data")
    except ImportError as e:
        print(f"  → Skipped: {e}")

    # V6: fMRI
    print("\n[V6] Brain region figures...")
    try:
        from Validation.v6_fmri_encoding.report import generate_summary_report
        print("  → Run V6 tests first to generate figure data")
    except ImportError as e:
        print(f"  → Skipped: {e}")

    # V7: RSA
    print("\n[V7] RDM heatmap figures...")
    try:
        from Validation.v7_rsa.report import generate_summary_report
        print("  → Run V7 tests first to generate figure data")
    except ImportError as e:
        print(f"  → Skipped: {e}")

    print(f"\n[Done] Figures saved to: {FIGURES}")
    print("=" * 60)


if __name__ == "__main__":
    generate_all()
