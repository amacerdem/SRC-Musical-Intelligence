"""Layer 08 -- Belief observe() Validation.

Validates observe() for all 131 beliefs (36 Core + 65 Appraisal + 30
Anticipation).  For each belief we create synthetic mechanism output of the
correct OUTPUT_DIM and verify shape, bounds, determinism, and numerical
cleanliness.

~15 parametrised tests x 131 beliefs.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import (
    _BeliefBase,
    CoreBelief,
    AppraisalBelief,
    AnticipationBelief,
)


# ======================================================================
# Constants
# ======================================================================

B = 2       # batch size
T = 50      # time steps (shorter than session T for speed)
SEED = 42
FALLBACK_DIM = 10   # if mechanism name not found in mechanism_dims


# ======================================================================
# Module-scope fixture: (belief, dim) pairs
# ======================================================================

@pytest.fixture(scope="module")
def belief_mech_pairs(
    all_beliefs: List[Any],
    mechanism_dims: Dict[str, int],
) -> List[Tuple[Any, int]]:
    """Return list of (belief_instance, mechanism_output_dim) pairs."""
    pairs: List[Tuple[Any, int]] = []
    for belief in all_beliefs:
        mech_name = getattr(belief, "MECHANISM", None)
        dim = mechanism_dims.get(mech_name, FALLBACK_DIM) if mech_name else FALLBACK_DIM
        pairs.append((belief, dim))
    return pairs


def _make_input(dim: int, value: str = "random") -> Tensor:
    """Create a (B, T, dim) input tensor."""
    if value == "zeros":
        return torch.zeros(B, T, dim)
    if value == "ones":
        return torch.ones(B, T, dim)
    if value == "large":
        return torch.full((B, T, dim), 10.0)
    if value == "negative":
        return torch.full((B, T, dim), -1.0)
    if value == "mixed":
        torch.manual_seed(SEED + 1)
        return torch.randn(B, T, dim)  # includes negatives
    # default: random uniform [0, 1]
    torch.manual_seed(SEED)
    return torch.rand(B, T, dim)


# ======================================================================
# Shape Tests
# ======================================================================

class TestObserveOutputShape:
    """observe() must return (B, T) regardless of belief type."""

    def test_all_beliefs_return_bt(self, belief_mech_pairs):
        """Every belief.observe(input) returns shape (B, T)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if out.shape != (B, T):
                failures.append(
                    f"{belief.NAME}: expected ({B}, {T}), got {tuple(out.shape)}"
                )
        assert not failures, "Shape failures:\n" + "\n".join(failures)

    def test_output_is_2d(self, belief_mech_pairs):
        """Output tensor must always be exactly 2-dimensional."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if out.dim() != 2:
                failures.append(f"{belief.NAME}: dim={out.dim()}")
        assert not failures, "Non-2D outputs:\n" + "\n".join(failures)

    def test_batch_dim_matches(self, belief_mech_pairs):
        """Output batch dimension matches input batch dimension."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if out.shape[0] != B:
                failures.append(
                    f"{belief.NAME}: batch={out.shape[0]}, expected {B}"
                )
        assert not failures, "Batch mismatch:\n" + "\n".join(failures)

    def test_time_dim_matches(self, belief_mech_pairs):
        """Output time dimension matches input time dimension."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if out.shape[1] != T:
                failures.append(
                    f"{belief.NAME}: time={out.shape[1]}, expected {T}"
                )
        assert not failures, "Time mismatch:\n" + "\n".join(failures)


# ======================================================================
# Numerical Cleanliness
# ======================================================================

class TestObserveNumericalCleanliness:
    """No NaN, no Inf in any observe() output."""

    def test_no_nan_random_input(self, belief_mech_pairs):
        """observe() with random input produces no NaN."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN detected in: {failures}"

    def test_no_inf_random_input(self, belief_mech_pairs):
        """observe() with random input produces no Inf."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if torch.isinf(out).any():
                failures.append(belief.NAME)
        assert not failures, f"Inf detected in: {failures}"

    def test_no_nan_zeros_input(self, belief_mech_pairs):
        """observe() with all-zeros input produces no NaN."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "zeros")
            with torch.no_grad():
                out = belief.observe(inp)
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from zeros in: {failures}"

    def test_no_nan_ones_input(self, belief_mech_pairs):
        """observe() with all-ones input produces no NaN."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "ones")
            with torch.no_grad():
                out = belief.observe(inp)
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from ones in: {failures}"

    def test_no_nan_mixed_input(self, belief_mech_pairs):
        """observe() with mixed positive/negative input produces no NaN."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "mixed")
            with torch.no_grad():
                out = belief.observe(inp)
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from mixed in: {failures}"


