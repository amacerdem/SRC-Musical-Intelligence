# H3 Execution Model

> Version 2.0.0 | Updated 2026-02-13

## 1. Pipeline Overview

H3 sits between the spectral representation (R3) and the cognitive models (C3 Brain). It transforms a dense time-frequency tensor into a sparse set of temporal features, computed only where demanded.

```
Audio Signal
    |
    v
+----------+     +----------+     +-------------------+     +------------------+
|  Cochlea | --> |    R3    | --> |        H3         | --> |   Brain (C3)     |
| 128-mel  |     | (B,T,128)|     | sparse dict       |     | 96 models        |
+----------+     +----------+     | {4-tuple: (B,T)}  |     | 9 units          |
                                  +-------------------+     +------------------+
                  Frame rate: 172.27 Hz (5.8 ms/frame)
```

### Input

- **R3 tensor**: shape `(B, T, 128)` -- batch of spectral feature sequences
- **Demand set**: collection of 4-tuples `(r3_idx, horizon, morph, law)` aggregated from all C3 models

### Output

- **H3Output**: sparse dict mapping each demanded 4-tuple to a tensor of shape `(B, T)`

### Address Space

| Axis | Range | Description |
|------|-------|-------------|
| `r3_idx` | 0--127 | Which R3 spectral feature to temporally process |
| `horizon` | 0--31 | Temporal scale (4 bands: Micro, Meso, Macro, Ultra) |
| `morph` | 0--23 | Temporal transformation function (mean, slope, variance, etc.) |
| `law` | 0--2 | Causal direction: L0=past (Memory), L1=future (Prediction), L2=bidirectional (Integration) |

Theoretical space: 128 x 32 x 24 x 3 = 294,912 tuples. Actual usage: ~8,600 (~2.9%).

---

## 2. Execution Phases

### Phase 1: Demand Collection

Each C3 model declares its temporal needs as a tuple of `H3DemandSpec` named tuples:

```python
class SomeModel(C3Model):
    h3_demand = (
        H3DemandSpec(r3_idx=5, horizon=6, morph=0, law=0),
        H3DemandSpec(r3_idx=5, horizon=6, morph=1, law=0),
        # ... typically 40-120 specs per model
    )
```

The Brain aggregates demands from all 96 models into a single set. Duplicate 4-tuples (same feature demanded by multiple models) are deduplicated -- each unique tuple is computed exactly once.

### Phase 2: Demand Tree Construction

`DemandTree.build()` restructures the flat set of 4-tuples into a tree grouped by horizon:

```python
demand_tree = {
    horizon_idx: {(r3_idx, morph_idx, law_idx), ...},
    # one entry per unique demanded horizon
}
```

This grouping is the key to efficient execution: attention weights depend only on horizon, so they can be computed once and reused for all tuples at that horizon.

### Phase 3: Horizon Loop

The outer loop iterates over unique demanded horizons (typically ~15 of 32):

```python
for h_idx in sorted(demand_tree.keys()):
    horizon = EventHorizon(h_idx)        # get frame count for this horizon
    n_frames = horizon.n_frames
    weights = compute_attention_weights(n_frames)  # Phase 5

    for (r3_idx, morph_idx, law_idx) in demand_tree[h_idx]:
        # Phases 4-6 for each tuple at this horizon
        ...
```

### Phase 4: Window Selection

For each tuple, the law determines which frames fall within the attention window:

| Law | Name | Window | Description |
|-----|------|--------|-------------|
| L0 | Memory | `[t - n_frames + 1, t]` | Past context only |
| L1 | Prediction | `[t, t + n_frames - 1]` | Future context only |
| L2 | Integration | `[t - n_frames//2, t + n_frames//2]` | Bidirectional |

The window is extracted from the R3 tensor for the specified `r3_idx`, yielding a slice of shape `(B, window_size)` for each frame `t`.

### Phase 5: Attention Weighting

The exponential decay kernel is applied within the window:

```
A(dt) = exp(-3 * |dt| / H)
```

where `ATTENTION_DECAY = 3.0` and `H` is the horizon frame count. Implementation:

```python
positions = torch.linspace(0, 1, window_size)   # normalized [0, 1]
weights = torch.exp(-ATTENTION_DECAY * (1 - positions))  # peak at end
weights = weights / weights.sum()                # normalize to sum=1
```

