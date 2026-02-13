# H3 Registry -- Demand Address Space

**Version**: 2.0.0
**Theoretical space**: 294,912 addresses
**Actual usage**: ~8,600 tuples (~2.9% occupancy)
**Code reference**: `mi_beta.ear.h3.extractor.H3Extractor`, `mi_beta.core.constants`
**Updated**: 2026-02-13

---

## Address Format

Every H3 demand is a **4-tuple**:

```
(r3_idx, horizon, morph, law)
```

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `r3_idx` | int | [0, 127] | Index into the R3 feature vector (128 features) |
| `horizon` | int | [0, 31] | Temporal horizon index (32 horizons) |
| `morph` | int | [0, 23] | Morphological descriptor index (24 morphs) |
| `law` | int | [0, 2] | Temporal perspective law index (3 laws) |

### Example

```python
(5, 6, 0, 0)
# r3_idx=5 (roughness_total), horizon=6 (H6, 200ms), morph=0 (attention_weighted_mean), law=0 (L0 Memory)
# "The attention-weighted mean of roughness_total over a 200ms causal window"
```

---

## Flat Index Formula

For storage and lookup, the 4-tuple can be converted to a flat integer index:

```
flat_idx = r3_idx * (32 * 24 * 3) + horizon * (24 * 3) + morph * 3 + law
```

Expanded:

```
flat_idx = r3_idx * 2304 + horizon * 72 + morph * 3 + law
```

### Inverse mapping (flat index to tuple):

```python
law      = flat_idx % 3
morph    = (flat_idx // 3) % 24
horizon  = (flat_idx // 72) % 32
r3_idx   = flat_idx // 2304
```

### Field strides

| Field | Stride | Meaning |
|-------|-------:|---------|
| `law` | 1 | Adjacent flat indices differ by law |
| `morph` | 3 | Consecutive morphs are 3 apart |
| `horizon` | 72 | Consecutive horizons are 72 apart |
| `r3_idx` | 2,304 | Consecutive R3 features are 2,304 apart |

---

## Theoretical Space

```
128 (R3 features) x 32 (horizons) x 24 (morphs) x 3 (laws) = 294,912 addresses
```

| Dimension | Count | Bits Required |
|-----------|------:|:-------------:|
| R3 features | 128 | 7 |
| Horizons | 32 | 5 |
| Morphs | 24 | 5 |
| Laws | 3 | 2 |
| **Total** | **294,912** | **19** |

The flat index fits in a 19-bit unsigned integer (max value = 294,911).

---

## Actual Usage

### Estimated demand by source

| Source | R3 Features | Est. Tuples | Notes |
|--------|:-----------:|:-----------:|-------|
| R3 v1 features | 49 (indices 0-48) | ~5,210 | From 96 C3 models across 9 units |
| R3 v2 features | 79 (indices 49-127) | ~3,400 | Estimated from expansion groups F-K |
| **Total** | **128** | **~8,610** | |

### Occupancy: ~8,610 / 294,912 = **~2.9%**

### Demand distribution by axis

| Axis | Active Values | Total | Active % | Notes |
|------|:------------:|:-----:|:--------:|-------|
| R3 features | ~90 of 128 | 128 | ~70% | Not all features are temporally demanded |
| Horizons | ~18 of 32 | 32 | ~56% | Many horizons unused; demand clusters at mechanism-specific scales |
| Morphs | ~16 of 24 | 24 | ~67% | M0, M1, M2, M4, M5, M9, M14, M18, M20 are most common |
| Laws | 3 of 3 | 3 | 100% | All three laws are used |

---

## Sparsity Analysis

### Why is the space so sparse?

1. **Demand-driven design**: Each C3 model declares only the H3 tuples it needs. A typical model demands 12-150 tuples out of the 294,912 possible.

2. **Mechanism specialization**: Each mechanism operates at specific horizons (e.g., BEP only at H6/H9/H11). This creates strong horizon selectivity -- most horizons are irrelevant for most mechanisms.

3. **Feature relevance**: Not every R3 feature needs temporal morphology at every horizon. Spectral features (brightness, centroid) are meaningful at meso/macro horizons but not at sub-neural micro horizons. Onset features need micro horizons but not ultra horizons.

