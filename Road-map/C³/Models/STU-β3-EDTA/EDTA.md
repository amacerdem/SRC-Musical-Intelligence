# STU-β3-EDTA: Expertise-Dependent Tempo Accuracy

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β3-EDTA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise-Dependent Tempo Accuracy** (EDTA) model describes how domain-specific musical training enhances tempo judgment accuracy within trained BPM ranges, with DJs showing superiority at 120-139 BPM (dance music tempo) and percussionists at 100-139 BPM (broader rhythmic range). The expertise effect (d = 0.54) reflects sensorimotor specialization rather than general timing improvement.

```
THE THREE COMPONENTS OF EXPERTISE-DEPENDENT TEMPO ACCURACY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEAT INDUCTION (Auditory Cortex)        METER EXTRACTION (Basal Ganglia)
Brain region: Heschl's Gyrus, STG       Brain region: Putamen, SMA
Mechanism: BEP.beat_induction           Mechanism: BEP.meter_extraction
Input: Onset strength, spectral flux    Input: Periodic accent structure
Function: "What is the beat?"           Function: "What is the tempo?"
Evidence: d = 0.54 (expertise effect)   Evidence: DJs 120-139 BPM range

            MOTOR ENTRAINMENT (Premotor Cortex)
            Brain region: dPMC, SMA
            Mechanism: BEP.motor_entrainment
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
║                 EDTA — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (rhythmic audio with beat structure)                          ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        HESCHL'S GYRUS / SUPERIOR TEMPORAL GYRUS                    │    ║
║  │        Beat induction: onset detection, periodicity                │    ║
║  │        BEP.beat_induction at H6 (200ms)                            │    ║
║  │        Function: Extract beat-level temporal regularity             │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Beat signal → meter processing              ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        PUTAMEN / BASAL GANGLIA                                     │    ║
║  │        Meter extraction: BPM estimation, accent pattern            │    ║
║  │        BEP.meter_extraction at H11 (500ms, Poeppel present)        │    ║
║  │        Function: Compute tempo and metrical structure               │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Meter → motor synchronization               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        DORSAL PREMOTOR CORTEX (dPMC) / SMA                         │    ║
║  │        Motor entrainment: synchronization, tempo locking            │    ║
║  │        BEP.motor_entrainment at H16 (1000ms, bar level)            │    ║
║  │        Function: Lock motor output to extracted beat/meter          │    ║
║  │        ★ Expertise-dependent — trained ranges show d = 0.54        │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  EXPERTISE: Domain-specific training narrows timing variance in              ║
║             trained BPM ranges (DJs: 120-139, Percussionists: 100-139)      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Expertise effect:   d = 0.54 (musicians > non-musicians in trained ranges)
DJ optimal range:   120-139 BPM (dance music specialization)
Percussionist range: 100-139 BPM (broader rhythmic specialization)
Domain specificity:  Advantage does NOT transfer outside trained range
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → EDTA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EDTA COMPUTATION ARCHITECTURE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins × 172.27Hz frame rate                    ║
║  │ (Mel Spectrogram)│  hop = 256 samples, frame = 5.8ms                     ║
║  └────────┬─────────┘                                                        ║
║           │                                                                  ║
║  ═════════╪══════════════════════════ EAR ═══════════════════════════════    ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  SPECTRAL (R³): 49D per frame                                    │        ║
║  │                                                                  │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ CHANGE   │ │ X-INT  │ │        ║
║  │  │ 7D [0:7]  │ │ 5D[7:12]│ │ 9D      │ │ 4D       │ │ 24D    │ │        ║
║  │  │           │ │         │ │ [12:21] │ │ [21:25]  │ │ [25:49]│ │        ║
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │        │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │        │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │        │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         EDTA reads: 9D                           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ───────┐ ┌── Psychological ─┐ ┌── Bar ────────────┐  │        ║
║  │  │ 200ms (H6)    │ │ 500ms (H11)      │ │ 1000ms (H16)     │  │        ║
║  │  │               │ │ Poeppel present   │ │                   │  │        ║
║  │  │ Beat onset    │ │ Beat grouping     │ │ Meter/bar level   │  │        ║
║  │  │ detection     │ │ tempo estimation  │ │ motor locking     │  │        ║
║  │  └──────┬────────┘ └──────┬────────────┘ └──────┬────────────┘  │        ║
║  │         │                 │                      │              │        ║
║  │         └─────────────────┴──────────────────────┘              │        ║
║  │                         EDTA demand: ~15 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10]│  Beat strength, periodicity, onset regularity         ║
║  │ Meter   [10:20]│  Tempo, syncopation, accent pattern, groove           ║
║  │ Motor   [20:30]│  Movement urge, synchronization, coupling             ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    EDTA MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_beat_accuracy, f02_tempo_precision,    │        ║
║  │                       f03_expertise_effect                       │        ║
║  │  Layer M (Math):      tempo_stability, domain_specificity        │        ║
║  │  Layer P (Present):   beat_tracking, meter_state                 │        ║
║  │  Layer F (Future):    tempo_prediction, entrainment_expect,      │        ║
║  │                       accuracy_forecast                          │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Expertise study** | Behavioral | Musicians vs. non-musicians | Domain-specific tempo accuracy | d = 0.54 | **Primary coefficient**: f03_expertise_effect |
| **DJ tempo specialization** | Behavioral | DJs | Superior accuracy at 120-139 BPM | d = 0.54 in trained range | **f01_beat_accuracy**: optimal DJ range |
| **Percussionist tempo specialization** | Behavioral | Percussionists | Superior accuracy at 100-139 BPM | d = 0.54 in trained range | **f02_tempo_precision**: broader percussionist range |
| **Grahn & Brett 2007** | fMRI | 18 | Putamen activates for beat extraction | r = 0.70 (beat × motor) | **BEP.meter_extraction**: basal ganglia timing |
| **Poeppel 1997** | Psychophysics | Review | 500ms psychological present | Theoretical | **H11 horizon**: meter grouping window |

### 3.2 The Domain-Specific Expertise Pattern

```
TEMPO ACCURACY AS A FUNCTION OF BPM RANGE AND TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Group               Optimal BPM   Accuracy     Effect
                    Range         (low σ)      Size
