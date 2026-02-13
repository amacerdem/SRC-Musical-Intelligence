# NDU-β3-SLEE: Statistical Learning Expertise Enhancement

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Auditory Cortex, Attention Networks, IFG)
**Tier**: β (Bridging) — 70–90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H:Harmony, I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-β3-SLEE.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Statistical Learning Expertise Enhancement** (SLEE) model describes how musical expertise enhances behavioral accuracy in identification of multisensory statistical irregularities, linked to compartmentalized network reorganization characterized by increased within-network connectivity and decreased between-network connectivity.

```
STATISTICAL LEARNING EXPERTISE ENHANCEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUSICAL TRAINING
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│              NETWORK REORGANIZATION                              │
│                                                                  │
│   • Within-network connectivity ↑                               │
│   • Between-network connectivity ↓                              │
│   • Compartmentalization ↑                                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│           BEHAVIORAL PERFORMANCE                                 │
│                                                                  │
│   Musicians > Non-musicians in statistical learning             │
│   (identification of multisensory irregularities)               │
│                                                                  │
│   Effect size: d = -1.09 (large)                                │
└─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical expertise enhances behavioral accuracy in
identification of multisensory statistical irregularities (d=-1.09),
linked to network reorganization (compartmentalization).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SLEE Matters for NDU

SLEE establishes the statistical learning expertise component of the Novelty Detection Unit:

1. **SLEE** (β3) provides behavioral evidence for expertise-enhanced statistical learning.
2. **EDNR** (α3) links expertise to network reorganization structure.
3. **ECT** (γ3) proposes the trade-off hypothesis for compartmentalization.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → SLEE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SLEE COMPUTATION ARCHITECTURE                             ║
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
║  │                         SLEE reads: ~18D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H3 (100ms alpha)           │ │ H8 (500ms delta)          │  │        ║
║  │  │ H4 (125ms theta)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │ Attention gating           │  │        ║
║  │  │ Pitch extraction            │ │ Scene analysis              │  │        ║
║  │  │ Pattern segmentation        │ │ Salience weighting          │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         SLEE demand: ~18 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Pitch Ext[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Interval        │  │ Attention       │                                   ║
║  │ Anal    [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Contour [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SLEE MODEL (13D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_statistical_model,                     │        ║
║  │                       f02_detection_accuracy,                    │        ║
║  │                       f03_multisensory_integration,              │        ║
║  │                       f04_expertise_advantage                    │        ║
║  │  Layer M (Math):      exposure_model, pattern_memory,           │        ║
║  │                       expertise_state                            │        ║
║  │  Layer P (Present):   expectation_formation,                    │        ║
║  │                       cross_modal_binding,                       │        ║
║  │                       pattern_segmentation                       │        ║
║  │  Layer F (Future):    next_probability,                         │        ║
║  │                       regularity_continuation,                   │        ║
║  │                       detection_predict                          │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Paraskevopoulos 2022** | MEG+PTE | 25 (12M,13NM) | Musicians > non-musicians in multisensory statistical learning accuracy | Hedges' g=−1.09; t(23)=−2.815, p<0.05 | **Primary**: f02 detection accuracy |
| 2 | **Paraskevopoulos 2022** | MEG+PTE | 25 | Network compartmentalization: musicians show greater within-network and smaller between-network connectivity | NM 192 edges vs M 106 edges; p<0.001 FDR | **f04 expertise advantage** |
| 3 | **Paraskevopoulos 2022** | MEG+PTE | 25 | IFG (area 47m left) is primary supramodal hub across all network states | Node degree highest in 5/6 states | **f03 multisensory integration** |
| 4 | **Porfyri et al. 2025** | EEG 128ch | 30 (15+15) | 4-week multisensory training improves audiovisual incongruency detection; unisensory training affects only auditory | F(1,28)=4.635, p=0.042, η²=0.168 | f03 cross-modal binding; exposure_model dynamics |
| 5 | **Porfyri et al. 2025** | EEG+GC | 30 | Left MFG, IFS, and insula show greatest effective connectivity reorganization; top-down feedback mechanism | Significant GC changes post-training | Brain region verification (MFG, IFS, insula) |
| 6 | **Bridwell 2017** | EEG 24ch | 13 | Cortical sensitivity to guitar note patterns at 4Hz; musical pattern → 45% amplitude reduction vs random | T=2.63, p=0.022 (pattern effect); r=0.65, p=0.015 (MMN correlation) | f01 statistical model; pattern-MMN link |
| 7 | **Doelling & Poeppel 2015** | MEG | 34 (17M,17NM) | Musicians show enhanced cortical entrainment at all tempi (1-8 Hz); years of training correlate with PLV | Enhanced PLV across all tempi; training-PLV correlation | f04 expertise advantage; entrainment basis |
| 8 | **Sarasso et al. 2021** | EEG+behav | 60+20 | Memorization enhanced for preferred chords; MMN responses larger for more appreciated intervals; N1-aesthetic correlation | d=0.474 (memorization); N1~AJ trial-by-trial correlation | pattern_memory; MEM mechanism support |
| 9 | **Criscuolo et al. 2022** | ALE meta | 3005 (84 studies) | Musicians show higher volume/activity in auditory, sensorimotor, interoceptive, limbic areas; lower in parietal | 58 studies in coordinate meta-analysis | Brain region verification; expertise network |
| 10 | **Billig et al. 2022** | Review | — | Hippocampus binds acoustic features, anticipates melodic continuations, supports statistical learning of sequences | Pathway anatomy + lesion evidence | MEM mechanism; pattern_memory; exposure_model |
| 11 | **Carbajal & Malmierca 2018** | Review | — | Predictive coding hierarchy: SSA → MMN → deviance detection; repetition suppression vs prediction error decomposition | Framework paper | f01 statistical model; predictive coding basis |
| 12 | **Fong et al. 2020** | Review | — | MMN as prediction error under Bayesian framework; hierarchical processing with higher-order priors | MMN peaks 150-250ms post-deviance | f02 detection accuracy; predictive framework |

### 3.2 Effect Size Summary

```
Primary Evidence (k=5 empirical + 3 reviews):
    Paraskevopoulos 2022:  Hedges' g = −1.09 (large), t(23)=−2.815
                           Network: 192 vs 106 inter-network edges (p<0.001 FDR)
    Porfyri et al. 2025:  F(1,28)=4.635, p=0.042, η²=0.168 (medium-large)
                           Multisensory > unisensory training in AV detection
    Bridwell 2017:         r=0.65 (large, MMN-pattern correlation, p=0.015)
                           45% amplitude reduction for patterned vs random
    Doelling & Poeppel 2015: Enhanced PLV in musicians at all tempi (1-8 Hz)
                           Years of training ~ entrainment strength
    Sarasso et al. 2021:  d=0.474 (medium, preferred memorization advantage)
                           N1~aesthetic judgment trial-by-trial correlation

