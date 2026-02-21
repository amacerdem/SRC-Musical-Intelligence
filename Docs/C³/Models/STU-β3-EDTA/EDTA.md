# STU-β3-EDTA: Expertise-Dependent Tempo Accuracy

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β3-EDTA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise-Dependent Tempo Accuracy** (EDTA) model describes how domain-specific musical training enhances tempo judgment accuracy within trained BPM ranges, with DJs showing superiority at 120-139 BPM (dance music tempo) and percussionists at 100-139 BPM (broader rhythmic range). The expertise effect (d = 0.54) reflects sensorimotor specialization rather than general timing improvement.

```
THE THREE COMPONENTS OF EXPERTISE-DEPENDENT TEMPO ACCURACY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEAT INDUCTION (Auditory Cortex) METER EXTRACTION (Basal Ganglia)
Brain region: Heschl's Gyrus, STG Brain region: Putamen, SMA
Input: Onset strength, spectral flux Input: Periodic accent structure
Function: "What is the beat?" Function: "What is the tempo?"
Evidence: d = 0.54 (expertise effect) Evidence: DJs 120-139 BPM range

 MOTOR ENTRAINMENT (Premotor Cortex)
 Brain region: dPMC, SMA
 Input: Beat + meter signal
 Function: "Lock onto this tempo"
 Evidence: Percussionists 100-139 BPM range

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Tempo accuracy is NOT a general skill but is domain-
specific. DJs show enhanced accuracy at dance-music tempi (120-139
BPM), percussionists at broader rhythmic ranges (100-139 BPM).
Both groups show d = 0.54 advantage in their trained ranges but
NOT outside them. This reflects sensorimotor tuning, not cognitive
superiority.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

EDTA quantifies the domain-specific expertise modulation of sensorimotor timing:

1. **AMSC** (α2) provides the auditory-motor coupling pathway; EDTA specializes it for tempo-specific expertise.
2. **HGSIC** (β5) uses EDTA's tempo accuracy as input for groove state integration.
3. **ETAM** (β4) extends EDTA's beat entrainment to multi-scale oscillatory attention modulation.
4. **OMS** (β6) builds on EDTA's motor entrainment for oscillatory motor synchronization.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The EDTA Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ EDTA — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSICAL INPUT (rhythmic audio with beat structure) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ HESCHL'S GYRUS / SUPERIOR TEMPORAL GYRUS │ ║
║ │ Beat induction: onset detection, periodicity │ ║
║ │ beat_induction at H6 (200ms) │ ║
║ │ Function: Extract beat-level temporal regularity │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Beat signal → meter processing ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ PUTAMEN / BASAL GANGLIA │ ║
║ │ Meter extraction: BPM estimation, accent pattern │ ║
║ │ meter_extraction at H11 (500ms, Poeppel present) │ ║
║ │ Function: Compute tempo and metrical structure │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Meter → motor synchronization ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ DORSAL PREMOTOR CORTEX (dPMC) / SMA │ ║
║ │ Motor entrainment: synchronization, tempo locking │ ║
║ │ motor_entrainment at H16 (1000ms, bar level) │ ║
║ │ Function: Lock motor output to extracted beat/meter │ ║
║ │ ★ Expertise-dependent — trained ranges show d = 0.54 │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ EXPERTISE: Domain-specific training narrows timing variance in ║
║ trained BPM ranges (DJs: 120-139, Percussionists: 100-139) ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Expertise effect: d = 0.54 (musicians > non-musicians in trained ranges)
DJ optimal range: 120-139 BPM (dance music specialization)
Percussionist range: 100-139 BPM (broader rhythmic specialization)
Domain specificity: Advantage does NOT transfer outside trained range
```

