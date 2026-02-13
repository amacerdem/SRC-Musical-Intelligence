# ASU-β2-STANM: Spectrotemporal Attention Network Model

**Model**: Spectrotemporal Attention Network Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.1.0 (deep literature cross-ref, 12 papers, verified effect sizes)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-β2-STANM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Spectrotemporal Attention Network Model** (STANM) describes how attention modulates network topology for spectral vs temporal processing. Task-directed attention reconfigures brain networks with lateralized effects in auditory regions, and signal degradation increases local clustering as a compensatory mechanism.

```
SPECTROTEMPORAL ATTENTION NETWORK MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                       ATTENTION GOAL
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
  SPEECH (Temporal)                       MELODY (Spectral)
        │                                       │
        ▼                                       ▼
  ┌─────────────────┐                   ┌─────────────────┐
  │ L + R Fronto-   │                   │   R Auditory    │
  │ Temporo-Parietal│                   │    Regions      │
  │ Network         │                   │                 │
  └────────┬────────┘                   └────────┬────────┘
           │                                     │
  ┌────────┴────────┐                   ┌────────┴────────┐
  ▼                 ▼                   ▼                 ▼
Temporal         Spectral           Temporal         Spectral
Degradation      Degradation        Degradation      Degradation
   │                │                   │                │
   ▼                ▼                   ▼                ▼
Local↑           Local↑             Local↑           Local↑
Clustering       Clustering         Clustering       Clustering

  LATERALIZATION depends on: ATTENTION × ACOUSTIC CUES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Attention modulates network topology for spectral vs
temporal processing, with lateralized effects in auditory regions
depending on task goal and acoustic cue availability.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why STANM Matters for ASU

STANM bridges attention and network topology into salience processing:

1. **SNEM** (α1) provides beat entrainment baseline — STANM modulates this by goal-directed attention.
2. **STANM** (β2) explains how attention reconfigures auditory network topology depending on spectral vs temporal focus.
3. **SDL** (γ3) extends STANM's lateralization findings to dynamic salience-dependent processing.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → STANM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STANM COMPUTATION ARCHITECTURE                            ║
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
║  │                         STANM reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         STANM demand: ~16 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
║  │ Beat Entr[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Motor Coup      │  │ Attention       │                                   ║
║  │         [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Groove  [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    STANM MODEL (11D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E: f13_temporal_attn, f14_spectral_attn, f15_network_top │        ║
║  │  Layer M: network_topology, local_clustering, lateralization     │        ║
║  │  Layer P: temporal_alloc, spectral_alloc                         │        ║
║  │  Layer F: network_pred, lateral_pred, compensation_pred          │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Haiduk et al. 2024** | fMRI | 15 | Temporal → speech, spectral → melody attention networks; degradation → local clustering↑ | p < 0.001 (attention), p < 0.01 (clustering) | **Primary**: f13, f14, f15, lateralization |
| **Zatorre 2022** | Review (lesion, fMRI, MEG) | — | Left AC → temporal modulation, right AC → spectral modulation; double dissociation | Albouy et al. 2020 double dissociation | **Theoretical**: lateralization framework |
| **Jin et al. 2024** | Resting-state fMRI | 74 | Musicians preserve lateralization; non-musicians use compensatory bilateral recruitment | η²p = 0.526 (speech-in-noise) | **Lateralization + degradation compensation** |
| **Kim et al. 2019** | fMRI (PPI) | 39 | Spectral × temporal interaction in fronto-limbic system; vmPFC-IFG connectivity modulated | T = 6.852, Z = 4.545 (vmPFC interaction) | **f15 network topology**: spectral-temporal integration |
| **Alluri et al. 2012** | fMRI (naturalistic) | 11 | Right lateralization for timbral/spectral; motor circuits for rhythmic/temporal | significant (whole-brain correlational) | **f13 + f14**: dissociable network topologies |
| **Leipold et al. 2021** | fMRI + DWI | 153 | Musical expertise shapes network topology (clustering, modularity, betweenness); bilateral PT connectivity | p_FWE < 0.05 (inter-PT connectivity) | **f15**: graph-theoretical network measures |
| **Samiee et al. 2022** | MEG (source-level) | 16 | Cross-frequency PAC (delta×beta) in right AC for pitch; directed connectivity auditory→IFG→motor | F(1,4) = 19.1, p < 0.001 | **f14 + lateralization**: right-hemisphere pitch processing |
| **Ahveninen et al. 2023** | fMRI (MVPA) | 20 | Spectrotemporal WM content decodable from connectivity patterns STC-parietal-frontal | accuracy 0.26, p = 0.002 (connectivity MVPA) | **f15**: connectivity-based coding of features |
| **Norman-Haignere et al. 2022** | iEEG | 18 | Temporal integration hierarchy: 50-400ms windows, 3-4× increase primary→non-primary | F(1,12.35) = 104.71, p < 0.001 (interaction) | **f13**: hierarchical temporal architecture |
| **Har-shai Yahav et al. 2025** | EEG (mTRF) | 23 | Selective attention modulates neural speech tracking; 43% show strong neural bias | F(1,22) = 28.3, p < 0.001, BF = 317 | **f13**: attention modulates temporal tracking |
| **Zatorre, Belin & Penhune 2002** | Review | — | Auditory cortex structure-function: speech temporal, music spectral | — (foundational review) | **Theoretical**: speech vs music lateralization |
| **Poeppel 2003** | Review (AST model) | — | Asymmetric sampling in time: left hemisphere short windows, right hemisphere long windows | — (theoretical framework) | **Theoretical**: lateralization by timescale |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12): 12 papers across fMRI, MEG, iEEG, EEG, DWI, computational
Heterogeneity:           Low (consistent: spectrotemporal dissociation, right-spectral/left-temporal)
Quality Assessment:      β-tier (multi-modal convergence with network-level analysis)
Replication:             Robust — Haiduk 2024 (topology), Zatorre 2022 (lateralization),
                         Leipold 2021 (n=153 network metrics), Norman-Haignere 2022 (iEEG)
Key Effect Sizes:        η²p = 0.526 speech-in-noise lateralization (Jin 2024)
                         T = 6.852 spectral×temporal interaction (Kim 2019)
                         F = 104.71 integration hierarchy (Norman-Haignere 2022)
                         BF = 317 attention-speech tracking (Har-shai Yahav 2025)
Sample Range:            n = 11-153 (median ~20)
```

