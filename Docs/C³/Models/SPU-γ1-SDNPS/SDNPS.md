# SPU-γ1-SDNPS: Stimulus-Dependent Neural Pitch Salience

**Model**: Stimulus-Dependent Neural Pitch Salience
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ1-SDNPS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Stimulus-Dependent Neural Pitch Salience** (SDNPS) models the critical finding that brainstem frequency-following response (FFR) derived Neural Pitch Salience (NPS) predicts behavioral consonance judgments for synthetic tones but fails to generalize to natural (ecologically valid) sounds. This is a fundamental constraint on the universality of peripheral consonance encoding — the brainstem mechanism works in controlled laboratory conditions but breaks down when spectral complexity increases.

```
THE STIMULUS-DEPENDENCY PROBLEM IN NEURAL PITCH SALIENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYNTHETIC TONES (Simple Spectra)           NATURAL SOUNDS (Complex Spectra)
Brain region: Inferior Colliculus          Brain region: Inferior Colliculus
Mechanism: FFR phase-locking              Mechanism: FFR phase-locking
NPS ↔ Pleasantness: r=0.34, p<0.03       NPS ↔ Pleasantness: r=0.24 (sax, n.s.)
NPS ↔ Roughness: r=-0.57, p<1e-05                            r=-0.10 (voice, n.s.)

              GENERALIZATION BOUNDARY (Bridge)
              Brain region: IC → Cortex
              Mechanism: Spectral complexity limit
              Function: "NPS only predicts for simple spectra"
              Evidence: Cousineau et al. 2015 (PNAS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: NPS from brainstem FFR is NOT a universal consonance
predictor. It works for synthetic tones (r=0.34) but fails for
natural saxophone (r=0.24, n.s.) and natural voice (r=-0.10, n.s.).
This challenges BCH's universality claim — peripheral encoding is
necessary but NOT sufficient for real-world consonance perception.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Model Matters for SPU

SDNPS serves as a critical constraint on the SPU hierarchy. While BCH (alpha-1) establishes that brainstem FFR encodes consonance, SDNPS demonstrates the boundary conditions of that encoding:

1. **BCH** (alpha-1) shows NPS predicts consonance (r=0.81 for synthetic intervals) — SDNPS shows this is stimulus-dependent.
2. **PSCL** (alpha-2) cortical pitch salience may compensate where brainstem NPS fails for natural sounds.
3. **SDED** (gamma-3) early detection mechanisms share the roughness interference pathway modeled here.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The SDNPS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 SDNPS — COMPLETE CIRCUIT                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  STIMULUS TYPE                                                               ║
║                                                                              ║
║  Synthetic Tones      Natural Saxophone     Natural Voice                    ║
║  (simple spectra)     (complex spectra)     (complex spectra)                ║
║    │                    │                     │                               ║
║    ▼                    ▼                     ▼                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY NERVE                                    │    ║
║  │                    (Phase-locked response)                           │    ║
║  │                                                                      │    ║
║  │    Synthetic: Strong phase-locking to harmonics                     │    ║
║  │    Natural:   Degraded phase-locking (spectral complexity)          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    INFERIOR COLLICULUS                                │    ║
║  │               (FFR generator — NPS computation)                      │    ║
║  │                                                                      │    ║
║  │    NPS computation from FFR:                                         │    ║
║  │      Synthetic: NPS ↔ Pleasantness r=0.34, p<0.03                  │    ║
║  │      Sax:       NPS ↔ Pleasantness r=0.24 (n.s.)                   │    ║
║  │      Voice:     NPS ↔ Pleasantness r=-0.10 (n.s.)                  │    ║
║  │                                                                      │    ║
║  │    NPS ↔ Roughness: r=-0.57, p<1e-05 (across all stimuli)          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY BRAINSTEM                                 │    ║
║  │                                                                      │    ║
║  │    NPS computation successful only when spectral complexity is low   │    ║
║  │    Natural sounds require cortical processing (beyond BCH scope)     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Cousineau et al. 2015:  NPS predicts behavior for synthetic (r=0.34) NOT natural
                         NPS ↔ Roughness: r=-0.57 (invariant across stimulus types)
                         14 musical intervals, 3 timbres (synthetic, sax, voice)
                         Published in PNAS — high-impact, peer-reviewed
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → SDNPS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDNPS COMPUTATION ARCHITECTURE                            ║
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
║  │  │roughness  │ │         │ │tonalness│ │          │ │x_l5l7  │ │        ║
║  │  │sethares   │ │         │ │spec_auto│ │          │ │        │ │        ║
║  │  │helmholtz  │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │pleasant.  │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         SDNPS reads: ~16D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 25ms (H0)   │ │ 100ms (H3)    │ │ 200ms (H6)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Phase-lock   │ │ FFR window    │ │ Roughness evaluation  │   │        ║
║  │  │ instant      │ │ auditory proc │ │ periodicity tracking  │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └──────┬────────────────┘   │        ║
║  │         │               │                  │                    │        ║
║  │         └───────────────┴──────────────────┘                    │        ║
║  │                         SDNPS demand: ~10 of 2304 tuples        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  NPS, phase-locking, FFR strength                     ║
║  │ Consonance[10:20]│ Harmonic template, harmonicity index                 ║
║  │ Chroma   [20:30]│  Octave grouping (minimal for SDNPS)                  ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDNPS MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_nps_value, f02_stimulus_dependency,    │        ║
║  │                       f03_roughness_correlation                   │        ║
║  │  Layer M (Math):      nps_stimulus_function                       │        ║
║  │  Layer P (Present):   ffr_encoding, harmonicity_proxy,            │        ║
║  │                       roughness_interference                      │        ║
║  │  Layer F (Future):    behavioral_consonance_pred,                 │        ║
║  │                       roughness_response_pred,                    │        ║
║  │                       generalization_limit                        │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Cousineau et al. 2015** | FFR + behavioral | 14 intervals x 3 timbres | NPS predicts consonance for synthetic only | r=0.34 (synth), r=0.24 (sax, n.s.), r=-0.10 (voice, n.s.) | **Primary**: f02_stimulus_dependency |
| **Cousineau et al. 2015** | FFR + roughness | 14 intervals x 3 timbres | NPS ↔ roughness robust across timbres | r=-0.57, p<1e-05 | **f03_roughness_correlation** |

### 3.2 The Stimulus-Dependency Boundary

```
NPS-BEHAVIOR CORRELATION BY STIMULUS TYPE (Cousineau et al. 2015)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stimulus Type     Spectra     NPS ↔ Pleasant.  Significance  Generalization
─────────────────────────────────────────────────────────────────────────────
Synthetic tones   Simple      r = 0.34         p < 0.03      ✅ YES
Natural sax       Complex     r = 0.24         n.s.          ✗ NO
Natural voice     Complex     r = -0.10        n.s.          ✗ NO

