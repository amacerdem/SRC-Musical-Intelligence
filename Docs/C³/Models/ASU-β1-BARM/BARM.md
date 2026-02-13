# ASU-β1-BARM: Beat Ability Regulatory Model

**Model**: Beat Ability Regulatory Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-β1-BARM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Beat Ability Regulatory Model** (BARM) describes how individual differences in beat perception ability (BAT) modulate perceptual regularization tendencies. Low BAT individuals show stronger regularization effects and benefit more from sensorimotor synchronization (tapping), while high BAT individuals show more veridical perception.

```
BEAT ABILITY REGULATORY MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                     ┌─────────────────┐
                     │  Beat Ability   │
                     │    (BAT)        │
                     └────────┬────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
    LOW BAT                                   HIGH BAT
         │                                         │
         ▼                                         ▼
  ┌─────────────────┐                     ┌─────────────────┐
  │ Strong          │                     │ Minimal         │
  │ Regularization  │                     │ Regularization  │
  │ Effect          │                     │ Effect          │
  └────────┬────────┘                     └────────┬────────┘
           │                                       │
           │  + Sensorimotor                       │
           │    Synchronization                    │
           ▼                                       ▼
  ┌─────────────────┐                     ┌─────────────────┐
  │ Regularization↓ │                     │   Consistent    │
  │ (Benefit from   │                     │   Performance   │
  │  movement)      │                     │   (No change)   │
  └─────────────────┘                     └─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Low BAT individuals benefit MOST from tapping.
Individual differences in beat perception ability modulate both
regularization and the benefit of sensorimotor synchronization.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why BARM Matters for ASU

BARM bridges individual differences into salience processing:

1. **SNEM** (α1) provides beat entrainment baseline — BARM modulates this by individual ability.
2. **BARM** (β1) explains why the same rhythmic stimulus produces different salience responses across individuals.
3. **DGTP** (γ2) extends BARM's individual differences to domain-general temporal processing.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → BARM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BARM COMPUTATION ARCHITECTURE                             ║
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
║  │                         BARM reads: ~12D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         BARM demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
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
║  │                    BARM MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E: f10_regularization, f11_beat_alignment, f12_sync_ben  │        ║
║  │  Layer M: veridical_perception, regularization_effect            │        ║
║  │  Layer P: beat_alignment_accuracy, regularization_strength       │        ║
║  │  Layer F: beat_accuracy_pred, sync_benefit_pred, indiv_diff_pred│        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Rathcke et al. 2024** | Behavioral | 87 | High BAT → less regularization; low BAT benefits most from tapping | ER > 19 (BAT), ER > 3999 (tapping), ER = 59.61 (interaction) | **Primary**: f10, f11, f12 (BAT × regularization × sync) |
| **Grahn & Brett 2007** | fMRI | 27 | Metric simple rhythms → greater basal ganglia + SMA activation | significant (musicians > non-musicians in PMC) | **Brain regions**: basal ganglia, SMA, PMC |
| **Hoddinott & Grahn 2024** | fMRI (7T) RSA | 26 | Putamen + SMA encode beat strength; RSA dissociates beat from rhythm | significant (RSA pattern dissimilarity) | **Brain regions**: putamen, SMA beat-strength encoding |
| **Niarchou et al. 2022** | GWAS | 606,825 | 69 loci for beat synchronization; SNP heritability 13-16% | h² = 0.13-0.16, r = -0.40 (self-report vs. tapping) | **Individual differences**: genetic basis for BAT |
| **Scartozzi et al. 2024** | EEG | 57 | Beta power at accented beats correlates with perceptual abilities | r = 0.42 (p = 0.001, Bonferroni), d' = 1.65 | **f11 beat alignment**: neural marker for BAT |
| **Lazzari et al. 2025** | TMS | 111 | Right caudal dPMC causally involved in beat perception | OR = 22.16 (on-beat responses) | **Brain regions**: right dPMC causal role |
| **Dalla Bella et al. 2024** | ML + BAASTA | 79 | Perception-motor interaction classifies rhythmic ability | d = 1.8 (musician classification, ~90% accuracy) | **f11 + f12**: perception-motor interactions key |
| **Mansuri et al. 2022** | Psychophysics + Bayesian | 7 | Systematic regularization errors in rhythm perception; BELL loss function | significant (Bayesian model fit) | **f10 regularization**: quantifies temporal distortion |
| **Large et al. 2023** | Review (dynamical systems) | — | Cross-cultural regularization toward integer ratios; oscillator entrainment models | — (review) | **Theoretical**: f10 regularization, entrainment framework |
| **Repp 2005** | Review | — | Comprehensive SMS literature: phase correction, period correction, individual differences | — (review, 200+ studies) | **Theoretical**: f12 synchronization mechanisms |
| **Gregor et al. 2025** | Behavioral (online BAT) | 62 | Online BAT reliability ICC > 0.60; stroke patients weaker beat perception | ICC > 0.60, gait asymmetry linked to BAT | **f11 validation**: BAT reliable across modalities |
| **Ross & Balasubramaniam 2022** | Mini review | — | Motor simulation supports beat prediction without overt movement; SMA + basal ganglia + cerebellum | — (review) | **Brain regions**: motor simulation hypothesis |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12): 12 papers across behavioral, fMRI, EEG, TMS, GWAS, computational
Heterogeneity:           Low (consistent: BAT modulates regularization across methods)
Quality Assessment:      β-tier (strong Bayesian behavioral + converging neural imaging)
Replication:             Robust — Rathcke 2024 (ER>3999), Grahn series (fMRI),
                         Scartozzi 2024 (EEG beta), Niarchou 2022 (GWAS n=606K)
Key Effect Sizes:        ER > 3999 tapping benefit (Rathcke 2024)
                         r = 0.42 beta-BAT correlation (Scartozzi 2024)
                         d = 1.8 musician classification (Dalla Bella 2024)
                         h² = 0.13-0.16 heritability (Niarchou 2022)
                         OR = 22.16 right dPMC beat (Lazzari 2025)
Sample Range:            n = 7-606,825 (median ~57)
```

