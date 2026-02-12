# RPU-γ1-LDAC: Liking-Dependent Auditory Cortex

**Model**: Liking-Dependent Auditory Cortex
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, AED+CPD+C0P mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-γ1-LDAC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Liking-Dependent Auditory Cortex** (LDAC) model describes how auditory cortex (right STG) activity tracks moment-to-moment liking, suggesting pleasure-dependent modulation of sensory processing. Critically, the interaction between information content (IC) and liking shows that high IC combined with disliking produces the lowest STG activation.

```
LIKING-DEPENDENT AUDITORY CORTEX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACOUSTIC INPUT                           NEURAL RESPONSE
─────────────                            ───────────────

Musical Features ──────────────────► Auditory Processing
     │                                   (R STG tracking)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│               LIKING-DEPENDENT MODULATION                        │
│                                                                  │
│   R STG                    IC × LIKING INTERACTION               │
│   ═════                    ═══════════════════════                │
│   Tracks moment-           High IC + Disliked → LOWEST STG      │
│   to-moment liking         High IC + Liked → Normal STG         │
│   (d = 0.18, p < 0.018)   (d = 1.22, p < 0.008)               │
│                                                                  │
│   Sensory Processing                                             │
│   ═══════════════════                                            │
│   Pleasure gates sensory gain                                    │
│   Liked music → enhanced cortical response                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

LIKING: R STG continuously modulated by pleasure
IC × LIKING: Surprising + disliked = maximal sensory suppression
GATING: Pleasure-dependent sensory gain control

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Auditory cortex does not passively process sound —
pleasure actively modulates sensory gain, with the strongest
suppression when surprising events occur in disliked music.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why LDAC Matters for RPU

LDAC provides the sensory-reward gating mechanism for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking via inverted-U preference.
5. **MCCN** (β2) maps cortical network during chills.
6. **MEAMR** (β3) bridges memory to reward.
7. **LDAC** (γ1) reveals that pleasure feeds back to modulate sensory cortex — a top-down reward-to-perception pathway.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → LDAC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LDAC COMPUTATION ARCHITECTURE                             ║
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
║  │                         LDAC reads: ~13D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ──────────────┐ ┌── C0P Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)             │ │ H2 (75ms alpha)           │  │        ║
║  │  │ H8 (500ms delta)             │ │ H8 (500ms delta)          │  │        ║
║  │  │ H16 (1000ms beat)            │ │                            │  │        ║
║  │  │                              │ │ IC computation              │  │        ║
║  │  │ Continuous liking tracking   │ │ Surprise detection          │  │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         LDAC demand: ~12 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensory-Reward Gate ═════     ║
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
║  │                    LDAC MODEL (6D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_stg_liking_coupling,                   │        ║
║  │                       f02_pleasure_gating,                        │        ║
║  │                       f03_ic_liking_interaction,                   │        ║
║  │                       f04_moment_to_moment                        │        ║
║  │  Layer P (Present):   stg_modulation_state                        │        ║
║  │  Layer F (Future):    sensory_gating_pred                         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Gold 2023** | fMRI | — | R STG ↔ moment-to-moment liking | d = 0.18, p < 0.018 | **Primary**: f01 STG-liking coupling |
| **Gold 2023** | fMRI | — | High IC × disliked = lowest STG | d = 1.22, p < 0.008 | **f03 IC-liking interaction** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=2):  Both findings from single fMRI study
Heterogeneity:           N/A (single study)
Quality Assessment:      γ-tier (preliminary fMRI, moderate effect sizes)
Replication:             Consistent with reward modulation of sensory cortex
```

---

## 4. R³ Input Mapping: What LDAC Reads

### 4.1 R³ Feature Dependencies (~13D of 49D)

| R³ Group | Index | Feature | LDAC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Sensory quality (inverse) | Dissonance level |
| **A: Consonance** | [4] | sensory_pleasantness | Hedonic quality | Pleasure tracking |
| **B: Energy** | [8] | loudness | Sensory salience | Attention capture |
| **B: Energy** | [10] | spectral_flux | Musical deviation | Change detection |
| **C: Timbre** | [13] | spectral_centroid | Brightness | Timbre tracking |
| **D: Change** | [21] | spectral_change | Information content (IC) | Surprise level |
| **D: Change** | [22] | energy_change | Dynamic shift | Unexpected events |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Auditory gating proxy | STG modulation |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
AED.valence_tracking[0:10] ────┼──► STG liking coupling
H³ mean/trend tuples ──────────┘   Moment-to-moment pleasure tracking

