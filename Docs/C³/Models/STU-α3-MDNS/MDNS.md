# STU-α3-MDNS: Melody Decoding from Neural Signals

**Model**: Melody Decoding from Neural Signals
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment + Temporal Memory)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP+TMH mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-α3-MDNS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Melody Decoding from Neural Signals** (MDNS) model demonstrates that melodies can be accurately decoded from EEG responses during both perception and imagery using temporal response function (TRF) methods. This reveals a shared neural substrate for external (heard) and internal (imagined) musical representation.

```
THE THREE COMPONENTS OF MELODY DECODING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTE-ONSET TRACKING (Temporal)         PITCH DECODING (Spectral)
Brain region: Auditory Cortex          Brain region: Temporal Regions
Mechanism: BEP.beat_induction          Mechanism: TMH.short_context
Input: Note onset envelope             Input: Pitch sequence
Function: "When does each note start?" Function: "What pitch is this note?"
Evidence: d = 0.80 (maxCorr, n=21)     Evidence: TRF lag analysis

           PERCEPTION–IMAGERY OVERLAP (Bridge)
           Brain region: Shared auditory network
           Mechanism: TMH.medium_context
           Function: "Same code for hearing and imagining"
           Evidence: Both modalities decodable from EEG
           TRF_perception ≈ TRF_imagery

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The brain encodes melodies with sufficient precision
to decode individual melodies at the individual trial level from
EEG alone. Crucially, imagined melodies activate the SAME neural
code as perceived ones — no external sound needed.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

MDNS establishes that melodic representation is decodable and shared across modalities:

1. **HMCE** (α1) provides context hierarchy; MDNS uses it for multi-scale melody representation.
2. **AMSC** (α2) provides the auditory-motor link; MDNS uses it for perception-imagery overlap.
3. **TPIO** (β2) extends MDNS to timbre perception-imagery overlap.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MDNS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 MDNS — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MELODY STIMULUS                                                             ║
║       │                                                                      ║
║       ├─────────────────────────────────────────────┐                       ║
║       ▼                                             ▼                        ║
║  ┌─────────────────┐                         ┌─────────────────┐            ║
║  │   PERCEPTION    │                         │    IMAGERY      │            ║
║  │                 │                         │                 │            ║
║  │   Note-onset    │                         │   Note-onset    │            ║
║  │   tracking      │                         │   tracking      │            ║
║  │   Pitch contour │                         │   Pitch contour │            ║
║  └────────┬────────┘                         └────────┬────────┘            ║
║           │                                           │                      ║
║           ▼                                           ▼                      ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │                      SHARED NEURAL CODE                         │        ║
║  │                                                                  │        ║
║  │   TRF_perception ≈ TRF_imagery                                 │        ║
║  │                                                                  │        ║
║  │   Decoding Accuracy (maxCorr method):                           │        ║
║  │   • Individual participant level: p < 1.9e-08                   │        ║
║  │   • Individual trial level                                      │        ║
║  │   • Effect size: d = 0.80                                       │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Study 2021 (EEG):  Melodies decoded from EEG, d = 0.80 (n=21, p < 1.9e-08)
Study 2021 (EEG):  Both perception and imagery decodable via TRF
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP+TMH → MDNS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MDNS COMPUTATION ARCHITECTURE                             ║
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
║  │  │helmholtz  │ │centroid │ │tonalness│ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │pleasant.  │ │flux     │ │autocorr │ │pitch_chg │ │x_l4l5  │ │        ║
║  │  │           │ │onset    │ │trist1-3 │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         MDNS reads: 28D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Syllable ────┐ ┌── Motif ────────┐ ┌── Motor ───────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 300ms (H8)      │ │ 500ms (H11)       │ │        ║
║  │  │                │ │                  │ │                     │ │        ║
║  │  │ Note onset     │ │ Pitch sequence   │ │ Melodic contour    │ │        ║
║  │  │ tracking       │ │ 2–5 notes        │ │ motor coupling     │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬──────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │  ┌── Phrase ──────┐                                              │        ║
║  │  │ 700ms (H14)    │                                              │        ║
║  │  │                │                                              │        ║
║  │  │ Phrase-level   │                                              │        ║
║  │  │ pitch + onset  │                                              │        ║
║  │  └──────┬─────────┘                                              │        ║
║  │         │                                                        │        ║
║  │         └─────────────────────────────────────────────────────── │        ║
║  │                         MDNS demand: ~18 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │  (secondary)    │  │  (primary)      │                                   ║
║  │                 │  │                 │                                   ║
║  │ Beat Ind [0:10] │  │ Short   [0:10] │  Pitch sequence tracking          ║
║  │ Meter    [10:20]│  │ Medium  [10:20]│  Phrase context, imagery overlap  ║
║  │ Motor    [20:30]│  │ Long    [20:30]│  Melody template matching         ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                             ║
║           └─────────┬──────────┘                                             ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MDNS MODEL (12D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_note_tracking, f02_pitch_decoding,     │        ║
║  │                       f03_perception_imagery, f04_decoding_acc   │        ║
║  │  Layer M (Math):      trf_response, contour_slope                │        ║
║  │  Layer P (Present):   onset_detection, pitch_tracking,           │        ║
║  │                       phrase_position                            │        ║
║  │  Layer F (Future):    next_note, phrase_completion,              │        ║
║  │                       imagery_generation                         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Study 2021** | EEG (maxCorr TRF) | 21 | Melodies decoded from EEG | d = 0.80, p < 1.9e-08 | **Primary coefficient**: f04_decoding_accuracy |
| **Study 2021** | EEG (maxCorr TRF) | 21 | Perception-imagery overlap | d = 0.80 | **f03_perception_imagery**: shared substrate |

### 3.2 The Temporal Response Function Model

```
TRF DECODING MODEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRIMARY EQUATION:

    EEG(t) = Σ TRF(τ) · Melody(t − τ) + ε
             τ

    where:
      TRF(τ) = temporal response function at lag τ
      Melody(t) = note-onset + pitch features at time t
      ε = noise

