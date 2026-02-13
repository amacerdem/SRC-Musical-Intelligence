# H3 Temporal Architecture -- Extension Guide

**Version**: 2.0.0
**Purpose**: Developer guide for extending the H3 temporal morphology space
**Audience**: MI contributors adding new horizons, morphs, or laws
**Updated**: 2026-02-13

---

## 1. Adding a New Horizon

Horizons are temporal window durations. Adding one is moderately common (e.g., to fill a gap between existing horizons or extend the Ultra band).

### Steps

1. **Choose the duration (ms) and compute frame count**
   - Frame count = `ceil(duration_ms / 5.804)`  (frame period = 1000 / 172.27 Hz)
   - Ensure the new horizon does not duplicate an existing one (see [Registry/HorizonCatalog.md](Registry/HorizonCatalog.md))

2. **Update `mi_beta/core/constants.py`**
   - Insert the new duration into `HORIZON_MS` tuple at the correct sorted position
   - All horizons must be strictly increasing; the index is the position in the tuple
   - Update `N_HORIZONS` if it is defined separately

3. **Update EventHorizon contract**
   - If `EventHorizon` performs validation on horizon count or range, update bounds
   - Code path: `mi_beta/ear/h3/event_horizon.py`

4. **Update WarmUp logic**
   - The warm-up buffer length depends on the maximum horizon
   - If the new horizon exceeds H31 (981,000 ms), update `Pipeline/WarmUp.md` and the warm-up computation in `mi_beta/ear/h3/extractor.py`

5. **Update documentation**
   - `Registry/HorizonCatalog.md` -- add row to the full table, update band summary
   - `Bands/{Band}/` -- add or update the relevant band sub-document
   - `00-INDEX.md` -- update horizon count and theoretical space calculation
   - `CHANGELOG.md` -- record the addition

6. **Update demand declarations**
   - Any C3 model that should use the new horizon needs its `h3_demand` updated
   - Update the corresponding `Demand/{UNIT}-H3-DEMAND.md`

### Constraints

- Maximum horizon count is currently 32 (5 bits in the flat index). Exceeding 32 requires updating `DemandAddressSpace` and the flat index formula.
- Horizons below 5.8 ms (1 frame) are not meaningful at the current frame rate.

---

## 2. Adding a New Morph

Morphs are statistical descriptors computed over windowed R3 features. Adding one is moderately common when new analytical perspectives are needed.

### Steps

1. **Define the morph mathematically**
   - Write a clear formula with defined input/output ranges
   - Determine the minimum window size (in frames) required for the computation
   - Verify the morph is not redundant with existing morphs (see [Registry/MorphCatalog.md](Registry/MorphCatalog.md))

2. **Implement in `MorphComputer`**
   - Code path: `mi_beta/ear/h3/morph.py`
   - Add a new method following the existing pattern (input: windowed tensor, output: scalar tensor)
   - Register the method in the morph dispatch table

3. **Update `mi_beta/core/constants.py`**
   - Append the morph name to `MORPH_NAMES` tuple
   - Add a `(gain, bias)` entry to `MORPH_SCALE` for output normalization to [0, 1]
   - Update `N_MORPHS` if it is defined separately

4. **Calibrate MORPH_SCALE**
   - Run the morph over a representative dataset to determine raw output range
   - Set `gain` and `bias` so that `gain * raw + bias` maps the 1st-99th percentile range to [0, 1]
   - Document calibration methodology in `Morphology/MorphScaling.md`

5. **Update documentation**
   - `Registry/MorphCatalog.md` -- add row to the full table with formula, category, min window
   - `Morphology/{Category}.md` -- add to the relevant category document
   - `00-INDEX.md` -- update morph count and theoretical space calculation
   - `CHANGELOG.md` -- record the addition

6. **Update demand declarations**
   - Add the new morph to relevant C3 model `h3_demand` tuples
   - Update `Demand/{UNIT}-H3-DEMAND.md` for affected units

### Constraints

- Maximum morph count is currently 24. Exceeding 24 requires updating `DemandAddressSpace` and the flat index formula.
- All morph outputs must be normalizable to [0, 1] via MORPH_SCALE.
- Minimum window must be >= 1 frame.

---

## 3. Adding a New Law

Laws define temporal perspective (past, future, or bidirectional). Adding a new law is **extremely rare** -- the three existing laws cover the fundamental temporal directions. Consider carefully whether the new perspective is truly distinct from L0/L1/L2.

### Steps

1. **Define the kernel function**
   - Specify window selection rule: which frames are included
   - Specify attention weight formula: how frames within the window are weighted
   - Justify why this cannot be expressed as a combination of existing laws

