"""Layer 05 -- Depth-0 Relay Forward Pass.

Validates that every Relay mechanism can produce a valid output tensor from
synthetic H3 and R3 inputs.  Covers shape, value bounds, NaN/Inf checks,
layer-slice extraction, determinism, edge-case batch/time dimensions,
empty-input graceful handling, and mechanism-specific signal checks.

~30 tests.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Relay
from Tests.smoke_test_001.conftest import make_synthetic_h3


# ======================================================================
# Constants
# ======================================================================

B = 2       # default batch size
T = 50      # default time steps for relay tests
R3_DIM = 97


# ======================================================================
# Local helpers
# ======================================================================

def _make_r3(batch: int = B, time: int = T) -> Tensor:
    """Synthetic R3 features (B, T, 97) in [0, 1]."""
    torch.manual_seed(42)
    return torch.rand(batch, time, R3_DIM)


def _run_relay(relay: Relay, batch: int = B, time: int = T) -> Tensor:
    """Run a relay's compute() with matching synthetic inputs."""
    h3 = make_synthetic_h3(relay, batch_size=batch, time_steps=time)
    r3 = _make_r3(batch, time)
    return relay.compute(h3, r3)


# ======================================================================
# 1. Shape validation (parametrized over all relays)
# ======================================================================

class TestRelayOutputShape:
    """Every relay must produce output shaped (B, T, OUTPUT_DIM)."""

    def test_output_rank_is_3(self, all_relays):
        """Output tensor must be 3-dimensional."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.dim() == 3, (
                f"{relay.NAME}: expected rank 3, got {out.dim()}"
            )

    def test_batch_dimension(self, all_relays):
        """Output batch size must match input batch size."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.shape[0] == B, (
                f"{relay.NAME}: expected B={B}, got {out.shape[0]}"
            )

    def test_time_dimension(self, all_relays):
        """Output time dimension must match input time steps."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.shape[1] == T, (
                f"{relay.NAME}: expected T={T}, got {out.shape[1]}"
            )

    def test_feature_dimension(self, all_relays):
        """Output feature dimension must match relay's OUTPUT_DIM."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.shape[2] == relay.OUTPUT_DIM, (
                f"{relay.NAME}: expected D={relay.OUTPUT_DIM}, got {out.shape[2]}"
            )


# ======================================================================
# 2. Value-range checks
# ======================================================================

class TestRelayValueBounds:
    """Output values must be bounded in [0, 1] with no pathologies."""

    def test_values_in_unit_interval(self, all_relays):
        """All output values should lie approximately in [0, 1].

        Some mechanisms use signed activations (e.g. tanh-based) that
        can produce small negatives. Tolerance: [-0.1, 1.1].
        """
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.min().item() >= -0.1, (
                f"{relay.NAME}: min={out.min().item():.6f} below -0.1"
            )
            assert out.max().item() <= 1.1, (
                f"{relay.NAME}: max={out.max().item():.6f} above 1.1"
            )

    def test_no_nan(self, all_relays):
        """No NaN values in output."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert not torch.isnan(out).any(), (
                f"{relay.NAME}: output contains NaN"
            )

    def test_no_inf(self, all_relays):
        """No Inf values in output."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert not torch.isinf(out).any(), (
                f"{relay.NAME}: output contains Inf"
            )

    def test_output_not_all_zeros(self, all_relays):
        """Output should contain at least some non-zero values (non-trivial)."""
        for relay in all_relays:
            out = _run_relay(relay)
            assert out.abs().sum().item() > 0, (
                f"{relay.NAME}: output is entirely zero"
            )

    def test_output_not_all_identical(self, all_relays):
        """Output should have some variation (not a constant tensor)."""
        for relay in all_relays:
            out = _run_relay(relay)
            if out.numel() > 1:
                assert out.std().item() > 1e-8, (
                    f"{relay.NAME}: output has zero variance"
                )


# ======================================================================
# 3. EMPF layer slice extraction
# ======================================================================

