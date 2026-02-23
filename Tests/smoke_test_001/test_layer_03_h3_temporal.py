"""Layer 03 — H3 Sparse Temporal Morphology.

Validates H3Extractor output: demanded tuples present, shapes correct,
values bounded, empty/single demands, horizon differentiation, and
law semantics.

~25 tests using session-scope fixtures from conftest.
"""
from __future__ import annotations

from typing import Dict, Set, Tuple

import pytest
import torch
from torch import Tensor


# ======================================================================
# Valid ranges for H3 tuple components
# ======================================================================

VALID_R3_RANGE = range(0, 97)
VALID_HORIZON_RANGE = range(0, 32)
VALID_MORPH_RANGE = range(0, 24)
VALID_LAW_RANGE = range(0, 3)


# ======================================================================
# Output completeness
# ======================================================================

class TestH3OutputCompleteness:
    """Every demanded tuple must appear in the output."""

    def test_all_demands_present(self, h3_features, all_demands):
        """Every 4-tuple in the demand set has a corresponding entry."""
        missing = all_demands - set(h3_features.keys())
        assert len(missing) == 0, (
            f"{len(missing)} demanded tuples missing from H3 output: "
            f"{list(missing)[:10]}..."
        )

    def test_n_tuples_matches_demand_size(self, h3_output, all_demands):
        """h3_output.n_tuples == len(all_demands)."""
        assert h3_output.n_tuples == len(all_demands), (
            f"n_tuples={h3_output.n_tuples} but demand set has {len(all_demands)} tuples"
        )

    def test_no_extra_tuples(self, h3_features, all_demands):
        """Output does not contain tuples not in the demand set."""
        extra = set(h3_features.keys()) - all_demands
        assert len(extra) == 0, (
            f"{len(extra)} unexpected tuples in H3 output: {list(extra)[:10]}..."
        )

    def test_demand_set_non_empty(self, all_demands):
        """The demand set is non-empty (mechanisms registered demands)."""
        assert len(all_demands) > 0, "No H3 demands collected from mechanisms"


# ======================================================================
# Shape validation
# ======================================================================

class TestH3OutputShapes:
    """Each H3 feature tensor must have shape (B, T)."""

    def test_all_shapes_2d(self, h3_features):
        """Every value tensor is exactly 2-dimensional."""
        for key, tensor in h3_features.items():
            assert tensor.dim() == 2, (
                f"Tuple {key} has {tensor.dim()}D tensor, expected 2D"
            )

    def test_batch_dimension_consistent(self, h3_features, batch_size):
        """Batch dimension matches across all tuples."""
        for key, tensor in h3_features.items():
            assert tensor.shape[0] == batch_size, (
                f"Tuple {key}: batch={tensor.shape[0]}, expected {batch_size}"
            )

    def test_time_dimension_consistent(self, h3_features, time_steps):
        """Time dimension matches across all tuples."""
        for key, tensor in h3_features.items():
            assert tensor.shape[1] == time_steps, (
                f"Tuple {key}: T={tensor.shape[1]}, expected {time_steps}"
            )


# ======================================================================
# Value bounds
# ======================================================================

class TestH3ValueBounds:
    """H3 features must be bounded, finite, and clean."""

    def test_no_nan(self, h3_features):
        """No NaN values in any H3 feature."""
        for key, tensor in h3_features.items():
            assert not torch.isnan(tensor).any(), f"Tuple {key} contains NaN"

    def test_no_inf(self, h3_features):
        """No Inf values in any H3 feature."""
        for key, tensor in h3_features.items():
            assert not torch.isinf(tensor).any(), f"Tuple {key} contains Inf"

    def test_values_in_unit_interval(self, h3_features):
        """All H3 values in [0, 1]."""
        for key, tensor in h3_features.items():
            assert tensor.min() >= 0.0, (
                f"Tuple {key}: min={tensor.min().item()} < 0"
            )
            assert tensor.max() <= 1.0, (
                f"Tuple {key}: max={tensor.max().item()} > 1"
            )

    def test_dtype_float(self, h3_features):
        """All H3 tensors are float32."""
        for key, tensor in h3_features.items():
            assert tensor.dtype == torch.float32, (
                f"Tuple {key}: dtype={tensor.dtype}, expected float32"
            )


# ======================================================================
# Tuple component validation
# ======================================================================

class TestH3TupleComponents:
    """Validate that tuple components are within legal ranges."""

    def test_r3_idx_valid(self, all_demands):
        """All r3_idx values are in [0, 96]."""
        for r3_idx, h, m, l in all_demands:
            assert r3_idx in VALID_R3_RANGE, f"r3_idx={r3_idx} out of range"

    def test_horizon_valid(self, all_demands):
        """All horizon values are in [0, 31]."""
        for r3_idx, h, m, l in all_demands:
            assert h in VALID_HORIZON_RANGE, f"horizon={h} out of range"

    def test_morph_valid(self, all_demands):
        """All morph values are in [0, 23]."""
        for r3_idx, h, m, l in all_demands:
            assert m in VALID_MORPH_RANGE, f"morph={m} out of range"

    def test_law_valid(self, all_demands):
        """All law values are in [0, 2]."""
        for r3_idx, h, m, l in all_demands:
            assert l in VALID_LAW_RANGE, f"law={l} out of range"


