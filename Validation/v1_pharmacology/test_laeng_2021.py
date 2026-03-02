"""V1 Test — Laeng et al. 2021: Opioid antagonism selectively affects arousal.

Predictions:
    1. Naltrexone (↓OPI) → ↓arousal (reduced physiological response)
    2. Naltrexone → valence preserved (cognitive evaluation unaffected)
    3. This demonstrates a dissociation: OPI affects bodily/arousal, not valence
"""
from __future__ import annotations

import pytest

from Validation.v1_pharmacology.simulate import PharmacologicalSimulator


@pytest.mark.v1
class TestLaeng2021:
    """Reproduce Laeng et al. 2021 opioid-arousal dissociation."""

    def test_naltrexone_decreases_arousal(self, laeng_results):
        """Naltrexone should reduce physiological arousal to music."""
        naltrexone = laeng_results[0]  # LAENG_NALTREXONE
        placebo = laeng_results[2]     # LAENG_PLACEBO

        comparison = PharmacologicalSimulator.compare_to_baseline(
            naltrexone, placebo, measure="arousal",
        )
        assert comparison["direction"] == "decrease", (
            f"Naltrexone should decrease arousal, got {comparison['direction']} "
            f"(delta={comparison['delta']:.4f}, {comparison['percent_change']:.1f}%)"
        )

    def test_naltrexone_preserves_valence(self, laeng_results):
        """Naltrexone should preserve valence (cognitive evaluation unaffected)."""
        naltrexone_valence = laeng_results[1]  # LAENG_VALENCE_PRESERVED
        placebo = laeng_results[2]             # LAENG_PLACEBO

        comparison = PharmacologicalSimulator.compare_to_baseline(
            naltrexone_valence, placebo, measure="valence",
        )

        # Valence change should be small (<15% from baseline)
        assert PharmacologicalSimulator.check_direction(comparison, "preserved"), (
            f"Naltrexone should preserve valence (|change| < 15%), "
            f"got {comparison['percent_change']:.1f}%"
        )

    def test_arousal_valence_dissociation(self, laeng_results):
        """Demonstrate OPI dissociation: arousal affected more than valence."""
        naltrexone_arousal = laeng_results[0]
        naltrexone_valence = laeng_results[1]
        placebo = laeng_results[2]

        arousal_comp = PharmacologicalSimulator.compare_to_baseline(
            naltrexone_arousal, placebo, measure="arousal",
        )
        valence_comp = PharmacologicalSimulator.compare_to_baseline(
            naltrexone_valence, placebo, measure="valence",
        )

        # The absolute change in arousal should be larger than in valence
        arousal_change = abs(arousal_comp["percent_change"])
        valence_change = abs(valence_comp["percent_change"])

        assert arousal_change > valence_change, (
            f"Expected arousal change ({arousal_change:.1f}%) > "
            f"valence change ({valence_change:.1f}%) — OPI should affect "
            f"bodily/arousal more than cognitive valence"
        )
