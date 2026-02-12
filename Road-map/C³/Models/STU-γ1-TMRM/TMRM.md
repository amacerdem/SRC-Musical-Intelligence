# STU-γ1-TMRM: Tempo Memory Reproduction Method

**Model**: Tempo Memory Reproduction Method
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ1-TMRM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Tempo Memory Reproduction Method** (TMRM) model describes how tempo memory accuracy depends on the reproduction method: sensory feedback (adjusting a tempo slider) produces dramatically better accuracy than motor reproduction (tapping), with an optimal internal tempo reference around 120 BPM (500 ms IOI). Musical expertise further enhances reproduction precision.

```
THE THREE COMPONENTS OF TEMPO MEMORY REPRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SENSORY REPRODUCTION (Adjusting)       MOTOR REPRODUCTION (Tapping)
Method: Tempo slider / dial            Method: Finger/hand tapping
Brain region: SMA + Auditory Cortex    Brain region: Cerebellum + Premotor
Mechanism: BEP.beat_induction          Mechanism: BEP.motor_entrainment
Advantage: d = 2.76 over tapping       Baseline: motor-only reproduction
Function: "Match what I hear"          Function: "Produce the beat"

              OPTIMAL TEMPO (Internal Reference)
              Value: 120 BPM (500 ms IOI)
              Shape: Quadratic optimum
              Function: "Internal tempo template"
              Evidence: d = 0.58 (quadratic fit)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Sensory support during recall (adjusting) dramatically
outperforms motor-only reproduction (tapping) at d = 2.76. This
dissociation reveals two distinct pathways: an auditory-sensory route
(SMA + auditory cortex) and a motor-cerebellar route. Both converge
on an internal 120 BPM reference template. Musical expertise enhances
precision across both methods (d = 0.59).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

TMRM reveals the method-dependent nature of tempo memory retrieval:

1. **AMSC** (α2) provides the auditory-motor coupling; TMRM shows that the sensory arm of this coupling dominates tempo recall.
2. **HMCE** (α1) provides temporal context hierarchy; TMRM uses context encoding to anchor the internal 120 BPM reference.
3. **HGSIC** (β5) models groove from optimal complexity; TMRM's optimal tempo (120 BPM) aligns with peak groove zones.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The TMRM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 TMRM — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (rhythmic, tempo-bearing sequences)                           ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        SUPPLEMENTARY MOTOR AREA (SMA)                               │    ║
║  │        Internal tempo representation, beat anticipation             │    ║
║  │        Optimal: 120 BPM (500 ms IOI)                               │    ║
║  │        ★ Adjusting method: sensory feedback loop via SMA            │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                    ┌─────────┴──────────┐                                    ║
║                    ▼                    ▼                                     ║
║  ┌──────────────────────┐   ┌──────────────────────┐                        ║
║  │  AUDITORY CORTEX     │   │  CEREBELLUM          │                        ║
║  │  Sensory pathway     │   │  Motor pathway       │                        ║
║  │  Adjusting method    │   │  Tapping method      │                        ║
║  │  d = 2.76 advantage  │   │  Baseline accuracy   │                        ║
║  │  (tempo slider)      │   │  (finger tapping)    │                        ║
║  └──────────┬───────────┘   └──────────┬───────────┘                        ║
║             │                          │                                     ║
║             └──────────┬───────────────┘                                     ║
║                        ▼                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        PREMOTOR CORTEX                                              │    ║
║  │        Motor planning, reproduction execution                       │    ║
║  │        Expertise effect: d = 0.59 (musicians > non-musicians)       │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  DISSOCIATION: Adjusting (sensory) vs Tapping (motor), d = 2.76           ║
║  OPTIMAL: 120 BPM quadratic peak (d = 0.58)                               ║
║  EXPERTISE: Musicians > non-musicians (d = 0.59)                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Levitin & Cook 1996:  Adjusting > tapping, d = 2.76 (n = 46)
Levitin & Cook 1996:  120 BPM optimal tempo, quadratic (d = 0.58)
Drake & Botte 1993:   Expertise improves tempo precision, d = 0.59
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → TMRM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TMRM COMPUTATION ARCHITECTURE                             ║
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
║  │                         TMRM reads: 9D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ────────┐ ┌── Psy Present ──┐ ┌── Bar ─────────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 500ms (H11)     │ │ 1000ms (H16)      │ │        ║
║  │  │                │ │                  │ │                    │ │        ║
║  │  │ Single beat    │ │ Psychological    │ │ Bar-level meter   │ │        ║
║  │  │ (120–300 BPM)  │ │ present window   │ │ integration       │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬─────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         TMRM demand: 15 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10]│  Beat strength, tempo, phase, regularity              ║
║  │ Meter    [10:20]│  Meter, syncopation, accent pattern, groove          ║
║  │ Motor    [20:30]│  Movement urge, sync precision, coupling             ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    TMRM MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_adjusting_advantage,                   │        ║
║  │                       f02_optimal_tempo, f03_expertise_accuracy  │        ║
║  │  Layer M (Math):      method_dissociation, tempo_deviation       │        ║
║  │  Layer P (Present):   sensory_state, motor_state                 │        ║
║  │  Layer F (Future):    tempo_prediction, method_confidence,       │        ║
║  │                       reproduction_accuracy                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Levitin & Cook 1996** | Behavioral | 46 | Adjusting > tapping for tempo accuracy | d = 2.76 | **Primary coefficient**: f01_adjusting_advantage |
| **Levitin & Cook 1996** | Behavioral | 46 | 120 BPM optimal (quadratic peak) | d = 0.58 | **f02_optimal_tempo**: quadratic optimum |
| **Drake & Botte 1993** | Behavioral | 24 | Musicians > non-musicians in tempo precision | d = 0.59 | **f03_expertise_accuracy**: training effect |
| **Drake & Botte 1993** | Behavioral | 24 | Method dissociation: adjusting vs tapping | Qualitative | **method_dissociation**: pathway separation |

### 3.2 The Sensory Support Advantage

```
TEMPO REPRODUCTION ACCURACY BY METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method         Mechanism      Accuracy     Effect vs Tapping
───────────────────────────────────────────────────────────────
Adjusting      Sensory        Higher       d = 2.76 (huge)
Tapping        Motor          Lower        baseline

