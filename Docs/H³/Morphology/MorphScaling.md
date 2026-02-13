# H3 Morphology -- MORPH_SCALE Calibration

**Version**: 2.0.0
**Purpose**: Normalization protocol for mapping all morph raw outputs to [0, 1]
**Code reference**: `mi_beta.core.constants.MORPH_SCALE`
**Implementation**: `mi_beta.ear.h3.morph.MorphComputer` (normalization step)
**Updated**: 2026-02-13

---

## 1. Purpose

Each of the 24 morphs produces values in a different natural range. M1 (unweighted_mean) outputs values in [0, 1] because its R3 input is already normalized. M8 (velocity) outputs values around [-0.1, 0.1]. M7 (kurtosis) outputs values in [1, 20+]. The downstream C3 models expect all H3 outputs in a uniform [0, 1] range.

`MORPH_SCALE` provides per-morph normalization constants that transform raw morph outputs into the [0, 1] range. This normalization is the final step before H3 values enter the C3 models.

---

## 2. Normalization Formulas

### 2.1 Unsigned Morphs

For morphs whose raw output is non-negative (M0-M5, M7, M10, M13, M14, M15, M17, M19, M20, M21, M22):

```
output = clamp(raw / MORPH_SCALE[morph_idx], 0.0, 1.0)
```

This is equivalent to the affine form with calibrated gain and bias:

```
gain = 1 / (P99 - P1)
bias = -P1 / (P99 - P1)
output = clamp(gain * raw + bias, 0.0, 1.0)
```

Where P1 and P99 are the 1st and 99th percentile values from the calibration dataset.

For morphs whose raw output naturally starts at 0 (e.g., M2 std, M10 velocity_std), this simplifies to `gain = 1 / P99` and `bias = 0`, which is the same as dividing by `MORPH_SCALE`.

### 2.2 Signed Morphs

For morphs whose raw output spans a signed range centered at zero (M6, M8, M9, M11, M12, M18, M23) and curvature (M16):

```
output = clamp((raw / MORPH_SCALE[morph_idx] + 1) / 2, 0.0, 1.0)
```

This centers zero at 0.5:
- `raw = 0` maps to `output = 0.5`
- `raw = +MORPH_SCALE` maps to `output = 1.0`
- `raw = -MORPH_SCALE` maps to `output = 0.0`

**Signed morphs**: M6 (skewness), M8 (velocity), M9 (velocity_mean), M11 (acceleration), M12 (acceleration_mean), M16 (curvature), M18 (trend), M23 (symmetry).

---

## 3. MORPH_SCALE Array

The canonical `MORPH_SCALE` values from `mi_beta/core/constants.py`:

```python
MORPH_SCALE = [
    1.0,    # M0  attention_weighted_mean  -- R3 input already [0,1]
    1.0,    # M1  unweighted_mean          -- R3 input already [0,1]
    0.25,   # M2  std                      -- typical max ~0.25
    1.0,    # M3  median                   -- R3 input already [0,1]
    1.0,    # M4  max                      -- R3 input already [0,1]
    1.0,    # M5  range                    -- max possible 1.0
    2.0,    # M6  skewness                 -- typical range [-2, 2]    (signed)
    5.0,    # M7  kurtosis                 -- typical range [1, 5]
    0.1,    # M8  velocity                 -- typical max ~0.1/frame   (signed)
    0.05,   # M9  velocity_mean            -- smoothed velocity        (signed)
    0.05,   # M10 velocity_std             -- velocity dispersion
    0.01,   # M11 acceleration             -- typical max ~0.01/frame^2 (signed)
    0.005,  # M12 acceleration_mean        -- smoothed acceleration    (signed)
    0.005,  # M13 acceleration_std         -- acceleration dispersion
    1.0,    # M14 periodicity              -- autocorrelation [0,1]
    1.0,    # M15 smoothness               -- [0,1] by construction
    0.1,    # M16 curvature                -- typical max ~0.1         (signed)
    100.0,  # M17 shape_period             -- frames; max ~100 frames
    0.01,   # M18 trend                    -- slope per frame          (signed)
    1.0,    # M19 stability                -- [0,1] by construction
    3.0,    # M20 entropy                  -- max ~log2(16) = 4.0 bits
    20.0,   # M21 zero_crossings           -- max ~20 crossings
    10.0,   # M22 peaks                    -- max ~10 peaks
    1.0,    # M23 symmetry                 -- correlation [-1,1]       (signed)
]
```

### 3.1 Scale Value Summary Table

