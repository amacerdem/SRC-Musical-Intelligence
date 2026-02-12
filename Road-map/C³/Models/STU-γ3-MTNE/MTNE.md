# STU-γ3-MTNE: Music Training Neural Efficiency

**Model**: Music Training Neural Efficiency
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, TMH mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ3-MTNE.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Music Training Neural Efficiency** (MTNE) model describes how music training improves executive function (specifically inhibition) while maintaining stable or decreased prefrontal cortex activation. This dissociation -- better behavioral performance (d = 0.60) with unchanged neural activation (d = 0.04) -- constitutes the hallmark of **neural efficiency**: the trained brain achieves more with less metabolic cost. In untrained controls, equivalent behavioral improvement requires increased neural recruitment (compensatory processing).

```
THE NEURAL EFFICIENCY DISSOCIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUSIC-TRAINED GROUP                    CONTROL GROUP
Behavioral: d = 0.60 improvement       Behavioral: baseline
Neural:     d = 0.04 stable            Neural:     increased activation
VLPFC:      low activation             VLPFC:      high activation
Result:     NEURAL EFFICIENCY          Result:     COMPENSATORY EFFORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The DCCS-VLPFC correlation r = -0.57 means better
executive function performance correlates with LOWER prefrontal
activation in trained individuals. Music training builds efficient
neural circuits that require fewer resources for the same output.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

MTNE provides a training-dependent efficiency framework that contextualizes other STU models:

1. **HMCE** (alpha1) provides hierarchical temporal context; MTNE explains why trained listeners encode that context with fewer neural resources.
2. **AMSC** (alpha2) describes auditory-motor coupling; MTNE predicts that trained individuals achieve stronger coupling with less prefrontal overhead.
3. **PTGMP** (gamma4) describes structural grey matter plasticity from piano training; MTNE captures the functional efficiency counterpart of that structural change.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MTNE Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 MTNE — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  EXECUTIVE FUNCTION DEMAND (e.g., inhibition task)                           ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        VENTROLATERAL PREFRONTAL CORTEX (VLPFC)                    │    ║
║  │        Primary efficiency site                                     │    ║
║  │        Trained: stable activation despite improved performance     │    ║
║  │        Untrained: increased activation for same output             │    ║
║  │        DCCS-VLPFC correlation: r = -0.57                          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Prefrontal control pathways                  ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        DORSOLATERAL PREFRONTAL CORTEX (DLPFC)                     │    ║
║  │        Working memory and task-switching support                    │    ║
║  │        Reduced recruitment in trained individuals                  │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        ANTERIOR CINGULATE CORTEX (ACC)                            │    ║
║  │        Conflict monitoring and error detection                     │    ║
║  │        More efficient conflict resolution in trained group         │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        SUPPLEMENTARY MOTOR AREA (SMA)                             │    ║
║  │        Motor planning and sequencing                               │    ║
║  │        Automatized sensorimotor routines in trained group          │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  EFFICIENCY: Better behavior (d=0.60) + stable activation (d=0.04)          ║
║  CORRELATION: DCCS performance ↔ VLPFC activation: r = -0.57               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Behavioral improvement (inhibition):   d = 0.60
Neural activation change:              d = 0.04 (essentially zero)
DCCS-VLPFC efficiency correlation:     r = -0.57
Interpretation: Trained brains do MORE with LESS prefrontal effort
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TMH → MTNE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MTNE COMPUTATION ARCHITECTURE                             ║
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
║  │  │pleasant   │ │amplitude│ │bright-  │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │stumpf     │ │loudness │ │ness     │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │sharpness│ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │           │ │flux     │ │roughness│ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         MTNE reads: 30D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Syllable ────┐ ┌── Beat ──────────┐ ┌── Section ────────┐ │        ║
║  │  │ 300ms (H8)     │ │ 700ms (H14)      │ │ 5000ms (H20)     │ │        ║
║  │  │                │ │                   │ │                    │ │        ║
║  │  │ Rapid exec.    │ │ Sustained exec.   │ │ Long-term         │ │        ║
║  │  │ function       │ │ function          │ │ efficiency        │ │        ║
║  │  └──────┬─────────┘ └──────┬────────────┘ └──────┬─────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         MTNE demand: ~16 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  TMH (30D)      │  Temporal Memory Hierarchy mechanism                   ║
║  │                 │                                                        ║
║  │ Short   [0:10] │  Rapid inhibition, onset-locked exec. function         ║
║  │ Medium  [10:20]│  Sustained task engagement, conflict monitoring         ║
║  │ Long    [20:30]│  Long-term efficiency, automatization tracking         ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MTNE MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_inhibition_gain,                       │        ║
║  │                       f02_neural_efficiency,                      │        ║
║  │                       f03_vlpfc_efficiency, f04_efficiency_ratio  │        ║
║  │  Layer M (Math):      efficiency_index, dissociation_score       │        ║
║  │  Layer P (Present):   exec_load, conflict_monitor                │        ║
║  │  Layer F (Future):    efficiency_predict, resource_forecast       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Moreno et al. (2011)** | fNIRS + behavioral | ~20 | Music training improves inhibition (DCCS task) | d = 0.60, p < 0.05 | **f01_inhibition_gain**: behavioral improvement |
| **Moreno et al. (2011)** | fNIRS | ~20 | Stable neural activation despite improved performance | d = 0.04 (NS) | **f02_neural_efficiency**: stable PFC |
| **Moreno et al. (2011)** | fNIRS + behavioral | ~20 | DCCS performance ↔ VLPFC activation negative correlation | r = -0.57, p < 0.05 | **f03_vlpfc_efficiency**: efficiency marker |

### 3.2 The Neural Efficiency Dissociation

```
BEHAVIORAL vs. NEURAL RESPONSE TO MUSIC TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Group           Behavioral    Neural (PFC)   Interpretation
────────────────────────────────────────────────────────────
Music-trained   d = +0.60     d = +0.04      EFFICIENT: More output,
                improved      stable          same neural cost

