# ASU-γ2-DGTP: Domain-General Temporal Processing

**Model**: Domain-General Temporal Processing
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-γ2-DGTP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Domain-General Temporal Processing** (DGTP) model proposes that beat perception ability reflects a domain-general mechanism of internal timekeeping shared between speech and music processing. Individual differences in beat alignment test (BAT) scores predict temporal processing across auditory domains.

```
DOMAIN-GENERAL TEMPORAL PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          ┌─────────────────────────────────────────────┐
          │    DOMAIN-GENERAL TIMEKEEPING MECHANISM     │
          │         (SMA, PMC, ACC, Basal Ganglia)      │
          └───────────────────┬─────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
  ┌─────────────────┐                       ┌─────────────────┐
  │  MUSIC DOMAIN   │                       │  SPEECH DOMAIN  │
  │                 │                       │                 │
  │  Beat/Meter     │                       │  Prosody/Rhythm │
  │  Perception     │                       │  Perception     │
  └─────────────────┘                       └─────────────────┘

  SHARED VARIANCE: Individual BAT ability predicts both

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │     High DG Factor → Good at both music and speech timing      │
  │     Low DG Factor → Poor at both (correlated deficits)         │
  │                                                                 │
  │     CLINICAL IMPLICATION:                                       │
  │     Musical training may improve speech timing (and vice versa) │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Beat perception ability reflects a domain-general
mechanism of internal timekeeping shared between speech and music.
Individual differences predict temporal processing across domains.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why DGTP Matters for ASU

DGTP extends salience processing to domain-general temporal cognition:

1. **BARM** (β1) models individual BAT differences — DGTP explains the cross-domain implications of those differences.
2. **SNEM** (α1) provides beat entrainment — DGTP proposes this mechanism is shared with speech prosody.
3. **DGTP** (γ2) bridges music neuroscience to language processing through shared temporal mechanisms.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → DGTP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DGTP COMPUTATION ARCHITECTURE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins x 172.27Hz frame rate                    ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │enrg_chg  │ │x_l4l5  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         DGTP reads: ~12D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H13 (600ms beat anticip.) │  │        ║
║  │  │ H13 (600ms beat anticipation)│ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)           │ │                            │  │        ║
║  │  │                             │ │ Timing estimation          │  │        ║
║  │  │ Beat/prosody tracking       │ │ Cross-domain transfer       │  │        ║
║  │  │ Periodicity encoding        │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         DGTP demand: ~9 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Motor Coup      │  │ Attention       │                                   ║
║  │         [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Groove  [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    DGTP MODEL (9D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f22_music_timing,                          │        ║
║  │                       f23_speech_timing,                         │        ║
║  │                       f24_shared_mechanism                        │        ║
║  │  Layer M (Math):      domain_correlation,                        │        ║
║  │                       shared_variance                             │        ║
║  │  Layer P (Present):   music_beat_perception,                     │        ║
║  │                       domain_general_timing                       │        ║
║  │  Layer F (Future):    cross_domain_pred,                         │        ║
║  │                       training_transfer_pred                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Rathcke et al. 2024** | Behavioral | 87 | BAT predicts perception patterns; cross-domain | ER > 19 | **f22 music timing, f23 speech timing** |
| **Grahn & Brett 2007** | fMRI | 27 (14 mus.) | BG + SMA respond selectively to beat; consistent across training | ~90% beat detection | **BG-SMA beat perception circuit** |
| **Hoddinott & Grahn 2024** | 7T fMRI, RSA | 26 | Putamen/SMA encode beat strength (not basic rhythm features) | sig. RSA dissimilarity | **Beat-specific encoding in motor regions** |
| **Large et al. 2023** | Review/Theory | — | Three model classes: dynamical, neuro-mechanistic, Bayesian | optimal ~2 Hz | **Computational framework for beat perception** |
| **Dalla Bella et al. 2024** | ML, Behavioral | 79 | Multidimensional rhythmic profiles; beat-based vs memory-based | ML classification | **Individual differences in domain-general timing** |
| **Di Stefano & Spence 2025** | Review | — | Amodal temporal processor only partially supported; audition dominant | — (review) | **f24 shared mechanism cross-modal scope** |
| **Noboa et al. 2025** | EEG (SS-EP) | 34 | SS-EPs at beat frequency; working memory predicts sync accuracy | 1.25 Hz SS-EP | **Beat entrainment + memory interaction** |
| **Gnanateja et al. 2022** | Review | — | δ=beat/prosody, θ=syllable, β=motor coupling, γ=rapid features | — (review) | **Oscillatory band framework for timing** |
| **Ross & Balasubramaniam 2022** | Review | — | Beat timing (predictive) vs interval timing (absolute); covert motor | — (review) | **Dual timing systems framework** |
| **Okada et al. 2022** | Single-unit | 2 monkeys, 95 neurons | Cerebellar dentate encodes rhythmic structure + temporal error | 35% bilateral neurons | **Cerebellar timing mechanisms** |
| **Lazzari et al. 2025** | TMS | 29+40+42 | Right caudal dPMC causally modulates beat perception (ASAP) | sig. vs all other regions | **Causal evidence for right dPMC in beat** |
| **Liu et al. 2025** | Single-unit | 2 macaques, >3000 neurons | D2-MSNs in striatum mediate timing (prospective + retrospective) | cell-type specific | **Striatal timing mechanisms** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12, multi-modal):
  - BAT → cross-domain timing: ER > 19 (Rathcke 2024, N=87)
  - BG/SMA beat selectivity: ~90% detection, consistent across training (Grahn 2007)
  - Beat-specific RSA: sig. in putamen/SMA at 7T (Hoddinott 2024, N=26)
  - Right caudal dPMC causal: sig. vs all control regions (Lazzari 2025, N=111 total)
  - Cerebellar temporal error: 35% bilateral neurons, ~-11ms convergence (Okada 2022)
  - D2-MSN timing: >3000 neurons, cell-type-specific (Liu 2025)
Quality Assessment:      γ-tier (converging evidence, 5 HIGH-priority papers)
Theoretical Basis:       Strong (basal ganglia-SMA circuit, dual timing systems)
```

