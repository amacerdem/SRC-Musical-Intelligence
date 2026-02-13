# H3 Registry -- Morph Catalog

**Version**: 2.0.0
**Count**: 24 morphs (M0-M23) across 5 categories
**Code reference**: `mi_beta.core.constants.MORPH_NAMES`, `mi_beta.core.constants.MORPH_SCALE`
**Implementation**: `mi_beta.ear.h3.morph.MorphComputer`
**Updated**: 2026-02-13

---

## Complete Morph Table

| Index | Name | Formula | Category | Min Window (frames) | Output Range | Description |
|:-----:|------|---------|----------|:-------------------:|:------------:|-------------|
| M0 | attention_weighted_mean | `sum(A(dt) * x) / sum(A(dt))` | Distribution | 1 | [0, 1] | Attention-weighted mean using temporal kernel |
| M1 | unweighted_mean | `sum(x) / N` | Distribution | 1 | [0, 1] | Simple arithmetic mean over window |
| M2 | std | `sqrt(sum((x - mean)^2) / N)` | Distribution | 2 | [0, +inf) | Standard deviation of values in window |
| M3 | median | `middle value` | Distribution | 1 | [0, 1] | Median (50th percentile) of window values |
| M4 | max | `max(x)` | Distribution | 1 | [0, 1] | Maximum value in window |
| M5 | range | `max(x) - min(x)` | Distribution | 2 | [0, 1] | Dynamic range within window |
| M6 | skewness | `sum((x - mean)^3) / (N * std^3)` | Distribution | 3 | (-inf, +inf) | Third standardized moment; asymmetry of distribution |
| M7 | kurtosis | `sum((x - mean)^4) / (N * std^4)` | Distribution | 4 | [1, +inf) | Fourth standardized moment; tail heaviness |
| M8 | velocity | `dx/dt` | Dynamics | 2 | (-inf, +inf) | First difference (instantaneous rate of change) |
| M9 | velocity_mean | `mean(dx/dt)` | Dynamics | 2 | (-inf, +inf) | Mean of first differences over window |
| M10 | velocity_std | `std(dx/dt)` | Dynamics | 2 | [0, +inf) | Standard deviation of first differences |
| M11 | acceleration | `d^2x/dt^2` | Dynamics | 3 | (-inf, +inf) | Second difference (rate of change of velocity) |
| M12 | acceleration_mean | `mean(d^2x/dt^2)` | Dynamics | 3 | (-inf, +inf) | Mean of second differences over window |
| M13 | acceleration_std | `std(d^2x/dt^2)` | Dynamics | 3 | [0, +inf) | Standard deviation of second differences |
| M14 | periodicity | `max(autocorrelation[lag > 0])` | Rhythm | 4 | [0, 1] | Peak autocorrelation at non-zero lag |
| M15 | smoothness | `1 / (1 + \|jerk\| / sigma)` | Dynamics | 3 | (0, 1] | Inverse jerk magnitude, normalized; 1 = perfectly smooth |
| M16 | curvature | `mean(\|d^2x/dt^2\|)` | Symmetry | 3 | [0, +inf) | Mean absolute second derivative |
| M17 | shape_period | `zero-crossing period of velocity` | Rhythm | 4 | [0, +inf) | Period estimated from velocity zero-crossings |
| M18 | trend | `linear regression slope` | Dynamics | 2 | (-inf, +inf) | OLS slope of value vs. time |
| M19 | stability | `1 / (1 + var / sigma^2)` | Symmetry | 2 | (0, 1] | Inverse normalized variance; 1 = perfectly stable |
| M20 | entropy | `-sum(p * log(p))` from 16-bin histogram | Information | 4 | [0, 1] | Shannon entropy, normalized to [0, 1] via log(16) |
| M21 | zero_crossings | `count of sign changes in (x - mean)` | Dynamics | 2 | [0, N-1] | Number of times signal crosses its mean |
| M22 | peaks | `count of local maxima` | Rhythm | 3 | [0, N-2] | Number of local maxima in window |
| M23 | symmetry | `correlation(x, reverse(x))` | Symmetry | 2 | [-1, 1] | Pearson correlation of signal with its time-reverse |