# ======================================================================
# Empty and single demand edge cases
# ======================================================================

class TestH3EdgeCases:
    """Edge cases: empty demand, single demand."""

    def test_empty_demand_yields_empty_output(self, h3_extractor, r3_features):
        """Extracting with an empty demand set returns no features."""
        out = h3_extractor.extract(r3_features, set())
        assert out.n_tuples == 0
        assert len(out.features) == 0

    def test_single_demand(self, h3_extractor, r3_features):
        """A single-element demand set returns exactly one feature."""
        demand = {(0, 4, 0, 0)}  # r3_idx=0, H=4, M=mean, L=memory
        out = h3_extractor.extract(r3_features, demand)
        assert out.n_tuples == 1
        assert len(out.features) == 1
        key = (0, 4, 0, 0)
        assert key in out.features
        assert out.features[key].shape[0] == r3_features.shape[0]


# ======================================================================
# Horizon differentiation
# ======================================================================

class TestH3HorizonDifferentiation:
    """Same r3_idx with different horizons should produce different values."""

    def test_different_horizons_yield_different_values(self, h3_extractor, r3_features):
        """Two horizons on the same r3_idx and morph produce distinct tensors."""
        demand = {
            (0, 1, 0, 0),   # H=1
            (0, 8, 0, 0),   # H=8
            (0, 16, 0, 0),  # H=16
        }
        out = h3_extractor.extract(r3_features, demand)
        t1 = out.features[(0, 1, 0, 0)]
        t8 = out.features[(0, 8, 0, 0)]
        t16 = out.features[(0, 16, 0, 0)]
        # At least two of the three should differ
        diffs = [
            not torch.allclose(t1, t8, atol=1e-6),
            not torch.allclose(t1, t16, atol=1e-6),
            not torch.allclose(t8, t16, atol=1e-6),
        ]
        assert sum(diffs) >= 1, (
            "All horizons produced identical values — horizon differentiation failed"
        )


# ======================================================================
# Morph differentiation
# ======================================================================

class TestH3MorphDifferentiation:
    """Different morphs on the same r3_idx/horizon should differ."""

    def test_different_morphs_differ(self, h3_extractor, r3_features):
        """Mean (M0) vs std (M2) vs velocity (M8) produce distinct features."""
        demand = {
            (0, 4, 0, 0),   # M=mean
            (0, 4, 2, 0),   # M=std
            (0, 4, 8, 0),   # M=velocity
        }
        out = h3_extractor.extract(r3_features, demand)
        t_mean = out.features[(0, 4, 0, 0)]
        t_std = out.features[(0, 4, 2, 0)]
        t_vel = out.features[(0, 4, 8, 0)]
        diffs = [
            not torch.allclose(t_mean, t_std, atol=1e-6),
            not torch.allclose(t_mean, t_vel, atol=1e-6),
            not torch.allclose(t_std, t_vel, atol=1e-6),
        ]
        assert sum(diffs) >= 1, (
            "All morphs produced identical values — morph differentiation failed"
        )


# ======================================================================
# Law differentiation
# ======================================================================

class TestH3LawDifferentiation:
    """Different laws should produce different temporal perspectives."""

    def test_different_laws_differ(self, h3_extractor, r3_features):
        """L0 (memory/backward) vs L1 (forward) produce distinct features."""
        demand = {
            (0, 4, 0, 0),   # L=memory
            (0, 4, 0, 1),   # L=forward
        }
        out = h3_extractor.extract(r3_features, demand)
        t_l0 = out.features[(0, 4, 0, 0)]
        t_l1 = out.features[(0, 4, 0, 1)]
        # They should differ — backward vs forward lookback
        # Allow some tolerance for very short sequences
        assert not torch.allclose(t_l0, t_l1, atol=1e-4), (
            "L0 (memory) and L1 (forward) produced identical values"
        )


# ======================================================================
# Reproducibility
# ======================================================================

class TestH3Reproducibility:
    """H3 extraction should be deterministic."""

    def test_deterministic_extraction(self, h3_extractor, r3_features):
        """Running extract twice with same inputs yields identical results."""
        demand = {(0, 4, 0, 0), (10, 8, 2, 0)}
        out1 = h3_extractor.extract(r3_features, demand)
        out2 = h3_extractor.extract(r3_features, demand)
        for key in demand:
            assert torch.allclose(out1.features[key], out2.features[key], atol=1e-7), (
                f"Non-deterministic output for tuple {key}"
            )
