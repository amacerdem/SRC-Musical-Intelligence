# ASU-α3-CSG: Consonance-Salience Gradient

**Model**: Consonance-Salience Gradient
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-α3-CSG.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Consonance-Salience Gradient** (CSG) model describes how dissonance level systematically modulates salience network activation. Strong dissonance activates ACC/insula (salience network), intermediate dissonance increases sensory processing demands in Heschl's gyrus, and consonance enables efficient processing with positive valence.

```
CONSONANCE-SALIENCE GRADIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           CONSONANCE LEVEL
  Consonant ◄─────────────────────────────────► Strong Dissonance

  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │  CONSONANT  │    │INTERMEDIATE │    │   STRONG    │
  │  (Octave,   │    │ DISSONANCE  │    │ DISSONANCE  │
  │   Fifth)    │    │ (m3, dim)   │    │  (Tritone)  │
  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
         │                  │                   │
         ▼                  ▼                   ▼
  Low Processing     Heschl's Gyrus ↑    ACC + Bilateral AI
  Demand             (sensory evidence)   (SALIENCE NETWORK)
                     d = 1.9              d = 5.16

  RT: 4333ms         RT: 6792ms          RT: moderate
  Valence: +3.5      Valence: ~5.7       Valence: -6.8
                     (ambiguous)         (negative)

  AESTHETIC EFFECT:
  Consonant > Dissonant for appreciation (p<0.001, d=2.008)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Dissonance drives salience network activation with a
graded response: strong dissonance → ACC/AI, intermediate →
Heschl's gyrus, consonance → efficient processing + positive valence.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why CSG Matters for ASU

CSG completes the α-tier salience triad by linking consonance to affective evaluation:

1. **SNEM** (α1) provides beat/meter entrainment baseline for temporal salience.
2. **IACM** (α2) extends salience to spectral complexity (inharmonicity-driven attention capture).
3. **CSG** (α3) links salience to consonance gradients and affective evaluation.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → CSG)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CSG COMPUTATION ARCHITECTURE                              ║
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
║  │  │sethares   │ │loudness │ │tonalness│ │enrg_chg  │ │x_l4l5  │ │        ║
║  │  │pleasantns │ │spec_cent│ │sharpness│ │          │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         CSG reads: ~16D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H3 (100ms alpha)           │ │ H8 (500ms delta)          │  │        ║
║  │  │ H4 (125ms theta)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │ Salience evaluation        │  │        ║
║  │  │ Consonance tracking         │ │ Affective dynamics         │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         CSG demand: ~18 of 2304 tuples           │        ║
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
║  │                    CSG MODEL (12D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f07_salience_activation,                   │        ║
║  │                       f08_sensory_evidence,                      │        ║
║  │                       f09_consonance_valence                      │        ║
║  │  Layer M (Math):      salience_response,                          │        ║
║  │                       rt_valence_judgment, aesthetic_appreciation  │        ║
║  │  Layer P (Present):   salience_network, affective_eval,          │        ║
║  │                       sensory_load                                │        ║
║  │  Layer F (Future):    valence_pred, processing_pred,             │        ║
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
| **Bravo 2017** | fMRI | 45 | Intermediate: RT=6792ms vs consonant 4333ms | d = 2458 (RT diff), p < 0.016 | **f08 sensory evidence** |
| **Bravo 2017** | fMRI | 12 | Intermediate → R.Heschl's gyrus | d = 1.9, p < 0.033 FWE | **f08 sensory evidence** |
| **Bravo 2017** | fMRI | 12 | Strong dissonance → ACC, bilateral AI | d = 5.16, p < 0.05 | **f07 salience activation** |
| **Bravo 2017** | fMRI | 45 | Linear consonance-valence trend | d = 3.31, p < 0.01 | **f09 consonance-valence** |
| **Sarasso 2019** | EEG | 22 | Consonant > dissonant appreciation | d = 2.008, p < 0.001 | **Aesthetic appreciation** |
| **Fishman et al.** | AEP/ECoG | 3+2 | Phase-locked activity in A1/Heschl's graded by consonance-dissonance | significant | **Direct cortical graded response** |
| **Foo et al. 2016** | ECoG | 8 | Dissonant chords → enhanced high gamma in STG, 75-200ms | p < 0.001 | **STG differential processing** |
| **Wöhrle et al.** | MEG | 30 | N1m graded by consonance/dissonance within chord progressions | significant | **MEG graded salience** |
| **Koelsch et al.** | fMRI | 11 | Dissonant → amygdala/hippocampus; consonant → anterior insula/Heschl's/ventral striatum | significant | **Full salience gradient circuit** |
| **Kim et al.** | fMRI | — | Dissonance → ↓ STG/insula BOLD; vmPFC/NAc interaction | significant | **Spectral-temporal reward integration** |
| **Cheung et al.** | fMRI | 79 | Amygdala/hippocampus reflect uncertainty×surprise; NAc reflects uncertainty | significant | **Salience integration for harmonic expectancy** |
| **Musical chills EEG** | HD-EEG | 18 | Theta in OFC graded by pleasure; SMA engagement | significant | **Aesthetic appreciation neural correlate** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12): 12 papers with converging multi-method evidence
Salience activation:     d = 5.16 (ACC/AI, Bravo 2017)
Sensory processing:      d = 1.9 (Heschl's, Bravo 2017)
Valence mapping:         d = 3.31 (consonance-valence, Bravo 2017)
Aesthetic preference:    d = 2.008 (Sarasso 2019)
Cortical phase-locking:  Graded across consonance-dissonance (Fishman, Foo, Wöhrle)
Quality Assessment:      α-tier (direct fMRI/EEG/ECoG/MEG measurement)
Replication:             Multi-species (monkey+human), multi-method convergence
```