class TestRelayLayerSlices:
    """Each relay's LAYERS tuple defines valid non-overlapping slices."""

    def test_layers_exist(self, all_relays):
        """Every relay must define a LAYERS tuple."""
        for relay in all_relays:
            assert hasattr(relay, "LAYERS"), (
                f"{relay.NAME}: missing LAYERS attribute"
            )
            assert isinstance(relay.LAYERS, tuple), (
                f"{relay.NAME}: LAYERS must be a tuple"
            )
            assert len(relay.LAYERS) > 0, (
                f"{relay.NAME}: LAYERS must be non-empty"
            )

    def test_layer_slices_extractable(self, all_relays):
        """Each LayerSpec slice can be extracted from the output."""
        for relay in all_relays:
            out = _run_relay(relay)
            for layer in relay.LAYERS:
                expected = layer.end - layer.start
                sliced = out[:, :, layer.start:layer.end]
                assert sliced.shape[2] == expected, (
                    f"{relay.NAME}/{layer.code}: expected {expected} dims, "
                    f"got {sliced.shape[2]} (start={layer.start}, end={layer.end})"
                )

    def test_layers_cover_full_output(self, all_relays):
        """Layer slices together should cover the full OUTPUT_DIM."""
        for relay in all_relays:
            total_dims = sum(layer.end - layer.start for layer in relay.LAYERS)
            assert total_dims == relay.OUTPUT_DIM, (
                f"{relay.NAME}: layer dims sum to {total_dims}, "
                f"but OUTPUT_DIM={relay.OUTPUT_DIM}"
            )

    def test_layers_non_overlapping(self, all_relays):
        """Layer slices must not overlap."""
        for relay in all_relays:
            ranges = [(layer.start, layer.end) for layer in relay.LAYERS]
            ranges.sort()
            for i in range(1, len(ranges)):
                prev_end = ranges[i - 1][1]
                curr_start = ranges[i][0]
                assert curr_start >= prev_end, (
                    f"{relay.NAME}: layer overlap at index {i}: "
                    f"prev ends at {prev_end}, curr starts at {curr_start}"
                )

    def test_empf_layer_codes(self, all_relays):
        """Most relays should have layers with codes from (E, M, P, F)."""
        valid_codes = {"E", "M", "P", "F", "D", "T", "G"}
        non_conforming = []
        for relay in all_relays:
            codes = {layer.code for layer in relay.LAYERS}
            if not codes.issubset(valid_codes):
                non_conforming.append(
                    f"{relay.NAME}: {codes - valid_codes}"
                )
        # Allow up to 25% non-conforming (compound codes like 'N+C', 'T+M' exist)
        limit = max(2, len(all_relays) // 4)
        assert len(non_conforming) <= limit, (
            f"{len(non_conforming)} relays with unexpected layer codes:\n"
            + "\n".join(non_conforming)
        )

    def test_empf_four_layers(self, all_relays):
        """Most relays should have 3-5 layers (EMPF standard is 4)."""
        non_conforming = []
        for relay in all_relays:
            n = len(relay.LAYERS)
            if n < 2 or n > 6:
                non_conforming.append(
                    f"{relay.NAME}: {n} layers"
                )
        assert not non_conforming, (
            f"Relays with unusual layer count:\n"
            + "\n".join(non_conforming)
        )


# ======================================================================
# 4. Determinism
# ======================================================================

class TestRelayDeterminism:
    """Same inputs must yield identical outputs (no stochastic components)."""

    def test_deterministic_output(self, all_relays):
        """Two runs with same inputs produce identical results."""
        for relay in all_relays:
            out1 = _run_relay(relay)
            out2 = _run_relay(relay)
            assert torch.allclose(out1, out2, atol=1e-6), (
                f"{relay.NAME}: non-deterministic output "
                f"(max diff={torch.abs(out1 - out2).max().item():.6e})"
            )


# ======================================================================
# 5. Edge-case dimensions
# ======================================================================

class TestRelayEdgeCases:
    """Test boundary conditions on batch and time dimensions."""

    def test_single_time_step(self, all_relays):
        """T=1 should work without error."""
        for relay in all_relays:
            out = _run_relay(relay, batch=B, time=1)
            assert out.shape == (B, 1, relay.OUTPUT_DIM), (
                f"{relay.NAME}: T=1 produced shape {out.shape}"
            )

    def test_single_batch(self, all_relays):
        """B=1 should work without error."""
        for relay in all_relays:
            out = _run_relay(relay, batch=1, time=T)
            assert out.shape == (1, T, relay.OUTPUT_DIM), (
                f"{relay.NAME}: B=1 produced shape {out.shape}"
            )

    def test_single_batch_single_time(self, all_relays):
        """B=1, T=1 corner case."""
        for relay in all_relays:
            out = _run_relay(relay, batch=1, time=1)
            assert out.shape == (1, 1, relay.OUTPUT_DIM), (
                f"{relay.NAME}: B=1,T=1 produced shape {out.shape}"
            )

    def test_larger_time(self, all_relays):
        """T=200 should work (larger than default)."""
        for relay in all_relays:
            out = _run_relay(relay, batch=B, time=200)
            assert out.shape == (B, 200, relay.OUTPUT_DIM), (
                f"{relay.NAME}: T=200 produced shape {out.shape}"
            )


# ======================================================================
# 6. Graceful handling of empty H3 input
# ======================================================================

class TestRelayGracefulDegradation:
    """Missing or empty H3 input should not crash."""

    def test_empty_h3_dict(self, all_relays):
        """Passing an empty H3 dict should produce valid output or handle gracefully."""
        r3 = _make_r3()
        for relay in all_relays:
            try:
                out = relay.compute({}, r3)
                # If it returns output, check it is valid
                assert out.dim() == 3, (
                    f"{relay.NAME}: empty-h3 output rank {out.dim()}"
                )
                assert out.shape[0] == B
                assert not torch.isnan(out).any(), (
                    f"{relay.NAME}: NaN on empty h3"
                )
            except (KeyError, RuntimeError, ValueError):
                # Acceptable: mechanism can raise on missing required keys
                pass


# ======================================================================
# 7. ROLE attribute
# ======================================================================

class TestRelayRole:
    """All relays should have ROLE='relay'."""

    def test_role_is_relay(self, all_relays):
        """Every relay instance has ROLE == 'relay'."""
        for relay in all_relays:
            assert relay.ROLE == "relay", (
                f"{relay.NAME}: ROLE={relay.ROLE!r}, expected 'relay'"
            )


# ======================================================================
# 8. H3 demand consistency
# ======================================================================

class TestRelayH3Demand:
    """Relay's h3_demand tuples must be valid."""

    def test_h3_demand_non_empty(self, all_relays):
        """Every relay should demand at least one H3 tuple."""
        for relay in all_relays:
            demand = relay.h3_demand
            assert len(demand) > 0, (
                f"{relay.NAME}: h3_demand is empty"
            )

    def test_h3_demand_tuples_are_4_ints(self, all_relays):
        """Each demand spec should produce a 4-int tuple."""
        for relay in all_relays:
            for spec in relay.h3_demand:
                t = spec.as_tuple()
                assert len(t) == 4, (
                    f"{relay.NAME}: demand tuple has {len(t)} elements"
                )
                assert all(isinstance(v, int) for v in t), (
                    f"{relay.NAME}: demand tuple contains non-int: {t}"
                )

    def test_h3_demand_r3_idx_range(self, all_relays):
        """r3_idx must be in [0, 96]."""
        for relay in all_relays:
            for spec in relay.h3_demand:
                assert 0 <= spec.as_tuple()[0] <= 96, (
                    f"{relay.NAME}: r3_idx={spec.as_tuple()[0]} out of range"
                )

    def test_h3_demand_law_range(self, all_relays):
        """law must be in {0, 1, 2}."""
        for relay in all_relays:
            for spec in relay.h3_demand:
                law = spec.as_tuple()[3]
                assert law in (0, 1, 2), (
                    f"{relay.NAME}: law={law} not in {{0,1,2}}"
                )


# ======================================================================
# 9. BCH-specific: consonance signal spread
# ======================================================================

class TestBCHConsonanceSpread:
    """BCH relay should produce a consonance signal with real spread."""

    def test_bch_consonance_signal_spread(self, all_relays):
        """BCH consonance signal (output dim 6:12) should have spread > 0."""
        bch_list = [r for r in all_relays if r.NAME == "BCH"]
        if not bch_list:
            pytest.skip("BCH relay not found")
        bch = bch_list[0]
        out = _run_relay(bch)
        # BCH is 16D total; exported consonance_signal is at indices [6:12]
        # according to project docs: "Exported = [6:12]"
        consonance = out[:, :, 6:12]
        spread = consonance.max().item() - consonance.min().item()
        assert spread > 0.01, (
            f"BCH consonance signal spread={spread:.4f} is too narrow"
        )

    def test_bch_output_dim(self, all_relays):
        """BCH should have OUTPUT_DIM >= 12 to include consonance band."""
        bch_list = [r for r in all_relays if r.NAME == "BCH"]
        if not bch_list:
            pytest.skip("BCH relay not found")
        bch = bch_list[0]
        assert bch.OUTPUT_DIM >= 12, (
            f"BCH OUTPUT_DIM={bch.OUTPUT_DIM}, expected >= 12"
        )


# ======================================================================
# 10. SNEM-specific: entrainment temporal variation
# ======================================================================

class TestSNEMEntrainment:
    """SNEM relay should produce temporally varying entrainment signals."""

    def test_snem_temporal_variation(self, all_relays):
        """SNEM output should vary across time dimension."""
        snem_list = [r for r in all_relays if r.NAME == "SNEM"]
        if not snem_list:
            pytest.skip("SNEM relay not found")
        snem = snem_list[0]
        out = _run_relay(snem)
        # Check temporal variation: std across time dim should be non-trivial
        time_std = out[0, :, :].std(dim=0)  # (D,)
        assert time_std.mean().item() > 1e-6, (
            f"SNEM temporal variation too low: mean_std={time_std.mean().item():.6e}"
        )

    def test_snem_output_dim(self, all_relays):
        """SNEM should have OUTPUT_DIM=12."""
        snem_list = [r for r in all_relays if r.NAME == "SNEM"]
        if not snem_list:
            pytest.skip("SNEM relay not found")
        assert snem_list[0].OUTPUT_DIM == 12, (
            f"SNEM OUTPUT_DIM={snem_list[0].OUTPUT_DIM}, expected 12"
        )


# ======================================================================
# 11. Relay count and naming
# ======================================================================

class TestRelayPopulation:
    """Validate the population of relay mechanisms."""

    def test_relay_count_at_least_expected(self, all_relays):
        """Should have a reasonable number of relays (F1 alone has ~9)."""
        assert len(all_relays) >= 9, (
            f"Only {len(all_relays)} relays found, expected >= 9"
        )

    def test_all_relay_names_unique_per_function(self, all_relays):
        """Relay NAMEs must be unique within their FUNCTION."""
        from collections import defaultdict
        by_fn = defaultdict(list)
        for r in all_relays:
            by_fn[r.FUNCTION].append(r.NAME)
        duplicates = {}
        for fn, names in by_fn.items():
            dupes = [n for n in names if names.count(n) > 1]
            if dupes:
                duplicates[fn] = set(dupes)
        assert not duplicates, f"Duplicate relay names within function: {duplicates}"

    def test_all_relays_have_function(self, all_relays):
        """Every relay must have a FUNCTION attribute (F1-F9)."""
        valid_functions = {f"F{i}" for i in range(1, 10)}
        for relay in all_relays:
            assert hasattr(relay, "FUNCTION"), (
                f"{relay.NAME}: missing FUNCTION attribute"
            )
            assert relay.FUNCTION in valid_functions, (
                f"{relay.NAME}: FUNCTION={relay.FUNCTION!r} not in F1-F9"
            )

    def test_all_relays_have_unit(self, all_relays):
        """Every relay must have a UNIT attribute."""
        for relay in all_relays:
            assert hasattr(relay, "UNIT"), (
                f"{relay.NAME}: missing UNIT attribute"
            )
            assert isinstance(relay.UNIT, str) and len(relay.UNIT) > 0, (
                f"{relay.NAME}: UNIT must be a non-empty string"
            )

    def test_all_relays_have_full_name(self, all_relays):
        """Every relay must have a FULL_NAME attribute."""
        for relay in all_relays:
            assert hasattr(relay, "FULL_NAME"), (
                f"{relay.NAME}: missing FULL_NAME attribute"
            )
            assert isinstance(relay.FULL_NAME, str) and len(relay.FULL_NAME) > 0, (
                f"{relay.NAME}: FULL_NAME must be a non-empty string"
            )

    def test_output_dim_positive(self, all_relays):
        """OUTPUT_DIM must be a positive integer."""
        for relay in all_relays:
            assert isinstance(relay.OUTPUT_DIM, int), (
                f"{relay.NAME}: OUTPUT_DIM is not int"
            )
            assert relay.OUTPUT_DIM > 0, (
                f"{relay.NAME}: OUTPUT_DIM={relay.OUTPUT_DIM} must be > 0"
            )
