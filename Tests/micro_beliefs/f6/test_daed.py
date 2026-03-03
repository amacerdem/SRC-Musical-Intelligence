"""Micro-belief tests — DAED relay (Dopamine Anticipation-Experience Dissociation).

5 beliefs tested:
  1. da_caudate          (Appraisal)    — caudate DA (anticipatory reward)
  2. da_nacc             (Appraisal)    — NAcc DA (consummatory reward)
  3. dissociation_index  (Appraisal)    — |anticipatory - consummatory| gap
  4. temporal_phase      (Appraisal)    — anticipatory/(anticipatory+consummatory)
  5. wanting_ramp        (Anticipation) — wanting trajectory / ramp-up

Mechanism: DAED (8D relay, Phase 0a)
Key R³ inputs: roughness[0], pleasantness[4], loudness[8],
               onset_strength[10], spectral_change[21], energy_change[22],
               coupling[25:33]
Key H³: loudness velocity at H16(1s), spectral entropy at H4(125ms),
         pleasantness mean at H16(1s), roughness velocity at H8(500ms)

Extraction formulas:
  f01 = σ(0.35×loud_vel_1s + 0.20×spec_entropy + 0.15×rough_vel)
  f02 = σ(0.35×pleas_mean_1s + 0.15×loud_mean_1s)
  f03 = wanting_index (anticipatory composite)
  f04 = liking_index (consummatory composite)
  dissociation = |f01 - f02|
  temporal_phase = f01 / (f01 + f02 + eps)
  caudate_activation = σ(0.35×f01 + 0.30×f03 + 0.20×energy_vel + 0.15×phase)
  nacc_activation = σ(0.35×f02 + 0.30×f04 + 0.20×pleas_trend + 0.15×coupling)

Science:
  - Salimpoor 2011: caudate r=0.71 (anticipatory), NAcc r=0.84 (consummatory), PET, N=8
  - Berridge 2007: wanting vs liking dissociation, NAcc opioid hotspot
  - Gold 2023: ventral striatum crossover d=1.07
  - Mohebi 2024: striatal DA gradient (VS tau=981s, DMS tau=414s)
"""
from __future__ import annotations

from Tests.micro_beliefs.audio_stimuli import noise, silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, STRINGS,
    midi_note, midi_chord, midi_isochronous,
    midi_crescendo,
    major_triad,
    C4 as MC4,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_halves, assert_stable, assert_in_range,
)


# =====================================================================
# 1. da_caudate (Appraisal)
# =====================================================================

class TestDaCaudate:
    """Caudate DA — anticipatory dopamine activation.

    observe = DAED[6] (caudate_activation)
    σ(0.35×f01 + 0.30×f03 + 0.20×energy_vel + 0.15×phase)
    High energy + onset density → high f01 → high caudate.

    Science: Salimpoor 2011 — caudate DA peaks BEFORE musical climax
    (anticipation phase, r=0.71, PET, N=8).
    """

    BELIEF = "da_caudate"

    def test_energetic_above_quiet(self, runner):
        """Loud fast beats >> quiet sustained note for caudate DA.

        Salimpoor 2011: caudate activation tracks energy buildup.
        Loud fast onsets → high f01 → high caudate.
        """
        res_high = runner.run(
            midi_isochronous(MC4, 180.0, 18, program=PIANO, velocity=110),
            [self.BELIEF],
        )[self.BELIEF]
        res_low = runner.run(
            midi_note(MC4, 5.0, program=PIANO, velocity=30),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_high, res_low, "loud_fast", "quiet_sustained")

    def test_crescendo_above_static(self, runner):
        """Crescendo >> static chord for caudate DA.

        Building intensity → rising energy_vel → higher caudate.
        """
        res_cresc = runner.run(
            midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO),
            [self.BELIEF],
        )[self.BELIEF]
        res_static = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=50),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cresc, res_static, "crescendo", "sustained_chord")

    def test_above_silence(self, runner):
        """Energetic beats >> silence for caudate DA."""
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=90),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_beats, res_sil, "beats", "silence")

    def test_stable(self, runner):
        """Sustained chord should be stable."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_isochronous(MC4, 120.0, 12),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 2. da_nacc (Appraisal)
# =====================================================================

class TestDaNacc:
    """NAcc DA — consummatory dopamine activation.

    observe = DAED[7] (nacc_activation)
    σ(0.35×f02 + 0.30×f04 + 0.20×pleas_trend + 0.15×coupling)
    f02 driven by pleasantness + loudness means → consonant = high.

    Science: Salimpoor 2011 — NAcc DA peaks AT musical climax
    (consummation phase, r=0.84, PET, N=8).
    """

    BELIEF = "da_nacc"

    def test_pleasant_above_noise(self, runner):
        """Consonant chord >> noise for NAcc DA.

        Salimpoor 2011: NAcc tracks consummatory pleasure.
        f02 = σ(0.35×pleas_mean_1s + ...) → consonant > noise.
        """
        res_cons = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_cons, res_noise, "major_chord", "noise")

    def test_warm_above_harsh(self, runner):
        """Warm organ chord >> harsh noise for NAcc DA.

        Warm timbre + consonance → high f02 → high NAcc.
        """
        res_warm = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        res_noise = runner.run(noise(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_warm, res_noise, "organ_chord", "noise")

    def test_above_silence(self, runner):
        """Musical content >> silence for NAcc DA."""
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "chord", "silence")

    def test_stable(self, runner):
        """Sustained chord should be stable."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_chord(major_triad(MC4), 4.0),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 3. dissociation_index (Appraisal)
