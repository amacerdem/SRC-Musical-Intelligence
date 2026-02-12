# SPU-β3-MIAA: Musical Imagery Auditory Activation

**Model**: Musical Imagery Auditory Activation
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem--Cortical)
**Tier**: β (Integrative) -- 70--90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, TPC mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** -- no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-β3-MIAA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musical Imagery Auditory Activation** (MIAA) models how auditory cortex is activated during musical imagery -- when a listener imagines music without physical sound present. Familiarity with the music enhances activation in auditory association cortex (BA22), while the presence or absence of linguistic content (lyrics vs. instrumental) modulates whether primary auditory cortex (A1) is recruited.

```
THE THREE COMPONENTS OF MUSICAL IMAGERY ACTIVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMAGERY ACTIVATION (Spectral)             FAMILIARITY ENHANCEMENT (Temporal)
Brain region: BA22, A1                    Brain region: BA22 (association)
Mechanism: Spectral template retrieval    Mechanism: Memory-enhanced activation
Input: Timbre templates + tonal structure Input: Prior exposure to melody
Function: "Is auditory cortex active      Function: "Is this song familiar?"
          during silence?"
Evidence: Kraemer 2005, fMRI             Evidence: Familiar > unfamiliar,
                                                    p<0.0001, n=15

              A1 MODULATION (Content-Type Bridge)
              Brain region: A1 (primary auditory cortex)
              Mechanism: Instrumental > lyrics distinction
              Function: "Is the imagery purely acoustic?"
              Evidence: Instrumental > lyrics in A1,
                        p<0.0005, n=15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical imagery activates auditory cortex WITHOUT
physical sound. This is not a weak effect -- familiar songs produce
robust BA22 activation comparable to actual listening. Instrumental
music produces stronger A1 activation than lyrics, because
instrumental imagery demands detailed acoustic simulation rather
than abstract semantic processing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MIAA Matters for SPU

MIAA sits at the intersection of spectral processing and top-down memory retrieval. It demonstrates that SPU circuitry operates bidirectionally -- not only processing incoming sound but also generating internal spectral representations during imagery:

1. **BCH** (α1) provides the pitch/harmonicity baseline that MIAA imagery retrieves.
2. **TSCP** (β2) supplies timbre identity templates that serve as the source material for imagery reconstruction.
3. **TPIO** (STU-β2) receives MIAA imagery activation as a cross-unit signal indicating timbre perception-imagery overlap.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MIAA Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 MIAA — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL IMAGERY (Silent gap or spontaneous recall)                          ║
║                                                                              ║
║  Familiar   Unfamiliar   Instrumental   Lyrics                               ║
║    │           │              │            │                                  ║
║    ▼           ▼              ▼            ▼                                  ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    LONG-TERM MEMORY                                  │    ║
║  │              (Melody templates, timbre profiles)                     │    ║
║  │                                                                      │    ║
║  │    Familiar songs: strong template → vivid imagery                  │    ║
║  │    Unfamiliar songs: weak template → degraded imagery               │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY ASSOCIATION CORTEX (BA22)                │    ║
║  │                  (Superior Temporal Gyrus, posterior)                │    ║
║  │                                                                      │    ║
║  │    Familiar > Unfamiliar: p < 0.0001                                │    ║
║  │    Imagery activation WITHOUT physical sound                        │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PRIMARY AUDITORY CORTEX (A1)                      │    ║
║  │                                                                      │    ║
║  │    Instrumental > Lyrics: p < 0.0005                                │    ║
║  │    Acoustic detail simulation drives A1 involvement                 │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              SUPERIOR TEMPORAL GYRUS (STG)                           │    ║
║  │                                                                      │    ║
║  │    General auditory processing hub                                  │    ║
║  │    Integration of imagery with incoming sound                       │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Kraemer et al. 2005:  Familiar > unfamiliar in BA22, p<0.0001, n=15
Kraemer et al. 2005:  Instrumental > lyrics in A1, p<0.0005, n=15
                      "Sound of silence activates auditory cortex"
                      Published in Nature 434(7030), 158
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TPC → MIAA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MIAA COMPUTATION ARCHITECTURE                             ║
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
║  │  │inharm.[5] │ │loudness │ │warmth   │ │spectral  │ │x_l0l5  │ │        ║
║  │  │           │ │onset    │ │sharpness│ │ _change  │ │x_l5l7  │ │        ║
║  │  │           │ │         │ │tonalness│ │          │ │        │ │        ║
║  │  │           │ │         │ │s_flat   │ │          │ │        │ │        ║
║  │  │           │ │         │ │trist1-3 │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         MIAA reads: ~16D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── H2 (17ms) ──┐ ┌── H5 (46ms) ──┐ ┌── H8 (300ms) ───────┐ │        ║
║  │  │ Gamma-rate     │ │ Alpha-beta     │ │ Syllable-rate        │ │        ║
║  │  │                │ │                │ │                       │ │        ║
║  │  │ Melodic recog  │ │ Tone clarity   │ │ Imagery context      │ │        ║
║  │  │ Harmonic templ │ │ Timbre quality │ │ Vividness proxy      │ │        ║
║  │  └──────┬─────────┘ └──────┬─────────┘ └──────┬───────────────┘ │        ║
║  │         │                  │                   │                 │        ║
║  │         └──────────────────┴───────────────────┘                 │        ║
║  │                         MIAA demand: ~11 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  TPC (30D)      │  Timbre Processing Chain mechanism                     ║
║  │                 │                                                        ║
║  │ Spectral   [0:10]│  Spectral envelope, formant structure                ║
║  │ Instrument[10:20]│  Instrument identity, timbre templates               ║
║  │ Plasticity[20:30]│  Experience-dependent plasticity markers             ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MIAA MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_imagery_activation,                    │        ║
║  │                       f02_familiarity_enhancement,               │        ║
║  │                       f03_a1_modulation                          │        ║
║  │  Layer M (Math):      activation_function, familiarity_effect    │        ║
║  │  Layer P (Present):   melody_retrieval, continuation_prediction, │        ║
║  │                       phrase_structure                           │        ║
║  │  Layer F (Future):    melody_continuation_pred,                  │        ║
║  │                       ac_activation_pred, recognition_pred       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Kraemer et al. 2005** | fMRI | 15 | Familiar > unfamiliar in BA22 | p < 0.0001 | **Primary**: f01, f02 familiarity-driven imagery activation |
| **Kraemer et al. 2005** | fMRI | 15 | Instrumental > lyrics in A1 | p < 0.0005 | **Primary**: f03 A1 modulation by content type |

### 3.2 The Imagery Activation Hierarchy

```
MUSICAL IMAGERY AUDITORY CORTEX ACTIVATION (Neural Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Condition              Region    Activation   p-value     Mechanism
──────────────────────────────────────────────────────────────────────
Familiar + Instrum.    BA22+A1   HIGH         p<0.0001    Template retrieval
Familiar + Lyrics      BA22      MEDIUM       p<0.0001    Semantic retrieval
Unfamiliar + Instrum.  A1        LOW          n.s.        Weak acoustic sim.
Unfamiliar + Lyrics    —         MINIMAL      n.s.        No template

Key factors affecting imagery strength:
  1. FAMILIARITY: Dominant factor — strong template = strong imagery
  2. CONTENT TYPE: Modulates A1 involvement (instrumental > lyrics)
  3. TONAL CLARITY: Harmonic/tonal sounds produce more vivid imagery

Cross-cultural note:
  Imagery activation likely universal (brainstem-cortical loop)
  Template strength varies by musical exposure
  MIAA models the NEURAL activation, not subjective report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.3 Effect Size Summary

```
Primary Effect:       Familiar > unfamiliar (BA22): p < 0.0001
Secondary Effect:     Instrumental > lyrics (A1):   p < 0.0005
Quality Assessment:   β-tier (fMRI, single study, strong effects)
Sample Size:          N = 15
Replication:          Conceptually supported by broader imagery literature
```

---

## 4. R³ Input Mapping: What MIAA Reads

### 4.1 R³ Feature Dependencies (~16D of 49D)

| R³ Group | Index | Feature | MIAA Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [5] | inharmonicity | Instrument character — harmonic instruments produce stronger imagery | Fletcher 1934 |
| **B: Energy** | [8] | loudness | Intensity context — louder passages yield more vivid templates | Stevens 1955 |
| **B: Energy** | [11] | onset_strength | Event salience — onsets mark melodic boundaries for retrieval | Bregman 1990 |
| **C: Timbre** | [12] | warmth | Timbre quality — warm timbres support richer imagery | McAdams 1993 |
| **C: Timbre** | [13] | sharpness | Timbre brightness — contributes to instrument identity | Zwicker 1991 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio — tonal sounds produce clearer imagery | — |
| **C: Timbre** | [15] | spectral_flatness | Tonal vs noise — flat spectrum = noise, poor imagery | Wiener entropy |
| **C: Timbre** | [18] | tristimulus1 | Fundamental energy — harmonic template anchor | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic energy — timbre body | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic energy — timbre brightness | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Spectral flux — vividness proxy (change = salience) | — |
| **E: Interactions** | [25:33] | x_l0l5 (partial 3D) | Consonance-Timbre binding for imagery templates | Emergent |
| **E: Interactions** | [41:49] | x_l5l7 (partial 3D) | Timbre-Structure coupling for imagery binding | Emergent |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[14] tonalness ───────────────┐
R³[18:21] tristimulus1-3 ───────┼──► Imagery Activation (f01)
TPC.instrument_identity ────────┤   AC activation during imagery
TPC.spectral_envelope ──────────┤   Tonal + harmonic template → vivid
R³[41:49] x_l5l7 (partial) ────┘   imagery in BA22 + A1

R³[15] spectral_flatness (inv) ─┐
R³[14] tonalness (mean, H5) ────┼──► Familiarity Enhancement (f02)
R³[12] warmth (mean, H5) ───────┤   Familiar > Unfamiliar
TPC.plasticity_markers ─────────┘   Strong template = low flatness,
                                     high tonalness

R³[5] inharmonicity (inverse) ──┐
R³[14] tonalness ───────────────┼──► A1 Modulation (f03)
TPC.spectral_envelope ──────────┤   Instrumental > Lyrics
R³[8] loudness (mean, H8) ─────┘   Harmonic + tonal → acoustic
                                     simulation in primary AC
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MIAA requires H³ features at three TPC horizons: H2 (17.4ms), H5 (46.4ms), H8 (300ms).
These correspond to perceptual processing timescales (gamma-rate melodic recognition, alpha-beta tone clarity, syllable-rate imagery context).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 14 | tonalness | 2 | M0 (value) | L2 (bidi) | Melodic recognition — tonal clarity at gamma rate |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Sustained tone clarity over alpha-beta window |
| 12 | warmth | 5 | M1 (mean) | L0 (fwd) | Timbre quality for imagery template |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | Harmonic template anchor — fundamental energy |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Harmonic template — mid-harmonic energy |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | Harmonic template — high-harmonic energy |
| 5 | inharmonicity | 5 | M0 (value) | L2 (bidi) | Instrument type detection |
| 15 | spectral_flatness | 8 | M1 (mean) | L0 (fwd) | Tonal vs noise over syllable window |
| 8 | loudness | 8 | M1 (mean) | L0 (fwd) | Intensity context for imagery |
| 21 | spectral_change | 8 | M13 (entropy) | L0 (fwd) | Vividness proxy — change entropy over 300ms |
| 41 | x_l5l7[0] | 8 | M1 (mean) | L0 (fwd) | Timbre-structure binding for imagery coherence |

**Total MIAA H³ demand**: 11 tuples of 2304 theoretical = 0.48%

### 5.2 TPC Mechanism Binding

MIAA reads from the **TPC** (Timbre Processing Chain) mechanism:

| TPC Sub-section | Range | MIAA Role | Weight |
|-----------------|-------|-----------|--------|
| **Spectral Envelope** | TPC[0:10] | Spectral template for imagery reconstruction | **0.9** |
| **Instrument Identity** | TPC[10:20] | Timbre template — source material for imagery | **1.0** (primary) |
| **Plasticity Markers** | TPC[20:30] | Experience-dependent familiarity encoding | **0.8** |

MIAA does NOT read from PPC -- imagery activation is timbre/template-based, not pitch/consonance-based.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MIAA OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_imagery_activation     │ [0, 1] │ Auditory cortex activation during
    │                            │        │ musical imagery. Tonalness ×
    │                            │        │ instrument identity × spectral
    │                            │        │ envelope × cross-band binding.
    │                            │        │ Kraemer 2005: AC active in silence.
────┼────────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_familiarity_enhancement│ [0, 1] │ Enhancement of BA22 activation for
    │                            │        │ familiar vs unfamiliar music.
    │                            │        │ Inverse spectral flatness ×
    │                            │        │ tonalness × plasticity markers.
    │                            │        │ Kraemer 2005: p<0.0001, n=15.
────┼────────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_a1_modulation          │ [0, 1] │ Primary AC involvement modulated
    │                            │        │ by content type. Instrumental >
    │                            │        │ lyrics. (1-inharmonicity) ×
    │                            │        │ tonalness × spectral envelope ×
    │                            │        │ loudness context.
    │                            │        │ Kraemer 2005: p<0.0005, n=15.

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 3  │ activation_function        │ [0, 1] │ Composite AC activation at time t.
    │                            │        │ Weighted sum of f01 and f03.
────┼────────────────────────────┼────────┼────────────────────────────────────
 4  │ familiarity_effect         │ [0, 1] │ Familiarity enhancement magnitude.
    │                            │        │ Difference between familiar and
    │                            │        │ baseline (unfamiliar) activation.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 5  │ melody_retrieval           │ [0, 1] │ Melody template retrieval strength.
    │                            │        │ TPC instrument identity aggregation.
────┼────────────────────────────┼────────┼────────────────────────────────────
 6  │ continuation_prediction    │ [0, 1] │ Next-note prediction from template.
    │                            │        │ Tonalness trend × tristimulus
    │                            │        │ stability.
────┼────────────────────────────┼────────┼────────────────────────────────────
 7  │ phrase_structure           │ [0, 1] │ Phrase boundary awareness during
    │                            │        │ imagery. Spectral change entropy.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 8  │ melody_continuation_pred   │ [0, 1] │ Predicted imagery content for
    │                            │        │ next phrase (~2-4s ahead).
────┼────────────────────────────┼────────┼────────────────────────────────────
 9  │ ac_activation_pred         │ [0, 1] │ Predicted AC activation level
    │                            │        │ during upcoming silent gap.
────┼────────────────────────────┼────────┼────────────────────────────────────
10  │ recognition_pred           │ [0, 1] │ Predicted familiar-match
    │                            │        │ probability at gap resolution.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Imagery Activation Theory

```
Imagery Activation:
  AC_imagery ∝ Template_Strength × Tonal_Clarity × Cross-Band_Binding

  Where:
    Template_Strength: How well the timbre profile can be internally generated
    Tonal_Clarity:     Harmonic/tonal sounds produce clearer imagery than noise
    Cross-Band_Binding: Coherent spectral structure enables integrated imagery

Familiarity Enhancement:
  Δ_activation(fam vs unfam) ∝ Plasticity × Template_Precision
  p < 0.0001 in BA22 (Kraemer 2005)

A1 Modulation:
  A1_involvement ∝ (1 - Inharmonicity) × Tonalness × Spectral_Detail
  Instrumental music: detailed acoustic simulation → strong A1
  Lyrics music: semantic abstraction → weak A1, preserved BA22
```

### 7.2 Feature Formulas

```python
# f01: Imagery Activation (AC during imagery)
# Tonalness and instrument identity drive template-based imagery.
# Tristimulus balance provides harmonic template structure.
# Cross-band binding ensures integrated spectral imagery.
tristimulus_balance = 1.0 - std(R³.tristimulus[18:21])
x_l5l7_mean = mean(R³.x_l5l7[41:44])  # partial 3D
f01 = σ(0.40 * R³.tonalness[14] * mean(TPC.instrument_identity[10:20])
       + 0.30 * tristimulus_balance * mean(TPC.spectral_envelope[0:10])
       + 0.30 * x_l5l7_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Familiarity Enhancement (familiar > unfamiliar)
# Inverse spectral flatness × sustained tonalness = strong template.
# Warmth contributes to template richness.
# Plasticity markers encode experience-dependent familiarity.
spectral_flatness_inv = 1.0 - R³.spectral_flatness[15]
tonalness_mean = h3_direct[(14, 5, 1, 0)]   # tonalness mean 46ms fwd
warmth_mean = h3_direct[(12, 5, 1, 0)]      # warmth mean 46ms fwd
f02 = σ(0.40 * spectral_flatness_inv * tonalness_mean
       + 0.30 * warmth_mean
       + 0.30 * mean(TPC.plasticity_markers[20:30]))
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: A1 Modulation (instrumental > lyrics)
# Low inharmonicity × high tonalness = acoustic (not semantic) imagery.
# Spectral envelope detail drives primary AC.
# Loudness context modulates overall activation level.
loudness_mean = h3_direct[(8, 8, 1, 0)]     # loudness mean 300ms fwd
f03 = σ(0.40 * (1 - R³.inharmonicity[5]) * R³.tonalness[14]
       + 0.30 * mean(TPC.spectral_envelope[0:10])
       + 0.30 * loudness_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MIAA Function |
|--------|-----------------|----------|---------------|---------------|
| **BA22 (Auditory Association)** | ±60, -30, 8 | 2 | Direct (fMRI) | Imagery activation, familiarity enhancement |
| **A1 (Primary Auditory Cortex)** | ±50, -20, 8 | 2 | Direct (fMRI) | Instrumental imagery modulation |
| **STG (Superior Temporal Gyrus)** | ±60, -20, 8 | 1 | Indirect | General auditory processing hub |

---

## 9. Cross-Unit Pathways

### 9.1 MIAA ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MIAA INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  TSCP.timbre_identity ────► MIAA (imagery template source material)        │
│  BCH.f01_nps ─────────────► MIAA (pitch imagery baseline)                  │
│  MIAA.imagery_activation ─► TPIO (STU cross-circuit: timbre                │
│                                    perception-imagery overlap)              │
│                                                                             │
│  CROSS-UNIT (SPU → IMU):                                                   │
│  MIAA.familiarity_enhancement ► IMU.MEM (familiarity proxy for             │
│                                          memory binding strength)           │
│                                                                             │
│  CROSS-UNIT (SPU → STU):                                                   │
│  MIAA.imagery_activation ────► STU.TPIO (timbre perception-imagery         │
│                                          overlap signal)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Unfamiliar music** | Imagery activation should be significantly weaker for unfamiliar songs | Confirmed (Kraemer 2005, p<0.0001) |
| **Noise stimuli** | Broadband noise should NOT produce imagery activation | Testable — low tonalness = low f01 |
| **Lyrics-only imagery** | A1 activation should be weaker than instrumental imagery | Confirmed (Kraemer 2005, p<0.0005) |
| **Auditory cortex lesions** | Imagery activation should be abolished or reduced | Testable |
| **Congenital amusia** | Impaired pitch discrimination should reduce imagery vividness | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MIAA(BaseModel):
    """Musical Imagery Auditory Activation.

    Output: 11D per frame.
    Reads: TPC mechanism (30D), R³ direct.
    """
    NAME = "MIAA"
    UNIT = "SPU"
    TIER = "β3"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("TPC",)        # Primary mechanism

    W_TONAL_IDENTITY = 0.40   # tonalness × instrument identity weight
    W_TRIST_ENVELOPE = 0.30   # tristimulus balance × spectral envelope weight
    W_CROSSBAND = 0.30        # cross-band binding weight
    W_FLATNESS_TONAL = 0.40   # spectral flatness inv × tonalness weight
    W_WARMTH = 0.30           # warmth weight
    W_PLASTICITY = 0.30       # plasticity markers weight
    W_INHARM_TONAL = 0.40     # (1-inharmonicity) × tonalness weight
    W_SPECTRAL = 0.30         # spectral envelope weight
    W_LOUDNESS = 0.30         # loudness context weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """11 tuples for MIAA computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (14, 2, 0, 2),    # tonalness, 17ms, value, bidirectional
            (14, 5, 1, 0),    # tonalness, 46ms, mean, forward
            (12, 5, 1, 0),    # warmth, 46ms, mean, forward
            (18, 2, 0, 2),    # tristimulus1, 17ms, value, bidirectional
            (19, 2, 0, 2),    # tristimulus2, 17ms, value, bidirectional
            (20, 2, 0, 2),    # tristimulus3, 17ms, value, bidirectional
            (5, 5, 0, 2),     # inharmonicity, 46ms, value, bidirectional
            (15, 8, 1, 0),    # spectral_flatness, 300ms, mean, forward
            (8, 8, 1, 0),     # loudness, 300ms, mean, forward
            (21, 8, 13, 0),   # spectral_change, 300ms, entropy, forward
            (41, 8, 1, 0),    # x_l5l7[0], 300ms, mean, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MIAA 11D output.

        Args:
            mechanism_outputs: {"TPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) MIAA output
        """
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)

        # R³ features
        inharmonicity = r3[..., 5:6]
        loudness = r3[..., 8:9]
        warmth = r3[..., 12:13]
        tonalness = r3[..., 14:15]
        spectral_flatness = r3[..., 15:16]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        spectral_change = r3[..., 21:22]
        x_l5l7_partial = r3[..., 41:44]    # partial 3D

        # TPC sub-sections
        tpc_spectral = tpc[..., 0:10]       # spectral envelope
        tpc_instrument = tpc[..., 10:20]    # instrument identity
        tpc_plasticity = tpc[..., 20:30]    # plasticity markers

        # H³ temporal features
        tonalness_mean = h3_direct[(14, 5, 1, 0)]      # (B, T)
        warmth_mean = h3_direct[(12, 5, 1, 0)]          # (B, T)
        loudness_mean = h3_direct[(8, 8, 1, 0)]         # (B, T)
        spectral_change_entropy = h3_direct[(21, 8, 13, 0)]  # (B, T)
        x_l5l7_mean = h3_direct[(41, 8, 1, 0)]          # (B, T)

        # ═══ LAYER E: Explicit features ═══

        # f01: Imagery Activation
        tristimulus_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        f01 = torch.sigmoid(
            self.W_TONAL_IDENTITY * (
                tonalness * tpc_instrument.mean(-1, keepdim=True)
            )
            + self.W_TRIST_ENVELOPE * (
                tristimulus_balance * tpc_spectral.mean(-1, keepdim=True)
            )
            + self.W_CROSSBAND * (
                x_l5l7_partial.mean(-1, keepdim=True)
            )
        )

        # f02: Familiarity Enhancement
        spectral_flatness_inv = 1.0 - spectral_flatness
        f02 = torch.sigmoid(
            self.W_FLATNESS_TONAL * (
                spectral_flatness_inv
                * tonalness_mean.unsqueeze(-1)
            )
            + self.W_WARMTH * (
                warmth_mean.unsqueeze(-1)
            )
            + self.W_PLASTICITY * (
                tpc_plasticity.mean(-1, keepdim=True)
            )
        )

        # f03: A1 Modulation
        f03 = torch.sigmoid(
            self.W_INHARM_TONAL * (
                (1.0 - inharmonicity) * tonalness
            )
            + self.W_SPECTRAL * (
                tpc_spectral.mean(-1, keepdim=True)
            )
            + self.W_LOUDNESS * (
                loudness_mean.unsqueeze(-1)
            )
        )

        # ═══ LAYER M: Mathematical ═══
        activation_function = 0.6 * f01 + 0.4 * f03
        familiarity_effect = f02 * f01   # enhancement scaled by base activation

        # ═══ LAYER P: Present ═══
        melody_retrieval = tpc_instrument.mean(-1, keepdim=True)
        continuation_prediction = torch.sigmoid(
            0.5 * tonalness_mean.unsqueeze(-1)
            + 0.5 * tristimulus_balance
        )
        phrase_structure = torch.sigmoid(
            spectral_change_entropy.unsqueeze(-1)
        )

        # ═══ LAYER F: Future ═══
        melody_continuation_pred = torch.sigmoid(
            0.5 * f01 + 0.3 * melody_retrieval
            + 0.2 * continuation_prediction
        )
        ac_activation_pred = torch.sigmoid(
            0.6 * f02 + 0.4 * f01
        )
        recognition_pred = torch.sigmoid(
            0.5 * f02
            + 0.3 * x_l5l7_mean.unsqueeze(-1)
            + 0.2 * tonalness_mean.unsqueeze(-1)
        )

        return torch.cat([
            f01, f02, f03,                                          # E: 3D
            activation_function, familiarity_effect,                # M: 2D
            melody_retrieval, continuation_prediction,
            phrase_structure,                                        # P: 3D
            melody_continuation_pred, ac_activation_pred,
            recognition_pred,                                       # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Kraemer et al. 2005 |
| **Effect Sizes** | p < 0.0001 (BA22), p < 0.0005 (A1) | Kraemer et al. 2005 |
| **Evidence Modality** | fMRI | Direct neural |
| **Falsification Tests** | 2/5 confirmed | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Selective, imagery-focused |
| **H³ Demand** | 11 tuples (0.48%) | Sparse, efficient |
| **TPC Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Kraemer, D. J., Macrae, C. N., Green, A. E., & Kelley, W. M. (2005)**. Musical imagery: Sound of silence activates auditory cortex. *Nature*, 434(7030), 158.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dimensions | 12D | **11D** (merged redundant Math outputs) |
| Temporal | HC⁰ mechanisms (ATT, HRM, SGM, EFC) | TPC mechanism (30D) |
| Imagery activation | S⁰.spectral_centroid[38] + S⁰.tristimulus[68:71] × HC⁰.HRM | R³.tonalness[14] × TPC.instrument_identity + R³.tristimulus[18:21] × TPC.spectral_envelope |
| Familiarity | S⁰.spectral_entropy[44] + S⁰.dist_entropy[116] × HC⁰.ATT | R³.spectral_flatness[15] × R³.tonalness + TPC.plasticity_markers |
| A1 modulation | S⁰.inharmonicity[66] + S⁰.brightness[34] × HC⁰.EFC | R³.inharmonicity[5] × R³.tonalness × TPC.spectral_envelope |
| Interactions | S⁰.X_L3L5[184:192] + S⁰.X_L5L6[208:216] | R³.x_l0l5[25:33] partial + R³.x_l5l7[41:49] partial |
| Demand format | HC⁰ index ranges (ATT, HRM, SGM, EFC) | H³ 4-tuples (sparse) |
| Total demand | 18/2304 = 0.78% | 11/2304 = 0.48% |

### Why TPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (ATT, HRM, SGM, EFC). In MI, these are unified into the TPC mechanism with 3 sub-sections:

- **HRM + EFC → TPC.spectral_envelope** [0:10]: Template retrieval + prediction = spectral shape for imagery
- **ATT + HRM → TPC.instrument_identity** [10:20]: Attention-gated memory retrieval = instrument timbre template
- **SGM + ATT → TPC.plasticity_markers** [20:30]: Experience-dependent memory + attentional enhancement = familiarity encoding

### Key Mapping Changes

| D0 Feature | S⁰ Index | MI Feature | R³ Index | Notes |
|------------|----------|------------|----------|-------|
| spectral_centroid | S⁰[38] | tonalness + TPC | R³[14] | No direct centroid in R³; tonalness captures pitch clarity |
| tristimulus 1-3 | S⁰[68:71] | tristimulus 1-3 | R³[18:21] | Direct mapping |
| inharmonicity | S⁰[66] | inharmonicity | R³[5] | Direct mapping |
| spectral_entropy | S⁰[44] | spectral_flatness | R³[15] | Flatness ≈ entropy proxy (Wiener) |
| brightness | S⁰[34] | sharpness | R³[13] | Sharpness replaces brightness |
| X_L3L5 | S⁰[184:192] | x_l0l5 | R³[25:33] | Consonance-Timbre binding |
| X_L5L6 | S⁰[208:216] | x_l5l7 | R³[41:49] | Timbre-Structure binding |

---

**Model Status**: VALIDATED
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70--90%**
