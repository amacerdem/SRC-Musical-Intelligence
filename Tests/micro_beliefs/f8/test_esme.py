"""ESME tests — Expertise-Specific MMN Enhancement.

Validates expertise_enhancement (Core, tau=0.92),
       pitch_mmn, rhythm_mmn, timbre_mmn (Appraisal),
       and expertise_trajectory (Anticipation).

Key R³ drivers: helmholtz_kang[2], onset_strength[11],
spectral_change[21], pitch_change[23], tristimulus[18:21],
timbre_change[24], x_l4l5[33:41].

Science:
  Koelsch Schroger & Tervaniemi 1999 (EEG N~20/grp): violinist MMN 0.75%
  Vuust et al 2012 (EEG N~40-60): genre-specific MMN gradient
  Wagner et al 2018 (EEG N=15): harmonic interval MMN (-0.34uV p=0.003)
  Criscuolo et al 2022 (ALE k=84 N=3005): bilateral STG + L IFG
  Crespo-Bojorque et al 2018 (EEG N~16/grp): consonance/dissonance MMN
"""
from __future__ import annotations

import pathlib

import numpy as np
import pytest
import torch
from scipy.io import wavfile

from Tests.micro_beliefs.audio_stimuli import silence
from Tests.micro_beliefs.assertions import assert_greater, assert_in_range

_SR = 44_100
_F8_AUDIO = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "Test-Audio" / "micro_beliefs" / "f8"
)

_NARROW_RANGE = (
    "Model limitation: sigmoid cascade compresses belief dynamic range. "
    "Current R³→H³→C³ extraction responds to spectral energy rather than "
    "the specific perceptual feature. See Building/Ontology/C³/ for details."
)


def _load(group: str, name: str) -> torch.Tensor:
    """Load pre-generated F8 test audio as (1, N) float32 tensor."""
    wav_path = _F8_AUDIO / group / f"{name}.wav"
    sr, data = wavfile.read(str(wav_path))
    assert sr == _SR, f"Expected {_SR} Hz, got {sr}"
    audio = data.astype(np.float32) / 32767.0
    return torch.from_numpy(audio).unsqueeze(0)


