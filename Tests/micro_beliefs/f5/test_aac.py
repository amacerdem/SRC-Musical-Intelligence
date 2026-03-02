"""Micro-belief tests — AAC relay (Autonomic-Affective Coupling).

5 beliefs tested:
  1. emotional_arousal   (Core, tau=0.5)  — "How activated am I?"
  2. chills_intensity     (Appraisal)      — goosebump / frisson signal
  3. ans_dominance        (Appraisal)      — autonomic nervous system drive
  4. driving_signal       (Anticipation)   — rhythmic energy prediction
  (Note: AAC has 5 beliefs in code — the 5th discovered during exploration)

Mechanism: AAC (14D relay, Phase 0a)
Key R³ inputs: amplitude[7], loudness[10], onset_strength[11],
               spectral_flux[21], entropy[22]
Key H³: amplitude at H9 (350ms micro), onset/flux at H16

Formulas:
  emotional_arousal = 0.50×E0:emotional_arousal + 0.30×P0:current_intensity
                      + 0.20×I1:ans_composite
  chills_intensity  = I0:chills_intensity (1.0)
  ans_dominance     = E1:ans_response (1.0)
  driving_signal    = P1:driving_signal (1.0)

Science:
  - Salimpoor 2011: chills + DA release, N=217, PET
  - Gomez 2007: ANS coupling with music, N=24
  - Rickard 2004: arousal from amplitude + tempo, N=60
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import noise, silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, STRINGS,
    midi_note, midi_chord, midi_isochronous,
    midi_crescendo,
    major_triad,
    C4 as MC4,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
    assert_stable,
)


# =====================================================================
# 1. emotional_arousal (Core, tau=0.5)
# =====================================================================

class TestEmotionalArousal:
    """Loud + fast stimuli should score highest for arousal.

    observe = 0.50×E0 + 0.30×P0 + 0.20×I1
    E0 driven by amplitude + onset_strength + spectral_flux.

    Science: Rickard 2004 — arousal from amplitude + tempo (N=60).
    """

    BELIEF = "emotional_arousal"

    def test_loud_above_quiet(self, runner):
        """Loud chord (vel=120) >> soft chord (vel=30) for arousal.

        Rickard 2004: amplitude is primary arousal predictor.
        """
        res_loud = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=120),
            [self.BELIEF],
        )[self.BELIEF]
        res_quiet = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=30),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_loud, res_quiet, "loud_chord", "quiet_chord")

    def test_fast_above_slow(self, runner):
        """Fast isochronous (240 BPM) >> slow (60 BPM) for arousal.

        High onset density → high onset_strength → high E0.
        """
        res_fast = runner.run(
            midi_isochronous(MC4, 240.0, 24, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_slow = runner.run(
            midi_isochronous(MC4, 60.0, 8, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_fast, res_slow, "fast_240bpm", "slow_60bpm")

    def test_loud_fast_above_quiet_sustained(self, runner):
        """Loud fast beats >> quiet sustained note for arousal.

        Combined amplitude + onset density → maximum E0 separation.
        Single-variable contrasts (entropy, noise) have too narrow range.
        """
        res_loud_fast = runner.run(
            midi_isochronous(MC4, 180.0, 18, program=PIANO, velocity=120),
            [self.BELIEF],
        )[self.BELIEF]
        res_quiet = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=30),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_loud_fast, res_quiet, "loud_fast", "quiet_sustained")

    def test_crescendo_rising(self, runner):
        """Crescendo should show rising arousal.

        Increasing amplitude → increasing E0 → rising emotional_arousal.
        """
        audio = midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_above_silence(self, runner):
        """Loud chord >> silence."""
        res_loud = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=100),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_loud, res_sil, "loud_chord", "silence")

    def test_stable_on_sustained(self, runner):
        """Sustained organ chord should be stable."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=PIANO, velocity=120),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. chills_intensity (Appraisal)
# =====================================================================

class TestChillsIntensity:
    """Chills / frisson — direct relay from I0:chills_intensity.

    observe = I0:chills_intensity (1.0)
    Peaks at loudness crescendo apexes.

    Science: Salimpoor 2011 — chills + DA release in nucleus accumbens (PET, N=217).
    """

    BELIEF = "chills_intensity"

    def test_crescendo_above_quiet_sustained(self, runner):
        """Crescendo ending loud >> sustained quiet for chills.

        Salimpoor 2011: chills peak at expectation violations (crescendo apex).
        """
        res_cresc = runner.run(
            midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO),
            [self.BELIEF],
        )[self.BELIEF]
        res_quiet = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=40),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cresc, res_quiet, "crescendo", "quiet_sustained")

    def test_above_silence(self, runner):
        """Musical content >> silence for chills."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=STRINGS, velocity=90),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "strings_chord", "silence")

    def test_stable_on_sustained(self, runner):
        """Sustained chord should produce stable chills signal."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            midi_crescendo(MC4, 12, 0.4, 20, 120),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. ans_dominance (Appraisal)
# =====================================================================

class TestAnsDominance:
    """Autonomic nervous system drive — direct relay from E1:ans_response.

    observe = E1:ans_response (1.0)
    High energy + arousal → high ANS activation.

    Science: Gomez 2007 — ANS coupling with music arousal (N=24).
    """

    BELIEF = "ans_dominance"

    def test_high_energy_above_low(self, runner):
        """Loud fast beats >> quiet sustained note for ANS dominance.

        Gomez 2007: ANS responds to amplitude × onset density.
        """
        res_high = runner.run(
            midi_isochronous(MC4, 180.0, 18, program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        res_low = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=35),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_high, res_low, "loud_fast", "quiet_sustained")

    def test_above_silence(self, runner):
        """Energetic beats >> silence."""
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=90),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_sil, "beats", "silence")

    def test_stable(self, runner):
        """Sustained chord should be stable."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            midi_isochronous(MC4, 120.0, 12),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. driving_signal (Anticipation)
# =====================================================================

class TestDrivingSignal:
    """Rhythmic energy prediction — direct relay from P1:driving_signal.

    observe = P1:driving_signal (1.0)
    Tracks rhythmic driving force — higher for regular beats.
    """

    BELIEF = "driving_signal"

    def test_rhythmic_above_static(self, runner):
        """Isochronous beats >> sustained chord for driving signal.

        Regular onsets create rhythmic drive; sustained tone has none.
        """
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        res_static = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_beats, res_static, "isochronous", "sustained_chord")

    def test_rhythmic_above_noise(self, runner):
        """Isochronous beats >> noise for driving signal.

        Regular onsets create clear rhythmic drive; noise has no onset structure.
        P1 relay has narrow dynamic range for tempo differences alone.
        """
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_noise, "isochronous", "noise")

    def test_above_silence(self, runner):
        """Rhythmic content >> silence."""
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_sil, "beats", "silence")

    def test_stable(self, runner):
        """Sustained rhythm should be stable."""
        result = runner.run(
            midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            midi_isochronous(MC4, 120.0, 12),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
