"""V2 Test — IDyOM Convergent Validity: MI prediction error ↔ IDyOM IC.

MI processes audio through a full R³→H³→C³ pipeline while IDyOM operates
on symbolic pitch sequences.  Cross-modal convergent validity between these
fundamentally different representations is expected to be weak-to-moderate.

Predictions:
    1. Mean per-melody Pearson r > 0.0 (positive direction of convergence)
    2. At least one melody shows significant (p < 0.05) correlation
    3. Mean Spearman rho > 0.0 (positive rank-order trend)

Thresholds are conservative because:
  - MI derives surprise from audio via Bayesian belief update (acoustic domain)
  - IDyOM uses conditional pitch probabilities (symbolic domain)
  - Synthesized piano tones limit acoustic variation between notes
  - A leave-one-out simplified n-gram model approximates IDyOM
The key validation is directional: MI and IDyOM should agree on the
*direction* of surprise (positive r), not reach strong convergence.
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
    """IDyOM IC should correlate with MI information content belief."""

    @pytest.fixture(scope="class")
    def corpus_data(self, idyom_corpus_dir, mi_bridge, module_data):
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

        # Stash for auto-reporting
        module_data["v2"] = {
            "comparisons": comparisons,
            "aggregate": aggregate,
        }

        return {
            "comparisons": comparisons,
            "aggregate": aggregate,
            "n_melodies": len(melodies),
        }

    def test_positive_mean_correlation(self, corpus_data):
        """Mean per-melody correlation should be positive.

        Directional convergence: MI's acoustic information content should
        agree with IDyOM's symbolic IC on which notes are more surprising.
        """
        agg = corpus_data["aggregate"]
        assert agg["mean_pearson_r"] > 0.0, (
            f"Expected positive mean r, got {agg['mean_pearson_r']:.3f}"
        )

    def test_at_least_one_significant(self, corpus_data):
        """At least one melody should show significant correlation."""
        agg = corpus_data["aggregate"]
        assert agg["n_significant_005"] >= 1, (
            f"Expected ≥1 significant melody, got {agg['n_significant_005']}"
        )

    def test_positive_spearman_trend(self, corpus_data):
        """Rank-order agreement (Spearman) should be positive."""
        agg = corpus_data["aggregate"]
        assert agg["mean_spearman_rho"] > 0.0, (
            f"Expected positive Spearman rho, got {agg['mean_spearman_rho']:.3f}"
        )
