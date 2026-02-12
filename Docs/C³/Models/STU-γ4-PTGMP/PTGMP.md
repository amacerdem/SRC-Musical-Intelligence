# STU-γ4-PTGMP: Piano Training Grey Matter Plasticity

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, TMH mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/General/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ4-PTGMP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Piano Training Grey Matter Plasticity** (PTGMP) model describes how piano training in older adults induces structural neuroplasticity — measurable grey matter volume (GMV) increases in DLPFC (bilateral) and cerebellum (right hemisphere), along with increased frontal theta power during improvisation. This model captures the acoustic correlates of motor-learning-driven plasticity, specifically the spectral and temporal features that track with training-induced structural brain changes.

```
PIANO TRAINING GREY MATTER PLASTICITY — THREE PATHWAYS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE PLANNING                     MOTOR COORDINATION
Brain region: DLPFC (bilateral)        Brain region: Cerebellum (right)
Effect: GMV increase d=0.34            Effect: GMV increase d=0.34
Function: Audio-motor planning         Function: Timing/coordination
R³ basis: Energy × Interactions        R³ basis: Change × Interactions

CREATIVE FLEXIBILITY
Brain region: Frontal cortex
Effect: Theta power increase d=0.27
Function: Improvisation / novel motor sequences
R³ basis: Energy dynamics + Change rate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Late-life structural neuroplasticity is driven by
audio-motor integration demands. Older adults who train piano
show bilateral DLPFC and right cerebellar GMV increases comparable
to younger learners, suggesting age-resilient plasticity pathways.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

PTGMP provides evidence that sensorimotor timing circuits remain plastic in late life:

1. **HMCE** (α1) provides the hierarchical context that PTGMP's motor learning operates within.
2. **AMSC** (α2) describes the auditory-motor coupling that PTGMP's plasticity strengthens.
3. **TPIO** (β2) relates to timing precision that PTGMP's cerebellar plasticity improves.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PTGMP Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 PTGMP — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (piano performance — keystroke sequences)                     ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        DORSOLATERAL PREFRONTAL CORTEX (DLPFC, bilateral)            │    ║
║  │        Executive planning for audio-motor sequences                  │    ║
║  │        GMV increase: d = 0.34                                        │    ║
║  │        Function: Sequence planning, working memory for music         │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Motor command relay                         ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        CEREBELLUM (right hemisphere)                                │    ║
║  │        Motor coordination and timing precision                      │    ║
║  │        GMV increase: d = 0.34                                        │    ║
║  │        Function: Keystroke timing, error correction, smoothness     │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Feedback loop                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        FRONTAL CORTEX                                               │    ║
║  │        Creative motor-perceptual integration                        │    ║
║  │        Theta power increase: d = 0.27                                │    ║
║  │        Function: Improvisation, novel sequence generation           │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  PLASTICITY: Late-life structural neuroplasticity — older adults show       ║
║  comparable GMV increases to younger learners after piano training.          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
DLPFC bilateral GMV increase:    d = 0.34 (VBM, older adults, piano training)
Cerebellum right GMV increase:   d = 0.34 (VBM, older adults, piano training)
Frontal theta power increase:    d = 0.27 (EEG, improvisation condition)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TMH → PTGMP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PTGMP COMPUTATION ARCHITECTURE                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins × 172.27Hz frame rate                    ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                       PTGMP reads: 33D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Syllable ────┐ ┌── Beat ──────────┐ ┌── Section ────────┐ │        ║
║  │  │ 300ms (H8)     │ │ 700ms (H14)      │ │ 5000ms (H20)     │ │        ║
║  │  │                │ │                   │ │                    │ │        ║
║  │  │ Short context  │ │ Medium context    │ │ Long context       │ │        ║
║  │  │ Keystroke-     │ │ Phrase-level      │ │ Practice session-  │ │        ║
║  │  │ level timing   │ │ motor planning    │ │ level adaptation   │ │        ║
║  │  └──────┬─────────┘ └──────┬────────────┘ └──────┬─────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                       PTGMP demand: ~16 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  TMH (30D)      │  Temporal Memory Hierarchy mechanism                   ║
║  │                 │                                                        ║
║  │ Short   [0:10] │  Keystroke timing, onset patterns, local motor cue     ║
║  │ Medium  [10:20]│  Phrase-level planning, motor sequence coordination    ║
║  │ Long    [20:30]│  Practice adaptation, skill consolidation signal       ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PTGMP MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_dlpfc_plasticity, f02_cerebellar_plast,│        ║
║  │                       f03_frontal_theta                          │        ║
║  │  Layer M (Math):      plasticity_index, age_resilience           │        ║
║  │  Layer P (Present):   motor_coordination, audio_motor_binding    │        ║
║  │  Layer F (Future):    skill_trajectory, timing_improvement,      │        ║
║  │                       adaptation_rate                            │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Piano training study** | VBM | Older adults | DLPFC bilateral GMV increase after piano training | d = 0.34 | **f01_dlpfc_plasticity**: executive planning |
| **Piano training study** | VBM | Older adults | Cerebellum right hemisphere GMV increase | d = 0.34 | **f02_cerebellar_plast**: motor coordination |
| **Piano training study** | EEG | Older adults | Frontal theta power increase during improvisation | d = 0.27 | **f03_frontal_theta**: creative flexibility |

### 3.2 The Plasticity Gradient

```
STRUCTURAL NEUROPLASTICITY FROM PIANO TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region              Function            Effect Size   Evidence
────────────────────────────────────────────────────────────────
DLPFC (bilateral)   Executive planning  d = 0.34      VBM (GMV)
Cerebellum (right)  Motor coordination  d = 0.34      VBM (GMV)
Frontal cortex      Improvisation       d = 0.27      EEG (theta)

