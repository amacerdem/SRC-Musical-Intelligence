# H3 Morphology -- Distribution (M0-M7)

**Version**: 2.0.0
**Category**: Distribution
**Morphs**: 8 (M0-M7)
**Purpose**: Statistical moments and order statistics describing the value distribution within a temporal window
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer.compute_M0` through `compute_M7`
**Updated**: 2026-02-13

---

## Overview

Distribution morphs capture the statistical shape of an R3 feature's value distribution within a temporal window. They answer the question: *what does the distribution of this feature look like over the last N frames?* These 8 morphs cover central tendency (M0, M1, M3), extremes (M4, M5), spread (M2), and higher-order shape (M6, M7).

Distribution morphs are the most broadly applicable category. All 8 are valid at Meso horizons and above. At Micro band, M0, M1, M3, and M4 are available from H0 (1 frame), while the full set requires H3 (4 frames) for M7 kurtosis.

---

## Category Summary

| Index | Name | Min Window | Output Range | Signed | MORPH_SCALE |
|:-----:|------|:----------:|:------------:|:------:|:-----------:|
| M0 | attention_weighted_mean | 1 | [0, 1] | No | 1.0 |
| M1 | unweighted_mean | 1 | [0, 1] | No | 1.0 |
| M2 | std | 2 | [0, +inf) | No | 0.25 |
| M3 | median | 1 | [0, 1] | No | 1.0 |
| M4 | max | 1 | [0, 1] | No | 1.0 |
| M5 | range | 2 | [0, 1] | No | 1.0 |
| M6 | skewness | 3 | (-inf, +inf) | Yes | 2.0 |
| M7 | kurtosis | 4 | [1, +inf) | No | 5.0 |

---

## M0: attention_weighted_mean

**Formula**:
```
M0(x, A) = sum(A(dt) * x(t + dt)) / sum(A(dt))
```

Where `A(dt) = exp(-3|dt|/H)` is the attention kernel.

**Properties**:
- **Output range**: [0, 1] (inherits from R3 input range)
- **Min window**: 1 frame
- **Signed**: No
- **MORPH_SCALE**: 1.0 (input already [0, 1])

**Key distinction**: M0 is the **only morph that uses the attention kernel weights**. All other morphs operate on unweighted windowed values. The attention kernel gives exponentially decaying weight to frames further from the reference point, making M0 a temporally-focused central tendency measure.

**Musical interpretation**: The "current value" of a feature with smooth temporal context. At short horizons, M0 closely tracks the instantaneous R3 value. At longer horizons, it provides a smoothed, recency-weighted average. Useful for representing "what the feature sounds like right now, given recent context."

**Common use cases**:
- SPU/ASU: Baseline feature level for auditory scene analysis
- All units: Default "current value" descriptor when temporal smoothing is desired
- Comparison baseline for M1 (unweighted) to measure recency bias

---

## M1: unweighted_mean

**Formula**:
```
M1(x) = sum(x) / N
```

Where N is the number of frames in the window.

**Properties**:
- **Output range**: [0, 1] (inherits from R3 input range)
- **Min window**: 1 frame
- **Signed**: No
- **MORPH_SCALE**: 1.0 (input already [0, 1])

**Musical interpretation**: The flat average of the feature over the window. Unlike M0, all frames contribute equally. At Macro horizons, M1 represents the "overall level" of a feature across a section -- for example, the average loudness of a passage, or the average spectral brightness of a phrase.

**Common use cases**:
- IMU/STU: Long-term average levels for memory and structural comparison
- MPU: Baseline beat-level energy for motor prediction
- All units: Reference value for computing deviations (M2, M6, M7 use M1 internally)

---

## M2: std

**Formula**:
```
M2(x) = sqrt(sum((x - mean)^2) / N)
```

Where `mean = M1(x)` and N is the window size in frames.

**Properties**:
- **Output range**: [0, +inf) (practically bounded by R3 [0, 1] input, so max ~0.5)
- **Min window**: 2 frames (need at least 2 values for meaningful deviation)
- **Signed**: No
- **MORPH_SCALE**: 0.25 (typical max ~0.25; scale maps to [0, 1])

**Musical interpretation**: How much the feature varies within the window. High M2 indicates dynamic, changing content (e.g., rapidly fluctuating loudness). Low M2 indicates steady, stable content (e.g., sustained tone at constant pitch). At Meso horizons, M2 on energy features captures beat-level dynamics. At Macro horizons, M2 captures section-level variability.

**Common use cases**:
- ASU: Feature variability as an indicator of scene complexity
- NDU: Baseline variability for novelty detection (unexpected changes in M2 signal novelty)
- ARU: Aesthetic evaluation of dynamic contrast within passages
- All units: Denominator in standardized measures (skewness, kurtosis use std internally)

---

## M3: median

**Formula**:
```
M3(x) = middle value of sorted window
```

For even N: average of the two middle values.

**Properties**:
- **Output range**: [0, 1] (inherits from R3 input range)
- **Min window**: 1 frame
- **Signed**: No
- **MORPH_SCALE**: 1.0 (input already [0, 1])

**Musical interpretation**: A robust measure of central tendency that is resistant to outliers. When a feature has occasional extreme values (e.g., a single loud transient in an otherwise quiet passage), M3 remains stable while M1 shifts. The difference M1 - M3 itself indicates the influence of outliers.

**Common use cases**:
- IMU: Robust level estimation for emotional memory (not skewed by transient peaks)
- PCU: Baseline prediction targets that are stable against outlier frames
- STU: Structural comparison where transient events should not dominate

---

## M4: max

**Formula**:
```
M4(x) = max(x_1, x_2, ..., x_N)
```

**Properties**:
- **Output range**: [0, 1] (inherits from R3 input range)
- **Min window**: 1 frame
- **Signed**: No
- **MORPH_SCALE**: 1.0 (input already [0, 1])

**Musical interpretation**: The peak value of the feature within the window. At Micro horizons, M4 captures onset peaks and attack transients. At Meso horizons, M4 captures beat-level peaks (downbeat accents). At Macro horizons, M4 captures the climax point of a section.

**Common use cases**:
- SPU: Onset detection via peak amplitude at H3-H6
- ARU: Section-level climax detection at H18-H22
- MPU: Beat accent strength at H9-H11
- AED: Arousal peak tracking at H6 and H16

---

## M5: range

**Formula**:
```
M5(x) = max(x) - min(x)
```

**Properties**:
- **Output range**: [0, 1] (max possible range for [0, 1] input)
- **Min window**: 2 frames
- **Signed**: No
- **MORPH_SCALE**: 1.0 (max possible value is 1.0)

**Musical interpretation**: The dynamic range of the feature within the window. High M5 indicates wide swings (e.g., loud-soft contrasts within a passage). Low M5 indicates constrained values (e.g., steady sustained tone). Related to M2 (std) but more sensitive to extremes. M5 = 0 implies perfect constancy; M5 = 1 implies full-range traversal.

**Common use cases**:
- AED: Arousal range detection (wide energy swings signal high arousal)
- CPD: Change point candidates (sudden increase in M5 at a boundary)
- ASU: Scene complexity indicator (wide feature range = complex scene)

---

## M6: skewness

**Formula**:
```
M6(x) = sum((x - mean)^3) / (N * std^3)
```

Where `mean = M1(x)` and `std = M2(x)`.

**Properties**:
- **Output range**: (-inf, +inf) (typical range ~[-3, 3] for musical signals)
- **Min window**: 3 frames (need at least 3 values for meaningful third moment)
- **Signed**: Yes (centered at 0.5 after scaling)
- **MORPH_SCALE**: 2.0 (signed scaling: `(raw / 2.0 + 1) / 2` maps [-2, 2] to [0, 1])

**Musical interpretation**: Asymmetry of the feature distribution within the window. Positive skewness (output > 0.5) means the distribution has a right tail -- most values are low with occasional high peaks (e.g., sparse loud accents in a quiet passage). Negative skewness (output < 0.5) means the distribution has a left tail -- most values are high with occasional dips (e.g., a loud passage with brief quiet gaps).

**Common use cases**:
- STU: Structural characterization -- verse sections often show different skewness than chorus
- IMU: Emotional valence correlates (asymmetric energy profiles map to different affects)
- NDU: Novelty detection -- skewness shifts indicate distributional change

**Edge cases**: When std = 0 (constant values), skewness is undefined. Implementation returns 0.0 (output maps to 0.5 after signed scaling).

---

## M7: kurtosis

**Formula**:
```
M7(x) = sum((x - mean)^4) / (N * std^4)
```

Where `mean = M1(x)` and `std = M2(x)`. This is the raw (non-excess) kurtosis; a normal distribution has kurtosis = 3.

**Properties**:
- **Output range**: [1, +inf) (minimum kurtosis = 1 for a Bernoulli distribution)
- **Min window**: 4 frames (need at least 4 values for meaningful fourth moment)
- **Signed**: No
- **MORPH_SCALE**: 5.0 (typical range ~[1, 5]; scale maps via `raw / 5.0`)

**Musical interpretation**: Tail heaviness of the feature distribution. High kurtosis (leptokurtic, > 3) indicates heavy tails -- the feature spends most time near the mean but occasionally takes extreme values (e.g., sparse transient events). Low kurtosis (platykurtic, < 3) indicates light tails -- values spread more uniformly without sharp peaks. At Macro horizons, kurtosis characterizes whether a section has a uniform texture or is punctuated by extreme events.

**Common use cases**:
- NDU: Heavy-tailed distributions signal unpredictable, surprise-rich content
- IMU: Kurtosis of energy features correlates with perceived "punchiness" or "smoothness"
- STU: Section differentiation -- different structural sections have characteristic kurtosis profiles

**Edge cases**: When std = 0, kurtosis is undefined. Implementation returns 1.0 (minimum kurtosis). At the minimum window of 4 frames, kurtosis estimates are noisy; prefer H5+ (8 frames) for reliable values.

---

## Horizon Interaction Summary

| Morph | H0 (1f) | H1 (2f) | H2 (3f) | H3 (4f) | H5+ (8f+) | Meso+ (52f+) |
|-------|:-------:|:-------:|:-------:|:-------:|:---------:|:------------:|
| M0 | Valid | Valid | Valid | Valid | Good | Excellent |
| M1 | Valid | Valid | Valid | Valid | Good | Excellent |
| M2 | -- | Valid | Valid | Valid | Good | Excellent |
| M3 | Valid | Valid | Valid | Valid | Good | Excellent |
| M4 | Valid | Valid | Valid | Valid | Good | Excellent |
| M5 | -- | Valid | Valid | Valid | Good | Excellent |
| M6 | -- | -- | Valid | Valid | Good | Excellent |
| M7 | -- | -- | -- | Valid | Good | Excellent |

**Legend**: `--` = below minimum window, `Valid` = computable but noisy, `Good` = reliable, `Excellent` = statistically robust.

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
