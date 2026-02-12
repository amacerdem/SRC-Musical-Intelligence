# RPU-γ3-SSPS: Saddle-Shaped Preference Surface

**Model**: Saddle-Shaped Preference Surface
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.1.0 (literature-verified evidence, corrected citations, expanded brain regions)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-γ3-SSPS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Saddle-Shaped Preference Surface** (SSPS) model describes how musical preference follows a saddle-shaped surface in the IC (information content) x entropy space: highest liking at high uncertainty/low surprise OR low uncertainty/intermediate surprise. This extends IUCP's inverted-U with a more complex interaction topology.

```
SADDLE-SHAPED PREFERENCE SURFACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    INFORMATION CONTENT (Surprise)
                    Low ◄────────────────────► High

   ENTROPY      ┌─────────────────────────────────────────────┐
   (Uncertainty)│          LIKING SURFACE                     │
                │                                             │
   High     ─── │    ★ HIGH ═════════════════╗                │
     │          │                            ║                │
     │          │                    ★ LOW   ║                │
     │          │                            ║                │
     ▼          │    ╔═════════════════ ★ HIGH                │
   Low      ─── │    ║                                        │
                └─────────────────────────────────────────────┘

   PEAK ZONES:
     1. High entropy + Low IC (predictable in uncertain context)
     2. Low entropy + Medium IC (moderate surprise in stable context)

   SADDLE: Negative interaction coefficient between IC and Entropy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical preference is not simply an inverted-U —
it follows a saddle-shaped surface where two distinct optimal
zones emerge from the IC × entropy interaction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SSPS Matters for RPU

SSPS provides the refined preference topology for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking via inverted-U preference.
5. **MCCN** (β2) maps cortical chills network.
6. **MEAMR** (β3) bridges memory to reward.
7. **LDAC** (γ1) reveals sensory-reward gating.
8. **IOTMS** (γ2) explains individual opioid differences.
9. **SSPS** (γ3) refines the preference surface from IUCP's inverted-U to a saddle shape — two optimal zones emerge from IC x entropy interaction.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → SSPS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SSPS COMPUTATION ARCHITECTURE                             ║
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
║  │                         SSPS reads: ~12D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── C0P Horizons ─────────────┐ ┌── AED Horizons ──────────┐  │        ║
║  │  │ H2 (75ms alpha)             │ │ H8 (500ms delta)          │  │        ║
║  │  │ H8 (500ms delta)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)           │ │                            │  │        ║
║  │  │                             │ │ Preference evaluation      │  │        ║
║  │  │ IC / entropy computation    │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         SSPS demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Preference Surface ═════     ║
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
║  │                    SSPS MODEL (6D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_ic_value,                              │        ║
║  │                       f02_entropy_value,                          │        ║
║  │                       f03_saddle_position,                        │        ║
║  │                       f04_peak_proximity                          │        ║
║  │  Layer P (Present):   surface_position_state                      │        ║
║  │  Layer F (Future):    optimal_zone_pred                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Cheung et al. 2019** | Behavioral + fMRI | 39 + 40 | Saddle-shaped IC x entropy interaction on chord pleasantness; regression surface resembles a saddle, not simple inverted-U | Interaction beta = -0.124, p = 0.000246; R^2_marginal = 0.476 | **Primary**: f03 saddle position, f04 peak proximity |
| 2 | **Cheung et al. 2019** | fMRI (ROI) | 40 | Bilateral amygdala/hippocampus and auditory cortex show IC x entropy interaction; NAcc reflects uncertainty only | L Amyg: beta = -0.116, p = 0.045; R Amyg: beta = -0.140, p = 0.002; L AC: beta = -0.182, p < 0.001; R AC: beta = -0.128, p = 0.002; NAcc uncertainty: beta = 0.242, p = 0.002 | **Brain regions**: amygdala, hippocampus, auditory cortex, NAcc |
| 3 | **Gold et al. 2019b** | Behavioral (IDyOM) | 43 + 27 | Inverted-U for IC and entropy on liking; IC x entropy interaction: preferences for low uncertainty/high surprise and high uncertainty/low surprise | Quadratic IC: p < 0.001; Quadratic entropy: p < 0.001; Interaction: p < 0.001 | **Replication**: confirms two optimal zones in melodic stimuli |
| 4 | **Gold et al. 2023** | fMRI + behavioral (IDyOM) | 24 | Saddle-shaped liking surface replicated in naturalistic melodies; VS reflects surprise x liking interaction (RPE-like pattern); R STG reflects liking | IC x entropy model: R^2 = 0.496, p < 0.001; R STG liking: t(23) = 2.56, p = 0.018; VS IC x liking: t(23) = 2.92, p = 0.008 (R STG) | **fMRI replication**: VS RPE pattern, R STG liking |
| 5 | **Albury et al. 2023** | Behavioral | 120 (4 groups) | Context shifts predictability-liking relationship: same stimuli rated differently depending on surrounding complexity | Significant context x predictability interaction, p < 0.05 | **Supports**: context-dependency of saddle surface position |
| 6 | **Kim et al. 2019** | fMRI (2 experiments) | 16 + 23 | Spectral x temporal interaction in fronto-limbic system: vmPFC, NAcc, caudate, putamen; vmPFC-IFG connectivity reduced for dual disruption | Significant 2x2 interaction in vmPFC, NAcc, caudate, putamen (p < 0.05 corrected) | **Supports**: multi-dimensional preference surface in fronto-limbic reward circuit |
| 7 | **Zioga et al. 2024** | EEG + behavioral | 40 | Inverted-U between note probability and pleasantness; intermediate probability notes elicit larger N100/P200; creativity link | Significant quadratic liking-probability, p < 0.05; N100/P200 modulation at intermediate probability | **Supports**: inverted-U as foundation for saddle; ERP correlates of preference |
| 8 | **Mencke et al. 2019** | Theory/MIR analysis | -- | Atonal music: uncertainty can lead to pleasure via correct predictions in uncertain contexts; proposes weak predictive model engagement | N/A (theoretical framework) | **Framework**: explains Zone 1 (high entropy + low IC) preference mechanism |

### 3.2 Effect Size Summary

```
Primary Evidence (k=8):  3 fMRI, 2 behavioral, 1 EEG, 1 fMRI-dual, 1 theoretical
Heterogeneity:           Low-moderate (consistent saddle/interaction across 3 independent labs)
Quality Assessment:      gamma-tier → strengthened by multi-study convergence
Replication:
  - Saddle shape: Cheung 2019 (chords), Gold 2019b (melodies), Gold 2023 (melodies+fMRI)
  - Brain regions: Cheung 2019 (amygdala/AC), Gold 2023 (VS/R STG), Kim 2019 (vmPFC/NAcc)
  - Inverted-U foundation: Gold 2019b, Zioga 2024, Albury 2023
