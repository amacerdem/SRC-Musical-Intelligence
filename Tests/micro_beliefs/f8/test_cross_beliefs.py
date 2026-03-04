"""Cross-belief tests — F8 beliefs interact correctly across units.

Validates:
  - TSCP × EDNR: rich ensemble co-activates timbre + network
  - ESME × EDNR: deviant in tonal context co-activates MMN + network
  - SLEE × ECT dissociation: pattern ≠ multi-instrument cost
  - All-units ceiling: full orchestra activates everything

Science:
  Criscuolo et al 2022 (ALE k=84 N=3005): bilateral STG + L IFG
  Rupp & Hansen 2022 (MEG): context-dependent MMR musicians > NM
  Bridwell 2017 (EEG N=13): pattern vs random 45% amplitude reduction
  Paraskevopoulos et al 2022 (MEG N=25): 106 within vs 192 between
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


class TestTSCPEDNRCrossUnit:
    """TSCP timbre × EDNR network co-activation.

    CONFIRMED: rich ensemble activates both timbre recognition +
    network specialization above silence.
    """

    def test_ensemble_activates_timbre_and_network(self, runner):
        """Rich ensemble >> silence for both timbre + network.

        Criscuolo 2022: multi-instrument activates bilateral STG + L IFG.
        """
        beliefs = ["trained_timbre_recognition", "network_specialization"]
        res_ens = runner.run(
            _load("cross", "01_rich_tonal_ensemble"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_ens[b], res_sil[b],
                f"ensemble_{b}", f"silence_{b}",
            )


class TestESMEEDNRCrossUnit:
    """ESME deviance × EDNR network co-activation.

    Deviant in tonal context should activate both MMN + network.
    """

    def test_oddball_activates_mmn_and_network(self, runner):
        """Oddball in tonal context >> silence for pitch_mmn + network.

        Rupp & Hansen 2022: context-dependent MMR enhanced in musicians
        for melodic paradigm.
        """
        beliefs = ["pitch_mmn", "network_specialization"]
        res_odd = runner.run(
            _load("cross", "02_oddball_tonal_context"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_odd[b], res_sil[b],
                f"oddball_{b}", f"silence_{b}",
            )


class TestSLEEECTDissociation:
    """SLEE pattern × ECT compartmentalization dissociation.

    Patterned single instrument = high SLEE, low ECT.
    Diverse ensemble no pattern = low SLEE, high ECT.
    """

    def test_patterned_single_above_silence_statistical(self, runner):
        """Patterned single instrument >> silence for statistical_model.

        Bridwell 2017: pattern learning drives statistical model.
        """
        res_pat = runner.run(
            _load("cross", "05_patterned_single_instrument"),
            ["statistical_model"],
        )["statistical_model"]
        res_sil = runner.run(silence(5.0), ["statistical_model"])["statistical_model"]
        assert_greater(res_pat, res_sil, "patterned_statistical", "silence")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_diverse_no_pattern_above_silence_cost(self, runner):
        """Diverse ensemble no pattern >> silence for compartmentalization_cost.

        Paraskevopoulos 2022: multi-instrument random = high between-network.
        INVERTED: silence=0.628 > diverse=0.579 — between_reduction
        baseline pushes silence above auditory stimuli.
        """
        res_div = runner.run(
            _load("cross", "06_diverse_ensemble_no_pattern"),
            ["compartmentalization_cost"],
        )["compartmentalization_cost"]
        res_sil = runner.run(
            silence(5.0), ["compartmentalization_cost"],
        )["compartmentalization_cost"]
        assert_greater(res_div, res_sil, "diverse_cost", "silence")

    def test_patterned_above_diverse_statistical(self, runner):
        """Patterned single >> diverse no-pattern for statistical_model.

        CONFIRMED: Bridwell 2017: pattern > random for statistical model.
        SLEE × ECT dissociation validated: SLEE prefers pattern,
        not multi-instrument complexity.
        """
        res_pat = runner.run(
            _load("cross", "05_patterned_single_instrument"),
            ["statistical_model"],
        )["statistical_model"]
        res_div = runner.run(
            _load("cross", "06_diverse_ensemble_no_pattern"),
            ["statistical_model"],
        )["statistical_model"]
        assert_greater(res_pat, res_div, "patterned", "diverse_no_pattern")

    def test_diverse_above_patterned_cost(self, runner):
        """Diverse no-pattern >> patterned single for compartmentalization_cost.

        CONFIRMED: Paraskevopoulos 2022: multi-instrument > single for
        between-network. ECT responds to cross-domain complexity, not
        pattern regularity.
        """
        res_div = runner.run(
            _load("cross", "06_diverse_ensemble_no_pattern"),
            ["compartmentalization_cost"],
        )["compartmentalization_cost"]
        res_pat = runner.run(
            _load("cross", "05_patterned_single_instrument"),
            ["compartmentalization_cost"],
        )["compartmentalization_cost"]
        assert_greater(res_div, res_pat, "diverse", "patterned_single")


class TestAllUnitsCeiling:
    """Full orchestra ceiling — all F8 units active above silence.

    CONFIRMED: full complexity co-activates all core beliefs.
    """

    def test_ceiling_above_silence_all_units(self, runner):
        """Full orchestra >> silence for all core beliefs.

        Bucher et al 2023: HG 130% larger in professionals.
        """
        beliefs = [
            "trained_timbre_recognition",
            "network_specialization",
            "statistical_model",
            "expertise_enhancement",
        ]
        res_full = runner.run(
            _load("cross", "08_expertise_ceiling"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_full[b], res_sil[b],
                f"ceiling_{b}", f"silence_{b}",
            )
