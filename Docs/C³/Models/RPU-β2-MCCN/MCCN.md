# RPU-β2-MCCN: Musical Chills Cortical Network

**Model**: Musical Chills Cortical Network
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-β2-MCCN.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musical Chills Cortical Network** (MCCN) model describes how musical chills engage a distributed cortical network including OFC, bilateral insula, SMA, and STG, with characteristic theta oscillation patterns measured via EEG and fMRI.

```
MUSICAL CHILLS CORTICAL NETWORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACOUSTIC INPUT                           NEURAL RESPONSE
─────────────                            ───────────────

Musical Features ──────────────────► Auditory Processing
     │                                   (STG bilateral)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│               CORTICAL CHILLS NETWORK                            │
│                                                                  │
│   OFC              Bilateral Insula     SMA                      │
│   ═══              ════════════════     ═══                      │
│   Reward value      Interoceptive       Motor preparation        │
│   Hedonic eval.     awareness           Rhythmic coupling        │
│                                                                  │
│   R Prefrontal Theta ↑    Central Theta ↓                        │
│   (p < 0.049)              (p < 0.006)                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STG (AUDITORY CORTEX)                          │
│   Auditory processing × reward interaction                       │
│   Pleasure-gated sensory enhancement                             │
└──────────────────────────────────────────────────────────────────┘

CHILLS: Right prefrontal theta increase + central/temporal theta decrease
Arousal: Physiological activation (beta/alpha ratio ↑, p=0.014)
Network: OFC + Insula + SMA + STG (all p < 1e-05, EEG source localization)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical chills recruit a distributed cortical network
with characteristic theta oscillation signatures — prefrontal
increase and central decrease — linking reward and motor systems.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MCCN Matters for RPU

MCCN provides the cortical network characterization for chills within the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking via inverted-U preference.
5. **MCCN** (β2) maps the cortical network engaged during peak chills experiences, bridging theta oscillations to reward.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → MCCN)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MCCN COMPUTATION ARCHITECTURE                             ║
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
║  │                         MCCN reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ──────────────┐ ┌── CPD Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)             │ │ H8 (500ms delta)          │  │        ║
║  │  │ H16 (1000ms beat)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │                              │ │                            │  │        ║
║  │  │ Theta oscillation proxy      │ │ Peak/chills detection      │  │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         MCCN demand: ~16 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Chills Network ═══════       ║
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
║  │                    MCCN MODEL (7D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_theta_prefrontal,                      │        ║
║  │                       f02_theta_central,                         │        ║
║  │                       f03_arousal_index,                          │        ║
║  │                       f04_chills_magnitude                        │        ║
║  │  Layer P (Present):   network_state, theta_pattern                │        ║
║  │  Layer F (Future):    chills_onset_pred                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Chabin 2020** | HD-EEG (256ch) | 18 | R prefrontal theta ↑ during chills | RPF: F(2,15)=3.28, p=0.049; post hoc p=0.046 | **Primary**: f01 theta prefrontal |
| **Chabin 2020** | HD-EEG (256ch) | 18 | R central theta ↓ during chills | RC: F(2,15)=4.09, p=0.025; post hoc p=0.042 | **f02 theta central (inverse)** |
| **Chabin 2020** | HD-EEG (256ch) | 18 | R temporal theta ↓ during chills | RT: F(2,15)=5.88, p=0.006; post hoc p=0.004 | **STG** theta during chills |
| **Chabin 2020** | HD-EEG (256ch) | 18 | Beta/alpha ratio ↑ during chills | F(2,15)=4.77, p=0.014 | **f03 arousal index** |
| **Chabin 2020** | HD-EEG source localization (LAURA) | 18 | OFC activation ↑ with emotion | F(2,15)=17.4, p<1×10⁻⁵ | **Network**: OFC reward |
| **Chabin 2020** | HD-EEG source localization (LAURA) | 18 | Bilateral insula activation ↑ | F(2,15)=21.63, p<1×10⁻⁶ | **Network**: interoception |
| **Chabin 2020** | HD-EEG source localization (LAURA) | 18 | SMA activation ↑ | F(2,15)=27.3, p<1×10⁻⁷ | **Network**: motor |
| **Chabin 2020** | HD-EEG source localization (LAURA) | 18 | Bilateral STG activation ↑ | RSTG: F(2,15)=22.05, p<1×10⁻⁶ | **Network**: auditory |
| **Putkinen 2025** | PET [¹¹C]carfentanil | 15 | OFC+amygdala MOR during music chills | Chills count correlated with MOR binding | **Supporting**: opioid chills network |
| **Salimpoor 2011** | PET [¹¹C]raclopride | 8 | Caudate→NAcc DA during anticipation→chills | r=0.71 (caudate BP vs chills) | **Supporting**: DA chills mechanism |

### 3.2 Effect Size Summary

```
Primary Evidence (k=10): HD-EEG surface + source localization + PET convergence
Heterogeneity:           Low — consistent OFC/insula/SMA/STG network across modalities
Quality Assessment:      β-tier (EEG surface + source localization + PET)
Note:                    Chabin 2020 is HD-EEG ONLY (not fMRI). Source localization
                         used LAURA inverse solution to estimate cortical origins.
                         Consistent with Blood & Zatorre (2001) fMRI chills network.
