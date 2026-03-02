"""Micro-belief tests — MEAMN relay (Music-Evoked Autobiographical Memory Network).

7 beliefs tested:
  1. autobiographical_retrieval  (Core, tau=0.85) — "I remember this"
  2. nostalgia_intensity         (Core, tau=0.8)  — "This feels like home"
  3. emotional_coloring          (Core, tau=0.75) — "This makes me feel..."
  4. retrieval_probability       (Appraisal)      — memory accessibility
  5. memory_vividness            (Appraisal)      — retrieval × emotion product
  6. self_relevance              (Appraisal)      — vmPFC self-referential
  7. vividness_trajectory        (Anticipation)   — "Memory will become vivid"

Stimuli rationale:
  - MEAMN reads R³ via: warmth[12], stumpf_fusion[3], roughness[0],
    loudness[10], x_l0l5[25:33], x_l5l7[41:49]
  - E0:f01_retrieval = 0.90 × (0.40×x_l0l5×retrieval + 0.30×retrieval×stumpf
    + 0.30×x_l0l5×stumpf)  [BCH-style additive pairwise]
    where retrieval = 0.50×stumpf_mean_1s + 0.50×stumpf_mean_5s
  - E1:f02_nostalgia = 0.85 × x_l5l7.mean × familiarity_proxy
    where familiarity = 0.50×warmth_val_1s + 0.50×warmth_mean_5s
  - E2:f03_emotion = 0.85 × (0.40×valence×loudness + 0.30×valence×arousal
    + 0.30×loudness×arousal)  [BCH-style additive pairwise]

Science:
  - Janata 2009: mPFC tracks tonal space, N=13, p<0.0003
  - Sakakibara 2025: EEG nostalgia, N=33, eta_p^2=0.636
  - Belfi 2016: music-evoked memories more vivid than word-cued
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, G4, C5,
    crossfade, harmonic_complex, inharmonic_complex, noise,
    rich_dyad, silence,
)
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, STRINGS, CHOIR, FLUTE,
    midi_chord, midi_note, midi_melody, midi_progression,
    midi_melody_with_chords,
    major_triad, minor_triad, dominant_seventh,
    diatonic_scale, chromatic_cluster,
    C3, G3, A3, F3,
    C4 as MC4, E4, F4 as MF4, G4 as MG4,
    C5 as MC5, D5, E5, F5, G5,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_in_range,
    assert_ordering, assert_stable, assert_falling, assert_rising,
)


# =====================================================================
# 1. autobiographical_retrieval (Core, tau=0.85)
# =====================================================================

class TestAutobiographicalRetrieval:
    """Warm, consonant music should score higher than harsh/dissonant.

    observe = 0.40×P0:memory_state + 0.30×E0:f01_retrieval + 0.30×P1:emotional_color
    E0 depends on stumpf_fusion × x_l0l5 × warmth.
    tau=0.85: very slow decay — memories persist.
    """

    BELIEF = "autobiographical_retrieval"

    def test_warm_organ_above_cluster(self, runner):
        """Organ C major >> 12-note cluster for retrieval.

        Janata 2009: mPFC tracks tonal space coherence (N=13, p<0.0003).
        Organ provides high warmth + stumpf_fusion + x_l5l7.
        """
        res_organ = runner.run(
            midi_chord(major_triad(C3) + major_triad(MC4), 6.0,
                       program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_cluster = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 6.0,
                       program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_cluster, "organ_cmaj", "cluster_12")

    def test_melody_above_cluster(self, runner):
        """Piano melody >> chromatic cluster for retrieval.

        Structured melodic input provides high stumpf_fusion + x_l0l5 drive.
        Cluster has low stumpf (dissonant) → low retrieval binding.
        Janata 2009: tonal coherence drives mPFC autobiographical retrieval.
        """
        melody = diatonic_scale(MC4, 8)
        res_mel = runner.run(
            midi_melody(melody, [0.5] * 8, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_cluster = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 6.0,
                       program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_mel, res_cluster, "piano_melody", "cluster")

    def test_strings_above_cluster(self, runner):
        """Strings melody >> chromatic cluster for retrieval.

        Warm timbral melody provides familiarity + consonance drive.
        Cluster has maximal roughness → minimal autobiographical binding.
        """
        melody = diatonic_scale(MC4, 8)
        res_str = runner.run(
            midi_melody(melody, [0.75] * 8, program=STRINGS, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_cluster = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 6.0,
                       program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_str, res_cluster, "strings_melody", "cluster")

    def test_consonance_hierarchy(self, runner):
        """P1 (unison) > P5 > m2 for retrieval — follows stumpf_fusion.

        Bidelman 2009: brainstem FFR follows Pythagorean hierarchy (r>=0.81).
        """
        stims = {
            "P1": rich_dyad(C4, C4, duration_s=4.0),
            "P5": rich_dyad(C4, G4, duration_s=4.0),
            "m2": rich_dyad(C4, Db4, duration_s=4.0),
        }
        results = {
            k: runner.run(v, [self.BELIEF])[self.BELIEF]
            for k, v in stims.items()
        }
        assert_ordering(results, ["P1", "P5", "m2"], self.BELIEF)

    def test_transition_rising(self, runner):
        """Dissonant→consonant transition should show rising retrieval.

        Tests tau=0.85 temporal dynamics: slow rise as warmth appears.
        """
        audio = crossfade(
            inharmonic_complex(C4, 8, 1.2, 5.0),
            harmonic_complex(C4, 8, 5.0),
            5.0,
        )
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_sustained_stability(self, runner):
        """Sustained organ chord should be stable over time (tau=0.85)."""
        result = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        """Values should be in [0, 1] for all stimulus types."""
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            midi_chord(chromatic_cluster(MC4, 12), 4.0),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. nostalgia_intensity (Core, tau=0.8)
# =====================================================================

class TestNostalgiaIntensity:
    """Warm timbres + consonance should score highest for nostalgia.

    observe = 0.40×P2:nostalgia_link + 0.30×E1:f02_nostalgia + 0.30×P0:memory_state
    E1 = σ(0.70 × x_l5l7.mean × familiarity_proxy)
    familiarity_proxy = 0.50×warmth_val_1s + 0.50×warmth_mean_5s

    Science: Sakakibara 2025 — warm timbres enhance nostalgia (eta_p^2=0.636).
    """

    BELIEF = "nostalgia_intensity"

    def test_choir_above_piano(self, runner):
        """Choir (max warmth) > piano for nostalgia.

        Sakakibara 2025: vocal timbres trigger strongest nostalgia.
        """
        res_choir = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=CHOIR, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_piano = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=PIANO, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_choir, res_piano, "choir", "piano")

    def test_organ_above_silence(self, runner):
        """Organ C major >> silence for nostalgia.

        Warm organ timbre drives E1:f02_nostalgia via x_l5l7×warmth.
        Silence produces baseline nostalgia (~0.55).
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_organ, res_sil, "organ_cmaj", "silence")

    def test_strings_above_noise(self, runner):
        """Strings (warm timbre) >> noise for nostalgia."""
        res_str = runner.run(
            midi_note(MC4, 6.0, program=STRINGS, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_str, res_noise, "strings", "noise")

    def test_warm_to_cold_falling(self, runner):
        """Organ (5s) → cluster (5s) should show falling nostalgia.

        Tests temporal tracking: warmth drops at 5s boundary.
        """
        # Build two-part stimulus
        pm_organ = midi_chord(
            major_triad(C3) + major_triad(MC4), 10.0,
            program=ORGAN, velocity=75,
        )
        pm_cluster = midi_chord(
            chromatic_cluster(MC4, 12), 10.0,
            program=PIANO, velocity=110,
        )
        # Use crossfade as proxy for warm→harsh transition
        audio = crossfade(
            harmonic_complex(C4, 8, 5.0),
            inharmonic_complex(C4, 8, 1.2, 5.0),
            5.0,
        )
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="falling")

    def test_sustained_stability(self, runner):
        """Sustained warm timbre should be stable (tau=0.8)."""
        result = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=CHOIR),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. emotional_coloring (Core, tau=0.75)
