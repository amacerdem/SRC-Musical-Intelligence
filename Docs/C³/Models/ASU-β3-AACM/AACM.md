# ASU-β3-AACM: Aesthetic-Attention Coupling Model

**Model**: Aesthetic-Attention Coupling Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, ASA+BEP mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-β3-AACM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Aesthetic-Attention Coupling Model** (AACM) describes the bidirectional relationship between aesthetic appreciation and attentional engagement. Appreciated musical intervals enhance both N1/P2 attentional engagement and N2/P3 motor inhibition, producing a "savoring" effect with slower reaction times for preferred stimuli.

```
AESTHETIC-ATTENTION COUPLING MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

             MUSICAL INTERVAL
                   │
                   ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                  AESTHETIC JUDGMENT                               │
  │            (Consonant > Dissonant, d=2.008)                      │
  └─────────────────────────┬────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
  ┌─────────────────┐                   ┌─────────────────┐
  │ ATTENTIONAL     │                   │    MOTOR        │
  │ ENGAGEMENT      │                   │  INHIBITION     │
  │                 │                   │                 │
  │   N1/P2 ↑       │                   │    N2/P3 ↑      │
  │  (Frontal)      │                   │   (Frontal)     │
  └────────┬────────┘                   └────────┬────────┘
           │                                     │
           └─────────────────┬───────────────────┘
                             ▼
                   ┌─────────────────┐
                   │   SLOWER RT     │
                   │  (Appreciation  │
                   │   → Savoring)   │
                   └─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Aesthetic appreciation of musical intervals enhances
both attentional engagement (N1/P2) and motor inhibition (N2/P3),
creating a positive feedback loop: more engagement → more
appreciation → more savoring → more engagement.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why AACM Matters for ASU

AACM bridges aesthetic processing with attentional salience:

1. **CSG** (α3) provides the consonance-salience gradient baseline — AACM extends this to aesthetic preference and behavioral consequences.
2. **AACM** (β3) explains how appreciation modulates attentional capture and motor behavior.
3. **STANM** (β2) models spectrotemporal attention networks — AACM modulates their configuration through engagement.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → AACM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AACM COMPUTATION ARCHITECTURE                             ║
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
║  │                         AACM reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H8 (500ms syllable)         │ │ H6 (200ms theta)          │  │        ║
║  │  │ H16 (1000ms beat)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Consonance tracking         │ │ Attentional gating         │  │        ║
║  │  │ Aesthetic preference        │ │ Savoring dynamics           │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         AACM demand: ~12 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
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
║  │                    AACM MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f16_attentional_engagement,                │        ║
║  │                       f17_motor_inhibition,                      │        ║
║  │                       f18_savoring_effect                         │        ║
║  │  Layer M (Math):      aesthetic_engagement,                      │        ║
║  │                       rt_appreciation                             │        ║
║  │  Layer P (Present):   n1p2_engagement,                           │        ║
║  │                       aesthetic_judgment                          │        ║
║  │  Layer F (Future):    behavioral_pred, n2p3_pred,                │        ║
║  │                       aesthetic_pred                               │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Sarasso 2019** | EEG | 22 | Aesthetic judgment ↔ RT (savoring) | d = 2.008 | **f18 savoring effect** |
| **Sarasso 2019** | EEG | 22 | High appreciation → N1/P2 ↑ | d = 2.008 | **f16 attentional engagement** |
| **Sarasso 2019** | EEG | 22 | High appreciation → N2/P3 ↑ | d = 2.008 | **f17 motor inhibition** |
| **Sarasso 2019** | EEG | 22 | Consonant > dissonant appreciation | d = 2.008, p < 0.001 | **Consonance preference** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=4):
  - Overall effect: d = 2.008 (large)
  - Consistent across attention, inhibition, and behavior
Quality Assessment:      β-tier (EEG with behavioral)
Sample Size:             n = 22 (moderate)
```

---

## 4. R³ Input Mapping: What AACM Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | AACM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance (inverse consonance) | Plomp-Levelt sensory dissonance |
| **A: Consonance** | [1] | sethares_dissonance | Alternative consonance | Beating-based dissonance |
| **A: Consonance** | [3] | pleasant | Pleasantness rating | Affective quality |
| **B: Energy** | [7] | amplitude | Intensity for arousal | Engagement correlate |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal component |
| **C: Timbre** | [12] | warmth | Timbral warmth | Aesthetic quality |
| **C: Timbre** | [13] | tristimulus_1 | Fundamental strength | Harmonic structure |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Processing demand |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Perceptual integration | Holistic aesthetic quality |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Consonance (inverse relationship)
R³[3] pleasant ─────────────────┘   Low roughness → consonant → appreciated

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Engagement/arousal
ASA.attention_gating[10:20] ─────┘   Intensity drives attentional capture