Control         baseline      increased      COMPENSATORY: Same output,
                              activation     more neural cost

DCCS-VLPFC correlation: r = -0.57
  Meaning: Higher DCCS score → lower VLPFC activation
  This is the signature of neural efficiency.

Note: The near-zero neural effect (d = 0.04) in the trained
group is the KEY finding. It means training does NOT increase
activation -- it OPTIMIZES it. The brain learns to do more
with less metabolic expenditure.
```

### 3.3 Effect Size Summary

```
Behavioral Effect:    d = 0.60 (inhibition improvement, Moreno et al. 2011)
Neural Effect:        d = 0.04 (stable activation — neural efficiency)
Efficiency Correlation: r = -0.57 (DCCS ↔ VLPFC, negative = efficient)
Quality Assessment:   γ-tier (speculative — single fNIRS study, moderate n)
Replication:          Converges with neural efficiency literature
                      (Neubauer & Fink 2009, Dunst et al. 2014)
                      but direct music-efficiency link needs replication
```

---

## 4. R³ Input Mapping: What MTNE Reads

### 4.1 R³ Feature Dependencies (30D of 49D)

| R³ Group | Index | Feature | MTNE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | pleasant | Hedonic processing load | Reward-efficiency coupling |
| **A: Consonance** | [1] | stumpf | Harmonic consonance | Tonal complexity as exec. demand |
| **B: Energy** | [7] | amplitude | Stimulus intensity | Processing resource demand |
| **B: Energy** | [8] | loudness | Perceptual intensity | Neural effort scaling |
| **B: Energy** | [9] | spectral_centroid | Spectral brightness | Spectral complexity proxy |
| **B: Energy** | [10] | spectral_flux | Information rate | Inhibition demand marker |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Executive switching demand |
| **C: Timbre** | [12] | brightness | Timbral clarity | Processing ease |
| **C: Timbre** | [16] | roughness | Sensory dissonance | Conflict monitoring load |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Rapid inhibition demand |
| **D: Change** | [22] | energy_change | Intensity dynamics | Sustained exec. effort |
| **D: Change** | [23] | pitch_change | Melodic dynamics | Task-switching proxy |
| **D: Change** | [24] | timbre_change | Timbral evolution | Stimulus novelty |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation x Perceptual coupling | Cross-domain exec. binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics x Perceptual coupling | Motor-perceptual exec. function |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
R³[11] onset_strength ───────────┼──► Rapid Executive Function
R³[21] spectral_change ──────────┘   TMH.short_context at H8 (300ms)
                                      Math: inhibit = σ(α · flux · onset ·
                                                        TMH.short[mean])

R³[7] amplitude ──────────────────┐
R³[8] loudness ───────────────────┤
R³[22] energy_change ─────────────┼──► Sustained Executive Function
R³[16] roughness ─────────────────┘   TMH.medium_context at H14 (700ms)
                                      Math: sustain = σ(β · energy ·
                                                        roughness · TMH.med)

R³[25:33] x_l0l5 (8D) ──────────┐
R³[33:41] x_l4l5 (8D) ──────────┼──► Long-term Efficiency
R³[0] pleasant ──────────────────┘   TMH.long_context at H20 (5000ms)
                                      Math: effic = σ(γ · x_coupling ·
                                                      autocorr · TMH.long)

DCCS-VLPFC link ──────────────────── Efficiency Ratio
                                      Better performance → lower activation
                                      Math: ratio = behavioral / neural_cost
                                      r = -0.57 (Moreno et al. 2011)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MTNE requires H³ features at three TMH horizons: H8 (300ms), H14 (700ms), H20 (5000ms).
These correspond to rapid inhibition → sustained executive engagement → long-term efficiency timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 8 | M1 (mean) | L0 (fwd) | Mean information rate (rapid) |
| 10 | spectral_flux | 8 | M8 (velocity) | L0 (fwd) | Change in information rate |
| 11 | onset_strength | 8 | M1 (mean) | L0 (fwd) | Mean onset rate (inhibition demand) |
| 21 | spectral_change | 8 | M3 (std) | L0 (fwd) | Spectral variability (exec. load) |
| 7 | amplitude | 14 | M1 (mean) | L0 (fwd) | Mean intensity over phrase |
| 8 | loudness | 14 | M1 (mean) | L0 (fwd) | Mean loudness over phrase |
| 8 | loudness | 14 | M18 (trend) | L0 (fwd) | Loudness trajectory |
| 16 | roughness | 14 | M1 (mean) | L0 (fwd) | Mean sensory dissonance |
| 22 | energy_change | 14 | M13 (entropy) | L0 (fwd) | Unpredictability of energy dynamics |
| 22 | energy_change | 14 | M11 (acceleration) | L0 (fwd) | Rate of energy change change |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term cross-domain coupling |
| 25 | x_l0l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Section-level self-similarity |
| 33 | x_l4l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term dynamics coupling |
| 33 | x_l4l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Long-range repetition detection |
| 0 | pleasant | 20 | M1 (mean) | L0 (fwd) | Long-term hedonic level |
| 0 | pleasant | 20 | M18 (trend) | L0 (fwd) | Hedonic trajectory |

**Total MTNE H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 TMH Mechanism Binding

MTNE reads from the **TMH** (Temporal Memory Hierarchy) mechanism:

| TMH Sub-section | Range | MTNE Role | Weight |
|-----------------|-------|-----------|--------|
| **Short Context** | TMH[0:10] | Rapid exec. function: inhibition onset, switching demand | **1.0** (primary) |
| **Medium Context** | TMH[10:20] | Sustained exec. function: conflict monitoring, effort tracking | **1.0** (primary) |
| **Long Context** | TMH[20:30] | Long-term efficiency: automatization, resource optimization | **1.0** (primary) |

MTNE does NOT read from BEP -- neural efficiency is about executive function and prefrontal resource allocation, not beat entrainment.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MTNE OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_inhibit_gain  │ [0, 1] │ Behavioral inhibition improvement (d=0.60).
    │                   │        │ Music-trained executive function gain.
    │                   │        │ f01 = σ(0.30 · flux_mean · onset_mean ·
    │                   │        │         TMH.short_mean + 0.25 · spec_std)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_neural_effic  │ [0, 1] │ Neural efficiency: stable PFC activation
    │                   │        │ despite improved behavioral output (d=0.04).
    │                   │        │ f02 = σ(0.25 · energy_mean · roughness_mean
    │                   │        │         · TMH.medium_mean
    │                   │        │         + 0.20 · loudness_trend)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_vlpfc_effic   │ [0, 1] │ VLPFC efficiency proxy (r=-0.57).
    │                   │        │ Lower activation = higher performance.
    │                   │        │ f03 = 1.0 - σ(0.30 · entropy_energy ·
    │                   │        │                loudness_mean
    │                   │        │                + 0.25 · energy_accel)
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_effic_ratio   │ [0, 1] │ Efficiency ratio: behavioral / neural cost.
    │                   │        │ High = more output per unit activation.
    │                   │        │ f04 = f01 · f03

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ efficiency_index  │ [0, 1] │ Weighted efficiency across timescales.
    │                   │        │ Longer timescales → stronger efficiency.
    │                   │        │ idx = (1·f01 + 2·f02 + 3·f03) / 6
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ dissociation_score│ [0, 1] │ Behavior-neural dissociation strength.
    │                   │        │ High behavior + low neural = high score.
    │                   │        │ score = f01 · (1 - (1 - f03))

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ exec_load         │ [0, 1] │ Current executive function load.
    │                   │        │ TMH.short_context aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ conflict_monitor  │ [0, 1] │ Current conflict monitoring level (ACC).
    │                   │        │ TMH.medium_context + roughness features.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ efficiency_predict│ [0, 1] │ Predicted efficiency for upcoming segment.
    │                   │        │ Autocorrelation-based efficiency forecast.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ resource_forecast │ [0, 1] │ Predicted neural resource demand.
    │                   │        │ Trend + entropy-driven cost estimate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
MANIFOLD RANGE: STU MTNE [219:229]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Neural Efficiency Function

```
Neural Efficiency Model:

    Efficiency = Behavioral_Performance / Neural_Cost

    For Music-Trained:
      Behavioral:   d = 0.60 (improved inhibition on DCCS)
      Neural:       d = 0.04 (stable VLPFC activation)
      Efficiency:   HIGH (0.60 / ~0.04 ≈ 15× ratio)

    For Controls:
      Behavioral:   baseline (no improvement)
      Neural:       increased activation (compensatory)
      Efficiency:   LOW (0 / increased → near zero)

    DCCS-VLPFC Relationship:
      Activation(VLPFC) = α · (1 / Performance) + β
      r = -0.57: inverse relationship (efficiency signature)

    Sigmoid Saturation Rule:
      All σ(Σ wᵢ · gᵢ) formulas have |wᵢ| summing ≤ 1.0