# =====================================================================

class TestEmotionalColoring:
    """Loud consonant music should score highest for emotional coloring.

    observe = 0.40×P1:emotional_color + 0.30×E2:f03_emotion + 0.30×M0:meam_retrieval
    E2 = σ(0.60 × (1-roughness) × loudness × arousal)

    HIGH: low roughness (consonant) + high loudness (forte).
    LOW: high roughness (dissonant) + low loudness (pp).
    """

    BELIEF = "emotional_coloring"

    def test_loud_consonant_above_quiet_dissonant(self, runner):
        """Piano C major ff >> Piano m2 pp for emotional coloring.

        E2 = σ(0.60 × (1-roughness) × loudness × arousal).
        """
        res_loud = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=120),
            [self.BELIEF],
        )[self.BELIEF]
        res_quiet = runner.run(
            midi_chord([MC4, MC4 + 1], 5.0, program=PIANO, velocity=30),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_loud, res_quiet, "loud_consonant", "quiet_dissonant")

    def test_consonant_above_dissonant_same_loudness(self, runner):
        """C major > 12-note cluster at same velocity for emotional coloring.

        Roughness difference drives valence: (1-roughness) term.
        """
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_diss = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cons, res_diss, "consonant", "dissonant")

    def test_rich_texture_above_noise(self, runner):
        """Flute+organ ensemble >> noise for emotional coloring.

        Rich consonant ensemble: high valence (low roughness) + high loudness + arousal.
        Noise: roughness ≈ 1 → valence ≈ 0, suppresses emotional coloring.
        E2 = 0.85 × (0.40×valence×loudness + 0.30×valence×arousal + 0.30×loudness×arousal).
        """
        melody_notes = [E5, D5, MC5, E5, F5]
        melody_durs = [1.0] * 5
        chord_notes = [major_triad(MC4), minor_triad(A3),
                       major_triad(F3), major_triad(G3), major_triad(MC4)]
        chord_durs = [1.0] * 5
        res_rich = runner.run(
            midi_melody_with_chords(
                melody_notes, melody_durs, chord_notes, chord_durs,
                melody_program=FLUTE, chord_program=ORGAN,
            ),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_rich, res_noise, "flute_organ", "noise")

    def test_transition_rising(self, runner):
        """Noise→harmonic crossfade should show rising emotional coloring."""
        audio = crossfade(noise(4.0), harmonic_complex(C4, 8, 4.0), 4.0)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=PIANO, velocity=120),
            midi_chord([MC4, MC4 + 1], 4.0, program=PIANO, velocity=30),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. retrieval_probability (Appraisal)