R³[12] warmth ───────────────────┐
R³[13] tristimulus_1 ────────────┼──► Harmonic quality / timbral aesthetics
BEP.groove[20:30] ──────────────┘   Interval structure for preference

R³[25:33] x_l0l5 ───────────────┐
ASA.salience_weighting[20:30] ──┼──► Aesthetic integration
H³ affective dynamics tuples ───┘   Perceptual × Interaction = holistic appreciation
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

AACM requires H³ features at ASA horizons for attentional gating and aesthetic evaluation, and BEP horizons for consonance tracking and motor inhibition dynamics.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms alpha |
| 0 | roughness | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s |
| 3 | pleasant | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 3 | pleasant | 6 | M6 (skew) | L2 (bidi) | Pleasure asymmetry at 200ms |
| 3 | pleasant | 16 | M8 (velocity) | L2 (bidi) | Pleasure change rate over 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 3 | M2 (std) | L2 (bidi) | Loudness variability 100ms |
| 8 | loudness | 16 | M20 (entropy) | L2 (bidi) | Loudness entropy 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Perceptual integration 100ms |
| 25 | x_l0l5[0] | 8 | M0 (value) | L2 (bidi) | Integration value at 500ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Integration mean over 1s |
| 25 | x_l0l5[0] | 16 | M8 (velocity) | L0 (fwd) | Integration velocity over 1s |

