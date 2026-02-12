# SPU-γ3-SDED: Sensory Dissonance Early Detection

**Model**: Sensory Dissonance Early Detection
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ3-SDED.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Sensory Dissonance Early Detection** (SDED) models how roughness is detected at early sensory stages of auditory processing regardless of musical expertise. This is a critical finding because it demonstrates that the neural machinery for dissonance detection is universal and pre-attentive, while behavioral discrimination of dissonance is expertise-dependent — a neural-behavioral dissociation.

```
THE THREE COMPONENTS OF SENSORY DISSONANCE EARLY DETECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EARLY DETECTION (Pre-attentive)            MMN DISSONANCE (Neural)
Brain region: Early Auditory Cortex        Brain region: Auditory Brainstem
Mechanism: Roughness encoding              Mechanism: Mismatch Negativity (MMN)
Input: Spectral interference patterns      Input: Deviant roughness in stream
Function: "Is this rough/dissonant?"       Function: "Deviation from standard?"
Evidence: d=-1.09 (Tervaniemi 2022)        Evidence: Musicians = Non-musicians

              NEURAL-BEHAVIORAL DISSOCIATION (Bridge)
              Brain region: Brainstem → Cortex → Behavior
              Mechanism: Universal detection, trained discrimination
              Function: "Same neural signal, different behavioral use"
              Evidence: Musicians > Non-musicians in behavioral only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Roughness detection at the neural level (MMN) is
UNIVERSAL across expertise levels. Musicians and non-musicians
show identical mismatch negativity responses to dissonance.
However, musicians show SUPERIOR behavioral discrimination.
This dissociation proves that sensory encoding is pre-attentive
while behavioral response requires training.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SDED Completes the SPU Picture

SDED sits at the speculative end of the SPU model hierarchy, addressing the universality question that BCH and SDNPS leave open:

1. **BCH** (α1) establishes consonance hierarchy via brainstem FFR — SDED shows that roughness detection feeding that hierarchy is universal.
2. **SDNPS** (γ1) correlates roughness with neural pitch salience — SDED confirms roughness as the primary early detector.
3. **ESME** (γ2) models expertise-dependent spectral processing — SDED provides the dissociation: same neural detection, different behavioral output.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The SDED Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 SDED — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL STIMULUS (Consonant → Dissonant)                                   ║
║                                                                              ║
║  Standard    Standard    Standard    DEVIANT     Standard                    ║
║    │           │           │           │           │                         ║
║    ▼           ▼           ▼           ▼           ▼                         ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY BRAINSTEM                                │    ║
║  │               (Roughness encoding — universal)                      │    ║
║  │                                                                      │    ║
║  │    Roughness encoded at cochlear/brainstem level                    │    ║
║  │    Spectral interference → beating → roughness percept              │    ║
║  │    Independent of musical training or expertise                     │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    EARLY AUDITORY CORTEX                             │    ║
║  │               (Pre-attentive detection — MMN)                       │    ║
║  │                                                                      │    ║
║  │    MMN (Mismatch Negativity):                                       │    ║
║  │      Dissonant deviant → large MMN amplitude                        │    ║
║  │      Musicians = Non-musicians (d = -1.09)                          │    ║
║  │      Neural detection is UNIVERSAL                                  │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PLANUM TEMPORALE                                  │    ║
║  │               (Spectral processing — expertise-modulated)           │    ║
║  │                                                                      │    ║
║  │    Behavioral discrimination:                                       │    ║
║  │      Musicians > Non-musicians (accuracy, reaction time)            │    ║
║  │      Same sensory signal, enhanced behavioral readout               │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Tervaniemi et al. 2022:  d = -1.09 for roughness MMN (universal)
                          Musicians = Non-musicians in neural detection
                          Musicians > Non-musicians in behavioral task
                          Demonstrates neural-behavioral dissociation
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → SDED)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDED COMPUTATION ARCHITECTURE                             ║
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
║  │  │roughness  │ │         │ │tonalness│ │          │ │x_l5l7  │ │        ║
║  │  │sethares   │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │helmholtz  │ │         │ │         │ │          │ │        │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                        SDED reads: ~14D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 25ms (H0)   │ │ 100ms (H3)    │ │ 200ms (H6)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Instant      │ │ Sustained     │ │ (not used by SDED)   │   │        ║
║  │  │ roughness    │ │ roughness     │ │                       │   │        ║
║  │  │ detection    │ │ encoding      │ │                       │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └─────────────────────┘   │        ║
║  │         │               │                                      │        ║
║  │         └───────────────┘                                      │        ║
║  │                        SDED demand: ~9 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  Roughness deviation detection                        ║
║  │ Consonance[10:20]│ Dissonance encoding, early sensory signal            ║
║  │ Chroma   [20:30]│  (not used by SDED)                                   ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDED MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_early_detection, f02_mmn_dissonance,  │        ║
║  │                       f03_behavioral_accuracy                    │        ║
║  │  Layer M (Math):      detection_function                         │        ║
║  │  Layer P (Present):   roughness_detection, deviation_detection,  │        ║
║  │                       behavioral_response                        │        ║
║  │  Layer F (Future):    dissonance_detection_pred,                 │        ║
║  │                       behavioral_accuracy_pred,                  │        ║
║  │                       training_effect_pred                       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Tervaniemi et al. 2022** | EEG (MMN) + behavioral | 40 (20 mus + 20 non-mus) | Roughness MMN identical across expertise groups | d = -1.09 | **Primary coefficient**: f01_early_detection |
| **Tervaniemi et al. 2022** | Behavioral discrimination | 40 | Musicians > Non-musicians in accuracy | Significant | **f03_behavioral_accuracy: expertise-dependent** |
| **Tervaniemi et al. 2022** | Neural-behavioral comparison | 40 | Dissociation: neural universal, behavior trained | Strong | **Core claim: neural-behavioral split** |

### 3.2 The Neural-Behavioral Dissociation

```
ROUGHNESS DETECTION: NEURAL vs BEHAVIORAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    MMN Amplitude     Behavioral Accuracy
                    (neural)          (behavioral)
