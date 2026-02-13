# BaseMechanism -- Mechanism Interface

> **Code**: `mi_beta/contracts/base_mechanism.py`
> **Kind**: Abstract Base Class (ABC)
> **Imports from**: (none -- leaf ABC)

## Purpose

A mechanism is a sub-computation within a `BaseModel`. It reads H3 temporal features and R3 spectral features and produces a fixed-dimensional output tensor that the parent model combines with other mechanism outputs to form its final output.

Mechanisms are the atomic computational units of the MI-Beta brain. By convention, each mechanism produces a 30-D output (configurable via `OUTPUT_DIM`). The 30-D convention comes from the C³ meta-analysis framework where each mechanism produces a standardised feature block.

---

## Class Constants (must override in every subclass)

| Constant | Type | Default | Description |
|----------|------|---------|-------------|
| `NAME` | `str` | `""` | Short mechanism identifier (e.g. `"AED"`, `"CPD"`, `"C0P"`) |
| `FULL_NAME` | `str` | `""` | Full descriptive name (e.g. `"Affective Evaluation of Dynamics"`) |
| `OUTPUT_DIM` | `int` | `30` | Output dimensionality. Default 30D per C³ convention; override if different |
| `HORIZONS` | `Tuple[int, ...]` | `()` | Horizon indices this mechanism operates over. E.g. `(9, 16, 18)` = H9 (350ms), H16 (1s), H18 (2s) |

---

## Abstract Members

### `h3_demand -> Set[Tuple[int, int, int, int]]` (property)

The set of H3 4-tuples `(r3_idx, horizon, morph, law)` this mechanism needs. The union of all mechanism demands within a model defines the model's total H3 demand. Each tuple maps to a single `(B, T)` scalar time series in the H3Output.

### `compute(h3_features, r3_features) -> Tensor`

Compute the mechanism output.

| Parameter | Type | Shape | Description |
|-----------|------|-------|-------------|
| `h3_features` | `Dict[Tuple[int,int,int,int], Tensor]` | `{4-tuple: (B, T)}` | Temporal features; only tuples declared in `h3_demand` are guaranteed present |
| `r3_features` | `Tensor` | `(B, T, 49)` | R3 spectral features |

**Returns**: `(B, T, OUTPUT_DIM)` mechanism output tensor.

---

## Computed Helpers

| Property | Return Type | Description |
|----------|-------------|-------------|
| `demand_count` | `int` | Number of unique H3 demands declared |
| `horizons_used` | `Set[int]` | Horizon indices actually referenced in `h3_demand`; should match `HORIZONS` |
| `r3_indices_used` | `Set[int]` | R3 feature indices referenced in `h3_demand` |

---

## Validation Rules (`validate()`)

Returns a list of error messages (empty if valid). Checks:

1. `NAME` must be non-empty
2. `FULL_NAME` must be non-empty
3. `OUTPUT_DIM` must be > 0
4. `HORIZONS` (if declared) must match the actual horizons extracted from `h3_demand`; a mismatch is flagged as an inconsistency

---

## Example Subclass

```python
class AED(BaseMechanism):
    NAME = "AED"
    FULL_NAME = "Affective Evaluation of Dynamics"
    OUTPUT_DIM = 30
    HORIZONS = (9, 16, 18)  # 350ms, 1s, 2s

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        return {(10, 9, 4, 2), (8, 9, 8, 2), ...}

    def compute(self, h3_features, r3_features) -> Tensor:
        ...
```
