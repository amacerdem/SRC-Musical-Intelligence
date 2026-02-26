"""Micro-belief tests — PCCR associator (Pitch Chroma Class Recognition).

Depth 2 associator — requires BCH (depth 0) + PSCL (depth 1) upstream.

2 beliefs tested:
  7. pitch_identity       (Core, tau=0.4)
  8. octave_equivalence   (Appraisal)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    A4, C4, C5, Fsharp4, G4,
    harmonic_complex, inharmonic_complex, noise, rich_dyad,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range,
)


# =====================================================================
# 7. pitch_identity (Core)
# =====================================================================

class TestPitchIdentity:
    """Clear harmonic tones should produce confident pitch-class
    identification; inharmonic/noise should not."""

    BELIEF = "pitch_identity"

    def test_harmonic_vs_inharmonic(self, runner):
        """Harmonic complex (clear chroma) > inharmonic (ambiguous chroma)."""
        res_h = runner.run(
            harmonic_complex(C4, 8), [self.BELIEF]
        )[self.BELIEF]
        res_i = runner.run(
            inharmonic_complex(C4, 8, 1.15), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_h, res_i, "harmonic", "inharmonic")

    def test_pitched_vs_noise(self, runner):
        """Harmonic complex >> noise."""
        res_h = runner.run(
            harmonic_complex(A4, 8), [self.BELIEF]
        )[self.BELIEF]
        res_n = runner.run(noise(), [self.BELIEF])[self.BELIEF]
        assert_greater(res_h, res_n, "harmonic", "noise")

    def test_range(self, runner):
        result = runner.run(
            harmonic_complex(C4), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 8. octave_equivalence (Appraisal)
# =====================================================================

class TestOctaveEquivalence:
    """Octave pairs should show highest octave equivalence."""

    BELIEF = "octave_equivalence"

    def test_octave_vs_tritone(self, runner):
        """Rich octave pair > rich tritone dyad."""
        res_oct = runner.run(rich_dyad(C4, C5), [self.BELIEF])[self.BELIEF]
        res_tt = runner.run(
            rich_dyad(C4, Fsharp4), [self.BELIEF]
        )[self.BELIEF]
        assert_greater(res_oct, res_tt, "octave", "tritone")

    def test_octave_vs_fifth(self, runner):
        """Rich octave pair > rich perfect fifth."""
        res_oct = runner.run(rich_dyad(C4, C5), [self.BELIEF])[self.BELIEF]
        res_p5 = runner.run(rich_dyad(C4, G4), [self.BELIEF])[self.BELIEF]
        assert_greater(res_oct, res_p5, "octave", "P5")

    def test_range(self, runner):
        result = runner.run(rich_dyad(C4, C5), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, self.BELIEF)
