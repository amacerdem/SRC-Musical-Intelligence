# Musical Intelligence (MI) — Technical Architecture Report

**Date:** 17 February 2026
**Version:** Kernel v1.0 (post-familiarity activation)
**Codebase:** `Musical_Intelligence/` — 194 Python files

---

## 1. Executive Summary

Musical Intelligence (MI) is a glass-box computational model of musical cognition. Unlike generative AI systems (Suno, MusicLM) that learn statistical patterns from audio corpora, MI implements an explicit cognitive architecture grounded in computational neuroscience — predictive coding, precision-weighted Bayesian inference, and salience-gated reward.

The system processes raw audio through three hierarchical layers:

```
Audio (WAV)
   │
   ▼
┌──────────────────────────────────────────────┐
│  COCHLEA — Mel Spectrogram (B, 128, T)       │
└──────────────────────┬───────────────────────┘
                       │
   ▼                   ▼
┌─────────────┐  ┌─────────────────────────────┐
│  R³ — Early │  │  Audio waveform (optional)   │
│  Perceptual │◄─┤  for psychoacoustic models   │
│  Front-End  │  └─────────────────────────────┘
│  128D / frame│
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  H³ — Multi-Scale Temporal Morphology       │
│  (r3_idx, horizon, morph, law) → (B, T)     │
│  Demand-driven sparse computation            │
└──────────────────────┬──────────────────────┘
                       │
   ┌───────────────────┼───────────────────┐
   │                   │                   │
   ▼                   ▼                   ▼
┌────────┐      ┌────────────┐      ┌──────────┐
│  BCH   │      │  Beliefs   │      │ Precision│
│  Relay │      │  (4 active)│      │  Engine  │
│  L0    │      │            │      │  (PCU)   │
└───┬────┘      └─────┬──────┘      └────┬─────┘
    │                 │                   │
    └─────────┬───────┘                   │
              │                           │
              ▼                           │
┌─────────────────────────────────────────┴────┐
│  C³ Kernel — Single-Pass Belief Cycle        │
│  Phase 0 → 1 → 2a → 2b → 2c → 3            │
│                                               │
│  Output: beliefs{5} + PE{4} + precision{4}   │
│          + reward(B,T)                        │
└──────────────────────────────────────────────┘
```

**Current state (17 Feb 2026):**
- 4 active beliefs + 1 default + BCH relay
- 8/9 diagnostic checks pass on 3-piece comparative stress test
- ~1,100 frames/sec on Apple Silicon (30s audio, T=5168)
- End-to-end pipeline: ~7 seconds for 30 seconds of audio

---

## 2. Theoretical Foundations

MI draws from three theoretical frameworks:

### 2.1 Predictive Coding (Rao & Ballard 1999, Friston 2005)
The brain continuously generates predictions about incoming sensory input. When predictions fail, **prediction error (PE)** signals propagate upward. MI implements this at the belief level: each belief predicts its own next state, observes the actual sensory input, and computes PE = observed - predicted.

### 2.2 Active Inference (Friston 2010)
Precision-weighted prediction errors drive belief updating via Bayesian fusion:
```
gain = pi_obs / (pi_obs + pi_pred)
posterior = (1 - gain) * predicted + gain * observed
```
High sensory precision (reliable observation) increases gain toward the observation. High prediction precision (confident model) reduces gain, favoring the prediction.

### 2.3 Inverted-U Reward (Berlyne 1971, Schmidhuber 2010)
Musical reward arises from the interaction of surprise and familiarity:
```
surprise   = |PE| * pi_pred * (1 - familiarity)
resolution = (1 - |PE|) * pi_pred * familiarity
reward     = salience * (surprise + resolution + exploration - monotony) * fam_mod
fam_mod    = 4 * familiarity * (1 - familiarity)   // inverted-U, peaks at 0.5
```
This captures the "Goldilocks zone" of musical engagement: too predictable is boring (monotony), too unpredictable is chaotic (no resolution), moderate surprise with familiar context is rewarding.

---

## 3. Module Architecture

### 3.1 File Count Overview

| Module | Files | Purpose |
|--------|------:|---------|
| `contracts/` | 19 | Interfaces, dataclasses, nucleus hierarchy |
| `ear/r3/` | 39 | 128D spectral feature extraction |
| `ear/h3/` | 43 | Multi-scale temporal morphology |
| `brain/` | 55 | C³ cognitive kernel, beliefs, regions, neuro |
| `hybrid/` | 14 | Emotion-driven audio transformation |
| `config/` | 9 | YAML configuration |
| `data/` | 7 | Dataset handling, preprocessing |
| `training/` | 7 | BCH training pipeline |
| `evaluation/` | 6 | Metrics, white-box analysis |
| `utils/` + `visualization/` | 2 | Stubs |
| **Total** | **194** | |