R³[21] spectral_change ────────┐
R³[4] sensory_pleasantness ────┼──► IC × Liking interaction
C0P.expectation_surprise[10:20]┘   High IC + disliked → suppression

R³[8] loudness ─────────────────┐
R³[10] spectral_flux ───────────┼──► Sensory gating
AED.arousal_dynamics[10:20] ────┘   Pleasure-modulated gain control

R³[25:33] x_l0l5 ──────────────────► Auditory cortex gating proxy
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

LDAC requires H³ features at short-to-mid timescales for continuous liking tracking (100-500ms) and IC computation (75ms for surprise detection). The rapid feedback loop from reward to sensory cortex demands fast temporal resolution.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms |
| 4 | sensory_pleasantness | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |
| 21 | spectral_change | 2 | M0 (value) | L0 (fwd) | IC at 75ms (surprise detection) |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | IC velocity at 500ms |
| 21 | spectral_change | 16 | M20 (entropy) | L2 (bidi) | IC entropy over 1s |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Spectral flux at 100ms |
| 10 | spectral_flux | 8 | M2 (std) | L2 (bidi) | Flux variability 500ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Auditory gating at 100ms |
| 25 | x_l0l5[0] | 16 | M20 (entropy) | L2 (bidi) | Gating entropy over 1s |

**Total LDAC H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | LDAC Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **AED** | Valence Tracking | AED[0:10] | Moment-to-moment liking | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Arousal-dependent gating | **0.8** |
| **AED** | Emotional Trajectory | AED[20:30] | Emotional context | 0.5 |
| **CPD** | Anticipation | CPD[0:10] | Anticipatory gating | 0.5 |
| **CPD** | Peak Experience | CPD[10:20] | Peak-related STG modulation | 0.6 |
| **CPD** | Resolution | CPD[20:30] | Post-peak sensory return | 0.4 |
| **C0P** | Tension-Release | C0P[0:10] | Tension gating | 0.5 |
| **C0P** | Expectation-Surprise | C0P[10:20] | IC computation | **0.8** (secondary) |
| **C0P** | Approach-Avoidance | C0P[20:30] | Sensory approach/avoid | 0.7 |

---

## 6. Output Space: 6D Multi-Layer Representation

### 6.1 Complete Output Specification

```
LDAC OUTPUT TENSOR: 6D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_stg_liking_coupling  │ [0, 1] │ R STG tracks moment-to-moment liking.
    │                          │        │ f01 = σ(0.35 * pleasantness_100ms
    │                          │        │       + 0.35 * mean(AED.valence[0:10])
    │                          │        │       + 0.30 * mean_pleasantness_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_pleasure_gating      │ [0, 1] │ Pleasure gates sensory gain.
    │                          │        │ f02 = σ(0.35 * f01
    │                          │        │       + 0.35 * mean(AED.arousal[10:20])
    │                          │        │       + 0.30 * loudness_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_ic_liking_interact   │ [0, 1] │ IC × Liking interaction.
    │                          │        │ f03 = σ(0.35 * ic_75ms * (1 - f01)
    │                          │        │       + 0.35 * mean(C0P.expect[10:20])
    │                          │        │       + 0.30 * ic_entropy_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_moment_to_moment     │ [0, 1] │ Continuous tracking signal.
    │                          │        │ f04 = σ(0.40 * f01
    │                          │        │       + 0.30 * f02
    │                          │        │       + 0.30 * spectral_flux_100ms)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ stg_modulation_state     │ [0, 1] │ Current STG modulation level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ sensory_gating_pred      │ [0, 1] │ Predicted sensory gating state.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Liking-Dependent Sensory Modulation Function

```
STG_Modulation = α·Liking + β·IC_interaction + γ·Arousal_gating

Parameters:
    α = 1.0  (liking coupling weight)
    β = 0.8  (IC interaction weight)
    γ = 0.5  (arousal gating weight)