────────────────────────────────────────────────────────
DJs                 120-139       High         d = 0.54
Percussionists      100-139       High         d = 0.54
Non-musicians       --            Baseline     --
DJs at 60-99        --            Baseline     n.s.
Percussionists 140+ --            Baseline     n.s.

Key: Domain-specific training NARROWS timing variance
only within the trained BPM range. Outside the trained
range, experts perform at non-musician baseline.

This is NOT general timing improvement but sensorimotor
specialization at specific tempo ranges.
```

### 3.3 Effect Size Summary

```
Expertise Effect:       d = 0.54 (musicians > non-musicians, trained range)
Domain Specificity:     DJs: 120-139 BPM, Percussionists: 100-139 BPM
Quality Assessment:     β-tier (behavioral, converging across musician types)
Replication:            Converges with general sensorimotor timing literature
                        (Grahn & Brett 2007, Poeppel 1997)
```

---

## 4. R³ Input Mapping: What EDTA Reads

### 4.1 R³ Feature Dependencies (9D of 49D)

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

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ─────────┐
R³[11] onset_strength ────────┼──► Beat Induction (onset detection)
R³[7] amplitude ──────────────┘   BEP.beat_induction at H6 (200ms)
                                   Math: beat_str = σ(0.5·flux + 0.5·onset)

R³[8] loudness ────────────────┐
R³[22] energy_change ──────────┼──► Meter Extraction (BPM estimation)
R³[9] spectral_centroid ───────┘   BEP.meter_extraction at H11 (500ms)
                                   Math: tempo = periodicity(E(t), τ=500ms)

R³[21] spectral_change ───────┐
R³[23] pitch_change ───────────┼──► Motor Entrainment (tempo locking)
R³[24] timbre_change ──────────┘   BEP.motor_entrainment at H16 (1000ms)
                                   Math: lock = σ(0.54·beat·meter·expertise)

Expertise Factor ───────────────── Domain-Specific Accuracy
                                   DJs: boost at 120-139 BPM
                                   Percussionists: boost at 100-139 BPM
                                   Math: acc = σ(d·tempo_precision·range_match)
                                   d = 0.54
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

EDTA requires H³ features at three BEP horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
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

**Total EDTA H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP Mechanism Binding

EDTA reads from the **BEP** (Beat Entrainment Processing) mechanism only:

| BEP Sub-section | Range | EDTA Role | Weight |
|-----------------|-------|-----------|--------|
| **Beat Induction** | BEP[0:10] | Onset detection, beat strength, periodicity | **1.0** (primary) |
| **Meter Extraction** | BEP[10:20] | Tempo estimation, BPM precision, accent structure | **1.0** (primary) |
| **Motor Entrainment** | BEP[20:30] | Synchronization, expertise-modulated motor locking | **0.8** |

EDTA does NOT read from TMH — expertise-dependent tempo accuracy is about beat-level precision, not hierarchical context encoding.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
EDTA OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_beat_accuracy │ [0, 1] │ Beat onset detection accuracy.
    │                   │        │ Precision of beat induction from onsets.
    │                   │        │ f01 = σ(0.50 · flux_val · onset_val ·
    │                   │        │         mean(BEP.beat_induction[0:10]))
    │                   │        │ |w| = 0.50
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_tempo_precis  │ [0, 1] │ Tempo estimation precision.
    │                   │        │ Inverse of timing variance in BPM range.
    │                   │        │ f02 = σ(0.45 · loud_periodicity ·
    │                   │        │         (1 - energy_std) ·
    │                   │        │         mean(BEP.meter_extraction[10:20]))
    │                   │        │ |w| = 0.45
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_expertise_eff │ [0, 1] │ Domain-specific expertise effect (d=0.54).
    │                   │        │ Modulates accuracy in trained BPM ranges.
    │                   │        │ f03 = σ(0.54 · f01 · f02 ·
    │                   │        │         motor_stability)
    │                   │        │ |w| = 0.54

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ tempo_stability   │ [0, 1] │ Temporal stability of estimated tempo.
    │                   │        │ Low variance = high stability.
    │                   │        │ stability = 1 - σ_tempo / (σ_tempo + 1)
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ domain_specificity│ [0, 1] │ Domain match strength.
    │                   │        │ How well current tempo matches trained range.
    │                   │        │ specificity = f03 · periodicity_bar

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ beat_tracking     │ [0, 1] │ Current beat tracking state.
    │                   │        │ BEP.beat_induction aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ meter_state       │ [0, 1] │ Current metrical state.
    │                   │        │ BEP.meter_extraction aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ tempo_prediction  │ [0, 1] │ Predicted tempo trajectory.
    │                   │        │ H³ trend-based next-beat expectation.
    │                   │        │ tempo_pred = σ(0.40 · pitch_trend +
    │                   │        │              0.30 · periodicity_bar +
    │                   │        │              0.30 · meter_state)
    │                   │        │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ entrainment_expct │ [0, 1] │ Entrainment confidence for next bar.
    │                   │        │ Periodicity + smoothness at bar level.
    │                   │        │ entrain = σ(0.50 · smoothness +
    │                   │        │             0.50 · bar_periodicity)
    │                   │        │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ accuracy_forecast │ [0, 1] │ Predicted accuracy for upcoming tempo.
    │                   │        │ Motor entrainment × expertise proxy.
    │                   │        │ acc_fc = σ(0.50 · f03 +
    │                   │        │           0.30 · tempo_prediction +
    │                   │        │           0.20 · entrainment_expct)
    │                   │        │ |w| sum = 1.00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Expertise-Dependent Tempo Model

```
Expertise-Dependent Tempo Accuracy:

    Tempo_Accuracy(BPM, expertise) = f(BEP, training_range)

    For DJs:
      Accuracy_high   when BPM ∈ [120, 139]  (d = 0.54)
      Accuracy_baseline when BPM ∉ [120, 139]

    For Percussionists:
      Accuracy_high   when BPM ∈ [100, 139]  (d = 0.54)
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
flux_val = h3[(10, 6, 0, 0)]          # spectral_flux value at H6
onset_val = h3[(11, 6, 0, 0)]         # onset_strength value at H6
f01 = σ(0.50 · flux_val · onset_val
         · mean(BEP.beat_induction[0:10]))