---

## 4. R³ — Early Perceptual Front-End

### 4.1 Identity
R³ is the first processing layer after cochlear mel-spectrogram extraction. It produces a dense 128-dimensional feature vector at every time frame, capturing spectral, timbral, harmonic, rhythmic, and psychoacoustic properties of the audio signal.

**Ontology:** Frozen v1.0.0
**Boundary constraints:** Frame ±2, no EMA/state, no cross-domain products, no prediction, deterministic.

### 4.2 Architecture

```
Mel (B, 128, T)  +  Audio (B, N) [optional]
         │                    │
         ▼                    ▼
┌────────────────────────────────────────┐
│  StageExecutor (3-stage DAG)           │
│                                        │
│  Stage 1: Independent groups (A-D, F)  │
│  Stage 2: Dependent groups (G, H)      │
│  Stage 3: Cross-group (J, K)           │
│                                        │
│  Groups E, I: DISSOLVED → C³/H³        │
└────────────────────┬───────────────────┘
                     │
                     ▼
         FeatureNormalizer → clamp [0, 1]
                     │
                     ▼
           R3Output (B, T, 128)
```

### 4.3 Feature Groups

| Group | Name | Indices | Dim | Key Features |
|-------|------|---------|----:|--------------|
| **A** | Consonance | [0:7] | 7 | roughness, sethares_dissonance, helmholtz_kang, sensory_pleasantness, harmonic_deviation, stumpf_fusion, consonance_signal |
| **B** | Energy | [7:12] | 5 | amplitude, velocity_A, velocity_D, RMS, spectral_centroid |
| **C** | Timbre | [12:21] | 9 | brightness_kuttruff, spectral_spread, spectral_flatness, spectral_rolloff, zero_crossing_rate, crest_factor, MFCC_1-3 |
| **D** | Change | [21:25] | 4 | spectral_flux, onset_strength, delta_RMS, delta_centroid |
| **E** | ~~Interactions~~ | [25:41] | 16 | *Dissolved to C³/H³ (kept for backward compat)* |
| **F** | Pitch/Chroma | [25:41] | 16 | F0_estimate, voicing_probability, chroma[12], pitch_salience, inharmonicity |
| **G** | Rhythm | [41:51] | 10 | tempo_estimate, beat_strength, pulse_clarity, rhythmic_regularity, onset_strength, ... |
| **H** | Harmony | [51:63] | 12 | tonalness, key_clarity, mode, tonal_stability, chord_complexity, harmonic_change, ... |
| **I** | ~~Information~~ | [63:83] | 20 | *Dissolved to C³/H³ (kept for backward compat)* |
| **J** | Timbre Extended | [63:83] | 20 | spectral_contrast[7], spectral_bandwidth, attack_time, decay_time, ... |
| **K** | Modulation | [83:97] | 14 | AM_depth, AM_rate, FM_depth, FM_rate, vibrato_extent, tremolo_rate, ... |
| | *Gap (reserved)* | [97:128] | 31 | Available for future features |

**Total active: 97D** (core) + 31D gap = 128D output.

### 4.4 Psychoacoustic Models (Group A)

When raw audio is available, Group A uses real psychoacoustic computation instead of mel-proxy heuristics:

- **Sethares 1993 Pairwise Dissonance:** Models sensory dissonance between partial pairs using parameterized exponential functions (D*=0.24, A1=-3.51, A2=-5.75)
- **Plomp-Levelt Roughness:** Critical bandwidth model (Zwicker) for roughness perception
- **HPS F0 Estimation:** Harmonic Product Spectrum for fundamental frequency extraction
- **Harmonic Template Matching:** Correlates observed spectrum with ideal harmonic series

**Impact:** Consonance spread increased from 0.6% (mel-proxy) to 45% (psychoacoustic) across musical intervals. BCH consonance hierarchy P1>P5>P4>M3>m6>TT — 6/6 correct.

---

## 5. H³ — Multi-Scale Temporal Morphology Engine

### 5.1 Identity
H³ is a stateless temporal operator that computes morphological features across multiple time horizons. It answers the question: "How does R³ feature X behave over time scale Y, looking in direction Z?"

