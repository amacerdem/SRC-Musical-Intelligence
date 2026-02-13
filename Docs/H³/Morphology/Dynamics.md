# H3 Morphology -- Dynamics (M8-M13, M15, M18, M21)

**Version**: 2.0.0
**Category**: Dynamics
**Morphs**: 9 (M8-M13, M15, M18, M21)
**Purpose**: Temporal derivatives, trend, smoothness, and oscillation descriptors capturing how R3 features change over time
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer.compute_M8` through `compute_M21`
**Updated**: 2026-02-13

---

## Overview

Dynamics morphs capture the temporal evolution of R3 features -- not what a feature's value is, but how it is changing. This is the largest morph category (9 morphs), spanning first-order derivatives (velocity), second-order derivatives (acceleration), third-order derivatives (jerk, via smoothness), linear trend, and oscillation counting.

Dynamics morphs are central to musical perception. Velocity tracks crescendo and decrescendo. Acceleration tracks the onset of change (a sudden shift from steady to rising). Smoothness distinguishes legato from staccato textures. Trend captures gradual builds and decays across phrases or sections. Zero crossings measure oscillatory behavior.

---

## Category Summary

| Index | Name | Derivative Order | Min Window | Output Range | Signed | MORPH_SCALE |
|:-----:|------|:----------------:|:----------:|:------------:|:------:|:-----------:|
| M8 | velocity | 1st | 2 | (-inf, +inf) | Yes | 0.1 |
| M9 | velocity_mean | 1st (averaged) | 2 | (-inf, +inf) | Yes | 0.05 |
| M10 | velocity_std | 1st (std) | 2 | [0, +inf) | No | 0.05 |
| M11 | acceleration | 2nd | 3 | (-inf, +inf) | Yes | 0.01 |
| M12 | acceleration_mean | 2nd (averaged) | 3 | (-inf, +inf) | Yes | 0.005 |
| M13 | acceleration_std | 2nd (std) | 3 | [0, +inf) | No | 0.005 |
| M15 | smoothness | 3rd (inverse jerk) | 3 | (0, 1] | No | 1.0 |
| M18 | trend | regression slope | 2 | (-inf, +inf) | Yes | 0.01 |
| M21 | zero_crossings | count | 2 | [0, N-1] | No | 20.0 |

---

## M8: velocity

**Formula**:
```
M8(x, t) = dx/dt = x(t) - x(t-1)
```

The instantaneous first difference at the current frame.

**Properties**:
- **Output range**: (-inf, +inf) (practically [-1, 1] for R3 features in [0, 1])
- **Min window**: 2 frames (need current and previous frame)
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 0.1 (signed scaling: `(raw / 0.1 + 1) / 2` maps [-0.1, 0.1] to [0, 1])

**Musical interpretation**: The rate of change of the feature at this instant. Positive velocity (output > 0.5) means the feature is increasing -- for energy features, this is a crescendo; for spectral features, a brightening. Negative velocity (output < 0.5) means the feature is decreasing -- decrescendo, darkening. Zero velocity (output = 0.5) means the feature is momentarily steady.

**Common use cases**:
- MPU: Beat-level energy velocity for motor prediction (anticipating accents)
- ASU: Onset detection at Micro horizons via energy velocity spikes
- NDU: Prediction error based on unexpected velocity changes
- IMU: Emotional arousal tracking via energy velocity at Macro horizons

---

## M9: velocity_mean

**Formula**:
```
M9(x) = mean(dx/dt) = (1/N) * sum(x(t+i) - x(t+i-1)) for i in window
```

Equivalently: `M9 = (x_last - x_first) / N`, the net displacement divided by window length.

**Properties**:
- **Output range**: (-inf, +inf) (practically smaller than M8 due to averaging)
- **Min window**: 2 frames
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 0.05 (signed scaling: `(raw / 0.05 + 1) / 2`)

**Musical interpretation**: The average rate of change over the window. While M8 captures the instantaneous change, M9 smooths out frame-to-frame fluctuations to reveal the net trend direction. Positive M9 (output > 0.5) indicates the feature is generally rising over the window. At Meso horizons, M9 on energy features captures whether a beat-length passage is generally getting louder or softer.

**Common use cases**:
- STU: Structural momentum -- is the passage building or receding?
- BEP: Beat-level energy trajectory for entrainment
- C0P: Contextual prediction of feature trajectories at Macro horizons

**Relationship to M18 (trend)**: M9 and M18 both capture directional tendency, but M9 is the simple mean of first differences while M18 uses linear regression. For linear signals they are equivalent; for non-linear signals, M18 is more robust to outlier frames.

---

## M10: velocity_std

**Formula**:
```
M10(x) = std(dx/dt) = sqrt(mean((v - mean(v))^2))
```

Where `v(i) = x(i) - x(i-1)` for each frame pair in the window.

**Properties**:
- **Output range**: [0, +inf) (practically bounded)
- **Min window**: 2 frames
- **Signed**: No
- **MORPH_SCALE**: 0.05 (scale maps typical max ~0.05 to 1.0)

**Musical interpretation**: The variability of the rate of change. High M10 indicates erratic, unpredictable changes -- the feature sometimes rises sharply, sometimes falls, with no consistent pattern. Low M10 indicates smooth, consistent change -- the feature moves steadily in one direction. At Meso horizons, high M10 on energy features signals rhythmically complex passages (syncopation, accents). At Macro horizons, low M10 indicates smooth, predictable evolution.

**Common use cases**:
- NDU: High velocity variability correlates with perceived unpredictability
- ASU: Scene complexity measure -- chaotic scenes have high M10
- TMH: Temporal memory encoding priority -- high M10 events are more memorable

---

## M11: acceleration

**Formula**:
```
M11(x, t) = d^2x/dt^2 = v(t) - v(t-1) = x(t) - 2*x(t-1) + x(t-2)
```

The instantaneous second difference at the current frame.

**Properties**:
- **Output range**: (-inf, +inf) (practically [-2, 2] for R3 features)
- **Min window**: 3 frames (need current and two previous frames)
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 0.01 (signed scaling: `(raw / 0.01 + 1) / 2`)

**Musical interpretation**: The rate of change of velocity -- how rapidly the direction of change is itself changing. Positive acceleration (output > 0.5) means the feature is speeding up in its current direction or decelerating from a decrease. In musical terms, positive acceleration on energy features signals the onset of a crescendo (the beginning of a dynamic swell). Negative acceleration signals the onset of a decrescendo or the tapering of a crescendo.

**Common use cases**:
- PPC: Pre-attentive detection of onset transients (sharp acceleration at attack)
- ASA: Scene change detection via acceleration spikes
- MPU: Motor planning for anticipated tempo changes

---

## M12: acceleration_mean

**Formula**:
```
M12(x) = mean(d^2x/dt^2) = (1/M) * sum(a(i)) for i in window
```

Where `a(i) = x(i) - 2*x(i-1) + x(i-2)` and M is the count of valid second-difference frames.

**Properties**:
- **Output range**: (-inf, +inf) (practically very small: ~[-0.05, 0.05])
- **Min window**: 3 frames
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 0.005 (signed scaling: `(raw / 0.005 + 1) / 2`)

**Musical interpretation**: The average acceleration over the window. Near zero when the feature changes at a constant rate (linear trend). Positive M12 indicates the feature is generally accelerating upward -- the crescendo is intensifying. Negative M12 indicates decelerating or accelerating downward. At Macro horizons, M12 captures whether a section's dynamic trajectory is convex (intensifying) or concave (tapering).

**Common use cases**:
- TMH: Hierarchical memory encoding -- sections with strong average acceleration are structurally significant
- C0P: Contextual prediction -- anticipating whether a build will continue intensifying

---

## M13: acceleration_std

**Formula**:
```
M13(x) = std(d^2x/dt^2) = sqrt(mean((a - mean(a))^2))
```

Where `a(i) = x(i) - 2*x(i-1) + x(i-2)`.

**Properties**:
- **Output range**: [0, +inf) (practically bounded)
- **Min window**: 3 frames
- **Signed**: No
- **MORPH_SCALE**: 0.005 (scale maps typical max ~0.005 to 1.0)

**Musical interpretation**: The variability of acceleration. High M13 indicates that the rate of change is itself erratically changing -- highly turbulent dynamics. Low M13 indicates smooth, predictable acceleration (or deceleration). At Meso horizons, high M13 on energy features indicates rhythmically complex patterns with irregular accents. At Macro horizons, it reflects structural unpredictability.

**Common use cases**:
- NDU: Acceleration variability as a novelty indicator
- ASU: Turbulence measure for scene analysis

---

## M15: smoothness

**Formula**:
```
M15(x) = 1 / (1 + |jerk| / sigma)
```

Where:
- `jerk = d^3x/dt^3 = a(t) - a(t-1)` (third temporal derivative)
- `sigma` = a normalizing constant (std of the signal or a fixed reference)

**Properties**:
- **Output range**: (0, 1] (1.0 = perfectly smooth, approaching 0 = maximally jerky)
- **Min window**: 3 frames (need 4 values for third derivative, but implementation uses windowed estimate with 3)
- **Signed**: No
- **MORPH_SCALE**: 1.0 (already in (0, 1])

**Musical interpretation**: How smoothly the feature evolves. High smoothness (near 1.0) indicates legato-like behavior -- the feature changes gradually without abrupt shifts. Low smoothness (near 0.0) indicates staccato-like behavior -- the feature exhibits sharp, jerky transitions. At Meso horizons on energy features, smoothness distinguishes legato passages from staccato articulation. At Macro horizons, it characterizes whether sections transition smoothly or abruptly.

**Common use cases**:
- MPU: Motor smoothness prediction -- smooth musical gestures correlate with smooth motor responses
- ASU: Textural classification -- legato vs. staccato vs. marcato
- ARU: Aesthetic smoothness evaluation of musical passages

**Relationship to M11 (acceleration)**: Smoothness is derived from the third derivative (jerk), one order higher than acceleration. While acceleration detects the onset of change, smoothness evaluates the quality of that change -- smooth vs. abrupt.

---

## M18: trend

**Formula**:
```
M18(x) = OLS slope of x vs. time index
```

Computed via ordinary least squares: `slope = cov(x, t) / var(t)` where `t` is the frame index within the window.

**Properties**:
- **Output range**: (-inf, +inf) (practically ~[-0.01, 0.01] per frame)
- **Min window**: 2 frames
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 0.01 (signed scaling: `(raw / 0.01 + 1) / 2`)

**Musical interpretation**: The linear trend direction and magnitude over the window. Positive trend (output > 0.5) indicates a gradual upward build. Negative trend (output < 0.5) indicates a gradual decline. Unlike M9 (velocity_mean), M18 uses regression and is more robust to isolated outlier frames. At Macro horizons (H16-H22), trend captures the large-scale trajectory of features across musical sections -- a gradual crescendo, a slow brightening, a steady harmonic darkening.

**Common use cases**:
- TMH: Long-term trend detection for structural memory -- is the piece gradually building?
- C0P: Contextual prediction of where the feature is heading at Macro timescales
- IMU: Emotional arc tracking -- gradual intensity builds in emotional memory
- STU: Section-level trajectory classification (building, receding, stable)

---

## M21: zero_crossings

**Formula**:
```
M21(x) = count of sign changes in (x - mean(x))
```

For each consecutive pair `(x_i, x_{i+1})`: if `(x_i - mean) * (x_{i+1} - mean) < 0`, count a crossing.

**Properties**:
- **Output range**: [0, N-1] (maximum when every consecutive pair crosses the mean)
- **Min window**: 2 frames
- **Signed**: No
- **MORPH_SCALE**: 20.0 (count-valued; `raw / 20.0` normalizes typical range to [0, 1])

**Musical interpretation**: The oscillation frequency of the feature around its mean. High zero-crossing count indicates rapid alternation -- the feature oscillates quickly around its average (e.g., vibrato, tremolo, or rapid fluctuation). Low count indicates the feature stays mostly on one side of its mean (e.g., a sustained value with gradual drift). At Meso horizons, zero crossings on energy features proxy for rhythmic pulse rate. At Macro horizons, they indicate sectional oscillation.

**Common use cases**:
- BEP: Rhythmic pulse proxy at Meso horizons (zero crossings of energy correlate with beat rate)
- ASA: Oscillation frequency for auditory stream segregation
- CPD: Change point detection -- sudden shifts in zero-crossing rate indicate structural boundaries

**Relationship to M14 (periodicity)**: Zero crossings measure oscillation frequency (how often the feature crosses its mean), while periodicity measures regularity (how consistent those oscillations are). A feature can have many zero crossings but low periodicity if the crossings are irregularly spaced.

---

## Derivative Chain

The dynamics morphs form a derivative chain:

```
R3 feature x(t)
    |
    | d/dt
    v