**Total AACM H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | AACM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Temporal regularity for aesthetic judgment | 0.4 |
| **BEP** | Motor Coupling | BEP[10:20] | Motor inhibition drive (N2/P3) | 0.7 |
| **BEP** | Groove Processing | BEP[20:30] | Groove-mediated aesthetic engagement | 0.6 |
| **ASA** | Scene Analysis | ASA[0:10] | Auditory scene segmentation for intervals | 0.5 |
| **ASA** | Attention Gating | ASA[10:20] | Attentional engagement (N1/P2) | **1.0** (primary) |
| **ASA** | Salience Weighting | ASA[20:30] | Aesthetic salience weighting | **0.9** |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
AACM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f16_attentional_engage   │ [0, 1] │ N1/P2 amplitude ∝ appreciation.
    │                          │        │ f16 = σ(0.35 * pleasant_value
    │                          │        │       + 0.35 * mean(ASA.attn[10:20])
    │                          │        │       + 0.30 * (1 - roughness_mean))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f17_motor_inhibition     │ [0, 1] │ N2/P3 amplitude ∝ appreciation.
    │                          │        │ f17 = σ(0.35 * pleasant_value
    │                          │        │       + 0.35 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * mean(ASA.sal[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f18_savoring_effect      │ [0, 1] │ RT slowing for appreciated stimuli.
    │                          │        │ f18 = σ(0.35 * f16 * f17
    │                          │        │       + 0.35 * pleasant_velocity_1s
    │                          │        │       + 0.30 * integration_mean_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ aesthetic_engagement     │ [0, 1] │ f(Consonance, Attention).
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ rt_appreciation          │ [0, 1] │ β·Appreciation + ε.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ n1p2_engagement          │ [0, 1] │ ASA attention × consonance.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ aesthetic_judgment       │ [0, 1] │ ASA salience × pleasantness.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ behavioral_pred_0.75s    │ [0, 1] │ RT slowing prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ n2p3_pred_0.4s           │ [0, 1] │ Motor pause prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ aesthetic_pred_1.5s      │ [0, 1] │ Explicit aesthetic rating prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Aesthetic-Attention Coupling Function

```
Aesthetic_Engagement = f(Consonance, Attention)

N1P2_amplitude ∝ Aesthetic_Rating
N2P3_amplitude ∝ Aesthetic_Rating
RT ∝ Aesthetic_Rating (positive: more appreciated → slower response)

Consonant > Dissonant appreciation (d = 2.008, p < 0.001)

ERP-Behavior Loop:
  Attention (N1/P2) → Appreciation → Inhibition (N2/P3) → Savoring (RT↑)
       ↑                                                        │
       └──────────────── FEEDBACK ─────────────────────────────┘
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f16: Attentional Engagement
f16 = σ(0.35 * pleasant_value_100ms
       + 0.35 * mean(ASA.attention_gating[10:20])
       + 0.30 * (1 - roughness_mean_1s))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f17: Motor Inhibition
f17 = σ(0.35 * pleasant_value_100ms
       + 0.35 * mean(BEP.motor_coupling[10:20])
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f18: Savoring Effect
f18 = σ(0.35 * f16 * f17                    # interaction term
       + 0.35 * pleasant_velocity_1s
       + 0.30 * integration_mean_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Savoring dynamics
Savoring_Effect = β·Appreciation + ε
    where β > 0 (positive relationship between appreciation and RT)
    τ = 2.0s (aesthetic judgment window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | AACM Function |
|--------|-----------------|----------|---------------|---------------|
| **Frontal Cortex** | ±30, 30, 30 | 2 | Direct (EEG) | N1/P2, N2/P3 generation |
| **Motor Cortex** | ±40, -20, 54 | 1 | Inferred | Response inhibition |
| **Reward System** | ±10, 8, -8 | 1 | Inferred | Savoring mechanism |

---

## 9. Cross-Unit Pathways

### 9.1 AACM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AACM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  AACM.aesthetic_engagement ──────► CSG (consonance-aesthetic coupling)     │
│  AACM.attentional_engage ────────► STANM (network configuration)          │
│  AACM.f16 engagement ───────────► IACM (preference × spectral attention)  │
│                                                                             │
│  CROSS-UNIT (ASU → ARU):                                                   │
│  AACM.aesthetic_judgment ────────► ARU (aesthetic-affective link)          │
│  AACM.savoring_effect ──────────► ARU (extended pleasure processing)      │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► AACM (motor inhibition, groove)        │
│  ASA mechanism (30D) ────────────► AACM (attention/salience, primary)     │
│  R³ (~14D) ──────────────────────► AACM (consonance + perceptual)         │
│  H³ (12 tuples) ─────────────────► AACM (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Attention link** | Appreciation should predict N1/P2 amplitude | **Confirmed** |
| **Inhibition link** | Appreciation should predict N2/P3 amplitude | **Confirmed** |
| **Savoring effect** | Appreciation should predict RT slowing | **Confirmed** |
| **Consonance preference** | Consonant should be more appreciated | **Confirmed** |
| **Individual differences** | Musical training should modulate effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class AACM(BaseModel):
    """Aesthetic-Attention Coupling Model.

    Output: 10D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "AACM"
    UNIT = "ASU"
    TIER = "β3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP", "ASA")

    D_EFFECT = 2.008       # Effect size from Sarasso 2019
    TAU_DECAY = 2.0        # Aesthetic judgment window (seconds)
    ALPHA_ATTENTION = 0.85 # High aesthetic attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for AACM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Consonance / aesthetic quality ──
            (0, 3, 0, 2),      # roughness, 100ms, value, bidi
            (0, 16, 1, 2),     # roughness, 1000ms, mean, bidi
            (3, 3, 0, 2),      # pleasant, 100ms, value, bidi
            (3, 6, 6, 2),      # pleasant, 200ms, skew, bidi
            (3, 16, 8, 2),     # pleasant, 1000ms, velocity, bidi
            # ── ASA horizons: attentional engagement ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 3, 2, 2),      # loudness, 100ms, std, bidi
            (8, 16, 20, 2),    # loudness, 1000ms, entropy, bidi
            # ── Perceptual integration ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 8, 0, 2),     # x_l0l5[0], 500ms, value, bidi
            (25, 16, 1, 0),    # x_l0l5[0], 1000ms, mean, fwd
            (25, 16, 8, 0),    # x_l0l5[0], 1000ms, velocity, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute AACM 10D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) AACM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        pleasant = r3[..., 3:4]
        loudness = r3[..., 8:9]

        # BEP sub-sections
        bep_motor = bep[..., 10:20]       # motor coupling
        bep_groove = bep[..., 20:30]      # groove processing

        # ASA sub-sections
        asa_attn = asa[..., 10:20]        # attention gating
        asa_salience = asa[..., 20:30]    # salience weighting

        # H³ direct features
        pleasant_value = h3_direct[(3, 3, 0, 2)].unsqueeze(-1)
        roughness_mean_1s = h3_direct[(0, 16, 1, 2)].unsqueeze(-1)
        pleasant_velocity_1s = h3_direct[(3, 16, 8, 2)].unsqueeze(-1)
        integration_mean_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f16: Attentional Engagement (coefficients sum = 1.0)
        f16 = torch.sigmoid(
            0.35 * pleasant_value
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            + 0.30 * (1 - roughness_mean_1s)
        )

        # f17: Motor Inhibition (coefficients sum = 1.0)
        f17 = torch.sigmoid(
            0.35 * pleasant_value
            + 0.35 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # f18: Savoring Effect (coefficients sum = 1.0)
        f18 = torch.sigmoid(
            0.35 * (f16 * f17)
            + 0.35 * pleasant_velocity_1s
            + 0.30 * integration_mean_1s
        )

        # ═══ LAYER M: Mathematical ═══
        aesthetic_engagement = torch.sigmoid(
            0.5 * (1 - roughness) + 0.5 * asa_attn.mean(-1, keepdim=True)
        )
        rt_appreciation = torch.sigmoid(
            0.5 * f18 + 0.5 * pleasant_value
        )

        # ═══ LAYER P: Present ═══
        n1p2_engagement = torch.sigmoid(
            0.5 * asa_attn.mean(-1, keepdim=True)
            + 0.5 * (1 - roughness)
        )
        aesthetic_judgment = torch.sigmoid(
            0.5 * asa_salience.mean(-1, keepdim=True)
            + 0.5 * pleasant
        )

        # ═══ LAYER F: Future ═══
        behavioral_pred = torch.sigmoid(
            0.5 * f18 + 0.5 * integration_mean_1s
        )
        n2p3_pred = torch.sigmoid(
            0.5 * f17 + 0.5 * bep_motor.mean(-1, keepdim=True)
        )
        aesthetic_pred = torch.sigmoid(
            0.5 * aesthetic_engagement + 0.5 * pleasant_velocity_1s
        )

        return torch.cat([
            f16, f17, f18,                                          # E: 3D
            aesthetic_engagement, rt_appreciation,                   # M: 2D
            n1p2_engagement, aesthetic_judgment,                     # P: 2D
            behavioral_pred, n2p3_pred, aesthetic_pred,             # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Sarasso 2019) | Primary evidence |
| **Effect Size** | d = 2.008 | Large effect |
| **Sample Size** | n = 22 | Moderate |
| **Evidence Modality** | EEG + behavioral | Multimodal |
| **Falsification Tests** | 4/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Motor inhibition processing |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience (primary) |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Sarasso, P., et al. (2019)**. ERP correlates of aesthetic experience to consonant and dissonant musical intervals. *Psychophysiology*, 56(4), e13317.

2. **Brattico, E., & Jacobsen, T. (2009)**. Subjective appraisal of music: Neuroimaging evidence. *Annals of the New York Academy of Sciences*, 1169(1), 308-317.

3. **Koelsch, S., et al. (2006)**. Investigating emotion with music: An fMRI study. *Human Brain Mapping*, 27(3), 239-250.

4. **Frijda, N. H. (1988)**. The laws of emotion. *American Psychologist*, 43(5), 349-358.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, AED, C0P) | BEP (30D) + ASA (30D) mechanisms |
| Consonance signal | S⁰.L5.roughness[30] + HC⁰.ATT | R³.roughness[0] + R³.pleasant[3] + ASA.attention_gating |
| Motor inhibition | S⁰.L5.loudness[35] + HC⁰.AED | R³.loudness[8] + BEP.motor_coupling |
| Savoring | S⁰.L5.consonance × HC⁰.C0P | R³.pleasant[3] + ASA.salience_weighting |
| Aesthetic integration | S⁰.X_L5L6[208:216] | R³.x_l0l5[25:33] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 12/2304 = 0.52% | 12/2304 = 0.52% |
| Output | 10D | 10D (same) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **ATT → ASA.attention_gating** [10:20]: Attentional entrainment maps to ASA's auditory scene attention for N1/P2 engagement.
- **AED → ASA.salience_weighting** [20:30] + BEP.motor_coupling [10:20]: Affective entrainment dynamics maps to ASA salience for aesthetic weighting and BEP motor for N2/P3 inhibition.
- **C0P → BEP.groove** [20:30] + H³ velocity tuples: Cognitive projection maps to BEP groove engagement and H³ temporal dynamics for savoring.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