Properties:
- Peak weight at the anchor frame: 1.0 (before normalization)
- Boundary weight: exp(-3) = 4.98%
- Half-life at 0.231 * H frames from anchor

Attention weights are computed once per horizon and reused for all tuples at that horizon. They are truncated to the actual window length and re-normalized when the window extends beyond sequence boundaries (see [WarmUp.md](WarmUp.md)).

### Phase 6: Morph Computation

`MorphComputer.compute(window, weights, morph_idx)` dispatches to one of 24 morph functions. Each morph takes the windowed R3 slice and the attention weights, producing a single scalar per frame per batch element. See [H3-MORPH-CATALOG.md](../H3-MORPH-CATALOG.md) for the full catalog.

```python
result[t] = morph_fn(r3_window, attention_weights)  # scalar per batch element
```

### Phase 7: Result Packing

All computed morph series are packed into the `H3Output` features dict:

```python
features = {
    (r3_idx, horizon, morph, law): tensor(B, T),  # one entry per demanded tuple
    ...
}
```

This dict is the sole interface between H3 and the Brain. Each C3 model indexes into it using its declared demand specs.

---

## 3. Data Flow Diagram

```
R3 Tensor (B, T, 128)
    |
    |  index by r3_idx
    v
R3 Feature Series (B, T)         Demand Set (~8,600 4-tuples)
    |                                  |
    |                                  v
    |                          DemandTree.build()
    |                                  |
    |                                  v
    |                          {horizon: {(r3,morph,law),...}}
    |                                  |
    |         +------------------------+
    |         |
    v         v
+---+----+--------+
| For each horizon |
|  n_frames = H(h) |
|  weights = A(dt)  |  <-- computed once per horizon
+--------+---------+
         |
         v
+--------+---------+
| For each tuple    |
|  window = law(t)  |  <-- select past/future/bidi
|  w = truncate(wt) |
|  val = morph(w,w) |  <-- dispatch to morph function
+--------+---------+
         |
         v
features dict {(r3,h,m,l): (B,T)}
         |
         v
    H3Output --> Brain (C3 models)
```

---

## 4. Complexity Analysis

The dominant cost is the morph computation loop:

```
Total cost = SUM over demanded horizons h of:
    T * |tuples_at_h| * O(morph_cost(n_frames_h))
```

Most morphs are linear in window size, giving:

```
O(H_unique * T * max(N_tuples_per_horizon) * max(n_frames))
```

In practice:
- `H_unique` = ~15 demanded horizons
- `T` = sequence length in frames (e.g., 17,227 for 100s of audio)
- `N_tuples_per_horizon` ranges from ~100 (Micro) to ~50 (Ultra)
- `n_frames` ranges from 1 (H0) to 168,999 (H31)

The Ultra band dominates per-frame cost but has the fewest tuples. See [Performance.md](Performance.md) for detailed cost breakdowns and optimization strategies.

---

## 5. Deduplication

When two or more C3 models demand the same 4-tuple, the computation happens exactly once. This is inherent in the set-based DemandTree structure. The resulting tensor in the features dict is shared (read-only) by all consuming models.

Example: if both `SPU-alpha1-PPD` and `ASU-beta2-ASR` demand `(5, 6, 0, 0)`, the morph is computed once and both models read from the same dict entry.

---

## 6. Code References

| Component | File | Key Function/Class |
|-----------|------|--------------------|
| Demand spec | `mi_beta/ear/h3/demand.py` | `H3DemandSpec`, `DemandTree.build()` |
| Horizon params | `mi_beta/ear/h3/horizon.py` | `EventHorizon`, `n_frames` |
| Attention kernel | `mi_beta/ear/h3/attention.py` | `compute_attention_weights()` |
| Morph dispatch | `mi_beta/ear/h3/morph.py` | `MorphComputer.compute()` |
| Pipeline entry | `mi_beta/ear/h3/__init__.py` | `H3Extractor` |

---

## 7. Cross-References

- [SparsityStrategy.md](SparsityStrategy.md) -- Why only ~2.9% of the address space is computed
- [Performance.md](Performance.md) -- Cost model and optimization strategies
- [WarmUp.md](WarmUp.md) -- Boundary effects when windows are incomplete
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Design rationale for the address space
- [H3-MORPH-CATALOG.md](../H3-MORPH-CATALOG.md) -- All 24 morph functions
