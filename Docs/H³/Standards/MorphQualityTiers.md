# H3 Morph Quality Tiers

> Version 2.0.0 | Updated 2026-02-13

---

## 1. Overview

Each of the 24 H3 morphs has different numerical properties depending on window size (horizon), input signal characteristics, and the statistical operation involved. A morph that is perfectly stable at Macro horizons (thousands of frames) may produce unreliable or degenerate results at Micro horizons (1-43 frames) where sample counts are insufficient for the underlying estimator.

This document defines a three-tier quality classification for every morph-band combination and assesses whether the current `MORPH_SCALE` calibration produces well-behaved [0, 1] outputs across typical music inputs.

---

## 2. Quality Tier Definitions

| Tier | Label | Criteria |
|:----:|-------|---------|
| **R** | Reliable | Stable computation across all valid inputs. Output variance from numerical noise < 1% of signal variance. Estimator bias negligible relative to signal magnitude. |
| **M** | Marginal | Acceptable for most inputs but may degrade for edge cases (constant input, very short windows, extreme dynamic range). Output variance from numerical noise < 10% of signal variance. |
| **U** | Unstable | Numerical issues expected. Results may be NaN, infinite, or dominated by noise. Output variance from numerical noise may exceed signal variance. Not suitable for downstream decision-making without additional guards. |

**Tier assignment rationale**: Tiers are determined by the minimum sample count required for the underlying statistical estimator to converge, cross-referenced against the frame counts available at each horizon band.

---

## 3. Per-Morph Quality Matrix

### 3.1 Distribution Morphs (M0-M7)

| Morph | ID | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) |
|-------|----|:-:|:-:|:-:|:-:|
| value | M0 | R | R | R | R |
| mean | M1 | R | R | R | R |
| std | M2 | M | R | R | R |
| median | M3 | R | R | R | R |
| max | M4 | R | R | R | R |
| range | M5 | M | R | R | R |
| skewness | M6 | U | M | R | R |
| kurtosis | M7 | U | M | R | R |

**Notes**: M0 (value), M1 (mean), M3 (median), M4 (max) are simple operations that are always stable regardless of window size. M2 (std) and M5 (range) become marginal at Micro because variance estimation with fewer than 10 samples has high relative error. M6 (skewness) and M7 (kurtosis) require at least 30 samples for stable higher-moment estimation and are unstable at Micro where most horizons have fewer than 30 frames.

### 3.2 Dynamics Morphs (M8-M13, M15)

| Morph | ID | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) |
|-------|----|:-:|:-:|:-:|:-:|
| velocity | M8 | M | R | R | R |
| velocity_mean | M9 | M | R | R | R |
| velocity_std | M10 | M | R | R | R |
| acceleration | M11 | U | R | R | R |
| acceleration_mean | M12 | U | R | R | R |
| acceleration_std | M13 | U | R | R | R |
| smoothness | M15 | M | R | R | R |

**Notes**: First derivatives (M8-M10, M15) need at least 3 points (2 differences) for a meaningful estimate, making them marginal at early Micro horizons (H0=1, H1=2) and reliable from H2 onward. Second derivatives (M11-M13) need at least 5 points and are unstable at H0-H3 (1-5 frames).

### 3.3 Rhythm Morphs (M14, M17, M22)

| Morph | ID | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) |
|-------|----|:-:|:-:|:-:|:-:|
| periodicity | M14 | U | R | R | R |
| shape_period | M17 | U | M | R | R |
| peaks | M22 | U | M | R | R |

**Notes**: Autocorrelation-based periodicity (M14) requires sufficient samples to detect at least one full cycle, making it unreliable below ~30 frames. Shape_period (M17) and peaks (M22) similarly need enough data to identify periodic structure and local maxima.

### 3.4 Trend and Stability Morphs (M18, M19, M21)

| Morph | ID | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) |
|-------|----|:-:|:-:|:-:|:-:|
| trend | M18 | M | R | R | R |
| stability | M19 | M | R | R | R |
| zero_crossings | M21 | M | R | R | R |

**Notes**: Linear regression slope (M18) and inverse variance (M19) need at least 10 frames for reliable estimation. Zero crossings (M21) need sufficient span to be meaningful. All three are marginal at Micro.

### 3.5 Information and Symmetry Morphs (M16, M20, M23)