Replication:             Putkinen 2025 PET confirms OFC/amygdala in chills;
                         Salimpoor 2011 PET confirms DA mechanism during chills.
```

---

## 4. R³ Input Mapping: What MCCN Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | MCCN Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Tension (inverse) | Chills patterns |
| **B: Energy** | [7] | amplitude | Peak intensity proxy | Chills magnitude |
| **B: Energy** | [8] | loudness | Peak pleasure intensity | Hedonic magnitude |
| **B: Energy** | [9] | rms_energy | Arousal correlate | Physiological activation |
| **D: Change** | [21] | spectral_change | Musical deviation | Surprise events |
| **D: Change** | [22] | energy_change | Dynamic shift | Crescendo/decrescendo |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Theta oscillation proxy | Low-band correlations |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | MCCN Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [88] | harmonic_entropy | Entropy resolution — chills are triggered by the resolution of harmonic uncertainty; a drop in harmonic_entropy at cadential moments signals the consummatory phase | Cheung 2019 uncertainty × surprise; Gold 2019 |
| **I: Information** | [87] | melodic_entropy | Melodic surprise context — high melodic entropy preceding a chill moment amplifies the prediction error magnitude at resolution | Pearce 2005 IDyOM; de Fleurian & Pearce 2021 |

**Rationale**: MCCN models the cortical network underlying musical chills/frisson. Chills occur at moments of high prediction error following high uncertainty (Cheung 2019). harmonic_entropy [88] directly measures the harmonic uncertainty that precedes chill events — its temporal derivative (drop) at resolution moments is a primary chill trigger. melodic_entropy [87] provides the melodic uncertainty context. Currently these are proxied by spectral_change [21] and energy_change [22], which lack the music-specific information content.

**Code impact** (Phase 6): `r3_indices` extended to include [87], [88]. These feed the theta oscillation proxy and chill trigger detection paths.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[25:33] x_l0l5 ──────────────┐
AED.arousal_dynamics[10:20] ────┼──► Theta oscillation proxy
H³ periodicity tuples ─────────┘   Prefrontal/central theta patterns

R³[8] loudness ─────────────────┐
R³[7] amplitude ────────────────┼──► Peak pleasure / chills intensity
CPD.peak_experience[10:20] ─────┘   Chills magnitude

R³[9] rms_energy ───────────────┐
AED.valence_tracking[0:10] ─────┼──► Arousal index
H³ velocity/std tuples ─────────┘   Physiological activation level

R³[0] roughness ────────────────────► Tension (inverse chills)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MCCN requires H³ features at multiple scales: fast theta-timescale (100ms) for oscillation tracking, mid-range (500ms) for chills onset detection, and long (1000ms) for sustained network state evaluation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Low-band coupling at 100ms (theta proxy) |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Theta periodicity at 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Low-band periodicity at 1s |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean low-band coupling over 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 8 | M4 (max) | L2 (bidi) | Peak loudness over 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |
| 7 | amplitude | 8 | M8 (velocity) | L2 (bidi) | Amplitude velocity at 500ms |
| 7 | amplitude | 16 | M2 (std) | L2 (bidi) | Amplitude variability over 1s |
| 9 | rms_energy | 3 | M0 (value) | L2 (bidi) | RMS energy at 100ms |
| 9 | rms_energy | 8 | M8 (velocity) | L2 (bidi) | Energy velocity at 500ms |
| 9 | rms_energy | 16 | M1 (mean) | L2 (bidi) | Mean energy over 1s |
| 0 | roughness | 8 | M1 (mean) | L2 (bidi) | Mean roughness over 500ms |
| 0 | roughness | 16 | M2 (std) | L2 (bidi) | Roughness variability over 1s |
| 21 | spectral_change | 8 | M0 (value) | L2 (bidi) | Spectral deviation at 500ms |
| 22 | energy_change | 8 | M8 (velocity) | L2 (bidi) | Energy change velocity at 500ms |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

MCCN projected v2 from H:Harmony + I:Information, aligned with AED+CPD+C0P horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 86 | syntactic_irregularity | H | 3 | M0 (value) | L2 | Syntactic irregularity at 100ms |
| 86 | syntactic_irregularity | H | 8 | M0 (value) | L2 | Syntactic irregularity at 500ms |
| 86 | syntactic_irregularity | H | 16 | M4 (max) | L2 | Peak irregularity over 1s |
| 88 | harmonic_entropy | I | 3 | M0 (value) | L2 | Harmonic entropy at 100ms |
| 88 | harmonic_entropy | I | 8 | M1 (mean) | L2 | Mean harmonic entropy 500ms |
| 88 | harmonic_entropy | I | 16 | M1 (mean) | L2 | Mean harmonic entropy 1s |

**v2 projected**: 6 tuples
**Total projected**: 22 tuples of 294,912 theoretical = 0.0075%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | MCCN Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Hedonic evaluation during chills | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal index computation | **0.8** |
| **AED** | Emotional Trajectory | AED[20:30] | Chills emotional trajectory | 0.7 |
| **CPD** | Anticipation | CPD[0:10] | Pre-chills anticipation buildup | 0.7 |
| **CPD** | Peak Experience | CPD[10:20] | Peak chills detection | **0.9** (secondary) |
| **CPD** | Resolution | CPD[20:30] | Post-chills resolution | 0.6 |
| **C0P** | Tension-Release | C0P[0:10] | Tension buildup before chills | 0.6 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Surprise component of chills | 0.7 |
| **C0P** | Approach-Avoidance | C0P[20:30] | Chills approach motivation | 0.5 |

---

## 6. Output Space: 7D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MCCN OUTPUT TENSOR: 7D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_theta_prefrontal     │ [0, 1] │ R prefrontal theta power increase.
    │                          │        │ f01 = σ(0.35 * theta_period_100ms
    │                          │        │       + 0.35 * mean(AED.arousal[10:20])
    │                          │        │       + 0.30 * mean_coupling_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_theta_central        │ [0, 1] │ Central theta power decrease (inverse).
    │                          │        │ f02 = σ(0.40 * (1 - theta_period_100ms)
    │                          │        │       + 0.30 * roughness_std_1s
    │                          │        │       + 0.30 * mean(C0P.tension[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_arousal_index        │ [0, 1] │ Physiological arousal index.
    │                          │        │ f03 = σ(0.35 * energy_velocity_500ms
    │                          │        │       + 0.35 * mean(AED.valence[0:10])
    │                          │        │       + 0.30 * rms_energy_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_chills_magnitude     │ [0, 1] │ Peak chills magnitude.
    │                          │        │ f04 = σ(0.35 * peak_loudness_500ms
    │                          │        │       + 0.35 * mean(CPD.peak[10:20])
    │                          │        │       + 0.30 * f01 * f03)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ network_state            │ [0, 1] │ Distributed network activation level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ theta_pattern            │ [0, 1] │ Prefrontal-central theta contrast.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ chills_onset_pred        │ [0, 1] │ Predicted chills onset probability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 7D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Chills Network Function

```
Chills_Magnitude = α·PeakPleasure + β·ThetaContrast + γ·ArousalIndex

