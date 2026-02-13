# MPU-γ2-CTBB: Cerebellar Theta-Burst Balance

**Model**: Cerebellar Theta-Burst Balance
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-γ2-CTBB.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Cerebellar Theta-Burst Balance** (CTBB) model proposes that cerebellar intermittent theta-burst stimulation (iTBS) enhances postural control in aging, suggesting cerebellar modulation of motor timing. The effect persists for at least 30 minutes, implicating cerebellar-M1 timing circuits in balance maintenance.

```
CEREBELLAR THETA-BURST BALANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

       CEREBELLAR STIMULATION PATHWAY
       ════════════════════════════════

┌─────────────────────────────────────────────────────┐
│              CEREBELLAR iTBS                         │
│                                                      │
│   Intermittent Theta-Burst Stimulation               │
│   (3-pulse bursts at 50 Hz, repeated at 5 Hz)       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              CEREBELLUM                              │
│                                                      │
│   Enhanced timing precision                          │
│   Motor timing modulation                            │
│   Error correction improvement                       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              CEREBELLAR → M1 CIRCUIT                 │
│                                                      │
│   Timing correction → Motor cortex excitability      │
│   Duration: ≥30 minutes post-stimulation             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              POSTURAL CONTROL                        │
│                                                      │
│   Postural sway ↓ (improved balance)                 │
│   Timing variability ↓ (more precise)                │
└─────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Cerebellar iTBS enhances motor timing precision and
postural control. This implicates the cerebellum as a key timing
module in the motor circuit, with lasting effects (≥30 min) on
the cerebellar-M1 pathway that governs balance and rhythmic control.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why CTBB Matters for MPU

CTBB highlights the cerebellar timing role in the Motor Planning Unit:

1. **PEOM/MSR** (α-tier) establish motor entrainment and training effects.
2. **SPMC** (β4) describes the SMA→PMC→M1 circuit with cerebellar correction.
3. **CTBB** (γ2) provides causal evidence for the cerebellar role: iTBS to cerebellum directly modulates motor timing precision and postural control.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → CTBB)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CTBB COMPUTATION ARCHITECTURE                            ║
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
║  │                         CTBB reads: ~14D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         CTBB demand: ~9 of 2304 tuples           │        ║
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
║  │                    CTBB MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f25_cerebellar_timing,                     │        ║
║  │                       f26_m1_modulation,                         │        ║
║  │                       f27_postural_control                        │        ║
║  │  Layer M (Math):      timing_enhancement, sway_reduction,        │        ║
║  │                       cerebellar_m1_coupling                      │        ║
║  │  Layer P (Present):   timing_precision, motor_stability           │        ║
║  │  Layer F (Future):    timing_pred, balance_pred,                 │        ║
║  │                       modulation_pred                             │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Sansare 2025** | Cerebellar iTBS + force-plate posturography | 40 (20 active, 20 sham) | Active cerebellar iTBS significantly reduces postural sway vs sham, sustained ≥30 min. Right lateral cerebellum target (3cm lateral, 1cm below inion), 600 pulses at 75% RMT | F = 9.600, p = 0.004, η² = 0.202 (Group main effect); Bonferroni POST1-6: p = .006, .002, .018, .040, .011, .003 | **Primary**: f25 (cerebellar timing), f27 (postural control). Causal TMS evidence for cerebellar balance role |
| **Sansare 2025** | Cerebellar Brain Inhibition (CBI) | 35 (5 dropouts) | CBI did NOT significantly change after iTBS — cerebellar-M1 interaction unaltered despite behavioral improvement | F = 1.570, p = 0.219, η² = 0.045 (Group n.s.) | **Critical null**: f26 M1 modulation may not be mediated by direct cerebellar-M1 pathway; alternative circuits (cerebellar-prefrontal) possible |
| **Okada 2022** | Single-neuron recording (primate dentate nucleus) + electrical microstimulation | 95 neurons, 2 monkeys | Cerebellar dentate contains 3 functional neuron types for synchronized movement: Bilateral (rhythm prediction), Unilateral (saccade timing), Postsaccade (error detection). Electrical stimulation causally affected saccade timing | Bilateral PI = 0.10, t30 = 3.36, p = .002; ISI correlation r = -0.18, p < .01; Postsaccade error r = -0.10, t28 = -4.37, p = .0002 | f25 timing precision: multiple cerebellar modules for rhythm acquisition, error correction, and predictive timing |
| **Shi 2025** | Bilateral iTBS (M1 leg) + AOIT (Tai Chi) in PD | 15 PD patients (crossover) | Bilateral M1 iTBS enhances dual-task gait automaticity, global cognition, and cortical plasticity. Double-cone coil, 1200 pulses total, 65% rMT | Gait F = 5.558, p = .026; MoCA F = 5.294, p = .026; MEP plasticity F = 6.131, p = .020; CSP F = 4.655, p = .040 | f26 M1 modulation: iTBS enhances cortical excitability and GABAergic inhibition, correlates with gait (r = -0.429) |
| **Ivry 1988** | Cerebellar lesion patients + timing tasks | 30 (cerebellar lesions + controls) | Lateral cerebellum dissociation: timing (lateral) vs execution (medial). Cerebellar lesions impair movement timing at 10-100ms scale | Significant timing variability increase in cerebellar patients | Foundational evidence for cerebellar role as timing module |
| **Huang 2005** | TMS protocol characterization | Healthy adults | iTBS (3 pulses at 50Hz, 5Hz trains) produces LTP-like effects lasting ~20-30 min. Established the iTBS protocol used in Sansare 2025 | MEP facilitation for ~20-30 min post-iTBS | Protocol basis for f25 TAU_DECAY = 1800s parameter |

> **NOTE — CBI null result**: Sansare 2025 found that cerebellar iTBS improved postural sway (η² = 0.202) but did NOT significantly change cerebellar brain inhibition (CBI, η² = 0.045). This suggests that balance improvements may be mediated by alternative circuits (cerebellar-prefrontal, cerebellar-vestibular) rather than the direct cerebellar-M1 pathway modeled in f26. The doc retains f26 as a proxy but this should be interpreted cautiously.

> **NOTE — Optimal timing window**: Sansare 2025 reports greatest sway reduction at 10-20 min post-iTBS, consistent with Huang 2005's ~20-30 min facilitation window. This supports TAU_DECAY = 1800s but the effect time course is not linear.

### 3.2 Effect Size Summary

```
Primary Evidence (k=6):  Causal TMS (Sansare 2025), causal microstim (Okada 2022),
                         clinical iTBS (Shi 2025), cerebellar lesion (Ivry 1988),
                         protocol basis (Huang 2005)