# =====================================================================

class TestDissociationIndex:
    """Wanting-liking dissociation — |anticipatory - consummatory| gap.

    observe = DAED[4] (dissociation_index = |f01 - f02|)
    High when wanting ≠ liking: e.g. high energy but low consonance
    (high f01, low f02) or vice versa.

    Science: Berridge 2007 — wanting/liking dissociation in NAcc,
    mu-opioid vs mesolimbic DA pathways.
    """

    BELIEF = "dissociation_index"

    def test_crescendo_above_sustained_consonant(self, runner):
        """Crescendo (high energy, moderate pleasure) >> sustained organ
        (moderate energy, high pleasure) for dissociation.

        Crescendo: high f01 (loudness velocity), moderate f02 → gap.
        Sustained organ: moderate f01, moderate f02 → smaller gap.
        """
        res_cresc = runner.run(
            midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO),
            [self.BELIEF],
        )[self.BELIEF]
        res_sus = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_cresc, res_sus, "crescendo", "sustained_organ")

    def test_output_valid(self, runner):
        """Dissociation index produces valid output for musical input.

        |f01 - f02| should always be >= 0 and within bounds.
        """
        result = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        mn, mx = result.min().item(), result.max().item()
        assert mn >= -0.05, f"dissociation min={mn:.4f} below range"
        assert mx <= 1.05, f"dissociation max={mx:.4f} above range"

    def test_range(self, runner):
        for audio in [
            midi_crescendo(MC4, 12, 0.4, 20, 120),
            midi_chord(major_triad(MC4), 4.0, program=ORGAN),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 4. temporal_phase (Appraisal)
# =====================================================================

class TestTemporalPhase:
    """DA reward phase — f01/(f01+f02+eps), tracks anticipatory vs consummatory.

    observe = DAED[5] (temporal_phase)
    Ratio reflects which dopamine system dominates.
    f01 = anticipatory DA, f02 = consummatory DA.
    ~1.0 = pure anticipation (f01 >> f02, caudate dominant)
    ~0.5 = balanced transition state
    ~0.0 = pure consummation (f02 >> f01, NAcc dominant)

    Science: Salimpoor 2011 — caudate→NAcc temporal shift during music
    (anticipatory → consummatory transition, PET, N=8).
    Mohebi 2024 — striatal DA gradient (VS tau=981s, DMS tau=414s).
    """

    BELIEF = "temporal_phase"

    def test_output_valid(self, runner):
        """Temporal phase produces in-range, stable output for music.

        Phase is a ratio — should be bounded [0, 1].
        """
        result = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        mn, mx = result.min().item(), result.max().item()
        assert mn >= -0.05, f"phase min={mn:.4f} below range"
        assert mx <= 1.05, f"phase max={mx:.4f} above range"
        std = result[:, 50:].std().item()
        assert std < 0.15, f"phase std={std:.4f} too high"

    def test_above_silence(self, runner):
        """Musical content >> silence for temporal phase.

        Music should activate some phase output above silent baseline.
        """
        res_mus = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "chord", "silence")

    def test_stable_on_sustained(self, runner):
        """Sustained chord should produce stable phase."""
        result = runner.run(
            midi_chord(major_triad(MC4), 6.0, program=ORGAN, velocity=75),
            [self.BELIEF],
        )[self.BELIEF]
        assert_stable(result, self.BELIEF)

    def test_range(self, runner):
        for audio in [
            midi_isochronous(MC4, 120.0, 12),
            midi_chord(major_triad(MC4), 4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)


# =====================================================================
# 5. wanting_ramp (Anticipation)
# =====================================================================

class TestWantingRamp:
    """Wanting trajectory — tracks anticipatory wanting build-up.

    observe = DAED[2] (f03:wanting_index)
    Driven by anticipatory composite — onset density, energy velocity.

    Science: Berridge 2007 — wanting ramps up before reward delivery,
    distinct from liking which peaks at delivery.
    """

    BELIEF = "wanting_ramp"

    def test_rhythmic_above_static(self, runner):
        """Isochronous beats >> sustained chord for wanting ramp.

        Berridge 2007: rhythmic drive creates forward-wanting trajectory.
        Onsets → anticipatory activation → wanting ramp.
        """
        res_beats = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        res_static = runner.run(
            midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70),
            [self.BELIEF],
        )[self.BELIEF]
        assert_greater(res_beats, res_static, "isochronous", "sustained_chord")

    def test_crescendo_rising(self, runner):
        """Crescendo should show rising wanting ramp.

        Building amplitude → escalating anticipatory wanting.
        """
        audio = midi_crescendo(MC4, 16, 0.35, 20, 120, program=PIANO)
        result = runner.run(audio, [self.BELIEF])[self.BELIEF]
        assert_halves(result, self.BELIEF, direction="rising")

    def test_above_silence(self, runner):
        """Musical content >> silence for wanting ramp."""
        res_mus = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85),
            [self.BELIEF],
        )[self.BELIEF]
        res_sil = runner.run(silence(5.0), [self.BELIEF])[self.BELIEF]
        assert_greater(res_mus, res_sil, "beats", "silence")

    def test_range(self, runner):
        for audio in [
            midi_isochronous(MC4, 120.0, 12),
            silence(4.0),
        ]:
            result = runner.run(audio, [self.BELIEF])[self.BELIEF]
            assert_in_range(result, self.BELIEF)