---

## 4. R³ Input Mapping: What BARM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | BARM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength proxy | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal correlate |
| **B: Energy** | [10] | spectral_flux | Onset detection | Beat salience marker |
| **B: Energy** | [11] | onset_strength | Beat marker strength | Rhythmic event detection |
| **D: Change** | [21] | spectral_change | Tempo change tracking | Beat interval dynamics |
| **D: Change** | [22] | energy_change | Energy dynamics | Regularization detection |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Automatic entrainment | Motor-auditory coupling |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | BARM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [72] | event_density | Temporal event density | Quantifies rhythmic event rate; high density increases beat-ability regulatory demand |

**Rationale**: BARM regulates beat ability through onset_strength [11] and spectral_flux [10] as v1 proxies for rhythmic structure. event_density [72] provides a direct measure of temporal event rate that determines the regulatory load on beat tracking mechanisms — dense event streams require stronger regulatory control to maintain stable beat entrainment. This addresses the gap between onset detection (v1) and aggregate rhythmic density (v2).

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ───────────┐
R³[11] onset_strength ──────────┼──► Beat detection / tempo estimation
BEP.beat_entrainment[0:10] ────┘   Reference beat for BAT assessment

R³[21] spectral_change ─────────┐
R³[22] energy_change ───────────┼──► Tempo change tracking
BEP.motor_coupling[10:20] ─────┘   Beat-to-beat interval dynamics

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Beat strength / perceptual loudness
BEP.groove[20:30] ──────────────┘   Groove-based regularization

R³[25:33] x_l0l5 ───────────────┐
ASA.attention_gating[10:20] ────┼──► Motor-auditory coupling
H³ periodicity/velocity tuples ┘   Sensorimotor synchronization
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

BARM requires H³ features at BEP horizons for beat/timing tracking and ASA horizons for regularization assessment. The demand reflects individual-difference modulation of temporal perception.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 8 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 500ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 1000ms |
| 11 | onset_strength | 3 | M1 (mean) | L2 (bidi) | Mean onset strength 100ms |
| 11 | onset_strength | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Beat amplitude at 100ms |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean amplitude over 1s |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | Tempo velocity at 500ms |
| 21 | spectral_change | 8 | M14 (periodicity) | L0 (fwd) | Tempo periodicity 500ms |
| 22 | energy_change | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |
| 25 | x_l0l5[0] | 8 | M0 (value) | L2 (bidi) | Coupling value at 500ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 25 | x_l0l5[0] | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s |

**v1 demand**: 14 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for BARM from G[65:75] and J[94:114].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 66 | beat_strength | G | 3 | M0 (value) | L2 | Perceptual beat strength for BAT at 100ms |
| 107 | spectral_contrast_1 | J | 8 | M0 (value) | L2 | Spectral contrast for tempo dynamics at 500ms |

