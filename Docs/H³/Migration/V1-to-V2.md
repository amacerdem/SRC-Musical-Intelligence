# H3 Migration Guide -- V1 to V2

> Version 2.0.0 | Updated 2026-02-13

## 1. Overview

The H3 v1-to-v2 migration accommodates the R3 feature expansion from 49 dimensions (groups A-E) to 128 dimensions (groups A-K, adding 79 new features in groups F through K). This expansion widens the H3 input tensor but does not alter the H3 engine, horizons, morphs, laws, or any existing demand tuple.

**v1 baseline**:
- 49 R3 features (groups A-E, indices [0:49])
- 112,896 theoretical H3 space (49 x 32 x 24 x 3)
- ~5,210 actual tuples across 96 models in 9 units

**v2 target**:
- 128 R3 features (groups A-K, indices [0:128])
- 294,912 theoretical H3 space (128 x 32 x 24 x 3)
- ~8,610 actual tuples (~5,210 v1 + ~3,400 v2 additions)

**Migration principle**: Purely additive. No v1 tuple is removed, modified, or reindexed. The H3 engine code requires zero changes because it is feature-agnostic -- `r3_idx` is an integer index into the R3 tensor, and the engine makes no assumptions about the tensor's width beyond what is demanded.

---

## 2. What Changes

| Component | v1 | v2 | Change Type |
|-----------|----|----|-------------|
| R3 feature count | 49 | 128 | Input expansion |
| R3 tensor shape | (B, T, 49) | (B, T, 128) | Tensor widening |
| Theoretical H3 space | 112,896 | 294,912 | Address space growth |
| Actual H3 tuples | ~5,210 | ~8,610 | Demand growth (+65%) |
| H3 engine code | -- | -- | **No change** |
| DemandTree code | -- | -- | **No change** |
| MorphComputer code | -- | -- | **No change** |
| AttentionKernel code | -- | -- | **No change** |
| Constants (horizons, morphs, laws) | -- | -- | **No change** |
| C3 DemandSpec tuples | Only [0:49] | [0:128] | **Model-level update** |

The only code-level changes occur in two places:

1. **R3 extractor** (upstream of H3): Produces a wider output tensor.
2. **C3 model DemandSpec declarations**: Individual models append new 4-tuples referencing `r3_idx` values in [49:128].

---

## 3. What Does NOT Change

The following H3 components are entirely unaffected by the v1-to-v2 migration:

**Horizons**: Same 32 horizons (H0-H31). Same HORIZON_FRAMES values:
```
H0=1, H1=2, H2=3, H3=5, H4=9, H5=17, H6=26, H7=43,
H8=52, H9=69, H10=86, H11=104, H12=138, H13=172, H14=259, H15=345,
H16=518, H17=862, H18=1724, H19=2586, H20=3448, H21=4310, H22=5172, H23=6897,
H24=8621, H25=12931, H26=20690, H27=34483, H28=71314, H29=103448, H30=137931, H31=169043
```

**Morphs**: Same 24 morphs (M0-M23). Same MORPH_SCALE normalization constants. Same formulas. All morph computations are feature-agnostic: they operate on a windowed, weighted 1D time series regardless of which R3 feature produced it.

**Laws**: Same 3 laws (L0 Memory, L1 Prediction, L2 Integration). Same attention kernel `A(dt) = exp(-3|dt|/H)` with ATTENTION_DECAY = 3.0. Same boundary weight ~4.98%.

**DemandTree structure**: Groups tuples by horizon regardless of `r3_idx`. Adding v2 tuples simply adds entries to existing horizon groups or creates entries at horizons not previously demanded.

**MorphComputer**: All 24 `compute_*` methods accept a windowed values tensor and an attention weights tensor. They do not inspect or depend on `r3_idx`.

**Frame rate**: 172.27 Hz (5.8 ms/frame) is determined by the cochlea pipeline, not by H3.

---

## 4. Migration Steps

### Step 1: R3 Expansion (Phase 5, Ear Pipeline)

Update the R3 extractor to produce an output tensor of shape `(B, T, 128)` instead of `(B, T, 49)`.

- The R3 pipeline adds 79 new feature extraction functions for groups F through K.
- The H3Extractor receives the wider tensor transparently.
- `H3Extractor.extract()` indexes only the demanded columns via `r3_tensor[:, :, r3_idx]`, so unused columns incur no computational cost.
- The R3 tensor's memory footprint increases from `B * T * 49 * 4` to `B * T * 128 * 4` bytes (2.61x), but this is the input tensor only and is shared across all H3 computations.

### Step 2: DemandSpec Updates (Phase 5, C3 Models)

Each C3 model that consumes v2 features adds new 4-tuples to its `h3_demand` set. The procedure is documented in detail in [DemandSpec-Update.md](DemandSpec-Update.md).

Key points:
- Existing v1 tuples are unchanged. New tuples are appended.
- Each new tuple references an `r3_idx` in [49:127].
- Horizon, morph, and law selections follow the model's existing mechanism assignments and perceptual role.
- Example: PCU-alpha1-HTP adds `(92, 12, 0, 1)` for predictive_entropy at H12, value morph, prediction law.