Key effect sizes:
  - Interaction beta = -0.124 (Cheung 2019, behavioral)
  - R^2 = 0.476-0.496 (Cheung 2019, Gold 2023 full models)
  - Amygdala interaction: beta = -0.116 to -0.140 (Cheung 2019 fMRI)
  - VS RPE-like pattern: p = 0.008 (Gold 2023 fMRI)
```

---

## 4. R³ Input Mapping: What SSPS Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | SSPS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Musical complexity | Harmonic density |
| **A: Consonance** | [4] | sensory_pleasantness | Liking proxy | Hedonic quality |
| **B: Energy** | [8] | loudness | Perceptual salience | Attention weight |
| **D: Change** | [21] | spectral_change | Information content (IC) | Temporal surprise |
| **D: Change** | [24] | concentration_change | Entropy / uncertainty | Spectral complexity |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | IC × Entropy surface | Saddle position |
| **E: Interactions** | [25] | x_l0l5[0] | Context integration | Preference prediction |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[21] spectral_change ────────┐
C0P.expectation_surprise[10:20]┼──► Information Content (IC)
H³ IC velocity/entropy tuples ─┘   Temporal surprise level

R³[24] concentration_change ───┐
R³[0] roughness ───────────────┼──► Entropy / uncertainty
H³ entropy/std tuples ─────────┘   Spectral complexity

R³[33:41] x_l4l5 ─────────────┐
CPD.anticipation[0:10] ────────┼──► IC × Entropy saddle surface
AED.valence_tracking[0:10] ────┘   Saddle position computation

R³[4] sensory_pleasantness ────┐
R³[8] loudness ────────────────┼──► Peak proximity / liking
C0P.approach_avoidance[20:30] ─┘   Optimal zone detection
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SSPS requires H³ features at mid-to-long timescales for entropy assessment (needs context window) and IC computation. The saddle surface emerges from sustained IC × entropy interaction, requiring 500ms-1s integration.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 21 | spectral_change | 2 | M0 (value) | L0 (fwd) | IC at 75ms (fast surprise) |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | IC velocity at 500ms |
| 21 | spectral_change | 16 | M20 (entropy) | L2 (bidi) | IC entropy over 1s |
| 24 | concentration_change | 8 | M2 (std) | L2 (bidi) | Concentration std 500ms |
| 24 | concentration_change | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy 1s |
| 0 | roughness | 8 | M1 (mean) | L2 (bidi) | Mean roughness 500ms |
| 0 | roughness | 16 | M2 (std) | L2 (bidi) | Roughness variability 1s |
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms |
| 4 | sensory_pleasantness | 16 | M15 (smoothness) | L0 (fwd) | Pleasantness smoothness 1s |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L2 (bidi) | IC-perceptual coupling 500ms |
| 33 | x_l4l5[0] | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy 1s |
| 25 | x_l0l5[0] | 8 | M2 (std) | L2 (bidi) | Context variability 500ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean context 1s |

**Total SSPS H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | SSPS Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Liking evaluation | **0.8** |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal-complexity mapping | 0.7 |
| **AED** | Emotional Trajectory | AED[20:30] | Preference trajectory | 0.5 |
| **CPD** | Anticipation | CPD[0:10] | Saddle zone anticipation | **0.9** (secondary) |
| **CPD** | Peak Experience | CPD[10:20] | Optimal zone peak detection | 0.7 |
| **CPD** | Resolution | CPD[20:30] | Post-peak preference return | 0.6 |
| **C0P** | Tension-Release | C0P[0:10] | IC tension component | 0.7 |
| **C0P** | Expectation-Surprise | C0P[10:20] | IC computation | **1.0** (primary) |
| **C0P** | Approach-Avoidance | C0P[20:30] | Preference approach/avoid | **0.8** |

---

## 6. Output Space: 6D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SSPS OUTPUT TENSOR: 6D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_ic_value             │ [0, 1] │ Current information content level.
    │                          │        │ f01 = σ(0.35 * ic_75ms
    │                          │        │       + 0.35 * mean(C0P.expect[10:20])
    │                          │        │       + 0.30 * ic_velocity_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_entropy_value        │ [0, 1] │ Current entropy / uncertainty level.
    │                          │        │ f02 = σ(0.35 * concentration_entropy_1s
    │                          │        │       + 0.35 * roughness_std_1s
    │                          │        │       + 0.30 * context_variability_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_saddle_position      │ [0, 1] │ Position on saddle surface.
    │                          │        │ f03 = σ(0.35 * saddle_value
    │                          │        │       + 0.35 * mean(CPD.anticip[0:10])
    │                          │        │       + 0.30 * coupling_entropy_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_peak_proximity       │ [0, 1] │ Proximity to optimal zone peak.
    │                          │        │ f04 = σ(0.35 * f03
    │                          │        │       + 0.35 * mean(C0P.approach[20:30])
    │                          │        │       + 0.30 * pleasantness_smoothness_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ surface_position_state   │ [0, 1] │ Current position on preference surface.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ optimal_zone_pred        │ [0, 1] │ Predicted movement toward optimal zone.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Saddle Surface Function

```
Preference(IC, Entropy) = β1·IC + β2·IC² + β3·Entropy + β4·Entropy² + β5·(IC × Entropy)

