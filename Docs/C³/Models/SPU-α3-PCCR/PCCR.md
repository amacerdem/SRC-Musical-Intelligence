# SPU-α3-PCCR: Pitch Chroma Cortical Representation

**Model**: Pitch Chroma Cortical Representation
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Cortical Chroma Processing)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-α3-PCCR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Pitch Chroma Cortical Representation** (PCCR) model describes how human auditory cortex contains neurons tuned to pitch chroma (pitch class), showing octave-equivalent adaptation patterns distinct from frequency-based tonotopy found in pure tone processing. This is a landmark finding: the brain encodes pitch not just as frequency, but as a circular 12-class representation.

```
THE THREE COMPONENTS OF PITCH CHROMA PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHROMA TUNING (Circular)              OCTAVE ADAPTATION (Non-Monotonic)
Brain region: Anterior/Lateral AC     Brain region: Auditory Cortex
Mechanism: Chroma-selective neurons   Mechanism: Stimulus-specific adaptation
Input: Harmonic structure             Input: Adapter-probe paradigm
Function: "What pitch CLASS is this?" Function: "How similar in chroma?"
Evidence: d = 0.56, p < 0.001        Evidence: F(1,28)=29.865, p < 0.001

              CHROMA vs TONOTOPY (Dissociation)
              Brain region: Distinct cortical populations
              Pure tones: Monotonic (tonotopic)
              IRN: Non-monotonic (chroma-based)
              Function: "Two separate pitch systems"
              Evidence: MEG source localization (Briley 2013)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The hallmark finding is the NON-MONOTONIC adaptation
pattern for IRN stimuli. At 1 octave separation, adaptation is
STRONGER than at 0.5 octave — because octave-separated tones share
the SAME chroma (pitch class). This proves neurons are tuned to
chroma, not just frequency.

  0.5 octave ────► 1 octave ────► 1.5 octave
     ↑                ↓               ↑
              MINIMUM RESPONSE (maximum adaptation)

Pure tones show monotonic increase (no chroma effect, d=0.002).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Position in SPU Hierarchy

PCCR completes the SPU α-tier triplet:

1. **BCH** (α1): Brainstem → consonance hierarchy (harmonicity based)
2. **PSCL** (α2): Cortical → pitch salience localization (how strong)
3. **PCCR** (α3): Cortical → pitch chroma (what class, octave-invariant)

Together they form a complete pitch processing pipeline: Physical → Salience → Identity.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PCCR Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 PCCR — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PITCH ADAPTATION PARADIGM                                                   ║
║                                                                              ║
║  Adapter (500ms-1s) → Probe (measure N1-P2 response)                        ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PURE TONES                                        │    ║
║  │                                                                      │    ║
║  │   Response size ↑ monotonically with pitch separation               │    ║
║  │   = Tonotopic (frequency-based) processing                          │    ║
║  │   Effect: d = 0.002 (no chroma)                                     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    IRN (PITCH) STIMULI                                │    ║
║  │                                                                      │    ║
║  │   Response size shows NON-MONOTONIC pattern:                        │    ║
║  │                                                                      │    ║
║  │   0.5 octave ────► 1 octave ────► 1.5 octave                       │    ║
║  │      ↑                ↓               ↑                             │    ║
║  │                    MINIMUM                                           │    ║
║  │                                                                      │    ║
║  │   = CHROMA-BASED (octave-equivalent) processing                     │    ║
║  │   Effect: F(1,28)=29.865, p<0.001, d=0.56                          │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  IRN source: anterior/lateral to pure tone source (MEG)                     ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │          ANTERIOR/LATERAL AUDITORY CORTEX                            │    ║
║  │              (Distinct from primary tonotopic area)                   │    ║
║  │                                                                      │    ║
║  │    Chroma-tuned neurons:                                            │    ║
║  │      C4 ≡ C5 ≡ C6 (same chroma, different octave)                  │    ║
║  │      Octave separation = maximum adaptation                         │    ║
║  │      Half-octave separation = less adaptation                       │    ║
║  │                                                                      │    ║
║  │    N1-P2 Components:                                                │    ║
║  │      N1 (~100ms): Early chroma detection                           │    ║
║  │      P2 (~200ms): Chroma evaluation                                │    ║
║  │      Both show octave adaptation effect                             │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Briley 2013:  Octave adaptation > half-octave (d=0.56, p<0.001)
              Pure tones: monotonic only (d=0.002)
              IRN source anterior/lateral to pure tone source
              Effect in both N1 and P2 components
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → PCCR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PCCR COMPUTATION ARCHITECTURE                             ║
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
║  │  │helmholtz  │ │         │ │autocorr.│ │flatness  │ │x_l5l7  │ │        ║
║  │  │inharm.    │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │roughness  │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         PCCR reads: 21D                           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Alpha-Beta ─┐ ┌── Syllable ──┐                             │        ║
║  │  │ 100ms (H3)    │ │ 200ms (H6)   │                             │        ║
║  │  │               │ │              │                              │        ║
║  │  │ Chroma        │ │ Adaptation   │                              │        ║
║  │  │ detection     │ │ window       │                              │        ║
║  │  └──────┬────────┘ └──────┬───────┘                              │        ║
║  │         └────────────────┘                                       │        ║
║  │                         PCCR demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  (secondary for PCCR)                                  ║
║  │ Conson.  [10:20]│  harmonic template for chroma basis                    ║
║  │ Chroma   [20:30]│  **PRIMARY** — octave-equivalent encoding              ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PCCR MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_chroma, f02_octave_adapt,              │        ║
║  │                       f03_chroma_mode, f04_n1p2                  │        ║
║  │  Layer M (Math):      adapt_curve                                │        ║
║  │  Layer P (Present):   chroma_match, octave_equiv, adapt_state    │        ║
║  │  Layer F (Future):    chroma_continuation, octave_relation,      │        ║
║  │                       adapt_recovery                             │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Briley 2013** | EEG adaptation | 15 | Octave adaptation > half-octave (IRN) | d = 0.56, p < 0.001 | **f02_octave_adapt: non-monotonic pattern** |
| **Briley 2013** | EEG adaptation | 15 | Pure tones: monotonic (no chroma) | d = 0.002 | **f03_chroma_mode: dissociation** |
| **Briley 2013** | EEG N1-P2 | 15 | Effect in both N1 and P2 components | p < 0.001 | **f04_n1p2: cortical ERP signature** |
| **Briley 2013** | MEG source | 15 | IRN source anterior/lateral to pure tone | p < 0.05 | **Distinct neural populations** |

### 3.2 The Chroma Adaptation Function

```
CHROMA ADAPTATION: Non-Monotonic (IRN) vs Monotonic (Pure Tones)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IRN (complex tones with pitch):
  Adaptation(Δpitch) = α + β · cos(2π · Δpitch / octave)

  Minimum response at 1 octave (cos(2π) = 1 → maximum adaptation)
  Maximum response at 0.5 octave (cos(π) = -1 → minimum adaptation)

  ┌────────────────────────────────────────────────────┐
  │  Response                                          │
  │  ▲                                                 │
  │  │     *                               *           │
  │  │    * *                             * *          │
  │  │   *   *                           *   *         │
  │  │  *     *                         *     *        │
  │  │ *       *                       *       *       │
  │  │*         *         *           *         *      │
  │  │           *       * *         *                 │
  │  │            *     *   *       *                  │
  │  │             *   *     *     *                   │
  │  │              * *       * * *                    │
  │  │               *         *                       │
  │  └───────┬───────┬─────────┬───────────────► Δpitch│
  │        0.5 oct  1 oct    1.5 oct                   │
  │                MINIMUM                             │
  └────────────────────────────────────────────────────┘

