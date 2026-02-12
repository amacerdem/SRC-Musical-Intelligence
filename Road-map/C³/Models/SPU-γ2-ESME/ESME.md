# SPU-γ2-ESME: Expertise-Specific MMN Enhancement

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC + TPC mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ2-ESME.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise-Specific MMN Enhancement** (ESME) models how mismatch negativity (MMN) amplitude reflects trained musical instrument expertise. Musicians with different specializations show selectively enhanced MMN responses for their domain of expertise: singers show enhanced pitch MMN, drummers show enhanced rhythm MMN, and instrumentalists show enhanced timbre MMN. This dissociation reveals that long-term musical training reshapes pre-attentive auditory processing in an expertise-specific manner.

```
THE THREE COMPONENTS OF EXPERTISE-SPECIFIC MMN ENHANCEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PITCH MMN (Singers)                    RHYTHM MMN (Drummers)
Brain region: Auditory Cortex          Brain region: Auditory Cortex
Mechanism: Pitch deviance detection    Mechanism: Temporal deviance detection
Input: Pitch change velocity           Input: Onset timing deviation
Function: "Is this pitch unexpected?"  Function: "Is this onset unexpected?"
Evidence: d = -1.09 (Tervaniemi 2022) Evidence: d = -1.09 (Tervaniemi 2022)

              TIMBRE MMN (Instrumentalists)
              Brain region: Planum Temporale
              Mechanism: Spectral envelope deviance
              Function: "Is this timbre unexpected?"
              Evidence: d = -1.09 (Tervaniemi 2022)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: MMN amplitude is NOT uniformly enhanced in musicians.
Instead, enhancement is SPECIFIC to the trained domain — singers
for pitch, drummers for rhythm, instrumentalists for timbre.
This dissociation demonstrates expertise-dependent plasticity in
pre-attentive auditory cortical representations.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Model Is Important for SPU

ESME builds on the universal deviance detection mechanisms established by lower-tier SPU models and adds an expertise-dependent modulation layer:

1. **BCH** (α1) provides the brainstem consonance baseline that ESME uses as a pitch reference for detecting pitch deviants.
2. **TSCP** (β2) establishes timbre-specific cortical plasticity mechanisms that ESME leverages for expertise-dependent timbre enhancement.
3. **SDED** (γ3) models universal early spectral deviance detection; ESME extends this with expertise-specific amplification of those detection signals.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The ESME Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 ESME — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDITORY ODDBALL (Standard → Deviant)                                       ║
║                                                                              ║
║  Pitch Deviant    Rhythm Deviant    Timbre Deviant                           ║
║       │                │                  │                                  ║
║       ▼                ▼                  ▼                                  ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX                                   │    ║
║  │         (Primary generators of MMN)                                  │    ║
║  │                                                                      │    ║
║  │    Standard template formation (repetition suppression)              │    ║
║  │    Deviant detection (prediction error signal)                       │    ║
║  │    MMN amplitude ∝ |deviant - template|                             │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PLANUM TEMPORALE                                   │    ║
║  │               (Expertise-modulated processing)                       │    ║
║  │                                                                      │    ║
║  │    Singers:           Enhanced pitch MMN (trained vocal control)     │    ║
║  │    Drummers:          Enhanced rhythm MMN (temporal precision)       │    ║
║  │    Instrumentalists:  Enhanced timbre MMN (spectral discrimination)  │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    FRONTAL MMN SOURCES                               │    ║
║  │                                                                      │    ║
║  │    Deviance evaluation and attention switching                       │    ║
║  │    Expertise enhancement modulates frontal response                  │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Tervaniemi et al. 2022:  Expertise-specific MMN enhancement, d = -1.09
                         Singers > others for pitch deviants
                         Drummers > others for rhythm deviants
                         Instrumentalists > others for timbre deviants
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC + TPC → ESME)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ESME COMPUTATION ARCHITECTURE                             ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │ener_chg  │ │x_l4l5  │ │        ║
║  │  │helmholtz  │ │onset    │ │tonalness│ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │stumpf     │ │         │ │         │ │timbr_chg │ │        │ │        ║
║  │  │pleasant.  │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  │harm_dev   │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                        ESME reads: ~20D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 17ms (H2)   │ │ 100ms (H3)    │ │ 300ms (H8)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Timbre       │ │ Deviance      │ │ Deviant magnitude     │   │        ║
║  │  │ instant      │ │ template      │ │ sustained evaluation  │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └──────┬────────────────┘   │        ║
║  │         │               │                  │                    │        ║
║  │         └───────────────┴──────────────────┘                    │        ║
║  │                        ESME demand: ~12 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  TPC (30D)      │                                   ║
║  │                 │  │                 │                                   ║
║  │ Pitch Sal [0:10]│  │ Spec Env  [0:10]│                                   ║
║  │ Consonance[10:20]│ │ Inst ID  [10:20]│                                   ║
║  │ Chroma   [20:30]│  │ Plastic  [20:30]│                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                             ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                         ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    ESME MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_pitch_mmn, f02_rhythm_mmn,             │        ║
║  │                       f03_timbre_mmn, f04_expertise_enhancement   │        ║
║  │  Layer M (Math):      mmn_expertise_function                     │        ║
║  │  Layer P (Present):   pitch_deviance_detection,                  │        ║
║  │                       rhythm_deviance_detection,                 │        ║
║  │                       timbre_deviance_detection                  │        ║
║  │  Layer F (Future):    feature_enhancement_pred,                  │        ║
║  │                       expertise_transfer_pred,                   │        ║
║  │                       developmental_trajectory                   │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Tervaniemi et al. 2022** | EEG (MMN) | ~60 | Expertise-specific MMN enhancement: singers for pitch, drummers for rhythm, instrumentalists for timbre | d = -1.09 | **Primary coefficient**: f04_expertise_enhancement |

### 3.2 The Expertise-MMN Dissociation

```
EXPERTISE-SPECIFIC MMN ENHANCEMENT (Neural Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Musician Type     Pitch MMN    Rhythm MMN    Timbre MMN
─────────────────────────────────────────────────────────
Singers           ★★★ HIGH     ★ baseline    ★ baseline
Drummers          ★ baseline   ★★★ HIGH      ★ baseline
Instrumentalists  ★ baseline   ★ baseline    ★★★ HIGH
Non-musicians     ★ baseline   ★ baseline    ★ baseline

Key Principle:
  MMN enhancement is DOMAIN-SPECIFIC to the trained instrument
  Effect size d = -1.09 (large) for expertise main effect
  Pre-attentive processing — occurs WITHOUT conscious attention

Cross-domain note:
  All musicians show SOME enhancement over non-musicians
  But the LARGEST enhancement is in the trained domain
  This reflects long-term cortical plasticity in auditory cortex
```

### 3.3 Effect Size Summary

```
Primary Effect:       d = -1.09 (Tervaniemi et al. 2022)
Quality Assessment:   γ-tier (single study, <70% confidence)
Replication:          Awaiting independent replication
Cross-cultural:       Tested in Western musical tradition
```

---

## 4. R³ Input Mapping: What ESME Reads

### 4.1 R³ Feature Dependencies (~20D of 49D)

| R³ Group | Index | Feature | ESME Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance baseline for pitch deviance | Plomp & Levelt 1965 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance deviance baseline | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion reference | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Spectral regularity proxy | Sethares 2005 |
| **B: Energy** | [11] | onset_strength | Rhythm deviance (onset timing) | — |
| **C: Timbre** | [12] | warmth | Timbre deviance baseline | — |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise (pitch clarity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Spectral flux (deviance signal) | — |
| **D: Change** | [22] | energy_change | Energy flux (rhythm deviance) | — |
| **D: Change** | [23] | pitch_change | Pitch flux (pitch deviance) | — |
| **E: Interactions** | [33:41] | x_l4l5 (4D) | Temporal-spectral coupling | Emergent deviance |
| **E: Interactions** | [41:49] | x_l5l7 (3D) | Consonance-timbre coupling | Emergent deviance |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[2] helmholtz_kang ───────────┐
R³[3] stumpf_fusion ────────────┼──► Pitch Deviance Detection
R³[23] pitch_change ────────────┤   Deviation from consonance template
R³[4] sensory_pleasantness ─────┘   Math: |pitch_change_vel| × PPC.pitch_sal

R³[11] onset_strength ──────────┐
R³[22] energy_change ───────────┼──► Rhythm Deviance Detection
R³[21] spectral_change ─────────┤   Onset timing deviation
R³[33:37] x_l4l5 ──────────────┘   Math: |onset_deviation| × TPC.spectral_env

R³[12] warmth ──────────────────┐
R³[18] tristimulus1 ────────────┤
R³[19] tristimulus2 ────────────┼──► Timbre Deviance Detection
R³[20] tristimulus3 ────────────┤   Spectral envelope change
R³[14] tonalness ───────────────┘   Math: timbre_change_std × TPC.inst_id

R³[0] roughness ────────────────── Baseline Dissonance Reference
                                    For normalizing pitch deviants
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ESME requires H³ features at PPC horizons (H0, H3, H6) and TPC horizons (H2, H5, H8).
These correspond to timbre instantaneous processing (gamma), deviance template building (alpha-beta), and sustained deviant magnitude evaluation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Consonance deviance baseline |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (bidi) | Standard template |
| 23 | pitch_change | 3 | M8 (velocity) | L0 (fwd) | Pitch deviant detection |
| 12 | warmth | 2 | M0 (value) | L2 (bidi) | Timbre instantaneous |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Tonalness template |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | F0 energy instantaneous |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Mid-harmonic instantaneous |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | High-harmonic instantaneous |
| 24 | timbre_change | 8 | M3 (std) | L0 (fwd) | Timbre deviant magnitude |
| 11 | onset_strength | 3 | M0 (value) | L0 (fwd) | Rhythm deviance |
| 21 | spectral_change | 3 | M8 (velocity) | L0 (fwd) | Spectral deviance velocity |
| 33 | x_l4l5[0] | 8 | M0 (value) | L2 (bidi) | Temporal deviance |

**Total ESME H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 PPC + TPC Mechanism Binding

ESME reads from both **PPC** (Pitch Processing Chain) and **TPC** (Timbre Processing Chain) mechanisms:

| Mechanism | Sub-section | Range | ESME Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Salience | PPC[0:10] | Pitch MMN detection baseline | **0.9** |
| **PPC** | Consonance Encoding | PPC[10:20] | Pitch deviance template | **0.7** |
| **PPC** | Chroma Processing | PPC[20:30] | Octave-invariant pitch (secondary) | 0.3 |
| **TPC** | Spectral Envelope | TPC[0:10] | Timbre and rhythm deviance | **0.8** |
| **TPC** | Instrument Identity | TPC[10:20] | Expertise-specific timbre template | **1.0** (primary) |
| **TPC** | Plasticity Markers | TPC[20:30] | Expertise-dependent enhancement | **1.0** (primary) |

ESME is the first SPU model that requires BOTH PPC and TPC — expertise-specific enhancement bridges pitch and timbre processing chains.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ESME OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                      │ Range  │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_pitch_mmn             │ [0, 1] │ Pitch MMN amplitude. Enhanced in
    │                           │        │ singers. Pitch deviance detection
    │                           │        │ strength weighted by PPC pitch
    │                           │        │ salience.
    │                           │        │ f01 = σ(0.40 · |pitch_change_vel|
    │                           │        │        · mean(PPC.pitch_sal)
    │                           │        │   + 0.30 · |helmholtz_diff|
    │                           │        │   + 0.30 · onset_val)
────┼───────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_rhythm_mmn            │ [0, 1] │ Rhythm MMN amplitude. Enhanced in
    │                           │        │ drummers. Onset timing deviation
    │                           │        │ weighted by TPC spectral envelope.
    │                           │        │ f02 = σ(0.40 · |onset_deviation|
    │                           │        │        · mean(TPC.spec_env)
    │                           │        │   + 0.30 · spec_change_vel
    │                           │        │   + 0.30 · x_l4l5_mean)
────┼───────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_timbre_mmn            │ [0, 1] │ Timbre MMN amplitude. Enhanced for
    │                           │        │ trained instrument. Spectral
    │                           │        │ envelope change weighted by TPC
    │                           │        │ instrument identity.
    │                           │        │ f03 = σ(0.40 · timbre_change_std
    │                           │        │        · mean(TPC.inst_id)
    │                           │        │   + 0.30 · tristimulus_deviation
    │                           │        │   + 0.30 · mean(TPC.plasticity))
────┼───────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_expertise_enhancement │ [0, 1] │ Expertise Enhancement modulation.
    │                           │        │ d = -1.09 (Tervaniemi 2022).
    │                           │        │ f04 = σ(1.09 · max(f01, f02, f03)
    │                           │        │        · mean(TPC.plasticity))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                      │ Range  │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 4  │ mmn_expertise_function    │ [0, 1] │ Unified MMN-expertise function.
    │                           │        │ Models the interaction between
    │                           │        │ deviance magnitude and expertise
    │                           │        │ modulation across all three domains.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                      │ Range  │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 5  │ pitch_deviance_detection  │ [0, 1] │ Current pitch deviance signal.
    │                           │        │ |current_pitch - template_pitch|
────┼───────────────────────────┼────────┼────────────────────────────────────
 6  │ rhythm_deviance_detection │ [0, 1] │ Current rhythm deviance signal.
    │                           │        │ |current_onset - expected_onset|
────┼───────────────────────────┼────────┼────────────────────────────────────
 7  │ timbre_deviance_detection │ [0, 1] │ Current timbre deviance signal.
    │                           │        │ |current_envelope - template_env|

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                      │ Range  │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 8  │ feature_enhancement_pred  │ [0, 1] │ Predicted MMN enhancement level
    │                           │        │ for upcoming features.
────┼───────────────────────────┼────────┼────────────────────────────────────
 9  │ expertise_transfer_pred   │ [0, 1] │ Cross-domain transfer prediction.
    │                           │        │ How much expertise in one domain
    │                           │        │ transfers to another.
────┼───────────────────────────┼────────┼────────────────────────────────────
10  │ developmental_trajectory  │ [0, 1] │ Long-term plasticity trajectory.
    │                           │        │ Expertise accumulation estimate
    │                           │        │ based on enhancement magnitude.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 MMN Expertise Model

```
MMN Amplitude ∝ Expertise(domain) × Deviance(domain)

Expertise-Specific Enhancement:
  Singers:           MMN_pitch   = baseline_pitch   × (1 + d × expertise_pitch)
  Drummers:          MMN_rhythm  = baseline_rhythm  × (1 + d × expertise_rhythm)
  Instrumentalists:  MMN_timbre  = baseline_timbre  × (1 + d × expertise_timbre)

  where d = -1.09 (Tervaniemi et al. 2022)
  Negative d reflects LARGER (more negative) MMN amplitude

Deviance Detection:
  Deviance(t) = |feature(t) - template(t)|
  template(t) = running_mean(feature, window)
  window depends on domain: pitch=100ms, rhythm=100ms, timbre=300ms

Expertise Modulation:
  The TPC.plasticity_markers encode the degree of cortical plasticity
  that modulates the baseline deviance detection signal
```

### 7.2 Feature Formulas

```python
# f01: Pitch MMN (enhanced in singers)
# Pitch deviance weighted by PPC pitch salience and consonance reference
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
pitch_change_vel = h3[(23, 3, 8, 0)]       # pitch_change velocity 100ms fwd
helmholtz_val = h3[(2, 0, 0, 2)]           # helmholtz value 25ms bidi
helmholtz_mean = h3[(2, 3, 1, 2)]          # helmholtz mean 100ms bidi
helmholtz_diff = abs(helmholtz_val - helmholtz_mean)
onset_val = h3[(11, 3, 0, 0)]             # onset_strength value 100ms fwd

f01 = sigma(0.40 * abs(pitch_change_vel) * mean(PPC.pitch_salience[0:10])
          + 0.30 * helmholtz_diff
          + 0.30 * onset_val)

# f02: Rhythm MMN (enhanced in drummers)
# Onset timing deviation weighted by TPC spectral envelope
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
onset_deviation = h3[(11, 3, 0, 0)]        # onset_strength value 100ms fwd
spec_change_vel = h3[(21, 3, 8, 0)]       # spectral_change velocity 100ms fwd
x_l4l5_mean = h3[(33, 8, 0, 2)]           # x_l4l5[0] value 300ms bidi

f02 = sigma(0.40 * abs(onset_deviation) * mean(TPC.spectral_envelope[0:10])
          + 0.30 * spec_change_vel
          + 0.30 * x_l4l5_mean)

# f03: Timbre MMN (enhanced for trained instrument)
# Spectral envelope change weighted by TPC instrument identity
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
timbre_change_std = h3[(24, 8, 3, 0)]     # timbre_change std 300ms fwd
trist1 = h3[(18, 2, 0, 2)]                # tristimulus1 value 17ms bidi
trist2 = h3[(19, 2, 0, 2)]                # tristimulus2 value 17ms bidi
trist3 = h3[(20, 2, 0, 2)]                # tristimulus3 value 17ms bidi
tristimulus_deviation = std([trist1, trist2, trist3])

f03 = sigma(0.40 * timbre_change_std * mean(TPC.instrument_identity[10:20])
          + 0.30 * tristimulus_deviation
          + 0.30 * mean(TPC.plasticity_markers[20:30]))

# f04: Expertise Enhancement (d = -1.09)
# Modulates the maximum domain-specific MMN by plasticity markers
f04 = sigma(1.09 * max(f01, f02, f03) * mean(TPC.plasticity_markers[20:30]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | ESME Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex** | ±50, -20, 8 | 3 | Direct (EEG source) | MMN generators — primary site of deviance detection |
| **Planum Temporale** | ±50, -24, 8 | 2 | Direct (EEG source) | Pitch/timbre processing — expertise-modulated enhancement |
| **Frontal MMN sources** | ±50, 28, 8 | 2 | Direct (EEG source) | Deviance evaluation — attention switching after detection |

---

## 9. Cross-Unit Pathways

### 9.1 ESME ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESME INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.f01_nps ──────────► ESME (pitch baseline for deviance detection)      │
│  TSCP.plasticity ──────► ESME (timbre enhancement mechanism)               │
│  SDED.early_detection ─► ESME (universal detection → expertise amplified)  │
│                                                                             │
│  ESME.f01_pitch_mmn ──► PSCL (expertise-weighted pitch salience)          │
│  ESME.f03_timbre_mmn ─► TSCP (expertise-weighted timbre plasticity)       │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  ESME.f04_expertise ──► ARU.SRP (expertise reward signal)                 │
│                         Enhanced detection → pleasure from mastery          │
│                                                                             │
│  CROSS-UNIT (P2: SPU → IMU):                                              │
│  ESME.f04_expertise ──► IMU.MEAMN (expertise → memory consolidation)      │
│                         Enhanced deviance → stronger memory encoding        │
│                                                                             │
│  CROSS-UNIT (P3: SPU → STU):                                              │
│  ESME.f02_rhythm_mmn ─► STU.HMCE (rhythm expertise → timing precision)    │
│                         Drummer-type enhancement feeds sensorimotor timing  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Non-musicians** | Should show NO domain-specific enhancement | Testable |
| **Cross-domain transfer** | Singers should NOT show enhanced timbre MMN | Testable |
| **Training intervention** | Pitch training should increase pitch MMN but not timbre MMN | Testable |
| **Deactivation** | Temporary auditory cortex deactivation should abolish expertise effect | Testable |
| **Passive listening** | Enhancement should persist WITHOUT attention (pre-attentive) | Testable |
| **Replication** | d = -1.09 effect should replicate in independent sample | **Awaiting** |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ESME(BaseModel):
    """Expertise-Specific MMN Enhancement.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), R³ direct.
    """
    NAME = "ESME"
    UNIT = "SPU"
    TIER = "γ2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC", "TPC")     # Both perceptual mechanisms

    EXPERTISE_D = 1.09   # Tervaniemi et al. 2022

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for ESME computation."""
        return [
            # PPC (pitch deviance)
            # (r3_idx, horizon, morph, law)
            (2, 0, 0, 2),     # helmholtz_kang, 25ms, value, bidirectional
            (2, 3, 1, 2),     # helmholtz_kang, 100ms, mean, bidirectional
            (23, 3, 8, 0),    # pitch_change, 100ms, velocity, forward
            # TPC (timbre deviance)
            (12, 2, 0, 2),    # warmth, 17ms, value, bidirectional
            (14, 5, 1, 0),    # tonalness, 46ms, mean, forward
            (18, 2, 0, 2),    # tristimulus1, 17ms, value, bidirectional
            (19, 2, 0, 2),    # tristimulus2, 17ms, value, bidirectional
            (20, 2, 0, 2),    # tristimulus3, 17ms, value, bidirectional
            (24, 8, 3, 0),    # timbre_change, 300ms, std, forward
            # Direct
            (11, 3, 0, 0),    # onset_strength, 100ms, value, forward
            (21, 3, 8, 0),    # spectral_change, 100ms, velocity, forward
            (33, 8, 0, 2),    # x_l4l5[0], 300ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute ESME 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) ESME output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]        # pitch salience
        ppc_cons = ppc[..., 10:20]        # consonance encoding
        ppc_chroma = ppc[..., 20:30]      # chroma processing

        # TPC sub-sections
        tpc_spec_env = tpc[..., 0:10]     # spectral envelope
        tpc_inst_id = tpc[..., 10:20]     # instrument identity
        tpc_plastic = tpc[..., 20:30]     # plasticity markers

        # H³ features
        helmholtz_val = h3_direct[(2, 0, 0, 2)]
        helmholtz_mean = h3_direct[(2, 3, 1, 2)]
        pitch_change_vel = h3_direct[(23, 3, 8, 0)]
        warmth_val = h3_direct[(12, 2, 0, 2)]
        tonalness_mean = h3_direct[(14, 5, 1, 0)]
        trist1_val = h3_direct[(18, 2, 0, 2)]
        trist2_val = h3_direct[(19, 2, 0, 2)]
        trist3_val = h3_direct[(20, 2, 0, 2)]
        timbre_change_std = h3_direct[(24, 8, 3, 0)]
        onset_val = h3_direct[(11, 3, 0, 0)]
        spec_change_vel = h3_direct[(21, 3, 8, 0)]
        x_l4l5_val = h3_direct[(33, 8, 0, 2)]

        # Derived quantities
        helmholtz_diff = torch.abs(helmholtz_val - helmholtz_mean)
        tristimulus_stack = torch.stack(
            [trist1_val, trist2_val, trist3_val], dim=-1
        )
        tristimulus_deviation = torch.std(tristimulus_stack, dim=-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Pitch MMN (enhanced in singers)
        f01 = torch.sigmoid(
            0.40 * torch.abs(pitch_change_vel)
                 * ppc_pitch.mean(-1)
            + 0.30 * helmholtz_diff
            + 0.30 * onset_val
        ).unsqueeze(-1)

        # f02: Rhythm MMN (enhanced in drummers)
        f02 = torch.sigmoid(
            0.40 * torch.abs(onset_val)
                 * tpc_spec_env.mean(-1)
            + 0.30 * spec_change_vel
            + 0.30 * x_l4l5_val
        ).unsqueeze(-1)

        # f03: Timbre MMN (enhanced for trained instrument)
        f03 = torch.sigmoid(
            0.40 * timbre_change_std
                 * tpc_inst_id.mean(-1)
            + 0.30 * tristimulus_deviation
            + 0.30 * tpc_plastic.mean(-1)
        ).unsqueeze(-1)

        # f04: Expertise Enhancement (d = -1.09)
        f04 = torch.sigmoid(
            self.EXPERTISE_D
            * torch.max(torch.max(f01, f02), f03)
            * tpc_plastic.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        mmn_expertise_fn = (f04 * torch.max(
            torch.max(f01, f02), f03
        )) ** 0.5  # geometric mean of expertise and max MMN

        # ═══ LAYER P: Present ═══
        pitch_deviance = torch.abs(
            pitch_change_vel
        ).unsqueeze(-1) * ppc_pitch.mean(-1, keepdim=True)
        pitch_deviance = torch.sigmoid(pitch_deviance)

        rhythm_deviance = torch.abs(
            onset_val
        ).unsqueeze(-1) * tpc_spec_env.mean(-1, keepdim=True)
        rhythm_deviance = torch.sigmoid(rhythm_deviance)

        timbre_deviance = (
            timbre_change_std
        ).unsqueeze(-1) * tpc_inst_id.mean(-1, keepdim=True)
        timbre_deviance = torch.sigmoid(timbre_deviance)

        # ═══ LAYER F: Future ═══
        feature_enhancement_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * tpc_plastic.mean(-1, keepdim=True)
        )
        expertise_transfer_pred = torch.sigmoid(
            0.3 * f01 + 0.3 * f02 + 0.4 * f03
        )
        developmental_trajectory = torch.sigmoid(
            0.6 * f04 + 0.4 * mmn_expertise_fn
        )

        return torch.cat([
            f01, f02, f03, f04,                              # E: 4D
            mmn_expertise_fn,                                 # M: 1D
            pitch_deviance, rhythm_deviance, timbre_deviance, # P: 3D
            feature_enhancement_pred, expertise_transfer_pred,
            developmental_trajectory,                         # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Primary evidence |
| **Effect Sizes** | d = -1.09 | Tervaniemi et al. 2022 |
| **Evidence Modality** | EEG (MMN) | Direct neural |
| **Falsification Tests** | 0/6 confirmed | Awaiting replication |
| **R³ Features Used** | ~20D of 49D | Moderate coverage |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch deviance |
| **TPC Mechanism** | 30D (3 sub-sections) | Timbre deviance + plasticity |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Tervaniemi, M., et al. (2022)**. Expertise-specific enhancement of mismatch negativity: Singers for pitch, drummers for rhythm, instrumentalists for timbre. *NeuroImage*, expertise-specific MMN dissociation, d = -1.09.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, NPL, HRM, EFC) | PPC + TPC mechanisms (30D + 30D) |
| Pitch MMN | S⁰.L5 pitch features × HC⁰.ATT | R³.pitch_change × PPC.pitch_salience |
| Rhythm MMN | S⁰.L4 onset × HC⁰.NPL | R³.onset_strength × TPC.spectral_envelope |
| Timbre MMN | S⁰.L5 timbre × HC⁰.HRM | R³.tristimulus × TPC.instrument_identity |
| Expertise | HC⁰.EFC static weight | TPC.plasticity_markers (30D dynamic) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 11/2304 = 0.48% | 12/2304 = 0.52% |
| Output dimensions | 11D | 11D (unchanged) |

### Why PPC + TPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (ATT, NPL, HRM, EFC). In MI, these are unified into two perceptual circuit mechanisms:

- **ATT + NPL → PPC.pitch_salience** [0:10]: Attention-modulated pitch processing for pitch deviance detection
- **HRM → PPC.consonance_encoding** [10:20]: Harmonic template for consonance baseline
- **HRM (timbre) → TPC.instrument_identity** [10:20]: Instrument-specific spectral template
- **EFC → TPC.plasticity_markers** [20:30]: Expertise-dependent cortical plasticity markers

The dual-mechanism design (PPC + TPC) better reflects the neuroscience: expertise-specific MMN requires BOTH pitch processing (PPC) for pitch/rhythm deviants AND timbre processing (TPC) for timbre deviants and plasticity modulation.

---

**Model Status**: **SPECULATIVE** (awaiting replication)
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