---

## Category Grouping

### Distribution (M0-M7) -- 8 morphs

Statistical moments and order statistics describing the value distribution within the temporal window.

| Index | Name | Key Property |
|:-----:|------|-------------|
| M0 | attention_weighted_mean | Kernel-weighted central tendency (law-dependent) |
| M1 | unweighted_mean | Simple central tendency |
| M2 | std | Spread / variability |
| M3 | median | Robust central tendency (outlier-resistant) |
| M4 | max | Peak value (onset/attack detection) |
| M5 | range | Dynamic range / volatility |
| M6 | skewness | Asymmetry (positive = right-tailed) |
| M7 | kurtosis | Tail weight (>3 = heavy-tailed vs. normal) |

### Dynamics (M8-M13, M15, M18, M21) -- 9 morphs

Temporal derivatives and trend descriptors capturing how features change over time.

| Index | Name | Key Property |
|:-----:|------|-------------|
| M8 | velocity | Instantaneous change rate |
| M9 | velocity_mean | Average change rate over window |
| M10 | velocity_std | Variability of change rate |
| M11 | acceleration | Instantaneous change of change rate |
| M12 | acceleration_mean | Average acceleration over window |
| M13 | acceleration_std | Variability of acceleration |
| M15 | smoothness | Jerk-based smoothness measure |
| M18 | trend | Linear trend direction and magnitude |
| M21 | zero_crossings | Oscillation frequency proxy |

### Rhythm (M14, M17, M22) -- 3 morphs

Periodicity and repetition descriptors for rhythmic feature analysis.

| Index | Name | Key Property |
|:-----:|------|-------------|
| M14 | periodicity | Strength of dominant periodicity |
| M17 | shape_period | Dominant period from velocity zero-crossings |
| M22 | peaks | Event density / pulse count |

### Information (M20) -- 1 morph

Information-theoretic descriptor measuring unpredictability of the feature distribution.

| Index | Name | Key Property |
|:-----:|------|-------------|
| M20 | entropy | Distributional complexity / unpredictability |

### Symmetry (M16, M19, M23) -- 3 morphs

Shape and stability descriptors measuring geometric properties of the temporal trajectory.

| Index | Name | Key Property |
|:-----:|------|-------------|
| M16 | curvature | Bending magnitude of trajectory |
| M19 | stability | Temporal consistency / stationarity |
| M23 | symmetry | Time-reversal invariance |

---

## MORPH_SCALE Calibration

Each morph output is normalized to [0, 1] via affine transformation: `output = gain * raw + bias`.

The `MORPH_SCALE` constant in `mi_beta/core/constants.py` stores `(gain, bias)` tuples calibrated against a representative dataset (1st-99th percentile mapping to [0, 1]).

