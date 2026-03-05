"""V4 Test — DEAM Continuous Emotion: MI valence/arousal vs. human ratings.

MI extracts continuous valence and arousal from the Ψ³ affect domain, then
correlates with crowd-sourced DEAM annotations at 2Hz.

Predictions (10-song subset, 30s excerpts, zero-lag):
    1. Mean per-song arousal correlation r > 0.0 (positive direction)
    2. Mean per-song valence correlation r > 0.0 (positive direction)
    3. At least one song shows significant arousal correlation (p < 0.05)

Conservative thresholds reflect the small sample (10 songs) and limited
overlap window (15s after annotation offset).
"""
from __future__ import annotations

import pytest

from Validation.v4_deam.preprocess import load_annotations, load_song_ids
from Validation.v4_deam.run_mi_emotion import batch_extract
from Validation.v4_deam.correlate import correlate_song, aggregate_correlations


@pytest.mark.v4
@pytest.mark.requires_download
@pytest.mark.slow
class TestValenceArousal:
    """MI continuous emotion should correlate with human DEAM ratings."""

    @pytest.fixture(scope="class")
    def deam_results(self, mi_bridge, deam_audio_dir, deam_annotations_dir):
        """Load DEAM, run MI, compute correlations."""
        # Load annotations
        valence_ann = load_annotations(deam_annotations_dir, "valence")
        arousal_ann = load_annotations(deam_annotations_dir, "arousal")

        # Load song list
        songs = load_song_ids(deam_audio_dir)

        # Filter to songs with both audio and annotations
        valid_songs = [
            (sid, path) for sid, path in songs
            if sid in valence_ann and sid in arousal_ann
        ][:10]  # limit for 8 GB RAM (each song ≈ 200 MB peak)

        if len(valid_songs) < 5:
            pytest.skip("Too few DEAM songs with matching annotations")

        # Run MI
        mi_outputs = batch_extract(mi_bridge, valid_songs, max_songs=10)

        # Compute correlations
        per_song = []
        for song_id, _ in valid_songs:
            if song_id not in mi_outputs:
                continue
            corr = correlate_song(
                mi_outputs[song_id],
                valence_ann[song_id],
                arousal_ann[song_id],
            )
            corr["song_id"] = song_id
            per_song.append(corr)

        aggregate = aggregate_correlations(per_song)
        return {"per_song": per_song, "aggregate": aggregate}

    def test_arousal_positive_correlation(self, deam_results):
        """Mean arousal correlation should be positive.

        MI arousal (0.7*NE + 0.3*OPI) should track human arousal ratings
        in the positive direction. r > 0 confirms directional agreement.
        """
        agg = deam_results["aggregate"]
        assert agg["mean_r_arousal"] > 0.0, (
            f"Expected positive mean arousal r, got {agg['mean_r_arousal']:.3f}"
        )

    def test_valence_positive_correlation(self, deam_results):
        """Mean valence correlation should be positive.

        Valence is harder to predict from audio, but MI's C³ dopamine
        pathway provides tonal-valence signals.
        """
        agg = deam_results["aggregate"]
        assert agg["mean_r_valence"] > 0.0, (
            f"Expected positive mean valence r, got {agg['mean_r_valence']:.3f}"
        )

    def test_at_least_one_significant_arousal(self, deam_results):
        """At least one song should show significant arousal correlation."""
        agg = deam_results["aggregate"]
        assert agg["n_sig_arousal_005"] >= 1, (
            f"Expected ≥1 significant arousal, got {agg['n_sig_arousal_005']}"
        )