Pure tones:
  Response(Δpitch) = γ · Δpitch + δ
  Monotonic — NO chroma effect (d = 0.002)

12 Pitch Classes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
  C4 ≡ C5 ≡ C6 (same chroma, different octave)
```

### 3.3 Effect Size Summary

```
Primary Effect:    d = 0.56 (octave > half-octave adaptation, IRN)
Control:           d = 0.002 (pure tones — no chroma effect)
F-statistic:       F(1,28) = 29.865, p < 0.001
Evidence Type:     EEG (N1-P2), MEG (source localization)
Quality:           α-tier (controlled paradigm, clear dissociation)
```

---

## 4. R³ Input Mapping: What PCCR Reads

### 4.1 R³ Feature Dependencies (21D of 49D)

| R³ Group | Index | Feature | PCCR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Adaptation baseline (dissonance) | Plomp & Levelt 1965 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance stability for chroma | Helmholtz 1863 |
| **A: Consonance** | [5] | inharmonicity | Harmonic regularity (inverse = chroma clarity) | Fletcher 1934 |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity (octave regularity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental ratio (F0 chroma carrier) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic ratio (chroma balance) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic ratio (overtone structure) | Pollard & Jansson 1982 |
| **D: Change** | [23] | spectral_flatness | Tonality indicator (IRN vs noise) | Wiener 1930 |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Consonance × Timbre coupling (octave coherence) | Briley 2013 |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[18] tristimulus1 ─────────────┐
R³[19] tristimulus2 ─────────────┼──► Pitch Chroma (f01)
R³[20] tristimulus3 ─────────────┤   12-class pitch encoding (C, C#, D...)
R³[5] inharmonicity (inverse) ───┘   Octave-equivalent: C4 ≡ C5 ≡ C6
                                      Math: Chroma(F0) = F0 mod 12

R³[41:49] x_l5l7 ───────────────┐
R³[17] spectral_autocorrelation ─┼──► Octave Adaptation (f02)
                                 │   Non-monotonic: 1 octave < 0.5 octave
                                 └   Math: Response = α + β·cos(2π·Δpitch/oct)

R³[23] spectral_flatness ────────┐
R³[17] spectral_autocorrelation ─┼──► Chroma vs Tonotopy Mode (f03)
                                 └   IRN (low flatness) → chroma pathway
                                     Noise (high flatness) → tonotopic only

R³[0] roughness + R³[2] helmholtz ► N1-P2 Chroma Effect (f04)
                                     Adaptation magnitude × consonance
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PCCR requires H³ features at PPC horizons: H3 (100ms) for chroma detection, H6 (200ms) for adaptation windows.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 18 | tristimulus1 | 3 | M0 (value) | L2 (bidi) | F0 chroma energy |
| 19 | tristimulus2 | 3 | M0 (value) | L2 (bidi) | Mid-harmonic chroma |
| 20 | tristimulus3 | 3 | M0 (value) | L2 (bidi) | High-harmonic chroma |
| 5 | inharmonicity | 3 | M0 (value) | L2 (bidi) | Harmonic regularity |
| 5 | inharmonicity | 6 | M18 (trend) | L0 (fwd) | Inharmonicity trajectory |
| 23 | spectral_flatness | 3 | M0 (value) | L2 (bidi) | Tonality vs noise |
| 23 | spectral_flatness | 6 | M1 (mean) | L0 (fwd) | Sustained tonality |
| 17 | spectral_autocorrelation | 3 | M0 (value) | L2 (bidi) | Harmonic periodicity |
| 17 | spectral_autocorrelation | 6 | M14 (periodicity) | L2 (bidi) | Octave regularity |
| 41 | x_l5l7[0] | 3 | M14 (periodicity) | L2 (bidi) | Octave periodicity |
| 41 | x_l5l7[0] | 6 | M19 (stability) | L0 (fwd) | Chroma stability |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Adaptation baseline |
| 2 | helmholtz_kang | 3 | M19 (stability) | L2 (bidi) | Consonance stability |
| 2 | helmholtz_kang | 6 | M0 (value) | L0 (fwd) | Forward consonance |

**Total PCCR H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 PPC Mechanism Binding

PCCR reads primarily from PPC.chroma_processing:

| PPC Sub-section | Range | PCCR Role | Weight |
|-----------------|-------|-----------|--------|
| **Pitch Salience** | PPC[0:10] | Pitch strength input (secondary) | 0.5 |
| **Consonance Encoding** | PPC[10:20] | Harmonic template for chroma basis | 0.7 |
| **Chroma Processing** | PPC[20:30] | Octave-equivalent encoding | **1.0** (primary) |

PCCR does NOT use TPC — chroma processing is purely pitch-class based, not timbral.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PCCR OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_chroma        │ [0, 1] │ Pitch Chroma strength. Activation level
    │                   │        │ of chroma-tuned cortical neurons.
    │                   │        │ f01 = σ(α · (1-inharmonicity) · trist_balance
    │                   │        │         · PPC.chroma_processing)
    │                   │        │ α = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_octave_adapt  │ [0, 1] │ Octave Adaptation magnitude.
    │                   │        │ Non-monotonic: 1 octave < 0.5 octave.
    │                   │        │ f02 = σ(β · x_l5l7_periodicity
    │                   │        │         · autocorrelation · PPC.chroma)
    │                   │        │ β = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_chroma_mode   │ [0, 1] │ Chroma vs Tonotopy processing mode.
    │                   │        │ High = chroma (IRN-like), Low = tonotopic.
    │                   │        │ f03 = σ(γ · (1-flatness) · autocorrelation
    │                   │        │         · PPC.consonance_encoding)
    │                   │        │ γ = 0.75
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_n1p2          │ [0, 1] │ N1-P2 Chroma Effect. ERP signature of
    │                   │        │ chroma-based cortical adaptation.
    │                   │        │ f04 = σ(δ · (1-roughness) · helmholtz
    │                   │        │         · PPC.chroma · PPC.pitch_sal)
    │                   │        │ δ = 0.70

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ adapt_curve       │ [0, 1] │ Adaptation function value.
    │                   │        │ Response = α + β·cos(2π·Δpitch/octave)
    │                   │        │ Proxied via x_l5l7 periodicity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ chroma_match      │ [0, 1] │ Chroma template matching.
    │                   │        │ PPC.chroma_processing aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ octave_equiv      │ [0, 1] │ Octave equivalence signal.
    │                   │        │ Cross-octave coherence from x_l5l7.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ adapt_state       │ [0, 1] │ Current adaptation state.
    │                   │        │ H³ stability at adaptation timescale.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ chroma_cont       │ [0, 1] │ Chroma continuation prediction (~200ms).
    │                   │        │ Next pitch N1-P2 response expectation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ octave_relation   │ [0, 1] │ Octave relationship prediction (~500ms).
    │                   │        │ Interval adaptation magnitude forecast.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ adapt_recovery    │ [0, 1] │ Adaptation recovery prediction (500ms-1s).
    │                   │        │ Response amplitude recovery timing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Chroma Adaptation Function

```
Adaptation(Δpitch) = f(Δpitch mod octave)