The sensory support advantage (d = 2.76) is among the largest
effect sizes in music cognition, suggesting fundamentally
different neural pathways:

Adjusting: SMA + Auditory Cortex → Sensory feedback loop
   - Listener matches perceived tempo against internal template
   - Continuous perceptual comparison
   - Exploits beat induction from BEP

Tapping: Cerebellum + Premotor → Motor-only reproduction
   - Relies on interval timing without sensory correction
   - Discrete motor output, no perceptual feedback
   - Exploits motor entrainment from BEP

Optimal tempo: 120 BPM (500 ms IOI)
   - Quadratic accuracy peak (d = 0.58)
   - Aligns with preferred spontaneous motor tempo
   - Within BEP H11 (500 ms) psychological present window
```

### 3.3 Effect Size Summary

```
Adjusting > Tapping:   d = 2.76 (Levitin & Cook 1996, behavioral)
Optimal Tempo:         d = 0.58 (quadratic peak at 120 BPM)
Expertise Effect:      d = 0.59 (Drake & Botte 1993, musicians > non-musicians)
Quality Assessment:    γ-tier (behavioral only, no neural imaging)
Replication:           Limited — key studies from 1990s, few direct replications
```

---

## 4. R³ Input Mapping: What TMRM Reads

### 4.1 R³ Feature Dependencies (9D of 49D)

| R³ Group | Index | Feature | TMRM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat intensity dynamics | Sound energy as tempo cue |
| **B: Energy** | [8] | loudness | Perceptual intensity for sensory pathway | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid | Timbral brightness anchoring tempo | Spectral balance |
| **B: Energy** | [10] | spectral_flux | Onset/beat transition detection | Beat boundary marker |
| **B: Energy** | [11] | onset_strength | Beat event marking precision | Onset clarity |
| **D: Change** | [21] | spectral_change | Tempo-correlated spectral dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Rhythmic energy dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour supporting tempo | Pitch rate of change |
| **D: Change** | [24] | timbre_change | Instrument identity dynamics | Timbral change rate |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[8] loudness ─────────────────┐
R³[10] spectral_flux ───────────┼──► Sensory Pathway (Adjusting Method)
R³[11] onset_strength ──────────┘   BEP.beat_induction at H6 (200ms)
                                    Math: S_adjust = σ(w · loud · flux · onset
                                                        · BEP.beat_induction)
                                    d = 2.76 advantage over motor

R³[7] amplitude ────────────────┐
R³[22] energy_change ───────────┼──► Motor Pathway (Tapping Method)
R³[21] spectral_change ─────────┘   BEP.motor_entrainment at H11 (500ms)
                                    Math: M_tap = σ(w · amp · energy_chg
                                                     · BEP.motor_entrainment)
                                    Baseline reproduction

R³[8] loudness ─────────────────┐
R³[9] spectral_centroid ────────┼──► Optimal Tempo Reference (120 BPM)
                                    BEP.meter_extraction at H16 (1000ms)
                                    Math: T_opt = 1 − (tempo − 120)² / k
                                    Quadratic peak at 500 ms IOI

R³[23] pitch_change ────────────┐
R³[24] timbre_change ───────────┼──► Expertise Modulation
                                    Finer feature discrimination
                                    d = 0.59 expertise effect
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

TMRM requires H³ features at three BEP horizons: H6 (200ms beat), H11 (500ms psychological present), H16 (1000ms bar).
These correspond to single-beat → tempo reference → bar-level timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 8 | loudness | 6 | M4 (max) | L0 (fwd) | Beat peak loudness |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat onset count per window |
| 11 | onset_strength | 6 | M4 (max) | L0 (fwd) | Strongest onset in beat window |
| 8 | loudness | 11 | M14 (periodicity) | L0 (fwd) | Tempo regularity at 500ms |
| 8 | loudness | 11 | M15 (smoothness) | L0 (fwd) | Smoothness of beat pattern |
| 10 | spectral_flux | 11 | M14 (periodicity) | L0 (fwd) | Beat periodicity (tempo proxy) |
| 22 | energy_change | 11 | M8 (velocity) | L0 (fwd) | Rhythmic energy dynamics |
| 22 | energy_change | 11 | M14 (periodicity) | L0 (fwd) | Energy periodicity |
| 7 | amplitude | 11 | M4 (max) | L0 (fwd) | Peak amplitude at tempo scale |
| 7 | amplitude | 16 | M18 (trend) | L0 (fwd) | Bar-level intensity trend |
| 8 | loudness | 16 | M14 (periodicity) | L0 (fwd) | Bar-level periodicity |
| 8 | loudness | 16 | M18 (trend) | L0 (fwd) | Loudness trajectory over bar |
| 21 | spectral_change | 16 | M8 (velocity) | L0 (fwd) | Spectral change rate at bar |
| 22 | energy_change | 16 | M15 (smoothness) | L0 (fwd) | Energy smoothness at bar level |
| 11 | onset_strength | 16 | M17 (peaks) | L0 (fwd) | Beat count per bar |

**Total TMRM H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP Mechanism Binding

TMRM reads from the **BEP** (Beat Entrainment Processing) mechanism:

| BEP Sub-section | Range | TMRM Role | Weight |
|-----------------|-------|-----------|--------|
| **Beat Induction** | BEP[0:10] | Sensory pathway — beat strength, tempo extraction | **1.0** (primary) |
| **Meter Extraction** | BEP[10:20] | Optimal tempo — meter, groove, accent pattern | **0.8** |
| **Motor Entrainment** | BEP[20:30] | Motor pathway — tapping reproduction baseline | **0.7** |

TMRM does NOT read from TMH — tempo memory reproduction is about beat-level entrainment and motor synchronization, not hierarchical context encoding.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
TMRM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: STU TMRM [199:209]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_adjusting_adv   │ [0, 1] │ Sensory support advantage (d = 2.76).
    │                     │        │ Adjusting > tapping for tempo accuracy.
    │                     │        │ f01 = σ(0.35 · loud_peak · flux_period
    │                     │        │         · BEP.beat_induction_mean)
    │                     │        │ Coefficients: |0.35| ≤ 1.0 ✓
────┼─────────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_optimal_tempo   │ [0, 1] │ 120 BPM quadratic optimum (d = 0.58).
    │                     │        │ Internal reference at 500 ms IOI.
    │                     │        │ f02 = σ(0.30 · period_loud · period_flux
    │                     │        │         · BEP.meter_extraction_mean)
    │                     │        │ Coefficients: |0.30| ≤ 1.0 ✓
────┼─────────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_expertise_acc   │ [0, 1] │ Musicians > non-musicians (d = 0.59).
    │                     │        │ Expertise enhances reproduction precision.
    │                     │        │ f03 = σ(0.30 · smooth_energy · f01 · f02)
    │                     │        │ Coefficients: |0.30| ≤ 1.0 ✓

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 3  │ method_dissociation │ [0, 1] │ Adjusting − tapping pathway difference.
    │                     │        │ High = sensory dominates, low = motor.
    │                     │        │ dissoc = σ(f01 − motor_state)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 4  │ tempo_deviation     │ [0, 1] │ Distance from optimal 120 BPM.
    │                     │        │ 0 = at optimum, 1 = far from 120 BPM.
    │                     │        │ dev = 1 − f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 5  │ sensory_state       │ [0, 1] │ Sensory pathway activation (SMA + auditory).
    │                     │        │ BEP.beat_induction aggregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 6  │ motor_state         │ [0, 1] │ Motor pathway activation (cerebellum + premotor).
    │                     │        │ BEP.motor_entrainment aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 7  │ tempo_prediction    │ [0, 1] │ Predicted next-beat tempo stability.
    │                     │        │ Periodicity + trend-based expectation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 8  │ method_confidence   │ [0, 1] │ Confidence in current reproduction method.
    │                     │        │ Smoothness × regularity at bar level.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 9  │ reproduction_acc    │ [0, 1] │ Expected reproduction accuracy.
    │                     │        │ Combines sensory + motor + expertise.
    │                     │        │ acc = σ(0.40 · f01 + 0.30 · f02
    │                     │        │         + 0.30 · f03)
    │                     │        │ Coefficients: |0.40+0.30+0.30| = 1.0 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Method Dissociation Model

```
Tempo Memory Reproduction:

    Adjusting (sensory):
      Accuracy_adjust = f(sensory_feedback, internal_template)
      Brain: SMA + Auditory Cortex
      Advantage: d = 2.76 over tapping

    Tapping (motor):
      Accuracy_tap = f(motor_timing, interval_reproduction)
      Brain: Cerebellum + Premotor Cortex
      Baseline accuracy

    Optimal Tempo:
      Accuracy(BPM) = A_max · exp(−(BPM − 120)² / (2σ²))
      Peak at 120 BPM (500 ms IOI), σ ≈ 40 BPM
      d = 0.58 quadratic fit

    Expertise Modulation:
      Accuracy_expert = Accuracy_base · (1 + d_exp · expertise)
      d_exp = 0.59 (Drake & Botte 1993)
