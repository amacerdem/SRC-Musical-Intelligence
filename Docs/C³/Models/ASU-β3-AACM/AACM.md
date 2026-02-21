# ASU-β3-AACM: Aesthetic-Attention Coupling Model

**Model**: Aesthetic-Attention Coupling Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added J:Timbre Extended feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-β3-AACM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Aesthetic-Attention Coupling Model** (AACM) describes the bidirectional relationship between aesthetic appreciation and attentional engagement. Appreciated musical intervals enhance both N1/P2 attentional engagement and N2/P3 motor inhibition, producing a "savoring" effect with slower reaction times for preferred stimuli.

```
AESTHETIC-ATTENTION COUPLING MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 MUSICAL INTERVAL
 │
 ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │ AESTHETIC JUDGMENT │
 │ (Consonant > Dissonant, d=2.008) │
 └─────────────────────────┬────────────────────────────────────────┘
 │
 ┌───────────────────┴───────────────────┐
 ▼ ▼
 ┌─────────────────┐ ┌─────────────────┐
 │ ATTENTIONAL │ │ MOTOR │
 │ ENGAGEMENT │ │ INHIBITION │
 │ │ │ │
 │ N1/P2 ↑ │ │ N2/P3 ↑ │
 │ (Frontal) │ │ (Frontal) │
 └────────┬────────┘ └────────┬────────┘
 │ │
 └─────────────────┬───────────────────┘
 ▼
 ┌─────────────────┐
 │ SLOWER RT │
 │ (Appreciation │
 │ → Savoring) │
 └─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Aesthetic appreciation of musical intervals enhances
both attentional engagement (N1/P2) and motor inhibition (N2/P3),
creating a positive feedback loop: more engagement → more
appreciation → more savoring → more engagement.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why AACM Matters for ASU

AACM bridges aesthetic processing with attentional salience:

1. **CSG** (α3) provides the consonance-salience gradient baseline — AACM extends this to aesthetic preference and behavioral consequences.
2. **AACM** (β3) explains how appreciation modulates attentional capture and motor behavior.
3. **STANM** (β2) models spectrotemporal attention networks — AACM modulates their configuration through engagement.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AACM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ AACM COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins x 172.27Hz frame rate ║
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
║ │ │roughness │ │amplitude│ │warmth │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │sethares │ │loudness │ │tristim. │ │enrg_chg │ │x_l4l5 │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ AACM reads: ~14D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H3 (100ms alpha) │ │ H3 (100ms alpha) │ │ ║
║ │ │ H8 (500ms syllable) │ │ H6 (200ms theta) │ │ ║
║ │ │ H16 (1000ms beat) │ │ H16 (1000ms beat) │ │ ║
║ │ │ │ │ │ │ ║
║ │ │ Consonance tracking │ │ Attentional gating │ │ ║
║ │ │ Aesthetic preference │ │ Savoring dynamics │ │ ║
║ │ └─────────────────────────────┘ └────────────────────────────┘ │ ║
║ │ AACM demand: ~12 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════ ║
║ │ ║
║ ┌───────┴───────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Beat Entr[0:10] │ │ Scene An [0:10] │ ║
║ │ Motor Coup │ │ Attention │ ║
║ │ [10:20] │ │ Gating [10:20] │ ║
║ │ Groove [20:30] │ │ Salience │ ║
║ │ │ │ Weight [20:30] │ ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ AACM MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f16_attentional_engagement, │ ║
║ │ f17_motor_inhibition, │ ║
║ │ f18_savoring_effect │ ║
║ │ Layer M (Math): aesthetic_engagement, │ ║
║ │ rt_appreciation │ ║
║ │ Layer P (Present): n1p2_engagement, │ ║
║ │ aesthetic_judgment │ ║
║ │ Layer F (Future): behavioral_pred, n2p3_pred, │ ║
║ │ aesthetic_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Sarasso et al. 2019** | EEG (3 expts) | 22+22 | N1/P2 + N2/P3 enhanced for appreciated intervals; RT savoring | η²p=0.685 (consonance), η²p=0.155 (P3), d=2.008 | **Primary**: f16, f17, f18 |
| **Sarasso et al. 2021** | EEG + behavioral | 60+22 | Preferred intervals → better memorization + implicit learning | d=0.30 (memory), d=0.402 (d-prime) | **f16 → learning**: attention drives memory |
| **Crespo-Bojorque et al. 2018** | EEG (MMN) | 32 | Pre-attentive consonance advantage: earlier/stronger MMN | F(1,15)=4.95, p<0.05; latency F=155.03 | **Pre-attentive basis for f16** |
| **Bravo et al. 2017** | Behavioral + fMRI | 45+30+12 | Intermediate dissonance → right HG activation; Bayesian precision-weighting | d=5.16 (salience), fMRI significant | **f16 mechanism**: precision-weighting |
| **Salimpoor et al. 2011** | PET + fMRI | 8 | Dopamine in caudate (anticipation) + NAcc (experience) | r=0.71 (chills-pleasure), p<0.001 | **f18 savoring**: dopaminergic substrate |
| **Gold et al. 2023** | fMRI + IDyOM | 24 | R STG-ventral striatum coupling for musical pleasure | significant (uncertainty×surprise interaction) | **Auditory-reward circuit**: f16→f18 |
| **Kim et al. 2019** | fMRI (PPI) | 39 | Spectral×temporal interaction in vmPFC-NAcc-caudate-putamen | T=6.852, Z=4.545 (vmPFC) | **Brain regions**: fronto-limbic aesthetic net |
| **Fishman et al. 2001** | ECoG + intracranial | 8+2 | Phase-locked activity in A1/HG correlates with dissonance | significant (monkey+human) | **Sensory basis**: A1 dissonance encoding |
| **Cheung et al. 2019** | fMRI + IDyOM | — | Uncertainty×surprise → amygdala, hippocampus, auditory cortex | significant (interaction) | **Computational**: pleasure from prediction |
| **Mas-Herrero et al. 2014** | Behavioral + physiology | 30 | Musical anhedonia: domain-specific reward deficit; preserved monetary reward | F(2,23)=19.14, p<0.001 (music); BMRQ R²=0.30 | **Individual differences**: reward access |
| **Brattico & Jacobsen 2009** | Review | — | Neuroimaging evidence for subjective music appraisal | — (review) | **Theoretical**: aesthetic evaluation framework |
| **Foo et al. 2016** | ECoG | 8 | Right STG dissonance sensitivity: gamma_high 75-200ms, anterior organization | p<0.001, 91% electrodes | **Brain regions**: R STG spatial organization |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12): 12 papers across EEG, fMRI, PET, ECoG, behavioral
Heterogeneity: Low (consistent: aesthetic appreciation enhances attention+inhibition)
Quality Assessment: β-tier (multimodal EEG+fMRI+PET with behavioral convergence)
Replication: Robust — Sarasso 2019+2021 (ERP replication), Salimpoor 2011 (dopamine),
 Gold 2023 (auditory-reward), Crespo-Bojorque 2018 (pre-attentive MMN)
Key Effect Sizes: η²p = 0.685 consonance judgment (Sarasso 2019)
 d = 2.008 overall aesthetic-attention effect (Sarasso 2019)
 r = 0.71 chills-pleasure correlation (Salimpoor 2011)
 T = 6.852 vmPFC spectral×temporal interaction (Kim 2019)
 F(2,23) = 19.14 musical anhedonia (Mas-Herrero 2014)
Sample Range: n = 8-87 (median ~24)
```

