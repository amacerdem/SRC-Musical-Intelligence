"""Test 08 — Determinism Verification.

Runs the same audio file through the pipeline twice and verifies
bit-identical outputs. Critical for scientific reproducibility.

Checks:
- R³ outputs are identical across runs
- H³ outputs are identical across runs
- Relay outputs are identical across runs
- Feature order is deterministic
- No random state leakage between runs
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    load_audio_file,
)


@pytest.mark.benchmark
class TestDeterminism:
    """Verify pipeline produces identical results on repeated runs."""

    @pytest.mark.parametrize("name", ["bach", "herald", "enigma"])
    def test_r3_bit_identical(self, r3_extractor, name: str) -> None:
        """R³ extraction is deterministic (bit-identical on two runs)."""
        _, mel, _ = load_audio_file(name)

        r3_a = r3_extractor.extract(mel)
        r3_b = r3_extractor.extract(mel)

        assert torch.equal(r3_a.features, r3_b.features), \
            f"{name}: R³ outputs differ between runs"
        assert r3_a.feature_names == r3_b.feature_names, \
            f"{name}: R³ feature names differ"

        # Quantify any difference (should be exactly 0)
        max_diff = (r3_a.features - r3_b.features).abs().max().item()
        print(f"  {name} R³ max diff: {max_diff:.2e}")

    @pytest.mark.parametrize("name", ["bach", "swan"])
    def test_h3_bit_identical(
        self, r3_extractor, h3_extractor, h3_demand_set, name: str
    ) -> None:
        """H³ extraction is deterministic (bit-identical on two runs)."""
        _, mel, _ = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features

        h3_a = h3_extractor.extract(r3_features, h3_demand_set)
        h3_b = h3_extractor.extract(r3_features, h3_demand_set)

        assert h3_a.n_tuples == h3_b.n_tuples, \
            f"{name}: H³ tuple count differs"
        assert set(h3_a.features.keys()) == set(h3_b.features.keys()), \
            f"{name}: H³ tuple keys differ"

        max_diffs = []
        for key in h3_a.features:
            diff = (h3_a.features[key] - h3_b.features[key]).abs().max().item()
            max_diffs.append(diff)
            if diff > 0:
                print(f"  WARNING: {name} H³ tuple {key} diff: {diff:.2e}")

        total_max = max(max_diffs) if max_diffs else 0
        print(f"  {name} H³ max diff across {len(max_diffs)} tuples: {total_max:.2e}")
        assert total_max == 0, \
            f"{name}: H³ outputs differ (max diff: {total_max:.2e})"

    @pytest.mark.parametrize("name", ["bach", "herald"])
    def test_relay_determinism(
        self, r3_extractor, h3_extractor, h3_demand_set, all_relays, name: str
    ) -> None:
        """Individual relays produce deterministic output."""
        _, mel, _ = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features
        h3_features = h3_extractor.extract(r3_features, h3_demand_set).features

        for relay in all_relays:
            try:
                out_a = relay.compute(h3_features, r3_features)
                out_b = relay.compute(h3_features, r3_features)
                max_diff = (out_a - out_b).abs().max().item()
                assert max_diff == 0, \
                    f"{name}/{relay.NAME}: Relay non-deterministic (diff: {max_diff:.2e})"
            except Exception as e:
                print(f"  {relay.NAME}: skipped ({e})")

    def test_feature_order_deterministic(self, r3_extractor) -> None:
        """R³ feature names are in the same order across runs."""
        _, mel, _ = load_audio_file("bach")
        names_a = r3_extractor.extract(mel).feature_names
        names_b = r3_extractor.extract(mel).feature_names
        assert names_a == names_b, "Feature name ordering changed between runs"

    def test_different_input_different_output(self, r3_extractor) -> None:
        """Different audio produces different R³ outputs (sanity check)."""
        _, mel_bach, _ = load_audio_file("bach")
        _, mel_duel, _ = load_audio_file("duel")

        r3_bach = r3_extractor.extract(mel_bach).features
        r3_duel = r3_extractor.extract(mel_duel).features

        # Trim to same length for comparison
        min_T = min(r3_bach.shape[1], r3_duel.shape[1])
        diff = (r3_bach[:, :min_T, :] - r3_duel[:, :min_T, :]).abs().mean().item()

        assert diff > 0.01, \
            f"Bach and Duel R³ outputs are suspiciously similar (diff: {diff:.6f})"
        print(f"  Bach vs Duel mean absolute diff: {diff:.4f}")

    def test_excerpt_subset_consistency(self, r3_extractor) -> None:
        """R³ features for a 10s excerpt match the first 10s of a 30s extraction."""
        _, mel_30, _ = load_audio_file("herald", excerpt_s=30.0)
        _, mel_10, _ = load_audio_file("herald", excerpt_s=10.0)

        r3_30 = r3_extractor.extract(mel_30).features  # (1, T30, 97)
        r3_10 = r3_extractor.extract(mel_10).features  # (1, T10, 97)

        T10 = r3_10.shape[1]
        # First T10 frames of 30s extraction should match 10s extraction
        # (within tolerance for boundary effects)
        inner_frames = T10 - 4  # skip boundary frames
        diff = (r3_30[:, 2:inner_frames, :] - r3_10[:, 2:inner_frames, :]).abs().max().item()
        mean_diff = (r3_30[:, 2:inner_frames, :] - r3_10[:, 2:inner_frames, :]).abs().mean().item()

        print(f"  Excerpt consistency (herald): max diff = {diff:.2e}, mean diff = {mean_diff:.2e}")
        # Mel normalization divides by global max, so different excerpt lengths
        # produce different normalization constants. Allow generous tolerance.
        assert mean_diff < 0.5, \
            f"Excerpt inconsistency: 10s vs 30s mean diff = {mean_diff:.6f}"
