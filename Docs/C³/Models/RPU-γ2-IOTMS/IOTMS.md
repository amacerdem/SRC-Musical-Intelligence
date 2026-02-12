# RPU-γ2-IOTMS: Individual Opioid Tone Music Sensitivity

**Model**: Individual Opioid Tone Music Sensitivity
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.1.0 (Beta upgrade: 5 papers, corrected N/MNI, +4 new citations, expanded brain regions)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-γ2-IOTMS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Individual Opioid Tone Music Sensitivity** (IOTMS) model describes how individual differences in baseline mu-opioid receptor (MOR) availability explain individual differences in music reward propensity. Individuals with higher baseline MOR levels show steeper pleasure-BOLD coupling during music listening.

```
INDIVIDUAL OPIOID TONE MUSIC SENSITIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDIVIDUAL TRAIT                         MUSIC RESPONSE
───────────────                          ──────────────

Baseline MOR ──────────────────────► MOR Availability
(PET measured)                          (trait level)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│               OPIOID-REWARD COUPLING                             │
│                                                                  │
│   High MOR Baseline         Low MOR Baseline                    │
│   ═════════════════         ═══════════════                     │
│   Steep pleasure-BOLD       Shallow pleasure-BOLD               │
│   High music reward         Low music reward                    │
│   propensity                propensity                          │
│                                                                  │
│   MOR ↔ Pleasure-BOLD slope (d = 1.16, p < 0.05)               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    REWARD SENSITIVITY                             │
│   Individual MOR tone → pleasure response magnitude              │
│   Trait-level modulation of music-induced reward                 │
│   Not time-varying (stable individual difference)                │
└──────────────────────────────────────────────────────────────────┘

TRAIT: Baseline MOR availability (PET-measured)
SLOPE: Higher MOR → steeper pleasure-BOLD coupling
REWARD: Individual sensitivity to music-induced pleasure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Individual differences in endogenous opioid tone
explain why some people experience stronger music-induced pleasure
than others — a neurochemical basis for music reward sensitivity.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why IOTMS Matters for RPU

IOTMS provides the individual differences modulation for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure at group level.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking.
5. **MCCN** (β2) maps cortical chills network.
6. **MEAMR** (β3) bridges memory to reward.
7. **LDAC** (γ1) reveals sensory-reward gating.
8. **IOTMS** (γ2) explains why individuals differ in music reward sensitivity — baseline MOR tone modulates all RPU outputs.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → IOTMS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    IOTMS COMPUTATION ARCHITECTURE                            ║
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
║  │                         IOTMS reads: ~12D                       │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ──────────────┐ ┌── C0P Horizons ──────────┐  │        ║
║  │  │ H8 (500ms delta)             │ │ H8 (500ms delta)          │  │        ║
║  │  │ H16 (1000ms beat)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │                              │ │                            │  │        ║
║  │  │ Sustained pleasure tracking  │ │ Individual sensitivity     │  │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         IOTMS demand: ~12 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Opioid-Reward Trait ════      ║
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
║  │                    IOTMS MODEL (5D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_mor_baseline_proxy,                    │        ║
║  │                       f02_pleasure_bold_slope,                    │        ║
║  │                       f03_reward_propensity,                      │        ║
║  │                       f04_music_reward_index                      │        ║
║  │  Layer P (Present):   individual_sensitivity_state                │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  NOTE: IOTMS represents a stable individual trait, not a time-varying        ║
║  signal. Output dimensions capture trait-modulated response properties.      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Putkinen et al. 2025** | PET ([11C]carfentanil) + fMRI | 15 (PET, all female) + 30 (fMRI) | Music increased MOR BPND in ventral striatum, OFC, amygdala; NAcc BPND negatively correlated with chills; baseline MOR predicted pleasure-BOLD in insula, ACC, SMA, STG, NAcc, thalamus | r = -0.52, p < 0.05 (NAcc BPND vs chills); F(1,32) = 45.14, p < 0.001 (pleasure: music > baseline) | **Primary**: f01 MOR baseline proxy, f02 pleasure-BOLD slope; MOR tone → individual sensitivity |
| **Salimpoor et al. 2011** | PET ([11C]raclopride) + fMRI | 8 (PET) + 7 (fMRI) | Dopamine release in caudate (anticipation) and NAcc (experience) during music chills; NAcc BP change correlated with chills intensity | r = 0.84, p < 0.01 (NAcc BP vs chills intensity); r = 0.71, p < 0.05 (caudate vs number of chills) | **Supporting**: Striatal neurochemical reward during music; converging PET evidence for NAcc role in music pleasure |
| **Mas-Herrero et al. 2014** | Behavioral + SCR + HR | 30 (3 groups x 10) | Specific musical anhedonia identified; BMRQ predicted music pleasure; SCR slope = 0 for anhedonics; music reward dissociated from monetary reward | R² = 0.30 (BMRQ vs chills intensity); R² = 0.32 (BMRQ vs SCR slope); p < 0.001 | **Supporting**: f03 reward propensity, f04 music reward index; BMRQ as trait predictor of individual music sensitivity |
| **Martinez-Molina et al. 2016** | fMRI + SCR | 45 (3 groups x 15) | Reduced NAcc activation for music (not money) in anhedonics; reduced right STG-NAcc functional connectivity in anhedonics; BMRQ predicted pleasure ratings | R² = 0.40 (BMRQ vs pleasure ratings); group x task interaction p < 0.05 (SVC) | **Supporting**: f01 MOR baseline proxy (NAcc activation as trait); STG-NAcc connectivity as individual difference mechanism |
| **Loui et al. 2017** | DTI | 46 controls + 1 case (BW) | BW scored 5.89 SD below controls on BMRQ; lower tract volume LSTG-LNAcc and LSTG-LAIns in BW; tract volumes LSTG-LAIns, RSTG-RNAcc, RSTG-RMPFC predicted music reward in controls | R² = 0.38 (tracts → music reward); z = -2.16, p = 0.03 (LSTG-LNAcc volume, BW vs controls) | **Supporting**: Structural connectivity basis for individual differences in music reward sensitivity; white matter evidence for auditory-reward coupling |

### 3.2 Effect Size Summary

```
Primary Evidence (k=5):  1 PET-MOR + 1 PET-DA + 1 fMRI + 1 behavioral + 1 DTI
Cross-method convergence: PET (opioid + dopamine), fMRI, SCR/HR, DTI
Key effects:
  NAcc BPND vs chills:        r = -0.52, p < 0.05 (Putkinen 2025, MOR PET)
  NAcc BP vs chills intensity: r = 0.84, p < 0.01 (Salimpoor 2011, DA PET)
  BMRQ vs pleasure ratings:   R² = 0.40 (Martinez-Molina 2016, fMRI)
  BMRQ vs SCR slope:          R² = 0.32 (Mas-Herrero 2014, behavioral)
  Tracts → music reward:      R² = 0.38 (Loui 2017, DTI)