2. **Update `mi_beta/core/constants.py`**
   - Append the law name to `LAW_NAMES`
   - Update `N_LAWS` if defined separately

3. **Modify the attention kernel**
   - Code path: `mi_beta/ear/h3/attention.py`
   - Add a new branch in the kernel computation for the new law index
   - The kernel must produce a weight vector of the same length as the window

4. **Update H3Extractor**
   - Ensure the extractor handles the new law index in demand tuples
   - Code path: `mi_beta/ear/h3/extractor.py`

5. **Update documentation**
   - `Registry/LawCatalog.md` -- add row and detailed description
   - `Laws/` -- create a new `L{n}-{Name}.md` document
   - `Registry/DemandAddressSpace.md` -- update law range and theoretical space
   - `00-INDEX.md` -- update law count and theoretical space calculation
   - `CHANGELOG.md` -- record the addition

### Constraints

- Adding a law multiplies the theoretical space by `(N_LAWS + 1) / N_LAWS`. With 128 features, 32 horizons, 24 morphs: each additional law adds 98,304 theoretical addresses.
- This is a major architectural change requiring review.

---

## 4. Documentation Update Checklist

After any extension, verify all of the following files are updated:

### For a new horizon

| File | Update Required |
|------|----------------|
| `mi_beta/core/constants.py` | Add to `HORIZON_MS` |
| `Registry/HorizonCatalog.md` | Add table row |
| `Registry/DemandAddressSpace.md` | Update theoretical space if count changes |
| `Bands/{Band}/` relevant doc | Add horizon details |
| `00-INDEX.md` | Update counts and summary tables |
| `CHANGELOG.md` | Record change |
| `Demand/{UNIT}-H3-DEMAND.md` | Update affected units |

### For a new morph

| File | Update Required |
|------|----------------|
| `mi_beta/core/constants.py` | Add to `MORPH_NAMES`, `MORPH_SCALE` |
| `mi_beta/ear/h3/morph.py` | Implement computation |
| `Registry/MorphCatalog.md` | Add table row |
| `Registry/DemandAddressSpace.md` | Update theoretical space if count changes |
| `Morphology/{Category}.md` | Add morph details |
| `Morphology/MorphScaling.md` | Add calibration data |
| `00-INDEX.md` | Update counts and summary tables |
| `CHANGELOG.md` | Record change |
| `Demand/{UNIT}-H3-DEMAND.md` | Update affected units |

### For a new law

| File | Update Required |
|------|----------------|
| `mi_beta/core/constants.py` | Add to `LAW_NAMES` |
| `mi_beta/ear/h3/attention.py` | Add kernel branch |
| `mi_beta/ear/h3/extractor.py` | Handle new law index |
| `Registry/LawCatalog.md` | Add table row + description |
| `Registry/DemandAddressSpace.md` | Update theoretical space |
| `Laws/L{n}-{Name}.md` | Create new document |
| `00-INDEX.md` | Update counts and summary tables |
| `CHANGELOG.md` | Record change |
| `Demand/{UNIT}-H3-DEMAND.md` | Update affected units |

---

## 5. Testing Requirements

All extensions must pass the following before merge:

1. **Unit tests**: New morph/law computations must have dedicated unit tests
2. **Shape tests**: Verify output tensor shapes match expectations for all demanded tuples
3. **Range tests**: Verify all outputs fall within [0, 1] after MORPH_SCALE normalization
4. **Warm-up test**: If a new horizon is added, verify warm-up buffer is sufficient
5. **Demand consistency**: Run the demand validator to ensure no C3 model references undefined H3 tuples
6. **Regression**: Full test suite must pass with no regressions

---

## 6. Version Bump Protocol

| Change Type | Version Bump | Example |
|-------------|:------------:|---------|
| New morph (additive) | Minor | 2.0.0 -> 2.1.0 |
| New horizon (additive) | Minor | 2.0.0 -> 2.1.0 |
| New law (architectural) | Major | 2.0.0 -> 3.0.0 |
| Morph formula correction | Patch | 2.0.0 -> 2.0.1 |
| MORPH_SCALE recalibration | Patch | 2.0.0 -> 2.0.1 |
| Documentation-only update | None | (no version change) |

When bumping a version:
1. Update `00-INDEX.md` version field
2. Add a new section to `CHANGELOG.md`
3. Update `H3-TEMPORAL-ARCHITECTURE.md` version field
4. Tag the commit with `h3-v{X.Y.Z}`

---

**Code path**: `mi_beta/ear/h3/`
**Constants**: `mi_beta/core/constants.py`
**Parent index**: [00-INDEX.md](00-INDEX.md)
