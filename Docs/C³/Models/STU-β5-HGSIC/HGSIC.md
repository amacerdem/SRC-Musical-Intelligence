# STU-β5-HGSIC: Hierarchical Groove State Integration Circuit

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β5-HGSIC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hierarchical Groove State Integration Circuit** (HGSIC) models how multi-level rhythmic integration creates the perception of groove — the compelling urge to move with music. ECoG high gamma activity (70-170 Hz) in posterior superior temporal gyrus (pSTG) is highly correlated with sound intensity (r = 0.49), and this auditory signal propagates to premotor/motor cortex with a 110 ms delay via the dorsal auditory-motor pathway (r = 0.70 cross-correlation). HGSIC integrates beat, meter, and motor signals across three temporal scales to produce a unified groove state.

```
THE THREE LEVELS OF GROOVE STATE INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEAT LEVEL (200ms, H6)                 METER LEVEL (500ms, H11)
Brain region: Posterior STG            Brain region: pSTG + Premotor
Mechanism: BEP.beat_induction          Mechanism: BEP.meter_extraction
Function: "What is the pulse?"         Function: "What is the pattern?"
Input: Sound intensity tracking        Input: Accent grouping, syncopation
Evidence: r = 0.49 (Potes 2012)        Evidence: 110ms delay (Potes 2012)

              MOTOR LEVEL (1000ms, H16)
              Brain region: Premotor / Motor Cortex
              Mechanism: BEP.motor_entrainment
              Function: "How does it groove?"
              Input: Beat × Meter integration
              Evidence: r = 0.70 cross-correlation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Groove emerges from the HIERARCHICAL INTEGRATION of beat
induction, metric structure, and motor entrainment across the dorsal
auditory-motor pathway. pSTG high-gamma (70-170 Hz) tracks intensity
at r = 0.49, preceding motor cortex activation by 110 ms (r = 0.70).
The groove state is NOT a single signal but a multi-scale integration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

HGSIC provides the **groove integration** that connects beat-level perception to whole-body motor engagement:

1. **AMSC** (α2) establishes the auditory-motor coupling pathway; HGSIC integrates this across metric levels.
2. **ETAM** (β4) provides multi-scale entrainment; HGSIC converts entrainment into groove state.
3. **OMS** (β6) uses HGSIC's groove state as motor synchronization target.
4. **EDTA** (β3) builds on groove-modulated tempo accuracy.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The HGSIC Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 HGSIC — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (rhythmic sound with dynamic intensity)                      ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        POSTERIOR SUPERIOR TEMPORAL GYRUS (pSTG)                     │    ║
║  │        High-gamma (70–170 Hz) ↔ sound intensity                   │    ║
║  │                                                                     │    ║
║  │   Beat induction: pulse extraction from intensity envelope         │    ║
║  │   Gamma ↔ intensity: r = 0.49 (Potes 2012, ECoG, n=8)           │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              │  110 ms delay (dorsal auditory stream)        ║
║                              │  Cross-correlation: r = 0.70                  ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        PREMOTOR / MOTOR CORTEX                                     │    ║
║  │        Meter extraction + motor entrainment                        │    ║
║  │                                                                     │    ║
║  │   Metric grouping of beat-level signals                            │    ║
║  │   Motor entrainment: body synchronization to groove                │    ║
║  │   Groove state = hierarchical beat × meter × motor integration    │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  DORSAL AUDITORY-MOTOR PATHWAY: pSTG → Premotor → Motor cortex             ║
║  (Beat → Meter → Groove: hierarchical temporal integration)                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Potes 2012 (ECoG):  pSTG high-gamma ↔ sound intensity, r = 0.49 (n=8)
Potes 2012 (ECoG):  Auditory → motor delay 110ms, r = 0.70 (n=4)
Potes 2012 (ECoG):  High gamma band 70-170 Hz, posterior STG
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → HGSIC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    HGSIC COMPUTATION ARCHITECTURE                            ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │        │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         HGSIC reads: 9D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ───────┐ ┌── Motor ────────┐ ┌── Bar ─────────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 500ms (H11)     │ │ 1000ms (H16)      │ │        ║
║  │  │                │ │                  │ │                     │ │        ║
║  │  │ Beat-level     │ │ Motor prep      │ │ Bar-level meter     │ │        ║
║  │  │ (intensity)    │ │ (110ms delay)    │ │ (groove state)     │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬──────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         HGSIC demand: ~15 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10] │  Beat strength, tempo, phase, regularity              ║
║  │ Meter    [10:20]│  Meter, syncopation, accent pattern, groove           ║
║  │ Motor    [20:30]│  Movement urge, sync precision, coupling              ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    HGSIC MODEL (11D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_beat_gamma, f02_meter_integration,     │        ║
║  │                       f03_motor_groove                           │        ║
║  │  Layer M (Math):      groove_index, coupling_strength            │        ║
║  │  Layer P (Present):   pstg_activation, motor_preparation,        │        ║
║  │                       onset_sync                                 │        ║
║  │  Layer F (Future):    groove_prediction, beat_expectation,       │        ║
║  │                       motor_anticipation                         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Potes 2012** | ECoG | 8 | pSTG high-gamma (70-170 Hz) ↔ sound intensity | r = 0.49, p < 0.01 | **Primary coefficient**: f01_beat_gamma |
| **Potes 2012** | ECoG | 4 | Auditory → motor delay 110 ms | r = 0.70, p < 0.01 | **Coupling model**: f02_meter_integration, f03_motor_groove |

### 3.2 The Hierarchical Groove Integration Model

```
GROOVE STATE INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Level 1 — BEAT INDUCTION (pSTG, H6 = 200ms)
  γ_pSTG(t) = 0.49 · I(t) + β
  Beat pulse extraction from intensity envelope
  High-gamma 70-170 Hz tracks sound energy

