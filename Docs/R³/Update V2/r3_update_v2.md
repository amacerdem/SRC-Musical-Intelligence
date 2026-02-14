# R³ Update V2: Compositional Feature Gap Analysis & Enhancement Roadmap

**Version**: 1.0.0
**Date**: 2026-02-14
**Author**: MI Architecture Team
**Status**: DRAFT — Starting Document for Phase 5+ Planning

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current State Assessment](#2-current-state-assessment)
3. [The Compositional Gap Problem](#3-the-compositional-gap-problem)
4. [Gap Analysis by Domain](#4-gap-analysis-by-domain)
5. [C³ Model Dependency Analysis](#5-c3-model-dependency-analysis)
6. [H³ Temporal Demand Implications](#6-h3-temporal-demand-implications)
7. [Solution Taxonomy: Bridge Features](#7-solution-taxonomy-bridge-features)
8. [Implementation Roadmap](#8-implementation-roadmap)
9. [Known Code Issues](#9-known-code-issues)
10. [Risk Assessment](#10-risk-assessment)
11. [Open Questions](#11-open-questions)
12. [References](#12-references)

---

## 1. Executive Summary

R³ v2 is **fully implemented** at 128D across 11 groups (A-K) and validates end-to-end (Swan Lake test: 30s audio → R³(128D) → H³(7782 tuples) → C³(1006D)). However, a fundamental architectural gap exists:

> **R³ excels at frame-level physical/spectral measurements but provides only crude approximations for compositional and music-theoretic features.**

Features like `tonal_stability` [84], `key_clarity` [75], `syntactic_irregularity` [86], and `melodic_entropy` [87] — which 41+ C³ models depend on — are computed as simple frame-level DSP proxies of what should be hierarchical music-theoretic computations. The chroma itself, which underpins Groups F, H, and I (totaling 35 dimensions), is derived from mel spectrograms via Gaussian soft-assignment rather than from CQT or f0 tracking, introducing systematic errors below 200 Hz.

This document identifies the problems, surveys state-of-the-art solutions, and proposes a tiered enhancement roadmap that preserves real-time performance at 172.27 Hz while significantly improving compositional feature quality.

### Key Numbers

| Metric | Value |
|--------|-------|
| Current R³ dimensionality | 128D |
| Groups with compositional features | F, G, H, I (35D) |
| C³ models depending on Group I | 41 / 96 (42.7%) |
| C³ models depending on Group G | 36 / 96 (37.5%) |
| C³ models depending on Group H | 16 / 96 (16.7%) |
| C³ models depending on Group F | 19 / 96 (19.8%) |
| Most-referenced v2 feature | melodic_entropy [87] (35+ models) |
| Frame budget at 172.27 Hz | 5.8 ms |
| Estimated cost of Tier 1 enhancements | < 0.1 ms |

---

## 2. Current State Assessment

### 2.1 R³ v2 Architecture (128D)

R³ operates as a 3-stage DAG computing 128 spectral features per frame at 172.27 Hz (sr=44100, hop=256):

```
Stage 1 (Independent, parallel):
  A: Consonance .......... [0:7]    7D   ← mel only
  B: Energy .............. [7:12]   5D   ← mel only
  C: Timbre .............. [12:21]  9D   ← mel only
  D: Change .............. [21:25]  4D   ← mel only
  F: Pitch & Chroma ...... [49:65]  16D  ← mel only
  J: Timbre Extended ..... [94:114] 20D  ← mel only
  K: Modulation .......... [114:128] 14D ← mel only

Stage 2 (Dependencies):
  E: Interactions ........ [25:49]  24D  ← A, B, C, D
  G: Rhythm & Groove ..... [65:75]  10D  ← B (onset_strength)
  H: Harmony & Tonality .. [75:87]  12D  ← F (chroma)

Stage 3 (Final):
  I: Information ......... [87:94]  7D   ← F, G, H
```

**Implementation**: All 11 groups are fully coded (not stubs) in `Musical_Intelligence/ear/r3/groups/`. Auto-discovery loads groups dynamically. Extractor produces `(B, T, 128)` tensors clamped to [0,1].

### 2.2 What Works Well (Physical/Spectral Domain)

Groups A-E, J, K provide high-quality physical measurements:

| Group | Quality | Basis |
|-------|---------|-------|
| A: Consonance | **High** | Sethares dissonance, Helmholtz-Kang, Stumpf fusion — well-established psychoacoustic models |
| B: Energy | **High** | Amplitude, loudness, onset strength — direct spectral measurements |
| C: Timbre | **Standard** | Sharpness, warmth, tristimulus — established timbral descriptors |
| D: Change | **Standard** | Spectral flux, entropy — straightforward temporal derivatives |
| E: Interactions | **Standard** | Cross-domain products — mathematically valid combinations |
| J: Timbre Extended | **Standard** | MFCC (DCT-II), spectral contrast — industry-standard features |
| K: Modulation | **Standard** | Zwicker sharpness, fluctuation strength — psychoacoustic standards |

These 93 dimensions (A-E + J-K) are computed from well-understood DSP operations with direct physical or psychoacoustic grounding. They form a solid foundation.

### 2.3 What Falls Short (Compositional Domain)

Groups F, G, H, I (35D) attempt music-theoretic computations but achieve only approximate quality:

| Feature | Index | Documented Quality | Root Problem |
|---------|-------|-------------------|--------------|
| chroma [49:60] | F | Approximate | Mel → chroma via Gaussian blur; bins merge below 200 Hz |
| pitch_height [61] | F | Approximate | Weighted mean of mel bins, not f0 tracking |
| key_clarity [75] | H | Standard* | K-S correlation on approximate chroma; single-frame, no temporal context |
| tonnetz [76:81] | H | Standard* | Projection of approximate chroma; inherits chroma errors |
| tonal_stability [84] | H | Approximate | key_clarity × (1 - smoothed_harmonic_change); crude composite |
| syntactic_irregularity [86] | H | Approximate | KL from best diatonic template; not Lerdahl tension hierarchy |
| melodic_entropy [87] | I | Approximate | Chroma transition entropy; not IDyOM |
| harmonic_entropy [88] | I | Approximate | KL(chroma ‖ chroma_avg); not chord transition model |
| rhythmic_IC [89] | I | Standard* | Depends on onset detection accuracy + tempo estimation |
| predictive_entropy [92] | I | Standard | Running variance of mel residuals; no learned prediction model |
| tonal_ambiguity [93] | I | Standard | Entropy of softmax(key_correlations); reasonable but input-limited |

*Standard quality with known limitations inherited from upstream approximations.

---

## 3. The Compositional Gap Problem

### 3.1 The Fundamental Issue

Music theory operates at multiple hierarchical levels:

```
Level 5: Form         (AABA, sonata, rondo)     — minutes
Level 4: Section      (verse, chorus, bridge)    — 10-60 seconds
Level 3: Phrase       (antecedent-consequent)    — 2-8 seconds
Level 2: Chord/Beat   (I-V-vi-IV progression)   — 0.3-2 seconds
Level 1: Note/Onset   (individual pitches)       — 50-500 ms
Level 0: Spectral     (partials, envelope)       — per-frame (5.8 ms)
```

R³ operates exclusively at **Level 0** (spectral, per-frame). Even the "higher-level" features in Groups F-I are computed as frame-level statistics:

- `key_clarity` = single-frame correlation with key templates (Level 0 computation pretending to be Level 2-3)
- `melodic_entropy` = running EMA of pitch-class transitions (Level 0-1 approximation of Level 3-4 patterns)
- `syncopation_index` = onset peaks relative to autocorrelation-derived metrical grid (Level 1 approximation of Level 2-3 metrical hierarchy)

The gap: **No explicit representation of Level 2-5 structure exists in R³.** The H³ temporal morphology layer partially addresses this by computing temporal statistics over R³ features, but H³ operates on approximate inputs and cannot recover information that R³ never extracted.

### 3.2 The Chroma Bottleneck

Almost all compositional features flow through the chroma representation (Group F, indices 49-60). The current chroma is derived from mel spectrograms:

```python
# Current: mel → chroma via 128×12 Gaussian soft-assignment
chroma_matrix[mel_bin, pc] = exp(-0.5 * (mel_freq - pc_freq)^2 / sigma^2)
chroma = mel @ chroma_matrix  # (B, 128, T) @ (128, 12) → (B, 12, T)
```

**Problems:**
1. **Low-frequency blurring**: Below ~200 Hz (mel bins 0-15), mel bins span > 1 semitone, causing pitch-class blurring. A C2 (65 Hz) and C#2 (69 Hz) may map to the same mel bin.
2. **Harmonic interference**: Mel spectrograms do not separate fundamentals from harmonics. A strong C3 fundamental contributes energy to C3, C4, G4, C5, E5 chroma bins simultaneously.
3. **No temporal resolution**: Each chroma frame is computed from a single mel frame (~5.8 ms / 23 ms STFT window). True pitch perception integrates over 50-200 ms.
4. **No polyphonic separation**: Cannot distinguish a C major chord (C+E+G sounding simultaneously) from a sequence C→E→G within the same STFT window.

**Impact cascade**: Every downstream feature in H and I inherits these errors. `key_clarity` correlates noisy chroma against key templates. `tonnetz` projects noisy chroma into tonal space. `melodic_entropy` tracks transitions between noisy pitch classes.

### 3.3 The Information Approximation Chain

Group I features are "information about information" — they measure predictability, surprise, and entropy of musical events. The current implementation approximates these via frame-level running statistics:

```
True IDyOM melodic IC:    P(note | corpus + context) via variable-order Markov model
Current melodic_entropy:  H(transition_counts[prev_pc, :]) via EMA

True harmonic surprise:   P(chord | key + previous_chords) via syntax model
Current harmonic_entropy: KL(chroma_t || chroma_avg) via running EMA

True rhythmic IC:         P(IOI | metric_context) via rhythmic model
Current rhythmic_IC:      -log(IOI_hist[current_IOI]) via running histogram
```

Each approximation loses:
- **Long-range context**: EMA has ~2s effective memory; musical structure spans 8-60 seconds
- **Multiple viewpoints**: IDyOM uses pitch, interval, contour, scale degree simultaneously; we use only pitch class
- **Learned regularities**: IDyOM trains on a corpus; we use uniform priors with EMA adaptation
- **Hierarchical structure**: Real musical expectation depends on phrase position, form, and genre; we use only local statistics

### 3.4 The Rhythm Approximation

Group G uses onset autocorrelation for tempo estimation — a reasonable approach, but limited compared to state-of-the-art beat tracking:

| Aspect | Current (Autocorrelation) | State-of-the-art (DBN / Deep) |
|--------|--------------------------|-------------------------------|
| Tempo estimation accuracy | ~70% (Ballroom dataset) | ~95% (madmom DBN) |
| Beat position accuracy | Frame-level only | Sub-frame (interpolated) |
| Meter detection | Nested subdivision heuristic | Learned metrical hierarchy |
| Downbeat detection | Not implemented | DBN with bar-level tracking |
| Tempo change tracking | Sliding window argmax | Online Bayesian filtering |

The 25% accuracy gap in tempo estimation propagates to all downstream rhythm features: beat_strength, pulse_clarity, syncopation_index, metricality_index, groove_index.

---

## 4. Gap Analysis by Domain

### 4.1 Tonal Domain (Groups F + H): 28D

**Current strengths:**
- Chroma → tonnetz projection is mathematically correct (Harte 2006)
- Krumhansl-Kessler key profiles are the standard reference
- Harmonic change via cosine similarity is well-motivated

**Critical gaps:**

| Gap | Current | Needed | Impact |
|-----|---------|--------|--------|
| **Chroma quality** | Mel Gaussian blur (σ=0.5st) | CQT-based HPCP or f0-informed chroma | All H and I features affected |
| **Key tracking over time** | Single-frame K-S correlation | Sliding-window key tracking with hysteresis | tonal_stability, modulation detection |
| **Chord recognition** | Not implemented | Template or learned chord labels | syntactic_irregularity, harmonic syntax |
| **Tonal tension** | Not implemented | Farbood parametric model or Lerdahl hierarchy | Emotional/cognitive models in NDU, RPU |
| **DFT of chroma** | Not implemented | Fourier coefficients on Z₁₂ (Amiot/Yust) | Direct interval-class and key information |
| **Spiral Array position** | Not implemented | 3D helix position (Chew 2000) | Tonal distance, modulation paths |
| **Voice leading quality** | L1 chroma distance | Proper voice-leading computation | voice_leading_distance accuracy |

**Missing dimensions (candidates for expansion):**
- `chroma_dft_magnitudes` (6D): Fourier coefficients |f1|-|f6| encoding interval-class distribution
- `chroma_dft_f5_phase` (1D): Direct key identification from f5 angle
- `tonal_centroid_norm` (1D): Distance from tonal center = tonal clarity
- `spiral_array_ce` (3D): Center of Effect in Chew's spiral space
- `chord_template_activations` (12-25D): Major/minor/dim/aug template correlations
- `tonal_tension_farbood` (1D): Parametric tension from multiple cues

### 4.2 Temporal Domain (Group G): 10D

**Current strengths:**
- Wiener-Khinchin autocorrelation is efficient and principled
- LHL syncopation model has theoretical basis
- Groove composite (sync × bass × clarity) matches literature

**Critical gaps:**

| Gap | Current | Needed | Impact |
|-----|---------|--------|--------|
| **Beat tracking accuracy** | Autocorrelation argmax (~70%) | DBN or deep beat tracker (95%) | All G features |
| **Downbeat/bar detection** | Not implemented | Metrical hierarchy tracking | syncopation_index, metricality |
| **Tempo change tracking** | Sliding window argmax | Bayesian online tempo tracker | tempo_stability, musical form |
| **Microtiming** | Not implemented | Deviation from grid quantization | Groove, swing, expressive timing |
| **Phrase segmentation** | Not implemented | Novelty detection on SSM or learned boundaries | Form-level structure |

**Missing dimensions (candidates):**
- `downbeat_strength` (1D): Confidence in bar-level metrical position
- `swing_ratio` (1D): Degree of swing/shuffle in timing
- `phrase_boundary_likelihood` (1D): Probability of being at a phrase boundary
- `tempo_change_rate` (1D): Rate of tempo acceleration/deceleration

### 4.3 Information Domain (Group I): 7D

**Current strengths:**
- Frame-level KL divergence and entropy are computationally valid
- EMA running statistics adapt to piece-specific distributions
- Warm-up ramp prevents cold-start artifacts

**Critical gaps:**

| Gap | Current | Needed | Impact |
|-----|---------|--------|--------|
| **Melodic prediction model** | Chroma transition entropy | IDyOM-lite (trained Markov on corpus) | melodic_entropy quality |
| **Harmonic prediction model** | KL(chroma ‖ avg) | Chord transition probabilities | harmonic_entropy quality |
| **Long-range context** | EMA τ=2s | Multi-scale memory (2s, 8s, 30s) | All I features |
| **Multiple viewpoints** | Pitch class only | + interval, contour, scale degree | melodic_entropy richness |
| **Corpus-learned priors** | Uniform priors (EMA adaptation) | Pre-trained distributions | Absolute vs. relative surprise |
| **Hierarchical prediction** | Flat prediction | Multi-level (note, phrase, section) | predictive_entropy depth |

**Missing dimensions (candidates):**
- `chord_transition_surprisal` (1D): -log P(chord_t | chord_{t-1}, key) from trained model
- `melodic_contour_ic` (1D): Information content of pitch contour (up/down/same)
- `multi_scale_surprise` (3D): Surprise at beat, phrase, and section timescales
- `prediction_error_precision` (1D): Precision-weighted prediction error (Friston)

### 4.4 Cross-Domain Gaps

| Gap | Groups Affected | Description |
|-----|----------------|-------------|
| **No form-level features** | All | No representation of verse/chorus/bridge structure |
| **No cadence detection** | H, I | No harmonic closure / phrase ending signal |
| **No tension model** | H, I | No integrated tension/relaxation trajectory |
| **No expressive timing** | G | No rubato, acceleration, ritardando |
| **No polyphonic texture** | F, H | Cannot separate voices/instruments from mel |

---

## 5. C³ Model Dependency Analysis

### 5.1 Feature Adoption Across 96 Models

The C³ models' R³ v2 dependencies reveal which features are most critical:

```
Group I (Information):    41 models (42.7%)  ████████████████████▌
Group G (Rhythm):         36 models (37.5%)  ██████████████████▊
Group F (Pitch):          19 models (19.8%)  █████████▉
Group H (Harmony):        16 models (16.7%)  ████████▍
```

### 5.2 Top 10 Most-Referenced R³ v2 Features

| Rank | Feature | Index | Group | Models | Primary Units |
|------|---------|-------|-------|--------|---------------|
| 1 | **melodic_entropy** | [87] | I | 35+ | PCU, RPU, STU, SPU, MPU |
| 2 | **harmonic_entropy** | [88] | I | 25+ | PCU, RPU, NDU, ARU |
| 3 | **predictive_entropy** | [92] | I | 20+ | RPU, NDU, PCU, ARU |
| 4 | **beat_strength** | [66] | G | 18+ | STU, MPU, ASU |
| 5 | **tempo_estimate** | [65] | G | 16+ | MPU, STU, ASU |
| 6 | **syncopation_index** | [68] | G | 14+ | STU, MPU, IMU |
| 7 | **key_clarity** | [75] | H | 12+ | PCU, NDU, ARU |
| 8 | **tonal_stability** | [84] | H | 10+ | NDU, RPU, ARU |
| 9 | **harmonic_change** | [83] | H | 8+ | PCU, RPU, NDU |
| 10 | **chroma** | [49:60] | F | 12+ | SPU, IMU, PCU |

### 5.3 Unit-Specific Dependency Patterns

| Unit | Models | Primary Groups | Key Features | Sensitivity to Gap |
|------|--------|---------------|--------------|-------------------|
| **PCU** (Predictive Coding) | 10 | I, H, F | melodic/harmonic/predictive entropy | **CRITICAL** — PCU's core function is prediction; garbage-in from I group = garbage-out |
| **RPU** (Reward Processing) | 10 | I, G, H | melodic_entropy, harmonic_entropy, spectral_surprise | **HIGH** — reward computation depends on accurate surprise signals |
| **NDU** (Neuromodulation) | 8 | I, H | predictive_entropy, tonal_ambiguity | **HIGH** — neuromodulator dynamics driven by prediction error |
| **STU** (Structural Timing) | 20 | I, G | melodic_entropy, beat_strength, syncopation | **HIGH** — timing models need accurate rhythm features |
| **MPU** (Motor Planning) | 11 | I, G | tempo_estimate, beat_strength, groove | **MEDIUM** — motor entrainment needs reliable beat/tempo |
| **ARU** (Arousal) | 9 | I, H, G | predictive_entropy, harmonic_entropy | **MEDIUM** — arousal modulated by surprise and tension |
| **IMU** (Integrative Memory) | 10 | I, G, F | melodic_entropy, chroma | **MEDIUM** — memory encoding depends on feature accuracy |
| **SPU** (Sensory Processing) | 9 | I, F, H | melodic_entropy, chroma | **LOW-MEDIUM** — sensory processing more tolerant of noise |
| **ASU** (Auditory Scene) | 9 | I, G | melodic_entropy, beat_strength | **LOW-MEDIUM** — scene analysis has other strong inputs |

### 5.4 Implication

**Improving Group I features has the highest downstream impact** — 41 models (42.7%) directly consume these features. The predictive coding units (PCU, NDU, RPU) are most sensitive because their core computation (prediction error, surprise, reward) depends on the accuracy of information-theoretic inputs.

Improving Group G features has the second-highest impact, particularly for STU (20 models, the largest unit) and MPU (11 models, motor planning).

---

## 6. H³ Temporal Demand Implications

### 6.1 H³ Architecture Summary

H³ transforms R³ features into temporal morphology via 4-tuples `(r3_idx, horizon, morph, law)`:

- **128 R³ indices** × **32 horizons** (5.8 ms → 981 s) × **24 morphs** (mean, velocity, entropy, ...) × **3 laws** (past/future/bidirectional) = **294,912 theoretical space**
- Only **~8,600 tuples** (~2.9%) are actually computed per run (demand-driven)

### 6.2 How Compositional Features Drive H³ Demands

The R³ v2 expansion from 49D→128D adds ~2,800 new H³ tuples:

| New Group | Estimated Tuples | Key H³ Patterns |
|-----------|-----------------|-----------------|
| F (Pitch) | ~800-1200 | Chroma evolves at chord (H6-H9), phrase (H12-H16), section (H18) scales |
| G (Rhythm) | ~400-600 | "Temporal-of-temporal": rhythm features are already temporal; H³ creates 2nd-order |
| H (Harmony) | ~500-800 | Key trajectory at phrase-section scales; tonnetz drift for modulation |
| I (Information) | ~300-500 | Meta-predictions: "how will prediction uncertainty trend?" |
| J, K | ~400-500 | Lower priority; timbre and modulation rate stability |

### 6.3 Critical H³ Horizons for Compositional Features

```
H6  (200 ms)  — Auditory scene analysis; chord-level chroma stability
H9  (340 ms)  — Beat period (Meso); rhythm feature onset
H12 (525 ms)  — Universal horizon: ALL 7 I features demanded here
H16 (1.0 s)   — Auditory working memory; structural boundary
H18 (2.0 s)   — Core macro: section-level tonal trajectory
H22 (8.5 s)   — Phrase grouping; melodic arc
H26 (36 s)    — Movement-level form; key area alternation
```

### 6.4 The Temporal-of-Temporal Problem

Group G features (rhythm) are themselves derived from multi-onset windows (~1-2 seconds of onset history). H³ computing morphs over G features creates second-order temporal representation:

| Level | Question | Example |
|-------|----------|---------|
| **R³ (raw)** | What is the rhythm NOW? | tempo = 120 BPM, groove = high |
| **H³ on G** | How does rhythm CHANGE? | tempo accelerates 120→140 over 16 bars; groove intensifies |

This is architecturally elegant but introduces minimum-horizon constraints: H³ morphs on G features are only meaningful at H9+ (because G features already integrate ~344 frames). The formal minimum-window analysis for "temporal features that are themselves temporal" is not yet documented.

### 6.5 Warm-Up Interactions

Group I features use a 344-frame (~2.0s) EMA warm-up ramp. H³ morphs computed over the warm-up period receive attenuated inputs:

- **Micro horizons (H0-H7)**: Largely within warm-up → H³ values may be unreliable
- **Meso+ horizons (H9+)**: Windows extend beyond warm-up → H³ values mostly stable

This interaction is one reason I group demand concentrates at Meso-Macro horizons rather than Micro.

### 6.6 Implication for Enhancement

Any R³ enhancement must consider H³ downstream:
1. **New features need morph compatibility**: Output must be continuous, [0,1] normalized, differentiable
2. **Warm-up periods must be declared**: H³ needs to know when features stabilize
3. **Temporal resolution matters**: Features computed at lower rates (e.g., 43 Hz deep models) need explicit H³ handling
4. **New dependencies may require DAG restructuring**: If a Tier 2/3 feature depends on a new slow computation, the 3-stage DAG may need a 4th stage

---

## 7. Solution Taxonomy: Bridge Features

Based on comprehensive literature survey and feasibility analysis at 172.27 Hz (5.8 ms frame budget).

### 7.1 Tier 1: Quick Wins (< 0.1 ms, immediate implementation)

These can be computed from existing chroma at negligible cost:

| Feature | Dims | Method | Cost | Theory Basis |
|---------|------|--------|------|-------------|
| **DFT of chroma (magnitudes)** | 6 | FFT on Z₁₂ | ~0.01 ms | Amiot 2016, Yust 2015 |
| **DFT of chroma (f5 phase)** | 1 | Phase angle of 5th coefficient | ~0.001 ms | Direct key identification |
| **Tonal centroid norm** | 1 | ‖tonnetz‖ | ~0.001 ms | Harte 2006 |
| **Key correlation spread** | 1 | max_corr / second_best_corr | ~0.001 ms | Key confidence |
| **Spiral Array CE** | 3 | Weighted average in 3D helix | ~0.01 ms | Chew 2000 |
| **Interval-class content** | 6 | Chroma autocorrelation | ~0.01 ms | Forte / pitch-class set theory |
| **Tonal dissonance (pc-space)** | 1 | Weighted chroma products at dissonant intervals | ~0.005 ms | Harmonic tension in pc space |
| **Onset density (smoothed)** | 1 | Onset envelope integral over sliding window | ~0.005 ms | Event rate |

**Total: ~20 new dimensions at < 0.1 ms combined**

#### Why DFT of Chroma is the Single Highest-Value Addition

The Discrete Fourier Transform of the 12D chroma vector (treating it as a function on Z₁₂) yields 7 complex coefficients (6 magnitudes + 1 real DC), each with direct music-theoretic meaning:

```
|f1|: Chromatic clustering → unison/semitone prominence
|f2|: Whole-tone content → Debussy, augmented sonorities
|f3|: Minor-third / diminished content → dim7 chords, octatonic
|f4|: Major-third content → augmented triads, hexatonic
|f5|: Diatonic clustering → KEY STRENGTH (strongest for diatonic music)
|f6|: Tritone content → dominant function, tension
Phase(f5): KEY IDENTIFICATION → the angle directly encodes the key!
```

This is "the most theoretically elegant bridge between spectral analysis and music theory" (Amiot 2016). The computation is a 12-point DFT — six complex multiplies, essentially free on GPU. Yet it provides:
- Direct key identification without template matching
- Interval-class distribution without combinatorial analysis
- Scale-type classification (diatonic, whole-tone, chromatic, octatonic)
- A principled basis for tonal distance (Yust 2015)

### 7.2 Tier 2: Medium Effort (0.1-2 ms, targeted implementation)

These require additional computation or small models:

| Feature | Dims | Method | Cost | Theory Basis |
|---------|------|--------|------|-------------|
| **Farbood tension model** | 1 | Weighted combination of Tier 1 features | ~0.1 ms | Farbood 2012 |
| **IDyOM-lite surprisal** | 2-3 | Trained 12×12 transition matrix, multi-viewpoint | ~0.05 ms | Pearce 2005 (simplified) |
| **Chord template activations** | 12-25 | Template matching on normalized chroma | ~0.2 ms | Major/minor/dim/aug templates |
| **Chord transition surprisal** | 1 | -log P(chord_t \| chord_{t-1}) from pre-trained table | ~0.05 ms | Rohrmeier & Graepel 2012 |
| **Novelty/boundary detection** | 1 | Checkerboard kernel on sliding SSM | ~0.5 ms | Foote 2000, McFee 2014 |
| **RNN-based predictive coding** | 8-32 | Small GRU on R³ features | ~0.5-1 ms | Friston 2010 (free-energy principle) |
| **Multi-scale surprise** | 3 | EMA at τ=2s, 8s, 30s | ~0.03 ms | Hierarchical temporal receptive fields |
| **Key tracking with hysteresis** | 2 | Smoothed K-S + modulation detection | ~0.05 ms | Toiviainen & Krumhansl 2003 |

**Total: ~25-60 new dimensions at ~1.5-3 ms combined**

#### Farbood Tension Model

Farbood (2012) proposes a parametric model of musical tension based on:
1. **Melodic expectation** (pitch proximity, reversal) — computable from chroma velocity
2. **Harmonic change** (already in R³ as [83])
3. **Onset density** (already in R³ as [72] event_density)
4. **Dynamics** (already in R³ as [7-9] amplitude/velocity/acceleration)
5. **Rhythmic regularity** (already in R³ as [74])
6. **Register** (already in R³ as [61] pitch_height)

Most inputs already exist in R³. The tension model is essentially a weighted sum with time-decaying memory:

```python
tension_t = sum(w_i * feature_i_t) + decay * tension_{t-1}
```

Weights from Farbood 2012: onset_density > dynamics > harmonic_change > melodic_expectation.

This could be added as a single new R³ feature or computed in a post-processing layer.

#### IDyOM-Lite

Instead of the full IDyOM system (Common Lisp, symbolic input, multiple viewpoints), implement a simplified version:

1. **Pre-train** a 12×12 pitch-class transition matrix on a large MIDI corpus (e.g., Lakh MIDI dataset, ~176K tracks)
2. **At runtime**: IC = -log₂(P(pc_t | pc_{t-1})) using the pre-trained matrix
3. **Add viewpoints**: interval (12×12 interval transition), contour (3×3 up/down/same transition), scale degree (7×7 in-key transitions)
4. **Short-term adaptation**: Blend corpus prior with piece-specific EMA, e.g., P_combined = 0.7 × P_corpus + 0.3 × P_piece

This is a significant improvement over the current chroma-transition entropy, which uses uniform priors and a single pitch-class viewpoint.

### 7.3 Tier 3: Long-Term (5-50 ms, subsampled at 20-43 Hz)

These require deep models and run at lower temporal resolution:

| Feature | Dims | Method | Cost | Theory Basis |
|---------|------|--------|------|-------------|
| **Deep chord recognition** | 25-170 | BTC Transformer on CQT | ~5-10 ms @43Hz | Won et al. 2021 |
| **MERT embeddings** | 768→32 (PCA) | MERT-25M forward pass | ~10-20 ms @43Hz | Li et al. 2023 |
| **Polyphonic transcription** | variable | Basic Pitch (Spotify) | ~20-50 ms @43Hz | Bittner et al. 2022 |
| **Structure segmentation** | variable | CNN boundary detector | ~10-20 ms @43Hz | Kim et al. 2023 |
| **CQT-based chroma** | 12 | CQT → fold to 12 bins | ~2-5 ms @172Hz | Superior to mel-based chroma |

**Integration strategy for Tier 3:**
Run at native rate (20-43 Hz), maintain a state buffer, and upsample/repeat to 172 Hz. The latency is 25-50 ms, below the ~100 ms perceptual threshold for harmonic change.

#### MERT Integration

MERT (Music Understanding Model, Li et al. 2023) provides 768D embeddings that encode key, chord, beat, pitch, and instrument information. Strategy:

1. Run MERT-25M at 43 Hz (every 4th R³ frame) → 768D raw embeddings
2. PCA to 32D (retaining ~85% variance based on MIR literature)
3. Upsample to 172 Hz via linear interpolation
4. Fuse with R³ via concatenation or gating

This adds a "learned compositional representation" branch that complements the handcrafted R³ features. The PCA dimensions would encode implicit key, chord, meter, and texture information that R³ cannot extract from mel alone.

---

## 8. Implementation Roadmap

### Phase 5A: Tier 1 Quick Wins (Estimated: 1-2 weeks)

**Goal**: Add ~20 highest-value dimensions at negligible computational cost.

| Step | Action | Impact |
|------|--------|--------|
| 1 | Add `chroma_dft` computation to Group F or new Group L | 7D of pure music theory at ~0.01 ms |
| 2 | Add `tonal_centroid_norm` to Group H | 1D key clarity metric |
| 3 | Add `key_correlation_spread` to Group H | 1D key confidence |
| 4 | Add `spiral_array_ce` to Group H | 3D tonal position |
| 5 | Add `interval_class_content` to Group F | 6D pitch-class set theory |
| 6 | Update R3_DIM from 128 to ~148 | Propagate through H³, C³ |
| 7 | Run Swan Lake validation | Verify end-to-end pipeline |
| 8 | Update C³ model docs with new feature bindings | Section 4.2 in each model |

**Decision point**: Where do new features live?
- **Option A**: Expand existing groups (F gets DFT, H gets spiral array)
- **Option B**: New Group L: "Tonal Theory" [128:148] — clean separation
- **Recommendation**: Option B for clean modularity, but requires DAG update

### Phase 5B: Tier 2 Medium Effort (Estimated: 3-6 weeks)

**Goal**: Add ~30 dimensions requiring trained models or composite features.

| Step | Action | Impact |
|------|--------|--------|
| 1 | Train IDyOM-lite transition matrices on Lakh MIDI | Corpus-informed priors |
| 2 | Implement Farbood tension model | 1D integrated tension |
| 3 | Add chord template activations | 12-25D chord recognition |
| 4 | Implement novelty detection (checkerboard on SSM) | 1D phrase boundary |
| 5 | Add multi-scale surprise (3 EMA timescales) | 3D hierarchical surprise |
| 6 | Add key tracking with hysteresis | 2D modulation detection |
| 7 | Update R3_DIM to ~178 | Full Tier 2 integration |
| 8 | Comprehensive validation suite | Quality metrics per feature |

**Risk**: Tier 2 features add ~1.5-3 ms to per-frame budget. Current timing: Cochlea 1.7s, R³ 1.2s for 5168 frames → ~0.23 ms/frame average. Budget has headroom.

### Phase 6: Tier 3 Deep Integration (Estimated: 2-3 months)

**Goal**: Add deep-learned branch at reduced temporal resolution.

| Step | Action | Impact |
|------|--------|--------|
| 1 | Integrate MERT-25M as optional branch | 32D learned representations |
| 2 | Build CQT-based chroma pipeline | Superior chroma quality |
| 3 | Add BTC chord recognition at 43 Hz | Explicit chord labels |
| 4 | Implement upsample/fusion layer | Multi-rate integration |
| 5 | Design H³ handling for subsampled features | Temporal demand alignment |
| 6 | Performance optimization (ONNX, TensorRT) | GPU efficiency |

**Decision point**: Should Tier 3 features replace or augment existing Tier 0 features?
- **Replace**: `cqt_chroma` replaces mel-based `chroma`; all downstream features improve
- **Augment**: Both representations coexist; C³ models can use either
- **Recommendation**: Augment initially, replace after validation

### Phase 7: C³ Model Adaptation (Estimated: ongoing)

Update C³ models to leverage new R³ features:
1. Update Section 4.2 (R³ v2 expansion) in all 96 model docs
2. Update R³ input mappings for new indices
3. Rebuild H³ demand profiles for new features
4. Retrain/recalibrate C³ models with expanded inputs

---

## 9. Known Code Issues

### 9.1 Active Bugs

| Issue | Group | Location | Severity | Description |
|-------|-------|----------|----------|-------------|
| **C-A duplication** | C | `c_timbre/group.py` | Medium | `warmth` = `stumpf_fusion`, `spectral_smoothness` = `1-sethares`, `spectral_autocorrelation` = `helmholtz_kang` — 3 of 9 timbre features are duplicates of Group A |
| **D concentration bug** | D | `d_change/group.py:41-44` | Medium | `distribution_concentration` maps both uniform and concentrated distributions to 1.0 — incorrect normalization |
| **E proxy fallback** | E | `e_interactions/group.py:37` | Low | Fallback uses `helmholtz_proxy = tonalness` instead of true autocorrelation when dependencies unavailable |

### 9.2 Architectural Concerns

| Concern | Description | Impact |
|---------|-------------|--------|
| **Chroma quality ceiling** | All F/H/I features limited by mel→chroma quality | All compositional features |
| **Single-frame key estimation** | No temporal smoothing in key_clarity | Noisy key trajectory |
| **EMA-only memory** | All running statistics use single timescale (τ=2s) | No multi-scale context |
| **No learned components** | Entire R³ is handcrafted; no adaptation to genre/style | Limited generalization |
| **Group E oversize** | 24D for cross-domain interactions may be redundant | Dimensionality budget |

### 9.3 Known Doc-Code Discrepancies (Deferred to Phase 5)

These are documented in the C³ model upgrade workflow and gap logs:
- All ASU models: `MECHANISM_NAMES = ("ASA",)` in code vs `("BEP","ASA")` in docs
- All ASU models: `h3_demand = ()` empty in code vs populated in docs
- All gamma models: `OUTPUT_DIM = 10` in code vs 9 in docs
- R³ naming discrepancy: docs use semantic labels, code uses computational names (6 known mismatches)

---

## 10. Risk Assessment

### 10.1 Dimensionality Expansion Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **R³ DIM increase breaks downstream** | High | High | Version gate: R3_DIM_V2 = 128 (legacy), R3_DIM_V3 = 148+ (new) |
| **H³ tuple explosion** | Medium | Medium | Demand-driven computation limits actual tuples |
| **C³ model retraining cost** | Medium | Medium | Add new features as optional inputs initially |
| **Performance regression** | Low | High | Tier 1 adds < 0.1 ms; Tier 2 within budget |

### 10.2 Quality Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **CQT chroma doesn't improve enough** | Medium | Medium | Benchmark on annotated datasets before integration |
| **IDyOM-lite corpus bias** | Medium | Low | Blend corpus + piece-specific priors |
| **MERT embeddings opaque** | High | Low | PCA + probing for interpretability |
| **Farbood weights genre-dependent** | Medium | Low | Calibrate on diverse dataset; consider adaptive weights |

### 10.3 Backward Compatibility

Any R³ expansion must maintain:
1. **Indices 0-127 unchanged** — existing C³ model bindings remain valid
2. **Output range [0,1]** — all new features normalized consistently
3. **H³ warm-up protocol** — new features declare warm-up frame count
4. **Stage-DAG compatibility** — new features fit into existing 3-stage pipeline or extend to 4 stages

---

## 11. Open Questions

### Architectural Questions

1. **Should new features extend R³ beyond 128D or replace low-value existing features?**
   - Group E (24D interactions) may be partially redundant with expanded tonal/rhythm features
   - Group C has 3 duplicated features that could be replaced

2. **Should Tier 3 (deep models) be part of R³ or a separate layer (R⁴)?**
   - R³ is defined as handcrafted spectral features
   - Learned representations may deserve their own layer with different contracts

3. **How should multi-rate features integrate with the pipeline?**
   - 172 Hz handcrafted + 43 Hz deep: interpolation, repetition, or attention-based fusion?

4. **What is the right dimensionality budget?**
   - Current: 128D. Tier 1: +20 = 148D. Tier 2: +30 = 178D. Tier 3: +32 = 210D.
   - At what point does dimensionality expansion hurt more than help?

### Research Questions

5. **Can DFT-of-chroma replace multiple existing Group H features?**
   - |f5| may subsume key_clarity. Phase(f5) may subsume key estimation. |f1|-|f6| may subsume tonnetz.
   - Empirical comparison needed.

6. **What corpus should IDyOM-lite be trained on?**
   - Lakh MIDI (176K tracks, Western pop/rock/classical) vs. domain-specific corpora
   - Cross-genre generalization vs. genre-specific models

7. **How sensitive are C³ models to R³ feature quality?**
   - Are models robust to noisy chroma, or does quality improvement yield proportional gains?
   - Ablation study needed: original chroma vs. CQT chroma → C³ output comparison

8. **Is Group E worth its 24D budget?**
   - Cross-domain interactions (energy×consonance, etc.) are simple products
   - Could the 24D be better spent on music-theoretic features?

### Validation Questions

9. **What ground-truth datasets exist for compositional features?**
   - Key: GiantSteps-Key, MIREX key detection
   - Chord: Isophonics, Billboard
   - Beat: MIREX beat tracking, Ballroom
   - Structure: SALAMI, Isophonics

10. **How should "quality improvement" be measured?**
    - Direct feature quality: correlation with annotations
    - Downstream impact: C³ model output quality with old vs. new R³
    - End-to-end: HYBRID transformation quality with improved features

---

## 12. References

### Tonal Analysis & Key Detection
- Krumhansl, C. E. (1990). *Cognitive Foundations of Musical Pitch*. Oxford University Press.
- Krumhansl, C. E. & Kessler, E. J. (1982). "Tracing the Dynamic Changes in Perceived Tonal Organization in a Spatial Representation of Musical Keys." Psychological Review 89(4), 334-368.
- Temperley, D. (2001). *The Cognition of Basic Musical Structures*. MIT Press.
- Korzeniowski, F. & Widmer, G. (2018). "End-to-end Musical Key Estimation Using a CNN." EUSIPCO.
- Toiviainen, P. & Krumhansl, C. L. (2003). "Measuring and Modeling Real-Time Responses to Music." Music Perception 21(2), 187-223.

### Tonal Geometry & Spaces
- Harte, C., Sandler, M. & Gasser, M. (2006). "Detecting Harmonic Change in Musical Audio." ACM MM.
- Chew, E. (2000-2014). *Mathematical and Computational Modeling of Tonality: Theory and Applications*. Springer.
- Tymoczko, D. (2006). "The Geometry of Musical Chords." Science 313(5783), 72-74.
- Tymoczko, D. (2011). *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*. Oxford University Press.
- Amiot, E. (2016). *Music Through Fourier Space: Discrete Fourier Transform in Music Theory*. Springer.
- Yust, J. (2015). "Schubert's Harmonic Language and Fourier Phase Space." Journal of Music Theory 59(1), 121-181.

### Chord Recognition
- Won, M., Kim, J. & Nam, J. (2021). "Bi-Directional Transformer for Music Chord Recognition." ISMIR.
- McFee, B. & Bello, J. P. (2017). "Structured Training for Large-Vocabulary Chord Recognition." ISMIR.

### Tension & Hierarchy
- Lerdahl, F. & Jackendoff, R. (1983). *A Generative Theory of Tonal Music*. MIT Press.
- Lerdahl, F. & Krumhansl, C. L. (2007). "Modeling Tonal Tension." Music Perception 24(4), 329-366.
- Farbood, M. M. (2012). "A Parametric, Temporal Model of Musical Tension." Music Perception 29(4), 387-428.
- Herremans, D. & Chew, E. (2017). "Tension Ribbons: Quantifying and Visualising Tonal Tension." 2nd Conf. on Technologies for Music Notation and Representation.
- Hamanaka, M., Hirata, K. & Tojo, S. (2006). "Implementing 'A Generative Theory of Tonal Music'." Journal of New Music Research 35(4), 249-277.
- Rohrmeier, M. & Graepel, T. (2012). "Comparing Feature-Based Models of Harmony." 9th International Symposium on Computer Music Modelling and Retrieval.

### Information Dynamics
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal 27, 379-423.
- Pearce, M. T. (2005). *The Construction and Evaluation of Statistical Models of Melodic Structure in Music Perception and Composition*. PhD thesis, City University London.
- Pearce, M. T. (2018). "Statistical Learning and Probabilistic Prediction in Music Cognition." Annals of the New York Academy of Sciences 1423(1), 378-395.
- Hansen, N. C. & Pearce, M. T. (2014). "Predictive Uncertainty in Auditory Sequence Processing." Frontiers in Psychology 5, 1052.
- Cheung, V. K. M. et al. (2019). "Uncertainty and Surprise Jointly Predict Musical Pleasure and Amygdala, Hippocampus, and Auditory Cortex Activity." Current Biology 29(23), 4084-4092.
- Gold, B. P. et al. (2019). "Musical Reward Prediction Errors Engage the Nucleus Accumbens and Motivate Learning." PNAS 116(8), 3310-3315.
- Friston, K. (2010). "The Free-Energy Principle: A Unified Brain Theory?" Nature Reviews Neuroscience 11(2), 127-138.
- Skerritt-Davis, B. & Elhilali, M. (2018). "Temporal Coherence, Attention, and Auditory Scene Analysis." Trends in Neurosciences 41(4), 214-225.

### Rhythm & Beat Tracking
- Fraisse, P. (1982). "Rhythm and Tempo." In *The Psychology of Music*, 1st ed. (Deutsch, ed.). Academic Press.
- Longuet-Higgins, H. C. & Lee, C. S. (1984). "The Rhythmic Interpretation of Monophonic Music." Music Perception 1(4), 424-441.
- Witek, M. A. G. et al. (2014). "Effects of Polyphonic Context, Instrumentation, and Metrical Structure on Syncopation in Music." Music Perception 32(2), 201-217.
- Madison, G. (2006). "Experiencing Groove Induced by Music." Music Perception 24(2), 201-208.
- Janata, P. et al. (2012). "Sensorimotor Coupling in Music and the Psychology of the Groove." J. Exp. Psych: General 141(1), 54-75.
- Spiech, C. et al. (2022). "Rhythmic Information Content and Neural Synchronization." Cognition 226, 105180.

### Deep Learning & Foundation Models
- Li, Y. et al. (2023). "MERT: Acoustic Music Understanding Model with Large-Scale Self-Supervised Training." ICLR.
- Won, M. et al. (2020). "Data-Driven Harmonic Filters for Audio Representation Learning." ICASSP.
- Spijkervet, J. & Burgoyne, J. A. (2021). "Contrastive Learning of Musical Representations." ISMIR.
- Copet, J. et al. (2023). "Simple and Controllable Music Generation." NeurIPS (MusicGen).

### Spectral Analysis & Segmentation
- Foote, J. (2000). "Automatic Audio Segmentation Using a Measure of Audio Novelty." ICME.
- McFee, B. & Ellis, D. P. W. (2014). "Analyzing Song Structure with Spectral Clustering." ISMIR.
- Grill, T. & Schluter, J. (2015). "Music Boundary Detection Using Neural Networks on Spectrograms and Self-Similarity Lag Matrices." EUSIPCO.
- Kim, T. et al. (2023). "All-In-One Music Structure Analyzer." ISMIR.
- Bittner, R. M. et al. (2022). "A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation." ICASSP (Basic Pitch).

### Psychoacoustics & Perception
- Zwicker, E. & Fastl, H. (2013). *Psychoacoustics: Facts and Models*. 3rd ed. Springer.
- Grahn, J. A. & Brett, M. (2007). "Rhythm and Beat Perception in Motor Areas of the Brain." J. Cognitive Neuroscience 19(5), 893-906.
- Weineck, K. et al. (2022). "Neural Correlates of Spectral Flux." NeuroImage 261.

---

## Appendices

### A. Current R³ Feature Index (128D)

```
Group A: Consonance [0:7]
  [0]  roughness
  [1]  sethares_dissonance
  [2]  helmholtz_kang
  [3]  stumpf_fusion
  [4]  sensory_pleasantness
  [5]  inharmonicity
  [6]  harmonic_deviation

Group B: Energy [7:12]
  [7]  amplitude
  [8]  velocity_A
  [9]  acceleration_A
  [10] loudness
  [11] onset_strength

Group C: Timbre [12:21]
  [12] warmth                     ⚠ duplicate of [3]
  [13] sharpness
  [14] tonalness
  [15] clarity
  [16] spectral_smoothness        ⚠ duplicate of 1-[1]
  [17] spectral_autocorrelation   ⚠ duplicate of [2]
  [18] tristimulus1
  [19] tristimulus2
  [20] tristimulus3

Group D: Change [21:25]
  [21] spectral_flux
  [22] distribution_entropy
  [23] distribution_flatness
  [24] distribution_concentration  ⚠ normalization bug

Group E: Interactions [25:49]
  [25:33] energy × consonance (8D)
  [33:41] change × consonance (8D)
  [41:49] consonance × timbre (8D)

Group F: Pitch & Chroma [49:65]
  [49:61] chroma_0..chroma_11
  [61] pitch_height
  [62] pitch_class_entropy
  [63] pitch_salience
  [64] inharmonicity_index

Group G: Rhythm & Groove [65:75]
  [65] tempo_estimate
  [66] beat_strength
  [67] pulse_clarity
  [68] syncopation_index
  [69] metricality_index
  [70] isochrony_nPVI
  [71] groove_index
  [72] event_density
  [73] tempo_stability
  [74] rhythmic_regularity

Group H: Harmony & Tonality [75:87]
  [75] key_clarity
  [76] tonnetz_fifth_x
  [77] tonnetz_fifth_y
  [78] tonnetz_minor_x
  [79] tonnetz_minor_y
  [80] tonnetz_major_x
  [81] tonnetz_major_y
  [82] voice_leading_distance
  [83] harmonic_change
  [84] tonal_stability
  [85] diatonicity
  [86] syntactic_irregularity

Group I: Information & Surprise [87:94]
  [87] melodic_entropy
  [88] harmonic_entropy
  [89] rhythmic_information_content
  [90] spectral_surprise
  [91] information_rate
  [92] predictive_entropy
  [93] tonal_ambiguity

Group J: Timbre Extended [94:114]
  [94:107]  MFCC 1-13
  [107:114] spectral_contrast (7 octave bands)

Group K: Modulation & Psychoacoustic [114:128]
  [114:120] modulation_energy (6 rates)
  [120] modulation_centroid
  [121] modulation_bandwidth
  [122] sharpness_zwicker
  [123] fluctuation_strength
  [124] loudness_a_weighted
  [125] alpha_ratio
  [126] hammarberg_index
  [127] spectral_slope_0_500
```

### B. Proposed Tier 1 Feature Index (Expansion to ~148D)

```
Group L: Tonal Theory [128:148]  (NEW)
  [128:134] chroma_dft_mag_f1..f6    — DFT of chroma magnitudes
  [134]     chroma_dft_f5_phase       — Key angle from f5
  [135]     tonal_centroid_norm        — ‖tonnetz‖ = tonal clarity
  [136]     key_correlation_spread     — max_corr / 2nd_best
  [137:140] spiral_array_ce_x/y/z     — Chew spiral position
  [140:146] interval_class_ic1..ic6   — Chroma autocorrelation
  [146]     tonal_dissonance_pc        — Pitch-class space dissonance
  [147]     onset_density_smooth       — Smoothed event rate
```

### C. Computation Cost Budget

```
Current R³ timing (30s audio, T=5168 frames):
  Total R³: 1.2s → 0.23 ms/frame average

Frame budget at 172.27 Hz:
  Available: 5.8 ms/frame
  Current R³: 0.23 ms/frame
  Remaining: 5.57 ms/frame

Tier 1 additions: ~0.08 ms/frame  → Total: ~0.31 ms/frame  ✓
Tier 2 additions: ~1.5-3.0 ms     → Total: ~1.8-3.3 ms     ✓
Tier 3 additions: run at 43 Hz    → Total: amortized ~0.5 ms ✓
```

### D. Tier Priority by C³ Impact

```
Priority 1 (affects 41+ models):
  - Improve melodic_entropy [87] → IDyOM-lite
  - Improve harmonic_entropy [88] → chord transition model
  - Improve predictive_entropy [92] → multi-scale + learned predictor
  - Add DFT of chroma [128:134] → direct theory bridge

Priority 2 (affects 36+ models):
  - Improve tempo_estimate [65] → better beat tracking
  - Add Farbood tension → integrated tension signal
  - Add chord template activations → explicit harmony

Priority 3 (affects 16-19 models):
  - Improve chroma quality → CQT or f0-informed
  - Improve tonal_stability [84] → temporal key tracking
  - Add spiral array → tonal distance

Priority 4 (new capabilities):
  - Add phrase boundary detection → form structure
  - Add MERT embeddings → learned representations
  - Add polyphonic transcription → symbolic bridge
```

---

**End of Document**

*This document serves as the starting point for R³ enhancement planning. It should be revised as implementation progresses and new findings emerge.*
