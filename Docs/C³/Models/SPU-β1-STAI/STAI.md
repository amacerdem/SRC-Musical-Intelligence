# SPU-β1-STAI: Spectral-Temporal Aesthetic Integration

**Model**: Spectral-Temporal Aesthetic Integration
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-β1-STAI.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Spectral-Temporal Aesthetic Integration** (STAI) model describes how musical aesthetic appreciation emerges from the interaction between spectral structure (consonance/dissonance) and temporal structure (forward/reversed playback). Aesthetic preference peaks at intermediate spectral complexity combined with temporal predictability — when both dimensions are disrupted, activation in reward regions (NAcc, putamen) and auditory cortex (STG) drops, and vmPFC-IFG connectivity decreases.

```
THE TWO DIMENSIONS OF AESTHETIC INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPECTRAL INTEGRITY (Consonance)           TEMPORAL INTEGRITY (Direction)
Brain regions: STG, Planum Temporale      Brain regions: NAcc, Putamen, GP
Mechanism: PPC consonance encoding        Mechanism: TPC spectral envelope
Input: Harmonic structure quality         Input: Forward temporal flow
Function: "How consonant is this?"        Function: "Is this temporally intact?"
Evidence: d=0.52 (Kim 2019)              Evidence: d=0.52 (Kim 2019)

              AESTHETIC INTEGRATION (Bridge)
              Brain regions: vmPFC → IFG
              Mechanism: Spectral x Temporal interaction
              Function: "Combined aesthetic value"
              Evidence: vmPFC-IFG connectivity d=0.52

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Aesthetic preference peaks at intermediate spectral
complexity x temporal predictability. Neither dimension alone
suffices — the INTERACTION term (Spectral x Temporal) drives the
full aesthetic response. Kim 2019 used a 2x2 factorial design
(consonant/dissonant x forward/reversed) to demonstrate this.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why STAI Matters for SPU

STAI sits at the integrative level of the spectral processing hierarchy. It combines the consonance signals established by lower-tier SPU models with temporal structure to produce aesthetic valuation:

1. **BCH** (α1) provides the brainstem consonance signal that STAI uses as spectral integrity input.
2. **PSCL** (α2) provides cortical pitch salience that feeds STAI's pitch quality assessment.
3. **STAI** (β1) integrates spectral and temporal dimensions for aesthetic evaluation, bridging perceptual processing to reward circuitry (ARU).

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The STAI Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 STAI — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL STIMULUS (2x2 factorial design)                                     ║
║                                                                              ║
║  Consonant+Forward   Consonant+Reversed   Dissonant+Forward   Both Disrupted ║
║         │                    │                    │                  │        ║
║         ▼                    ▼                    ▼                  ▼        ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG)                            │    ║
║  │           (Bilateral superior temporal gyrus)                       │    ║
║  │                                                                     │    ║
║  │    Spectral disruption → ↓bilateral STG, planum temporale          │    ║
║  │    Intact consonance → full STG activation                          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                    ┌─────────┴─────────┐                                     ║
║                    ▼                   ▼                                      ║
║  ┌──────────────────────┐  ┌──────────────────────┐                         ║
║  │   REWARD CIRCUIT     │  │   VALUATION CIRCUIT  │                         ║
║  │   (NAcc, Putamen,    │  │   (vmPFC, IFG)       │                         ║
║  │    Globus Pallidus)  │  │                       │                         ║
║  │                      │  │   vmPFC-IFG coupling  │                         ║
║  │  Temporal disruption │  │   Both disrupted →    │                         ║
║  │  → ↓activation       │  │   ↓connectivity       │                         ║
║  └──────────┬───────────┘  └──────────┬────────────┘                         ║
║             │                         │                                       ║
║             └────────────┬────────────┘                                       ║
║                          ▼                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AESTHETIC JUDGMENT                                │    ║
║  │                                                                     │    ║
║  │    Both intact:     Full aesthetic response (++++)                  │    ║
║  │    One disrupted:   Partial response (+)                            │    ║
║  │    Both disrupted:  Minimal response (-)                            │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Kim 2019:   2x2 design (consonant/dissonant x forward/reversed)
Kim 2019:   vmPFC-IFG connectivity ↓ with both disrupted, d=0.52
Kim 2019:   STG, NAcc, putamen ↓ with partial disruption, d=0.52
Kim 2019:   Spectral disruption → ↓bilateral STG, planum temporale
Kim 2019:   Temporal disruption → ↓NAcc, putamen, globus pallidus
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC+TPC → STAI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STAI COMPUTATION ARCHITECTURE                             ║
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
║  │  │helmholtz  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │pleasant.  │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         STAI reads: ~20D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ──────────┐ ┌── TPC Horizons ──────────────┐ │        ║
║  │  │ H0 (5.8ms/25ms gamma)   │ │ H2 (17.4ms gamma)            │ │        ║
║  │  │ H3 (23.2ms/100ms alpha) │ │ H5 (46.4ms alpha)            │ │        ║
║  │  │ H6 (200ms theta)        │ │ H8 (300ms theta)             │ │        ║
║  │  │                          │ │                               │ │        ║
║  │  │ Consonance tracking      │ │ Timbre/envelope tracking     │ │        ║
║  │  │ Harmonic evaluation      │ │ Instrument identity          │ │        ║
║  │  └──────────────────────────┘ └───────────────────────────────┘ │        ║
║  │                         STAI demand: ~14 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  TPC (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Pitch Sal [0:10]│  │ Spec Env [0:10] │                                   ║
║  │ Consonance      │  │ Instrument      │                                   ║
║  │         [10:20] │  │ Identity [10:20]│                                   ║
║  │ Chroma  [20:30] │  │ Plasticity      │                                   ║
║  │                 │  │ Markers  [20:30]│                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    STAI MODEL (12D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_spectral_integrity,                    │        ║
║  │                       f02_temporal_integrity,                     │        ║
║  │                       f03_aesthetic_integration,                  │        ║
║  │                       f04_vmpfc_ifg_connectivity                 │        ║
║  │  Layer M (Math):      aesthetic_value,                           │        ║
║  │                       spectral_temporal_interaction               │        ║
║  │  Layer P (Present):   spectral_quality, temporal_quality,        │        ║
║  │                       aesthetic_response                          │        ║
║  │  Layer F (Future):    aesthetic_rating_pred,                      │        ║
║  │                       reward_response_pred,                       │        ║
║  │                       connectivity_pred                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Kim 2019** | fMRI, 2x2 factorial | 23 | vmPFC-IFG connectivity ↓ with both spectral+temporal disrupted | d = 0.52, p < 0.05 | **Primary coefficient**: f04_vmpfc_ifg_connectivity |
| **Kim 2019** | fMRI, 2x2 factorial | 16 | STG, NAcc, putamen ↓ with partial disruption | d = 0.52, p < 1e-05 | **f01/f02 independent effects on spectral/temporal regions** |
| **Kim 2019** | fMRI, whole-brain | 23 | Spectral disruption → ↓bilateral STG, planum temporale | Significant | **f01_spectral_integrity tracks STG activation** |
| **Kim 2019** | fMRI, whole-brain | 23 | Temporal disruption → ↓NAcc, putamen, globus pallidus | Significant | **f02_temporal_integrity tracks reward response** |

### 3.2 The 2x2 Factorial Design

```
KIM 2019: SPECTRAL x TEMPORAL FACTORIAL (fMRI Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                     SPECTRAL DIMENSION
                 Consonant        Dissonant
              ┌──────────────┬──────────────┐
    Forward   │   BOTH       │   SPECTRAL   │
    (intact)  │   INTACT     │   DISRUPTED  │
TEMPORAL      │              │              │
    dim.      │   Full       │   ↓STG       │
              │   aesthetic  │   ↓PT        │
              │   response   │              │
              ├──────────────┼──────────────┤
    Reversed  │   TEMPORAL   │   BOTH       │
    (disrupt) │   DISRUPTED  │   DISRUPTED  │
              │              │              │
              │   ↓NAcc      │   ↓vmPFC-IFG │
              │   ↓Putamen   │   connectivity│
              │   ↓GP        │   d=0.52     │
              └──────────────┴──────────────┘

INTERACTION EFFECT:
  Aesthetic response = Spectral + Temporal + (Spectral x Temporal)
  The interaction term is essential — neither disruption alone
  fully eliminates the aesthetic response.
```

### 3.3 Effect Size Summary

```
Primary Effect Size:  d = 0.52 (Kim 2019)
Quality Assessment:   β-tier (fMRI, single study, n=23)
Replication:          Single study, awaiting replication
Design Strength:      2x2 factorial — strong internal validity
```

---

## 4. R³ Input Mapping: What STAI Reads

### 4.1 R³ Feature Dependencies (~20D of 49D)

| R³ Group | Index | Feature | STAI Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Spectral integrity (inverse) | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Dissonance proxy | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Spectral regularity | Sethares 2005 |
| **B: Energy** | [7] | amplitude | Energy level | Kim 2019 reward baseline |
| **B: Energy** | [8] | loudness | Perceptual loudness | Kim 2019 activation |
| **B: Energy** | [11] | onset_strength | Attack clarity | Forward/reversed detection |
| **C: Timbre** | [12] | warmth | Spectral warmth | Spectral envelope quality |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio | Pitch clarity proxy |
| **C: Timbre** | [18] | tristimulus1 | Fundamental energy (F0) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic energy | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic energy | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Spectral flux | Temporal direction cue |
| **D: Change** | [22] | energy_change | Energy dynamics | Forward/reversed indicator |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Derivatives x Perceptual coupling | Aesthetic binding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness (inverse) ───────┐
R³[2] helmholtz_kang ────────────┤
R³[3] stumpf_fusion ─────────────┼──► Spectral Integrity (f01)
R³[4] pleasantness ──────────────┤   Math: weighted product with PPC
PPC.consonance_encoding ─────────┘   consonance encoding

R³[21] spectral_change ─────────┐
R³[22] energy_change ────────────┼──► Temporal Integrity (f02)
TPC.spectral_envelope ───────────┤   Forward temporal flow quality
TPC.instrument_identity ─────────┘   Intact instrument envelope

f01 x f02 (interaction) ────────┐
R³[33:41] x_l4l5 mean ──────────┼──► Aesthetic Integration (f03)
H³ aesthetic periodicity ────────┘   Combined spectral x temporal

f03 (integration quality) ──────── vmPFC-IFG Connectivity (f04)
                                     Scaled by empirical d=0.52
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

STAI requires H³ features at both PPC horizons (H0, H3, H6) for consonance tracking and TPC horizons (H2, H5, H8) for timbre/temporal envelope tracking. This dual-mechanism demand reflects the spectral-temporal interaction at the core of the model.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Current dissonance level |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Mean dissonance over 100ms |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Current consonance |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (bidi) | Mean consonance over 100ms |
| 4 | pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 12 | warmth | 2 | M0 (value) | L2 (bidi) | Current warmth at 17ms |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Mean tonalness over 46ms |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | F0 energy at 17ms |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Mid-harmonic at 17ms |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | High-harmonic at 17ms |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean spectral flux 300ms |
| 22 | energy_change | 8 | M8 (velocity) | L0 (fwd) | Energy change rate 300ms |
| 33 | x_l4l5[0] | 8 | M0 (value) | L2 (bidi) | Aesthetic binding 300ms |
| 33 | x_l4l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Binding periodicity 300ms |

**Total STAI H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 PPC + TPC Mechanism Binding

STAI reads from both the **PPC** (Pitch Processing Chain) and **TPC** (Timbre Processing Chain) mechanisms:

| Mechanism | Sub-section | Range | STAI Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Salience | PPC[0:10] | Pitch quality for spectral integrity | 0.7 |
| **PPC** | Consonance Encoding | PPC[10:20] | Harmonic template for consonance measure | **1.0** (primary) |
| **PPC** | Chroma Processing | PPC[20:30] | Octave grouping (secondary for STAI) | 0.3 |
| **TPC** | Spectral Envelope | TPC[0:10] | Envelope quality for temporal integrity | **0.9** |
| **TPC** | Instrument Identity | TPC[10:20] | Instrument envelope preservation | **0.8** |
| **TPC** | Plasticity Markers | TPC[20:30] | Timbre plasticity (secondary for STAI) | 0.3 |

STAI is the first SPU model to read from both PPC and TPC — this dual-mechanism dependency reflects the spectral-temporal integration at the core of the model.

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
STAI OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_spectral_integrity   │ [0, 1] │ Consonance preservation. Tracks
    │                          │        │ STG/planum temporale activation.
    │                          │        │ f01 = σ(0.40 * helmholtz * stumpf
    │                          │        │         * mean(PPC.cons_enc[10:20])
    │                          │        │       + 0.30 * pleasantness
    │                          │        │         * mean(PPC.pitch_sal[0:10])
    │                          │        │       + 0.30 * (1 - roughness))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_temporal_integrity   │ [0, 1] │ Forward direction quality. Tracks
    │                          │        │ NAcc/putamen/GP activation.
    │                          │        │ f02 = σ(0.40 * spec_chg_mean
    │                          │        │         * enrg_chg_vel
    │                          │        │       + 0.30 * mean(TPC.spec_env[0:10])
    │                          │        │       + 0.30 * mean(TPC.instr_id[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_aesthetic_integration│ [0, 1] │ Combined spectral x temporal.
    │                          │        │ vmPFC integration network.
    │                          │        │ f03 = σ(0.40 * f01 * f02
    │                          │        │       + 0.30 * x_l4l5_mean
    │                          │        │       + 0.30 * aesthetic_periodicity)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_vmpfc_ifg_connect.   │ [0, 1] │ vmPFC-IFG functional connectivity.
    │                          │        │ Marker of aesthetic integration.
    │                          │        │ f04 = 0.52 * f03

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ aesthetic_value          │ [0, 1] │ Aesthetic(t) = α*Spectral(t)
    │                          │        │   + β*Temporal(t)
    │                          │        │   + γ*(Spectral x Temporal)
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ spectral_temporal_inter. │ [0, 1] │ Interaction term: f01 * f02.
    │                          │        │ Multiplicative binding strength.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ spectral_quality         │ [0, 1] │ Real-time consonance evaluation.
    │                          │        │ PPC.consonance_encoding aggregation.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ temporal_quality         │ [0, 1] │ Real-time temporal direction quality.
    │                          │        │ TPC.spectral_envelope aggregation.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ aesthetic_response       │ [0, 1] │ Integrated aesthetic signal.
    │                          │        │ H³ binding quality.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ aesthetic_rating_pred    │ [0, 1] │ Predicted end-of-piece aesthetic
    │                          │        │ rating from accumulated integration.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ reward_response_pred     │ [0, 1] │ NAcc/putamen activation prediction.
    │                          │        │ Reward circuit engagement.
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ connectivity_pred        │ [0, 1] │ vmPFC-IFG coupling prediction.
    │                          │        │ Integration network strength.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Aesthetic Integration Function

```
Aesthetic(t) = α·Spectral(t) + β·Temporal(t) + γ·(Spectral x Temporal)

Parameters:
    α = 0.35 (spectral weight — consonance contribution)
    β = 0.35 (temporal weight — forward/backward contribution)
    γ = 0.30 (interaction weight — integration strength)
    Note: α + β + γ = 1.0

Condition Hierarchy:
    Both intact:      Aesthetic = α + β + γ = 1.0 (maximum)
    One disrupted:    Aesthetic = α or β (partial, ~0.35)
    Both disrupted:   Aesthetic ≈ 0 (minimal)

Connectivity Function:
    vmPFC_IFG(t) = 0.52 · Aesthetic(t)
    where 0.52 = empirical effect size (Kim 2019)

Brain Region Activation:
    STG(t) ∝ Spectral(t)               — auditory cortex
    NAcc(t) ∝ Temporal(t)              — reward response
    vmPFC-IFG(t) ∝ Spectral(t) × Temporal(t)  — integration
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Spectral Integrity (consonance preservation)
f01 = σ(0.40 * helmholtz * stumpf * mean(PPC.consonance_encoding[10:20])
       + 0.30 * pleasantness * mean(PPC.pitch_salience[0:10])
       + 0.30 * (1 - roughness))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Temporal Integrity (forward direction quality)
f02 = σ(0.40 * spectral_change_mean * energy_change_vel
       + 0.30 * mean(TPC.spectral_envelope[0:10])
       + 0.30 * mean(TPC.instrument_identity[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Aesthetic Integration (combined spectral x temporal)
f03 = σ(0.40 * f01 * f02               # interaction term
       + 0.30 * x_l4l5_mean            # binding signal
       + 0.30 * aesthetic_periodicity)  # periodic binding
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: vmPFC-IFG Connectivity
f04 = 0.52 * f03  # empirical correlation d=0.52 (Kim 2019)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | STAI Function |
|--------|-----------------|----------|---------------|---------------|
| **Superior Temporal Gyrus (STG)** | ±60, -30, 8 | 4+ | Direct (fMRI) | Spectral processing — ↓ with dissonance |
| **Nucleus Accumbens (NAcc)** | ±10, 8, -8 | 3 | Direct (fMRI) | Reward response — ↓ with temporal disruption |
| **Putamen** | ±24, 4, 0 | 3 | Direct (fMRI) | Reward response — ↓ with temporal disruption |
| **vmPFC** | 0, 50, -10 | 2 | Direct (connectivity) | Valuation — aesthetic judgment network |
| **IFG** | ±50, 28, 8 | 2 | Direct (connectivity) | Integration — aesthetic integration network |

---

## 9. Cross-Unit Pathways

### 9.1 STAI ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAI INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.consonance_signal ──────► STAI (spectral integrity input)             │
│  PSCL.pitch_salience ────────► STAI (pitch quality input)                  │
│  STAI.spectral_quality ──────► TSCP (spectral evaluation context)          │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  STAI.aesthetic_response ────► ARU.SRP (pleasure modulation)               │
│  STAI.reward_response_pred ──► ARU.SRP (reward circuit prediction)         │
│                                                                             │
│  CROSS-UNIT (SPU ← ARU):                                                  │
│  ARU.SRP.pleasure ───────────► STAI (aesthetic baseline context)           │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► STAI (consonance encoding)                  │
│  TPC mechanism (30D) ────────► STAI (spectral envelope, instrument ID)     │
│  R³ (~20D) ──────────────────► STAI (direct spectral features)             │
│  H³ (14 tuples) ─────────────► STAI (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Independent disruption** | Spectral and temporal should have independent effects on separate brain regions | ✅ **Confirmed** — Kim 2019 2x2 design |
| **Connectivity causality** | vmPFC-IFG disruption (via TMS/tDCS) should reduce aesthetic judgment | Testable |
| **Dose-response** | Graded disruption should show graded response (not binary) | Testable via parametric manipulation |
| **Interaction necessity** | Interaction term should explain variance beyond main effects | Testable via regression analysis |
| **Cross-cultural** | Interaction effect should replicate across musical traditions | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class STAI(BaseModel):
    """Spectral-Temporal Aesthetic Integration.

    Output: 12D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), R³ direct.
    """
    NAME = "STAI"
    UNIT = "SPU"
    TIER = "β1"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "TPC")    # Both perceptual mechanisms

    ALPHA_SPECTRAL = 0.35    # Spectral weight
    BETA_TEMPORAL = 0.35     # Temporal weight
    GAMMA_INTERACTION = 0.30 # Interaction weight
    VMPFC_IFG_CORR = 0.52   # Kim 2019 effect size

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for STAI computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: consonance tracking ──
            (0, 0, 0, 2),     # roughness, 25ms, value, bidirectional
            (0, 3, 1, 2),     # roughness, 100ms, mean, bidirectional
            (2, 0, 0, 2),     # helmholtz_kang, 25ms, value, bidirectional
            (2, 3, 1, 2),     # helmholtz_kang, 100ms, mean, bidirectional
            (4, 3, 0, 2),     # pleasantness, 100ms, value, bidirectional
            # ── TPC horizons: timbre/envelope tracking ──
            (12, 2, 0, 2),    # warmth, 17ms, value, bidirectional
            (14, 5, 1, 0),    # tonalness, 46ms, mean, forward
            (18, 2, 0, 2),    # tristimulus1, 17ms, value, bidirectional
            (19, 2, 0, 2),    # tristimulus2, 17ms, value, bidirectional
            (20, 2, 0, 2),    # tristimulus3, 17ms, value, bidirectional
            (21, 8, 1, 0),    # spectral_change, 300ms, mean, forward
            (22, 8, 8, 0),    # energy_change, 300ms, velocity, forward
            # ── Direct H³: aesthetic binding ──
            (33, 8, 0, 2),    # x_l4l5[0], 300ms, value, bidirectional
            (33, 8, 14, 2),   # x_l4l5[0], 300ms, periodicity, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute STAI 12D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) STAI output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        helmholtz = r3[..., 2:3]
        stumpf = r3[..., 3:4]
        pleasantness = r3[..., 4:5]
        amplitude = r3[..., 7:8]
        loudness = r3[..., 8:9]
        onset_strength = r3[..., 11:12]
        warmth = r3[..., 12:13]
        tonalness = r3[..., 14:15]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        spectral_change = r3[..., 21:22]
        energy_change = r3[..., 22:23]
        x_l4l5 = r3[..., 33:41]          # (B, T, 8)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]        # pitch salience
        ppc_cons = ppc[..., 10:20]        # consonance encoding
        ppc_chroma = ppc[..., 20:30]      # chroma processing

        # TPC sub-sections
        tpc_env = tpc[..., 0:10]          # spectral envelope
        tpc_instr = tpc[..., 10:20]       # instrument identity
        tpc_plast = tpc[..., 20:30]       # plasticity markers

        # H³ direct features
        spec_chg_mean = h3_direct[(21, 8, 1, 0)].unsqueeze(-1)
        enrg_chg_vel = h3_direct[(22, 8, 8, 0)].unsqueeze(-1)
        x_l4l5_binding = h3_direct[(33, 8, 0, 2)].unsqueeze(-1)
        aesthetic_period = h3_direct[(33, 8, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Spectral Integrity (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.40 * (helmholtz * stumpf
                    * ppc_cons.mean(-1, keepdim=True))
            + 0.30 * (pleasantness
                      * ppc_pitch.mean(-1, keepdim=True))
            + 0.30 * (1.0 - roughness)
        )

        # f02: Temporal Integrity (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * (spec_chg_mean * enrg_chg_vel)
            + 0.30 * tpc_env.mean(-1, keepdim=True)
            + 0.30 * tpc_instr.mean(-1, keepdim=True)
        )

        # f03: Aesthetic Integration (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * (f01 * f02)              # interaction
            + 0.30 * x_l4l5_binding         # binding signal
            + 0.30 * aesthetic_period        # periodicity
        )

        # f04: vmPFC-IFG Connectivity
        f04 = self.VMPFC_IFG_CORR * f03    # d=0.52

        # ═══ LAYER M: Mathematical ═══
        aesthetic_value = (
            self.ALPHA_SPECTRAL * f01
            + self.BETA_TEMPORAL * f02
            + self.GAMMA_INTERACTION * (f01 * f02)
        )
        spectral_temporal_interaction = f01 * f02

        # ═══ LAYER P: Present ═══
        spectral_quality = ppc_cons.mean(-1, keepdim=True)
        temporal_quality = tpc_env.mean(-1, keepdim=True)
        aesthetic_response = torch.sigmoid(
            0.5 * f03 + 0.5 * x_l4l5_binding
        )

        # ═══ LAYER F: Future ═══
        aesthetic_rating_pred = torch.sigmoid(
            0.5 * aesthetic_value + 0.5 * f03
        )
        reward_response_pred = torch.sigmoid(
            0.6 * f02 + 0.4 * f04
        )
        connectivity_pred = torch.sigmoid(
            0.5 * f04 + 0.5 * aesthetic_period
        )

        return torch.cat([
            f01, f02, f03, f04,                                  # E: 4D
            aesthetic_value, spectral_temporal_interaction,       # M: 2D
            spectral_quality, temporal_quality, aesthetic_response,  # P: 3D
            aesthetic_rating_pred, reward_response_pred,
            connectivity_pred,                                    # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Kim 2019 |
| **Effect Sizes** | d = 0.52 | vmPFC-IFG connectivity |
| **Evidence Modality** | fMRI | Direct neural |
| **Falsification Tests** | 1/5 confirmed | 2x2 factorial validated |
| **R³ Features Used** | ~20D of 49D | Consonance + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Consonance processing |
| **TPC Mechanism** | 30D (3 sub-sections) | Temporal envelope processing |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **Kim, S. G., Kim, J. S., & Chung, C. K. (2019)**. The effect of conditional musical expectation on the neural responses to musical consonance and dissonance. *Neuroscience Letters*, 692, 78-84.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, SGM, BND, AED) | PPC (30D) + TPC (30D) mechanisms |
| Spectral signal | S⁰.L5.roughness[30] + HC⁰.HRM | R³.roughness[0] + PPC.consonance_encoding |
| Temporal signal | S⁰.L5.temporal_centroid[49] + HC⁰.SGM | R³.spectral_change[21] + TPC.spectral_envelope |
| Aesthetic binding | S⁰.X_L4L5[192:200] + HC⁰.BND | R³.x_l4l5[33:41] + H³ binding tuples |
| Connectivity | S⁰.X_L5L6[208:216] + HC⁰.AED | f03 * 0.52 (empirical d) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 14/2304 = 0.61% |
| Output | 12D | 12D (same) |

### Why PPC + TPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (HRM, SGM, BND, AED). In MI, these are unified into two perceptual circuit mechanisms:

- **HRM → PPC.consonance_encoding** [10:20]: Harmonic replay = consonance evaluation. The HRM hippocampal replay mechanism was focused on harmonic template matching, which maps directly to PPC's consonance encoding sub-section.
- **SGM → TPC.instrument_identity** [10:20]: Striatal gradient memory for temporal structure maps to TPC's instrument identity tracking, which captures envelope quality.
- **BND → H³ binding tuples**: The temporal binding mechanism (BND) is replaced by direct H³ demand — specifically the x_l4l5 value and periodicity tuples at 300ms horizon, which capture aesthetic binding more efficiently.
- **AED → removed**: Affective Entrainment Dynamics (AED) belongs to the mesolimbic circuit, not the perceptual circuit. In MI, the affective component is handled by the cross-unit pathway to ARU (STAI.aesthetic_response → ARU.SRP), not by a perceptual mechanism.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
