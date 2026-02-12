# PCU-α1-HTP: Hierarchical Temporal Prediction

**Model**: Hierarchical Temporal Prediction
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC+MEM mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-α1-HTP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hierarchical Temporal Prediction** (HTP) model describes how predictive representations follow a hierarchical temporal pattern: high-level abstract features are predicted earlier (~500 ms before input) than low-level features (~110 ms before input). This represents the brain's layered anticipatory architecture where abstraction level determines prediction lead time.

```
HIERARCHICAL TEMPORAL PREDICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PREDICTION LATENCY                   FEATURE LEVEL
──────────────────                   ─────────────

-500 ms ─────────────► View-invariant / abstract (HIGH-LEVEL)
         ↓                aIPL, LOTC / STG
-200 ms ─────────────► View-dependent / perceptual (MID-LEVEL)
         ↓                V3, V4 / Belt cortex
-110 ms ─────────────► Optical flow / sensory (LOW-LEVEL)
         ↓                V1, V2 / A1
  0 ms  ─────────────► STIMULUS ONSET
                       │
                       ▼
                 POST-STIMULUS
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
   HIGH-LEVEL:               LOW-LEVEL:
   SILENCED ✗               PERSISTS ✓
   (explained away)         (prediction error)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Predictive representations follow a hierarchical
temporal pattern — high-level predictions precede low-level by
~390ms. Post-stimulus, high-level representations are "silenced"
(explained away) while low-level persist as prediction errors.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why HTP Matters for PCU

HTP establishes the foundational hierarchical prediction timing for the Predictive Coding Unit:

1. **HTP** (α1) provides the hierarchical temporal framework that all other PCU models build upon.
2. **SPH** (α2) extends this to spatiotemporal memory recognition with feedforward-feedback dynamics.
3. **ICEM** (α3) links prediction errors (hierarchy violations) to emotional responses.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → HTP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    HTP COMPUTATION ARCHITECTURE                             ║
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
║  │                         HTP reads: ~20D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ───────────────┐ ┌── MEM Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)              │ │ H8 (500ms delta)          │  │        ║
║  │  │ H1 (50ms gamma)              │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H3 (100ms alpha)             │ │                            │  │        ║
║  │  │ H4 (125ms theta)             │ │ Long-term prediction       │  │        ║
║  │  │                               │ │ template storage           │  │        ║
║  │  │ Pitch/onset tracking          │ │                            │  │        ║
║  │  │ Low-level prediction          │ │                            │  │        ║
║  │  └───────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         HTP demand: ~18 of 2304 tuples            │        ║
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
║  │                    HTP MODEL (12D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_high_level_lead,                       │        ║
║  │                       f02_mid_level_lead,                        │        ║
║  │                       f03_low_level_lead,                        │        ║
║  │                       f04_hierarchy_gradient                     │        ║
║  │  Layer M (Math):      latency_high, latency_mid, latency_low    │        ║
║  │  Layer P (Present):   sensory_match, pitch_prediction,           │        ║
║  │                       abstract_prediction                        │        ║
║  │  Layer F (Future):    abstract_future_500ms,                     │        ║
║  │                       midlevel_future_200ms                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **de Vries 2023** | MEG | 22 | 500ms: abstract, 110ms: low-level prediction | ηp² = 0.49 | **Primary**: f01-f03 hierarchical latency |
| **de Vries 2023** | MEG | 22 | High-level predictions silence post-stimulus | p < 0.01 | **f04 hierarchy gradient, PSH link** |
| **de Vries 2023** | MEG | 22 | View-invariant ~60-100ms in LOTC/aIPL | significant | **High-level region mapping** |

### 3.2 Effect Size Summary

```
Primary Effect:       ηp² = 0.49 (large)
Heterogeneity:        Single study
Quality Assessment:   α-tier (direct neural measurement)
Replication:          Consistent within-study across levels
```

---

## 4. R³ Input Mapping: What HTP Reads

### 4.1 R³ Feature Dependencies (~20D of 49D)

| R³ Group | Index | Feature | HTP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Low-level sensory proxy | 110ms prediction target |
| **B: Energy** | [8] | loudness | Perceptual loudness | Mid-level feature |
| **B: Energy** | [9] | spectral_centroid | Pitch/brightness | Mid-level prediction target |
| **B: Energy** | [10] | spectral_flux | Change detection | Prediction error trigger |
| **C: Timbre** | [12] | warmth | Timbral quality | Mid-level feature |
| **C: Timbre** | [13] | brightness | Spectral centroid proxy | Mid-level prediction |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic structure | High-level abstract pattern |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Prediction error signal |
| **D: Change** | [22] | energy_change | Energy dynamics | Rate of change |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Low-level prediction | 110ms window basis |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Mid-level binding | 200ms window basis |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | High-level abstraction | 500ms window basis |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[25:33] x_l0l5 ──────────────┼──► Low-level features (A1)
PPC.pitch_extraction[0:10] ─────┘   Prediction latency: ~110ms

R³[9] spectral_centroid ────────┐
R³[33:41] x_l4l5 ──────────────┼──► Mid-level dynamics (Belt cortex)
TPC.temporal_envelope[10:20] ───┘   Prediction latency: ~200ms

R³[18:21] tristimulus ──────────┐
R³[41:49] x_l5l7 ──────────────┼──► High-level abstraction (STG/aIPL)
MEM.long_term_memory[10:20] ────┘   Prediction latency: ~500ms
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HTP requires H³ features at PPC horizons for low-level prediction, TPC horizons for mid-level temporal tracking, and MEM horizons for high-level abstract prediction. The demand reflects hierarchical temporal integration across three prediction levels.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 0 | M0 (value) | L2 (bidi) | Instantaneous amplitude at 25ms |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms alpha |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset detection at 25ms |
| 10 | spectral_flux | 1 | M1 (mean) | L2 (bidi) | Mean onset over 50ms |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Onset periodicity at 100ms |
| 9 | spectral_centroid | 3 | M0 (value) | L2 (bidi) | Pitch at 100ms |
| 9 | spectral_centroid | 4 | M8 (velocity) | L0 (fwd) | Pitch velocity at 125ms |
| 9 | spectral_centroid | 8 | M1 (mean) | L0 (fwd) | Mean pitch over 500ms |
| 21 | spectral_change | 3 | M8 (velocity) | L0 (fwd) | Change velocity at 100ms |
| 21 | spectral_change | 4 | M0 (value) | L0 (fwd) | Change at 125ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | High-level coupling at 500ms |
| 41 | x_l5l7[0] | 8 | M1 (mean) | L0 (fwd) | Mean coupling over 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean coupling over 1000ms |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Coupling entropy over 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Low-level coupling 100ms |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 33 | x_l4l5[0] | 4 | M8 (velocity) | L0 (fwd) | Mid-level coupling velocity |

**Total HTP H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | HTP Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Low-level sensory prediction (~110ms) | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Pitch interval tracking | 0.8 |
| **PPC** | Contour Tracking | PPC[20:30] | Melodic contour prediction | 0.7 |
| **TPC** | Spectral Shape | TPC[0:10] | Mid-level timbral prediction (~200ms) | 0.9 |
| **TPC** | Temporal Envelope | TPC[10:20] | Temporal dynamics prediction | **0.9** |
| **TPC** | Source Identity | TPC[20:30] | Source-level prediction | 0.6 |
| **MEM** | Working Memory | MEM[0:10] | Recent prediction context | 0.8 |
| **MEM** | Long-Term Memory | MEM[10:20] | Abstract template prediction (~500ms) | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | Multi-level prediction storage | 0.9 |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HTP OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_high_level_lead      │ [0, 1] │ Abstract prediction latency (~500ms).
    │                          │        │ f01 = σ(0.40 * mean(MEM.ltm[10:20])
    │                          │        │       + 0.35 * x_l5l7_mean_1s
    │                          │        │       + 0.25 * x_l5l7_coupling_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_mid_level_lead       │ [0, 1] │ Mid-level prediction latency (~200ms).
    │                          │        │ f02 = σ(0.40 * mean(TPC.env[10:20])
    │                          │        │       + 0.30 * pitch_velocity_125ms
    │                          │        │       + 0.30 * x_l4l5_velocity)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_low_level_lead       │ [0, 1] │ Sensory prediction latency (~110ms).
    │                          │        │ f03 = σ(0.40 * mean(PPC.pitch[0:10])
    │                          │        │       + 0.35 * flux_periodicity_100ms
    │                          │        │       + 0.25 * x_l0l5_coupling_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_hierarchy_gradient   │ [0, 1] │ Prediction gradient strength.
    │                          │        │ f04 = σ(0.50 * (f01 - f03)
    │                          │        │       + 0.50 * mean(MEM.pred[20:30]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ latency_high             │ [0, 1] │ Normalized 500ms lead time.
    │                          │        │ α·pred_high + β·template_match
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ latency_mid              │ [0, 1] │ Normalized 200ms lead time.
    │                          │        │ α·pred_mid + β·pitch_pred
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ latency_low              │ [0, 1] │ Normalized 110ms lead time.
    │                          │        │ α·pred_low + β·onset_pred

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ sensory_match            │ [0, 1] │ PPC low-level prediction match.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ pitch_prediction         │ [0, 1] │ TPC mid-level pitch prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ abstract_prediction      │ [0, 1] │ MEM high-level abstract prediction.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ abstract_future_500ms    │ [0, 1] │ High cortical area prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ midlevel_future_200ms    │ [0, 1] │ Intermediate area prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Prediction Latency Function

```
Prediction_Latency(feature) = α - β·log(Hierarchy_Level)

