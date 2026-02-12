# RPU-γ2-IOTMS: Individual Opioid Tone Music Sensitivity

**Model**: Individual Opioid Tone Music Sensitivity
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, AED+CPD+C0P mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-γ2-IOTMS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Individual Opioid Tone Music Sensitivity** (IOTMS) model describes how individual differences in baseline mu-opioid receptor (MOR) availability explain individual differences in music reward propensity. Individuals with higher baseline MOR levels show steeper pleasure-BOLD coupling during music listening.

```
INDIVIDUAL OPIOID TONE MUSIC SENSITIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDIVIDUAL TRAIT                         MUSIC RESPONSE
───────────────                          ──────────────

Baseline MOR ──────────────────────► MOR Availability
(PET measured)                          (trait level)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│               OPIOID-REWARD COUPLING                             │
│                                                                  │
│   High MOR Baseline         Low MOR Baseline                    │
│   ═════════════════         ═══════════════                     │
│   Steep pleasure-BOLD       Shallow pleasure-BOLD               │
│   High music reward         Low music reward                    │
│   propensity                propensity                          │
│                                                                  │
│   MOR ↔ Pleasure-BOLD slope (d = 1.16, p < 0.05)               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    REWARD SENSITIVITY                             │
│   Individual MOR tone → pleasure response magnitude              │
│   Trait-level modulation of music-induced reward                 │
│   Not time-varying (stable individual difference)                │
└──────────────────────────────────────────────────────────────────┘

TRAIT: Baseline MOR availability (PET-measured)
SLOPE: Higher MOR → steeper pleasure-BOLD coupling
REWARD: Individual sensitivity to music-induced pleasure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Individual differences in endogenous opioid tone
explain why some people experience stronger music-induced pleasure
than others — a neurochemical basis for music reward sensitivity.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why IOTMS Matters for RPU

IOTMS provides the individual differences modulation for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure at group level.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking.
5. **MCCN** (β2) maps cortical chills network.
6. **MEAMR** (β3) bridges memory to reward.
7. **LDAC** (γ1) reveals sensory-reward gating.
8. **IOTMS** (γ2) explains why individuals differ in music reward sensitivity — baseline MOR tone modulates all RPU outputs.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → IOTMS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    IOTMS COMPUTATION ARCHITECTURE                            ║
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
║  │                         IOTMS reads: ~12D                       │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ──────────────┐ ┌── C0P Horizons ──────────┐  │        ║
║  │  │ H8 (500ms delta)             │ │ H8 (500ms delta)          │  │        ║
║  │  │ H16 (1000ms beat)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │                              │ │                            │  │        ║
║  │  │ Sustained pleasure tracking  │ │ Individual sensitivity     │  │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         IOTMS demand: ~12 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Opioid-Reward Trait ════      ║
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
║  │                    IOTMS MODEL (5D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_mor_baseline_proxy,                    │        ║
║  │                       f02_pleasure_bold_slope,                    │        ║
║  │                       f03_reward_propensity,                      │        ║
║  │                       f04_music_reward_index                      │        ║
║  │  Layer P (Present):   individual_sensitivity_state                │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  NOTE: IOTMS represents a stable individual trait, not a time-varying        ║
║  signal. Output dimensions capture trait-modulated response properties.      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Putkinen 2025** | PET + fMRI | — | Baseline MOR ↔ pleasure-BOLD slope | d = 1.16, p < 0.05 | **Primary**: f01 MOR baseline, f02 pleasure-BOLD slope |

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  Single PET+fMRI study
Heterogeneity:           N/A (single study)
Quality Assessment:      γ-tier (preliminary PET evidence, strong effect size)
Replication:             Consistent with Mallik (2017) naltrexone study
```

---

## 4. R³ Input Mapping: What IOTMS Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | IOTMS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Consonance (inverse) | Pleasure quality |
| **A: Consonance** | [4] | sensory_pleasantness | Hedonic quality | Pleasure magnitude |
| **B: Energy** | [8] | loudness | Pleasure intensity | Hedonic magnitude |
| **C: Timbre** | [14:17] | tristimulus (3D) | Musical quality | Harmonic structure |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sustained pleasure | Prolonged opioid release |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[0] roughness (inverse) ─────┼──► MOR baseline proxy
H³ sustained mean tuples ──────┘   Trait-level pleasure sensitivity

