"""Cross-belief tests — F6 beliefs interact correctly across units.

Validates:
  - SRP wanting × DAED da_caudate co-activation (anticipatory pathway)
  - SRP liking × DAED da_nacc co-activation (consummatory pathway)
  - SRP tension × harmonic_tension internal consistency
  - SRP prediction_error × prediction_match inverse relationship
  - Cross-unit: energetic music activates both wanting + caudate
  - Cross-unit: consonant music activates both liking + nacc

Science:
  - Salimpoor 2011: caudate (anticipation) → NAcc (consummation) shift
  - Berridge 2007: wanting (mesolimbic DA) vs liking (mu-opioid) dissociation
  - Gold 2023: VS crossover — anticipatory→consummatory transition (d=1.07)
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO,
    midi_note, midi_chord, midi_isochronous,
    midi_crescendo, midi_irregular_rhythm,
    major_triad, chromatic_cluster, dominant_seventh,
    C4 as MC4,
)
from Tests.micro_beliefs.assertions import assert_greater


class TestSRPInternalConsistency:
    """SRP tension and harmonic_tension should co-vary."""

    def test_tension_and_harmonic_tension_covary(self, runner):
        """Dissonant stimulus → both tension AND harmonic_tension above consonant.

        Koelsch 2013: harmonic tension is a component of overall musical tension.
        Both T0:tension and M0:harmonic_tension track dissonance.
        """
        beliefs = ["tension", "harmonic_tension"]

        res_diss = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            beliefs,
        )
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_diss[b], res_cons[b],
                f"cluster_{b}", f"major_{b}",
            )

    def test_prediction_error_and_match_inverse(self, runner):
        """Irregular → high PE, low match; Regular → low PE, high match.

        Cheung 2019: C2 PE driven by spectral/entropy surprise.
        Zatorre & Salimpoor 2013: T1 match driven by (1-C2) + onset periodicity.
        Tests relative ordering WITHIN each belief across stimuli.
        """
        beliefs = ["prediction_error", "prediction_match"]

        res_irreg = runner.run(
            midi_irregular_rhythm(MC4, 16, program=PIANO, velocity=80),
            beliefs,
        )
        res_reg = runner.run(
            midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=80),
            beliefs,
        )

        # Irregular → higher PE
        assert_greater(
            res_irreg["prediction_error"], res_reg["prediction_error"],
            "irregular_PE", "regular_PE",
        )
        # Regular → higher match
        assert_greater(
            res_reg["prediction_match"], res_irreg["prediction_match"],
            "regular_match", "irregular_match",
        )


class TestAnticipatoryCrossUnit:
    """SRP wanting × DAED da_caudate co-activation."""

    def test_energetic_activates_wanting_and_caudate(self, runner):
        """Loud fast beats → both wanting AND da_caudate above silence.

        Salimpoor 2011: caudate DA tracks anticipatory wanting.
        Both SRP wanting (P0) and DAED caudate track onset density + energy.
        """
        beliefs = ["wanting", "da_caudate"]
        res_fast = runner.run(
            midi_isochronous(MC4, 180.0, 18, program=PIANO, velocity=110),
            beliefs,
        )
        res_sil = runner.run(silence(5.0), beliefs)

        for b in beliefs:
            assert_greater(
                res_fast[b], res_sil[b],
                f"loud_fast_{b}", f"silence_{b}",
            )

    def test_crescendo_activates_wanting_and_caudate(self, runner):
        """Crescendo → both wanting AND da_caudate above quiet sustained.

        Building intensity drives both anticipatory pathways.
        """
        beliefs = ["wanting", "da_caudate"]
        res_cresc = runner.run(
            midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO),
            beliefs,
        )
        res_quiet = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=30),
            beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_cresc[b], res_quiet[b],
                f"crescendo_{b}", f"quiet_{b}",
            )


class TestConsummatoryCrossUnit:
    """SRP liking × DAED da_nacc co-activation."""

    def test_consonant_activates_liking_and_nacc(self, runner):
        """Consonant chord → both liking AND da_nacc above dissonant cluster.

        Salimpoor 2011: NAcc DA tracks consummatory pleasure.
        Both SRP liking (P1) and DAED NAcc track pleasantness + consonance.
        SRP sigmoid cascade elevates noise baselines; cluster is reliable floor.
        """
        beliefs = ["liking", "da_nacc"]
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            beliefs,
        )
        res_clust = runner.run(
            midi_chord(chromatic_cluster(MC4, 6), 5.0, program=PIANO, velocity=80),
            beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_cons[b], res_clust[b],
                f"major_{b}", f"cluster_{b}",
            )


class TestRewardPeakCrossUnit:
    """Peak detection × chills proximity co-activation at climax."""

    def test_crescendo_peaks_and_chills(self, runner):
        """Crescendo → both peak_detection AND chills_proximity above quiet.

        Salimpoor 2011: peak pleasure moments coincide with chills.
        Both M2:peak_detection and F1:chills_proximity track intensity peaks.
        """
        beliefs = ["peak_detection", "chills_proximity"]
        res_cresc = runner.run(
            midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO),
            beliefs,
        )
        res_quiet = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=40),
            beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_cresc[b], res_quiet[b],
                f"crescendo_{b}", f"quiet_{b}",
            )


class TestTensionResolutionCrossUnit:
    """Tension × resolution_expectation: dominant → high both."""

    def test_dominant_drives_tension_and_resolution(self, runner):
        """Dominant 7th → both tension AND resolution_expectation above tonic.

        Koelsch 2013: V7 creates tension with strong resolution expectancy.
        Dominant chord: tritone → tension; strong tonal pull → resolution expected.
        """
        from Tests.micro_beliefs.real_audio_stimuli import G3
        beliefs = ["tension", "resolution_expectation"]
        res_dom = runner.run(
            midi_chord(dominant_seventh(G3), 5.0, program=PIANO, velocity=80),
            beliefs,
        )
        res_ton = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            beliefs,
        )

        for b in beliefs:
            assert_greater(
                res_dom[b], res_ton[b],
                f"dominant_{b}", f"tonic_{b}",
            )
