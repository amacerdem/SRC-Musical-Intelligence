"""Micro-belief tests — BCH relay (Brainstem Consonance Hierarchy).

4 beliefs tested:
  1. harmonic_stability      (Core, tau=0.3)
  2. interval_quality        (Appraisal)
  3. harmonic_template_match (Appraisal)
  4. consonance_trajectory   (Anticipation)

Stimuli use ``rich_dyad()`` (harmonic complex pairs) rather than pure
sine ``dyad()`` because the Sethares / Plomp-Levelt psychoacoustic
models require multiple partials to produce meaningful consonance
ordering.

Calibrated ordering (rich_dyad, 6 harmonics each):
  harmonic_stability:  Unison > Octave > P5 > P4 > {TT,M3,m3,m6} > m2
  interval_quality:    Octave ~ Unison >> {mid group} >> m2
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4, C5,
    crossfade, harmonic_complex, inharmonic_complex, noise, rich_dyad,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
    assert_ordering, assert_stable,
)


# =====================================================================
# 1. harmonic_stability (Core)
# =====================================================================

class TestHarmonicStability:
    """Consonant intervals (rich harmonics) should score higher than
    dissonant ones; harmonic complexes > noise > inharmonic."""

    BELIEF = "harmonic_stability"

    def test_consonance_groups(self, runner):
        """Unison > P5 > m2 (clear separation groups)."""
        stims = {
            "Unison": rich_dyad(C4, C4),
            "P5": rich_dyad(C4, G4),
            "m2": rich_dyad(C4, Db4),
        }
        results = {
            k: runner.run(v, [self.BELIEF])[self.BELIEF]
            for k, v in stims.items()
        }
        assert_ordering(results, ["Unison", "P5", "m2"], self.BELIEF)

    def test_octave_above_fifth(self, runner):
        """Octave > P5 (2:1 > 3:2 ratio)."""
        res_oct = runner.run(rich_dyad(C4, C5), [self.BELIEF])[self.BELIEF]
        res_p5 = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_greater(res_oct, res_p5, "Octave", "P5")

    def test_transition_rising(self, runner):
        """Crossfade noise→harmonic should show rising stability."""
        audio = crossfade(noise(4.0), harmonic_complex(C4, 8, 4.0), 4.0)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_harmonic_vs_noise(self, runner):
        """Harmonic complex tone should score higher than noise."""
        res_h = runner.run(harmonic_complex(C4), [self.BELIEF])[self.BELIEF]
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_n, "harmonic_complex", "noise")

    def test_harmonic_vs_inharmonic(self, runner):
        """Harmonic > inharmonic complex."""
        res_h = runner.run(harmonic_complex(C4, 8), [self.BELIEF])[self.BELIEF]
        res_i = runner.run(
            inharmonic_complex(C4, 8, 1.15), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_h, res_i, "harmonic", "inharmonic")

    def test_sustained_stability(self, runner):
        """Sustained unison should be stable over time."""
        result = runner.run(
            rich_dyad(C4, C4, duration_s=3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        """Values should be in [0, 1]."""
        for audio in [rich_dyad(C4, G4), rich_dyad(C4, Db4), noise()]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. interval_quality (Appraisal)
# =====================================================================

class TestIntervalQuality:
    """Octave/Unison should score highest; m2 lowest."""

    BELIEF = "interval_quality"

    def test_octave_above_m2(self, runner):
        """Octave >> m2 (strong separation in E2:hierarchy)."""
        res_oct = runner.run(rich_dyad(C4, C5), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(rich_dyad(C4, Db4), [self.BELIEF])[self.BELIEF]
        assert_greater(res_oct, res_m2, "Octave", "m2")

    def test_unison_above_m2(self, runner):
        """Unison >> m2."""
        res_uni = runner.run(rich_dyad(C4, C4), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(rich_dyad(C4, Db4), [self.BELIEF])[self.BELIEF]
        assert_greater(res_uni, res_m2, "Unison", "m2")

    def test_harmonic_above_inharmonic(self, runner):
        """Harmonic complex >> inharmonic complex."""
        res_h = runner.run(harmonic_complex(C4, 8), [self.BELIEF])[self.BELIEF]
        res_i = runner.run(
            inharmonic_complex(C4, 8, 1.15), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_h, res_i, "harmonic", "inharmonic")

    def test_range(self, runner):
        result = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. harmonic_template_match (Appraisal)
# =====================================================================

class TestHarmonicTemplateMatch:
    """Harmonic series should match better than inharmonic or noise."""

    BELIEF = "harmonic_template_match"

    def test_harmonic_vs_inharmonic(self, runner):
        """Harmonic complex > inharmonic complex."""
        res_h = runner.run(harmonic_complex(C4, 8), [self.BELIEF])[self.BELIEF]
        res_i = runner.run(
            inharmonic_complex(C4, 8, 1.15), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_h, res_i, "harmonic", "inharmonic")

    def test_harmonic_vs_noise(self, runner):
        """Harmonic complex > noise."""
        res_h = runner.run(harmonic_complex(C4, 8), [self.BELIEF])[self.BELIEF]
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_n, "harmonic", "noise")

    def test_range(self, runner):
        result = runner.run(harmonic_complex(C4), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. consonance_trajectory (Anticipation)
# =====================================================================

class TestConsonanceTrajectory:
    """Forward prediction of consonance trend."""

    BELIEF = "consonance_trajectory"

    def test_stable_trajectory(self, runner):
        """Sustained unison should produce stable trajectory."""
        result = runner.run(
            rich_dyad(C4, C4, duration_s=3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_rising_trajectory(self, runner):
        """noise→harmonic crossfade should produce rising trajectory."""
        audio = crossfade(noise(4.0), harmonic_complex(C4, 8, 4.0), 4.0)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_falling_trajectory(self, runner):
        """harmonic→noise crossfade should produce falling trajectory."""
        audio = crossfade(harmonic_complex(C4, 8, 4.0), noise(4.0), 4.0)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="falling")

    def test_range(self, runner):
        result = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)