M8: velocity = dx/dt
    |
    | d/dt
    v
M11: acceleration = d^2x/dt^2
    |
    | d/dt
    v
(jerk = d^3x/dt^3) --> M15: smoothness = 1/(1 + |jerk|/sigma)
```

At each level, both the instantaneous value and windowed statistics are available:

| Derivative Order | Instantaneous | Mean | Std |
|:----------------:|:------------:|:----:|:---:|
| 0th (value) | x(t) | M1 | M2 |
| 1st (velocity) | M8 | M9 | M10 |
| 2nd (acceleration) | M11 | M12 | M13 |
| 3rd (jerk) | (internal) | -- | -- via M15 |

---

## Horizon Interaction Summary

| Morph | H0 (1f) | H1 (2f) | H2 (3f) | H3+ (4f+) | Meso (52f+) | Macro (172f+) |
|-------|:-------:|:-------:|:-------:|:---------:|:-----------:|:------------:|
| M8 | -- | Valid | Valid | Good | Good | Good |
| M9 | -- | Valid | Valid | Good | Excellent | Excellent |
| M10 | -- | Valid | Valid | Good | Excellent | Excellent |
| M11 | -- | -- | Valid | Good | Good | Good |
| M12 | -- | -- | Valid | Good | Excellent | Excellent |
| M13 | -- | -- | Valid | Good | Excellent | Excellent |
| M15 | -- | -- | Valid | Good | Excellent | Excellent |
| M18 | -- | Valid | Valid | Good | Excellent | Excellent |
| M21 | -- | Valid | Valid | Good | Excellent | Excellent |

**Note**: Instantaneous dynamics morphs (M8, M11) are meaningful at all valid horizons. Windowed statistics (M9, M10, M12, M13) become more robust with larger windows. At Ultra horizons, instantaneous dynamics morphs (M8, M11) are less informative than their windowed counterparts (M9, M12, M18).

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [MorphScaling.md](MorphScaling.md) |
| H3 architecture (morph axis) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Morphology index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
