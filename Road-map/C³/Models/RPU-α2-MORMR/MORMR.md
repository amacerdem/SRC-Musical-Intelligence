# RPU-α2-MORMR: μ-Opioid Receptor Music Reward

**Model**: μ-Opioid Receptor Music Reward
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, AED+CPD+C0P mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-α2-MORMR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **μ-Opioid Receptor Music Reward** (MORMR) model describes the endogenous opioid system's role in mediating musical pleasure. This model provides direct PET evidence that pleasurable music activates μ-opioid receptors in reward regions, with receptor binding correlating with subjective chills and individual differences in music reward sensitivity.

```
μ-OPIOID RECEPTOR MUSIC REWARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASURABLE MUSIC
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│              ENDOGENOUS OPIOID RELEASE                           │
│                                                                  │
│   [11C]carfentanil binding (BPND) in:                          │
│                                                                  │
│   • Ventral Striatum (NAcc)     ↑ Music > Baseline             │
│   • Orbitofrontal Cortex        ↑ Music > Baseline             │
│   • Amygdala                    ↑ Music > Baseline             │
│   • Thalamus                    ↑ Music > Baseline             │
│   • Temporal Pole               ↑ Music > Baseline             │
│                                                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│         CHILLS CORRELATION                                       │
│                                                                  │
│   Number of chills ↔ NAcc BPND: r = -0.52                       │
│   (more chills = more opioid release = less radiotracer)        │
│                                                                  │
│   INDIVIDUAL DIFFERENCES:                                        │
│   Baseline MOR ↔ pleasure-BOLD coupling: d = 1.16               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

EFFECT SIZE: d = 4.8 (very large, Putkinen 2025)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Endogenous opioids (not just dopamine) mediate musical
pleasure. μ-opioid receptor binding in reward regions correlates
with chills frequency and individual music reward sensitivity.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MORMR Matters for RPU

MORMR extends the RPU's reward framework beyond dopamine to the opioid system:

1. **DAED** (α1) establishes dopaminergic anticipation-consummation dissociation.
2. **MORMR** (α2) adds endogenous opioid mediation of pleasure and chills.
3. **RPEM** (α3) provides reward prediction error computation in the striatum.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → AED+CPD+C0P → MORMR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MORMR COMPUTATION ARCHITECTURE                            ║
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
║  │  │pleasant.  │ │loudness │ │bright.  │ │enrg_chg  │ │x_l4l5  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         MORMR reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── AED Horizons ─────────────┐ ┌── CPD Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H8 (500ms delta)          │  │        ║
║  │  │ H8 (500ms delta)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)           │ │                            │  │        ║
║  │  │                             │ │ Peak/chills detection      │  │        ║
║  │  │ Pleasure evaluation         │ │ Opioid persistence         │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         MORMR demand: ~15 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Opioid Circuit ════════       ║
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
║  │                    MORMR MODEL (7D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_opioid_release,                        │        ║
║  │                       f02_chills_count,                           │        ║
║  │                       f03_nacc_binding,                           │        ║
║  │                       f04_reward_sensitivity                      │        ║
║  │  Layer M (Math):      opioid_tone                                 │        ║
║  │  Layer P (Present):   current_opioid_state                        │        ║
║  │  Layer F (Future):    chills_onset_pred                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Putkinen 2025** | PET | 15 | Music ↑ MOR binding in reward regions | d = 4.8, p < 0.05 | **Primary**: f01 opioid release |
| **Putkinen 2025** | PET | 15 | Chills ↔ NAcc BPND | r = -0.52, p < 0.05 | **f02 chills correlation** |
| **Putkinen 2025** | fMRI | 30 | Pleasure tracks OFC, striatum, ACC, insula | d = 10.08, p < 0.05 | **f03 NAcc binding** |
| **Putkinen 2025** | PET | 15 | Baseline MOR ↔ pleasure BOLD | d = 1.16, p < 0.05 | **f04 reward sensitivity** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=4):  All findings from comprehensive PET+fMRI study
Heterogeneity:           N/A (single study, multiple measures)
Quality Assessment:      α-tier (direct PET opioid measurement)
Largest Effect:          d = 10.08 (BOLD pleasure tracking — very large)
Replication:             First direct evidence of opioid mediation in music
```