# ======================================================================
# Value Bounds
# ======================================================================

class TestObserveValueBounds:
    """observe() output should be bounded, ideally in [0, 1]."""

    def test_output_lower_bounded(self, belief_mech_pairs):
        """Output >= -0.1 (allow small numerical tolerance below 0)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            mn = out.min().item()
            if mn < -0.1:
                failures.append(f"{belief.NAME}: min={mn:.4f}")
        assert not failures, "Below -0.1:\n" + "\n".join(failures)

    def test_output_upper_bounded(self, belief_mech_pairs):
        """Output <= 1.1 (allow small tolerance above 1)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            mx = out.max().item()
            if mx > 1.1:
                failures.append(f"{belief.NAME}: max={mx:.4f}")
        assert not failures, "Above 1.1:\n" + "\n".join(failures)

    def test_output_not_all_zero(self, belief_mech_pairs):
        """Random input should not produce all-zero output (degenerate)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if (out == 0.0).all():
                failures.append(belief.NAME)
        assert not failures, f"All-zero output from random input: {failures}"

    def test_output_dtype_float32(self, belief_mech_pairs):
        """Output must be float32."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            if out.dtype != torch.float32:
                failures.append(f"{belief.NAME}: dtype={out.dtype}")
        assert not failures, "Wrong dtype:\n" + "\n".join(failures)


# ======================================================================
# Determinism
# ======================================================================

class TestObserveDeterminism:
    """Same input must always produce same output (no stochastic observe)."""

    def test_deterministic_output(self, belief_mech_pairs):
        """Two calls with the same input produce identical output."""
        failures = []
        for belief, dim in belief_mech_pairs:
            torch.manual_seed(SEED)
            inp = torch.rand(B, T, dim)
            with torch.no_grad():
                out1 = belief.observe(inp.clone())
                out2 = belief.observe(inp.clone())
            if not torch.allclose(out1, out2, atol=1e-6):
                max_diff = (out1 - out2).abs().max().item()
                failures.append(f"{belief.NAME}: max_diff={max_diff:.2e}")
        assert not failures, "Non-deterministic:\n" + "\n".join(failures)


# ======================================================================
# Sensitivity (different inputs -> different outputs)
# ======================================================================