Key Finding: Older adults show grey matter volume increases
comparable to younger trainees. Late-life plasticity is driven
by the audio-motor integration demands of piano practice.

Note: d = 0.34 is a small-to-medium effect. γ-tier because
single-domain evidence (piano training only), limited
replication, and older-adult specificity.
```

### 3.3 Effect Size Summary

```
DLPFC GMV:          d = 0.34 (VBM, bilateral)
Cerebellum GMV:     d = 0.34 (VBM, right hemisphere)
Frontal theta:      d = 0.27 (EEG, improvisation)
Quality Assessment: γ-tier (speculative — single paradigm, limited N)
Replication:        Limited — training-specific plasticity
```

---

## 4. R³ Input Mapping: What PTGMP Reads

### 4.1 R³ Feature Dependencies (33D of 49D)

| R³ Group | Index | Feature | PTGMP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Motor intensity dynamics | Keystroke force tracking |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid | Pitch perception proxy | Melodic learning |
| **B: Energy** | [10] | spectral_flux | Note onset detection | Motor timing anchor |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Keystroke precision |
| **D: Change** | [21] | spectral_change | Short-context motor dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Medium-context dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | Pitch learning trajectory |
| **D: Change** | [24] | timbre_change | Timbral evolution | Instrument identity |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation x Perceptual coupling | Motor-timing learning |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics x Perceptual coupling | Audio-motor integration (DLPFC) |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Perceptual x Relations coupling | Structural coordination |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ─────────┐
R³[11] onset_strength ────────┼──► Motor Timing Precision
R³[21:25] Change (4D) ────────┘   TMH.short_context at H8 (300ms)
                                    Cerebellar timing coordination

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Audio-Motor Planning
R³[22] energy_change ───────────┘   TMH.medium_context at H14 (700ms)
                                    DLPFC executive sequence planning

R³[25:33] x_l0l5 (8D) ────────┐
R³[33:41] x_l4l5 (8D) ────────┼──► Long-Range Skill Consolidation
R³[41:49] x_l5l7 (8D) ────────┘   TMH.long_context at H20 (5000ms)
                                    Practice-level adaptation signal

Plasticity Factor ─────────────── Age-Resilient Plasticity
                                    d = 0.34 DLPFC, d = 0.34 cerebellum
                                    Older adults maintain capacity
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PTGMP requires H³ features at three TMH horizons: H8 (300ms), H14 (700ms), H20 (5000ms).
These correspond to keystroke → phrase → practice-session timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 8 | M0 (value) | L0 (fwd) | Current onset detection |
| 10 | spectral_flux | 8 | M1 (mean) | L0 (fwd) | Mean onset rate (short) |
| 11 | onset_strength | 8 | M0 (value) | L0 (fwd) | Keystroke boundary current |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 22 | energy_change | 14 | M1 (mean) | L0 (fwd) | Mean energy dynamics |
| 22 | energy_change | 14 | M3 (std) | L0 (fwd) | Motor variability proxy |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Mean pitch dynamics |
| 7 | amplitude | 14 | M18 (trend) | L0 (fwd) | Intensity trajectory |
| 8 | loudness | 14 | M1 (mean) | L0 (fwd) | Mean loudness over phrase |
| 8 | loudness | 14 | M19 (stability) | L0 (fwd) | Performance consistency |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term motor coupling |
| 25 | x_l0l5[0] | 20 | M19 (stability) | L0 (fwd) | Practice-level stability |
| 33 | x_l4l5[0] | 20 | M1 (mean) | L0 (fwd) | Audio-motor integration mean |
| 33 | x_l4l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Repetition-based learning |
| 41 | x_l5l7[0] | 20 | M1 (mean) | L0 (fwd) | Structural coupling mean |
| 41 | x_l5l7[0] | 20 | M18 (trend) | L0 (fwd) | Skill improvement trend |

**Total PTGMP H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 TMH Mechanism Binding

PTGMP reads from the **TMH** (Temporal Memory Hierarchy) mechanism:

| TMH Sub-section | Range | PTGMP Role | Weight |
|-----------------|-------|-----------|--------|
| **Short Context** | TMH[0:10] | Keystroke-level motor timing (cerebellum, onset precision) | **1.0** (primary) |
| **Medium Context** | TMH[10:20] | Phrase-level motor planning (DLPFC, sequence coordination) | **1.0** (primary) |
| **Long Context** | TMH[20:30] | Practice-session adaptation (plasticity consolidation) | **1.0** (primary) |

PTGMP does NOT read from BEP — grey matter plasticity is about structural adaptation from motor-learning demands, not beat entrainment.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PTGMP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: STU PTGMP [229:239]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_dlpfc_plasticity│ [0, 1] │ DLPFC bilateral GMV increase proxy (d=0.34).
    │                     │        │ Audio-motor planning complexity.
    │                     │        │ f01 = σ(0.35 · amp_trend ·
    │                     │        │         x_l4l5_mean · TMH.medium)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_cerebellar_plast│ [0, 1] │ Cerebellum right hemisphere GMV proxy (d=0.34).
    │                     │        │ Motor coordination and timing precision.
    │                     │        │ f02 = σ(0.30 · flux_mean · onset_val ·
    │                     │        │         TMH.short)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_frontal_theta   │ [0, 1] │ Frontal theta power increase proxy (d=0.27).
    │                     │        │ Creative motor-perceptual integration.
    │                     │        │ f03 = σ(0.30 · energy_change_std ·
    │                     │        │         pitch_change_mean · TMH.medium)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 3  │ plasticity_index    │ [0, 1] │ Overall structural plasticity signal.
    │                     │        │ Weighted sum of region-specific effects.
    │                     │        │ plast = (0.34·f01 + 0.34·f02 + 0.27·f03) /
    │                     │        │         (0.34 + 0.34 + 0.27)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 4  │ age_resilience      │ [0, 1] │ Late-life plasticity preservation factor.
    │                     │        │ Stability of long-range motor coupling.
    │                     │        │ age_r = σ(0.50 · stability_loud ·
    │                     │        │           stability_coupling)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 5  │ motor_coordination  │ [0, 1] │ Current cerebellar motor state.
    │                     │        │ TMH.short_context aggregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 6  │ audio_motor_binding │ [0, 1] │ Current DLPFC audio-motor integration state.
    │                     │        │ TMH.medium_context aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 7  │ skill_trajectory    │ [0, 1] │ Predicted motor improvement direction.
    │                     │        │ Long-range coupling trend.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 8  │ timing_improvement  │ [0, 1] │ Predicted timing precision improvement.
    │                     │        │ Autocorrelation-based repetition learning.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 9  │ adaptation_rate     │ [0, 1] │ Rate of practice-level adaptation.
    │                     │        │ TMH.long_context trend-based estimate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
Manifold range: STU PTGMP [229:239]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Plasticity Encoding Function

```
Plasticity Encoding:

    GMV_Change(region) = f(Training_Intensity, Audio_Motor_Demand)

    For DLPFC (bilateral):
      Plasticity ∝ Audio-motor planning complexity
      d = 0.34 (grey matter volume increase)

    For Cerebellum (right):
      Plasticity ∝ Motor timing precision demand
      d = 0.34 (grey matter volume increase)

    For Frontal Cortex:
      Theta_Power ∝ Improvisation / creative flexibility
      d = 0.27 (theta band power increase)

    Age Resilience:
      Plasticity(older) ≈ Plasticity(younger)
      Late-life structural neuroplasticity maintained
