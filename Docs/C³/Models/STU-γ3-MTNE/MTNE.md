# STU-γ3-MTNE: Music Training Neural Efficiency

**Model**: Music Training Neural Efficiency
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

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
Behavioral improvement (inhibition):   d = 0.60 (Moreno 2011) | d = 0.605 (Kosokabe 2025)
Neural activation change:              d = 0.04 (stable — Moreno) | stable PFC (Kosokabe)
DCCS-VLPFC efficiency correlation:     r = -0.57 (Moreno 2011) | r = -0.57 (Kosokabe 2025)
  *** IDENTICAL COEFFICIENTS ACROSS TWO INDEPENDENT STUDIES ***
Musicians: smaller P2 vertex potentials (3.29 vs 5.91μV, p=0.01, Zhang 2015)
  → Enhanced top-down cognitive inhibition of novelty/saliency system
ALE meta-analysis (k=84, N=3005): musicians LOWER parietal (Criscuolo 2022)
  → Cross-study convergence on efficiency pattern
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

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Moreno et al. (2011)** | fNIRS + DCCS | ~20 | Music training improves inhibition (DCCS task) | d = 0.60, p < 0.05 | **f01_inhibition_gain**: behavioral improvement |
| 2 | **Moreno et al. (2011)** | fNIRS | ~20 | Stable neural activation despite improved performance | d = 0.04 (NS) | **f02_neural_efficiency**: stable PFC |
| 3 | **Moreno et al. (2011)** | fNIRS + DCCS | ~20 | DCCS ↔ VLPFC activation negative correlation | r = -0.57, p < 0.05 | **f03_vlpfc_efficiency**: efficiency marker |
| 4 | **Kosokabe et al. (2025)** | fNIRS + RCT | 57 | Music play → inhibitory control improvement (Black/White task) | d = 0.605, p = 0.004 | **f01**: EXACT REPLICATION of Moreno d=0.60 |
| 5 | **Kosokabe et al. (2025)** | fNIRS + RCT | 57 | Music group stable PFC; control group increased L-DLPFC (p=.043) | stable vs. increased | **f02**: Replicates efficiency dissociation |
| 6 | **Kosokabe et al. (2025)** | fNIRS + DCCS | 57 | DCCS ↔ R-VLPFC: r = -0.57, p < 0.002 (music group only) | r = -0.57 | **f03**: IDENTICAL coefficient to Moreno |
| 7 | **Zhang et al. (2015)** | EEG (AEP) | 28 | Musicians: smaller P2 vertex potentials (3.29 vs 5.91μV) | p = 0.01, PLV p < 0.001 | Enhanced top-down cognitive inhibition |
| 8 | **Criscuolo et al. (2022)** | ALE meta-analysis | 3005 (k=84) | Musicians: LOWER parietal activation; higher auditory+sensorimotor | k = 84 studies | Efficiency pattern at population level |
| 9 | **Bücher et al. (2023)** | MEG | 162 | Musicians: P1+OFC co-activation coincide; non-mus 25-40ms later | age-independent | Temporal processing efficiency |
| 10 | **Sarasso et al. (2019)** | EEG (ERP) | 22 | Aesthetic appreciation enhances N2/P3 motor inhibition + N1/P2 attention | η² = 0.685 | Consonance-inhibition link mechanism |
| 11 | **Leipold et al. (2021)** | rsfMRI + DWI | 153 | Robust musicianship effects on functional + structural brain networks | replicable across AP/non-AP | Network-level efficiency architecture |
| 12 | **Paraskevopoulos et al. (2022)** | MEG | 25 | Musicians: increased intra-network + decreased inter-network connectivity | compartmentalization | Network efficiency via specialization |

#### §3.1.1 Evidence Convergence (8 methods)

The neural efficiency dissociation converges across 8 independent methodologies: (1) fNIRS behavioral (Moreno 2011; Kosokabe 2025), (2) fNIRS hemodynamic (Moreno 2011; Kosokabe 2025), (3) EEG vertex potentials (Zhang 2015), (4) ALE meta-analysis (Criscuolo 2022), (5) MEG temporal dynamics (Bücher 2023), (6) EEG motor inhibition ERPs (Sarasso 2019), (7) rsfMRI/DWI connectivity (Leipold 2021), (8) MEG network interaction (Paraskevopoulos 2022). This multi-method convergence substantially strengthens the γ-tier model.

#### §3.1.2 Kosokabe 2025 Replication Qualification