**Ontology:** Frozen v1.0.0
**Boundary constraints:** No EMA, no state, no prediction, no cross-feature binding. Pure window operator.

### 5.2 4-Tuple Addressing

Every H³ feature is uniquely identified by a 4-tuple:

```
(r3_idx, horizon, morph, law)
   │        │       │      │
   │        │       │      └── Window direction: L0=memory, L1=forward, L2=integration
   │        │       └── Morphology: M0-M23 (24 types in 6 families)
   │        └── Time horizon: H0-H31 (32 log-spaced, 5.8ms to 981s)
   └── Source R³ feature index (0-96)
```

**Theoretical space:** 97 × 32 × 24 × 3 = 223,488 tuples
**Active (demanded):** ~8,600 tuples (full C³) or 28 tuples (kernel mode)

### 5.3 Horizon Bands

| Band | Range | Horizons | Musical Role |
|------|-------|----------|--------------|
| **Micro** | 5.8ms–46ms | H0-H7 | Attack transients, roughness fluctuation |
| **Meso** | 46ms–373ms | H8-H15 | Note-level, beat-level dynamics |
| **Macro** | 373ms–3.0s | H16-H23 | Phrase-level, structural sections |
| **Ultra** | 3.0s–981s | H24-H31 | Piece-level arc, long-term memory |

### 5.4 Morphology Families (24 Morphs)

| Family | Morphs | Examples | Purpose |
|--------|--------|----------|---------|
| **Distribution** | M0-M3 | mean, median, mode, quantile | Statistical shape within window |
| **Dynamics** | M4-M10, M18 | std, velocity(M8), trend(M18) | Temporal change patterns |
| **Rhythm** | M14-M15 | periodicity, beat_strength | Cyclic pattern detection |
| **Information** | M11-M13 | entropy, surprise, redundancy | Information-theoretic measures |
| **Symmetry** | M19-M23 | skewness, balance, ascent/descent | Temporal asymmetry patterns |

**Key morphs for C³:**
- **M2 (std):** Used for precision estimation and familiarity measurement
- **M8 (velocity):** Edge difference, horizon-independent
- **M14 (periodicity):** Cyclic pattern detection for belief prediction
- **M18 (trend):** Regression slope, horizon-dependent — primary predict() input

### 5.5 Window Laws (3 Directions)

| Law | Code | Direction | Kernel |
|-----|------|-----------|--------|
| **L0** | `memory` | Backward (causal) | Past-only exponential decay |
| **L1** | `forward` | Forward (anticipatory) | Future-only exponential decay |
| **L2** | `integration` | Bidirectional | Symmetric exponential decay |

**Note:** L1 is named "prediction" in some code — this is a misnomer. L1 is merely a forward-looking window operator. Actual prediction is a C³ function.

### 5.6 Demand-Driven Computation

H³ computes only demanded tuples. Demands are collected from downstream consumers:

```python
# C³ Kernel collects demands from all beliefs + relays
demands = kernel.h3_demands()
# Returns: Set[(r3_idx, horizon, morph, law)]
# Current kernel: 28 tuples (17 BCH L0 + 11 belief demands)

# H³ extracts only what's demanded
h3_out = h3_ext.extract(r3_features, demands)
# Returns: Dict[(r3_idx, h, m, l) → Tensor(B, T)]
```

### 5.7 Batch Optimization

Original implementation used a per-frame Python loop (40M+ iterations for 5K frames). Replaced with `torch.unfold` batch computation — H³ now completes in 0.02s for 5,168 frames.

---

## 6. C³ — Cognitive Brain

### 6.1 Identity
C³ is a distributed belief-level predictive coding architecture. It maintains a set of beliefs about the current musical state, continuously predicts their evolution, computes prediction errors, and derives reward from the interaction of surprise and familiarity.

### 6.2 Kernel Architecture

The C³ Kernel is a single-pass, DAG-ordered scheduler that executes one belief cycle per audio frame:

```
Frame t arrives: R³(B,1,128) + H³{tuples → (B,1)}
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐   ┌───────────┐   ┌──────────┐
   │  BCH    │   │ Consonance│   │  Tempo   │
   │  Relay  │──▶│ observe() │   │ observe()│
   │  (L0)   │   └─────┬─────┘   └────┬─────┘
   └─────────┘         │              │
                       ▼              ▼
              ┌──────────────────────────────┐
              │ Phase 2a: predict() all      │
              │   + familiarity.observe()    │
              └──────────────┬───────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ PE_cons  │  │ PE_tempo │  │ PE_fam   │
        │ π_pred   │  │ π_pred   │  │ π_pred   │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             ▼             ▼             ▼
        ┌──────────────────────────────────────┐
        │ Phase 2c: Bayesian Update            │
        │   posterior = (1-gain)*pred + gain*obs│
        └──────────────────┬───────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │ Phase 3: Reward Aggregation          │
        │   surprise + resolution + exploration│
        │   - monotony, × familiarity_mod      │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                    KernelOutput{
                      beliefs: {5 posteriors},
                      pe: {4 prediction errors},
                      precision: {obs + pred},
                      reward: (B, T)
                    }
```

### 6.3 Belief Registry

| Belief | Owner | τ | Phase | Role |
|--------|-------|---|-------|------|
| `perceived_consonance` | SPU | 0.30 | 0 | Fast sensory — harmonic quality |
| `tempo_state` | STU | 0.70 | 0 | Medium inertia — rhythmic state |
| `familiarity_state` | IMU | 0.85 | 2a | High inertia — structural memory |
| `salience_state` | ASU | 0.50 | 1 | *Default 1.0 (not yet active)* |
| `reward_valence` | ARU | 0.80 | 3 | Terminal value — musical reward |

### 6.4 Belief Lifecycle

Each active belief follows the same lifecycle per frame:

```
1. OBSERVE:  Extract current value from R³/H³/relay inputs
             → Likelihood(value, precision_obs)

2. PREDICT:  Linear forward model from previous beliefs + H³ morphs
             → predicted = τ×prev + (1-τ)×baseline
                         + w_trend × H³_M18(trend)
                         + w_period × H³_M14(periodicity)
                         + w_ctx × Σ(context_beliefs_{t-1})

3. PE:       prediction_error = observed - predicted

4. PRECISION: PCU estimates π_pred from PE history stability

5. UPDATE:   Bayesian fusion
             → gain = π_obs / (π_obs + π_pred)
             → posterior = (1 - gain) × predicted + gain × observed
```

### 6.5 Belief Implementations

#### 6.5.1 PerceivedConsonance (SPU, τ=0.3)

**observe():**
- **BCH mode:** `0.5 × consonance_signal + 0.3 × template_match + 0.2 × hierarchy`
- **Fallback:** Weighted R³ consonance group (pleasantness, stumpf_fusion, tonalness, roughness, sethares)
- **precision_obs:** BCH cross-signal agreement `1/(variability + 0.1)`

**predict():**
- H³ demands: `(roughness, H8, M18, L0)` trend, `(tonalness, H12, M14, L0)` periodicity
- Weights: w_trend=0.15, w_period=0.10, context={tempo: 0.1}

#### 6.5.2 TempoState (STU, τ=0.7)

**observe():**
- Weighted R³ rhythm: `0.35×tempo + 0.25×beat + 0.25×pulse + 0.15×regularity`
- **precision_obs:** `onset_regularity × amplitude / (H³_std + eps)`

**predict():**
- H³ demands: `(onset_strength, H6, M18, L0)` trend, `(onset_strength, H6, M14, L0)` periodicity
- Weights: w_trend=0.20, w_period=0.25, context={consonance: 0.05}

#### 6.5.3 FamiliarityState (IMU, τ=0.85)

**observe():**
- **H³ mode:** Inverted standard deviation of tonal features at macro horizon (H16, ~4s)
  - `familiarity = 1 / (1 + 5 × H³_M2_std)`
  - Features: tonalness, key_clarity, tonal_stability (65% H³ stability + 35% R³ level)
- **Fallback:** R³-only weighted average (precision=0.5)
- **precision_obs:** Cross-feature stability agreement

**predict():**
- H³ demands: `(tonalness, H16, M18, L0)` trend
- Weights: w_trend=0.10, w_period=0.0, context={consonance: 0.1}

**Reward interaction:** Familiarity posterior replaces constant 0.5 in reward formula. Familiarity PE is NOT a reward source — it modulates reward, doesn't generate it.

#### 6.5.4 RewardValence (ARU, τ=0.8)

**observe():** Not directly observed — value set by RewardAggregator from PE dict.