IC_Liking_Interaction:
    High IC + Disliked → Lowest STG (suppression, d = 1.22)
    High IC + Liked → Normal STG
    Low IC → Liking-independent

τ_decay = 0.5s  (rapid continuous tracking, Gold 2023)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: STG Liking Coupling
f01 = σ(0.35 * pleasantness_100ms
       + 0.35 * mean(AED.valence_tracking[0:10])
       + 0.30 * mean_pleasantness_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Pleasure Gating
f02 = σ(0.35 * f01
       + 0.35 * mean(AED.arousal_dynamics[10:20])
       + 0.30 * loudness_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: IC × Liking Interaction (high IC + disliked → high f03 = suppression)
f03 = σ(0.35 * ic_75ms * (1.0 - f01)        # IC × inverse liking
       + 0.35 * mean(C0P.expectation_surprise[10:20])
       + 0.30 * ic_entropy_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Moment-to-Moment Tracking
f04 = σ(0.40 * f01
       + 0.30 * f02
       + 0.30 * spectral_flux_100ms)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# Temporal dynamics
dSTG/dt = τ⁻¹ · (Target_Modulation - Current_STG)
    where τ = 0.5s (rapid tracking)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | LDAC Function |
|--------|-----------------|----------|---------------|---------------|
| **R STG** | 52, -22, 8 | 2 | Direct (fMRI) | Liking-dependent modulation + IC interaction |

---

## 9. Cross-Unit Pathways

### 9.1 LDAC ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LDAC INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  LDAC.stg_liking_coupling ────► RPEM (liking → RPE modulation)            │
│  LDAC.ic_liking_interaction ──► IUCP (IC×liking → preference surface)     │
│  LDAC.pleasure_gating ────────► MORMR (gating → opioid modulation)       │
│  LDAC.moment_to_moment ──────► DAED (tracking → DA anticipation)         │
│                                                                             │
│  CROSS-UNIT (RPU → ASU):                                                   │
│  LDAC.stg_modulation ────────► ASU.sensory_gain (auditory processing)     │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► LDAC (valence/arousal evaluation)        │
│  CPD mechanism (30D) ──────────► LDAC (peak-related modulation)           │
│  C0P mechanism (30D) ──────────► LDAC (IC/expectation computation)        │
│  R³ (~13D) ─────────────────────► LDAC (direct spectral features)        │
│  H³ (12 tuples) ────────────────► LDAC (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **STG-liking coupling** | R STG should track moment-to-moment liking | ✅ **Confirmed** (d = 0.18, p < 0.018, Gold 2023) |
| **IC × disliking** | High IC + disliked should produce lowest STG | ✅ **Confirmed** (d = 1.22, p < 0.008, Gold 2023) |
| **Liked music enhancement** | Liked music should show enhanced STG response | Testable |
| **Attention control** | Active vs. passive listening should modulate effect | Testable |
| **Causal direction** | Disrupting reward should reduce STG modulation | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class LDAC(BaseModel):
    """Liking-Dependent Auditory Cortex Model.

    Output: 6D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "LDAC"
    UNIT = "RPU"
    TIER = "γ1"
    OUTPUT_DIM = 6
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    TAU_DECAY = 0.5           # Rapid continuous tracking (Gold 2023)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for LDAC computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── AED horizons: liking tracking ──
            (4, 3, 0, 2),     # sensory_pleasantness, 100ms, value, bidi
            (4, 8, 1, 2),     # sensory_pleasantness, 500ms, mean, bidi
            (4, 16, 2, 2),    # sensory_pleasantness, 1000ms, std, bidi
            # ── Sensory features ──
            (8, 3, 0, 2),     # loudness, 100ms, value, bidi
            (8, 16, 1, 2),    # loudness, 1000ms, mean, bidi
            # ── C0P horizons: IC computation ──
            (21, 2, 0, 0),    # spectral_change, 75ms, value, fwd
            (21, 8, 8, 0),    # spectral_change, 500ms, velocity, fwd
            (21, 16, 20, 2),  # spectral_change, 1000ms, entropy, bidi
            # ── Spectral flux / deviation ──
            (10, 3, 0, 2),    # spectral_flux, 100ms, value, bidi
            (10, 8, 2, 2),    # spectral_flux, 500ms, std, bidi
            # ── Auditory gating ──
            (25, 3, 0, 2),    # x_l0l5[0], 100ms, value, bidi
            (25, 16, 20, 2),  # x_l0l5[0], 1000ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute LDAC 6D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,6) LDAC output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_arousal = aed[..., 10:20]
        c0p_expect = c0p[..., 10:20]

        # H³ direct features
        pleasantness_100ms = h3_direct[(4, 3, 0, 2)].unsqueeze(-1)
        mean_pleasantness_500ms = h3_direct[(4, 8, 1, 2)].unsqueeze(-1)
        loudness_100ms = h3_direct[(8, 3, 0, 2)].unsqueeze(-1)
        ic_75ms = h3_direct[(21, 2, 0, 0)].unsqueeze(-1)
        ic_entropy_1s = h3_direct[(21, 16, 20, 2)].unsqueeze(-1)
        spectral_flux_100ms = h3_direct[(10, 3, 0, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: STG Liking Coupling (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * pleasantness_100ms
            + 0.35 * aed_valence.mean(-1, keepdim=True)
            + 0.30 * mean_pleasantness_500ms
        )

        # f02: Pleasure Gating (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * f01
            + 0.35 * aed_arousal.mean(-1, keepdim=True)
            + 0.30 * loudness_100ms
        )

        # f03: IC × Liking Interaction (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * (ic_75ms * (1.0 - f01))
            + 0.35 * c0p_expect.mean(-1, keepdim=True)
            + 0.30 * ic_entropy_1s
        )

        # f04: Moment-to-Moment (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.40 * f01
            + 0.30 * f02
            + 0.30 * spectral_flux_100ms
        )

        # ═══ LAYER P: Present ═══
        stg_modulation = torch.sigmoid(
            0.5 * f04 + 0.5 * f02
        )

        # ═══ LAYER F: Future ═══
        sensory_gating_pred = torch.sigmoid(
            0.5 * f01 + 0.5 * f03
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            stg_modulation,                # P: 1D
            sensory_gating_pred,           # F: 1D
        ], dim=-1)  # (B, T, 6)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Gold 2023) | Preliminary evidence |
| **Effect Sizes** | 2 (d = 0.18, d = 1.22) | fMRI contrasts |
| **Evidence Modality** | fMRI | Direct neural |
| **Falsification Tests** | 2/5 confirmed | Moderate validity |
| **R³ Features Used** | ~13D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Valence/arousal evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Peak-related modulation |
| **C0P Mechanism** | 30D (3 sub-sections) | IC/expectation computation |
| **Output Dimensions** | **6D** | 3-layer structure |

---

## 13. Scientific References

1. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2023)**. Liking-dependent modulation of auditory cortex activity. *[Preliminary fMRI findings]*.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, EFC, AED, ASA) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Liking signal | S⁰.L5.loudness[35] + S⁰.L5.centroid[38] + HC⁰.AED | R³.sensory_pleasantness[4] + AED.valence_tracking |
| IC signal | S⁰.L9.entropy_T[116] + HC⁰.EFC | R³.spectral_change[21] + C0P.expectation_surprise |
| Sensory gating | S⁰.L0[0:4] + S⁰.X_L0L1[128:136] + HC⁰.ATT | R³.x_l0l5[25:33] + AED.arousal_dynamics |
| Deviation | S⁰.L5.spectral_flux[45] + HC⁰.ASA | R³.spectral_flux[10] + H³ std tuples |
| Demand format | HC⁰ index ranges (15 tuples) | H³ 4-tuples (12 tuples, sparse) |
| Total demand | 15/2304 = 0.65% | 12/2304 = 0.52% |
| Output | 6D | 6D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **ATT → AED.arousal_dynamics** [10:20]: Attentional entrainment maps to AED's arousal-dependent sensory gating.
- **EFC → C0P.expectation_surprise** [10:20]: Efference copy prediction maps to C0P's IC computation for surprise.
- **AED → AED.valence_tracking** [0:10]: Affective entrainment remains as AED valence for liking tracking.
- **ASA → CPD.peak_experience** [10:20]: Auditory scene analysis maps to CPD's peak-related STG modulation.

---

**Model Status**: ⚠️ **PRELIMINARY**
**Output Dimensions**: **6D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