---

## 4. R³ Input Mapping: What CSG Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | CSG Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance (inverse consonance) | Plomp-Levelt critical bandwidth |
| **A: Consonance** | [1] | sethares | Alternative consonance metric | Sethares beating model |
| **A: Consonance** | [4] | sensory_pleasantness | Consonance level | Direct pleasantness |
| **B: Energy** | [7] | amplitude | Intensity | Physical arousal basis |
| **B: Energy** | [8] | loudness | Arousal correlate | Stevens intensity perception |
| **B: Energy** | [9] | spectral_centroid | Brightness | Timbral salience |
| **C: Timbre** | [12] | warmth | Spectral envelope quality | Harmonic structure |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Processing demand |
| **D: Change** | [22] | energy_change | Energy dynamics | Arousal change |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Salience integration | Multi-feature binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | CSG Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **F: Pitch** | [62] | pitch_class_entropy | Tonal diversity measure | Information theory: entropy over pitch-class distribution quantifies consonance ambiguity — high entropy signals complex harmonic contexts that modulate CSG's salience gradient |

**Rationale**: CSG links consonance to salience via roughness [0], sethares [1], and sensory_pleasantness [4]. These v1 features capture sensory consonance but not distributional tonal complexity. pitch_class_entropy [62] adds an information-theoretic dimension: when pitch classes are uniformly distributed (high entropy), consonance judgments become ambiguous, increasing the salience gradient slope. This complements existing A-group features without redundancy.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness ────────────────┐
R³[1] sethares ─────────────────┼──► Dissonance (inverse = consonance)
R³[4] sensory_pleasantness ────┘   High roughness → dissonant → salience↑

R³[8] loudness ─────────────────┐
R³[7] amplitude ────────────────┼──► Arousal component
ASA.salience_weighting[20:30] ─┘   Intensity → emotional activation

R³[12] warmth ──────────────────┐
R³[9] spectral_centroid ───────┼──► Harmonic structure quality
BEP.beat_entrainment[0:10] ───┘   Interval identity for consonance

R³[25:33] x_l0l5 ──────────────┐
ASA.attention_gating[10:20] ───┼──► Integrated salience signal
H³ entropy/velocity tuples ────┘   Perceptual × feature = holistic assessment
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

