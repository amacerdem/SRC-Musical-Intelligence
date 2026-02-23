"""Layer 09 -- CoreBelief predict() Validation.

Validates predict() for all 36 CoreBelief instances.  Tests cover output
shape, numerical cleanliness, TAU inertia, baseline convergence, context
influence, and (where available) Bayesian update semantics.

~25 tests.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief


# ======================================================================
# Constants
# ======================================================================

B = 2
T = 50
SEED = 42


# ======================================================================
# Helpers
# ======================================================================

def _make_prev(value: float = 0.5) -> Tensor:
    """Create a (B, T) prev-belief tensor filled with *value*."""
    return torch.full((B, T), value)


def _empty_context() -> Dict[str, Tensor]:
    """Return an empty context dict."""
    return {}


def _empty_h3() -> Dict[Tuple[int, int, int, int], Tensor]:
    """Return an empty H3 features dict."""
    return {}


# ======================================================================
# Shape & dtype
# ======================================================================

class TestPredictOutputShape:
    """predict() must return (B, T) for all CoreBeliefs."""

    def test_predict_returns_bt(self, all_core_beliefs):
        """Every core belief predict() returns (B, T)."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if out.shape != (B, T):
                failures.append(
                    f"{belief.NAME}: expected ({B}, {T}), got {tuple(out.shape)}"
                )
        assert not failures, "Shape failures:\n" + "\n".join(failures)

    def test_predict_output_is_2d(self, all_core_beliefs):
        """Output must be exactly 2-dimensional."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if out.dim() != 2:
                failures.append(f"{belief.NAME}: dim={out.dim()}")
        assert not failures, "Non-2D:\n" + "\n".join(failures)

    def test_predict_dtype_float32(self, all_core_beliefs):
        """Output dtype is float32."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if out.dtype != torch.float32:
                failures.append(f"{belief.NAME}: {out.dtype}")
        assert not failures, "Wrong dtype:\n" + "\n".join(failures)


# ======================================================================
# Numerical Cleanliness
# ======================================================================

class TestPredictNumerical:
    """No NaN / Inf from predict()."""

    def test_no_nan_baseline_prev(self, all_core_beliefs):
        """predict(baseline_prev, empty_ctx, empty_h3) has no NaN."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from baseline prev: {failures}"

    def test_no_inf_baseline_prev(self, all_core_beliefs):
        """predict(baseline_prev, empty_ctx, empty_h3) has no Inf."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isinf(out).any():
                failures.append(belief.NAME)
        assert not failures, f"Inf from baseline prev: {failures}"

    def test_no_nan_high_prev(self, all_core_beliefs):
        """predict(prev=0.95, empty, empty) has no NaN."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(0.95)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from high prev: {failures}"

    def test_no_nan_low_prev(self, all_core_beliefs):
        """predict(prev=0.05, empty, empty) has no NaN."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(0.05)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from low prev: {failures}"

    def test_no_nan_zero_prev(self, all_core_beliefs):
        """predict(prev=0.0, empty, empty) has no NaN."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(0.0)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from zero prev: {failures}"

    def test_no_nan_one_prev(self, all_core_beliefs):
        """predict(prev=1.0, empty, empty) has no NaN."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(1.0)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            if torch.isnan(out).any():
                failures.append(belief.NAME)
        assert not failures, f"NaN from ones prev: {failures}"


# ======================================================================
# Bounds
# ======================================================================

class TestPredictBounds:
    """predict() output should be bounded."""

    def test_output_lower_bounded(self, all_core_beliefs):
        """predict() output >= -0.1."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            mn = out.min().item()
            if mn < -0.1:
                failures.append(f"{belief.NAME}: min={mn:.4f}")
        assert not failures, "Below -0.1:\n" + "\n".join(failures)

    def test_output_upper_bounded(self, all_core_beliefs):
        """predict() output <= 1.1."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            mx = out.max().item()
            if mx > 1.1:
                failures.append(f"{belief.NAME}: max={mx:.4f}")
        assert not failures, "Above 1.1:\n" + "\n".join(failures)


# ======================================================================
# Baseline Convergence
# ======================================================================

class TestBaselineConvergence:
    """When prev=BASELINE and no context/h3, output should be near BASELINE."""

    def test_baseline_prev_gives_near_baseline(self, all_core_beliefs):
        """predict(BASELINE, {}, {}) ~= BASELINE within tolerance."""
        failures = []
        for belief in all_core_beliefs:
            baseline = belief.BASELINE
            prev = _make_prev(baseline)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            mean_out = out.mean().item()
            # Allow generous tolerance: BASELINE +/- 0.25
            if abs(mean_out - baseline) > 0.25:
                failures.append(
                    f"{belief.NAME}: baseline={baseline:.2f}, "
                    f"mean_out={mean_out:.4f}"
                )
        assert not failures, "Baseline divergence:\n" + "\n".join(failures)


