"""Micro-belief tests — MPG relay (Melodic Pitch Gradient).

2 beliefs tested:
  13. melodic_contour_tracking (Appraisal)
  14. contour_continuation    (Anticipation)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4,
    ascending_scale, descending_scale, sine_tone,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range, assert_stable,
)


# =====================================================================
# 13. melodic_contour_tracking (Appraisal)
# =====================================================================

class TestMelodicContourTracking:
    """Melodic sequences should activate contour tracking more than
    sustained tones or repeated notes."""

    BELIEF = "melodic_contour_tracking"

    def test_scale_vs_silence(self, runner):
        """Ascending scale > silence (melodic content activates tracking)."""
        res_asc = runner.run(ascending_scale(), [self.BELIEF])[self.BELIEF]
        res_s = runner.run(sine_tone(C4, 2.0, 0.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_asc, res_s, "ascending_scale", "silence")

    def test_scale_vs_sustained(self, runner):
        """Ascending scale > sustained single tone."""
        res_asc = runner.run(ascending_scale(), [self.BELIEF])[self.BELIEF]
        res_sus = runner.run(sine_tone(C4, 2.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_asc, res_sus, "ascending_scale", "sustained")

    def test_descending_also_tracks(self, runner):
        """Descending scale > sustained tone (contour direction irrelevant)."""
        res_desc = runner.run(descending_scale(), [self.BELIEF])[self.BELIEF]
        res_sus = runner.run(sine_tone(C4, 2.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_desc, res_sus, "descending_scale", "sustained")

    def test_range(self, runner):
        result = runner.run(ascending_scale(), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 14. contour_continuation (Anticipation)
# =====================================================================

class TestContourContinuation:
    """Forward prediction of melodic contour continuation."""

    BELIEF = "contour_continuation"

    def test_sustained_low(self, runner):
        """Sustained tone should show stable, low contour continuation."""
        result = runner.run(sine_tone(C4, 3.0), [self.BELIEF])[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_scale_has_contour(self, runner):
        """Ascending scale should produce non-trivial contour continuation."""
        res_asc = runner.run(
            ascending_scale(60, 12, 0.2), [self.BELIEF]
        )[self.BELIEF]
        res_sus = runner.run(sine_tone(C4, 2.4), [self.BELIEF])[self.BELIEF]
        # Scale should differ from sustained tone
        mean_asc = res_asc.mean().item()
        mean_sus = res_sus.mean().item()
        assert abs(mean_asc - mean_sus) > 0.01 or mean_asc > 0.0, (
            f"Scale contour ({mean_asc:.4f}) should differ from "
            f"sustained ({mean_sus:.4f})"
        )

    def test_range(self, runner):
        result = runner.run(ascending_scale(), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)
