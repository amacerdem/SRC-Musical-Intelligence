# H3 Sparsity Strategy

> Version 2.0.0 | Updated 2026-02-13

## 1. Problem Statement

The H3 address space spans 4 axes:

| Axis | Cardinality | Description |
|------|-------------|-------------|
| r3_idx | 128 | R3 spectral features |
| horizon | 32 | Temporal scales |
| morph | 24 | Transformation functions |
| law | 3 | Causal directions |

The full Cartesian product yields **294,912 unique 4-tuples**. Computing all of them for every frame in a sequence would require:

```
Dense tensor: (B, T, 128, 32, 24, 3) float32
            = 294,912 * 4 bytes per frame per batch element
            = ~1.12 MB per frame per batch element

For T = 17,227 frames (100s audio at 172.27 Hz):
            = ~19.3 GB per batch element
```

This is prohibitive. Most of these tuples are never consumed by any C3 model.

---

## 2. Solution: Demand-Driven Lazy Evaluation

H3 computes nothing unless a C3 model explicitly demands it. The pipeline:

1. Each C3 model declares exactly which 4-tuples it needs via `h3_demand`
2. The Brain aggregates and deduplicates all demands
3. `DemandTree.build()` organizes demands for efficient iteration
4. Only demanded tuples are computed; all others are never materialized

This transforms H3 from a dense tensor computation into a sparse, demand-driven extraction.

---

## 3. Occupancy Analysis

### Overall Occupancy

| Metric | Value |
|--------|-------|
| Theoretical space | 294,912 tuples |
| Actual demands | ~8,600 tuples |
| **Occupancy** | **~2.9%** |

### Horizon Coverage

Of the 32 possible horizons, only ~15 are actually demanded by any model (~47% horizon coverage). Since horizon is the expensive axis (attention weights must be computed per horizon), this provides significant savings.

| Band | Horizons | Demanded | Coverage |
|------|----------|----------|----------|
| Micro (H0--H7) | 8 | ~5 | ~63% |
| Meso (H8--H15) | 8 | ~4 | ~50% |
| Macro (H16--H23) | 8 | ~5 | ~63% |
| Ultra (H24--H31) | 8 | ~1 | ~13% |

### Axis Contribution to Sparsity

The sparsity arises from all four axes, but not equally:

- **r3_idx**: Models demand only the R3 features relevant to their cognitive function. A beat detector does not need every spectral feature. Typical model demands ~10--20 of 128 features.
- **horizon**: Each mechanism operates at specific temporal scales. Only ~15 of 32 horizons are demanded.
- **morph**: Models demand only the temporal transformations they need. Typical model uses ~3--6 of 24 morphs.
- **law**: Most demands use L0 (Memory). L1 (Prediction) and L2 (Integration) are less common.

---

## 4. DemandTree: The Sparsity Enabler

The `DemandTree` data structure organizes the sparse demand set for efficient computation:

```python
demand_tree = {
    h_idx: {(r3_idx, morph_idx, law_idx), ...},
    ...
}
```

This grouping is not arbitrary. It reflects the computational structure:

1. **Attention weights** depend only on `horizon` -- computed once per horizon, O(n_frames)
2. **Window selection** depends on `law` -- O(1) lookup per frame
3. **Morph computation** depends on `morph` -- dispatched per tuple

By grouping on horizon first, the most expensive shared computation (attention weights) is maximally reused.

---

## 5. Memory Comparison: Dense vs. Sparse

### Dense Approach (Not Used)

```
Storage per frame: 294,912 * 4 bytes = 1.12 MB
For T = 17,227: 294,912 * 17,227 * 4 bytes = ~19.3 GB
```

### Sparse Approach (Actual)

```
Storage per frame: ~8,600 * 4 bytes = ~33.6 KB
For T = 17,227: 8,600 * 17,227 * 4 bytes = ~566 MB
```

| Sequence Length | Dense (B=1) | Sparse (B=1) | Reduction |
|----------------|-------------|--------------|-----------|
| 10s (1,723 frames) | ~1.93 GB | ~56.6 MB | 34x |
| 30s (5,168 frames) | ~5.79 GB | ~169.8 MB | 34x |
| 100s (17,227 frames) | ~19.3 GB | ~566 MB | 34x |
| 300s (51,681 frames) | ~57.9 GB | ~1.70 GB | 34x |

The reduction factor is constant at ~34x because it equals the ratio of theoretical to actual tuples (294,912 / 8,600 = 34.3).

---

## 6. Per-Unit Sparsity

Each of the 9 C3 units demands a different number of tuples, depending on the number and complexity of its models:

| Unit | Models | Approx. Tuples | % of Theoretical |
|------|--------|-----------------|------------------|
| SPU | 9 | ~450 | 0.15% |
| STU | 14 | ~900 | 0.31% |
| IMU | 15 | ~1,200 | 0.41% |
| ASU | 9 | ~360 | 0.12% |
| NDU | 9 | ~400 | 0.14% |
| MPU | 10 | ~500 | 0.17% |
| PCU | 10 | ~500 | 0.17% |
| ARU | 10 | ~500 | 0.17% |
| RPU | 10 | ~400 | 0.14% |
| **Total (pre-dedup)** | **96** | **~5,210** | **1.77%** |
| **Total (post-dedup)** | -- | **~8,600** | **2.92%** |

Note: The post-dedup total is larger than the simple sum because the table above shows per-unit counts before cross-unit deduplication is considered. Actual unique tuples across all units total ~8,600 after deduplication of overlapping demands.

---

## 7. Per-Tier Sparsity

Models at different tiers have different demand sizes, reflecting their complexity:

| Tier | Models per Unit | Typical Tuples per Model | Horizons Used | Morphs Used |
|------|----------------|--------------------------|---------------|-------------|
| Alpha (1--3) | 3 | ~120 | 4--6 | 4--6 |
| Beta (4--6) | 3--4 | ~60 | 3--4 | 3--4 |
| Gamma (7--10) | 3--4 | ~40 | 2--3 | 2--3 |

Alpha models demand the most because they are the primary feature extractors. Beta and gamma models often reuse the same R3 features at the same horizons, adding only different morph/law combinations, which contributes to deduplication savings.

---

## 8. Sparsity and Future Evolution

As the R3 feature space evolves (currently at v1 with 49 semantically named features mapped to 128 computational features), the occupancy is expected to remain low or decrease:

- Adding new R3 features increases the denominator (128 may grow) without proportionally increasing demands
- New models may overlap significantly with existing demands, benefiting from deduplication
- The demand-driven architecture means unused features incur zero cost

The current 2.9% occupancy represents a practical ceiling: it reflects the union of all cognitive demands across 96 models. Individual models are far sparser.

---

## 9. Code References

| Component | File | Key Element |
|-----------|------|-------------|
| Demand aggregation | `mi_beta/ear/h3/demand.py` | `DemandTree.build()` |
| Demand declaration | C3 model files | `h3_demand` class attribute |
| Sparse output | `mi_beta/ear/h3/__init__.py` | `H3Output.features` dict |

---

## 10. Cross-References

- [ExecutionModel.md](ExecutionModel.md) -- How the DemandTree drives the execution loop
- [Performance.md](Performance.md) -- Cost implications of sparsity
- [WarmUp.md](WarmUp.md) -- Boundary effects unrelated to sparsity
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Design rationale for the address space dimensions