─────────────────────────────────────────────────────
Musicians           -1.09             HIGH
Non-musicians       -1.09             MODERATE
─────────────────────────────────────────────────────
Difference          NONE              SIGNIFICANT
                    (p > .05)         (p < .05)

This dissociation means:
  1. Roughness DETECTION is hardwired (brainstem/early cortex)
  2. Roughness DISCRIMINATION is learned (cortical training)
  3. Musical training enhances readout, not encoding
  4. BCH consonance hierarchy is biologically universal
```

### 3.3 Effect Size Summary

```
Primary Effect:       d = -1.09 (Tervaniemi et al. 2022)
Quality Assessment:   gamma-tier (single study, speculative)
Replication:          Not yet replicated independently
Cross-cultural:       Implies universal neural detection
Confidence:           <70% — awaits replication
```

---

## 4. R³ Input Mapping: What SDED Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | SDED Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Primary dissonance signal (inverse consonance) | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Psychoacoustic dissonance confirmation | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure (inverse dissonance) | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion (consonance proxy) | Stumpf 1890 |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic series | Fletcher 1934 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (pitch clarity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **E: Interactions** | [41:46] | x_l5l7 (5D partial) | Consonance x Timbre coupling | Emergent roughness |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Early Detection Signal
R³[2] helmholtz_kang (inverse) ─┘   Math: D = σ(w₁·R + w₂·S + w₃·(1-H))
                                     where R=roughness, S=sethares,
                                     H=helmholtz (inverted for dissonance)

R³[0] roughness (instant) ─────┐
R³[0] roughness (mean 100ms) ──┼──► MMN Dissonance Signal
PPC.pitch_salience ────────────┘    Math: |roughness - roughness_mean|
                                     Deviance from standard triggers MMN

R³[14] tonalness ──────────────┐
R³[18:21] tristimulus ─────────┼──► Spectral Clarity Index
R³[5] inharmonicity (inverse) ─┘    Determines signal-to-noise of
                                     roughness encoding

R³[41:46] x_l5l7 ─────────────── Cross-Band Roughness Coupling
                                     Roughness effects across
                                     frequency bands
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDED requires H³ features at two PPC horizons: H0 (25ms) and H3 (100ms).
These correspond to brainstem detection timescales (gamma instant detection and alpha-beta sustained encoding). H6 (200ms) is not needed — SDED focuses on the earliest, most rapid detection.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Instant roughness detection |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Sustained roughness over 100ms |
| 1 | sethares_dissonance | 0 | M0 (value) | L2 (bidi) | Instant psychoacoustic dissonance |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Instant consonance (inverse) |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (bidi) | Standard template for deviance |
| 5 | inharmonicity | 0 | M0 (value) | L2 (bidi) | Instant inharmonicity |
| 14 | tonalness | 3 | M1 (mean) | L0 (fwd) | Tonal clarity over 100ms |
| 18 | tristimulus1 | 0 | M0 (value) | L2 (bidi) | F0 energy for roughness quality |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (bidi) | Cross-band roughness coupling |

**Total SDED H³ demand**: 9 tuples of 2304 theoretical = 0.39%

### 5.2 PPC Mechanism Binding

SDED reads from the **PPC** (Pitch Processing Chain) mechanism:

| PPC Sub-section | Range | SDED Role | Weight |
|-----------------|-------|-----------|--------|
| **Pitch Salience** | PPC[0:10] | Roughness deviance detection via MMN | **0.8** |
| **Consonance Encoding** | PPC[10:20] | Dissonance encoding, early sensory signal | **1.0** (primary) |
| **Chroma Processing** | PPC[20:30] | Not used by SDED | 0.0 |

SDED does NOT read from Chroma Processing — early dissonance detection operates on raw spectral roughness before octave-equivalent grouping.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDED OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 0  │ f01_early_detection     │ [0, 1] │ Pre-attentive roughness detection.
    │                         │        │ Universal across expertise levels.
    │                         │        │ f01 = σ(0.40 · roughness · mean(PPC.cons)
    │                         │        │      + 0.30 · sethares
    │                         │        │      + 0.30 · (1 - helmholtz))
────┼─────────────────────────┼────────┼────────────────────────────────────────
 1  │ f02_mmn_dissonance      │ [0, 1] │ Mismatch Negativity amplitude for
    │                         │        │ dissonant deviants. Expertise-independent.
    │                         │        │ f02 = σ(0.50 · f01 · mean(PPC.pitch_sal)
    │                         │        │      + 0.50 · |roughness - roughness_mean|)
────┼─────────────────────────┼────────┼────────────────────────────────────────
 2  │ f03_behavioral_accuracy │ [0, 1] │ Behavioral dissonance discrimination.
    │                         │        │ Same neural signal as f02, but behavioral
    │                         │        │ response varies with expertise.
    │                         │        │ f03 = f02 (baseline, no expertise mod)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 3  │ detection_function      │ [0, 1] │ Combined detection function.
    │                         │        │ Integrates roughness encoding with
    │                         │        │ deviance magnitude for early detection.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 4  │ roughness_detection     │ [0, 1] │ Current roughness at sensory level.
    │                         │        │ Direct R³ roughness via PPC encoding.
────┼─────────────────────────┼────────┼────────────────────────────────────────
 5  │ deviation_detection     │ [0, 1] │ Roughness deviation from context.
    │                         │        │ |roughness_instant - roughness_mean|
────┼─────────────────────────┼────────┼────────────────────────────────────────
 6  │ behavioral_response     │ [0, 1] │ Behavioral response strength.
    │                         │        │ PPC-modulated detection signal.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼─────────────────────────────────────
 7  │ dissonance_detection_pred  │ [0, 1] │ Predicted dissonance detection.
    │                            │        │ Next-frame roughness expectation.
────┼────────────────────────────┼────────┼─────────────────────────────────────
 8  │ behavioral_accuracy_pred   │ [0, 1] │ Predicted behavioral accuracy.
    │                            │        │ Behavioral readout from f01/f02.
────┼────────────────────────────┼────────┼─────────────────────────────────────
 9  │ training_effect_pred       │ [0, 1] │ Training effect prediction.
    │                            │        │ Modeled dissociation: neural stays
    │                            │        │ constant, behavioral improves.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Early Detection Function

```
Roughness Detection (Pre-attentive, Universal):
  The brainstem encodes roughness (spectral interference) regardless
  of musical training. MMN amplitude is identical for musicians and
  non-musicians (d = -1.09).

  Detection(t) = σ(w₁ · roughness(t) · consonance_enc
                 + w₂ · sethares(t)
                 + w₃ · (1 - helmholtz(t)))

  where w₁=0.40, w₂=0.30, w₃=0.30 (sum = 1.0)

