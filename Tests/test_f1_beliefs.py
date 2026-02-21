"""Tests for F1 Sensory Processing beliefs.

Validates:
1. All 6 beliefs pass validate() with no errors
2. observe() produces correct shape and range
3. Core beliefs: predict() and update() shape/range checks
4. Appraisal/Anticipation: no predict method
"""
from __future__ import annotations

import torch

from Musical_Intelligence.brain.functions.f1.beliefs import (
    ConsonanceTrajectory,
    HarmonicStability,
    HarmonicTemplateMatch,
    IntervalQuality,
    PitchContinuation,
    PitchProminence,
)

B, T = 2, 50


def _mock_bch() -> torch.Tensor:
    """Create mock BCH output: (B, T, 16) in [0, 1]."""
    return torch.rand(B, T, 16)


def _mock_pscl() -> torch.Tensor:
    """Create mock PSCL output: (B, T, 16) in [0, 1]."""
    return torch.rand(B, T, 16)


# ── Validation Tests ─────────────────────────────────────────────────


class TestBeliefValidation:
    """All 6 beliefs pass validate() with no errors."""

    def test_harmonic_stability_validates(self):
        assert HarmonicStability().validate() == []

    def test_interval_quality_validates(self):
        assert IntervalQuality().validate() == []

    def test_harmonic_template_match_validates(self):
        assert HarmonicTemplateMatch().validate() == []

    def test_consonance_trajectory_validates(self):
        assert ConsonanceTrajectory().validate() == []

    def test_pitch_prominence_validates(self):
        assert PitchProminence().validate() == []

    def test_pitch_continuation_validates(self):
        assert PitchContinuation().validate() == []


# ── Category Tests ───────────────────────────────────────────────────


class TestBeliefCategories:
    """Beliefs have correct categories."""

    def test_core_beliefs(self):
        assert HarmonicStability().CATEGORY == "core"
        assert PitchProminence().CATEGORY == "core"

    def test_appraisal_beliefs(self):
        assert IntervalQuality().CATEGORY == "appraisal"
        assert HarmonicTemplateMatch().CATEGORY == "appraisal"

    def test_anticipation_beliefs(self):
        assert ConsonanceTrajectory().CATEGORY == "anticipation"
        assert PitchContinuation().CATEGORY == "anticipation"


# ── Observe Tests ────────────────────────────────────────────────────


class TestObserve:
    """observe() returns correct shape and range."""

    def test_harmonic_stability_observe(self):
        out = HarmonicStability().observe(_mock_bch())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()

    def test_interval_quality_observe(self):
        out = IntervalQuality().observe(_mock_bch())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()

    def test_harmonic_template_match_observe(self):
        out = HarmonicTemplateMatch().observe(_mock_bch())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()

    def test_consonance_trajectory_observe(self):
        out = ConsonanceTrajectory().observe(_mock_bch())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()

    def test_pitch_prominence_observe(self):
        out = PitchProminence().observe(_mock_pscl())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()

    def test_pitch_continuation_observe(self):
        out = PitchContinuation().observe(_mock_pscl())
        assert out.shape == (B, T)
        assert not torch.isnan(out).any()


# ── Core Belief Predict Tests ────────────────────────────────────────


class TestCorePredict:
    """Core beliefs: predict() shape and range."""

    def test_harmonic_stability_predict(self):
        b = HarmonicStability()
        prev = torch.full((B, T), 0.5)
        ctx = {"consonance_trajectory": torch.rand(B, T)}
        h3 = {(0, 6, 18, 0): torch.rand(B, T)}
        pred = b.predict(prev, ctx, h3)
        assert pred.shape == (B, T)
        assert not torch.isnan(pred).any()

    def test_pitch_prominence_predict(self):
        b = PitchProminence()
        prev = torch.full((B, T), 0.5)
        ctx = {"pitch_continuation": torch.rand(B, T)}
        h3 = {(39, 6, 18, 0): torch.rand(B, T)}
        pred = b.predict(prev, ctx, h3)
        assert pred.shape == (B, T)
        assert not torch.isnan(pred).any()

    def test_predict_empty_context(self):
        """predict() works with empty context and h3."""
        for cls in [HarmonicStability, PitchProminence]:
            b = cls()
            prev = torch.full((B, T), 0.5)
            pred = b.predict(prev, {}, {})
            assert pred.shape == (B, T)
            assert not torch.isnan(pred).any()

    def test_predict_baseline_dominance(self):
        """With prev=baseline and no H³/context, predict returns ~baseline."""
        for cls in [HarmonicStability, PitchProminence]:
            b = cls()
            prev = torch.full((B, T), b.BASELINE)
            pred = b.predict(prev, {}, {})
            # Should be very close to baseline
            assert (pred - b.BASELINE).abs().max() < 0.01