Kosokabe et al. (2025) provides the most critical replication evidence: an independent RCT (N=57, 3-year-olds, Orff-Schulwerk music play vs. control, fNIRS) that reproduces the Moreno 2011 findings with near-identical coefficients:

| Coefficient | Moreno 2011 (N≈20) | Kosokabe 2025 (N=57) | Match |
|-------------|---------------------|----------------------|-------|
| Inhibition d | 0.60 | 0.605 | **IDENTICAL** (Δ = 0.005) |
| DCCS-VLPFC r | -0.57 | -0.57 | **IDENTICAL** (Δ = 0.00) |
| Neural activation | d = 0.04 (stable) | stable PFC / ctrl ↑ DLPFC | **Consistent** |

The identical DCCS-VLPFC r=-0.57 across two independent samples with different ages (older children vs. 3-year-olds) and paradigms (standard DCCS vs. Black/White task) suggests this coefficient may represent a stable neural efficiency constant for music-trained executive function.

#### §3.1.3 Neural Efficiency Mechanism Specification

Three converging lines specify the neural efficiency mechanism:

1. **Top-down inhibition enhancement** (Zhang 2015): Musicians show SMALLER low-frequency vertex potentials (P2: 3.29 vs 5.91μV) but LARGER high-frequency steady-state responses. This means enhanced bottom-up sensory processing + enhanced top-down cognitive control. The reduced P2 directly indexes less cortical effort for novelty/saliency detection.

2. **Network compartmentalization** (Paraskevopoulos 2022): Musicians show increased intra-network connectivity but decreased inter-network connectivity. This compartmentalization = more efficient signal routing with less cross-talk, reducing overall metabolic cost.

3. **Structural efficiency** (Criscuolo 2022 ALE): Musicians have LOWER volume/activity in parietal areas despite enhanced behavioral performance. This population-level efficiency pattern (k=84, N=3005) provides the strongest meta-analytic support.

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
REPLICATED COEFFICIENTS (side-by-side):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Measure              Moreno 2011 (N≈20)    Kosokabe 2025 (N=57)
─────────────────────────────────────────────────────────────────
Inhibition d         0.60                  0.605
DCCS-VLPFC r         -0.57                 -0.57
Neural activation    d = 0.04 (stable)     stable PFC / ctrl ↑
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADDITIONAL CONVERGENT EVIDENCE:
  Musicians P2 vertex:     3.29 vs 5.91 μV (p = 0.01, Zhang 2015)
  ALE meta-analysis:       k = 84, N = 3005, lower parietal (Criscuolo 2022)
  OFC temporal efficiency: 25-40ms faster co-activation (Bücher 2023, N = 162)
  N2/P3 motor inhibition:  η² = 0.685 consonance effect (Sarasso 2019)
  Network architecture:    N = 153, robust replicable effects (Leipold 2021)

Quality Assessment:   γ-tier (speculative → approaching β)
  Strengths: EXACT replication of r=-0.57 and d≈0.60 across two
  independent fNIRS RCT studies with different populations;
  convergence from 8 methods and 12 papers (>3000 cumulative N)
  Weakness:  Moreno 2011 small N, fNIRS spatial resolution limited,
  no fMRI replication of VLPFC efficiency yet