**Reward formula:**
```
For each predictive belief i:
  surprise_i   = |PE_i| × π_pred × (1 - familiarity)
  resolution_i = (1 - |PE_i|) × π_pred × familiarity
  exploration_i = |PE_i| × (1 - π_pred)
  monotony_i    = π_pred²

  reward_i = salience × (w1×surprise + w2×resolution + w3×exploration - w4×monotony)

reward_total = Σ reward_i × (0.5 + 0.5 × familiarity_mod)
familiarity_mod = 4 × familiarity × (1 - familiarity)    // inverted-U peak at 0.5
```

Default weights: w_surprise=1.0, w_resolution=1.2, w_exploration=0.3, w_monotony=0.8

### 6.6 Precision Engine (PCU)

The PCU is NOT a belief owner. It estimates prediction precision (π_pred) per belief:

- Maintains sliding window of PE history (32 frames)
- Stability = 1/variance of recent PEs
- Consistency = agreement between short/long PE windows
- Output range: [0.01, 10.0], EMA-smoothed with τ=0.6
- Normalized to [0, 1] in reward formula via `/10.0`

### 6.7 BCH Kernel Wrapper

The BCH (Bridge Consonance Hierarchy) relay is wrapped for causal kernel operation:

| Rule | Description |
|------|-------------|
| **1** | Only 3 of 16D exposed: hierarchy(E[2]), consonance_signal(P[8]), template_match(P[9]) |
| **2** | H³ demand deduplication against belief demands |
| **3** | Consonance observe(): `0.5×cons_signal + 0.3×template_match + 0.2×hierarchy` |
| **4** | precision_obs from BCH cross-signal variability |
| **5** | L0 (memory) only — 17/50 BCH H³ tuples. L1/L2 disabled for causal online mode |

### 6.8 Full C³ Architecture (Beyond Kernel)

The kernel is the minimal real-time belief cycle. The full C³ includes:

- **96 Nuclei** across 10 cognitive units (SPU, STU, ASU, IMU, ARU, MPU, NDU, PCU, ...)
- **5 Processing Depths:** Relay (0) → Encoder (1) → Associator (2) → Integrator (3) → Hub (4-5)
- **26-Region RAM** (Region Activation Map): A1/HG, STG, IFG, dlPFC, vmPFC, OFC, ACC, Amygdala, Hippocampus, VTA, NAcc, ...
- **4-Channel Neurochemical State:** DA (dopamine), NE (norepinephrine), OPI (opioid), 5HT (serotonin)
- **Psi Interpreter (Ψ³):** Maps C³ internals to 6 experiential domains: affect, emotion, aesthetic, bodily, cognitive, temporal
- **Total output:** ~1006D (C³ tensor) + 26D (RAM) + 4D (neuro) + Ψ³

---

## 7. HYBRID — Emotion-Driven Audio Transformation

### 7.1 Identity
HYBRID v0.1 transforms existing audio based on emotional targets. Unlike EQ/filter approaches that merely adjust frequency balance, HYBRID performs structural transformation via HPSS decomposition + transient shaping + harmonic density manipulation.

### 7.2 Pipeline

```
Audio → STFT (phase-preserve) → HPSS
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              Harmonic      Percussive     Residual
                │               │
                ▼               ▼
         Spectral Ops     Transient Ops
         (pitch-class      (attack/decay
          reweighting,      shaping,
          harmonic          timing warp)
          doubles)
                │               │
                └───────┬───────┘
                        ▼
                   Recombine + Safety
                   (gain clamp [-12dB, +6dB],
                    soft-clip limiter,
                    loudness normalize,
                    temporal smoothing)
                        │
                        ▼
               Optional R³ Calibration
               (closed-loop, 2-5 iters)
                        │
                        ▼
                   Output Audio
```

### 7.3 Control Surface

**5 Emotion sliders** (range ±1.0):
- valence, arousal, tension, warmth, brightness

**7 Structural sliders:**
- tempo_shift, rubato, swing, push_pull, rhythm_density, harmonic_mode_bias, harmonic_rhythm

**Global strength:** 0.0–1.0

### 7.4 R³ Calibration Loop

HYBRID includes a closed-loop calibration system that:
1. Transforms audio with current parameters
2. Extracts R³ features from transformed audio
3. Compares to R³ targets derived from emotion sliders
4. Adjusts transform strength proportionally
5. Repeats (2-5 iterations) until R³ deltas converge

---

## 8. Contracts Layer

### 8.1 Nucleus Hierarchy

All cognitive processing units follow a depth-based role hierarchy:

| Depth | Role | Description | Example |
|------:|------|-------------|---------|
| 0 | **Relay** | Sensory routing, no upstream deps | BCH |
| 1 | **Encoder** | Feature extraction from R³/H³ | — |
| 2 | **Associator** | Cross-feature binding | — |
| 3 | **Integrator** | Multi-modal integration | — |
| 4-5 | **Hub** | Convergence, global workspace | ARU |

### 8.2 Evidence Tiers

All 96 models declare evidence provenance:

| Tier | Confidence | Meaning |
|------|-----------|---------|
| **Alpha** | 0.7-0.9 | Strong empirical support, >5 citations |
| **Beta** | 0.4-0.7 | Moderate support, 2-5 citations |
| **Gamma** | 0.1-0.4 | Theoretical/analogical, <2 citations |

### 8.3 Key Dataclasses

- **BrainOutput:** `tensor(B,T,N) + ram(B,T,26) + neuro(B,T,4) + psi(PsiState)`
- **PsiState:** 6 domains × N scalars (affect, emotion, aesthetic, bodily, cognitive, temporal)
- **R3FeatureSpec:** Feature registration with group, index, description, citation, unit
- **H3DemandSpec:** `(r3_idx, horizon, morph, law)` frozen tuple with `.as_tuple()` method
- **Likelihood:** `(value: Tensor, precision: Tensor)` — observation + confidence
- **KernelOutput:** `beliefs{} + pe{} + precision_obs{} + precision_pred{} + reward`

---

## 9. H³ Demand Budget

Current kernel demands (28 tuples total):

| Source | Tuples | Details |
|--------|-------:|---------|
| BCH L0 | 17 | 50 BCH demands filtered to law==0 |
| Consonance predict | 4 | (roughness,H8,M18,L0), (tonalness,H12,M14,L0) + M2 variants |
| Tempo predict | 4 | (onset_strength,H6,M18,L0), (onset_strength,H6,M14,L0) + M2 variants |
| Familiarity predict | 2 | (tonalness,H16,M18,L0) + M2 variant |
| Familiarity observe | 3 | (tonalness,H16,M2,L0), (key_clarity,H16,M2,L0), (tonal_stability,H16,M2,L0) |
| **Deduplication** | -2 | Overlapping tuples removed by set union |
| **Total** | **28** | |

---

## 10. Validation Results

### 10.1 3-Piece Stress Test (17 Feb 2026)

Pieces: Swan Lake (orchestral waltz), Bach Cello Suite No.1 (solo monophonic), Beethoven Pathetique Sonata (solo piano, Grave-Allegro)

| Metric | Swan Lake | Bach Cello | Beethoven |
|--------|----------:|-----------:|----------:|
| Consonance mean | 0.546 | 0.561 | 0.542 |
| Consonance range | 0.248 | 0.268 | **0.340** |
| Tempo mean | 0.589 | 0.610 | 0.595 |
| Tempo range | 0.097 | **0.153** | 0.138 |
| Familiarity mean | 0.799 | 0.800 | 0.798 |
| Familiarity range | 0.601 | **0.616** | 0.310 |
| Reward mean | **0.148** | 0.099 | 0.083 |
| Reward range | 0.492 | **0.510** | 0.333 |
| PE_cons adaptation | 25.1% | 12.2% | **43.4%** |
| PE_fam adaptation | -2.1% | **32.8%** | -6.8% |
| Fam drift (30s) | +0.011 | **+0.048** | +0.018 |

### 10.2 Diagnostic Checks (8/9 PASS)

| Check | Result |
|-------|--------|
| PE_cons decreases over time (Swan Lake) | PASS |
| PE_cons decreases over time (Bach Cello) | PASS |
| PE_cons decreases over time (Beethoven) | PASS |
| Consonance range spread > 1.2x (1.37x) | PASS |
| PE_cons std spread > 1.2x (1.41x) | PASS |
| Reward mean spread > 0.01 (0.0655) | PASS |
| Tempo range spread > 1.2x (1.58x) | PASS |
| Familiarity mean spread > 0.02 (0.0019) | **FAIL** |
| Familiarity active (range > 0.01) | PASS |

**FAIL analysis:** Familiarity mean converges to ~0.80 for all pieces due to high inertia (τ=0.85) over only 30 seconds. The **range** clearly differentiates (0.60 vs 0.62 vs 0.31), as do **adaptation rate** (Bach 32.8%) and **drift** (Bach +0.048). The mean spread failure is an expected consequence of high τ + short excerpts, not an architectural flaw.

### 10.3 Key Behavioral Findings

