"""Micro-belief tests — PSCL encoder (Pitch Salience in Cortex).

Depth 1 encoder — requires BCH (depth 0) upstream output.

2 beliefs tested:
  5. pitch_prominence  (Core, tau=0.35)
  6. pitch_continuation (Anticipation)

Note: Pure sine tones can score HIGHER on pitch prominence than
harmonic complexes because their pitch is maximally unambiguous.
Tests focus on pitched vs unpitched contrasts.
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    A4, C4,
    crossfade, harmonic_complex, noise, silence, sine_tone,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
)


# =====================================================================
# 5. pitch_prominence (Core)
# =====================================================================

class TestPitchProminence:
    """Pitched sounds should score higher than noise/silence."""

    BELIEF = "pitch_prominence"

    def test_harmonic_vs_noise(self, runner):
        """Harmonic complex (clear f0) >> noise (no pitch)."""
        res_h = runner.run(
            harmonic_complex(A4, 10), [self.BELIEF]
        )[self.BELIEF]
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_n, "harmonic_complex", "noise")

    def test_sine_vs_noise(self, runner):
        """Pure sine (clear pitch) >> noise (no pitch)."""
        res_s = runner.run(sine_tone(A4), [self.BELIEF])[self.BELIEF]
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_s, res_n, "sine", "noise")

    def test_pitched_vs_silence(self, runner):
        """Harmonic complex > silence."""
        res_h = runner.run(
            harmonic_complex(A4, 10), [self.BELIEF]
        )[self.BELIEF]
        res_s = runner.run(silence(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_s, "harmonic_complex", "silence")

    def test_pitch_to_noise_transition(self, runner):
        """Crossfade harmonic->noise should show falling pitch prominence."""
        audio = crossfade(harmonic_complex(A4, 10, 3.0), noise(3.0), 3.0)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="falling")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(A4), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 6. pitch_continuation (Anticipation)
# =====================================================================

class TestPitchContinuation:
    """Sustained pitch should predict continuation; noise should not."""

    BELIEF = "pitch_continuation"

    def test_sustained_vs_noise(self, runner):
        """Sustained sine > noise."""
        res_s = runner.run(
            sine_tone(A4, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_n = runner.run(noise(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_s, res_n, "sustained_sine", "noise")

    def test_pitched_vs_silence(self, runner):
        """Harmonic complex > silence for pitch continuation."""
        res_h = runner.run(
            harmonic_complex(A4, 10, 3.0), [self.BELIEF]
        )[self.BELIEF]
        res_s = runner.run(silence(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_s, "harmonic_complex", "silence")

    def test_range(self, runner):
        result = runner.run(
            sine_tone(A4, 3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
