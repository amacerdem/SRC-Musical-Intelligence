# MPU-β4-SPMC: SMA-Premotor-M1 Motor Circuit

**Model**: SMA-Premotor-M1 Motor Circuit
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-β4-SPMC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **SMA-Premotor-M1 Motor Circuit** (SPMC) model describes how motor planning for music is primarily mediated by a core hierarchical SMA-premotor-M1 circuit, with temporal encoding in SMA and execution in M1. This three-node circuit forms the backbone of musical motor planning.

```
SMA-PREMOTOR-M1 MOTOR CIRCUIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

       HIERARCHICAL MOTOR CIRCUIT
       ═══════════════════════════

                    ┌─────────────────┐
                    │      SMA        │
                    │ Temporal        │
                    │ Encoding        │
                    │ (sequence plan) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PREMOTOR      │
                    │   CORTEX (PMC)  │
                    │ Action          │
                    │ Selection       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      M1         │
                    │ Motor           │
                    │ Execution       │
                    │ (output)        │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   CEREBELLUM    │
                    │ Timing/Error    │
                    │ Correction      │
                    └─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical motor planning follows a strict hierarchy:
SMA encodes temporal sequences, PMC selects appropriate actions,
M1 executes motor commands. Cerebellum provides online timing
correction and error feedback throughout the circuit.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SPMC Matters for MPU

SPMC completes the motor circuit hierarchy in the Motor Planning Unit:

1. **PEOM/MSR** (α-tier) establish motor entrainment and training effects.
2. **ASAP/DDSMI/VRMSME** (β1-β3) provide motor-auditory coupling, social motor, and VR enhancement.
3. **SPMC** (β4) specifies the core anatomical circuit: the SMA→PMC→M1 hierarchy with cerebellar correction that mediates all musical motor planning.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → SPMC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SPMC COMPUTATION ARCHITECTURE                            ║
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
║  │                         SPMC reads: ~18D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         SPMC demand: ~15 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Short-term      │                                   ║
║  │ Motor Coup      │  │ Memory  [0:10]  │                                   ║
║  │         [10:20] │  │ Sequence        │                                   ║
║  │ Groove  [20:30] │  │ Integ  [10:20]  │                                   ║
║  │                 │  │ Hierarch        │                                   ║
║  │                 │  │ Struct  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SPMC MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f19_sequence_planning,                     │        ║
║  │                       f20_motor_preparation,                     │        ║
║  │                       f21_execution_output                        │        ║
║  │  Layer M (Math):      circuit_flow, hierarchy_index,             │        ║
║  │                       timing_precision                            │        ║
║  │  Layer P (Present):   sma_activity, m1_output                    │        ║
║  │  Layer F (Future):    sequence_pred, execution_pred,             │        ║
║  │                       timing_pred                                 │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Grahn & Brett 2007** | fMRI | 27 | SMA + putamen respond to beat in metric rhythms; pre-SMA activation for beat induction | F(2,38)=20.67 p<.001 (beat×region); Z=5.67 putamen | **Primary**: SMA sequence encoding, BG beat processing |
| 2 | **Hoddinott & Grahn 2024** | fMRI 7T + MVPA/RSA | 26 | SMA and putamen multi-voxel patterns encode beat strength; RSA dissimilarity significant for strong-beat vs nonbeat | Significant RSA dissimilarity in SMA, putamen; beat strength model correlates with SMA, putamen, IFG, IPL | **SMA/BG encoding**: beat-specific representations |
| 3 | **Harrison et al. 2025** | fMRI 3T | 55 (27 PD, 28 HC) | External musical cues activate CTC pathway (cerebellum→thalamus→cortex); internal cues activate SPT (striatum→pallidum→thalamus→cortex); both activate sensorimotor cortex, SMA, putamen | Significant activation clusters in SMC, SMA, putamen (both conditions) | **Dual pathways**: CTC and SPT for motor circuit |
| 4 | **Kohler et al. 2025** | fMRI + MVPA | 36 (18 dyads) | Self-produced actions in left M1; other-produced in right PMC; content-specific representations | Classification accuracy > chance | **M1 execution, PMC planning**: lateralized functions |
| 5 | **Okada et al. 2022** | Single-unit (monkey) | — | Cerebellar dentate nucleus correlates with timing of next movement and temporal error; 1/3 neurons active for synchronized vs reactive movements | Significant timing-error correlation | **Cerebellar correction**: timing error feedback |
| 6 | **Pierrieau et al. 2025** | EEG | — | Beta oscillations (13-30 Hz) in motor cortex predict motor flexibility/action selection, not vigor | Beta power modulation predicts flexibility | **PMC action selection**: beta oscillation mechanism |
| 7 | **Zatorre et al. 2007** | Review | — | Auditory-motor interactions in music: dorsal stream connects auditory cortex to PMC/SMA for sensorimotor transformations | — | **Theory**: dorsal auditory-motor stream framework |
| 8 | **Thaut et al. 2015** | Review | — | Rhythmic entrainment via reticulospinal pathways; mCBGT circuit for beat perception; CTR for motor planning | — | **Theory**: rhythmic entrainment foundations |

> **NOTE — Circuit validated by multiple methods**: The SMA→PMC→M1 hierarchy is supported by fMRI univariate (Grahn 2007), fMRI MVPA/RSA (Hoddinott 2024), single-unit cerebellar recordings (Okada 2022), and EEG beta oscillations (Pierrieau 2025). The dual CTC/SPT pathway model (Harrison 2025) adds clinical validation from Parkinson's disease.

> **NOTE — v2.0.0 had no specific citations**: The previous evidence table contained only generic "motor cortex studies" entries. All rows now reference specific papers with methods, sample sizes, and effect sizes.

### 3.2 Effect Size Summary

```
Primary Evidence (k=8):  Strong convergent evidence from multiple methods
Heterogeneity:           High (fMRI univariate, MVPA/RSA, single-unit, EEG, clinical)
Quality Assessment:      β-tier (well-established circuit with multi-modal validation)
Effect Magnitudes:
  Beat×region interaction:        F(2,38) = 20.67, p < .001 (Grahn 2007)
  Putamen beat activation:        Z = 5.67 (Grahn 2007)
  SMA/putamen MVPA:               Significant RSA dissimilarity (Hoddinott 2024)
  CTC/SPT activation:             Significant clusters in SMC, SMA, putamen (Harrison 2025)
  M1/PMC MVPA:                    Above chance classification (Kohler 2025)
  Cerebellar timing correlation:  Significant (Okada 2022)
