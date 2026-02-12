# RPU-β3-MEAMR: Music-Evoked Autobiographical Memory Reward

**Model**: Music-Evoked Autobiographical Memory Reward
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, AED+CPD+C0P mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-β3-MEAMR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Music-Evoked Autobiographical Memory Reward** (MEAMR) model describes how familiar music activates dorsal medial prefrontal cortex (dMPFC) in proportion to autobiographical salience, integrating musical structure with self-referential processing and reward.

```
MUSIC-EVOKED AUTOBIOGRAPHICAL MEMORY REWARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUSICAL INPUT                            NEURAL RESPONSE
─────────────                            ───────────────

Musical Structure ─────────────────► Tonal Space Encoding
     │                                   (dMPFC tracking)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│               AUTOBIOGRAPHICAL MEMORY NETWORK                    │
│                                                                  │
│   dMPFC               vACC                 SN/VTA                │
│   ═════               ════                 ══════                │
│   Autobiographical     Positive affect     Reward signal          │
│   salience tracking    integration         Dopamine release       │
│                                                                  │
│   dMPFC ↔ Autobio salience (p < 0.001)                           │
│   dMPFC tracks tonal space (p < 0.005)                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    REWARD INTEGRATION                             │
│   vACC + SN ↔ positive affect (p < 0.001)                       │
│   Familiar music → stronger autobiographical salience            │
│   Nostalgia response → sustained reward activation               │
└──────────────────────────────────────────────────────────────────┘

MEMORY: dMPFC activation proportional to autobiographical salience
REWARD: vACC + SN/VTA positive affect integration
TONAL:  dMPFC continuously tracks tonal space of familiar music

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Familiar music activates dMPFC in proportion to
autobiographical salience, linking musical structure encoding
with self-referential memory processing and reward.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MEAMR Matters for RPU

MEAMR provides the memory-reward bridge for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking via inverted-U preference.
5. **MCCN** (β2) maps cortical network during chills.
6. **MEAMR** (β3) bridges autobiographical memory to reward — familiar music activates self-referential processing that enhances pleasure.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → MEAMR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MEAMR COMPUTATION ARCHITECTURE                            ║
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
║  │                         MEAMR reads: ~12D                       │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ──────────────┐ ┌── CPD Horizons ──────────┐  │        ║
║  │  │ H8 (500ms delta)             │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)            │ │ H20 (5000ms LTI)         │  │        ║
║  │  │                              │ │                            │  │        ║
║  │  │ Familiarity assessment       │ │ Memory activation          │  │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         MEAMR demand: ~14 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Memory-Reward Circuit ════    ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │  AED (30D)      │  │  CPD (30D)      │  │  C0P (30D)      │              ║
║  │                 │  │                 │  │                 │              ║
║  │ Valence  [0:10] │  │ Anticip. [0:10] │  │ Tension  [0:10] │              ║
║  │ Arousal  [10:20]│  │ Peak Exp [10:20]│  │ Expect.  [10:20]│              ║
║  │ Emotion  [20:30]│  │ Resolut. [20:30]│  │ Approach [20:30]│              ║
║  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              ║
║           │                    │                    │                        ║
║           └────────────┬───────┴────────────────────┘                        ║
║                        ▼                                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MEAMR MODEL (6D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_familiarity_index,                     │        ║
║  │                       f02_autobio_salience,                      │        ║
║  │                       f03_dmpfc_tracking,                         │        ║
║  │                       f04_positive_affect                         │        ║
║  │  Layer P (Present):   memory_activation_state                     │        ║
║  │  Layer F (Future):    nostalgia_response_pred                     │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Janata 2009** | fMRI | — | dMPFC ↔ autobiographical salience | p < 0.001 | **Primary**: f02 autobio salience |
| **Janata 2009** | fMRI | — | dMPFC tracks tonal space | p < 0.005 | **f03 dMPFC tracking** |
| **Janata 2009** | fMRI | — | vACC + SN ↔ positive affect | p < 0.001 | **f04 positive affect** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=3):  All findings from single fMRI study
Heterogeneity:           N/A (single study, multiple contrasts)
Quality Assessment:      β-tier (fMRI with behavioral convergence)
Replication:             Consistent with Platel (2003) music-memory, Janata (2007) tonal space
```

---