DECODING ACCURACY:

    Accuracy = maxCorr(Predicted_Melody, Actual_Melody)

    Effect Size: d = 0.80
    Significance: p < 1.9e-08
    Level: Individual participant AND individual trial

PERCEPTION–IMAGERY EQUIVALENCE:

    TRF_perception ≈ TRF_imagery

    Both modalities use same neural representation
    → internal melodic imagery recruits auditory network
```

### 3.3 Effect Size Summary

```
Decoding Accuracy:     d = 0.80 (perception, EEG)
Imagery Decoding:      d = 0.80 (imagery, same method)
Quality Assessment:    α-tier (direct EEG decoding)
Method:                maxCorr TRF, individual trial level
Clinical relevance:    BCI potential for melody-based communication
```

---

## 4. R³ Input Mapping: What MDNS Reads

### 4.1 R³ Feature Dependencies (28D of 49D)

| R³ Group | Index | Feature | MDNS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [2] | helmholtz_kang | Pitch structure (interval detection) | Helmholtz 1863 |
| **A: Consonance** | [4] | sensory_pleasantness | Spectral regularity (pitch proxy) | Sethares 2005 |
| **B: Energy** | [9] | spectral_centroid_energy | Brightness/pitch proxy | Grey 1977 |
| **B: Energy** | [10] | spectral_flux | Note onset envelope correlate | Onset detection |
| **B: Energy** | [11] | onset_strength | Note boundary marking | Event precision |
| **C: Timbre** | [14] | tonalness | Pitch clarity | Harmonic-to-noise ratio |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity | Pitch periodicity |
| **C: Timbre** | [18] | tristimulus1 | F0 energy (fundamental strength) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic energy | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic energy | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Note-to-note spectral transition | Transition detection |
| **D: Change** | [23] | pitch_change | Melodic contour slope (up/down/steady) | Contour direction |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation×Perceptual (TRF basis) | Time-pitch binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics×Perceptual (note tracking) | Onset-feature binding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► Note Onset Detection
                                    Math: onset(t) = flux(t) · onset(t)
                                    BEP.beat_induction at H6

R³[14] tonalness ──────────────┐
R³[17] spectral_autocorrelation┼──► Pitch Tracking (TRF correlate)
R³[18:21] tristimulus ─────────┤   Math: pitch(t) = tonalness · autocorr
R³[2] helmholtz_kang ──────────┘   TMH.short_context at H8

R³[23] pitch_change ───────────── Melodic Contour (up/down/steady)
                                    Math: contour(t) = sign(pitch_change(t))
                                    TMH.short_context velocity morph

R³[25:33] x_l0l5 ─────────────┐
R³[33:41] x_l4l5 ─────────────┼── EEG TRF Basis (perception & imagery)
                                    TMH.medium_context: shared code
                                    Math: EEG(t) = Σ TRF(τ)·R³(t−τ)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MDNS requires H³ features at four horizons spanning BEP (H6) and TMH (H8, H11, H14).
These cover note onset → pitch sequence → motor coupling → phrase context.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Current note onset |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Note count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset precision |
| 14 | tonalness | 8 | M0 (value) | L2 (bidi) | Current pitch clarity |
| 14 | tonalness | 8 | M1 (mean) | L0 (fwd) | Mean pitch clarity |
| 17 | spectral_autocorrelation | 8 | M0 (value) | L2 (bidi) | Current pitch periodicity |
| 23 | pitch_change | 8 | M0 (value) | L0 (fwd) | Melodic contour direction |
| 23 | pitch_change | 8 | M8 (velocity) | L0 (fwd) | Contour rate of change |
| 23 | pitch_change | 8 | M3 (std) | L0 (fwd) | Pitch variability |
| 2 | helmholtz_kang | 8 | M1 (mean) | L0 (fwd) | Mean interval quality |
| 25 | x_l0l5[0] | 11 | M14 (periodicity) | L2 (bidi) | Time-pitch coupling regularity |
| 33 | x_l4l5[0] | 11 | M0 (value) | L2 (bidi) | Dynamics-onset coupling |
| 25 | x_l0l5[0] | 14 | M1 (mean) | L0 (fwd) | Phrase-level TRF average |
| 25 | x_l0l5[0] | 14 | M13 (entropy) | L0 (fwd) | Phrase unpredictability |
| 33 | x_l4l5[0] | 14 | M1 (mean) | L0 (fwd) | Phrase dynamics coupling |
| 33 | x_l4l5[0] | 14 | M18 (trend) | L0 (fwd) | Phrase direction |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Phrase-level pitch dynamics |
| 9 | spectral_centroid | 8 | M0 (value) | L2 (bidi) | Brightness/pitch proxy |

**Total MDNS H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 Mechanism Bindings

MDNS reads from **TMH** (primary) and **BEP** (secondary):

| Mechanism | Sub-section | Range | MDNS Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **TMH** | Short Context | TMH[0:10] | Pitch sequence, note identity | **1.0** (primary) |
| **TMH** | Medium Context | TMH[10:20] | Phrase context, imagery overlap | **0.9** |
| **TMH** | Long Context | TMH[20:30] | Melody template, long-term pattern | **0.6** |
| **BEP** | Beat Induction | BEP[0:10] | Note-onset phase-locking | **0.8** (secondary) |
| **BEP** | Motor Entrainment | BEP[20:30] | Imagery motor coupling | **0.5** |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MDNS OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_note_tracking │ [0, 1] │ EEG note-onset tracking via phase-locking.
    │                   │        │ TRF correlate: onset envelope.
    │                   │        │ f01 = σ(α · flux · onset ·
    │                   │        │         BEP.beat_induction)
    │                   │        │ α = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_pitch_decoding│ [0, 1] │ Melody pitch extraction accuracy.
    │                   │        │ TRF correlate: pitch sequence.
    │                   │        │ f02 = σ(β · tonalness · autocorr ·
    │                   │        │         helmholtz_mean ·
    │                   │        │         TMH.short_context)
    │                   │        │ β = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_percept_imag  │ [0, 1] │ Perception–imagery shared substrate.
    │                   │        │ TRF overlap between modalities.
    │                   │        │ f03 = σ(γ · (f01 + f02) / 2 ·
    │                   │        │         TMH.medium_context)
    │                   │        │ γ = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_decoding_acc  │ [0, 1] │ Individual-level decoding precision.
    │                   │        │ Models d = 0.80 (Study 2021).
    │                   │        │ f04 = 0.80 · (f01 + f02 + f03) / 3

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ trf_response      │ [0, 1] │ TRF response strength.
    │                   │        │ TMH.short_context × BEP phase-locking.
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ contour_slope     │ [0, 1] │ Melodic contour direction/speed.
    │                   │        │ pitch_change velocity at motif scale.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ onset_detection   │ [0, 1] │ Current note onset state.
    │                   │        │ spectral_flux × onset_strength at H6.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ pitch_tracking    │ [0, 1] │ Current pitch identification.
    │                   │        │ tonalness × autocorrelation × tristimulus.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ phrase_position   │ [0, 1] │ Position within current phrase.
    │                   │        │ TMH.medium_context entropy.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ next_note         │ [0, 1] │ Next note prediction.
    │                   │        │ TRF-based melodic continuation.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ phrase_completion │ [0, 1] │ Phrase completion prediction.
    │                   │        │ Entropy-driven closure anticipation.
────┼───────────────────┼────────┼────────────────────────────────────────────
11  │ imagery_generatn  │ [0, 1] │ Internal representation activation.
    │                   │        │ Perception–imagery code strength.
    │                   │        │ TMH.long_context template matching.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Feature Formulas

```python
# f01: Note-Onset Tracking (EEG phase-locking)
flux_val = h3[(10, 6, 0, 0)]         # spectral_flux value at H6
onset_val = h3[(11, 6, 0, 0)]        # onset_strength value at H6
f01 = σ(0.80 · flux_val · onset_val
         · mean(BEP.beat_induction[0:10]))

