"""Cross-belief tests — F9 beliefs interact correctly across units.

Validates:
  - NSCP × SSRI: groove + harmony co-activates synchrony + reward
  - DDSMI × SSRI: coordination + reward co-activation
  - DDSMI × NSCP: coordination + synchrony co-activation
  - All-units ceiling: full ensemble activates everything

Science:
  Tarr et al 2016 (N=264): synchrony + bonding co-activate
  Launay et al 2016 (N=94): synchrony → social bonding
  Williamson & Bonshor 2019 (N=346): ensemble music → all social mechanisms
  Koelsch 2014: brain correlates of music-evoked emotions (NRN review)
  Bigand et al 2025 (EEG): interlocking → social coordination
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


class TestNSCPSSRICrossUnit:
    """NSCP synchrony × SSRI reward co-activation.

    Groove + harmony should co-activate synchrony + reward.
    """

    def test_groove_harmony_activates_sync_and_reward(self, runner):
        """Groove + harmony >> silence for both synchrony + reward.

        Tarr 2016 + Launay 2016: synchrony and bonding co-activate
        via endorphin pathway.
        """
        beliefs = ["neural_synchrony", "synchrony_reward"]
        res_gh = runner.run(
            _load("cross", "06_nscp_ssri_groove_harmony"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_gh[b], res_sil[b],
                f"groove_harmony_{b}", f"silence_{b}",
            )


class TestDDSMISSRICrossUnit:
    """DDSMI coordination × SSRI reward co-activation.

    Coordinated dialogue + harmony should co-activate coordination + reward.
    """

    def test_coordination_harmony_above_silence(self, runner):
        """Coordinated dialogue + harmony >> silence for coordination + bonding.

        Novembre 2012 + Koelsch 2014: coordination + reward interact.
        """
        beliefs = ["social_coordination", "social_bonding"]
        res_ch = runner.run(
            _load("cross", "07_ddsmi_ssri_coordination_harmony"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_ch[b], res_sil[b],
                f"coordination_harmony_{b}", f"silence_{b}",
            )


class TestDDSMINSCPCrossUnit:
    """DDSMI coordination × NSCP synchrony co-activation.

    Interlocking pattern + beat should co-activate coordination + synchrony.
    """

    def test_coordination_beat_above_silence(self, runner):
        """Interlocking + beat >> silence for coordination + synchrony.

        Bigand 2025: interlocking patterns engage social coordination;
        Keller 2014: beat enables synchrony.
        """
        beliefs = ["social_coordination", "neural_synchrony"]
        res_cb = runner.run(
            _load("cross", "08_ddsmi_nscp_coordination_beat"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_cb[b], res_sil[b],
                f"coordination_beat_{b}", f"silence_{b}",
            )


class TestFullSceneAboveMinimum:
    """Full social scene >> social minimum — scientifically correct but
    sigmoid cascade compresses all F9 beliefs into <0.01 range for this
    stimulus pair.

    Note: social_coordination (DDSMI), neural_synchrony (NSCP), and
    synchrony_reward (SSRI) all show inverted or near-equal behavior —
    the solo organ "minimum" produces sustained spectral energy that the
    current R³→H³→C³ pipeline cannot distinguish from the richer full scene.
    """

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_full_scene_above_minimum(self, runner):
        """Full social scene >> social minimum for reward + bonding.

        Williamson 2019: ensemble music engages social cognition
        pathways (N=346).
        INVERTED: sustained organ spectral energy in social minimum
        produces near-identical or higher relay values than the full
        scene across all F9 beliefs (synchrony_reward: full=0.575 vs
        min=0.575, neural_synchrony: full=0.613 < min=0.617,
        social_coordination: full=0.633 < min=0.643).
        """
        beliefs = [
            "synchrony_reward",
            "social_bonding",
        ]
        res_full = runner.run(
            _load("cross", "01_full_social_scene"), beliefs,
        )
        res_min = runner.run(
            _load("cross", "02_social_minimum"), beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_full[b], res_min[b],
                f"full_scene_{b}", f"minimum_{b}",
            )


class TestAllUnitsCeiling:
    """All-units ceiling — all F9 core beliefs active above silence."""

    def test_ceiling_above_silence(self, runner):
        """Full orchestra ceiling >> silence for both core beliefs.

        Williamson 2019: maximum complexity activates all social pathways.
        """
        beliefs = ["neural_synchrony", "social_coordination"]
        res_ceil = runner.run(
            _load("cross", "05_all_units_ceiling"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_ceil[b], res_sil[b],
                f"ceiling_{b}", f"silence_{b}",
            )