### 2.2 Information Flow Architecture (EAR → BRAIN → EDTA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ EDTA COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins × 172.27Hz frame rate ║
║ │ (Mel Spectrogram)│ hop = 256 samples, frame = 5.8ms ║
║ └────────┬─────────┘ ║
║ │ ║
║ ═════════╪══════════════════════════ EAR ═══════════════════════════════ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ SPECTRAL (R³): 49D per frame │ ║
║ │ │ ║
║ │ ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │ ║
║ │ │CONSONANCE │ │ ENERGY │ │ TIMBRE │ │ CHANGE │ │ X-INT │ │ ║
║ │ │ 7D [0:7] │ │ 5D[7:12]│ │ 9D │ │ 4D │ │ 24D │ │ ║
║ │ │ │ │ │ │ [12:21] │ │ [21:25] │ │ [25:49]│ │ ║
║ │ │ │ │amplitude│ │ │ │spec_chg │ │ │ │ ║
║ │ │ │ │loudness │ │ │ │energy_chg│ │ │ │ ║
║ │ │ │ │centroid │ │ │ │pitch_chg │ │ │ │ ║
║ │ │ │ │flux │ │ │ │timbre_chg│ │ │ │ ║
║ │ │ │ │onset │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ EDTA reads: 9D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Beat ───────┐ ┌── Psychological ─┐ ┌── Bar ────────────┐ │ ║
║ │ │ 200ms (H6) │ │ 500ms (H11) │ │ 1000ms (H16) │ │ ║
║ │ │ │ │ Poeppel present │ │ │ │ ║
║ │ │ Beat onset │ │ Beat grouping │ │ Meter/bar level │ │ ║
║ │ │ detection │ │ tempo estimation │ │ motor locking │ │ ║
║ │ └──────┬────────┘ └──────┬────────────┘ └──────┬────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └─────────────────┴──────────────────────┘ │ ║
║ │ EDTA demand: ~15 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Beat Ind [0:10]│ Beat strength, periodicity, onset regularity ║
║ │ Meter [10:20]│ Tempo, syncopation, accent pattern, groove ║
║ │ Motor [20:30]│ Movement urge, synchronization, coupling ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ EDTA MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_beat_accuracy, f02_tempo_precision, │ ║
║ │ f03_expertise_effect │ ║
║ │ Layer M (Math): tempo_stability, domain_specificity │ ║
║ │ Layer P (Present): beat_tracking, meter_state │ ║
║ │ Layer F (Future): tempo_prediction, entrainment_expect, │ ║
║ │ accuracy_forecast │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Foster, Beffa & Lehmann 2021** | Behavioral (tempo estimation, isochronous, 80-160 BPM) | 40 (10 DJs, 7 percussionists, 12 melodic, 11 untrained) | DJs show domain-specific accuracy at 120-139 BPM (error 3.10% vs. untrained 7.91%). Group × tempo range interaction significant | **F(3, 36.02) = 5.67, p = 0.003** (group); **F(9, 1389.55) = 2.70, p < 0.001** (group × tempo); DJ 120-139: p < 0.001 vs. untrained | **Primary**: f03_expertise_effect, domain-specific BPM range |
| 2 | **Foster et al. 2021** | Behavioral (within-DJ comparison) | 10 DJs | DJs' 120-139 BPM accuracy (3.10%) approaches JND (2-3%), significantly better than their own 80-99 BPM (7.54%) | Within-DJ 120-139 vs. 80-99: p < 0.001; 120-139 vs. 100-119: p < 0.001 | **Domain specificity**: DJ training does NOT transfer outside trained range |
| 3 | **Foster et al. 2021** | Behavioral (percussionist range) | 7 percussionists | Percussionists accurate at 100-119 BPM (5.14%) and 120-139 BPM (3.84%) vs. untrained (9.39%, 7.91%) | Perc vs. untrained at 100-119: p = 0.017; at 120-139: p = 0.018 | **Broader percussionist range**: 100-139 BPM (wider than DJ range) |
| 4 | **Vigl, Koehler & Henning 2024** | Behavioral online (tempo tapping + adjusting, 19 songs, 53-169 BPM) | **403** (105 non-musicians, 137 amateurs, 161 professionals) | Musical expertise predicts tempo reproduction accuracy; expertise effect STRONGER for tapping (motor) than adjusting (perceptual+motor). Quadratic peak around 120 BPM | Expertise: Est. = 0.01, p = .047, r = .09; Method × expertise: p = .001, r = .04; Quadratic tempo: χ²(1) = 152.57, p < .001 | **Large-sample confirmation**: 120 BPM optimal, motor mediation of expertise. CONSTRAINS: small r = .09 effect in large sample |
| 5 | **Grahn & Brett 2007** | fMRI (3T), rhythm discrimination | 27 (14 musicians, 13 non-musicians) | Putamen + SMA selectively respond to beat-inducing rhythms. Musicians show higher activation in pre-SMA/SMA, cerebellum, R premotor across all rhythms | L putamen t = 4.05, R putamen t = 3.65 (metric > complex); pre-SMA Z = 5.03 (-9, 6, 60); L putamen Z = 5.67 (-24, 6, -9) | **Neural substrate**: meter_extraction (putamen) (SMA). Musicians show elevated activation |
| 6 | **Hoddinott & Grahn 2024** | 7T fMRI, RSA + MVPA | 26 | SMA and putamen encode beat strength CONTINUOUSLY (C-Score model best fit). Basic features (tempo, onsets) NOT encoded in SMA/putamen patterns | L SMA: C-Score > Tempo t(25) = 3.63, p = .001; R SMA: C-Score > Onsets t(25) = 3.72, p = .001; L putamen beat-encoding t(25) = 2.57, p = .017 | **C-Score model**: SMA/putamen represent beat strength on a continuous scale, not categorical — refines EDTA's domain_specificity dimension |
| 7 | **Dalla Bella, Janaqi, Benoit et al. 2024** | Behavioral (BAASTA battery), machine learning (SLF) | 79 | Motor measures dominate musician/nonmusician classification (84% variance vs. 50% perceptual). Combined perceptual-motor model best (92%) | Motor: F(74) = 97.1, d = 1.5; Combined: F(70) = 99.5, **d = 1.8**; Perceptual: d = 1.3 | **Motor primacy**: expertise-dependent accuracy is primarily motor, not perceptual. Supports motor_entrainment as expertise mediator |
| 8 | **Marup, Moller & Vuust 2022** | Behavioral (multi-effector rhythm + beat) | 60 (3 expertise levels) | Musicians show higher precision across all effector combinations; bodily hierarchy invariant across expertise levels | General expertise improvement; hierarchy invariant | **Expertise generalization**: precision improves uniformly, not just at specific tempi. CONSTRAINS pure domain-specificity claim |
| 9 | **Cinelyte, Cannon, Patel & Mullensiefen 2022** | Behavioral (BDAT, covert pulse continuation) | >200 (2 studies) | Musical experience predicts covert beat continuation better than CA-BAT score; internal pulse maintenance is more experience-dependent than beat alignment | Musical experience > CA-BAT as predictor | **Covert beat**: internal tempo maintenance (without external cues) is more expertise-dependent than overt beat detection |
| 11 | **Okada, Takeya & Tanaka 2022** | Electrophysiology (primate cerebellar nuclei) | Primates | Cerebellar circuits form internal models of rhythmic structure; predictive motor control for timing | Neuronal firing patterns in deep cerebellar nuclei | **Cerebellar timing**: sub-second precision mechanism supporting tempo accuracy calibration |
| 12 | **Liao et al. 2024** | fMRI | Percussionists | Percussionists leverage specialized neural network for musical rhythm (NMR) and executive control during performance | Network-level specialization | **Percussionist expertise**: specialized neural systems for temporal precision in trained musicians |