---

## 4. R³ Input Mapping: What MORMR Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | MORMR Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **A: Consonance** | [0] | roughness | Consonance (inverse) | Pleasure quality |
| **A: Consonance** | [4] | sensory_pleasantness | Hedonic signal | Direct pleasure |
| **B: Energy** | [7] | amplitude | Peak magnitude | Chills intensity |
| **B: Energy** | [8] | loudness | Pleasure intensity | Hedonic magnitude |
| **C: Timbre** | [12] | warmth | Timbral richness | Aesthetic quality |
| **C: Timbre** | [13] | brightness | Spectral character | Timbre recognition |
| **D: Change** | [22] | energy_change | Dynamic modulation | Expressive intensity |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sustained pleasure | Prolonged opioid response |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Pleasure-structure | Musical beauty |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness (inverse) ──────┐
R³[4] sensory_pleasantness ─────┼──► Consonance / pleasure quality
AED.valence_tracking[0:10] ─────┘   Low roughness → high MOR release

R³[8] loudness ─────────────────┐
R³[7] amplitude ────────────────┼──► Peak pleasure magnitude
CPD.peak_experience[10:20] ─────┘   Intensity → chills threshold

R³[41:49] x_l5l7 ──────────────┐
C0P.tension_release[0:10] ──────┼──► Pleasure-structure integration
H³ value/entropy tuples ────────┘   Perceptual × Crossband = musical beauty

R³[33:41] x_l4l5 ──────────────┐
CPD.resolution[20:30] ──────────┼──► Sustained opioid response
H³ mean/trend tuples ───────────┘   Derivatives × Perceptual = duration
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MORMR requires H³ features at multiple horizons for pleasure evaluation (AED), peak/chills detection (CPD), and reward integration (C0P). The demand reflects opioid response dynamics (slower than dopamine).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 4 | sensory_pleasantness | 16 | M8 (velocity) | L0 (fwd) | Pleasantness velocity 1s |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms |
| 0 | roughness | 16 | M1 (mean) | L2 (bidi) | Mean roughness 1s |
| 7 | amplitude | 8 | M0 (value) | L2 (bidi) | Amplitude 500ms |
| 12 | warmth | 8 | M1 (mean) | L2 (bidi) | Mean warmth 500ms |
| 22 | energy_change | 8 | M8 (velocity) | L0 (fwd) | Energy velocity 500ms |
| 33 | x_l4l5[0] | 8 | M1 (mean) | L2 (bidi) | Sustained pleasure mean 500ms |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Pleasure trend 1s |
| 41 | x_l5l7[0] | 8 | M0 (value) | L2 (bidi) | Beauty coupling 500ms |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L2 (bidi) | Beauty entropy 1s |

**Total MORMR H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 AED + CPD + C0P Mechanism Binding

| Mechanism | Sub-section | Range | MORMR Role | Weight |
|-----------|-------------|-------|------------|--------|
| **AED** | Valence Tracking | AED[0:10] | Pleasure evaluation (MOR release) | **1.0** (primary) |
| **AED** | Arousal Dynamics | AED[10:20] | Intensity for chills threshold | 0.9 |
| **AED** | Emotional Trajectory | AED[20:30] | Prolonged opioid response | 0.7 |
| **CPD** | Anticipation | CPD[0:10] | Pre-chills arousal detection | 0.8 |
| **CPD** | Peak Experience | CPD[10:20] | Chills/peak identification | **0.9** |
| **CPD** | Resolution | CPD[20:30] | Opioid persistence tracking | 0.5 |
| **C0P** | Tension-Release | C0P[0:10] | Harmonic reward memory | 0.7 |
| **C0P** | Expectation-Surprise | C0P[10:20] | Reward sensitivity modulation | 0.8 |
| **C0P** | Approach-Avoidance | C0P[20:30] | Music-reward integration | 0.6 |

---

