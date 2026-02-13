# H3 Law L1 -- Prediction (Present --> Future)

**Version**: 2.0.0
**Law index**: 1
**Direction**: Anticipatory (forward-looking)
**Window**: `[t, min(T, t+n))`
**Kernel**: `A(dt) = exp(-3|t'-t|/H)` for `t'` in `[t, t+n-1]`
**Causality**: Non-causal -- requires future frames
**Latency**: n frames (full horizon duration)
**Code reference**: `mi_beta.ear.h3.attention.AttentionKernel`, law=1
**Updated**: 2026-02-13

---

## Overview

L1 (Prediction) is the anticipatory temporal law. It places the attention window entirely in the future, looking forward from the current frame `t`. The exponential kernel peaks at the present moment (weight = 1.0) and decays into the future, reaching ~5% at the most distant frame in the window. L1 captures where a feature is heading -- the anticipated trajectory weighted by prediction confidence that decreases with temporal distance.

L1 is non-causal: it requires access to frames that have not yet occurred at time `t`. This introduces latency equal to the full horizon duration in real-time applications, but poses no constraint for offline analysis.

---

## Window Definition

```
Window: [t,  min(T, t + n))
```

Where:
- `t` = current frame index
- `n` = horizon frame count (from `HORIZON_FRAMES[horizon]`)
- `T` = total frames in the signal

The window includes `n` frames: from `t` through `t + n - 1` (inclusive). The `min(T, ...)` clamp handles the track end boundary -- when `t + n > T`, the window is truncated at the final frame.

```python
# L1 window selection
window = range(t, min(T, t + n))
```

---

## Kernel Formula

```
A(dt) = exp(-3 * |t' - t| / H)    for t' in [t, t+n-1]
```