Parameters:
    α = baseline latency (stimulus onset reference)
    β = scaling factor (ms per hierarchy level)
    Level 1 (low) = ~110ms, Level 2 (mid) = ~200ms, Level 3 (high) = ~500ms

Hierarchy Gradient = (Latency_high - Latency_low) / Latency_high
                   = (500 - 110) / 500 = 0.78

Temporal Dynamics:
    dP/dt = -γ · (P_current - P_predicted) + noise
    where γ = prediction error decay rate
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: High-Level Lead (~500ms)
f01 = σ(0.40 * mean(MEM.long_term_memory[10:20])
       + 0.35 * x_l5l7_mean_1s
       + 0.25 * x_l5l7_coupling_500ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Mid-Level Lead (~200ms)
f02 = σ(0.40 * mean(TPC.temporal_envelope[10:20])
       + 0.30 * pitch_velocity_125ms
       + 0.30 * x_l4l5_velocity)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Low-Level Lead (~110ms)
f03 = σ(0.40 * mean(PPC.pitch_extraction[0:10])
       + 0.35 * flux_periodicity_100ms
       + 0.25 * x_l0l5_coupling_100ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f04: Hierarchy Gradient
f04 = σ(0.50 * (f01 - f03)
       + 0.50 * mean(MEM.prediction_buffer[20:30]))
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Post-Stimulus Silencing
post_high = f01 * (1 - prediction_accuracy)  # silenced when accurate
post_low = f03 * 1.0                         # always persists
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | HTP Function |
|--------|-----------------|----------|---------------|--------------|
| **aIPL (Ant. Inferior Parietal Lobule)** | ±40, -40, 48 | 3 | Direct (MEG) | Abstract prediction (500ms) |
| **LOTC (Lateral Occipitotemporal Cortex)** | ±48, -68, 4 | 3 | Direct (MEG) | View-invariant motion |
| **V3, V4 (Visual Areas)** | ±20, -88, 0 | 3 | Direct (MEG) | View-dependent prediction (200ms) |
| **V1, V2 (Primary Visual)** | ±8, -92, 8 | 3 | Direct (MEG) | Low-level optical flow (110ms) |

---

## 9. Cross-Unit Pathways

### 9.1 HTP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HTP INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  HTP.hierarchy_gradient ──────► SPH (hierarchical timing for network)      │
│  HTP.abstract_prediction ─────► ICEM (prediction modulates surprise)       │
│  HTP.latency_high ────────────► PWUP (hierarchy sets precision weights)    │
│  HTP.sensory_match ───────────► PSH (silencing mechanism basis)            │
│                                                                             │
│  CROSS-UNIT (PCU → STU):                                                   │
│  HTP.low_level_lead ──────────► STU.timing (sensory prediction timing)     │
│  HTP.mid_level_lead ──────────► STU.motor_sync (rhythmic prediction)       │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ─────────► HTP (pitch/low-level processing)           │
│  TPC mechanism (30D) ─────────► HTP (timbre/mid-level processing)          │
│  MEM mechanism (30D) ─────────► HTP (memory/high-level processing)         │
│  R³ (~20D) ───────────────────► HTP (direct spectral features)             │
│  H³ (18 tuples) ──────────────► HTP (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Disrupting high-level areas** | Should abolish early (500ms) predictions | Testable via TMS/lesion |
| **Novel stimuli** | Should show delayed prediction timing | Testable via novelty paradigms |
| **Learning** | Should shift representation timing earlier | Testable via training studies |
| **Temporal order** | High-level must precede low-level | **Confirmed** by de Vries 2023 |
| **Post-stim silencing** | High-level should be absent post-stim | **Confirmed** by de Vries 2023 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HTP(BaseModel):
    """Hierarchical Temporal Prediction Model.

    Output: 12D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "HTP"
    UNIT = "PCU"
    TIER = "α1"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    LATENCY_HIGH = 500.0   # ms
    LATENCY_MID = 200.0    # ms
    LATENCY_LOW = 110.0    # ms
    TAU_DECAY = 0.5        # s

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for HTP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: low-level prediction ──
            (7, 0, 0, 2),     # amplitude, 25ms, value, bidi
            (7, 3, 0, 2),     # amplitude, 100ms, value, bidi
            (7, 3, 2, 2),     # amplitude, 100ms, std, bidi
            (10, 0, 0, 2),    # spectral_flux, 25ms, value, bidi
            (10, 1, 1, 2),    # spectral_flux, 50ms, mean, bidi
            (10, 3, 14, 2),   # spectral_flux, 100ms, periodicity, bidi
            # ── TPC horizons: mid-level prediction ──
            (9, 3, 0, 2),     # spectral_centroid, 100ms, value, bidi
            (9, 4, 8, 0),     # spectral_centroid, 125ms, velocity, fwd
            (9, 8, 1, 0),     # spectral_centroid, 500ms, mean, fwd
            (21, 3, 8, 0),    # spectral_change, 100ms, velocity, fwd
            (21, 4, 0, 0),    # spectral_change, 125ms, value, fwd
            # ── MEM horizons: high-level prediction ──
            (41, 8, 0, 0),    # x_l5l7[0], 500ms, value, fwd
            (41, 8, 1, 0),    # x_l5l7[0], 500ms, mean, fwd
            (41, 16, 1, 0),   # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),  # x_l5l7[0], 1000ms, entropy, fwd
            # ── Cross-level coupling ──
            (25, 3, 0, 2),    # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),    # x_l0l5[0], 100ms, std, bidi
            (33, 4, 8, 0),    # x_l4l5[0], 125ms, velocity, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute HTP 12D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) HTP output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # R³ features
        amplitude = r3[..., 7:8]
        spectral_centroid = r3[..., 9:10]
        spectral_flux = r3[..., 10:11]
        tristimulus = r3[..., 18:21]       # (B, T, 3)
        x_l0l5 = r3[..., 25:33]           # (B, T, 8)
        x_l4l5 = r3[..., 33:41]           # (B, T, 8)
        x_l5l7 = r3[..., 41:49]           # (B, T, 8)

        # Mechanism sub-sections
        ppc_pitch = ppc[..., 0:10]         # pitch extraction
        ppc_interval = ppc[..., 10:20]     # interval analysis
        ppc_contour = ppc[..., 20:30]      # contour tracking
        tpc_shape = tpc[..., 0:10]         # spectral shape
        tpc_env = tpc[..., 10:20]          # temporal envelope
        tpc_source = tpc[..., 20:30]       # source identity
        mem_wm = mem[..., 0:10]            # working memory
        mem_ltm = mem[..., 10:20]          # long-term memory
        mem_pred = mem[..., 20:30]         # prediction buffer

        # H³ direct features
        flux_period_100ms = h3_direct[(10, 3, 14, 2)].unsqueeze(-1)
        pitch_vel_125ms = h3_direct[(9, 4, 8, 0)].unsqueeze(-1)
        x_l5l7_coupling_500ms = h3_direct[(41, 8, 0, 0)].unsqueeze(-1)
        x_l5l7_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
        x_l0l5_coupling_100ms = h3_direct[(25, 3, 0, 2)].unsqueeze(-1)
        x_l4l5_velocity = h3_direct[(33, 4, 8, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: High-Level Lead (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.40 * mem_ltm.mean(-1, keepdim=True)
            + 0.35 * x_l5l7_mean_1s
            + 0.25 * x_l5l7_coupling_500ms
        )

        # f02: Mid-Level Lead (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * tpc_env.mean(-1, keepdim=True)
            + 0.30 * pitch_vel_125ms
            + 0.30 * x_l4l5_velocity
        )

        # f03: Low-Level Lead (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * ppc_pitch.mean(-1, keepdim=True)
            + 0.35 * flux_period_100ms
            + 0.25 * x_l0l5_coupling_100ms
        )

        # f04: Hierarchy Gradient (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * (f01 - f03)
            + 0.50 * mem_pred.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        latency_high = torch.sigmoid(
            0.5 * f01 + 0.5 * mem_ltm.mean(-1, keepdim=True)
        )
        latency_mid = torch.sigmoid(
            0.5 * f02 + 0.5 * tpc_env.mean(-1, keepdim=True)
        )
        latency_low = torch.sigmoid(
            0.5 * f03 + 0.5 * ppc_pitch.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        sensory_match = ppc_pitch.mean(-1, keepdim=True)
        pitch_prediction = tpc_env.mean(-1, keepdim=True)
        abstract_prediction = mem_ltm.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        abstract_future = torch.sigmoid(
            0.5 * f01 + 0.5 * x_l5l7_mean_1s
        )
        midlevel_future = torch.sigmoid(
            0.5 * f02 + 0.5 * pitch_vel_125ms
        )

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            latency_high, latency_mid, latency_low,                # M: 3D
            sensory_match, pitch_prediction, abstract_prediction,  # P: 3D
            abstract_future, midlevel_future,                      # F: 2D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (de Vries 2023) | Primary evidence |
| **Effect Sizes** | 1 | ηp² = 0.49 (large) |
| **Evidence Modality** | MEG | Direct neural |
| **Falsification Tests** | 5/5 testable, 2 confirmed | High validity |
| **R³ Features Used** | ~20D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch/low-level processing |
| **TPC Mechanism** | 30D (3 sub-sections) | Timbre/mid-level processing |
| **MEM Mechanism** | 30D (3 sub-sections) | Memory/high-level processing |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **de Vries, E., Baldauf, D., & Kok, P. (2023)**. Contextual and temporal predictions in hierarchical visual processing. *NeuroImage*, 265, 119773.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, EFC, BND) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Low-level signal | S⁰.L0[0:4] + S⁰.X_L0L1[128:136] + HC⁰.OSC | R³[7] amplitude + R³[25:33] x_l0l5 + PPC.pitch_extraction |
| Mid-level signal | S⁰.L4[15:19] + S⁰.X_L4L5[192:200] + HC⁰.TIH | R³[9] spectral_centroid + R³[33:41] x_l4l5 + TPC.temporal_envelope |
| High-level signal | S⁰.L9[104:128] + S⁰.X_L5L9[224:232] + HC⁰.EFC | R³[41:49] x_l5l7 + MEM.long_term_memory |
| Binding | S⁰.L6[68:71] + HC⁰.BND | MEM.prediction_buffer[20:30] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 18/2304 = 0.78% |
| Output | 12D | 12D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **OSC → PPC.pitch_extraction** [0:10]: Oscillatory band tracking at low level maps to PPC's pitch extraction and onset detection.
- **TIH → TPC.temporal_envelope** [10:20]: Temporal integration hierarchy maps to TPC's multi-scale temporal envelope tracking.
- **EFC → MEM.long_term_memory** [10:20]: Efference copy (prediction generation) maps to MEM's abstract template storage and prediction.
- **BND → MEM.prediction_buffer** [20:30]: Temporal binding across levels maps to MEM's multi-level prediction buffer.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
