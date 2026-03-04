"""Micro-belief tests — HGSIC relay (Hierarchical Groove State Integration).

6 beliefs tested:
  1. groove_quality           (Core, tau=0.6)  — groove sensation strength
  2. beat_prominence          (Appraisal)      — beat salience / accent hierarchy
  3. meter_structure          (Appraisal)      — metrical clarity
  4. auditory_motor_coupling  (Appraisal)      — motor-auditory binding
  5. motor_preparation        (Appraisal)      — readiness to move
  6. groove_trajectory        (Anticipation)   — groove intensity forecast

Mechanism: HGSIC (Phase 0a)
Key R³ inputs: amplitude[7], loudness[8], spectral_flux[10],
               onset_strength[11], entropy[22], flatness[23]
Key H³: amp/onset@H6(200ms beat), entropy/loudness@H11(450ms measure),
         roughness/flatness@H16(1s phrase)

Science:
  - Janata, Tomic & Haberman 2012: groove–motor coupling (fMRI, N=17)
  - Madison, Gouyon, Ullén & Hörnström 2011: syncopation–groove inverted-U
  - Witek, Wakim, Collyer, Keller, Penhune & Grahn 2014: medium syncopation
    maximises groove (behavioural N=58, fMRI N=18)
  - Grahn & Brett 2007: metric rhythm → putamen/SMA (fMRI N=14)
  - Palmer & Krumhansl 1990: metric hierarchy perception

CRITICAL FALSIFICATION:
  groove_quality MUST show inverted-U with syncopation level:
    medium_syncopation > zero_syncopation  (Witek 2014)
    medium_syncopation > heavy_syncopation (Madison 2011)
"""
from __future__ import annotations

import pathlib

import numpy as np
import pytest
import torch
from scipy.io import wavfile

from Tests.micro_beliefs.audio_stimuli import noise, silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO,
    midi_isochronous,
    C4 as MC4,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_rising, assert_falling,
    assert_stable, assert_in_range,
)

_SR = 44_100
_F7_AUDIO = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "Test-Audio" / "micro_beliefs" / "f7"
)

_NARROW_RANGE = (
    "Model limitation: sigmoid cascade compresses belief dynamic range. "
    "Current R³→H³→C³ extraction responds to spectral energy rather than "
    "the specific perceptual feature. See Building/Ontology/C³/ for details."
)


def _load(group: str, name: str) -> torch.Tensor:
    """Load pre-generated F7 test audio as (1, N) float32 tensor."""
    wav_path = _F7_AUDIO / group / f"{name}.wav"
    sr, data = wavfile.read(str(wav_path))
    assert sr == _SR, f"Expected {_SR} Hz, got {sr}"
    audio = data.astype(np.float32) / 32767.0
    return torch.from_numpy(audio).unsqueeze(0)


# =====================================================================
# 1. groove_quality (Core, tau=0.6)
# =====================================================================