| Index | Name | MORPH_SCALE | Type | Normalization Formula |
|:-----:|------|:-----------:|:----:|----------------------|
| M0 | attention_weighted_mean | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M1 | unweighted_mean | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M2 | std | 0.25 | Unsigned | `clamp(raw / 0.25, 0, 1)` |
| M3 | median | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M4 | max | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M5 | range | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M6 | skewness | 2.0 | Signed | `clamp((raw / 2.0 + 1) / 2, 0, 1)` |
| M7 | kurtosis | 5.0 | Unsigned | `clamp(raw / 5.0, 0, 1)` |
| M8 | velocity | 0.1 | Signed | `clamp((raw / 0.1 + 1) / 2, 0, 1)` |
| M9 | velocity_mean | 0.05 | Signed | `clamp((raw / 0.05 + 1) / 2, 0, 1)` |
| M10 | velocity_std | 0.05 | Unsigned | `clamp(raw / 0.05, 0, 1)` |
| M11 | acceleration | 0.01 | Signed | `clamp((raw / 0.01 + 1) / 2, 0, 1)` |
| M12 | acceleration_mean | 0.005 | Signed | `clamp((raw / 0.005 + 1) / 2, 0, 1)` |
| M13 | acceleration_std | 0.005 | Unsigned | `clamp(raw / 0.005, 0, 1)` |
| M14 | periodicity | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M15 | smoothness | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M16 | curvature | 0.1 | Signed | `clamp((raw / 0.1 + 1) / 2, 0, 1)` |
| M17 | shape_period | 100.0 | Unsigned | `clamp(raw / 100.0, 0, 1)` |
| M18 | trend | 0.01 | Signed | `clamp((raw / 0.01 + 1) / 2, 0, 1)` |
| M19 | stability | 1.0 | Unsigned | `clamp(raw / 1.0, 0, 1)` |
| M20 | entropy | 3.0 | Unsigned | `clamp(raw / 3.0, 0, 1)` |
| M21 | zero_crossings | 20.0 | Unsigned | `clamp(raw / 20.0, 0, 1)` |
| M22 | peaks | 10.0 | Unsigned | `clamp(raw / 10.0, 0, 1)` |
| M23 | symmetry | 1.0 | Signed | `clamp((raw / 1.0 + 1) / 2, 0, 1)` |

---

## 4. Calibration Protocol

The MORPH_SCALE values are determined through empirical calibration. The protocol is:

### Step 1: Select Representative Dataset

Choose a diverse dataset of ~100 tracks spanning multiple genres, tempos, instrumentations, and dynamic ranges. The dataset should include:
- Quiet and loud passages
- Fast and slow tempos
- Solo and ensemble textures
- Acoustic and electronic timbres
- Simple and complex harmonic language

### Step 2: Compute Raw Morph Outputs

For each morph M, compute the raw (pre-normalization) output across all (r3_idx, horizon, law) combinations demanded by any C3 model. This produces a large distribution of raw values per morph.

### Step 3: Record Percentiles

For each morph, record:
- **P1**: 1st percentile of raw values
- **P99**: 99th percentile of raw values
- **P50**: Median (for sanity checking)

### Step 4: Compute Gain and Bias

**For unsigned morphs** (P1 near 0):
```
MORPH_SCALE[m] = P99
gain = 1.0 / P99
bias = 0.0
```

**For unsigned morphs** (P1 not near 0):
```
gain = 1.0 / (P99 - P1)
bias = -P1 / (P99 - P1)
MORPH_SCALE[m] = P99 - P1  (effective scale)
```

**For signed morphs** (symmetric around 0):
```
MORPH_SCALE[m] = max(|P1|, |P99|)
```

### Step 5: Validate

After setting MORPH_SCALE values:
1. Recompute all morph outputs with normalization applied
2. Verify < 2% of outputs fall outside [0, 1] (i.e., are clamped)
3. Verify the distribution is well-spread within [0, 1] (not clustered near 0 or 1)
4. Verify signed morphs center near 0.5

---

## 5. Per-Morph Calibration Status

| Index | Name | Calibration Status | Notes |
|:-----:|------|:------------------:|-------|
| M0 | attention_weighted_mean | Preliminary | Input is [0,1]; scale 1.0 is theoretical |
| M1 | unweighted_mean | Preliminary | Input is [0,1]; scale 1.0 is theoretical |
| M2 | std | Preliminary | Scale 0.25 is estimated from R3 variance range |
| M3 | median | Preliminary | Input is [0,1]; scale 1.0 is theoretical |
| M4 | max | Preliminary | Input is [0,1]; scale 1.0 is theoretical |
| M5 | range | Preliminary | Max possible 1.0; may need mild rescaling |
| M6 | skewness | Preliminary | Scale 2.0 estimated; true range TBD |
| M7 | kurtosis | Preliminary | Scale 5.0 estimated; excess kurtosis range TBD |
| M8 | velocity | Preliminary | Scale 0.1 estimated from R3 frame-to-frame variation |
| M9 | velocity_mean | Preliminary | Scale 0.05 estimated |
| M10 | velocity_std | Preliminary | Scale 0.05 estimated |
| M11 | acceleration | Preliminary | Scale 0.01 estimated |
| M12 | acceleration_mean | Preliminary | Scale 0.005 estimated |
| M13 | acceleration_std | Preliminary | Scale 0.005 estimated |
| M14 | periodicity | Preliminary | Autocorrelation is [0,1]; scale 1.0 is theoretical |
| M15 | smoothness | Preliminary | Output is (0,1]; scale 1.0 is theoretical |
| M16 | curvature | Preliminary | Scale 0.1 estimated from typical second derivatives |
| M17 | shape_period | Preliminary | Scale 100.0 frames = ~580 ms; covers tempo range |
| M18 | trend | Preliminary | Scale 0.01 estimated from regression slopes |
| M19 | stability | Preliminary | Output is (0,1]; scale 1.0 is theoretical |
| M20 | entropy | Preliminary | Scale 3.0; max raw = 4.0 bits = log2(16) |
| M21 | zero_crossings | Preliminary | Scale 20.0 estimated from typical count range |
| M22 | peaks | Preliminary | Scale 10.0 estimated from typical count range |
| M23 | symmetry | Preliminary | Correlation is [-1,1]; scale 1.0 is exact |