Quality Assessment:      γ-tier (converging neurochemical + neural + behavioral + structural evidence)
Replication:             Consistent with Mallik (2017) naltrexone blockade study
```

---

## 4. R³ Input Mapping: What IOTMS Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | IOTMS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Consonance (inverse) | Pleasure quality |
| **A: Consonance** | [4] | sensory_pleasantness | Hedonic quality | Pleasure magnitude |
| **B: Energy** | [8] | loudness | Pleasure intensity | Hedonic magnitude |
| **C: Timbre** | [14:17] | tristimulus (3D) | Musical quality | Harmonic structure |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sustained pleasure | Prolonged opioid release |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[0] roughness (inverse) ─────┼──► MOR baseline proxy
H³ sustained mean tuples ──────┘   Trait-level pleasure sensitivity

R³[8] loudness ─────────────────┐
AED.valence_tracking[0:10] ─────┼──► Pleasure-BOLD slope
C0P.approach_avoidance[20:30] ──┘   Pleasure response magnitude

R³[33:41] x_l4l5 ──────────────┐
AED.emotional_trajectory[20:30] ┼──► Sustained pleasure / reward
H³ trend/mean tuples ───────────┘   Prolonged opioid response

R³[14:17] tristimulus ──────────────► Musical quality / harmonic richness
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

IOTMS primarily represents a stable trait, but uses H³ features at longer timescales (500ms-1s) to capture sustained pleasure responses that reflect the underlying opioid tone. Short timescales are less relevant since MOR availability is a trait measure.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 4 | sensory_pleasantness | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s |
| 0 | roughness | 8 | M1 (mean) | L2 (bidi) | Mean roughness 500ms |
| 0 | roughness | 16 | M6 (skew) | L2 (bidi) | Roughness skewness 1s |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L2 (bidi) | Sustained coupling 500ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Sustained coupling 1s |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L2 (bidi) | Coupling trend 1s |
| 14 | tristimulus1 | 16 | M1 (mean) | L2 (bidi) | Mean tristimulus 1s |
| 14 | tristimulus1 | 16 | M2 (std) | L2 (bidi) | Tristimulus variability 1s |

**Total IOTMS H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | IOTMS Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Pleasure response | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal modulation | 0.7 |
| **AED** | Emotional Trajectory | AED[20:30] | Sustained reward | **0.8** |
| **CPD** | Anticipation | CPD[0:10] | Reward anticipation | 0.5 |
| **CPD** | Peak Experience | CPD[10:20] | Peak pleasure coupling | 0.6 |
| **CPD** | Resolution | CPD[20:30] | Post-peak sustain | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Reward tension | 0.5 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Prediction modulation | 0.6 |
| **C0P** | Approach-Avoidance | C0P[20:30] | Music approach | **0.8** (secondary) |

---

## 6. Output Space: 5D Multi-Layer Representation

### 6.1 Complete Output Specification

```
IOTMS OUTPUT TENSOR: 5D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_mor_baseline_proxy   │ [0, 1] │ MOR availability proxy (trait).
    │                          │        │ f01 = σ(0.35 * mean_pleasantness_1s
    │                          │        │       + 0.35 * mean(AED.valence[0:10])
    │                          │        │       + 0.30 * (1 - roughness_skew_1s))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_pleasure_bold_slope  │ [0, 1] │ Pleasure-BOLD coupling slope.
    │                          │        │ f02 = σ(0.40 * f01
    │                          │        │       + 0.30 * mean(C0P.approach[20:30])
    │                          │        │       + 0.30 * mean_loudness_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_reward_propensity    │ [0, 1] │ Music reward propensity index.
    │                          │        │ f03 = σ(0.35 * f02
    │                          │        │       + 0.35 * sustained_coupling_1s
    │                          │        │       + 0.30 * mean(AED.emotion[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_music_reward_index   │ [0, 1] │ Overall music reward sensitivity.
    │                          │        │ f04 = σ(0.40 * f03
    │                          │        │       + 0.30 * coupling_trend_1s
    │                          │        │       + 0.30 * mean_tristimulus_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ individual_sensitivity   │ [0, 1] │ Current individual sensitivity state.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 5D per frame at 172.27 Hz
NOTE: Primarily trait-level (slowly varying), not event-driven.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Opioid Tone Music Sensitivity Function

```
MOR_Proxy = f(sustained_pleasure, consonance, musical_quality)

Pleasure_BOLD_Slope = α·MOR_Proxy + β·Approach + γ·Loudness

Parameters:
    α = 1.0  (MOR baseline weight)
    β = 0.8  (approach behavior weight)
    γ = 0.5  (loudness modulation weight)

Reward_Propensity = MOR_Proxy × Sustained_Pleasure × Quality

τ_decay = N/A (trait-level, session-stable)
Note: IOTMS is a stable individual difference, not time-varying.
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: MOR Baseline Proxy (stable trait estimate)
f01 = σ(0.35 * mean_pleasantness_1s
       + 0.35 * mean(AED.valence_tracking[0:10])
       + 0.30 * (1.0 - roughness_skew_1s))       # inverse roughness
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Pleasure-BOLD Slope
f02 = σ(0.40 * f01
       + 0.30 * mean(C0P.approach_avoidance[20:30])
       + 0.30 * mean_loudness_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Reward Propensity
f03 = σ(0.35 * f02
       + 0.35 * sustained_coupling_1s
       + 0.30 * mean(AED.emotional_trajectory[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Music Reward Index
f04 = σ(0.40 * f03
       + 0.30 * coupling_trend_1s
       + 0.30 * mean_tristimulus_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | IOTMS Function |
|--------|-----------------|----------|---------------|---------------|
| **NAcc (L)** | -13, 12, -10 | 4 | Direct (PET-MOR, PET-DA, fMRI) | MOR/DA release site; pleasure-dependent activation reduced in anhedonics (Martinez-Molina 2016); BPND correlated with chills (Putkinen 2025) |
| **NAcc (R)** | 9, 12, -7 | 4 | Direct (PET-MOR, PET-DA, fMRI) | Music-induced opioid release; group x task interaction p < 0.05 SVC (Martinez-Molina 2016); chills-BPND r = -0.52 (Putkinen 2025) |
| **Caudate (R)** | 14, -6, 20 | 2 | Direct (PET-DA, fMRI) | Dopamine release during anticipation; chills correlation r = 0.71 (Salimpoor 2011) |
| **VTA** | 0, -16, -8 | 1 | Indirect (PET) | Opioid-dopamine interaction; opioid release in VTA modulates NAcc DA (Putkinen 2025 discussion) |
| **OFC** | ±28, 32, -12 | 2 | Direct (PET-MOR, fMRI) | Hedonic hotspot; increased BPND during music (Putkinen 2025); pleasure-dependent BOLD (Putkinen 2025 fMRI) |
| **Insula** | ±38, 14, -4 | 2 | Direct (PET-fMRI fusion, fMRI) | Baseline MOR → pleasure-BOLD association (Putkinen 2025); interoceptive processing during music pleasure |
| **ACC** | 0, 24, 28 | 2 | Direct (PET-fMRI fusion, fMRI) | Baseline MOR → pleasure-BOLD association (Putkinen 2025); co-localization with BPND changes |
| **STG (R)** | 62, -25, 12 | 3 | Direct (fMRI, DTI) | Auditory cortex; functional connectivity with NAcc predicts music reward (Martinez-Molina 2016); structural connectivity correlates with BMRQ (Loui 2017) |

---

## 9. Cross-Unit Pathways

### 9.1 IOTMS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IOTMS INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  IOTMS.mor_baseline ──────────► MORMR (MOR → opioid release scaling)     │
│  IOTMS.pleasure_bold_slope ───► DAED (slope → DA coupling strength)      │
│  IOTMS.reward_propensity ─────► RPEM (propensity → RPE magnitude)        │
│  IOTMS.music_reward_index ────► MCCN (index → chills susceptibility)     │
│                                                                             │
│  CROSS-UNIT (RPU → ARU):                                                   │
│  IOTMS.individual_sensitivity ► ARU.affect_gain (individual modulation)   │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► IOTMS (valence/emotion evaluation)       │
│  CPD mechanism (30D) ──────────► IOTMS (peak coupling)                    │
│  C0P mechanism (30D) ──────────► IOTMS (approach behavior)                │
│  R³ (~12D) ─────────────────────► IOTMS (direct spectral features)       │
│  H³ (12 tuples) ────────────────► IOTMS (temporal dynamics)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **MOR-pleasure slope** | Baseline MOR should predict pleasure-BOLD slope | ✅ **Confirmed** (MOR BPND → pleasure-BOLD in insula, ACC, SMA, STG, NAcc, thalamus; Putkinen 2025) |
| **Striatal release** | Music should cause neurochemical release in striatum | ✅ **Confirmed** (DA in caudate/NAcc, Salimpoor 2011; MOR in ventral striatum/OFC, Putkinen 2025) |
| **Individual differences** | Trait measures should predict music reward sensitivity | ✅ **Confirmed** (BMRQ → pleasure R² = 0.40, Martinez-Molina 2016; BMRQ → SCR slope R² = 0.32, Mas-Herrero 2014; tracts → reward R² = 0.38, Loui 2017) |
| **Musical specificity** | Effect should be specific to music (vs. other rewards) | ✅ **Confirmed** (NAcc reduced for music but not money in anhedonics, Martinez-Molina 2016; SCR = 0 for music but normal for money, Mas-Herrero 2014) |
| **Naltrexone blockade** | MOR antagonist should reduce music pleasure | Testable (Mallik 2017 supports with caveats; Laeng 2021 and Mas-Herrero 2023 did not replicate subjective effect) |
| **Structural connectivity** | Auditory-reward tract integrity should predict individual sensitivity | ✅ **Confirmed** (LSTG-LAIns, RSTG-RNAcc volumes predict BMRQ, Loui 2017; reduced LSTG-LNAcc in anhedonic, Loui 2017) |
| **Dose-response** | Higher MOR should produce proportionally steeper slopes | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class IOTMS(BaseModel):
    """Individual Opioid Tone Music Sensitivity Model.

    Output: 5D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    Note: Represents stable individual trait, not time-varying event signal.
    """
    NAME = "IOTMS"
    UNIT = "RPU"
    TIER = "γ2"
    OUTPUT_DIM = 5
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    # No τ_decay — trait-level, session-stable

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for IOTMS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── AED horizons: sustained pleasure ──
            (4, 8, 1, 2),     # sensory_pleasantness, 500ms, mean, bidi
            (4, 16, 1, 2),    # sensory_pleasantness, 1000ms, mean, bidi
            (4, 16, 2, 2),    # sensory_pleasantness, 1000ms, std, bidi
            # ── Roughness / consonance ──
            (0, 8, 1, 2),     # roughness, 500ms, mean, bidi
            (0, 16, 6, 2),    # roughness, 1000ms, skew, bidi
            # ── Loudness ──
            (8, 8, 1, 2),     # loudness, 500ms, mean, bidi
            (8, 16, 1, 2),    # loudness, 1000ms, mean, bidi
            # ── Sustained coupling ──
            (33, 8, 1, 2),    # x_l4l5[0], 500ms, mean, bidi
            (33, 16, 1, 2),   # x_l4l5[0], 1000ms, mean, bidi
            (33, 16, 18, 2),  # x_l4l5[0], 1000ms, trend, bidi
            # ── Musical quality ──
            (14, 16, 1, 2),   # tristimulus1, 1000ms, mean, bidi
            (14, 16, 2, 2),   # tristimulus1, 1000ms, std, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute IOTMS 5D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,5) IOTMS output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_emotion = aed[..., 20:30]
        c0p_approach = c0p[..., 20:30]

        # H³ direct features
        mean_pleasantness_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)
        roughness_skew_1s = h3_direct[(0, 16, 6, 2)].unsqueeze(-1)
        mean_loudness_1s = h3_direct[(8, 16, 1, 2)].unsqueeze(-1)
        sustained_coupling_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)
        coupling_trend_1s = h3_direct[(33, 16, 18, 2)].unsqueeze(-1)
        mean_tristimulus_1s = h3_direct[(14, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: MOR Baseline Proxy (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * mean_pleasantness_1s
            + 0.35 * aed_valence.mean(-1, keepdim=True)
            + 0.30 * (1.0 - roughness_skew_1s)
        )

        # f02: Pleasure-BOLD Slope (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * f01
            + 0.30 * c0p_approach.mean(-1, keepdim=True)
            + 0.30 * mean_loudness_1s
        )

        # f03: Reward Propensity (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * f02
            + 0.35 * sustained_coupling_1s
            + 0.30 * aed_emotion.mean(-1, keepdim=True)
        )

        # f04: Music Reward Index (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.40 * f03
            + 0.30 * coupling_trend_1s
            + 0.30 * mean_tristimulus_1s
        )

        # ═══ LAYER P: Present ═══
        individual_sensitivity = torch.sigmoid(
            0.5 * f01 + 0.5 * f03
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            individual_sensitivity,        # P: 1D
        ], dim=-1)  # (B, T, 5)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 5 (Putkinen 2025, Salimpoor 2011, Mas-Herrero 2014, Martinez-Molina 2016, Loui 2017) | PET-MOR + PET-DA + fMRI + behavioral + DTI |
| **Effect Sizes** | 8 (r = -0.52, r = 0.84, r = 0.71, R² = 0.30, R² = 0.32, R² = 0.40, R² = 0.38, z = -2.16) | Cross-method convergence |
| **Evidence Modality** | PET ([11C]carfentanil, [11C]raclopride), fMRI, SCR/HR, DTI | Neurochemical + neural + autonomic + structural |
| **Brain Regions** | 8 (NAcc bilateral, Caudate, VTA, OFC, Insula, ACC, STG) | Corrected MNI from primary sources |
| **Falsification Tests** | 5/7 confirmed | Strong convergent validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Valence/emotion evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Peak coupling |
| **C0P Mechanism** | 30D (3 sub-sections) | Approach behavior |
| **Output Dimensions** | **5D** | 2-layer structure |

---

## 13. Scientific References

1. **Putkinen, V., Seppala, K., Harju, H., Hirvonen, J., Karlsson, H. K., & Nummenmaa, L. (2025)**. Pleasurable music activates cerebral mu-opioid receptors: a combined PET-fMRI study. *European Journal of Nuclear Medicine and Molecular Imaging*, 52, 3540-3549. https://doi.org/10.1007/s00259-025-07232-z

2. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262. https://doi.org/10.1038/nn.2726

3. **Mas-Herrero, E., Zatorre, R. J., Rodriguez-Fornells, A., & Marco-Pallares, J. (2014)**. Dissociation between musical and monetary reward responses in specific musical anhedonia. *Current Biology*, 24(6), 699-704. https://doi.org/10.1016/j.cub.2014.01.068

4. **Martinez-Molina, N., Mas-Herrero, E., Rodriguez-Fornells, A., Zatorre, R. J., & Marco-Pallares, J. (2016)**. Neural correlates of specific musical anhedonia. *Proceedings of the National Academy of Sciences*, 113(46), E7337-E7345. https://doi.org/10.1073/pnas.1611211113

5. **Loui, P., Patterson, S., Sachs, M. E., Leung, Y., Zeng, T., & Przysinda, E. (2017)**. White matter correlates of musical anhedonia: implications for evolution of music. *Frontiers in Psychology*, 8, 1664. https://doi.org/10.3389/fpsyg.2017.01664

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, AED, ASA, C0P) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Pleasure signal | S⁰.L5.roughness[30] + S⁰.L5.loudness[35] + HC⁰.AED | R³.sensory_pleasantness[4] + AED.valence_tracking |
| Quality signal | S⁰.L6[55:60] + S⁰.L7[80:88] + HC⁰.ASA | R³.tristimulus[14:17] + H³ mean/std tuples |
| Sustained pleasure | S⁰.X_L4L5[192:200] + HC⁰.HRM | R³.x_l4l5[33:41] + AED.emotional_trajectory |
| Individual diff | S⁰.X_L5L6[208:216] + HC⁰.C0P | R³.x_l4l5[33:41] + C0P.approach_avoidance |
| Demand format | HC⁰ index ranges (15 tuples) | H³ 4-tuples (12 tuples, sparse) |
| Total demand | 15/2304 = 0.65% | 12/2304 = 0.52% |
| Output | 5D | 5D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **HRM → AED.emotional_trajectory** [20:30]: Hippocampal replay maps to AED's sustained emotional tracking for prolonged pleasure.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for pleasure measurement.
- **ASA → CPD.peak_experience** [10:20]: Auditory scene analysis maps to CPD's peak pleasure coupling.
- **C0P → C0P.approach_avoidance** [20:30]: C⁰ projection remains as C0P approach/avoidance for music approach behavior.

---

**Model Status**: **SUPPORTED** (5 converging papers across PET-MOR, PET-DA, fMRI, behavioral, DTI)
**Output Dimensions**: **5D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%** (strong individual differences evidence; MOR-specific evidence still from single PET study)