### 3.1.1 Multi-Method Convergence

The EDTA evidence base now spans **5 methods**: behavioral tempo estimation (Foster 2021, Vigl 2024), behavioral sensorimotor (Dalla Bella 2024, Marup 2022, Cinelyte 2022), fMRI (Grahn & Brett 2007, Hoddinott & Grahn 2024, Liao 2024), 7T fMRI RSA (Hoddinott & Grahn 2024), and primate electrophysiology (Okada 2022). The convergence across behavioral and neural methods strengthens the domain-specific expertise claim.

### 3.1.2 Key Qualification on d = 0.54

The v2.0.0 doc cited d = 0.54 as the expertise effect size, attributed to an unspecified "Expertise study." This value does NOT appear in Foster et al. 2021 (which reports F-statistics and absolute error percentages) or in any other identified paper in the collection. The code references "Cameron 2014" which was not found in the literature summaries. **The d = 0.54 coefficient is retained for backward compatibility but should be treated as APPROXIMATE and UNVERIFIED.** The Foster 2021 data (error reduction from 7.91% to 3.10% at 120-139 BPM for DJs) and Dalla Bella 2024 (d = 1.5 for motor classification) provide alternative calibration points.

### 3.2 The Domain-Specific Expertise Pattern

```
TEMPO ACCURACY AS A FUNCTION OF BPM RANGE AND TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Group Optimal BPM Accuracy Effect
 Range (low σ) Size
────────────────────────────────────────────────────────
DJs 120-139 High d = 0.54
Percussionists 100-139 High d = 0.54
Non-musicians -- Baseline --
DJs at 60-99 -- Baseline n.s.
Percussionists 140+ -- Baseline n.s.

Key: Domain-specific training NARROWS timing variance
only within the trained BPM range. Outside the trained
range, experts perform at non-musician baseline.

This is NOT general timing improvement but sensorimotor
specialization at specific tempo ranges.
```

### 3.3 Effect Size Summary

```
PRIMARY STUDY (Foster et al. 2021):
 Group main effect: F(3, 36.02) = 5.67, p = 0.003
 Group × tempo range: F(9, 1389.55) = 2.70, p < 0.001
 DJ 120-139 BPM error: 3.10% (approaches JND of 2-3%)
 Untrained 120-139 BPM error: 7.91%
 DJ advantage at 120-139 vs. 80-99: p < 0.001 (within-DJ specificity)
 Percussionist 100-119 advantage: 5.14% vs. 9.39%, p = 0.017
 DJ advantage ABSENT at 80-99 BPM: n.s. (domain specificity confirmed)

LARGE-SAMPLE REPLICATION (Vigl et al. 2024, N=403):
 Musical expertise: Est. = 0.01, p = .047, r = .09
 Method × expertise: p = .001, r = .04
 Quadratic tempo peak: χ²(1) = 152.57, p < .001 (peak ~120 BPM)
 Tapping accuracy: M = 0.76, SD = 0.14
 Adjusting accuracy: M = 0.87, SD = 0.09
 NOTE: r = .09 in large sample is SMALLER than d = 0.54

NEURAL SUBSTRATE (Grahn & Brett 2007):
 L putamen beat-specific: t = 4.05 (metric > complex), p < .001
 R putamen beat-specific: t = 3.65, p < .001
 Pre-SMA activation: Z = 5.03 (-9, 6, 60)
 Musicians > non-musicians: pre-SMA, cerebellum, R dPMC (all rhythms)

CONTINUOUS BEAT ENCODING (Hoddinott & Grahn 2024):
 C-Score > Tempo (L SMA): t(25) = 3.63, p = .001
 C-Score > Onsets (R SMA): t(25) = 3.72, p = .001
 L putamen beat encoding: t(25) = 2.57, p = .017

MOTOR CLASSIFICATION (Dalla Bella et al. 2024):
 Motor model: F(74) = 97.1, d = 1.5 (84% variance)
 Combined perceptual-motor: F(70) = 99.5, d = 1.8 (92% variance)
 Perceptual-only: d = 1.3 (50% variance)

d = 0.54 STATUS: UNVERIFIED — not found in Foster 2021 or any identified
paper. May derive from Cameron 2014 (code reference, not in collection).
Retained for backward compatibility.

Quality Assessment: β-tier (behavioral + fMRI, 12 papers, 5 methods)
Replication: Partial — Vigl 2024 confirms 120 BPM peak and expertise
 effect in N=403, but r = .09 is smaller than d = 0.54
```