4. **Morph redundancy avoidance**: Models typically need only 3-8 morphs per (r3_idx, horizon, law) combination, not all 24. Distribution morphs (M0-M4) are most common; advanced morphs (M6, M7, M16, M17) are used sparingly.

5. **Law selectivity**: Most units use 2 of 3 laws. Only STU, NDU, PCU, ARU, and RPU use all three.

### Sparsity by unit

| Unit | Est. Tuples | % of Space | Primary Horizons | Primary Laws |
|------|:-----------:|:----------:|:----------------:|:------------:|
| SPU | ~450 | 0.15% | H0-H6, H12, H16 | L0, L2 |
| STU | ~900 | 0.31% | H6-H22 | L0, L1, L2 |
| IMU | ~1,200 | 0.41% | H12-H25 | L0, L2 |
| ASU | ~360 | 0.12% | H3-H9 | L2 |
| NDU | ~400 | 0.14% | H3-H18 | L0, L1, L2 |
| MPU | ~500 | 0.17% | H6-H11 | L0, L1 |
| PCU | ~500 | 0.17% | H0-H20 | L0, L1, L2 |
| ARU | ~500 | 0.17% | H6-H19 | L0, L1, L2 |
| RPU | ~400 | 0.14% | H6-H18 | L0, L1, L2 |

**Note**: Tuples overlap between units (same H3 tuple demanded by multiple models). Total unique tuples (~8,600) is less than the sum of per-unit tuples because of shared demands.

---

## Lazy Computation Strategy

The H3 engine exploits sparsity through demand-driven lazy computation:

1. **Demand collection**: At initialization, all C3 models register their H3 demand tuples
2. **Deduplication**: Duplicate demands across models are merged into a unique demand set
3. **DemandTree construction**: Tuples are grouped into a tree keyed by horizon for efficient batch computation
4. **Lazy evaluation**: At each frame, only demanded tuples are computed; the rest of the 294,912-address space is never touched

### DemandTree Structure

The DemandTree groups demands by horizon for efficient windowed computation:

```python
DemandTree = Dict[int, List[Tuple[int, int, int]]]
# horizon -> [(r3_idx, morph, law), ...]

# Example:
{
    6:  [(5, 0, 0), (5, 2, 0), (12, 0, 2), ...],   # H6 (200ms): 45 demands
    9:  [(5, 0, 0), (5, 14, 2), ...],                # H9 (350ms): 32 demands
    16: [(5, 0, 0), (5, 1, 0), (12, 18, 1), ...],   # H16 (1s): 58 demands
    ...
}
```

**Rationale for horizon-keyed grouping**: All demands at the same horizon share the same window size. The extractor computes the windowed R3 slice once per horizon, then evaluates all (r3_idx, morph, law) combinations within that window. This avoids redundant window computation.

### Computational Savings

| Approach | Tuples Computed | Relative Cost |
|----------|:--------------:|:-------------:|
| Dense (all 294,912) | 294,912 | 1.0x |
| Demand-driven (~8,600) | ~8,600 | 0.029x |
| **Savings** | | **~34x** |

---

## H3DemandSpec Reference

Each C3 model declares its H3 demands via the `H3DemandSpec` contract. See [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) for the full specification.

### Key fields

```python
class H3DemandSpec:
    h3_demand: Tuple[Tuple[int, int, int, int], ...]
    # Each inner tuple: (r3_idx, horizon, morph, law)
```

### Validation rules

- `r3_idx` must be in `[0, N_R3_FEATURES - 1]` = `[0, 127]`
- `horizon` must be in `[0, N_HORIZONS - 1]` = `[0, 31]`
- `morph` must be in `[0, N_MORPHS - 1]` = `[0, 23]`
- `law` must be in `[0, N_LAWS - 1]` = `[0, 2]`
- Morph minimum window must be <= horizon frame count (e.g., M7 requires >= 4 frames, so H0 with 1 frame is invalid for M7)
- No duplicate tuples within a single model's demand

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry index**: [00-INDEX.md](00-INDEX.md)
