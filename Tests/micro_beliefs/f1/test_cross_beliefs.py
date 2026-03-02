"""Cross-belief consistency tests — verify correlated F1 belief pairs.

Scientific claims:
  - harmonic_stability UP => consonance_salience_gradient DOWN (inverse)
  - harmonic_stability UP => interval_quality UP (positive)
  - pitch_prominence UP => pitch_identity UP (positive)
  - aesthetic_quality correlates with harmonic_stability (rank order)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4, C5,
    harmonic_complex, noise, rich_dyad,
)
from Tests.micro_beliefs.assertions import assert_greater, WARMUP_FRAMES


def _mean(t):
    """Trimmed mean after warmup."""
    if t.shape[-1] > WARMUP_FRAMES * 2:
        return t[:, WARMUP_FRAMES:].mean().item()
    return t.mean().item()


class TestHSvCSG:
    """harmonic_stability UP <=> consonance_salience_gradient DOWN."""

    def test_p1_vs_m2(self, runner):
        """Unison has high HS, low CSG; m2 has low HS, high CSG."""
        targets = ["harmonic_stability", "consonance_salience_gradient"]
        p1 = runner.run(rich_dyad(C4, C4, 6, 3.0), targets)
        m2 = runner.run(rich_dyad(C4, Db4, 6, 3.0), targets)
        assert _mean(p1["harmonic_stability"]) > _mean(m2["harmonic_stability"])
        assert _mean(m2["consonance_salience_gradient"]) > _mean(p1["consonance_salience_gradient"])

    def test_p5_vs_m2(self, runner):
        """P5 has high HS, low CSG; m2 has low HS, high CSG."""
        targets = ["harmonic_stability", "consonance_salience_gradient"]
        p5 = runner.run(rich_dyad(C4, G4, 6, 3.0), targets)
        m2 = runner.run(rich_dyad(C4, Db4, 6, 3.0), targets)
        assert _mean(p5["harmonic_stability"]) > _mean(m2["harmonic_stability"])
        assert _mean(m2["consonance_salience_gradient"]) > _mean(p5["consonance_salience_gradient"])


class TestHSvIQ:
    """harmonic_stability UP => interval_quality UP."""

    def test_p1_vs_m2(self, runner):
        targets = ["harmonic_stability", "interval_quality"]
        p1 = runner.run(rich_dyad(C4, C4, 6, 3.0), targets)
        m2 = runner.run(rich_dyad(C4, Db4, 6, 3.0), targets)
        assert _mean(p1["harmonic_stability"]) > _mean(m2["harmonic_stability"])
        assert _mean(p1["interval_quality"]) > _mean(m2["interval_quality"])

    def test_p8_vs_m2(self, runner):
        targets = ["harmonic_stability", "interval_quality"]
        p8 = runner.run(rich_dyad(C4, C5, 6, 3.0), targets)
        m2 = runner.run(rich_dyad(C4, Db4, 6, 3.0), targets)
        assert _mean(p8["harmonic_stability"]) > _mean(m2["harmonic_stability"])
        assert _mean(p8["interval_quality"]) > _mean(m2["interval_quality"])


class TestPPvPI:
    """pitch_prominence UP => pitch_identity UP."""

    def test_harmonic_vs_noise(self, runner):
        targets = ["pitch_prominence", "pitch_identity"]
        h = runner.run(harmonic_complex(C4, 8, 3.0), targets)
        n = runner.run(noise(3.0), targets)
        assert _mean(h["pitch_prominence"]) > _mean(n["pitch_prominence"])
        assert _mean(h["pitch_identity"]) > _mean(n["pitch_identity"])
