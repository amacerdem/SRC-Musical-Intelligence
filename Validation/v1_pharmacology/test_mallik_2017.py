"""V1 Test — Mallik et al. 2017: Opioid antagonism reduces musical emotion.

Predictions:
    1. Naltrexone (↓OPI) → ↓emotion (reduced pleasure from both happy/sad music)
    2. Emotional engagement should be reduced across all emotion dimensions
"""
from __future__ import annotations

import pytest

from Validation.v1_pharmacology.simulate import PharmacologicalSimulator


@pytest.mark.v1
class TestMallik2017:
    """Reproduce Mallik et al. 2017 opioid-emotion findings."""

    def test_naltrexone_decreases_emotion(self, mallik_results):
        """Naltrexone should decrease overall emotional response to music."""
        naltrexone = mallik_results[0]  # MALLIK_NALTREXONE
        placebo = mallik_results[1]     # MALLIK_PLACEBO

        comparison = PharmacologicalSimulator.compare_to_baseline(
            naltrexone, placebo, measure="emotion",
        )
        assert comparison["direction"] == "decrease", (
            f"Naltrexone should decrease emotion, got {comparison['direction']} "
            f"(delta={comparison['delta']:.4f}, {comparison['percent_change']:.1f}%)"
        )

    def test_opi_channel_reduced(self, mallik_results):
        """The OPI neurochemical channel should be reduced by naltrexone."""
        naltrexone = mallik_results[0]
        placebo = mallik_results[1]

        assert naltrexone.opi_mean < placebo.opi_mean, (
            f"Expected naltrexone OPI ({naltrexone.opi_mean:.4f}) < "
            f"placebo OPI ({placebo.opi_mean:.4f})"
        )

    def test_reward_also_reduced(self, mallik_results):
        """Naltrexone should also reduce reward (opioids contribute to reward)."""
        naltrexone = mallik_results[0]
        placebo = mallik_results[1]

        comparison = PharmacologicalSimulator.compare_to_baseline(
            naltrexone, placebo, measure="reward",
        )
        # Opioid blockade reduces hedonic aspects of music
        assert comparison["delta"] <= 0, (
            f"Expected naltrexone to reduce or preserve reward, "
            f"got increase of {comparison['delta']:.4f}"
        )
