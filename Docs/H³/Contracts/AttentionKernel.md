# AttentionKernel -- Interface Contract

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code**: `mi_beta/ear/h3/attention.py`
**Function**: `compute_attention_weights()`

---

## 1. Purpose

`compute_attention_weights` generates an exponential decay kernel that assigns higher weight to more recent frames within a temporal window. This kernel is the attention mechanism for H3: it determines how much influence each frame in a window has on the final morph computation. The function is called once per unique horizon in the demand set, and the resulting weights are reused across all tuples sharing that horizon.

---

## 2. Signature

```python
def compute_attention_weights(
    window_size: int,
    device: torch.device = torch.device("cpu"),
    decay: float = ATTENTION_DECAY     # 3.0
) -> Tensor                             # (window_size,)
```

### Input Contract

| Parameter | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| `window_size` | `int` | -- | >= 1 | Number of frames in the temporal window |
| `device` | `torch.device` | `cpu` | Valid torch device | Target device for the output tensor |
| `decay` | `float` | `3.0` | > 0 | Exponential decay rate constant |

### Output Contract

| Return | Type | Shape | Value Range | Description |
|--------|------|-------|-------------|-------------|
| `weights` | `torch.Tensor` | `(window_size,)` | `[exp(-decay), 1.0]` | Unnormalized attention weights |

---

## 3. Formula

```
positions = linspace(0, 1, window_size)
weights[i] = exp(-decay * (1 - positions[i]))
```

Equivalently, using the notation from the H3 architecture document:

```
A(dt) = exp(-ATTENTION_DECAY * |dt| / H)
```

Where `|dt| / H` is mapped to `(1 - positions[i])` via the linspace normalization, so that position 0 (oldest frame) maps to `dt/H = 1` and position `window_size - 1` (newest frame) maps to `dt/H = 0`.

---

## 4. Weight Distribution

With the default `ATTENTION_DECAY = 3.0`:

| Position | Normalized dt | Weight | Interpretation |
|----------|:------------:|:------:|----------------|
| 0 (oldest) | 1.0 | `exp(-3.0)` = 0.0498 | ~5% influence |
| 0.25 | 0.75 | `exp(-2.25)` = 0.1054 | ~11% influence |
| 0.50 (middle) | 0.50 | `exp(-1.50)` = 0.2231 | ~22% influence |
| 0.75 | 0.25 | `exp(-0.75)` = 0.4724 | ~47% influence |
| 1.0 (newest) | 0.0 | `exp(0)` = 1.0000 | 100% influence |

The ratio between the newest and oldest frame weights is `exp(3.0)` = 20.09x.

---

## 5. Kernel Shape

```
Weight
  1.0 |                                              *
      |                                           **
      |                                        **
      |                                     ***
      |                                  ***
  0.5 |                             ****
      |                         ****
      |                    *****
      |              ******
      |        ******
 0.05 |********
      +------------------------------------------------
      oldest                                     newest
                      Frame Position
```

The curve is a monotonically increasing exponential. The newest frame always receives weight 1.0, and the oldest frame receives weight `exp(-decay)`.

---

## 6. Edge Cases

| Condition | Behavior | Rationale |
|-----------|----------|-----------|
| `window_size == 1` | Returns `ones(1)` | Single frame needs no weighting |
| `window_size == 0` | Returns `ones(0)` (empty tensor) | Degenerate case, handled by early return |

---

## 7. Normalization

The returned weights are **not** normalized (they do not sum to 1.0). Normalization is performed by the caller (H3Extractor) after slicing the weights to match the actual window length at each time step:

```python
# In H3Extractor._compute_morph_series():
w = weights[:win_len]
w = w / w.sum().clamp(min=1e-8)
```

This design allows the same weight tensor to be sliced to different lengths at different time steps (due to boundary effects) without recomputing the exponential.

---

## 8. Design Rationale

### Why decay = 3.0?

The value `ATTENTION_DECAY = 3.0` was chosen to give the oldest frame in any window approximately 5% of the weight of the newest frame (`exp(-3) = 0.0498`). This provides:

- **Recency bias**: Recent frames dominate the morph computation, reflecting perceptual salience of recent events.
- **Non-zero history**: Older frames still contribute, preventing the morph from degenerating into a point estimate at the current frame.
- **Consistent ratio**: The 20:1 newest-to-oldest ratio holds regardless of window size, providing scale-invariant temporal weighting.

### Why exponential rather than linear or Gaussian?

- Exponential decay matches perceptual models of temporal integration (e.g., leaky integrator models in auditory neuroscience).
- It provides a monotonic weighting that unambiguously prioritizes recency.
- The single-parameter form (`decay`) is simple to tune and reason about.

### Why not normalize in this function?

Boundary truncation in H3Extractor means the caller may use a prefix slice `weights[:k]` where `k < window_size`. Normalizing here would require renormalization after slicing anyway. Deferring normalization avoids redundant computation and keeps this function a pure kernel generator.

---

## 9. Usage in H3Extractor

```python
# Called once per unique horizon:
weights = compute_attention_weights(n_frames, device=device)

# Used many times per horizon (once per tuple, per time step):
w = weights[:win_len]
w = w / w.sum().clamp(min=1e-8)
result[:, t] = self.morph_computer.compute(window, w, m_idx)
```

---

## 10. Dependencies

| Component | Role |
|-----------|------|
| `mi_beta/core/constants.py` | `ATTENTION_DECAY` (= 3.0) |
| `torch` | `linspace`, `exp`, `ones` |

---

## 11. Cross-References

| Document | Location |
|----------|----------|
| H3Extractor (consumer) | [H3Extractor.md](H3Extractor.md) |
| EventHorizon (provides window_size) | [EventHorizon.md](EventHorizon.md) |
| H3 Architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Contracts Index | [00-INDEX.md](00-INDEX.md) |
| Code | `mi_beta/ear/h3/attention.py` |