```

### 7.2 Feature Formulas

```python
# f01: Inhibition Gain (d = 0.60 behavioral improvement)
flux_mean = h3[(10, 8, 1, 0)]        # spectral_flux mean at H8
onset_mean = h3[(11, 8, 1, 0)]       # onset_strength mean at H8
spec_std = h3[(21, 8, 3, 0)]         # spectral_change std at H8
f01 = σ(0.30 · flux_mean · onset_mean
         · mean(TMH.short_context[0:10])
         + 0.25 · spec_std)
# |0.30| + |0.25| = 0.55 ≤ 1.0 ✓

# f02: Neural Efficiency (d = 0.04 stable activation)
energy_mean = h3[(7, 14, 1, 0)]      # amplitude mean at H14
roughness_mean = h3[(16, 14, 1, 0)]  # roughness mean at H14
loudness_trend = h3[(8, 14, 18, 0)]  # loudness trend at H14
f02 = σ(0.25 · energy_mean · roughness_mean
         · mean(TMH.medium_context[10:20])
         + 0.20 · loudness_trend)
# |0.25| + |0.20| = 0.45 ≤ 1.0 ✓

# f03: VLPFC Efficiency (r = -0.57, inverted)
entropy_energy = h3[(22, 14, 13, 0)] # energy_change entropy at H14
loudness_mean = h3[(8, 14, 1, 0)]    # loudness mean at H14
energy_accel = h3[(22, 14, 11, 0)]   # energy_change acceleration at H14
f03 = 1.0 - σ(0.30 · entropy_energy · loudness_mean
                + 0.25 · energy_accel)