1. **Beethoven has strongest consonance adaptation** (43.4%) — dramatic Grave→Allegro transition creates large initial surprise that the system learns rapidly.

2. **Bach has strongest familiarity adaptation** (32.8% PE_fam reduction) — contrapuntal patterns are initially surprising but become predictable. Familiarity drifts +0.048 (0.757→0.805) = "patterns learned."

3. **Swan Lake has highest reward** (mean 0.148) — its predictable waltz structure generates consistent resolution reward with moderate surprise.

4. **Familiarity modulation reshapes reward** — before activation, Bach appeared "most emotional" (widest reward range). After activation, the reward becomes more structurally meaningful: Swan Lake's repetitive structure generates higher resolution, while Bach's volatility generates wider but lower-mean reward.

### 10.4 Pipeline Performance

| Stage | Time (30s audio) | FPS |
|-------|------------------:|----:|
| Cochlea (mel) | 1.7s | — |
| R³ extraction | 1.9s | 2,720 |
| H³ sparse (28 tuples) | 0.02s | 258,400 |
| C³ kernel (4 beliefs) | 4.7s | 1,100 |
| **Total** | **~7.9s** | — |

---

## 11. Directory Structure

```
Musical_Intelligence/
├── __init__.py
│
├── contracts/                          # 19 files — Interfaces & types
│   ├── bases/
│   │   ├── base_model.py
│   │   ├── base_semantic_group.py
│   │   ├── base_spectral_group.py
│   │   ├── base_unit.py
│   │   └── nucleus.py                 # Relay→Encoder→Associator→Integrator→Hub
│   └── dataclasses/
│       ├── brain_output.py             # BrainOutput + PsiState
│       ├── demand_spec.py              # H3DemandSpec
│       ├── feature_spec.py             # R3FeatureSpec
│       ├── model_metadata.py           # Evidence tiers + falsification
│       ├── neuro_link.py
│       ├── region_link.py
│       └── ...
│
├── ear/                                # 82 files — Perceptual front-end
│   ├── r3/                             # 39 files — 128D spectral extraction
│   │   ├── extractor.py
│   │   ├── constants/                  # feature_names, group_boundaries, ...
│   │   ├── groups/                     # 9 spectral groups (A-K, E/I dissolved)
│   │   │   ├── a_consonance/group.py   # Sethares, Plomp-Levelt, HPS F0
│   │   │   ├── b_energy/group.py
│   │   │   ├── c_timbre/group.py
│   │   │   ├── d_change/group.py
│   │   │   ├── f_pitch_chroma/group.py
│   │   │   ├── g_rhythm_groove/group.py
│   │   │   ├── h_harmony/group.py
│   │   │   ├── j_timbre_extended/group.py
│   │   │   └── k_modulation/group.py
│   │   ├── pipeline/                   # DAG executor, normalization, warmup
│   │   └── registry/                   # Feature map, auto-discovery
│   │
│   └── h3/                             # 43 files — Temporal morphology
│       ├── extractor.py
│       ├── constants/                  # horizons, morphs, laws, scaling
│       ├── bands/                      # micro, meso, macro, ultra
│       ├── morphology/                 # 24 morph computers + batch optimization
│       ├── attention/                  # L0 memory, L1 forward, L2 integration
│       ├── demand/                     # Demand tree, aggregator
│       └── pipeline/                   # Executor, warmup
│
├── brain/                              # 55 files — C³ Cognitive Brain
│   ├── orchestrator.py                 # BrainOrchestrator (full 96-nucleus mode)
│   ├── executor.py                     # Depth-ordered DAG scheduler
│   ├── psi_interpreter.py              # Ψ³ cognitive readout
│   │
│   ├── kernel/                         # 12 files — Belief-cycle engine
│   │   ├── scheduler.py                # C3Kernel (single-pass 5-phase)
│   │   ├── belief.py                   # Abstract Belief + Likelihood
│   │   ├── precision.py                # PrecisionEngine (PCU)
│   │   ├── reward.py                   # RewardAggregator
│   │   ├── beliefs/
│   │   │   ├── consonance.py           # SPU, τ=0.3
│   │   │   ├── tempo.py                # STU, τ=0.7
│   │   │   ├── familiarity.py          # IMU, τ=0.85
│   │   │   └── reward.py               # ARU, τ=0.8
│   │   └── relays/
│   │       └── bch_wrapper.py          # BCH causal L0-only adapter
│   │
│   ├── units/                          # Cognitive units
│   │   └── spu/relays/bch.py           # BCH relay (12D, 50 H³ demands)
│   │
│   ├── neurochemicals/                 # 6 files — DA, NE, OPI, 5HT
│   │   ├── manager.py
│   │   ├── dopamine.py
│   │   ├── norepinephrine.py
│   │   ├── opioid.py
│   │   └── serotonin.py
│   │
│   └── regions/                        # 29 files — 26 brain regions
│       ├── registry.py
│       ├── a1_hg.py ... pag.py         # Cortical (12) + Subcortical (9) + Brainstem (5)
│       └── _region.py                  # Region dataclass (MNI coords, Brodmann areas)
│
├── hybrid/                             # 14 files — Audio transformation
│   ├── hybrid_transformer.py           # Main pipeline
│   ├── controls.py                     # EmotionControls (5 sliders + 7 structural)
│   ├── calibration.py                  # R³ closed-loop feedback
│   ├── cli.py                          # CLI interface
│   └── ops/
│       ├── stft_ops.py                 # Phase-preserving STFT
│       ├── hpss_ops.py                 # Harmonic-Percussive Source Separation
│       ├── transient_ops.py            # Transient shaping
│       ├── harmonic_ops.py             # Harmonic doubles
│       ├── pitchclass_ops.py           # Pitch-class reweighting
│       ├── structure_ops.py            # Beat grid, onset, chroma, novelty
│       └── timing_ops.py              # Tempo, rubato, microtiming, rhythm density
│
├── config/                             # 9 files — YAML configuration
├── data/                               # 7 files — Dataset handling
├── training/                           # 7 files — BCH training pipeline
├── evaluation/                         # 6 files — Metrics, white-box analysis
├── utils/                              # 1 file  — Stubs
└── visualization/                      # 1 file  — Stubs
```

