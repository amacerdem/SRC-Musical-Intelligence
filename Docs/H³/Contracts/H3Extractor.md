# H3Extractor -- Interface Contract

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code**: `mi_beta/ear/h3/__init__.py`
**Class**: `H3Extractor`

---

## 1. Purpose

H3Extractor is the top-level orchestrator and sole entry point for H3 temporal context extraction. It receives an R3 spectral feature tensor and a sparse demand set, then computes only the requested temporal features. Every C3 model in the system interacts with H3 exclusively through this class.

---

## 2. Constructor

```python
def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | `MIBetaConfig` | `MI_BETA_CONFIG` | Global configuration object |

**Initialization**:
- Stores `self.config`
- Instantiates `self.morph_computer = MorphComputer()`

No GPU allocation or precomputation occurs at construction time.

---

## 3. Primary Method: `extract()`

```python
def extract(
    self,
    r3: Tensor,
    demand: Set[Tuple[int, int, int, int]]
) -> H3Output
```

### Input Contract

| Parameter | Type | Shape / Format | Constraints |
|-----------|------|---------------|-------------|
| `r3` | `torch.Tensor` | `(B, T, 49)` | B = batch size, T = time frames, D = 49 R3 features |
| `demand` | `Set[Tuple[int,int,int,int]]` | Set of `(r3_idx, horizon, morph, law)` | `r3_idx` in [0,48], `horizon` in [0,31], `morph` in [0,23], `law` in [0,2] |

### Output Contract

| Field | Type | Description |
|-------|------|-------------|
| `H3Output.features` | `Dict[Tuple[int,int,int,int], Tensor]` | Maps each demanded 4-tuple `(r3_idx, h, m, l)` to a `(B, T)` tensor |

The output dict contains exactly one entry per demanded 4-tuple. Each value tensor has the same batch and time dimensions as the input R3 tensor.

---

## 4. Execution Flow

```
extract(r3, demand)
  |
  |-- DemandTree.build(demand)
  |     Returns: Dict[horizon_idx -> {(r3_idx, morph, law), ...}]
  |
  |-- For each horizon_idx in tree:
  |     |
  |     |-- EventHorizon(horizon_idx)
  |     |     Returns: horizon wrapper with .frames property
  |     |
  |     |-- n_frames = min(horizon.frames, T)
  |     |
  |     |-- compute_attention_weights(n_frames, device)
  |     |     Returns: (n_frames,) decay kernel
  |     |
  |     |-- For each (r3_idx, morph_idx, law_idx) in horizon group:
  |     |     |
  |     |     |-- r3_scalar = r3[..., r3_idx]     # (B, T)
  |     |     |
  |     |     |-- _compute_morph_series(...)
  |     |     |     Returns: (B, T) result tensor
  |     |     |
  |     |     |-- features[(r3_idx, h, m, l)] = result
  |
  |-- Return H3Output(features=features)
```

---

## 5. Internal Method: `_compute_morph_series()`

```python
def _compute_morph_series(
    self, r3_scalar, B, T, n_frames,
    m_idx, l_idx, weights, device, dtype
) -> Tensor
```

This method implements the per-frame sliding window loop. For each time step `t` in `[0, T)`, it:

1. **Selects the window** according to the law index
2. **Slices and normalizes attention weights** to match actual window length
3. **Computes the morph** via `self.morph_computer.compute()`

### Law Window Selection (Section 5.1)

| Law | Index | Name | Window Start | Window End | Semantics |
|-----|:-----:|------|-------------|-----------|-----------|
| L0 | 0 | Memory | `max(0, t - n_frames + 1)` | `t + 1` | Past context only |
| L1 | 1 | Prediction | `t` | `min(T, t + n_frames)` | Future context only |
| L2 | 2 | Integration | `max(0, t - half)` | `min(T, t + n_frames - half)` | Bidirectional (half = n_frames // 2) |

**Edge behavior**: At sequence boundaries (near `t = 0` or `t = T-1`), windows are truncated. The attention weights are sliced to `weights[:win_len]` and renormalized: `w = w / w.sum().clamp(min=1e-8)`.

### Return Value

A `(B, T)` tensor where each `result[:, t]` is the scalar morph output for time step `t` across all batch items.

---

## 6. Performance Characteristics

| Factor | Complexity | Notes |
|--------|-----------|-------|
| Outer loop | O(H) | H = number of unique horizons in demand |
| Inner loop | O(N_h) | N_h = number of (r3, morph, law) tuples per horizon |
| Per-tuple | O(T * W) | T = time frames, W = window size (horizon-dependent) |
| Total | O(H * N_h * T * W) | W varies from 1 to ~169,000 frames across horizons |

Attention weights are computed once per horizon and reused across all tuples sharing that horizon. This is the primary optimization enabled by `DemandTree`.

---

## 7. Dependencies

| Component | Role | Document |
|-----------|------|----------|
| `DemandTree` | Groups demand by horizon | [DemandTree.md](DemandTree.md) |
| `EventHorizon` | Maps horizon index to frame count | [EventHorizon.md](EventHorizon.md) |
| `MorphComputer` | Dispatches morph computation | [MorphComputer.md](MorphComputer.md) |
| `compute_attention_weights` | Produces decay kernel | [AttentionKernel.md](AttentionKernel.md) |
| `H3Output` | Return type (dataclass) | `mi_beta/ear/h3/__init__.py` |
| `MIBetaConfig` | Configuration | `mi_beta/core/config.py` |

---

## 8. Usage Example

```python
from mi_beta.ear.h3 import H3Extractor

extractor = H3Extractor()

# Demand: R3 feature 0, horizon 4, morph 0 (weighted mean), law 0 (memory)
demand = {(0, 4, 0, 0), (5, 4, 2, 1), (12, 10, 8, 2)}
h3_output = extractor.extract(r3_tensor, demand)

# Access individual features
feature = h3_output.features[(0, 4, 0, 0)]  # shape: (B, T)
```

---

## 9. Cross-References

| Document | Location |
|----------|----------|
| H3 Architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| H3DemandSpec | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| Demand Format | [../Demand/](../Demand/) |
| Law Specifications | [../Laws/](../Laws/) |
| Contracts Index | [00-INDEX.md](00-INDEX.md) |
| Code | `mi_beta/ear/h3/__init__.py` |