| Position | dt = |t' - t| | Weight A(dt) | Role |
|----------|:---:|:--------:|------|
| Current frame (t' = t) | 0 | 1.000 | Peak -- full attention on the present |
| Half-life (t' = t + 0.231H) | 0.231H | 0.500 | Half of peak attention |
| Midpoint (t' = t + H/2) | H/2 | 0.223 | ~22% of peak |
| Window edge (t' = t + n - 1) | ~H | 0.050 | ~5% of peak -- fading boundary |

The kernel is **not renormalized** after boundary clamping. At track end, edge frames naturally receive less total attention weight.

---

## Kernel Visualization

For horizon H = 10 frames, centered at frame t = 15:

```
Weight
1.00 |  *  <- t=15 (current, peak)
     |     *
0.67 |        *
     |           *
     |              *
0.37 |                 *
     |                    *
     |                       *
     |                          *
0.05 |                             *  *  *  *  *  <- most distant frames (~5%)
     +--|--|--|--|--|--|--|--|--|--|--> frame
      15 16 17 18 19 20 21 22 23 24
      now  --------> future ------->

Direction of decay: present --- exponential ---> future
```

```
L1 Prediction window at t=15, H=10:
Frame: [15]  16   17   18   19   20   21   22   23   24
Weight: 1.00 .67  .50  .37  .27  .20  .14  .10  .07  .05
        peak  ---------- exponential decay ----------->
```

---

## Properties

| Property | Value |
|----------|-------|
| Causality | Non-causal -- requires future frames |
| Future frames used | n - 1 (full horizon minus current frame) |
| Real-time latency | n frames = horizon duration |
| Peak weight | 1.0 at current frame t |
| Edge weight | exp(-3) = 0.0498 at most distant frame |
| Half-life | 0.231 * H frames from present |
| Effective width | ~67% of H (region where A > 0.5) |
| Boundary handling | Right-clamped at frame T (no renormalization) |

---

## Neuroscience Basis

L1 models the brain's predictive processing machinery:

- **Predictive coding** (Friston, 2005): The brain continuously generates predictions about incoming sensory input via hierarchical generative models. L1 morphs capture the anticipated temporal trajectory of features, weighted by confidence that decays with prediction horizon.
- **Anticipatory attention** (Clark, 2013): The predictive brain actively prepares for expected events before they occur. In music, listeners anticipate beat onsets, harmonic resolutions, and melodic continuations. L1 encodes these anticipatory representations.
- **Forward models in motor cortex**: Motor planning involves forward simulation of upcoming actions and their sensory consequences. In music perception, the motor system entrains to rhythm and generates beat predictions (Grahn & Brett, 2007). L1 at meso horizons captures this motor-predictive timescale.
- **Bayesian brain hypothesis**: Prediction error -- the difference between prediction and reality -- drives learning and attention. NDU uses the divergence between L1 (prediction) and L0 (memory) to detect novelty, directly implementing this Bayesian surprise framework.

---

## Musical Role

L1 answers the question: **"Where is this feature heading?"**

It captures anticipatory structure -- what is expected to happen next, weighted by confidence in the prediction. Specific musical functions include:

- **Beat prediction**: MPU uses L1 morphs at meso horizons (H6-H11) to project the expected timing and strength of upcoming beats. The exponential decay reflects decreasing confidence in distant beat predictions.
- **Harmonic expectation**: PCU uses L1 to anticipate pitch and chroma trajectories, enabling detection of expected resolutions (e.g., dominant-to-tonic) and unexpected deviations.
- **Phrase-boundary anticipation**: At macro horizons, L1 morphs capture the expected trajectory of features over musical sections, enabling prediction of phrase endings and structural boundaries.
- **Novelty/surprise detection**: NDU compares L0 (what happened) with L1 (what was expected) to quantify prediction error. Large divergence signals novelty -- an unexpected harmonic change, a rhythmic disruption, a sudden timbral shift.

---

## Primary Unit Users

| Unit | Role of L1 | Key Morphs at L1 | Primary Horizons |
|------|-----------|-------------------|------------------|
| **NDU** | Prediction for novelty detection (primary) | M0, M1, M2, M8 | H3-H6 (Micro) |
| **MPU** | Beat prediction / forward entrainment | M0, M8, M14 | H6-H11 (Micro-Meso) |
| **PCU** | Pitch prediction / harmonic expectation | M0, M8, M18 | H6-H16 (Micro-Macro) |
| **STU** | Tonal prediction / key expectation | M0, M1, M19 | H16-H22 (Macro) |
| **ARU** | Arousal prediction / dynamic anticipation | M0, M2, M18 | H6-H16 (Micro-Macro) |
| **RPU** | Rhythm prediction / pattern anticipation | M0, M14, M22 | H9-H16 (Meso-Macro) |

---

## Usage by Unit

| Unit | Uses L1? | Rationale |
|------|:--------:|-----------|
| SPU | **No** | Spectral processing is descriptive, not predictive |
| STU | Yes | Tonal prediction -- anticipates key changes and harmonic direction |
| IMU | **No** | Memory-centric unit -- past traces dominate; uses L0 + L2 |
| ASU | **No** | Scene analysis uses balanced integration (L2) only |
| NDU | Yes | Primary L1 user -- prediction baseline for novelty/surprise |
| MPU | Yes | Beat prediction requires forward-looking temporal projection |
| PCU | Yes | Pitch prediction anticipates melodic and harmonic trajectory |
| ARU | Yes | Arousal prediction anticipates dynamic buildup and release |
| RPU | Yes | Rhythm prediction anticipates metric and groove continuation |

**Coverage**: 6 of 9 units. SPU, IMU, and ASU omit L1 because their processing is either descriptive (SPU), memory-centric (IMU), or integration-centric (ASU).

---

## Latency Implications

L1 is non-causal -- it requires frames from the future. The processing implications depend on the application context:

### Offline Processing

In offline mode (analyzing a complete audio file), the full signal is available. L1 morphs can be computed at every frame with complete future context. No latency penalty.

### Real-Time Processing

In real-time mode, L1 morphs at horizon H require **H frames of lookahead**:

| Horizon | Frames | Duration | Lookahead Required |
|---------|:------:|:--------:|:------------------:|
| H3 | 4 | 23.2 ms | 23.2 ms |
| H6 | 34 | 200 ms | 200 ms |
| H9 | 60 | 350 ms | 350 ms |
| H11 | 78 | 450 ms | 450 ms |
| H16 | 172 | 1,000 ms | 1,000 ms |
| H18 | 345 | 2,000 ms | 2,000 ms |

For real-time systems, the maximum L1 lookahead determines the minimum system latency. Models that require L1 at macro horizons (H16+) introduce 1-25 seconds of latency -- acceptable for analytical tools but prohibitive for live performance.

### Hybrid Strategy

A practical real-time architecture uses L0 for immediate response and L1 only at micro/meso horizons where the latency is tolerable (< 500 ms). Macro-scale predictions can be deferred or approximated.

---

## Complementarity with L0

The L0-L1 pair forms the core of novelty detection in NDU:

```
L0 (Memory):     "What has the feature been doing?"     --> recent history
L1 (Prediction): "What should the feature do next?"     --> anticipated future

Novelty = divergence(L0_morphs, L1_morphs)

High novelty:  L0 and L1 diverge --> surprise, structural boundary
Low novelty:   L0 and L1 agree   --> continuation, stability
```

This comparison is computed across multiple morphs and horizons. For example:
- L0.M0 (recent mean) vs L1.M0 (predicted mean) at H6: is the current loudness different from what was expected?
- L0.M8 (recent velocity) vs L1.M8 (predicted velocity) at H9: is the rate of change following the expected trajectory?
- L0.M18 (recent trend) vs L1.M18 (predicted trend) at H16: is the section-level trajectory matching prediction?

---

## Horizon Interaction

L1 operates meaningfully at all horizon scales, though its character changes:

| Band | Horizons | L1 Captures | Example |
|------|----------|-------------|---------|
| **Micro** | H0-H7 | Immediate onset/transient prediction | "Will loudness increase in the next 200ms?" |
| **Meso** | H8-H15 | Beat-level prediction, rhythmic anticipation | "Where is the next beat expected?" |
| **Macro** | H16-H23 | Phrase/section trajectory prediction | "Is pitch expected to rise over the next 2s?" |
| **Ultra** | H24-H28 | Movement-scale prediction (rare usage) | "What is the expected overall timbral trajectory?" |

At micro horizons, L1 predicts immediate continuation of transient events. At meso horizons, it captures rhythmic and metric anticipation. At macro horizons, it projects section-level structural expectations. Ultra-scale L1 is rarely used -- prediction confidence is too low at movement timescales.

---

## Code Path

```
mi_beta/ear/h3/attention.py    -- compute_attention_weights(window, t, n_frames)
mi_beta/ear/h3/__init__.py     -- H3Extractor selects law=1 window
mi_beta/core/constants.py      -- LAW_NAMES[1] = "prediction", ATTENTION_DECAY = 3.0
```

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
**Attention kernel contract**: [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md)
**H3 architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