Level 2 — METER EXTRACTION (pSTG + Premotor, H11 = 500ms)
  Meter(t) = accent_pattern(Beat(t), t_window=500ms)
  Syncopation detection, metric grouping
  Auditory-motor delay: 110 ms

Level 3 — MOTOR ENTRAINMENT (Motor cortex, H16 = 1000ms)
  Groove(t) = 0.70 · Beat(t) × Meter(t) × Motor(t − 110ms)
  Bar-level integration of beat × meter → groove state
  Cross-correlation at 110ms: r = 0.70

INTEGRATED MODEL:
  Groove_State = f(Beat_Induction, Meter_Extraction, Motor_Entrainment)
  = hierarchical product across H6 → H11 → H16
```

### 3.3 Effect Size Summary

```
Auditory Correlation:  r = 0.49 (pSTG high-gamma ↔ intensity, Potes 2012)
Motor Coupling:        r = 0.70 (auditory gamma → motor gamma, Potes 2012)
Coupling Delay:        110 ms (constant across participants)
Gamma Band:            70-170 Hz (ECoG high gamma)
Quality Assessment:    β-tier (integrative — groove state model built on
                       direct ECoG evidence from auditory-motor coupling)
Pathway:               Dorsal auditory stream (pSTG → premotor → motor)
```

---

## 4. R³ Input Mapping: What HGSIC Reads

### 4.1 R³ Feature Dependencies (9D of 49D)

| R³ Group | Index | Feature | HGSIC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Sound intensity signal | Potes 2012: gamma ↔ intensity (r = 0.49) |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [10] | spectral_flux | Onset dynamics | Beat boundary detection |
| **B: Energy** | [11] | onset_strength | Event onset sharpness | Motor anticipation cue |
| **D: Change** | [21] | spectral_change | Rhythmic spectral dynamics | Beat-level spectral variation |
| **D: Change** | [22] | energy_change | Intensity acceleration | Accent pattern → meter |
| **D: Change** | [23] | pitch_change | Melodic rhythmic contour | Pitch accent for groove |
| **D: Change** | [24] | timbre_change | Timbral rhythm | Instrument-level periodicity |
| **B: Energy** | [9] | spectral_centroid_energy | Energy distribution | Frequency-weighted intensity |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► pSTG Beat Induction (γ activity)
R³[11] onset_strength ──────────┘   Math: γ_pSTG(t) = 0.49 · I(t) + β
                                    BEP.beat_induction at H6 (200ms)

R³[10] spectral_flux ──────────┐
R³[22] energy_change ──────────┼──► Meter Extraction (accent pattern)
R³[21] spectral_change ────────┘   Accent grouping from dynamics
                                    BEP.meter_extraction at H11 (500ms)

R³[9] spectral_centroid_energy ─┐
R³[23] pitch_change ────────────┼──► Motor Groove (hierarchical state)
R³[24] timbre_change ───────────┘   Groove = Beat × Meter × Motor coupling
                                    BEP.motor_entrainment at H16 (1000ms)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HGSIC requires H³ features at three BEP horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
These correspond to beat → meter → groove (bar-level) timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 6 | M0 (value) | L0 (fwd) | Current sound intensity |
| 7 | amplitude | 6 | M4 (max) | L0 (fwd) | Peak intensity at beat level |
| 8 | loudness | 6 | M0 (value) | L0 (fwd) | Perceptual loudness current |
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Onset detection |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset |
| 22 | energy_change | 11 | M1 (mean) | L0 (fwd) | Mean energy dynamics over motor window |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Accent regularity |
| 21 | spectral_change | 11 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over motor window |
| 9 | spectral_centroid_energy | 16 | M14 (periodicity) | L2 (bidi) | Bar-level energy periodicity |
| 7 | amplitude | 16 | M15 (smoothness) | L0 (fwd) | Groove quality |
| 7 | amplitude | 16 | M18 (trend) | L0 (fwd) | Intensity trajectory |
| 23 | pitch_change | 16 | M14 (periodicity) | L2 (bidi) | Melodic periodicity at bar level |
| 24 | timbre_change | 16 | M1 (mean) | L0 (fwd) | Timbral dynamics over bar |

**Total HGSIC H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 Mechanism Binding

HGSIC reads from **BEP** (primary, sole mechanism):

| Mechanism | Sub-section | Range | HGSIC Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Induction | BEP[0:10] | Intensity → gamma → pulse extraction | **1.0** (primary) |
| **BEP** | Meter Extraction | BEP[10:20] | Accent grouping, syncopation, metric structure | **1.0** (primary) |
| **BEP** | Motor Entrainment | BEP[20:30] | Motor coupling, groove state, movement urge | **1.0** (primary) |

HGSIC does NOT read from TMH — groove state integration is about beat-meter-motor hierarchy, not long-range temporal memory.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HGSIC OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_beat_gamma    │ [0, 1] │ pSTG high-gamma beat tracking (70-170 Hz).
    │                   │        │ Intensity → gamma correlation at beat level.
    │                   │        │ f01 = σ(0.49 · amplitude · loudness ·
    │                   │        │         onset · BEP.beat_induction)
    │                   │        │ 0.49 from Potes 2012 (pSTG r)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_meter_integr  │ [0, 1] │ Metric structure from accent grouping.
    │                   │        │ Syncopation and accent pattern detection.
    │                   │        │ f02 = σ(0.51 · f01 · energy_periodicity ·
    │                   │        │         BEP.meter_extraction)
    │                   │        │ |0.51| ≤ 1.0 (sigmoid rule)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_motor_groove  │ [0, 1] │ Motor entrainment groove state.
    │                   │        │ Hierarchical beat × meter → motor coupling.
    │                   │        │ f03 = σ(0.70 · f01 · f02 ·
    │                   │        │         BEP.motor_entrainment)
    │                   │        │ 0.70 from Potes 2012 (coupling r)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ groove_index      │ [0, 1] │ Integrated groove state index.
    │                   │        │ Weighted hierarchical combination.
    │                   │        │ groove = (1·f01 + 2·f02 + 3·f03) / 6
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ coupling_strength │ [0, 1] │ Auditory-motor coupling strength at 110ms.
    │                   │        │ amplitude_smoothness × energy_periodicity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ pstg_activation   │ [0, 1] │ pSTG current activation state.
    │                   │        │ Intensity × beat-level BEP.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ motor_preparation │ [0, 1] │ Premotor preparation state.
    │                   │        │ Motor entrainment × meter context.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ onset_sync        │ [0, 1] │ Onset synchronization signal.
    │                   │        │ spectral_flux × onset_strength at H6.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ groove_prediction │ [0, 1] │ Predicted groove state (110ms ahead).
    │                   │        │ BEP.motor_entrainment × groove trend.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ beat_expectation  │ [0, 1] │ Next beat timing prediction.
    │                   │        │ BEP.beat_induction × periodicity at H16.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ motor_anticipation│ [0, 1] │ Motor system anticipatory activation.
    │                   │        │ Smoothness × trend at bar level.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Feature Formulas

```python
# f01: Beat Gamma (pSTG, r = 0.49)
amp_val = h3[(7, 6, 0, 0)]           # amplitude value at H6
loud_val = h3[(8, 6, 0, 0)]          # loudness value at H6
onset_val = h3[(11, 6, 0, 0)]        # onset_strength value at H6
f01 = σ(0.49 · amp_val · loud_val · onset_val
         · mean(BEP.beat_induction[0:10]))