CSG requires H³ features at BEP horizons for consonance tracking and ASA horizons for salience evaluation and affective dynamics. The demand reflects the integration of consonance over multiple time scales for graded salience response.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Instantaneous roughness at 25ms |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Mean roughness over 100ms |
| 0 | roughness | 3 | M2 (std) | L2 (bidi) | Roughness variability 100ms |
| 0 | roughness | 16 | M1 (mean) | L2 (bidi) | Mean roughness over 1s |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 4 | sensory_pleasantness | 3 | M8 (velocity) | L2 (bidi) | Pleasantness velocity 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness over 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |
| 1 | sethares | 3 | M0 (value) | L2 (bidi) | Sethares dissonance 100ms |
| 1 | sethares | 8 | M8 (velocity) | L0 (fwd) | Sethares velocity 500ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Spectral change velocity 125ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Salience coupling 100ms |
| 25 | x_l0l5[0] | 8 | M0 (value) | L2 (bidi) | Salience coupling 500ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean salience coupling 1s |
| 22 | energy_change | 3 | M8 (velocity) | L0 (fwd) | Energy change velocity 100ms |
| 9 | spectral_centroid | 3 | M0 (value) | L2 (bidi) | Brightness at 100ms |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

CSG is projected to consume R³ v2 features from F[49:65], aligned with BEP+ASA horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 64 | inharmonicity | F | 0 | M0 (value) | L2 | v2 inharmonicity for graded salience at 25ms |
| 64 | inharmonicity | F | 3 | M0 (value) | L2 | Inharmonicity at 100ms for consonance grading |
| 64 | inharmonicity | F | 8 | M0 (value) | L2 | Inharmonicity at 500ms for sustained assessment |

**v2 projected**: 3 tuples
**Total projected**: 21 tuples of 294,912 theoretical = 0.0071%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | CSG Role | Weight |
|-----------|-------------|-------|----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Harmonic structure context | 0.5 |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor valence | 0.3 |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic context for consonance | 0.2 |
| **ASA** | Scene Analysis | ASA[0:10] | Consonance-in-scene assessment | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Salience detection for dissonance | **1.0** |
| **ASA** | Salience Weighting | ASA[20:30] | Consonance-affective weighting | **0.9** |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
CSG OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼────────────────────────────────────
 0  │ f07_salience_activation  │ [0, 1]  │ ACC/AI activation level.
    │                          │         │ f07 = σ(0.40 * (1-consonance)
    │                          │         │       + 0.35 * mean(ASA.attn[10:20])
    │                          │         │       + 0.25 * loudness_entropy)
────┼──────────────────────────┼─────────┼────────────────────────────────────
 1  │ f08_sensory_evidence     │ [0, 1]  │ Heschl's gyrus processing load.
    │                          │         │ f08 = σ(0.40 * ambiguity
    │                          │         │       + 0.35 * mean(ASA.scene[0:10])
    │                          │         │       + 0.25 * roughness_std)
