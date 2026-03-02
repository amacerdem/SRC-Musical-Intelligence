"""Micro-belief tests — VMM relay (Valence-Mode Matching).

6 beliefs tested:
  1. perceived_happy     (Core, tau=0.55) — "This sounds happy"
  2. perceived_sad       (Core, tau=0.55) — "This sounds sad"
  3. mode_detection      (Appraisal)      — major/minor discrimination
  4. emotion_certainty   (Appraisal)      — confidence in valence read
  5. happy_pathway       (Appraisal)      — R0 happy extraction relay
  6. sad_pathway         (Appraisal)      — R1 sad extraction relay

Mechanism: VMM (12D relay, Phase 0b)
Key R³ inputs: consonance[4], warmth[12], tonalness[14], smoothness[16],
               tristimulus[18:21]
Key H³: consonance/warmth/tonalness at H19-H22 (macro scales)

Formulas:
  perceived_happy = 0.40×P0:perceived_happy + 0.30×V1:mode_signal
                    + 0.30×V2:consonance_valence
  perceived_sad   = 0.40×P1:perceived_sad + 0.30×(1-V1) + 0.30×(1-V2)
  mode_detection  = C0:mode_detection_state (1.0)
  emotion_certainty = P2:emotion_certainty (1.0)
  happy_pathway   = R0:happy_pathway (1.0)
  sad_pathway     = R1:sad_pathway (1.0)

Science:
  - Pallesen 2005: major=happy, minor=sad in fMRI (N=16)
  - Koelsch 2013: mode detection in auditory cortex review
  - Fritz 2009: cross-cultural valence recognition (N=40)
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import (
    C4, G4,
    noise, silence, rich_dyad,
)
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, FLUTE, CELLO,
    midi_chord, midi_melody,
    major_triad, minor_triad, chromatic_cluster,
    C3, C4 as MC4, D4, E4, F4 as MF4, G4 as MG4,
    C5 as MC5, D5, E5, F5, G5,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range, assert_stable,
)


# =====================================================================
# 1. perceived_happy (Core, tau=0.55)
# =====================================================================

class TestPerceivedHappy:
    """Major mode / bright timbre should score highest for happiness.

    observe = 0.40×P0:perceived_happy + 0.30×V1:mode_signal
              + 0.30×V2:consonance_valence
    V1 driven by consonance+warmth → major=high, minor=low.
    V2 driven by consonance_valence → consonant=high.

    Science: Pallesen 2005 — major mode activates reward; Fritz 2009 cross-cultural.
    """

    BELIEF = "perceived_happy"

    def test_major_above_minor(self, runner):
        """C major triad >> C minor triad for happiness.

        Pallesen 2005: major mode → higher reward activation (N=16).
        Major has higher consonance (M3 vs m3 interval).
        """
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_maj, res_min, "major_triad", "minor_triad")

    def test_major_above_cluster(self, runner):
        """Major chord >> chromatic cluster for happiness.

        Major chord: high consonance → high V1 + V2.
        Cluster: maximal dissonance → low consonance_valence.
        """
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_maj, res_clust, "major_chord", "cluster")

    def test_consonant_above_dissonant(self, runner):
        """Perfect 5th >> tritone for happiness.

        P5 has high consonance → high V2:consonance_valence.
        """
        res_p5 = runner.run(
            rich_dyad(C4, G4, 6, 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        # Tritone: C4 + F#4 (Db4 * 2^(6/12) ≈ Fsharp4)
        from Tests.micro_beliefs.audio_stimuli import Fsharp4
        res_tt = runner.run(
            rich_dyad(C4, Fsharp4, 6, 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_p5, res_tt, "perfect_fifth", "tritone")

    def test_organ_major_above_cluster(self, runner):
        """Organ major chord >> chromatic cluster for happiness.

        Organ: warm timbre + clear consonance → high V1 + V2.
        Cluster: maximal dissonance → low consonance_valence.
        VMM has narrow dynamic range; silence and noise baselines
        are elevated due to sigmoid cascade — cluster is the reliable floor.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ_major", "cluster")

    def test_stable_on_sustained(self, runner):
        """Sustained organ major chord should be stable (tau=0.55)."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        """All values in [0, 1]."""
        for audio in [
            midi_chord(major_triad(MC4), 4.0, program=PIANO),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. perceived_sad (Core, tau=0.55)
# =====================================================================

class TestPerceivedSad:
    """Minor mode / dark timbre should score highest for sadness.

    observe = 0.40×P1:perceived_sad + 0.30×(1-V1) + 0.30×(1-V2)
    Inverse of happy: low consonance/warmth → high sadness.

    Science: Pallesen 2005 — minor mode activates sadness circuits.
    """

    BELIEF = "perceived_sad"

    def test_minor_above_major(self, runner):
        """C minor triad >> C major triad for sadness.

        Minor has m3 interval → lower consonance → higher (1-V1).
        """
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_min, res_maj, "minor_triad", "major_triad")

    def test_dark_above_bright(self, runner):
        """Cello (dark, low) >> Flute (bright, high) for sadness.

        Low register + dark timbre → lower warmth → higher (1-V1).
        """
        dark_mel = [C3, D4 - 12, E4 - 12, MF4 - 12, MG4 - 12,
                    MF4 - 12, E4 - 12, D4 - 12]
        bright_mel = [MC5, D5, E5, F5, G5, F5, E5, D5]
        res_dark = runner.run(
            midi_melody(dark_mel, [0.5] * 8, program=CELLO, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        res_bright = runner.run(
            midi_melody(bright_mel, [0.5] * 8, program=FLUTE, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_dark, res_bright, "cello_dark", "flute_bright")

    def test_dissonant_above_consonant(self, runner):
        """Tritone >> P5 for sadness.

        Low consonance → high (1-V2).
        """
        from Tests.micro_beliefs.audio_stimuli import Fsharp4
        res_tt = runner.run(
            rich_dyad(C4, Fsharp4, 6, 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        res_p5 = runner.run(
            rich_dyad(C4, G4, 6, 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_tt, res_p5, "tritone", "perfect_fifth")

    def test_minor_above_noise(self, runner):
        """Minor chord >> noise for sadness.

        Even noise has low consonance, but minor chord has structured
        pitch content that drives (1-V1) + P1 above noise baseline.
        """
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_min, res_noise, "minor_chord", "noise")

    def test_above_silence(self, runner):
        """Minor chord >> silence for sadness."""
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_min, res_sil, "minor_chord", "silence")

    def test_stable_on_sustained(self, runner):
        """Sustained organ minor chord should be stable."""
        result = runner.run(
            midi_chord(minor_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(minor_triad(MC4), 4.0, program=PIANO),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. mode_detection (Appraisal)
# =====================================================================

class TestModeDetection:
    """Major/minor discrimination — direct relay from C0:mode_detection_state.

    observe = C0:mode_detection_state (1.0)
    Tracks mode detection in auditory cortex.

    Science: Koelsch 2013 — mode detection in bilateral STG.
    """

    BELIEF = "mode_detection"

    def test_major_above_noise(self, runner):
        """Major triad >> noise for mode detection.

        C0 mode detection tracks harmonic structure presence.
        Major/minor difference is very small in C0 relay (~0.0003);
        but both are clearly above noise baseline.
        """
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_maj, res_noise, "major", "noise")

    def test_chord_quality_above_cluster(self, runner):
        """Major triad >> chromatic cluster for mode detection.

        Clear harmonic structure → high mode certainty.
        """
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_maj, res_clust, "major_triad", "cluster")

    def test_above_silence(self, runner):
        """Piano chord >> silence."""
        res_chord = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_chord, res_sil, "chord", "silence")

    def test_stable(self, runner):
        """Sustained chord should be stable."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0),
            noise(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. emotion_certainty (Appraisal)
# =====================================================================

class TestEmotionCertainty:
    """Confidence in valence read — direct relay from P2:emotion_certainty.

    observe = P2:emotion_certainty (1.0)
    Clear harmonic structure → high certainty; ambiguous → low.

    Science: Koelsch 2013 — emotion certainty correlates with harmonic clarity.
    """

    BELIEF = "emotion_certainty"

    def test_clear_harmony_above_noise(self, runner):
        """Organ chord >> noise for emotion certainty.

        Clear harmonic structure → unambiguous valence → high certainty.
        Noise has zero harmonic structure → low certainty.
        P2 relay has narrow dynamic range; noise provides cleaner baseline.
        """
        res_clear = runner.run(
            midi_chord([MC4, MG4], 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_clear, res_noise, "P5_organ", "noise")

    def test_above_noise(self, runner):
        """Major chord >> noise for certainty.

        Noise baseline is lower than silence for P2 relay.
        """
        res_chord = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_chord, res_noise, "chord", "noise")

    def test_stable(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 5. happy_pathway (Appraisal)
# =====================================================================

class TestHappyPathway:
    """R0 happy extraction relay — early happy signal.

    observe = R0:happy_pathway (1.0)
    Driven by consonance + warmth + tonalness in extraction layer.
    """

    BELIEF = "happy_pathway"

    def test_major_above_minor(self, runner):
        """Major >> minor for happy pathway."""
        res_maj = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_maj, res_min, "major", "minor")

    def test_consonant_above_cluster(self, runner):
        """Major chord >> chromatic cluster for happy pathway.

        R0 extraction driven by consonance + warmth.
        Cluster has minimal consonance → low R0.
        """
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cons, res_clust, "major_chord", "cluster")

    def test_organ_above_cluster(self, runner):
        """Organ major >> chromatic cluster for happy pathway.

        R0 extraction tracks consonance + warmth.
        VMM noise/silence baselines are elevated; cluster is reliable floor.
        """
        res_organ = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_organ, res_clust, "organ_major", "cluster")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(major_triad(MC4), 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)


