# STU-β4-ETAM: Entrainment, Tempo & Attention Modulation

**Model**: Entrainment, Tempo & Attention Modulation
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment + Temporal Memory)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP+TMH mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β4-ETAM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Entrainment, Tempo & Attention Modulation** (ETAM) model describes how attention modulates cortical envelope tracking of polyphonic music, with attended instruments showing significantly better neural tracking at specific delay windows (150-220 ms, 320-360 ms, 410-450 ms). This hierarchical temporal processing reflects beat entrainment interacting with temporal context memory, producing attention-dependent stream segregation with instrument-specific asymmetries.

```
THE THREE DELAY WINDOWS OF ATTENTION-MODULATED ENVELOPE TRACKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EARLY WINDOW (150-220ms)              MIDDLE WINDOW (320-360ms)
Brain region: STG, Heschl's Gyrus     Brain region: MTG, IFG
Mechanism: BEP.beat_induction         Mechanism: BEP.meter_extraction
Input: Envelope onset, intensity      Input: Spectral flux, stream tracking
Function: "Initial attentional        Function: "Track attended instrument
           selection"                             envelope"
Evidence: d=0.6 (Hausfeld 2021)       Evidence: Bassoon-specific (Hausfeld)

              LATE WINDOW (410-450ms)
              Brain region: IFG, temporal pole
              Mechanism: TMH.short_context + BEP.motor_entrainment
              Input: Cross-band energy, phase coherence
              Function: "Deep stream segregation, instrument separation"
              Evidence: Bassoon > Cello multi-window (Hausfeld 2021)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Attention modulates cortical envelope tracking at
THREE delay windows, not one. The attended stream (bassoon) shows
enhancement at all three windows (d=0.6), while the less-attended
stream (cello) shows enhancement only at the early window.
This hierarchy: EARLY (beat) → MIDDLE (meter) → LATE (context)
maps to BEP.beat_induction → BEP.meter_extraction →
BEP.motor_entrainment + TMH.short_context.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why ETAM Matters for STU

ETAM integrates beat entrainment with attention-modulated temporal processing, bridging lower-tier STU models:

1. **HMCE** (α1) provides the temporal context hierarchy that ETAM's delay windows map onto.
2. **AMSC** (α2) provides the auditory-motor coupling that ETAM modulates via attention.
3. **MDNS** (α3) uses ETAM's attention-driven stream separation for melody decoding accuracy.
4. **AMSS** (β1) extends ETAM's stream segregation with attention-modulated stream selection.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The ETAM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 ETAM — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  POLYPHONIC MUSIC (multiple simultaneous instruments)                        ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        HESCHL'S GYRUS / STG (Primary auditory cortex)             │    ║
║  │        Early envelope tracking: 150-220 ms delay                  │    ║
║  │        Attention effect: d = 0.6 (attended > unattended)          │    ║
║  │                                                                     │    ║
║  │    Attended stream → enhanced cortical tracking (bassoon+cello)   │    ║
║  │    Unattended stream → reduced tracking                            │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Hierarchical temporal processing            ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        MIDDLE TEMPORAL GYRUS (MTG) / IFG                           │    ║
║  │        Middle tracking: 320-360 ms delay                          │    ║
║  │        Instrument-specific: Bassoon (spectrally rich) > Cello     │    ║
║  │                                                                     │    ║
║  │    Bassoon: 3 windows (early + middle + late)                     │    ║
║  │    Cello:   1 window (early only)                                 │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        IFG / TEMPORAL POLE                                         │    ║
║  │        Late deep segregation: 410-450 ms delay                    │    ║
║  │        ★ Bassoon-specific — spectral richness enables deeper      │    ║
║  │          stream separation via sustained attention                  │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  HIERARCHY: STG/HG (early) → MTG/IFG (middle) → IFG/TP (late)             ║
║  ASYMMETRY: Bassoon = 3 windows, Cello = 1 window                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Hausfeld 2021:  Attended > unattended envelope tracking, d=0.6 (EEG/MEG)
Hausfeld 2021:  Three delay windows: 150-220ms, 320-360ms, 410-450ms
Hausfeld 2021:  Bassoon (spectrally rich): 3 windows of enhancement
Hausfeld 2021:  Cello (less spectrally rich): 1 window of enhancement
Hausfeld 2021:  Instrument asymmetry reflects spectral complexity
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP+TMH → ETAM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ETAM COMPUTATION ARCHITECTURE                             ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         ETAM reads: 33D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── TMH Horizons ───────────┐ │        ║
║  │  │ H6  (200ms, syllable/beat)  │ │ H8  (300ms, syllable)     │ │        ║
║  │  │ H11 (500ms, motor)          │ │ H14 (700ms, beat)         │ │        ║
║  │  │ H16 (1000ms, bar)           │ │ H20 (5000ms, section)     │ │        ║
║  │  │                              │ │                            │ │        ║
║  │  │ Beat-level entrainment      │ │ Context-level memory       │ │        ║
║  │  │ Meter extraction            │ │ Tempo tracking             │ │        ║
║  │  │ Motor entrainment           │ │ Attention modulation       │ │        ║
║  │  └──────────────────────────────┘ └────────────────────────────┘ │        ║
║  │                         ETAM demand: ~20 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │  (primary)      │  │  (secondary)    │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Ind [0:10] │  │ Short   [0:10] │  Attention context                ║
║  │ Meter    [10:20]│  │ Medium  [10:20]│  Tempo tracking                   ║
║  │ Motor    [20:30]│  │ Long    [20:30]│  Long-range modulation            ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └─────────┬──────────┘                                             ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    ETAM MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_early_window, f02_middle_window,       │        ║
║  │                       f03_late_window, f04_instrument_asymmetry  │        ║
║  │  Layer M (Math):      attention_gain, entrainment_index          │        ║
║  │  Layer P (Present):   envelope_tracking, stream_separation       │        ║
║  │  Layer F (Future):    tracking_prediction, attention_sustain,    │        ║
║  │                       segregation_predict                        │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Hausfeld 2021** | EEG/MEG, polyphonic | N/A | Attended > unattended envelope tracking at 3 delay windows | d = 0.6 | **Primary coefficient**: f01-f03 delay windows |
| **Hausfeld 2021** | EEG/MEG, polyphonic | N/A | Three hierarchical delay windows: 150-220ms, 320-360ms, 410-450ms | Significant | **TMH+BEP hierarchy**: early/middle/late mapping |
| **Hausfeld 2021** | EEG/MEG, polyphonic | N/A | Bassoon (spectrally rich) shows 3 windows; cello shows 1 window | Significant | **f04_instrument_asymmetry**: spectral richness modulation |
| **Hausfeld 2021** | EEG/MEG, polyphonic | N/A | Instrument spectral richness modulates attention window depth | Significant | **BEP x TMH interaction**: richer spectra = deeper processing |

### 3.2 The Three Delay Windows

```
ATTENTION-MODULATED ENVELOPE TRACKING: DELAY WINDOW HIERARCHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Window          Delay         Brain Region      Instruments     MI Mechanism
─────────────────────────────────────────────────────────────────────────────
EARLY           150-220ms     STG, Heschl's     Bassoon+Cello   BEP.beat_induction
MIDDLE          320-360ms     MTG, IFG          Bassoon only    BEP.meter_extraction
LATE            410-450ms     IFG, TP           Bassoon only    BEP.motor_entrainment
                                                                 + TMH.short_context