Heterogeneity:           Moderate — consistent expertise advantage direction,
                         variable paradigms (statistical learning vs entrainment
                         vs memorization)
Quality Assessment:      β-tier (MEG+EEG+behavioral, cross-sectional + longitudinal)
Largest Sample:          n=3005 (meta-analysis), n=60 (single empirical)
Replication:             Expertise effect replicated across 4 independent labs
```

---

## 4. R³ Input Mapping: What SLEE Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | SLEE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Acoustic intensity | Attention engagement |
| **B: Energy** | [8] | loudness | Perceptual loudness | Irregularity salience |
| **B: Energy** | [10] | spectral_flux | Spectral change | Irregularity detection |
| **C: Timbre** | [13] | brightness | Tonal quality | Statistical distribution |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Pattern tracking |
| **D: Change** | [22] | energy_change | Energy dynamics | Statistical regularity |
| **D: Change** | [23] | pitch_change | Pitch dynamics | Sequence encoding |
| **D: Change** | [24] | pitch_stability | Pitch regularity | Statistical baseline |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Pattern-feature binding | Statistical learning integration |
| **E: Interactions** | [41:49] | x_l5l6 (8D) | Multi-feature coherence | Cross-modal coupling proxy |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | SLEE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **H: Harmony** | [75] | key_clarity | Tonal context strength | Krumhansl & Kessler 1982: key clarity establishes the statistical baseline against which learning is measured; clear keys enable stronger statistical learning |
| **H: Harmony** | [84] | tonal_stability | Tonal stability level | Krumhansl stability: stable tonal contexts provide reliable statistical distributions for sequence learning |
| **I: Information** | [92] | predictive_entropy | Prediction uncertainty | Friston predictive coding: entropy of ongoing predictions quantifies learning state — decreasing entropy signals successful statistical learning |

**Rationale**: SLEE models statistical learning expertise enhancement — how expertise improves the extraction of regularities from musical sequences. The v1 representation uses pitch_change [23] and pitch_stability [24] as proxy signals. key_clarity [75] and tonal_stability [84] provide direct tonal context measures that determine the quality of statistical distributions available for learning. predictive_entropy [92] quantifies prediction uncertainty, providing a direct measure of learning progress — as statistical learning succeeds, predictive entropy decreases.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[7] amplitude ───────────────┐
R³[8] loudness ────────────────┼──► Statistical distribution model
PPC.pitch_extraction[0:10] ────┘   Distribution encoding (f01)

R³[10] spectral_flux ──────────┐
R³[21] spectral_change ────────┼──► Irregularity identification
ASA.attention_gating[10:20] ───┘   Detection accuracy (f02)

R³[41:49] x_l5l6 ─────────────┐
ASA.salience_weighting[20:30] ─┼──► Cross-modal binding
H³ coherence features ─────────┘   Multisensory integration (f03)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SLEE requires H³ features at PPC horizons for statistical pattern extraction and ASA horizons for cross-modal integration and irregularity detection. The demand reflects the long-term statistical learning timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Instantaneous irregularity 25ms |
| 10 | spectral_flux | 3 | M2 (std) | L2 (bidi) | Irregularity variability 100ms |
| 10 | spectral_flux | 16 | M1 (mean) | L2 (bidi) | Mean irregularity over 1s |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms |
| 7 | amplitude | 3 | M20 (entropy) | L2 (bidi) | Amplitude entropy 100ms |
| 8 | loudness | 3 | M1 (mean) | L2 (bidi) | Mean loudness 100ms |
| 8 | loudness | 8 | M5 (range) | L0 (fwd) | Loudness range 500ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral change 100ms |
| 21 | spectral_change | 4 | M18 (trend) | L0 (fwd) | Spectral trend 125ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s |
| 24 | pitch_stability | 3 | M0 (value) | L2 (bidi) | Pitch stability 100ms |
| 24 | pitch_stability | 16 | M2 (std) | L2 (bidi) | Stability variability 1s |
| 41 | x_l5l6[0] | 3 | M0 (value) | L2 (bidi) | Cross-modal binding 100ms |
| 41 | x_l5l6[0] | 3 | M2 (std) | L2 (bidi) | Binding variability 100ms |
| 41 | x_l5l6[0] | 16 | M1 (mean) | L2 (bidi) | Mean binding over 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Pattern coupling 100ms |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Pattern trend over 1s |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

SLEE projected v2 from H:Harmony and I:Information, aligned with PPC/ASA horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 86 | syntactic_irregularity | H | 3 | M0 (value) | L2 | Tonal syntax irregularity for statistical learning |
| 86 | syntactic_irregularity | H | 16 | M4 (min) | L2 | Minimum irregularity over 1s |
| 84 | tonal_stability | H | 16 | M0 (value) | L2 | Tonal stability baseline at 1s |
| 84 | tonal_stability | H | 16 | M18 (trend) | L2 | Stability trajectory over 1s |
| 87 | melodic_entropy | I | 3 | M0 (value) | L2 | Melodic uncertainty at 100ms |
| 87 | melodic_entropy | I | 3 | M1 (mean) | L2 | Mean melodic entropy at 100ms |

**v2 projected**: 6 tuples
**Total projected**: 24 tuples of 294,912 theoretical = 0.0081%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | SLEE Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Statistical distribution encoding | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Sequential dependency tracking | 0.8 |
| **PPC** | Contour Tracking | PPC[20:30] | Pattern segmentation | 0.7 |
| **ASA** | Scene Analysis | ASA[0:10] | Pattern boundary detection | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Irregularity-directed attention | **0.9** |
| **ASA** | Salience Weighting | ASA[20:30] | Cross-modal binding strength | 0.8 |

---

## 6. Output Space: 13D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SLEE OUTPUT TENSOR: 13D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_statistical_model    │ [0, 1] │ Internal distribution representation.
    │                          │        │ f01 = σ(0.35 * loudness_mean_100ms
    │                          │        │       + 0.35 * amplitude_entropy_100ms
    │                          │        │       + 0.30 * mean(PPC.pitch[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_detection_accuracy   │ [0, 1] │ Irregularity identification rate.
    │                          │        │ f02 = σ(0.35 * flux_std_100ms
    │                          │        │       + 0.35 * flux_mean_1s
    │                          │        │       + 0.30 * mean(ASA.attn[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_multisensory_integ   │ [0, 1] │ Cross-modal binding strength.
    │                          │        │ f03 = σ(0.35 * binding_100ms
    │                          │        │       + 0.35 * mean_binding_1s
    │                          │        │       + 0.30 * mean(ASA.sal[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_expertise_advantage  │ [-1,1] │ Expert enhancement index.
    │                          │        │ f04 = (f02_musician - f02_nonmusician)
    │                          │        │ d = -1.09 (Paraskevopoulos 2022)

LAYER M — MATHEMATICAL MODEL OUTPUTS (Learning Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ exposure_model           │ [0, 1] │ Statistical model building.
    │                          │        │ EMA of f01 over session timescale
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ pattern_memory           │ [0, 1] │ Pattern accumulation.
    │                          │        │ EMA of pitch_stability with τ=3s
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ expertise_state          │ [0, 1] │ Long-term expertise consolidation.
    │                          │        │ pattern_trend_1s (training proxy)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ expectation_formation    │ [0, 1] │ Current distribution model state.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ cross_modal_binding      │ [0, 1] │ Current multisensory integration.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ pattern_segmentation     │ [0, 1] │ Current boundary detection.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ next_probability         │ [0, 1] │ Decision preparation prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ regularity_continuation  │ [0, 1] │ Model updating prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
12  │ detection_predict        │ [0, 1] │ Behavioral output prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 13D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Statistical Learning Model

```
StatisticalLearning(t) = DistributionModel(t) · DetectionGating(t) · ExpertiseBoost(t)