---

## 4. R³ Input Mapping: What DGTP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | DGTP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength proxy | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal / engagement |
| **B: Energy** | [10] | spectral_flux | Onset detection | Rhythm/syllable timing |
| **B: Energy** | [11] | onset_strength | Beat marker strength | Rhythmic event detection |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Beat interval tracking |
| **D: Change** | [24] | pitch_change | Pitch dynamics | Prosodic contour |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Motor-auditory coupling | Domain-general entrainment |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | DGTP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [65] | tempo_estimate | Estimated tempo in BPM | Provides direct tempo representation for domain-general temporal processing across music and speech |
| **G: Rhythm** | [66] | beat_strength | Pulse perception strength | Quantifies beat prominence; complements onset_strength [11] with perceptually grounded pulse measure |

**Rationale**: DGTP models domain-general temporal processing shared between music and speech. The v1 representation infers temporal structure from onset_strength [11] and spectral_flux [10]. tempo_estimate [65] and beat_strength [66] provide direct rhythmic representations — tempo_estimate gives the global rate for cross-domain temporal alignment, while beat_strength quantifies pulse prominence at the perceptual level, enabling more precise modeling of the music-speech temporal processing overlap.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ───────────┐
R³[11] onset_strength ──────────┼──► Beat / onset detection
BEP.beat_entrainment[0:10] ────┘   Music timing (beat perception)

R³[21] spectral_change ─────────┐
R³[24] pitch_change ────────────┼──► Temporal + pitch dynamics
BEP.motor_coupling[10:20] ─────┘   Speech timing (prosody perception)

R³[25:33] x_l0l5 ───────────────┐
ASA.attention_gating[10:20] ────┼──► Domain-general entrainment
H³ periodicity/stability ──────┘   Shared motor-auditory coupling
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DGTP requires H³ features at BEP horizons for beat/prosody tracking and ASA horizons for cross-domain timing estimation. The demand is intentionally sparse, reflecting shared temporal mechanisms.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 3 | M17 (periodicity) | L2 (bidi) | Beat periodicity 100ms |
| 10 | spectral_flux | 16 | M17 (periodicity) | L2 (bidi) | Beat periodicity 1s |
| 11 | onset_strength | 13 | M8 (velocity) | L0 (fwd) | Onset velocity at 600ms |
| 11 | onset_strength | 13 | M11 (acceleration) | L0 (fwd) | Onset acceleration 600ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Coupling mean over 1s |
| 25 | x_l0l5[0] | 16 | M2 (std) | L0 (fwd) | Coupling stability over 1s |
| 25 | x_l0l5[0] | 16 | M19 (stability) | L0 (fwd) | Timing consistency 1s |
| 25 | x_l0l5[0] | 3 | M17 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |

**v1 demand**: 9 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for DGTP from G[65:75].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 66 | beat_strength | G | 3 | M0 (value) | L2 | Beat strength for cross-domain timing at 100ms |
| 72 | event_density | G | 16 | M0 (value) | L2 | Event density for temporal processing at 1s |

