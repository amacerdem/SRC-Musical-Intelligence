"""Micro-belief tests — SDED relay (Spectral Dissonance Energy Detection).

1 belief tested:
  11. spectral_complexity (Appraisal)

SDED reads roughness, spectral flux, and deviation metrics.
Dissonant clusters with beating partials produce highest complexity.
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import (
    A4, C4, Db4, D4,
    dyad, noise, silence, sine_tone,
)
from Tests.micro_beliefs.assertions import assert_greater, assert_in_range


class TestSpectralComplexity:
    """Spectrally complex stimuli should score higher than simple ones."""

    BELIEF = "spectral_complexity"

    def test_cluster_vs_sine(self, runner):
        """Dense dissonant cluster > pure sine."""
        cluster = dyad(C4, Db4) + sine_tone(D4, 2.0, 0.3)
        res_s = runner.run(sine_tone(A4), [self.BELIEF])[self.BELIEF]
        res_c = runner.run(cluster, [self.BELIEF])[self.BELIEF]
        assert_greater(res_c, res_s, "cluster", "sine")

    def test_noise_vs_silence(self, runner):
        """Noise > silence (noise has spectral energy everywhere)."""
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        res_s = runner.run(silence(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_n, res_s, "noise", "silence")

    def test_range(self, runner):
        result = runner.run(sine_tone(A4), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)