**v2 projected**: 2 tuples
**Total projected**: 16 tuples of 294,912 theoretical = 0.0054%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | BARM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Beat tracking for BAT | **1.0** (primary) |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor synchronization | **0.9** |
| **BEP** | Groove Processing | BEP[20:30] | Regularization drive | 0.7 |
| **ASA** | Scene Analysis | ASA[0:10] | Auditory pattern segmentation | 0.4 |
| **ASA** | Attention Gating | ASA[10:20] | Beat attention modulation | 0.6 |
| **ASA** | Salience Weighting | ASA[20:30] | Beat salience for BAT | 0.5 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
BARM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f10_regularization_tend  │ [0, 1] │ Bias toward isochrony.
    │                          │        │ f10 = σ(0.35 * (1-BAT) * groove_mean
    │                          │        │       + 0.35 * tempo_periodicity
    │                          │        │       + 0.30 * mean(BEP.groove[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f11_beat_alignment       │ [0, 1] │ Individual BAT ability level.
    │                          │        │ f11 = σ(0.40 * beat_periodicity_1s
    │                          │        │       + 0.30 * mean(BEP.beat[0:10])
    │                          │        │       + 0.30 * onset_periodicity_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f12_sync_benefit         │ [0, 1] │ Movement enhancement effect.
    │                          │        │ f12 = σ(0.40 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * coupling_period_1s
    │                          │        │       + 0.30 * (1-f11) * motor_mean)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ veridical_perception     │ [0, 1] │ α·BAT + β·Exposure + γ·Interaction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ regularization_effect    │ [0, 1] │ Regularization magnitude f(BAT).

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ beat_alignment_accuracy  │ [0, 1] │ BEP beat-locked alignment.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ regularization_strength  │ [0, 1] │ BEP groove-driven regularization.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ beat_accuracy_pred_0.75s │ [0, 1] │ Veridical perception prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ sync_benefit_pred        │ [0, 1] │ Trial-level movement benefit.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ individual_diff_pred     │ [0, 1] │ Session-level BAT screening.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Veridical Perception Function

```
Veridical_Perception = α·BAT + β·Exposure_Type + γ·(BAT × Exposure)

Parameters:
    BAT = Beat Alignment Test score [0-1]
    Exposure_Type = Listen-Only: 0, Listen-and-Tap: 1
    α = Main effect of BAT (positive)
    β = Main effect of tapping (positive)
    γ = Interaction (negative: low BAT gains more)

Evidence Ratios:
    High BAT → less regularization:    ER > 19 (strong)
    Tap-exposure enhances veridicality: ER > 3999 (decisive)
    Low BAT benefits most from tapping: ER = 59.61 (strong)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f10: Regularization Tendency
f10 = σ(0.35 * (1 - beat_alignment) * groove_mean
       + 0.35 * tempo_periodicity_500ms
       + 0.30 * mean(BEP.groove[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f11: Beat Alignment
f11 = σ(0.40 * beat_periodicity_1s
       + 0.30 * mean(BEP.beat_entrainment[0:10])
       + 0.30 * onset_periodicity_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f12: Synchronization Benefit
f12 = σ(0.40 * mean(BEP.motor_coupling[10:20])
       + 0.30 * coupling_periodicity_1s
       + 0.30 * (1 - f11) * motor_coupling_mean)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | BARM Function |
|--------|-----------------|----------|---------------|---------------|
| **SMA** (Supplementary Motor Area) | 0, -6, 58 | 5 | fMRI (Grahn & Brett 2007, Hoddinott & Grahn 2024) | Beat-strength encoding, temporal regularization |
| **Putamen** | ±12, 8, -4 | 4 | fMRI RSA (Hoddinott & Grahn 2024), fMRI (Grahn & Brett 2007) | Beat perception, metric structure encoding |
| **Right dPMC** (dorsal premotor cortex) | 32, -4, 58 | 3 | TMS (Lazzari et al. 2025, OR=22.16) | Causal role in beat perception (right-lateralized) |
| **PMC** (bilateral premotor cortex) | ±40, -8, 54 | 3 | fMRI (Grahn & Brett 2007, musicians > non-musicians) | Motor preparation for beat tracking |
| **ACC** (Anterior Cingulate Cortex) | 0, 24, 32 | 2 | Literature inference | Timing error monitoring |
| **Cerebellum** | 0, -60, -20 | 3 | fMRI (Grahn & Brett 2007), review (Ross & Balasubramaniam 2022) | Beat timing precision, error correction |
| **STG** (Superior Temporal Gyrus) | ±58, -20, 8 | 3 | EEG (Scartozzi et al. 2024, beta r=0.42) | Beat perception, rhythmic pattern analysis |
| **Anterior Insula** | ±34, 18, -4 | 2 | Salience network node | Individual difference modulation of beat salience |

---

## 9. Cross-Unit Pathways

### 9.1 BARM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BARM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  BARM.beat_alignment ────────────► SNEM (modulates entrainment strength)  │
│  BARM.regularization_tendency ───► DGTP (individual differences)          │
│  BARM.sync_benefit ──────────────► STANM (network configuration)          │
│                                                                             │
│  CROSS-UNIT (ASU → STU):                                                   │
│  BARM.beat_alignment ────────────► STU (sensorimotor timing precision)    │
│  BARM.individual_diff_pred ──────► STU (trait-level modulation)           │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► BARM (beat/motor/groove, primary)      │
│  ASA mechanism (30D) ────────────► BARM (attention/salience)              │
│  R³ (~12D) ──────────────────────► BARM (direct spectral features)        │
│  H³ (14 tuples) ─────────────────► BARM (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **BAT independence** | Low BAT should show stronger regularization | **Confirmed** |
| **Tapping benefit** | Movement should enhance veridical perception | **Confirmed** |
| **Interaction** | Low BAT should benefit more from tapping | **Confirmed** |
| **Neural correlates** | BAT should correlate with SMA/PMC activity | Testable |
| **Training effects** | Musical training should increase BAT | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class BARM(BaseModel):
    """Beat Ability Regulatory Model.

    Output: 10D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "BARM"
    UNIT = "ASU"
    TIER = "β1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP", "ASA")

    ALPHA_BAT = 0.7        # BAT main effect weight
    BETA_TAP = 0.5         # Tapping main effect
    GAMMA_INTERACT = -0.3  # Interaction (negative)
    TAU_DECAY = 4.0        # Integration window (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for BARM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: beat tracking ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 8, 14, 2),    # spectral_flux, 500ms, periodicity, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 3, 1, 2),     # onset_strength, 100ms, mean, bidi
            (11, 16, 14, 2),   # onset_strength, 1000ms, periodicity, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
            # ── Timing dynamics ──
            (21, 8, 8, 0),     # spectral_change, 500ms, velocity, fwd
            (21, 8, 14, 0),    # spectral_change, 500ms, periodicity, fwd
            (22, 8, 8, 0),     # energy_change, 500ms, velocity, fwd
            # ── Motor-auditory coupling ──
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 8, 0, 2),     # x_l0l5[0], 500ms, value, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 21, 2),   # x_l0l5[0], 1000ms, zero_crossings, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]

        # ASA sub-sections
        asa_attn = asa[..., 10:20]

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)
        onset_period_1s = h3_direct[(11, 16, 14, 2)].unsqueeze(-1)
        tempo_period_500ms = h3_direct[(21, 8, 14, 0)].unsqueeze(-1)
        coupling_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E ═══
        f11 = torch.sigmoid(
            0.40 * beat_period_1s
            + 0.30 * bep_beat.mean(-1, keepdim=True)
            + 0.30 * onset_period_1s
        )
        f10 = torch.sigmoid(
            0.35 * (1 - f11) * bep_groove.mean(-1, keepdim=True)
            + 0.35 * tempo_period_500ms
            + 0.30 * bep_groove.mean(-1, keepdim=True)
        )
        f12 = torch.sigmoid(
            0.40 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * coupling_period_1s
            + 0.30 * (1 - f11) * bep_motor.mean(-1, keepdim=True)
        )

        # ═══ LAYER M ═══
        veridical = torch.sigmoid(0.5 * f11 + 0.5 * f12)
        reg_effect = torch.sigmoid(0.5 * f10 + 0.5 * (1 - f11))

        # ═══ LAYER P ═══
        beat_acc = bep_beat.mean(-1, keepdim=True)
        reg_strength = torch.sigmoid(
            0.5 * bep_groove.mean(-1, keepdim=True)
            + 0.5 * f10
        )

        # ═══ LAYER F ═══
        beat_pred = torch.sigmoid(0.5 * f11 + 0.5 * beat_period_1s)
        sync_pred = torch.sigmoid(0.5 * f12 + 0.5 * coupling_period_1s)
        indiv_pred = f11

        return torch.cat([
            f10, f11, f12,                          # E: 3D
            veridical, reg_effect,                   # M: 2D
            beat_acc, reg_strength,                  # P: 2D
            beat_pred, sync_pred, indiv_pred,        # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (Rathcke 2024 primary + 11 converging studies) | Multi-method evidence |
| **Effect Sizes** | 8+ significant | ER>3999, r=0.42, d=1.8, h²=0.16, OR=22.16 |
| **Sample Range** | n = 7–606,825 (median ~57) | Behavioral, fMRI, EEG, TMS, GWAS |
| **Evidence Modality** | Behavioral, fMRI, EEG, TMS, GWAS, computational | Multi-modal convergence |
| **Falsification Tests** | 3/5 confirmed | Moderate validity |
| **R³ Features Used** | ~12D of 49D | Energy + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing (primary) |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Rathcke, T., et al. (2024)**. Beat alignment ability modulates perceptual regularization and sensorimotor synchronization benefits. *Journal of Experimental Psychology: Human Perception and Performance*, (in press).

2. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. `Literature/c3: Rhythm and Beat Perception in Motor Areas of the Brain`

3. **Hoddinott, K., & Grahn, J. A. (2024)**. Neural representations of beat and rhythm in motor areas of the brain. *NeuroImage*. `Literature/c3: neural-representations-of-beat-and-rhythm-in-motor`

4. **Niarchou, M., Gustavson, D. E., Sathirapongsasuti, J. F., et al. (2022)**. Genome-wide association study of musical beat synchronization demonstrates high polygenicity. *Nature Human Behaviour*, 6, 1292-1309. `Literature/c3: genome-wide-association-study-of-musical-beat-sync`

5. **Scartozzi, S., Bhattacharya, J., Bhatt, S., & Bhatt, G. (2024)**. The neural correlates of spontaneous beat processing. *Neuropsychologia*. `Literature/c3: the-neural-correlates-of-spontaneous-beat-processi`

6. **Lazzari, M., Villata, S., Molinaro, N., Mas-Herrero, E., et al. (2025)**. Topography of functional organization of beat perception in the premotor cortex. *Current Biology*. `Literature/c3: topography-of-functional-organization-of-beat-perc`

7. **Dalla Bella, S., Farrugia, N., Benoit, C.-E., Begel, V., et al. (2024)**. Unravelling individual rhythmic abilities using machine learning. *Scientific Reports*. `Literature/c3: Unravelling individual rhythmic abilities using machine learning`

8. **Mansuri, A., Aleem, H., & Grzywacz, N. M. (2022)**. Systematic errors in the perception of rhythm. *Attention, Perception, & Psychophysics*. `Literature/c3: Systematic errors in the perception of rhythm`

9. **Large, E. W., Herrera, J. A., & Velasco, M. J. (2023)**. Dynamic models for musical rhythm perception and coordination. *Frontiers in Computational Neuroscience*. `Literature/c3: dynamic-models-for-musical-rhythm-perception-and-c`

10. **Repp, B. H. (2005)**. Sensorimotor synchronization: A review of the tapping literature. *Psychonomic Bulletin & Review*, 12(6), 969-992.

11. **Gregor, S., Bakan, J. A., Engel, L., Ross, B., & Patterson, K. K. (2025)**. Feasibility and reliability of an online version of the beat alignment test in neurotypical adults and people with stroke. `Literature/c3: Feasibility and reliability of an online version of the beat alignment test in`

12. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives on entrainment, simulation, and prediction. `Literature/c3: Time Perception for Musical Rhythms Sensorimotor Perspectives on Entrainment, Si`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — same |
| Temporal | HC⁰ mechanisms (NPL, PTM, GRV) | BEP (30D) + ASA (30D) mechanisms | BEP + ASA — same |
| Beat tracking | S⁰.L4.velocity_T[15] + HC⁰.NPL | R³.spectral_flux[10] + BEP.beat_entrainment | Same — verified |
| Regularization | S⁰.L9.std_T[108] + HC⁰.PTM | R³.spectral_change[21] + BEP.groove | Same — verified |
| Synchronization | S⁰.X_L0L1[128:136] + HC⁰.GRV | R³.x_l0l5[25:33] + BEP.motor_coupling | Same — verified |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) | 14 tuples — same |
| Total demand | 12/2304 = 0.52% | 14/2304 = 0.61% | 14/2304 = 0.61% |
| Output | 10D | 10D (same) | 10D — same |
| Papers | 1 | 4 | **12** (+8 new) |
| Brain regions | 2 | 4 | **8** (+4 new: putamen, dPMC, cerebellum, STG) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **NPL → BEP.beat_entrainment** [0:10]: Neural phase locking for beat tracking maps to BEP's beat frequency monitoring.
- **PTM → BEP.groove** [20:30] + H³ velocity tuples: Predictive timing maps to BEP's groove processing and H³ temporal dynamics.
- **GRV → BEP.motor_coupling** [10:20]: Groove/motor coupling maps to BEP's sensorimotor synchronization.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