### Step 3: Validation

Run acceptance criteria for all new v2 tuples:

1. **Regression test**: Execute the H3 pipeline with a v1-only demand set on a fixed input. Compare outputs against golden-reference values saved from v1. All outputs must be bit-identical.
2. **v2 output range**: All new tuple outputs must be in [0, 1] (post MORPH_SCALE normalization).
3. **NaN check**: No NaN values in any v2 output for any of the standard test inputs (see [AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md)).
4. **Morph accuracy**: New tuples pass the same morph accuracy benchmarks as v1 tuples (max absolute error < 1e-5 vs NumPy reference).

### Step 4: Incremental Adoption

Models adopt v2 features independently at their own pace:

1. No cross-model dependencies. Model A can adopt v2 features while Model B remains v1-only.
2. No unit-level coordination required. Models within the same unit can be at different v2 adoption levels.
3. **Priority order** (based on cross-unit demand analysis):
   - **P1**: I: Information [87:94] -- Highest cross-unit demand (PCU, RPU, IMU)
   - **P2**: G: Rhythm [65:75] -- Critical for STU (14 models) and MPU (10 models)
   - **P3**: H: Harmony [75:87] -- High demand from NDU, PCU, IMU
   - **P4**: F: Pitch [49:65] -- Medium demand from SPU, IMU, PCU
   - **P5**: J: Timbre [94:114] -- Medium demand, SPU and ASU primary
   - **P6**: K: Modulation [114:128] -- Lowest demand, STU and ARU primary
4. Each model's v2 adoption is tracked in its model documentation version history.

---

## 5. Backward Compatibility Guarantee

The following guarantees hold throughout and after the v1-to-v2 migration:

| Guarantee | Description |
|-----------|-------------|
| **Tuple stability** | All v1 DemandSpec tuples (r3_idx in [0:48]) continue to work unchanged. No reindexing. |
| **Output identity** | v1-only models produce bit-identical outputs before and after v2 migration. |
| **Engine transparency** | The H3 engine is fully backward compatible because it is feature-agnostic. It indexes into the R3 tensor by integer position and applies the same morph/law/horizon logic regardless of feature identity. |
| **No forced adoption** | No model is required to adopt v2 features. A model can remain v1-only indefinitely. |
| **Demand isolation** | Adding v2 tuples to one model does not affect the H3 outputs of any other model. DemandTree groups are per-extraction-call, not shared. |

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| V1 output regression | Very Low | High | Golden-reference regression test with bit-identical comparison |
| V2 feature NaN | Low | Medium | MORPH_SCALE normalization + output clamping to [0, 1] |
| V2 morph instability at small horizons | Low | Medium | MorphQualityTiers gates morph-horizon combinations |
| Performance degradation | Low | Medium | Demand-driven sparsity limits computation to demanded tuples only; ~65% more tuples within GPU budget |
| Memory pressure | Low | Low | R3 tensor 2.61x wider; H3 output ~65% larger; both well within 16GB unified memory |
| Index collision | None | -- | v2 indices [49:127] are disjoint from v1 indices [0:48] by construction |
| Morph formula inadequacy for v2 features | Low | Medium | v2 features are normalized to [0,1] by R3 pipeline; morphs are feature-agnostic |

---

## 7. Timeline

| Phase | Activity | H3 Impact |
|-------|----------|-----------|
| Phase 4 (current) | H3 documentation suite | Migration guide written (this document) |
| Phase 5 | R3 v2 implementation + H3 validation | R3 tensor widens to 128D; v2 tuples validated |
| Phase 5 | C3 model DemandSpec updates | Models begin adopting v2 tuples per priority order |
| Phase 6 | R3 formula revisions | Improved R3 feature quality flows through to H3 automatically |
| Phase 6+ | Continued v2 adoption | Models continue adding v2 tuples as features stabilize |

Models can begin adopting v2 features as soon as the R3 v2 extractor is operational (Phase 5). Adoption may continue through Phase 6 and beyond as R3 feature quality improves.

---

## 8. Cross-References

| Related Document | Location |
|-----------------|----------|
| DemandSpec update procedure | [DemandSpec-Update.md](DemandSpec-Update.md) |
| R3 v2 H3 impact analysis | [../Expansion/R3v2-H3-Impact.md](../Expansion/R3v2-H3-Impact.md) |
| Expansion group files (F-K) | [../Expansion/](../Expansion/) |
| Acceptance criteria | [../Validation/AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md) |
| Benchmark plan | [../Validation/BenchmarkPlan.md](../Validation/BenchmarkPlan.md) |
| Morph quality tiers | [../Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md) |
| Per-unit demand documentation | [../Demand/](../Demand/) |
| DemandAddressSpace registry | [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md) |
| H3DemandSpec contract (C3) | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| R3 feature catalog | [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md) |
| Migration index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial migration guide (Phase 4H) |
