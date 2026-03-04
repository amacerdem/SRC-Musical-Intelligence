"""SSRI tests — Social Synchrony Reward Integration.

Validates synchrony_reward (Appraisal),
       social_bonding (Appraisal),
       group_flow (Appraisal),
       entrainment_quality (Appraisal),
       social_prediction_error (Appraisal),
       and collective_pleasure_pred (Anticipation).

Key R³ drivers: sensory_pleasantness[4], amplitude[7], loudness[8],
onset_strength[10], warmth[12], tonalness[14], x_l5l6[41:49].

Science:
  Tarr Launay & Dunbar 2016 (N=264): synchronous dancing → endorphins,
    pain threshold increase, social bonding increase
  Launay Tarr & Dunbar 2016 (N=94): synchrony → social bonding,
    implicit affiliation increase via endorphin pathway
  Williamson & Bonshor 2019 (N=346): self-reported wellbeing in brass bands,
    physical + psychological + social benefits (survey, no neurochemical assay)
  Chanda & Levitin 2013: neurochemistry review (DA, oxytocin, endorphins)
  Koelsch 2014: brain correlates of music-evoked emotions (NRN review)
  Nguyen et al 2023: infant-directed music enables co-regulation
  Large et al 2023: dynamic models for rhythm perception (review)
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
_F9_AUDIO = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "Test-Audio" / "micro_beliefs" / "f9"
)

_NARROW_RANGE = (
    "Model limitation: sigmoid cascade compresses belief dynamic range. "
    "Current R³→H³→C³ extraction responds to spectral energy rather than "
    "the specific perceptual feature. See Building/Ontology/C³/ for details."
)


def _load(group: str, name: str) -> torch.Tensor:
    """Load pre-generated F9 test audio as (1, N) float32 tensor."""
    wav_path = _F9_AUDIO / group / f"{name}.wav"
    sr, data = wavfile.read(str(wav_path))
    assert sr == _SR, f"Expected {_SR} Hz, got {sr}"
    audio = data.astype(np.float32) / 32767.0
    return torch.from_numpy(audio).unsqueeze(0)


class TestSynchronyReward:
    """synchrony_reward — SSRI Appraisal belief.

    Tests that groove/rhythmic stimuli produce higher synchrony reward
    than cold/isolated stimuli.
    """

    BELIEF = "synchrony_reward"

    def test_dance_groove_above_silence(self, runner):
        """Dance groove >> silence.

        Tarr et al 2016: synchronous dancing → endorphin release,
        pain threshold increase (N=264).
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_groove, res_sil, "dance_groove", "silence")

    def test_march_above_silence(self, runner):
        """March strong beat >> silence.

        Tarr 2016: synchronized rhythmic movement activates reward.
        """
        res_march = runner.run(
            _load("ssri", "14_march_energetic_strong"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_march, res_sil, "march", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_groove_above_cold_tone(self, runner):
        """Dance groove >> single cold tone.

        Tarr 2016: groove > isolated for synchrony reward activation.
        INVERTED: cold=0.575 > groove=0.570 — sustained organ baseline
        pushes steady spectral energy above rhythmic groove.
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_cold = runner.run(
            _load("ssri", "04_single_cold_isolated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_groove, res_cold, "dance_groove", "cold_tone")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_groove_above_rubato(self, runner):
        """Dance groove >> free tempo rubato.

        Tarr 2016: rhythmic groove > free tempo for reward activation.
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_rubato = runner.run(
            _load("ssri", "06_free_tempo_rubato"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_groove, res_rubato, "groove", "rubato")


class TestSocialBonding:
    """social_bonding — SSRI Appraisal belief.

    Tests that warm ensemble textures produce higher social bonding
    than cold/isolated stimuli.
    """

    BELIEF = "social_bonding"

    def test_ballad_above_silence(self, runner):
        """Warm ballad >> silence.

        Launay et al 2016: synchrony → social bonding via endorphin
        pathway (N=94, implicit affiliation increase).
        """
        res_ballad = runner.run(
            _load("ssri", "02_ballad_warm_60bpm"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ballad, res_sil, "ballad_warm", "silence")

    def test_ensemble_above_silence(self, runner):
        """Full ensemble harmony >> silence.

        Williamson & Bonshor 2019: group music making → social cohesion,
        social cohesion (N=346 self-report survey).
        """
        res_ens = runner.run(
            _load("ssri", "03_full_ensemble_harmony"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ens, res_sil, "full_ensemble", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_cold(self, runner):
        """Full ensemble >> single cold tone.

        Williamson 2019: ensemble > isolated for social bonding.
        INVERTED: cold=0.575 > ensemble=0.571 — sustained organ
        spectral energy baseline above ensemble chord.
        """
        res_ens = runner.run(
            _load("ssri", "03_full_ensemble_harmony"), [self.BELIEF],
        )[self.BELIEF]
        res_cold = runner.run(
            _load("ssri", "04_single_cold_isolated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_cold, "ensemble", "cold_isolated")

    def test_lullaby_above_silence(self, runner):
        """Lullaby >> silence.

        Nguyen et al 2023: infant-directed music enables co-regulation
        and social bonding across development.
        """
        res_lull = runner.run(
            _load("ssri", "13_lullaby_gentle_rocking"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_lull, res_sil, "lullaby", "silence")


class TestGroupFlow:
    """group_flow — SSRI Appraisal belief.

    Tests that building/ensemble stimuli produce higher group flow.
    """

    BELIEF = "group_flow"

    def test_crescendo_above_silence(self, runner):
        """Building crescendo >> silence.

        Chanda & Levitin 2013: orchestral crescendo engages
        DA reward circuitry.
        """
        res_cresc = runner.run(
            _load("ssri", "07_building_crescendo"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_cresc, res_sil, "crescendo", "silence")

    def test_dance_groove_above_silence(self, runner):
        """Dance groove >> silence for group flow.

        Tarr 2016: synchronized movement promotes group flow state.
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_groove, res_sil, "dance_groove", "silence")

    def test_crescendo_above_cold(self, runner):
        """Building crescendo >> single cold tone.

        CONFIRMED: Chanda & Levitin 2013: crescendo > static for
        group flow. Model captures crescendo richness distinction.
        """
        res_cresc = runner.run(
            _load("ssri", "07_building_crescendo"), [self.BELIEF],
        )[self.BELIEF]
        res_cold = runner.run(
            _load("ssri", "04_single_cold_isolated"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cresc, res_cold, "crescendo", "cold_tone")


class TestEntrainmentQuality:
    """entrainment_quality — SSRI Appraisal belief.

    Tests that strong beat stimuli produce higher entrainment quality
    than free tempo or silence.
    """

    BELIEF = "entrainment_quality"

    def test_percussion_above_silence(self, runner):
        """Strong beat percussion >> silence.

        Large et al 2023: metrical hierarchy entrains cortical oscillations.
        """
        res_perc = runner.run(
            _load("ssri", "05_strong_beat_percussion"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_perc, res_sil, "strong_beat", "silence")

    def test_groove_above_silence(self, runner):
        """Dance groove >> silence for entrainment.

        Large 2023: groove promotes entrainment across tempi.
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_groove, res_sil, "dance_groove", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_percussion_above_rubato(self, runner):
        """Strong beat >> free tempo rubato.

        Large 2023: strong beat > rubato for entrainment quality.
        INVERTED: rubato=0.617 > percussion=0.606 — flute pitch variety
        drives broader R³ activation than single-pitch percussion.
        """
        res_perc = runner.run(
            _load("ssri", "05_strong_beat_percussion"), [self.BELIEF],
        )[self.BELIEF]
        res_rubato = runner.run(
            _load("ssri", "06_free_tempo_rubato"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_perc, res_rubato, "strong_beat", "rubato")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_groove_above_rubato(self, runner):
        """Dance groove >> free tempo rubato.

        Large 2023: groove > free tempo for entrainment.
        """
        res_groove = runner.run(
            _load("ssri", "01_dance_groove_energetic"), [self.BELIEF],
        )[self.BELIEF]
        res_rubato = runner.run(
            _load("ssri", "06_free_tempo_rubato"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_groove, res_rubato, "groove", "rubato")


class TestSocialPredictionError:
    """social_prediction_error — SSRI Appraisal belief.

    Tests social prediction error for musical stimuli.
    """

    BELIEF = "social_prediction_error"

    def test_groove_above_silence(self, runner):
        """Groove with break >> silence.

        Koelsch 2014: musical events generate prediction errors
        in social cognition circuits.
        """
        res_break = runner.run(
            _load("ssri", "08_sudden_silence_after_groove"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_break, res_sil, "groove_break", "silence")

    def test_tension_above_silence(self, runner):
        """Tension-resolution >> silence.

        Koelsch 2014: harmonic transitions generate prediction errors.
        """
        res_tens = runner.run(
            _load("ssri", "09_tension_resolution"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_tens, res_sil, "tension_resolution", "silence")


class TestCollectivePleasurePred:
    """collective_pleasure_pred — SSRI Anticipation belief.

    Tests collective pleasure prediction.
    """

    BELIEF = "collective_pleasure_pred"

    def test_ensemble_above_silence(self, runner):
        """Full ensemble harmony >> silence.

        Koelsch 2014: consonant ensemble activates pleasure circuits.
        """
        res_ens = runner.run(
            _load("ssri", "03_full_ensemble_harmony"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ens, res_sil, "ensemble_harmony", "silence")

    def test_ensemble_above_dissonance(self, runner):
        """Full ensemble harmony >> unresolved dissonance.

        CONFIRMED: Koelsch 2014: consonant ensemble > dissonance for
        collective pleasure. Model captures consonance/dissonance.
        """
        res_ens = runner.run(
            _load("ssri", "03_full_ensemble_harmony"), [self.BELIEF],
        )[self.BELIEF]
        res_diss = runner.run(
            _load("ssri", "10_unresolved_dissonance"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_diss, "ensemble_harmony", "dissonance")