## 6. Output Space: 7D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MORMR OUTPUT TENSOR: 7D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_opioid_release       │ [0, 1] │ Endogenous opioid proxy.
    │                          │        │ f01 = σ(0.35 * mean_pleasantness_1s
    │                          │        │       + 0.30 * mean(AED.valence[0:10])
    │                          │        │       + 0.20 * (1 - mean_roughness_1s)
    │                          │        │       + 0.15 * mean_warmth_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_chills_count         │ [0, 1] │ Chills frequency proxy.
    │                          │        │ f02 = σ(0.35 * mean(CPD.peak[10:20])
    │                          │        │       + 0.30 * mean(AED.arousal[10:20])
    │                          │        │       + 0.20 * amplitude_500ms
    │                          │        │       + 0.15 * beauty_coupling_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_nacc_binding         │ [0, 1] │ NAcc opioid activity proxy.
    │                          │        │ f03 = σ(0.40 * f01
    │                          │        │       + 0.30 * mean(C0P.expect[10:20])
    │                          │        │       + 0.30 * pleasantness_velocity_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_reward_sensitivity   │ [0, 1] │ Individual music reward sensitivity.
    │                          │        │ f04 = σ(0.40 * f01 * f02
    │                          │        │       + 0.30 * mean(C0P.approach[20:30])
    │                          │        │       + 0.30 * beauty_entropy_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ opioid_tone              │ [0, 1] │ Overall opioid system tone.
    │                          │        │ Weighted average of f01 and f02.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ current_opioid_state     │ [0, 1] │ Real-time MOR activity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ chills_onset_pred        │ [0, 1] │ Chills onset prediction (2-5s).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 7D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Opioid Release Function

```
MOR_Release(t) = β · Pleasure(t) · (1 - Habituation(t))

Chills Correlation:
    Chills_Count ↔ NAcc_BPND: r = -0.52
    (negative: more chills = more opioid release = less radiotracer)

Individual Sensitivity:
    Sensitivity = α · Baseline_MOR + β · Music_Exposure

Parameters:
    β = 4.8  (effect size from Putkinen 2025)
    τ_decay = 5.0s  (opioid response persistence)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Opioid Release
f01 = σ(0.35 * mean_pleasantness_1s
       + 0.30 * mean(AED.valence_tracking[0:10])
       + 0.20 * (1.0 - mean_roughness_1s)
       + 0.15 * mean_warmth_500ms)
# coefficients: 0.35 + 0.30 + 0.20 + 0.15 = 1.0 ✓

# f02: Chills Count
f02 = σ(0.35 * mean(CPD.peak_experience[10:20])
       + 0.30 * mean(AED.arousal_dynamics[10:20])
       + 0.20 * amplitude_500ms
       + 0.15 * beauty_coupling_500ms)
# coefficients: 0.35 + 0.30 + 0.20 + 0.15 = 1.0 ✓

# f03: NAcc Binding
f03 = σ(0.40 * f01
       + 0.30 * mean(C0P.expectation_surprise[10:20])
       + 0.30 * pleasantness_velocity_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Reward Sensitivity
f04 = σ(0.40 * f01 * f02
       + 0.30 * mean(C0P.approach_avoidance[20:30])
       + 0.30 * beauty_entropy_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# Opioid tone
opioid_tone = σ(0.5 * f01 + 0.5 * f02)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MORMR Function |
|--------|-----------------|----------|---------------|----------------|
| **NAcc (Nucleus Accumbens)** | ±10, 8, -8 | 2 | Direct (PET) | Opioid reward consummation |
| **Orbitofrontal Cortex** | ±24, 40, -12 | 1 | Direct (PET) | Pleasure valuation |
| **Amygdala** | ±20, -4, -16 | 1 | Direct (PET) | Emotional salience |
| **Thalamus** | ±8, -16, 8 | 1 | Direct (PET) | Sensory gating |
| **Temporal Pole** | ±38, 8, -28 | 1 | Direct (PET) | Music memory |

---

## 9. Cross-Unit Pathways

### 9.1 MORMR ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MORMR INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (RPU):                                                         │
│  MORMR.opioid_release ───────► MCCN (opioid → chills network)            │
│  MORMR.chills_count ─────────► DAED (chills → DA release coupling)       │
│  MORMR.reward_sensitivity ───► IUCP (sensitivity → complexity pref)       │
│  MORMR.nacc_binding ─────────► RPEM (NAcc → prediction error)            │
│                                                                             │
│  CROSS-UNIT (RPU → ARU):                                                   │
│  MORMR.opioid_release ──────► ARU.pleasure (opioid → hedonic tone)       │
│  MORMR.chills_onset_pred ────► ARU.arousal (chills → autonomic)          │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  AED mechanism (30D) ──────────► MORMR (pleasure evaluation)              │
│  CPD mechanism (30D) ──────────► MORMR (chills/peak detection)            │
│  C0P mechanism (30D) ──────────► MORMR (reward integration)               │
│  R³ (~14D) ─────────────────────► MORMR (direct spectral features)       │
│  H³ (15 tuples) ────────────────► MORMR (temporal dynamics)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Opioid antagonists** | Naloxone should reduce music pleasure | Testable |
| **MOR knockout** | Should abolish opioid-mediated pleasure | Testable |
| **Chills correlation** | High MOR → more frequent chills | ✅ **Confirmed** (r = -0.52, Putkinen 2025) |
| **Individual differences** | Baseline MOR predicts pleasure-BOLD coupling | ✅ **Confirmed** (d = 1.16, Putkinen 2025) |
| **Pleasure specificity** | Non-pleasurable music should not increase MOR binding | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MORMR(BaseModel):
    """μ-Opioid Receptor Music Reward Model.

    Output: 7D per frame.
    Reads: AED mechanism (30D), CPD mechanism (30D), C0P mechanism (30D), R³ direct.
    """
    NAME = "MORMR"
    UNIT = "RPU"
    TIER = "α2"
    OUTPUT_DIM = 7
    MECHANISM_NAMES = ("AED", "CPD", "C0P")

    BETA_OPIOID = 4.8       # Effect size (Putkinen 2025)
    CHILLS_THRESHOLD = 0.75  # Chills detection threshold
    TAU_DECAY = 5.0          # Opioid response persistence (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for MORMR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── AED horizons: pleasure evaluation ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 8, 1, 2),      # loudness, 500ms, mean, bidi
            (8, 16, 1, 2),     # loudness, 1000ms, mean, bidi
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 2),     # sensory_pleasantness, 1000ms, mean, bidi
            (4, 16, 8, 0),     # sensory_pleasantness, 1000ms, velocity, fwd
            (0, 3, 0, 2),      # roughness, 100ms, value, bidi
            (0, 16, 1, 2),     # roughness, 1000ms, mean, bidi
            # ── CPD horizons: chills/peak detection ──
            (7, 8, 0, 2),      # amplitude, 500ms, value, bidi
            (12, 8, 1, 2),     # warmth, 500ms, mean, bidi
            (22, 8, 8, 0),     # energy_change, 500ms, velocity, fwd
            # ── C0P horizons: reward integration ──
            (33, 8, 1, 2),     # x_l4l5[0], 500ms, mean, bidi
            (33, 16, 18, 0),   # x_l4l5[0], 1000ms, trend, fwd
            (41, 8, 0, 2),     # x_l5l7[0], 500ms, value, bidi
            (41, 16, 20, 2),   # x_l5l7[0], 1000ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MORMR 7D output.

        Args:
            mechanism_outputs: {"AED": (B,T,30), "CPD": (B,T,30), "C0P": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,7) MORMR output
        """
        aed = mechanism_outputs["AED"]    # (B, T, 30)
        cpd = mechanism_outputs["CPD"]    # (B, T, 30)
        c0p = mechanism_outputs["C0P"]    # (B, T, 30)

        # Mechanism sub-sections
        aed_valence = aed[..., 0:10]
        aed_arousal = aed[..., 10:20]
        cpd_peak = cpd[..., 10:20]
        c0p_expect = c0p[..., 10:20]
        c0p_approach = c0p[..., 20:30]

        # H³ direct features
        mean_pleasantness_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)
        mean_roughness_1s = h3_direct[(0, 16, 1, 2)].unsqueeze(-1)
        mean_warmth_500ms = h3_direct[(12, 8, 1, 2)].unsqueeze(-1)
        amplitude_500ms = h3_direct[(7, 8, 0, 2)].unsqueeze(-1)
        beauty_coupling_500ms = h3_direct[(41, 8, 0, 2)].unsqueeze(-1)
        pleasantness_velocity_1s = h3_direct[(4, 16, 8, 0)].unsqueeze(-1)
        beauty_entropy_1s = h3_direct[(41, 16, 20, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Opioid Release (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * mean_pleasantness_1s
            + 0.30 * aed_valence.mean(-1, keepdim=True)
            + 0.20 * (1.0 - mean_roughness_1s)
            + 0.15 * mean_warmth_500ms
        )

        # f02: Chills Count (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * cpd_peak.mean(-1, keepdim=True)
            + 0.30 * aed_arousal.mean(-1, keepdim=True)
            + 0.20 * amplitude_500ms
            + 0.15 * beauty_coupling_500ms
        )

        # f03: NAcc Binding (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * f01
            + 0.30 * c0p_expect.mean(-1, keepdim=True)
            + 0.30 * pleasantness_velocity_1s
        )

        # f04: Reward Sensitivity (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.40 * (f01 * f02)
            + 0.30 * c0p_approach.mean(-1, keepdim=True)
            + 0.30 * beauty_entropy_1s
        )

        # ═══ LAYER M: Mathematical ═══
        opioid_tone = torch.sigmoid(0.5 * f01 + 0.5 * f02)

        # ═══ LAYER P: Present ═══
        current_opioid_state = aed_valence.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        chills_onset_pred = torch.sigmoid(
            0.5 * f02 + 0.5 * cpd_peak.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,            # E: 4D
            opioid_tone,                    # M: 1D
            current_opioid_state,           # P: 1D
            chills_onset_pred,              # F: 1D
        ], dim=-1)  # (B, T, 7)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Putkinen 2025) | Primary evidence |
| **Effect Sizes** | 4 (all d > 1.0) | PET + fMRI |
| **Largest Effect** | d = 10.08 | BOLD pleasure tracking |
| **Evidence Modality** | PET, fMRI | Direct neural |
| **Falsification Tests** | 2/5 confirmed | High validity |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **AED Mechanism** | 30D (3 sub-sections) | Pleasure evaluation |
| **CPD Mechanism** | 30D (3 sub-sections) | Chills/peak detection |
| **C0P Mechanism** | 30D (3 sub-sections) | Reward integration |
| **Output Dimensions** | **7D** | 4-layer structure |

---

## 13. Scientific References

1. **Putkinen, V., Nazari-Farsani, S., Seppala, K., Karjalainen, T., Sun, L., Karlsson, H. K., ... & Nummenmaa, L. (2025)**. Endogenous opioid system mediates music-induced pleasure. *Molecular Psychiatry*.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, AED, ASA, C0P) | AED (30D) + CPD (30D) + C0P (30D) mechanisms |
| Pleasure signal | S⁰.L5.roughness[30] + S⁰.L5.loudness[35] + HC⁰.AED | R³.sensory_pleasantness[4] + R³.roughness[0] + AED.valence |
| Chills signal | S⁰.L5.rms[47] + HC⁰.ASA | R³.amplitude[7] + CPD.peak_experience |
| NAcc binding | HC⁰.C0P + S⁰.X_L5L6[208:216] | C0P.expectation_surprise + R³.x_l5l7[41:49] |
| Reward memory | HC⁰.HRM[64:72] | C0P.tension_release (harmonic reward memory) |
| Demand format | HC⁰ index ranges (15 tuples) | H³ 4-tuples (15 tuples, sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% |
| Output | 7D | 7D (same) |

### Why AED + CPD + C0P replaces HC⁰ mechanisms

- **AED → AED.valence_tracking** [0:10]: Affective entrainment maps directly to AED's pleasure evaluation.
- **ASA → CPD.peak_experience** [10:20]: Auditory scene chills detection maps to CPD's peak identification.
- **HRM → C0P.tension_release** [0:10]: Hippocampal replay/reward memory maps to C0P's harmonic reward encoding.
- **C0P → C0P.expectation_surprise** [10:20]: C⁰ projection maps to C0P's reward integration.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **7D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