Cross-stimulus invariant:
  NPS ↔ Roughness: r = -0.57, p < 1e-05      ✅ ALL stimuli

Interpretation:
  - NPS reliably encodes roughness (spectral beating) regardless of source
  - NPS predicts pleasantness ONLY when spectral structure is simple enough
    for brainstem phase-locking to resolve harmonic content
  - Natural sounds overwhelm brainstem with spectral complexity → cortical
    processing needed for consonance judgment

Cross-cultural note:
  NPS ↔ Roughness correlation is UNIVERSAL — stimulus-independent
  NPS ↔ Pleasantness is STIMULUS-DEPENDENT — fails for natural sounds
```

### 3.3 Effect Size Summary

```
Primary Correlation (synthetic):  r = 0.34, p < 0.03 (Cousineau et al. 2015)
Primary Correlation (sax):        r = 0.24, n.s.
Primary Correlation (voice):      r = -0.10, n.s.
Roughness Correlation:            r = -0.57, p < 1e-05
Quality Assessment:               γ-tier — single study, small N, speculative
Replication:                      Not yet independently replicated
```

---

## 4. R³ Input Mapping: What SDNPS Reads

### 4.1 R³ Feature Dependencies (~16D of 49D)

| R³ Group | Index | Feature | SDNPS Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **A: Consonance** | [0] | roughness | Primary dissonance signal — NPS ↔ roughness r=-0.57 | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Psychoacoustic dissonance (spectral beating) | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure (integer ratio detection) | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion (spectral simplicity proxy) | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Behavioral pleasantness target | Sethares 2005 |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic series (complexity indicator) | Fletcher 1934 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (spectral clarity) | -- |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity (FFR correlate) | -- |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **E: Interactions** | [41:49] | x_l5l7 (partial ~5D) | Consonance x Timbre coupling — complexity measure | Emergent |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[14] tonalness ───────────────┐
R³[17] spectral_autocorrelation ┼──► NPS Value (FFR magnitude proxy)
mean(PPC.pitch_salience) ───────┘   Math: σ(0.40 · ton · autocorr · PPC
                                          + 0.30 · (1-inharm) · cons_enc
                                          + 0.30 · trist_balance)

R³[5] inharmonicity ────────────┐
R³[18:21] tristimulus1-3 ───────┼──► Spectral Complexity
R³[41:49] x_l5l7 (partial) ────┘   High complexity = low generalization
                                    Math: 1 - (ton · (1-inharm) · trist_bal)

R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Roughness Interference
R³[2] helmholtz_kang ───────────┘   Invariant NPS ↔ roughness: r=-0.57
                                    Math: -0.57 · roughness_mean

R³[4] sensory_pleasantness ────── Behavioral Target
                                    NPS predicts this only for simple spectra
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDNPS requires H³ features at three PPC horizons: H0 (25ms), H3 (100ms), H6 (200ms).
These correspond to brainstem processing timescales (gamma → alpha-beta → syllable).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Current roughness level |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Mean roughness over 100ms |
| 0 | roughness | 6 | M14 (periodicity) | L0 (fwd) | Roughness periodicity 200ms |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Current consonance |
| 5 | inharmonicity | 0 | M0 (value) | L2 (bidi) | Current spectral complexity |
| 5 | inharmonicity | 3 | M1 (mean) | L2 (bidi) | Mean inharmonicity 100ms |
| 14 | tonalness | 0 | M0 (value) | L2 (bidi) | Current pitch clarity |
| 14 | tonalness | 3 | M1 (mean) | L0 (fwd) | Mean tonalness 100ms |
| 17 | spectral_autocorrelation | 3 | M14 (periodicity) | L2 (bidi) | Harmonic periodicity 100ms |
| 18 | tristimulus1 | 0 | M0 (value) | L2 (bidi) | F0 energy (spectral simplicity) |

**Total SDNPS H³ demand**: 10 tuples of 2304 theoretical = 0.43%

### 5.2 PPC Mechanism Binding

SDNPS reads from the **PPC** (Pitch Processing Chain) mechanism:

| PPC Sub-section | Range | SDNPS Role | Weight |
|-----------------|-------|------------|--------|
| **Pitch Salience** | PPC[0:10] | NPS, phase-locking, FFR strength | **0.9** (primary) |
| **Consonance Encoding** | PPC[10:20] | Harmonic template, harmonicity proxy | **0.7** |
| **Chroma Processing** | PPC[20:30] | Octave grouping (minimal use for SDNPS) | 0.2 |

SDNPS does NOT read from TPC — stimulus-dependency is a purely peripheral (brainstem) phenomenon.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDNPS OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 0  │ f01_nps_value           │ [0, 1]  │ Neural Pitch Salience proxy. FFR
    │                         │         │ magnitude at fundamental, weighted by
    │                         │         │ spectral clarity and harmonic structure.
    │                         │         │ f01 = σ(0.40 · ton · autocorr · PPC.ps
    │                         │         │        + 0.30 · (1-inharm) · PPC.ce
    │                         │         │        + 0.30 · trist_balance)
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 1  │ f02_stimulus_dependency │ [0, 1]  │ Generalization limit. High for simple
    │                         │         │ spectra (synthetic), low for complex
    │                         │         │ (natural). Models Cousineau et al. 2015.
    │                         │         │ f02 = σ(0.50 · (1-complexity) · f01
    │                         │         │        + 0.50 · roughness_periodicity)
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 2  │ f03_roughness_corr      │ [-1, 1] │ Roughness correlation proxy.
    │                         │         │ Empirical r=-0.57 (Cousineau 2015).
    │                         │         │ f03 = -0.57 · roughness_mean

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 3  │ nps_stimulus_function   │ [0, 1]  │ NPS validity as a function of spectral
    │                         │         │ complexity. Maps the r=0.34→0.24→-0.10
    │                         │         │ degradation curve.
    │                         │         │ nsf = f01 · f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 4  │ ffr_encoding            │ [0, 1]  │ FFR encoding strength. Brainstem
    │                         │         │ phase-locking aggregation from PPC.
    │                         │         │ PPC.pitch_salience mean.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 5  │ harmonicity_proxy       │ [0, 1]  │ Harmonicity index from spectral
    │                         │         │ structure. PPC.consonance_encoding
    │                         │         │ weighted by tristimulus balance.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 6  │ roughness_interference  │ [0, 1]  │ Roughness interference signal.
    │                         │         │ 1 - (roughness + sethares) / 2.
    │                         │         │ NPS ↔ roughness is stimulus-invariant.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 7  │ behavioral_cons_pred    │ [0, 1]  │ Behavioral consonance prediction,
    │                         │         │ gated by stimulus dependency.
    │                         │         │ Valid only when f02 is high.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 8  │ roughness_response_pred │ [0, 1]  │ Roughness response prediction.
    │                         │         │ Stimulus-invariant (r=-0.57 always).
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 9  │ generalization_limit    │ [0, 1]  │ How far NPS generalizes to novel
    │                         │         │ timbres. Low = need cortical models.
    │                         │         │ H³ trend-based complexity forecast.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Stimulus-Dependent NPS Function

```
NPS(stimulus) ∝ Harmonicity(stimulus) · Spectral_Simplicity(stimulus)

