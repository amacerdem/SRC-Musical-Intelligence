"""Micro-belief tests — HCMC encoder (Hippocampal-Cortical Memory Circuit).

3 beliefs tested:
  1. episodic_encoding       (Core, tau=0.7) — "I am encoding this pattern"
  2. episodic_boundary       (Appraisal)     — "Phrase ended, new one began"
  3. consolidation_strength  (Appraisal)     — "Hippocampal→cortical transfer"

Mechanism: HCMC (11D, Depth 1, reads MEAMN relay output)
Key R³ inputs: stumpf_fusion[3], spectral_flux[21], onset_strength[11],
               loudness[10], amplitude[7], harmonicity[5], tonalness[14],
               entropy[22], x_l0l5[25:33], x_l5l7[41:49]

Formulas:
  E0:fast_binding = σ(0.35×x_l0l5×stumpf_1s + 0.35×stumpf×stumpf_1s
                      + 0.30×onset_str×loudness)
  E1:episodic_seg = σ(0.40×flux×flux_1s + 0.30×entropy×flux
                      + 0.30×onset_str×flux)
  E2:cortical_storage = σ(0.35×x_l5l7×harm_5s + 0.35×harmonicity×autocorr_5s
                          + 0.30×(1-entropy)×tonalness)

Science:
  - Fernandez-Rubio 2022: hippocampal binding at 4th tone (N=71, p<0.001)
  - Zacks 2007: event segmentation theory (N=72)
  - Rolls 2013: CA3 autoassociative binding
  - Sikka 2015: hippocampal→cortical shift for melody (N=40)
"""
from __future__ import annotations

import pytest
import numpy as np

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4, C5,
    harmonic_complex, inharmonic_complex, noise, silence, crossfade,
    rich_dyad,
)
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, VIOLIN, FLUTE, STRINGS,
    midi_note, midi_chord, midi_melody, midi_progression,
    midi_isochronous, midi_crescendo, midi_decrescendo,
    major_triad, minor_triad, dominant_seventh,
    diatonic_scale, chromatic_cluster,
    C3, G3, A3, F3,
    C4 as MC4, D4, E4, F4 as MF4, G4 as MG4, Ab4,
    C5 as MC5,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
    assert_ordering, assert_stable, assert_rising, assert_falling,
)


# =====================================================================
# 1. episodic_encoding (Core, tau=0.7)
# =====================================================================