# |0.30| + |0.25| = 0.55 ≤ 1.0 ✓
# Inverted: high complexity → high activation → LOW efficiency

# f04: Efficiency Ratio (behavioral × VLPFC efficiency)
f04 = f01 · f03
# Multiplicative: both must be high for high efficiency
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MTNE Function |
|--------|-----------------|----------|---------------|---------------|
| **VLPFC** | ±48, 28, 4 | Direct | fNIRS | Primary efficiency site (r = -0.57) |
| **DLPFC** | ±44, 36, 24 | Direct | fNIRS | Working memory support, reduced in trained |
| **ACC** | 0, 24, 34 | Indirect | Literature | Conflict monitoring and error detection |
| **SMA** | 0, -6, 58 | Indirect | Literature | Automatized sensorimotor routines |

---

## 9. Cross-Unit Pathways

### 9.1 MTNE ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MTNE INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  HMCE.context_depth ──────► MTNE (deeper context → more efficient)         │
│  MTNE.efficiency_index ───► AMSC (efficiency modulates motor coupling)     │
│  PTGMP.grey_matter ───────► MTNE (structural plasticity → functional       │
│                                    efficiency, gamma4 → gamma3 link)       │
│                                                                             │
│  CROSS-UNIT (P4: STU internal):                                            │
│  TMH.context_depth ↔ MTNE.efficiency_index                                │
│  Longer temporal context → more efficient processing                       │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  MTNE.exec_load ──────► ARU (executive load → emotional regulation)        │
│  Lower exec. load in trained → more resources for affective processing     │
│                                                                             │
│  CROSS-UNIT (P6: STU → IMU):                                              │
│  MTNE.neural_efficiency ──► IMU (efficiency → memory encoding quality)     │
│  Efficient PFC → better integration of musical structure into memory       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Increased PFC in trained** | If music training INCREASES PFC activation proportionally to behavioral gain, the efficiency model is wrong | Testable |
| **No behavioral gain** | If music training shows no executive function improvement (d < 0.20), the behavioral side of efficiency fails | Testable |
| **Positive DCCS-VLPFC correlation** | If higher DCCS performance correlates with HIGHER VLPFC activation (r > 0), the efficiency signature is absent | Testable |
| **Behavioral improvement with stable neural** | Trained group should show d > 0.30 behavioral + d < 0.15 neural simultaneously | **Partially confirmed**: d = 0.60 + d = 0.04 |
| **Negative efficiency correlation** | DCCS ↔ VLPFC should be negative (r < 0) in trained group | **Partially confirmed**: r = -0.57 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MTNE(BaseModel):
    """Music Training Neural Efficiency.

    Output: 10D per frame.
    Reads: TMH mechanism (30D), R³ direct.
    Zero learned parameters — all deterministic.
    """
    NAME = "MTNE"
    UNIT = "STU"
    TIER = "γ3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TMH",)        # Primary mechanism

    # Coefficient saturation rule: |wᵢ| must sum ≤ 1.0 per sigmoid
    ALPHA_1 = 0.30   # Inhibition: flux × onset × TMH weight
    ALPHA_2 = 0.25   # Inhibition: spectral std weight
    BETA_1 = 0.25    # Efficiency: energy × roughness × TMH weight
    BETA_2 = 0.20    # Efficiency: loudness trend weight
    GAMMA_1 = 0.30   # VLPFC: entropy × loudness weight
    GAMMA_2 = 0.25   # VLPFC: energy acceleration weight

    # Moreno et al. 2011 effect sizes
    BEHAVIORAL_D = 0.60  # Inhibition improvement
    NEURAL_D = 0.04      # Stable activation (efficiency)
    DCCS_VLPFC_R = -0.57 # Efficiency correlation

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for MTNE computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Rapid executive function (H8 = 300ms)
            (10, 8, 1, 0),    # spectral_flux, mean, forward
            (10, 8, 8, 0),    # spectral_flux, velocity, forward
            (11, 8, 1, 0),    # onset_strength, mean, forward
            (21, 8, 3, 0),    # spectral_change, std, forward
            # Sustained executive function (H14 = 700ms)
            (7, 14, 1, 0),    # amplitude, mean, forward
            (8, 14, 1, 0),    # loudness, mean, forward
            (8, 14, 18, 0),   # loudness, trend, forward
            (16, 14, 1, 0),   # roughness, mean, forward
            (22, 14, 13, 0),  # energy_change, entropy, forward
            (22, 14, 11, 0),  # energy_change, acceleration, forward
            # Long-term efficiency (H20 = 5000ms)
            (25, 20, 1, 0),   # x_l0l5[0], mean, forward
            (25, 20, 22, 0),  # x_l0l5[0], autocorrelation, forward
            (33, 20, 1, 0),   # x_l4l5[0], mean, forward
            (33, 20, 22, 0),  # x_l4l5[0], autocorrelation, forward
            (0, 20, 1, 0),    # pleasant, mean, forward
            (0, 20, 18, 0),   # pleasant, trend, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MTNE 10D output.

        Args:
            mechanism_outputs: {"TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) MTNE output
        """
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short context
        tmh_medium = tmh[..., 10:20]      # medium context
        tmh_long = tmh[..., 20:30]        # long context

        # ═══ LAYER E: Explicit features ═══

        # f01: Inhibition Gain (d = 0.60 behavioral improvement)
        flux_mean = h3_direct[(10, 8, 1, 0)].unsqueeze(-1)
        onset_mean = h3_direct[(11, 8, 1, 0)].unsqueeze(-1)
        spec_std = h3_direct[(21, 8, 3, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(
            self.ALPHA_1 * flux_mean * onset_mean
            * tmh_short.mean(-1, keepdim=True)
            + self.ALPHA_2 * spec_std
        )  # |0.30| + |0.25| = 0.55 ≤ 1.0 ✓

        # f02: Neural Efficiency (d = 0.04 stable activation)
        energy_mean = h3_direct[(7, 14, 1, 0)].unsqueeze(-1)
        roughness_mean = h3_direct[(16, 14, 1, 0)].unsqueeze(-1)
        loudness_trend = h3_direct[(8, 14, 18, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(
            self.BETA_1 * energy_mean * roughness_mean
            * tmh_medium.mean(-1, keepdim=True)
            + self.BETA_2 * loudness_trend
        )  # |0.25| + |0.20| = 0.45 ≤ 1.0 ✓

        # f03: VLPFC Efficiency (r = -0.57, inverted)
        entropy_energy = h3_direct[(22, 14, 13, 0)].unsqueeze(-1)
        loudness_mean = h3_direct[(8, 14, 1, 0)].unsqueeze(-1)
        energy_accel = h3_direct[(22, 14, 11, 0)].unsqueeze(-1)
        f03 = 1.0 - torch.sigmoid(
            self.GAMMA_1 * entropy_energy * loudness_mean
            + self.GAMMA_2 * energy_accel
        )  # |0.30| + |0.25| = 0.55 ≤ 1.0 ✓
        # Inverted: high complexity → high activation → LOW efficiency

        # f04: Efficiency Ratio (behavioral × VLPFC efficiency)
        f04 = f01 * f03

        # ═══ LAYER M: Mathematical ═══
        efficiency_index = (1 * f01 + 2 * f02 + 3 * f03) / 6
        dissociation_score = f01 * f03  # same as f04 by definition

        # ═══ LAYER P: Present ═══
        exec_load = tmh_short.mean(-1, keepdim=True)
        conflict_monitor = torch.sigmoid(
            0.50 * tmh_medium.mean(-1, keepdim=True)
            + 0.50 * roughness_mean
        )  # |0.50| + |0.50| = 1.0 ≤ 1.0 ✓

        # ═══ LAYER F: Future ═══
        autocorr_x = h3_direct[(25, 20, 22, 0)].unsqueeze(-1)
        autocorr_d = h3_direct[(33, 20, 22, 0)].unsqueeze(-1)
        efficiency_predict = torch.sigmoid(
            0.35 * autocorr_x + 0.35 * autocorr_d
            + 0.30 * tmh_long.mean(-1, keepdim=True)
        )  # |0.35| + |0.35| + |0.30| = 1.0 ≤ 1.0 ✓

        pleasant_trend = h3_direct[(0, 20, 18, 0)].unsqueeze(-1)
        resource_forecast = torch.sigmoid(
            0.40 * entropy_energy + 0.30 * energy_accel
            + 0.30 * pleasant_trend
        )  # |0.40| + |0.30| + |0.30| = 1.0 ≤ 1.0 ✓

        return torch.cat([
            f01, f02, f03, f04,                                   # E: 4D
            efficiency_index, dissociation_score,                  # M: 2D
            exec_load, conflict_monitor,                           # P: 2D
            efficiency_predict, resource_forecast,                 # F: 2D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Moreno et al. 2011 (fNIRS) |
| **Effect Sizes** | d = 0.60 (behavioral), d = 0.04 (neural), r = -0.57 | Moreno et al. 2011 |
| **Evidence Modality** | fNIRS, behavioral (DCCS) | Indirect neural |
| **Falsification Tests** | 2/5 partially confirmed | Low-moderate validity |
| **R³ Features Used** | 30D of 49D | All groups (Consonance + Energy + Timbre + Change + Interactions) |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **TMH Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure (E4 + M2 + P2 + F2) |

---

## 13. Scientific References

1. **Moreno, S., et al. (2011)**. Short-term music training enhances verbal intelligence and executive function. *Psychological Science*. (fNIRS + behavioral, DCCS task, ~20 participants, music vs. visual arts training)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L5, L6, L9, L4, X_L4L5, X_L5L9 | R³ (49D): Consonance, Energy, Timbre, Change, Interactions |
| Temporal | HC⁰ mechanisms (OSC, ATT, ITM, EFC) | TMH mechanism (30D) |
| Efficiency proxy | X_L5L9 [224:232] (Perceptual x Statistics) | H³ morphs at H14 + inverted sigmoid |
| Inhibition proxy | X_L4L5 [192:200] (Derivatives x Perceptual) | TMH.short_context + R³ flux/onset/change |
| Statistics | S⁰.L9 entropy [116:120], kurtosis [120:124] | H³ M13 (entropy), M11 (acceleration), M3 (std) |
| Demand format | HC⁰ index ranges (27 tuples, 1.17%) | H³ 4-tuples (16 tuples, 0.69%) |
| Output dimensions | 11D | **10D** (catalog value supersedes legacy) |
| VLPFC efficiency | Inferred from X_L5L9 stability | Explicit inverted sigmoid: f03 = 1 - σ(...) |

### Why TMH replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, ATT, ITM, EFC). In MI, these are unified into the TMH mechanism with 3 sub-sections:
- **OSC + ATT → TMH.short_context** [0:10]: Neural oscillation coupling and attentional gating → rapid executive function (inhibition onset, task-switching demand)
- **ITM → TMH.medium_context** [10:20]: Interval timing mechanism → sustained executive engagement (conflict monitoring, effort tracking over phrases)
- **EFC → TMH.long_context** [20:30]: Efference copy / forward model → long-term efficiency tracking (automatization, resource optimization across sections)

### Key Semantic Differences

1. **Neural efficiency**: D0 inferred efficiency from X_L5L9 stability (trained subjects showed stable X_L5L9 while controls increased). MI explicitly models efficiency via an inverted sigmoid on complexity features -- high complexity maps to high activation need, and the inversion produces the efficiency signal (lower = more efficient).
2. **Output reduction 11D → 10D**: The catalog specifies 10D for MTNE. The legacy 11D included a separate `control_compensation` feature; in MI, this is implicitly captured by the inverted f03 (low f03 = high activation = compensatory).
3. **Demand reduction 27 → 16 tuples**: D0 used 5 different event horizons (25ms to 1000ms) across 4 mechanisms. MI consolidates to 3 TMH horizons (300ms, 700ms, 5000ms) with targeted morphs, reducing sparsity from 1.17% to 0.69%.
4. **Hedonic input**: MI adds R³ pleasant (consonance) as a long-term input, reflecting the reward-efficiency coupling hypothesis: positive hedonic experience may facilitate more efficient neural processing.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
