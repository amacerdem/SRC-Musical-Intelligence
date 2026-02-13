# H3 Morphology -- Symmetry (M16, M19, M23)

**Version**: 2.0.0
**Category**: Symmetry
**Morphs**: 3 (M16, M19, M23)
**Purpose**: Shape, stability, and time-reversal descriptors measuring geometric and structural properties of the temporal trajectory
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer.compute_M16`, `compute_M19`, `compute_M23`
**Updated**: 2026-02-13

---

## Overview

Symmetry morphs characterize the geometric and structural properties of an R3 feature's temporal trajectory. Where Distribution morphs (M0-M7) describe *what values* the feature takes, and Dynamics morphs (M8-M13, M15, M18, M21) describe *how those values change*, Symmetry morphs describe the *shape and character* of that change -- is the trajectory smooth or angular (curvature), stable or volatile (stability), and palindromic or directional (symmetry)?

These three morphs provide complementary perspectives on temporal structure that are especially useful for L2 (Integration) law computations, where bidirectional context is available.

---

## Category Summary

| Index | Name | Min Window | Output Range | Signed | MORPH_SCALE |
|:-----:|------|:----------:|:------------:|:------:|:-----------:|
| M16 | curvature | 3 | [0, +inf) | Yes | 0.1 |
| M19 | stability | 2 | (0, 1] | No | 1.0 |
| M23 | symmetry | 2 | [-1, 1] | Yes | 1.0 |

---

## M16: curvature

**Formula**:
```
M16(x) = mean(|d^2x/dt^2|) = (1/M) * sum(|x(t) - 2*x(t-1) + x(t-2)|)
```

Where M is the count of valid second-difference frames within the window.

**Properties**:
- **Output range**: [0, +inf) (practically bounded; typical max ~0.1 for R3 features)
- **Min window**: 3 frames (need at least 3 values to compute second difference)
- **Signed**: Yes (treated as signed for scaling purposes because the raw value maps to a one-sided range that needs centering consideration)
- **MORPH_SCALE**: 0.1 (signed scaling: `(raw / 0.1 + 1) / 2`; since raw is non-negative, output range is effectively [0.5, 1.0] unless raw exceeds the scale)

**Scaling note**: Although curvature is non-negative, the MORPH_SCALE system treats it as signed to maintain consistency with the derivative-family morphs. In practice, the signed mapping means that zero curvature maps to 0.5, and typical curvature values map to [0.5, 1.0]. This convention ensures that "no curvature" (straight-line trajectory) sits at the midpoint, with increasing curvature moving toward 1.0.

**Musical interpretation**: The average bending of the feature's temporal trajectory. High curvature means the feature trajectory has many inflection points or sharp turns -- the feature does not move in straight lines but curves rapidly. Musically, high curvature on energy features indicates complex dynamic contours (crescendo-decrescendo patterns, sforzando accents). Low curvature indicates straight-line trajectories (steady state or linear ramps).

**Relationship to M11 (acceleration)**: M16 is the mean of the *absolute* second derivative, while M11 is the instantaneous signed second derivative. M16 is always non-negative and captures trajectory bending regardless of direction. M11 captures the signed acceleration at a single point in time.

**Common use cases**:
- ARU: Aesthetic evaluation of contour complexity -- highly curved trajectories are more interesting
- TMH: Temporal memory encoding -- curved trajectories are more memorable than linear ones
- ASU: Scene complexity -- complex scenes produce curved feature trajectories
- SPU: Gestalt contour analysis -- curvature affects perceptual grouping

---

## M19: stability

**Formula**:
```
M19(x) = 1 / (1 + var(x) / sigma^2)
```

Where:
- `var(x) = sum((x - mean)^2) / N` is the variance within the window
- `sigma^2` is a normalizing constant (reference variance, typically 1.0 for pre-normalized R3 features)

**Properties**:
- **Output range**: (0, 1] (1.0 = perfectly stable, approaching 0 = maximally unstable)
- **Min window**: 2 frames (need at least 2 values to compute variance)
- **Signed**: No
- **MORPH_SCALE**: 1.0 (already in (0, 1])

**Musical interpretation**: How temporally stationary the feature is within the window. High stability (near 1.0) means the feature value hardly changes -- a sustained pitch, a steady loudness, a consistent timbre. Low stability (near 0.0) means the feature varies widely -- rapid fluctuations, turbulent transitions, or dramatic shifts within the window.

Stability is related to M2 (std) but expressed on a different scale. M2 gives the absolute spread; M19 maps that spread onto a bounded (0, 1] range via the inverse-variance transform. The advantage of M19 is that its output is naturally bounded and interpretable: 1.0 always means "perfectly stable" regardless of the feature's absolute scale.

**Horizon interaction**:

| Horizon Band | Stability Character |
|-------------|-------------------|
| Micro (H0-H7) | Frame-level stability; detects micro-fluctuations and onset transients |
| Meso (H8-H15) | Beat-level stability; stable = sustained notes, unstable = ornaments/trills |
| Macro (H16-H23) | Section-level stationarity; stable = homogeneous texture, unstable = transitional passage |
| Ultra (H24+) | Movement-level consistency; high stability across a movement = uniform character |

**Common use cases**:
- C0P: Contextual prediction -- stable features are easy to predict, unstable features require attention
- CPD: Change point detection -- sudden drops in stability signal structural boundaries
- TMH: Temporal memory hierarchy -- stability changes demarcate memory segments
- ASU: Auditory scene stability -- stable scenes are parsed; unstable boundaries trigger re-analysis
- IMU: Emotional stability tracking at Macro horizons

---

## M23: symmetry

**Formula**:
```
M23(x) = correlation(x, reverse(x))
```

Computed as Pearson correlation between the windowed signal and its time-reverse:
```
M23 = sum((x(t) - mean_x) * (x_rev(t) - mean_rev)) / (N * std_x * std_rev)
```

Where `x_rev(t) = x(N-1-t)` is the time-reversed signal. Since `mean_x = mean_rev` and `std_x = std_rev`, this simplifies to:
```
M23 = sum((x(t) - mean) * (x(N-1-t) - mean)) / sum((x(t) - mean)^2)
```

**Properties**:
- **Output range**: [-1, 1] (1.0 = perfect palindrome, -1.0 = perfect anti-palindrome, 0.0 = no symmetry)
- **Min window**: 2 frames
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 1.0 (signed scaling: `(raw / 1.0 + 1) / 2` maps [-1, 1] to [0, 1])

**Musical interpretation**: Whether the feature's temporal contour is palindromic (the same forward and backward). High symmetry (output > 0.5) indicates the feature forms an arch shape -- it rises then falls (or falls then rises) in a mirror pattern. This is extremely common in musical phrases: a crescendo followed by a decrescendo, an ascending melody followed by a descending one, a tension-release pattern.

Low symmetry (output < 0.5) indicates asymmetric temporal structure -- the feature's beginning and ending behave differently. Anti-symmetry (output near 0.0, raw near -1.0) means the temporal contour is inverted when reversed -- what went up at the start goes down at the end, and vice versa.

**Symmetry near 0.5 (raw near 0.0)** indicates no particular relationship between the forward and backward contour -- typical of noise-like or complex polyphonic passages.

**Horizon interaction**:

| Horizon Band | What Symmetry Captures |
|-------------|----------------------|
| Micro (H3-H7) | Onset symmetry: is the attack profile symmetric? (Usually not -- attacks are fast, decays slow) |
| Meso (H8-H15) | Beat symmetry: is there a symmetric pulse shape? (Downbeat-upbeat balance) |
| Macro (H16-H23) | Phrase symmetry: arc-like phrase structure (tension-resolution patterns) |
| Ultra (H24+) | Movement symmetry: does the movement mirror itself? (ABA form = high symmetry) |

**Common use cases**:
- ARU: Aesthetic resonance -- arch-shaped phrases are perceived as more satisfying
- STU: Structural form detection -- ABA and rondo forms produce high symmetry at appropriate horizons
- SPU: Gestalt closure -- symmetric contours create stronger perceptual grouping
- IMU: Emotional narrative -- symmetric emotional arcs (calm-tension-calm) are a fundamental affective pattern

**L2 (Integration) law affinity**: Symmetry is particularly natural under L2 (Integration) law, which provides bidirectional temporal context. Under L0 (Memory) or L1 (Prediction), only half the temporal context is available, making the symmetry computation less meaningful. Many symmetry demands use L2.

---

## Symmetry Morph Interactions

The three symmetry morphs provide complementary geometric perspectives:

```
M16 (curvature):   "How bent is the trajectory?"    bending magnitude
M19 (stability):   "How stationary is the feature?"  constancy measure
M23 (symmetry):    "Is the contour palindromic?"     mirror correlation
```

**Typical combinations**:

| M16 | M19 | M23 | Temporal Character |
|:---:|:---:|:---:|-------------------|
| Low | High | High | Flat, stable, symmetric -- sustained tone, static texture |
| High | Low | High | Curved but symmetric -- arch-shaped crescendo-decrescendo |
| High | Low | Low | Curved and asymmetric -- one-directional build, attack-decay |
| Low | High | Low | Stable but asymmetric -- slight drift in one direction |
| High | Low | ~0.5 | Curved, volatile, no symmetry -- complex, unpredictable contour |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [MorphScaling.md](MorphScaling.md) |
| H3 architecture (morph axis) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| L2 Integration law | [../Laws/L2-Integration.md](../Laws/L2-Integration.md) |
| Morphology index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
