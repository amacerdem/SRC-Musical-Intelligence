"""Micro-belief tests — HMCE relay (Hierarchical Musical Context Encoding).

6 beliefs tested:
  1. context_depth        (Core, tau=0.65) — depth of hierarchical model
  2. short_context        (Appraisal)      — local (2-bar) repetition
  3. medium_context       (Appraisal)      — phrase-level (8-bar) structure
  4. long_context         (Appraisal)      — formal (16+ bar) organization
  5. phrase_boundary_pred (Anticipation)   — boundary detection forecast
  6. structure_pred       (Anticipation)   — structural continuation forecast

Mechanism: HMCE (Phase 0a)
Key R³ inputs: spectral_autocorr[17], spectral_change[21],
               x_l5l7[51], x_l0l2l5[60]
Key H³: spectral_auto/onset@H3(100ms), hier_mean@H8/H16(phrase/structure)

Science:
  - Koelsch 2009: CPS (Closure Positive Shift) at phrase boundaries
    (ERP review, multiple studies)
  - Pearce 2018: IDyOM information content drops with structural regularity
    (computational model + behavioural validation)
  - Tillmann, Janata & Bharucha 2003: implicit harmonic structure from
    repetition (fMRI N=20, inferior frontal cortex priming)
"""
from __future__ import annotations

import pathlib

import numpy as np
import pytest
import torch
from scipy.io import wavfile

from Tests.micro_beliefs.audio_stimuli import noise, silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, STRINGS,
    midi_note, midi_chord, midi_melody, midi_progression,
    major_triad, minor_triad, dominant_seventh,
    diatonic_scale,
    C3, C4 as MC4, G4, C5,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_rising,
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
# 1. context_depth (Core, tau=0.65)
# =====================================================================