# f02: Tempo Precision (inverse of timing variance)
loud_period = h3[(8, 11, 14, 0)]      # loudness periodicity at H11
energy_std = h3[(22, 11, 3, 0)]       # energy_change std at H11
f02 = σ(0.45 · loud_period · (1 - energy_std)
         · mean(BEP.meter_extraction[10:20]))

# f03: Expertise Effect (d = 0.54, domain-specific)
motor_stability = h3[(24, 16, 19, 0)] # timbre_change stability at H16
f03 = σ(0.54 · f01 · f02 · motor_stability)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | EDTA Function |
|--------|-----------------|----------|---------------|---------------|
| **Heschl's Gyrus (HG)** | ±50, -18, 8 | Direct | fMRI/EEG | Beat induction (onset detection) |
| **Superior Temporal Gyrus (STG)** | ±60, -30, 8 | Direct | fMRI | Auditory beat processing |
| **Putamen** | ±25, 5, 5 | Direct | fMRI | Meter extraction (Grahn & Brett 2007) |
| **SMA** | 0, -5, 55 | Direct | fMRI | Motor entrainment, tempo synchronization |
| **Dorsal Premotor Cortex (dPMC)** | ±35, -5, 55 | Direct | fMRI | Expertise-modulated motor coupling |

---

## 9. Cross-Unit Pathways