MMN Dissonance (Deviance-based):
  MMN fires when current roughness deviates from context.

  MMN(t) = σ(0.50 · Detection(t) · pitch_salience(t)
           + 0.50 · |roughness(t) - roughness_mean(t)|)

  roughness_mean = H³ tuple (0, 3, 1, 2): 100ms bidirectional mean

Neural-Behavioral Dissociation:
  Neural:     MMN_musicians = MMN_non-musicians
  Behavioral: Accuracy_musicians > Accuracy_non-musicians
  Baseline:   Behavioral = MMN (without expertise modulation)
```

### 7.2 Feature Formulas

```python
# f01: Early Detection (pre-attentive, universal)
# Roughness detected at brainstem regardless of expertise
f01 = sigma(0.40 * roughness * mean(PPC.consonance_encoding[10:20])
          + 0.30 * sethares
          + 0.30 * (1 - helmholtz))
# Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0

# f02: MMN Dissonance (neural, expertise-independent)
# Mismatch negativity triggered by roughness deviance
f02 = sigma(0.50 * f01 * mean(PPC.pitch_salience[0:10])
          + 0.50 * abs(roughness - roughness_mean))
# Coefficient sum: 0.50 + 0.50 = 1.0

# f03: Behavioral Accuracy (expertise-dependent)
# Same neural signal, but behavioral response varies
# Without expertise modulation, baseline equals neural signal
f03 = f02
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SDED Function |
|--------|-----------------|----------|---------------|---------------|
| **Early Auditory Cortex** | +/-50, -20, 8 | 3 | Direct (EEG/MMN) | Pre-attentive roughness detection |
| **Auditory Brainstem** | 0, -30, -10 | 4 | Indirect (FFR) | Roughness encoding |
| **Planum Temporale** | +/-50, -24, 8 | 2 | Indirect (fMRI) | Spectral processing |