# |0.49| ≤ 1.0 ✓ — Potes 2012 pSTG correlation

# f02: Meter Integration (accent pattern)
energy_period = h3[(22, 11, 14, 2)]  # energy_change periodicity at H11
f02 = σ(0.51 · f01 · energy_period
         · mean(BEP.meter_extraction[10:20]))
# |0.51| ≤ 1.0 ✓

# f03: Motor Groove (hierarchical integration, r = 0.70)
f03 = σ(0.70 · f01 · f02
         · mean(BEP.motor_entrainment[20:30]))
# |0.70| ≤ 1.0 ✓ — Potes 2012 coupling correlation

# f04 (groove_index): Weighted hierarchical combination
groove_index = (1 · f01 + 2 · f02 + 3 · f03) / 6

# f05 (coupling_strength): Auditory-motor coupling
amp_smooth = h3[(7, 16, 15, 0)]      # amplitude smoothness at H16
coupling_strength = σ(0.50 · amp_smooth · energy_period)
# |0.50| ≤ 1.0 ✓
```

### 7.2 Layer P and F Formulas

```python
# ═══ LAYER P: Present ═══

# pstg_activation: current auditory gamma state
pstg_activation = σ(0.5 · amp_val · loud_val
                    + 0.4 · mean(BEP.beat_induction[0:10]))