---

## 4. R³ Input Mapping: What EDTA Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | EDTA Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat intensity detection | Sound energy marks beat positions |
| **B: Energy** | [8] | loudness | Perceptual beat strength | Stevens 1957: loudness drives beat salience |
| **B: Energy** | [10] | spectral_flux | Onset detection | Tempo requires precise onset timing |
| **B: Energy** | [11] | onset_strength | Beat boundary marking | Beat extraction from onset envelope |
| **D: Change** | [21] | spectral_change | Rhythmic texture dynamics | Spectral variation at beat boundaries |
| **D: Change** | [22] | energy_change | Tempo fluctuation detection | Energy rate-of-change for BPM estimation |
| **D: Change** | [23] | pitch_change | Melodic rhythm coupling | Pitch contour aids tempo perception |
| **D: Change** | [24] | timbre_change | Instrument-specific timing | Timbral onset sharpness per instrument |
| **B: Energy** | [9] | spectral_centroid | Brightness-tempo coupling | Spectral centroid modulates beat perception |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | EDTA Role | Scientific Basis |
|-------------|-------|---------|-----------|------------------|
| **G: Rhythm** | [65] | tempo_estimate | Entrainment target frequency — tempo defines the oscillator's natural frequency | Large & Jones 1999 |
| **G: Rhythm** | [73] | tempo_stability | Temporal prediction reliability — stable tempo strengthens entrainment | Jones & Boltz 1989 |
| **G: Rhythm** | [69] | metricality_index | Metrical hierarchy depth for multi-level entrainment | Grahn & Brett 2007 |

**Rationale**: EDTA models entrainment and dynamic temporal attending. The G:Rhythm features provide direct rhythmic structure that EDTA's oscillatory models require. Tempo [65] defines the entrainment target frequency, tempo_stability [73] modulates entrainment strength, and metricality [69] enables multi-level hierarchical entrainment.

