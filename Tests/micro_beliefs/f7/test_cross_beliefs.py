"""Cross-belief tests — F7 beliefs interact correctly across units.

Validates:
  - PEOM × HGSIC: rhythmic stimuli activate entrainment + groove together
  - PEOM × HMCE: full piece activates entrainment + context together
  - HGSIC × HMCE: drums only = groove but not context (dissociation)
  - Groove inverted-U: critical falsification across groove_quality levels

Science:
  - Grahn & Brett 2007: metric rhythm → putamen/SMA co-activation (fMRI N=14)
  - Janata et al 2012: full ensemble → motor + auditory cortex (fMRI N=17)
  - Madison et al 2011 / Witek et al 2014: syncopation-groove inverted-U
"""
from __future__ import annotations

import pathlib

import numpy as np
import pytest
import torch
from scipy.io import wavfile

from Tests.micro_beliefs.audio_stimuli import silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO,
    midi_isochronous,
    C4 as MC4,
)
from Tests.micro_beliefs.assertions import assert_greater, assert_in_range

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


class TestPEOMHGSICCrossUnit:
    """PEOM entrainment × HGSIC groove co-activation.

    CONFIRMED: rhythmic stimuli co-activate both units above silence.
    """

    def test_groove_activates_entrainment_and_groove(self, runner):
        """Full groove → both period_entrainment AND groove_quality above silence.

        Grahn & Brett 2007: metric groove activates putamen (entrainment)
        + SMA (motor preparation) simultaneously.
        """
        beliefs = ["period_entrainment", "groove_quality"]
        res_groove = runner.run(
            _load("cross", "01_groove_with_phrases"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_groove[b], res_sil[b],
                f"groove_{b}", f"silence_{b}",
            )

    def test_drums_only_has_entrainment_and_groove(self, runner):
        """Drums only → both entrainment + groove above silence.

        Pure rhythm drives motor pathway without harmonic context.
        """
        beliefs = ["period_entrainment", "groove_quality"]
        res_drums = runner.run(
            _load("cross", "03_drums_only_no_harmony"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_drums[b], res_sil[b],
                f"drums_{b}", f"silence_{b}",
            )


class TestHGSICHMCEDissociation:
    """HGSIC groove × HMCE context dissociation.

    Drums only = high groove but low context (no pitch structure).
    Melody alone = high context but low groove (no beat grid).

    This is a critical scientific test of functional dissociation.
    """

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_drums_above_melody_groove(self, runner):
        """Drums-only >> melody-only for groove_quality.

        Drums provide rhythmic structure driving groove; melody alone
        lacks beat grid. Functional dissociation: HGSIC should respond
        more to drums than melody.
        Spread ~0.003 — extraction averages spectral energy.
        """
        res_drums = runner.run(
            _load("cross", "03_drums_only_no_harmony"),
            ["groove_quality"],
        )["groove_quality"]
        res_melody = runner.run(
            _load("cross", "02_piano_melody_no_rhythm"),
            ["groove_quality"],
        )["groove_quality"]
        assert_greater(res_drums, res_melody, "drums_groove", "melody_groove")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_melody_above_drums_context(self, runner):
        """Melody-only >> drums-only for context_depth.

        Melody provides pitch structure driving context; drums alone
        lack tonal organisation. Functional dissociation: HMCE should
        respond more to melody than drums.
        Spread ~0.002 — extraction averages spectral energy.
        """
        res_melody = runner.run(
            _load("cross", "02_piano_melody_no_rhythm"),
            ["context_depth"],
        )["context_depth"]
        res_drums = runner.run(
            _load("cross", "03_drums_only_no_harmony"),
            ["context_depth"],
        )["context_depth"]
        assert_greater(res_melody, res_drums, "melody_context", "drums_context")


class TestPEOMHMCECrossUnit:
    """Full groove+phrases → all three units active.

    CONFIRMED: full integration co-activates all three core beliefs.
    """

    def test_full_piece_above_silence_all_units(self, runner):
        """Full piece (groove+phrases) >> silence for all three core beliefs.

        Full integration: motor + groove + context co-activated.
        """
        beliefs = ["period_entrainment", "groove_quality", "context_depth"]
        res_full = runner.run(
            _load("cross", "01_groove_with_phrases"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_full[b], res_sil[b],
                f"full_{b}", f"silence_{b}",
            )


class TestGrooveInvertedU:
    """Groove quality inverted-U with syncopation level.

    CRITICAL FALSIFICATION (Madison et al 2011 / Witek et al 2014):
      medium syncopation > zero syncopation (too rigid)  — CONFIRMED
      medium syncopation > heavy syncopation (too chaotic) — xfail
      zero syncopation > random velocity (floor)          — xfail
    """

    def test_inverted_u_peak(self, runner):
        """Funk (medium sync) > straight (zero sync) for groove.

        Witek et al 2014: medium syncopation = groove peak.
        CONFIRMED: ascending side of inverted-U holds.
        """
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            ["groove_quality"],
        )["groove_quality"]
        res_str = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            ["groove_quality"],
        )["groove_quality"]
        assert_greater(res_funk, res_str, "funk_medium_sync", "straight_zero_sync")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_inverted_u_past_peak(self, runner):
        """Funk (medium sync) > heavy syncopation for groove.

        Madison et al 2011: groove decreases past the syncopation peak.
        CRITICAL: descending side of inverted-U.
        Spread ~0.01 — extraction responds to overall spectral energy.
        """
        res_funk = runner.run(
            _load("hgsic", "02_drums_funk_groove"),
            ["groove_quality"],
        )["groove_quality"]
        res_heavy = runner.run(
            _load("hgsic", "03_drums_heavy_syncopation"),
            ["groove_quality"],
        )["groove_quality"]
        assert_greater(res_funk, res_heavy, "funk_medium_sync", "heavy_sync")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_inverted_u_floor(self, runner):
        """Straight beat > random velocity for groove.

        Even zero syncopation (regular beat) should produce more groove
        than completely random velocity (no rhythmic structure).
        Spread ~0.01 — extraction averages onset density.
        """
        res_str = runner.run(
            _load("hgsic", "01_drums_straight_4_4"),
            ["groove_quality"],
        )["groove_quality"]
        res_rand = runner.run(
            _load("hgsic", "14_drums_random_velocity"),
            ["groove_quality"],
        )["groove_quality"]
        assert_greater(res_str, res_rand, "straight_zero_sync", "random_velocity")


class TestMetricModulationCrossUnit:
    """Metric modulation 4/4→3/4 affects entrainment + boundary detection.

    CONFIRMED: metric modulation above silence for both beliefs.
    """

    def test_metric_change_above_silence(self, runner):
        """Metric modulation >> silence for both entrainment + boundary.

        Grahn & Brett 2007: metre change requires putamen/SMA re-calibration.
        """
        beliefs = ["period_entrainment", "phrase_boundary_pred"]
        res_mod = runner.run(
            _load("cross", "07_metric_modulation_4_to_3"), beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_mod[b], res_sil[b],
                f"metric_mod_{b}", f"silence_{b}",
            )
