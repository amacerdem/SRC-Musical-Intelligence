# H³ Ontology & Boundary Specification

**Version**: 1.0.0
**Status**: FROZEN (ontological boundaries)
**Date**: 2026-02-16
**Depends on**: R³ Ontology v1.0.0 (R3-ONTOLOGY-BOUNDARY.md)

---

## 1. Formal Definition

**H³ is a Multi-Scale Temporal Morphology Engine.**

It answers one question: **"How does this acoustic feature behave over time?"**

H³ takes each R³ feature and computes deterministic, model-free statistical descriptors over sliding windows at multiple temporal scales. It transforms the instantaneous spectral snapshot (R³) into a temporal geometry that describes motion, stability, rhythm, and shape — without modelling the listener's expectations, memory, or predictions.

### Boundary Sentence

> H³ = the set of deterministic, stateless, window-based statistical transforms applied to R³ features, parameterized by (feature, scale, operator, direction), requiring no accumulated state, no listener model, no prediction, and no cross-feature binding.

### What H³ Is

- A **stateless** window operator (no memory beyond the current window)
- A **deterministic** mathematical transform (same input window → same output)
- A **single-feature** processor (each computation operates on one R³ index)
- A **demand-driven** system (only computes what C³ models request)
- A **scale-parameterized** engine (the same operator at different horizons yields different results)

### What H³ Is Not

- Not a prediction engine (C³ handles expectation and surprise)
- Not a feature binder (C³ handles cross-feature interactions)
- Not a memory system (C³ maintains belief states and temporal priors)
- Not a reward/value system (C³ computes salience and affective value)
- Not biologically exact (mathematical clarity is the design principle; neuroscience is validation, not constraint)

### The R³ → H³ → C³ Stack

```
R³: "What does the sound look like right now?"    (frame-local, 97D)
     ↓
H³: "How does each feature behave over time?"     (window-local, sparse)
     ↓
C³: "What does this temporal pattern mean?"        (model-based, cognitive)
```

Each layer answers a fundamentally different question. No layer may answer another layer's question.

---

## 2. Statelessness Principle

H³ maintains **zero state** between computations. Every output is a pure function of the window content.

### What Stateless Means

```python
# H³ pseudocode — pure function of window
def h3_compute(r3_feature: Tensor, window: Tensor, weights: Tensor) -> float:
    """
    No self._state
    No self._running_average
    No self._frame_count
    No self._previous_output
    """
    return morph_function(window, weights)
```

### The Statelessness Test

If the implementation contains any of these patterns, it violates the statelessness principle:

```python
# VIOLATION: temporal state beyond window
self._ema = (1 - alpha) * self._ema + alpha * x          # EMA
self._count += 1                                          # accumulated counter
self._baseline = self._baseline * decay + x * (1-decay)   # running baseline
if self._prev_output is not None:                          # cross-call dependency
```

Every H³ computation must be reproducible from the window content alone. Given the same R³ feature values within a window, the same H³ output must result, regardless of what happened before or after that window.

### Consequence for Execution

H³ computations at different time steps are **embarrassingly parallel**. Any frame `t` can be computed independently of any other frame, because there is no temporal dependency between outputs. The current `torch.unfold` vectorization exploits this property.

---

## 3. Inclusion Rules

A temporal descriptor belongs in H³ if and only if ALL of the following hold:

### Rule 1: Window Locality

The computation uses only the content of a single sliding window. The window is defined by a horizon (scale), a law (direction), and an attention kernel. Nothing outside the window is accessed.

### Rule 2: Single-Feature Operation

The computation operates on exactly one R³ feature index. It does not combine, multiply, or correlate values from different R³ features.

- Allowed: velocity of `spectral_flux` = `flux(t) - flux(t-1)`
- Forbidden: correlation of `spectral_flux` and `amplitude` = binding

### Rule 3: No Listener Model

The computation does not require a model of the listener's expectations, experience, or musical knowledge. It describes **what the signal does over time**, not **what the listener expects**.

- Allowed: periodicity = autocorrelation peak within window (signal property)
- Forbidden: surprise = divergence from expected periodicity (listener model)

### Rule 4: No Accumulated State

The computation does not depend on any information from outside the current window. No EMA, no running baselines, no frame counters, no warmup confidence ramps.