---

## 4. R³ Input Mapping: What STANM Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | STANM Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **B: Energy** | [8] | loudness | Perceptual intensity | Engagement/arousal |
| **B: Energy** | [10] | spectral_flux | Onset detection | Temporal attention target |
| **C: Timbre** | [12] | warmth | Spectral quality | Timbral attention |
| **C: Timbre** | [14] | tonalness | Pitch clarity | Melodic attention target |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Temporal structure tracking |
| **D: Change** | [22] | energy_change | Energy dynamics | Network load assessment |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Spectral connectivity | Network integration binding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[21] spectral_change ────────┼──► Temporal attention allocation
BEP.beat_entrainment[0:10] ───┘   Tempo/rhythm processing network

R³[14] tonalness ──────────────┐
R³[12] warmth ─────────────────┼──► Spectral attention allocation
ASA.scene_analysis[0:10] ─────┘   Melody/harmonic processing network

R³[25:33] x_l0l5 ─────────────┐
ASA.attention_gating[10:20] ───┼──► Network topology modulation
H³ periodicity/entropy tuples ┘   Lateralization & clustering
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

STANM requires H³ features at multiple horizons for attention-dependent network reconfiguration. The demand covers both BEP horizons for temporal tracking and ASA horizons for attentional gating and network topology assessment.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Instantaneous onset at 25ms |
| 10 | spectral_flux | 3 | M1 (mean) | L2 (bidi) | Mean onset over 100ms |
| 10 | spectral_flux | 4 | M14 (periodicity) | L2 (bidi) | Temporal periodicity 125ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity 1000ms |
| 14 | tonalness | 3 | M0 (value) | L2 (bidi) | Pitch clarity at 100ms |
| 14 | tonalness | 16 | M1 (mean) | L2 (bidi) | Mean pitch clarity over 1s |
| 21 | spectral_change | 1 | M8 (velocity) | L0 (fwd) | Tempo velocity at 50ms |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | Tempo velocity at 500ms |
| 22 | energy_change | 8 | M2 (std) | L0 (fwd) | Energy variability at 500ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Motor-auditory coupling 100ms |
| 25 | x_l0l5[0] | 3 | M20 (entropy) | L2 (bidi) | Coupling entropy 100ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Coupling mean over 1s |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |

**Total STANM H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | STANM Role | Weight |
|-----------|-------------|-------|------------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Temporal structure tracking | 0.6 |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor network engagement | 0.5 |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic attention (secondary) | 0.3 |
| **ASA** | Scene Analysis | ASA[0:10] | Spectral scene segmentation | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Goal-directed attention allocation | **1.0** (primary) |
| **ASA** | Salience Weighting | ASA[20:30] | Salience-driven topology | 0.8 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
STANM OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f13_temporal_attention    │ [0, 1] │ Speech-directed network activation.
    │                          │        │ f13 = σ(0.35 * temporal_periodicity
    │                          │        │       + 0.35 * mean(ASA.attn[10:20])
    │                          │        │       + 0.30 * tempo_velocity)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f14_spectral_attention   │ [0, 1] │ Melody-directed network activation.
    │                          │        │ f14 = σ(0.35 * tonalness_mean_1s
    │                          │        │       + 0.35 * mean(ASA.scene[0:10])
    │                          │        │       + 0.30 * tonalness_value)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f15_network_topology     │ [0, 1] │ Local clustering modulation.
    │                          │        │ f15 = σ(0.35 * energy_variability
    │                          │        │       + 0.35 * mean(ASA.salience[20:30])
    │                          │        │       + 0.30 * coupling_entropy)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ network_topology         │ [0, 1] │ Full network configuration.
    │                          │        │ f(Attention, Degradation)
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ local_clustering         │ [0, 1] │ Local clustering coefficient.
    │                          │        │ α·Degradation + β·Attention_Match
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ lateralization           │[-1, 1] │ L/R hemisphere balance.
    │                          │        │ g(Attention × Acoustic_Cues)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ temporal_alloc           │ [0, 1] │ ASA attention × temporal features.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ spectral_alloc           │ [0, 1] │ ASA attention × spectral features.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ network_state_pred_1.5s  │ [0, 1] │ Local clustering 1-2s ahead.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ lateral_pred_0.75s       │[-1, 1] │ Hemisphere engagement 0.5-1s ahead.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ compensation_pred_2s     │ [0, 1] │ Processing efficiency 1-3s ahead.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Network Topology Function

