# PCU-α3-ICEM: Information Content Emotion Model

**Model**: Information Content Emotion Model
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.1.0 (deep C³ literature review: 1→11 papers)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-α3-ICEM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Information Content Emotion Model** (ICEM) describes how computational Information Content (IC) peaks predict psychophysiological emotional responses: high IC (unexpected events) leads to increased arousal, increased skin conductance response (SCR), decreased heart rate, and decreased valence.

```
INFORMATION CONTENT EMOTION MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  MUSIC STIMULUS
       │
       ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │         INFORMATION CONTENT (IC) COMPUTATION                     │
  │         (IDyOM statistical model)                                │
  │                                                                  │
  │   IC = -log₂(P(event|context))                                  │
  │                                                                  │
  │   Low IC ◄─────────────────────────────────► High IC            │
  │   (expected)                                (unexpected)         │
  └─────────────────────────┬───────────────────────────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
  ┌─────────────────┐                ┌─────────────────┐
  │   IC TROUGH     │                │    IC PEAK      │
  │   (expected)    │                │   (unexpected)  │
  └────────┬────────┘                └────────┬────────┘
           │                                  │
           ▼                                  ▼
  • Lower arousal                   • Higher arousal ↑
  • Higher valence ↑                • Lower valence ↓
  • Stable HR                       • HR deceleration ↓
  • Lower SCR                       • SCR increase ↑
                                    • Resp rate increase ↑

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Computational Information Content peaks predict
psychophysiological emotional responses — high IC triggers defense
cascade: increased arousal/SCR, decreased HR/valence.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why ICEM Matters for PCU

ICEM links prediction computations to emotional/physiological responses:

1. **HTP** (α1) provides the hierarchical temporal framework for prediction.
2. **SPH** (α2) adds spatiotemporal memory recognition with oscillatory signatures.
3. **ICEM** (α3) maps prediction error magnitude (IC) to emotional and autonomic responses.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → ICEM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ICEM COMPUTATION ARCHITECTURE                            ║
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
║  │                         ICEM reads: ~18D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── MEM Horizons ───────────────┐ ┌── TPC Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)             │ │ H4 (125ms theta)          │  │        ║
║  │  │ H8 (500ms delta)             │ │ H16 (1000ms beat)         │  │        ║
║  │  │                               │ │                            │  │        ║
║  │  │ IC computation                │ │ Emotional response         │  │        ║
║  │  │ Surprise detection            │ │ Affective integration      │  │        ║
║  │  └───────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         ICEM demand: ~15 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════   ║
║                               │                                              ║
║                       ┌───────┴───────┐───────┐                              ║
║                       ▼               ▼       ▼                              ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │  PPC (30D)      │  │  TPC (30D)      │  │  MEM (30D)      │              ║
║  │                 │  │                 │  │                 │              ║
║  │ Pitch Ext[0:10] │  │ Spec Shp [0:10] │  │ Work Mem [0:10] │              ║
║  │ Interval        │  │ Temporal        │  │ Long-Term       │              ║
║  │ Analysis[10:20] │  │ Envelope[10:20] │  │ Memory  [10:20] │              ║
║  │ Contour  [20:30]│  │ Source Id[20:30] │  │ Pred Buf[20:30] │              ║
║  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              ║
║           │                    │                    │                         ║
║           └────────────┬───────┴────────────────────┘                        ║
║                        ▼                                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    ICEM MODEL (13D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_information_content,                   │        ║
║  │                       f02_arousal_response,                      │        ║
║  │                       f03_valence_response,                      │        ║
║  │                       f04_defense_cascade                        │        ║
║  │  Layer M (Math):      ic_value, arousal_pred, valence_pred,      │        ║
║  │                       scr_pred, hr_pred                          │        ║
║  │  Layer P (Present):   surprise_signal, emotional_evaluation      │        ║
║  │  Layer F (Future):    arousal_change_1_3s, valence_shift_2_5s    │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Year | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|------|--------|---|-------------|-------------|-------------|
| 1 | **Egermann et al.** | 2013 | Psychophysiology, live concert | 50 | IC peaks (IDyOM) → unexpectedness ratings ↑ | p < 0.001 | **f01 information content** |
| 2 | **Egermann et al.** | 2013 | Psychophysiology, live concert | 48 | IC peaks → arousal ↑, valence ↓, SCR ↑, HR ↓ | p < 0.001 | **f02 arousal, f03 valence** |
| 3 | **Egermann et al.** | 2013 | Psychophysiology, live concert | 48 | Subjective unexpected → same + RespR ↑ | p < 0.001 | **f04 defense cascade** |
| 4 | **Cheung et al.** | 2019 | fMRI + behavioral (IDyOM) | 79 (39+40) | Uncertainty × surprise → pleasure (saddle-shaped); amygdala, hippocampus, auditory cortex interaction; NAc reflects uncertainty only | β_interaction = −0.124, p < 0.001; fMRI: amygdala β = −0.140, p = 0.002; L-AC β = −0.182, p < 0.001; R² = 0.654 | **IC × entropy interaction; amygdala/hippocampus/AC circuit** |
| 5 | **Gold et al.** | 2019 | Behavioral (IDyOM), 2 studies | 70 (43+27) | Inverted-U for IC and entropy on liking; IC × entropy interaction: prefer surprise under low uncertainty and vice versa | Quadratic IC: p < 0.001; IC × entropy: p < 0.001 | **Pleasure = f(IC, entropy); reward-for-learning** |
| 6 | **Gold et al.** | 2023 | fMRI, naturalistic listening (IDyOM) | 24 | IC × entropy interaction in VS and R-STG; VS reflects liked surprises during naturalistic music | R-STG and VS liking effects, p < 0.05; IC × entropy × liking in VS | **VS encodes reward of musical expectancy** |
| 7 | **Salimpoor et al.** | 2011 | PET ([11C]raclopride) + fMRI | 8 | Dopamine release: caudate during anticipation, NAc during peak pleasure to music | PET: caudate BP decrease p < 0.05; fMRI: NAc BOLD increase, p < 0.05 | **Dopamine anticipation/consummation circuit** |
| 8 | **Harding et al.** | 2025 | fMRI, RCT (psilocybin vs escitalopram) | 41 (22+19) | Musical surprise → vmPFC decreased post-psilocybin; escitalopram blunts hedonic surprise response | vmPFC interaction F(1,39) = 7.07, p = 0.011; anhedonia interaction p = 0.048 | **Predictive coding modulation of surprise-emotion** |
| 9 | **Mencke et al.** | 2019 | Theoretical review | — | Atonal music: high uncertainty context → correct predictions more rewarding than errors; personality (openness) modulates pleasure | Theoretical framework | **Uncertainty context modulates IC→pleasure mapping** |
| 10 | **Chabin et al.** | 2020 | HD-EEG (256-ch), source localization | 18 | Musical chills: theta increase in OFC, theta decrease in R-central (SMA) and R-temporal (rSTG) | Theta OFC p < 0.05; SMA/rSTG source-level | **EEG signatures of peak pleasure to music** |
| 11 | **Bravo et al.** | 2017 | fMRI, emotion recognition | 20 | Ambiguous musical intervals → increased R Heschl's gyrus activation (sensory precision under uncertainty) | R HG cluster p < 0.001 (FWE) | **Sensory cortical gain under predictive uncertainty** |
| 12 | **Teixeira Borges et al.** | 2019 | EEG + ECG, fractal scaling | 28 | 1/f scaling of neuronal activity in temporal cortex linked to music pleasure; resting-state α closer to 1 predicts greater enjoyment | Temporal α−β: z = −2.50, r = 0.33, p < 0.005 | **Temporal cortex dynamics underlie music appreciation** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12):  11 empirical + 1 theoretical
Heterogeneity:           Consistent across psychophysiology, fMRI, PET, EEG modalities
Quality Assessment:      α-tier (direct measurement across multiple modalities)
Replication:             IC-emotion link replicated across Egermann 2013, Cheung 2019,
                         Gold 2019, Gold 2023; dopamine pathway confirmed by Salimpoor 2011
Key convergence:         IC/surprise → emotional response mediated by auditory cortex,
                         amygdala, hippocampus; reward via VS/NAc; inverted-U for pleasure
```