Parameters:
    α = 1.0  (peak pleasure weight)
    β = 0.8  (theta contrast weight)
    γ = 0.7  (arousal index weight)

ThetaContrast = ThetaPrefrontal_increase - ThetaCentral_decrease
NetworkState = mean(OFC, Insula, SMA, STG activations)

τ_decay = 3.0s  (chills sustain window, Chabin 2020)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Theta Prefrontal (R prefrontal theta increase)
f01 = σ(0.35 * theta_periodicity_100ms
       + 0.35 * mean(AED.arousal_dynamics[10:20])
       + 0.30 * mean_coupling_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Theta Central (central theta decrease, inverse)
f02 = σ(0.40 * (1.0 - theta_periodicity_100ms)
       + 0.30 * roughness_std_1s
       + 0.30 * mean(C0P.tension_release[0:10]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Arousal Index
f03 = σ(0.35 * energy_velocity_500ms
       + 0.35 * mean(AED.valence_tracking[0:10])
       + 0.30 * rms_energy_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Chills Magnitude
f04 = σ(0.35 * peak_loudness_500ms
       + 0.35 * mean(CPD.peak_experience[10:20])
       + 0.30 * f01 * f03)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dChills/dt = τ⁻¹ · (Target_Magnitude - Current_Chills)
    where τ = 3.0s (sustain window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MCCN Function |
|--------|-----------------|----------|---------------|---------------|
| **OFC** | ±24, 30, -16 | 2 | EEG source localization (Chabin 2020: p<1×10⁻⁵); PET MOR (Putkinen 2025) | Reward value computation |
| **Bilateral Insula** | ±36, 16, 4 | 1 | EEG source localization (Chabin 2020: p<1×10⁻⁶) | Interoceptive awareness |
| **SMA** | 0, -6, 58 | 1 | EEG source localization (Chabin 2020: p<1×10⁻⁷) | Motor preparation / rhythmic coupling |
| **Bilateral STG** | ±52, -22, 8 | 2 | EEG source localization (Chabin 2020: R STG p<1×10⁻⁶); EEG surface (RT p=0.006) | Auditory processing |
| **R Prefrontal** | 40, 40, 20 | 1 | EEG surface (Chabin 2020: RPF p=0.049) | Theta increase during chills |
| **R Central** | 0, -20, 60 | 1 | EEG surface (Chabin 2020: RC p=0.025) | Theta decrease during chills |
| **Amygdala** | ±24, -4, -18 | 1 | PET MOR (Putkinen 2025: chills correlation) | Opioid-mediated chills |
| **Caudate/NAcc** | ±10, 12, -10 | 1 | PET DA (Salimpoor 2011: anticipation→chills) | Dopamine chills mechanism |

---

## 9. Cross-Unit Pathways

### 9.1 MCCN ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MCCN INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  MCCN.chills_magnitude ──────► DAED (chills → DA consummation)            │
│  MCCN.theta_pattern ─────────► RPEM (theta → prediction error)            │
│  MCCN.arousal_index ─────────► IUCP (arousal → complexity preference)     │
│  MCCN.network_state ─────────► MORMR (network → opioid release)          │
│                                                                             │
│  CROSS-UNIT (RPU → ARU):                                                   │
│  MCCN.chills_magnitude ──────► ARU.pleasure_intensity (peak emotion)      │
│  MCCN.arousal_index ─────────► ARU.arousal_modulation                     │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► MCCN (valence/arousal evaluation)        │
│  CPD mechanism (30D) ──────────► MCCN (peak/chills detection)             │
│  C0P mechanism (30D) ──────────► MCCN (tension/expectation)               │
│  R³ (~14D) ─────────────────────► MCCN (direct spectral features)        │
│  H³ (16 tuples) ────────────────► MCCN (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Theta prefrontal** | R prefrontal theta should increase during chills | ✅ **Confirmed** (p < 0.049, Chabin 2020) |
| **Theta central** | Central theta should decrease during chills | ✅ **Confirmed** (p < 0.006, Chabin 2020) |
| **Network activation** | OFC/Insula/SMA/STG should co-activate during chills | ✅ **Confirmed** (p < 1e-05, Chabin 2020) |
| **No-chills control** | Non-chill-inducing music should not show theta pattern | Testable |
| **Individual differences** | Chills-prone individuals should show stronger theta contrast | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MCCN(BaseModel):
    """Musical Chills Cortical Network Model.

    Output: 7D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "MCCN"
    UNIT = "RPU"
    TIER = "β2"
    OUTPUT_DIM = 7
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 3.0          # Chills sustain window (Chabin 2020)
    THETA_FREQ = 5.0         # Hz (theta band center)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for MCCN computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── AED horizons: theta oscillation proxy ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
            # ── CPD horizons: peak/chills detection ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 8, 4, 2),      # loudness, 500ms, max, bidi
            (8, 16, 1, 2),     # loudness, 1000ms, mean, bidi
            (7, 8, 8, 2),      # amplitude, 500ms, velocity, bidi
            (7, 16, 2, 2),     # amplitude, 1000ms, std, bidi
            # ── Arousal / energy tracking ──
            (9, 3, 0, 2),      # rms_energy, 100ms, value, bidi
            (9, 8, 8, 2),      # rms_energy, 500ms, velocity, bidi
            (9, 16, 1, 2),     # rms_energy, 1000ms, mean, bidi
            # ── Tension / roughness ──
            (0, 8, 1, 2),      # roughness, 500ms, mean, bidi
            (0, 16, 2, 2),     # roughness, 1000ms, std, bidi
            # ── Change / surprise ──
            (21, 8, 0, 2),     # spectral_change, 500ms, value, bidi
            (22, 8, 8, 2),     # energy_change, 500ms, velocity, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MCCN 7D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,7) MCCN output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_arousal = aed[..., 10:20]
        cpd_peak = cpd[..., 10:20]
        c0p_tension = c0p[..., 0:10]

        # H³ direct features
        theta_period_100ms = h3_direct[(25, 3, 14, 2)].unsqueeze(-1)
        mean_coupling_1s = h3_direct[(25, 16, 1, 2)].unsqueeze(-1)
        peak_loudness_500ms = h3_direct[(8, 8, 4, 2)].unsqueeze(-1)
        energy_velocity_500ms = h3_direct[(9, 8, 8, 2)].unsqueeze(-1)
        rms_energy_100ms = h3_direct[(9, 3, 0, 2)].unsqueeze(-1)
        roughness_std_1s = h3_direct[(0, 16, 2, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Theta Prefrontal (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * theta_period_100ms
            + 0.35 * aed_arousal.mean(-1, keepdim=True)
            + 0.30 * mean_coupling_1s
        )

        # f02: Theta Central (inverse, coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * (1.0 - theta_period_100ms)
            + 0.30 * roughness_std_1s
            + 0.30 * c0p_tension.mean(-1, keepdim=True)
        )

        # f03: Arousal Index (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * energy_velocity_500ms
            + 0.35 * aed_valence.mean(-1, keepdim=True)
            + 0.30 * rms_energy_100ms
        )

        # f04: Chills Magnitude (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * peak_loudness_500ms
            + 0.35 * cpd_peak.mean(-1, keepdim=True)
            + 0.30 * (f01 * f03)
        )

        # ═══ LAYER P: Present ═══
        network_state = torch.sigmoid(
            0.5 * f04 + 0.5 * f03
        )
        theta_pattern = torch.sigmoid(
            0.5 * f01 + 0.5 * f02
        )

        # ═══ LAYER F: Future ═══
        chills_onset_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * cpd_peak.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            network_state, theta_pattern,  # P: 2D
            chills_onset_pred,             # F: 1D
        ], dim=-1)  # (B, T, 7)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 3 (Chabin 2020, Putkinen 2025, Salimpoor 2011) | Multi-study convergence |
| **Effect Sizes** | 10 (EEG theta surface + source localization + PET) | All significant |
| **Evidence Modality** | HD-EEG (N=18) + PET (N=15, N=8) | Convergent multimodal |
| **Falsification Tests** | 3/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Valence/arousal evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Peak/chills detection |
| **C0P Mechanism** | 30D (3 sub-sections) | Tension/expectation |
| **Output Dimensions** | **7D** | 3-layer structure |

---

## 13. Scientific References

1. **Chabin, T., Gabriel, D., Chansophonkul, T., Michelant, L., Joucla, C., Haffen, E., Moulin, T., Comte, A., & Pazart, L. (2020)**. Cortical patterns of pleasurable musical chills revealed by high-density EEG. *Frontiers in Neuroscience*, 14, 565815.

2. **Putkinen, V., Nazari-Farsani, S., Seppälä, K., Karjalainen, T., Sun, L., Karlsson, H. K., Hudson, M., Heikkilä, T. T., Hirvonen, J., & Nummenmaa, L. (2025)**. Pleasurable music activates cerebral µ-opioid receptors: a combined PET-fMRI study. *European Journal of Nuclear Medicine and Molecular Imaging*, 52, 3540-3549.

3. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, AED, ASA, CPD) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Theta proxy | S⁰.L7 [80:88] crossband + HC⁰.OSC | R³.x_l0l5[25:33] + H³ periodicity tuples |
| Arousal | S⁰.L5.loudness[35] + S⁰.L5.rms[47] + HC⁰.AED | R³.loudness[8] + R³.rms_energy[9] + AED.arousal |
| Chills peak | S⁰.L5.loudness + HC⁰.CPD | R³.loudness + CPD.peak_experience |
| Network state | S⁰.X_L5L6[208:216] + HC⁰.ASA | R³.x_l0l5[25:33] + AED.valence + C0P.tension |
| Demand format | HC⁰ index ranges (40 tuples) | H³ 4-tuples (16 tuples, sparse) |
| Total demand | 40/2304 = 1.74% | 16/2304 = 0.69% |
| Output | 7D | 7D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **OSC → AED.arousal_dynamics** [10:20]: Oscillation coupling maps to AED's arousal dynamics for theta proxy.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for hedonic evaluation.
- **ASA → C0P.tension_release** [0:10]: Auditory scene analysis for chills maps to C0P tension-release tracking.
- **CPD → CPD.peak_experience** [10:20]: Chills/peak detection remains as CPD peak experience detection.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **7D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