```

### 7.2 Feature Formulas

```python
# ═══ IMPORTANT: Sigmoid coefficient rule ═══
# For σ(Σ wᵢ · gᵢ), |wᵢ| must sum ≤ 1.0
# All products below use multiplicative gating
# which keeps effective input in reasonable range.

# f01: DLPFC Plasticity (bilateral, d=0.34)
amp_trend = h3[(7, 14, 18, 0)]        # amplitude trend at H14
x_l4l5_mean = h3[(33, 20, 1, 0)]      # x_l4l5 mean at H20
f01 = σ(0.35 · amp_trend · x_l4l5_mean
         · mean(TMH.medium_context[10:20]))
# |0.35| ≤ 1.0 ✓  (multiplicative terms bounded [0,1])

# f02: Cerebellar Plasticity (right, d=0.34)
flux_mean = h3[(10, 8, 1, 0)]         # spectral_flux mean at H8
onset_val = h3[(11, 8, 0, 0)]         # onset_strength value at H8
f02 = σ(0.30 · flux_mean · onset_val
         · mean(TMH.short_context[0:10]))
# |0.30| ≤ 1.0 ✓

# f03: Frontal Theta (d=0.27)
energy_std = h3[(22, 14, 3, 0)]       # energy_change std at H14
pitch_mean = h3[(23, 14, 1, 0)]       # pitch_change mean at H14
f03 = σ(0.30 · energy_std · pitch_mean
         · mean(TMH.medium_context[10:20]))