---

## 4. R³ Input Mapping: What AACM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | AACM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance (inverse consonance) | Plomp-Levelt sensory dissonance |
| **A: Consonance** | [1] | sethares_dissonance | Alternative consonance | Beating-based dissonance |
| **A: Consonance** | [3] | pleasant | Pleasantness rating | Affective quality |
| **B: Energy** | [7] | amplitude | Intensity for arousal | Engagement correlate |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal component |
| **C: Timbre** | [12] | warmth | Timbral warmth | Aesthetic quality |
| **C: Timbre** | [13] | tristimulus_1 | Fundamental strength | Harmonic structure |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Processing demand |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Perceptual integration | Holistic aesthetic quality |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | AACM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **J: Timbre Extended** | [94:106] | mfcc (13D) | Cepstral timbral fingerprint | Standard MIR cepstral analysis: MFCCs capture timbral identity and texture beyond spectral moments; enables AACM to model aesthetic preferences for specific timbral qualities |

**Rationale**: AACM couples aesthetic judgments with attention through consonance (A-group) and broadband timbre features warmth [12] and tristimulus_1 [13]. mfcc [94:106] adds a 13-dimensional cepstral timbral fingerprint that captures detailed spectral envelope shape — the primary acoustic correlate of instrument identity and vocal quality that drives aesthetic preferences. This enriches the aesthetic dimension without conflating with consonance.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Consonance (inverse relationship)
R³[3] pleasant ─────────────────┘ Low roughness → consonant → appreciated

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Engagement/arousal