### Rule 5: Deterministic and Model-Free

The computation uses no learned parameters, trained weights, or fitted models. Every morph is a closed-form function of the window content and the attention kernel.

---

## 4. Exclusion Rules

A temporal descriptor must NOT be in H³ if ANY of the following hold:

| Violation | Example | Destination |
|-----------|---------|-------------|
| Requires running baseline | surprise = KL(x(t) ∥ baseline) | C³ |
| Requires prediction model | expected_periodicity - actual_periodicity | C³ |
| Combines multiple R³ features | correlation(flux, amplitude) | C³ input layer |
| Requires belief state | Bayesian posterior over key | C³ |
| Requires reward weighting | salience = prediction_error × reward | C³ |
| Requires cross-window dependency | trend_of_trend (H³ output as H³ input) | C³ |

### The Prediction Test

If a descriptor's name or formula contains any of: "expected," "predicted," "surprising," "belief," "prior," "posterior," "reward," "salience," "error" — it almost certainly belongs in C³, not H³.

H³ computes: **"What is the periodicity?"**
C³ computes: **"Is this periodicity expected?"**

---

## 5. The 4-Tuple Address Space

Every H³ descriptor is uniquely addressed by a 4-tuple:

```
(r3_idx, horizon, morph, law)
```

| Field | Range | Meaning |
|-------|-------|---------|
| `r3_idx` | 0–96 | Which R³ feature (post-ontology-freeze indexing) |
| `horizon` | 0–31 | Which temporal scale (H0–H31) |
| `morph` | 0–23 | Which statistical operator (M0–M23) |
| `law` | 0–2 | Which window direction (L0–L2) |

**Theoretical space**: 97 × 32 × 24 × 3 = **223,488 tuples**
**Active demand**: ~8,600 tuples (~3.9% occupancy)
**Design**: Sparse — only demanded tuples are computed

---

## 6. Morph Catalogue

24 morphs organized in 6 families. Every morph is a pure function of the window content `x[0..W-1]` and attention weights `w[0..W-1]`.

### 6.1 Distribution Family (M0–M7)

Describe the statistical shape of feature values within the window.

| M# | Name | Formula | Signed | Min W |
|----|------|---------|--------|-------|
| M0 | weighted_mean | Σ(w_i · x_i) / Σ(w_i) | No | 1 |
| M1 | mean | (1/W) · Σ x_i | No | 1 |
| M2 | std | √(var(x)) | No | 2 |
| M3 | median | median(x) | No | 1 |
| M4 | max | max(x) | No | 1 |
| M5 | range | max(x) − min(x) | No | 2 |
| M6 | skewness | E[(x−μ)³] / σ³ | **Yes** | 3 |
| M7 | kurtosis | E[(x−μ)⁴] / σ⁴ − 3 | No | 4 |

### 6.2 Dynamics Family (M8–M13, M15, M18, M21)

Describe the temporal motion of the feature.

| M# | Name | Formula | Signed | Min W | Horizon-Dependent? |
|----|------|---------|--------|-------|-------------------|
| M8 | velocity | x[W-1] − x[W-2] | **Yes** | 2 | **No** — always ±1 frame edge difference |
| M9 | velocity_mean | mean(dx/dt) over window | **Yes** | 3 | Yes |
| M10 | velocity_std | std(dx/dt) over window | No | 3 | Yes |
| M11 | acceleration | dx²/dt² at edge | **Yes** | 3 | **No** — always ±2 frame edge |
| M12 | acceleration_mean | mean(d²x/dt²) over window | **Yes** | 4 | Yes |
| M13 | acceleration_std | std(d²x/dt²) over window | No | 4 | Yes |
| M15 | smoothness | 1 / (1 + velocity_std) | No | 3 | Yes |
| M18 | trend | linear regression slope over W | **Yes** | 3 | **Yes** — this is scale-dependent velocity |
| M21 | zero_crossings | count(sign_changes(x − mean(x))) / W | No | 3 | Yes |

**Critical distinction — M8 vs M18**:
- **M8 (velocity)**: Instantaneous rate of change. Always `x(t) − x(t-1)`. Same value regardless of horizon. Use when you need "what is the feature doing RIGHT NOW?"
- **M18 (trend)**: Scale-dependent rate of change. Regression slope over entire window. Different values at different horizons. Use when you need "what is the overall direction at this temporal scale?"