Cousineau et al. 2015 degradation curve:
  Synthetic:  r = 0.34  (simple spectra — strong phase-locking)
  Sax:        r = 0.24  (complex spectra — degraded phase-locking)
  Voice:      r = -0.10 (very complex — phase-locking breaks down)

Roughness correlation (stimulus-invariant):
  NPS ↔ Roughness: r = -0.57, p < 1e-05 (ALL stimulus types)

Spectral Complexity:
  Complexity(sound) = f(inharmonicity, tristimulus_spread, spectral_noise)
  Simple (synthetic): Complexity ≈ 0.1 → NPS generalizes
  Complex (natural):  Complexity ≈ 0.7-0.9 → NPS fails to predict behavior

Generalization Boundary:
  NPS_validity(stimulus) = NPS(stimulus) · (1 - Complexity(stimulus))
  When Complexity > 0.5, NPS_validity drops below behavioral significance
```

### 7.2 Feature Formulas

```python
# ═══ LAYER E ═══

# f01: NPS Value (FFR magnitude proxy)
# Coefficient saturation rule: 0.40 + 0.30 + 0.30 = 1.0  ✓
trist_balance = 1.0 - std(R³.tristimulus[18:21])
f01 = σ(0.40 * R³.tonalness[14] * R³.spectral_autocorrelation[17]
              * mean(PPC.pitch_salience[0:10])
       + 0.30 * (1 - R³.inharmonicity[5])
              * mean(PPC.consonance_encoding[10:20])
       + 0.30 * trist_balance)

