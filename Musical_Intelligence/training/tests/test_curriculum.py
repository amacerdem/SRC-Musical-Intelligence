"""Tests for curriculum weight scheduling.

Verifies:
- Phase transitions at correct epochs
- Weight interpolation between phases
- All 14 loss terms present in weights
"""
from __future__ import annotations

import pytest

from Musical_Intelligence.training.loss.curriculum import (
    LOSS_NAMES,
    CurriculumScheduler,
)


class TestCurriculumScheduler:
    """Test 5-phase curriculum weight schedule."""

    @pytest.fixture
    def scheduler(self):
        return CurriculumScheduler(interpolate=True)

    @pytest.fixture
    def scheduler_no_interp(self):
        return CurriculumScheduler(interpolate=False)

    def test_all_14_terms_present(self, scheduler):
        weights = scheduler.get_weights(epoch=0)
        for name in LOSS_NAMES:
            assert name in weights

    def test_phase_1(self, scheduler_no_interp):
        """Phase 1 (ep 0-49): Mel-heavy."""
        weights = scheduler_no_interp.get_weights(epoch=0)
        assert weights["encode_mel"] == 1.0
        assert weights["encode_c3"] == 0.0

    def test_phase_2(self, scheduler_no_interp):
        """Phase 2 (ep 50-149): R3-heavy."""
        weights = scheduler_no_interp.get_weights(epoch=50)
        assert weights["encode_r3"] == 1.0
        assert weights["encode_mel"] == 0.5

    def test_phase_3(self, scheduler_no_interp):
        """Phase 3 (ep 150-299): H3-heavy."""
        weights = scheduler_no_interp.get_weights(epoch=150)
        assert weights["encode_h3"] == 1.0

    def test_phase_4(self, scheduler_no_interp):
        """Phase 4 (ep 300-499): C3-heavy."""
        weights = scheduler_no_interp.get_weights(epoch=300)
        assert weights["encode_c3"] == 1.0

    def test_phase_5(self, scheduler_no_interp):
        """Phase 5 (ep 500+): Full balance."""
        weights = scheduler_no_interp.get_weights(epoch=500)
        assert weights["fill_c3"] == 1.0
        assert weights["encode_c3"] == 1.0

    def test_phase_numbers(self, scheduler):
        assert scheduler.get_phase(0) == 1
        assert scheduler.get_phase(25) == 1
        assert scheduler.get_phase(50) == 2
        assert scheduler.get_phase(100) == 2
        assert scheduler.get_phase(150) == 3
        assert scheduler.get_phase(300) == 4
        assert scheduler.get_phase(500) == 5
        assert scheduler.get_phase(1000) == 5

    def test_interpolation_midpoint(self, scheduler):
        """Test interpolation between Phase 1 and Phase 2."""
        weights = scheduler.get_weights(epoch=25)  # Midpoint of Phase 1→2

        # At epoch 25, 50% through Phase 1→2 transition
        # encode_mel should be between 1.0 (Phase 1) and 0.5 (Phase 2)
        assert 0.5 < weights["encode_mel"] < 1.0

        # encode_r3 should be between 0.5 (Phase 1) and 1.0 (Phase 2)
        assert 0.5 < weights["encode_r3"] < 1.0

    def test_weights_non_negative(self, scheduler):
        """All weights should be non-negative at every epoch."""
        for epoch in range(0, 700, 10):
            weights = scheduler.get_weights(epoch)
            for name, w in weights.items():
                assert w >= 0, f"Negative weight at epoch {epoch}: {name}={w}"

    def test_late_epoch_stable(self, scheduler_no_interp):
        """Weights should be stable after Phase 5."""
        w600 = scheduler_no_interp.get_weights(600)
        w1000 = scheduler_no_interp.get_weights(1000)
        for name in LOSS_NAMES:
            assert w600[name] == w1000[name]