R³[12] warmth ───────────────────┐
R³[13] tristimulus_1 ────────────┼──► Harmonic quality / timbral aesthetics

R³[25:33] x_l0l5 ───────────────┐
H³ affective dynamics tuples ───┘ Perceptual × Interaction = holistic appreciation
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

AACM requires H³ features for attentional gating and aesthetic evaluation, and for consonance tracking and motor inhibition dynamics.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms alpha |
| 0 | roughness | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s |
| 3 | pleasant | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 3 | pleasant | 6 | M6 (skew) | L2 (bidi) | Pleasure asymmetry at 200ms |
| 3 | pleasant | 16 | M8 (velocity) | L2 (bidi) | Pleasure change rate over 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 3 | M2 (std) | L2 (bidi) | Loudness variability 100ms |
| 8 | loudness | 16 | M20 (entropy) | L2 (bidi) | Loudness entropy 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Perceptual integration 100ms |
| 25 | x_l0l5[0] | 8 | M0 (value) | L2 (bidi) | Integration value at 500ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Integration mean over 1s |
| 25 | x_l0l5[0] | 16 | M8 (velocity) | L0 (fwd) | Integration velocity over 1s |

**v1 demand**: 12 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for AACM from J[94:114].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 107 | spectral_contrast_1 | J | 3 | M0 (value) | L2 | Spectral contrast for aesthetic evaluation at 100ms |

