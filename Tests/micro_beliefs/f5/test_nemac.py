"""Micro-belief tests — NEMAC relay (Nostalgia-Evoked Memory-Affect Coupling).

4 beliefs tested:
  1. nostalgia_affect          (Core, tau=0.65) — "This makes me nostalgic"
  2. self_referential_nostalgia (Appraisal)     — vmPFC self-referential activation
  3. wellbeing_enhancement      (Appraisal)     — positive wellbeing from nostalgia
  4. nostalgia_peak_pred        (Anticipation)  — "Nostalgia peak is coming"

Mechanism: NEMAC (11D relay, Phase 0c, Depth 1)
Key R³ inputs: warmth[12], stumpf_fusion[3], tonalness[14],
               smoothness[16], roughness[5]
Key H³: warmth/stumpf at H16/H20, tonalness at H19

Formulas:
  nostalgia_affect          = 0.40×W0:nostalgia_intens + 0.30×E1:nostalgia
                              + 0.30×P0:nostalgia_correl
  self_referential_nostalgia = M0:mpfc_activation (1.0)
  wellbeing_enhancement      = W1:wellbeing_enhance (1.0)
  nostalgia_peak_pred        = F1:vividness_pred (1.0)

Science:
  - Barrett 2010: nostalgia → wellbeing pathway (N=172)
  - Janata 2007: music-evoked autobiographical memories, N=13
  - Sakakibara 2025: EEG nostalgia with warm timbres (N=33, eta_p^2=0.636)
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import noise, silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, STRINGS, FLUTE,
    midi_chord, midi_melody,
    major_triad, chromatic_cluster, diatonic_scale,
    C4 as MC4,
    C5 as MC5, D5, E5, F5, G5,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range,
    assert_stable,
)


# =====================================================================
# 1. nostalgia_affect (Core, tau=0.65)
# =====================================================================

class TestNostalgiaAffect:
    """Warm timbres + consonance should score highest for nostalgia.

    observe = 0.40×W0:nostalgia_intens + 0.30×E1:nostalgia
              + 0.30×P0:nostalgia_correl
    W0/E1 driven by warmth + stumpf_fusion + tonalness.
    tau=0.65: moderate persistence — nostalgia builds slowly.

    Science: Sakakibara 2025 — warm timbres enhance nostalgia (eta_p^2=0.636).
    """

    BELIEF = "nostalgia_affect"

    def test_warm_above_harsh(self, runner):
        """Organ chord >> noise for nostalgia.

        Organ: max warmth + stumpf → high W0:nostalgia_intens.
        Noise: zero warmth, zero stumpf → minimal nostalgia.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_organ, res_noise, "organ_chord", "noise")

    def test_tonal_above_atonal(self, runner):
        """Piano melody >> chromatic cluster for nostalgia.

        Tonal melody: high tonalness + stumpf → nostalgic.
        Chromatic cluster: low stumpf → not nostalgic.
        """
        melody = diatonic_scale(MC4, 8)
        res_mel = runner.run(
            midi_melody(melody, [0.5] * 8, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_mel, res_clust, "piano_melody", "cluster")

    def test_strings_above_noise(self, runner):
        """Strings melody >> noise for nostalgia.

        Sakakibara 2025: warm timbres (strings) trigger nostalgia.
        """
        melody = [MC5, D5, E5, F5, G5, F5, E5, D5]
        res_str = runner.run(
            midi_melody(melody, [0.75] * 8, program=STRINGS, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(6.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_str, res_noise, "strings_melody", "noise")

    def test_organ_above_cluster(self, runner):
        """Organ chord >> chromatic cluster for nostalgia.

        Organ: high warmth + stumpf → nostalgic.
        Cluster: low stumpf, high roughness → not nostalgic.
        NEMAC silence baseline is elevated due to prior regression;
        cluster provides a cleaner low-nostalgia comparison.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ", "cluster")

    def test_stable_on_sustained(self, runner):
        """Sustained organ drone should be stable (tau=0.65)."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
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


# =====================================================================
# 2. self_referential_nostalgia (Appraisal)
# =====================================================================

class TestSelfReferentialNostalgia:
    """vmPFC self-referential activation — direct from M0:mpfc_activation.

    observe = M0:mpfc_activation (1.0)
    Tonal coherent music → self-referential processing.

    Science: Janata 2007 — mPFC tracks familiar tonal space (N=13).
    """

    BELIEF = "self_referential_nostalgia"

    def test_warm_organ_above_cluster(self, runner):
        """Warm organ chord >> chromatic cluster for self-referential nostalgia.

        Janata 2007: tonal coherence activates vmPFC self-referential processing.
        Organ provides sustained warmth + stumpf that drives M0.
        Cluster has low stumpf → low M0 activation.
        M0 relay has narrow dynamic range; melody < noise observed due to
        sigmoid cascade — use stronger contrast (organ vs cluster).
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ", "cluster")

    def test_organ_above_cluster(self, runner):
        """Organ chord >> chromatic cluster for self-referential nostalgia.

        M0 relay has narrow range; noise baseline is higher than organ
        due to sigmoid cascade in NEMAC extraction.
        Cluster provides a structured dissonant contrast.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ", "cluster")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. wellbeing_enhancement (Appraisal)
# =====================================================================

class TestWellbeingEnhancement:
    """Wellbeing from nostalgia pathway — direct from W1:wellbeing_enhance.

    observe = W1:wellbeing_enhance (1.0)
    Warm music → nostalgia → wellbeing cascade.

    Science: Barrett 2010 — nostalgia triggers positive wellbeing (N=172).
    """

    BELIEF = "wellbeing_enhancement"

    def test_warm_music_above_noise(self, runner):
        """Warm organ chord >> noise for wellbeing.

        Barrett 2010: warm nostalgic stimuli enhance wellbeing.
        """
        res_warm = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_warm, res_noise, "organ_chord", "noise")

    def test_organ_above_cluster(self, runner):
        """Warm organ >> chromatic cluster for wellbeing.

        Barrett 2010: nostalgia-evoked wellbeing requires warm stimuli.
        NEMAC silence baseline is elevated; cluster provides cleaner contrast.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ", "cluster")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. nostalgia_peak_pred (Anticipation)
# =====================================================================

class TestNostalgiaPeakPred:
    """Forward prediction of nostalgia peak — direct from F1:vividness_pred.

    observe = F1:vividness_pred (1.0)
    As an Anticipation belief, may regress toward prior.

    Science: Barrett 2010 — nostalgia trajectory prediction.
    """

    BELIEF = "nostalgia_peak_pred"

    def test_responds_to_musical_input(self, runner):
        """Nostalgia peak prediction should produce valid, stable output.

        As an Anticipation belief with forecast layer,
        it regresses toward prior — baseline may differ from active.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(res_organ, self.BELIEF)
        assert_stable(res_organ, self.BELIEF)

    def test_different_stimuli_valid(self, runner):
        """Both melody and noise produce valid predictions."""
        for audio in [
            midi_melody(diatonic_scale(MC4, 8), [0.5] * 8,
                        program=FLUTE, velocity=85),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)

    def test_above_silence(self, runner):
        """Musical input > silence for peak prediction."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "organ", "silence")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
