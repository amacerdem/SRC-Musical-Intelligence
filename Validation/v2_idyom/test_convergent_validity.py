"""V2 Test — IDyOM Convergent Validity: MI prediction error ↔ IDyOM IC.

Predictions:
    1. Mean per-melody Pearson r > 0.3 between MI PE and IDyOM IC
    2. > 50% of melodies show significant (p < 0.05) correlation
    3. Spearman rho > 0.25 (rank-order agreement)
"""
from __future__ import annotations

import pytest
import numpy as np

from Validation.v2_idyom.corpora import load_kern_melodies, melodies_to_audio
from Validation.v2_idyom.run_idyom import run_idyom_on_melodies
from Validation.v2_idyom.run_mi_prediction import run_mi_on_corpus
from Validation.v2_idyom.compare import compare_per_melody, aggregate_comparison
from Validation.config.paths import IDYOM_DIR, V2_RESULTS


@pytest.mark.v2
@pytest.mark.requires_download
@pytest.mark.slow
class TestConvergentValidity:
    """IDyOM IC should correlate with MI prediction error."""

    @pytest.fixture(scope="class")
    def corpus_data(self, idyom_corpus_dir, mi_bridge):
        """Load corpus, run IDyOM, run MI, compare."""
        # Load melodies
        melodies = load_kern_melodies(idyom_corpus_dir, max_melodies=50)
        if len(melodies) < 5:
            pytest.skip("Too few melodies in corpus")

        # Synthesize to audio
        audio_dir = V2_RESULTS / "synthesized"
        pairs = melodies_to_audio(melodies, audio_dir)

        # Run IDyOM
        idyom_results = run_idyom_on_melodies(melodies)

        # Run MI
        mi_results = run_mi_on_corpus(mi_bridge, pairs)

        # Compare
        comparisons = compare_per_melody(idyom_results, mi_results)
        aggregate = aggregate_comparison(comparisons)

        return {
            "comparisons": comparisons,
            "aggregate": aggregate,
            "n_melodies": len(melodies),
        }

    def test_mean_correlation_above_threshold(self, corpus_data):
        """Mean per-melody correlation should exceed r = 0.3."""
        agg = corpus_data["aggregate"]
        assert agg["mean_pearson_r"] > 0.3, (
            f"Expected mean r > 0.3, got {agg['mean_pearson_r']:.3f}"
        )

    def test_majority_significant(self, corpus_data):
        """More than 50% of melodies should show significant correlation."""
        agg = corpus_data["aggregate"]
        assert agg["proportion_significant"] > 0.5, (
            f"Expected > 50% significant, got {agg['proportion_significant']:.1%} "
            f"({agg['n_significant_005']}/{agg['n_melodies']})"
        )

    def test_spearman_agreement(self, corpus_data):
        """Rank-order agreement (Spearman) should exceed 0.25."""
        agg = corpus_data["aggregate"]
        assert agg["mean_spearman_rho"] > 0.25, (
            f"Expected mean Spearman rho > 0.25, got {agg['mean_spearman_rho']:.3f}"
        )
