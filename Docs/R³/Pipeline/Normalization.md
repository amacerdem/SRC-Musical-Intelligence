# Pipeline: Normalization

**Purpose**: Documents the [0,1] normalization contract, the methods used across groups, known issues, and best practices for new features.

---

## 1. Why [0,1] Normalization

All R3 features target the range `[0, 1]`. This contract exists for three reasons:

### 1.1 Neural Network Compatibility

C3 brain models consume R3 features directly as input. Neural networks with sigmoid or softmax activations operate most efficiently when inputs are pre-normalized to a consistent scale. A `[0,1]` range:
- Avoids saturation in sigmoid-family activations.
- Provides a natural "off/on" interpretation (0 = absent, 1 = maximally present).
- Enables direct use as attention weights or gating values.

### 1.2 Consistent Scale

Cross-group interactions (Group E) multiply features from different groups. For the product `a * b` to be meaningful, both `a` and `b` must be on comparable scales. If loudness were in dB (e.g., -60 to 0) and roughness were in [0, 1], their product would be dominated by the loudness term.

### 1.3 Interpretability

A value of 0.8 for `key_clarity` and 0.8 for `onset_strength` should convey comparable "strength" in their respective domains. This enables:
- Threshold-based gating (e.g., "if feature > 0.5, activate pathway").
- Meaningful visualization (all features on the same axis).
- Feature importance comparison across domains.

---

## 2. Normalization Methods

The R3 architecture uses five normalization methods across its features:

### 2.1 Sigmoid

```python
output = torch.sigmoid(x * gain)
```

Maps any real-valued input to `(0, 1)` via the logistic function. The `gain` parameter controls sharpness.

**Properties**:
- Smooth and differentiable.
- Never exactly reaches 0 or 1.
- Introduces nonlinear compression (values far from center are squashed).

**Used by**:
- `[0] roughness`: `sigmoid(mel.var(dim=1) / mel.mean(dim=1))`
- `[8] velocity_A`: `sigmoid((amp[t] - amp[t-1]) * 5.0)` (gain=5.0)
- `[9] acceleration_A`: `sigmoid((vel[t] - vel[t-2]) * 5.0)` (gain=5.0)
- `[126] hammarberg_index`: `sigmoid((peak_low - peak_high) / 5.0)`
- `[127] spectral_slope_0_500`: `sigmoid(slope * 10)` (gain=10)

### 2.2 Min-Max Normalization

```python
output = (x - x_min) / (x_max - x_min)
```

Linearly maps the range `[x_min, x_max]` to `[0, 1]`. Can be frame-level (dynamic) or pre-computed (static).

**Properties**:
- Preserves linear relationships.
- Requires knowledge of expected range.
- Vulnerable to outliers (a single extreme value compresses everything else).

**Used by**:
- `[7] amplitude`: `mel.pow(2).mean(dim=1).sqrt() / max_val` (batch-level max)
- `[11] onset_strength`: `relu(diff).sum(dim=1) / max_val`
- `[21] spectral_flux`: `norm(diff) / max_val`
- `[65] tempo_estimate`: `(bpm - 30) / (300 - 30)` (BPM range)
- `[75] key_clarity`: `(corr - 0.3) / 0.65` (empirical correlation range)
- Phase 6 MFCC [94-106]: `(mfcc / mfcc_scale + 1) / 2` (per-coefficient scale)

### 2.3 Clamp

```python
output = x.clamp(0, 1)
```

Hard clips values outside `[0, 1]`. Used when the raw computation naturally produces near-[0,1] values but may occasionally exceed the bounds.

**Properties**:
- Simplest possible normalization.
- Introduces non-differentiable points at boundaries.
- Information loss for out-of-range values.

**Used by**:
- `[2] helmholtz_kang`: Correlation in [-1,1], clamped to [0,1].
- `[24] distribution_concentration`: HHI clamp (known bug -- see Section 4).
- `[64] inharmonicity_index`: Clamp(0,1) (typical values 0-0.5).
- Various Phase 6 features as a safety net after primary normalization.

### 2.4 Natural Ratio

```python
output = partial_sum / total_sum
```

When a feature is inherently a ratio or proportion, it naturally falls in `[0, 1]` without additional normalization.

**Properties**:
- Physically meaningful (proportion of total).
- No information loss.
- Requires positive-valued components.

**Used by**:
- `[3] stumpf_fusion`: `mel[:, :N//4, :].sum() / mel.sum()` (low-frequency ratio)
- `[12] warmth`: Same formula as [3] (documented duplicate).
- `[13] sharpness`: `mel[:, 3*N//4:, :].sum() / mel.sum()` (high-frequency ratio)
- `[14] tonalness`: `mel.max() / mel.sum()` (peak dominance)
- `[15] clarity`: `spectral_centroid / N` (normalized centroid)
- `[18-20] tristimulus 1/2/3`: Third-band energy ratios.
- `[22] distribution_entropy`: `-sum(p*log(p)) / log(128)` (normalized entropy).
- `[23] distribution_flatness`: Geometric/arithmetic mean ratio (Wiener entropy).
- Phase 6 chroma [49-60]: L1-normalized pitch class distribution (sum=1.0).