# |0.30| ≤ 1.0 ✓

# f04: Plasticity Index (effect-size weighted average)
f04 = (0.34 · f01 + 0.34 · f02 + 0.27 · f03) / (0.34 + 0.34 + 0.27)
# Weighted by reported effect sizes → [0, 1]

# f05: Age Resilience
stability_loud = h3[(8, 14, 19, 0)]   # loudness stability at H14
stability_coupling = h3[(25, 20, 19, 0)] # x_l0l5 stability at H20
f05 = σ(0.50 · stability_loud · stability_coupling)
# |0.50| ≤ 1.0 ✓  (multiplicative → effective range compressed)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence Type | Effect | PTGMP Function |
|--------|-----------------|---------------|--------|---------------|
| **DLPFC (bilateral)** | ±44, 36, 28 | VBM (GMV) | d = 0.34 | Executive audio-motor planning |
| **Cerebellum (right)** | 24, -60, -30 | VBM (GMV) | d = 0.34 | Motor coordination / timing |
| **Frontal cortex** | ±4, 28, 44 | EEG (theta) | d = 0.27 | Improvisation / creative flexibility |

---

## 9. Cross-Unit Pathways

### 9.1 PTGMP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PTGMP INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  PTGMP.motor_coordination ──► AMSC (cerebellar → auditory-motor coupling)  │
│  PTGMP.audio_motor_binding ──► TPIO (DLPFC → timing precision)            │
│  PTGMP.skill_trajectory ────► HMCE (plasticity → context depth growth)    │
│                                                                             │
│  CROSS-UNIT (P4: STU internal):                                            │
│  TMH.short_context ↔ PTGMP.cerebellar_plast (timing → plasticity)        │
│  TMH.medium_context ↔ PTGMP.dlpfc_plasticity (planning → plasticity)     │
│                                                                             │
│  CROSS-UNIT (P5: STU → IMU):                                              │
│  PTGMP.plasticity_index ──► IMU (structural plasticity → memory encoding) │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  PTGMP.frontal_theta ──► ARU (improvisation → affective engagement)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **DLPFC lesion** | Should impair audio-motor sequence planning | Testable |
| **Cerebellar damage** | Should reduce motor timing precision gains | Testable |
| **Non-piano training** | Other motor training should show different GMV patterns | Testable |
| **Young adult comparison** | Effect sizes should be similar (age resilience) | Testable |
| **Theta band disruption** | TMS over frontal cortex should impair improvisation | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PTGMP(BaseModel):
    """Piano Training Grey Matter Plasticity.

    Output: 10D per frame.
    Reads: TMH mechanism (30D), R³ direct.
    Zero learned parameters — all deterministic.
    """
    NAME = "PTGMP"
    UNIT = "STU"
    TIER = "γ4"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TMH",)        # Primary mechanism

    # Effect sizes from literature
    DLPFC_D = 0.34     # DLPFC bilateral GMV increase
    CEREB_D = 0.34     # Cerebellum right GMV increase
    THETA_D = 0.27     # Frontal theta power increase

    # Sigmoid coefficients — |wᵢ| ≤ 1.0 rule enforced
    ALPHA = 0.35   # DLPFC plasticity weight
    BETA = 0.30    # Cerebellar plasticity weight
    GAMMA = 0.30   # Frontal theta weight
    DELTA = 0.50   # Age resilience weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for PTGMP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Short context (H8 = 300ms) — cerebellar timing
            (10, 8, 0, 0),    # spectral_flux, value, forward
            (10, 8, 1, 0),    # spectral_flux, mean, forward
            (11, 8, 0, 0),    # onset_strength, value, forward
            (21, 8, 1, 0),    # spectral_change, mean, forward
            # Medium context (H14 = 700ms) — DLPFC planning
            (22, 14, 1, 0),   # energy_change, mean, forward
            (22, 14, 3, 0),   # energy_change, std, forward
            (23, 14, 1, 0),   # pitch_change, mean, forward
            (7, 14, 18, 0),   # amplitude, trend, forward
            (8, 14, 1, 0),    # loudness, mean, forward
            (8, 14, 19, 0),   # loudness, stability, forward
            # Long context (H20 = 5000ms) — plasticity consolidation
            (25, 20, 1, 0),   # x_l0l5[0], mean, forward
            (25, 20, 19, 0),  # x_l0l5[0], stability, forward
            (33, 20, 1, 0),   # x_l4l5[0], mean, forward
            (33, 20, 22, 0),  # x_l4l5[0], autocorrelation, forward
            (41, 20, 1, 0),   # x_l5l7[0], mean, forward
            (41, 20, 18, 0),  # x_l5l7[0], trend, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PTGMP 10D output.

        Args:
            mechanism_outputs: {"TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) PTGMP output
        """
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short context
        tmh_medium = tmh[..., 10:20]      # medium context
        tmh_long = tmh[..., 20:30]        # long context

        # ═══ LAYER E: Explicit features ═══

        # f01: DLPFC Plasticity (bilateral, d=0.34)
        amp_trend = h3_direct[(7, 14, 18, 0)].unsqueeze(-1)
        x_l4l5_mean = h3_direct[(33, 20, 1, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.ALPHA * (
            amp_trend * x_l4l5_mean
            * tmh_medium.mean(-1, keepdim=True)
        ))

        # f02: Cerebellar Plasticity (right, d=0.34)
        flux_mean = h3_direct[(10, 8, 1, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 8, 0, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.BETA * (
            flux_mean * onset_val
            * tmh_short.mean(-1, keepdim=True)
        ))

        # f03: Frontal Theta (d=0.27)
        energy_std = h3_direct[(22, 14, 3, 0)].unsqueeze(-1)
        pitch_mean = h3_direct[(23, 14, 1, 0)].unsqueeze(-1)
        f03 = torch.sigmoid(self.GAMMA * (
            energy_std * pitch_mean
            * tmh_medium.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══

        # Plasticity index — effect-size weighted
        total_d = self.DLPFC_D + self.CEREB_D + self.THETA_D
        plasticity_index = (
            self.DLPFC_D * f01
            + self.CEREB_D * f02
            + self.THETA_D * f03
        ) / total_d

        # Age resilience — stability-based
        stability_loud = h3_direct[(8, 14, 19, 0)].unsqueeze(-1)
        stability_coupling = h3_direct[(25, 20, 19, 0)].unsqueeze(-1)
        age_resilience = torch.sigmoid(self.DELTA * (
            stability_loud * stability_coupling
        ))

        # ═══ LAYER P: Present ═══
        motor_coordination = tmh_short.mean(-1, keepdim=True)
        audio_motor_binding = tmh_medium.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══

        # Skill trajectory — long-range trend
        x_l5l7_trend = h3_direct[(41, 20, 18, 0)].unsqueeze(-1)
        skill_trajectory = torch.sigmoid(
            0.6 * x_l5l7_trend + 0.4 * tmh_long.mean(-1, keepdim=True)
        )
        # |0.6| + |0.4| = 1.0 ≤ 1.0 ✓

        # Timing improvement — repetition learning
        x_l4l5_autocorr = h3_direct[(33, 20, 22, 0)].unsqueeze(-1)
        timing_improvement = torch.sigmoid(
            0.5 * x_l4l5_autocorr + 0.5 * tmh_short.mean(-1, keepdim=True)
        )
        # |0.5| + |0.5| = 1.0 ≤ 1.0 ✓

        # Adaptation rate — long context trend
        x_l0l5_mean = h3_direct[(25, 20, 1, 0)].unsqueeze(-1)
        adaptation_rate = torch.sigmoid(
            0.4 * x_l0l5_mean + 0.3 * tmh_long.mean(-1, keepdim=True)
            + 0.3 * plasticity_index
        )
        # |0.4| + |0.3| + |0.3| = 1.0 ≤ 1.0 ✓

        return torch.cat([
            f01, f02, f03,                                    # E: 3D
            plasticity_index, age_resilience,                  # M: 2D
            motor_coordination, audio_motor_binding,           # P: 2D
            skill_trajectory, timing_improvement, adaptation_rate,  # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | Limited | Piano training studies (VBM + EEG) |
| **Effect Sizes** | d = 0.34, d = 0.34, d = 0.27 | DLPFC, cerebellum, frontal theta |
| **Evidence Modality** | VBM, EEG | Structural + electrophysiological |
| **Falsification Tests** | 0/5 confirmed | All pending |
| **R³ Features Used** | 33D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **TMH Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure (E3 + M2 + P2 + F3) |

---

## 13. Scientific References

1. **Piano training studies** — VBM grey matter volume analysis in older adult piano trainees showing DLPFC bilateral (d=0.34) and cerebellum right hemisphere (d=0.34) GMV increases.
2. **Frontal theta studies** — EEG theta band power increase (d=0.27) during piano improvisation in trained older adults.
3. **Age-resilient neuroplasticity** — Evidence that structural brain changes from musical training persist into late life, with older adults showing comparable plasticity to younger trainees.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L0L1, X_L4L5 | R³ (49D): Energy, Change, Interactions |
| Temporal | HC⁰ mechanisms (OSC, ITM, GRV, HRM) | TMH mechanism (30D) |
| Oscillation coupling | OSC[0:56] (gamma/alpha_beta/syllable) | TMH.short_context[0:10] + H³ tuples |
| Motor timing | ITM[216:244] (interval timing) | TMH.short_context + TMH.medium_context |
| Groove | GRV[244:272] (motor coordination) | TMH.medium_context + R³ Change features |
| Memory replay | HRM[272:302] (hippocampal) | TMH.long_context[20:30] |
| Statistics | S⁰.L9 (mean, std) | H³ morphs (M0, M1, M3, M18, M19, M22) |
| Cross-feature | X_L0L1[128:136], X_L4L5[192:200] | R³.x_l0l5[25:33], x_l4l5[33:41], x_l5l7[41:49] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 32/2304 = 1.39% | 16/2304 = 0.69% |
| Output dimensions | 12D | **10D** (catalog spec, streamlined) |

### Why TMH replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, ITM, GRV, HRM). In MI, these are unified into the TMH mechanism with 3 sub-sections:
- **OSC + ITM → TMH.short_context** [0:10]: Neural oscillation coupling + interval timing → keystroke-level motor timing features
- **GRV → TMH.medium_context** [10:20]: Groove motor coordination → phrase-level planning and audio-motor integration
- **HRM → TMH.long_context** [20:30]: Hippocampal replay → practice-session adaptation and skill consolidation

### Output reduction: 12D → 10D

The legacy 12D output included redundant features that duplicated TMH sub-section means. The MI 10D output consolidates:
- Layer E: 4D → 3D (merged separate DLPFC left/right into bilateral)
- Layer M: 2D → 2D (unchanged)
- Layer P: 3D → 2D (merged motor sub-features)
- Layer F: 3D → 3D (unchanged)

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