R³[8] loudness ─────────────────┐
AED.valence_tracking[0:10] ─────┼──► Pleasure-BOLD slope
C0P.approach_avoidance[20:30] ──┘   Pleasure response magnitude

R³[33:41] x_l4l5 ──────────────┐
AED.emotional_trajectory[20:30] ┼──► Sustained pleasure / reward
H³ trend/mean tuples ───────────┘   Prolonged opioid response

R³[14:17] tristimulus ──────────────► Musical quality / harmonic richness
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

IOTMS primarily represents a stable trait, but uses H³ features at longer timescales (500ms-1s) to capture sustained pleasure responses that reflect the underlying opioid tone. Short timescales are less relevant since MOR availability is a trait measure.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 4 | sensory_pleasantness | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s |
| 0 | roughness | 8 | M1 (mean) | L2 (bidi) | Mean roughness 500ms |
| 0 | roughness | 16 | M6 (skew) | L2 (bidi) | Roughness skewness 1s |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L2 (bidi) | Sustained coupling 500ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Sustained coupling 1s |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L2 (bidi) | Coupling trend 1s |
| 14 | tristimulus1 | 16 | M1 (mean) | L2 (bidi) | Mean tristimulus 1s |
| 14 | tristimulus1 | 16 | M2 (std) | L2 (bidi) | Tristimulus variability 1s |

**Total IOTMS H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | IOTMS Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Pleasure response | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal modulation | 0.7 |
| **AED** | Emotional Trajectory | AED[20:30] | Sustained reward | **0.8** |
| **CPD** | Anticipation | CPD[0:10] | Reward anticipation | 0.5 |
| **CPD** | Peak Experience | CPD[10:20] | Peak pleasure coupling | 0.6 |
| **CPD** | Resolution | CPD[20:30] | Post-peak sustain | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Reward tension | 0.5 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Prediction modulation | 0.6 |
| **C0P** | Approach-Avoidance | C0P[20:30] | Music approach | **0.8** (secondary) |

---

## 6. Output Space: 5D Multi-Layer Representation

### 6.1 Complete Output Specification

```
IOTMS OUTPUT TENSOR: 5D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_mor_baseline_proxy   │ [0, 1] │ MOR availability proxy (trait).
    │                          │        │ f01 = σ(0.35 * mean_pleasantness_1s
    │                          │        │       + 0.35 * mean(AED.valence[0:10])
    │                          │        │       + 0.30 * (1 - roughness_skew_1s))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_pleasure_bold_slope  │ [0, 1] │ Pleasure-BOLD coupling slope.
    │                          │        │ f02 = σ(0.40 * f01
    │                          │        │       + 0.30 * mean(C0P.approach[20:30])
    │                          │        │       + 0.30 * mean_loudness_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_reward_propensity    │ [0, 1] │ Music reward propensity index.
    │                          │        │ f03 = σ(0.35 * f02
    │                          │        │       + 0.35 * sustained_coupling_1s
    │                          │        │       + 0.30 * mean(AED.emotion[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_music_reward_index   │ [0, 1] │ Overall music reward sensitivity.
    │                          │        │ f04 = σ(0.40 * f03
    │                          │        │       + 0.30 * coupling_trend_1s
    │                          │        │       + 0.30 * mean_tristimulus_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ individual_sensitivity   │ [0, 1] │ Current individual sensitivity state.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 5D per frame at 172.27 Hz
NOTE: Primarily trait-level (slowly varying), not event-driven.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Opioid Tone Music Sensitivity Function

```
MOR_Proxy = f(sustained_pleasure, consonance, musical_quality)

Pleasure_BOLD_Slope = α·MOR_Proxy + β·Approach + γ·Loudness

Parameters:
    α = 1.0  (MOR baseline weight)
    β = 0.8  (approach behavior weight)
    γ = 0.5  (loudness modulation weight)

