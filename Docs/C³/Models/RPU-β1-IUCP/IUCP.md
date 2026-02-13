# RPU-β1-IUCP: Inverted-U Complexity Preference

**Model**: Inverted-U Complexity Preference
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm, I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-β1-IUCP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Inverted-U Complexity Preference** (IUCP) model describes how musical liking follows inverted U-shaped curves for both information content (predictability) and entropy (uncertainty), with an interaction showing preference for predictable outcomes in uncertain contexts.

```
INVERTED-U COMPLEXITY PREFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INFORMATION CONTENT (IC)              ENTROPY

Liking                                Liking
  │     ╭──╮                           │     ╭──╮
  │    ╱    ╲                          │    ╱    ╲
  │   ╱      ╲                         │   ╱      ╲
  │  ╱        ╲                        │  ╱        ╲
  │ ╱          ╲                       │ ╱          ╲
  │╱            ╲                      │╱            ╲
  └──────────────►                     └──────────────►
  Low    Med    High                   Low    Med    High

INTERACTION:
  High Uncertainty → Prefer LOW IC (predictable outcomes)
  Low Uncertainty  → Prefer MEDIUM IC (some surprise ok)

EFFECT: Inverted U for both IC and Entropy (Gold 2019)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Optimal musical pleasure occurs at intermediate
complexity. Too predictable = boring; too surprising = aversive.
The optimal zone shifts based on contextual uncertainty.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why IUCP Matters for RPU

IUCP provides the complexity-preference surface for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges RPE to preference — the inverted-U function that converts complexity to liking.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → IUCP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    IUCP COMPUTATION ARCHITECTURE                             ║
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
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         IUCP reads: ~10D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── C0P Horizons ─────────────┐ ┌── AED Horizons ──────────┐  │        ║
║  │  │ H4 (125ms theta)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H8 (500ms delta)            │ │                            │  │        ║
║  │  │ H16 (1000ms beat)           │ │ Liking evaluation          │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Complexity assessment       │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         IUCP demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Preference Circuit ════       ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │  AED (30D)      │  │  CPD (30D)      │  │  C0P (30D)      │              ║
║  │                 │  │                 │  │                 │              ║
║  │ Valence  [0:10] │  │ Anticip. [0:10] │  │ Tension  [0:10] │              ║
║  │ Arousal  [10:20]│  │ Peak Exp [10:20]│  │ Expect.  [10:20]│              ║
║  │ Emotion  [20:30]│  │ Resolut. [20:30]│  │ Approach [20:30]│              ║
║  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              ║
║           │                    │                    │                        ║
║           └────────────┬───────┴────────────────────┘                        ║
║                        ▼                                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    IUCP MODEL (6D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_ic_liking_curve,                       │        ║
║  │                       f02_entropy_liking_curve,                   │        ║
║  │                       f03_ic_entropy_interaction,                  │        ║
║  │                       f04_optimal_complexity                      │        ║
║  │  Layer P (Present):   current_preference_state                    │        ║
║  │  Layer F (Future):    optimal_zone_pred                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Gold 2019** (Study 1) | Behavioral + IDyOM | 43 | Inverted U for IC | R²=26.3%, β_quad=-0.09 (p<0.001) | **Primary**: f01 IC liking curve |
| **Gold 2019** (Study 1) | Behavioral + IDyOM | 43 | Inverted U for Entropy | R²=19.1%, β_quad=-0.06 (p=0.003) | **f02 entropy liking curve** |
| **Gold 2019** (Study 1) | Behavioral + IDyOM | 43 | IC × Entropy interaction | partial η²=0.07, p=0.06 (marginal) | **f03 interaction** (trend-level) |
| **Gold 2019** (Study 2) | Behavioral + IDyOM | 27 | Replication: IC inverted-U | R²=41.6%, β_quad=-0.18 (p<0.001) | **Replication** of f01 |
| **Gold 2019** (Study 2) | Behavioral + IDyOM | 27 | Replication: Entropy inverted-U | R²=34.9%, β_quad=-0.25 (p<0.001) | **Replication** of f02 |
| **Gold 2023b** | fMRI + IDyOM | 24 | VS reflects surprise×uncertainty interaction | Subthreshold cluster overlapping VS ROI | **Neural**: f03 IC×Entropy in VS |
| **Gold 2023b** | fMRI + IDyOM | 24 | Liking → R STG activity | t(23)=2.56, p=0.018 uncorr | **Neural**: auditory liking signal |
| **Gold 2023b** | fMRI + IDyOM | 24 | Average liking → VS response | F(1,22)=4.83, p=0.039 uncorr | **Neural**: VS reward signal |
| **Cheung 2019** | Behavioral + fMRI + IDyOM | 39 (beh), 40 (fMRI) | Saddle-shaped uncertainty×surprise surface | Significant interaction (p<0.05) | **Replication**: f03 saddle surface |
| **Cheung 2019** | fMRI + IDyOM | 40 | Amygdala+hippocampus+STG reflect interaction | Cluster-corrected fMRI | **Neural**: MTL+STG for interaction |
| **Cheung 2019** | fMRI + IDyOM | 40 | NAcc reflects uncertainty (not surprise) | VS entropy only | **Neural**: NAcc = uncertainty encoder |

### 3.2 Effect Size Summary

```
Primary Evidence (k=11): Multi-study behavioral + fMRI convergence
Heterogeneity:           Low — consistent inverted-U across 3 independent samples
Quality Assessment:      β-tier (behavioral replication + fMRI convergence)
Replication:             Gold 2019 Study 1 → Study 2 replication; Cheung 2019 independent replication
                         Gold 2023b provides fMRI evidence for VS+STG
