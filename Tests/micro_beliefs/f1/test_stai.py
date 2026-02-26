"""Micro-belief tests — STAI encoder (Spectral-Temporal Aesthetic Integration).

Cross-function mechanism (F5 primary, F1 beliefs).

3 beliefs tested:
  15. aesthetic_quality         (Core, tau=0.4)
  16. spectral_temporal_synergy (Appraisal)
  17. reward_response_pred      (Anticipation)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4,
    crossfade, dyad, harmonic_complex, noise,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
)


# =====================================================================
# 15. aesthetic_quality (Core)
# =====================================================================

class TestAestheticQuality:
    """Consonant harmonics should score higher than dissonant noise."""

    BELIEF = "aesthetic_quality"

    def test_consonant_vs_dissonant(self, runner):
        """Harmonic complex + P5 > m2 + noise."""
        beautiful = harmonic_complex(C4, 8) + dyad(C4, G4)
        ugly = dyad(C4, Db4) + noise(2.0, 0.1)
        res_b = runner.run(beautiful, [self.BELIEF])[self.BELIEF]
        res_u = runner.run(ugly, [self.BELIEF])[self.BELIEF]
        assert_greater(res_b, res_u, "consonant", "dissonant")

    def test_declining_aesthetic(self, runner):
        """Crossfade harmonic→dissonance should show falling quality."""
        audio = crossfade(
            harmonic_complex(C4, 8, 3.0),
            dyad(C4, Db4, 3.0),
            3.0,
        )
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="falling")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 16. spectral_temporal_synergy (Appraisal)
# =====================================================================

class TestSpectralTemporalSynergy:
    """Stable harmonic tones should show higher spectral-temporal synergy
    than noise."""

    BELIEF = "spectral_temporal_synergy"

    def test_harmonic_vs_noise(self, runner):
        """Harmonic complex > noise."""
        res_h = runner.run(
            harmonic_complex(C4, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_n = runner.run(noise(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_n, "harmonic", "noise")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 17. reward_response_pred (Anticipation)
# =====================================================================

class TestRewardResponsePred:
    """High aesthetic state should predict higher reward response."""

    BELIEF = "reward_response_pred"

    def test_beautiful_vs_noise(self, runner):
        """Consonant harmonics > noise."""
        beautiful = (
            harmonic_complex(C4, 8, 3.0, 0.2)
            + harmonic_complex(G4, 6, 3.0, 0.15)
        )
        res_b = runner.run(beautiful, [self.BELIEF])[self.BELIEF]
        res_n = runner.run(noise(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_b, res_n, "consonant_harmonics", "noise")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