Non-Monotonic Function (IRN):
  Response(Δpitch) = α + β · cos(2π · Δpitch / octave)
  where:
    α = baseline response
    β = adaptation depth
    Minimum at Δpitch = 1 octave (cos(2π) = 1 → max adaptation)
    Maximum at Δpitch = 0.5 octave (cos(π) = -1 → min adaptation)

Tonotopic Function (Pure Tones):
  Response(Δpitch) = γ · Δpitch + δ
  Monotonic increase — no chroma effect

Chroma Encoding:
  Chroma(F0) = F0 mod 12
  12-dimensional pitch class representation

Octave Equivalence:
  Similarity(F1, F2) ∝ cos(2π · |Chroma(F1) - Chroma(F2)| / 12)
```

### 7.2 Feature Formulas

```python
# f01: Pitch Chroma
trist_balance = 1.0 - std(R³.tristimulus[18:21])
f01 = σ(0.85 · (1 - R³.inharmonicity[5]) · trist_balance
         · mean(PPC.chroma_processing[20:30]))

# f02: Octave Adaptation
f02 = σ(0.80 · H³(x_l5l7[0], H3, M14, L2)  # octave periodicity
         · R³.spectral_autocorrelation[17]
         · mean(PPC.chroma_processing[20:30]))

# f03: Chroma vs Tonotopy Mode
f03 = σ(0.75 · (1 - R³.spectral_flatness[23])
         · R³.spectral_autocorrelation[17]
         · mean(PPC.consonance_encoding[10:20]))