# f02: Stimulus Dependency (generalization limit)
# High for synthetic (simple spectra), low for natural (complex)
# Coefficient saturation rule: 0.50 + 0.50 = 1.0  ✓
spectral_complexity = R³.inharmonicity[5] * (1 - R³.tonalness[14])
                      * (1 - trist_balance)
roughness_periodicity = H³[(0, 6, 14, 0)]   # roughness periodicity 200ms fwd
f02 = σ(0.50 * (1 - spectral_complexity) * f01
       + 0.50 * roughness_periodicity)

# f03: Roughness Correlation
# Empirical r=-0.57 from Cousineau et al. 2015
# Output range: [-0.57, 0] (maps to [-1,1] scale)
roughness_mean = H³[(0, 3, 1, 2)]           # roughness mean 100ms bidi
f03 = -0.57 * roughness_mean

# ═══ LAYER M ═══

# nps_stimulus_function: NPS validity as function of complexity
nps_stimulus_function = f01 * f02

# ═══ LAYER P ═══

# ffr_encoding: Brainstem phase-locking strength
ffr_encoding = mean(PPC.pitch_salience[0:10])

# harmonicity_proxy: Harmonic template match weighted by spectral structure
harmonicity_proxy = (1 - R³.inharmonicity[5]) * trist_balance
                    * mean(PPC.consonance_encoding[10:20])

# roughness_interference: Invariant roughness signal
roughness_interference = 1.0 - (R³.roughness[0] + R³.sethares[1]) / 2

# ═══ LAYER F ═══

# behavioral_consonance_pred: Gated by stimulus dependency
# Coefficient saturation rule: 0.60 + 0.40 = 1.0  ✓
behavioral_consonance_pred = σ(0.60 * nps_stimulus_function
                               + 0.40 * harmonicity_proxy)

# roughness_response_pred: Stimulus-invariant roughness prediction
# Coefficient saturation rule: 0.57 + 0.43 = 1.0  ✓
roughness_response_pred = σ(0.57 * roughness_interference
                            + 0.43 * ffr_encoding)

