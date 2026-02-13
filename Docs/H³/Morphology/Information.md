# H3 Morphology -- Information (M20)

**Version**: 2.0.0
**Category**: Information
**Morphs**: 1 (M20)
**Purpose**: Information-theoretic descriptor measuring distributional complexity and unpredictability of R3 features over time
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer.compute_M20`
**Updated**: 2026-02-13

---

## Overview

The Information category contains a single morph -- M20 entropy -- which applies Shannon information theory to the temporal distribution of R3 feature values. Unlike the Distribution morphs (M0-M7) which describe central tendency and spread via statistical moments, M20 captures distributional complexity in a fundamentally different way: it measures how many bits of information are needed to describe the feature's behavior within the window.

M20 is the only morph that discretizes the continuous R3 feature values into a histogram before computing its descriptor. This makes it uniquely sensitive to window size -- short windows produce quantization artifacts in the histogram, while long windows yield robust entropy estimates.

---

## M20: entropy

**Formula**:
```
M20(x) = -sum(p_i * log2(p_i)) / log2(B)
```

Where:
- Values `x` within the window are binned into a `B = 16` bin histogram over the range [0, 1]
- `p_i = count_i / N` is the probability estimate for bin `i` (N = total frame count)
- Bins with `p_i = 0` are excluded from the sum (by convention, `0 * log(0) = 0`)
- Division by `log2(B) = log2(16) = 4.0` normalizes the output to [0, 1]

**Computation steps**:
1. Collect all R3 feature values `x(t)` within the window
2. Bin values into 16 equally-spaced bins over [0, 1]
3. Compute probability `p_i` for each bin
4. Compute Shannon entropy: `H = -sum(p_i * log2(p_i))`
5. Normalize: `M20 = H / log2(16)`

**Properties**:
- **Output range**: [0, 1] (0 = all values in one bin, 1 = uniform distribution across all 16 bins)
- **Min window**: 4 frames (technical minimum for a histogram; practical minimum is 16+ frames)
- **Signed**: No
- **MORPH_SCALE**: 3.0 (scale maps via `raw / 3.0`; since raw maximum is `log2(16) = 4.0` bits, and normalization by `log2(16)` brings it to [0, 1], the MORPH_SCALE of 3.0 provides headroom for the raw bit value before normalization)

---

## Musical Interpretation

**High entropy (near 1.0)**: The feature visits all parts of its range with roughly equal frequency. This indicates complex, unpredictable behavior -- the feature does not favor any particular value. Musically, this corresponds to sections with wide-ranging, uniformly distributed dynamics (e.g., a passage that is sometimes loud, sometimes quiet, sometimes moderate, with no dominant level).

**Low entropy (near 0.0)**: The feature concentrates around a single value. This indicates simple, predictable behavior -- the feature strongly favors one region of its range. Musically, this corresponds to sustained, stable passages (e.g., a held chord at constant loudness, a drone).

**Medium entropy (~0.5)**: The feature uses part of its range but not uniformly. This is typical of most musical content -- there is variety, but certain values are preferred (e.g., a feature that is usually moderate with occasional peaks).

---

## Horizon Sensitivity

M20 is the most horizon-sensitive morph in the system due to its dependence on histogram quality.

| Horizon | Frames | Frames per Bin (16 bins) | Entropy Quality | Notes |
|---------|:------:|:------------------------:|:--------------:|-------|
| H0-H2 | 1-3 | < 1 | Invalid | Fewer frames than bins; degenerate histogram |
| H3 | 4 | 0.25 | Poor | Most bins empty; quantization dominates |
| H5 | 8 | 0.5 | Marginal | Many bins empty; entropy underestimates complexity |
| H6 | 34 | 2.1 | Acceptable | Some bins have data; basic complexity measure |
| H7 | 43 | 2.7 | Acceptable | Moderate histogram quality |
| H8+ | 52+ | 3.3+ | Good | Bins well-populated; reliable entropy |
| H12+ | 90+ | 5.6+ | Excellent | Robust histogram; minimal quantization artifacts |
| H16+ | 172+ | 10.8+ | Excellent | Statistically robust entropy estimate |

**Recommendation**: Use M20 at Meso horizons (H8+) and above for reliable results. At Micro band, M20 output is dominated by quantization noise and should be interpreted with caution.

**Quantization artifact**: With N < 16 frames, most histogram bins are empty, and entropy is artificially low regardless of the actual complexity of the signal. As N increases, the histogram fills out and entropy converges to the true distributional complexity.

---

## Use Cases

### Section Complexity Tracking

At Macro horizons (H16-H22), M20 on energy features tracks the dynamic complexity of musical sections. Verses with simple, steady dynamics show low entropy. Bridge sections with varied dynamics show higher entropy. Climactic passages with wide-ranging dynamics show the highest entropy.

```
(r3_idx=7, horizon=18, morph=20, law=0)
"How complex is the energy distribution over the last 2 seconds?"
```

### Novelty Detection Support

When combined with temporal derivatives, entropy changes signal novel events. A sudden increase in M20 indicates that a previously predictable feature has become complex -- a transition to a new section, the introduction of new instrumentation, or a textural change.

```
Compare M20 at consecutive frames:
dM20/dt > threshold --> novelty event candidate
```

### Information Rate Estimation

The rate of entropy change over time provides an estimate of information flow. Sections where entropy is rapidly changing contain more "news" than sections where entropy is stable. This supports the NDU (Novelty Detection Unit) and IMU (Impression Management Unit) in prioritizing attention.

### Timbral Diversity

At Macro horizons on timbre features (R3 [12:21] for v1, [94:114] for v2 extended timbre), M20 measures timbral diversity. High entropy indicates a section uses a wide range of timbral colors; low entropy indicates homogeneous timbre.

---

## Relationship to R3 v2 Information Group [87:94]

The R3 v2 expansion introduces a dedicated Information & Surprise feature group at indices [87:94]. These R3 features are **spectral-domain** information measures (computed per-frame from the spectrogram). M20 applied to these features creates a **temporal entropy of spectral entropy** -- a second-order information measure:

```
R3[87:94] = per-frame spectral information measures
M20 of R3[87:94] = temporal distribution of those information measures

Example: M20(R3[87], H18, L0)
= entropy of the spectral entropy distribution over the last 2 seconds
= "how variable has the spectral unpredictability been?"
```

This second-order measure is particularly useful for detecting transitions between structurally distinct sections where the information content itself changes character.

---

## Edge Cases

| Condition | Behavior | Rationale |
|-----------|----------|-----------|
| N < 4 frames | Returns NaN or 0.0 | Below minimum window; histogram is degenerate |
| All values identical | Returns 0.0 | All mass in one bin; entropy = 0 |
| All values uniformly spread | Returns 1.0 (or near 1.0) | Mass equally distributed; maximum entropy |
| Values outside [0, 1] | Clamped to [0, 1] before binning | R3 features should be in [0, 1]; clamping is a safety net |
| Single non-zero bin | Returns 0.0 | No uncertainty in distribution |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [MorphScaling.md](MorphScaling.md) |
| H3 architecture (morph axis) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| R3 v2 Information group | [../Expansion/I-InformationSurprise-Temporal.md](../Expansion/I-InformationSurprise-Temporal.md) |
| Morphology index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