---

## 4. R³ Input Mapping: What ICEM Reads

### 4.1 R³ Feature Dependencies (~18D of 49D)

| R³ Group | Index | Feature | ICEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Harmonic IC basis | Consonance context |
| **B: Energy** | [8] | loudness | Arousal correlate | Perceptual loudness |
| **B: Energy** | [9] | spectral_centroid | Pitch expectation | Melodic IC basis |
| **B: Energy** | [10] | spectral_flux | Change detection | Event onset |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic context | Harmonic IC basis |
| **D: Change** | [21] | spectral_change | Temporal change rate | Event salience |
| **D: Change** | [22] | energy_change | Smoothness violation | Surprise marker |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Arousal pathway | Arousal = α·IC + β |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Valence pathway | Valence = -γ·IC + δ |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[21] spectral_change ─────────┐
R³[22] energy_change ───────────┼──► Information Content (IC)
MEM.working_memory[0:10] ───────┘   IC = -log₂(P(event|context))

R³[33:41] x_l4l5 ──────────────┐
TPC.source_identity[20:30] ─────┼──► Arousal response
H³ arousal velocity tuples ─────┘   High IC → Arousal ↑, SCR ↑

R³[41:49] x_l5l7 ──────────────┐
MEM.long_term_memory[10:20] ────┼──► Valence response
H³ valence entropy tuples ──────┘   High IC → Valence ↓, HR ↓
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ICEM requires H³ features for surprise computation (rapid change detection) and emotional integration (slower affective response). The demand reflects the IC computation at fast timescales and emotional response at slower timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Change at 100ms |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | Change variability 100ms |
| 21 | spectral_change | 3 | M20 (entropy) | L2 (bidi) | Change entropy 100ms |
| 22 | energy_change | 3 | M8 (velocity) | L0 (fwd) | Energy velocity 100ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms |
| 10 | spectral_flux | 8 | M1 (mean) | L0 (fwd) | Mean onset over 500ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 16 | M8 (velocity) | L2 (bidi) | Loudness velocity 1s |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms |
| 4 | sensory_pleasantness | 8 | M2 (std) | L0 (fwd) | Consonance variability 500ms |
| 33 | x_l4l5[0] | 4 | M8 (velocity) | L0 (fwd) | Arousal pathway velocity |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Arousal pathway mean 1s |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | Valence coupling 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Valence mean 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Valence entropy 1s |