```

### 7.2 Feature Formulas

```python
# f01: Adjusting Advantage (sensory support, d = 2.76)
loud_peak = h3[(8, 6, 4, 0)]         # loudness max at H6
flux_period = h3[(10, 11, 14, 0)]    # spectral_flux periodicity at H11
f01 = σ(0.35 · loud_peak · flux_period
         · mean(BEP.beat_induction[0:10]))
# Coefficient check: |0.35| ≤ 1.0 ✓

# f02: Optimal Tempo (120 BPM quadratic peak, d = 0.58)
period_loud = h3[(8, 11, 14, 0)]     # loudness periodicity at H11
period_flux = h3[(10, 6, 17, 0)]     # spectral_flux peaks at H6
f02 = σ(0.30 · period_loud · period_flux
         · mean(BEP.meter_extraction[10:20]))
# Coefficient check: |0.30| ≤ 1.0 ✓

# f03: Expertise Accuracy (d = 0.59)
smooth_energy = h3[(22, 16, 15, 0)]  # energy_change smoothness at H16
f03 = σ(0.30 · smooth_energy · f01 · f02)
# Coefficient check: |0.30| ≤ 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | TMRM Function |
|--------|-----------------|----------|---------------|---------------|
| **SMA** | 0, -5, 55 | Primary | fMRI/behavioral | Internal tempo representation, beat anticipation |
| **Cerebellum** | ±25, -60, -30 | Primary | fMRI/behavioral | Motor timing, tapping pathway |
| **Premotor Cortex** | ±45, 0, 45 | Secondary | fMRI | Motor planning, reproduction execution |
| **Auditory Cortex** | ±55, -20, 8 | Secondary | Behavioral inference | Sensory feedback loop (adjusting) |