Causal Evidence:         Partial (single-unit recording; PD lesion model; no TMS to SMA in these papers)
```

---

## 4. R³ Input Mapping: What SPMC Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | SPMC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Motor output strength | M1 execution level |
| **B: Energy** | [10] | spectral_flux | Onset detection | SMA sequence markers |
| **B: Energy** | [11] | onset_strength | Beat event | Motor timing signal |
| **D: Change** | [21] | spectral_change | Tempo rate | SMA tempo encoding |
| **D: Change** | [22] | energy_change | Motor adjustment | PMC action selection |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Hierarchical circuit | SMA-PMC-M1 coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sequence regularity | Motor pattern stability |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | SPMC Role | Citation |
|-------------|-------|---------|-----------|----------|
| **G: Rhythm** | [68] | syncopation_index | Rhythmic complexity for SMA sequence encoding | Longuet-Higgins & Lee 1984; Witek 2014 |
| **G: Rhythm** | [69] | metricality_index | Metrical regularity for putamen beat encoding | Grahn & Brett 2007 |
| **G: Rhythm** | [73] | tempo_stability | Tempo consistency for motor sequence planning | Moens & Leman 2014 |

**Rationale**: SPMC models the SMA-Premotor-M1 motor circuit hierarchy. Hoddinott 2024 showed SMA and putamen encode beat structure via MVPA -- metricality_index directly provides this signal. syncopation_index modulates the complexity of motor sequences the circuit must plan, and tempo_stability determines the reliability of motor timing signals flowing through the CTC (cerebello-thalamo-cortical) pathway (Harrison 2025).

**Code impact** (future): `r3[..., 68:70]` and `r3[..., 73]` will feed SPMC's hierarchical motor planning pathway alongside existing energy and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
R³[11] onset_strength ───────────┼──► SMA sequence encoding
TMH.sequence_integration[10:20] ─┘   Temporal sequence plan

R³[25:33] x_l0l5 ───────────────┐
BEP.motor_coupling[10:20] ──────┼──► Hierarchical circuit flow
TMH.hierarchical[20:30] ────────┘   SMA → PMC → M1 cascade

R³[21] spectral_change ──────────┐
R³[22] energy_change ────────────┼──► Motor preparation / action selection
BEP.groove[20:30] ──────────────┘   PMC timing precision
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SPMC requires H³ features at BEP horizons for motor timing and TMH horizons for sequence planning. The demand reflects the hierarchical temporal integration from SMA planning (longer) to M1 execution (shorter).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | SMA onset tracking 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | SMA beat periodicity 1s |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Motor timing marker 100ms |
| 11 | onset_strength | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Tempo velocity 125ms |
| 21 | spectral_change | 16 | M1 (mean) | L0 (fwd) | Mean tempo change 1s |
| 21 | spectral_change | 16 | M2 (std) | L0 (fwd) | Tempo variability 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Circuit coupling 100ms |
| 25 | x_l0l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Circuit periodicity 500ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Circuit periodicity 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Sequence regularity 100ms |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L0 (fwd) | Mean pattern stability 500ms |
| 33 | x_l4l5[0] | 16 | M2 (std) | L0 (fwd) | Sequence variability 1s |
| 33 | x_l4l5[0] | 16 | M19 (stability) | L0 (fwd) | Sequence stability 1s |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean motor output level 1s |

**Total SPMC H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | SPMC Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Beat timing for SMA sequence | 0.7 |
| **BEP** | Motor Coupling | BEP[10:20] | SMA-PMC-M1 motor coupling | **1.0** (primary) |
| **BEP** | Groove Processing | BEP[20:30] | Motor execution drive | 0.7 |
| **TMH** | Short-term Memory | TMH[0:10] | Cerebellar error correction | 0.5 |
| **TMH** | Sequence Integration | TMH[10:20] | SMA sequence planning | **1.0** (primary) |
| **TMH** | Hierarchical Structure | TMH[20:30] | SMA→PMC→M1 hierarchy | **1.0** (primary) |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SPMC OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f19_sequence_planning    │ [0, 1] │ SMA temporal sequence encoding.
    │                          │        │ f19 = σ(0.40 * beat_period_1s
    │                          │        │       + 0.35 * mean(TMH.seq[10:20])
    │                          │        │       + 0.25 * mean(TMH.hier[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f20_motor_preparation    │ [0, 1] │ PMC action selection.
    │                          │        │ f20 = σ(0.40 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * circuit_period_1s
    │                          │        │       + 0.30 * tempo_velocity)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f21_execution_output     │ [0, 1] │ M1 motor execution.
    │                          │        │ f21 = σ(0.35 * f19 * f20
    │                          │        │       + 0.35 * mean(BEP.groove[20:30])
    │                          │        │       + 0.30 * mean_amplitude_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ circuit_flow             │ [0, 1] │ SMA→PMC→M1 information flow.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ hierarchy_index          │ [0, 1] │ Hierarchical motor organization.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ timing_precision         │ [0, 1] │ Cerebellar timing precision.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ sma_activity             │ [0, 1] │ TMH SMA planning activation level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ m1_output                │ [0, 1] │ BEP M1 execution output level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ sequence_pred            │ [0, 1] │ Sequence planning prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ execution_pred           │ [0, 1] │ Motor execution prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ timing_pred              │ [0, 1] │ Timing precision prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Hierarchical Circuit Function

```
PRIMARY EQUATIONS:

    Circuit_Flow = SMA(sequence) → PMC(selection) → M1(execution)