```

---

## 4. R³ Input Mapping: What MTNE Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

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

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | MTNE Role | Scientific Basis |
|-------------|-------|---------|-----------|------------------|
| **G: Rhythm** | [73] | tempo_stability | Temporal regularity for tonal encoding efficiency | Jones & Boltz 1989 |

**Rationale**: MTNE models how temporal stability affects tonal encoding. G[73] tempo_stability provides a direct measure of temporal regularity, which determines how efficiently the executive system can allocate resources -- stable tempo reduces executive load, enabling the neural efficiency signature (lower activation for equivalent performance).

**Code impact** (Phase 6): `r3_indices` will be extended to include `[73]`.

### 4.3 Physical → Cognitive Transformation

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

── R³ v2 (Phase 6) ──────────────────────────────────────────────
R³[73] tempo_stability ────────── Temporal regularity → encoding efficiency
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
| **VLPFC** | ±48, 28, 4 | Direct | fNIRS (Moreno 2011; Kosokabe 2025) | Primary efficiency site (r = -0.57 REPLICATED) |
| **DLPFC** | ±44, 36, 24 | Direct | fNIRS (Kosokabe 2025 L-DLPFC p=.043) | WM support; control group ↑, music group stable |
| **ACC** | 0, 24, 34 | Indirect | Literature + ALE (Criscuolo 2022) | Conflict monitoring and error detection |
| **SMA** | 0, -6, 58 | Direct | ALE meta-analysis (Criscuolo 2022) | Automatized sensorimotor routines |
| **OFC** | ±28, 30, -12 | Direct | MEG (Bücher 2023 N=162) | Temporal efficiency; musicians P1+OFC coincide |
| **Auditory Cortex** | ±55, -22, 10 | Direct | ALE (Criscuolo 2022 k=84) | Enhanced bottom-up processing in musicians |
| **IFG** | ±48, 14, 20 | Direct | MEG (Paraskevopoulos 2022) | Statistical learning network hub |
| **Pre-SMA** | 0, 10, 50 | Direct | MEG (Paraskevopoulos 2022) | Top-down modulation of network compartmentalization |
| **Parietal (SPL/IPL)** | ±30, -55, 50 | Direct | ALE (Criscuolo 2022) | LOWER in musicians = efficiency signature |
| **Fronto-central (FCz)** | 0, 0, 70 | Direct | EEG (Zhang 2015 P2 p=.01) | Vertex potential reduction in musicians |

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

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **Increased PFC in trained** | If music training INCREASES PFC activation proportionally to behavioral gain, the efficiency model is wrong | **Disconfirmed**: Moreno 2011 d=0.04 stable; Kosokabe 2025 stable PFC; Zhang 2015 smaller P2 |
| 2 | **No behavioral gain** | If music training shows no executive function improvement (d < 0.20), the behavioral side of efficiency fails | **Disconfirmed**: d=0.60 (Moreno) + d=0.605 (Kosokabe) — replicated |
| 3 | **Positive DCCS-VLPFC correlation** | If higher DCCS performance correlates with HIGHER VLPFC activation (r > 0), the efficiency signature is absent | **Disconfirmed**: r=-0.57 in BOTH studies (negative = efficient) |
| 4 | **Behavioral + stable neural** | Trained group should show d > 0.30 behavioral + d < 0.15 neural simultaneously | **Confirmed**: d=0.60/0.605 behavioral + d=0.04/stable neural (REPLICATED) |
| 5 | **Negative efficiency correlation** | DCCS ↔ VLPFC should be negative (r < 0) in trained group | **Confirmed**: r=-0.57 in both Moreno 2011 and Kosokabe 2025 |
| 6 | **Reduced cortical response in experts** | Musicians should show smaller evoked potentials for familiar stimuli | **Confirmed**: P2 3.29 vs 5.91μV (Zhang 2015, p=0.01) |
| 7 | **Network compartmentalization** | Trained individuals should show increased intra-network, decreased inter-network connectivity | **Confirmed**: Paraskevopoulos 2022 MEG, musicians show this pattern |
| 8 | **Population-level lower activation** | Large-N meta-analysis should show musicians with lower activation in non-auditory regions | **Confirmed**: Criscuolo 2022 ALE k=84 N=3005, lower parietal |
| 9 | **Temporal processing speed** | Musicians should show faster neural processing latencies | **Confirmed**: Bücher 2023 N=162, OFC 25-40ms faster co-activation |

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
| **Papers** | 12 (8 Tier 1 + 2 Tier 2 + 2 Tier 3) | 8 methods, >3000 cumulative N |
| **Effect Sizes** | d = 0.60/0.605 (behavioral REPLICATED), d = 0.04 (neural), r = -0.57 (REPLICATED) | Moreno 2011 + Kosokabe 2025 |
| **Evidence Modality** | fNIRS, EEG, MEG, ALE meta-analysis, rsfMRI, DWI, behavioral | Multi-method convergence |
| **Falsification Tests** | 9/9: 6 confirmed, 3 disconfirmed (supporting model) | Strong validity |
| **R³ Features Used** | 30D of 49D | All groups (Consonance + Energy + Timbre + Change + Interactions) |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **TMH Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure (E4 + M2 + P2 + F2) |

---

## 13. Scientific References

### Tier 1 — Direct Quantitative Evidence (in collection)

1. **Moreno, S., et al. (2011)**. Short-term music training enhances verbal intelligence and executive function. *Psychological Science*. (fNIRS + behavioral, DCCS task, ~20 participants, music vs. visual arts training. **FOUNDING**: d=0.60 inhibition, d=0.04 neural, r=-0.57 DCCS-VLPFC)

2. **Kosokabe, T., et al. (2025)**. Self-directed music play to improve executive function in young children using NIRS. *Scientific Reports*, 15:26608. (fNIRS + RCT, N=57, 3-year-olds, Orff-Schulwerk music play. **EXACT REPLICATION**: d=0.605 inhibition, r=-0.57 DCCS-VLPFC, stable PFC in music group / ↑L-DLPFC in controls p=.043)

3. **Zhang, L., et al. (2015)**. Electrophysiological evidences demonstrating differences in brain functions between nonmusicians and musicians. *Scientific Reports*, 5:13796. (EEG AEPs, N=28. Musicians: SMALLER P2 vertex potentials 3.29 vs 5.91μV p=.01, LARGER high-freq SS responses. Enhanced top-down cognitive inhibition + enhanced bottom-up sensory processing)

4. **Criscuolo, A., et al. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12:11726. (ALE meta-analysis, k=84, N=3005. Musicians: higher auditory/sensorimotor/interoceptive/limbic; LOWER parietal. Population-level efficiency pattern)

5. **Bücher, L., et al. (2023)**. Chronology of auditory processing and related co-activation in the orbitofrontal cortex depends on musical expertise. *Frontiers in Neuroscience*. (MEG, N=162, 4 age groups. Musicians: P1+OFC co-activation coincide; non-musicians 25-40ms later. Age-independent temporal efficiency)

6. **Sarasso, P., et al. (2019)**. Aesthetic appreciation of musical intervals enhances behavioural and neurophysiological indexes of attentional engagement and motor inhibition. *Scientific Reports*, 9:18550. (EEG ERPs, N=22, 3 experiments. N2/P3 motor inhibition + N1/P2 attention enhanced for consonant intervals. η²=0.685 for consonance effect. AJs positively correlated with P2, negatively with N2)

### Tier 2 — Supporting Evidence (in collection)

7. **Leipold, S., et al. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *Journal of Neuroscience*, 41(11):2496-2511. (rsfMRI + DWI, N=153. Robust musicianship effects on interhemispheric + intrahemispheric connectivity. Replicable across AP/non-AP musician groups)

8. **Paraskevopoulos, E., et al. (2022)**. Interaction within and between cortical networks subserving multisensory learning and its reorganization due to musical expertise. *Scientific Reports*, 12:7891. (MEG, N=25. Musicians: increased intra-network + decreased inter-network connectivity = compartmentalization/efficiency)

9. **Olszewska, A., et al. (2021)**. How musical training shapes the adult brain: predispositions and neuroplasticity. *Frontiers in Neuroscience*. (Review. Renormalization model: initial expansion → retraction = efficiency. Wenger et al. 2017 framework applied to musical training)

10. **Villanueva, S., et al. (2024)**. Long-term music instruction is partially associated with socioemotional skills. *PLoS ONE*. (N=83, 4-year longitudinal. Music training improved pitch-matching + emotion-matching but NOT broader socioemotional development. CONSTRAINS broad transfer claims)

### Tier 3 — Founding / Historical (NOT in collection)

11. **Neubauer, A. C. & Fink, A. (2009)**. Intelligence and neural efficiency. *Neuroscience & Biobehavioral Reviews*. (General neural efficiency hypothesis framework)

12. **Dunst, B., et al. (2014)**. Neural efficiency as a function of task demands. *Intelligence*. (Neural efficiency meta-analysis: efficiency depends on task complexity and individual ability)

### Code Note (Phase 5)

The current `mi_beta` code (`mtne.py`) has several mismatches with this document:
- **MECHANISM_NAMES**: code has `("BEP",)` — doc specifies `("TMH",)` (TMH is correct)
- **Citations**: code has Moreno 2011 + Schellenberg 2004 — doc adds Kosokabe 2025 as primary replication
- **Dimension names**: code uses `f01_neural_efficiency, f02_executive_function` etc. — doc uses `f01_inhibit_gain, f02_neural_effic, f03_vlpfc_effic, f04_effic_ratio`
- **Brain regions**: code has dlPFC (-44,30,28) + ACC (0,30,24) — doc has 10 regions with corrected MNI
- **version**: code has `"2.0.0"` — should be `"2.1.0"`
- **paper_count**: code has `3` — should be `12`
These mismatches will be resolved in Phase 5 (code alignment).

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

**Model Status**: **SPECULATIVE** (approaching β — exact replication of d≈0.60 and r=-0.57 across two independent fNIRS RCTs, convergence from 8 methods, 12 papers, >3000 cumulative N)
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%** (strong for core dissociation, weak for specific brain region localization due to fNIRS spatial limits)