### 2.5 Custom / Composite

Some features use domain-specific transformations:

**Complement**: `output = 1 - x` (for inverse features)
- `[5] inharmonicity`: `1 - helmholtz_kang[2]`
- `[16] spectral_smoothness`: `1 - sethares_dissonance[1]`

**Linear combination**: `output = w1 * a + w2 * b` (weighted composite)
- `[4] sensory_pleasantness`: `0.6 * (1 - sethares[1]) + 0.4 * stumpf[3]`
- `[6] harmonic_deviation`: `0.5 * sethares[1] + 0.5 * (1 - helmholtz[2])`

**Exponential mapping**: `output = 1 - exp(-x)` (KL divergence to [0,1])
- `[86] syntactic_irregularity`: `1 - exp(-KL)`
- `[88] harmonic_entropy`: `(1 - exp(-KL)) * confidence`
- `[90] spectral_surprise`: `(1 - exp(-KL)) * confidence`

**Ratio compression**: `output = x / (x + 1)` (maps [0, inf) to [0, 1))
- `[125] alpha_ratio`: `low / (low + high)` (or `x / (x + 1)`)

---

## 3. Per-Group Normalization Choices

### Group A: Consonance [0:7]

| Index | Feature | Method | Formula |
|:-----:|---------|--------|---------|
| 0 | roughness | sigmoid | `sigmoid(var/mean)` |
| 1 | sethares_dissonance | max-norm | `mean(abs(diff)) / max` |
| 2 | helmholtz_kang | clamp | `corr(mel[k], mel[k+1]).clamp(0,1)` |
| 3 | stumpf_fusion | ratio | `low_sum / total_sum` |
| 4 | sensory_pleasantness | composite | `0.6*(1-[1]) + 0.4*[3]` |
| 5 | inharmonicity | complement | `1 - [2]` |
| 6 | harmonic_deviation | composite | `0.5*[1] + 0.5*(1-[2])` |

### Group B: Energy [7:12]

| Index | Feature | Method | Formula |
|:-----:|---------|--------|---------|
| 7 | amplitude | max-norm | `rms / max_val` |
| 8 | velocity_A | sigmoid | `sigmoid(diff * 5.0)` |
| 9 | acceleration_A | sigmoid | `sigmoid(diff * 5.0)` |
| 10 | loudness | max-norm | `amp^0.3 / max_val` |
| 11 | onset_strength | max-norm | `relu(diff).sum / max_val` |

### Group C: Timbre [12:21]

| Index | Feature | Method | Formula |
|:-----:|---------|--------|---------|
| 12 | warmth | ratio | `low_sum / total_sum` |
| 13 | sharpness | ratio | `high_sum / total_sum` |
| 14 | tonalness | ratio | `max / sum` |
| 15 | clarity | ratio | `centroid / N` |
| 16 | spectral_smoothness | complement | `1 - [1]` |
| 17 | spectral_autocorrelation | clamp | `corr.clamp(0,1)` |
| 18-20 | tristimulus 1/2/3 | ratio | `band_sum / total_sum` |

### Group D: Change [21:25]

| Index | Feature | Method | Formula |
|:-----:|---------|--------|---------|
| 21 | spectral_flux | max-norm | `L2_norm(diff) / max` |
| 22 | distribution_entropy | ratio | `-sum(p*log(p)) / log(128)` |
| 23 | distribution_flatness | ratio | `geomean / arithmean` |
| 24 | distribution_concentration | clamp | `HHI * N, clamp(0,1)` (BUG) |

### Group E: Interactions [25:49]

| Index | Feature | Method | Formula |
|:-----:|---------|--------|---------|
| 25-48 | cross-products | product | `feature_a * feature_b` (both in [0,1]) |

Product of two [0,1] values is naturally in [0,1]. However, this creates a zero-bias: small values in either operand produce very small products.

---

## 4. Known Issues

### 4.1 Stevens' Law Double Compression

**Affected features**: `[10] loudness`

**Problem**: Loudness is computed as `amplitude^0.3` where amplitude is already derived from the log-mel spectrogram. The mel spectrogram uses log1p normalization, so the computation chain is:

```
raw audio -> STFT -> mel filterbank -> log1p -> mel
                                                  |
                                                  v
                        RMS of log-mel values     -> amplitude [7]
                                                  |
                                                  v
                        amplitude^0.3             -> loudness [10]
```

