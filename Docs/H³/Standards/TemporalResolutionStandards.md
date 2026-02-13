# H3 Temporal Resolution Standards

> Version 2.0.0 | Updated 2026-02-13

---

## 1. Overview

H3 operates across 5 orders of magnitude in window size, from 1 frame (5.8 ms at H0) to 169,043 frames (981 s at H31). Different morphs have fundamentally different minimum window requirements for numerical stability: a simple mean is valid on a single sample, but kurtosis requires 50+ samples for the fourth central moment to converge.

This document defines the minimum temporal resolution standards for each morph category and provides a horizon-morph compatibility matrix showing where each category achieves Reliable, Marginal, or Unstable quality.

---

## 2. Frame-to-Duration Conversion

All 32 horizons with exact frame counts and durations at 172.27 Hz frame rate.

| Horizon | Band | Frames | Duration (ms) | Duration (s) | Musical Reference |
|:-------:|:----:|-------:|--------------:|--------------:|-------------------|
| H0 | Micro | 1 | 5.8 | 0.006 | Single frame |
| H1 | Micro | 2 | 11.6 | 0.012 | Sub-onset |
| H2 | Micro | 3 | 17.4 | 0.017 | Onset rise |
| H3 | Micro | 5 | 29.0 | 0.029 | Attack transient |
| H4 | Micro | 9 | 52.2 | 0.052 | Consonant duration |
| H5 | Micro | 17 | 98.7 | 0.099 | Syllable |
| H6 | Micro | 26 | 150.9 | 0.151 | 16th note at 100 BPM |
| H7 | Micro | 43 | 249.6 | 0.250 | 8th note at 120 BPM |
| H8 | Meso | 52 | 301.9 | 0.302 | Short beat |
| H9 | Meso | 69 | 400.5 | 0.400 | Beat at 150 BPM |
| H10 | Meso | 86 | 499.2 | 0.499 | Beat at 120 BPM |
| H11 | Meso | 104 | 603.6 | 0.604 | Beat at 100 BPM |
| H12 | Meso | 138 | 801.1 | 0.801 | Half note |
| H13 | Meso | 172 | 998.5 | 0.999 | ~1 second |
| H14 | Meso | 259 | 1503.1 | 1.503 | ~1.5 seconds |
| H15 | Meso | 345 | 2002.4 | 2.002 | ~2 seconds |
| H16 | Macro | 518 | 3006.3 | 3.006 | One measure (4/4 at 80 BPM) |
| H17 | Macro | 862 | 5003.2 | 5.003 | ~5 seconds |
| H18 | Macro | 1,724 | 10,006.4 | 10.006 | ~10 seconds |
| H19 | Macro | 2,586 | 15,009.6 | 15.010 | ~15 seconds |
| H20 | Macro | 3,448 | 20,012.8 | 20.013 | ~20 seconds |
| H21 | Macro | 4,310 | 25,016.0 | 25.016 | ~25 seconds |
| H22 | Macro | 5,172 | 30,019.2 | 30.019 | ~30 seconds |
| H23 | Macro | 6,897 | 40,025.6 | 40.026 | ~40 seconds |
| H24 | Ultra | 8,621 | 50,037.6 | 50.038 | ~50 seconds |
| H25 | Ultra | 12,931 | 75,050.8 | 75.051 | ~75 seconds |
| H26 | Ultra | 20,690 | 120,076.0 | 120.076 | ~2 minutes |
| H27 | Ultra | 34,483 | 200,132.2 | 200.132 | ~3.3 minutes |
| H28 | Ultra | 71,314 | 413,936.2 | 413.936 | ~6.9 minutes |
| H29 | Ultra | 103,448 | 600,478.0 | 600.478 | ~10 minutes |
| H30 | Ultra | 137,931 | 800,542.6 | 800.543 | ~13.3 minutes |
| H31 | Ultra | 169,043 | 981,109.4 | 981.109 | ~16.4 minutes |

---

## 3. Minimum Window Requirements by Morph Category

| Category | Morphs | Min Frames (R) | Min Frames (M) | Rationale |
|----------|--------|:--:|:--:|-----------|
| **Level** | M0, M1, M3, M4 | 1 | 1 | Direct value or simple aggregation. Valid on any window size including single-frame. |
| **Dispersion** | M2, M5 | 10 | 3 | Variance estimation requires sufficient samples for the second central moment to converge. With N < 10, relative error from sample variance bias is significant. |
| **Shape** | M6, M7, M16, M23 | 30 | 10 | Higher moments (3rd, 4th) and shape comparisons require large N for convergence. Below N=30, skewness and kurtosis estimators have high variance and are dominated by outliers. |
| **Dynamics 1st** | M8, M9, M10, M15 | 3 | 2 | Finite differences require at least 2 points to produce 1 difference. With N=3, one gets 2 differences sufficient for a meaningful velocity estimate. |
| **Dynamics 2nd** | M11, M12, M13 | 5 | 3 | Second derivatives require at least 3 points for 1 second difference. With N=5, one gets 3 second differences for a basic estimate plus boundary handling. |
| **Rhythm** | M14, M17, M22 | 30 | 15 | Autocorrelation requires at least one full cycle to detect periodicity. Peak detection requires enough span for local maxima to be distinguishable from noise. |
| **Information** | M20 | 20 | 8 | Shannon entropy over a 16-bin histogram requires enough samples to populate bins meaningfully. With N < 8, most bins are empty and entropy is dominated by quantization. |
| **Trend** | M18, M21 | 10 | 5 | Linear regression (M18) needs sufficient span for slope estimation. Zero crossings (M21) need enough frames for crossing events to be statistically meaningful. |
| **Stability** | M19 | 10 | 5 | Inverse variance requires the same convergence as M2 (std) since stability = 1 / (variance + eps). |