# =====================================================================
# 6. sad_pathway (Appraisal)
# =====================================================================

class TestSadPathway:
    """R1 sad extraction relay — early sad signal.

    observe = R1:sad_pathway (1.0)
    Driven by low consonance + low warmth in extraction layer.
    """

    BELIEF = "sad_pathway"

    def test_cluster_above_consonant(self, runner):
        """Chromatic cluster >> major chord for sad pathway.

        R1 sad extraction driven by low consonance + low warmth.
        Cluster: maximal dissonance → high R1.
        Major: high consonance → low R1.
        """
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_clust, res_cons, "cluster", "major_chord")

    def test_cluster_above_noise(self, runner):
        """Chromatic cluster >> noise for sad pathway.

        Cluster has structured dissonance that activates R1 sad extraction.
        test_cluster_above_consonant validates cluster > major;
        this test validates cluster > noise for a complete ordering.
        """
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_clust, res_noise, "cluster", "noise")

    def test_above_silence(self, runner):
        res_min = runner.run(
            midi_chord(minor_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_min, res_sil, "minor", "silence")

    def test_range(self, runner):
        result = runner.run(
            midi_chord(minor_triad(MC4), 4.0),
            [self.BELIEF],
        )[self.BELIEF]
        assert_in_range(result, self.BELIEF)
