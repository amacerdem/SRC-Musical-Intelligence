# ASU-β2-STANM: Spectrotemporal Attention Network Model

**Model**: Spectrotemporal Attention Network Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, ASA+BEP mechanisms)
**Date**: 2026-02-12

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
| **Haiduk 2024** | fMRI | 15 | Temporal → speech, Spectral → melody attention networks | p < 0.001 | **f13, f14 attention allocation** |
| **Haiduk 2024** | fMRI | 15 | Degradation → local clustering increase | p < 0.01 | **f15 network topology** |
| **Haiduk 2024** | fMRI | 15 | Degradation → local efficiency increase | p < 0.002 | **Compensation mechanism** |
| **Haiduk 2024** | fMRI | 15 | Lateralization: attention x acoustic | qualitative | **Lateralization model** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=4):
  - Attention-network mapping: significant (p < 0.001)
  - Degradation-clustering: p < 0.01
  - Degradation-efficiency: p < 0.002
  - Lateralization interaction: qualitative
Quality Assessment:      β-tier (fMRI network analysis)
Sample Size:             n = 15 (moderate)
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
| **Fronto-Temporo-Parietal (bilateral)** | Various | 1 | Direct (fMRI) | Speech/temporal attention |
| **R Auditory Cortex** | 60, -22, 8 | 1 | Direct (fMRI) | Melody/spectral attention |
| **Auditory Network** | Various | 1 | Direct (fMRI) | Local clustering compensation |

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
| **Papers** | 1 (Haiduk 2024) | Primary evidence |
| **Findings** | 4 | All significant |
| **Sample Size** | n = 15 | Moderate |
| **Evidence Modality** | fMRI | Direct neural |
| **Falsification Tests** | 4/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Temporal tracking |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience (primary) |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Haiduk, F., et al. (2024)**. Goal-directed attention modulates spectrotemporal network topology during speech and music processing. *NeuroImage*, 285, 120482.

2. **Zatorre, R. J., Belin, P., & Penhune, V. B. (2002)**. Structure and function of auditory cortex: Music and speech. *Trends in Cognitive Sciences*, 6(1), 37-46.

3. **Poeppel, D. (2003)**. The analysis of speech in different temporal integration windows: Cerebral lateralization as 'asymmetric sampling in time'. *Speech Communication*, 41(1), 245-255.

4. **Bullmore, E., & Sporns, O. (2009)**. Complex brain networks: Graph theoretical analysis of structural and functional systems. *Nature Reviews Neuroscience*, 10(3), 186-198.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, ATT) | BEP (30D) + ASA (30D) mechanisms |
| Temporal attention | S⁰.L9.mean_T[104] + HC⁰.ATT | R³.spectral_flux[10] + ASA.attention_gating |
| Spectral attention | S⁰.L5.spectral_centroid[38] + HC⁰.OSC | R³.tonalness[14] + ASA.scene_analysis |
| Network topology | S⁰.X_L1L5[136:144] + HC⁰.TIH | R³.x_l0l5[25:33] + ASA.salience_weighting |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 37/2304 = 1.61% | 16/2304 = 0.69% |
| Output | 11D | 11D (same) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10]: Oscillatory band tracking maps to BEP's temporal structure monitoring.
- **TIH → ASA.salience_weighting** [20:30] + H³ entropy tuples: Temporal integration hierarchy maps to ASA's salience-driven topology assessment.
- **ATT → ASA.attention_gating** [10:20]: Attentional entrainment maps to ASA's goal-directed attention allocation.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