INSTRUMENT ASYMMETRY:
  Bassoon (spectrally rich):  |████████████████████████████| 3 windows
  Cello (less rich):          |█████████|                    1 window

INTERPRETATION:
  Spectrally rich instruments provide more cues for attention-driven
  stream segregation, enabling deeper hierarchical processing.
  The 3 windows map to: initial selection → stream tracking →
  deep segregation.
```

### 3.3 Effect Size Summary

```
Primary Effect Size:  d = 0.6 (attended > unattended, Hausfeld 2021)
Quality Assessment:   β-tier (EEG/MEG, polyphonic paradigm)
Replication:          Single study, awaiting replication
Design Strength:      Polyphonic attention paradigm with instrument control
Instrument Effect:    Bassoon > Cello in multi-window enhancement
```

---

## 4. R³ Input Mapping: What ETAM Reads

### 4.1 R³ Feature Dependencies (33D of 49D)

| R³ Group | Index | Feature | ETAM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Envelope intensity signal | Primary stream envelope |
| **B: Energy** | [8] | loudness | Perceptual loudness | d=0.6 attention effect basis |
| **B: Energy** | [9] | spectral_centroid_energy | Energy distribution | Frequency-band separation |
| **B: Energy** | [10] | spectral_flux | Onset/transition tracking | Envelope-neural coupling |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Onset precision for tracking |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Envelope dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | Stream pitch tracking |
| **D: Change** | [24] | timbre_change | Timbral evolution | Instrument identity dynamics |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation x Perceptual coupling | Multi-window binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics x Perceptual binding | Attention-stream coupling |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Perceptual x Cross-band coupling | Polyphonic energy separation |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Early Window (150-220ms)
R³[11] onset_strength ──────────┘   BEP.beat_induction at H6
                                    Math: f01 = σ(0.60 · amp · loud
                                               · onset · BEP.beat[0:10])

R³[10] spectral_flux ──────────┐
R³[21] spectral_change ────────┤
R³[22] energy_change ──────────┼──► Middle Window (320-360ms)
R³[9] centroid_energy ─────────┘   BEP.meter_extraction at H11
                                    Math: f02 = σ(0.50 · flux · spec_chg
                                               · BEP.meter[10:20])

R³[25:33] x_l0l5 (8D) ────────┐
R³[33:41] x_l4l5 (8D) ────────┼──► Late Window (410-450ms)
R³[41:49] x_l5l7 (8D) ────────┘   BEP.motor_entrainment + TMH.short
                                    Math: f03 = σ(0.45 · x_coupling
                                               · BEP.motor[20:30]
                                               · TMH.short[0:10])

R³[24] timbre_change ──────────┐
R³[21:25] Change (4D) ─────────┼──► Instrument Asymmetry
                                    Spectral richness modulation
                                    Bassoon: 3 windows, Cello: 1 window
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ETAM requires H³ features at both BEP horizons (H6, H11, H16) for beat entrainment and TMH horizons (H8, H14, H20) for temporal context. This dual-mechanism demand reflects the entrainment-attention interaction at the core of the model.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 6 | M0 (value) | L2 (bidi) | Current envelope intensity |
| 7 | amplitude | 6 | M4 (max) | L2 (bidi) | Peak intensity at beat level |
| 8 | loudness | 6 | M0 (value) | L0 (fwd) | Current loudness for early window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Onset detection for attention selection |
| 10 | spectral_flux | 11 | M0 (value) | L0 (fwd) | Flux for middle window tracking |
| 10 | spectral_flux | 11 | M17 (peaks) | L0 (fwd) | Event count over motor window |
| 22 | energy_change | 11 | M8 (velocity) | L0 (fwd) | Envelope change rate |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Envelope regularity |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 21 | spectral_change | 8 | M3 (std) | L0 (fwd) | Spectral variability |
| 25 | x_l0l5[0] | 16 | M0 (value) | L2 (bidi) | Bar-level coupling signal |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Bar-level repetition |
| 33 | x_l4l5[0] | 16 | M0 (value) | L2 (bidi) | Dynamics coupling at bar |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Coupling trajectory |
| 41 | x_l5l7[0] | 14 | M1 (mean) | L0 (fwd) | Perceptual x cross-band mean |
| 41 | x_l5l7[0] | 14 | M13 (entropy) | L0 (fwd) | Stream separation entropy |
| 24 | timbre_change | 8 | M0 (value) | L0 (fwd) | Current timbre dynamics |
| 24 | timbre_change | 14 | M3 (std) | L0 (fwd) | Timbre variability for asymmetry |
| 8 | loudness | 14 | M1 (mean) | L0 (fwd) | Mean loudness over beat window |
| 8 | loudness | 20 | M18 (trend) | L0 (fwd) | Long-range loudness trend |

**Total ETAM H³ demand**: 20 tuples of 2304 theoretical = 0.87%

### 5.2 BEP + TMH Mechanism Binding

ETAM reads from both the **BEP** (Beat Entrainment Pathway) and **TMH** (Temporal Memory Hierarchy) mechanisms:

| Mechanism | Sub-section | Range | ETAM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Induction | BEP[0:10] | Early window (150-220ms): initial attention selection | **1.0** (primary) |
| **BEP** | Meter Extraction | BEP[10:20] | Middle window (320-360ms): stream tracking | **0.9** |
| **BEP** | Motor Entrainment | BEP[20:30] | Late window (410-450ms): deep segregation | **0.8** |
| **TMH** | Short Context | TMH[0:10] | Late window modulation: attention-context binding | **0.7** |
| **TMH** | Medium Context | TMH[10:20] | Tempo stability context for attention sustain | **0.5** (secondary) |
| **TMH** | Long Context | TMH[20:30] | Long-range attention modulation (structural) | **0.3** (tertiary) |

ETAM is the first STU β-tier model to read from all three BEP sub-sections, reflecting the full hierarchy of attention-modulated delay windows.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ETAM OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_early_window        │ [0, 1] │ Early attention window (150-220ms).
    │                         │        │ STG/Heschl's envelope tracking.
    │                         │        │ Both instruments (bassoon+cello).
    │                         │        │ f01 = σ(0.35 * amp_val * loud_val
    │                         │        │       + 0.35 * onset_val
    │                         │        │         * mean(BEP.beat_ind[0:10])
    │                         │        │       + 0.30 * amp_peak)
────┼─────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_middle_window       │ [0, 1] │ Middle attention window (320-360ms).
    │                         │        │ MTG/IFG stream tracking.
    │                         │        │ Bassoon-specific enhancement.
    │                         │        │ f02 = σ(0.40 * flux_val
    │                         │        │         * mean(BEP.meter[10:20])
    │                         │        │       + 0.30 * spec_chg_mean
    │                         │        │       + 0.30 * energy_vel)
────┼─────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_late_window         │ [0, 1] │ Late attention window (410-450ms).
    │                         │        │ IFG/temporal pole deep segregation.
    │                         │        │ Bassoon-specific, spectral richness.
    │                         │        │ f03 = σ(0.35 * x_coupling_bar
    │                         │        │         * mean(BEP.motor[20:30])
    │                         │        │       + 0.35 * x_l5l7_mean
    │                         │        │         * mean(TMH.short[0:10])
    │                         │        │       + 0.30 * stream_entropy)
────┼─────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_instrument_asymmetry│ [0, 1] │ Instrument-dependent asymmetry.
    │                         │        │ Bassoon (3 windows) vs cello (1).
    │                         │        │ Spectral richness modulation.
    │                         │        │ f04 = σ(0.50 * timbre_var
    │                         │        │       + 0.50 * (f02 * f03))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────
 4  │ attention_gain          │ [0, 1] │ Attention-modulated tracking gain.
    │                         │        │ Weighted sum across 3 windows.
    │                         │        │ gain = 0.60*(f01+f02+f03)/3
────┼─────────────────────────┼────────┼────────────────────────────────────
 5  │ entrainment_index       │ [0, 1] │ Beat entrainment strength.
    │                         │        │ BEP periodicity × envelope regularity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────
 6  │ envelope_tracking       │ [0, 1] │ Real-time envelope-neural coupling.
    │                         │        │ Attended stream tracking quality.
────┼─────────────────────────┼────────┼────────────────────────────────────
 7  │ stream_separation       │ [0, 1] │ Polyphonic stream separation state.
    │                         │        │ Cross-band energy x attention.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────
 8  │ tracking_prediction     │ [0, 1] │ Predicted tracking quality at next
    │                         │        │ beat cycle. BEP-trend based.
────┼─────────────────────────┼────────┼────────────────────────────────────
 9  │ attention_sustain       │ [0, 1] │ Predicted attention sustainability.
    │                         │        │ TMH context-driven endurance.
────┼─────────────────────────┼────────┼────────────────────────────────────
10  │ segregation_predict     │ [0, 1] │ Predicted stream segregation depth.
    │                         │        │ Multi-window enhancement prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Attention-Modulated Envelope Tracking

```
Envelope Tracking with Attention:

    Tracking(t, instrument) = Σ_w Attention(w) · Envelope(t - Δ_w)

    where w ∈ {early, middle, late}
          Δ_early  = 150-220ms
          Δ_middle = 320-360ms
          Δ_late   = 410-450ms

