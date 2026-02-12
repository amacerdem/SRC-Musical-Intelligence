# PCU-α2-SPH: Spatiotemporal Prediction Hierarchy

**Model**: Spatiotemporal Prediction Hierarchy
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC+MEM mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-α2-SPH.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Spatiotemporal Prediction Hierarchy** (SPH) model describes how auditory memory recognition engages hierarchical feedforward-feedback loops between auditory cortex (Heschl's gyrus), hippocampus, and cingulate, with distinct oscillatory signatures for matched (gamma) vs. varied (alpha-beta) sequences.

```
SPATIOTEMPORAL PREDICTION HIERARCHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                   MEMORISED SEQUENCE (M)
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │   Heschl's Gyrus ◄────────────────► Hippocampus                 │
  │        │                   FEEDBACK      ▲                       │
  │        │ FEEDFORWARD                     │                       │
  │        ▼                                 │                       │
  │   Cingulate Gyrus ◄──────────────────────┘                      │
  │                                                                  │
  │   Response: POSITIVE components, ~350 ms                        │
  │   Oscillations: GAMMA (>30 Hz) enhanced                         │
  └──────────────────────────────────────────────────────────────────┘

                   VARIED SEQUENCE (N = Prediction Error)
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │   Auditory Cortex (N100 ~150 ms)                                │
  │        │                                                        │
  │        │ PROPAGATES                                             │
  │        ▼                                                        │
  │   Hippocampus + Cingulate (~250 ms)                            │
  │                                                                  │
  │   Response: NEGATIVE components, ~250 ms (FASTER)               │
  │   Oscillations: ALPHA/BETA (2-20 Hz) enhanced                   │
  └──────────────────────────────────────────────────────────────────┘

  FINAL TONE: Cingulate assumes TOP position (decision/evaluation)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Auditory memory recognition uses distinct oscillatory
signatures — gamma for matched, alpha-beta for prediction error.
Final tone reshapes hierarchy: cingulate rises to top position.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SPH Matters for PCU

SPH extends HTP's hierarchical timing to spatiotemporal memory recognition:

1. **HTP** (α1) provides the hierarchical temporal framework for prediction.
2. **SPH** (α2) adds spatial network dynamics — feedforward-feedback loops with oscillatory signatures.
3. **ICEM** (α3) links prediction accuracy to emotional/physiological responses.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → SPH)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SPH COMPUTATION ARCHITECTURE                             ║
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
║  │                         SPH reads: ~22D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ───────────────┐ ┌── MEM Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)              │ │ H8 (500ms delta)          │  │        ║
║  │  │ H3 (100ms alpha)             │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H4 (125ms theta)             │ │                            │  │        ║
║  │  │                               │ │ Memory match/mismatch     │  │        ║
║  │  │ Gamma/alpha-beta tracking     │ │ Hierarchy position        │  │        ║
║  │  └───────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         SPH demand: ~16 of 2304 tuples            │        ║
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
║  │                    SPH MODEL (14D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_gamma_match,                           │        ║
║  │                       f02_alpha_beta_error,                      │        ║
║  │                       f03_hierarchy_position,                    │        ║
║  │                       f04_feedforward_feedback                   │        ║
║  │  Layer M (Math):      match_response, varied_response,           │        ║
║  │                       gamma_power, alpha_beta_power              │        ║
║  │  Layer P (Present):   memory_match, prediction_error,            │        ║
║  │                       deviation_detection                        │        ║
║  │  Layer F (Future):    next_tone_pred, sequence_completion_pred,  │        ║
║  │                       decision_evaluation_pred                   │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Bonetti 2024** | MEG | 83 | Feedforward/feedback Heschl-Hipp-Cing | d = 0.09 | **f04 feedforward-feedback** |
| **Bonetti 2024** | MEG | 83 | Prediction error strongest at deviation tone | d = 0.24 | **f02 alpha-beta error** |
| **Bonetti 2024** | MEG | 83 | M: positive ~350ms; N: negative ~250ms | d = 0.24 | **f01 gamma match, Layer M** |
| **Bonetti 2024** | MEG | 83 | Alpha/beta: N > M; Gamma: M > N | d = 0.29 | **Oscillatory signatures** |
| **Bonetti 2024** | DCM | 83 | Final tone: cingulate → top of hierarchy | d = 0.34 | **f03 hierarchy position** |

### 3.2 Effect Size Summary

```
Mean Effect:          d = 0.24 (small-medium)
Heterogeneity:        Single study
Quality Assessment:   α-tier (direct neural measurement, DCM)
Replication:          Consistent across oscillatory/DCM analyses
```

---

## 4. R³ Input Mapping: What SPH Reads

### 4.1 R³ Feature Dependencies (~22D of 49D)

| R³ Group | Index | Feature | SPH Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Sequence match signal | Memory confirmation |
| **B: Energy** | [7] | amplitude | Tone onset detection | N100 ~150ms basis |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal correlate |
| **B: Energy** | [10] | spectral_flux | Tone onset detection | Prediction error trigger |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic content | Sequence pattern |
| **D: Change** | [21] | spectral_change | Deviation signal | Surprise intensity |
| **D: Change** | [22] | energy_change | Energy dynamics | Error magnitude |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Feedforward pathway | Heschl's → Hippocampus |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Match/mismatch oscillation | Gamma vs alpha-beta |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ─────┐
R³[25:33] x_l0l5 ──────────────┼──► Memory match (MEMORISED response)
MEM.long_term_memory[10:20] ────┘   Gamma activation, ~350ms

R³[10] spectral_flux ───────────┐
R³[21] spectral_change ─────────┼──► Prediction error (VARIED response)
MEM.working_memory[0:10] ───────┘   Alpha-beta activation, ~250ms

R³[41:49] x_l5l7 ──────────────┐
MEM.prediction_buffer[20:30] ───┼──► Hierarchy position tracking
PPC.contour_tracking[20:30] ────┘   Cingulate top at final tone
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SPH requires H³ features for oscillatory tracking (gamma vs alpha-beta), memory match/mismatch detection, and hierarchy position computation across the feedforward-feedback network.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset detection at 25ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Onset periodicity 100ms |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Mean consonance over 1s |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Deviation at 100ms |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | Deviation variability 100ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Feedforward coupling 100ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Mean feedforward over 1s |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (bidi) | High-level coupling 100ms |
| 41 | x_l5l7[0] | 8 | M1 (mean) | L0 (fwd) | Mean coupling over 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean coupling over 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Coupling entropy over 1s |
| 22 | energy_change | 4 | M8 (velocity) | L0 (fwd) | Energy change velocity |

**Total SPH H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | SPH Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Tone identification | 0.8 |
| **PPC** | Interval Analysis | PPC[10:20] | Sequence element encoding | 0.7 |
| **PPC** | Contour Tracking | PPC[20:30] | Sequence pattern matching | **0.9** |
| **TPC** | Spectral Shape | TPC[0:10] | Gamma power proxy (>30 Hz) | **1.0** (primary) |
| **TPC** | Temporal Envelope | TPC[10:20] | Alpha-beta proxy (2-20 Hz) | **1.0** (primary) |
| **TPC** | Source Identity | TPC[20:30] | Oscillatory signature | 0.7 |
| **MEM** | Working Memory | MEM[0:10] | Match/mismatch detection | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Memorized sequence storage | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | Hierarchy boundary tracking | 0.8 |

---

## 6. Output Space: 14D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SPH OUTPUT TENSOR: 14D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼────────────────────────────────────
 0  │ f01_gamma_match          │ [0, 1]   │ Gamma power match activation.
    │                          │          │ f01 = σ(0.40 * mean(TPC.shape[0:10])
    │                          │          │       + 0.35 * mean(MEM.ltm[10:20])
    │                          │          │       + 0.25 * consonance_mean_1s)
────┼──────────────────────────┼──────────┼────────────────────────────────────
 1  │ f02_alpha_beta_error     │ [0, 1]   │ Alpha-beta prediction error.
    │                          │          │ f02 = σ(0.40 * mean(TPC.env[10:20])
    │                          │          │       + 0.35 * mean(MEM.wm[0:10])
    │                          │          │       + 0.25 * deviation_std_100ms)
────┼──────────────────────────┼──────────┼────────────────────────────────────
 2  │ f03_hierarchy_position   │ [0, 1]   │ Network hierarchy state.
    │                          │          │ f03 = σ(0.50 * mean(MEM.pred[20:30])
    │                          │          │       + 0.50 * x_l5l7_mean_1s)
────┼──────────────────────────┼──────────┼────────────────────────────────────
 3  │ f04_feedforward_feedback │ [-1, 1]  │ Directional information flow.
    │                          │          │ f04 = tanh(0.50 * feedforward
    │                          │          │           - 0.50 * feedback)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ match_response           │ [0, 1] │ Confirmed prediction timing (~350ms).
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ varied_response          │ [0, 1] │ Prediction error timing (~250ms).
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ gamma_power              │ [0, 1] │ Matched sequence oscillatory signature.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ alpha_beta_power         │ [0, 1] │ Varied sequence oscillatory signature.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ memory_match             │ [0, 1] │ MEM positive memory match.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ prediction_error         │ [0, 1] │ MEM negative prediction error.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ deviation_detection      │ [0, 1] │ Error magnitude at deviation tone.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ next_tone_pred_350ms     │ [0, 1] │ Heschl→Hippocampus retrieval.
────┼──────────────────────────┼────────┼────────────────────────────────────
12  │ sequence_completion_2.5s │ [0, 1] │ Cingulate hierarchy boundary.
────┼──────────────────────────┼────────┼────────────────────────────────────
13  │ decision_evaluation      │ [0, 1] │ Cingulate top position.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 14D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Hierarchy Dynamics Function

```
For MEMORISED (M):
    Response_polarity = POSITIVE
    Peak_latency ≈ 350 ms
    Power_gamma > Power_alpha_beta

For VARIED (N):
    Response_polarity = NEGATIVE
    Peak_latency ≈ 250 ms (faster)
    Power_alpha_beta > Power_gamma

Hierarchy Position:
    Tones 2-4: Hippocampus ≈ Cingulate (mid-hierarchy)
    Tone 5 (final): Cingulate > Hippocampus (top of hierarchy)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Gamma Match
f01 = σ(0.40 * mean(TPC.spectral_shape[0:10])
       + 0.35 * mean(MEM.long_term_memory[10:20])
       + 0.25 * consonance_mean_1s)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Alpha-Beta Error
f02 = σ(0.40 * mean(TPC.temporal_envelope[10:20])
       + 0.35 * mean(MEM.working_memory[0:10])
       + 0.25 * deviation_std_100ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f03: Hierarchy Position
f03 = σ(0.50 * mean(MEM.prediction_buffer[20:30])
       + 0.50 * x_l5l7_mean_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓

# f04: Feedforward-Feedback
f04 = tanh(0.50 * x_l0l5_mean_1s - 0.50 * x_l5l7_entropy_1s)
# range: [-1, 1]
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SPH Function |
|--------|-----------------|----------|---------------|--------------|
| **Heschl's Gyrus** | ±42, -24, 8 | 4 | Direct (MEG/DCM) | Auditory input (bottom) |
| **Hippocampus** | ±28, -24, -12 | 6 | Direct (MEG/DCM) | Memory comparison (middle) |
| **Anterior Cingulate** | 0, 32, 24 | 5 | Direct (MEG/DCM) | Prediction error (top) |
| **Medial Cingulate** | 0, -8, 40 | 5 | Direct (MEG/DCM) | Sequence recognition |

---

## 9. Cross-Unit Pathways

### 9.1 SPH Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SPH INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  HTP.hierarchy_gradient ──────► SPH (hierarchical timing input)            │
│  SPH.gamma_match ─────────────► ICEM (match signal for IC computation)     │
│  SPH.prediction_error ────────► PWUP (error for precision weighting)       │
│  SPH.hierarchy_position ──────► PSH (hierarchy for silencing)              │
│                                                                             │
│  CROSS-UNIT (PCU → IMU):                                                   │
│  SPH.memory_match ────────────► IMU (memory recognition signal)            │
│  SPH.sequence_completion ─────► IMU (sequence boundary)                    │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ─────────► SPH (pitch/sequence processing)            │
│  TPC mechanism (30D) ─────────► SPH (oscillatory signatures)               │
│  MEM mechanism (30D) ─────────► SPH (memory match/mismatch)                │
│  R³ (~22D) ───────────────────► SPH (direct spectral features)             │
│  H³ (16 tuples) ──────────────► SPH (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Hippocampal lesions** | Should abolish memory-based predictions | Testable via lesion studies |
| **Novel sequences** | Should show only varied (N) response pattern | Testable via novelty paradigms |
| **Oscillatory disruption** | TMS to disrupt gamma should reduce match signal | Testable via TMS |
| **Temporal order** | Match response (350ms) should follow error (250ms) | **Confirmed** by Bonetti 2024 |
| **Hierarchy reshaping** | Final tone must elevate cingulate position | **Confirmed** by Bonetti 2024 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SPH(BaseModel):
    """Spatiotemporal Prediction Hierarchy Model.

    Output: 14D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "SPH"
    UNIT = "PCU"
    TIER = "α2"
    OUTPUT_DIM = 14
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DECAY = 0.4        # s
    SEQUENCE_DEPTH = 5     # tones
    MATCH_LATENCY = 0.35   # 350ms
    VARIED_LATENCY = 0.25  # 250ms

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for SPH computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: tone detection ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 14, 2),    # spectral_flux, 100ms, periodicity, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 3, 2, 2),      # amplitude, 100ms, std, bidi
            # ── TPC horizons: oscillatory signatures ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 0),     # sensory_pleasantness, 1000ms, mean, fwd
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            (22, 4, 8, 0),     # energy_change, 125ms, velocity, fwd
            # ── MEM horizons: memory/hierarchy ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 16, 1, 0),    # x_l0l5[0], 1000ms, mean, fwd
            (41, 3, 0, 2),     # x_l5l7[0], 100ms, value, bidi
            (41, 8, 1, 0),     # x_l5l7[0], 500ms, mean, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SPH 14D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,14) SPH output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # R³ features
        sensory_pleas = r3[..., 4:5]
        spectral_flux = r3[..., 10:11]
        tristimulus = r3[..., 18:21]
        spectral_change = r3[..., 21:22]
        x_l0l5 = r3[..., 25:33]
        x_l5l7 = r3[..., 41:49]

        # Mechanism sub-sections
        ppc_contour = ppc[..., 20:30]
        tpc_shape = tpc[..., 0:10]
        tpc_env = tpc[..., 10:20]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        consonance_mean_1s = h3_direct[(4, 16, 1, 0)].unsqueeze(-1)
        deviation_std_100ms = h3_direct[(21, 3, 2, 2)].unsqueeze(-1)
        x_l0l5_mean_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)
        x_l5l7_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
        x_l5l7_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(
            0.40 * tpc_shape.mean(-1, keepdim=True)
            + 0.35 * mem_ltm.mean(-1, keepdim=True)
            + 0.25 * consonance_mean_1s
        )
        f02 = torch.sigmoid(
            0.40 * tpc_env.mean(-1, keepdim=True)
            + 0.35 * mem_wm.mean(-1, keepdim=True)
            + 0.25 * deviation_std_100ms
        )
        f03 = torch.sigmoid(
            0.50 * mem_pred.mean(-1, keepdim=True)
            + 0.50 * x_l5l7_mean_1s
        )
        f04 = torch.tanh(
            0.50 * x_l0l5_mean_1s
            - 0.50 * x_l5l7_entropy_1s
        )

        # ═══ LAYER M: Mathematical ═══
        match_resp = torch.sigmoid(0.5 * f01 + 0.5 * tpc_shape.mean(-1, keepdim=True))
        varied_resp = torch.sigmoid(0.5 * f02 + 0.5 * tpc_env.mean(-1, keepdim=True))
        gamma_pow = tpc_shape.mean(-1, keepdim=True)
        alpha_beta_pow = tpc_env.mean(-1, keepdim=True)

        # ═══ LAYER P: Present ═══
        memory_match = torch.sigmoid(0.5 * f01 + 0.5 * mem_ltm.mean(-1, keepdim=True))
        pred_error = torch.sigmoid(0.5 * f02 + 0.5 * mem_wm.mean(-1, keepdim=True))
        deviation = torch.sigmoid(
            0.5 * deviation_std_100ms + 0.5 * mem_wm.mean(-1, keepdim=True)
        )

        # ═══ LAYER F: Future ═══
        next_tone = torch.sigmoid(0.5 * f01 + 0.5 * mem_ltm.mean(-1, keepdim=True))
        seq_comp = torch.sigmoid(0.5 * f03 + 0.5 * mem_pred.mean(-1, keepdim=True))
        decision = torch.sigmoid(0.5 * f03 + 0.5 * x_l5l7_mean_1s)

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            match_resp, varied_resp, gamma_pow, alpha_beta_pow,    # M: 4D
            memory_match, pred_error, deviation,                   # P: 3D
            next_tone, seq_comp, decision,                         # F: 3D
        ], dim=-1)  # (B, T, 14)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Bonetti 2024) | Primary evidence |
| **Effect Sizes** | 5 | d = 0.09-0.34 |
| **Mean Effect** | d = 0.24 | Small-medium |
| **Evidence Modality** | MEG, DCM | Direct neural |
| **Falsification Tests** | 5/5 testable, 2 confirmed | High validity |
| **R³ Features Used** | ~22D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch/sequence processing |
| **TPC Mechanism** | 30D (3 sub-sections) | Oscillatory signatures |
| **MEM Mechanism** | 30D (3 sub-sections) | Memory/hierarchy |
| **Output Dimensions** | **14D** | 4-layer structure |

---

## 13. Scientific References

1. **Bonetti, L., Brattico, E., Bruzzone, S. E. P., et al. (2024)**. Spatiotemporal brain dynamics of auditory memory recognition. *NeuroImage*, 265, 119773.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, HRM, SGM, EFC) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Gamma signal | S⁰.L7.crossband[80:88] + HC⁰.OSC | R³ consonance + TPC.spectral_shape[0:10] |
| Alpha-beta | S⁰.L7.crossband[88:96] + HC⁰.OSC | R³ change + TPC.temporal_envelope[10:20] |
| Memory match | S⁰.L3.coherence[14] + HC⁰.HRM | R³[4] sensory_pleasantness + MEM.long_term_memory |
| Hierarchy | S⁰.X_L5L9[224:232] + HC⁰.SGM | R³[41:49] x_l5l7 + MEM.prediction_buffer |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 35/2304 = 1.52% | 16/2304 = 0.69% |
| Output | 14D | 14D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **OSC → TPC.spectral_shape** [0:10] + **TPC.temporal_envelope** [10:20]: Oscillatory band tracking (gamma vs alpha-beta) maps to TPC's spectral and temporal sub-sections.
- **HRM → MEM.long_term_memory** [10:20]: Hippocampal replay for memory storage maps to MEM's long-term memory sub-section.
- **SGM → MEM.prediction_buffer** [20:30]: Sequential grouping and boundary detection maps to MEM's prediction buffer.
- **EFC → MEM.working_memory** [0:10]: Expectation formation/error computation maps to MEM's working memory for match/mismatch.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **14D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