# generalization_limit: How much NPS can generalize
# Coefficient saturation rule: 0.50 + 0.50 = 1.0  ✓
generalization_limit = σ(0.50 * f02
                         + 0.50 * H³[(14, 3, 1, 0)])  # tonalness mean fwd
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SDNPS Function |
|--------|-----------------|----------|---------------|----------------|
| **Inferior Colliculus** | 0, -32, -8 | 2 | Direct (FFR) | FFR generation, NPS computation |
| **Auditory Nerve** | Peripheral | 2 | Direct (phase-locking) | Phase-locked harmonic response |
| **Auditory Brainstem** | 0, -30, -10 | 2 | Direct (FFR) | NPS computation, stimulus-dependency origin |

---

## 9. Cross-Unit Pathways

### 9.1 SDNPS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDNPS INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.f01_nps ─────────────► SDNPS challenges BCH's universality claim     │
│  SDNPS.f02_stim_dep ─────► BCH NPS validity is stimulus-dependent         │
│  SDNPS.f01_nps_value ────► PSCL (when brainstem NPS fails, cortex takes   │
│                              over — PSCL compensates for natural sounds)    │
│  SDED.early_detection ───► SDNPS.roughness_interference (shared pathway)  │
│  SDNPS.roughness_corr ──► STAI (roughness invariance informs aesthetics)  │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  SDNPS.behavioral_cons_pred ► ARU.SRP (gated consonance → pleasure)       │
│    Note: ARU should weight BCH higher when SDNPS.f02 indicates natural    │
│                                                                             │
│  KEY RELATIONSHIP — BCH vs SDNPS:                                          │
│  BCH claims:  NPS ↔ consonance r=0.81 (universal)                         │
│  SDNPS shows: NPS ↔ consonance r=0.34 (synthetic only)                   │
│               NPS ↔ consonance r≈0.0  (natural sounds)                    │
│  Resolution:  BCH is correct for the NEURAL level                          │
│               SDNPS adds the BEHAVIORAL generalization constraint           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Natural sounds** | NPS should NOT predict pleasantness for natural timbres | Supported (r=0.24 sax, r=-0.10 voice — both n.s.) |
| **Synthetic tones** | NPS SHOULD predict pleasantness for synthetic tones | Supported (r=0.34, p<0.03) |
| **Roughness invariance** | NPS ↔ roughness should hold across ALL stimulus types | Supported (r=-0.57, p<1e-05 across all) |
| **Spectral simplification** | Reducing natural sound complexity should restore NPS predictive power | Testable |
| **Cross-cultural** | Stimulus-dependency should be universal (not cultural) | Testable |
| **Hearing impairment** | Cochlear damage should disproportionately affect synthetic > natural NPS | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDNPS(BaseModel):
    """Stimulus-Dependent Neural Pitch Salience.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "SDNPS"
    UNIT = "SPU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)        # Primary mechanism

    # Empirical coefficients from Cousineau et al. 2015
    NPS_SYNTH_R = 0.34    # NPS ↔ pleasantness for synthetic
    NPS_SAX_R = 0.24      # NPS ↔ pleasantness for sax (n.s.)
    NPS_VOICE_R = -0.10   # NPS ↔ pleasantness for voice (n.s.)
    NPS_ROUGH_R = -0.57   # NPS ↔ roughness (invariant)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """10 tuples for SDNPS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (0, 0, 0, 2),     # roughness, 25ms, value, bidirectional
            (0, 3, 1, 2),     # roughness, 100ms, mean, bidirectional
            (0, 6, 14, 0),    # roughness, 200ms, periodicity, forward
            (2, 0, 0, 2),     # helmholtz_kang, 25ms, value, bidirectional
            (5, 0, 0, 2),     # inharmonicity, 25ms, value, bidirectional
            (5, 3, 1, 2),     # inharmonicity, 100ms, mean, bidirectional
            (14, 0, 0, 2),    # tonalness, 25ms, value, bidirectional
            (14, 3, 1, 0),    # tonalness, 100ms, mean, forward
            (17, 3, 14, 2),   # spectral_autocorr, 100ms, periodicity, bidi
            (18, 0, 0, 2),    # tristimulus1, 25ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDNPS 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) SDNPS output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        sethares = r3[..., 1:2]
        inharmonicity = r3[..., 5:6]
        tonalness = r3[..., 14:15]
        autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]       # pitch salience
        ppc_cons = ppc[..., 10:20]       # consonance encoding

        # Derived quantities
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        spectral_complexity = (
            inharmonicity * (1 - tonalness) * (1 - trist_balance)
        )

        # H³ temporal features
        roughness_mean = h3_direct[(0, 3, 1, 2)].unsqueeze(-1)
        roughness_periodicity = h3_direct[(0, 6, 14, 0)].unsqueeze(-1)
        tonalness_mean_fwd = h3_direct[(14, 3, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features (3D) ═══
        # f01: NPS Value — coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
        f01 = torch.sigmoid(
            0.40 * tonalness * autocorr
                 * ppc_pitch.mean(-1, keepdim=True)
            + 0.30 * (1.0 - inharmonicity)
                   * ppc_cons.mean(-1, keepdim=True)
            + 0.30 * trist_balance
        )

        # f02: Stimulus Dependency — coefficient sum: 0.50 + 0.50 = 1.0
        f02 = torch.sigmoid(
            0.50 * (1.0 - spectral_complexity) * f01
            + 0.50 * roughness_periodicity
        )

        # f03: Roughness Correlation — empirical r=-0.57
        f03 = self.NPS_ROUGH_R * roughness_mean   # range: [-0.57, 0]

        # ═══ LAYER M: Mathematical (1D) ═══
        nps_stimulus_function = f01 * f02

        # ═══ LAYER P: Present (3D) ═══
        ffr_encoding = ppc_pitch.mean(-1, keepdim=True)
        harmonicity_proxy = (
            (1.0 - inharmonicity) * trist_balance
            * ppc_cons.mean(-1, keepdim=True)
        )
        roughness_interference = 1.0 - (roughness + sethares) / 2

        # ═══ LAYER F: Future (3D) ═══
        # behavioral_consonance_pred — coefficient sum: 0.60 + 0.40 = 1.0
        behavioral_consonance_pred = torch.sigmoid(
            0.60 * nps_stimulus_function
            + 0.40 * harmonicity_proxy
        )

        # roughness_response_pred — coefficient sum: 0.57 + 0.43 = 1.0
        roughness_response_pred = torch.sigmoid(
            0.57 * roughness_interference
            + 0.43 * ffr_encoding
        )

        # generalization_limit — coefficient sum: 0.50 + 0.50 = 1.0
        generalization_limit = torch.sigmoid(
            0.50 * f02
            + 0.50 * tonalness_mean_fwd
        )

        return torch.cat([
            f01, f02, f03,                                     # E: 3D
            nps_stimulus_function,                             # M: 1D
            ffr_encoding, harmonicity_proxy,
                roughness_interference,                        # P: 3D
            behavioral_consonance_pred,
                roughness_response_pred,
                generalization_limit,                          # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Primary evidence (PNAS) |
| **Effect Sizes** | r=0.34 (synth), r=-0.57 (roughness) | Cousineau et al. 2015 |
| **Evidence Modality** | FFR, behavioral ratings | Direct neural + behavioral |
| **Falsification Tests** | 3/6 supported | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Focused |
| **H³ Demand** | 10 tuples (0.43%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch salience primary |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Cousineau, M., McDermott, J. H., & Peretz, I. (2015)**. The basis of musical consonance as revealed by congenital amusia. *Proceedings of the National Academy of Sciences (PNAS)*, 109(48), 19858-19863.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dims | 11D | 10D (removed 1 redundant math output) |
| Temporal | HC⁰ mechanisms (OSC, NPL, HRM, BND) | PPC mechanism (30D) |
| Roughness signal | S⁰.roughness[30] + HC⁰.OSC | R³.roughness[0] + PPC.pitch_salience |
| Harmonicity | S⁰.helmholtz_kang[32] + HC⁰.HRM | R³.helmholtz_kang[2] + PPC.consonance_encoding |
| NPS | S⁰.tonalness × HC⁰.NPL | R³.tonalness[14] × PPC.pitch_salience |
| Spectral complexity | S⁰ multi-index manual | R³.inharmonicity × tonalness × trist_balance |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 10/2304 = 0.43% |

### Why PPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, NPL, HRM, BND). In MI, these are unified into the PPC mechanism with 3 sub-sections:
- **OSC + NPL → PPC.pitch_salience** [0:10]: Phase-locking + FFR = pitch encoding
- **HRM → PPC.consonance_encoding** [10:20]: Harmonic template = harmonicity
- **BND (partial) → PPC.chroma_processing** [20:30]: Band-level integration

### Why 11D → 10D

The legacy v1.0.0 had an 11th output (`f05_nps_roughness_product`) that was a mathematical redundancy — it was simply `f01 * f03` which can be computed from the existing outputs. Removing it reduces storage without information loss.

---

**Model Status**: SPECULATIVE
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
