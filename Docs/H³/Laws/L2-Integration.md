# H3 Law L2 -- Integration (Bidirectional)

**Version**: 2.0.0
**Law index**: 2
**Direction**: Bidirectional (symmetric)
**Window**: `[max(0, t-half), min(T, t+n-half))` where `half = n // 2`
**Kernel**: `A(dt) = exp(-3|t'-t|/H)` for all `t'` in window
**Causality**: Semi-causal -- uses both past and future frames
**Latency**: n/2 frames (half horizon duration)
**Code reference**: `mi_beta.ear.h3.attention.AttentionKernel`, law=2
**Updated**: 2026-02-13

---

## Overview

L2 (Integration) is the bidirectional temporal law. It centers the attention window on the current frame `t`, extending equally into the past and future. The exponential kernel peaks at the present moment (weight = 1.0) and decays symmetrically in both directions, reaching ~5% at both window edges. L2 captures the overall character of a feature around the present -- a holistic view that combines memory and anticipation into a unified perceptual description.

L2 treats past and future identically. For stationary signals, L2 morphs approximate the "true" local statistics better than either L0 or L1 alone, because they use the full available context around the point of interest.

---

## Window Definition

```
half = n // 2
Window: [max(0, t - half),  min(T, t + n - half))
```

Where:
- `t` = current frame index
- `n` = horizon frame count (from `HORIZON_FRAMES[horizon]`)
- `half` = `n // 2` (integer division)
- `T` = total frames in the signal

The window spans `n` frames total: approximately `half` frames before `t` and `n - half` frames from `t` onward. For even `n`, the split is exactly symmetric. For odd `n`, one extra frame falls on the future side. Boundary clamping (`max(0, ...)`, `min(T, ...)`) handles track start and end.

```python
# L2 window selection
half = n // 2
window = range(max(0, t - half), min(T, t + n - half))
```

---

## Kernel Formula

```
A(dt) = exp(-3 * |t' - t| / H)    for t' in [t-half, t+n-half-1]
```

