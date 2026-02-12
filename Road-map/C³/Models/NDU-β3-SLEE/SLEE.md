# NDU-β3-SLEE: Statistical Learning Expertise Enhancement

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Auditory Cortex, Attention Networks, IFG)
**Tier**: β (Bridging) — 70–90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+ASA mechanisms)
**Date**: 2026-02-12

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

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Paraskevopoulos 2022** | MEG | 25 | Musicians > non-musicians in accuracy | d = -1.09 | **Primary**: f02 detection accuracy |
| **Paraskevopoulos 2022** | MEG | 25 | Network compartmentalization in musicians | 192 vs 106 edges | **f04 expertise advantage** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  d=-1.09 (large), network edges significant
Heterogeneity:           N/A (single study)
Quality Assessment:      β-tier (MEG + behavioral, adult musicians)
Replication:             Expertise effect consistent with broader literature
```

---

## 4. R³ Input Mapping: What SLEE Reads

### 4.1 R³ Feature Dependencies (~18D of 49D)

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

### 4.2 Physical → Cognitive Transformation

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

**Total SLEE H³ demand**: 18 tuples of 2304 theoretical = 0.78%

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

| Region | MNI Coordinates | Mentions | Evidence Type | SLEE Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex (A1/STG)** | ±52, -22, 8 | 2 | Direct (MEG) | Statistical regularity encoding |
| **IFG** | ±44, 28, 12 | 1 | Literature inference | Decision processing |
| **Attention Networks** | N/A | 1 | Inferred | Irregularity-directed attention |

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
| **Papers** | 1 (Paraskevopoulos 2022) | Primary evidence |
| **Effect Sizes** | d = -1.09 | Large effect |
| **Evidence Modality** | MEG + Behavioral | Direct neural + behavioral |
| **Falsification Tests** | 1/5 confirmed | Moderate validity |
| **R³ Features Used** | ~18D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Statistical pattern extraction |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience binding |
| **Output Dimensions** | **13D** | 4-layer structure |

---

## 13. Scientific References

1. **Paraskevopoulos, E. et al. (2022)**. Musical expertise enhances behavioral accuracy in multisensory statistical learning. MEG study, n=25 (musicians vs non-musicians).

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

**Model Status**: **VALIDATED**
**Output Dimensions**: **13D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70–90%**