Requesting M8 at multiple horizons is **redundant** (same computation, same result). Requesting M18 at multiple horizons is **informative** (different scales reveal different trends).

### 6.3 Rhythm Family (M14, M17, M22)

Describe periodic structure within the window.

| M# | Name | Formula | Signed | Min W |
|----|------|---------|--------|-------|
| M14 | periodicity | max(autocorr(x)[lag_min:]) / autocorr(x)[0] | No | 8 |
| M17 | shape_period | argmax(autocorr(x)[lag_min:]) in frames | No | 8 |
| M22 | peaks | count(local_maxima(x)) / W | No | 3 |

**Boundary note**: M14 computes autocorrelation **within the window only**. No reference distribution, no expected periodicity, no baseline. This is a signal property, not a listener property.

### 6.4 Information Family (M20)

| M# | Name | Formula | Signed | Min W |
|----|------|---------|--------|-------|
| M20 | entropy | −Σ p_i · log(p_i) where p = histogram(x, 16 bins) | No | 4 |

**Boundary note**: M20 computes Shannon entropy of the **window's value distribution**. No comparison to any baseline. This measures "how spread out are the feature values within this window?" — a statistical shape descriptor, not an information-theoretic surprise measure.

### 6.5 Symmetry Family (M16, M19, M23)

| M# | Name | Formula | Signed | Min W |
|----|------|---------|--------|-------|
| M16 | curvature | mean(|d²x/dt²|) | **Yes** | 3 |
| M19 | stability | 1 / (1 + std(x)) | No | 2 |
| M23 | symmetry | corr(x, reverse(x)) | **Yes** | 3 |

### 6.6 Summary

| Family | Morphs | Count | Purpose |
|--------|--------|-------|---------|
| Distribution | M0–M7 | 8 | Shape of values in window |
| Dynamics | M8–M13, M15, M18, M21 | 9 | Temporal motion |
| Rhythm | M14, M17, M22 | 3 | Periodic structure |
| Information | M20 | 1 | Value distribution complexity |
| Symmetry | M16, M19, M23 | 3 | Temporal shape properties |
| **Total** | | **24** | |

---

## 7. Horizon Scale

### 7.1 Principle

Horizons are **quasi-logarithmically spaced** across four perceptual bands:

| Band | Range | Duration | Frames | Count | Musical Analogy |
|------|-------|----------|--------|-------|-----------------|
| **Micro** | H0–H7 | 5.8ms–250ms | 1–43 | 8 | Note attacks, transients |
| **Meso** | H8–H15 | 300ms–800ms | 52–138 | 8 | Beats, short phrases |
| **Macro** | H16–H23 | 1s–25s | 172–4307 | 8 | Measures, sections |
| **Ultra** | H24–H31 | 36s–981s | 6202–168999 | 8 | Movements, full works |

### 7.2 Design Rationale

Log spacing follows the principle of **relative temporal resolution**: the difference between 100ms and 200ms is perceptually significant, but the difference between 100s and 100.1s is not. Each doubling of time scale adds roughly equal perceptual information.

This aligns (but is not constrained by) Temporal Receptive Window (TRW) durations observed in auditory cortex hierarchies — shorter windows in primary auditory cortex, progressively longer windows in association areas.

### 7.3 Architectural Pivot: H6 = 200ms

H6 (200ms, 34 frames) is the **architectural pivot point**:
- Below H6: sub-note processing (attacks, micro-timing, timbral fluctuations)
- Above H6: supra-note processing (beats, phrases, sections)
- At H6: the boundary between "sound quality" and "musical structure"

This is the densest demand region — the most C³ models request H³ features at or near H6.

### 7.4 What Is Frozen

The **principle** of quasi-logarithmic spacing across four bands is frozen. The **specific values** of individual horizons may be adjusted (e.g., H3 correction from 23ms to 70ms) as long as:
1. The count remains 32 (8 per band)
2. The log-spacing property is maintained
3. Band boundaries are preserved (micro < 300ms, meso < 1s, macro < 30s)

---

## 8. Law Types (Window Orientation)

### 8.1 Principle