────┼──────────────────────────┼─────────┼────────────────────────────────────
 2  │ f09_consonance_valence   │ [-1, 1] │ Linear consonance-valence mapping.
    │                          │         │ f09 = tanh(0.50 * pleasantness_vel
    │                          │         │       + 0.50 * pleasantness_mean_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼────────────────────────────────────
 3  │ salience_response        │ [0, 1]  │ Graded salience network response.
────┼──────────────────────────┼─────────┼────────────────────────────────────
 4  │ rt_valence_judgment      │ [0, 1]  │ Inverted-U RT function.
────┼──────────────────────────┼─────────┼────────────────────────────────────
 5  │ aesthetic_appreciation   │ [0, 1]  │ Consonance preference index.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼────────────────────────────────────
 6  │ salience_network         │ [0, 1]  │ ASA attention-gated salience.
────┼──────────────────────────┼─────────┼────────────────────────────────────
 7  │ affective_evaluation     │ [-1, 1] │ ASA salience-weighted valence.
────┼──────────────────────────┼─────────┼────────────────────────────────────
 8  │ sensory_load             │ [0, 1]  │ BEP oscillatory processing load.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼────────────────────────────────────
 9  │ valence_pred_1.5s        │ [-1, 1] │ Behavioral valence prediction.
────┼──────────────────────────┼─────────┼────────────────────────────────────
10  │ processing_pred_0.75s    │ [0, 1]  │ Heschl's load prediction.
────┼──────────────────────────┼─────────┼────────────────────────────────────
11  │ aesthetic_pred_3s        │ [0, 1]  │ Appreciation prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Salience Response Function

```
Salience_Response(consonance) =
    if consonance < threshold_low (0.3):
        Salience_Network(ACC, AI) → HIGH ACTIVATION (d = 5.16)
    elif threshold_low ≤ c < threshold_high (0.7):
        Sensory_Cortex(Heschl) → INCREASED PROCESSING (d = 1.9)
    else:
        Baseline_Processing → EFFICIENT

RT(valence_judgment) ∝ |consonance - midpoint|⁻¹
    RT_consonant = 4333ms, RT_intermediate = 6792ms

Valence(consonance) = a · consonance + b
    Consonant: +3.5, Ambiguous: ~5.7, Dissonant: -6.8

Aesthetic_Appreciation = β · consonance + ε
    Consonant > Dissonant: d = 2.008, p < 0.001
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f07: Salience Activation
consonance = sensory_pleasantness_value  # R³[4]
dissonance = 1.0 - consonance
f07 = σ(0.40 * dissonance
       + 0.35 * mean(ASA.attention_gating[10:20])
       + 0.25 * loudness_entropy)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f08: Sensory Evidence (inverted-U)
ambiguity = 1.0 - |consonance - 0.5| * 2  # peaks at 0.5
f08 = σ(0.40 * ambiguity
       + 0.35 * mean(ASA.scene_analysis[0:10])
       + 0.25 * roughness_std)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f09: Consonance-Valence ([-1, 1] range)
f09 = tanh(0.50 * pleasantness_velocity
          + 0.50 * pleasantness_mean_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Temporal dynamics
dSalience/dt = τ⁻¹ · (Target_Salience - Current_Salience)
    where τ = 4.0s (integration window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | CSG Function |
|--------|-----------------|----------|---------------|--------------|
| **ACC** | 0, 24, 32 | 4 | Direct (fMRI: Bravo 2017) | Salience network hub for dissonance |
| **AI (Anterior Insula)** | ±34, 18, -4 | 3 | Direct (fMRI: Bravo 2017, Koelsch) | Salience network, consonance processing |
| **Heschl's Gyrus** | ±42, -22, 8 | 4 | Direct (fMRI, ECoG: Fishman, Foo 2016) | Sensory evidence weighting, phase-locked graded response |
| **Amygdala** | ±24, -6, -18 | 3 | Direct (fMRI: Koelsch, Cheung) | Dissonance-driven salience, uncertainty integration |
| **vmPFC** | 0, 52, -6 | 2 | Direct (fMRI: Kim, Cheung) | Reward/valence integration, limbic-frontal mediation |
| **Ventral Striatum (NAc)** | ±10, 12, -6 | 2 | Direct (fMRI: Kim, Cheung) | Consonance-reward coupling |

---

## 9. Cross-Unit Pathways

### 9.1 CSG ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CSG INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  CSG.salience_activation ────────► AACM (aesthetic attention modulation)   │
│  CSG.consonance_valence ─────────► IACM (salience network complement)     │
│  CSG.sensory_load ────────────────► STANM (network reconfiguration)       │
│  CSG.aesthetic_appreciation ──────► PWSM (precision for consonance)       │
│                                                                             │
│  CROSS-UNIT (ASU → ARU):                                                   │
│  CSG.consonance_valence ──────────► ARU.affect (valence information)      │
│  CSG.aesthetic_appreciation ──────► ARU.reward (consonance pleasure)      │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ──────────── ► CSG (harmonic context)                 │
│  ASA mechanism (30D) ──────────── ► CSG (attention/salience, primary)     │
│  R³ (~16D) ──────────────────────► CSG (direct consonance features)       │
│  H³ (18 tuples) ─────────────────► CSG (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Salience network lesion** | ACC lesions should reduce dissonance salience | Testable |
| **Consonance manipulation** | Parametric consonance should produce graded response | **Confirmed** |
| **RT pattern** | Intermediate should produce longest RT | **Confirmed** |
| **Valence linearity** | Consonance-valence should be monotonic | **Confirmed** |
| **Aesthetic preference** | Consonance preference should be robust | **Confirmed** |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class CSG(BaseModel):
    """Consonance-Salience Gradient.

    Output: 12D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "CSG"
    UNIT = "ASU"
    TIER = "α3"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("BEP", "ASA")

    THRESHOLD_LOW = 0.3     # Strong dissonance boundary
    THRESHOLD_HIGH = 0.7    # Consonance boundary
    D_SALIENCE = 5.16       # Effect size for salience activation
    D_SENSORY = 1.9         # Effect size for sensory processing
    D_VALENCE = 3.31        # Effect size for valence
    TAU_DECAY = 4.0         # Integration window (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for CSG computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: consonance tracking ──
            (0, 0, 0, 2),     # roughness, 25ms, value, bidi
            (0, 3, 1, 2),     # roughness, 100ms, mean, bidi
            (0, 3, 2, 2),     # roughness, 100ms, std, bidi
            (0, 16, 1, 2),    # roughness, 1000ms, mean, bidi
            (4, 3, 0, 2),     # sensory_pleasantness, 100ms, value, bidi
            (4, 3, 8, 2),     # sensory_pleasantness, 100ms, velocity, bidi
            (4, 16, 1, 2),    # sensory_pleasantness, 1000ms, mean, bidi
            # ── ASA horizons: salience evaluation ──
            (8, 3, 0, 2),     # loudness, 100ms, value, bidi
            (8, 3, 20, 2),    # loudness, 100ms, entropy, bidi
            (8, 16, 1, 2),    # loudness, 1000ms, mean, bidi
            (1, 3, 0, 2),     # sethares, 100ms, value, bidi
            (1, 8, 8, 0),     # sethares, 500ms, velocity, fwd
            (21, 4, 8, 0),    # spectral_change, 125ms, velocity, fwd
            # ── Direct H³: salience coupling ──
            (25, 3, 0, 2),    # x_l0l5[0], 100ms, value, bidi
            (25, 8, 0, 2),    # x_l0l5[0], 500ms, value, bidi
            (25, 16, 1, 2),   # x_l0l5[0], 1000ms, mean, bidi
            (22, 3, 8, 0),    # energy_change, 100ms, velocity, fwd
            (9, 3, 0, 2),     # spectral_centroid, 100ms, value, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute CSG 12D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) CSG output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        sethares = r3[..., 1:2]
        pleasantness = r3[..., 4:5]
        loudness = r3[..., 8:9]

        # ASA sub-sections
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # BEP sub-sections
        bep_beat = bep[..., 0:10]

        # H³ direct features
        loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)
        roughness_std = h3_direct[(0, 3, 2, 2)].unsqueeze(-1)
        pleasantness_velocity = h3_direct[(4, 3, 8, 2)].unsqueeze(-1)
        pleasantness_mean_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)

        # Consonance proxy
        consonance = pleasantness
        dissonance = 1.0 - consonance
        ambiguity = 1.0 - torch.abs(consonance - 0.5) * 2

        # ═══ LAYER E: Explicit features ═══
        f07 = torch.sigmoid(
            0.40 * dissonance
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            + 0.25 * loudness_entropy
        )
        f08 = torch.sigmoid(
            0.40 * ambiguity
            + 0.35 * asa_scene.mean(-1, keepdim=True)
            + 0.25 * roughness_std
        )
        f09 = torch.tanh(
            0.50 * pleasantness_velocity
            + 0.50 * pleasantness_mean_1s
        )

        # ═══ LAYER M: Mathematical ═══
        salience_response = torch.sigmoid(
            0.5 * f07 + 0.3 * f08 + 0.2 * dissonance
        )
        rt_judgment = torch.sigmoid(
            0.5 * ambiguity + 0.5 * f08
        )
        aesthetic = torch.sigmoid(
            0.5 * consonance + 0.5 * pleasantness_mean_1s
        )

        # ═══ LAYER P: Present ═══
        salience_net = asa_attn.mean(-1, keepdim=True)
        affective_eval = torch.tanh(
            0.5 * asa_salience.mean(-1, keepdim=True)
            + 0.5 * f09
        )
        sensory_load = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * ambiguity
        )

        # ═══ LAYER F: Future ═══
        valence_pred = torch.tanh(
            0.5 * f09 + 0.5 * pleasantness_mean_1s
        )
        processing_pred = torch.sigmoid(
            0.5 * f08 + 0.5 * ambiguity
        )
        aesthetic_pred = torch.sigmoid(
            0.5 * aesthetic + 0.5 * consonance
        )

        return torch.cat([
            f07, f08, f09,                                          # E: 3D
            salience_response, rt_judgment, aesthetic,               # M: 3D
            salience_net, affective_eval, sensory_load,             # P: 3D
            valence_pred, processing_pred, aesthetic_pred,           # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (Bravo, Sarasso + 7 converging studies) | Multi-method evidence |
| **Effect Sizes** | 8+ significant | d=5.16, d=1.9, d=3.31, d=2.008 |
| **Primary Effect** | d = 5.16 | Salience activation |
| **Evidence Modality** | fMRI, EEG, ECoG, MEG, AEP | Multi-modal convergence |
| **Falsification Tests** | 4/5 confirmed | High validity |
| **R³ Features Used** | ~16D of 49D | Consonance + energy + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Harmonic context (secondary) |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience (primary) |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **Bravo, F., et al. (2017)**. Neural mechanisms underlying valence inferences to sound: The role of the right anterior insula and the anterior cingulate cortex. *European Journal of Neuroscience*, 45(1), 115-128.

2. **Sarasso, P., et al. (2019)**. ERP correlates of aesthetic experience to consonant and dissonant musical intervals. *Psychophysiology*, 56(4), e13317.

3. **Seeley, W. W., et al. (2007)**. Dissociable intrinsic connectivity networks for salience processing and executive control. *Journal of Neuroscience*, 27(9), 2349-2356.

4. **Plomp, R., & Levelt, W. J. (1965)**. Tonal consonance and critical bandwidth. *Journal of the Acoustical Society of America*, 38(4), 548-560.

5. **Fishman, Y. I., et al.** Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. `Literature/c3: Consonance and Dissonance of Musical Chords Neural Correlates in Auditory Cortex`

6. **Foo, F., et al. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154. `Literature/c3: foo_2016_differential_processing_consonance_dissonance_superior_temporal_gyrus`

7. **Wöhrle, J., et al. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. `Literature/c3: Neuromagnetic representation of musical roundness in chord progressions`

8. **Koelsch, S., et al.** Investigating emotion with music: An fMRI study. `Literature/c3: Investigating emotion with music An fMRI study`

9. **Kim, S. G., et al.** Brain networks underlying aesthetic appreciation as modulated by interaction of spectral and temporal organisations of music. `Literature/c3: Brain networks underlying aesthetic appreciation as modulated by interaction of`

10. **Cheung, V. K. M., et al.** Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. `Literature/c3: Uncertainty and Surprise Jointly Predict Musical Pleasure and Amygdala, Hippocam`

11. **Musical chills HD-EEG.** Cortical patterns of pleasurable musical chills revealed by high-density EEG. `Literature/c3: Cortical Patterns of Pleasurable Musical Chills Revealed by High Density EEG`

12. **Auditory and reward structures.** Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. `Literature/c3: Auditory and reward structures reflect the pleasure of musical expectancies duri`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, AED) | BEP (30D) + ASA (30D) mechanisms |
| Consonance | S⁰.L5.roughness[30] + S⁰.L5.sethares[31] | R³.roughness[0] + R³.sethares[1] + R³.sensory_pleasantness[4] |
| Salience | S⁰.L5.loudness[35] + HC⁰.ATT | R³.loudness[8] + ASA.attention_gating |
| Affective | S⁰.L6.spectral_envelope[55:60] + HC⁰.AED | R³.warmth[12] + ASA.salience_weighting |
| Integration | S⁰.X_L5L6[208:216] | R³.x_l0l5[25:33] + H³ tuples |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 26/2304 = 1.13% | 18/2304 = 0.78% |
| Output | 12D | 12D (same) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10]: Oscillatory band tracking maps to BEP's harmonic context monitoring (secondary).
- **ATT → ASA.attention_gating** [10:20]: Attentional salience for dissonance maps to ASA's attention gating (primary).
- **AED → ASA.salience_weighting** [20:30]: Affective entrainment dynamics maps to ASA's consonance-weighted salience evaluation.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