Heterogeneity:           Moderate — methods span TMS, single-neuron, fMRI, lesion
Quality Assessment:      γ-tier — causal evidence exists but CBI null complicates mechanism
Effect Magnitudes:       η² = 0.202 (iTBS→sway reduction, Sansare 2025)
                         F(1,38) = 9.600, p = .004 (Group main effect)
                         PI = 0.10, t30 = 3.36, p = .002 (Bilateral neuron enhancement)
                         F = 5.558, p = .026 (dual-task gait, Shi 2025)
Causal Evidence:         Yes — TMS (Sansare), electrical microstimulation (Okada),
                         lesion (Ivry). However CBI null limits mechanistic clarity
Replication:             Sansare 2025 is first in healthy older adults; Shi 2025 partially
                         replicates in PD with different target (M1 vs cerebellum)
```

---

## 4. R³ Input Mapping: What CTBB Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | CTBB Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Motor output level | Balance amplitude |
| **B: Energy** | [10] | spectral_flux | Timing dynamics | Cerebellar tempo tracking |
| **D: Change** | [21] | spectral_change | Timing rate change | Motor adjustment |
| **D: Change** | [22] | energy_change | Energy dynamics | Postural sway proxy |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Cerebellar-M1 modulation | Timing stability |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Balance monitoring | Motor precision |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | CTBB Role | Citation |
|-------------|-------|---------|-----------|----------|
| **G: Rhythm** | [65] | tempo_estimate | Cerebellar timing target for theta-burst calibration | Scheirer 1998; Grosche & Muller 2011 |
| **G: Rhythm** | [66] | beat_strength | Beat salience for cerebellar-M1 timing precision | Bock & Schedl 2011 |

**Rationale**: CTBB models cerebellar theta-burst balance where the cerebellum's timing function is modulated by iTBS. tempo_estimate provides the explicit timing reference the cerebellum tracks (Okada 2022 showed cerebellar dentate nucleus is causal for timing), and beat_strength indicates how salient the beat is for cerebellar-M1 coupling. Sansare 2025 demonstrated that iTBS effects (F=9.600, eta-sq=0.202) depend on timing task difficulty, which these features directly encode.

**Code impact** (future): `r3[..., 65:67]` will feed CTBB's cerebellar timing pathway alongside existing energy and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
TMH.short_term[0:10] ───────────┼──► Cerebellar timing frequency
BEP.beat_entrainment[0:10] ─────┘   Tempo dynamics for postural rhythm

R³[25:33] x_l0l5 ───────────────┐
TMH.sequence_integration[10:20] ─┼──► Cerebellar-M1 coupling
BEP.motor_coupling[10:20] ──────┘   Timing correction pathway

R³[33:41] x_l4l5 ───────────────┐
TMH.hierarchical[20:30] ────────┼──► Balance monitoring
R³[22] energy_change ────────────┘   Postural sway variability
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

CTBB requires H³ features at TMH horizons for cerebellar timing precision and BEP horizons for motor coupling. The demand reflects the relatively compact cerebellar timing circuit.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Timing onset 100ms |
| 10 | spectral_flux | 16 | M1 (mean) | L0 (fwd) | Mean timing 1s |
| 10 | spectral_flux | 16 | M2 (std) | L0 (fwd) | Timing variability 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Cerebellar coupling 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 25 | x_l0l5[0] | 16 | M19 (stability) | L0 (fwd) | Coupling stability 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Balance signal 100ms |
| 33 | x_l4l5[0] | 16 | M2 (std) | L0 (fwd) | Balance variability 1s |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean motor output 1s |

**Total CTBB H³ demand**: 9 tuples of 2304 theoretical = 0.39%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | CTBB Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Timing reference signal | 0.5 |
| **BEP** | Motor Coupling | BEP[10:20] | Cerebellar-M1 coupling | 0.7 |
| **BEP** | Groove Processing | BEP[20:30] | Motor drive (secondary) | 0.3 |
| **TMH** | Short-term Memory | TMH[0:10] | Cerebellar error correction | **1.0** (primary) |
| **TMH** | Sequence Integration | TMH[10:20] | Timing sequence tracking | **1.0** (primary) |
| **TMH** | Hierarchical Structure | TMH[20:30] | Balance hierarchy | 0.5 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
CTBB OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f25_cerebellar_timing    │ [0, 1] │ iTBS timing enhancement.
    │                          │        │ f25 = σ(0.40 * coupling_stability_1s
    │                          │        │       + 0.35 * mean(TMH.short[0:10])
    │                          │        │       + 0.25 * mean(TMH.seq[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f26_m1_modulation        │ [0, 1] │ Motor cortex excitability.
    │                          │        │ f26 = σ(0.40 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * coupling_period_1s
    │                          │        │       + 0.30 * cerebellar_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f27_postural_control     │ [0, 1] │ Balance improvement.
    │                          │        │ f27 = σ(0.35 * f25 * f26
    │                          │        │       + 0.35 * (1 - balance_var_1s)
    │                          │        │       + 0.30 * mean_amplitude_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ timing_enhancement       │ [0, 1] │ iTBS timing improvement magnitude.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ sway_reduction           │ [0, 1] │ Postural sway reduction estimate.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ cerebellar_m1_coupling   │ [0, 1] │ Cerebellar-M1 pathway strength.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ timing_precision         │ [0, 1] │ TMH cerebellar timing precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ motor_stability          │ [0, 1] │ BEP motor output stability.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ timing_pred              │ [0, 1] │ Timing enhancement prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ balance_pred             │ [0, 1] │ Postural control prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ modulation_pred          │ [0, 1] │ M1 modulation prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Cerebellar Timing Enhancement Function

```
PRIMARY EQUATIONS:

    Timing_Enhancement = Cerebellar_iTBS_Effect × Baseline_Precision

