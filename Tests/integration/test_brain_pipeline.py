"""Integration tests for the MI brain pipeline (H3 + R3 -> Brain).

Tests verify that the BrainOrchestrator produces correct output shapes,
value ranges, unit slice coverage, and per-unit output consistency.

Run with::

    pytest Tests/integration/test_brain_pipeline.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root on sys.path
# ---------------------------------------------------------------------------
_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import pytest
import torch

from Musical_Intelligence.brain import BrainOrchestrator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPECTED_TOTAL_DIM = 1006
EXPECTED_UNIT_COUNT = 9
UNIT_NAMES = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU")


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture(scope="module")
def brain() -> BrainOrchestrator:
    """Module-scoped BrainOrchestrator (expensive init, reuse)."""
    return BrainOrchestrator()


@pytest.fixture(scope="module")
def synthetic_r3() -> torch.Tensor:
    """Synthetic R3 features: (B=1, T=100, 97) in [0, 1].

    T=100 keeps tests fast while providing enough frames for all
    mechanisms and models to operate.
    """
    gen = torch.Generator().manual_seed(42)
    return torch.rand(1, 100, 97, generator=gen)


@pytest.fixture(scope="module")
def synthetic_h3(brain: BrainOrchestrator) -> dict:
    """Synthetic H3 features covering the brain's full demand set.

    Collects the union of H3 demands from all mechanisms and all units,
    then generates a (B=1, T=100) tensor of random values in [0, 1]
    for each demanded 4-tuple.
    """
    B, T = 1, 100
    gen = torch.Generator().manual_seed(123)

    # Collect all demands from mechanisms
    demand_set = brain._mechanism_runner.h3_demand

    # Collect all demands from units
    for unit in brain._units.values():
        demand_set |= unit.h3_demand

    # Generate synthetic H3 features for every demanded tuple
    h3_features = {}
    for key in sorted(demand_set):
        h3_features[key] = torch.rand(B, T, generator=gen)

    return h3_features


@pytest.fixture(scope="module")
def brain_output(brain, synthetic_h3, synthetic_r3):
    """Pre-computed brain output for the module."""
    return brain.forward(synthetic_h3, synthetic_r3)


# ======================================================================
# Tests
# ======================================================================

class TestBrainForwardShape:
    """Brain forward pass produces correct output shape."""

    def test_brain_forward_shape(self, brain_output) -> None:
        """Output tensor is (B=1, T=100, 1006)."""
        tensor = brain_output.tensor
        assert tensor.shape == (1, 100, EXPECTED_TOTAL_DIM), (
            f"Brain output shape {tensor.shape} != "
            f"expected (1, 100, {EXPECTED_TOTAL_DIM})"
        )

    def test_brain_forward_dtype(self, brain_output) -> None:
        """Output tensor is float32."""
        assert brain_output.tensor.dtype == torch.float32, (
            f"Expected float32, got {brain_output.tensor.dtype}"
        )


class TestBrainForwardRange:
    """Brain output values are in [0, 1]."""

    def test_brain_forward_range(self, brain_output) -> None:
        """All output values should be in [0, 1]."""
        tensor = brain_output.tensor
        assert tensor.min() >= 0.0, (
            f"Brain output min={tensor.min().item():.6f} < 0"
        )
        assert tensor.max() <= 1.0, (
            f"Brain output max={tensor.max().item():.6f} > 1"
        )

    def test_brain_forward_no_nan(self, brain_output) -> None:
        """Output must contain no NaN values."""
        assert not torch.isnan(brain_output.tensor).any(), (
            "Brain output contains NaN values"
        )

    def test_brain_forward_no_inf(self, brain_output) -> None:
        """Output must contain no infinite values."""
        assert not torch.isinf(brain_output.tensor).any(), (
            "Brain output contains infinite values"
        )


class TestBrainUnitSlicesComplete:
    """All 9 units are present and slices span [0, 1006)."""

    def test_all_units_present(self, brain_output) -> None:
        """All 9 unit names appear in unit_slices."""
        slices = brain_output.unit_slices
        for name in UNIT_NAMES:
            assert name in slices, f"Unit {name!r} missing from unit_slices"
        assert len(slices) == EXPECTED_UNIT_COUNT, (
            f"Expected {EXPECTED_UNIT_COUNT} units, got {len(slices)}"
        )

    def test_slices_contiguous(self, brain_output) -> None:
        """Unit slices form a contiguous partition of [0, 1006)."""
        slices = brain_output.unit_slices
        # Build sorted list by start offset
        ordered = sorted(slices.items(), key=lambda kv: kv[1][0])

        expected_start = 0
        for name, (start, end) in ordered:
            assert start == expected_start, (
                f"Unit {name!r} starts at {start}, expected {expected_start}. "
                f"Gap detected."
            )
            assert end > start, (
                f"Unit {name!r} has zero-width slice ({start}, {end})"
            )
            expected_start = end

        assert expected_start == EXPECTED_TOTAL_DIM, (
            f"Slices end at {expected_start}, expected {EXPECTED_TOTAL_DIM}"
        )

    def test_slices_span_full_range(self, brain_output) -> None:
        """First slice starts at 0, last slice ends at 1006."""
        slices = brain_output.unit_slices
        all_starts = [s for s, e in slices.values()]
        all_ends = [e for s, e in slices.values()]
        assert min(all_starts) == 0, (
            f"Minimum slice start is {min(all_starts)}, expected 0"
        )
        assert max(all_ends) == EXPECTED_TOTAL_DIM, (
            f"Maximum slice end is {max(all_ends)}, "
            f"expected {EXPECTED_TOTAL_DIM}"
        )


class TestBrainUnitOutputsMatchSlices:
    """Per-unit output dimensions match their declared slices."""

    def test_unit_outputs_match_slices(self, brain_output) -> None:
        """Each unit_output's last dimension matches its slice width."""
        slices = brain_output.unit_slices
        outputs = brain_output.unit_outputs

        for name in UNIT_NAMES:
            assert name in outputs, (
                f"Unit {name!r} missing from unit_outputs"
            )
            start, end = slices[name]
            expected_dim = end - start
            actual_dim = outputs[name].shape[-1]
            assert actual_dim == expected_dim, (
                f"Unit {name!r}: output dim {actual_dim} != "
                f"slice width {expected_dim} (slice={start}:{end})"
            )

    def test_unit_outputs_reconstruct_brain(self, brain_output) -> None:
        """Concatenating unit outputs in order reproduces the full tensor."""
        ordered_outputs = [
            brain_output.unit_outputs[name] for name in UNIT_NAMES
        ]
        reconstructed = torch.cat(ordered_outputs, dim=-1)
        assert torch.allclose(
            reconstructed, brain_output.tensor, atol=1e-6
        ), "Concatenated unit outputs do not match brain tensor"

    def test_unit_output_shapes_are_3d(self, brain_output) -> None:
        """Every unit output is a 3D tensor (B, T, D)."""
        for name, tensor in brain_output.unit_outputs.items():
            assert tensor.ndim == 3, (
                f"Unit {name!r} output has {tensor.ndim} dims, expected 3"
            )
            assert tensor.shape[0] == 1, (
                f"Unit {name!r} batch dim is {tensor.shape[0]}, expected 1"
            )
            assert tensor.shape[1] == 100, (
                f"Unit {name!r} time dim is {tensor.shape[1]}, expected 100"
            )


class TestBrainOrchestratorProperties:
    """Orchestrator metadata properties are consistent."""

    def test_total_dim(self, brain: BrainOrchestrator) -> None:
        """total_dim property returns 1006."""
        assert brain.total_dim == EXPECTED_TOTAL_DIM

    def test_unit_dims_sum(self, brain: BrainOrchestrator) -> None:
        """Sum of unit_dims equals total_dim."""
        dims = brain.unit_dims
        assert sum(dims.values()) == EXPECTED_TOTAL_DIM, (
            f"Sum of unit dims {sum(dims.values())} != {EXPECTED_TOTAL_DIM}"
        )

    def test_model_count(self, brain: BrainOrchestrator) -> None:
        """model_count returns the expected number of models (96)."""
        count = brain.model_count
        assert count == 96, f"Expected 96 models, got {count}"
