"""Unit tests for the H3 vectorized executor.

Tests the H3Executor's 7-phase pipeline: demand handling, output shape,
value range, empty demands, single-tuple execution, and law coverage.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.ear.h3.pipeline.executor import H3Executor
from Musical_Intelligence.ear.h3.demand.demand_tree import DemandTree
from Musical_Intelligence.ear.h3.constants.laws import (
    LAW_MEMORY,
    LAW_PREDICTION,
    LAW_INTEGRATION,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

B, T, D = 2, 60, 97  # batch, time steps, R3 feature dim


@pytest.fixture(scope="module")
def executor() -> H3Executor:
    """Single H3Executor instance for the module."""
    return H3Executor()


@pytest.fixture(scope="module")
def r3_tensor() -> Tensor:
    """Synthetic R3 feature tensor: (B, T, 128) in [0, 1]."""
    torch.manual_seed(77)
    return torch.rand(B, T, D)


@pytest.fixture(scope="module")
def small_demand_set():
    """Small demand set with tuples spanning all 3 laws.

    Format: {(r3_idx, horizon, morph, law), ...}
    Uses low horizons so windows fit within T=60.
    """
    return {
        (0, 0, 0, LAW_MEMORY),       # H0 (1 frame), M0 mean, L0 memory
        (0, 0, 1, LAW_MEMORY),       # H0, M1 mean, L0
        (5, 3, 2, LAW_PREDICTION),   # H3 (4 frames), M2 std, L1 prediction
        (10, 6, 4, LAW_INTEGRATION), # H6 (34 frames), M4 max, L2 integration
        (3, 3, 0, LAW_MEMORY),       # H3, M0 mean, L0
    }


@pytest.fixture(scope="module")
def demand_tree(small_demand_set):
    """Pre-built demand tree from the small demand set."""
    return DemandTree.build(small_demand_set)


@pytest.fixture(scope="module")
def execution_results(executor, r3_tensor, demand_tree):
    """Pre-computed execution results for reuse across tests."""
    return executor.execute(r3_tensor, demand_tree)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestExecutorReturnsDict:
    """Verify executor.execute returns a Dict[tuple, Tensor]."""

    def test_executor_returns_dict(self, execution_results):
        """execute() must return a dict."""
        assert isinstance(execution_results, dict)

    def test_executor_keys_are_4tuples(self, execution_results):
        """Every key must be a 4-tuple of ints."""
        for key in execution_results:
            assert isinstance(key, tuple) and len(key) == 4, (
                f"Key {key} is not a 4-tuple"
            )
            assert all(isinstance(x, int) for x in key), (
                f"Key {key} contains non-int elements"
            )

    def test_executor_values_are_tensors(self, execution_results):
        """Every value must be a torch.Tensor."""
        for key, val in execution_results.items():
            assert isinstance(val, Tensor), (
                f"Value for key {key} is {type(val)}, expected Tensor"
            )


class TestExecutorOutputShape:
    """Verify each output tensor has shape (B, T)."""

    def test_executor_output_shape(self, execution_results):
        """Each value in the results dict must be (B, T)."""
        for key, val in execution_results.items():
            assert val.shape == (B, T), (
                f"Key {key}: expected shape ({B}, {T}), got {val.shape}"
            )


class TestExecutorOutputRange:
    """Verify all output values are in [0, 1]."""

    def test_executor_output_range(self, execution_results):
        """All values in the output dict must be in [0, 1]."""
        for key, val in execution_results.items():
            assert val.min().item() >= 0.0, (
                f"Key {key}: min value {val.min().item()} < 0"
            )
            assert val.max().item() <= 1.0, (
                f"Key {key}: max value {val.max().item()} > 1"
            )


class TestExecutorEmptyDemand:
    """Verify empty demand returns empty dict."""

    def test_executor_empty_demand(self, executor, r3_tensor):
        """An empty demand tree must produce an empty result dict."""
        empty_tree = DemandTree.build(set())
        result = executor.execute(r3_tensor, empty_tree)
        assert result == {}, (
            f"Expected empty dict for empty demand, got {len(result)} entries"
        )


class TestExecutorSingleTuple:
    """Verify a single demand tuple produces exactly one result."""

    def test_executor_single_tuple(self, executor, r3_tensor):
        """A demand set with one 4-tuple must produce exactly one result."""
        single_demand = {(0, 0, 0, 0)}  # r3_idx=0, H0, M0, L0
        tree = DemandTree.build(single_demand)
        result = executor.execute(r3_tensor, tree)
        assert len(result) == 1, (
            f"Expected 1 result entry, got {len(result)}"
        )
        key = next(iter(result))
        assert key == (0, 0, 0, 0)
        assert result[key].shape == (B, T)


class TestExecutorLawCoverage:
    """Verify all 3 laws produce non-zero output."""

    @pytest.mark.parametrize(
        "law_idx,law_name",
        [
            (LAW_MEMORY, "Memory"),
            (LAW_PREDICTION, "Prediction"),
            (LAW_INTEGRATION, "Integration"),
        ],
    )
    def test_executor_law_coverage(self, executor, r3_tensor, law_idx, law_name):
        """Law L{law_idx} ({law_name}) must produce non-zero output on
        random R3 data with a morph that has a non-trivial output.
        """
        # Use H3 (4 frames) and M0 (weighted mean) -- works for any law
        demand = {(0, 3, 0, law_idx)}
        tree = DemandTree.build(demand)
        result = executor.execute(r3_tensor, tree)
        key = (0, 3, 0, law_idx)
        assert key in result, f"Key {key} not found in results"
        # For random R3 input, the output should have non-zero elements
        assert result[key].abs().sum().item() > 0.0, (
            f"Law {law_name} (L{law_idx}) produced all-zero output"
        )


class TestExecutorDemandTreeIntegration:
    """Verify the executor handles demand trees correctly."""

    def test_executor_result_count_matches_demand(
        self, execution_results, small_demand_set
    ):
        """Number of result entries must match number of demanded tuples."""
        assert len(execution_results) == len(small_demand_set), (
            f"Expected {len(small_demand_set)} results, "
            f"got {len(execution_results)}"
        )

    def test_executor_result_keys_match_demand(
        self, execution_results, small_demand_set
    ):
        """Result keys must exactly match the demanded 4-tuples."""
        result_keys = set(execution_results.keys())
        assert result_keys == small_demand_set, (
            f"Result keys {result_keys} do not match demand {small_demand_set}"
        )