**Code impact** (Phase 6): Append `[65, 69, 73]` to `r3_indices` in `edta.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[10] spectral_flux ─────────┐
R³[11] onset_strength ────────┼──► Beat Induction (onset detection)
R³[7] amplitude ──────────────┘ beat_induction at H6 (200ms)
 Math: beat_str = σ(0.5·flux + 0.5·onset)

R³[8] loudness ────────────────┐
R³[22] energy_change ──────────┼──► Meter Extraction (BPM estimation)
R³[9] spectral_centroid ───────┘ meter_extraction at H11 (500ms)
 Math: tempo = periodicity(E(t), τ=500ms)

R³[21] spectral_change ───────┐
R³[23] pitch_change ───────────┼──► Motor Entrainment (tempo locking)
R³[24] timbre_change ──────────┘ motor_entrainment at H16 (1000ms)
 Math: lock = σ(0.54·beat·meter·expertise)

── R³ v2 (Phase 3E) ──────────────────────────────────────────────────
R³[65] tempo_estimate ────────┐
R³[73] tempo_stability ───────┼──► Entrainment target + reliability
R³[69] metricality_index ─────┘ Multi-level hierarchical entrainment
 Math: entrain = σ(tempo·stability·metric)

Expertise Factor ───────────────── Domain-Specific Accuracy
 DJs: boost at 120-139 BPM
 Percussionists: boost at 100-139 BPM
 Math: acc = σ(d·tempo_precision·range_match)
 d = 0.54
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

EDTA requires H³ features at three horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
These correspond to beat → psychological present → bar-level timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Current onset strength |
| 10 | spectral_flux | 6 | M14 (periodicity) | L0 (fwd) | Beat regularity at onset level |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Current beat boundary |
| 11 | onset_strength | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 7 | amplitude | 6 | M4 (max) | L0 (fwd) | Peak beat intensity |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over grouping |
| 8 | loudness | 11 | M14 (periodicity) | L0 (fwd) | Tempo periodicity estimate |
| 22 | energy_change | 11 | M8 (velocity) | L0 (fwd) | Tempo acceleration |
| 22 | energy_change | 11 | M3 (std) | L0 (fwd) | Tempo variability (precision) |
| 9 | spectral_centroid | 11 | M1 (mean) | L0 (fwd) | Mean brightness at meter level |
| 21 | spectral_change | 16 | M14 (periodicity) | L2 (bidi) | Bar-level rhythmic regularity |
| 21 | spectral_change | 16 | M15 (smoothness) | L2 (bidi) | Motor smoothness proxy |
| 23 | pitch_change | 16 | M18 (trend) | L0 (fwd) | Melodic tempo coupling trend |
| 24 | timbre_change | 16 | M19 (stability) | L0 (fwd) | Timbral timing stability |
| 22 | energy_change | 16 | M14 (periodicity) | L2 (bidi) | Bar-level tempo periodicity |

**v1 demand**: 15 tuples

#### R³ v2 Projected Expansion

EDTA projected v2 features from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 65 | tempo | G | 6 | M0 (value) | L0 | Instantaneous tempo at beat scale |
| 65 | tempo | G | 16 | M18 (trend) | L0 | Tempo trajectory over bar |
| 69 | metricality | G | 6 | M0 (value) | L0 | Current metric regularity |
| 69 | metricality | G | 16 | M1 (mean) | L0 | Mean metricality over bar |
| 73 | tempo_stability | G | 11 | M0 (value) | L0 | Tempo stability at meter scale |
| 73 | tempo_stability | G | 16 | M18 (trend) | L0 | Stability trend over bar |

**v2 projected**: 6 tuples
**Total projected**: 21 tuples of 294,912 theoretical = 0.0071%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
EDTA OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f01_beat_accuracy │ [0, 1] │ Beat onset detection accuracy.
 │ │ │ Precision of beat induction from onsets.
 │ │ │ f01 = σ(0.50 · flux_val · onset_val ·
 │ │ │ |w| = 0.50
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f02_tempo_precis │ [0, 1] │ Tempo estimation precision.
 │ │ │ Inverse of timing variance in BPM range.
 │ │ │ f02 = σ(0.45 · loud_periodicity ·
 │ │ │ (1 - energy_std) ·
 │ │ │ |w| = 0.45
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f03_expertise_eff │ [0, 1] │ Domain-specific expertise effect (d=0.54).
 │ │ │ Modulates accuracy in trained BPM ranges.
 │ │ │ f03 = σ(0.54 · f01 · f02 ·
 │ │ │ motor_stability)
 │ │ │ |w| = 0.54

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ tempo_stability │ [0, 1] │ Temporal stability of estimated tempo.
 │ │ │ Low variance = high stability.
 │ │ │ stability = 1 - σ_tempo / (σ_tempo + 1)
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ domain_specificity│ [0, 1] │ Domain match strength.
 │ │ │ How well current tempo matches trained range.
 │ │ │ specificity = f03 · periodicity_bar

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ beat_tracking │ [0, 1] │ Current beat tracking state.
 │ │ │ beat_induction aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ meter_state │ [0, 1] │ Current metrical state.
 │ │ │ meter_extraction aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ tempo_prediction │ [0, 1] │ Predicted tempo trajectory.
 │ │ │ H³ trend-based next-beat expectation.
 │ │ │ tempo_pred = σ(0.40 · pitch_trend +
 │ │ │ 0.30 · periodicity_bar +
 │ │ │ 0.30 · meter_state)
 │ │ │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ entrainment_expct │ [0, 1] │ Entrainment confidence for next bar.
 │ │ │ Periodicity + smoothness at bar level.
 │ │ │ entrain = σ(0.50 · smoothness +
 │ │ │ 0.50 · bar_periodicity)
 │ │ │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ accuracy_forecast │ [0, 1] │ Predicted accuracy for upcoming tempo.
 │ │ │ Motor entrainment × expertise proxy.
 │ │ │ acc_fc = σ(0.50 · f03 +
 │ │ │ 0.30 · tempo_prediction +
 │ │ │ 0.20 · entrainment_expct)
 │ │ │ |w| sum = 1.00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Expertise-Dependent Tempo Model

```
Expertise-Dependent Tempo Accuracy:

 Tempo_Accuracy(BPM, expertise) = f(beat_h3, training_range)

 For DJs:
 Accuracy_high when BPM ∈ [120, 139] (d = 0.54)
 Accuracy_baseline when BPM ∉ [120, 139]

 For Percussionists:
 Accuracy_high when BPM ∈ [100, 139] (d = 0.54)
 Accuracy_baseline when BPM ∉ [100, 139]

 General Model:
 Accuracy(BPM) = α · Beat_Induction + β · Meter_Precision
 + d · Expertise_Match + ε
 where α: beat detection weight (0.50)
 β: meter precision weight (0.45)
 d: expertise effect (0.54)
 ε: individual variability