---

## 9. Cross-Unit Pathways

### 9.1 TMRM Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TMRM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  TMRM.sensory_state ────────► AMSC (sensory pathway feeds motor coupling) │
│  TMRM.motor_state ──────────► EDTA (motor baseline for tempo accuracy)    │
│  TMRM.optimal_tempo ────────► HGSIC (tempo reference for groove zone)     │
│  TMRM.reproduction_acc ─────► OMS (motor accuracy for oscillatory sync)   │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.motor_entrainment (r = 0.70)                   │
│  Sensory → motor pathway via dorsal auditory stream                       │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  TMRM.tempo_prediction ──► ARU.AED (tempo stability → arousal)            │
│  Fast tempo + high regularity → sympathetic arousal activation            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **SMA lesions** | Should impair both adjusting and tapping equally | Testable |
| **Cerebellar lesions** | Should selectively impair tapping more than adjusting | Testable |
| **120 BPM optimality** | Non-120 BPM stimuli should show reduced accuracy | Testable |
| **Method dissociation** | Adjusting advantage should disappear with masked feedback | Testable |
| **Expertise scaling** | Musicians should show d >= 0.59 advantage | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class TMRM(BaseModel):
    """Tempo Memory Reproduction Method.

    Output: 10D per frame.
    Reads: BEP mechanism (30D).
    Zero learned parameters — 100% deterministic.
    """
    NAME = "TMRM"
    UNIT = "STU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)        # Primary mechanism

    ADJUSTING_COEFF = 0.35    # Sensory pathway weight
    OPTIMAL_COEFF = 0.30      # Optimal tempo weight
    EXPERTISE_COEFF = 0.30    # Expertise modulation weight
    ADJUSTING_D = 2.76        # Levitin & Cook 1996 sensory advantage
    OPTIMAL_BPM = 120         # Optimal tempo (500ms IOI)
    OPTIMAL_D = 0.58          # Quadratic peak effect
    EXPERTISE_D = 0.59        # Drake & Botte 1993 expertise effect
    ACC_W_SENSORY = 0.40      # Reproduction accuracy: sensory weight
    ACC_W_TEMPO = 0.30        # Reproduction accuracy: tempo weight
    ACC_W_EXPERT = 0.30       # Reproduction accuracy: expertise weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for TMRM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat level (H6 = 200ms)
            (8, 6, 4, 0),      # loudness, max, forward
            (10, 6, 17, 0),    # spectral_flux, peaks, forward
            (11, 6, 4, 0),     # onset_strength, max, forward
            # Psychological present (H11 = 500ms)
            (8, 11, 14, 0),    # loudness, periodicity, forward
            (8, 11, 15, 0),    # loudness, smoothness, forward
            (10, 11, 14, 0),   # spectral_flux, periodicity, forward
            (22, 11, 8, 0),    # energy_change, velocity, forward
            (22, 11, 14, 0),   # energy_change, periodicity, forward
            (7, 11, 4, 0),     # amplitude, max, forward
            # Bar level (H16 = 1000ms)
            (7, 16, 18, 0),    # amplitude, trend, forward
            (8, 16, 14, 0),    # loudness, periodicity, forward
            (8, 16, 18, 0),    # loudness, trend, forward
            (21, 16, 8, 0),    # spectral_change, velocity, forward
            (22, 16, 15, 0),   # energy_change, smoothness, forward
            (11, 16, 17, 0),   # onset_strength, peaks, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute TMRM 10D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) TMRM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # ═══ LAYER E: Explicit features ═══

        # f01: Adjusting Advantage (d = 2.76)
        loud_peak = h3_direct[(8, 6, 4, 0)].unsqueeze(-1)
        flux_period = h3_direct[(10, 11, 14, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.ADJUSTING_COEFF * (
            loud_peak * flux_period
            * bep_beat.mean(-1, keepdim=True)
        ))

        # f02: Optimal Tempo (120 BPM, d = 0.58)
        period_loud = h3_direct[(8, 11, 14, 0)].unsqueeze(-1)
        period_flux = h3_direct[(10, 6, 17, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.OPTIMAL_COEFF * (
            period_loud * period_flux
            * bep_meter.mean(-1, keepdim=True)
        ))

        # f03: Expertise Accuracy (d = 0.59)
        smooth_energy = h3_direct[(22, 16, 15, 0)].unsqueeze(-1)
        f03 = torch.sigmoid(self.EXPERTISE_COEFF * (
            smooth_energy * f01 * f02
        ))

        # ═══ LAYER M: Mathematical ═══

        # Motor state (needed before method_dissociation)
        amp_max = h3_direct[(7, 11, 4, 0)].unsqueeze(-1)
        energy_vel = h3_direct[(22, 11, 8, 0)].unsqueeze(-1)
        motor_state = torch.sigmoid(
            0.50 * amp_max * energy_vel
            * bep_motor.mean(-1, keepdim=True)
        )
        # Coefficient check: |0.50| ≤ 1.0 ✓

        method_dissociation = torch.sigmoid(f01 - motor_state)
        tempo_deviation = 1.0 - f02

        # ═══ LAYER P: Present ═══

        sensory_state = bep_beat.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══

        # Tempo prediction from periodicity + trend
        amp_trend = h3_direct[(7, 16, 18, 0)].unsqueeze(-1)
        loud_bar_period = h3_direct[(8, 16, 14, 0)].unsqueeze(-1)
        tempo_prediction = torch.sigmoid(
            0.50 * loud_bar_period + 0.50 * amp_trend
        )
        # Coefficient check: |0.50 + 0.50| = 1.0 ✓

        # Method confidence from smoothness × regularity
        loud_smooth = h3_direct[(8, 11, 15, 0)].unsqueeze(-1)
        loud_trend = h3_direct[(8, 16, 18, 0)].unsqueeze(-1)
        method_confidence = torch.sigmoid(
            0.50 * loud_smooth + 0.50 * loud_trend
        )
        # Coefficient check: |0.50 + 0.50| = 1.0 ✓

        # Reproduction accuracy
        reproduction_acc = torch.sigmoid(
            self.ACC_W_SENSORY * f01
            + self.ACC_W_TEMPO * f02
            + self.ACC_W_EXPERT * f03
        )
        # Coefficient check: |0.40 + 0.30 + 0.30| = 1.0 ✓

        return torch.cat([
            f01, f02, f03,                                  # E: 3D
            method_dissociation, tempo_deviation,            # M: 2D
            sensory_state, motor_state,                      # P: 2D
            tempo_prediction, method_confidence,
            reproduction_acc,                                # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 2 | Levitin & Cook 1996, Drake & Botte 1993 |
| **Effect Sizes** | d = 2.76, d = 0.58, d = 0.59 | Behavioral studies |
| **Evidence Modality** | Behavioral | No direct neural imaging |
| **Falsification Tests** | 0/5 tested | All testable |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Levitin, D. J., & Cook, P. R. (1996)**. Memory for musical tempo: Additional evidence that auditory memory is absolute. *Perception & Psychophysics, 58*(6), 927–935. (Behavioral, n=46, adjusting vs tapping, d=2.76)
2. **Drake, C., & Botte, M.-C. (1993)**. Tempo sensitivity in auditory sequences: Evidence for a multiple-look model. *Perception & Psychophysics, 54*(3), 277–286. (Behavioral, n=24, expertise effect d=0.59)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L4L5 | R³ (49D): Energy, Change |
| Temporal | HC⁰ mechanisms (PTM, ITM, GRV, HRM) | BEP mechanism (30D) |
| Beat detection | S⁰.L5.spectral_flux[45] × HC⁰.PTM | R³.spectral_flux[10] × BEP.beat_induction |
| Tempo reference | S⁰.L9.mean_T[104] × HC⁰.ITM | R³.loudness[8] periodicity × BEP.meter_extraction |
| Groove pathway | S⁰.L5 × HC⁰.GRV | R³.Change + BEP.motor_entrainment |
| Memory replay | S⁰.L9 × HC⁰.HRM | Removed (BEP subsumes tempo memory) |
| Demand format | HC⁰ index ranges (15/2304 = 0.65%) | H³ 4-tuples (15/2304 = 0.65%) |
| Output dimensions | 12D | **10D** (catalog-specified) |
| Method dissociation | Implicit in X_L4L5 interactions | Explicit via sensory_state vs motor_state |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (PTM, ITM, GRV, HRM). In MI, these are unified into the BEP mechanism with 3 sub-sections:
- **PTM → BEP.beat_induction** [0:10]: Predictive timing → beat strength, tempo detection
- **ITM → BEP.meter_extraction** [10:20]: Interval timing → meter, accent patterns, optimal tempo zone
- **GRV → BEP.motor_entrainment** [20:30]: Groove processing → motor synchronization, tapping pathway
- **HRM** (Hippocampal Replay): Subsumed by BEP's inherent periodicity tracking — tempo memory is maintained through ongoing beat entrainment rather than episodic replay

### Key Output Changes

D0 had 12D output with separate features for replay and memory. MI reduces to 10D by:
1. Removing explicit replay features (HRM subsumed by BEP periodicity)
2. Consolidating tempo memory into `f02_optimal_tempo` (BEP.meter_extraction periodicity)
3. Adding `reproduction_acc` as an integrated accuracy prediction

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