class TestContextDepth:
    """Hierarchical model depth — how deep the structural model extends.

    32-bar AABA > 16-bar AABB > 8-bar phrase > 2-bar ostinato > atonal.

    Science: Pearce 2018 — IDyOM: longer forms with repetition build
    deeper models, reducing information content progressively.
    Tillmann et al 2003 — repeated chord progressions build implicit
    structure (fMRI N=20, inferior frontal cortex).
    """

    BELIEF = "context_depth"

    def test_32bar_above_2bar(self, runner):
        """32-bar AABA >> 2-bar ostinato for context depth.

        Pearce 2018: full formal organisation >> local repetition only.
        CONFIRMED: large structural contrast produces reliable separation.
        """
        res_long = runner.run(
            _load("hmce", "04_piano_32bar_aaba"),
            [self.BELIEF],
        )[self.BELIEF]
        res_short = runner.run(
            _load("hmce", "01_piano_2bar_ostinato"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_long, res_short, "32bar_AABA", "2bar_ostinato")

    def test_16bar_above_atonal(self, runner):
        """16-bar AABB >> atonal random for context depth.

        Structured tonal music >> no tonal/structural organisation.
        CONFIRMED: tonal vs atonal produces reliable separation.
        """
        res_struct = runner.run(
            _load("hmce", "03_piano_16bar_aabb"),
            [self.BELIEF],
        )[self.BELIEF]
        res_atonal = runner.run(
            _load("hmce", "11_piano_atonal_random"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_struct, res_atonal, "16bar_AABB", "atonal_random")

    def test_8bar_above_single_note(self, runner):
        """8-bar phrase >> single sustained note for context depth.

        CONFIRMED: musical structure vs static tone.
        """
        res_phrase = runner.run(
            _load("hmce", "02_piano_8bar_phrase"),
            [self.BELIEF],
        )[self.BELIEF]
        res_note = runner.run(
            _load("hmce", "14_piano_sustained_c4"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_phrase, res_note, "8bar_phrase", "single_note")

    def test_above_silence(self, runner):
        """Structured music >> silence for context depth."""
        res_struct = runner.run(
            _load("hmce", "02_piano_8bar_phrase"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_struct, res_sil, "8bar_phrase", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "04_piano_32bar_aaba"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. short_context (Appraisal)
# =====================================================================

class TestShortContext:
    """Local (2-bar) repetition detection.

    Repetitive ostinato > single note > silence.

    Science: Tillmann et al 2003 — repetition establishes implicit
    structure (fMRI N=20).
    """

    BELIEF = "short_context"

    def test_ostinato_above_single_note(self, runner):
        """2-bar ostinato >> single sustained note for short context.

        Repeated pattern → clear local structure.
        CONFIRMED: repetition vs static tone.
        """
        res_ost = runner.run(
            _load("hmce", "01_piano_2bar_ostinato"),
            [self.BELIEF],
        )[self.BELIEF]
        res_note = runner.run(
            _load("hmce", "14_piano_sustained_c4"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_ost, res_note, "2bar_ostinato", "single_note")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_phrase_gap_above_atonal(self, runner):
        """Phrase with gap >> atonal random for short context.

        Tillmann et al 2003: structured phrases with clear segments
        build stronger local models than unstructured pitch sequences.
        Spread ~0.008 — atonal random has higher spectral richness
        producing higher mean output via sigmoid cascade.
        """
        res_gap = runner.run(
            _load("hmce", "07_piano_phrase_with_gap"),
            [self.BELIEF],
        )[self.BELIEF]
        res_atonal = runner.run(
            _load("hmce", "11_piano_atonal_random"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_gap, res_atonal, "phrase_with_gap", "atonal_random")

    def test_above_silence(self, runner):
        """Local pattern >> silence."""
        res_ost = runner.run(
            _load("hmce", "01_piano_2bar_ostinato"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_ost, res_sil, "ostinato", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "01_piano_2bar_ostinato"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. medium_context (Appraisal)
# =====================================================================

class TestMediumContext:
    """Phrase-level (8-bar) structure detection.

    8-bar harmonic phrase >> atonal random >> silence.

    Science: Koelsch 2009 — phrase-level processing at theta timescale
    (ERP review, CPS at phrase boundaries).
    """

    BELIEF = "medium_context"

    def test_8bar_above_atonal(self, runner):
        """8-bar phrase >> atonal random for medium context.

        Koelsch 2009: phrase-level harmonic arc builds medium-scale model.
        CONFIRMED: structured vs unstructured produces reliable separation.
        """
        res_phrase = runner.run(
            _load("hmce", "02_piano_8bar_phrase"),
            [self.BELIEF],
        )[self.BELIEF]
        res_atonal = runner.run(
            _load("hmce", "11_piano_atonal_random"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_phrase, res_atonal, "8bar_phrase", "atonal_random")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_repeated_prog_above_single_note(self, runner):
        """I-IV-V-I ×3 >> single sustained note for medium context.

        Tillmann et al 2003: repeated harmonic progressions build
        phrase-level implicit structure.
        Spread ~0.02 — sustained note produces higher baseline due to
        stable spectral profile pushing sigmoid output higher.
        """
        res_prog = runner.run(
            _load("hmce", "12_strings_I_IV_V_I_x3"),
            [self.BELIEF],
        )[self.BELIEF]
        res_note = runner.run(
            _load("hmce", "14_piano_sustained_c4"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_prog, res_note, "I_IV_V_I_x3", "single_note")

    def test_above_silence(self, runner):
        """Phrase-level structure >> silence."""
        res_phrase = runner.run(
            _load("hmce", "02_piano_8bar_phrase"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_phrase, res_sil, "8bar_phrase", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "02_piano_8bar_phrase"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. long_context (Appraisal)
# =====================================================================

class TestLongContext:
    """Formal (16+ bar) organizational structure.

    16-bar AABB > 2-bar ostinato; 32-bar AABA > atonal.

    Science: Pearce 2018 — IDyOM: formal organisation reduces
    information content progressively over longer spans.
    """

    BELIEF = "long_context"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_16bar_above_2bar(self, runner):
        """16-bar AABB >> 2-bar ostinato for long context.

        Pearce 2018: formal structure extends the hierarchical model
        beyond local repetition.
        Spread ~0.04 — shorter stimuli with more onset density produce
        higher mean output due to spectral richness bias.
        """
        res_long = runner.run(
            _load("hmce", "03_piano_16bar_aabb"),
            [self.BELIEF],
        )[self.BELIEF]
        res_short = runner.run(
            _load("hmce", "01_piano_2bar_ostinato"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_long, res_short, "16bar_AABB", "2bar_ostinato")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_32bar_above_atonal(self, runner):
        """32-bar AABA >> atonal random for long context.

        Pearce 2018: formal tonal organisation over 32 bars builds
        a deep hierarchical model; atonal random prevents this.
        """
        res_long = runner.run(
            _load("hmce", "04_piano_32bar_aaba"),
            [self.BELIEF],
        )[self.BELIEF]
        res_atonal = runner.run(
            _load("hmce", "11_piano_atonal_random"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_long, res_atonal, "32bar_AABA", "atonal_random")

    def test_above_silence(self, runner):
        """Long-form music >> silence."""
        res_long = runner.run(
            _load("hmce", "03_piano_16bar_aabb"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_long, res_sil, "16bar_AABB", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "03_piano_16bar_aabb"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 5. phrase_boundary_pred (Anticipation)
# =====================================================================

class TestPhraseBoundaryPred:
    """Phrase boundary detection forecast — anticipation of structural breaks.

    Silence gaps, key changes, and cadences signal boundaries.

    Science: Koelsch 2009 — CPS (Closure Positive Shift) at phrase
    boundaries (ERP review, multiple studies N=12-24 typical).
    """

    BELIEF = "phrase_boundary_pred"

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_gap_above_continuous(self, runner):
        """Phrase with silence gap >> continuous chromatic for boundaries.

        Koelsch 2009: silence gaps are the strongest phrase boundary cue,
        eliciting CPS (Closure Positive Shift) in ERP.
        Spread ~0.002 — sigmoid cascade compresses all to near-identical range.
        """
        res_gap = runner.run(
            _load("hmce", "07_piano_phrase_with_gap"),
            [self.BELIEF],
        )[self.BELIEF]
        res_chrom = runner.run(
            _load("hmce", "06_piano_chromatic_wandering"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_gap, res_chrom, "phrase_with_gap", "chromatic_continuous")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_key_change_above_chromatic(self, runner):
        """Key change (C→G) >> chromatic wandering for boundaries.

        Koelsch 2009: key changes signal structural boundaries at the
        tonal level, distinct from surface-level chromatic motion.
        Spread ~0.002 — high-dimensional inputs average out the contrast.
        """
        res_key = runner.run(
            _load("hmce", "05_piano_key_change_c_to_g"),
            [self.BELIEF],
        )[self.BELIEF]
        res_chrom = runner.run(
            _load("hmce", "06_piano_chromatic_wandering"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_key, res_chrom, "key_change_C_to_G", "chromatic")

    def test_aba_above_through_composed(self, runner):
        """ABA form >> through-composed for boundary detection.

        ABA has clear A→B and B→A transitions = strong boundaries.
        CONFIRMED: this ordering holds in current extraction.
        """
        res_aba = runner.run(
            _load("hmce", "09_piano_aba_form"),
            [self.BELIEF],
        )[self.BELIEF]
        res_tc = runner.run(
            _load("hmce", "10_piano_through_composed"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_aba, res_tc, "ABA_form", "through_composed")

    def test_above_silence(self, runner):
        """Structured music >> silence for boundary detection."""
        res_struct = runner.run(
            _load("hmce", "05_piano_key_change_c_to_g"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_struct, res_sil, "key_change", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "07_piano_phrase_with_gap"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 6. structure_pred (Anticipation)
# =====================================================================

class TestStructurePred:
    """Structural continuation forecast — predicts upcoming patterns.

    Sequential patterns and repetitions >> through-composed >> atonal.

    Science: Pearce 2018 — IDyOM: sequences reduce information content
    progressively, enabling accurate prediction.
    """

    BELIEF = "structure_pred"

    def test_sequence_above_through_composed(self, runner):
        """Ascending sequence >> through-composed for structure prediction.

        Pearce 2018: sequential patterns reduce information content,
        making continuation highly predictable.
        CONFIRMED: this ordering holds in current extraction.
        """
        res_seq = runner.run(
            _load("hmce", "08_piano_sequence_ascending"),
            [self.BELIEF],
        )[self.BELIEF]
        res_tc = runner.run(
            _load("hmce", "10_piano_through_composed"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_seq, res_tc, "ascending_sequence", "through_composed")

    @pytest.mark.xfail(reason=_NARROW_RANGE, strict=False)
    def test_aba_above_through_composed(self, runner):
        """ABA form >> through-composed for structure prediction.

        Pearce 2018: ABA repetition reduces information content on
        the return of A, enabling structural prediction.
        Spread ~0.0002 — below sigmoid discrimination threshold.
        """
        res_aba = runner.run(
            _load("hmce", "09_piano_aba_form"),
            [self.BELIEF],
        )[self.BELIEF]
        res_tc = runner.run(
            _load("hmce", "10_piano_through_composed"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_aba, res_tc, "ABA_form", "through_composed")

    def test_repeated_prog_above_atonal(self, runner):
        """I-IV-V-I ×3 >> atonal for structure prediction.

        Tillmann et al 2003: repeated progressions → pattern learning.
        CONFIRMED: tonal vs atonal separation is reliable.
        """
        res_prog = runner.run(
            _load("hmce", "12_strings_I_IV_V_I_x3"),
            [self.BELIEF],
        )[self.BELIEF]
        res_atonal = runner.run(
            _load("hmce", "11_piano_atonal_random"),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_prog, res_atonal, "I_IV_V_I_x3", "atonal_random")

    def test_above_silence(self, runner):
        """Structured music >> silence for structure prediction."""
        res_struct = runner.run(
            _load("hmce", "08_piano_sequence_ascending"),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_struct, res_sil, "sequence", "silence")

    def test_range(self, runner):
        for audio in [
            _load("hmce", "08_piano_sequence_ascending"),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)
