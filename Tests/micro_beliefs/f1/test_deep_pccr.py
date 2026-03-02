"""Deep PCCR tests — Multi-octave equivalence and pitch identity.

Validates:
  - Octave equivalence across multiple octave spans (C3/C4, C4/C5)
  - Octave > all non-octave intervals
  - Pitch identity gradient (harmonic > inharmonic > noise > silence)
  - Register effects on pitch identity
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4, Fsharp4, C5, midi_to_hz,
    harmonic_complex, inharmonic_complex, noise, silence, rich_dyad,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range,
)


C2 = midi_to_hz(36)
C3 = midi_to_hz(48)
C6 = midi_to_hz(84)


# =====================================================================
# octave_equivalence: Multi-octave invariance
# =====================================================================

class TestOctaveEquivalenceDeep:
    """Octave dyads should produce the highest octave equivalence."""

    BELIEF = "octave_equivalence"

    def test_octave_above_tritone(self, runner):
        oct = runner.run(rich_dyad(C4, C5, 6, 3.0), [self.BELIEF])[self.BELIEF]
        tt = runner.run(rich_dyad(C4, Fsharp4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(oct, tt, "Octave", "Tritone")

    def test_octave_above_fifth(self, runner):
        oct = runner.run(rich_dyad(C4, C5, 6, 3.0), [self.BELIEF])[self.BELIEF]
        p5 = runner.run(rich_dyad(C4, G4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(oct, p5, "Octave", "P5")

    def test_octave_above_m2(self, runner):
        oct = runner.run(rich_dyad(C4, C5, 6, 3.0), [self.BELIEF])[self.BELIEF]
        m2 = runner.run(rich_dyad(C4, Db4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(oct, m2, "Octave", "m2")

    def test_c3_c4_octave(self, runner):
        """C3-C4 octave > tritone (chroma invariance across low register)."""
        oct = runner.run(rich_dyad(C3, C4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        tt = runner.run(rich_dyad(C4, Fsharp4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(oct, tt, "C3-C4 octave", "Tritone")

    def test_c4_c5_octave(self, runner):
        """C4-C5 octave > tritone (standard register)."""
        oct = runner.run(rich_dyad(C4, C5, 6, 3.0), [self.BELIEF])[self.BELIEF]
        tt = runner.run(rich_dyad(C4, Fsharp4, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(oct, tt, "C4-C5 octave", "Tritone")

    @pytest.mark.parametrize("interval,f1,f2", [
        ("Octave", C4, C5),
        ("Tritone", C4, Fsharp4),
        ("m2", C4, Db4),
    ])
    def test_range(self, runner, interval, f1, f2):
        result = runner.run(rich_dyad(f1, f2, 6, 3.0), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, f"{self.BELIEF}({interval})")


# =====================================================================
# pitch_identity: Gradient and register effects
# =====================================================================

class TestPitchIdentityDeep:
    """Pitched sounds should produce stronger identity than unpitched."""

    BELIEF = "pitch_identity"

    def test_harmonic_vs_inharmonic(self, runner):
        h = runner.run(harmonic_complex(C4, 8, 3.0), [self.BELIEF])[self.BELIEF]
        i = runner.run(inharmonic_complex(C4, 8, 1.15, 3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(h, i, "harmonic", "inharmonic")

    def test_harmonic_vs_noise(self, runner):
        h = runner.run(harmonic_complex(C4, 8, 3.0), [self.BELIEF])[self.BELIEF]
        n = runner.run(noise(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(h, n, "harmonic", "noise")

    def test_harmonic_vs_silence(self, runner):
        h = runner.run(harmonic_complex(C4, 8, 3.0), [self.BELIEF])[self.BELIEF]
        s = runner.run(silence(3.0), [self.BELIEF])[self.BELIEF]
        assert_greater(h, s, "harmonic", "silence")

    @pytest.mark.parametrize("register,midi", [("C2", 36), ("C4", 60), ("C6", 84)])
    def test_register_nonzero(self, runner, register, midi):
        """Pitch identity should be non-zero at all registers."""
        freq = midi_to_hz(midi)
        result = runner.run(
            harmonic_complex(freq, 8, 3.0), [self.BELIEF]
        )[self.BELIEF]
        assert_in_range(result, f"{self.BELIEF}({register})")