---

## 12. Design Principles

1. **Glass-Box:** Every intermediate value has semantic meaning. Consonance IS consonance. No latent dimensions.

2. **Ontology-First:** R³ and H³ ontologies are frozen before implementation. Code must conform to boundary documents.

3. **Demand-Driven:** H³ computes only what C³ requests. No speculative computation.

4. **Bayesian Updating:** All belief updates use precision-weighted fusion. No heuristic blending.

5. **Evidence-Grounded:** All 96 models declare evidence tier, citations, and falsification criteria.

6. **Deterministic:** No random state, no sampling. Same input → same output.

7. **No Learning (v1.0):** All weights are configured, not trained. The system is a fixed computational theory, not a learned approximation.

8. **Causal Online:** The kernel operates in causal mode (L0 only for BCH). Can process audio in real-time.

9. **Modular Activation:** Beliefs can be activated incrementally. Current: 4/5 active. Salience pending.

---

## 13. Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Familiarity mean doesn't differentiate across pieces (30s) | τ=0.85 too slow for short excerpts | Range and adaptation rate differentiate; needs longer pieces |
| Salience still default 1.0 | Reward formula doesn't gate by attention | Next activation target |
| observe() weights are heuristic | Not empirically validated | All configurable in YAML; future calibration studies |
| R³ naming discrepancy | Docs use semantic names, code uses computational | Deferred to Phase 5 |
| No learning in v1.0 | Weights fixed, no adaptation | By design; learning = Phase 6+ |
| BCH L1/L2 fallback | P-layer outputs degrade in causal mode | Functional but suboptimal; L2 demands fallback to R³ raw |
| pi_pred normalization | PrecisionEngine outputs [0.01, 10.0] but reward assumes [0, 1] | Fixed with /10.0 normalization |

---

## 14. Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| P1: Contracts | Done (17 files) | Interfaces, dataclasses, nucleus hierarchy |
| P2: Ear (R³+H³) | Done (82 files) | Spectral + temporal feature extraction |
| P3: Brain (C³) | Done (55 files) | 96 nuclei, 10 mechanisms, 5 pathways |
| P3.1: C³ Kernel | Done (12 files) | Minimal belief cycle, BCH injection |
| P3.2: Familiarity | Done | Active belief, H³ macro stability |
| P3.3: Salience | Pending | ASU activation, attention gating |
| P4: HYBRID v0.1 | Done (14 files) | Audio transformation, R³ calibration |
| P5: Naming/Docs | Pending | Resolve R³ naming discrepancy, doc-code sync |
| P6: Learning | Future | Learned weights, plasticity, inverse heads |

---

*End of Report*
