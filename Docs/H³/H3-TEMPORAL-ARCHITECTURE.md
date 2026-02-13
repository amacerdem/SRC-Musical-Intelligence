# H3 Temporal Architecture -- Definitive Design Document

**Version**: 2.0.0
**Updated**: 2026-02-13
**Status**: Canonical specification for H3 temporal morphology layer
**Companion**: [R3-SPECTRAL-ARCHITECTURE.md](../R3/R3-SPECTRAL-ARCHITECTURE.md)

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Pipeline Position](#2-pipeline-position)
3. [The 4-Tuple Address System](#3-the-4-tuple-address-system)
4. [Axis 1: Horizons (32 Temporal Scales)](#4-axis-1-horizons-32-temporal-scales)
5. [Axis 2: Morphs (24 Statistical Descriptors)](#5-axis-2-morphs-24-statistical-descriptors)
6. [Axis 3: Laws (3 Temporal Perspectives)](#6-axis-3-laws-3-temporal-perspectives)
7. [Attention Kernel](#7-attention-kernel)
8. [Mechanism Integration](#8-mechanism-integration)
9. [Demand Aggregation](#9-demand-aggregation)
10. [Sparsity Analysis](#10-sparsity-analysis)
11. [R3 v2 Expansion Impact](#11-r3-v2-expansion-impact)
12. [Code Architecture](#12-code-architecture)
13. [Cross-References](#13-cross-references)

---

## 1. Design Philosophy

H3 is the temporal morphology layer of the MI architecture. Where R3 produces a dense 128D spectral snapshot at each frame, H3 asks: *how does each spectral feature behave over time?* The answer is not a single number but a structured family of descriptors -- statistical morphs computed at specific temporal horizons under different causal laws.

Four principles govern H3's design:

### 1.1 Demand-Driven Sparse Computation

The theoretical H3 space contains 294,912 possible 4-tuples, but no model needs more than ~150. The system computes only what is demanded. Each C3 model declares its H3 demands via `H3DemandSpec` instances, and the H3 engine computes precisely those tuples and nothing else. This is not an optimization -- it is the core architectural premise. The space is intentionally vast so that models can address any temporal question about any spectral feature, while the sparsity keeps computation tractable.

### 1.2 Three-Axis Orthogonal Space

H3 decomposes temporal behavior along three independent axes:

- **Horizon**: *At what timescale?* (5.8 ms to 981 seconds)
- **Morph**: *What property?* (mean, velocity, entropy, periodicity, ...)
- **Law**: *From what temporal perspective?* (past, future, or both)

These axes are fully orthogonal: any morph can be computed at any horizon under any law. The 4-tuple `(r3_idx, horizon, morph, law)` uniquely identifies every possible temporal descriptor.

### 1.3 Musical-Perceptual Grounding

Each horizon maps to a recognizable musical timescale: onset transients (Micro), beat periods (Meso), musical sections (Macro), entire movements (Ultra). Each morph captures a perceptually relevant property of temporal behavior. Each law mirrors a distinct cognitive process -- memory, prediction, integration. H3 is not an arbitrary statistical engine; it is designed around how humans perceive and process temporal structure in music.

### 1.4 Lazy Evaluation

H3 does no precomputation. At runtime, the `DemandTree` groups all demanded tuples by horizon. For each demanded horizon, attention weights are computed once, then reused across all morphs and laws at that horizon. Horizons not demanded by any model are never touched.

---

## 2. Pipeline Position

```
Audio Signal (44,100 Hz)
    |
    v
Cochlea (128-mel spectrogram, B x 128 x T @ 172.27 Hz)
    |
    v
+================================================================+
|              R3 Spectral Extractor (128D)                       |
|   Groups A-K: Consonance, Energy, Timbre, Change, Interactions, |
|   Pitch, Rhythm, Harmony, Information, TimbreExt, Modulation    |
+================================================================+
    |
    v
R3 Output: (B, T, 128) -- dense spectral tensor, [0,1] range
    |
    v
+================================================================+
|              H3 Temporal Morphology Layer (sparse)              |
|                                                                 |
|   Input:  R3 tensor (B, T, 128)                                |
|   Demand: ~8,600 4-tuples from 96 C3 models                    |
|   Output: sparse dict {(r3_idx, horizon, morph, law): (B, T)}  |
|                                                                 |
|   For each demanded horizon H:                                  |
|     1. Compute attention weights A(dt) = exp(-3|dt|/H)         |
|     2. Select window per law (L0/L1/L2)                         |
|     3. For each demanded morph at H: apply morph function       |
+================================================================+
    |
    v
Brain (C3 models: SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU)
    |
    v
C3 Output: (B, T, 1006) -- full perceptual representation
```

H3 is a **temporal transformer**: it takes dense per-frame spectral features and produces sparse morphological descriptors that characterize *how* those features change over time. The output dimensionality is not fixed -- it equals the number of demanded tuples, which varies by model configuration.

**Key invariants**:
- H3 reads R3 output; it never reads raw audio or mel spectrograms
- H3 output values are in `[0, 1]` (morph-specific normalization via `MORPH_SCALE`)
- H3 is stateless between frames (all temporal context comes from the attention window)
- Frame rate is inherited from R3: 172.27 Hz (5.8 ms/frame)

---

## 3. The 4-Tuple Address System

Every H3 value is identified by a canonical 4-tuple address:

```
(r3_idx, horizon, morph, law)
```

| Field | Range | Description |
|-------|-------|-------------|
| `r3_idx` | 0-127 | Which R3 spectral feature to observe temporally |
| `horizon` | 0-31 (H0-H31) | At what temporal scale (window size) |
| `morph` | 0-23 (M0-M23) | What statistical property to extract |
| `law` | 0-2 (L0-L2) | What causal direction (past, future, both) |

### Address Space Metrics

| Metric | v1 (49D R3) | v2 (128D R3) |
|--------|:-----------:|:------------:|
| Theoretical space | 49 x 32 x 24 x 3 = 112,896 | 128 x 32 x 24 x 3 = 294,912 |
| Estimated actual tuples | ~5,200 | ~8,600 |
| Occupancy | ~4.6% | ~2.9% |
| Tuples per model (range) | 12-150 | 20-200 |

### Address Examples

```
(7, 6, 8, 0)   -- R3[7] amplitude, H6 200ms, M8 velocity, L0 Memory
                   "How fast is amplitude changing over the last 200ms?"

(0, 16, 14, 2) -- R3[0] roughness, H16 1000ms, M14 periodicity, L2 Integration
                   "Is roughness periodic at the 1-second scale (bidirectional)?"

(61, 20, 18, 1) -- R3[61] pitch_height, H20 5000ms, M18 trend, L1 Prediction
                    "Is pitch trending upward over the next 5 seconds?"
```

### Demand Declaration

Each C3 model declares its H3 demands as a tuple of `H3DemandSpec` instances:

```python
h3_demand = (
    H3DemandSpec(r3_idx=7,  horizon=6,  morph=8, law=0),
    H3DemandSpec(r3_idx=7,  horizon=6,  morph=9, law=0),
    H3DemandSpec(r3_idx=0,  horizon=16, morph=1, law=2),
    # ...
)
```

The demand is immutable per model version. Changing H3 demand requires a model version bump.

---

## 4. Axis 1: Horizons (32 Temporal Scales)

The horizon axis spans five orders of magnitude, from sub-beat transients (5.8 ms) to full musical works (~16 minutes). The 32 horizons are organized into 4 perceptual bands.

### 4.1 Complete Horizon Table

#### Micro Band (H0-H7): Sensory / Sub-Beat

| ID | Duration | Frames | Musical Scale | Neuroscience Basis |
|:--:|:--------:|:------:|--------------|-------------------|
| H0 | 5.8 ms | 1 | Single frame, onset detection | Cochlear nucleus temporal resolution |
| H1 | 11.6 ms | 2 | Double frame, fine timing | Brainstem ITD resolution |
| H2 | 17.4 ms | 3 | Sub-onset grouping | Auditory nerve adaptation |
| H3 | 23.2 ms | 4 | Consonant onset, attack | Pre-attentive grouping (MMN) |
| H4 | 34.8 ms | 6 | Short attack transient | Temporal integration window |
| H5 | 46.4 ms | 8 | Phoneme / short note boundary | Categorical perception boundary |
| H6 | 200 ms | 34 | Short note, sixteenth note | Auditory scene analysis window |
| H7 | 250 ms | 43 | Beat subdivision, eighth note | Echoic memory boundary |

**Micro band character**: Raw sensory integration. These horizons capture onset transients, attack profiles, and sub-beat dynamics. H6 (200 ms) is the most commonly demanded micro horizon -- it sits at the boundary of auditory scene analysis.

#### Meso Band (H8-H15): Beat / Phrase

| ID | Duration | Frames | Musical Scale | Neuroscience Basis |
|:--:|:--------:|:------:|--------------|-------------------|
| H8 | 300 ms | 52 | Fast beat (200 BPM) | Motor cortex entrainment onset |
| H9 | 350 ms | 60 | Quick beat (170 BPM) | Preferred tapping rate lower |
| H10 | 400 ms | 69 | Moderate beat (150 BPM) | Auditory cortex beat period |
| H11 | 450 ms | 78 | Walking tempo (133 BPM) | Sensorimotor coupling sweet spot |
| H12 | 525 ms | 90 | Common beat (114 BPM) | Preferred tempo zone (van Noorden) |
| H13 | 600 ms | 103 | Standard beat (100 BPM) | Comfortable tempo range |
| H14 | 700 ms | 121 | Slow beat (86 BPM) | Extended beat period |
| H15 | 800 ms | 138 | Half-note, slow tempo | Motor planning window |

**Meso band character**: Beat-level integration. These horizons align with musical beat periods across the full tempo range. H9-H12 cover the "preferred tempo" zone (100-170 BPM) where human rhythmic entrainment is strongest.

#### Macro Band (H16-H23): Section / Passage

| ID | Duration | Frames | Musical Scale | Neuroscience Basis |
|:--:|:--------:|:------:|--------------|-------------------|
| H16 | 1,000 ms | 172 | 1 measure @ 240 BPM | Working memory consolidation |
| H17 | 1,500 ms | 259 | 1 measure @ 160 BPM | Short phrase boundary |
| H18 | 2,000 ms | 345 | 1 measure @ 120 BPM | Auditory working memory span |
| H19 | 3,000 ms | 517 | 2-measure phrase | Phrase grouping (Lerdahl & Jackendoff) |
| H20 | 5,000 ms | 861 | Short passage | Episodic buffer integration |
| H21 | 8,000 ms | 1,378 | Extended passage / verse | Narrative arc unit |
| H22 | 15,000 ms | 2,584 | Musical section (A of ABA) | Long-term memory encoding |
| H23 | 25,000 ms | 4,307 | Multi-section span | Hierarchical form perception |

**Macro band character**: Structural and narrative integration. These horizons capture musical form -- measures, phrases, sections, and multi-section arcs. H18 (2 s) is the most frequently demanded macro horizon, aligning with the auditory working memory span.

#### Ultra Band (H24-H31): Movement / Full Work

| ID | Duration | Frames | Musical Scale | Neuroscience Basis |
|:--:|:--------:|:------:|--------------|-------------------|
| H24 | 36,000 ms | 6,202 | Movement intro / extended section | Long-term auditory memory |
| H25 | 60,000 ms | 10,336 | Short movement / song | Episodic memory consolidation |
| H26 | 120,000 ms | 20,672 | Standard movement | Autobiographical association |
| H27 | 200,000 ms | 34,453 | Extended movement | Sustained attention span |
| H28 | 414,000 ms | 71,319 | Multi-movement span | Narrative comprehension |
| H29 | 600,000 ms | 103,359 | Long movement / half work | Global structure integration |
| H30 | 800,000 ms | 137,812 | Near-complete work | Cumulative form perception |
| H31 | 981,000 ms | 168,999 | Full work (~16 min) | Complete aesthetic arc |

**Ultra band character**: Whole-work integration. These horizons are used sparingly, primarily by MEM (Memory Consolidation) mechanisms. They capture cumulative statistical properties over entire musical movements or complete works.

### 4.2 Horizon Distribution Visualization

```
Duration (log scale):
5.8ms                                                        981s
|----|----|--------|----------|------------|----------------|
  H0  H3   H6  H7  H9 H12 H15 H16  H18  H20  H22  H25  H28  H31
  |        |       |          |          |         |         |
  Micro    |  Meso |   Macro  |          |  Ultra  |         |
           |       |          |          |         |         |
 Onset   Beat   Note    Measure    Section    Movement    Work
```

### 4.3 Frame Count Progression

The frame counts follow a roughly exponential progression, ensuring uniform resolution on a logarithmic timescale:

```
Micro:  1, 2, 3, 4, 6, 8, 34, 43
Meso:   52, 60, 69, 78, 90, 103, 121, 138
Macro:  172, 259, 345, 517, 861, 1378, 2584, 4307
Ultra:  6202, 10336, 20672, 34453, 71319, 103359, 137812, 168999
```

---

## 5. Axis 2: Morphs (24 Statistical Descriptors)

A morph is a function that takes an attention-weighted window of R3 feature values and produces a single scalar descriptor. The 24 morphs are organized into 6 categories.

### 5.1 Complete Morph Table

| ID | Name | Formula / Description | Category | Min Window |
|:--:|------|----------------------|----------|:----------:|
| M0 | value | Attention-weighted mean: sum(A(dt) * x(t+dt)) / sum(A(dt)) | Level | 1 |
| M1 | mean | Arithmetic mean over window | Level | 1 |
| M2 | std | Standard deviation over window | Dispersion | 2 |
| M3 | median | Median value over window | Level | 1 |
| M4 | max | Maximum value over window | Level | 1 |
| M5 | range | max - min over window | Dispersion | 2 |
| M6 | skewness | Third standardized moment | Shape | 3 |
| M7 | kurtosis | Fourth standardized moment (excess) | Shape | 4 |
| M8 | velocity | dR3/dt (first temporal derivative) | Dynamics | 2 |
| M9 | velocity_mean | Mean of velocity over window | Dynamics | 3 |
| M10 | velocity_std | Standard deviation of velocity | Dynamics | 3 |
| M11 | acceleration | d^2R3/dt^2 (second temporal derivative) | Dynamics | 3 |
| M12 | acceleration_mean | Mean of acceleration over window | Dynamics | 4 |
| M13 | acceleration_std | Standard deviation of acceleration | Dynamics | 4 |
| M14 | periodicity | Autocorrelation peak (normalized) | Rhythm | 8 |
| M15 | smoothness | 1 / (1 + \|jerk\| / sigma) | Dynamics | 4 |
| M16 | curvature | Second derivative normalized by arc length | Shape | 3 |
| M17 | shape_period | Oscillation period (zero-crossing interval) | Rhythm | 8 |
| M18 | trend | Linear regression slope over window | Dynamics | 3 |
| M19 | stability | 1 / (1 + var / sigma^2) | Dispersion | 3 |
| M20 | entropy | Shannon entropy of value distribution | Information | 4 |
| M21 | zero_crossings | Count of mean-crossings in window | Dynamics | 3 |
| M22 | peaks | Count of local maxima in window | Rhythm | 3 |
| M23 | symmetry | Forward/backward correlation (time reversal) | Shape | 4 |

### 5.2 Category Summary

| Category | Morphs | Count | What It Captures |
|----------|--------|:-----:|-----------------|
| **Level** | M0, M1, M3, M4 | 4 | Central tendency -- where is the feature? |
| **Dispersion** | M2, M5, M19 | 3 | Spread and stability -- how variable is it? |
| **Shape** | M6, M7, M16, M23 | 4 | Distribution shape -- asymmetric? peaked? curved? reversible? |
| **Dynamics** | M8, M9, M10, M11, M12, M13, M15, M18, M21 | 9 | Temporal derivatives -- velocity, acceleration, smoothness, trend |
| **Rhythm** | M14, M17, M22 | 3 | Periodic structure -- is it repeating? at what rate? |
| **Information** | M20 | 1 | Uncertainty -- is the behavior predictable or surprising? |

### 5.3 MORPH_SCALE Calibration

Each morph produces values in different natural ranges. The `MORPH_SCALE` array in `mi_beta/core/constants.py` provides per-morph normalization factors to map outputs into `[0, 1]`:

```python
MORPH_SCALE = [
    1.0,   # M0  value       -- already [0,1] from R3
    1.0,   # M1  mean        -- already [0,1] from R3
    0.25,  # M2  std         -- typical max ~0.25
    1.0,   # M3  median      -- already [0,1]
    1.0,   # M4  max         -- already [0,1]
    1.0,   # M5  range       -- max 1.0
    2.0,   # M6  skewness    -- typical range [-2, 2]
    5.0,   # M7  kurtosis    -- typical range [-3, 7] (excess)
    0.1,   # M8  velocity    -- typical max ~0.1/frame
    0.05,  # M9  vel_mean    -- smoothed velocity
    0.05,  # M10 vel_std     -- velocity dispersion
    0.01,  # M11 acceleration -- typical max ~0.01/frame^2
    0.005, # M12 acc_mean    -- smoothed acceleration
    0.005, # M13 acc_std     -- acceleration dispersion
    1.0,   # M14 periodicity -- autocorrelation [0,1]
    1.0,   # M15 smoothness  -- [0,1] by construction
    0.1,   # M16 curvature   -- typical max ~0.1
    100.0, # M17 shape_period -- frames; max ~100
    0.01,  # M18 trend       -- slope per frame
    1.0,   # M19 stability   -- [0,1] by construction
    3.0,   # M20 entropy     -- max ~log2(bins) bits
    20.0,  # M21 zero_cross  -- max ~20 crossings
    10.0,  # M22 peaks       -- max ~10 peaks
    1.0,   # M23 symmetry    -- correlation [-1,1] -> [0,1]
]
```

Normalization formula: `output = clamp(raw_morph / MORPH_SCALE[morph_idx], 0.0, 1.0)`

For morphs that produce signed values (M6 skewness, M8 velocity, M11 acceleration, M16 curvature, M18 trend, M23 symmetry), the mapping is `(raw / scale + 1) / 2` to center zero at 0.5.

### 5.4 Morph-Horizon Interaction

Not all morphs are meaningful at all horizons. Minimum window requirements constrain which combinations are valid:

| Morph | Min Window (frames) | Smallest Valid Horizon |
|-------|:-------------------:|:---------------------:|
| M0-M5 (Level, Dispersion) | 1-2 | H0 (1 frame) |
| M6, M8, M16, M18, M21 | 2-3 | H1 (2 frames) |
| M7, M11-M13, M15, M19, M20, M23 | 3-4 | H3 (4 frames) |
| M14, M17 (periodicity, shape_period) | 8 | H5 (8 frames) |
| M22 (peaks) | 3 | H2 (3 frames) |

---

## 6. Axis 3: Laws (3 Temporal Perspectives)

The three laws determine the causal direction of the attention window. They model three distinct cognitive processes: remembering, anticipating, and integrating.

### 6.1 L0 -- Memory (Past -> Present)

**Direction**: Causal. Looks backward from the current frame.
**Window**: `[max(0, t - n + 1), t + 1)` where `n` = horizon in frames
**Cognitive basis**: Echoic memory, auditory streaming, sensory trace decay
**Kernel shape**: Exponential decay into the past

```
Past -------- Now ---- Future
[====A(dt)===>|t]
    causal    ^
    window    current frame
```

**Primary users**: IMU (emotional memory), STU (structural recall), MPU (motor learning)

### 6.2 L1 -- Prediction (Present -> Future)

**Direction**: Anticipatory. Looks forward from the current frame.
**Window**: `[t, min(T, t + n))` where `n` = horizon in frames
**Cognitive basis**: Predictive coding, expectation formation, Bayesian brain hypothesis
**Kernel shape**: Exponential decay into the future

```
Past -------- Now ---- Future
              [t|==A(dt)===>]
              ^  anticipatory
              current frame
```

**Primary users**: NDU (novelty/prediction error), MPU (motor anticipation), PCU (predictive control)

### 6.3 L2 -- Integration (Past <-> Future)

**Direction**: Bidirectional symmetric. Centers the window on the current frame.
**Window**: `[max(0, t - half), min(T, t + n - half))` where `half = n // 2`
**Cognitive basis**: Gestalt perception, auditory scene analysis, temporal binding
**Kernel shape**: Symmetric exponential decay in both directions

```
Past -------- Now ---- Future
   [<==A(dt)==|t|==A(dt)==>]
      backward ^ forward
               current frame
```

**Primary users**: SPU (spatial integration), ASU (affective scene analysis), ARU (aesthetic resonance)

### 6.4 Law Usage Patterns by Unit

| Unit | L0 (Memory) | L1 (Prediction) | L2 (Integration) | Dominant |
|------|:-----------:|:---------------:|:-----------------:|:--------:|
| SPU | Low | Low | High | L2 |
| STU | High | Medium | Medium | L0 |
| IMU | High | Low | Medium | L0 |
| ASU | Low | Low | High | L2 |
| NDU | Low | High | Medium | L1 |
| MPU | Medium | High | Low | L1 |
| PCU | Low | High | Medium | L1 |
| ARU | Medium | Low | High | L2 |
| RPU | Medium | Medium | Medium | Mixed |

---

## 7. Attention Kernel

The attention kernel defines how much weight each frame in the window contributes to a morph computation.

### 7.1 Kernel Formula

```
A(dt) = exp(-ATTENTION_DECAY * |dt| / H)
```

Where:
- `dt` = temporal offset from the reference frame (in frames)
- `H` = horizon size (in frames)
- `ATTENTION_DECAY = 3.0` (constant across all computations)

### 7.2 Kernel Properties

| Property | Value | Derivation |
|----------|-------|-----------|
| Peak weight | 1.0 | A(0) = exp(0) = 1.0 |
| Boundary weight | ~4.98% | A(H) = exp(-3) = 0.0498 |
| Half-life | H * ln(2) / 3 = 0.231 * H | A(t_half) = 0.5 |
| Effective width | ~67% of H | Region where A(dt) > 0.5 |
| Normalization | Weights sum to 1.0 | Applied after window selection |

### 7.3 Boundary Design Rationale

The choice of `ATTENTION_DECAY = 3.0` is deliberate: at the window boundary (`|dt| = H`), the kernel weight is `exp(-3) ~= 5%`. This means:

- The boundary contributes ~5% of peak weight -- present but not dominant
- 95% of the total weight falls within the horizon window
- The decay is steep enough to preserve locality, gentle enough to avoid abrupt cutoffs

### 7.4 Kernel Visualization (Normalized)

```
Weight
1.0 |*
    | *
    |  *
0.5 |   *                     <- half-life at 0.231*H
    |     *
    |       **
    |          ***
0.05|              *******    <- boundary (~5% weight)
0.0 +-----|------|------|-->  dt/H
    0    0.33   0.67   1.0
```

### 7.5 Window Selection by Law

Given horizon `H` in frames and current time `t`:

```python
if law == L0:  # Memory (causal)
    window = range(max(0, t - n + 1), t + 1)
    # dt = frame - t  (negative for past frames)

elif law == L1:  # Prediction (anticipatory)
    window = range(t, min(T, t + n))
    # dt = frame - t  (positive for future frames)

elif law == L2:  # Integration (bidirectional)
    half = n // 2
    window = range(max(0, t - half), min(T, t + n - half))
    # dt = frame - t  (both positive and negative)
```

For all laws, the kernel uses `|dt|` so the decay is symmetric in magnitude. The law determines only which frames are included.

---

## 8. Mechanism Integration

The 10 C3 mechanisms define characteristic H3 access patterns. Each mechanism operates at specific horizon bands and demands particular morph combinations.

### 8.1 Mechanism-Horizon Map

| Mechanism | Full Name | Horizons | Band | Est. Tuples/Model |
|:---------:|-----------|:--------:|:----:|:-----------------:|
| PPC | Pre-attentive Pattern Capture | H0, H3, H6 | Micro | ~60 |
| TPC | Temporal Pattern Completion | H6, H12, H16 | Micro-Macro | ~45 |
| BEP | Beat Entrainment Prediction | H6, H9, H11 | Micro-Meso | ~50 |
| ASA | Auditory Scene Analysis | H3, H6, H9 | Micro-Meso | ~40 |
| TMH | Temporal Memory Hierarchy | H16, H18, H20, H22 | Macro | ~80 |
| MEM | Memory Consolidation | H18, H20, H22, H25 | Macro-Ultra | ~100 |
| SYN | Temporal Synchronization | H12, H16, H18 | Meso-Macro | ~50 |
| AED | Arousal/Energy Detection | H6, H16 | Micro+Macro | ~30 |
| CPD | Change Point Detection | H9, H16, H18 | Meso-Macro | ~40 |
| C0P | Contextual Prediction | H18, H19, H20 | Macro | ~45 |

### 8.2 Horizon-Mechanism Heatmap

```
Horizon:  H0 H1 H2 H3 H4 H5 H6 H7 H8 H9 H10 H11 H12 H13 H14 H15 H16 H17 H18 H19 H20 H21 H22 H23 H24 H25
          |  |  |  |  |  |  |  |  |  |  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
PPC:      #  .  .  #  .  .  #  .  .  .  .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
TPC:      .  .  .  .  .  .  #  .  .  .  .   .   #   .   .   .   #   .   .   .   .   .   .   .   .   .
BEP:      .  .  .  .  .  .  #  .  .  #  .   #   .   .   .   .   .   .   .   .   .   .   .   .   .   .
ASA:      .  .  .  #  .  .  #  .  .  #  .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
TMH:      .  .  .  .  .  .  .  .  .  .  .   .   .   .   .   .   #   .   #   .   #   .   #   .   .   .
MEM:      .  .  .  .  .  .  .  .  .  .  .   .   .   .   .   .   .   .   #   .   #   .   #   .   .   #
SYN:      .  .  .  .  .  .  .  .  .  .  .   .   #   .   .   .   #   .   #   .   .   .   .   .   .   .
AED:      .  .  .  .  .  .  #  .  .  .  .   .   .   .   .   .   #   .   .   .   .   .   .   .   .   .
CPD:      .  .  .  .  .  .  .  .  .  #  .   .   .   .   .   .   #   .   #   .   .   .   .   .   .   .
C0P:      .  .  .  .  .  .  .  .  .  .  .   .   .   .   .   .   .   .   #   #   #   .   .   .   .   .
          |              |         |              |                   |              |              |
          Micro          |    Meso |              |       Macro       |    Ultra     |
                         +--------+              +-------------------+
                          Beat zone               Structural zone

Legend: # = demanded horizon, . = not demanded
```

### 8.3 Mechanism Character Profiles

**Fast-response mechanisms** (Micro focus):
- **PPC** scans at H0/H3/H6 for onset transients and pre-attentive patterns
- **ASA** bridges H3/H6/H9 for auditory scene formation and stream segregation

**Beat-level mechanisms** (Meso focus):
- **BEP** tracks H6/H9/H11 for rhythmic entrainment at beat tempo
- **TPC** bridges H6/H12/H16 for pattern completion across beat-to-measure scales

**Structural mechanisms** (Macro focus):
- **TMH** spans H16/H18/H20/H22 for hierarchical temporal memory
- **MEM** extends into Ultra at H18/H20/H22/H25 for long-term consolidation
- **C0P** operates at H18/H19/H20 for contextual prediction within sections
- **SYN** links H12/H16/H18 for cross-timescale synchronization

**Multi-scale mechanisms**:
- **AED** jumps from Micro H6 to Macro H16, detecting arousal at two scales
- **CPD** spans H9/H16/H18, detecting structural change points

---

## 9. Demand Aggregation

### 9.1 Aggregation Pipeline

```
C3 Model Declaration          Mechanism Defaults          DemandTree Grouping
+-------------------+      +--------------------+      +-------------------+
| model.h3_demand = |      | mechanism adds its |      | Group by horizon: |
| (H3DemandSpec,    | ---> | default horizon    | ---> | H6: [(r3,m,l)...] |
|  H3DemandSpec,    |      | demands if model   |      | H9: [(r3,m,l)...] |
|  ...)             |      | does not override  |      | H16:[(r3,m,l)...] |
+-------------------+      +--------------------+      +-------------------+
                                                               |
                                                               v
                                                        Horizon Loop
                                                        +-------------------+
                                                        | For each horizon: |
                                                        |  1. weights once  |
                                                        |  2. for each      |
                                                        |     (r3,morph,law)|
                                                        |     -> compute    |
                                                        +-------------------+
```

### 9.2 Horizon Loop Optimization

The critical optimization: attention weights are computed **once per horizon**, then reused across all morphs and laws at that horizon. This means the cost scales with the number of *unique horizons demanded*, not the number of tuples.

```python
# Pseudocode for H3 computation
for horizon in demand_tree.unique_horizons():
    n_frames = HORIZON_FRAMES[horizon]
    for law in demand_tree.laws_at(horizon):
        window = select_window(t, n_frames, law)
        weights = compute_attention_weights(window, t, n_frames)  # once per (horizon, law)
        for (r3_idx, morph) in demand_tree.features_at(horizon, law):
            r3_slice = r3_tensor[:, :, r3_idx]
            result[(r3_idx, horizon, morph, law)] = apply_morph(r3_slice, window, weights, morph)
```

### 9.3 Unit-Level Demand Summary

| Unit | Models | Mechanisms | Primary Band | Est. Tuples | Largest Consumer |
|------|:------:|-----------|:------------:|:-----------:|:----------------:|
| SPU | 9 | PPC, TPC | Micro-Macro | ~450 | TPC at H6-H16 |
| STU | 14 | BEP, TMH, TPC | All bands | ~900 | TMH at H16-H22 |
| IMU | 15 | MEM, TMH, BEP, SYN, PPC | Macro-Ultra | ~1,200 | MEM at H18-H25 |
| ASU | 9 | ASA | Micro-Meso | ~360 | ASA at H3-H9 |
| NDU | 9 | ASA, PPC, TMH, MEM | All bands | ~400 | ASA at H3-H6 |
| MPU | 10 | BEP | Micro-Meso | ~500 | BEP at H6-H11 |
| PCU | 10 | PPC, TPC, MEM, AED, C0P, ASA | All bands | ~500 | C0P at H18-H20 |
| ARU | 10 | AED, CPD, C0P, ASA, MEM | Micro-Macro | ~500 | AED at H6+H16 |
| RPU | 10 | AED, CPD, C0P, TMH, MEM, BEP, ASA | All bands | ~400 | CPD at H9+H16 |
| **Total** | **96** | **10** | | **~5,210** | |

### 9.4 Demand Distribution by Band

```
Tuples
2000 |
     |       ####
1500 |       ####
     |       ####   ####
1000 |       ####   ####
     |  ###  ####   ####
 500 |  ###  ####   ####   ##
     |  ###  ####   ####   ##
   0 +------+------+------+------+
       Micro  Meso  Macro  Ultra
       ~900   ~1400 ~2400  ~500
```

Macro band dominates overall demand (~46%), reflecting the importance of musical structure (measures, phrases, sections) to perceptual processing. Micro and Meso are heavily demanded by fast-response and beat-level mechanisms. Ultra is sparse, used primarily by MEM.

---

## 10. Sparsity Analysis

### 10.1 Why Sparse?

The theoretical space of 294,912 tuples would require computing every possible morph for every R3 feature at every horizon under every law -- for every frame. This is computationally prohibitive and perceptually unnecessary. No brain region needs all 128 spectral features analyzed at all 32 timescales with all 24 statistical descriptors under all 3 causal laws.

Instead, each C3 model demands only the specific temporal descriptors relevant to its perceptual function. The aggregate demand (~8,600 tuples) occupies only ~2.9% of the theoretical space.

### 10.2 Computation Savings

| Metric | Dense | Sparse | Savings |
|--------|:-----:|:------:|:-------:|
| Tuples computed per frame | 294,912 | ~8,600 | 97.1% |
| Unique horizons (max) | 32 | ~15 | 53.1% |
| Memory (float32, per frame) | ~1.12 MB | ~33.6 KB | 97.0% |
| Morph calls per frame | 294,912 | ~8,600 | 97.1% |
| Attention weight sets | 32 x 3 = 96 | ~15 x 2 = ~30 | 68.8% |

### 10.3 Sparse Storage

H3 output is stored as a Python dictionary mapping 4-tuples to tensors:

```python
h3_output: Dict[Tuple[int, int, int, int], Tensor]
# Key: (r3_idx, horizon, morph, law)
# Value: Tensor of shape (B, T)

# Example access:
amplitude_velocity_200ms_memory = h3_output[(7, 6, 8, 0)]
roughness_periodicity_1s_integration = h3_output[(0, 16, 14, 2)]
```

A dense tensor representation would be `(B, T, 128, 32, 24, 3)` -- 6 dimensions, 294,912 features per frame. The sparse dict avoids allocating storage for the 97.1% of tuples that no model demands.

### 10.4 Tier Patterns

Different model tiers (alpha, beta, gamma) show characteristic demand patterns:

| Tier | Typical Tuples/Model | Horizon Spread | Morph Diversity |
|------|:-------------------:|:--------------:|:---------------:|
| Alpha | ~60-120 | 3-6 horizons | 10-18 morphs |
| Beta | ~40-80 | 2-4 horizons | 8-14 morphs |
| Gamma | ~30-50 | 2-3 horizons | 6-10 morphs |

Alpha models (highest complexity) tend to demand more horizons and more diverse morphs. Gamma models (lowest complexity) focus on fewer horizons with core morphs (M0, M1, M2, M8, M18).

---

## 11. R3 v2 Expansion Impact

### 11.1 Dimensional Growth

The R3 expansion from 49D to 128D directly scales the H3 address space:

| Metric | R3 v1 (49D) | R3 v2 (128D) | Change |
|--------|:-----------:|:------------:|:------:|
| Theoretical space | 112,896 | 294,912 | +161% |
| R3 index range | [0:48] | [0:127] | +79 features |
| Estimated tuples | ~5,200 | ~8,600 | +65% |
| Occupancy | ~4.6% | ~2.9% | -1.7pp |

### 11.2 New R3 Groups as Temporal Demand Targets

The 6 new R3 groups (F-K) introduce 79 new spectral features, each a potential target for temporal morphology. The temporal priority varies by group:

| R3 Group | Range | Dim | Temporal Priority | Rationale |
|----------|:-----:|:---:|:-----------------:|-----------|
| F: Pitch & Chroma | [49:65] | 16 | **HIGH** | Melodic contour, pitch drift, chroma stability are inherently temporal |
| G: Rhythm & Groove | [65:75] | 10 | **HIGH** | Tempo stability, groove evolution, beat strength trends |
| H: Harmony & Tonality | [75:87] | 12 | **HIGH** | Key change detection, harmonic rhythm, tonnetz trajectories |
| I: Information & Surprise | [87:94] | 7 | **MEDIUM** | Entropy trends, surprise accumulation over sections |
| J: Timbre Extended | [94:114] | 20 | **MEDIUM** | MFCC trajectories, timbral evolution over phrases |
| K: Modulation & Psycho. | [114:128] | 14 | **MEDIUM** | Modulation rate stability, psychoacoustic feature trends |

### 11.3 Estimated New Demand

| Source | Tuples |
|--------|:------:|
| Existing demand (v1 features, r3_idx 0-48) | ~5,200 |
| F: Pitch & Chroma temporal demands | ~800 |
| G: Rhythm & Groove temporal demands | ~600 |
| H: Harmony & Tonality temporal demands | ~700 |
| I: Information & Surprise temporal demands | ~400 |
| J: Timbre Extended temporal demands | ~500 |
| K: Modulation & Psychoacoustic temporal demands | ~400 |
| **Total estimated** | **~8,600** |

### 11.4 High-Priority Temporal Demands (Examples)

**Pitch & Chroma (F)**:
- `(61, H18, M18, L0)` -- pitch_height trend over 2s (memory): melodic contour direction
- `(49:61, H16, M19, L2)` -- chroma stability at 1s (integration): tonal center strength
- `(62, H20, M20, L0)` -- pitch_class_entropy entropy at 5s: tonal ambiguity evolution

**Rhythm & Groove (G)**:
- `(65, H22, M19, L0)` -- tempo_estimate stability at 15s: tempo consistency
- `(67, H12, M8, L1)` -- pulse_clarity velocity at 525ms: beat clarity change prediction
- `(71, H18, M18, L2)` -- groove_index trend at 2s: groove intensity trajectory

**Harmony & Tonality (H)**:
- `(75, H20, M2, L0)` -- key_clarity std at 5s: key stability measurement
- `(83, H16, M22, L2)` -- harmonic_change peaks at 1s: harmonic rhythm detection
- `(76:82, H18, M18, L0)` -- tonnetz trend at 2s: tonal space drift direction

---

## 12. Code Architecture

### 12.1 File Structure

```
mi_beta/
|-- ear/
|   |-- h3/
|   |   |-- __init__.py       H3Extractor: top-level entry point
|   |   |-- demand.py         DemandTree: demand aggregation and grouping
|   |   |-- horizon.py        EventHorizon: horizon constants and frame conversion
|   |   |-- morph.py          MorphComputer: 24-method dispatch table
|   |   |-- attention.py      compute_attention_weights: kernel computation
|   |
|-- core/
    |-- constants.py          HORIZON_MS, MORPH_NAMES, LAW_NAMES, MORPH_SCALE
```

### 12.2 Module Responsibilities

#### `__init__.py` -- H3Extractor

The top-level class that orchestrates H3 computation:
- Receives R3 tensor `(B, T, 128)` and a `DemandTree`
- Iterates unique horizons, computes attention weights, dispatches morph calls
- Returns sparse dict `{4-tuple: Tensor(B, T)}`

#### `demand.py` -- DemandTree

Aggregates and organizes H3 demands from all C3 models:
- Collects `H3DemandSpec` tuples from all models
- Deduplicates (same tuple demanded by multiple models computed only once)
- Groups by horizon for efficient iteration
- Provides iteration methods: `unique_horizons()`, `laws_at(h)`, `features_at(h, l)`

#### `horizon.py` -- EventHorizon

Manages the 32 horizon definitions:
- `HORIZON_MS`: list of 32 durations in milliseconds
- `HORIZON_FRAMES`: derived frame counts at 172.27 Hz
- `horizon_to_frames(h)`: converts horizon index to frame count
- `horizon_band(h)`: returns band name (Micro/Meso/Macro/Ultra)

#### `morph.py` -- MorphComputer

Implements all 24 morph functions via a dispatch table:
- `compute(morph_idx, values, weights)`: dispatches to the appropriate method
- Each morph function takes attention-weighted values and returns a scalar per frame
- MORPH_SCALE normalization applied after computation

#### `attention.py` -- compute_attention_weights

Computes the exponential decay kernel:
- `compute_attention_weights(window, t, n_frames)`: returns normalized weight array
- Formula: `A(dt) = exp(-3 * |dt| / n_frames)`
- Weights are normalized to sum to 1.0

### 12.3 Constants Reference

The following constants are defined in `mi_beta/core/constants.py`:

```python
# 32 horizons in milliseconds
HORIZON_MS = [
    5.8, 11.6, 17.4, 23.2, 34.8, 46.4, 200, 250,           # Micro H0-H7
    300, 350, 400, 450, 525, 600, 700, 800,                  # Meso H8-H15
    1000, 1500, 2000, 3000, 5000, 8000, 15000, 25000,        # Macro H16-H23
    36000, 60000, 120000, 200000, 414000, 600000, 800000, 981000  # Ultra H24-H31
]

# 24 morph names
MORPH_NAMES = [
    "value", "mean", "std", "median", "max", "range",
    "skewness", "kurtosis", "velocity", "velocity_mean",
    "velocity_std", "acceleration", "acceleration_mean",
    "acceleration_std", "periodicity", "smoothness",
    "curvature", "shape_period", "trend", "stability",
    "entropy", "zero_crossings", "peaks", "symmetry"
]

# 3 law names
LAW_NAMES = ["memory", "prediction", "integration"]

# Attention kernel decay constant
ATTENTION_DECAY = 3.0

# Frame rate
FRAME_RATE = 172.27  # Hz (hop_length=256, sr=44100)
```

### 12.4 Execution Flow

```
C3 Model Initialization
    |
    v
Each model registers H3DemandSpec tuples
    |
    v
DemandTree.build() -- aggregate, deduplicate, group by horizon
    |
    v
Per-frame execution:
    |
    +-- For each unique horizon h in demand_tree:
    |     |
    |     +-- n = HORIZON_FRAMES[h]
    |     |
    |     +-- For each demanded law l at horizon h:
    |     |     |
    |     |     +-- window = select_window(t, n, l)
    |     |     +-- weights = compute_attention_weights(window, t, n)
    |     |     |
    |     |     +-- For each demanded (r3_idx, morph) at (h, l):
    |     |           |
    |     |           +-- slice = r3_tensor[:, window, r3_idx]
    |     |           +-- raw = MorphComputer.compute(morph, slice, weights)
    |     |           +-- normalized = normalize(raw, MORPH_SCALE[morph])
    |     |           +-- output[(r3_idx, h, morph, l)] = normalized
    |     |
    |     +-- (next law)
    |
    +-- (next horizon)
    |
    v
Return: Dict[(r3_idx, horizon, morph, law)] -> Tensor(B, T)
```

---

## 13. Cross-References

### 13.1 H3 Documentation Tree

| Document | Path | Content |
|----------|------|---------|
| Master index | [H3/00-INDEX.md](00-INDEX.md) | Directory structure, summary tables |
| **This document** | [H3/H3-TEMPORAL-ARCHITECTURE.md](H3-TEMPORAL-ARCHITECTURE.md) | Definitive architecture spec |
| Horizon catalog | [H3/Registry/HorizonCatalog.md](Registry/HorizonCatalog.md) | All 32 horizons, full metadata |
| Morph catalog | [H3/Registry/MorphCatalog.md](Registry/MorphCatalog.md) | All 24 morphs, formulas, MORPH_SCALE |
| Law catalog | [H3/Registry/LawCatalog.md](Registry/LawCatalog.md) | All 3 laws, kernel formulas |
| Demand address space | [H3/Registry/DemandAddressSpace.md](Registry/DemandAddressSpace.md) | 4-tuple system, sparsity analysis |
| Band documentation | [H3/Bands/](Bands/) | Per-band detailed analysis (Micro/Meso/Macro/Ultra) |
| Morph categories | [H3/Morphology/](Morphology/) | Per-category morph documentation |
| Law analysis | [H3/Laws/](Laws/) | Per-law detailed analysis (L0/L1/L2) |
| R3 v2 impact | [H3/Expansion/R3v2-H3-Impact.md](Expansion/R3v2-H3-Impact.md) | 128D expansion impact on H3 |

### 13.2 C3 Integration Documents

| Document | Path | Content |
|----------|------|---------|
| H3DemandSpec contract | [C3/Contracts/H3DemandSpec.md](../C3/Contracts/H3DemandSpec.md) | 4-tuple demand interface |
| H3 demand matrix | [C3/Matrices/H3-Demand.md](../C3/Matrices/H3-Demand.md) | All-model demand aggregation |
| Mechanism index | [C3/Mechanisms/00-INDEX.md](../C3/Mechanisms/00-INDEX.md) | All 10 mechanism specifications |
| Per-unit demand | [H3/Demand/](Demand/) | SPU/STU/IMU/ASU/NDU/MPU/PCU/ARU/RPU demand tables |

### 13.3 R3 Integration Documents

| Document | Path | Content |
|----------|------|---------|
| R3 architecture | [R3/R3-SPECTRAL-ARCHITECTURE.md](../R3/R3-SPECTRAL-ARCHITECTURE.md) | 128D spectral space definition |
| Feature catalog | [R3/Registry/FeatureCatalog.md](../R3/Registry/FeatureCatalog.md) | All 128 R3 features with indices |
| Dimension map | [R3/Registry/DimensionMap.md](../R3/Registry/DimensionMap.md) | Group-to-index mapping |

### 13.4 Code References

| Component | Code Path | Role |
|-----------|-----------|------|
| H3 extractor | `mi_beta/ear/h3/__init__.py` | Top-level H3 computation |
| Demand tree | `mi_beta/ear/h3/demand.py` | Demand aggregation |
| Event horizon | `mi_beta/ear/h3/horizon.py` | Horizon constants |
| Morph computer | `mi_beta/ear/h3/morph.py` | 24-method morph dispatch |
| Attention kernel | `mi_beta/ear/h3/attention.py` | Kernel weight computation |
| Constants | `mi_beta/core/constants.py` | HORIZON_MS, MORPH_NAMES, LAW_NAMES, MORPH_SCALE |

---

## Appendix A: Quick Reference Card

```
H3 = Temporal Morphology Layer
    Input:  R3 tensor (B, T, 128) @ 172.27 Hz
    Output: sparse dict {(r3_idx, horizon, morph, law): (B, T)}

Address:  (r3_idx, horizon, morph, law)
          128       32       24     3     = 294,912 theoretical
                                          = ~8,600 actual (~2.9%)

Kernel:   A(dt) = exp(-3|dt|/H), boundary ~5%

Horizons: Micro  H0-H7   5.8ms-250ms     onset, attack, transient
          Meso   H8-H15  300ms-800ms     beat, quarter note, motif
          Macro  H16-H23 1s-25s          measure, section, passage
          Ultra  H24-H31 36s-981s        movement, piece, full work

Morphs:   Level      M0,M1,M3,M4         value, mean, median, max
          Dispersion M2,M5,M19            std, range, stability
          Shape      M6,M7,M16,M23        skewness, kurtosis, curvature, symmetry
          Dynamics   M8-M13,M15,M18,M21   velocity, acceleration, smoothness, trend
          Rhythm     M14,M17,M22          periodicity, shape_period, peaks
          Information M20                 entropy

Laws:     L0 Memory      past->present    causal exponential decay
          L1 Prediction  present->future  anticipatory forward
          L2 Integration past<->future    bidirectional symmetric

Code:     mi_beta/ear/h3/ (5 files)
          mi_beta/core/constants.py
```
