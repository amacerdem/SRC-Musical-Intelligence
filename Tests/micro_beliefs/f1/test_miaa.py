"""Micro-belief tests — MIAA relay (Musical Imagery & Auditory Awareness).

2 beliefs tested:
  9. timbral_character    (Core, tau=0.5)
  10. imagery_recognition (Anticipation)

MIAA reads tonalness (R³[14]) and spectral_autocorrelation (R³[17]).
Harmonic complexes vs silence shows clearer differentiation than vs noise.
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4,
    harmonic_complex, inharmonic_complex, silence,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range, assert_stable,
)


# =====================================================================
# 9. timbral_character (Core)
# =====================================================================

class TestTimbralCharacter:
    """Harmonic tones should produce stronger timbral character than
    silence or inharmonic tones."""

    BELIEF = "timbral_character"

    def test_harmonic_vs_silence(self, runner):
        """Harmonic complex > silence."""
        res_h = runner.run(
            harmonic_complex(C4, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_s = runner.run(silence(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_s, "harmonic_complex", "silence")

    def test_harmonic_vs_inharmonic(self, runner):
        """Harmonic complex > inharmonic (clearer timbral template)."""
        res_h = runner.run(
            harmonic_complex(C4, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_i = runner.run(
            inharmonic_complex(C4, 8, 1.15, 3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_h, res_i, "harmonic", "inharmonic")

    def test_stable_timbre(self, runner):
        """Sustained harmonic complex should have stable timbral character."""
        result = runner.run(
            harmonic_complex(C4, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4, 8), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 10. imagery_recognition (Anticipation)
# =====================================================================

class TestImageryRecognition:
    """Pitched sounds should produce higher recognition prediction
    than silence."""

    BELIEF = "imagery_recognition"

    def test_pitched_vs_silence(self, runner):
        """Harmonic complex > silence."""
        res_h = runner.run(
            harmonic_complex(C4, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_s = runner.run(silence(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_s, "harmonic_complex", "silence")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4, 8), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