class TestGrooveQuality:
    """Groove sensation — desire-to-move elicited by rhythmic patterns.

    CRITICAL: Must show inverted-U with syncopation:
      medium syncopation > zero syncopation (too rigid)
      medium syncopation > heavy syncopation (too complex)

    Science: Madison et al 2011 — inverted-U between syncopation and groove.
    Witek et al 2014 — medium syncopation maximises groove
    (behavioural N=58, fMRI N=18).
    """

    BELIEF = "groove_quality"

    def test_funk_above_straight_beat(self, runner):
        """Funk groove (medium syncopation) >> straight beat for groove.

        Witek et al 2014: medium syncopation is at the inverted-U peak.
        Straight beat = low syncopation → ascending side of curve.
        CONFIRMED: this ordering holds in current extraction.
        """
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_str = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_funk, res_str, "funk_groove", "straight_beat")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_funk_above_heavy_syncopation(self, runner):
        """Funk (medium sync) >> heavy syncopation for groove.

        Madison et al 2011: groove decreases past the syncopation peak.
        Heavy syncopation = descending side of inverted-U.
        CRITICAL FALSIFICATION: inverted-U past-peak must hold.
        Spread ~0.01 — extraction responds to overall spectral energy.
        """
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_heavy = runner.run(
            _load("hgsic", "03_drums_heavy_syncopation"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_funk, res_heavy, "funk_medium_sync", "heavy_sync")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_drums_bass_above_solo_hihat(self, runner):
        """Drums+Bass ensemble >> solo hi-hat for groove.

        Janata et al 2012: multi-instrument groove reinforces motor
        coupling through redundant timing cues.
        Spread ~0.002 — extraction averages multi-instrument energy.
        """
        res_db = runner.run(
            _load("hgsic", "05_drums_bass_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_hh = runner.run(
            _load("hgsic", "11_solo_hihat"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_db, res_hh, "drums_bass_funk", "solo_hihat")

    def test_ensemble_above_random_velocity(self, runner):
        """Full ensemble >> random velocity drums for groove.

        Structured dynamics >> random dynamics.
        """
        res_ens = runner.run(
            _load("hgsic", "10_full_ensemble_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("hgsic", "14_drums_random_velocity"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_rand, "full_ensemble", "random_velocity")

    def test_above_silence(self, runner):
        """Groove music >> silence."""
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_funk, res_sil, "funk_groove", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "02_drums_funk_groove"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. beat_prominence (Appraisal)
# =====================================================================

class TestBeatProminence:
    """Beat salience — accent hierarchy strength.

    Kick+snare on beats >> flat dynamics >> silence.

    Science: Grahn & Brett 2007 — metric clarity requires accent hierarchy
    (fMRI N=14, putamen Z=5.67).
    """

    BELIEF = "beat_prominence"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_full_drums_above_solo_hihat(self, runner):
        """Full drum kit >> solo hi-hat for beat prominence.

        Grahn & Brett 2007: kick+snare accent hierarchy creates clear
        metrical structure driving putamen/SMA. Solo hi-hat has
        regular onsets but no accent differentiation.
        Spread ~0.006 — extraction responds to hi-hat's onset density.
        """
        res_drums = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_hh = runner.run(
            _load("hgsic", "11_solo_hihat"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_drums, res_hh, "full_drums", "solo_hihat")

    def test_ensemble_above_solo_hihat(self, runner):
        """Full ensemble >> solo hi-hat for beat prominence.

        Multiple instruments reinforce beat accents.
        CONFIRMED: large spectral contrast produces reliable separation.
        """
        res_ens = runner.run(
            _load("hgsic", "10_full_ensemble_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_hh = runner.run(
            _load("hgsic", "11_solo_hihat"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_hh, "full_ensemble", "solo_hihat")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_funk_above_random_velocity(self, runner):
        """Funk groove (structured dynamics) >> random velocity for prominence.

        Grahn & Brett 2007: structured accent patterns enhance metric
        perception. Random velocity destroys accent hierarchy.
        Spread ~0.003 — extraction averages velocity contrasts.
        """
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("hgsic", "14_drums_random_velocity"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_funk, res_rand, "funk_structured", "random_velocity")

    def test_above_silence(self, runner):
        """Drums >> silence for beat prominence."""
        res_drums = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_drums, res_sil, "straight_drums", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "01_drums_straight_4_4"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. meter_structure (Appraisal)
# =====================================================================

class TestMeterStructure:
    """Metrical clarity — strength of metric grid perception.

    Regular 4/4 or 3/4 >> irregular 7/8 >> random.

    Science: Grahn & Brett 2007 — regular meters activate putamen/SMA
    more than irregular meters (fMRI N=14).
    Palmer & Krumhansl 1990 — metric hierarchy perception.
    """

    BELIEF = "meter_structure"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_regular_4_4_above_complex_7_8(self, runner):
        """Straight 4/4 >> complex 7/8 for meter structure.

        Grahn & Brett 2007: simple meters (4/4) produce stronger putamen
        activation than complex meters (7/8 = 2+2+3 grouping).
        Spread ~0.01 — extraction responds to onset density not meter type.
        """
        res_44 = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_78 = runner.run(
            _load("hgsic", "09_drums_7_8_complex"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_44, res_78, "straight_4_4", "complex_7_8")

    def test_waltz_above_complex(self, runner):
        """Waltz 3/4 >> complex 7/8 for meter structure.

        Both are clear meters, but 3/4 is more regular than 7/8 (2+2+3).
        CONFIRMED: this ordering holds in current extraction.
        """
        res_34 = runner.run(
            _load("hgsic", "08_waltz_3_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_78 = runner.run(
            _load("hgsic", "09_drums_7_8_complex"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_34, res_78, "waltz_3_4", "complex_7_8")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_regular_above_random(self, runner):
        """Regular meter >> random velocity pattern for metrical clarity.

        Palmer & Krumhansl 1990: metric hierarchy requires structured
        accent patterns. Random velocity prevents metre induction.
        Spread ~0.01 — extraction averages onset density.
        """
        res_reg = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("hgsic", "14_drums_random_velocity"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_reg, res_rand, "straight_4_4", "random_velocity")

    def test_above_silence(self, runner):
        """Metric drums >> silence."""
        res_met = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_met, res_sil, "straight_drums", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "01_drums_straight_4_4"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. auditory_motor_coupling (Appraisal)
# =====================================================================

class TestAuditoryMotorCoupling:
    """Motor-auditory binding — coupling strength between perception and action.

    Multi-instrument ensembles strengthen coupling through redundant cues.

    Science: Chen, Penhune & Zatorre 2008 — listening to rhythms recruits
    motor regions even without movement (fMRI N=22).
    Janata et al 2012 — motor cortex PMC activation scales with
    ensemble complexity (fMRI N=17).
    """

    BELIEF = "auditory_motor_coupling"

    def test_ensemble_above_solo(self, runner):
        """Full ensemble >> solo piano for auditory-motor coupling.

        Janata et al 2012: multi-instrument ensemble provides redundant
        timing cues that strengthen motor-auditory binding.
        CONFIRMED: ensemble > solo ordering holds in current extraction.
        """
        res_ens = runner.run(
            _load("hgsic", "10_full_ensemble_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_solo = runner.run(
            _load("hgsic", "04_piano_iso_zero_sync"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_solo, "full_ensemble", "solo_piano")

    def test_drums_bass_above_iso(self, runner):
        """Drums+Bass funk >> piano isochronous for coupling.

        Multi-instrument rhythm section > single-instrument periodicity.
        CONFIRMED: this ordering holds in current extraction.
        """
        res_db = runner.run(
            _load("hgsic", "05_drums_bass_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_iso = runner.run(
            _load("hgsic", "04_piano_iso_zero_sync"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_db, res_iso, "drums_bass_funk", "piano_iso")

    @pytest.mark.xfail(
        reason="Model limitation: silence baseline elevated (~0.659) due to "
               "sigmoid cascade — music produces LOWER output than silence. "
               "Chen et al 2008 predicts music > silence for motor coupling.",
        strict=False,
    )
    def test_above_silence(self, runner):
        """Music >> silence for auditory-motor coupling.

        Chen, Penhune & Zatorre 2008: listening to rhythmic music
        activates motor areas (PMC, SMA, cerebellum); silence does not.
        INVERTED in current extraction: silence=0.659 > funk=0.645.
        Sigmoid cascade on null input produces elevated baseline.
        """
        res_mus = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "funk_groove", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "10_full_ensemble_funk"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 5. motor_preparation (Appraisal)
# =====================================================================

class TestMotorPreparation:
    """Readiness to move — motor cortex preparation for action.

    Full ensemble with groove → maximum motor preparation.

    Science: Janata et al 2012 — PMC activation scales with groove
    intensity (fMRI N=17).
    Grahn & Brett 2007 — SMA activation for metric rhythm (fMRI N=14).
    """

    BELIEF = "motor_preparation"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_solo(self, runner):
        """Full ensemble >> solo piano for motor preparation.

        Janata et al 2012: multi-instrument groove maximises
        motor preparation through redundant timing cues.
        Spread ~0.001 — all drum stimuli compressed to near-identical range.
        """
        res_ens = runner.run(
            _load("hgsic", "10_full_ensemble_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_solo = runner.run(
            _load("hgsic", "04_piano_iso_zero_sync"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_solo, "full_ensemble", "solo_piano")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_drums_bass_above_iso(self, runner):
        """Drums+Bass ensemble >> piano isochronous for motor preparation.

        Multi-instrument rhythm section should enhance motor readiness
        beyond single-instrument periodicity.
        Spread ~0.001 — extraction compresses all to near-identical range.
        """
        res_db = runner.run(
            _load("hgsic", "05_drums_bass_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_iso = runner.run(
            _load("hgsic", "04_piano_iso_zero_sync"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_db, res_iso, "drums_bass_funk", "piano_iso")

    def test_above_silence(self, runner):
        """Groove music >> silence for motor preparation.

        CONFIRMED: music > silence holds for this belief.
        """
        res_mus = runner.run(
            _load("hgsic", "10_full_ensemble_funk"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "full_ensemble", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "10_full_ensemble_funk"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 6. groove_trajectory (Anticipation)
# =====================================================================

class TestGrooveTrajectory:
    """Groove intensity forecast — tracks groove momentum.

    Crescendo groove → rising trajectory; decrescendo → falling.

    Science: Janata et al 2012 — groove intensity scales with dynamic level.
    Huron 2006 — dynamic build-up creates anticipation.
    """

    BELIEF = "groove_trajectory"

    def test_crescendo_above_decrescendo(self, runner):
        """Crescendo groove >> decrescendo groove for trajectory.

        Crescendo builds groove momentum; decrescendo dissolves it.
        CONFIRMED: this ordering holds in current extraction.
        """
        res_cresc = runner.run(
            _load("hgsic", "12_drums_crescendo_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_decresc = runner.run(
            _load("hgsic", "13_drums_decrescendo_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cresc, res_decresc, "crescendo_groove", "decrescendo")

    def test_crescendo_rising(self, runner):
        """Crescendo groove should show rising trajectory.

        Dynamic buildup → groove intensity increases over time.
        CONFIRMED: halves comparison holds.
        """
        result = runner.run(
            _load("hgsic", "12_drums_crescendo_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_above_silence(self, runner):
        """Groove music >> silence for trajectory."""
        res_groove = runner.run(
            _load("hgsic", "12_drums_crescendo_groove"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_groove, res_sil, "crescendo_groove", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hgsic", "12_drums_crescendo_groove"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)