| Morph | ID | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) |
|-------|----|:-:|:-:|:-:|:-:|
| curvature | M16 | U | M | R | R |
| entropy | M20 | U | R | R | R |
| symmetry | M23 | U | M | R | R |

**Notes**: Shannon entropy (M20) requires distributional diversity for a meaningful histogram; below ~20 frames the 16-bin histogram is too sparse. Curvature (M16) depends on second-derivative stability and needs ~30 frames for reliable shape estimation. Symmetry (M23) requires comparing first and second halves of the window, needing at least ~30 frames for meaningful comparison.

---

## 4. Minimum Window Size Requirements

| Morph | ID | MORPH_SCALE (gain, bias) | Min Frames (R) | Min Frames (M) | Limiting Factor |
|-------|:--:|:------------------------:|:--:|:--:|----------------|
| value | M0 | (1.0, 0.0) | 1 | 1 | None |
| mean | M1 | (1.0, 0.0) | 1 | 1 | None |
| std | M2 | (4.0, 0.0) | 10 | 3 | Variance convergence |
| median | M3 | (1.0, 0.0) | 1 | 1 | None |
| max | M4 | (1.0, 0.0) | 1 | 1 | None |
| range | M5 | (2.0, 0.0) | 10 | 3 | Min/max separation |
| skewness | M6 | (0.25, 0.5) | 30 | 10 | Third moment convergence |
| kurtosis | M7 | (0.1, 0.5) | 50 | 20 | Fourth moment convergence |
| velocity | M8 | (5.0, 0.5) | 3 | 2 | Finite difference |
| velocity_mean | M9 | (5.0, 0.5) | 5 | 3 | Derivative + aggregation |
| velocity_std | M10 | (10.0, 0.0) | 10 | 5 | Derivative variance |
| acceleration | M11 | (20.0, 0.5) | 5 | 3 | Second difference |
| acceleration_mean | M12 | (20.0, 0.5) | 8 | 5 | Second derivative + aggregation |
| acceleration_std | M13 | (40.0, 0.0) | 15 | 8 | Second derivative variance |
| periodicity | M14 | (1.0, 0.0) | 30 | 15 | Autocorrelation cycle detection |
| smoothness | M15 | (2.0, 0.0) | 3 | 2 | Derivative magnitude |
| curvature | M16 | (10.0, 0.5) | 30 | 10 | Second derivative shape |
| shape_period | M17 | (0.02, 0.0) | 50 | 20 | Spectral peak detection |
| trend | M18 | (50.0, 0.5) | 10 | 5 | Regression span |
| stability | M19 | (4.0, 0.0) | 10 | 5 | Inverse variance convergence |
| entropy | M20 | (0.5, 0.0) | 20 | 8 | Histogram bin population |
| zero_crossings | M21 | (0.1, 0.0) | 10 | 5 | Crossing event count |
| peaks | M22 | (0.2, 0.0) | 30 | 15 | Local maxima detection |
| symmetry | M23 | (1.0, 0.5) | 30 | 10 | Half-window comparison |

---

## 5. MORPH_SCALE Adequacy Assessment

The `MORPH_SCALE` array in `mi_beta/core/constants.py` defines `(gain, bias)` pairs for normalizing raw morph outputs to [0, 1] via `output = clamp(raw * gain + bias, 0, 1)`. The following assessment evaluates whether each scale produces well-distributed outputs for typical music inputs.

### 5.1 Well-Calibrated Morphs

| Morph | ID | Scale | Assessment |
|-------|:--:|:-----:|------------|
| value | M0 | (1.0, 0.0) | Good. R3 features are already in [0, 1]. |
| mean | M1 | (1.0, 0.0) | Good. Mean of [0, 1] values stays in [0, 1]. |
| std | M2 | (4.0, 0.0) | Good. Std of [0, 1] values rarely exceeds 0.25. |
| median | M3 | (1.0, 0.0) | Good. Same reasoning as M1. |
| max | M4 | (1.0, 0.0) | Good. Max of [0, 1] values stays in [0, 1]. |
| range | M5 | (2.0, 0.0) | Good. Range of [0, 1] values is at most 1.0; gain=2 uses ~50% for typical music. |
| skewness | M6 | (0.25, 0.5) | Good. Skewness centered at 0, gain contracts to avoid saturation. |
| kurtosis | M7 | (0.1, 0.5) | Good. Kurtosis centered at 3 (normal), shifted and scaled to ~0.5 center. |
| periodicity | M14 | (1.0, 0.0) | Good. Autocorrelation peak is naturally in [0, 1]. |
| smoothness | M15 | (2.0, 0.0) | Good. Derivative magnitudes are typically small for music. |
| symmetry | M23 | (1.0, 0.5) | Good. Symmetry measure centered at 0, bias shifts to 0.5. |

