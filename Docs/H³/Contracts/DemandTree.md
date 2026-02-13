# DemandTree -- Interface Contract

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code**: `mi_beta/ear/h3/demand.py`
**Class**: `DemandTree`

---

## 1. Purpose

DemandTree provides sparse routing for H3 demand sets. It reorganizes a flat set of 4-tuples into a horizon-keyed dictionary so that the H3Extractor can compute attention weights once per horizon and reuse them across all tuples sharing that horizon. This is a pure data-structure utility with no learnable parameters or state.

---

## 2. Static Method: `build()`

```python
@staticmethod
def build(
    demand: Set[Tuple[int, int, int, int]]
) -> Dict[int, Set[Tuple[int, int, int]]]
```

### Input Contract

| Parameter | Type | Format | Constraints |
|-----------|------|--------|-------------|
| `demand` | `Set[Tuple[int,int,int,int]]` | `{(r3_idx, horizon, morph, law), ...}` | `r3_idx` in [0,48], `horizon` in [0,31], `morph` in [0,23], `law` in [0,2] |

### Output Contract

| Return | Type | Format |
|--------|------|--------|
| `tree` | `Dict[int, Set[Tuple[int,int,int]]]` | `{horizon_idx: {(r3_idx, morph_idx, law_idx), ...}}` |

### Transformation

```
Input:  {(r3_idx, horizon, morph, law), ...}
                   |
                   v
Output: {horizon: {(r3_idx, morph, law), ...}}
```

The horizon index is extracted as the dictionary key. The remaining three elements (r3_idx, morph, law) are stored as a 3-tuple in the set for that horizon.

---

## 3. Static Method: `summary()`

```python
@staticmethod
def summary(demand: Set[Tuple[int, int, int, int]]) -> str
```

Returns a human-readable summary string describing the demand set structure. Useful for logging and debugging.

---

## 4. Example

```python
demand = {
    (0, 4, 0, 0),   # R3[0], horizon 4, weighted_mean, memory
    (0, 4, 2, 0),   # R3[0], horizon 4, std, memory
    (5, 4, 8, 1),   # R3[5], horizon 4, velocity, prediction
    (12, 10, 0, 2), # R3[12], horizon 10, weighted_mean, integration
}

tree = DemandTree.build(demand)
# Result:
# {
#     4:  {(0, 0, 0), (0, 2, 0), (5, 8, 1)},
#     10: {(12, 0, 2)},
# }
```

In this example, three tuples share horizon 4, so attention weights for horizon 4 are computed once and applied to all three. Horizon 10 has a single tuple.

---

## 5. Design Rationale

### Why horizon is the primary grouping key

The most expensive shared computation in H3Extractor is `compute_attention_weights()`, which depends only on the horizon (via `EventHorizon.frames`). Grouping by horizon ensures this computation happens once per unique horizon rather than once per demand tuple.

### Why not also group by law?

While law determines window selection (past/future/bidirectional), the actual window slicing is cheap (a tensor slice) and varies per time step `t`. There is no reusable intermediate result from grouping by law.

### Why not also group by R3 feature index?

R3 feature extraction (`r3[..., r3_idx]`) is a single indexing operation with negligible cost. Grouping by R3 index would add complexity without meaningful performance benefit.

### Why a set of tuples rather than nested dicts?

The flat set-of-tuples format is the canonical demand representation used throughout the MI system (defined in C3 model specifications). DemandTree converts this to the internal grouped format without requiring callers to change their demand representation.

---

## 6. Invariants

- Every 4-tuple in the input demand set appears exactly once in the output tree (as a 3-tuple under its horizon key)
- The union of all 3-tuples across all horizon keys reconstructs the original demand set (with horizon re-added)
- Empty demand produces an empty tree: `build(set()) == {}`
- Duplicate tuples in the input set are inherently deduplicated (set semantics)

---

## 7. Dependencies

| Component | Role |
|-----------|------|
| `mi_beta/core/constants.py` | `N_HORIZONS`, `N_MORPHS`, `N_LAWS` for validation bounds |

---

## 8. Cross-References

| Document | Location |
|----------|----------|
| H3Extractor (consumer) | [H3Extractor.md](H3Extractor.md) |
| Demand Format | [../Demand/](../Demand/) |
| H3DemandSpec | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| Contracts Index | [00-INDEX.md](00-INDEX.md) |
| Code | `mi_beta/ear/h3/demand.py` |
