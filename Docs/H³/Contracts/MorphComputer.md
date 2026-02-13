# MorphComputer -- Interface Contract

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code**: `mi_beta/ear/h3/morph.py`
**Class**: `MorphComputer`

---

## 1. Purpose

MorphComputer implements the 24 temporal morphologies (M0-M23) that characterize how an R3 feature behaves within a given time window. It uses a dispatch table to map morph indices to specialized computation methods. All methods share a consistent interface: a batched window of R3 values, a weight vector, and a morph index, producing a single scalar per batch item.

---

## 2. Primary Method: `compute()`

```python
def compute(
    self,
    window: Tensor,   # (B, win_len)
    weights: Tensor,   # (win_len,)
    morph_idx: int
) -> Tensor            # (B,)
```

### Input Contract

| Parameter | Type | Shape | Constraints |
|-----------|------|-------|-------------|
| `window` | `torch.Tensor` | `(B, win_len)` | B = batch size, win_len >= 1 |
| `weights` | `torch.Tensor` | `(win_len,)` | Pre-normalized attention weights (sum to 1.0) |
| `morph_idx` | `int` | scalar | 0 <= morph_idx <= 23 |

### Output Contract

| Return | Type | Shape | Description |
|--------|------|-------|-------------|
| result | `torch.Tensor` | `(B,)` | One scalar per batch item |

---

## 3. Dispatch Table

The constructor builds an internal dispatch dictionary mapping each morph index to its corresponding private method:

```python
self._dispatch = {
    0:  self._m0_weighted_mean,
    1:  self._m1_mean,
    2:  self._m2_std,
    ...
    23: self._m23_symmetry,
}
```

Calling `compute(window, weights, morph_idx)` performs `self._dispatch[morph_idx](window, weights)`.

---

## 4. Complete Morph Table

| ID | Name | Formula Summary | Category | Min Window | Signed |
|:--:|------|----------------|----------|:----------:|:------:|
| M0 | weighted_mean | `sum(w * x)` | Level | 1 | No |
| M1 | mean | `mean(x)` | Level | 1 | No |
| M2 | std | `std(x)` | Dispersion | 2 | No |
| M3 | median | `median(x)` | Level | 1 | No |
| M4 | max | `max(x)` | Level | 1 | No |
| M5 | range | `max(x) - min(x)` | Dispersion | 2 | No |
| M6 | skewness | `E[(x-mu)^3] / sigma^3` | Shape | 3 | Yes |
| M7 | kurtosis | `E[(x-mu)^4] / sigma^4 - 3` | Shape | 4 | Yes |
| M8 | velocity | `x[t] - x[t-1]` (last pair) | Dynamics | 2 | Yes |
| M9 | velocity_mean | `mean(diff(x))` | Dynamics | 2 | Yes |
| M10 | velocity_std | `std(diff(x))` | Dynamics | 3 | No |
| M11 | acceleration | `diff(diff(x))` (last triple) | Dynamics | 3 | Yes |
| M12 | acceleration_mean | `mean(diff(diff(x)))` | Dynamics | 3 | Yes |
| M13 | acceleration_std | `std(diff(diff(x)))` | Dynamics | 4 | No |
| M14 | periodicity | Autocorrelation peak ratio | Rhythm | 4 | No |
| M15 | smoothness | `1 / (1 + velocity_std)` | Dynamics | 3 | No |
| M16 | curvature | `mean(abs(diff(diff(x))))` | Shape | 3 | No |
| M17 | shape_period | Dominant period from autocorrelation | Rhythm | 4 | No |
| M18 | trend | Weighted linear regression slope | Dynamics | 2 | Yes |
| M19 | stability | `1 / (1 + std(x))` | Dispersion | 2 | No |
| M20 | entropy | Shannon entropy, 16 bins | Information | 4 | No |
| M21 | zero_crossings | Count of sign changes (normalized) | Dynamics | 2 | No |
| M22 | peaks | Count of local maxima (normalized) | Rhythm | 3 | No |
| M23 | symmetry | Correlation of first/second half | Shape | 4 | Yes |

---

## 5. Morph Categories

| Category | Morphs | Description |
|----------|--------|-------------|
| **Level** | M0, M1, M3, M4 | Central tendency and extrema |
| **Dispersion** | M2, M5, M19 | Spread and variability |
| **Shape** | M6, M7, M16, M23 | Distribution shape and curvature |
| **Dynamics** | M8, M9, M10, M11, M12, M13, M15, M18, M21 | Temporal derivatives, trends, smoothness |
| **Rhythm** | M14, M17, M22 | Periodicity, dominant period, peak count |
| **Information** | M20 | Entropy / unpredictability |

---

## 6. Edge Cases

### Window Smaller Than Minimum

When the actual window length is less than the morph's minimum required window size, the morph returns a safe default:

| Condition | Return Value | Rationale |
|-----------|-------------|-----------|
| `win_len < 2` for derivative morphs (M8-M13) | `zeros(B)` | No differences computable |
| `win_len < 3` for second derivatives (M11-M13, M16) | `zeros(B)` | No acceleration computable |
| `win_len < 4` for higher-order morphs (M7, M14, M17, M20, M23) | `zeros(B)` or `ones(B)` | Insufficient data for meaningful statistic |

These defaults ensure numerical stability without special-casing in the caller.

### Constant Windows

When all values in the window are identical (zero variance):
- M2 (std): returns 0.0
- M6 (skewness), M7 (kurtosis): returns 0.0 (division guarded by clamp)
- M15 (smoothness), M19 (stability): returns 1.0 (maximum smoothness/stability)
- M20 (entropy): returns 0.0 (no uncertainty)

---

## 7. Normalization

MorphComputer outputs raw morph values. The `MORPH_SCALE` constant (24 `(gain, bias)` tuples from `mi_beta/core/constants.py`) is **not** applied within this class. Normalization is applied downstream by the consuming model or pipeline stage.

```
Raw morph value -> (value * gain + bias) -> Normalized value
```

This separation keeps MorphComputer stateless and scale-agnostic.

---

## 8. Method Interface Pattern

Every private morph method follows the same signature:

```python
def _mN_name(self, window: Tensor, weights: Tensor) -> Tensor:
    """
    Args:
        window: (B, win_len) - R3 scalar values in the time window
        weights: (win_len,) - attention weights (pre-normalized)
    Returns:
        (B,) - one scalar per batch item
    """
```

The `weights` parameter is available to all morphs but only used by morphs that incorporate attention weighting (primarily M0 weighted_mean and M18 trend). Other morphs may ignore the weights and operate on the raw window values.

---

## 9. Dependencies

| Component | Role |
|-----------|------|
| `mi_beta/core/constants.py` | `N_MORPHS` (=24), `MORPH_SCALE` (normalization, not applied here) |
| `torch` | All computation is in PyTorch for GPU compatibility |

---

## 10. Cross-References

| Document | Location |
|----------|----------|
| H3Extractor (consumer) | [H3Extractor.md](H3Extractor.md) |
| Morphology Catalog | [../Morphology/](../Morphology/) |
| MORPH_SCALE Constants | `mi_beta/core/constants.py` |
| Contracts Index | [00-INDEX.md](00-INDEX.md) |
| Code | `mi_beta/ear/h3/morph.py` |