Laws define the **direction** of the sliding window relative to the current frame. They are purely geometric — they specify WHERE the window sits, not HOW the content is interpreted.

### 8.2 Three Laws

| Law | Code | Ontological Name | Window Position | Attention Peak |
|-----|------|-----------------|-----------------|----------------|
| L0 | LAW_MEMORY | **Memory** | [t−W+1, t] | Current frame (t) |
| L1 | LAW_PREDICTION | **Forward** | [t, t+W−1] | Future boundary (t+W−1) |
| L2 | LAW_INTEGRATION | **Integration** | [t−W/2, t+W/2] | Current frame (t) |

**Critical terminological correction**: L1 is called `LAW_PREDICTION` in code, but its ontological meaning is **"forward window direction"**. L1 does NOT predict anything. It selects a future window and computes the same deterministic morphs. The word "prediction" in the code name is a historical artifact that will be corrected in the next code refactoring.

**Actual prediction** (expectation models, surprise computation, prediction error) belongs exclusively in C³.

### 8.3 Attention Kernel

All three laws use the same exponential attention kernel:

```
weight(i) = exp(−λ · (1 − position(i)))
```

Where:
- `λ = 3.0` (ATTENTION_DECAY constant)
- `position(i)` ∈ [0, 1] maps window frames from oldest (0) to newest (1)
- Newest frame: weight = 1.0
- Oldest frame: weight ≈ 0.05

The kernel is a **recency bias** for L0/memory windows: recent frames contribute more than distant frames. For L1/forward windows, it becomes a **proximity bias**: frames closer to the present contribute more. For L2/integration, it becomes a **centrality bias**: frames near the center contribute more.

### 8.4 Causal vs Non-Causal

| Law | Causal? | Latency | Use Case |
|-----|---------|---------|----------|
| L0 (Memory) | Yes | 0 frames | Real-time processing, memory-dependent features |
| L1 (Forward) | No | W frames | Offline analysis, anticipatory features |
| L2 (Integration) | No | W/2 frames | Offline analysis, context-symmetric features |

For real-time applications, only L0 (Memory) outputs are available without latency. L1 and L2 require buffering future frames.

### 8.5 What Is Frozen

The **three-law system** (backward, forward, bidirectional) is frozen. The **attention kernel formula** is frozen. The specific value of `ATTENTION_DECAY` may be tuned.

---

## 9. Warm-Up Zones

### 9.1 Definition

A warm-up zone is the region at the beginning (L0, L2) or end (L1, L2) of the audio where the window cannot be fully populated. H³ outputs in warm-up zones are **zero** (undefined), not interpolated or estimated.

### 9.2 Warm-Up Frames by Law

| Law | Start Warm-Up | End Warm-Up |
|-----|---------------|-------------|
| L0 (Memory) | W − 1 frames | 0 |
| L1 (Forward) | 0 | W − 1 frames |
| L2 (Integration) | W/2 frames | W/2 frames |

### 9.3 Consequence

For very long horizons (H31 = 981s), the warm-up zone is enormous. Ultra-band features are only valid for the middle portion of long recordings. This is by design — H³ does not "guess" what happened before the recording started.

---

## 10. Demand-Driven Computation

### 10.1 Principle

H³ computes **only** what C³ models demand. The theoretical address space is 223,488 tuples. Active demand is ~8,600 tuples (~3.9% occupancy). This sparsity is a design feature, not a limitation.

### 10.2 Demand Flow

```
C³ model declares h3_demand → aggregate_demands() → DemandTree.build()
→ H3Executor.execute(r3_tensor, demand_tree) → sparse output dict
```

### 10.3 Demand Deduplication

If two C³ models both demand `(12, 6, 1, 0)` (R³ feature 12, H6, mean, memory), the computation happens once. The result is shared.

---

## 11. What Belongs to C³ (Not H³)

The following temporal processing capabilities belong in C³, not H³:

### 11.1 Prediction Error

```
C³: error = H³_output − C³_prediction
```

H³ provides the "what happened" (temporal morphology). C³ provides the "what was expected" (prediction model). The error is computed in C³.

### 11.2 Temporal Feature Binding

```
C³: interaction = H³(flux, H6, trend, memory) × H³(amplitude, H6, trend, memory)
```

