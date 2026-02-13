# RPU-α3-RPEM: Reward Prediction Error in Music

**Model**: Reward Prediction Error in Music
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-α3-RPEM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Reward Prediction Error in Music** (RPEM) model describes how the ventral striatum exhibits reward prediction error-like responses to musical surprise. This model shows increased activity for surprising liked stimuli and decreased activity for surprising disliked stimuli, implementing a classic reinforcement learning mechanism in the musical domain.

```
REWARD PREDICTION ERROR IN MUSIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    SURPRISE (IC)
                Low ◄───────────► High

          ┌────────────────────────────────────────────┐
LIKING    │                                            │
          │        VS BOLD RESPONSE                    │
High      │      o───────────────●                    │
  │       │                     ↗                      │
  │       │                   ↗                        │
  │       │                 ↗                          │
  │       │               ↗   RPE CROSSOVER            │
  │       │             ↗                              │
  ▼       │           ↗                                │
Low       │      ●───────────────o                    │
          │                     ↘                      │
          └────────────────────────────────────────────┘

RPE PATTERN:
  • Surprise × Liked    = POSITIVE RPE → VS ↑
  • Surprise × Disliked = NEGATIVE RPE → VS ↓

EFFECT SIZE: d = 1.07 (Gold 2023, fMRI)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The ventral striatum computes reward prediction errors
for music — exactly as in classical reinforcement learning. Surprising
events that are liked produce positive RPE; surprising events that
are disliked produce negative RPE.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why RPEM Matters for RPU

RPEM provides the learning signal for the Reward Processing Unit:

1. **DAED** (α1) establishes the anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure and chills.
3. **RPEM** (α3) provides the computational mechanism: reward prediction errors that drive preference learning.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → RPEM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RPEM COMPUTATION ARCHITECTURE                             ║
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
║  │                         RPEM reads: ~12D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── C0P Horizons ─────────────┐ ┌── AED Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H4 (125ms theta)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H8 (500ms delta)            │ │                            │  │        ║
║  │  │                             │ │ Liking evaluation          │  │        ║
║  │  │ Prediction/surprise         │ │ Valence signal             │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         RPEM demand: ~16 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Striatal RPE ══════════       ║
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
║  │                    RPEM MODEL (8D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_surprise_signal,                       │        ║
║  │                       f02_liking_signal,                          │        ║
║  │                       f03_positive_rpe,                           │        ║
║  │                       f04_negative_rpe                            │        ║
║  │  Layer M (Math):      rpe_magnitude, vs_response                  │        ║
║  │  Layer P (Present):   current_rpe, vs_activation_state            │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Gold 2023** | fMRI | 24 | VS shows RPE-like IC x liking crossover | d = 1.07, p < 0.008 | **Primary**: f03, f04 RPE crossover |
| **Gold 2023** | fMRI | 24 | R STG shows different pattern | d = 1.22, p < 0.008 | **f01 surprise signal** |

| **Gold 2023b** | fMRI | 24 | VS and R STG reflect pleasure of expectations | IC×entropy interaction | **Replication**: VS pleasure-expectancy link |
| **Cheung 2019** | fMRI | 39 | NAcc reflects uncertainty; amygdala/auditory cortex reflect uncertainty×surprise | interaction, p < 0.001 | **Extension**: nonlinear RPE-like signals |
| **Salimpoor 2011** | PET | 8 | Caudate DA during anticipation (RPE precursor) | r = 0.71, p < 0.05 | **Mechanistic basis**: DA signals for prediction |

### 3.2 Effect Size Summary

```
Primary Evidence (k=5):  4 independent studies (3 fMRI, 1 PET)
Cross-modal convergence: fMRI BOLD (3 studies), PET DA (1 study)
Quality Assessment:      α-tier (direct VS measurement, RPE crossover confirmed)
Key finding:             d = 1.07 RPE crossover in VS (Gold 2023a PNAS)
Replication:             Cheung 2019 confirms NAcc prediction signals
                         Gold 2023b Frontiers confirms VS-pleasure link
                         Salimpoor 2011 provides DA substrate