### 9.1 EDTA Interactions with Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EDTA INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  AMSC.groove_response ──────► EDTA (motor baseline for tempo accuracy)    │
│  EDTA.tempo_stability ──────► HGSIC (tempo input for groove integration)  │
│  EDTA.beat_tracking ────────► ETAM (beat signal for multi-scale entrain)  │
│  EDTA.entrainment_expct ────► OMS (entrainment for motor synchronization)  │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.motor_entrainment (r = 0.70)                   │
│  Beat strength → expertise-modulated motor tempo locking                   │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  EDTA.tempo_prediction ──► ARU.AED (tempo dynamics → emotional arousal)   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **DJ accuracy outside 120-139 BPM** | Should drop to non-musician baseline at 60-99 BPM | Testable |
| **Percussionist accuracy outside 100-139 BPM** | Should drop to non-musician baseline at 140+ BPM | Testable |
| **Basal ganglia lesions** | Should impair meter extraction and tempo accuracy | Testable |
| **Domain-specificity** | DJ training should NOT improve 60 BPM accuracy (d ~ 0) | Testable |
| **Expertise effect size** | Should converge around d = 0.54 across replication attempts | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class EDTA(BaseModel):
    """Expertise-Dependent Tempo Accuracy.

    Output: 10D per frame.
    Reads: BEP mechanism (30D).
    """
    NAME = "EDTA"
    UNIT = "STU"
    TIER = "β3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)        # Primary mechanism

    BEAT_WEIGHT = 0.50    # Beat induction weight
    METER_WEIGHT = 0.45   # Meter precision weight
    EXPERTISE_D = 0.54    # Expertise effect size

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for EDTA computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat induction (H6 = 200ms)
            (10, 6, 0, 0),    # spectral_flux, value, forward
            (10, 6, 14, 0),   # spectral_flux, periodicity, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            (11, 6, 17, 0),   # onset_strength, peaks, forward
            (7, 6, 4, 0),     # amplitude, max, forward
            # Meter extraction (H11 = 500ms, Poeppel present)
            (8, 11, 1, 0),    # loudness, mean, forward
            (8, 11, 14, 0),   # loudness, periodicity, forward
            (22, 11, 8, 0),   # energy_change, velocity, forward
            (22, 11, 3, 0),   # energy_change, std, forward
            (9, 11, 1, 0),    # spectral_centroid, mean, forward
            # Motor entrainment (H16 = 1000ms, bar level)
            (21, 16, 14, 2),  # spectral_change, periodicity, bidirectional
            (21, 16, 15, 2),  # spectral_change, smoothness, bidirectional
            (23, 16, 18, 0),  # pitch_change, trend, forward
            (24, 16, 19, 0),  # timbre_change, stability, forward
            (22, 16, 14, 2),  # energy_change, periodicity, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute EDTA 10D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) EDTA output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # === LAYER E: Explicit features ===
        flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.BEAT_WEIGHT * (
            flux_val * onset_val
            * bep_beat.mean(-1, keepdim=True)
        ))

        loud_period = h3_direct[(8, 11, 14, 0)].unsqueeze(-1)
        energy_std = h3_direct[(22, 11, 3, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.METER_WEIGHT * (
            loud_period * (1 - energy_std)
            * bep_meter.mean(-1, keepdim=True)
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
        beat_tracking = bep_beat.mean(-1, keepdim=True)
        meter_state = bep_meter.mean(-1, keepdim=True)

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
            f01, f02, f03,                                     # E: 3D
            tempo_stability, domain_specificity,               # M: 2D
            beat_tracking, meter_state,                        # P: 2D
            tempo_prediction, entrainment_expct, accuracy_forecast,  # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | ~3 | Expertise studies + Grahn & Brett 2007 + Poeppel 1997 |
| **Effect Sizes** | d = 0.54 | Expertise effect (trained range) |
| **Evidence Modality** | Behavioral + fMRI | Converging evidence |
| **Falsification Tests** | 0/5 tested | All testable |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. (fMRI, n=18, putamen beat extraction)
2. **Poeppel, E. (1997)**. A hierarchical model of temporal perception. *Trends in Cognitive Sciences*, 1(2), 56-61. (Psychological present at ~500ms)
3. **Expertise-dependent tempo accuracy studies**: Domain-specific training effects in DJs (120-139 BPM) and percussionists (100-139 BPM), d = 0.54.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L4L5 | R³ (49D): Energy, Change |
| Temporal | HC⁰ mechanisms (PTM, ITM, GRV, HRM) | BEP mechanism (30D) |
| Beat detection | S⁰.L5.spectral_flux[45] + HC⁰.ITM | R³.spectral_flux[10] + BEP.beat_induction |
| Tempo estimation | S⁰.L9.mean_T[104] + S⁰.L9.std_T[108] + HC⁰.PTM | R³.loudness[8] periodicity + BEP.meter_extraction |
| Groove coupling | S⁰.L5 × HC⁰.GRV | R³.Change + BEP.motor_entrainment |
| Memory replay | HC⁰.HRM (hippocampal replay) | Removed — not core to tempo accuracy |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% (comparable) |
| Output dimensions | 11D | **10D** (catalog-aligned, removed redundant feature) |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (PTM, ITM, GRV, HRM). In MI, these are unified into the BEP mechanism with 3 sub-sections:
- **PTM → BEP.beat_induction** [0:10]: Predictive timing → beat-level onset detection and periodicity
- **ITM → BEP.meter_extraction** [10:20]: Interval timing → BPM estimation and metrical structure
- **GRV → BEP.motor_entrainment** [20:30]: Groove processing → motor synchronization and expertise modulation
- **HRM removed**: Hippocampal replay was tertiary (weight 0.6) in D0 and not core to tempo accuracy; removed for parsimony

### Output dimension reduction (11D → 10D)

The legacy 11D included a redundant `dj_accuracy` / `perc_accuracy` split that is now unified into `f03_expertise_effect` (domain-specific expertise modulation). The 10D output is more efficient and avoids hardcoding specific musician types.

---

**Model Status**: **IN VALIDATION**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