class TestObserveSensitivity:
    """Verify beliefs are not constant functions."""

    def test_different_inputs_different_outputs(self, belief_mech_pairs):
        """Random vs ones input should usually produce different output."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp_rand = _make_input(dim, "random")
            inp_ones = _make_input(dim, "ones")
            with torch.no_grad():
                out_rand = belief.observe(inp_rand)
                out_ones = belief.observe(inp_ones)
            if torch.allclose(out_rand, out_ones, atol=1e-5):
                failures.append(belief.NAME)
        # Allow a few constant beliefs (some might legitimately ignore input)
        max_constant = max(5, len(belief_mech_pairs) // 20)  # 5% tolerance
        assert len(failures) <= max_constant, (
            f"{len(failures)} beliefs constant (allowed {max_constant}):\n"
            + "\n".join(failures)
        )

    def test_temporal_variation(self, belief_mech_pairs):
        """Output should vary across time for random input."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim)
            with torch.no_grad():
                out = belief.observe(inp)
            # Check that not all timesteps are identical
            std_t = out.std(dim=1).mean().item()
            if std_t < 1e-8:
                failures.append(f"{belief.NAME}: std_t={std_t:.2e}")
        # Allow some beliefs to be temporally constant
        max_const = max(5, len(belief_mech_pairs) // 10)  # 10% tolerance
        assert len(failures) <= max_const, (
            f"{len(failures)} beliefs temporally constant:\n"
            + "\n".join(failures)
        )


# ======================================================================
# Edge Cases
# ======================================================================

class TestObserveEdgeCases:
    """Edge-case inputs should not crash observe()."""

    def test_zeros_input_valid(self, belief_mech_pairs):
        """All-zeros input does not crash and returns (B, T)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "zeros")
            try:
                with torch.no_grad():
                    out = belief.observe(inp)
                if out.shape != (B, T):
                    failures.append(f"{belief.NAME}: shape={tuple(out.shape)}")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "Zeros input failures:\n" + "\n".join(failures)

    def test_ones_input_valid(self, belief_mech_pairs):
        """All-ones input does not crash and returns (B, T)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "ones")
            try:
                with torch.no_grad():
                    out = belief.observe(inp)
                if out.shape != (B, T):
                    failures.append(f"{belief.NAME}: shape={tuple(out.shape)}")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "Ones input failures:\n" + "\n".join(failures)

    def test_large_input_no_overflow(self, belief_mech_pairs):
        """Large-magnitude input (10.0) does not produce Inf or NaN."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = _make_input(dim, "large")
            try:
                with torch.no_grad():
                    out = belief.observe(inp)
                if torch.isnan(out).any() or torch.isinf(out).any():
                    failures.append(f"{belief.NAME}: NaN/Inf from large input")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "Large input failures:\n" + "\n".join(failures)

    def test_single_timestep(self, belief_mech_pairs):
        """T=1 input should still work (no crash)."""
        failures = []
        for belief, dim in belief_mech_pairs:
            inp = torch.rand(B, 1, dim)
            try:
                with torch.no_grad():
                    out = belief.observe(inp)
                if out.shape != (B, 1):
                    failures.append(
                        f"{belief.NAME}: T=1 shape={tuple(out.shape)}"
                    )
            except Exception as exc:
                failures.append(f"{belief.NAME}: T=1 error: {exc!r}")
        assert not failures, "T=1 failures:\n" + "\n".join(failures)


# ======================================================================
# Belief Type Counts (sanity check)
# ======================================================================

class TestBeliefCounts:
    """Verify expected belief counts per type and function."""

    EXPECTED_PER_FUNCTION = {
        "F1": 17, "F2": 15, "F3": 15, "F4": 13,
        "F5": 14, "F6": 16, "F7": 17, "F8": 14, "F9": 10,
    }

    def test_total_beliefs_131(self, all_beliefs):
        """Total belief count is 131."""
        assert len(all_beliefs) == 131, f"Got {len(all_beliefs)} beliefs"

    def test_core_beliefs_36(self, all_core_beliefs):
        """Core belief count is 36."""
        assert len(all_core_beliefs) == 36, f"Got {len(all_core_beliefs)} core"

    def test_appraisal_beliefs_65(self, all_appraisal_beliefs):
        """Appraisal belief count is 65."""
        assert len(all_appraisal_beliefs) == 65, (
            f"Got {len(all_appraisal_beliefs)} appraisal"
        )

    def test_anticipation_beliefs_30(self, all_anticipation_beliefs):
        """Anticipation belief count is 30."""
        assert len(all_anticipation_beliefs) == 30, (
            f"Got {len(all_anticipation_beliefs)} anticipation"
        )

    def test_per_function_counts(self, beliefs_by_function):
        """Each function has the expected number of beliefs."""
        failures = []
        for fn, expected in self.EXPECTED_PER_FUNCTION.items():
            actual = len(beliefs_by_function.get(fn, []))
            if actual != expected:
                failures.append(f"{fn}: expected {expected}, got {actual}")
        assert not failures, "Count mismatches:\n" + "\n".join(failures)

    def test_every_belief_has_mechanism(self, all_beliefs):
        """Every belief has a non-empty MECHANISM attribute."""
        failures = []
        for b in all_beliefs:
            mech = getattr(b, "MECHANISM", None)
            if not mech:
                failures.append(b.NAME)
        assert not failures, f"Missing MECHANISM: {failures}"

    def test_every_belief_has_function(self, all_beliefs):
        """Every belief has a FUNCTION attribute like 'F1'..'F9'."""
        valid = {f"F{i}" for i in range(1, 10)}
        failures = []
        for b in all_beliefs:
            fn = getattr(b, "FUNCTION", None)
            if fn not in valid:
                failures.append(f"{b.NAME}: FUNCTION={fn!r}")
        assert not failures, "Invalid FUNCTION:\n" + "\n".join(failures)