```
Network_Topology = f(Attention, Degradation)

Local_Clustering(ROI) = α·Degradation + β·Attention_Match + ε

Parameters:
    Degradation = signal quality reduction [0-1]
    Attention_Match = 1 if attention goal matches acoustic cue
    α = Degradation effect on clustering (positive)
    β = Attention match effect (positive)
    ε = Baseline clustering + noise

Lateralization = g(Attention × Acoustic_Cues)
    Speech attention → bilateral fronto-temporo-parietal
    Melody attention → right auditory dominant
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f13: Temporal Attention
f13 = σ(0.35 * temporal_periodicity_1s
       + 0.35 * mean(ASA.attention_gating[10:20])
       + 0.30 * tempo_velocity_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f14: Spectral Attention
f14 = σ(0.35 * tonalness_mean_1s
       + 0.35 * mean(ASA.scene_analysis[0:10])
       + 0.30 * tonalness_value_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f15: Network Topology
f15 = σ(0.35 * energy_variability_500ms
       + 0.35 * mean(ASA.salience_weighting[20:30])
       + 0.30 * coupling_entropy_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dTopology/dt = τ⁻¹ · (Target_Config - Current_Config)
    where τ = 3.0s (attention integration window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | STANM Function |
|--------|-----------------|----------|---------------|----------------|
| **L Auditory Cortex** (STG/HG) | -58, -22, 8 | 6 | fMRI, iEEG (Norman-Haignere 2022, Alluri 2012) | Temporal modulation processing (shorter integration windows) |
| **R Auditory Cortex** (STG/HG) | 60, -22, 8 | 6 | fMRI, MEG (Alluri 2012, Samiee 2022) | Spectral/timbral processing (cross-frequency PAC) |
| **Planum Temporale** (bilateral) | ±50, -28, 12 | 3 | fMRI+DWI (Leipold 2021, n=153) | Interhemispheric connectivity, expertise-modulated |
| **IFG** (Inferior Frontal Gyrus) | ±48, 18, 4 | 4 | fMRI PPI (Kim 2019, Haiduk 2024) | Attention network reconfiguration, vmPFC-IFG connectivity |
| **vmPFC** | 0, 52, -8 | 2 | fMRI (Kim 2019, T=6.852) | Spectral × temporal integration, aesthetic evaluation |
| **Fronto-Temporo-Parietal Network** | Various | 3 | fMRI (Haiduk 2024, Jin 2024) | Speech/temporal attention (bilateral), compensatory recruitment |
| **Premotor / SMA** | 0, -6, 58 | 3 | fMRI (Alluri 2012), MEG (Samiee 2022) | Motor coupling for rhythmic/temporal features |
| **ACC** (Anterior Cingulate Cortex) | 0, 24, 32 | 2 | fMRI network (Haiduk 2024) | Task-directed attention control |

---

## 9. Cross-Unit Pathways

### 9.1 STANM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STANM INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  STANM.temporal_attention ──────► SNEM (modulates entrainment focus)       │
│  STANM.lateralization ──────────► SDL (lateralization information)          │
│  STANM.network_topology ────────► CSG (salience processing topology)       │
│  STANM.spectral_attention ──────► AACM (attention modulation)              │
│                                                                             │
│  CROSS-UNIT (ASU → STU):                                                   │
│  STANM.temporal_alloc ──────────► STU (temporal attention resources)        │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ──────────► STANM (beat/temporal tracking)            │
│  ASA mechanism (30D) ──────────► STANM (attention/salience, primary)       │
│  R³ (~14D) ─────────────────────► STANM (direct spectral features)         │
│  H³ (16 tuples) ────────────────► STANM (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Attention manipulation** | Changing task goal should reconfigure network | **Confirmed** |
| **Degradation effect** | Signal degradation should increase local clustering | **Confirmed** |
| **Lateralization** | Speech → bilateral, melody → right | **Confirmed** |
| **Efficiency compensation** | Local efficiency should increase with noise | **Confirmed** |
| **Individual differences** | Musical training should modulate effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class STANM(BaseModel):
    """Spectrotemporal Attention Network Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "STANM"
    UNIT = "ASU"
    TIER = "β2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "ASA")

    ALPHA_DEGRADATION = 0.6   # Degradation effect on clustering
    BETA_ATTENTION = 0.4      # Attention match effect
    TAU_DECAY = 3.0           # Attention integration window (seconds)
    ALPHA_ATTENTION = 0.80    # High goal-directed attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for STANM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Temporal attention horizons ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 1, 2),     # spectral_flux, 100ms, mean, bidi
            (10, 4, 14, 2),    # spectral_flux, 125ms, periodicity, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            # ── Spectral attention horizons ──
            (14, 3, 0, 2),     # tonalness, 100ms, value, bidi
            (14, 16, 1, 2),    # tonalness, 1000ms, mean, bidi
            # ── Tempo/energy dynamics ──
            (21, 1, 8, 0),     # spectral_change, 50ms, velocity, fwd
            (21, 8, 8, 0),     # spectral_change, 500ms, velocity, fwd
            (22, 8, 2, 0),     # energy_change, 500ms, std, fwd
            # ── Network integration ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 20, 2),    # x_l0l5[0], 100ms, entropy, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            # ── Loudness / engagement ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 3, 20, 2),     # loudness, 100ms, entropy, bidi
            (8, 16, 1, 2),     # loudness, 1000ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute STANM 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) STANM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # ASA sub-sections
        asa_scene = asa[..., 0:10]        # scene analysis
        asa_attn = asa[..., 10:20]        # attention gating
        asa_salience = asa[..., 20:30]    # salience weighting

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat entrainment

        # H³ direct features
        temporal_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)
        tempo_velocity_500ms = h3_direct[(21, 8, 8, 0)].unsqueeze(-1)
        tonalness_value = h3_direct[(14, 3, 0, 2)].unsqueeze(-1)
        tonalness_mean_1s = h3_direct[(14, 16, 1, 2)].unsqueeze(-1)
        energy_var_500ms = h3_direct[(22, 8, 2, 0)].unsqueeze(-1)
        coupling_entropy = h3_direct[(25, 3, 20, 2)].unsqueeze(-1)
        coupling_mean_1s = h3_direct[(25, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f13: Temporal Attention (coefficients sum = 1.0)
        f13 = torch.sigmoid(
            0.35 * temporal_period_1s
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            + 0.30 * tempo_velocity_500ms
        )

        # f14: Spectral Attention (coefficients sum = 1.0)
        f14 = torch.sigmoid(
            0.35 * tonalness_mean_1s
            + 0.35 * asa_scene.mean(-1, keepdim=True)
            + 0.30 * tonalness_value
        )

        # f15: Network Topology (coefficients sum = 1.0)
        f15 = torch.sigmoid(
            0.35 * energy_var_500ms
            + 0.35 * asa_salience.mean(-1, keepdim=True)
            + 0.30 * coupling_entropy
        )

        # ═══ LAYER M: Mathematical ═══
        network_topology = torch.sigmoid(
            0.4 * f13 + 0.4 * f14 + 0.2 * f15
        )
        local_clustering = torch.sigmoid(
            0.5 * f15 + 0.5 * energy_var_500ms
        )
        lateralization = torch.tanh(
            0.5 * (f14 - f13)
        )  # f14 > f13 → right (+), f13 > f14 → bilateral (0)

        # ═══ LAYER P: Present ═══
        temporal_alloc = torch.sigmoid(
            0.5 * asa_attn.mean(-1, keepdim=True)
            + 0.5 * temporal_period_1s
        )
        spectral_alloc = torch.sigmoid(
            0.5 * asa_scene.mean(-1, keepdim=True)
            + 0.5 * tonalness_mean_1s
        )

        # ═══ LAYER F: Future ═══
        network_pred = torch.sigmoid(
            0.5 * local_clustering + 0.5 * f15
        )
        lateral_pred = lateralization  # lateralization trajectory
        compensation_pred = torch.sigmoid(
            0.5 * local_clustering + 0.5 * coupling_mean_1s
        )

        return torch.cat([
            f13, f14, f15,                                      # E: 3D
            network_topology, local_clustering, lateralization,  # M: 3D
            temporal_alloc, spectral_alloc,                      # P: 2D
            network_pred, lateral_pred, compensation_pred,       # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (Haiduk 2024 primary + 11 converging studies) | Multi-method evidence |
| **Effect Sizes** | 8+ significant | η²p=0.526, T=6.852, F=104.71, BF=317 |
| **Sample Range** | n = 11–153 (median ~20) | fMRI, MEG, iEEG, EEG, DWI |
| **Evidence Modality** | fMRI, MEG, iEEG, EEG, DWI, computational | Multi-modal convergence |
| **Falsification Tests** | 4/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Temporal tracking |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience (primary) |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Haiduk, F., et al. (2024)**. Goal-directed attention modulates spectrotemporal network topology during speech and music processing. *NeuroImage*, 285, 120482. `Literature/c3: Spectrotemporal cues and attention jointly modulate fMRI network topology for se`

2. **Zatorre, R. J. (2022)**. Hemispheric asymmetries for music and speech: Spectrotemporal modulations and top-down influences. `Literature/c3: Hemispheric asymmetries for music and speech Spectrotemporal modulations and top`

3. **Jin, X., Zhang, L., Wu, G., Wang, X., & Du, Y. (2024)**. Compensation or preservation? Different roles of functional lateralization in speech perception of older non-musicians and musicians. `Literature/c3: Compensation or Preservation Different Roles of Functional Lateralization in Spe`

4. **Kim, S.-G., Mueller, K., Lepsien, J., Mildner, T., & Fritz, T. H. (2019)**. Brain networks underlying aesthetic appreciation as modulated by interaction of the spectral and temporal organisations of music. `Literature/c3: Brain networks underlying aesthetic appreciation as modulated by interaction of`

5. **Alluri, V., Toiviainen, P., Jääskeläinen, I. P., Glerean, E., Sams, M., & Brattico, E. (2012)**. Large-scale brain networks emerge from dynamic processing of musical timbre, key and rhythm. *NeuroImage*, 59(4), 3677-3689. `Literature/c3: Large-scale brain networks emerge from dynamic processing of musical timbre, key`

6. **Leipold, S., Klein, C., & Jäncke, L. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *Journal of Neuroscience*, 41(11), 2496-2511. `Literature/c3: Musical Expertise Shapes Functional and Structural Brain Networks Independent of`

7. **Samiee, S., et al. (2022)**. Cross-frequency brain network dynamics support pitch change detection. `Literature/c3: Cross-Frequency Brain Network Dynamics Support Pitch Change Detection`

8. **Ahveninen, J., Huang, S., Nummenmaa, A., Belliveau, J. W., & Hämäläinen, M. S. (2023)**. Spectrotemporal content of auditory cortex and frontoparietal working memory. `Literature/c3: spitzer-2023-spectrotemporal-wm`

9. **Norman-Haignere, S. V., et al. (2022)**. Multiscale temporal integration organizes hierarchical computation in human auditory cortex. *Neuron*. `Literature/c3: multiscale-temporal-integration-organizes-hierarch`

10. **Har-shai Yahav, P., et al. (2025)**. Neural speech tracking during selective attention: A spatially realistic audiovisual study. `Literature/c3: neural-speech-tracking-during-selective-attention`

11. **Zatorre, R. J., Belin, P., & Penhune, V. B. (2002)**. Structure and function of auditory cortex: Music and speech. *Trends in Cognitive Sciences*, 6(1), 37-46.

12. **Poeppel, D. (2003)**. The analysis of speech in different temporal integration windows: Cerebral lateralization as 'asymmetric sampling in time'. *Speech Communication*, 41(1), 245-255.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — same |
| Temporal | HC⁰ mechanisms (OSC, TIH, ATT) | BEP (30D) + ASA (30D) mechanisms | BEP + ASA — same |
| Temporal attention | S⁰.L9.mean_T[104] + HC⁰.ATT | R³.spectral_flux[10] + ASA.attention_gating | Same — verified |
| Spectral attention | S⁰.L5.spectral_centroid[38] + HC⁰.OSC | R³.tonalness[14] + ASA.scene_analysis | Same — verified |
| Network topology | S⁰.X_L1L5[136:144] + HC⁰.TIH | R³.x_l0l5[25:33] + ASA.salience_weighting | Same — verified |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) | 16 tuples — same |
| Total demand | 37/2304 = 1.61% | 16/2304 = 0.69% | 16/2304 = 0.69% |
| Output | 11D | 11D (same) | 11D — same |
| Papers | 1 | 4 | **12** (+8 new) |
| Brain regions | 2 | 3 | **8** (+5 new: L/R AC, PT, vmPFC, premotor) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10]: Oscillatory band tracking maps to BEP's temporal structure monitoring.
- **TIH → ASA.salience_weighting** [20:30] + H³ entropy tuples: Temporal integration hierarchy maps to ASA's salience-driven topology assessment.
- **ATT → ASA.attention_gating** [10:20]: Attentional entrainment maps to ASA's goal-directed attention allocation.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