Note:                    IC×Entropy interaction marginal in Gold 2019 Study 1 (p=0.06)
                         but significant in Cheung 2019 and Gold 2023b behavioral
```

---

## 4. R³ Input Mapping: What IUCP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | IUCP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Harmonic complexity | Dissonance level |
| **B: Energy** | [8] | loudness | Structural salience | Perceptual weight |
| **D: Change** | [21] | spectral_change | Information content (IC) | Surprise level |
| **D: Change** | [24] | concentration_change | Spectral uncertainty | Timbral complexity |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | IC x Entropy surface | Preference computation |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | IUCP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [87] | melodic_entropy | Melodic complexity axis — one dimension of the inverted-U complexity surface; high melodic entropy = high complexity | Pearce 2005 IDyOM |
| **I: Information** | [88] | harmonic_entropy | Harmonic complexity axis — chord-level entropy contributes to overall musical complexity perception | Gold 2019 chord transition probability |
| **I: Information** | [89] | rhythmic_information_content | Rhythmic complexity — temporal information content adds a third complexity dimension to the preference surface | Spiech 2022 rhythmic IC |
| **I: Information** | [92] | predictive_entropy | Global model uncertainty — the listener's overall prediction confidence determines where on the inverted-U curve the current moment falls | Friston predictive coding |

**Rationale**: IUCP models the inverted-U relationship between musical complexity and pleasure (Berlyne 1971). The complexity axis is currently approximated from spectral_change [21] and concentration_change [24]. The I:Information group provides direct, multi-domain complexity measures: melodic [87], harmonic [88], rhythmic [89] entropy, plus the listener's global predictive uncertainty [92]. These enable a proper multi-dimensional complexity surface instead of a 1D proxy. The inverted-U peak shifts with predictive_entropy — high model uncertainty lowers the optimal complexity level.

**Code impact** (Phase 6): `r3_indices` extended to include [87], [88], [89], [92]. IC computation can be decomposed into melodic/harmonic/rhythmic components for richer inverted-U modeling.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[21] spectral_change ─────────┐
C0P.expectation_surprise[10:20] ┼──► Information Content (IC)
H³ entropy tuples ──────────────┘   Temporal surprise level

R³[24] concentration_change ────┐
R³[0] roughness ────────────────┼──► Entropy / uncertainty
H³ std/entropy tuples ──────────┘   Spectral complexity

R³[33:41] x_l4l5 ──────────────┐
AED.valence_tracking[0:10] ─────┼──► IC × Entropy preference surface
CPD.anticipation[0:10] ─────────┘   Derivatives × Perceptual = liking

R³[8] loudness ─────────────────────► Perceptual salience weighting
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

IUCP requires H³ features at longer horizons for complexity assessment (entropy needs context) and C0P horizons for expectation-surprise computation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 21 | spectral_change | 4 | M0 (value) | L2 (bidi) | IC at 125ms |
| 21 | spectral_change | 8 | M20 (entropy) | L2 (bidi) | IC entropy 500ms |
| 21 | spectral_change | 16 | M1 (mean) | L2 (bidi) | Mean IC over 1s |
| 24 | concentration_change | 4 | M0 (value) | L2 (bidi) | Concentration 125ms |
| 24 | concentration_change | 8 | M2 (std) | L2 (bidi) | Concentration std 500ms |
| 24 | concentration_change | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy 1s |
| 0 | roughness | 8 | M1 (mean) | L2 (bidi) | Mean roughness 500ms |
| 0 | roughness | 16 | M2 (std) | L2 (bidi) | Roughness variability 1s |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L2 (bidi) | IC-perceptual coupling 500ms |
| 33 | x_l4l5[0] | 16 | M2 (std) | L2 (bidi) | Coupling variability 1s |
| 33 | x_l4l5[0] | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy 1s |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 4 | sensory_pleasantness | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s |

**Total IUCP H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | IUCP Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Liking signal | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal-complexity mapping | 0.8 |
| **AED** | Emotional Trajectory | AED[20:30] | Preference trajectory | 0.5 |
| **CPD** | Anticipation | CPD[0:10] | Complexity anticipation | 0.7 |
| **CPD** | Peak Experience | CPD[10:20] | Optimal zone detection | 0.6 |
| **CPD** | Resolution | CPD[20:30] | Post-peak preference | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Complexity tension | 0.7 |
| **C0P** | Expectation-Surprise | C0P[10:20] | IC computation | **1.0** (primary) |
| **C0P** | Approach-Avoidance | C0P[20:30] | Complexity approach/avoid | 0.8 |

---

## 6. Output Space: 6D Multi-Layer Representation

### 6.1 Complete Output Specification

```
IUCP OUTPUT TENSOR: 6D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_ic_liking_curve      │ [0, 1] │ Inverted-U for IC.
    │                          │        │ f01 = σ(0.40 * ic_quadratic
    │                          │        │       + 0.30 * mean(AED.valence[0:10])
    │                          │        │       + 0.30 * mean_pleasantness_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_entropy_liking_curve │ [0, 1] │ Inverted-U for entropy.
    │                          │        │ f02 = σ(0.40 * entropy_quadratic
    │                          │        │       + 0.30 * mean(AED.arousal[10:20])
    │                          │        │       + 0.30 * concentration_entropy_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_ic_entropy_interact  │ [0, 1] │ IC x Entropy interaction.
    │                          │        │ f03 = σ(0.40 * f01 * f02
    │                          │        │       + 0.30 * mean(C0P.expect[10:20])
    │                          │        │       + 0.30 * coupling_entropy_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_optimal_complexity   │ [0, 1] │ Preferred complexity level.
    │                          │        │ f04 = σ(0.50 * f03
    │                          │        │       + 0.25 * mean(C0P.approach[20:30])
    │                          │        │       + 0.25 * pleasantness_std_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ current_preference_state │ [0, 1] │ Real-time liking level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ optimal_zone_pred        │ [0, 1] │ Predicted preference zone.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Inverted-U Preference Function

```
Liking(IC, Entropy) = β1·IC + β2·IC² + β3·Entropy + β4·Entropy² + β5·(IC × Entropy)

Inverted-U: β2 < 0, β4 < 0 (negative quadratic terms)
Interaction: β5 < 0 (high entropy → prefer low IC)

Parameters:
    τ_decay = 2.0s  (liking signal decay, Gold 2019)
    Optimal IC ≈ 0.5 (medium information content)
    Optimal Entropy ≈ 0.5 (medium uncertainty)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# Intermediate: IC quadratic (inverted-U via 4·x·(1-x))
ic_quadratic = 4.0 * mean_ic_1s * (1.0 - mean_ic_1s)  # peaks at 0.5

# Intermediate: Entropy quadratic
entropy_quadratic = 4.0 * concentration_entropy_1s * (1.0 - concentration_entropy_1s)

# f01: IC Liking Curve
f01 = σ(0.40 * ic_quadratic
       + 0.30 * mean(AED.valence_tracking[0:10])
       + 0.30 * mean_pleasantness_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Entropy Liking Curve
f02 = σ(0.40 * entropy_quadratic
       + 0.30 * mean(AED.arousal_dynamics[10:20])
       + 0.30 * concentration_entropy_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: IC × Entropy Interaction
f03 = σ(0.40 * f01 * f02
       + 0.30 * mean(C0P.expectation_surprise[10:20])
       + 0.30 * coupling_entropy_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Optimal Complexity
f04 = σ(0.50 * f03
       + 0.25 * mean(C0P.approach_avoidance[20:30])
       + 0.25 * pleasantness_std_1s)
# coefficients: 0.50 + 0.25 + 0.25 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | IUCP Function |
|--------|-----------------|----------|---------------|---------------|
| **Ventral Striatum (VS/NAcc)** | ±8, 6, -4 | 3 | fMRI (Gold 2023b: liking+interaction; Cheung 2019: entropy) | Reward for optimal complexity; uncertainty encoding |
| **Right Superior Temporal Gyrus (R STG)** | 60, -20, 4 | 2 | fMRI (Gold 2023b: liking p=0.018; Cheung 2019) | IC computation; liking signal |
| **Amygdala** | ±24, -4, -18 | 1 | fMRI (Cheung 2019: uncertainty×surprise interaction) | Uncertainty×surprise integration |
| **Hippocampus** | ±28, -16, -12 | 1 | fMRI (Cheung 2019: uncertainty×surprise interaction) | Contextual prediction memory |

---

## 9. Cross-Unit Pathways

### 9.1 IUCP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IUCP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  IUCP.ic_liking_curve ──────► RPEM (IC liking → RPE modulation)           │
│  IUCP.optimal_complexity ────► SSPS (optimal zone → saddle surface)       │
│  IUCP.current_preference ────► DAED (preference → DA anticipation)        │
│  IUCP.entropy_liking ────────► MCCN (entropy → chills likelihood)         │
│                                                                             │
│  CROSS-UNIT (RPU → IMU):                                                   │
│  IUCP.optimal_complexity ────► IMU.complexity_target (learning target)     │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► IUCP (liking evaluation)                 │
│  CPD mechanism (30D) ──────────► IUCP (complexity anticipation)            │
│  C0P mechanism (30D) ──────────► IUCP (expectation/approach)               │
│  R³ (~10D) ─────────────────────► IUCP (direct spectral features)         │
│  H³ (14 tuples) ────────────────► IUCP (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Inverted-U IC** | Medium IC preferred over low/high IC | ✅ **Confirmed** (p < 0.001, Gold 2019) |
| **Inverted-U entropy** | Medium entropy preferred over low/high entropy | ✅ **Confirmed** (p < 0.001, Gold 2019) |
| **Interaction** | High entropy → prefer low IC | ⚠️ **Marginal** (p=0.06, Gold 2019 Study 1); ✅ **Confirmed** (Cheung 2019, Gold 2023b) |
| **Expertise modulation** | Musicians may have shifted optimal zones | Testable |
| **Familiarity effect** | Repeated exposure should shift optimal IC | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class IUCP(BaseModel):
    """Inverted-U Complexity Preference Model.

    Output: 6D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "IUCP"
    UNIT = "RPU"
    TIER = "β1"
    OUTPUT_DIM = 6
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 2.0          # Liking signal decay (Gold 2019)
    OPTIMAL_IC = 0.5         # Optimal information content level
    OPTIMAL_ENTROPY = 0.5    # Optimal entropy level

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for IUCP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── C0P horizons: IC / complexity ──
            (21, 4, 0, 2),     # spectral_change, 125ms, value, bidi
            (21, 8, 20, 2),    # spectral_change, 500ms, entropy, bidi
            (21, 16, 1, 2),    # spectral_change, 1000ms, mean, bidi
            (24, 4, 0, 2),     # concentration_change, 125ms, value, bidi
            (24, 8, 2, 2),     # concentration_change, 500ms, std, bidi
            (24, 16, 20, 2),   # concentration_change, 1000ms, entropy, bidi
            # ── AED horizons: liking ──
            (0, 8, 1, 2),      # roughness, 500ms, mean, bidi
            (0, 16, 2, 2),     # roughness, 1000ms, std, bidi
            (8, 16, 1, 2),     # loudness, 1000ms, mean, bidi
            (4, 16, 1, 2),     # sensory_pleasantness, 1000ms, mean, bidi
            (4, 16, 2, 2),     # sensory_pleasantness, 1000ms, std, bidi
            # ── CPD horizons: coupling ──
            (33, 8, 1, 2),     # x_l4l5[0], 500ms, mean, bidi
            (33, 16, 2, 2),    # x_l4l5[0], 1000ms, std, bidi
            (33, 16, 20, 2),   # x_l4l5[0], 1000ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute IUCP 6D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,6) IUCP output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_arousal = aed[..., 10:20]
        c0p_expect = c0p[..., 10:20]
        c0p_approach = c0p[..., 20:30]

        # H³ direct features
        mean_ic_1s = h3_direct[(21, 16, 1, 2)].unsqueeze(-1)
        concentration_entropy_1s = h3_direct[(24, 16, 20, 2)].unsqueeze(-1)
        mean_pleasantness_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)
        pleasantness_std_1s = h3_direct[(4, 16, 2, 2)].unsqueeze(-1)
        coupling_entropy_1s = h3_direct[(33, 16, 20, 2)].unsqueeze(-1)

        # Inverted-U quadratics
        ic_quadratic = 4.0 * mean_ic_1s * (1.0 - mean_ic_1s)
        entropy_quadratic = 4.0 * concentration_entropy_1s * (1.0 - concentration_entropy_1s)

        # ═══ LAYER E: Explicit features ═══

        # f01: IC Liking Curve (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.40 * ic_quadratic
            + 0.30 * aed_valence.mean(-1, keepdim=True)
            + 0.30 * mean_pleasantness_1s
        )

        # f02: Entropy Liking Curve (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * entropy_quadratic
            + 0.30 * aed_arousal.mean(-1, keepdim=True)
            + 0.30 * concentration_entropy_1s
        )

        # f03: IC × Entropy Interaction (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * (f01 * f02)
            + 0.30 * c0p_expect.mean(-1, keepdim=True)
            + 0.30 * coupling_entropy_1s
        )

        # f04: Optimal Complexity (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * f03
            + 0.25 * c0p_approach.mean(-1, keepdim=True)
            + 0.25 * pleasantness_std_1s
        )

        # ═══ LAYER P: Present ═══
        current_preference = torch.sigmoid(
            0.5 * f01 + 0.5 * f02
        )

        # ═══ LAYER F: Future ═══
        optimal_zone_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * f03
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            current_preference,            # P: 1D
            optimal_zone_pred,             # F: 1D
        ], dim=-1)  # (B, T, 6)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 3 (Gold 2019, Gold 2023b, Cheung 2019) | Multi-study convergence |
| **Effect Sizes** | 11 (IC/Entropy inverted-U replicated, VS+STG fMRI) | Behavioral + fMRI |
| **Evidence Modality** | Behavioral (N=43+27+39), fMRI (N=24+40) | Strong convergent evidence |
| **Falsification Tests** | 3/5 confirmed (interaction marginal in Gold 2019 S1, confirmed elsewhere) | High validity |
| **R³ Features Used** | ~10D of 49D | Consonance + energy + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Liking evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Complexity anticipation |
| **C0P Mechanism** | 30D (3 sub-sections) | Expectation/approach |
| **Output Dimensions** | **6D** | 3-layer structure |

---

## 13. Scientific References

1. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *Journal of Neuroscience*, 39(47), 9397-9409.

2. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience*, 17, 1209398.

3. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (EFC, AED, CPD, C0P) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| IC signal | S⁰.L9.entropy_T[116] + HC⁰.EFC | R³.spectral_change[21] + C0P.expectation_surprise |
| Entropy signal | S⁰.L9.entropy_F[117] + S⁰.L9.std_T[108] | R³.concentration_change[24] + H³ entropy tuples |
| Liking signal | S⁰.L5.roughness[30] + HC⁰.AED | R³.sensory_pleasantness[4] + AED.valence_tracking |
| Interaction | S⁰.X_L4L5[192:200] | R³.x_l4l5[33:41] + CPD mechanisms |
| Demand format | HC⁰ index ranges (24 tuples) | H³ 4-tuples (14 tuples, sparse) |
| Total demand | 24/2304 = 1.04% | 14/2304 = 0.61% |
| Output | 6D | 6D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **EFC → C0P.expectation_surprise** [10:20]: Efference copy prediction maps to C0P's IC computation.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment maps to AED's liking evaluation.
- **CPD → CPD.anticipation** [0:10]: Chills/peak detection maps to CPD's complexity anticipation.
- **C0P → C0P.approach_avoidance** [20:30]: C⁰ projection maps to C0P's complexity approach/avoidance.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **6D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