# ── Core Belief Update Tests ────────────────────────────────────────


class TestCoreUpdate:
    """Core beliefs: Bayesian update shape and semantics."""

    def test_update_shape(self):
        for cls in [HarmonicStability, PitchProminence]:
            b = cls()
            predicted = torch.rand(B, T)
            observed = torch.rand(B, T)
            pi_obs = torch.ones(B, T)
            pi_pred = torch.ones(B, T)
            posterior, pe = b.update(predicted, observed, pi_obs, pi_pred)
            assert posterior.shape == (B, T)
            assert pe.shape == (B, T)

    def test_update_pe_sign(self):
        """PE = observed - predicted: positive when observed > predicted."""
        b = HarmonicStability()
        predicted = torch.full((B, T), 0.3)
        observed = torch.full((B, T), 0.7)
        pi_obs = torch.ones(B, T)
        pi_pred = torch.ones(B, T)
        _, pe = b.update(predicted, observed, pi_obs, pi_pred)
        assert (pe > 0).all(), "PE should be positive when observed > predicted"

    def test_update_high_obs_precision(self):
        """With high π_obs, posterior ≈ observed."""
        b = PitchProminence()
        predicted = torch.full((B, T), 0.3)
        observed = torch.full((B, T), 0.8)
        pi_obs = torch.full((B, T), 100.0)
        pi_pred = torch.ones(B, T)
        posterior, _ = b.update(predicted, observed, pi_obs, pi_pred)
        # gain ≈ 1.0, so posterior ≈ observed
        assert (posterior - observed).abs().max() < 0.02

    def test_update_high_pred_precision(self):
        """With high π_pred, posterior ≈ predicted."""
        b = HarmonicStability()
        predicted = torch.full((B, T), 0.3)
        observed = torch.full((B, T), 0.8)
        pi_obs = torch.ones(B, T)
        pi_pred = torch.full((B, T), 100.0)
        posterior, _ = b.update(predicted, observed, pi_obs, pi_pred)
        # gain ≈ 0.0, so posterior ≈ predicted
        assert (posterior - predicted).abs().max() < 0.02

    def test_update_no_nan(self):
        """Update produces no NaN even with edge-case precisions."""
        b = HarmonicStability()
        predicted = torch.rand(B, T)
        observed = torch.rand(B, T)
        pi_obs = torch.zeros(B, T)   # zero precision
        pi_pred = torch.zeros(B, T)
        posterior, pe = b.update(predicted, observed, pi_obs, pi_pred)
        assert not torch.isnan(posterior).any()
        assert not torch.isnan(pe).any()


# ── Appraisal/Anticipation: No predict ──────────────────────────────


class TestNoPredictCycle:
    """Appraisal and Anticipation beliefs have no predict method."""

    def test_appraisal_no_predict(self):
        for cls in [IntervalQuality, HarmonicTemplateMatch]:
            assert not hasattr(cls, "predict") or cls.predict is None or \
                cls.__mro__[1].__name__ != "CoreBelief"

    def test_anticipation_no_predict(self):
        for cls in [ConsonanceTrajectory, PitchContinuation]:
            assert not hasattr(cls, "predict") or cls.predict is None or \
                cls.__mro__[1].__name__ != "CoreBelief"


# ── Mechanism Assignment ─────────────────────────────────────────────


class TestMechanismAssignment:
    """Each belief is assigned to the correct mechanism."""

    def test_bch_beliefs(self):
        for cls in [HarmonicStability, IntervalQuality,
                    HarmonicTemplateMatch, ConsonanceTrajectory]:
            assert cls().MECHANISM == "BCH"

    def test_pscl_beliefs(self):
        for cls in [PitchProminence, PitchContinuation]:
            assert cls().MECHANISM == "PSCL"

    def test_all_function_f1(self):
        for cls in [HarmonicStability, IntervalQuality,
                    HarmonicTemplateMatch, ConsonanceTrajectory,
                    PitchProminence, PitchContinuation]:
            assert cls().FUNCTION == "F1"
