"""Micro-belief tests — CSG relay (Consonance-Salience Gradient).

1 belief tested:
  12. consonance_salience_gradient (Appraisal)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4,
    rich_dyad, silence,
)
from Tests.micro_beliefs.assertions import assert_greater, assert_in_range


class TestConsonanceSalienceGradient:
    """Dissonance drives salience network activation higher than consonance."""

    BELIEF = "consonance_salience_gradient"

    def test_dissonance_drives_salience(self, runner):
        """Minor 2nd (high dissonance) > Perfect 5th (consonant)."""
        res_m2 = runner.run(rich_dyad(C4, Db4), [self.BELIEF])[self.BELIEF]
        res_p5 = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_greater(res_m2, res_p5, "m2", "P5")

    def test_sound_vs_silence(self, runner):
        """Dissonant stimulus > silence."""
        res_m2 = runner.run(rich_dyad(C4, Db4), [self.BELIEF])[self.BELIEF]
        res_s = runner.run(silence(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_m2, res_s, "m2", "silence")

    def test_range(self, runner):
        result = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)