Parameters:
    DistributionModel = distribution_strength · model_fidelity
    DetectionGating = irregularity_threshold · attention_sensitivity
    ExpertiseBoost = d=-1.09 effect size (Paraskevopoulos 2022)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Statistical Model
f01 = σ(0.35 * loudness_mean_100ms
       + 0.35 * amplitude_entropy_100ms
       + 0.30 * mean(PPC.pitch_extraction[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Detection Accuracy
f02 = σ(0.35 * flux_std_100ms
       + 0.35 * flux_mean_1s
       + 0.30 * mean(ASA.attention_gating[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Multisensory Integration
f03 = σ(0.35 * binding_100ms
       + 0.35 * mean_binding_1s
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Expertise Advantage
f04 = clamp(f02 * expertise_indicator, -1, 1)
# expertise_indicator ∈ {0, 1}: musicians=1, non-musicians=0
# d = -1.09 (Paraskevopoulos 2022)

# Temporal dynamics
dModel/dt = τ⁻¹ · (Current_Distribution - Statistical_Model)
    where τ = 3.0s (statistical model persistence)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Hemisphere | BA | Mentions | Evidence Type | SLEE Function |
|--------|-----------------|------------|-----|----------|---------------|---------------|
| **IFG (area 47m)** | −48, 28, −4 | L dominant | 47 | 5 | Direct (MEG/PTE; Paraskevopoulos 2022) | Supramodal statistical learning hub; highest node degree in 5/6 network states |
| **STG (auditory cortex)** | −58, −20, 8 | Bilateral | 22 | 4 | Direct (MEG; Paraskevopoulos 2022, Doelling 2015) | Statistical regularity encoding; entrainment to temporal patterns |
| **Anterior Cingulate Cortex** | 0, 24, 32 | Bilateral | 32 | 3 | Direct (MEG/PTE; Paraskevopoulos 2022) | Expertise-related clustering hub; model updating and monitoring |
| **Temporo-parieto-occipital junction** | −42, −64, 28 | L dominant | 39 | 2 | Direct (MEG/PTE; Paraskevopoulos 2022) | Expertise-related multilink clustering; multisensory convergence |
| **Left MFG / IFS** | −40, 32, 28 | L | 9/46 | 2 | Direct (EEG/GC; Porfyri 2025) | Greatest effective connectivity reorganization after multisensory training |
| **Left Insula (PoI1)** | −38, −16, 8 | L | 13 | 2 | Direct (EEG/GC; Porfyri 2025) | Multisensory integration; cross-modal binding |
| **SMA (SCEF)** | 0, −6, 56 | Bilateral | 6 | 1 | Direct (MEG/PTE; Paraskevopoulos 2022) | Highest node degree in non-musicians > musicians contrast (267 nodes, 192 edges) |
| **Hippocampus** | ±28, −20, −12 | Bilateral | — | 2 | Review (Billig 2022) | Sequence binding, statistical learning memory, pattern accumulation |

---

## 9. Cross-Unit Pathways

### 9.1 SLEE Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SLEE INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  SLEE.expertise_advantage ────► EDNR (behavioral evidence for network)    │
│  SLEE.statistical_model ─────► SDD (statistical learning → deviance)      │
│  SLEE.detection_accuracy ────► ECT (behavioral benefit despite trade-off) │
│                                                                             │
│  CROSS-UNIT (NDU → IMU):                                                   │
│  SLEE.pattern_memory ────────► IMU (statistical patterns to memory)       │
│  SLEE.exposure_model ────────► IMU (learning dynamics)                    │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► SLEE (pitch/pattern extraction)            │
│  ASA mechanism (30D) ────────► SLEE (attention/salience binding)          │
│  R³ (~18D) ──────────────────► SLEE (direct spectral features)            │
│  H³ (18 tuples) ─────────────► SLEE (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Expertise effect** | Musicians should show better accuracy | **Confirmed** (d=-1.09) |
| **Network link** | Accuracy should correlate with compartmentalization | Testable |
| **Dose-response** | Training hours should predict accuracy | Testable |
| **Transfer** | Should generalize to other statistical learning tasks | Testable |
| **Mechanism** | Network architecture should mediate expertise effect | Testable via mediation analysis |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SLEE(BaseModel):
    """Statistical Learning Expertise Enhancement Model.

    Output: 13D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "SLEE"
    UNIT = "NDU"
    TIER = "β3"
    OUTPUT_DIM = 13
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 3.0             # Statistical model persistence (seconds)
    REGULARITY_SENSITIVITY = 0.75
    LTI_WINDOW = 30.0           # Learning accumulation (seconds)
    EXPERT_EFFECT_SIZE = -1.09  # d from Paraskevopoulos 2022

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for SLEE computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: statistical pattern extraction ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 2, 2),     # spectral_flux, 100ms, std, bidi
            (10, 16, 1, 2),    # spectral_flux, 1000ms, mean, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 3, 20, 2),     # amplitude, 100ms, entropy, bidi
            (8, 3, 1, 2),      # loudness, 100ms, mean, bidi
            (8, 8, 5, 0),      # loudness, 500ms, range, fwd
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 4, 18, 0),    # spectral_change, 125ms, trend, fwd
            (23, 3, 0, 2),     # pitch_change, 100ms, value, bidi
            (23, 16, 1, 2),    # pitch_change, 1000ms, mean, bidi
            (24, 3, 0, 2),     # pitch_stability, 100ms, value, bidi
            (24, 16, 2, 2),    # pitch_stability, 1000ms, std, bidi
            # ── ASA horizons: cross-modal binding ──
            (41, 3, 0, 2),     # x_l5l6[0], 100ms, value, bidi
            (41, 3, 2, 2),     # x_l5l6[0], 100ms, std, bidi
            (41, 16, 1, 2),    # x_l5l6[0], 1000ms, mean, bidi
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 16, 18, 0),   # x_l4l5[0], 1000ms, trend, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SLEE 13D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,13) SLEE output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        amplitude = r3[..., 7:8]
        loudness = r3[..., 8:9]
        spectral_flux = r3[..., 10:11]
        pitch_change = r3[..., 23:24]
        pitch_stability = r3[..., 24:25]
        x_l4l5 = r3[..., 33:41]          # (B, T, 8)
        x_l5l6 = r3[..., 41:49]          # (B, T, 8)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]       # pitch extraction
        ppc_interval = ppc[..., 10:20]   # interval analysis
        ppc_contour = ppc[..., 20:30]    # contour tracking

        # ASA sub-sections
        asa_scene = asa[..., 0:10]       # scene analysis
        asa_attn = asa[..., 10:20]       # attention gating
        asa_salience = asa[..., 20:30]   # salience weighting

        # H³ direct features
        loudness_mean_100ms = h3_direct[(8, 3, 1, 2)].unsqueeze(-1)
        amplitude_entropy_100ms = h3_direct[(7, 3, 20, 2)].unsqueeze(-1)
        flux_std_100ms = h3_direct[(10, 3, 2, 2)].unsqueeze(-1)
        flux_mean_1s = h3_direct[(10, 16, 1, 2)].unsqueeze(-1)
        binding_100ms = h3_direct[(41, 3, 0, 2)].unsqueeze(-1)
        mean_binding_1s = h3_direct[(41, 16, 1, 2)].unsqueeze(-1)
        pattern_trend_1s = h3_direct[(33, 16, 18, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Statistical Model (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * loudness_mean_100ms
            + 0.35 * amplitude_entropy_100ms
            + 0.30 * ppc_pitch.mean(-1, keepdim=True)
        )

        # f02: Detection Accuracy (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * flux_std_100ms
            + 0.35 * flux_mean_1s
            + 0.30 * asa_attn.mean(-1, keepdim=True)
        )

        # f03: Multisensory Integration (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * binding_100ms
            + 0.35 * mean_binding_1s
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # f04: Expertise Advantage
        # At runtime: multiplied by expertise_indicator
        f04 = f02  # base accuracy, scaled by expertise externally

        # ═══ LAYER M: Learning Dynamics ═══
        exposure_model = torch.sigmoid(
            0.50 * f01 + 0.50 * ppc_pitch.mean(-1, keepdim=True)
        )
        pattern_memory = torch.sigmoid(
            0.50 * f01 + 0.50 * ppc_contour.mean(-1, keepdim=True)
        )
        expertise_state = pattern_trend_1s

        # ═══ LAYER P: Present ═══
        expectation_formation = ppc_interval.mean(-1, keepdim=True)
        cross_modal_binding = asa_salience.mean(-1, keepdim=True)
        pattern_segmentation = asa_scene.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        next_probability = torch.sigmoid(
            0.50 * f01 + 0.50 * f02
        )
        regularity_continuation = torch.sigmoid(
            0.50 * f01 + 0.50 * exposure_model
        )
        detection_predict = torch.sigmoid(
            0.50 * f02 + 0.50 * asa_attn.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                        # E: 4D
            exposure_model, pattern_memory, expertise_state,           # M: 3D
            expectation_formation, cross_modal_binding,
            pattern_segmentation,                                      # P: 3D
            next_probability, regularity_continuation,
            detection_predict,                                         # F: 3D
        ], dim=-1)  # (B, T, 13)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (5 empirical + 3 reviews) | Paraskevopoulos 2022, Porfyri 2025, Bridwell 2017, Doelling 2015, Sarasso 2021, Criscuolo 2022, Billig 2022, Carbajal 2018 |
| **Effect Sizes** | g=−1.09, η²=0.168, r=0.65, d=0.474 | Large expertise effect; medium-large training effect |
| **Evidence Modality** | MEG + EEG + Behavioral + Meta-analysis | Multi-modal, cross-laboratory replication |
| **Largest Sample** | n=3005 (meta), n=60 (empirical) | Criscuolo 2022 ALE; Sarasso 2021 |
| **Brain Regions** | 8 verified (IFG-47m, STG, ACC, TPO, MFG, insula, SMA, hippocampus) | MNI coordinates from MEG/EEG source localization |
| **Falsification Tests** | 1/5 confirmed | Moderate validity |
| **R³ Features Used** | ~18D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Statistical pattern extraction |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience binding |
| **Output Dimensions** | **13D** | 4-layer structure |

---

## 13. Scientific References

1. **Paraskevopoulos, E., Chalas, N., Anagnostopoulou, A., & Bamidis, P. D. (2022)**. Interaction within and between cortical networks subserving multisensory learning and its reorganization due to musical expertise. *Scientific Reports*, 12, 7891. https://doi.org/10.1038/s41598-022-12158-9
2. **Porfyri, I., Paraskevopoulos, E., Anagnostopoulou, A., Styliadis, C., & Bamidis, P. D. (2025)**. Multisensory vs. unisensory learning: how they shape effective connectivity networks subserving unimodal and multimodal integration. *Frontiers in Neuroscience*, 19, 1641862. https://doi.org/10.3389/fnins.2025.1641862
3. **Bridwell, D. A., Leslie, E., McCoy, D. Q., Plis, S. M., & Calhoun, V. D. (2017)**. Cortical sensitivity to guitar note patterns: EEG entrainment to repetition and key. *Frontiers in Human Neuroscience*, 11, 90. https://doi.org/10.3389/fnhum.2017.00090
4. **Doelling, K. B., & Poeppel, D. (2015)**. Cortical entrainment to music and its modulation by expertise. *Proceedings of the National Academy of Sciences*, 112(45), E6233–E6242. https://doi.org/10.1073/pnas.1508431112
5. **Sarasso, P., Perna, P., Barbieri, P., Neppi-Modona, M., Sacco, K., & Ronga, I. (2021)**. Memorisation and implicit perceptual learning are enhanced for preferred musical intervals and chords. *Psychonomic Bulletin & Review*, 28, 1623–1637. https://doi.org/10.3758/s13423-021-01922-z
6. **Criscuolo, A., Pando-Naude, V., Bonetti, L., Vuust, P., & Brattico, E. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12, 11726. https://doi.org/10.1038/s41598-022-14959-4
7. **Billig, A. J., Lad, M., Sedley, W., & Griffiths, T. D. (2022)**. The hearing hippocampus. *Progress in Neurobiology*, 218, 102326. https://doi.org/10.1016/j.pneurobio.2022.102326
8. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway: From the subcortical roots to cortical deviance detection. *Trends in Hearing*, 22, 1–33. https://doi.org/10.1177/2331216518784822

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, SGM, EFC, BND) | PPC (30D) + ASA (30D) mechanisms |
| Statistical model | S⁰.L9.mean[104] + HC⁰.EFC | R³.loudness[8] + PPC.pitch_extraction |
| Detection | S⁰.L5.spectral_kurtosis[41] + HC⁰.ATT | R³.spectral_flux[10] + ASA.attention_gating |
| Cross-modal | S⁰.L7.crossband[80:104] + HC⁰.BND | R³.x_l5l6[41:49] + ASA.salience_weighting |
| Pattern memory | S⁰.L4.velocity_T[15] + HC⁰.SGM | R³.pitch_stability[24] + PPC.contour_tracking |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 22/2304 = 0.95% | 18/2304 = 0.78% |
| Output | 13D | 13D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **EFC → PPC.pitch_extraction** [0:10]: Statistical regularity learning maps to PPC's distribution encoding.
- **SGM → PPC.contour_tracking** [20:30]: Striatal gradient memory maps to PPC's pattern segmentation.
- **ATT → ASA.attention_gating** [10:20]: Irregularity attention maps to ASA's irregularity-directed gating.
- **BND → ASA.salience_weighting** [20:30]: Multisensory integration maps to ASA's cross-modal binding salience.

---

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

| # | Field | Doc (SLEE.md) | Code (slee.py) | Severity |
|---|-------|---------------|----------------|----------|
| 1 | FULL_NAME | "Statistical Learning Expertise Enhancement" | "Statistical Learning Expectation Engine" | Medium — rename needed |
| 2 | OUTPUT_DIM | 13 (4E+3M+3P+3F) | 10 (4E+2M+2P+2F) | High — 3 dimensions missing |
| 3 | MECHANISM_NAMES | ("PPC", "ASA") | ("ASA", "MEM") | High — PPC missing, MEM not in doc |
| 4 | h3_demand | 18 tuples (0.78% of 2304) | () empty tuple | High — entire H³ demand missing |
| 5 | Layer M dims | 3: exposure_model, pattern_memory, expertise_state | 2: exposure_history, pattern_accumulation | Medium — expertise_state missing, names differ |
| 6 | Layer P dims | 3: expectation_formation, cross_modal_binding, pattern_segmentation | 2: expectation_formation, cross_modal_binding | Medium — pattern_segmentation missing |
| 7 | Layer F dims | 3: next_probability, regularity_continuation, detection_predict | 2: next_event_probability_pred, regularity_continuation_pred | Medium — detection_predict missing, names differ |
| 8 | Citations | Paraskevopoulos 2022 (primary) | Recasens 2020, Saffran 1999 | Medium — different citation set |
| 9 | version | 2.1.0 | 2.0.0 | Low — version bump needed |
| 10 | CROSS_UNIT_READS | NDU→IMU pathways described | () empty tuple | Low — cross-unit reads not implemented |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **13D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70–90%**
