"""V1 Test — Ferreri et al. 2019: Dopamine modulates musical reward.

Predictions:
    1. Levodopa (↑DA) → ↑reward (more pleasure, more chills)
    2. Risperidone (↓DA) → ↓reward (less pleasure)
    3. Reward ordering: levodopa > placebo > risperidone
"""
from __future__ import annotations

import pytest

from Validation.v1_pharmacology.simulate import PharmacologicalSimulator


@pytest.mark.v1
class TestFerreri2019:
    """Reproduce Ferreri et al. 2019 dopamine-reward findings."""

    def test_levodopa_increases_reward(self, ferreri_results):
        """Levodopa (DA agonist) should increase reward relative to placebo."""
        levodopa = ferreri_results[0]   # FERRERI_LEVODOPA
        placebo = ferreri_results[2]    # FERRERI_PLACEBO

        comparison = PharmacologicalSimulator.compare_to_baseline(
            levodopa, placebo, measure="reward",
        )
        assert comparison["direction"] == "increase", (
            f"Levodopa should increase reward, got {comparison['direction']} "
            f"(delta={comparison['delta']:.4f}, {comparison['percent_change']:.1f}%)"
        )

    def test_risperidone_decreases_reward(self, ferreri_results):
        """Risperidone (D2 antagonist) should decrease reward relative to placebo."""
        risperidone = ferreri_results[1]  # FERRERI_RISPERIDONE
        placebo = ferreri_results[2]      # FERRERI_PLACEBO

        comparison = PharmacologicalSimulator.compare_to_baseline(
            risperidone, placebo, measure="reward",
        )
        assert comparison["direction"] == "decrease", (
            f"Risperidone should decrease reward, got {comparison['direction']} "
            f"(delta={comparison['delta']:.4f}, {comparison['percent_change']:.1f}%)"
        )

    def test_reward_ordering(self, ferreri_results):
        """Reward should follow: levodopa > placebo > risperidone."""
        levodopa = ferreri_results[0]
        risperidone = ferreri_results[1]
        placebo = ferreri_results[2]

        assert levodopa.reward_mean > placebo.reward_mean, (
            f"Expected levodopa ({levodopa.reward_mean:.4f}) > "
            f"placebo ({placebo.reward_mean:.4f})"
        )
        assert placebo.reward_mean > risperidone.reward_mean, (
            f"Expected placebo ({placebo.reward_mean:.4f}) > "
            f"risperidone ({risperidone.reward_mean:.4f})"
        )

    def test_da_channel_modulated(self, ferreri_results):
        """The DA neurochemical channel should be modulated by the drugs."""
        levodopa = ferreri_results[0]
        risperidone = ferreri_results[1]
        placebo = ferreri_results[2]

        # Levodopa should have higher DA than placebo
        assert levodopa.da_mean > placebo.da_mean, (
            f"Expected levodopa DA ({levodopa.da_mean:.4f}) > "
            f"placebo DA ({placebo.da_mean:.4f})"
        )
        # Risperidone should have lower DA than placebo
        assert risperidone.da_mean < placebo.da_mean, (
            f"Expected risperidone DA ({risperidone.da_mean:.4f}) < "
            f"placebo DA ({placebo.da_mean:.4f})"
        )

    def test_effect_size_direction(self, ferreri_results):
        """Published effect sizes: d=0.84 for levodopa, d=-0.67 for risperidone.

        We check that MI's effect size has the correct sign (not exact magnitude).
        """
        from Validation.infrastructure.stats import effect_size_cohen_d

        levodopa = ferreri_results[0]
        risperidone = ferreri_results[1]
        placebo = ferreri_results[2]

        # Effect size for levodopa vs placebo (reward time series)
        d_levo = effect_size_cohen_d(levodopa.mi_result.reward, placebo.mi_result.reward)
        assert d_levo > 0, f"Expected positive Cohen's d for levodopa, got {d_levo:.3f}"

        # Effect size for risperidone vs placebo
        d_risp = effect_size_cohen_d(risperidone.mi_result.reward, placebo.mi_result.reward)
        assert d_risp < 0, f"Expected negative Cohen's d for risperidone, got {d_risp:.3f}"