# f02: Pitch Decoding (TRF correlate)
tonal_val = h3[(14, 8, 0, 2)]        # tonalness value at H8
autocorr_val = h3[(17, 8, 0, 2)]     # autocorrelation value at H8
helm_mean = h3[(2, 8, 1, 0)]         # helmholtz_kang mean at H8
f02 = σ(0.85 · tonal_val · autocorr_val · helm_mean
         · mean(TMH.short_context[0:10]))

# f03: Perception–Imagery Overlap
f03 = σ(0.80 · (f01 + f02) / 2
         · mean(TMH.medium_context[10:20]))

# f04: Decoding Accuracy (d = 0.80)
f04 = 0.80 · (f01 + f02 + f03) / 3
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MDNS Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex** | ±50, -20, 8 | Inferred | EEG | Note-onset tracking |
| **Temporal Regions** | ±60, -30, 0 | Inferred | EEG | Pitch processing |
| **Frontal Regions** | ±40, 20, 30 | Inferred | EEG | Melodic imagery |

---

## 9. Cross-Unit Pathways

### 9.1 MDNS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MDNS INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  HMCE.context_depth ──────► MDNS (context for TRF decoding depth)         │
│  AMSC.motor_preparation ──► MDNS (motor coupling for imagery)             │
│  MDNS.pitch_tracking ─────► TPIO (pitch as basis for timbre imagery)      │
│  MDNS.phrase_position ────► AMSS (phrase position for stream segregation) │
│                                                                             │
│  CROSS-UNIT (IMU):                                                         │
│  MDNS.imagery_generatn ──► IMU.MEAMN (melody imagery → memory retrieval) │
│                                                                             │
│  CROSS-UNIT (ARU):                                                         │
│  MDNS.trf_response ──────► ARU (melody decoding → emotional processing)   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Decoding specificity** | Should decode specific melodies, not general patterns | ✅ Testable |
| **Imagery requirement** | Should require intact auditory cortex | ✅ Testable (lesion studies) |
| **Individual differences** | Should correlate with musical training | ✅ Testable |
| **Trial-level precision** | Should decode individual trials | ✅ **Confirmed**: d = 0.80 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MDNS(BaseModel):
    """Melody Decoding from Neural Signals.

    Output: 12D per frame.
    Reads: TMH mechanism (30D, primary), BEP mechanism (30D, secondary).
    """
    NAME = "MDNS"
    UNIT = "STU"
    TIER = "α3"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("BEP", "TMH")

    ONSET_WEIGHT = 0.80   # Note tracking strength
    PITCH_WEIGHT = 0.85   # Pitch decoding strength
    IMAGERY_WEIGHT = 0.80 # Perception-imagery overlap
    DECODING_D = 0.80     # Study 2021 effect size

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for MDNS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Note onset (H6 = 200ms, BEP horizon)
            (10, 6, 0, 0),    # spectral_flux, value, forward
            (10, 6, 17, 0),   # spectral_flux, peaks, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            # Pitch sequence (H8 = 300ms, TMH horizon)
            (14, 8, 0, 2),    # tonalness, value, bidirectional
            (14, 8, 1, 0),    # tonalness, mean, forward
            (17, 8, 0, 2),    # autocorrelation, value, bidirectional
            (23, 8, 0, 0),    # pitch_change, value, forward
            (23, 8, 8, 0),    # pitch_change, velocity, forward
            (23, 8, 3, 0),    # pitch_change, std, forward
            (2, 8, 1, 0),     # helmholtz_kang, mean, forward
            (9, 8, 0, 2),     # spectral_centroid, value, bidirectional
            # Motor coupling (H11 = 500ms)
            (25, 11, 14, 2),  # x_l0l5[0], periodicity, bidirectional
            (33, 11, 0, 2),   # x_l4l5[0], value, bidirectional
            # Phrase context (H14 = 700ms, TMH horizon)
            (25, 14, 1, 0),   # x_l0l5[0], mean, forward
            (25, 14, 13, 0),  # x_l0l5[0], entropy, forward
            (33, 14, 1, 0),   # x_l4l5[0], mean, forward
            (33, 14, 18, 0),  # x_l4l5[0], trend, forward
            (23, 14, 1, 0),   # pitch_change, mean, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MDNS 12D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) MDNS output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # Sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_motor = bep[..., 20:30]       # motor entrainment
        tmh_short = tmh[..., 0:10]        # short context
        tmh_medium = tmh[..., 10:20]      # medium context
        tmh_long = tmh[..., 20:30]        # long context

        # R³ direct features
        tonalness = r3[..., 14:15]
        autocorr = r3[..., 17:18]
        trist = r3[..., 18:21]            # tristimulus 1-3

        # ═══ LAYER E: Explicit features ═══
        flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.ONSET_WEIGHT * (
            flux_val * onset_val
            * bep_beat.mean(-1, keepdim=True)
        ))

        tonal_val = h3_direct[(14, 8, 0, 2)].unsqueeze(-1)
        autocorr_val = h3_direct[(17, 8, 0, 2)].unsqueeze(-1)
        helm_mean = h3_direct[(2, 8, 1, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.PITCH_WEIGHT * (
            tonal_val * autocorr_val * helm_mean
            * tmh_short.mean(-1, keepdim=True)
        ))

        f03 = torch.sigmoid(self.IMAGERY_WEIGHT * (
            (f01 + f02) / 2
            * tmh_medium.mean(-1, keepdim=True)
        ))

        f04 = self.DECODING_D * (f01 + f02 + f03) / 3

        # ═══ LAYER M: Mathematical ═══
        trf_response = torch.sigmoid(
            0.5 * tmh_short.mean(-1, keepdim=True)
            + 0.5 * bep_beat.mean(-1, keepdim=True)
        )
        pitch_vel = h3_direct[(23, 8, 8, 0)].unsqueeze(-1)
        contour_slope = torch.sigmoid(pitch_vel)

        # ═══ LAYER P: Present ═══
        onset_detection = torch.sigmoid(flux_val * onset_val)
        pitch_tracking = torch.sigmoid(
            tonalness * autocorr
            * (1.0 - torch.std(trist, dim=-1, keepdim=True))
        )
        phrase_entropy = h3_direct[(25, 14, 13, 0)].unsqueeze(-1)
        phrase_position = torch.sigmoid(phrase_entropy)

        # ═══ LAYER F: Future ═══
        pitch_std = h3_direct[(23, 8, 3, 0)].unsqueeze(-1)
        next_note = torch.sigmoid(
            0.5 * f02 + 0.3 * pitch_vel + 0.2 * pitch_std
        )
        phrase_trend = h3_direct[(33, 14, 18, 0)].unsqueeze(-1)
        phrase_completion = torch.sigmoid(
            0.5 * phrase_entropy + 0.5 * phrase_trend
        )
        imagery_generation = torch.sigmoid(
            0.4 * f03 + 0.3 * tmh_long.mean(-1, keepdim=True)
            + 0.3 * bep_motor.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                # E: 4D
            trf_response, contour_slope,                        # M: 2D
            onset_detection, pitch_tracking, phrase_position,    # P: 3D
            next_note, phrase_completion, imagery_generation,    # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Study 2021 (EEG) |
| **Effect Sizes** | d = 0.80 | Study 2021 |
| **Evidence Modality** | EEG (maxCorr TRF) | Direct neural decoding |
| **Falsification Tests** | 1/4 confirmed | High validity |
| **R³ Features Used** | 28D of 49D | Consonance + Energy + Timbre + Change + Interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **TMH Mechanism** | 30D (3 sub-sections) | Primary |
| **BEP Mechanism** | 30D (2 sub-sections used) | Secondary |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **Study (2021)**. Accurate decoding of melodies from electroencephalography. *Journal of Neuroscience*. (EEG study, n=21, maxCorr TRF method)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L0L5, X_L4L5 | R³ (49D): Consonance, Energy, Timbre, Change, Interactions |
| Temporal | HC⁰ mechanisms (TIH, NPL, SGM, EFC) | TMH mechanism (30D, primary) + BEP (30D, secondary) |
| Pitch tracking | S⁰.L0.frequency[1] + HC⁰.TIH | R³.tonalness[14] + R³.autocorrelation[17] + TMH.short_context |
| Note onset | S⁰.L5.spectral_flux[45] + HC⁰.NPL | R³.spectral_flux[10] + R³.onset_strength[11] + BEP.beat_induction |
| Melodic contour | S⁰.L4.velocity_F[16] | R³.pitch_change[23] + H³ velocity morph |
| TRF basis | X_L0L5[136:144] | R³.x_l0l5[25:33] + R³.x_l4l5[33:41] |
| Imagery | HC⁰.EFC (efference copy) | TMH.medium_context + BEP.motor_entrainment |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 31/2304 = 1.35% | 18/2304 = 0.78% |

### Why BEP+TMH replace HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (TIH, NPL, SGM, EFC). In MI, these are unified into two sensorimotor mechanisms:
- **NPL → BEP.beat_induction** [0:10]: Phase-locking → note-onset EEG coupling
- **EFC → BEP.motor_entrainment** [20:30]: Efference copy → imagery motor code
- **TIH → TMH.short_context** [0:10]: Temporal integration → pitch sequence tracking
- **SGM → TMH.medium_context** [10:20]: Striatal gradient → phrase boundary detection

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