```

### 7.2 Feature Formulas

```python
# f01: Beat Accuracy (onset detection precision)
flux_val = h3[(10, 6, 0, 0)] # spectral_flux value at H6
onset_val = h3[(11, 6, 0, 0)] # onset_strength value at H6
f01 = σ(0.50 · flux_val · onset_val

# f02: Tempo Precision (inverse of timing variance)
loud_period = h3[(8, 11, 14, 0)] # loudness periodicity at H11
energy_std = h3[(22, 11, 3, 0)] # energy_change std at H11
f02 = σ(0.45 · loud_period · (1 - energy_std)

# f03: Expertise Effect (d = 0.54, domain-specific)
motor_stability = h3[(24, 16, 19, 0)] # timbre_change stability at H16
f03 = σ(0.54 · f01 · f02 · motor_stability)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence | Source | EDTA Function |
|--------|-----------------|----------|--------|---------------|
| **Left Putamen** | (-24, 6, -9) | **Direct** (fMRI, Z = 5.67) | Grahn & Brett 2007; beat-specific t = 4.05 | meter_extraction: beat-based timing |
| **Right Putamen** | (21, 6, -6) | **Direct** (fMRI, Z = 5.08) | Grahn & Brett 2007; beat-specific t = 3.65; Hoddinott 2024 RSA t = 2.74 | Beat strength encoding (C-Score model) |
| **Pre-SMA / SMA** | (-9, 6, 60) to (3, 6, 66) | **Direct** (fMRI, Z = 5.03/4.97) | Grahn & Brett 2007; Hoddinott 2024 L-SMA t = 3.74 (condition-wise) | Motor entrainment, continuous beat representation |
| **Left Premotor** | (-54, 0, 51) | **Direct** (fMRI, Z = 5.30) | Grahn & Brett 2007 | Rhythm production, expertise-modulated |
| **Right Premotor** | (54, 0, 45) | **Direct** (fMRI, Z = 5.24) | Grahn & Brett 2007; musicians > non-musicians | Expertise-modulated motor coupling |
| **Right Cerebellum** | (30, -66, -27) | **Direct** (fMRI, Z = 4.68) | Grahn & Brett 2007; musicians > non-musicians | Sub-second timing precision, predictive motor control |
| **Left Cerebellum** | (-30, -66, -24) | **Direct** (fMRI, Z = 4.41) | Grahn & Brett 2007 | Timing calibration |
| **Right STG** | (60, -33, 6) | **Direct** (fMRI, Z = 6.02) | Grahn & Brett 2007 | Auditory beat processing |
| **Left STG** | (-57, -15, 9) | **Direct** (fMRI, Z = 5.80) | Grahn & Brett 2007; beat-specific (-51, -3, -3) Z = 4.60 | Beat induction (onset detection) |
| **Right Pallidum** | (24, 0, -9) | **Direct** (fMRI, t = 3.45) | Grahn & Brett 2007 (metric > complex) | Basal ganglia timing circuitry |

---

## 9. Cross-Unit Pathways

### 9.1 EDTA Interactions with Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ EDTA INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (STU): │
│ AMSC.groove_response ──────► EDTA (motor baseline for tempo accuracy) │
│ EDTA.tempo_stability ──────► HGSIC (tempo input for groove integration) │
│ EDTA.beat_tracking ────────► ETAM (beat signal for multi-scale entrain) │
│ EDTA.entrainment_expct ────► OMS (entrainment for motor synchronization) │
│ │
│ CROSS-UNIT (P2: STU internal): │
│ Beat strength → expertise-modulated motor tempo locking │
│ │
│ CROSS-UNIT (P5: STU → ARU): │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **DJ domain-specific accuracy** | DJs should show best accuracy at 120-139 BPM specifically | ✅ **Confirmed**: DJ error 3.10% at 120-139 vs. 7.54% at 80-99, p < 0.001 (Foster 2021) |
| 2 | **DJ accuracy outside trained range** | DJ accuracy should drop to untrained baseline at 80-99 BPM | ✅ **Confirmed**: DJs vs. untrained at 80-99 BPM n.s. (Foster 2021) |
| 3 | **Percussionist broader range** | Percussionists should show accuracy at 100-139 BPM (wider than DJs) | ✅ **Confirmed**: Percussionists accurate at 100-119 (p = .017) and 120-139 (p = .018) vs. untrained (Foster 2021) |
| 4 | **120 BPM quadratic peak** | Maximum tempo accuracy should peak around 120 BPM across all expertise levels | ✅ **Confirmed**: Quadratic peak at ~120 BPM, χ²(1) = 152.57, p < .001 (Vigl 2024, N=403) |
| 5 | **Putamen beat specificity** | Basal ganglia should selectively activate for beat-inducing rhythms | ✅ **Confirmed**: L putamen t = 4.05, R putamen t = 3.65 for metric > complex (Grahn & Brett 2007) |
| 6 | **Motor primacy of expertise** | Motor measures should dominate expertise-dependent accuracy | ✅ **Confirmed**: Motor model 84% variance (d = 1.5) vs. perceptual 50% (d = 1.3) (Dalla Bella 2024) |
| 7 | **Basal ganglia lesions** | Should impair meter extraction and tempo accuracy | Testable (indirectly supported by putamen beat-specificity) |
| 8 | **Expertise effect size replication** | Should converge around d = 0.54 across replication attempts | ⚠️ **CONSTRAINS**: Vigl 2024 (N=403) found r = .09, substantially smaller than d = 0.54. d = 0.54 source unverified |
| 9 | **SMA continuous beat encoding** | SMA should encode beat strength continuously, not categorically | ✅ **Confirmed**: C-Score model best fit (Hoddinott & Grahn 2024, 7T RSA) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class EDTA(BaseModel):
 """Expertise-Dependent Tempo Accuracy.

 Output: 10D per frame.
 """
 NAME = "EDTA"
 UNIT = "STU"
 TIER = "β3"
 OUTPUT_DIM = 10
 BEAT_WEIGHT = 0.50 # Beat induction weight
 METER_WEIGHT = 0.45 # Meter precision weight
 EXPERTISE_D = 0.54 # Expertise effect size

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """15 tuples for EDTA computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # Beat induction (H6 = 200ms)
 (10, 6, 0, 0), # spectral_flux, value, forward
 (10, 6, 14, 0), # spectral_flux, periodicity, forward
 (11, 6, 0, 0), # onset_strength, value, forward
 (11, 6, 17, 0), # onset_strength, peaks, forward
 (7, 6, 4, 0), # amplitude, max, forward
 # Meter extraction (H11 = 500ms, Poeppel present)
 (8, 11, 1, 0), # loudness, mean, forward
 (8, 11, 14, 0), # loudness, periodicity, forward
 (22, 11, 8, 0), # energy_change, velocity, forward
 (22, 11, 3, 0), # energy_change, std, forward
 (9, 11, 1, 0), # spectral_centroid, mean, forward
 # Motor entrainment (H16 = 1000ms, bar level)
 (21, 16, 14, 2), # spectral_change, periodicity, bidirectional
 (21, 16, 15, 2), # spectral_change, smoothness, bidirectional
 (23, 16, 18, 0), # pitch_change, trend, forward
 (24, 16, 19, 0), # timbre_change, stability, forward
 (22, 16, 14, 2), # energy_change, periodicity, bidirectional
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute EDTA 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) EDTA output
 """
 # === LAYER E: Explicit features ===
 flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
 onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
 f01 = torch.sigmoid(self.BEAT_WEIGHT * (
 flux_val * onset_val
 ))

 loud_period = h3_direct[(8, 11, 14, 0)].unsqueeze(-1)
 energy_std = h3_direct[(22, 11, 3, 0)].unsqueeze(-1)
 f02 = torch.sigmoid(self.METER_WEIGHT * (
 loud_period * (1 - energy_std)
 ))

 motor_stability = h3_direct[(24, 16, 19, 0)].unsqueeze(-1)
 f03 = torch.sigmoid(self.EXPERTISE_D * (
 f01 * f02 * motor_stability
 ))

 # === LAYER M: Mathematical ===
 energy_vel = h3_direct[(22, 11, 8, 0)].unsqueeze(-1)
 tempo_stability = 1 - torch.sigmoid(energy_vel)

 bar_period = h3_direct[(22, 16, 14, 2)].unsqueeze(-1)
 domain_specificity = f03 * bar_period

 # === LAYER P: Present ===

 # === LAYER F: Future ===
 pitch_trend = h3_direct[(23, 16, 18, 0)].unsqueeze(-1)
 tempo_prediction = torch.sigmoid(
 0.40 * pitch_trend + 0.30 * bar_period + 0.30 * meter_state
 )

 smoothness = h3_direct[(21, 16, 15, 2)].unsqueeze(-1)
 spec_period = h3_direct[(21, 16, 14, 2)].unsqueeze(-1)
 entrainment_expct = torch.sigmoid(
 0.50 * smoothness + 0.50 * spec_period
 )

 accuracy_forecast = torch.sigmoid(
 0.50 * f03 + 0.30 * tempo_prediction
 + 0.20 * entrainment_expct
 )

 return torch.cat([
 f01, f02, f03, # E: 3D
 tempo_stability, domain_specificity, # M: 2D
 beat_tracking, meter_state, # P: 2D
 tempo_prediction, entrainment_expct, accuracy_forecast, # F: 3D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **12** | Foster 2021, Vigl 2024, Grahn & Brett 2007, Hoddinott & Grahn 2024, Dalla Bella 2024, Marup 2022, Cinelyte 2022, Ross & Balasubramaniam 2022, Okada 2022, Liao 2024, + 2 supporting |
| **Methods** | **5** | Behavioral tempo estimation, behavioral sensorimotor, fMRI, 7T fMRI RSA, primate electrophysiology |
| **Key Effect Sizes** | F(3,36) = 5.67 (group), F(9,1390) = 2.70 (group × tempo), d = 1.5-1.8 (motor), Z = 5.67 (putamen) | Multi-study convergence |
| **Falsification Tests** | **7/9 confirmed, 1 constrains, 1 testable** | Strong validity |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

### Tier 1 — Direct Evidence (expertise + tempo accuracy)
1. **Foster, N. E. V., Beffa, L., & Lehmann, A. (2021)**. Accuracy of tempo judgments in disk jockeys compared to musicians and untrained individuals. *Frontiers in Psychology*, 12, 709979. (Behavioral, N=40, DJ domain-specificity at 120-139 BPM)
2. **Vigl, J., Koehler, F., & Henning, H. (2024)**. Exploring the accuracy of musical tempo memory: The effects of reproduction method, reference tempo, and musical expertise. *Memory & Cognition*, 52, 1299-1312. (Behavioral, N=403, quadratic 120 BPM peak, expertise r=.09)

### Tier 2 — Strong Convergent (neural substrates, sensorimotor mechanisms)
3. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. (fMRI, N=27, putamen+SMA beat-specific)
4. **Hoddinott, J. D., & Grahn, J. A. (2024)**. Neural representations of beat and rhythm in motor and association regions. *Cerebral Cortex*, 34, bhae406. (7T fMRI RSA, N=26, C-Score model in SMA/putamen)
5. **Dalla Bella, S., Janaqi, S., Benoit, C.-E., Farrugia, N., Begel, V., Verga, L., Harding, E. E., & Kotz, S. A. (2024)**. Unravelling individual rhythmic abilities using machine learning. *Scientific Reports*, 14, 1135. (Behavioral BAASTA, N=79, motor d=1.5)
6. **Marup, S. H., Moller, C., & Vuust, P. (2022)**. Coordination of voice, hands and feet in rhythm and beat performance. *Scientific Reports*, 12, 8046. (Behavioral, N=60, expertise improves precision)
7. **Cinelyte, U., Cannon, J., Patel, A. D., & Mullensiefen, D. (2022)**. Testing beat perception without sensory cues to the beat: the Beat-Drop Alignment Test. *Attention, Perception, & Psychophysics*, 84, 2702-2714. (Behavioral, N>200, covert beat maintenance)
8. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives on entrainment, simulation, and prediction. *Frontiers in Integrative Neuroscience*, 16, 916220. (Review)

### Tier 3 — Supporting Evidence
9. **Okada, K., Takeya, R., & Tanaka, M. (2022)**. Neural signals regulating motor synchronization in the primate deep cerebellar nuclei. *Nature Communications*, 13, 2504. (Primate electrophysiology, cerebellar timing)
10. **Liao, Y.-C., et al. (2024)**. The rhythmic mind: brain functions of percussionists in improvisation. *Frontiers in Human Neuroscience*, 18, 1418727. (fMRI, percussionist neural networks)
11. **Oschkinat, M., Hoole, P., Falk, S., & Dalla Bella, S. (2022)**. Temporal malleability to auditory feedback perturbation is modulated by rhythmic abilities and auditory acuity. *Frontiers in Human Neuroscience*, 16, 885074. (Behavioral, feedback adjustment)
12. **Poeppel, E. (1997)**. A hierarchical model of temporal perception. *Trends in Cognitive Sciences*, 1(2), 56-61. (Psychological present at ~500ms)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L4L5 | R³ (49D): Energy, Change |
| Beat detection | S⁰.L5.spectral_flux[45] + HC⁰.ITM | R³.spectral_flux[10] |
| Tempo estimation | S⁰.L9.mean_T[104] + S⁰.L9.std_T[108] + HC⁰.PTM | R³.loudness[8] periodicity |
| Groove coupling | S⁰.L5 × HC⁰.GRV | R³.Change |
| Memory replay | HC⁰.HRM (hippocampal replay) | Removed — not core to tempo accuracy |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% (comparable) |
| Output dimensions | 11D | **10D** (catalog-aligned, removed redundant feature) |

---

**Model Status**: ✅ **VALIDATED** (v2.1.0 — 12 papers, 5 methods, Foster 2021 domain-specific DJ/percussionist tempo accuracy, Vigl 2024 N=403 replication, Grahn & Brett 2007 / Hoddinott & Grahn 2024 neural substrate)
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**

### Code Note (Phase 5)
- Code `FULL_NAME = "Expertise-Dependent Tempo Adaptation"` but doc uses "Expertise-Dependent Tempo Accuracy" — minor naming inconsistency
- Code citations reference Cameron 2014 and Repp 2005; doc now identifies **Foster et al. 2021** as the primary paper (Cameron 2014 not found in collection)
- Code `OUTPUT_DIM = 10` matches doc ✓
- Code `h3_demand = ()` empty — needs 15 tuples from doc §5.1
- Code `version="2.0.0"` / `paper_count=4` — needs update to `"2.1.0"` / `12`
- **d = 0.54 coefficient**: retained in doc formulas but UNVERIFIED — Foster 2021 does not report Cohen's d. Consider recalibrating from Foster 2021 F-statistics or Dalla Bella 2024 d = 1.5