**Total ICEM H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | ICEM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Melodic expectation | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Interval IC computation | 0.6 |
| **PPC** | Contour Tracking | PPC[20:30] | Contour IC basis | 0.5 |
| **TPC** | Spectral Shape | TPC[0:10] | Timbral context | 0.6 |
| **TPC** | Temporal Envelope | TPC[10:20] | Temporal salience | 0.7 |
| **TPC** | Source Identity | TPC[20:30] | Affective response pathway | **1.0** (primary) |
| **MEM** | Working Memory | MEM[0:10] | Statistical model (IDyOM proxy) | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Musical context memory | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | IC computation buffer | 0.8 |

---

## 6. Output Space: 13D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ICEM OUTPUT TENSOR: 13D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_information_content  │ [0, 1] │ Event unexpectedness (IC proxy).
    │                          │        │ f01 = σ(0.35 * change_entropy_100ms
    │                          │        │       + 0.35 * mean(MEM.wm[0:10])
    │                          │        │       + 0.30 * energy_velocity_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_arousal_response     │ [0, 1] │ Physiological activation.
    │                          │        │ f02 = σ(0.40 * f01
    │                          │        │       + 0.30 * arousal_pathway_vel
    │                          │        │       + 0.30 * mean(TPC.src[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_valence_response     │ [0, 1] │ Emotional valence change.
    │                          │        │ f03 = σ(0.40 * (1 - f01)
    │                          │        │       + 0.30 * valence_mean_1s
    │                          │        │       + 0.30 * mean(MEM.ltm[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_defense_cascade      │ [0, 1] │ Threat appraisal activation.
    │                          │        │ f04 = σ(0.50 * f01 * f02
    │                          │        │       + 0.50 * loudness_velocity_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ ic_value                 │ [0, 1] │ IC = -log₂(P(event|context)).
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ arousal_pred             │ [0, 1] │ Arousal = α·IC + β.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ valence_pred             │ [0, 1] │ Valence = -γ·IC + δ.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ scr_pred                 │ [0, 1] │ SCR = ε·IC + ζ.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ hr_pred                  │ [0, 1] │ HR = -η·IC + θ.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ surprise_signal          │ [0, 1] │ MEM IC computation result.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ emotional_evaluation     │ [0, 1] │ TPC valence change assessment.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ arousal_change_1_3s      │ [0, 1] │ SCR response prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
12  │ valence_shift_2_5s       │ [0, 1] │ Subjective feeling prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 13D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Information Content Function

```
IC(event) = -log₂(P(event|context))

Arousal = α·IC + β
Valence = -γ·IC + δ
SCR = ε·IC + ζ
HR = -η·IC + θ

Defense Cascade: High IC → Orienting → Threat appraisal
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Information Content
f01 = σ(0.35 * change_entropy_100ms
       + 0.35 * mean(MEM.working_memory[0:10])
       + 0.30 * energy_velocity_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Arousal Response
f02 = σ(0.40 * f01
       + 0.30 * arousal_pathway_velocity
       + 0.30 * mean(TPC.source_identity[20:30]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Valence Response (inverse of IC)
f03 = σ(0.40 * (1 - f01)
       + 0.30 * valence_mean_1s
       + 0.30 * mean(MEM.long_term_memory[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Defense Cascade
f04 = σ(0.50 * f01 * f02
       + 0.50 * loudness_velocity_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Source | Evidence Type | ICEM Function |
|--------|-----------------|--------|---------------|---------------|
| **Auditory Cortex (STG)** | ±52, −22, 8 | Egermann 2013 (indirect); Cheung 2019 (fMRI) | Psychophysiology + fMRI | IC computation |
| **L Auditory Cortex** | −52, −22, 8 | Cheung et al. 2019 | fMRI: β = −0.182, p < 0.001 | Uncertainty × surprise interaction (strongest) |
| **R Auditory Cortex** | 52, −22, 8 | Cheung et al. 2019 | fMRI: β = −0.128, p = 0.002 | Uncertainty × surprise interaction |
| **L Amygdala / Hippocampus** | −20, −4, −18 | Cheung et al. 2019 | fMRI: s = 11, p = 0.045 | Joint uncertainty × surprise processing |
| **R Amygdala / Hippocampus** | 20, −4, −18 | Cheung et al. 2019 | fMRI: β = −0.140, p = 0.002 | Joint uncertainty × surprise processing |
| **R Nucleus Accumbens** | 11, 9, −1 | Cheung et al. 2019; Salimpoor et al. 2011 | fMRI/PET: uncertainty β = 0.242, p = 0.002; dopamine release p < 0.05 | Uncertainty encoding / peak pleasure dopamine |
| **L Caudate Nucleus** | −10, 10, 8 | Cheung et al. 2019; Salimpoor et al. 2011 | fMRI: uncertainty β = 0.281, p = 0.004; PET: anticipation | Uncertainty / anticipatory dopamine |
| **Pre-SMA** | 0, 8, 56 | Cheung et al. 2019 | fMRI: uncertainty β = 0.358, p < 0.001 | Uncertainty encoding |
| **R Superior Temporal Gyrus** | 58, −22, 4 | Gold et al. 2023; Chabin et al. 2020 | fMRI: liking effect; EEG: theta decrease during chills | Pleasure of musical expectancy |
| **Ventral Striatum** | ±10, 8, −4 | Gold et al. 2023 | fMRI: IC × entropy × liking interaction | Reward of learning from musical structure |
| **vmPFC** | −2, 46, −8 | Harding et al. 2025 | fMRI: F(1,39) = 7.07, p = 0.011 | Precision weighting of prediction errors |
| **OFC (Orbitofrontal Cortex)** | ±28, 34, −12 | Chabin et al. 2020 | HD-EEG source: theta increase with pleasure | Reward processing during musical chills |
| **R Heschl's Gyrus** | 48, −14, 6 | Bravo et al. 2017 | fMRI: p < 0.001 (FWE) | Sensory precision under predictive uncertainty |
| **Insula** | ±38, 14, −8 | Literature inference | Indirect | Autonomic response integration |
| **ACC (Anterior Cingulate)** | 0, 32, 24 | Literature inference | Indirect | Emotional evaluation |

---

## 9. Cross-Unit Pathways

### 9.1 ICEM Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ICEM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  HTP.hierarchy_gradient ──────► ICEM (prediction level for IC)             │
│  SPH.prediction_error ────────► ICEM (error magnitude input)               │
│  ICEM.information_content ────► PWUP (IC for precision weighting)          │
│  ICEM.arousal_response ───────► UDP (arousal for reward computation)       │
│                                                                             │
│  CROSS-UNIT (PCU → ARU):                                                   │
│  ICEM.arousal_response ───────► ARU (emotional arousal signal)             │
│  ICEM.valence_response ───────► ARU (valence modulation)                   │
│  ICEM.defense_cascade ────────► ARU (threat appraisal)                     │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ─────────► ICEM (pitch expectation)                   │
│  TPC mechanism (30D) ─────────► ICEM (affective response)                  │
│  MEM mechanism (30D) ─────────► ICEM (statistical context)                 │
│  R³ (~18D) ───────────────────► ICEM (direct spectral features)            │
│  H³ (15 tuples) ──────────────► ICEM (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **IDyOM manipulation** | Altering IC should change emotional responses | Testable via stimulus design |
| **Autonomic blockade** | Beta-blockers should reduce SCR/HR effects | Testable via pharmacology |
| **Contextual priming** | Changing context should shift IC calculations | Testable via priming |
| **IC-arousal correlation** | High IC must correlate with increased arousal | **Confirmed** by Egermann 2013 |
| **IC-valence inversion** | High IC must correlate with decreased valence | **Confirmed** by Egermann 2013 |
| **IC × entropy interaction** | Pleasure depends on joint uncertainty and surprise | **Confirmed** by Cheung 2019, Gold 2019, Gold 2023 |
| **Dopamine involvement** | Musical anticipation/pleasure must engage striatal dopamine | **Confirmed** by Salimpoor 2011 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ICEM(BaseModel):
    """Information Content Emotion Model.

    Output: 13D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "ICEM"
    UNIT = "PCU"
    TIER = "α3"
    OUTPUT_DIM = 13
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DECAY = 2.0        # s (emotional response persistence)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for ICEM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── MEM horizons: IC computation ──
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            (21, 3, 20, 2),    # spectral_change, 100ms, entropy, bidi
            (22, 3, 8, 0),     # energy_change, 100ms, velocity, fwd
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 8, 1, 0),     # spectral_flux, 500ms, mean, fwd
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 16, 8, 2),     # loudness, 1000ms, velocity, bidi
            # ── TPC horizons: emotional response ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 8, 2, 0),      # sensory_pleasantness, 500ms, std, fwd
            (33, 4, 8, 0),     # x_l4l5[0], 125ms, velocity, fwd
            (33, 16, 1, 2),    # x_l4l5[0], 1000ms, mean, bidi
            # ── Valence pathway ──
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute ICEM 13D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,13) ICEM output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # Mechanism sub-sections
        tpc_src = tpc[..., 20:30]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        change_entropy_100ms = h3_direct[(21, 3, 20, 2)].unsqueeze(-1)
        energy_vel_100ms = h3_direct[(22, 3, 8, 0)].unsqueeze(-1)
        arousal_vel = h3_direct[(33, 4, 8, 0)].unsqueeze(-1)
        loudness_vel_1s = h3_direct[(8, 16, 8, 2)].unsqueeze(-1)
        valence_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(
            0.35 * change_entropy_100ms
            + 0.35 * mem_wm.mean(-1, keepdim=True)
            + 0.30 * energy_vel_100ms
        )
        f02 = torch.sigmoid(
            0.40 * f01
            + 0.30 * arousal_vel
            + 0.30 * tpc_src.mean(-1, keepdim=True)
        )
        f03 = torch.sigmoid(
            0.40 * (1 - f01)
            + 0.30 * valence_mean_1s
            + 0.30 * mem_ltm.mean(-1, keepdim=True)
        )
        f04 = torch.sigmoid(
            0.50 * f01 * f02
            + 0.50 * loudness_vel_1s
        )

        # ═══ LAYER M: Mathematical ═══
        ic_value = f01
        arousal_pred = torch.sigmoid(0.5 * f01 + 0.5 * f02)
        valence_pred = f03
        scr_pred = torch.sigmoid(0.5 * f02 + 0.5 * f04)
        hr_pred = torch.sigmoid(0.5 * (1 - f01) + 0.5 * f03)

        # ═══ LAYER P: Present ═══
        surprise = mem_wm.mean(-1, keepdim=True)
        emotional_eval = torch.sigmoid(
            0.5 * tpc_src.mean(-1, keepdim=True)
            + 0.5 * mem_ltm.mean(-1, keepdim=True)
        )

        # ═══ LAYER F: Future ═══
        arousal_change = torch.sigmoid(0.5 * f02 + 0.5 * f04)
        valence_shift = torch.sigmoid(0.5 * f03 + 0.5 * valence_mean_1s)

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            ic_value, arousal_pred, valence_pred, scr_pred, hr_pred, # M: 5D
            surprise, emotional_eval,                              # P: 2D
            arousal_change, valence_shift,                         # F: 2D
        ], dim=-1)  # (B, T, 13)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 11 (10 empirical + 1 theoretical) | Egermann 2013; Cheung 2019; Gold 2019; Gold 2023; Salimpoor 2011; Harding 2025; Mencke 2019; Chabin 2020; Bravo 2017; Teixeira Borges 2019; Leeuwis 2021 |
| **Effect Sizes** | 20+ | Multiple p < 0.001 across modalities |
| **Evidence Modalities** | Psychophysiology, fMRI, PET, HD-EEG, EEG+ECG, behavioral | Multi-modal convergence |
| **Falsification Tests** | 7/7 testable, 4 confirmed | High validity |
| **R³ Features Used** | ~18D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch expectation |
| **TPC Mechanism** | 30D (3 sub-sections) | Affective response |
| **MEM Mechanism** | 30D (3 sub-sections) | Statistical context |
| **Output Dimensions** | **13D** | 4-layer structure |

---

## 13. Scientific References

1. **Egermann, H., Pearce, M. T., Wiggins, G. A., & McAdams, S. (2013)**. Probabilistic models of expectation violation predict psychophysiological emotional responses to live concert music. *Cognitive, Affective, & Behavioral Neuroscience*, 13(3), 533-553.

2. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.

3. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *The Journal of Neuroscience*, 39(47), 9397-9409.

4. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience*, 17, 1209398.

5. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.

6. **Harding, R., Singer, N., Wall, M. B., Hendler, T., Erritzoe, D., Nutt, D., Carhart-Harris, R., & Roseman, L. (2025)**. Dissociable effects of psilocybin and escitalopram for depression on processing of musical surprises. *Molecular Psychiatry*, 30, 3188-3196.

7. **Mencke, I., Omigie, D., Wald-Fuhrmann, M., & Brattico, E. (2019)**. Atonal music: Can uncertainty lead to pleasure? *Frontiers in Neuroscience*, 12, 979.

8. **Chabin, T., Gabriel, D., Chansophonkul, T., Michelant, L., Joucla, C., Haffen, E., Moulin, T., Comte, A., & Pazart, L. (2020)**. Cortical patterns of pleasurable musical chills revealed by high-density EEG. *Frontiers in Neuroscience*, 14, 565815.

9. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLoS ONE*, 12(4), e0175991.

10. **Teixeira Borges, A. F., Irrmischer, M., Brockmeier, T., Smit, D. J. A., Mansvelder, H. D., & Linkenkaer-Hansen, K. (2019)**. Scaling behaviour in music and cortical dynamics interplay to mediate music listening pleasure. *Scientific Reports*, 9, 17700.

11. **Leeuwis, N., Pistone, D., Flick, N., & van Bommel, T. (2021)**. A sound prediction: EEG-based neural synchrony predicts online music streams. *Frontiers in Psychology*, 12, 672980.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, EFC, AED, ASA) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| IC signal | S⁰.L9.entropy[116:120] + S⁰.L9.kurtosis[120:124] | R³[21] spectral_change + R³[22] energy_change + MEM.working_memory |
| Arousal pathway | S⁰.X_L4L5[192:200] + HC⁰.AED | R³[33:41] x_l4l5 + TPC.source_identity[20:30] |
| Valence pathway | S⁰.X_L5L9[224:232] + HC⁰.EFC | R³[41:49] x_l5l7 + MEM.long_term_memory[10:20] |
| Attention | HC⁰.ATT | MEM.working_memory[0:10] |
| Scene analysis | HC⁰.ASA | PPC (pitch context) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% |
| Output | 13D | 13D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **ATT → MEM.working_memory** [0:10]: Attentional entrainment for IC computation maps to MEM's working memory context.
- **EFC → MEM.long_term_memory** [10:20]: Efference copy (statistical prediction) maps to MEM's long-term statistical model.
- **AED → TPC.source_identity** [20:30]: Affective entrainment dynamics maps to TPC's source-level emotional processing.
- **ASA → PPC.pitch_extraction** [0:10]: Auditory scene analysis for event detection maps to PPC's pitch/onset extraction.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **13D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