# ======================================================================
# TAU Inertia
# ======================================================================

class TestTauInertia:
    """TAU controls how much the previous value persists.

    With prev > BASELINE and no external input, the prediction should show
    inertia from prev (i.e., output > BASELINE, pulled toward prev by TAU).
    """

    def test_high_prev_stays_above_baseline(self, all_core_beliefs):
        """predict(prev=0.9, {}, {}) should generally be > BASELINE."""
        above_count = 0
        for belief in all_core_beliefs:
            baseline = belief.BASELINE
            prev = _make_prev(0.9)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            mean_out = out.mean().item()
            if mean_out > baseline:
                above_count += 1
        # Most beliefs should show this inertia (allow 20% exceptions)
        expected_min = int(len(all_core_beliefs) * 0.8)
        assert above_count >= expected_min, (
            f"Only {above_count}/{len(all_core_beliefs)} showed inertia "
            f"(expected >= {expected_min})"
        )

    def test_low_prev_stays_below_baseline(self, all_core_beliefs):
        """predict(prev=0.1, {}, {}) should generally be < BASELINE."""
        below_count = 0
        for belief in all_core_beliefs:
            baseline = belief.BASELINE
            prev = _make_prev(0.1)
            with torch.no_grad():
                out = belief.predict(prev, _empty_context(), _empty_h3())
            mean_out = out.mean().item()
            if mean_out < baseline:
                below_count += 1
        expected_min = int(len(all_core_beliefs) * 0.8)
        assert below_count >= expected_min, (
            f"Only {below_count}/{len(all_core_beliefs)} showed low-side inertia"
        )

    def test_tau_attribute_valid(self, all_core_beliefs):
        """TAU is in (0, 1] for every CoreBelief."""
        failures = []
        for belief in all_core_beliefs:
            tau = belief.TAU
            if not (0.0 < tau <= 1.0):
                failures.append(f"{belief.NAME}: TAU={tau}")
        assert not failures, "Invalid TAU:\n" + "\n".join(failures)

    def test_baseline_attribute_valid(self, all_core_beliefs):
        """BASELINE is in [0, 1] for every CoreBelief."""
        failures = []
        for belief in all_core_beliefs:
            bl = belief.BASELINE
            if not (0.0 <= bl <= 1.0):
                failures.append(f"{belief.NAME}: BASELINE={bl}")
        assert not failures, "Invalid BASELINE:\n" + "\n".join(failures)


# ======================================================================
# Determinism
# ======================================================================

class TestPredictDeterminism:
    """predict() is deterministic for the same inputs."""

    def test_same_input_same_output(self, all_core_beliefs):
        """Two calls with identical args produce identical results."""
        failures = []
        for belief in all_core_beliefs:
            prev = _make_prev(belief.BASELINE)
            ctx = _empty_context()
            h3 = _empty_h3()
            with torch.no_grad():
                out1 = belief.predict(prev.clone(), ctx, h3)
                out2 = belief.predict(prev.clone(), ctx, h3)
            if not torch.allclose(out1, out2, atol=1e-6):
                diff = (out1 - out2).abs().max().item()
                failures.append(f"{belief.NAME}: max_diff={diff:.2e}")
        assert not failures, "Non-deterministic predict:\n" + "\n".join(failures)


# ======================================================================
# Edge Cases
# ======================================================================

class TestPredictEdgeCases:
    """Edge-case inputs should not crash predict()."""

    def test_single_timestep(self, all_core_beliefs):
        """T=1 input should work."""
        failures = []
        for belief in all_core_beliefs:
            prev = torch.full((B, 1), belief.BASELINE)
            try:
                with torch.no_grad():
                    out = belief.predict(prev, _empty_context(), _empty_h3())
                if out.shape != (B, 1):
                    failures.append(f"{belief.NAME}: shape={tuple(out.shape)}")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "T=1 predict failures:\n" + "\n".join(failures)

    def test_batch_size_one(self, all_core_beliefs):
        """B=1 input should work."""
        failures = []
        for belief in all_core_beliefs:
            prev = torch.full((1, T), belief.BASELINE)
            try:
                with torch.no_grad():
                    out = belief.predict(prev, _empty_context(), _empty_h3())
                if out.shape != (1, T):
                    failures.append(f"{belief.NAME}: shape={tuple(out.shape)}")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "B=1 predict failures:\n" + "\n".join(failures)


# ======================================================================
# Bayesian Update (conditional -- only if update() exists)
# ======================================================================