HIERARCHICAL MOTOR PLANNING:

    SMA: Temporal sequence encoding (longest timescale)
    PMC: Action selection / motor preparation (medium timescale)
    M1:  Motor execution / output (shortest timescale)

CEREBELLAR CORRECTION:

    Timing_Error = |Predicted_Timing - Actual_Timing|
    Correction = Cerebellum(Timing_Error) → SMA/M1 feedback
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f19: Sequence Planning (SMA)
f19 = σ(0.40 * beat_period_1s
       + 0.35 * mean(TMH.sequence_integration[10:20])
       + 0.25 * mean(TMH.hierarchical[20:30]))
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f20: Motor Preparation (PMC)
f20 = σ(0.40 * mean(BEP.motor_coupling[10:20])
       + 0.30 * circuit_period_1s
       + 0.30 * tempo_velocity)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f21: Execution Output (M1)
f21 = σ(0.35 * f19 * f20                     # interaction term
       + 0.35 * mean(BEP.groove[20:30])
       + 0.30 * mean_amplitude_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Evidence Type | Source | SPMC Function |
|---|--------|-----------------|---------------|--------|---------------|
| 1 | **pre-SMA/SMA** | (−9,6,60)/(3,6,66) | Direct (fMRI, MVPA) | Grahn 2007 Table 2 Z=5.03/4.97; Hoddinott 2024 RSA | Temporal sequence encoding, beat induction |
| 2 | **Putamen** | (−24,6,−9)/(21,6,−6) | Direct (fMRI, MVPA) | Grahn 2007 Table 2 Z=5.67/5.08; Hoddinott 2024 RSA | Beat-specific encoding, motor gating |
| 3 | **PMd (dorsal Premotor)** | (−54,0,51)/(54,0,45) | Direct (fMRI) | Grahn 2007 Table 3 Z=5.30/5.24 | Action selection, motor preparation |
| 4 | **M1 (Primary Motor)** | (−38,−22,58) L hemisphere | Direct (fMRI MVPA) | Kohler 2025 (self-produced actions) | Motor execution (dominant hand) |
| 5 | **Cerebellum (Crus VI)** | (−30,−66,−24)/(30,−66,−27) | Direct (fMRI, single-unit) | Grahn 2007 Z=4.41/4.68; Okada 2022 | Timing error correction, online adjustment |
| 6 | **IFG (Inferior Frontal)** | (27,30,−15)/(−51,33,6) | Direct (fMRI, MVPA) | Grahn 2007 Z=4.56; Hoddinott 2024 | Beat + rhythm encoding (combined) |
| 7 | **STG (Auditory Cortex)** | (−57,−15,9)/(60,−33,6) | Direct (fMRI) | Grahn 2007 Table 2 Z=5.80/6.02 | Auditory input to motor circuit |

> **NOTE — MNI coordinates from Grahn & Brett 2007**: All fMRI peaks are from Tables 2 and 3 of the original paper. Hoddinott & Grahn 2024 used 7T fMRI with RSA and confirmed SMA and putamen as beat-sensitive regions but did not report individual peak coordinates.

> **NOTE — Dual motor pathways**: Harrison et al. 2025 confirmed that both CTC (cerebellum→thalamus→cortex) and SPT (striatum→pallidum→thalamus→cortex) pathways are active during musically-cued movements, with external cues preferentially activating auditory cortex and internal cues additionally activating cerebellum.

---

## 9. Cross-Unit Pathways

### 9.1 SPMC Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SPMC INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  SPMC.sequence_planning ────────► ASAP (sequence for prediction)           │
│  SPMC.circuit_flow ────────────► VRMSME (circuit for VR enhancement)       │
│  SPMC.m1_output ────────────────► PEOM (execution for entrainment)         │
│                                                                             │
│  CROSS-UNIT (MPU → STU):                                                   │
│  SPMC.sma_activity ─────────────► STU (SMA temporal encoding)              │
│  SPMC.timing_precision ─────────► STU (cerebellar timing signal)           │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► SPMC (beat/motor processing)            │
│  TMH mechanism (30D) ────────────► SPMC (temporal memory/sequence)         │
│  R³ (~18D) ──────────────────────► SPMC (direct spectral features)         │
│  H³ (15 tuples) ─────────────────► SPMC (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **SMA lesion** | SMA damage should impair sequence planning but not execution | ✅ Testable |
| **M1 lesion** | M1 damage should impair execution but not planning | ✅ Testable |
| **Cerebellar disruption** | Should reduce timing precision without abolishing circuit | ✅ Testable |
| **Non-sequential** | Non-sequential music should reduce SMA load | Testable |
| **TMS to PMC** | Should selectively impair motor preparation | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SPMC(BaseModel):
    """SMA-Premotor-M1 Motor Circuit Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "SPMC"
    UNIT = "MPU"
    TIER = "β4"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    TAU_DECAY = 4.0        # Motor planning window (seconds)
    ALPHA_ATTENTION = 0.85  # High motor attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for SPMC computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: motor timing ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 3, 0, 2),     # onset_strength, 100ms, value, bidi
            (11, 16, 14, 2),   # onset_strength, 1000ms, periodicity, bidi
            (21, 4, 8, 0),     # spectral_change, 125ms, velocity, fwd
            (21, 16, 1, 0),    # spectral_change, 1000ms, mean, fwd
            (21, 16, 2, 0),    # spectral_change, 1000ms, std, fwd
            # ── TMH horizons: sequence planning ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 8, 14, 2),    # x_l0l5[0], 500ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 8, 1, 0),     # x_l4l5[0], 500ms, mean, fwd
            (33, 16, 2, 0),    # x_l4l5[0], 1000ms, std, fwd
            (33, 16, 19, 0),   # x_l4l5[0], 1000ms, stability, fwd
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SPMC 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) SPMC output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]
        tmh_seq = tmh[..., 10:20]
        tmh_hier = tmh[..., 20:30]

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)
        circuit_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        tempo_velocity = h3_direct[(21, 4, 8, 0)].unsqueeze(-1)
        mean_amplitude_1s = h3_direct[(7, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f19: Sequence Planning (SMA) (coefficients sum = 1.0)
        f19 = torch.sigmoid(
            0.40 * beat_period_1s
            + 0.35 * tmh_seq.mean(-1, keepdim=True)
            + 0.25 * tmh_hier.mean(-1, keepdim=True)
        )

        # f20: Motor Preparation (PMC) (coefficients sum = 1.0)
        f20 = torch.sigmoid(
            0.40 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * circuit_period_1s
            + 0.30 * tempo_velocity
        )

        # f21: Execution Output (M1) (coefficients sum = 1.0)
        f21 = torch.sigmoid(
            0.35 * (f19 * f20)
            + 0.35 * bep_groove.mean(-1, keepdim=True)
            + 0.30 * mean_amplitude_1s
        )

        # ═══ LAYER M: Mathematical ═══
        circuit_flow = torch.sigmoid(
            0.5 * f19 + 0.5 * f21
        )
        hierarchy_index = torch.sigmoid(
            0.5 * f19 + 0.5 * f20
        )
        timing_precision = torch.sigmoid(
            0.5 * tmh_short.mean(-1, keepdim=True)
            + 0.5 * beat_period_1s
        )

        # ═══ LAYER P: Present ═══
        sma_activity = tmh_seq.mean(-1, keepdim=True)
        m1_output = bep_groove.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        sequence_pred = torch.sigmoid(
            0.5 * f19 + 0.5 * beat_period_1s
        )
        execution_pred = torch.sigmoid(
            0.5 * f21 + 0.5 * bep_motor.mean(-1, keepdim=True)
        )
        timing_pred = torch.sigmoid(
            0.5 * timing_precision + 0.5 * tmh_hier.mean(-1, keepdim=True)
        )

        return torch.cat([
            f19, f20, f21,                                          # E: 3D
            circuit_flow, hierarchy_index, timing_precision,        # M: 3D
            sma_activity, m1_output,                                # P: 2D
            sequence_pred, execution_pred, timing_pred,             # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (2 primary fMRI, 1 MVPA, 1 clinical, 1 single-unit, 1 EEG, 2 reviews) | Grahn 2007, Hoddinott 2024, Harrison 2025, Kohler 2025, Okada 2022, Pierrieau 2025, Zatorre 2007, Thaut 2015 |
| **Effect Sizes** | F(2,38)=20.67 (beat×region); Z=5.67 (putamen); significant RSA, MVPA, clinical clusters | Multi-modal convergence |
| **Evidence Modality** | fMRI + MVPA/RSA + single-unit + EEG + clinical (PD) | Strong multi-method validation |
| **Brain Regions** | 7 (5 with MNI from Grahn 2007, 2 from MVPA) | pre-SMA/SMA, Putamen, PMd, M1, Cerebellum, IFG, STG |
| **Causal Evidence** | Partial (PD lesion model for BG; single-unit for cerebellum; no direct TMS to SMA) | Moderate |
| **Falsification Tests** | 3/5 testable | Moderate validity |
| **R³ Features Used** | ~18D of 49D | Energy + change + interactions |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/sequence |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893–906. https://doi.org/10.1162/jocn.2007.19.5.893
2. **Hoddinott, J. D., & Grahn, J. A. (2024)**. Neural representations of beat and rhythm in motor and association regions. *Cerebral Cortex*, 34, bhae406. https://doi.org/10.1093/cercor/bhae406
3. **Harrison, E. C., Grossen, S., Tueth, L. E., Haussler, A. M., Rawson, K. S., Campbell, M. C., & Earhart, G. M. (2025)**. Neural mechanisms underlying synchronization of movement to musical cues in Parkinson disease and aging. *Frontiers in Neuroscience*, 19, 1550802. https://doi.org/10.3389/fnins.2025.1550802
4. **Kohler, A., Novembre, G., Villringer, A., & Keller, P. E. (2025)**. Distinct and content-specific neural representations of self- and other-produced actions in joint piano performance. *Frontiers in Human Neuroscience*, 19, 1543131.
5. **Okada, K., Takeya, R., & Tanaka, M. (2022)**. Neural signals regulating motor synchronization in the primate deep cerebellar nuclei. *Nature Communications*, 13, 2504. https://doi.org/10.1038/s41467-022-30246-2
6. **Pierrieau, E., et al. (2025)**. Changes in cortical beta power predict motor control flexibility, not vigor. *Communications Biology*, 8, 1041.
7. **Zatorre, R. J., Chen, J. L., & Penhune, V. B. (2007)**. When the brain plays music: auditory-motor interactions in music perception and production. *Nature Reviews Neuroscience*, 8(7), 547–558. https://doi.org/10.1038/nrn2152
8. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: Rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185. https://doi.org/10.3389/fpsyg.2014.01185

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM, GRV) | BEP (30D) + TMH (30D) mechanisms |
| SMA encoding | S⁰.L4.τ_velocity_T[15] + HC⁰.PTM | R³.spectral_flux[10] + TMH.sequence_integration |
| PMC selection | S⁰.L9.Γ_entropy_T[116] + HC⁰.NPL | R³.spectral_change[21] + BEP.motor_coupling |
| M1 execution | S⁰.X_L0L4[128:136] + HC⁰.GRV | R³.x_l0l5[25:33] + BEP.groove |
| Cerebellar timing | S⁰.Γ_var[105] + HC⁰.ITM | H³ stability tuples + TMH.short_term |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **NPL → BEP.motor_coupling** [10:20]: Neural phase locking for SMA-PMC coupling maps to BEP's motor coupling.
- **PTM → TMH.sequence_integration** [10:20]: Predictive timing for SMA sequence planning maps to TMH's sequence integration.
- **ITM → TMH.short_term** [0:10]: Interval timing for cerebellar correction maps to TMH's short-term memory.
- **GRV → BEP.groove_processing** [20:30]: Groove processing for M1 execution drive maps to BEP's groove section.

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

> These mismatches are logged for Phase 5 resolution. The **doc is authoritative**; code should be updated.

| # | Field | Doc (SPMC.md) | Code (spmc.py) | Priority |
|---|-------|---------------|-----------------|----------|
| 1 | FULL_NAME | "SMA-Premotor-M1 Motor Circuit" | "Sensory-Predictive Motor Coupling" | HIGH |
| 2 | OUTPUT_DIM | 11 | 10 | HIGH |
| 3 | MECHANISM_NAMES | ("BEP", "TMH") | ("BEP",) — missing TMH | HIGH |
| 4 | h3_demand | 15 tuples (see Section 5.1) | () empty tuple | HIGH |
| 5 | Layer E dim names | f19_sequence_planning, f20_motor_preparation, f21_execution_output | f19_sma_temporal_encoding, f20_pmc_sequence_planning, f21_m1_execution_precision | MEDIUM |
| 6 | Layer M dimensions | 3D (circuit_flow, hierarchy_index, timing_precision) | 2D (hierarchical_flow_fn, timing_precision) | HIGH |
| 7 | Layer P dim names | sma_activity, m1_output | sma_pmc_m1_state, motor_sequence_complexity | MEDIUM |
| 8 | Layer F dim names | sequence_pred, execution_pred, timing_pred | sequence_execution_pred, timing_accuracy_pred, circuit_efficiency_pred | MEDIUM |
| 9 | Citations | Grahn 2007, Hoddinott 2024, Harrison 2025 + 5 more | Chen 2008, Zatorre 2007 | HIGH |
| 10 | brain_regions | 7 regions (pre-SMA/SMA, Putamen, PMd, M1, Cerebellum, IFG, STG) | 4 regions (SMA, PMC, Putamen, Cerebellum) | MEDIUM |
| 11 | CROSS_UNIT_READS | Not specified as empty | () empty tuple | LOW |
| 12 | compute() | Full pseudocode in Section 11.1 | Returns torch.zeros() stub | LOW (expected for beta) |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
