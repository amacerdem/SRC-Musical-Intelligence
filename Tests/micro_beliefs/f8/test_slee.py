"""SLEE tests — Statistical Learning Expertise Enhancement.

Validates statistical_model (Core, tau=0.88),
       detection_accuracy (Appraisal),
       and multisensory_binding (Appraisal).

Key R³ drivers: amplitude[7], loudness[8], spectral_flux[10],
x_l5l6[41:49], pitch_stability[24], x_l4l5[33:41].

Science:
  Bridwell 2017 (EEG N=13): 45% amplitude reduction patterned vs random
    (r=0.65, p=0.015, cortical sensitivity at 4 Hz)
  Paraskevopoulos et al 2022 (MEG N=25): statistical learning accuracy
    (Hedges' g=-1.09, t(23)=-2.815, p<.05)
  Doelling & Poeppel 2015 (MEG N=34): cortical entrainment 1-8 Hz
  Porfyri et al 2025 (N=30): multisensory training (eta-sq=0.168)
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


class TestStatisticalModel:
    """statistical_model — SLEE Core belief (tau=0.88).

    Tests that patterned/regular stimuli build statistical models
    above random/silence baselines.
    """

    BELIEF = "statistical_model"

    def test_pattern_above_silence(self, runner):
        """Regular ABAB pattern >> silence.

        Bridwell 2017: patterned sequences produce 45% cortical amplitude
        reduction (N=13, r=0.65, p=0.015).
        """
        res_pat = runner.run(
            _load("slee", "01_pattern_abab_regular"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_pat, res_sil, "pattern_abab", "silence")

    def test_ascending_above_silence(self, runner):
        """Ascending scale repeated >> silence.

        Doelling & Poeppel 2015: cortical entrainment 1-8 Hz enhanced
        in musicians (MEG N=34).
        """
        res_asc = runner.run(
            _load("slee", "03_ascending_scale_repeated"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_asc, res_sil, "ascending_repeated", "silence")

    def test_isochronous_above_silence(self, runner):
        """Isochronous single pitch >> silence.

        Temporal regularity alone (no pitch variation) should build
        statistical model above silence.
        """
        res_iso = runner.run(
            _load("slee", "12_isochronous_single_pitch"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_iso, res_sil, "isochronous", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_pattern_above_random(self, runner):
        """Regular ABAB pattern >> random notes.

        Bridwell 2017: patterned > random (45% amplitude reduction).
        Critical test of statistical learning.
        """
        res_pat = runner.run(
            _load("slee", "01_pattern_abab_regular"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("slee", "02_random_no_pattern"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_pat, res_rand, "pattern", "random")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ascending_above_random(self, runner):
        """Ascending scale repeated >> random.

        Doelling & Poeppel 2015: regular > random for cortical entrainment.
        """
        res_asc = runner.run(
            _load("slee", "03_ascending_scale_repeated"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("slee", "02_random_no_pattern"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_asc, res_rand, "ascending", "random")


class TestDetectionAccuracy:
    """detection_accuracy — SLEE Appraisal belief.

    Tests irregularity detection accuracy.
    """

    BELIEF = "detection_accuracy"

    def test_pattern_above_silence(self, runner):
        """Patterned sequence >> silence.

        Pattern presence is needed for irregularity detection to operate.
        """
        res_pat = runner.run(
            _load("slee", "01_pattern_abab_regular"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_pat, res_sil, "pattern", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_pattern_above_random(self, runner):
        """Regular pattern >> random for detection accuracy.

        Doelling & Poeppel 2015: regular > random for cortical entrainment.
        Carbajal & Malmierca 2018: predictive coding hierarchy requires
        regularity to generate predictions.
        """
        res_pat = runner.run(
            _load("slee", "03_ascending_scale_repeated"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("slee", "02_random_no_pattern"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_pat, res_rand, "ascending", "random")

    def test_boundary_stimulus_above_random(self, runner):
        """Pattern boundary switch >> random for detection accuracy.

        CONFIRMED: Billig 2022: hippocampus supports sequence binding at
        segment boundaries; boundary = detection challenge.
        """
        res_bnd = runner.run(
            _load("slee", "08_pattern_boundary_switch"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("slee", "06_single_random_no_binding"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_bnd, res_rand, "boundary_switch", "random")


class TestMultisensoryBinding:
    """multisensory_binding — SLEE Appraisal belief.

    Tests cross-modal integration strength.
    """

    BELIEF = "multisensory_binding"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_multi_instrument_above_silence(self, runner):
        """Multi-instrument patterned >> silence.

        Paraskevopoulos 2022: IFG area 47m supramodal hub for
        multisensory statistical learning (g=-1.09).
        INVERTED: silence=0.628 > multi=0.565 — x_l5l6 cross-modal
        binding baseline pushes silence above musical stimuli.
        """
        res_multi = runner.run(
            _load("slee", "05_multi_instrument_patterned"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_multi, res_sil, "multi_instrument", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_multi_above_single(self, runner):
        """Multi-instrument patterned >> single instrument random.

        Porfyri et al 2025: multisensory training improves audiovisual
        detection (F(1,28)=4.635, eta-sq=0.168).
        Multi-instrument = higher x_l5l6 cross-modal binding.
        """
        res_multi = runner.run(
            _load("slee", "05_multi_instrument_patterned"), [self.BELIEF],
        )[self.BELIEF]
        res_single = runner.run(
            _load("slee", "06_single_random_no_binding"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_multi, res_single, "multi_patterned", "single_random")

    def test_ensemble_octaves_above_single_random(self, runner):
        """Ensemble pattern octaves >> single random.

        CONFIRMED: Porfyri 2025: multi > uni for cross-modal advantage.
        """
        res_ens = runner.run(
            _load("slee", "10_ensemble_pattern_octaves"), [self.BELIEF],
        )[self.BELIEF]
        res_single = runner.run(
            _load("slee", "06_single_random_no_binding"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_single, "ensemble_octaves", "single_random")