| Position | dt = |t' - t| | Weight A(dt) | Role |
|----------|:---:|:--------:|------|
| Current frame (t' = t) | 0 | 1.000 | Peak -- full attention on the present |
| Half-life (both sides) | 0.231H | 0.500 | Half of peak attention |
| Midpoint (both sides) | H/2 | 0.223 | ~22% of peak |
| Past edge (t' = t - half) | ~H/2 | 0.223 | Symmetric decay into past |
| Future edge (t' = t + n - half - 1) | ~H/2 | 0.223 | Symmetric decay into future |

For the full-window edges (at distance ~H from center), weight reaches ~5%. Because L2 splits the horizon in half, each edge is at distance ~H/2, giving edge weights of ~22% -- higher than the boundary weights of L0 or L1.

The kernel is **not renormalized** after boundary clamping. At track start or end, edge frames naturally receive less total attention weight.

---

## Kernel Visualization

For horizon H = 10 frames, centered at frame t = 15:

```
Weight
1.00 |                    *  <- t=15 (current, peak)
     |                 *     *
     |              *           *
0.55 |           *                 *
     |        *                       *
     |     *                             *
0.30 |  *                                   *
     |                                         *
0.22 *                                            *
     |                                               *
0.16 |                                                  *
     +--|--|--|--|--|--|--|--|--|--|--> frame
      11 12 13 14 15 16 17 18 19 20
      <--- past --  now  -- future --->

Direction of decay: past <--- exp --- present --- exp ---> future
```

```
L2 Integration window at t=15, H=10:
Frame:  11   12   13   14  [15]  16   17   18   19   20
Weight: .22  .30  .41  .55 1.00  .55  .41  .30  .22  .16
        <-- decay --   peak    -- decay -->
```

---

## Properties

| Property | Value |
|----------|-------|
| Causality | Semi-causal -- uses past and future frames |
| Future frames used | n - half - 1 (approximately half the horizon) |
| Real-time latency | n/2 frames = half the horizon duration |
| Peak weight | 1.0 at current frame t |
| Edge weight (at +/- H/2) | exp(-1.5) = 0.223 at window edges |
| Half-life | 0.231 * H frames from present (both directions) |
| Effective width | ~67% of H (region where A > 0.5), centered |
| Symmetry | Past and future weighted identically |
| Boundary handling | Clamped at frames 0 and T (no renormalization) |

---

## Neuroscience Basis

L2 models the temporal integration window of auditory perception:

- **Temporal integration window** (Poeppel, 2003): Auditory perception operates within a "window of integration" where past and future events are fused into a unified perceptual experience. This window is typically 150-300 ms for low-level features and 1-3 seconds for higher-level structure, corresponding to meso and macro horizons.
- **The "perceptual present"**: Psychological research identifies a "specious present" -- a window of time experienced as "now" rather than "past" or "future" (James, 1890; Fraisse, 1984). L2 captures this extended present, where both recent memory and immediate anticipation contribute to the current percept.
- **Gestalt temporal grouping**: Auditory scene analysis groups events that fall within a temporal proximity window (Bregman, 1990). L2's symmetric kernel naturally implements this grouping, weighting nearby events (past or future) more strongly than distant ones.
- **Auditory cortex sustained response**: Neurons in auditory cortex maintain sustained responses that integrate both past and anticipated events, especially at higher cortical levels (Hasson et al., 2015). L2 mirrors this integration at its longer horizons.

---

## Musical Role

L2 answers the question: **"What is the overall character of this feature around now?"**

It provides a holistic temporal description that treats the present as the center of a contextual window, combining what has been heard with what is about to be heard. Specific musical functions include:

- **Contextual normalization**: L2 morphs like M1 (mean) and M2 (std) at macro horizons provide a local baseline for feature values. This enables normalization -- expressing a feature's current value relative to the local context rather than in absolute terms.
- **Steady-state characterization**: For sustained musical passages (held chords, sustained timbres), L2 provides the most accurate description because it uses the full context around the observation point. M19 (stability) under L2 captures whether a feature is truly steady or fluctuating.
- **Tonal stability assessment**: STU uses L2 to assess whether a tonal center is established by examining chroma features symmetrically around the present.
- **Scene analysis**: ASU uses L2 exclusively -- auditory scene formation requires balanced context, not biased toward past or future.

---

## Primary Unit Users

| Unit | Role of L2 | Key Morphs at L2 | Primary Horizons |
|------|-----------|-------------------|------------------|
| **SPU** | Spectral integration (primary) | M0, M1, M2, M19 | H6-H16 (Micro-Macro) |
| **ASU** | Scene analysis over balanced context | M0, M1, M5, M20 | H3-H9 (Micro-Meso) |
| **ARU** | Arousal from full context | M0, M2, M5, M18 | H6-H16 (Micro-Macro) |
| **STU** | Tonal stability / key context | M0, M1, M19 | H16-H22 (Macro) |
| **IMU** | Integrated perceptual context | M0, M1, M2 | H18-H25 (Macro-Ultra) |
| **NDU** | Contextual baseline for novelty | M0, M1, M2 | H3-H6 (Micro) |
| **PCU** | Pitch context / chroma integration | M0, M1, M19 | H6-H16 (Micro-Macro) |
| **RPU** | Rhythm context / metric integration | M0, M14, M19 | H9-H16 (Meso-Macro) |

---

## Usage by Unit

| Unit | Uses L2? | Rationale |
|------|:--------:|-----------|
| SPU | Yes | Spectral integration requires balanced temporal context |
| STU | Yes | Tonal stability assessment needs symmetric key context |
| IMU | Yes | Integrated perceptual context combines memory and anticipation |
| ASU | Yes | Scene analysis operates on balanced integration (L2 only) |
| NDU | Yes | Contextual baseline provides normalization for novelty detection |
| MPU | **No** | Beat tracking is causal (L0) + predictive (L1); bidirectional context not needed |
| PCU | Yes | Pitch context requires symmetric chroma integration |
| ARU | Yes | Arousal assessment benefits from full surrounding context |
| RPU | Yes | Rhythmic context assessment uses symmetric metric evaluation |

**Coverage**: 8 of 9 units. Only MPU omits L2, relying on L0 (recent beats) and L1 (predicted beats) for its causal-predictive beat tracking strategy.

---

## Symmetry Property

L2's defining characteristic is temporal symmetry: past and future receive identical weight at equal distance from `t`.

For **stationary signals** (where the statistical properties do not change over the window), this symmetry provides optimal estimation:

- L0 is biased toward recent frames, underweighting the older portion of the context
- L1 is biased toward near-future frames, underweighting distant predictions
- L2 uses the full context symmetrically, providing the minimum-variance estimate of local statistics

For **non-stationary signals** (transitions, boundaries), L2 may blur the transition point because it averages across both sides of the change. In such cases, L0 and L1 provide sharper boundary detection. This is why NDU uses all three laws: L2 for context, L0/L1 for boundary-sensitive comparison.

### Stationarity Example

Consider a sustained chord with constant loudness (R3[7] = 0.6):

```
L0.M0 at t:  weighted average biased toward recent frames  = ~0.60
L1.M0 at t:  weighted average biased toward upcoming frames = ~0.60
L2.M0 at t:  symmetric weighted average around t            = ~0.60  (lowest variance)
```

All three agree for stationary signals, but L2 has the lowest estimation variance because it uses the most balanced sample.

Now consider a sudden loudness jump at frame t (from 0.3 to 0.7):

```
L0.M0 at t:  mostly past frames (0.3) + current (0.7)      = ~0.35  (sees the jump)
L1.M0 at t:  current (0.7) + mostly future frames (0.7)     = ~0.68  (sees the new level)
L2.M0 at t:  half past (0.3) + half future (0.7)            = ~0.50  (blurs the boundary)
```

L0 and L1 capture the change more sharply; L2 smooths across it.

---

## Relationship to L0 and L1

L2 can be understood as a combination of L0 and L1 perspectives:

```
L0 (Memory):       [====A(dt)===>|t]         past only
L1 (Prediction):                [t|==A(dt)===>]   future only
L2 (Integration):  [<==A(dt)==|t|==A(dt)==>]  both
```

### Conceptual Relationship

L2 approximates the renormalized convolution of L0 and L1 perspectives. If we were to combine an L0 window and an L1 window centered at the same point `t`, the result would resemble an L2 window with modified weights. However, L2 is **computed independently** rather than derived from L0 and L1, for two reasons:

1. **Efficiency**: Computing L2 directly requires one pass over the window, not two passes plus combination.
2. **Kernel shape**: The direct L2 kernel is a clean symmetric exponential. A convolution of L0 and L1 would produce a different shape (peakier near center, with heavier tails).

### Complementary Roles

| Perspective | L0 (Memory) | L1 (Prediction) | L2 (Integration) |
|-------------|-------------|------------------|-------------------|
| Temporal bias | Past | Future | Balanced |
| Best for | Change detection, recent history | Anticipation, prediction error | Steady-state characterization, normalization |
| Boundary sensitivity | High (causal edge) | High (predictive edge) | Low (smooths across boundaries) |
| Stationarity estimate | Good | Good | Best (minimum variance) |
| Real-time latency | 0 | n frames | n/2 frames |

---

## Horizon Interaction

L2 operates meaningfully at all horizon scales:

| Band | Horizons | L2 Captures | Example |
|------|----------|-------------|---------|
| **Micro** | H0-H7 | Local onset context, symmetric transient envelope | "What is the average spectral centroid around this onset?" |
| **Meso** | H8-H15 | Beat-level character, local rhythmic context | "What is the overall energy level during this beat cycle?" |
| **Macro** | H16-H23 | Section character, tonal/dynamic context | "What is the tonal stability over this 2-second passage?" |
| **Ultra** | H24-H28 | Movement character, global normalization | "What is the overall loudness of this movement?" |

At micro horizons, L2 provides balanced local context for feature characterization. At macro and ultra horizons, L2 provides the contextual baseline against which local deviations (detected via L0 or L1) become meaningful.

---

## Code Path

```
mi_beta/ear/h3/attention.py    -- compute_attention_weights(window, t, n_frames)
mi_beta/ear/h3/__init__.py     -- H3Extractor selects law=2 window
mi_beta/core/constants.py      -- LAW_NAMES[2] = "integration", ATTENTION_DECAY = 3.0
```

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
**Attention kernel contract**: [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md)
**H3 architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