Reward_Propensity = MOR_Proxy × Sustained_Pleasure × Quality

τ_decay = N/A (trait-level, session-stable)
Note: IOTMS is a stable individual difference, not time-varying.
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: MOR Baseline Proxy (stable trait estimate)
f01 = σ(0.35 * mean_pleasantness_1s
       + 0.35 * mean(AED.valence_tracking[0:10])
       + 0.30 * (1.0 - roughness_skew_1s))       # inverse roughness
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Pleasure-BOLD Slope
f02 = σ(0.40 * f01
       + 0.30 * mean(C0P.approach_avoidance[20:30])
       + 0.30 * mean_loudness_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Reward Propensity
f03 = σ(0.35 * f02
       + 0.35 * sustained_coupling_1s
       + 0.30 * mean(AED.emotional_trajectory[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Music Reward Index
f04 = σ(0.40 * f03
       + 0.30 * coupling_trend_1s
       + 0.30 * mean_tristimulus_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | IOTMS Function |
|--------|-----------------|----------|---------------|---------------|
| **NAcc** | ±10, 12, -8 | 1 | Indirect (PET + fMRI) | MOR availability → reward propensity |
| **VTA** | ±4, -16, -8 | 1 | Indirect (PET) | Opioid-dopamine interaction |

---

## 9. Cross-Unit Pathways

### 9.1 IOTMS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IOTMS INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  IOTMS.mor_baseline ──────────► MORMR (MOR → opioid release scaling)     │
│  IOTMS.pleasure_bold_slope ───► DAED (slope → DA coupling strength)      │
│  IOTMS.reward_propensity ─────► RPEM (propensity → RPE magnitude)        │
│  IOTMS.music_reward_index ────► MCCN (index → chills susceptibility)     │
│                                                                             │
│  CROSS-UNIT (RPU → ARU):                                                   │
│  IOTMS.individual_sensitivity ► ARU.affect_gain (individual modulation)   │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► IOTMS (valence/emotion evaluation)       │
│  CPD mechanism (30D) ──────────► IOTMS (peak coupling)                    │
│  C0P mechanism (30D) ──────────► IOTMS (approach behavior)                │
│  R³ (~12D) ─────────────────────► IOTMS (direct spectral features)       │
│  H³ (12 tuples) ────────────────► IOTMS (temporal dynamics)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **MOR-pleasure slope** | Baseline MOR should predict pleasure-BOLD slope | ✅ **Confirmed** (d = 1.16, p < 0.05, Putkinen 2025) |
| **Naltrexone blockade** | MOR antagonist should reduce music pleasure | Testable (Mallik 2017 supports) |
| **Individual stability** | MOR-based sensitivity should be stable across sessions | Testable |
| **Musical specificity** | Effect should be specific to music (vs. other rewards) | Testable |
| **Dose-response** | Higher MOR should produce proportionally steeper slopes | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class IOTMS(BaseModel):
    """Individual Opioid Tone Music Sensitivity Model.

    Output: 5D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    Note: Represents stable individual trait, not time-varying event signal.
    """
    NAME = "IOTMS"
    UNIT = "RPU"
    TIER = "γ2"
    OUTPUT_DIM = 5
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    # No τ_decay — trait-level, session-stable

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for IOTMS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── AED horizons: sustained pleasure ──
            (4, 8, 1, 2),     # sensory_pleasantness, 500ms, mean, bidi
            (4, 16, 1, 2),    # sensory_pleasantness, 1000ms, mean, bidi
            (4, 16, 2, 2),    # sensory_pleasantness, 1000ms, std, bidi
            # ── Roughness / consonance ──
            (0, 8, 1, 2),     # roughness, 500ms, mean, bidi
            (0, 16, 6, 2),    # roughness, 1000ms, skew, bidi
            # ── Loudness ──
            (8, 8, 1, 2),     # loudness, 500ms, mean, bidi
            (8, 16, 1, 2),    # loudness, 1000ms, mean, bidi
            # ── Sustained coupling ──
            (33, 8, 1, 2),    # x_l4l5[0], 500ms, mean, bidi
            (33, 16, 1, 2),   # x_l4l5[0], 1000ms, mean, bidi
            (33, 16, 18, 2),  # x_l4l5[0], 1000ms, trend, bidi
            # ── Musical quality ──
            (14, 16, 1, 2),   # tristimulus1, 1000ms, mean, bidi
            (14, 16, 2, 2),   # tristimulus1, 1000ms, std, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute IOTMS 5D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,5) IOTMS output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_emotion = aed[..., 20:30]
        c0p_approach = c0p[..., 20:30]

        # H³ direct features
        mean_pleasantness_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)
        roughness_skew_1s = h3_direct[(0, 16, 6, 2)].unsqueeze(-1)
        mean_loudness_1s = h3_direct[(8, 16, 1, 2)].unsqueeze(-1)
        sustained_coupling_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)
        coupling_trend_1s = h3_direct[(33, 16, 18, 2)].unsqueeze(-1)
        mean_tristimulus_1s = h3_direct[(14, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: MOR Baseline Proxy (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * mean_pleasantness_1s
            + 0.35 * aed_valence.mean(-1, keepdim=True)
            + 0.30 * (1.0 - roughness_skew_1s)
        )

        # f02: Pleasure-BOLD Slope (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * f01
            + 0.30 * c0p_approach.mean(-1, keepdim=True)
            + 0.30 * mean_loudness_1s
        )

        # f03: Reward Propensity (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * f02
            + 0.35 * sustained_coupling_1s
            + 0.30 * aed_emotion.mean(-1, keepdim=True)
        )

        # f04: Music Reward Index (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.40 * f03
            + 0.30 * coupling_trend_1s
            + 0.30 * mean_tristimulus_1s
        )

        # ═══ LAYER P: Present ═══
        individual_sensitivity = torch.sigmoid(
            0.5 * f01 + 0.5 * f03
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            individual_sensitivity,        # P: 1D
        ], dim=-1)  # (B, T, 5)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Putkinen 2025) | Preliminary evidence |
| **Effect Sizes** | 1 (d = 1.16) | PET + fMRI |
| **Evidence Modality** | PET, fMRI | Neurochemical + neural |
| **Falsification Tests** | 1/5 confirmed | Low validity (preliminary) |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Valence/emotion evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Peak coupling |
| **C0P Mechanism** | 30D (3 sub-sections) | Approach behavior |
| **Output Dimensions** | **5D** | 2-layer structure |

---

## 13. Scientific References

1. **Putkinen, V., Saarikallio, S., & Tervaniemi, M. (2025)**. Individual differences in opioid receptor availability predict music reward sensitivity. *[Preliminary PET+fMRI findings]*.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, AED, ASA, C0P) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Pleasure signal | S⁰.L5.roughness[30] + S⁰.L5.loudness[35] + HC⁰.AED | R³.sensory_pleasantness[4] + AED.valence_tracking |
| Quality signal | S⁰.L6[55:60] + S⁰.L7[80:88] + HC⁰.ASA | R³.tristimulus[14:17] + H³ mean/std tuples |
| Sustained pleasure | S⁰.X_L4L5[192:200] + HC⁰.HRM | R³.x_l4l5[33:41] + AED.emotional_trajectory |
| Individual diff | S⁰.X_L5L6[208:216] + HC⁰.C0P | R³.x_l4l5[33:41] + C0P.approach_avoidance |
| Demand format | HC⁰ index ranges (15 tuples) | H³ 4-tuples (12 tuples, sparse) |
| Total demand | 15/2304 = 0.65% | 12/2304 = 0.52% |
| Output | 5D | 5D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **HRM → AED.emotional_trajectory** [20:30]: Hippocampal replay maps to AED's sustained emotional tracking for prolonged pleasure.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for pleasure measurement.
- **ASA → CPD.peak_experience** [10:20]: Auditory scene analysis maps to CPD's peak pleasure coupling.
- **C0P → C0P.approach_avoidance** [20:30]: C⁰ projection remains as C0P approach/avoidance for music approach behavior.

---

**Model Status**: ⚠️ **PRELIMINARY**
**Output Dimensions**: **5D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