Attention Gain:
    Gain_attended = d · Gain_baseline
    d = 0.6 (Hausfeld 2021)

Instrument Asymmetry:
    N_windows(bassoon)  = 3  (early + middle + late)
    N_windows(cello)    = 1  (early only)
    Asymmetry = spectral_richness · (f02 · f03)

    Spectrally rich instruments provide more cues for
    hierarchical attention-driven stream separation.
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Early Window (150-220ms, STG/Heschl's, d=0.6)
amp_val = h3[(7, 6, 0, 2)]           # amplitude value at H6
amp_peak = h3[(7, 6, 4, 2)]          # amplitude max at H6
loud_val = h3[(8, 6, 0, 0)]          # loudness value at H6
onset_val = h3[(11, 6, 0, 0)]        # onset_strength value at H6
f01 = σ(0.35 * amp_val * loud_val
       + 0.35 * onset_val * mean(BEP.beat_induction[0:10])
       + 0.30 * amp_peak)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Middle Window (320-360ms, MTG/IFG, bassoon-specific)
flux_val = h3[(10, 11, 0, 0)]        # spectral_flux value at H11
spec_chg_mean = h3[(21, 8, 1, 0)]    # spectral_change mean at H8
energy_vel = h3[(22, 11, 8, 0)]      # energy_change velocity at H11
f02 = σ(0.40 * flux_val * mean(BEP.meter_extraction[10:20])
       + 0.30 * spec_chg_mean
       + 0.30 * energy_vel)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Late Window (410-450ms, IFG/TP, bassoon-specific)
x_coupling_bar = h3[(25, 16, 0, 2)]  # x_l0l5 value at H16
x_l5l7_mean = h3[(41, 14, 1, 0)]     # x_l5l7 mean at H14
stream_entropy = h3[(41, 14, 13, 0)]  # x_l5l7 entropy at H14
f03 = σ(0.35 * x_coupling_bar * mean(BEP.motor_entrainment[20:30])
       + 0.35 * x_l5l7_mean * mean(TMH.short_context[0:10])
       + 0.30 * stream_entropy)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Instrument Asymmetry (spectral richness modulation)
timbre_var = h3[(24, 14, 3, 0)]      # timbre_change std at H14
f04 = σ(0.50 * timbre_var + 0.50 * (f02 * f03))
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | ETAM Function |
|--------|-----------------|----------|---------------|---------------|
| **Superior Temporal Gyrus (STG)** | ±60, -30, 8 | 3+ | Direct (EEG/MEG) | Early window (150-220ms) — initial attention selection |
| **Heschl's Gyrus (HG)** | ±50, -20, 8 | 2 | Direct (EEG/MEG) | Early window — primary auditory envelope tracking |
| **Middle Temporal Gyrus (MTG)** | ±60, -40, 0 | 2 | Direct (EEG/MEG) | Middle window (320-360ms) — stream tracking |
| **Inferior Frontal Gyrus (IFG)** | ±50, 28, 8 | 3 | Direct (EEG/MEG) | Middle + Late window — attention-driven segregation |

---

## 9. Cross-Unit Pathways

### 9.1 ETAM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ETAM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  HMCE.context_depth ──────► ETAM (context for attention window depth)      │
│  AMSC.auditory_activatn ──► ETAM (auditory gamma → envelope tracking)     │
│  ETAM.envelope_tracking ──► MDNS (attention-filtered stream for decoding) │
│  ETAM.stream_separation ──► AMSS (separated streams for selection)        │
│                                                                             │
│  CROSS-UNIT (P4: STU internal):                                            │
│  BEP.beat_induction ↔ TMH.short_context (entrainment × attention)         │
│  Beat strength modulates attention-driven envelope tracking depth          │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  ETAM.attention_gain ──► ARU (attention-modulated arousal)                │
│  Stronger envelope tracking → enhanced emotional engagement               │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────► ETAM (beat/meter/motor entrainment)        │
│  TMH mechanism (30D) ────────► ETAM (temporal context hierarchy)          │
│  R³ (~33D) ──────────────────► ETAM (direct spectral features)            │
│  H³ (20 tuples) ─────────────► ETAM (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Single-window instruments** | Low spectral-richness instruments should show only early window enhancement | ✅ **Confirmed**: Cello = 1 window (Hausfeld 2021) |
| **Multi-window instruments** | High spectral-richness instruments should show all 3 windows | ✅ **Confirmed**: Bassoon = 3 windows (Hausfeld 2021) |
| **Attention abolition** | Removing attention task should eliminate window hierarchy | Testable (passive vs active listening) |
| **Delay window stability** | The 150/320/410ms windows should be stable across musical stimuli | Testable (different polyphonic pieces) |
| **Dose-response** | Graded attention load should modulate tracking gain parametrically | Testable (dual-task paradigm) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ETAM(BaseModel):
    """Entrainment, Tempo & Attention Modulation.

    Output: 11D per frame.
    Reads: BEP mechanism (30D, primary), TMH mechanism (30D, secondary), R³ direct.
    """
    NAME = "ETAM"
    UNIT = "STU"
    TIER = "β4"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")    # Both sensorimotor mechanisms

    ATTENTION_D = 0.60    # Hausfeld 2021 effect size
    EARLY_DELAY = 0.185   # 150-220ms center (seconds)
    MIDDLE_DELAY = 0.340  # 320-360ms center (seconds)
    LATE_DELAY = 0.430    # 410-450ms center (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """20 tuples for ETAM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: beat entrainment ──
            # Early window (H6 = 200ms)
            (7, 6, 0, 2),     # amplitude, value, bidirectional
            (7, 6, 4, 2),     # amplitude, max, bidirectional
            (8, 6, 0, 0),     # loudness, value, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            # Middle window (H11 = 500ms)
            (10, 11, 0, 0),   # spectral_flux, value, forward
            (10, 11, 17, 0),  # spectral_flux, peaks, forward
            (22, 11, 8, 0),   # energy_change, velocity, forward
            (22, 11, 14, 2),  # energy_change, periodicity, bidirectional
            # Bar level (H16 = 1000ms)
            (25, 16, 0, 2),   # x_l0l5[0], value, bidirectional
            (25, 16, 14, 2),  # x_l0l5[0], periodicity, bidirectional
            (33, 16, 0, 2),   # x_l4l5[0], value, bidirectional
            (33, 16, 18, 0),  # x_l4l5[0], trend, forward
            # ── TMH horizons: temporal context ──
            # Syllable context (H8 = 300ms)
            (21, 8, 1, 0),    # spectral_change, mean, forward
            (21, 8, 3, 0),    # spectral_change, std, forward
            (24, 8, 0, 0),    # timbre_change, value, forward
            # Beat context (H14 = 700ms)
            (41, 14, 1, 0),   # x_l5l7[0], mean, forward
            (41, 14, 13, 0),  # x_l5l7[0], entropy, forward
            (24, 14, 3, 0),   # timbre_change, std, forward
            (8, 14, 1, 0),    # loudness, mean, forward
            # Section context (H20 = 5000ms)
            (8, 20, 18, 0),   # loudness, trend, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute ETAM 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) ETAM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short context
        tmh_medium = tmh[..., 10:20]      # medium context

        # H³ features — Early window
        amp_val = h3_direct[(7, 6, 0, 2)].unsqueeze(-1)
        amp_peak = h3_direct[(7, 6, 4, 2)].unsqueeze(-1)
        loud_val = h3_direct[(8, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)

        # H³ features — Middle window
        flux_val = h3_direct[(10, 11, 0, 0)].unsqueeze(-1)
        spec_chg_mean = h3_direct[(21, 8, 1, 0)].unsqueeze(-1)
        energy_vel = h3_direct[(22, 11, 8, 0)].unsqueeze(-1)

        # H³ features — Late window
        x_coupling_bar = h3_direct[(25, 16, 0, 2)].unsqueeze(-1)
        x_l5l7_mean = h3_direct[(41, 14, 1, 0)].unsqueeze(-1)
        stream_entropy = h3_direct[(41, 14, 13, 0)].unsqueeze(-1)

        # H³ features — Instrument asymmetry
        timbre_var = h3_direct[(24, 14, 3, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Early Window (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * (amp_val * loud_val)
            + 0.35 * (onset_val
                      * bep_beat.mean(-1, keepdim=True))
            + 0.30 * amp_peak
        )

        # f02: Middle Window (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * (flux_val
                    * bep_meter.mean(-1, keepdim=True))
            + 0.30 * spec_chg_mean
            + 0.30 * energy_vel
        )

        # f03: Late Window (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * (x_coupling_bar
                    * bep_motor.mean(-1, keepdim=True))
            + 0.35 * (x_l5l7_mean
                      * tmh_short.mean(-1, keepdim=True))
            + 0.30 * stream_entropy
        )

        # f04: Instrument Asymmetry (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * timbre_var
            + 0.50 * (f02 * f03)
        )

        # ═══ LAYER M: Mathematical ═══
        attention_gain = self.ATTENTION_D * (f01 + f02 + f03) / 3

        energy_period = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
        bar_period = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        entrainment_index = torch.sigmoid(
            0.5 * energy_period + 0.5 * bar_period
        )

        # ═══ LAYER P: Present ═══
        envelope_tracking = torch.sigmoid(
            0.5 * f01 + 0.3 * bep_beat.mean(-1, keepdim=True)
            + 0.2 * loud_val
        )

        x_dyn_bar = h3_direct[(33, 16, 0, 2)].unsqueeze(-1)
        stream_separation = torch.sigmoid(
            0.4 * f03 + 0.3 * f04 + 0.3 * x_dyn_bar
        )

        # ═══ LAYER F: Future ═══
        groove_trend = h3_direct[(33, 16, 18, 0)].unsqueeze(-1)
        tracking_prediction = torch.sigmoid(
            0.5 * f01 + 0.3 * groove_trend
            + 0.2 * bep_beat.mean(-1, keepdim=True)
        )

        loud_mean_beat = h3_direct[(8, 14, 1, 0)].unsqueeze(-1)
        loud_trend_long = h3_direct[(8, 20, 18, 0)].unsqueeze(-1)
        attention_sustain = torch.sigmoid(
            0.4 * tmh_medium.mean(-1, keepdim=True)
            + 0.3 * loud_mean_beat
            + 0.3 * loud_trend_long
        )

        segregation_predict = torch.sigmoid(
            0.4 * f03 + 0.3 * f04 + 0.3 * stream_entropy
        )

        return torch.cat([
            f01, f02, f03, f04,                              # E: 4D
            attention_gain, entrainment_index,                # M: 2D
            envelope_tracking, stream_separation,             # P: 2D
            tracking_prediction, attention_sustain,
            segregation_predict,                              # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Hausfeld 2021 |
| **Effect Sizes** | d = 0.6 | Attention modulation (attended > unattended) |
| **Evidence Modality** | EEG/MEG | Direct neural |
| **Falsification Tests** | 2/5 confirmed | Instrument asymmetry validated |
| **R³ Features Used** | 33D of 49D | Energy + Change + Interactions (all 3) |
| **H³ Demand** | 20 tuples (0.87%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage — all 3 windows |
| **TMH Mechanism** | 30D (3 sub-sections) | Context support — attention modulation |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Hausfeld, L., et al. (2021)**. Cortical tracking of polyphonic music: Attention modulates envelope tracking of attended instruments at specific delay windows (150-220ms, 320-360ms, 410-450ms). Effect size d=0.6 for attended vs. unattended streams. Bassoon (spectrally rich) shows 3-window enhancement; cello shows 1-window enhancement. (EEG/MEG study)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L7, X_L5L7 | R³ (49D): Energy, Change, Interactions |
| Temporal | HC⁰ mechanisms (TIH, ATT, NPL, SGM) | BEP (30D, primary) + TMH (30D, secondary) |
| Early window | S⁰.L0.amplitude[2] + HC⁰.ATT | R³.amplitude[7] + BEP.beat_induction |
| Middle window | S⁰.L5.spectral_flux[45] + HC⁰.TIH | R³.spectral_flux[10] + BEP.meter_extraction |
| Late window | S⁰.L7.crossband[80:88] + HC⁰.SGM | R³.x_l0l5[25:33] + BEP.motor_entrainment + TMH |
| Attention signal | S⁰.L4.velocity_A[17] × HC⁰.ATT | R³.energy_change[22] × BEP + TMH |
| Phase coherence | S⁰.L7.phase[96:104] × HC⁰.NPL | R³.x_l5l7[41:49] (cross-band coupling) |
| Instrument asymmetry | S⁰.L5.sharpness[36] × HC⁰.NPL | R³.timbre_change[24] (spectral richness) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 30/2304 = 1.30% | 20/2304 = 0.87% |
| Output | 11D | 11D (same) |

### Why BEP+TMH replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (TIH, ATT, NPL, SGM). In MI, these are unified into two sensorimotor mechanisms:

- **ATT → BEP.beat_induction** [0:10]: Attentional entrainment for initial selection maps to beat-level tracking. The ATT mechanism captured attention-modulated gain, which in MI is achieved by BEP.beat_induction's intensity-tracking at the beat timescale.
- **TIH → BEP.meter_extraction** [10:20]: Temporal integration hierarchy for multi-window processing maps to meter-level stream tracking. TIH's multi-scale integration is captured by BEP's meter sub-section at H11.
- **NPL → BEP.motor_entrainment** [20:30]: Neural phase-locking for deep segregation maps to motor entrainment. NPL's phase coherence is replaced by BEP's motor coupling at H16, which captures the late-window deep segregation.
- **SGM → TMH.short_context** [0:10] + **TMH.medium_context** [10:20]: Striatal gradient memory for long-range attention modulation maps to TMH's hierarchical context. SGM's structural memory is unified into TMH's temporal memory hierarchy.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