**Status key**:
- **Preliminary**: Scale value is an educated estimate based on theoretical ranges and informal testing. Not empirically calibrated against a representative dataset.
- **Calibrated**: Scale value derived from the formal calibration protocol (Step 1-5 above). -- *None yet; all calibration deferred to Phase 5.*

---

## 6. Edge Cases

### 6.1 Division by Zero

When `MORPH_SCALE[m] = 0` (should never occur in practice, as all scales are positive), the normalization would produce division by zero. Implementation guard:

```python
if MORPH_SCALE[morph_idx] == 0:
    return 0.0  # or NaN, depending on policy
```

### 6.2 Clamp Behavior

The `clamp(x, 0.0, 1.0)` operation is the final safety net. Values that exceed the expected range (e.g., extreme kurtosis, unusually large velocity) are hard-clipped to [0, 1]. The calibration protocol targets < 2% clamping rate, meaning extreme values are rare.

**Clamping is not an error** -- it is an expected boundary condition for outlier frames. However, if clamping occurs frequently (> 5% of frames for a given morph), the MORPH_SCALE value needs recalibration.

### 6.3 NaN Handling for Below-Min-Window Morphs

When a morph is computed at a horizon whose frame count is below the morph's minimum window requirement, the raw output is undefined. The implementation returns NaN or 0.0:

| Policy | Behavior | Downstream Effect |
|--------|----------|------------------|
| NaN propagation | `raw = NaN` --> `output = NaN` | C3 model must handle NaN inputs (mask or substitute) |
| Zero substitution | `raw = NaN` --> `output = 0.0` | C3 model sees zero, which may be misleading for signed morphs |

**Current policy**: Zero substitution for below-min-window cases. For signed morphs, this means the output is 0.0 (not 0.5), which incorrectly implies a maximally negative value. This is a known limitation; models should not demand morphs at horizons below the minimum window.

**Recommendation**: C3 models should validate their H3 demands against the minimum window table in [Registry/MorphCatalog.md](../Registry/MorphCatalog.md) to ensure all demanded tuples are within valid horizons.

### 6.4 Count-Valued Morphs

M21 (zero_crossings) and M22 (peaks) produce integer counts. Their MORPH_SCALE values (20.0 and 10.0 respectively) normalize the count to a [0, 1] fraction. This means:
- M21: 20 zero crossings maps to 1.0; 0 crossings maps to 0.0
- M22: 10 peaks maps to 1.0; 0 peaks maps to 0.0

At large horizons (Macro/Ultra), the actual count can exceed the MORPH_SCALE value, triggering clamping. Recalibration may adjust these scales upward for large-horizon applications.

### 6.5 Horizon-Dependent Scaling

Some morphs have raw ranges that vary with horizon size:
- **M21, M22**: Maximum count grows with window size (more frames = more possible crossings/peaks)
- **M17**: Period in frames; larger horizons can capture longer periods

The current MORPH_SCALE uses a fixed value for all horizons. A horizon-adaptive scaling system is under consideration for Phase 5, where the scale would vary as a function of frame count.

---

## 7. Relationship to H3-TEMPORAL-ARCHITECTURE.md

The `MORPH_SCALE` array and normalization formula documented here correspond to Section 5.3 of [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md). The architecture document provides the canonical scale values and the normalization formula. This document expands on the calibration protocol, edge cases, and per-morph status.

The values listed in Section 3 of this document must match those in the architecture document and in `mi_beta/core/constants.py`. Any discrepancy should be resolved by treating `constants.py` as the source of truth.

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| H3 architecture (Section 5.3) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Extension guide (adding morphs) | [../EXTENSION-GUIDE.md](../EXTENSION-GUIDE.md) |
| Morphology index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MORPH_SCALE constants | `mi_beta/core/constants.py` |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