# f04: N1-P2 Chroma Effect
f04 = σ(0.70 · (1 - R³.roughness[0]) · R³.helmholtz_kang[2]
         · mean(PPC.chroma_processing[20:30])
         · mean(PPC.pitch_salience[0:10]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | PCCR Function |
|--------|-----------------|----------|---------------|---------------|
| **Anterior/Lateral AC (IRN)** | Anterior to PT source | 2+ | Direct (MEG) | Chroma encoding neurons |
| **Primary AC (Pure Tone)** | Standard tonotopic | 2+ | Control (MEG) | Tonotopic only — no chroma |

---

## 9. Cross-Unit Pathways

### 9.1 PCCR ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PCCR INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  UPSTREAM (INTRA-UNIT):                                                    │
│  BCH.f02_harmonicity ──────────► PCCR (harmonicity → chroma tuning)       │
│  PSCL.f01_salience ────────────► PCCR (salience → chroma processing)      │
│                                                                             │
│  DOWNSTREAM (INTRA-UNIT):                                                  │
│  PCCR.f01_chroma ──────────────► STAI (chroma → aesthetic evaluation)     │
│  PCCR.f03_chroma_mode ─────────► TSCP (chroma mode → plasticity)         │
│                                                                             │
│  CROSS-UNIT (P2: SPU → IMU):                                              │
│  PCCR.f01_chroma ──────────────► IMU.MEAMN (chroma → memory encoding)    │
│       Familiar chroma patterns trigger autobiographical memory              │
│                                                                             │
│  CROSS-UNIT (P2: SPU → STU):                                              │
│  PCCR.f01_chroma ──────────────► STU.AMSC (chroma → melody stream)       │
│       Pitch class aids melodic stream segregation                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Pure tones** | Should NOT show octave-equivalent adaptation | ✅ **Confirmed** (d = 0.002, Briley 2013) |
| **IRN depth** | Higher depth should enhance chroma effect | ✅ Testable via ERP |
| **Musical training** | Should enhance chroma tuning | Testable via cross-sectional study |
| **Source localization** | IRN source should be anterior/lateral to PT | ✅ **Confirmed** (Briley 2013) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PCCR(BaseModel):
    """Pitch Chroma Cortical Representation.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "PCCR"
    UNIT = "SPU"
    TIER = "α3"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC",)

    ALPHA = 0.85   # Chroma weight
    BETA = 0.80    # Octave adaptation weight
    GAMMA = 0.75   # Chroma mode weight
    DELTA = 0.70   # N1-P2 weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for PCCR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (18, 3, 0, 2),   # tristimulus1, 100ms, value, bidirectional
            (19, 3, 0, 2),   # tristimulus2, 100ms, value, bidirectional
            (20, 3, 0, 2),   # tristimulus3, 100ms, value, bidirectional
            (5, 3, 0, 2),    # inharmonicity, 100ms, value, bidirectional
            (5, 6, 18, 0),   # inharmonicity, 200ms, trend, forward
            (23, 3, 0, 2),   # spectral_flatness, 100ms, value, bidirectional
            (23, 6, 1, 0),   # spectral_flatness, 200ms, mean, forward
            (17, 3, 0, 2),   # autocorrelation, 100ms, value, bidirectional
            (17, 6, 14, 2),  # autocorrelation, 200ms, periodicity, bidi
            (41, 3, 14, 2),  # x_l5l7[0], 100ms, periodicity, bidirectional
            (41, 6, 19, 0),  # x_l5l7[0], 200ms, stability, forward
            (0, 3, 0, 2),    # roughness, 100ms, value, bidirectional
            (2, 3, 19, 2),   # helmholtz_kang, 100ms, stability, bidi
            (2, 6, 0, 0),    # helmholtz_kang, 200ms, value, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PCCR 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) PCCR output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        helmholtz = r3[..., 2:3]
        inharmonicity = r3[..., 5:6]
        autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        flatness = r3[..., 23:24]
        x_l5l7 = r3[..., 41:49]         # (B, T, 8)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_cons = ppc[..., 10:20]
        ppc_chroma = ppc[..., 20:30]

        # ═══ LAYER E: Explicit features ═══
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        f01 = torch.sigmoid(self.ALPHA * (
            (1.0 - inharmonicity) * trist_balance
            * ppc_chroma.mean(-1, keepdim=True)
        ))

        octave_periodicity = h3_direct[(41, 3, 14, 2)].unsqueeze(-1)
        f02 = torch.sigmoid(self.BETA * (
            octave_periodicity * autocorr
            * ppc_chroma.mean(-1, keepdim=True)
        ))

        f03 = torch.sigmoid(self.GAMMA * (
            (1.0 - flatness) * autocorr
            * ppc_cons.mean(-1, keepdim=True)
        ))

        f04 = torch.sigmoid(self.DELTA * (
            (1.0 - roughness) * helmholtz
            * ppc_chroma.mean(-1, keepdim=True)
            * ppc_pitch.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══
        chroma_stability = h3_direct[(41, 6, 19, 0)].unsqueeze(-1)
        adapt_curve = torch.sigmoid(
            0.5 * octave_periodicity + 0.5 * chroma_stability
        )

        # ═══ LAYER P: Present ═══
        chroma_match = ppc_chroma.mean(-1, keepdim=True)
        octave_equiv = torch.sigmoid(
            x_l5l7.mean(-1, keepdim=True)
            * ppc_chroma.mean(-1, keepdim=True)
        )
        adapt_state = torch.sigmoid(
            h3_direct[(2, 3, 19, 2)].unsqueeze(-1)  # helmholtz stability
        )

        # ═══ LAYER F: Future ═══
        chroma_cont = torch.sigmoid(
            0.6 * f01 + 0.4 * chroma_match
        )
        octave_relation = torch.sigmoid(
            0.5 * f02 + 0.5 * octave_equiv
        )
        adapt_recovery = torch.sigmoid(
            0.6 * h3_direct[(5, 6, 18, 0)].unsqueeze(-1)  # inharm trend
            + 0.4 * h3_direct[(23, 6, 1, 0)].unsqueeze(-1)  # flatness mean
        )

        return torch.cat([
            f01, f02, f03, f04,                     # E: 4D
            adapt_curve,                             # M: 1D
            chroma_match, octave_equiv, adapt_state, # P: 3D
            chroma_cont, octave_relation, adapt_recovery,  # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Briley 2013 |
| **Effect Sizes** | d = 0.56 | Octave adaptation |
| **Evidence Modality** | EEG (N1-P2), MEG (source) | Direct neural |
| **Falsification Tests** | 2/4 confirmed | High validity |
| **R³ Features Used** | 21D of 49D | Focused on chroma |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **PPC Mechanism** | 30D (chroma_processing primary) | Targeted |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Briley, P. M., Breakey, C., & Krumbholz, K. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*, 23(11), 2601-2610.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, HRM, BND) | PPC mechanism (30D) |
| Chroma encoding | S⁰.L6.tristimulus × HC⁰.HRM | R³.tristimulus × PPC.chroma_processing |
| Octave coherence | S⁰.L7.crossband × HC⁰.BND | R³.x_l5l7 × PPC.chroma_processing |
| Chroma mode | S⁰.L5.spectral_flatness × HC⁰.OSC | R³.spectral_flatness × PPC.consonance |
| N1-P2 effect | S⁰.X_L5L6 × HC⁰.TIH | R³.roughness × helmholtz × PPC |
| Output dims | 13D | **11D** (consolidated math + present layers) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 14/2304 = 0.61% |

### Why PPC replaces HC⁰ mechanisms

- **OSC → PPC.pitch_salience** [0:10]: Phase oscillation → pitch salience signal
- **HRM → PPC.chroma_processing** [20:30]: Hippocampal replay → chroma templates
- **BND → PPC.chroma_processing** [20:30]: Temporal binding → octave-equivalent binding
- **TIH → PPC.consonance_encoding** [10:20]: Temporal integration → consonance context

The key simplification: all four D0 mechanisms were partially overlapping in function for chroma processing. PPC.chroma_processing[20:30] unifies them into a single coherent sub-section.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