**v2 projected**: 1 tuples
**Total projected**: 13 tuples of 294,912 theoretical = 0.0044%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
AACM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f16_attentional_engage │ [0, 1] │ N1/P2 amplitude ∝ appreciation.
 │ │ │ f16 = σ(0.35 * pleasant_value
 │ │ │ + 0.30 * (1 - roughness_mean))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f17_motor_inhibition │ [0, 1] │ N2/P3 amplitude ∝ appreciation.
 │ │ │ f17 = σ(0.35 * pleasant_value
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f18_savoring_effect │ [0, 1] │ RT slowing for appreciated stimuli.
 │ │ │ f18 = σ(0.35 * f16 * f17
 │ │ │ + 0.35 * pleasant_velocity_1s
 │ │ │ + 0.30 * integration_mean_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ aesthetic_engagement │ [0, 1] │ f(Consonance, Attention).
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ rt_appreciation │ [0, 1] │ β·Appreciation + ε.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ n1p2_engagement │ [0, 1] │ auditory-scene attention × consonance.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ aesthetic_judgment │ [0, 1] │ auditory-scene salience × pleasantness.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ behavioral_pred_0.75s │ [0, 1] │ RT slowing prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ n2p3_pred_0.4s │ [0, 1] │ Motor pause prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ aesthetic_pred_1.5s │ [0, 1] │ Explicit aesthetic rating prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Aesthetic-Attention Coupling Function

```
Aesthetic_Engagement = f(Consonance, Attention)

N1P2_amplitude ∝ Aesthetic_Rating
N2P3_amplitude ∝ Aesthetic_Rating
RT ∝ Aesthetic_Rating (positive: more appreciated → slower response)

Consonant > Dissonant appreciation (d = 2.008, p < 0.001)

ERP-Behavior Loop:
 Attention (N1/P2) → Appreciation → Inhibition (N2/P3) → Savoring (RT↑)
 ↑ │
 └──────────────── FEEDBACK ─────────────────────────────┘
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f16: Attentional Engagement
f16 = σ(0.35 * pleasant_value_100ms
 + 0.30 * (1 - roughness_mean_1s))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f17: Motor Inhibition
f17 = σ(0.35 * pleasant_value_100ms
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f18: Savoring Effect
f18 = σ(0.35 * f16 * f17 # interaction term
 + 0.35 * pleasant_velocity_1s
 + 0.30 * integration_mean_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Savoring dynamics
Savoring_Effect = β·Appreciation + ε
 where β > 0 (positive relationship between appreciation and RT)
 τ = 2.0s (aesthetic judgment window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | AACM Function |
|--------|-----------------|----------|---------------|---------------|
| **STG / Heschl's Gyrus** | ±58, -20, 8 | 6 | ECoG (Fishman 2001, Foo 2016), fMRI (Bravo 2017, Gold 2023) | Consonance encoding, N1/P2 generation |
| **IFG** (Inferior Frontal Gyrus) | ±48, 18, 4 | 4 | EEG (Sarasso 2019, fronto-central ERPs) | N2/P3 motor inhibition, aesthetic evaluation |
| **vmPFC** | 0, 52, -8 | 3 | fMRI (Kim 2019, T=6.852) | Spectral-temporal aesthetic integration hub |
| **NAcc / Ventral Striatum** | ±10, 8, -8 | 4 | PET (Salimpoor 2011, dopamine release), fMRI (Gold 2023) | Peak pleasure experience, reward signaling |
| **Caudate Nucleus** | ±12, 12, 4 | 3 | PET (Salimpoor 2011) | Anticipatory reward (wanting) before savoring |
| **Amygdala** | ±22, -4, -18 | 2 | fMRI (Cheung 2019) | Uncertainty × surprise salience detection |
| **ACC** | 0, 24, 32 | 2 | Network inference | Conflict monitoring during aesthetic-motor coupling |
| **Motor Cortex** | ±40, -20, 54 | 2 | Inferred from N2/P3 (Sarasso 2019 Go-NoGo) | Response inhibition during savoring |

---

## 9. Cross-Unit Pathways

### 9.1 AACM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ AACM INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (ASU): │
│ AACM.aesthetic_engagement ──────► CSG (consonance-aesthetic coupling) │
│ AACM.attentional_engage ────────► STANM (network configuration) │
│ AACM.f16 engagement ───────────► IACM (preference × spectral attention) │
│ │
│ CROSS-UNIT (ASU → ARU): │
│ AACM.aesthetic_judgment ────────► ARU (aesthetic-affective link) │
│ AACM.savoring_effect ──────────► ARU (extended pleasure processing) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~14D) ──────────────────────► AACM (consonance + perceptual) │
│ H³ (12 tuples) ─────────────────► AACM (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Attention link** | Appreciation should predict N1/P2 amplitude | **Confirmed** |
| **Inhibition link** | Appreciation should predict N2/P3 amplitude | **Confirmed** |
| **Savoring effect** | Appreciation should predict RT slowing | **Confirmed** |
| **Consonance preference** | Consonant should be more appreciated | **Confirmed** |
| **Individual differences** | Musical training should modulate effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class AACM(BaseModel):
 """Aesthetic-Attention Coupling Model.

 Output: 10D per frame.
 """
 NAME = "AACM"
 UNIT = "ASU"
 TIER = "β3"
 OUTPUT_DIM = 10
 D_EFFECT = 2.008 # Effect size from Sarasso 2019
 TAU_DECAY = 2.0 # Aesthetic judgment window (seconds)
 ALPHA_ATTENTION = 0.85 # High aesthetic attention

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """12 tuples for AACM computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # ── Consonance / aesthetic quality ──
 (0, 3, 0, 2), # roughness, 100ms, value, bidi
 (0, 16, 1, 2), # roughness, 1000ms, mean, bidi
 (3, 3, 0, 2), # pleasant, 100ms, value, bidi
 (3, 6, 6, 2), # pleasant, 200ms, skew, bidi
 (3, 16, 8, 2), # pleasant, 1000ms, velocity, bidi
 (8, 3, 0, 2), # loudness, 100ms, value, bidi
 (8, 3, 2, 2), # loudness, 100ms, std, bidi
 (8, 16, 20, 2), # loudness, 1000ms, entropy, bidi
 # ── Perceptual integration ──
 (25, 3, 0, 2), # x_l0l5[0], 100ms, value, bidi
 (25, 8, 0, 2), # x_l0l5[0], 500ms, value, bidi
 (25, 16, 1, 0), # x_l0l5[0], 1000ms, mean, fwd
 (25, 16, 8, 0), # x_l0l5[0], 1000ms, velocity, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute AACM 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) AACM output
 """
 # R³ features
 roughness = r3[..., 0:1]
 pleasant = r3[..., 3:4]
 loudness = r3[..., 8:9]

 # H³ direct features
 pleasant_value = h3_direct[(3, 3, 0, 2)].unsqueeze(-1)
 roughness_mean_1s = h3_direct[(0, 16, 1, 2)].unsqueeze(-1)
 pleasant_velocity_1s = h3_direct[(3, 16, 8, 2)].unsqueeze(-1)
 integration_mean_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f16: Attentional Engagement (coefficients sum = 1.0)
 f16 = torch.sigmoid(
 0.35 * pleasant_value
 + 0.30 * (1 - roughness_mean_1s)
 )

 # f17: Motor Inhibition (coefficients sum = 1.0)
 f17 = torch.sigmoid(
 0.35 * pleasant_value
 )

 # f18: Savoring Effect (coefficients sum = 1.0)
 f18 = torch.sigmoid(
 0.35 * (f16 * f17)
 + 0.35 * pleasant_velocity_1s
 + 0.30 * integration_mean_1s
 )

 # ═══ LAYER M: Mathematical ═══
 aesthetic_engagement = torch.sigmoid(
 )
 rt_appreciation = torch.sigmoid(
 0.5 * f18 + 0.5 * pleasant_value
 )

 # ═══ LAYER P: Present ═══
 n1p2_engagement = torch.sigmoid(
 + 0.5 * (1 - roughness)
 )
 aesthetic_judgment = torch.sigmoid(
 + 0.5 * pleasant
 )

 # ═══ LAYER F: Future ═══
 behavioral_pred = torch.sigmoid(
 0.5 * f18 + 0.5 * integration_mean_1s
 )
 n2p3_pred = torch.sigmoid(
 )
 aesthetic_pred = torch.sigmoid(
 0.5 * aesthetic_engagement + 0.5 * pleasant_velocity_1s
 )

 return torch.cat([
 f16, f17, f18, # E: 3D
 aesthetic_engagement, rt_appreciation, # M: 2D
 n1p2_engagement, aesthetic_judgment, # P: 2D
 behavioral_pred, n2p3_pred, aesthetic_pred, # F: 3D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (Sarasso 2019 primary + 11 converging studies) | Multi-method evidence |
| **Effect Sizes** | 8+ significant | η²p=0.685, d=2.008, r=0.71, T=6.852, F=19.14 |
| **Sample Range** | n = 8–87 (median ~24) | EEG, fMRI, PET, ECoG, behavioral |
| **Evidence Modality** | EEG, fMRI, PET, ECoG, behavioral | Multi-modal convergence |
| **Falsification Tests** | 4/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Sarasso, P., Ronga, I., Pistis, A., Forte, E., Garbarini, F., Ricci, R., & Neppi-Modona, M. (2019)**. Aesthetic appreciation of musical intervals enhances behavioural and neurophysiological indexes of attentional engagement and motor inhibition. *Psychophysiology*, 56(4), e13317. `Literature/c3: Aesthetic appreciation of musical intervals enhances behavioural and neurophysio`

2. **Sarasso, P., Perna, P., Barbieri, P., Neppi-Modona, M., Sacco, K., & Ronga, I. (2021)**. Memorisation and implicit perceptual learning are enhanced for preferred musical intervals and chords. `Literature/c3: Memorisation and implicit perceptual learning are enhanced for preferred musical`

3. **Crespo-Bojorque, P., Monte-Ordono, J., & Toro, J. M. (2018)**. Early neural responses underlie advantages for consonance over dissonance. `Literature/c3: Early neural responses underlie advantages for consonance over dissonance`

4. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. `Literature/c3: Sensory cortical response to uncertainty and low salience during recognition of`

5. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262. `Literature/c3: Anatomically distinct dopamine release during anticipation and experience of pe`

6. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. `Literature/c3: Auditory and reward structures reflect the pleasure of musical expectancies dur`

7. **Kim, S.-G., Mueller, K., Lepsien, J., Mildner, T., & Fritz, T. H. (2019)**. Brain networks underlying aesthetic appreciation as modulated by interaction of the spectral and temporal organisations of music. `Literature/c3: Brain networks underlying aesthetic appreciation as modulated by interaction of`

8. **Fishman, Y. I., et al. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86(6), 2761-2788. `Literature/c3: Consonance and Dissonance of Musical Chords Neural Correlates in Auditory Cortex`

9. **Cheung, V. K. M., et al. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092. `Literature/c3: Uncertainty and Surprise Jointly Predict Musical Pleasure and Amygdala, Hippocam`

10. **Mas-Herrero, E., Zatorre, R. J., Rodriguez-Fornells, A., & Marco-Pallarés, J. (2014)**. Dissociation between musical and monetary reward responses in specific musical anhedonia. *Current Biology*, 24(6), 699-704. `Literature/c3: Dissociation between Musical and Monetary Reward Responses in Specific Musical`

11. **Brattico, E., & Jacobsen, T. (2009)**. Subjective appraisal of music: Neuroimaging evidence. *Annals of the New York Academy of Sciences*, 1169(1), 308-317.

12. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. `Literature/c3: Differential Processing of Consonance and Dissonance within the Human Superior`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — same |
| Consonance signal | S⁰.L5.roughness[30] + HC⁰.ATT | R³.roughness[0] + R³.pleasant[3] | Same — verified |
| Motor inhibition | S⁰.L5.loudness[35] + HC⁰ affect | R³.loudness[8] | Same — verified |
| Savoring | S⁰.L5.consonance × HC⁰ cognitive | R³.pleasant[3] | Same — verified |
| Aesthetic integration | S⁰.X_L5L6[208:216] | R³.x_l0l5[25:33] | Same — verified |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) | 12 tuples — same |
| Total demand | 12/2304 = 0.52% | 12/2304 = 0.52% | 12/2304 = 0.52% |
| Output | 10D | 10D (same) | 10D — same |
| Papers | 1 | 4 | **12** (+8 new) |
| Brain regions | 2 | 3 | **8** (+5 new: vmPFC, NAcc, caudate, amygdala, HG) |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