The issue: Stevens' power law (`L ~ I^0.3`) should apply to the **linear** intensity, not to already-compressed log values. Applying `x^0.3` to log-mel values creates double compression:

```
Correct:    loudness = (linear_intensity)^0.3
Actual:     loudness = (log1p(linear_intensity))^0.3    <-- double compression
```

This compresses the dynamic range excessively, making quiet and loud passages less distinguishable than they should be.

**Phase 6 fix**:
```python
# Option A: Undo log before power law
mel_linear = mel.exp()
amplitude = mel_linear.pow(2).mean(dim=1).sqrt()
loudness = amplitude.pow(0.3) / max_val

# Option B: Full Zwicker ISO 532-1
# (requires Bark rebinning, specific loudness pattern)
```

### 4.2 Concentration Normalization Bug

**Affected feature**: `[24] distribution_concentration`

**Problem**: The Herfindahl-Hirschman Index (HHI) is computed as `sum(p_k^2) * N` and then clamped to [0,1]. The issue is that:

- For a uniform distribution: `HHI = sum((1/N)^2) * N = N * (1/N^2) * N = 1.0`
- For a concentrated distribution (single bin): `HHI = 1^2 * N = N` (then clamped to 1.0)

Both uniform and concentrated distributions map to 1.0, making the feature meaningless.

**Phase 6 fix**:
```python
# Correct normalization: 0 = uniform, 1 = concentrated
HHI = (p.pow(2).sum(dim=1))
concentration = (HHI - 1.0/N) / (1.0 - 1.0/N)
concentration = concentration.clamp(0, 1)
```

### 4.3 Sigmoid Gain Sensitivity

**Affected features**: `[8] velocity_A`, `[9] acceleration_A`, `[126] hammarberg_index`, `[127] spectral_slope_0_500`

**Problem**: Sigmoid normalization with fixed gain values (e.g., 5.0, 10.0) is sensitive to the input distribution. If the actual value distribution differs from what the gain was tuned for, the sigmoid either saturates (all values near 0 or 1) or underutilizes the range.

Velocity and acceleration use `gain=5.0`, which was chosen empirically but may not generalize across all audio material. Physical meaning is lost because sigmoid is nonlinear.

**Phase 6 consideration**: Replace sigmoid with percentile-based normalization or min-max with running statistics.

---

## 5. Best Practices for New Features

When implementing a new feature in a `BaseSpectralGroup` subclass:

### 5.1 Choose the Right Normalization Method

| Feature Type | Recommended Method | Rationale |
|-------------|-------------------|-----------|
| Energy ratio (part/whole) | Natural ratio | Already [0,1], no distortion |
| Entropy | / log(N) | Maximum entropy = log(N) |
| Correlation | Clamp(0,1) or (x+1)/2 | Depends on whether [-1,1] or [0,1] |
| Unbounded positive | x/(x+1) or sigmoid | Smooth compression |
| Bounded known range | Min-max | Preserves linearity |
| KL divergence | 1-exp(-x) | Maps [0,inf) to [0,1) |
| Difference / derivative | Sigmoid with calibrated gain | Center at expected mean |

### 5.2 Avoid Common Pitfalls

1. **Do not apply log to already-log values**. The mel spectrogram is already in log domain. If you need linear power, use `mel.exp()` first.

2. **Do not use batch-level max-norm for features that will be compared across batches**. Frame-level or dataset-level normalization is more stable.

3. **Document the normalization clearly** in the feature's `description` and in the `feature_names` docstring.

4. **Test edge cases**: Silent frames (mel near zero), single-tone frames (one mel bin active), white noise (all bins equal).

5. **Verify the output range** with assertions during development:
   ```python
   features = self._compute(mel)
   assert (features >= 0).all() and (features <= 1).all(), \
       f"Out of range: [{features.min():.3f}, {features.max():.3f}]"
   return features
   ```

### 5.3 Phase 6 Normalization Guidelines

For new groups F-K, the R3-V2-DESIGN.md specifies normalization per feature. Summary of methods used in new groups:

| Group | Primary Methods |
|-------|----------------|
| F: Pitch & Chroma | L1-norm (chroma), min-max (pitch height), entropy/log(12) |
| G: Rhythm & Groove | Min-max (BPM), autocorrelation (natural [0,1]), sigmoid (pulse clarity) |
| H: Harmony & Tonality | Min-max (key clarity), (x+1)/2 (tonnetz), L1-distance/2, cosine distance |
| I: Information & Surprise | 1-exp(-KL), entropy/log(N), with warm-up confidence ramp |
| J: Timbre Extended | Per-coefficient scaling (MFCC), /10+clamp (contrast) |
| K: Modulation | Per-rate max-norm (modulation), min-max (centroid), DIN formula (sharpness) |