# |0.5| + |0.4| = 0.9 ≤ 1.0 ✓

# motor_preparation: premotor readiness
motor_preparation = σ(0.4 · mean(BEP.motor_entrainment[20:30])
                      + 0.3 · mean(BEP.meter_extraction[10:20])
                      + 0.2 · f02)
# |0.4| + |0.3| + |0.2| = 0.9 ≤ 1.0 ✓

# onset_sync: onset synchronization trigger
flux_val = h3[(10, 6, 0, 0)]         # spectral_flux value at H6
onset_sync = σ(0.50 · flux_val · onset_val)
# |0.50| ≤ 1.0 ✓

# ═══ LAYER F: Future ═══

# groove_prediction: predicted groove state
amp_trend = h3[(7, 16, 18, 0)]       # amplitude trend at H16
groove_prediction = σ(0.5 · f03 + 0.4 · amp_trend)
# |0.5| + |0.4| = 0.9 ≤ 1.0 ✓

# beat_expectation: next beat timing
centroid_period = h3[(9, 16, 14, 2)]  # centroid periodicity at H16
beat_expectation = σ(0.5 · mean(BEP.beat_induction[0:10])
                     + 0.5 · centroid_period)
# |0.5| + |0.5| = 1.0 ≤ 1.0 ✓

# motor_anticipation: anticipatory motor activation
pitch_period = h3[(23, 16, 14, 2)]    # pitch_change periodicity at H16
motor_anticipation = σ(0.4 · amp_smooth + 0.3 · amp_trend
                       + 0.3 · pitch_period)