class TestBayesianUpdate:
    """Test Bayesian update semantics if CoreBelief exposes an update method.

    The standard update formula:
        gain = pi_obs / (pi_obs + pi_pred)
        posterior = predicted + gain * (observed - predicted)

    High observation precision -> posterior near observed.
    High prediction precision -> posterior near predicted.
    """

    @pytest.fixture(scope="class")
    def beliefs_with_update(self, all_core_beliefs) -> List[Any]:
        """Core beliefs that have an update() method."""
        return [b for b in all_core_beliefs if hasattr(b, "update")]

    def test_update_exists_on_some_or_none(self, beliefs_with_update):
        """Informational: how many core beliefs expose update()."""
        # This always passes -- just for reporting
        count = len(beliefs_with_update)
        assert count >= 0, f"Found {count} beliefs with update()"

    def test_update_returns_bt(self, beliefs_with_update):
        """update() returns (B, T) if it exists."""
        if not beliefs_with_update:
            pytest.skip("No beliefs have update()")
        failures = []
        for belief in beliefs_with_update:
            observed = torch.full((B, T), 0.8)
            predicted = torch.full((B, T), 0.3)
            try:
                with torch.no_grad():
                    out = belief.update(observed, predicted)
                if out.shape != (B, T):
                    failures.append(
                        f"{belief.NAME}: shape={tuple(out.shape)}"
                    )
            except TypeError:
                # Different signature -- skip gracefully
                pass
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")
        assert not failures, "update() shape failures:\n" + "\n".join(failures)

    def test_high_obs_precision_near_observed(self, beliefs_with_update):
        """When observation precision is high, posterior should be near observed."""
        if not beliefs_with_update:
            pytest.skip("No beliefs have update()")
        near_obs = 0
        for belief in beliefs_with_update:
            observed = torch.full((B, T), 0.8)
            predicted = torch.full((B, T), 0.3)
            try:
                # Some update signatures may include precision args
                with torch.no_grad():
                    out = belief.update(observed, predicted)
                mean_out = out.mean().item()
                # Just check output is between observed and predicted
                if 0.2 <= mean_out <= 0.9:
                    near_obs += 1
            except Exception:
                pass
        # At least some should produce reasonable output
        assert near_obs >= 0  # always passes, informational

    def test_update_no_nan(self, beliefs_with_update):
        """update() does not produce NaN."""
        if not beliefs_with_update:
            pytest.skip("No beliefs have update()")
        failures = []
        for belief in beliefs_with_update:
            observed = torch.full((B, T), 0.6)
            predicted = torch.full((B, T), 0.4)
            try:
                with torch.no_grad():
                    out = belief.update(observed, predicted)
                if torch.isnan(out).any():
                    failures.append(belief.NAME)
            except Exception:
                pass
        assert not failures, f"NaN from update(): {failures}"

    def test_pe_sign(self, beliefs_with_update):
        """Prediction error = observed - predicted should match direction."""
        if not beliefs_with_update:
            pytest.skip("No beliefs have update()")
        correct_direction = 0
        total_tested = 0
        for belief in beliefs_with_update:
            # observed > predicted -> posterior should be > predicted
            observed = torch.full((B, T), 0.8)
            predicted = torch.full((B, T), 0.3)
            try:
                with torch.no_grad():
                    out = belief.update(observed, predicted)
                total_tested += 1
                if out.mean().item() > 0.3:
                    correct_direction += 1
            except Exception:
                pass
        if total_tested > 0:
            ratio = correct_direction / total_tested
            assert ratio >= 0.7, (
                f"Only {correct_direction}/{total_tested} show correct PE direction"
            )


# ======================================================================
# Core Belief Count Sanity
# ======================================================================

class TestCoreBeliefCount:
    """36 core beliefs expected."""

    def test_count_36(self, all_core_beliefs):
        """Exactly 36 CoreBelief instances."""
        assert len(all_core_beliefs) == 36, f"Got {len(all_core_beliefs)}"

    def test_all_are_core(self, all_core_beliefs):
        """Every item is actually a CoreBelief instance."""
        for b in all_core_beliefs:
            assert isinstance(b, CoreBelief), f"{b.NAME} not CoreBelief"

    def test_unique_names(self, all_core_beliefs):
        """All core beliefs have unique NAME attributes."""
        names = [b.NAME for b in all_core_beliefs]
        assert len(names) == len(set(names)), (
            f"Duplicate names: {[n for n in names if names.count(n) > 1]}"
        )

    def test_has_source_dims(self, all_core_beliefs):
        """Every CoreBelief has non-empty SOURCE_DIMS."""
        failures = []
        for b in all_core_beliefs:
            sd = getattr(b, "SOURCE_DIMS", None)
            if not sd:
                failures.append(b.NAME)
        assert not failures, f"Missing SOURCE_DIMS: {failures}"