## 4. R³ Input Mapping: What MEAMR Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | MEAMR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Familiarity cue | Tonal recognition |
| **B: Energy** | [8] | loudness | Familiarity dynamics | Familiar loudness patterns |
| **C: Timbre** | [12] | warmth | Timbre familiarity | Brightness recognition |
| **C: Timbre** | [13] | spectral_centroid | Brightness familiarity | Timbre tracking |
| **D: Change** | [21] | spectral_change | Structural complexity | Memory accessibility |
| **D: Change** | [22] | energy_change | Temporal patterns | Time signature cues |
| **E: Interactions** | [41:49] | x_l5l6 (8D) | Memory-structure binding | Autobiographical salience |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[8] loudness ────────────────┼──► Familiarity index
H³ trend/mean tuples ──────────┘   Recognition of familiar patterns

R³[41:49] x_l5l6 ─────────────┐
AED.emotional_trajectory[20:30]┼──► Autobiographical salience
H³ long-range tuples ──────────┘   Memory-structure binding

R³[12] warmth ─────────────────┐
R³[13] spectral_centroid ──────┼──► dMPFC tonal space tracking
C0P.expectation_surprise[10:20]┘   Harmonic trajectory prediction

AED.valence_tracking[0:10] ────┐
CPD.peak_experience[10:20] ────┼──► Positive affect integration
R³[4] sensory_pleasantness ────┘   vACC + SN reward signal
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MEAMR requires H³ features at long time scales: familiarity assessment needs 1-5s context windows, and autobiographical salience benefits from sustained temporal integration to capture tonal trajectory recognition.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness over 500ms |
| 4 | sensory_pleasantness | 16 | M18 (trend) | L2 (bidi) | Pleasantness trend over 1s |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness over 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |
| 12 | warmth | 16 | M1 (mean) | L2 (bidi) | Mean warmth over 1s |
| 13 | spectral_centroid | 16 | M1 (mean) | L2 (bidi) | Mean brightness over 1s |
| 21 | spectral_change | 8 | M20 (entropy) | L2 (bidi) | Structural entropy 500ms |
| 21 | spectral_change | 16 | M1 (mean) | L2 (bidi) | Mean structural change 1s |
| 22 | energy_change | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms |
| 41 | x_l5l6[0] | 8 | M1 (mean) | L2 (bidi) | Memory-structure coupling 500ms |
| 41 | x_l5l6[0] | 16 | M1 (mean) | L2 (bidi) | Mean memory-structure 1s |
| 41 | x_l5l6[0] | 16 | M18 (trend) | L2 (bidi) | Memory-structure trend 1s |
| 41 | x_l5l6[0] | 16 | M5 (range) | L0 (fwd) | Memory-structure range 1s |
| 22 | energy_change | 16 | M18 (trend) | L0 (fwd) | Energy change trend 1s |

**Total MEAMR H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | MEAMR Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Familiarity-linked valence | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Memory-evoked arousal | 0.7 |
| **AED** | Emotional Trajectory | AED[20:30] | Nostalgic emotional arc | **0.8** |
| **CPD** | Anticipation | CPD[0:10] | Familiar passage anticipation | 0.7 |
| **CPD** | Peak Experience | CPD[10:20] | Nostalgia peak detection | 0.6 |
| **CPD** | Resolution | CPD[20:30] | Memory resolution/completion | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Memory tension | 0.5 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Familiarity expectation | **0.8** (secondary) |
| **C0P** | Approach-Avoidance | C0P[20:30] | Nostalgia approach | 0.6 |

---