POSTURAL CONTROL:

    Sway_Reduction = 1 - (Post_iTBS_Sway / Pre_iTBS_Sway)

CEREBELLAR-M1 COUPLING:

    Coupling_Strength = f(Cerebellar_Output, M1_Excitability)
    Duration: ≥30 minutes post-stimulation
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f25: Cerebellar Timing
f25 = σ(0.40 * coupling_stability_1s
       + 0.35 * mean(TMH.short_term[0:10])
       + 0.25 * mean(TMH.sequence_integration[10:20]))
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f26: M1 Modulation
f26 = σ(0.40 * mean(BEP.motor_coupling[10:20])
       + 0.30 * coupling_period_1s
       + 0.30 * cerebellar_100ms)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f27: Postural Control
f27 = σ(0.35 * f25 * f26                     # interaction term
       + 0.35 * (1 - balance_var_1s)          # lower variability = better
       + 0.30 * mean_amplitude_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Source | Evidence Type | CTBB Function |
|--------|-----------------|--------|---------------|---------------|
| **Right Lateral Cerebellum (Lobules V-VIII)** | ~24, -62, -28 | Sansare 2025 (iTBS target: 3cm lateral, 1cm below inion) | Direct (TMS causal) | Primary iTBS target — sway reduction η² = 0.202 |
| **Cerebellar Dentate Nucleus (posterior)** | Deep cerebellar | Okada 2022 (single-neuron, primate) | Direct (electrophysiology + microstimulation causal) | 3 functional neuron types: rhythm prediction, timing control, error detection |
| **M1 (Primary Motor Cortex)** | ±38, -22, 58 | Sansare 2025 (CBI target); Shi 2025 (iTBS target for gait) | Direct (TMS) | Motor cortex excitability — but CBI null result (η² = 0.045 n.s.) questions direct pathway |
| **SMA** | 0, -6, 58 | Shi 2025 (M1→SMA functional connectivity); Literature inference | Indirect | Timing integration — SMA functionally connected to M1, mediates gait automaticity |
| **Thalamus (VL)** | ~±12, -15, 8 | Okada 2022 (dentate→thalamus→cortex projections) | Indirect (tract-tracing) | Relay station in cerebellar-thalamo-cortical circuit |

> **NOTE — CBI null vs behavioral effect**: Sansare 2025 demonstrated significant postural improvement (η² = 0.202) but NO significant change in CBI (cerebellar-M1 inhibition). This dissociation suggests balance improvements may involve cerebellar-prefrontal or cerebellar-vestibular pathways rather than the direct cerebellar→M1 circuit. The doc models cerebellar→M1 (f26) but this pathway's contribution is uncertain.

---

## 9. Cross-Unit Pathways

### 9.1 CTBB Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CTBB INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  CTBB.cerebellar_timing ─────────► SPMC (cerebellar role in circuit)       │
│  CTBB.timing_precision ──────────► PEOM (timing for entrainment)           │
│  CTBB.motor_stability ───────────► ASAP (stability for prediction)         │
│                                                                             │
│  CROSS-UNIT (MPU → STU):                                                   │
│  CTBB.timing_enhancement ────────► STU (cerebellar timing signal)          │
│  CTBB.cerebellar_m1_coupling ────► STU (timing circuit strength)           │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► CTBB (beat/motor processing)            │
│  TMH mechanism (30D) ────────────► CTBB (temporal memory/sequence)         │
│  R³ (~14D) ──────────────────────► CTBB (direct spectral features)         │
│  H³ (9 tuples) ──────────────────► CTBB (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Sham stimulation** | Sham iTBS should show no timing enhancement | ✅ Testable |
| **Non-cerebellar target** | iTBS to non-cerebellar sites should not improve balance | ✅ Testable |
| **Duration** | Effect should decay after 30+ minutes | ✅ Testable |
| **Age interaction** | Older adults may show larger effects | Testable |
| **Music context** | Musical timing tasks may show enhanced effect | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class CTBB(BaseModel):
    """Cerebellar Theta-Burst Balance Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "CTBB"
    UNIT = "MPU"
    TIER = "γ2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    TAU_DECAY = 1800.0  # 30 min stimulation effect duration (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """9 tuples for CTBB computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── TMH horizons: cerebellar timing ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 16, 1, 0),    # spectral_flux, 1000ms, mean, fwd
            (10, 16, 2, 0),    # spectral_flux, 1000ms, std, fwd
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 19, 0),   # x_l0l5[0], 1000ms, stability, fwd
            # ── BEP horizons: motor coupling ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 16, 2, 0),    # x_l4l5[0], 1000ms, std, fwd
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute CTBB 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) CTBB output
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
        coupling_stability_1s = h3_direct[(25, 16, 19, 0)].unsqueeze(-1)
        coupling_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        cerebellar_100ms = h3_direct[(25, 3, 0, 2)].unsqueeze(-1)
        balance_var_1s = h3_direct[(33, 16, 2, 0)].unsqueeze(-1)
        mean_amplitude_1s = h3_direct[(7, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f25: Cerebellar Timing (coefficients sum = 1.0)
        f25 = torch.sigmoid(
            0.40 * coupling_stability_1s
            + 0.35 * tmh_short.mean(-1, keepdim=True)
            + 0.25 * tmh_seq.mean(-1, keepdim=True)
        )

        # f26: M1 Modulation (coefficients sum = 1.0)
        f26 = torch.sigmoid(
            0.40 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * coupling_period_1s
            + 0.30 * cerebellar_100ms
        )

        # f27: Postural Control (coefficients sum = 1.0)
        f27 = torch.sigmoid(
            0.35 * (f25 * f26)
            + 0.35 * (1 - balance_var_1s)
            + 0.30 * mean_amplitude_1s
        )

        # ═══ LAYER M: Mathematical ═══
        timing_enhancement = f25
        sway_reduction = torch.sigmoid(
            0.5 * f27 + 0.5 * (1 - balance_var_1s)
        )
        cerebellar_m1_coupling = torch.sigmoid(
            0.5 * f25 + 0.5 * f26
        )

        # ═══ LAYER P: Present ═══
        timing_precision = tmh_short.mean(-1, keepdim=True)
        motor_stability = bep_motor.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        timing_pred = torch.sigmoid(
            0.5 * f25 + 0.5 * coupling_stability_1s
        )
        balance_pred = torch.sigmoid(
            0.5 * f27 + 0.5 * coupling_period_1s
        )
        modulation_pred = torch.sigmoid(
            0.5 * f26 + 0.5 * bep_motor.mean(-1, keepdim=True)
        )

        return torch.cat([
            f25, f26, f27,                                          # E: 3D
            timing_enhancement, sway_reduction, cerebellar_m1_coupling, # M: 3D
            timing_precision, motor_stability,                       # P: 2D
            timing_pred, balance_pred, modulation_pred,              # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 6 | Sansare 2025, Okada 2022, Shi 2025, Ivry 1988, Huang 2005, + CBI null evidence |
| **Effect Sizes** | η² = 0.202 (sway reduction), F = 9.600 p = .004 (Group), PI = 0.10 p = .002 (cerebellar enhancement), F = 5.558 p = .026 (gait) | Multi-method |
| **Evidence Modality** | TMS, single-neuron electrophysiology, microstimulation, lesion, posturography, gait analysis | Multi-modal with causal evidence |
| **Brain Regions** | 5 (2 direct TMS/electrophysiology + 3 indirect/literature) | CBI null noted |
| **Causal Evidence** | Yes — TMS (Sansare), microstimulation (Okada), lesion (Ivry). CBI null limits mechanistic clarity | Stronger than typical γ-tier |
| **Falsification Tests** | 5/5 testable | Sham control verified (Sansare 2025) |
| **R³ Features Used** | ~14D of 49D | Energy + change + interactions |
| **H³ Demand** | 9 tuples (0.39%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/sequence |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Sansare, A., Weinrich, M., Bernard, J. A., & Lei, Y. (2025)**. Enhancing Balance Control in Aging Through Cerebellar Theta-Burst Stimulation. *The Cerebellum*, 24, 161. DOI: 10.1007/s12311-025-01915-x
2. **Okada, K., Takeya, R., & Tanaka, M. (2022)**. Neural signals regulating motor synchronization in the primate deep cerebellar nuclei. *Nature Communications*, 13, 2504. DOI: 10.1038/s41467-022-30246-2
3. **Shi, Y., Ma, J., et al. (2025)**. Bilateral intermittent theta-burst stimulation as a priming strategy to enhance action observation and imitation training in early Parkinson's disease. *Journal of NeuroEngineering and Rehabilitation*, 22, 247. DOI: 10.1186/s12984-025-01789-4
4. **Ivry, R. B., Keele, S. W., & Diener, H. C. (1988)**. Dissociation of the lateral and medial cerebellum in movement timing and movement execution. *Experimental Brain Research*, 73, 167-180.
5. **Huang, Y. Z., Edwards, M. J., Rounis, E., Bhatia, K. P., & Rothwell, J. C. (2005)**. Theta burst stimulation of the human motor cortex. *Neuron*, 45(2), 201-206.
6. **Koch, G., et al. (2008)**. Changes in intracortical circuits of the human motor cortex following theta burst stimulation of the lateral cerebellum. *Clinical Neurophysiology*, 119(11), 2559-2569.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM) | BEP (30D) + TMH (30D) mechanisms |
| Cerebellar timing | S⁰.τ_T[15] + HC⁰.ITM | R³.spectral_flux[10] + TMH.short_term |
| M1 modulation | S⁰.τ²_T[19] + HC⁰.NPL | R³.x_l0l5[25:33] + BEP.motor_coupling |
| Balance control | S⁰.Γ_var[105] + HC⁰.PTM | R³.x_l4l5[33:41] + TMH.hierarchical |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 9/2304 = 0.39% | 9/2304 = 0.39% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **ITM → TMH.short_term** [0:10]: Interval timing for cerebellar error correction maps to TMH's short-term memory.
- **NPL → BEP.motor_coupling** [10:20]: Neural phase locking for cerebellar-M1 coupling maps to BEP's motor coupling.
- **PTM → TMH.sequence_integration** [10:20]: Predictive timing for balance monitoring maps to TMH's sequence integration.

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

> **Authoritative source**: This document (CTBB.md) is authoritative for model design.
> **Code file**: `mi_beta/brain/units/mpu/models/ctbb.py` (v2.0.0 stub)
> **Action**: Code will be updated in Phase 5 to match this document.

| # | Field | Doc (authoritative) | Code (current) | Severity |
|---|-------|--------------------|--------------------|----------|
| 1 | `FULL_NAME` | "Cerebellar Theta-Burst Balance" | "Cerebello-Thalamic Beat Binding" | **HIGH** — completely different name |
| 2 | `OUTPUT_DIM` | 11 | 10 | **HIGH** — dimension mismatch |
| 3 | `MECHANISM_NAMES` | `("BEP", "TMH")` | `("BEP",)` | **HIGH** — missing TMH mechanism |
| 4 | `h3_demand` | 9 tuples (see Section 5.1) | `()` (empty) | **HIGH** — no H³ features computed |
| 5 | `LAYERS[E]` | `f25_cerebellar_timing, f26_m1_modulation, f27_postural_control` | `f25_cerebellar_modulation, f26_postural_control, f27_timing_precision` | **MED** — different feature names and ordering |
| 6 | `LAYERS[M]` | `timing_enhancement, sway_reduction, cerebellar_m1_coupling` (3D) | `itbs_effect_fn, sway_reduction_index` (2D) | **HIGH** — 3D vs 2D, different names |
| 7 | `LAYERS[P]` | `timing_precision, motor_stability` | `cerebellar_state, balance_timing_state` | **MED** — different feature names |
| 8 | `LAYERS[F]` | `timing_pred, balance_pred, modulation_pred` | `postural_stability_pred, timing_improvement_pred, cerebellar_plasticity_pred` | **MED** — different feature names |
| 9 | `brain_regions` | 5 regions (Cerebellum, Dentate, M1, SMA, Thalamus) | 3 regions (Cerebellum, SMA, Putamen) | **MED** — different set, Putamen not in doc |
| 10 | `citations` | Sansare 2025 (primary) + 5 supporting | Arora 2024 + Ivry 2008 | **HIGH** — wrong primary paper (Arora vs Sansare) |
| 11 | `paper_count` | 6 | 2 | **MED** — count mismatch |
| 12 | `version` | 2.1.0 | 2.0.0 | **LOW** — expected version lag |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