# =====================================================================

class TestRetrievalProbability:
    """Direct read of P0:memory_state — memory accessibility.

    observe = P0:memory_state (1.0 weight).
    Driven by same factors as autobiographical_retrieval but without
    prediction cycle — immediate observation.
    """

    BELIEF = "retrieval_probability"

    def test_consonant_above_dissonant(self, runner):
        """Consonant music > dissonant for retrieval probability."""
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_diss = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 5.0, program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cons, res_diss, "consonant", "dissonant")

    def test_above_silence(self, runner):
        """Musical stimulus > silence for retrieval probability."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "music", "silence")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 5. memory_vividness (Appraisal)
# =====================================================================

class TestMemoryVividness:
    """Product of retrieval × emotional color.

    observe = E0:f01_retrieval × P1:emotional_color (multiplicative).
    HIGH when both retrieval and emotion are strong.
    LOW when either is weak.

    Science: Belfi 2016 — music-evoked memories more vivid than word-cued.
    """

    BELIEF = "memory_vividness"

    def test_rich_ensemble_above_cluster(self, runner):
        """Warm rich ensemble >> harsh cluster for vividness.

        Both retrieval AND emotion must be high for product to be large.
        """
        melody_notes = [E5, D5, MC5, E5, F5, E5]
        melody_durs = [1.0] * 6
        chord_notes = [major_triad(MC4), minor_triad(A3),
                       major_triad(F3), major_triad(G3),
                       major_triad(MC4), major_triad(MC4)]
        chord_durs = [1.0] * 6
        res_rich = runner.run(
            midi_melody_with_chords(
                melody_notes, melody_durs, chord_notes, chord_durs,
                melody_program=FLUTE, chord_program=ORGAN,
            ),
            [self.BELIEF],
        )[self.BELIEF]
        res_cluster = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 6.0, program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_rich, res_cluster, "rich_ensemble", "cluster")

    def test_above_silence(self, runner):
        """Any music > silence for vividness."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "music", "silence")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 6. self_relevance (Appraisal)
# =====================================================================

class TestSelfRelevance:
    """Direct read of F2:self_ref_fc — vmPFC self-referential processing.

    observe = F2:self_ref_fc (1.0 weight).

    Science: Janata 2009 — mPFC self-referential processing (N=13, p=0.012).
    """

    BELIEF = "self_relevance"

    def test_warm_above_noise(self, runner):
        """Warm consonant music > noise for self-relevance."""
        res_warm = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_warm, res_noise, "warm_organ", "noise")

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 7. vividness_trajectory (Anticipation)
# =====================================================================

class TestVividnessTrajectory:
    """Forward prediction: memory will become vivid within 2-5s.

    observe = F0:mem_vividness_fc (1.0 weight).
    Should track future vividness — higher for engaged musical contexts.

    Science: Janata 2009 — hippocampal retrieval trajectory (N=9).
    """

    BELIEF = "vividness_trajectory"

    def test_engaged_above_silence(self, runner):
        """Musical engagement > silence for vividness forecast."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "organ_chord", "silence")

    def test_warm_above_harsh(self, runner):
        """Warm music > harsh music for vividness forecast."""
        res_warm = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=CHOIR, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_harsh = runner.run(
            midi_chord(chromatic_cluster(MC4, 12), 5.0, program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_warm, res_harsh, "choir", "cluster")

    def test_stable_prediction(self, runner):
        """Sustained warm input should produce stable trajectory."""
        result = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