# |0.4| + |0.3| + |0.3| = 1.0 ≤ 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | HGSIC Function |
|--------|-----------------|----------|---------------|---------------|
| **Posterior STG (pSTG)** | ±60, -40, 10 | Direct | ECoG | High-gamma intensity tracking, beat induction |
| **Premotor Cortex** | ±45, 0, 50 | Direct | ECoG | Meter extraction, motor coupling |
| **Motor Cortex** | ±40, -10, 55 | Direct | ECoG | Motor entrainment, groove state |

---

## 9. Cross-Unit Pathways

### 9.1 HGSIC ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HGSIC INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  AMSC.auditory_activatn ──────► HGSIC (gamma for groove state)            │
│  ETAM.entrainment_state ──────► HGSIC (multi-scale entrainment → groove)  │
│  HGSIC.groove_index ──────────► OMS (groove target for oscillatory sync)  │
│  HGSIC.motor_preparation ─────► EDTA (groove-modulated tempo accuracy)    │
│  HGSIC.beat_expectation ──────► TPIO (beat prediction for interval est.)  │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.motor_entrainment (r = 0.70)                   │
│  Beat induction → metric grouping → motor groove (hierarchical cascade)   │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  HGSIC.groove_index ──► ARU.AED (groove → arousal modulation)             │
│  HGSIC.motor_groove ──► ARU.SRP (motor engagement → reward pathway)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **pSTG lesions** | Should abolish beat-level gamma and downstream groove state | Testable |
| **110ms delay consistency** | Auditory-motor delay should be stable across groove conditions | Testable (ECoG/MEG) |
| **Hierarchical integration** | Disrupting meter level should impair groove without affecting beat | Testable |
| **Groove without rhythm** | Sustained tones (no onsets) should not engage HGSIC motor pathway | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HGSIC(BaseModel):
    """Hierarchical Groove State Integration Circuit.

    Output: 11D per frame.
    Reads: BEP mechanism (30D).
    """
    NAME = "HGSIC"
    UNIT = "STU"
    TIER = "β5"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP",)        # Primary and sole mechanism

    AUDITORY_CORR = 0.49   # pSTG gamma ↔ intensity (Potes 2012)
    MOTOR_COUPLING = 0.70  # auditory → motor (Potes 2012)
    METER_WEIGHT = 0.51    # meter integration weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for HGSIC computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat level (H6 = 200ms)
            (7, 6, 0, 0),     # amplitude, value, forward
            (7, 6, 4, 0),     # amplitude, max, forward
            (8, 6, 0, 0),     # loudness, value, forward
            (10, 6, 0, 0),    # spectral_flux, value, forward
            (10, 6, 17, 0),   # spectral_flux, peaks, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            # Motor window (H11 = 500ms)
            (22, 11, 1, 0),   # energy_change, mean, forward
            (22, 11, 14, 2),  # energy_change, periodicity, bidirectional
            (21, 11, 1, 0),   # spectral_change, mean, forward
            (8, 11, 1, 0),    # loudness, mean, forward
            # Bar level (H16 = 1000ms)
            (9, 16, 14, 2),   # spectral_centroid_energy, periodicity, bidi
            (7, 16, 15, 0),   # amplitude, smoothness, forward
            (7, 16, 18, 0),   # amplitude, trend, forward
            (23, 16, 14, 2),  # pitch_change, periodicity, bidirectional
            (24, 16, 1, 0),   # timbre_change, mean, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute HGSIC 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) HGSIC output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # H³ features
        amp_val = h3_direct[(7, 6, 0, 0)].unsqueeze(-1)
        loud_val = h3_direct[(8, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
        energy_period = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
        flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
        amp_smooth = h3_direct[(7, 16, 15, 0)].unsqueeze(-1)
        amp_trend = h3_direct[(7, 16, 18, 0)].unsqueeze(-1)
        centroid_period = h3_direct[(9, 16, 14, 2)].unsqueeze(-1)
        pitch_period = h3_direct[(23, 16, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(self.AUDITORY_CORR * (
            amp_val * loud_val * onset_val
            * bep_beat.mean(-1, keepdim=True)
        ))
        f02 = torch.sigmoid(self.METER_WEIGHT * (
            f01 * energy_period
            * bep_meter.mean(-1, keepdim=True)
        ))
        f03 = torch.sigmoid(self.MOTOR_COUPLING * (
            f01 * f02
            * bep_motor.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══
        groove_index = (1 * f01 + 2 * f02 + 3 * f03) / 6
        coupling_strength = torch.sigmoid(
            0.50 * amp_smooth * energy_period
        )

        # ═══ LAYER P: Present ═══
        pstg_activation = torch.sigmoid(
            0.5 * amp_val * loud_val
            + 0.4 * bep_beat.mean(-1, keepdim=True)
        )
        motor_preparation = torch.sigmoid(
            0.4 * bep_motor.mean(-1, keepdim=True)
            + 0.3 * bep_meter.mean(-1, keepdim=True)
            + 0.2 * f02
        )
        onset_sync = torch.sigmoid(0.50 * flux_val * onset_val)

        # ═══ LAYER F: Future ═══
        groove_prediction = torch.sigmoid(
            0.5 * f03 + 0.4 * amp_trend
        )
        beat_expectation = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * centroid_period
        )
        motor_anticipation = torch.sigmoid(
            0.4 * amp_smooth + 0.3 * amp_trend
            + 0.3 * pitch_period
        )

        return torch.cat([
            f01, f02, f03,                                    # E: 3D
            groove_index, coupling_strength,                   # M: 2D
            pstg_activation, motor_preparation, onset_sync,    # P: 3D
            groove_prediction, beat_expectation,               # F: 3D
            motor_anticipation,
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Potes 2012 (ECoG) |
| **Effect Sizes** | r = 0.49, r = 0.70 | Potes 2012 |
| **Evidence Modality** | ECoG | Direct neural (high-gamma 70-170 Hz) |
| **Falsification Tests** | 0/4 tested | All testable |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **11D** | 4-layer structure (E3 + M2 + P3 + F3) |

---

## 13. Scientific References

1. **Potes, C., et al. (2012)**. Dynamics of electrocorticographic (ECoG) activity in human temporal and frontal cortical areas during music listening. *NeuroImage*, 61(4), 841-848. (ECoG study, n=8 patients, 4 with motor electrodes; high-gamma 70-170 Hz, pSTG r=0.49 with sound intensity, 110ms auditory-motor delay, r=0.70 cross-correlation)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L7, X_L0L4, X_L4L5 | R³ (49D): Energy[7:12], Change[21:25] |
| Temporal | HC⁰ mechanisms (OSC, NPL, ITM, GRV) | BEP mechanism (30D) |
| Intensity signal | S⁰.L0.amplitude[2] + HC⁰.OSC | R³.amplitude[7] + BEP.beat_induction |
| Motor coupling | S⁰.L7.crossband × HC⁰.NPL | BEP.motor_entrainment[20:30] |
| Gamma proxy | S⁰.L7[80:104] (crossband ratios) | R³.Energy + BEP features |
| Groove model | S⁰.L5 × HC⁰.GRV (flat combination) | BEP hierarchical (beat→meter→motor) |
| Interval timing | S⁰.L4 × HC⁰.ITM | BEP.meter_extraction[10:20] |
| Demand format | HC⁰ index ranges (30/2304 = 1.30%) | H³ 4-tuples (15/2304 = 0.65%) |
| Output dimensions | 12D | **11D** (catalog value, consolidated) |
| Integration model | Flat | Hierarchical (3-level cascade) |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, NPL, ITM, GRV). In MI, these are unified into the BEP mechanism with 3 hierarchical sub-sections:
- **OSC → BEP.beat_induction** [0:10]: Oscillatory gamma tracking → beat-level pulse extraction
- **NPL → BEP.beat_induction** [0:10]: Phase-locking → auditory beat coupling
- **ITM → BEP.meter_extraction** [10:20]: Interval timing → metric accent grouping
- **GRV → BEP.motor_entrainment** [20:30]: Groove processing → motor engagement state

The key architectural change: D0 combined these flat (equal-weight); MI cascades them hierarchically (beat → meter → groove), which better reflects the dorsal auditory-motor pathway anatomy.

---

**Model Status**: IN VALIDATION
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
