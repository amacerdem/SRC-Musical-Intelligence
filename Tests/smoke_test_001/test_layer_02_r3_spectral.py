"""Layer 02 — R3 97D Spectral Extraction.

Validates R3Extractor output shape, value bounds, feature names, group
boundaries, temporal variation, and edge cases.

~20 tests using session-scope fixtures from conftest.
"""
from __future__ import annotations

import pytest
import torch
from torch import Tensor


# ======================================================================
# Group boundary constants
# ======================================================================

GROUPS = {
    "A": (0, 7),     # consonance 7D
    "B": (7, 12),    # energy 5D
    "C": (12, 21),   # timbre 9D
    "D": (21, 25),   # change 4D
    "F": (25, 41),   # pitch 16D
    "G": (41, 51),   # rhythm 10D
    "H": (51, 63),   # harmony 12D
    "J": (63, 83),   # timbre_ext 20D
    "K": (83, 97),   # modulation 14D
}

EXPECTED_GROUP_DIMS = {
    "A": 7, "B": 5, "C": 9, "D": 4, "F": 16,
    "G": 10, "H": 12, "J": 20, "K": 14,
}


# ======================================================================
# Shape & dtype
# ======================================================================

class TestR3OutputShape:
    """Verify output tensor shapes and types."""

    def test_output_shape_btd(self, r3_features, batch_size, time_steps):
        """Features shape is (B, T, 97)."""
        assert r3_features.shape == (batch_size, time_steps, 97)

    def test_output_is_float(self, r3_features):
        """Features dtype is float32."""
        assert r3_features.dtype == torch.float32

    def test_output_device_cpu(self, r3_features):
        """Features live on CPU."""
        assert r3_features.device.type == "cpu"


# ======================================================================
# Value bounds
# ======================================================================

class TestR3ValueBounds:
    """All R3 features should be bounded and clean."""

    def test_no_nan(self, r3_features):
        """No NaN values in output."""
        assert not torch.isnan(r3_features).any(), "R3 output contains NaN"

    def test_no_inf(self, r3_features):
        """No Inf values in output."""
        assert not torch.isinf(r3_features).any(), "R3 output contains Inf"

    def test_values_in_unit_interval(self, r3_features):
        """All values in [0, 1]."""
        assert r3_features.min() >= 0.0, f"Min value {r3_features.min().item()} < 0"
        assert r3_features.max() <= 1.0, f"Max value {r3_features.max().item()} > 1"


# ======================================================================
# Feature names & map
# ======================================================================

class TestR3FeatureMetadata:
    """Verify feature_names and feature_map metadata."""

    def test_feature_names_count(self, r3_output):
        """feature_names has exactly 97 entries."""
        assert len(r3_output.feature_names) == 97

    def test_feature_names_are_strings(self, r3_output):
        """Each feature name is a non-empty string."""
        for name in r3_output.feature_names:
            assert isinstance(name, str)
            assert len(name) > 0

    def test_feature_names_unique(self, r3_output):
        """All 97 feature names are unique."""
        assert len(set(r3_output.feature_names)) == 97

    def test_feature_map_total_dim(self, r3_output):
        """feature_map.total_dim == 97."""
        assert r3_output.feature_map.total_dim == 97

    def test_feature_map_has_groups(self, r3_output):
        """feature_map.groups is a non-empty collection."""
        groups = r3_output.feature_map.groups
        assert len(groups) > 0


# ======================================================================
# Group boundaries
# ======================================================================

class TestR3GroupBoundaries:
    """Verify the 9 R3 groups span [0, 97) with correct boundaries."""

    def test_group_count(self):
        """There are exactly 9 groups (A-K, skipping E and I)."""
        assert len(GROUPS) == 9

    def test_groups_cover_full_range(self):
        """Groups collectively span indices 0 to 97."""
        covered = set()
        for start, end in GROUPS.values():
            covered.update(range(start, end))
        assert covered == set(range(97))

    def test_groups_are_contiguous(self):
        """Groups are contiguous — no gaps or overlaps."""
        boundaries = sorted(GROUPS.values(), key=lambda x: x[0])
        for i in range(len(boundaries) - 1):
            assert boundaries[i][1] == boundaries[i + 1][0], (
                f"Gap between group ending at {boundaries[i][1]} "
                f"and group starting at {boundaries[i + 1][0]}"
            )
        assert boundaries[0][0] == 0
        assert boundaries[-1][1] == 97

    @pytest.mark.parametrize("group_name,expected_dim", EXPECTED_GROUP_DIMS.items())
    def test_group_dim(self, group_name, expected_dim):
        """Each group has the expected number of dimensions."""
        start, end = GROUPS[group_name]
        assert end - start == expected_dim


# ======================================================================
# Per-group variance
# ======================================================================

class TestR3GroupVariance:
    """Each group should show non-trivial variance across the feature set."""

    @pytest.mark.parametrize("group_name", list(GROUPS.keys()))
    def test_group_has_variance(self, r3_features, group_name):
        """Each group has variance > 0 (not all identical)."""
        start, end = GROUPS[group_name]
        group_data = r3_features[:, :, start:end]
        var = group_data.var()
        assert var > 0, f"Group {group_name} has zero variance"

    def test_groups_are_not_identical(self, r3_features):
        """Different groups produce different feature distributions."""
        group_means = []
        for start, end in GROUPS.values():
            group_means.append(r3_features[:, :, start:end].mean().item())
        # Not all group means should be the same
        assert len(set(round(m, 4) for m in group_means)) > 1, (
            "All group means are identical — groups may be duplicated"
        )


# ======================================================================
# Temporal variation
# ======================================================================

class TestR3TemporalVariation:
    """R3 features should vary over time (not constant across T)."""

    def test_temporal_variation_exists(self, r3_features):
        """Variance across the T dimension is > 0."""
        # (B, T, 97) → variance across T
        t_var = r3_features.var(dim=1)  # (B, 97)
        assert t_var.sum() > 0, "No temporal variation in R3 features"

    def test_most_features_vary_over_time(self, r3_features):
        """At least 50% of features have temporal variance > 0."""
        t_var = r3_features.var(dim=1).mean(dim=0)  # (97,)
        varying = (t_var > 0).sum().item()
        assert varying >= 49, f"Only {varying}/97 features vary over time"


# ======================================================================
# Edge cases
# ======================================================================

class TestR3EdgeCases:
    """Edge cases: T=1, zeros input, B=1."""

    def test_t_equals_1(self, r3_extractor):
        """R3 handles single-frame input (T=1)."""
        mel = torch.rand(1, 128, 1)
        out = r3_extractor.extract(mel)
        assert out.features.shape == (1, 1, 97)
        assert not torch.isnan(out.features).any()

    def test_zeros_input(self, r3_extractor):
        """R3 handles all-zeros mel input without crashing."""
        mel = torch.zeros(1, 128, 10)
        out = r3_extractor.extract(mel)
        assert out.features.shape == (1, 10, 97)
        assert not torch.isnan(out.features).any()

    def test_batch_1(self, r3_extractor):
        """R3 works with batch size 1."""
        mel = torch.rand(1, 128, 50)
        out = r3_extractor.extract(mel)
        assert out.features.shape[0] == 1
        assert out.features.shape[2] == 97