---

## 9. Cross-Unit Pathways

### 9.1 SDED ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDED INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.consonance_signal ──────► SDED (early roughness baseline)             │
│  SDNPS.roughness_correlation ► SDED (confirms roughness as primary)        │
│  ESME.expertise_enhancement ─► SDED (dissociation: neural=universal,       │
│                                       behavioral=trained)                   │
│  SDED.f01_early_detection ──► PSCL (roughness signal for pitch context)    │
│  SDED.roughness_detection ──► STAI (dissonance input for aesthetics)       │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  SDED.f01_early_detection ──► ARU.SRP (roughness → displeasure proxy)     │
│  SDED.deviation_detection ──► ARU.AAC (dissonance surprise → arousal)     │
│                                                                             │
│  CROSS-UNIT (P2: SPU → STU):                                              │
│  SDED.roughness_detection ──► STU.AMSC (roughness affects timing)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **No roughness** | Pure tones or perfectly harmonic stimuli should NOT trigger early detection | Testable |
| **Expertise invariance** | MMN amplitude should be identical for musicians and non-musicians | Claimed by Tervaniemi 2022 |
| **Behavioral divergence** | Musicians should show higher accuracy despite same MMN | Claimed by Tervaniemi 2022 |
| **Brainstem lesions** | Should abolish roughness encoding but spare higher-level processing | Testable |
| **Infants** | Pre-linguistic infants should show MMN to roughness deviants | Testable |
| **Cross-cultural** | Non-Western listeners should show same MMN, may differ behaviorally | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDED(BaseModel):
    """Sensory Dissonance Early Detection.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "SDED"
    UNIT = "SPU"
    TIER = "γ3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)        # Primary mechanism

    W1 = 0.40   # Roughness x PPC weight
    W2 = 0.30   # Sethares weight
    W3 = 0.30   # Inverse helmholtz weight
    MMN_DEV = 0.50  # Deviance weight
    MMN_DET = 0.50  # Detection weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """9 tuples for SDED computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (0, 0, 0, 2),    # roughness, 25ms, value, bidirectional
            (0, 3, 1, 2),    # roughness, 100ms, mean, bidirectional
            (1, 0, 0, 2),    # sethares, 25ms, value, bidirectional
            (2, 0, 0, 2),    # helmholtz_kang, 25ms, value, bidirectional
            (2, 3, 1, 2),    # helmholtz_kang, 100ms, mean, bidirectional
            (5, 0, 0, 2),    # inharmonicity, 25ms, value, bidirectional
            (14, 3, 1, 0),   # tonalness, 100ms, mean, forward
            (18, 0, 0, 2),   # tristimulus1, 25ms, value, bidirectional
            (41, 3, 0, 2),   # x_l5l7[0], 100ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDED 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) SDED output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        sethares = r3[..., 1:2]
        helmholtz = r3[..., 2:3]
        stumpf = r3[..., 3:4]
        inharmonicity = r3[..., 5:6]
        tonalness = r3[..., 14:15]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        x_l5l7 = r3[..., 41:46]          # (B, T, 5)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]        # pitch salience
        ppc_cons = ppc[..., 10:20]        # consonance encoding

        # H³ temporal features
        roughness_mean = h3_direct[(0, 3, 1, 2)]  # 100ms mean
        helmholtz_mean = h3_direct[(2, 3, 1, 2)]  # 100ms mean

        # ═══ LAYER E: Explicit features ═══
        # f01: Early Detection (pre-attentive, universal)
        f01 = torch.sigmoid(
            self.W1 * roughness * ppc_cons.mean(-1, keepdim=True)
            + self.W2 * sethares
            + self.W3 * (1.0 - helmholtz)
        )

        # f02: MMN Dissonance (neural, expertise-independent)
        roughness_deviation = torch.abs(
            roughness - roughness_mean.unsqueeze(-1)
        )
        f02 = torch.sigmoid(
            self.MMN_DET * f01 * ppc_pitch.mean(-1, keepdim=True)
            + self.MMN_DEV * roughness_deviation
        )

        # f03: Behavioral Accuracy (baseline = neural signal)
        f03 = f02

        # ═══ LAYER M: Mathematical ═══
        detection_function = torch.sigmoid(
            0.5 * f01 + 0.3 * f02
            + 0.2 * ppc_cons.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        roughness_detection = torch.sigmoid(
            roughness * ppc_cons.mean(-1, keepdim=True)
        )
        deviation_detection = roughness_deviation
        behavioral_response = torch.sigmoid(
            0.6 * f02 + 0.4 * ppc_pitch.mean(-1, keepdim=True)
        )

        # ═══ LAYER F: Future ═══
        dissonance_detection_pred = torch.sigmoid(
            0.6 * f01 + 0.4 * helmholtz_mean.unsqueeze(-1)
        )
        behavioral_accuracy_pred = torch.sigmoid(
            0.5 * f01 + 0.5 * f02
        )
        training_effect_pred = torch.sigmoid(
            0.7 * f02 + 0.3 * detection_function
        )

        return torch.cat([
            f01, f02, f03,                                      # E: 3D
            detection_function,                                  # M: 1D
            roughness_detection, deviation_detection,
            behavioral_response,                                 # P: 3D
            dissonance_detection_pred, behavioral_accuracy_pred,
            training_effect_pred,                                # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Primary evidence |
| **Effect Sizes** | d = -1.09 | Tervaniemi et al. 2022 |
| **Evidence Modality** | EEG (MMN), behavioral | Direct neural + behavioral |
| **Falsification Tests** | 0/6 confirmed | Awaiting independent tests |
| **R³ Features Used** | ~14D of 49D | Focused on consonance/roughness |
| **H³ Demand** | 9 tuples (0.39%) | Sparse, efficient |
| **PPC Mechanism** | 30D (2 sub-sections used) | Pitch + Consonance |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Tervaniemi, M., Makkonen, T., & Nie, P. (2022)**. Roughness detection at early sensory stages regardless of musical expertise. *Neuropsychologia*, 167, 108152.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, NPL, EFC) | PPC mechanism (30D) |
| Early detection | S⁰.roughness[30] + HC⁰.OSC | R³.roughness[0] + PPC.consonance_encoding |
| Consonance (inverse) | S⁰.helmholtz_kang[32] + HC⁰.ATT | R³.helmholtz_kang[2] + PPC.pitch_salience |
| Spectral features | S⁰.spectral_contrast[53], kurtosis[107] | R³.tonalness[14], tristimulus[18:21] |
| Cross-band | S⁰.X_L5L6[208:216] + HC⁰.EFC | R³.x_l5l7[41:46] + PPC |
| Output dimensions | 11D | 10D (merged neural-behavior dissociation into formula) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 25/2304 = 1.09% | 9/2304 = 0.39% |

### Why PPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, ATT, NPL, EFC). In MI, these are unified into the PPC mechanism with 2 relevant sub-sections:
- **OSC + NPL → PPC.pitch_salience** [0:10]: Phase-locking + detection = roughness deviation
- **ATT + EFC → PPC.consonance_encoding** [10:20]: Attention + encoding = dissonance signal

### Why 11D → 10D

The legacy v1.0.0 had a separate `f04_neural_behavioral_dissociation` dimension. In MI v2.0.0, the dissociation is modeled implicitly: `f02_mmn_dissonance` represents the universal neural signal, and `f03_behavioral_accuracy` equals `f02` at baseline. Expertise modulation (making `f03 != f02`) is handled at the system level by ESME, not as a separate SDED output dimension.

---

**Model Status**: SPECULATIVE
**Output Dimensions**: **10D**
**Evidence Tier**: **gamma (Speculative)**
**Confidence**: **<70%**