Saddle shape: β5 < 0 (negative interaction)
Peak zones:
  1. High Entropy + Low IC (predictable in uncertain context)
  2. Low Entropy + Medium IC (moderate surprise in stable context)

Parameters:
    τ_decay = 2.0s  (preference assessment window; chord duration in Cheung 2019 = 2.4s)
    Interaction_coeff = -0.5  (saddle coefficient)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# Intermediate: Saddle value from IC × Entropy interaction
zone1 = f02 * (1.0 - f01)         # high entropy + low IC
zone2 = (1.0 - f02) * ic_quadratic  # low entropy + medium IC
saddle_value = torch.max(zone1, zone2)

# f01: IC Value
f01 = σ(0.35 * ic_75ms
       + 0.35 * mean(C0P.expectation_surprise[10:20])
       + 0.30 * ic_velocity_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Entropy Value
f02 = σ(0.35 * concentration_entropy_1s
       + 0.35 * roughness_std_1s
       + 0.30 * context_variability_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Saddle Position
f03 = σ(0.35 * saddle_value
       + 0.35 * mean(CPD.anticipation[0:10])
       + 0.30 * coupling_entropy_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Peak Proximity
f04 = σ(0.35 * f03
       + 0.35 * mean(C0P.approach_avoidance[20:30])
       + 0.30 * pleasantness_smoothness_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dPreference/dt = τ⁻¹ · (Target_Position - Current_Position)
    where τ = 2.0s (preference assessment window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SSPS Function |
|--------|-----------------|----------|---------------|---------------|
| **Bilateral Amygdala/Hippocampus** | L: ~ -20, -6, -16; R: ~ 22, -4, -18 | 2 | Direct fMRI (Cheung 2019 ROI) | IC x entropy interaction (saddle computation); L: beta=-0.116, p=0.045; R: beta=-0.140, p=0.002 |
| **Bilateral Auditory Cortex (STG)** | L: ~ -58, -22, 6; R: ~ 58, -18, 6 | 3 | Direct fMRI (Cheung 2019, Gold 2023) | IC x entropy interaction; liking modulation; L: beta=-0.182, p<0.001; R: beta=-0.128, p=0.002 |
| **Right Superior Temporal Gyrus (R STG)** | ~ 58, -18, 6 | 2 | Direct fMRI (Gold 2023 ROI, Mas-Herrero 2021 meta) | Liking rating covariation (t(23)=2.56, p=0.018); surprise x liking interaction |
| **Ventral Striatum / NAcc** | R: ~ 10, 8, -8 | 3 | Direct fMRI (Cheung 2019, Gold 2023, Kim 2019) | Uncertainty encoding (beta=0.242, p=0.002, Cheung 2019); surprise x liking RPE-like pattern (Gold 2023) |
| **Caudate Nucleus** | L: ~ -12, 10, 8 | 2 | Direct fMRI (Cheung 2019, Kim 2019) | Uncertainty encoding (beta=0.281, p=0.004, Cheung 2019) |
| **vmPFC** | ~ 0, 46, -10 | 1 | Direct fMRI (Kim 2019) | Spectral x temporal interaction; fronto-limbic integration; complexity-preference integration |
| **Pre-SMA** | ~ 0, 10, 52 | 1 | Direct fMRI (Cheung 2019) | Uncertainty encoding (beta=0.358, p<0.001) |

### 8.2 Doc-Code Mismatch Note

The code (`ssps.py`) lists NAcc (10, 8, -8), OFC (28, 34, -12), and vmPFC (0, 46, -10) as brain regions. The literature supports NAcc and vmPFC but does not specifically implicate OFC for the IC x entropy saddle interaction. The primary evidence (Cheung 2019) identifies amygdala/hippocampus, auditory cortex, NAcc, caudate, and pre-SMA. OFC involvement is inferred from general reward processing literature but not directly validated for the saddle-shaped preference surface. Code should be updated in Phase 5.

---

## 9. Cross-Unit Pathways

### 9.1 SSPS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SSPS INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  SSPS.saddle_position ────────► IUCP (refines inverted-U with saddle)     │
│  SSPS.ic_value ───────────────► RPEM (IC level → RPE computation)         │
│  SSPS.peak_proximity ─────────► DAED (proximity → DA anticipation)        │
│  SSPS.entropy_value ──────────► LDAC (entropy → sensory gating)           │
│                                                                             │
│  CROSS-UNIT (RPU → IMU):                                                   │
│  SSPS.optimal_zone_pred ──────► IMU.learning_target (optimal complexity)  │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► SSPS (liking evaluation)                 │
│  CPD mechanism (30D) ──────────► SSPS (zone anticipation)                 │
│  C0P mechanism (30D) ──────────► SSPS (IC/approach computation)           │
│  R³ (~12D) ─────────────────────► SSPS (direct spectral features)        │
│  H³ (14 tuples) ────────────────► SSPS (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Saddle interaction** | IC x entropy interaction should be negative (saddle) | **Confirmed** (beta = -0.124, p = 0.000246, Cheung 2019; replicated Gold 2019b, Gold 2023) |
| **Two optimal zones** | Two distinct preference peaks should emerge | **Confirmed** (high entropy/low IC and low entropy/intermediate IC zones; Cheung 2019 Fig 2C, Gold 2019b, Gold 2023 Fig 1C-D) |
| **Zone 1** | High entropy + low IC should be preferred | **Confirmed** (Cheung 2019: high uncertainty chords with low surprise rated as more pleasant; Gold 2019b: replicated) |
| **Zone 2** | Low entropy + medium IC should be preferred | **Confirmed** (Cheung 2019: low uncertainty + high surprise chords rated as highly pleasant; Gold 2023: low uncertainty + intermediate surprise preferred) |
| **Monotonic alternative** | Purely monotonic IC/entropy effects should be rejected | **Partially confirmed** (Cheung 2019: interaction significant beyond main effects; Gold 2023: surprise shows linear decline, but interaction persists) |
| **Neural saddle** | Brain regions should show IC x entropy interaction | **Confirmed** (amygdala/hippocampus and auditory cortex: Cheung 2019; VS shows RPE-like surprise x liking: Gold 2023) |
| **Context modulation** | Preference surface should shift with context | **Confirmed** (Albury 2023: context changes liking-predictability relationship) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SSPS(BaseModel):
    """Saddle-Shaped Preference Surface Model.

    Output: 6D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "SSPS"
    UNIT = "RPU"
    TIER = "γ3"
    OUTPUT_DIM = 6
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 2.0            # Preference assessment window (Cheung 2019: 2.4s chord duration)
    INTERACTION_COEFF = -0.5   # Negative saddle coefficient

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for SSPS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── C0P horizons: IC computation ──
            (21, 2, 0, 0),     # spectral_change, 75ms, value, fwd
            (21, 8, 8, 0),     # spectral_change, 500ms, velocity, fwd
            (21, 16, 20, 2),   # spectral_change, 1000ms, entropy, bidi
            # ── Entropy / uncertainty ──
            (24, 8, 2, 2),     # concentration_change, 500ms, std, bidi
            (24, 16, 20, 2),   # concentration_change, 1000ms, entropy, bidi
            (0, 8, 1, 2),      # roughness, 500ms, mean, bidi
            (0, 16, 2, 2),     # roughness, 1000ms, std, bidi
            # ── Pleasantness / liking ──
            (4, 8, 1, 2),      # sensory_pleasantness, 500ms, mean, bidi
            (4, 16, 15, 0),    # sensory_pleasantness, 1000ms, smoothness, fwd
            (8, 16, 1, 2),     # loudness, 1000ms, mean, bidi
            # ── IC-perceptual coupling ──
            (33, 8, 1, 2),     # x_l4l5[0], 500ms, mean, bidi
            (33, 16, 20, 2),   # x_l4l5[0], 1000ms, entropy, bidi
            # ── Context integration ──
            (25, 8, 2, 2),     # x_l0l5[0], 500ms, std, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SSPS 6D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,6) SSPS output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        c0p_expect = c0p[..., 10:20]
        c0p_approach = c0p[..., 20:30]
        cpd_anticip = cpd[..., 0:10]

        # H³ direct features
        ic_75ms = h3_direct[(21, 2, 0, 0)].unsqueeze(-1)
        ic_velocity_500ms = h3_direct[(21, 8, 8, 0)].unsqueeze(-1)
        concentration_entropy_1s = h3_direct[(24, 16, 20, 2)].unsqueeze(-1)
        roughness_std_1s = h3_direct[(0, 16, 2, 2)].unsqueeze(-1)
        context_variability_500ms = h3_direct[(25, 8, 2, 2)].unsqueeze(-1)
        coupling_entropy_1s = h3_direct[(33, 16, 20, 2)].unsqueeze(-1)
        pleasantness_smoothness_1s = h3_direct[(4, 16, 15, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: IC Value (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * ic_75ms
            + 0.35 * c0p_expect.mean(-1, keepdim=True)
            + 0.30 * ic_velocity_500ms
        )

        # f02: Entropy Value (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * concentration_entropy_1s
            + 0.35 * roughness_std_1s
            + 0.30 * context_variability_500ms
        )

        # Saddle surface computation
        ic_quadratic = 4.0 * f01 * (1.0 - f01)     # peaks at 0.5
        zone1 = f02 * (1.0 - f01)                    # high entropy + low IC
        zone2 = (1.0 - f02) * ic_quadratic           # low entropy + medium IC
        saddle_value = torch.max(zone1, zone2)

        # f03: Saddle Position (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * saddle_value
            + 0.35 * cpd_anticip.mean(-1, keepdim=True)
            + 0.30 * coupling_entropy_1s
        )

        # f04: Peak Proximity (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * f03
            + 0.35 * c0p_approach.mean(-1, keepdim=True)
            + 0.30 * pleasantness_smoothness_1s
        )

        # ═══ LAYER P: Present ═══
        surface_position = torch.sigmoid(
            0.5 * f03 + 0.5 * f04
        )

        # ═══ LAYER F: Future ═══
        optimal_zone_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * saddle_value
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            surface_position,              # P: 1D
            optimal_zone_pred,             # F: 1D
        ], dim=-1)  # (B, T, 6)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (Cheung 2019, Gold 2019b, Gold 2023, Albury 2023, Kim 2019, Zioga 2024, Mencke 2019; 7 empirical + 1 theoretical) | Multi-lab convergence |
| **Total N** | ~371 (39+40+43+27+24+120+16+23+40 across studies) | Behavioral + fMRI + EEG |
| **Key Effect Sizes** | Interaction beta=-0.124 (Cheung 2019); R^2=0.476-0.496 (full models); amygdala beta=-0.116 to -0.140 | Behavioral + fMRI |
| **Evidence Modality** | fMRI (3 studies), behavioral (2), EEG (1), fMRI-dual (1), theoretical (1) | Multi-modal |
| **Falsification Tests** | 7/7 confirmed or partially confirmed | Strong validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Liking evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Zone anticipation |
| **C0P Mechanism** | 30D (3 sub-sections) | IC/approach computation |
| **Output Dimensions** | **6D** | 3-layer structure |

---

## 13. Scientific References

1. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology, 29*(23), 4084-4092. doi:10.1016/j.cub.2019.09.067
2. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019b)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *The Journal of Neuroscience, 39*(47), 9397-9409. doi:10.1523/JNEUROSCI.0428-19.2019
3. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience, 17*, 1209398. doi:10.3389/fnins.2023.1209398
4. **Albury, A. W., Bianco, R., Gold, B. P., & Penhune, V. B. (2023)**. Context changes judgments of liking and predictability for melodies. *Frontiers in Psychology, 14*, 1175682. doi:10.3389/fpsyg.2023.1175682
5. **Kim, S.-G., Mueller, K., Lepsien, J., Mildner, T., & Fritz, T. H. (2019)**. Brain networks underlying aesthetic appreciation as modulated by interaction of the spectral and temporal organisations of music. *Scientific Reports, 9*, 19446. doi:10.1038/s41598-019-55781-9
6. **Zioga, I., Harrison, P. M. C., Pearce, M., Bhattacharya, J., & Di Bernardi Luft, C. (2024)**. The association between liking, learning and creativity in music. *Scientific Reports, 14*, 19048. doi:10.1038/s41598-024-70027-z
7. **Mencke, I., Omigie, D., Wald-Fuhrmann, M., & Brattico, E. (2019)**. Atonal music: Can uncertainty lead to pleasure? *Frontiers in Neuroscience, 12*, 979. doi:10.3389/fnins.2018.00979
8. **Berlyne, D. E. (1971)**. *Aesthetics and Psychobiology*. Appleton-Century-Crofts.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (EFC, AED, CPD, C0P) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| IC signal | S⁰.L9.entropy_T[116] + HC⁰.EFC | R³.spectral_change[21] + C0P.expectation_surprise |
| Entropy signal | S⁰.L9.entropy_F[117] + S⁰.L5.roughness[30] | R³.concentration_change[24] + R³.roughness[0] + H³ entropy tuples |
| Saddle surface | S⁰.X_L4L5[192:200] + HC⁰.CPD | R³.x_l4l5[33:41] + CPD.anticipation |
| Context | S⁰.X_L0L1[128:136] + HC⁰.C0P | R³.x_l0l5[25] + C0P.approach_avoidance |
| Demand format | HC⁰ index ranges (24 tuples) | H³ 4-tuples (14 tuples, sparse) |
| Total demand | 24/2304 = 1.04% | 14/2304 = 0.61% |
| Output | 6D | 6D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **EFC → C0P.expectation_surprise** [10:20]: Efference copy prediction maps to C0P's IC computation for surprise.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for liking evaluation.
- **CPD → CPD.anticipation** [0:10]: Chills/peak detection maps to CPD's zone anticipation on the saddle surface.
- **C0P → C0P.approach_avoidance** [20:30]: C⁰ projection maps to C0P's approach/avoidance for preference peaks.

---

## 15. Doc-Code Mismatches

The following discrepancies exist between this document and `mi_beta/brain/units/rpu/models/ssps.py`. These are expected at v2.1.0 and will be reconciled in Phase 5.

| Aspect | Doc (v2.1.0) | Code (v2.0.0 stub) | Action |
|--------|-------------|---------------------|--------|
| FULL_NAME | "Saddle-Shaped Preference Surface" | "Social Signal Processing System" | Code needs correction |
| OUTPUT_DIM | 6 | 10 | Code needs correction (10D includes Layer M not in doc) |
| MECHANISM_NAMES | ("AED", "CPD", "C0P") | ("ASA",) | Code needs correction |
| CROSS_UNIT_READS | Not specified | ("ARU",) | Code needs correction |
| LAYERS | E(4D) + P(1D) + F(1D) = 6D | E(4D) + M(3D) + P(1D) + F(2D) = 10D | Code needs correction; Layer M not justified by literature |
| h3_demand | 14 tuples (detailed) | Empty tuple () | Code needs implementation |
| brain_regions | 7 regions (Amyg, AC, R STG, VS, Caudate, vmPFC, pre-SMA) | 3 regions (NAcc, OFC, vmPFC) | Code needs update |
| Citations | Cheung 2019 (primary), Gold 2019b, Gold 2023 + 5 more | Gold 2019 only | Code needs update |
| compute() | Full implementation in pseudocode | Returns zeros (stub) | Code needs Phase 5 implementation |

---

**Model Status**: **LITERATURE-VALIDATED** (upgraded from PRELIMINARY)
**Output Dimensions**: **6D**
**Evidence Tier**: **gamma (Integrative)** -- strengthened by multi-study convergence (8 papers, 3 independent labs)
**Confidence**: **55-70%** (upgraded from 50-70% based on replication across chords and melodies)