### 5.2 Clipping-Prone Morphs

| Morph | ID | Scale | Risk | Explanation |
|-------|:--:|:-----:|:----:|------------|
| velocity | M8 | (5.0, 0.5) | **Moderate** | May clip for percussive transients where onset_strength velocity at Micro horizons produces large derivatives. Typical clipping rate: ~5-15% of frames for percussive material. |
| velocity_std | M10 | (10.0, 0.0) | **Moderate** | High gain amplifies derivative variance. May saturate at 1.0 for highly variable signals. |
| acceleration | M11 | (20.0, 0.5) | **High** | Frequently clips for impulsive inputs (e.g., snare hits, staccato). Second derivatives of transient features can easily exceed 0.025 in magnitude. |
| acceleration_mean | M12 | (20.0, 0.5) | **Moderate** | Aggregation smooths peaks but gain=20 still amplifies. |
| acceleration_std | M13 | (40.0, 0.0) | **High** | Highest gain among all morphs. Second-derivative variance is amplified 40x, producing frequent saturation at 1.0 for any non-smooth input. |
| trend | M18 | (50.0, 0.5) | **Low** | Despite the highest gain in the system, linear regression slopes over H3 windows are typically very small (1e-4 to 1e-2), so 50x amplification rarely causes clipping. Exception: abrupt level changes at short horizons. |

### 5.3 Underutilized-Range Morphs

| Morph | ID | Scale | Issue | Explanation |
|-------|:--:|:-----:|:-----:|------------|
| shape_period | M17 | (0.02, 0.0) | **Underutilized** | Raw shape_period values (dominant cycle in frames) can be large. Gain=0.02 compresses them heavily, but this is intentional: it normalizes periods up to ~50 frames to [0, 1]. |
| zero_crossings | M21 | (0.1, 0.0) | **Underutilized** | Normalized zero-crossing count for stable signals (few crossings) maps to near-zero output. The [0, 1] range is poorly utilized when inputs are non-oscillatory. |
| peaks | M22 | (0.2, 0.0) | **Underutilized** | Peak count normalized by gain=0.2 means only 5+ peaks saturate the range. Smooth signals with 0-1 peaks produce outputs near 0.0, leaving most of the range unused. |
| entropy | M20 | (0.5, 0.0) | **Mild** | Maximum normalized entropy is ~1.0 (uniform 16-bin histogram), so gain=0.5 caps output at ~0.5. Full [0, 1] range is not utilized, but the lower half is well-distributed. |

---

## 6. Recommendations

### Phase 5: Quality Flags

Implement per-morph quality flags in the `H3Extractor` output. For each computed tuple `(r3_idx, horizon, morph, law)`, attach a quality tier indicator (R/M/U) based on the horizon band and morph combination. Downstream C3 models can use this flag to weight or discard marginal/unstable inputs.

### Phase 6: MORPH_SCALE Recalibration

Recalibrate `MORPH_SCALE` using corpus statistics from a representative music dataset. Specific actions:

1. Collect raw morph output distributions across a diverse music corpus (classical, jazz, rock, electronic, speech).
2. Fit gain/bias per morph to achieve a target distribution: median at 0.5, 95th percentile at 0.95.
3. Address clipping-prone morphs (M8, M10, M11, M13) by reducing gain or applying sigmoid normalization instead of linear clamp.
4. Address underutilized morphs (M21, M22) by increasing gain or switching to log-scale normalization.

### Documentation

Document known clipping behaviors in individual model documentation. Models consuming M11 (acceleration) or M13 (acceleration_std) should note that inputs are frequently saturated for percussive material and interpret accordingly.

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [../Morphology/MorphScaling.md](../Morphology/MorphScaling.md) |
| Temporal resolution standards | [TemporalResolutionStandards.md](TemporalResolutionStandards.md) |
| Acceptance criteria | [../Validation/AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| MORPH_SCALE constants | `mi_beta/core/constants.py` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial morph quality tier framework (Phase 4H) |