| Index | Name | Gain | Bias | Notes |
|:-----:|------|-----:|-----:|-------|
| M0 | attention_weighted_mean | TBD | TBD | Input already [0,1]; scale may be ~(1.0, 0.0) |
| M1 | unweighted_mean | TBD | TBD | Input already [0,1]; scale may be ~(1.0, 0.0) |
| M2 | std | TBD | TBD | Raw range [0, ~0.3]; needs upscaling |
| M3 | median | TBD | TBD | Input already [0,1]; scale may be ~(1.0, 0.0) |
| M4 | max | TBD | TBD | Input already [0,1]; scale may be ~(1.0, 0.0) |
| M5 | range | TBD | TBD | Raw range [0,1]; may need mild rescaling |
| M6 | skewness | TBD | TBD | Raw range ~[-3, 3]; needs centering + scaling |
| M7 | kurtosis | TBD | TBD | Raw range ~[1, 20]; needs scaling + offset |
| M8 | velocity | TBD | TBD | Raw range ~[-0.5, 0.5]; needs centering |
| M9 | velocity_mean | TBD | TBD | Raw range ~[-0.1, 0.1]; needs centering + upscaling |
| M10 | velocity_std | TBD | TBD | Raw range [0, ~0.3]; needs upscaling |
| M11 | acceleration | TBD | TBD | Raw range ~[-0.3, 0.3]; needs centering |
| M12 | acceleration_mean | TBD | TBD | Raw range ~[-0.05, 0.05]; needs centering + upscaling |
| M13 | acceleration_std | TBD | TBD | Raw range [0, ~0.2]; needs upscaling |
| M14 | periodicity | TBD | TBD | Raw range [0,1]; may be ~(1.0, 0.0) |
| M15 | smoothness | TBD | TBD | Raw range (0,1]; may be ~(1.0, 0.0) |
| M16 | curvature | TBD | TBD | Raw range [0, ~0.5]; needs upscaling |
| M17 | shape_period | TBD | TBD | Raw range [0, window_size]; needs normalization |
| M18 | trend | TBD | TBD | Raw range ~[-0.01, 0.01]; needs centering + upscaling |
| M19 | stability | TBD | TBD | Raw range (0,1]; may be ~(1.0, 0.0) |
| M20 | entropy | TBD | TBD | Already normalized to [0,1]; likely (1.0, 0.0) |
| M21 | zero_crossings | TBD | TBD | Raw range [0, N-1]; needs division by window size |
| M22 | peaks | TBD | TBD | Raw range [0, N-2]; needs division by window size |
| M23 | symmetry | TBD | TBD | Raw range [-1,1]; needs centering + scaling |

**TBD**: Actual calibration values will be populated in Phase 5 from `mi_beta/core/constants.py` after calibration runs. The Notes column indicates expected raw ranges to guide calibration.

### Calibration Protocol

1. Select a representative dataset (~100 tracks, diverse genres)
2. Compute each morph raw output across all (r3_idx, horizon, law) combinations
3. Record the 1st and 99th percentile values (P1, P99)
4. Set `gain = 1.0 / (P99 - P1)` and `bias = -P1 / (P99 - P1)`
5. Clamp final output to [0, 1] as a safety net

---

## Minimum Window Requirements

Morphs have minimum frame requirements to produce valid output. When a horizon's frame count is below the minimum, the morph output is undefined (returns NaN or 0.0, depending on implementation).

| Min Window | Morphs |
|:----------:|--------|
| 1 frame | M0, M1, M3, M4 |
| 2 frames | M2, M5, M8, M9, M10, M18, M19, M21, M23 |
| 3 frames | M6, M11, M12, M13, M15, M16, M22 |
| 4 frames | M7, M14, M17, M20 |

**Implication**: At H0 (1 frame), only M0, M1, M3, M4 are computable. At H1 (2 frames), the 2-frame morphs become available. All 24 morphs are available from H3 (4 frames) onward.

---

## Implementation Notes

### MorphComputer Architecture

```python
class MorphComputer:
    """Computes morph values over windowed R3 feature tensors.

    Each morph is a method: compute_M{idx}(window, weights) -> tensor
    Dispatch table maps morph index to method.
    """

    def compute(self, window: Tensor, morph_idx: int,
                weights: Optional[Tensor] = None) -> Tensor:
        """Dispatch to morph computation method."""
        ...
```

### Special Cases

- **M0 (attention_weighted_mean)**: Only morph that uses the attention kernel weights `A(dt)`. All other morphs use unweighted windowed values.
- **M20 (entropy)**: Uses a 16-bin histogram, making it sensitive to window size. Short windows (< 16 frames) may produce quantization artifacts.
- **M17 (shape_period)**: Output is in frames, not normalized. MORPH_SCALE must convert to a [0, 1] fraction of the horizon duration.
- **M21, M22 (zero_crossings, peaks)**: Count-valued morphs. MORPH_SCALE normalizes by dividing by window size.

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry index**: [00-INDEX.md](00-INDEX.md)