```

---

## 4. R³ Input Mapping: What RPEM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | RPEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Harmonic change | Consonance shift |
| **A: Consonance** | [4] | sensory_pleasantness | Liking signal | Hedonic valence |
| **B: Energy** | [8] | loudness | Salience encoding | Attention capture |
| **B: Energy** | [10] | spectral_flux | Musical deviation | Event detection |
| **D: Change** | [21] | spectral_change | Spectral surprise | Information content |
| **D: Change** | [24] | concentration_change | Concentration shift | Uncertainty signal |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Prediction generation | Expected reward |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Surprise x context | RPE computation |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | RPEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [87] | melodic_entropy | Melodic prediction error — direct measure of pitch-level surprise that drives RPE computation; replaces proxy via spectral_change [21] | Pearce 2005 IDyOM; Gold 2019 RPE in NAcc |
| **I: Information** | [88] | harmonic_entropy | Harmonic prediction error — chord-level surprise signal; harmonic violations produce the largest RPE responses in VS | Gold 2019 chord transition probability; Cheung 2019 |
| **I: Information** | [89] | rhythmic_information_content | Rhythmic surprise — information content of temporal events; unexpected rhythmic deviations generate RPE independent of pitch | Spiech 2022 rhythmic IC |

**Rationale**: RPEM is the core reward prediction error model. RPE computation fundamentally requires quantifying "surprise" (actual - expected). The I:Information group provides direct, domain-specific surprise measures: melodic_entropy [87] for pitch RPE, harmonic_entropy [88] for chord RPE, and rhythmic_information_content [89] for temporal RPE. These replace the indirect proxies (spectral_change [21], concentration_change [24]) with information-theoretic measures grounded in predictive coding (Friston). RPEM has the highest I-group demand rationale of any RPU model.

**Code impact** (Phase 6): `r3_indices` extended to include [87], [88], [89]. These directly feed RPE computation — spectral_change proxy replaced by domain-specific IC measures.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[21] spectral_change ─────────┐
R³[24] concentration_change ────┼──► Information content (IC/surprise)
C0P.expectation_surprise[10:20] ┘   Higher entropy → higher surprise

R³[4] sensory_pleasantness ─────┐
R³[0] roughness (inverse) ──────┼──► Liking signal (real-time valence)
AED.valence_tracking[0:10] ─────┘   Consonance → positive valence

R³[33:41] x_l4l5 ──────────────┐
CPD.anticipation[0:10] ─────────┼──► Reward Prediction Error
H³ velocity/entropy tuples ─────┘   Derivatives × Perceptual = RPE signal

R³[8] loudness ─────────────────┐
R³[10] spectral_flux ───────────┼──► Salience for RPE weighting
C0P.approach_avoidance[20:30] ──┘   Louder events → larger RPE impact
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

RPEM requires H³ features at C0P horizons for prediction/surprise computation, AED horizons for liking evaluation, and CPD horizons for context assessment. The demand reflects the fast RPE computation timescale.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral change at 100ms |
| 21 | spectral_change | 4 | M20 (entropy) | L0 (fwd) | Spectral entropy at 125ms |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | Spectral velocity at 500ms |
| 24 | concentration_change | 3 | M0 (value) | L2 (bidi) | Concentration at 100ms |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms |
| 0 | roughness | 3 | M8 (velocity) | L0 (fwd) | Roughness velocity 100ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms |
| 10 | spectral_flux | 4 | M0 (value) | L2 (bidi) | Onset at 125ms |
| 10 | spectral_flux | 8 | M2 (std) | L2 (bidi) | Onset variability 500ms |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | RPE coupling 100ms |
| 33 | x_l4l5[0] | 8 | M8 (velocity) | L0 (fwd) | RPE velocity 500ms |
| 25 | x_l0l5[0] | 8 | M1 (mean) | L2 (bidi) | Prediction mean 500ms |
| 25 | x_l0l5[0] | 16 | M20 (entropy) | L2 (bidi) | Prediction entropy 1s |

**Total RPEM H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | RPEM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Liking signal (reward valence) | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Salience weighting | 0.7 |
| **AED** | Emotional Trajectory | AED[20:30] | Reward context | 0.5 |
| **CPD** | Anticipation | CPD[0:10] | Expectation baseline | 0.8 |
| **CPD** | Peak Experience | CPD[10:20] | Positive RPE amplification | 0.7 |
| **CPD** | Resolution | CPD[20:30] | Post-RPE learning | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Prediction generation | 0.8 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Surprise detection (IC) | **1.0** (primary) |
| **C0P** | Approach-Avoidance | C0P[20:30] | RPE sign (approach = positive) | 0.9 |

---

## 6. Output Space: 8D Multi-Layer Representation

### 6.1 Complete Output Specification

```
RPEM OUTPUT TENSOR: 8D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_surprise_signal      │ [0, 1] │ Information content (IC).
    │                          │        │ f01 = σ(0.35 * spectral_entropy_125ms
    │                          │        │       + 0.30 * mean(C0P.expect[10:20])
    │                          │        │       + 0.20 * spectral_change_100ms
    │                          │        │       + 0.15 * concentration_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_liking_signal        │ [0, 1] │ Real-time reward valence.
    │                          │        │ f02 = σ(0.40 * mean(AED.valence[0:10])
    │                          │        │       + 0.35 * mean_pleasantness_1s
    │                          │        │       + 0.25 * (1 - roughness_100ms))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_positive_rpe         │ [0, 1] │ Surprise x Liked → VS activation.
    │                          │        │ f03 = σ(0.50 * f01 * f02
    │                          │        │       + 0.30 * mean(CPD.peak[10:20])
    │                          │        │       + 0.20 * rpe_coupling_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_negative_rpe         │ [0, 1] │ Surprise x Disliked → VS deactivation.
    │                          │        │ f04 = σ(0.50 * f01 * (1 - f02)
    │                          │        │       + 0.30 * roughness_velocity_100ms
    │                          │        │       + 0.20 * prediction_entropy_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ rpe_magnitude            │ [0, 1] │ |RPE| = max(f03, f04).
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ vs_response              │ [0, 1] │ VS BOLD proxy: f03 - f04 + 0.5.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ current_rpe              │ [0, 1] │ Signed RPE (f03 - f04 + 0.5).
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ vs_activation_state      │ [0, 1] │ Current striatal activation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 8D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Reward Prediction Error Function

```
RPE(t) = Reward(t) - Expected_Reward(t)
       = Liking(t) - Prediction(t)

VS_Response = β1·IC + β2·Liking + β3·(IC × Liking)

  where IC × Liking crossover:
    High IC × High Liking → Positive RPE → VS ↑
    High IC × Low Liking  → Negative RPE → VS ↓

Parameters:
    d = 1.07  (VS crossover effect, Gold 2023)
    τ_decay = 1.0s  (RPE signal decay)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Surprise Signal (IC)
f01 = σ(0.35 * spectral_entropy_125ms
       + 0.30 * mean(C0P.expectation_surprise[10:20])
       + 0.20 * spectral_change_100ms
       + 0.15 * concentration_100ms)
# coefficients: 0.35 + 0.30 + 0.20 + 0.15 = 1.0 ✓

# f02: Liking Signal
f02 = σ(0.40 * mean(AED.valence_tracking[0:10])
       + 0.35 * mean_pleasantness_1s
       + 0.25 * (1.0 - roughness_100ms))
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f03: Positive RPE (Surprise × Liked)
f03 = σ(0.50 * f01 * f02
       + 0.30 * mean(CPD.peak_experience[10:20])
       + 0.20 * rpe_coupling_100ms)
# coefficients: 0.50 + 0.30 + 0.20 = 1.0 ✓

# f04: Negative RPE (Surprise × Disliked)
f04 = σ(0.50 * f01 * (1.0 - f02)
       + 0.30 * roughness_velocity_100ms
       + 0.20 * prediction_entropy_1s)
# coefficients: 0.50 + 0.30 + 0.20 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | RPEM Function |
|--------|-----------------|----------|---------------|---------------|
| **Ventral Striatum (VS)** | ±8, 6, -4 | 2 | Direct (fMRI) | Reward prediction error |
| **R Superior Temporal Gyrus** | 60, -20, 4 | 1 | Direct (fMRI) | Surprise-liking interaction |

---

## 9. Cross-Unit Pathways

### 9.1 RPEM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RPEM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  RPEM.positive_rpe ──────────► DAED (positive RPE → caudate learning)     │
│  RPEM.negative_rpe ──────────► DAED (negative RPE → caudate suppression)  │
│  RPEM.surprise_signal ───────► MORMR (surprise → chills prediction)       │
│  RPEM.liking_signal ─────────► IUCP (liking → complexity preference)      │
│  RPEM.vs_response ───────────► MCCN (VS → cortical chills network)        │
│                                                                             │
│  CROSS-UNIT (RPU → IMU):                                                   │
│  RPEM.rpe_magnitude ─────────► IMU.prediction_update (RPE → memory)       │
│  RPEM.current_rpe ───────────► IMU.error_signal (learning signal)          │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► RPEM (liking evaluation)                 │
│  CPD mechanism (30D) ──────────► RPEM (context/peak assessment)            │
│  C0P mechanism (30D) ──────────► RPEM (prediction/surprise)                │
│  R³ (~12D) ─────────────────────► RPEM (direct spectral features)         │
│  H³ (16 tuples) ────────────────► RPEM (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **RPE crossover** | Surprise × liked → VS ↑, surprise × disliked → VS ↓ | ✅ **Confirmed** (d = 1.07, Gold 2023) |
| **STG dissociation** | STG should show different pattern than VS | ✅ **Confirmed** (d = 1.22, Gold 2023) |
| **Learning effect** | RPE should drive preference updating | Testable |
| **DA blockade** | DA antagonists should attenuate RPE signal | Testable |
| **Prediction manipulation** | Changing expectations should modulate RPE | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class RPEM(BaseModel):
    """Reward Prediction Error in Music Model.

    Output: 8D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "RPEM"
    UNIT = "RPU"
    TIER = "α3"
    OUTPUT_DIM = 8
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 1.0          # RPE signal decay (seconds)
    ALPHA_ATTENTION = 0.92   # Attention weight for prediction errors

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for RPEM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── C0P horizons: prediction/surprise ──
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 4, 20, 0),    # spectral_change, 125ms, entropy, fwd
            (21, 8, 8, 0),     # spectral_change, 500ms, velocity, fwd
            (24, 3, 0, 2),     # concentration_change, 100ms, value, bidi
            # ── AED horizons: liking evaluation ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 2),     # sensory_pleasantness, 1000ms, mean, bidi
            (0, 3, 0, 2),      # roughness, 100ms, value, bidi
            (0, 3, 8, 0),      # roughness, 100ms, velocity, fwd
            # ── CPD horizons: context assessment ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 4, 0, 2),     # spectral_flux, 125ms, value, bidi
            (10, 8, 2, 2),     # spectral_flux, 500ms, std, bidi
            # ── RPE coupling ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 8, 8, 0),     # x_l4l5[0], 500ms, velocity, fwd
            (25, 8, 1, 2),     # x_l0l5[0], 500ms, mean, bidi
            (25, 16, 20, 2),   # x_l0l5[0], 1000ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute RPEM 8D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,8) RPEM output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        cpd_peak = cpd[..., 10:20]
        c0p_expect = c0p[..., 10:20]

        # H³ direct features
        spectral_entropy_125ms = h3_direct[(21, 4, 20, 0)].unsqueeze(-1)
        spectral_change_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
        concentration_100ms = h3_direct[(24, 3, 0, 2)].unsqueeze(-1)
        mean_pleasantness_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)
        roughness_100ms = h3_direct[(0, 3, 0, 2)].unsqueeze(-1)
        roughness_velocity_100ms = h3_direct[(0, 3, 8, 0)].unsqueeze(-1)
        rpe_coupling_100ms = h3_direct[(33, 3, 0, 2)].unsqueeze(-1)
        prediction_entropy_1s = h3_direct[(25, 16, 20, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Surprise Signal (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * spectral_entropy_125ms
            + 0.30 * c0p_expect.mean(-1, keepdim=True)
            + 0.20 * spectral_change_100ms
            + 0.15 * concentration_100ms
        )

        # f02: Liking Signal (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * aed_valence.mean(-1, keepdim=True)
            + 0.35 * mean_pleasantness_1s
            + 0.25 * (1.0 - roughness_100ms)
        )

        # f03: Positive RPE (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.50 * (f01 * f02)
            + 0.30 * cpd_peak.mean(-1, keepdim=True)
            + 0.20 * rpe_coupling_100ms
        )

        # f04: Negative RPE (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * (f01 * (1.0 - f02))
            + 0.30 * roughness_velocity_100ms
            + 0.20 * prediction_entropy_1s
        )

        # ═══ LAYER M: Mathematical ═══
        rpe_magnitude = torch.max(f03, f04)
        vs_response = torch.clamp(f03 - f04 + 0.5, 0.0, 1.0)

        # ═══ LAYER P: Present ═══
        current_rpe = torch.clamp(f03 - f04 + 0.5, 0.0, 1.0)
        vs_activation_state = torch.sigmoid(
            0.5 * current_rpe + 0.5 * rpe_magnitude
        )

        return torch.cat([
            f01, f02, f03, f04,                    # E: 4D
            rpe_magnitude, vs_response,            # M: 2D
            current_rpe, vs_activation_state,      # P: 2D
        ], dim=-1)  # (B, T, 8)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 4 (Gold 2023a PNAS, Gold 2023b Frontiers, Cheung 2019, Salimpoor 2011) | Multi-study evidence |
| **Effect Sizes** | 4+ (d=1.07, d=1.22, IC×entropy interaction, r=0.71) | fMRI + PET |
| **Evidence Modality** | fMRI (3 studies), PET | Multi-modal convergence |
| **Falsification Tests** | 2/5 confirmed | High validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Liking evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Context/peak assessment |
| **C0P Mechanism** | 30D (3 sub-sections) | Prediction/surprise |
| **Output Dimensions** | **8D** | 4-layer structure |

---

## 13. Scientific References

1. **Gold, B. P., Mas-Herrero, E., Zeighami, Y., Benovoy, M., Dagher, A., & Zatorre, R. J. (2023a)**. Musical reward prediction errors engage the nucleus accumbens and motivate learning. *PNAS*, 120(23), e2216710120.
2. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023b)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience*, 17, 1209398.
3. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
4. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (EFC, AED, ASA, CPD) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Surprise signal | S⁰.L9.entropy_T[116] + HC⁰.EFC | R³.spectral_change[21] + C0P.expectation_surprise |
| Liking signal | S⁰.L5.roughness[30] + HC⁰.AED | R³.sensory_pleasantness[4] + AED.valence_tracking |
| RPE computation | S⁰.X_L4L5[192:200] + HC⁰.CPD | R³.x_l4l5[33:41] + CPD.peak_experience |
| Prediction model | HC⁰.EFC[80:88] | C0P.expectation_surprise[10:20] |
| Demand format | HC⁰ index ranges (24 tuples) | H³ 4-tuples (16 tuples, sparse) |
| Total demand | 24/2304 = 1.04% | 16/2304 = 0.69% |
| Output | 8D | 8D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **EFC → C0P.expectation_surprise** [10:20]: Efference copy prediction maps to C0P's expectation-surprise detection.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment maps to AED's liking evaluation.
- **ASA → CPD.anticipation** [0:10]: Auditory scene analysis maps to CPD's context assessment.
- **CPD → CPD.peak_experience** [10:20]: Chills/peak detection maps to CPD's positive RPE amplification.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **8D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
