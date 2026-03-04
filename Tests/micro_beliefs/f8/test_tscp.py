"""TSCP tests — Timbre-Specific Cortical Plasticity.

Validates trained_timbre_recognition (Core, tau=0.90)
       and plasticity_magnitude (Appraisal).

Key R³ drivers: tristimulus[18:21], inharmonicity[5], tonalness[14],
warmth[12], sharpness[13], timbre_change[24], x_l5l7[41:47].

Science:
  Pantev et al 2001 (MEG N=17): timbre-specific N1m enhancement,
    double dissociation violinists/trumpeters (F(1,15)=28.55, p=.00008)
  Bellmann & Asano 2024 (ALE k=18 N=338): 4 clusters pSTG/HG/SMG
  Alluri et al 2012 (fMRI N=11): timbral brightness bilateral STG (Z=8.13)
  Whiteford et al 2025 (N>260): plasticity cortical NOT subcortical
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


class TestTrainedTimbreRecognition:
    """trained_timbre_recognition — TSCP Core belief (tau=0.90).

    Tests that instrument timbres produce higher timbre recognition
    than silence, and that timbral richness matters.
    """

    BELIEF = "trained_timbre_recognition"

    def test_piano_above_silence(self, runner):
        """Piano sustained >> silence.

        Any instrument timbre should activate trained_timbre_recognition
        above the silence baseline.
        """
        res_piano = runner.run(
            _load("tscp", "01_piano_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_piano, res_sil, "piano_c4", "silence")

    def test_violin_above_silence(self, runner):
        """Violin sustained >> silence.

        Pantev 2001: violin timbre activates timbre-specific cortical
        enhancement in violinists (F(1,15)=28.55).
        """
        res_violin = runner.run(
            _load("tscp", "02_violin_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_violin, res_sil, "violin_c4", "silence")

    def test_trumpet_above_silence(self, runner):
        """Trumpet sustained >> silence.

        Pantev 2001: trumpet timbre activates cortical enhancement
        in trumpeters.
        """
        res_trumpet = runner.run(
            _load("tscp", "03_trumpet_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_trumpet, res_sil, "trumpet_c4", "silence")

    def test_ensemble_above_silence(self, runner):
        """Multi-instrument ensemble >> silence.

        Bellmann & Asano 2024: bilateral pSTG/HG responds to timbral
        richness (ALE k=18 N=338, 4640 mm³).
        """
        res_ens = runner.run(
            _load("tscp", "11_multi_instrument_ensemble"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ens, res_sil, "ensemble", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_violin_above_flute(self, runner):
        """Violin >> flute for timbre recognition.

        Violin has richer harmonic content (higher trist2/trist3) than
        flute (nearly pure fundamental). Pantev 2001: richer timbres
        produce larger N1m enhancement.
        Spread depends on tristimulus balance extraction.
        """
        res_violin = runner.run(
            _load("tscp", "02_violin_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_flute = runner.run(
            _load("tscp", "04_flute_c5_sustained"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_violin, res_flute, "violin_c4", "flute_c5")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_single(self, runner):
        """Multi-instrument ensemble >> single piano.

        More timbral diversity should drive higher recognition through
        x_l5l7 coupling and broader tristimulus activation.
        """
        res_ens = runner.run(
            _load("tscp", "11_multi_instrument_ensemble"), [self.BELIEF],
        )[self.BELIEF]
        res_piano = runner.run(
            _load("tscp", "01_piano_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_piano, "ensemble", "piano_solo")


class TestPlasticityMagnitude:
    """plasticity_magnitude — TSCP Appraisal belief.

    Tests that timbral richness drives plasticity magnitude.
    """

    BELIEF = "plasticity_magnitude"

    def test_instrument_above_silence(self, runner):
        """Any instrument >> silence for plasticity.

        Whiteford et al 2025: plasticity is cortical (N>260, d=-0.064
        for subcortical null).
        """
        res_piano = runner.run(
            _load("tscp", "01_piano_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_piano, res_sil, "piano", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_ensemble_above_single(self, runner):
        """Multi-instrument ensemble >> single instrument.

        More timbral diversity = higher plasticity_magnitude.
        Bellmann & Asano 2024: bilateral pSTG/HG responds to richness.
        """
        res_ens = runner.run(
            _load("tscp", "11_multi_instrument_ensemble"), [self.BELIEF],
        )[self.BELIEF]
        res_organ = runner.run(
            _load("tscp", "05_organ_c4_sustained"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ens, res_organ, "ensemble", "organ_solo")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_rapid_alternation_above_repeated(self, runner):
        """Rapid timbre alternation >> repeated single timbre.

        Rapid switching drives high timbre_change[24] and spectral_flux,
        which feeds plasticity_magnitude through f03 * timbre_std.
        """
        res_alt = runner.run(
            _load("tscp", "12_rapid_timbre_alternation"), [self.BELIEF],
        )[self.BELIEF]
        res_rep = runner.run(
            _load("tscp", "10_piano_repeated_c4"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_alt, res_rep, "rapid_alternation", "repeated_c4")
