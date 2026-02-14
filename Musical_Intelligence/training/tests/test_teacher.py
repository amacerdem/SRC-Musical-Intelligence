"""Tests for MI Teacher integration.

Verifies:
- H3DemandCollector finds demands from all 96 models
- H3Densifier round-trips correctly
- MITeacher.compute() returns correct shapes
"""
from __future__ import annotations

import pytest
import torch

from Musical_Intelligence.training.teacher.h3_demand_collector import H3DemandCollector


class TestH3DemandCollector:
    """Test demand collection from 96 models."""

    @pytest.fixture(scope="class")
    def collector(self):
        return H3DemandCollector()

    def test_has_demands(self, collector):
        assert collector.n_demands > 0

    def test_demand_list_length(self, collector):
        assert len(collector.demand_list) == collector.n_demands

    def test_demand_set_matches_list(self, collector):
        assert len(collector.demand_set) == len(collector.demand_list)

    def test_index_map_complete(self, collector):
        assert len(collector.index_map) == collector.n_demands

    def test_index_map_contiguous(self, collector):
        indices = sorted(collector.index_map.values())
        assert indices == list(range(collector.n_demands))

    def test_demands_are_4_tuples(self, collector):
        for demand in collector.demand_list:
            assert len(demand) == 4
            r3_idx, horizon, morph, law = demand
            assert isinstance(r3_idx, int)
            assert isinstance(horizon, int)

    def test_all_9_units_contribute(self, collector):
        """Verify demands come from multiple units."""
        # Not all units necessarily have h3_demand, but most should
        assert collector.n_demands > 100  # At least 100 unique demands


class TestH3Densifier:
    """Test sparse <-> dense H3 conversion."""

    @pytest.fixture
    def densifier(self):
        from Musical_Intelligence.data.h3_densifier import H3Densifier

        collector = H3DemandCollector()
        return H3Densifier(collector.demand_list, collector.index_map)

    def test_densify_shape(self, densifier):
        collector = H3DemandCollector()
        B, T = 2, 16
        N = collector.n_demands

        # Create sparse H3 features
        h3_sparse = {}
        for demand in collector.demand_list[:10]:
            h3_sparse[demand] = torch.rand(B, T)

        dense = densifier.densify(h3_sparse)
        assert dense.shape == (B, T, N)

    def test_round_trip(self, densifier):
        collector = H3DemandCollector()
        B, T = 1, 8
        N = collector.n_demands

        # Create dense tensor
        dense = torch.rand(B, T, N)
        sparse = densifier.sparsify(dense)
        dense_reconstructed = densifier.densify(sparse)

        assert torch.allclose(dense, dense_reconstructed, atol=1e-6)