class TestEpisodicEncoding:
    """Strong onsets + consonance produce highest episodic encoding.

    observe = 0.40×P0:binding_state + 0.30×E0:fast_binding + 0.30×P1:segmentation
    E0 = σ(0.35×x_l0l5×stumpf_1s + 0.35×stumpf×stumpf_1s + 0.30×onset_str×loudness)

    HIGH: strong rhythmic beats + consonant harmony (piano forte @120BPM).
    LOW: sustained quiet tone (no onsets after initial).

    Science: Fernandez-Rubio 2022 — hippocampal binding at 4th tone (N=71, p<0.001).
    """

    BELIEF = "episodic_encoding"

    def test_strong_beats_above_sustained(self, runner):
        """Piano @120BPM forte >> quiet sustained organ for encoding.

        Fernandez-Rubio 2022: repeated tonal onsets trigger hippocampal binding.
        """
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=100),
            [self.BELIEF],
        )[self.BELIEF]
        res_sust = runner.run(
            midi_note(MC4, 8.0, program=ORGAN, velocity=40),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_beats, res_sust, "strong_beats", "sustained_quiet")

    def test_consonant_beats_above_noise(self, runner):
        """Consonant beats >> noise for encoding."""
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=90),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(8.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_noise, "consonant_beats", "noise")

    def test_beats_above_silence(self, runner):
        """Any beats >> silence for encoding.

        Silence produces floor episodic_encoding (~0.56) — well below
        any stimulus with onsets (~0.60+).
        """
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_sil, "beats", "silence")

    def test_crescendo_rising(self, runner):
        """Crescendo beats (v=40→120) should show rising encoding.

        onset_str × loudness increases over time.
        """
        result = runner.run(
            midi_crescendo(MC4, n_steps=16, step_dur=0.5,
                           v_start=40, v_end=120, program=PIANO),
            [self.BELIEF],
        )[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_decrescendo_falling(self, runner):
        """Decrescendo beats (v=120→40) should show falling encoding."""
        result = runner.run(
            midi_decrescendo(MC4, n_steps=16, step_dur=0.5,
                             v_start=120, v_end=40, program=PIANO),
            [self.BELIEF],
        )[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="falling")

    def test_sustained_stability(self, runner):
        """Sustained beats at same velocity should be stable."""
        result = runner.run(
            midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=100),
            midi_note(MC4, 6.0, program=ORGAN, velocity=40),
            noise(6.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. episodic_boundary (Appraisal)
# =====================================================================

class TestEpisodicBoundary:
    """Abrupt spectral changes should score highest for boundary detection.

    observe = P1:segmentation_state (1.0 weight)
    E1 = σ(0.40×flux×flux_1s + 0.30×entropy×flux + 0.30×onset_str×flux)

    HIGH: abrupt key transitions (max spectral_flux at boundaries).
    LOW: sustained unchanging tone (zero flux after initial onset).

    Science: Zacks 2007 — event segmentation theory (N=72).
    """

    BELIEF = "episodic_boundary"

    def test_key_changes_above_drone(self, runner):
        """Abrupt key transitions >> smooth organ drone for boundary.

        Zacks 2007: event boundaries trigger segmentation at key changes.
        """
        # Rapid key changes
        pm_keys = midi_progression(
            [major_triad(MC4), major_triad(MF4),
             major_triad(Ab4), major_triad(E4)],
            [2.0, 2.0, 2.0, 2.0],
            program=PIANO, velocity=90,
        )
        res_keys = runner.run(pm_keys, [self.BELIEF])[self.BELIEF]

        # Smooth drone
        res_drone = runner.run(
            midi_chord([C3, MG4, MC4, E4, MG4], 8.0,
                       program=ORGAN, velocity=65),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_keys, res_drone, "key_changes", "smooth_drone")

    def test_rapid_changes_above_repetition(self, runner):
        """Rapid key changes > repeated same chord for boundary.

        Novelty at each chord boundary drives spectral_flux.
        """
        # Circle of fifths, 1s per key
        keys = [MC4, MG4, D4, A3]
        chords = [major_triad(k) for k in keys] * 2
        durs = [1.0] * 8
        res_changes = runner.run(
            midi_progression(chords, durs, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]

        # Same chord repeated
        same_chords = [major_triad(MC4)] * 8
        res_same = runner.run(
            midi_progression(same_chords, durs, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_changes, res_same, "key_changes", "repetition")

    def test_silence_gap_creates_boundary(self, runner):
        """Music with silence gap should detect boundary at gap.

        Spectral flux spikes at onset/offset transitions.
        """
        # Use crossfade from tone to silence to tone
        from Tests.micro_beliefs.audio_stimuli import concatenate
        seg1 = harmonic_complex(C4, 8, 3.0)
        seg2 = silence(1.0)
        seg3 = harmonic_complex(C4, 8, 3.0)
        audio = concatenate(seg1, seg2, seg3)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        # Should have boundary signal > silence alone
        res_sil = runner.run(silence(7.0), [self.BELIEF])[self.BELIEF]
        assert_greater(result, res_sil, "with_gap", "pure_silence")

    def test_above_silence(self, runner):
        """Any structured music > pure silence for boundary."""
        res_mus = runner.run(
            midi_progression(
                [major_triad(MC4), major_triad(MF4)],
                [3.0, 3.0], program=PIANO, velocity=80,
            ),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "music_with_changes", "silence")

    def test_range(self, runner):
        for audio in [
            midi_progression(
                [major_triad(MC4), major_triad(E4)],
                [3.0, 3.0], program=PIANO,
            ),
            midi_note(MC4, 6.0, program=ORGAN),
            noise(6.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. consolidation_strength (Appraisal)
# =====================================================================

class TestConsolidationStrength:
    """Sustained tonal coherence should maximize consolidation.

    observe = P2:storage_state (1.0 weight)
    E2 = σ(0.35×x_l5l7×harm_5s + 0.35×harmonicity×tonal_autocorr_5s
           + 0.30×(1-entropy)×tonalness)

    HIGH: sustained tonal music (high harmonicity + tonalness + low entropy).
    LOW: high entropy chaos (random clusters).

    Science: Sikka 2015 — hippocampal→cortical shift for melody (N=40).
    """

    BELIEF = "consolidation_strength"

    def test_tonal_above_silence(self, runner):
        """Tonal repetition >> silence for consolidation.

        Sikka 2015: tonal repetition enables hippocampal→cortical transfer.
        Silence floor (~0.578) is well below tonal stimuli (~0.67+).
        """
        res_tonal = runner.run(
            midi_progression([major_triad(MC4)] * 8, [1.0] * 8,
                             program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(8.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_tonal, res_sil, "tonal_repetition", "silence")

    def test_organ_drone_above_noise(self, runner):
        """Sustained organ drone >> noise for consolidation.

        Organ drone: max harmonicity, max tonalness, min entropy.
        """
        res_drone = runner.run(
            midi_chord([C3, MG4, MC4, E4, MG4], 8.0,
                       program=ORGAN, velocity=65),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(8.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_drone, res_noise, "organ_drone", "noise")

    def test_music_above_silence(self, runner):
        """Musical stimulus >> silence for consolidation.

        Any tonal input provides harmonicity + tonalness signals that
        drive cortical storage, absent in silence (~0.578 floor).
        """
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "piano_chord", "silence")

    def test_ordering(self, runner):
        """Organ drone > Piano beats > Noise for consolidation."""
        stims = {
            "Organ": midi_chord([C3, MC4, E4, MG4], 6.0,
                                program=ORGAN, velocity=70),
            "Piano": midi_isochronous(MC4, 120.0, 12,
                                      program=PIANO, velocity=80),
            "Noise": noise(6.0),
        }
        results = {
            k: runner.run(v, [self.BELIEF])[self.BELIEF]
            for k, v in stims.items()
        }
        assert_ordering(results, ["Organ", "Piano", "Noise"], self.BELIEF)

    def test_sustained_stability(self, runner):
        """Sustained tonal input should produce stable consolidation."""
        result = runner.run(
            midi_chord([C3, MC4], 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)