---

## 4. Horizon-Morph Compatibility Matrix

Quality tier by band for each morph category. Entries reflect the dominant tier within the band; see Section 3 for exact frame thresholds.

```
                Micro       Meso        Macro       Ultra
                H0-H7       H8-H15      H16-H23     H24-H31
                (1-43 fr)   (52-345 fr) (518-6897)  (8621-169K)
              +-----------+-----------+-----------+-----------+
Level         |     R     |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Dispersion    |    M/R    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Shape         |    U/M    |    M/R    |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Dynamics 1st  |    M/R    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Dynamics 2nd  |    U/M    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Rhythm        |     U     |    M/R    |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Information   |    U/M    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Trend         |    M/R    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
Stability     |    M/R    |     R     |     R     |     R     |
              +-----------+-----------+-----------+-----------+
```

**Reading the matrix**: Slash notation (e.g., M/R) indicates that early horizons in the band fall into the first tier while later horizons achieve the second. For example, Dispersion at Micro is M at H0-H3 (1-5 frames) and R at H4-H7 (9-43 frames), since the Reliable threshold is 10 frames.

---

## 5. Numerical Edge Cases

### 5.1 Constant Input

When the input R3 feature is constant across the window:
- **std (M2)**: Returns 0.0. No division-by-zero risk (variance = 0, std = 0).
- **velocity (M8)**: Returns 0.0 (zero derivative). After MORPH_SCALE: 0.0 * 5.0 + 0.5 = 0.5.
- **entropy (M20)**: Returns 0.0 (single bin occupied, log(1) = 0).
- **skewness (M6)**: Returns 0.0 (undefined for zero variance, handled by returning 0). After MORPH_SCALE: 0.0 * 0.25 + 0.5 = 0.5.
- **stability (M19)**: Returns maximum (1 / eps), clamped to 1.0 after normalization.

### 5.2 Single-Frame Window (H0)

At H0 (1 frame), only M0 (value) produces a meaningful result. All other morphs:
- **Aggregation morphs** (M1, M3, M4): Degenerate to M0 (single value = mean = median = max).
- **Dispersion morphs** (M2, M5): Return 0.0 (no variance with N=1).
- **Derivative morphs** (M8-M13): Return 0.0 (no temporal change with N=1).
- **All others**: Return 0.0 or bias value (M6: 0.5, M7: 0.5, M8: 0.5, etc.).

### 5.3 Silence (Zero-Valued Input)

When R3 features are 0.0 for extended periods (silence, very quiet passages):
- All morphs produce well-defined outputs (no NaN from zero input).
- Level morphs: 0.0. Dispersion morphs: 0.0. Dynamics morphs: 0.0 + bias.
- Entropy: 0.0 (constant zero = single bin). Periodicity: 0.0 (no signal to correlate).

### 5.4 Clipping at [0, 1] Boundaries

MORPH_SCALE normalization uses `clamp(raw * gain + bias, 0, 1)`:
- Values exceeding 1.0 are clamped to 1.0 (saturation). Information about magnitude above threshold is lost.
- Values below 0.0 are clamped to 0.0. This affects signed morphs (velocity, acceleration, trend, skewness) after bias centering: extreme negative values are floored.
- Clipping frequency depends on morph, gain, and input characteristics. See [MorphQualityTiers.md](MorphQualityTiers.md) Section 5 for per-morph clipping assessment.

### 5.5 Attention Weight Precision

The attention kernel `A(dt) = exp(-3|dt|/H)` produces weights that span a wide dynamic range:
- **At the window center** (dt=0): weight = 1.0 (maximum).
- **At the boundary** (|dt| = H): weight = exp(-3) = 0.0498.
- **At Ultra horizons** (H31, 169K frames): the kernel is evaluated at 169K positions. Weights at the boundary are small (0.0498) but nonzero. No underflow risk with float32 (minimum positive ~1.2e-38).
- **Normalization**: Kernel weights are divided by their sum. For large H, the sum is approximately `2H/3` (integral of exp(-3|dt|/H) over [-H, H]). No overflow risk.

---

## 6. Implementation Notes

- **MorphComputer** handles all edge cases through clamping and epsilon guards. The epsilon value is `1e-8`, applied to denominators in division operations (std, inverse variance, normalization).
- **MORPH_SCALE normalization**: `output = clamp(raw * gain + bias, 0, 1)`. This is a linear normalization followed by hard clipping. No sigmoid or soft saturation is used in the current implementation.
- **No division by zero**: std computation uses `std + eps` where `eps = 1e-8`. Stability (M19) uses `1 / (variance + eps)`.
- **NaN propagation**: If an upstream R3 feature is NaN (should not occur in normal operation), all morph outputs from that feature will be NaN. The H3 system does not independently guard against NaN inputs; this is the responsibility of the R3 layer.

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph quality tiers | [MorphQualityTiers.md](MorphQualityTiers.md) |
| Horizon catalog | [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md) |
| Morph catalog | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [../Morphology/MorphScaling.md](../Morphology/MorphScaling.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| Attention kernel contract | [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md) |
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| MORPH_SCALE constants | `mi_beta/core/constants.py` |
| HORIZON_FRAMES constants | `mi_beta/core/constants.py` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial temporal resolution standards (Phase 4H) |