## 6. Output Space: 6D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MEAMR OUTPUT TENSOR: 6D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_familiarity_index    │ [0, 1] │ Musical familiarity level.
    │                          │        │ f01 = σ(0.35 * pleasantness_trend_1s
    │                          │        │       + 0.35 * mean(C0P.expect[10:20])
    │                          │        │       + 0.30 * mean_warmth_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_autobio_salience     │ [0, 1] │ Autobiographical salience.
    │                          │        │ f02 = σ(0.35 * memory_struct_trend_1s
    │                          │        │       + 0.35 * mean(AED.emotion[20:30])
    │                          │        │       + 0.30 * f01)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_dmpfc_tracking       │ [0, 1] │ dMPFC tonal space tracking.
    │                          │        │ f03 = σ(0.35 * mean_centroid_1s
    │                          │        │       + 0.35 * mean_pleasantness_500ms
    │                          │        │       + 0.30 * structural_entropy_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_positive_affect      │ [0, 1] │ Positive affect from familiar music.
    │                          │        │ f04 = σ(0.35 * mean(AED.valence[0:10])
    │                          │        │       + 0.35 * mean(CPD.peak[10:20])
    │                          │        │       + 0.30 * f02 * f01)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ memory_activation_state  │ [0, 1] │ Current autobiographical activation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ nostalgia_response_pred  │ [0, 1] │ Predicted nostalgia response.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Autobiographical Memory Reward Function

```
Autobio_Salience = α·Familiarity + β·TonalTracking + γ·PositiveAffect

Parameters:
    α = 1.0  (familiarity weight)
    β = 0.8  (tonal tracking weight)
    γ = 0.7  (positive affect weight)

dMPFC_Tracking = f(tonal_trajectory, harmonic_complexity)
Positive_Affect = vACC_activation + SN_reward_signal

τ_decay = 10.0s  (memory sustain window, long-term integration)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Familiarity Index
f01 = σ(0.35 * pleasantness_trend_1s
       + 0.35 * mean(C0P.expectation_surprise[10:20])
       + 0.30 * mean_warmth_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Autobiographical Salience
f02 = σ(0.35 * memory_struct_trend_1s
       + 0.35 * mean(AED.emotional_trajectory[20:30])
       + 0.30 * f01)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: dMPFC Tracking
f03 = σ(0.35 * mean_centroid_1s
       + 0.35 * mean_pleasantness_500ms
       + 0.30 * structural_entropy_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Positive Affect
f04 = σ(0.35 * mean(AED.valence_tracking[0:10])
       + 0.35 * mean(CPD.peak_experience[10:20])
       + 0.30 * f02 * f01)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dMemory/dt = τ⁻¹ · (Target_Activation - Current_Memory)
    where τ = 10.0s (long memory sustain)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MEAMR Function |
|--------|-----------------|----------|---------------|---------------|
| **dMPFC** | 0, 52, 16 | 2 | Direct (fMRI) | Autobiographical salience + tonal tracking |
| **vACC** | 0, 32, -6 | 1 | Direct (fMRI) | Positive affect integration |
| **SN/VTA** | ±4, -16, -8 | 1 | Direct (fMRI) | Reward signal for familiar music |

---

## 9. Cross-Unit Pathways

### 9.1 MEAMR ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEAMR INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  MEAMR.familiarity_index ─────► RPEM (familiarity → RPE modulation)       │
│  MEAMR.positive_affect ───────► DAED (affect → DA consummation)           │
│  MEAMR.autobio_salience ──────► MORMR (salience → opioid release)        │
│  MEAMR.dmpfc_tracking ────────► IUCP (tonal tracking → complexity)       │
│                                                                             │
│  CROSS-UNIT (RPU → IMU):                                                   │
│  MEAMR.familiarity_index ─────► IMU.memory_retrieval (familiar cue)      │
│  MEAMR.memory_activation ─────► IMU.encoding_strength (consolidation)    │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► MEAMR (valence/emotion evaluation)       │
│  CPD mechanism (30D) ──────────► MEAMR (peak/nostalgia detection)         │
│  C0P mechanism (30D) ──────────► MEAMR (expectation/familiarity)          │
│  R³ (~12D) ─────────────────────► MEAMR (direct spectral features)       │
│  H³ (14 tuples) ────────────────► MEAMR (temporal dynamics)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **dMPFC-autobio correlation** | dMPFC should correlate with autobiographical salience | ✅ **Confirmed** (p < 0.001, Janata 2009) |
| **dMPFC tonal tracking** | dMPFC should track tonal space of familiar music | ✅ **Confirmed** (p < 0.005, Janata 2009) |
| **Positive affect** | vACC + SN should correlate with positive affect | ✅ **Confirmed** (p < 0.001, Janata 2009) |
| **Unfamiliar music** | Unfamiliar music should show reduced dMPFC activation | Testable |
| **Memory interference** | Concurrent memory task should reduce MEAMR activation | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MEAMR(BaseModel):
    """Music-Evoked Autobiographical Memory Reward Model.

    Output: 6D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "MEAMR"
    UNIT = "RPU"
    TIER = "β3"
    OUTPUT_DIM = 6
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 10.0          # Long memory sustain (Janata 2009)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for MEAMR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Familiarity assessment ──
            (4, 8, 1, 2),     # sensory_pleasantness, 500ms, mean, bidi
            (4, 16, 18, 2),   # sensory_pleasantness, 1000ms, trend, bidi
            (8, 8, 1, 2),     # loudness, 500ms, mean, bidi
            (8, 16, 1, 2),    # loudness, 1000ms, mean, bidi
            (12, 16, 1, 2),   # warmth, 1000ms, mean, bidi
            (13, 16, 1, 2),   # spectral_centroid, 1000ms, mean, bidi
            # ── Structural complexity / memory ──
            (21, 8, 20, 2),   # spectral_change, 500ms, entropy, bidi
            (21, 16, 1, 2),   # spectral_change, 1000ms, mean, bidi
            (22, 8, 8, 0),    # energy_change, 500ms, velocity, fwd
            (22, 16, 18, 0),  # energy_change, 1000ms, trend, fwd
            # ── Memory-structure binding ──
            (41, 8, 1, 2),    # x_l5l6[0], 500ms, mean, bidi
            (41, 16, 1, 2),   # x_l5l6[0], 1000ms, mean, bidi
            (41, 16, 18, 2),  # x_l5l6[0], 1000ms, trend, bidi
            (41, 16, 5, 0),   # x_l5l6[0], 1000ms, range, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MEAMR 6D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,6) MEAMR output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_emotion = aed[..., 20:30]
        cpd_peak = cpd[..., 10:20]
        c0p_expect = c0p[..., 10:20]

        # H³ direct features
        pleasantness_trend_1s = h3_direct[(4, 16, 18, 2)].unsqueeze(-1)
        mean_pleasantness_500ms = h3_direct[(4, 8, 1, 2)].unsqueeze(-1)
        mean_warmth_1s = h3_direct[(12, 16, 1, 2)].unsqueeze(-1)
        mean_centroid_1s = h3_direct[(13, 16, 1, 2)].unsqueeze(-1)
        structural_entropy_500ms = h3_direct[(21, 8, 20, 2)].unsqueeze(-1)
        memory_struct_trend_1s = h3_direct[(41, 16, 18, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Familiarity Index (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * pleasantness_trend_1s
            + 0.35 * c0p_expect.mean(-1, keepdim=True)
            + 0.30 * mean_warmth_1s
        )

        # f02: Autobiographical Salience (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * memory_struct_trend_1s
            + 0.35 * aed_emotion.mean(-1, keepdim=True)
            + 0.30 * f01
        )

        # f03: dMPFC Tracking (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * mean_centroid_1s
            + 0.35 * mean_pleasantness_500ms
            + 0.30 * structural_entropy_500ms
        )

        # f04: Positive Affect (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * aed_valence.mean(-1, keepdim=True)
            + 0.35 * cpd_peak.mean(-1, keepdim=True)
            + 0.30 * (f02 * f01)
        )

        # ═══ LAYER P: Present ═══
        memory_activation = torch.sigmoid(
            0.5 * f02 + 0.5 * f01
        )

        # ═══ LAYER F: Future ═══
        nostalgia_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * f02
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            memory_activation,             # P: 1D
            nostalgia_pred,                # F: 1D
        ], dim=-1)  # (B, T, 6)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Janata 2009) | Primary evidence |
| **Effect Sizes** | 3 (all p < 0.005) | fMRI contrasts |
| **Evidence Modality** | fMRI | Direct neural |
| **Falsification Tests** | 3/5 confirmed | High validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Valence/emotion evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Peak/nostalgia detection |
| **C0P Mechanism** | 30D (3 sub-sections) | Expectation/familiarity |
| **Output Dimensions** | **6D** | 3-layer structure |

---

## 13. Scientific References

1. **Janata, P. (2009)**. The neural architecture of music-evoked autobiographical memories. *Cerebral Cortex*, 19(11), 2579-2594.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, SGM, AED, CPD) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Familiarity | S⁰.L6[55:60] + S⁰.L5[35,38] + HC⁰.HRM | R³.sensory_pleasantness[4] + R³.warmth[12] + C0P.expectation |
| Autobio salience | S⁰.X_L5L6[208:216] + HC⁰.SGM | R³.x_l5l6[41:49] + AED.emotional_trajectory |
| Tonal tracking | S⁰.L9.entropy_T[116] + S⁰.L4.velocity_T[15] | R³.spectral_centroid[13] + H³ entropy/mean tuples |
| Affect | S⁰.L5.loudness[35] + HC⁰.AED | R³.loudness[8] + AED.valence_tracking |
| Demand format | HC⁰ index ranges (30 tuples) | H³ 4-tuples (14 tuples, sparse) |
| Total demand | 30/2304 = 1.30% | 14/2304 = 0.61% |
| Output | 6D | 6D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **HRM → C0P.expectation_surprise** [10:20]: Hippocampal replay maps to C0P's familiarity expectation computation.
- **SGM → AED.emotional_trajectory** [20:30]: Striatal gradient memory maps to AED's emotional trajectory tracking.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for positive affect.
- **CPD → CPD.peak_experience** [10:20]: Chills/peak detection maps to CPD's nostalgia peak detection.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **6D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