H³ computes each feature's temporal morphology independently. C³ binds them together. (Same principle as R³ → C³ for spatial binding.)

### 11.3 Surprise / Information-Theoretic Measures

```
C³: surprise = KL(current_distribution ∥ baseline_distribution)
```

Where `baseline_distribution` is an accumulated model of "what's normal" — this is exactly the kind of temporal state that H³ must not maintain.

### 11.4 Trend-of-Trend (Hierarchical Composition)

```
C³: meta_trend = trend(H³(flux, H18, trend, memory)) over H23
```

H³ does not take its own output as input. If a C³ model needs "how does the 2-second trend change over 25 seconds," it must compute this in its own layers using H³ outputs at both scales.

### 11.5 Adaptive Horizon Selection

```
C³: relevant_horizon = argmax(salience(H³_output_at_each_horizon))
```

H³ computes at fixed, declared horizons. C³ may select among them based on context, but H³ does not adapt its scales based on signal content.

---

## 12. Relationship to Neuroscience

### 12.1 Design Principle

H³ is designed with **mathematical clarity as the primary constraint** and **neuroscience as a validation check**. The morph catalogue, horizon scale, and law types are chosen for mathematical elegance and computational efficiency. Their alignment with known neuroscience (oscillatory bands, TRWs, cortical layers) is a sanity check, not a design constraint.

### 12.2 Where Biology Validates the Design

| H³ Component | Biological Correlate | Status |
|-------------|---------------------|--------|
| Micro band (H0–H7) | Gamma oscillations (30–100 Hz) | Validated |
| Meso band (H8–H15) | Beta-theta oscillations (4–30 Hz) | Validated |
| L0 (Memory) | Echoic memory, sensory trace | Validated |
| Attention kernel | Recency effects in auditory memory | Consistent |
| Morph catalogue | Auditory cortex response properties | Partially consistent |

### 12.3 Where Biology Diverges

| H³ Component | Biological Reality | H³ Simplification |
|-------------|-------------------|-------------------|
| Ultra band (H24–H31) | No known neural TRW > 60s | Mathematical extrapolation |
| L1 (Forward) | Requires prediction models in biology | H³ uses acausal future window |
| Statelessness | Auditory cortex has persistent state | H³ is pure window operator |
| Attention kernel | Real attention is content-dependent | H³ uses fixed exponential |

These divergences are **accepted engineering trade-offs**. H³ is not a brain simulation. It is a mathematical tool that produces temporal descriptors useful for C³ cognitive models.

---

## 13. Freeze Policy

### What Is Frozen (this document)

1. **The definition** (§1): H³ is a multi-scale temporal morphology engine
2. **The statelessness principle** (§2): No state beyond the current window
3. **The five inclusion rules** (§3): window-local, single-feature, no listener model, no state, deterministic
4. **The exclusion rules** (§4): no prediction, no binding, no baseline comparison
5. **The 4-tuple addressing scheme** (§5): (r3_idx, horizon, morph, law)
6. **The three-law system** (§8): memory, forward, integration (window directions only)
7. **The morph family structure** (§6): 6 families, closed catalogue
8. **The boundary sentence**: immutable reference

### What Can Still Evolve

1. **Morph count**: New morphs can be added if they pass all five inclusion rules
2. **Morph algorithms**: Specific implementations can be improved
3. **Horizon values**: Individual horizon durations can be adjusted within band constraints
4. **Attention decay**: The λ parameter may be tuned
5. **Normalization scales**: MORPH_SCALE values may be adjusted
6. **Demand volume**: More or fewer tuples may be requested as C³ models evolve

### Morph Proposal Gate

Any proposed new H³ morph must pass this checklist:

- [ ] Computable from window content and attention weights only?
- [ ] Operates on a single R³ feature (no cross-feature)?
- [ ] No running baseline, EMA, or accumulated state?
- [ ] No prediction, surprise, or expectation modelling?
- [ ] No learned parameters or trained weights?
- [ ] Not redundant with an existing morph? (correlation < 0.95 across test set)
- [ ] At least 4 C³ models demand it? (pragmatic threshold)

---

## Appendix A: Complete Morph Index