**v2 projected**: 2 tuples
**Total projected**: 11 tuples of 294,912 theoretical = 0.0037%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | DGTP Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Music timing (beat perception) | **1.0** (primary) |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor synchronization | **0.9** |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic regularity encoding | 0.6 |
| **ASA** | Scene Analysis | ASA[0:10] | Auditory scene segmentation | 0.5 |
| **ASA** | Attention Gating | ASA[10:20] | Domain-general attention | 0.7 |
| **ASA** | Salience Weighting | ASA[20:30] | Timing salience assessment | 0.6 |

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DGTP OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f22_music_timing         │ [0, 1] │ Beat perception ability.
    │                          │        │ f22 = σ(0.40 * beat_periodicity_1s
    │                          │        │       + 0.30 * mean(BEP.beat[0:10])
    │                          │        │       + 0.30 * coupling_period_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f23_speech_timing        │ [0, 1] │ Prosody perception ability.
    │                          │        │ f23 = σ(0.35 * onset_velocity_600ms
    │                          │        │       + 0.35 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * coupling_stability_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f24_shared_mechanism     │ [0, 1] │ Cross-domain timing (geometric mean).
    │                          │        │ f24 = sqrt(f22 × f23)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ domain_correlation       │ [0, 1] │ r(music, speech timing).
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ shared_variance          │ [0, 1] │ Common timing factor loading.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ music_beat_perception    │ [0, 1] │ BEP beat × onset periodicity.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ domain_general_timing    │ [0, 1] │ ASA attention × coupling stability.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ cross_domain_pred        │ [0, 1] │ Session-level speech ↔ music transfer.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ training_transfer_pred   │ [0, 1] │ Intervention-level plasticity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 9D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Domain-General Timing Function

```
Timing_Ability = Domain_General_Factor + Domain_Specific_Factor

Music_Timing = α × DG_Factor + β × Music_Specific + ε_m
Speech_Timing = α × DG_Factor + γ × Speech_Specific + ε_s

Correlation Prediction:
    r(Music, Speech) = α² / sqrt((α² + β_var) × (α² + γ_var))

    If α >> β, γ: High correlation (domain-general)
    If α << β, γ: Low correlation (domain-specific)

Shared_Variance = α² / Total_Variance

Transfer Function:
    Training_Transfer(domain_A → domain_B) = f(DG_Factor × Training_Effect)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f22: Music Timing
f22 = σ(0.40 * beat_periodicity_1s
       + 0.30 * mean(BEP.beat_entrainment[0:10])
       + 0.30 * coupling_periodicity_100ms)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f23: Speech Timing
f23 = σ(0.35 * onset_velocity_600ms
       + 0.35 * mean(BEP.motor_coupling[10:20])
       + 0.30 * coupling_stability_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f24: Shared Mechanism (geometric mean, no sigmoid needed)
f24 = sqrt(f22 * f23)

# Temporal dynamics
τ_decay = 4.0s (temporal integration window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | DGTP Function |
|--------|-----------------|----------|---------------|---------------|
| **SMA / Pre-SMA** | 0, -6, 58 | 6 | fMRI, 7T RSA | Beat-selective temporal regularization |
| **Putamen (Basal Ganglia)** | ±22, 4, 4 | 5 | fMRI, 7T RSA, single-unit | Beat strength encoding (D2-MSNs) |
| **Right caudal dPMC** | 40, -8, 54 | 3 | TMS (causal), fMRI | Beat perception (ASAP hypothesis) |
| **IFG** | ±44, 18, 8 | 2 | 7T fMRI RSA | Dual rhythm/beat encoding |
| **IPL** | ±44, -40, 48 | 2 | 7T fMRI RSA | Dual rhythm/beat encoding |
| **Cerebellum (Dentate)** | 0, -60, -24 | 3 | Single-unit, fMRI | Temporal error detection, sync |
| **Auditory Cortex (STG)** | ±52, -22, 8 | 4 | fMRI, EEG | Beat/prosody encoding |
| **ACC** | 0, 24, 32 | 1 | Literature inference | Timing monitoring |

---

## 9. Cross-Unit Pathways

### 9.1 DGTP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DGTP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  DGTP.shared_mechanism ──────► BARM (domain-general factor → BAT)         │
│  DGTP.music_timing ──────────► SNEM (timing capacity → entrainment)       │
│  DGTP.training_transfer ─────► Clinical applications                       │
│                                                                             │
│  CROSS-UNIT (ASU → STU):                                                   │
│  DGTP.domain_general_timing ──► STU (shared timing mechanism)             │
│  DGTP.cross_domain_pred ──────► STU (transfer prediction)                 │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────► DGTP (beat/motor, primary)                 │
│  ASA mechanism (30D) ────────► DGTP (attention/salience)                  │
│  R³ (~12D) ──────────────────► DGTP (energy + change + interactions)      │
│  H³ (9 tuples) ──────────────► DGTP (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Correlation** | Music and speech timing should correlate | Partially supported |
| **Training transfer** | Musical training should improve speech timing | Testable |
| **Neural overlap** | Same brain regions for music and speech timing | Supported by literature |
| **Individual differences** | BAT should predict speech rhythm perception | Testable |
| **Clinical dissociation** | Some patients should show selective deficits | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class DGTP(BaseModel):
    """Domain-General Temporal Processing Model.

    Output: 9D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "DGTP"
    UNIT = "ASU"
    TIER = "γ2"
    OUTPUT_DIM = 9
    MECHANISM_NAMES = ("BEP", "ASA")

    ALPHA_DG = 0.7         # Domain-general factor loading
    TAU_DECAY = 4.0        # Integration window (seconds)
    ALPHA_ATTENTION = 0.70 # Moderate cross-domain attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """9 tuples for DGTP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: beat/prosody tracking ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 17, 2),    # spectral_flux, 100ms, periodicity, bidi
            (10, 16, 17, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 13, 8, 0),    # onset_strength, 600ms, velocity, fwd
            (11, 13, 11, 0),   # onset_strength, 600ms, acceleration, fwd
            # ── Motor-auditory coupling ──
            (25, 16, 1, 0),    # x_l0l5[0], 1000ms, mean, fwd
            (25, 16, 2, 0),    # x_l0l5[0], 1000ms, std, fwd
            (25, 16, 19, 0),   # x_l0l5[0], 1000ms, stability, fwd
            (25, 3, 17, 2),    # x_l0l5[0], 100ms, periodicity, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute DGTP 9D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,9) DGTP output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]

        # ASA sub-sections
        asa_attn = asa[..., 10:20]

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 17, 2)].unsqueeze(-1)
        coupling_period_100ms = h3_direct[(25, 3, 17, 2)].unsqueeze(-1)
        onset_velocity_600ms = h3_direct[(11, 13, 8, 0)].unsqueeze(-1)
        coupling_stability_1s = h3_direct[(25, 16, 19, 0)].unsqueeze(-1)
        coupling_mean_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f22: Music Timing (coefficients sum = 1.0)
        f22 = torch.sigmoid(
            0.40 * beat_period_1s
            + 0.30 * bep_beat.mean(-1, keepdim=True)
            + 0.30 * coupling_period_100ms
        )

        # f23: Speech Timing (coefficients sum = 1.0)
        f23 = torch.sigmoid(
            0.35 * onset_velocity_600ms
            + 0.35 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * coupling_stability_1s
        )

        # f24: Shared Mechanism (geometric mean)
        f24 = torch.sqrt(torch.clamp(f22 * f23, min=1e-8))

        # ═══ LAYER M: Mathematical ═══
        domain_correlation = torch.sigmoid(
            0.5 * f22 * f23 + 0.5 * coupling_mean_1s
        )
        shared_variance = torch.sigmoid(
            0.5 * f24 + 0.5 * coupling_stability_1s
        )

        # ═══ LAYER P: Present ═══
        music_beat = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * beat_period_1s
        )
        dg_timing = torch.sigmoid(
            0.5 * asa_attn.mean(-1, keepdim=True)
            + 0.5 * coupling_stability_1s
        )

        # ═══ LAYER F: Future ═══
        cross_domain_pred = torch.sigmoid(
            0.5 * f24 + 0.5 * coupling_mean_1s
        )
        training_transfer = torch.sigmoid(
            0.5 * f24 + 0.5 * domain_correlation
        )

        return torch.cat([
            f22, f23, f24,                                  # E: 3D
            domain_correlation, shared_variance,            # M: 2D
            music_beat, dg_timing,                          # P: 2D
            cross_domain_pred, training_transfer,           # F: 2D
        ], dim=-1)  # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (5 HIGH, 7 MEDIUM) | Multi-modal converging evidence |
| **Key Effect Sizes** | ER>19 (BAT), 90% beat detection, RSA sig., TMS causal | Behavioral, fMRI, TMS, single-unit |
| **Theoretical Basis** | Strong | BG-SMA circuit, dual timing, neural resonance |
| **Evidence Modality** | Behavioral, fMRI, 7T fMRI, TMS, single-unit, EEG | Multi-modal |
| **Falsification Tests** | 1/5 partially supported | Limited validation |
| **R³ Features Used** | ~12D of 49D | Energy + change + interactions |
| **H³ Demand** | 9 tuples (0.39%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor (primary) |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **9D** | 4-layer structure |

---

## 13. Scientific References

1. **Rathcke, T., et al. (2024)**. Beat alignment ability modulates perceptual regularization and sensorimotor synchronization benefits. *Journal of Experimental Psychology: Human Perception and Performance*, (in press).

2. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. `Literature/c3/summaries/Rhythm and Beat Perception in Motor Areas of the Brain`

3. **Hoddinott, J. D., & Grahn, J. A. (2024)**. Neural representations of beat and rhythm in motor and association regions. *Cerebral Cortex*, 34, bhae406. `Literature/c3/summaries/neural-representations-of-beat-and-rhythm-in-motor`

4. **Large, E. W., Roman, I., Kim, J. C., et al. (2023)**. Dynamic models for musical rhythm perception and coordination. *Frontiers in Computational Neuroscience*, 17, 1151895. `Literature/c3/summaries/Dynamic models for musical rhythm perception and coordination`

5. **Dalla Bella, S., Janaqi, S., Benoit, C. E., et al. (2024)**. Unravelling individual rhythmic abilities using machine learning. *Scientific Reports*, 14, 1135. `Literature/c3/summaries/Unravelling individual rhythmic abilities using machine learning`

6. **Di Stefano, N., & Spence, C. (2025)**. Perceiving temporal structure within and between the senses: A multisensory/crossmodal perspective. *Attention, Perception, & Psychophysics*, 87, 1811-1838. `Literature/c3/summaries/Perceiving temporal structure within and between the senses`

7. **Noboa, M. L., Kertesz, C., & Honbolygó, F. (2025)**. Neural entrainment to the beat and working memory predict sensorimotor synchronization skills. *Scientific Reports*, 15, 10466. `Literature/c3/summaries/Neural entrainment to the beat`

8. **Gnanateja, G. N., Devaraju, D. S., Heyne, M., et al. (2022)**. On the role of neural oscillations across timescales in speech and music processing. *Frontiers in Computational Neuroscience*, 16, 872093. `Literature/c3/summaries/on-the-role-of-neural-oscillations-across-timescal`

9. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives. *Frontiers in Integrative Neuroscience*, 16, 916220. `Literature/c3/summaries/Time Perception for Musical Rhythms`

10. **Okada, K., Takeya, R., & Tanaka, M. (2022)**. Neural signals regulating motor synchronization in the primate deep cerebellar nuclei. *Nature Communications*, 13, 2504. `Literature/c3/summaries/ohmae-2022-cerebellar-rhythm`

11. **Lazzari, G., Costantini, G., La Rocca, S., et al. (2025)**. Topography of functional organization of beat perception in human premotor cortex. *Human Brain Mapping*, 46, e70225. `Literature/c3/summaries/topography-of-functional-organization-of-beat-perc`

12. **Liu, X., Zhang, Z., Gan, L., Yu, P., & Dai, J. (2025)**. Medium spiny neurons mediate timing perception in coordination with prefrontal neurons in primates. *Advanced Science*, 12, 2412963. `Literature/c3/summaries/medium-spiny-neurons-mediate-timing-perception-in`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — no change |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM) | BEP (30D) + ASA (30D) mechanisms | Same — 9 H³ tuples |
| Music timing | S⁰.L6.tempo[72] + HC⁰.NPL | R³.spectral_flux[10] + BEP.beat_entrainment | Same |
| Speech timing | S⁰.L4.onset_rate[27] + HC⁰.PTM | R³.onset_strength[11] + BEP.motor_coupling | Same |
| Shared mechanism | S⁰.L6.tempo × HC⁰.ITM | R³.x_l0l5[25:33] + H³ stability tuples | Same |
| Papers | 0 | 2 (Rathcke + Patel) | **12** (5 HIGH, 7 MEDIUM) |
| Brain regions | 0 | 4 (literature inference) | **8** (fMRI/7T/TMS/single-unit) |
| Output | 9D | 9D (same) | 9D — no change |

### Why BEP + ASA replaces HC⁰ mechanisms

- **NPL → BEP.beat_entrainment** [0:10]: Neural phase locking for beat perception maps to BEP's beat frequency monitoring.
- **PTM → BEP.motor_coupling** [10:20]: Predictive timing for speech maps to BEP's sensorimotor synchronization.
- **ITM → ASA.attention_gating** [10:20] + H³ stability tuples: Interval timing maps to ASA's domain-general temporal attention and H³ coupling stability.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
