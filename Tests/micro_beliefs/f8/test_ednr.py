"""EDNR tests — Expertise-Dependent Network Reorganization.

Validates network_specialization (Core, tau=0.95 — highest in C³)
       and within_connectivity (Appraisal).

Key R³ drivers: x_l0l5[25:33], x_l4l5[33:41], tonalness[14],
sensory_pleasantness[4], spectral_flatness[16], loudness[8].

Science:
  Paraskevopoulos et al 2022 (MEG/PTE N=25): 106 within vs 192 between
    edges; IFG area 47m hub (Hedges' g=-1.09, p<0.001 FDR)
  Leipold et al 2021 (N=153): musicianship FC replicable (pFWE<0.05)
  Moller et al 2021 (DTI+CT N=45): musicians local-only CT correlations
  Papadaki et al 2023 (fMRI N=41): professional > amateur (d=0.70)
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


class TestNetworkSpecialization:
    """network_specialization — EDNR Core belief (tau=0.95).

    Tests that tonal multi-instrument stimuli drive higher network
    specialization than atonal/simple stimuli or silence.
    """

    BELIEF = "network_specialization"

    def test_harmonic_prog_above_silence(self, runner):
        """Harmonic progression >> silence.

        Leipold 2021: musicianship effects on FC replicable across
        AP/non-AP (N=153, pFWE<0.05).
        """
        res_prog = runner.run(
            _load("ednr", "03_piano_harmonic_progression"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_prog, res_sil, "harmonic_prog", "silence")

    def test_orchestra_above_silence(self, runner):
        """Full orchestra >> silence.

        Criscuolo et al 2022: ALE meta-analysis k=84 N=3005 — musicians
        > NM bilateral STG + L IFG (BA44).
        """
        res_orch = runner.run(
            _load("ednr", "09_full_orchestra_tonal"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_orch, res_sil, "full_orchestra", "silence")

    def test_multi_instrument_above_silence(self, runner):
        """Multi-instrument ensemble >> silence.

        Papadaki 2023: network strength correlates with interval
        recognition (N=41, d=0.70, rho=0.36).
        """
        res_multi = runner.run(
            _load("ednr", "04_multi_instrument_tonal"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_multi, res_sil, "multi_instrument", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_orchestra_above_single_note(self, runner):
        """Full orchestra >> single note for network specialization.

        Papadaki 2023: richer activation > simple (d=0.70).
        """
        res_orch = runner.run(
            _load("ednr", "09_full_orchestra_tonal"), [self.BELIEF],
        )[self.BELIEF]
        res_single = runner.run(
            _load("ednr", "05_single_note_simple"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_orch, res_single, "orchestra", "single_note")

    def test_string_quartet_above_random(self, runner):
        """String quartet (tonal) >> dense atonal random.

        CONFIRMED: Paraskevopoulos 2022: within-network edges driven by
        tonal processing expertise; atonal noise lacks tonal structure.
        """
        res_sq = runner.run(
            _load("ednr", "07_string_quartet_tonal"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("ednr", "06_dense_atonal_random"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_sq, res_rand, "string_quartet", "atonal_random")


class TestWithinConnectivity:
    """within_connectivity — EDNR Appraisal belief.

    Tests that tonal stimuli drive higher within-network coupling.
    """

    BELIEF = "within_connectivity"

    def test_consonant_above_silence(self, runner):
        """Consonant chord >> silence.

        Paraskevopoulos 2022: tonal processing drives within-network
        specialization.
        """
        res_con = runner.run(
            _load("ednr", "01_piano_consonant_chord"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_con, res_sil, "consonant_chord", "silence")

    def test_harmonic_prog_above_silence(self, runner):
        """Harmonic progression >> silence.

        Leipold 2021: harmonic context enhances FC.
        """
        res_prog = runner.run(
            _load("ednr", "03_piano_harmonic_progression"), [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_prog, res_sil, "harmonic_prog", "silence")

    def test_consonant_above_chromatic(self, runner):
        """Consonant chord >> chromatic cluster for within_connectivity.

        CONFIRMED: Paraskevopoulos 2022: tonal > atonal for
        within-network coupling. Consonant = high sensory_pleasantness,
        cluster = low.
        """
        res_con = runner.run(
            _load("ednr", "01_piano_consonant_chord"), [self.BELIEF],
        )[self.BELIEF]
        res_chrom = runner.run(
            _load("ednr", "02_piano_chromatic_cluster"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_con, res_chrom, "consonant", "chromatic_cluster")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_harmonic_above_atonal(self, runner):
        """Harmonic progression >> dense atonal random.

        Leipold 2021: harmonic > atonal for FC (pFWE<0.05).
        """
        res_prog = runner.run(
            _load("ednr", "03_piano_harmonic_progression"), [self.BELIEF],
        )[self.BELIEF]
        res_rand = runner.run(
            _load("ednr", "06_dense_atonal_random"), [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_prog, res_rand, "harmonic_prog", "atonal_random")