```
DISTRIBUTION FAMILY
  M0   weighted_mean        Σ(w·x) / Σ(w)                    unsigned
  M1   mean                 (1/W)·Σx                          unsigned
  M2   std                  √(var(x))                         unsigned
  M3   median               median(x)                         unsigned
  M4   max                  max(x)                            unsigned
  M5   range                max(x) − min(x)                   unsigned
  M6   skewness             E[(x−μ)³] / σ³                    SIGNED
  M7   kurtosis             E[(x−μ)⁴] / σ⁴ − 3               unsigned

DYNAMICS FAMILY
  M8   velocity             x[W−1] − x[W−2]                  SIGNED    ← horizon-independent
  M9   velocity_mean        mean(Δx)                          SIGNED
  M10  velocity_std         std(Δx)                           unsigned
  M11  acceleration         Δ²x at edge                       SIGNED    ← horizon-independent
  M12  acceleration_mean    mean(Δ²x)                         SIGNED
  M13  acceleration_std     std(Δ²x)                          unsigned
  M15  smoothness           1/(1 + velocity_std)              unsigned
  M18  trend                OLS slope over W                  SIGNED    ← horizon-dependent
  M21  zero_crossings       sign_changes(x−μ) / W            unsigned

RHYTHM FAMILY
  M14  periodicity          max(autocorr[lag_min:]) / R[0]    unsigned
  M17  shape_period         argmax(autocorr[lag_min:])        unsigned
  M22  peaks                count(local_maxima) / W           unsigned

INFORMATION FAMILY
  M20  entropy              −Σ p_i·log(p_i), 16-bin hist     unsigned

SYMMETRY FAMILY
  M16  curvature            mean(|Δ²x|)                      SIGNED
  M19  stability            1/(1 + std(x))                    unsigned
  M23  symmetry             corr(x, reverse(x))              SIGNED

Signed morphs: {M6, M8, M9, M11, M12, M16, M18, M23}
```

## Appendix B: Horizon Table

```
MICRO BAND (H0–H7): 5.8ms – 250ms
  H0    5.8ms      1 frame     Single frame (R³ passthrough)
  H1   11.6ms      2 frames    Fine timing
  H2   17.4ms      3 frames    Sub-onset grouping
  H3   23.2ms      4 frames    Consonant onset
  H4   34.8ms      6 frames    Short attack transient
  H5   46.4ms      8 frames    Phoneme boundary
  H6  200.0ms     34 frames    ★ Architectural pivot (16th note @75 BPM)
  H7  250.0ms     43 frames    8th note subdivision

MESO BAND (H8–H15): 300ms – 800ms
  H8   300ms      52 frames    Fast beat (200 BPM)
  H9   350ms      60 frames    Primary beat (171 BPM)
  H10  400ms      69 frames    Moderate beat (150 BPM)
  H11  450ms      78 frames    Walking tempo (133 BPM)
  H12  525ms      90 frames    Two-beat motif
  H13  600ms     103 frames    Standard phrase
  H14  700ms     121 frames    Extended phrase
  H15  800ms     138 frames    Phrase boundary

MACRO BAND (H16–H23): 1s – 25s
  H16    1s      172 frames    Single measure @240 BPM
  H17  1.5s      259 frames    Single measure @160 BPM
  H18    2s      345 frames    Single measure @120 BPM
  H19    3s      517 frames    Two-measure phrase
  H20    5s      861 frames    Short passage
  H21    8s    1,378 frames    Extended passage/verse
  H22   15s    2,584 frames    Musical section
  H23   25s    4,307 frames    Multi-section span

ULTRA BAND (H24–H31): 36s – 981s
  H24   36s    6,202 frames    Movement intro
  H25   60s   10,336 frames    Short movement
  H26  120s   20,672 frames    Standard movement
  H27  200s   34,453 frames    Extended movement
  H28  414s   71,319 frames    Multi-movement
  H29  600s  103,359 frames    Half work
  H30  800s  137,812 frames    Near-complete work
  H31  981s  168,999 frames    Full work (~16 min)
```

---

*This document defines the ontological boundaries of H³. Together with R³ Ontology v1.0.0, it establishes the perceptual substrate upon which C³ cognitive models operate. The statelessness principle (§2), inclusion/exclusion rules (§3–4), and boundary sentence (§1) are frozen at v1.0.0. Implementation details evolve freely within these boundaries.*
