"""V4 Test — DEAM Continuous Emotion: MI valence/arousal vs. human ratings.

Predictions:
    1. Mean per-song arousal correlation r > 0.3
    2. Mean per-song valence correlation r > 0.2 (valence is harder)
    3. > 30% of songs show significant arousal correlation
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
        ][:50]  # limit for initial validation

        if len(valid_songs) < 10:
            pytest.skip("Too few DEAM songs with matching annotations")

        # Run MI
        mi_outputs = batch_extract(mi_bridge, valid_songs, max_songs=50)

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

    def test_arousal_correlation(self, deam_results):
        """Mean arousal correlation should exceed r = 0.3."""
        agg = deam_results["aggregate"]
        assert agg["mean_r_arousal"] > 0.3, (
            f"Expected mean arousal r > 0.3, got {agg['mean_r_arousal']:.3f}"
        )

    def test_valence_correlation(self, deam_results):
        """Mean valence correlation should exceed r = 0.2."""
        agg = deam_results["aggregate"]
        assert agg["mean_r_valence"] > 0.2, (
            f"Expected mean valence r > 0.2, got {agg['mean_r_valence']:.3f}"
        )

    def test_arousal_significance_proportion(self, deam_results):
        """At least 30% of songs should show significant arousal correlation."""
        agg = deam_results["aggregate"]
        proportion = agg["n_sig_arousal_005"] / max(agg["n_songs"], 1)
        assert proportion > 0.3, (
            f"Expected > 30% significant arousal, got {proportion:.1%} "
            f"({agg['n_sig_arousal_005']}/{agg['n_songs']})"
        )
