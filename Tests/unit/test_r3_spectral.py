"""Unit tests for R3 spectral feature extraction.

Tests the R3Extractor end-to-end: output shape, value range, feature names,
group structure, and auto-discovery of all 9 spectral groups (A-K).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so Musical_Intelligence is importable.
sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch

from Musical_Intelligence.ear import R3Extractor
from Musical_Intelligence.ear.r3.registry.auto_discovery import auto_discover_groups


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def extractor() -> R3Extractor:
    """Build the R3Extractor once for the entire module (expensive)."""
    return R3Extractor()


@pytest.fixture(scope="module")
def mel_input() -> torch.Tensor:
    """Synthetic mel spectrogram: (B=1, 128, T=100)."""
    torch.manual_seed(42)
    return torch.rand(1, 128, 100)


@pytest.fixture(scope="module")
def r3_output(extractor, mel_input):
    """Pre-computed R3 output for reuse across tests."""
    return extractor.extract(mel_input)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestR3ExtractorOutputShape:
    """Verify that R3 extraction produces the correct tensor shape."""

    def test_r3_extractor_output_shape(self, r3_output):
        """extract from (1,128,100) mel produces (1,100,97) features."""
        features = r3_output.features
        assert features.shape == (1, 100, 97), (
            f"Expected (1, 100, 97), got {features.shape}"
        )

    @pytest.mark.parametrize("batch_size", [1, 2, 4])
    def test_r3_extractor_batch_sizes(self, extractor, batch_size):
        """R3 extraction works with multiple batch sizes."""
        torch.manual_seed(0)
        mel = torch.rand(batch_size, 128, 50)
        out = extractor.extract(mel)
        assert out.features.shape == (batch_size, 50, 97)


class TestR3OutputRange:
    """Verify all R3 output values are in [0, 1]."""

    def test_r3_output_range(self, r3_output):
        """All feature values must lie in [0, 1]."""
        features = r3_output.features
        assert features.min().item() >= 0.0, (
            f"Min value {features.min().item()} is below 0"
        )
        assert features.max().item() <= 1.0, (
            f"Max value {features.max().item()} exceeds 1"
        )


class TestR3FeatureNames:
    """Verify feature names metadata."""

    def test_r3_feature_names_count(self, r3_output):
        """R3Output must report exactly 97 feature names."""
        names = r3_output.feature_names
        assert len(names) == 97, (
            f"Expected 97 feature names, got {len(names)}"
        )

    def test_r3_feature_names_unique(self, r3_output):
        """All 97 feature names must be unique."""
        names = r3_output.feature_names
        assert len(set(names)) == 97, "Duplicate feature names detected"

    def test_r3_feature_names_are_strings(self, r3_output):
        """Every feature name must be a non-empty string."""
        for name in r3_output.feature_names:
            assert isinstance(name, str) and len(name) > 0


class TestR3GroupBoundaries:
    """Verify the 9 spectral groups partition the 97-D space exactly."""

    def test_r3_group_boundaries(self, extractor):
        """9 groups must sum to exactly 97D with no gaps or overlaps."""
        feature_map = extractor.feature_map
        groups = feature_map.groups

        assert len(groups) == 9, (
            f"Expected 9 groups, got {len(groups)}"
        )

        total_dim = sum(g.dim for g in groups)
        assert total_dim == 97, (
            f"Group dimensions sum to {total_dim}, expected 97"
        )

        # Verify contiguous, non-overlapping coverage
        expected_start = 0
        for g in groups:
            assert g.start == expected_start, (
                f"Group {g.name!r} starts at {g.start}, expected {expected_start}"
            )
            assert g.end == g.start + g.dim, (
                f"Group {g.name!r}: end ({g.end}) != start + dim ({g.start + g.dim})"
            )
            expected_start = g.end

        assert expected_start == 97, (
            f"Final group ends at {expected_start}, expected 97"
        )


class TestR3AutoDiscovery:
    """Verify auto_discover_groups finds all 11 spectral groups."""

    def test_r3_groups_all_discovered(self):
        """auto_discover_groups() must return exactly 11 group instances."""
        groups = auto_discover_groups()
        assert len(groups) == 11, (
            f"Expected 11 discovered groups, got {len(groups)}"
        )

    def test_r3_groups_sorted_by_index(self):
        """Discovered groups must be sorted by INDEX_RANGE start."""
        groups = auto_discover_groups()
        starts = [g.INDEX_RANGE[0] for g in groups]
        assert starts == sorted(starts), (
            f"Groups are not sorted by INDEX_RANGE start: {starts}"
        )

    def test_r3_groups_have_unique_names(self):
        """Every discovered group must have a unique GROUP_NAME."""
        groups = auto_discover_groups()
        names = [g.GROUP_NAME for g in groups]
        assert len(set(names)) == len(names), (
            f"Duplicate GROUP_NAMEs: {names}"
        )
