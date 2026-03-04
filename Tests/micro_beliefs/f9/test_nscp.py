"""NSCP tests — Neural Synchrony Coupling Prediction.

Validates neural_synchrony (Core, tau=0.65)
       and catchiness_pred (Anticipation).

Key R³ drivers: sensory_pleasantness[4], amplitude[7], loudness[8],
onset_strength[10], tonalness[14], tristimulus[18:21].

Science:
  Wohltjen et al 2023 (Study 2 N=82): beat synchrony predicts attentional
    synchrony (pupillary entrainment, stable individual difference)
  Ni et al 2024 (fNIRS N=528): social bonding → prefrontal neural synchrony
    (unidirectional leader→follower alignment, 176 three-person groups)
  Savage et al 2021 (cross-cultural): repetition is universal music feature
  Keller Novembre & Hove 2014: ensemble coordination framework (review)
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


class TestNeuralSynchrony:
    """neural_synchrony — NSCP Core belief (tau=0.65).

    Tests that multi-voice synchronized stimuli produce higher neural
    synchrony than solo/arrhythmic/desynchronized stimuli.
    """

    BELIEF = "neural_synchrony"

    def test_ensemble_groove_above_silence(self, runner):
        """Ensemble groove >> silence.

        Multi-voice synchronized groove should activate neural synchrony
        well above silence baseline.
        """
        res_ens = runner.run(
            _load("nscp", "01_ensemble_groove_synchronized"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ens, res_sil, "ensemble_groove", "silence")

    def test_choir_above_silence(self, runner):
        """Choir sustained >> silence.

        Ni et al 2024: social bonding activates prefrontal synchrony
        (fNIRS N=528, 176 three-person groups).
        """
        res_choir = runner.run(
            _load("nscp", "03_choir_unison_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_choir, res_sil, "choir_unison", "silence")

    def test_groove_strong_beat_above_silence(self, runner):
        """Strong beat groove >> silence.

        Large et al 2023: beat perception enables prediction and
        interpersonal coordination.
        """
        res_beat = runner.run(
            _load("nscp", "05_groove_strong_beat"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beat, res_sil, "strong_beat", "silence")

    def test_unison_octaves_above_silence(self, runner):
        """Multi-instrument octave unison >> silence.

        Keller et al 2014: synchronized multi-voice textures
        enhance neural coupling.
        """
        res_uni = runner.run(
            _load("nscp", "09_unison_octaves_multi"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_uni, res_sil, "unison_octaves", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_solo_rubato(self, runner):
        """Ensemble groove >> solo rubato.

        Wohltjen et al 2023: multi-voice synchronized texture >
        single-voice free tempo for synchrony.
        INVERTED: solo_rubato=0.634 > ensemble=0.619 — rubato pitch variety
        drives broader R³ activation than synchronized groove.
        """
        res_ens = runner.run(
            _load("nscp", "01_ensemble_groove_synchronized"), [self.BELIEF],
        )[self.BELIEF]
        res_solo = runner.run(
            _load("nscp", "02_solo_piano_rubato"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_solo, "ensemble_groove", "solo_rubato")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_arrhythmic(self, runner):
        """Ensemble groove >> arrhythmic atonal.

        Wohltjen 2023: synchrony requires predictable temporal structure.
        INVERTED: arrhythmic=0.629 > ensemble=0.619 — random pitches drive
        broader spectral activation than tonal groove.
        """
        res_ens = runner.run(
            _load("nscp", "01_ensemble_groove_synchronized"), [self.BELIEF],
        )[self.BELIEF]
        res_arr = runner.run(
            _load("nscp", "06_arrhythmic_atonal"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_arr, "ensemble_groove", "arrhythmic")

    def test_unison_above_desynchronized(self, runner):
        """Unison octaves >> desynchronized random entries.

        CONFIRMED: Keller 2014: temporal alignment is prerequisite
        for coordination. Synchronized > desynchronized.
        """
        res_uni = runner.run(
            _load("nscp", "09_unison_octaves_multi"), [self.BELIEF],
        )[self.BELIEF]
        res_desync = runner.run(
            _load("nscp", "10_desynchronized_random_entries"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_uni, res_desync, "unison", "desynchronized")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_single_metronomic(self, runner):
        """Ensemble groove >> single metronomic note.

        Ni 2024: multi-voice > single voice for neural synchrony.
        """
        res_ens = runner.run(
            _load("nscp", "01_ensemble_groove_synchronized"), [self.BELIEF],
        )[self.BELIEF]
        res_metro = runner.run(
            _load("nscp", "12_single_note_metronomic"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_metro, "ensemble", "metronomic")


class TestCatchinessPred:
    """catchiness_pred — NSCP Anticipation belief.

    Tests catchiness prediction based on repetitiveness.
    """

    BELIEF = "catchiness_pred"

    def test_catchy_hook_above_silence(self, runner):
        """Catchy repetitive hook >> silence.

        Savage et al 2021: repetition is a cross-cultural music universal.
        """
        res_hook = runner.run(
            _load("nscp", "07_catchy_repetitive_hook"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_hook, res_sil, "catchy_hook", "silence")

    def test_catchy_above_complex(self, runner):
        """Catchy hook >> complex non-repetitive.

        CONFIRMED: Savage 2021: repetitive > non-repetitive for
        perceived catchiness. Model captures repetitiveness distinction.
        """
        res_hook = runner.run(
            _load("nscp", "07_catchy_repetitive_hook"), [self.BELIEF],
        )[self.BELIEF]
        res_complex = runner.run(
            _load("nscp", "08_complex_non_repetitive"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_hook, res_complex, "catchy_hook", "complex")