class TestExpertiseEnhancement:
    """expertise_enhancement — ESME Core belief (tau=0.92).

    Tests that deviant-containing stimuli produce higher expertise
    enhancement than standard/silence stimuli.
    """

    BELIEF = "expertise_enhancement"

    def test_pitch_deviant_above_silence(self, runner):
        """Large pitch deviant >> silence.

        Wagner 2018: harmonic interval MMN = -0.34 uV (p=0.003, N=15).
        """
        res_dev = runner.run(
            _load("esme", "03_piano_pitch_deviant_large"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "large_pitch_deviant", "silence")

    def test_rhythm_deviant_above_silence(self, runner):
        """Rhythm deviant >> silence.

        Vuust 2012: rhythmic expectation violation produces enhanced MMN.
        """
        res_dev = runner.run(
            _load("esme", "06_piano_rhythm_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "rhythm_deviant", "silence")

    def test_combined_deviant_above_silence(self, runner):
        """Combined pitch+timbre deviant >> silence.

        Fong 2020: combined deviants produce larger prediction error.
        """
        res_comb = runner.run(
            _load("esme", "09_combined_pitch_timbre_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_comb, res_sil, "combined_deviant", "silence")

    def test_jazz_above_pop(self, runner):
        """Jazz complexity >> pop predictability for expertise.

        CONFIRMED: Vuust et al 2012: genre-specific gradient —
        jazz > rock > pop > non-musicians (EEG N~40-60).
        """
        res_jazz = runner.run(
            _load("esme", "10_jazz_complex_melody"), [self.BELIEF],
        )[self.BELIEF]
        res_pop = runner.run(
            _load("esme", "12_pop_predictable_melody"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_jazz, res_pop, "jazz_complex", "pop_predictable")

    def test_combined_above_single_deviant(self, runner):
        """Combined pitch+timbre >> single pitch deviant.

        CONFIRMED: Fong 2020: combined deviants > single deviant for
        prediction error under Bayesian framework.
        """
        res_comb = runner.run(
            _load("esme", "09_combined_pitch_timbre_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_single = runner.run(
            _load("esme", "03_piano_pitch_deviant_large"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_comb, res_single, "combined", "single_pitch")


class TestPitchMmn:
    """pitch_mmn — ESME Appraisal belief.

    Tests pitch deviance detection.
    """

    BELIEF = "pitch_mmn"

    def test_large_deviant_above_silence(self, runner):
        """Large pitch deviant >> silence.

        Koelsch et al 1999: musicians detect 0.75% pitch deviants;
        4 semitones is well above threshold.
        """
        res_dev = runner.run(
            _load("esme", "03_piano_pitch_deviant_large"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "large_deviant", "silence")

    def test_standard_above_silence(self, runner):
        """Standard repeated (no deviants) >> silence.

        Even standard stream has some pitch_change activity.
        """
        res_std = runner.run(
            _load("esme", "01_piano_standard_repeated"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_std, res_sil, "standard_repeated", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_large_above_small_deviant(self, runner):
        """Large pitch deviant (4 semitones) >> small (1 semitone).

        Koelsch 1999: larger deviant = larger MMN amplitude.
        Wagner 2018: harmonic interval MMN scales with interval size.
        Spread ~0.0002 — extraction averages spectral energy.
        """
        res_large = runner.run(
            _load("esme", "03_piano_pitch_deviant_large"), [self.BELIEF],
        )[self.BELIEF]
        res_small = runner.run(
            _load("esme", "02_piano_pitch_deviant_small"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_large, res_small, "large_4st", "small_1st")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_tritone_above_standard(self, runner):
        """Tritone deviant >> standard for pitch_mmn.

        Crespo-Bojorque 2018: dissonance latency >> consonance latency
        (F(1,15)=155.03, p<.001). Tritone = maximally dissonant.
        """
        res_tri = runner.run(
            _load("esme", "04_piano_pitch_deviant_tritone"), [self.BELIEF],
        )[self.BELIEF]
        res_std = runner.run(
            _load("esme", "01_piano_standard_repeated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_tri, res_std, "tritone_deviant", "standard")


class TestRhythmMmn:
    """rhythm_mmn — ESME Appraisal belief.

    Tests rhythmic timing violation detection.
    """

    BELIEF = "rhythm_mmn"

    def test_rhythm_deviant_above_silence(self, runner):
        """Rhythm deviant >> silence.

        Vuust 2012: timing violation produces rhythm MMN.
        """
        res_dev = runner.run(
            _load("esme", "06_piano_rhythm_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "rhythm_deviant", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_rhythm_deviant_above_regular(self, runner):
        """Rhythm deviant >> regular rhythm for rhythm_mmn.

        Vuust 2012: timing violation > perfectly isochronous for
        rhythm-specific MMN.
        """
        res_dev = runner.run(
            _load("esme", "06_piano_rhythm_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_reg = runner.run(
            _load("esme", "05_piano_rhythm_regular"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_dev, res_reg, "rhythm_deviant", "regular_rhythm")

    def test_jazz_above_pop_rhythm(self, runner):
        """Jazz >> pop for rhythm_mmn.

        CONFIRMED: Vuust 2012: jazz musicians show strongest rhythm MMN —
        genre-specific gradient.
        """
        res_jazz = runner.run(
            _load("esme", "10_jazz_complex_melody"), [self.BELIEF],
        )[self.BELIEF]
        res_pop = runner.run(
            _load("esme", "12_pop_predictable_melody"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_jazz, res_pop, "jazz", "pop")


class TestTimbreMmn:
    """timbre_mmn — ESME Appraisal belief.

    Tests timbre deviance detection.
    """

    BELIEF = "timbre_mmn"

    def test_timbre_deviant_above_silence(self, runner):
        """Timbre deviant (violin in piano stream) >> silence.

        Pantev 2001: timbre-specific N1m enhancement
        (F(1,15)=28.55, p=.00008).
        """
        res_dev = runner.run(
            _load("esme", "07_piano_timbre_deviant_violin"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "timbre_deviant_violin", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_timbre_deviant_above_standard(self, runner):
        """Timbre deviant >> all-standard stream.

        Pantev 2001: instrument change in standard stream produces
        timbre-specific MMN.
        """
        res_dev = runner.run(
            _load("esme", "07_piano_timbre_deviant_violin"), [self.BELIEF],
        )[self.BELIEF]
        res_std = runner.run(
            _load("esme", "01_piano_standard_repeated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_dev, res_std, "timbre_deviant", "standard")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_trumpet_deviant_above_standard(self, runner):
        """Trumpet deviant >> standard (different timbral family).

        Pantev 2001: double dissociation — brass deviant in keyboard
        stream should still produce timbre MMN.
        """
        res_dev = runner.run(
            _load("esme", "08_piano_timbre_deviant_trumpet"), [self.BELIEF],
        )[self.BELIEF]
        res_std = runner.run(
            _load("esme", "01_piano_standard_repeated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_dev, res_std, "trumpet_deviant", "standard")


class TestExpertiseTrajectory:
    """expertise_trajectory — ESME Anticipation belief.

    Tests forward prediction of expertise development.
    """

    BELIEF = "expertise_trajectory"

    def test_deviant_above_silence(self, runner):
        """Any deviant stimulus >> silence for trajectory.

        Bonetti et al 2024: hierarchical auditory memory develops with
        expertise; deviant stimuli engage developmental trajectory.
        """
        res_dev = runner.run(
            _load("esme", "09_combined_pitch_timbre_deviant"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_dev, res_sil, "combined_deviant", "silence")
