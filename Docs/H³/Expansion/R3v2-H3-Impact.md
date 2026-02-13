# R3 v2 Expansion -- H3 Impact Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Overview

The R3 spectral layer expands from 49 features (v1, groups A-E) to 128 features (v2, groups A-K) with the addition of 79 new features across six groups:

| Group | Name | Dimensions | Indices |
|-------|------|:----------:|---------|
| F | Pitch & Chroma | 16D | [49:65] |
| G | Rhythm & Groove | 10D | [65:75] |
| H | Harmony & Tonality | 12D | [75:87] |
| I | Information & Surprise | 7D | [87:94] |
| J | Timbre Extended | 20D | [94:114] |
| K | Modulation & Psychoacoustic | 14D | [114:128] |

This expansion directly impacts H3 because the first axis of every H3 4-tuple is `r3_idx` -- the integer index into the R3 feature tensor. Adding 79 new indices means 79 new features that C3 models can place temporal demand on.

**Key insight**: The horizons (32), morphs (24), and laws (3) are unchanged. These are temporal operations that act on any R3 feature identically. What changes is the set of `r3_idx` values that appear in `H3DemandSpec` tuples. The H3 engine is fully feature-agnostic -- `r3_idx` is simply an integer offset into the dense R3 tensor.

---

## 2. Space Expansion Analysis

### Theoretical Space

| Metric | v1 | v2 | Growth |
|--------|---:|---:|:------:|
| R3 features | 49 | 128 | 2.61x |
| Horizons | 32 | 32 | 1.00x |
| Morphs | 24 | 24 | 1.00x |
| Laws | 3 | 3 | 1.00x |
| **Theoretical 4-tuples** | **112,896** | **294,912** | **2.61x** |

### Actual Demand

| Metric | v1 | v2 (combined) | Growth |
|--------|---:|:-------------:|:------:|
| Active tuples | ~5,210 | ~8,610 | ~1.65x |
| Occupancy | ~4.6% | ~2.9% | -37% relative |
| Models | 96 | 96 | 1.00x |
| Units | 9 | 9 | 1.00x |

The occupancy rate drops from ~4.6% to ~2.9% because the new features are consumed more selectively than the original 49. Groups F-K serve specialized perceptual functions (pitch tracking, rhythm analysis, harmonic structure) that are relevant to specific units rather than broadly demanded across the entire brain architecture.

### Why Growth is Sub-Linear

Three factors constrain actual demand growth:

1. **Unit specialization**: Each unit consumes only the R3 groups relevant to its perceptual function. STU consumes G (Rhythm) heavily but ignores F (Pitch). SPU consumes F but not G.
2. **Horizon selectivity**: New features don't demand all 32 horizons. Chroma evolution is meaningful at H6-H18 but not at H0-H3 (too fast for tonal change) or H24-H31 (too slow to track).
3. **Morph parsimony**: Most new features need only 3-6 morphs, not all 24. Tempo stability needs M0, M1, M2, M18 but not M6 (skewness) or M23 (symmetry).

---

## 3. Per-Group Temporal Priority

| Group | Priority | Temporal Character | Primary Horizons | Primary Mechanisms | Primary Units |
|-------|:--------:|-------------------|:----------------:|-------------------|---------------|
| F: Pitch & Chroma | HIGH | Chroma evolution tracks tonal movement across phrases; pitch contour operates at note/beat scale | H3-H16 | PPC, TPC, MEM | SPU, IMU, PCU |
| G: Rhythm & Groove | HIGH | Rhythmic features need beat-rate and metric-hierarchy horizons; temporal-of-temporal hierarchy | H12-H22 | BEP, TMH | STU, MPU |
| H: Harmony & Tonality | HIGH | Harmonic rhythm operates at phrase-to-section timescales; chord and key change rates | H12-H22 | SYN, TPC, MEM | NDU, PCU, IMU |
| I: Information & Surprise | MEDIUM-HIGH | Prediction error and surprise have dynamics at all scales; information rate tracks complexity | H6-H22 | PPC, TPC, AED, CPD | PCU, RPU, IMU |
| J: Timbre Extended | MEDIUM | MFCC evolution and spectral contrast change at Meso timescales; timbral memory | H6-H18 | PPC, ASA | SPU, ASU |
| K: Modulation & Psycho | MEDIUM | Modulation features are already temporal (Hz rates); their evolution matters at Macro timescales | H16-H25 | TMH, MEM | STU, ARU |

### Priority Rationale

**HIGH** groups (F, G, H) represent core musical dimensions -- pitch, rhythm, harmony -- whose temporal evolution is fundamental to music perception. Every musical style relies on how these features change over time. The majority of C3 models in at least 2-3 units will place direct demand on these groups.

**MEDIUM-HIGH** (I) captures information-theoretic quantities whose temporal dynamics are central to predictive processing (PCU's core function) but are consumed by fewer units overall.

**MEDIUM** groups (J, K) extend existing capabilities (J extends C group timbre, K adds modulation rates) and serve more specialized analytical functions. Their temporal demand is real but narrower in scope.

---

## 4. Per-Unit v2 Demand Expansion

| Unit | v1 Tuples | v2 Additions | Total | Primary New Groups | Growth |
|------|:---------:|:------------:|:-----:|-------------------|:------:|
| SPU | ~450 | ~350 | ~800 | F (chroma, pitch), J (MFCC extended) | +78% |
| STU | ~900 | ~600 | ~1,500 | G (rhythm, groove), K (modulation rates) | +67% |
| IMU | ~1,200 | ~500 | ~1,700 | I (information), H (harmony), F (chroma) | +42% |
| ASU | ~360 | ~250 | ~610 | F (pitch salience), J (MFCC, contrast) | +69% |
| NDU | ~400 | ~350 | ~750 | H (harmony), I (information) | +88% |
| MPU | ~500 | ~400 | ~900 | G (rhythm, groove) | +80% |
| PCU | ~500 | ~500 | ~1,000 | I (information), H (harmony), F (pitch) | +100% |
| ARU | ~500 | ~200 | ~700 | Indirect (pathway features), K (fluctuation) | +40% |
| RPU | ~400 | ~250 | ~650 | I (information), H (harmony) | +63% |
| **Total** | **~5,210** | **~3,400** | **~8,610** | | **+65%** |

### Observations

- **PCU** has the largest relative growth (+100%) because information-theoretic and harmonic features are central to predictive coding.
- **NDU** grows substantially (+88%) as harmonic novelty detection is a primary function.
- **STU** has the largest absolute growth (+600 tuples) driven by the G:Rhythm group, which is mission-critical for timing.
- **IMU** remains the largest total consumer (~1,700 tuples) due to its broad integrative role.
- **ARU** has the smallest growth (+40%) because affective features are consumed indirectly through pathways rather than direct R3 indexing.

---

## 5. Horizon Demand Shifts

### v1 Horizon Distribution

The v1 demand profile is heavily weighted toward Meso and Macro bands, reflecting BEP-dominant (STU, MPU) and TMH/MEM-dominant (IMU, STU) processing:

```
Band       Micro (H0-H7)  Meso (H8-H15)  Macro (H16-H23)  Ultra (H24-H31)
v1 share   ~18%           ~35%            ~40%              ~7%
```

### v2 Horizon Shift

The addition of groups F-K shifts the distribution:

```
Band       Micro (H0-H7)  Meso (H8-H15)  Macro (H16-H23)  Ultra (H24-H31)
v2 share   ~16%           ~38%            ~40%              ~6%
```

| Band | v1 Tuples | v2 Additions | Combined | Shift |
|------|:---------:|:------------:|:--------:|:-----:|
| Micro (H0-H7) | ~940 | ~350 | ~1,290 | Modest growth: F pitch at H3-H6 |
| Meso (H8-H15) | ~1,820 | ~1,400 | ~3,220 | Largest growth: G rhythm at H9-H12, H harmony at H12 |
| Macro (H16-H23) | ~2,090 | ~1,450 | ~3,540 | Significant growth: F/H at H16-H18, K at H16-H22 |
| Ultra (H24-H31) | ~360 | ~200 | ~560 | Minimal growth: only K modulation at H25 |

### Key Shifts

- **Meso band gains the most absolute demand** from G group rhythm features at BEP horizons (H9, H11) and H group harmonic features at SYN horizons (H12).
- **Macro band remains dominant** as F chroma and H harmony features at phrase/section timescales (H16, H18) add substantial demand.
- **Micro band grows modestly** -- pitch onset detection at H3-H6 adds ~350 tuples from F group.
- **Ultra band is nearly unchanged** -- new features do not require 36s+ observation windows. Only K group modulation trajectory at H25 adds sparse demand.

---

## 6. Morph Demand Patterns for New Groups

Each new R3 group has characteristic morph demand patterns driven by the perceptual statistics that are meaningful for that feature type.

### F: Pitch & Chroma

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous chroma/pitch values |
| Mean | M1 | Prevailing key center, average pitch height |
| Std | M2 | Tonal instability, pitch variability |
| Velocity | M8 | Harmonic rhythm rate, melodic contour slope |
| Periodicity | M14 | Cyclic tonal patterns (verse/chorus key returns) |
| Trend | M18 | Modulation direction (ascending/descending key drift) |

### G: Rhythm & Groove

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous tempo, beat strength |
| Mean | M1 | Average tempo, mean groove level |
| Std | M2 | Tempo variability, rhythmic irregularity |
| Periodicity | M14 | Cyclic beat patterns, metric periodicity |
| Trend | M18 | Long-term tempo drift (accelerando/ritardando) |
| Entropy | M20 | Rhythmic complexity measure |

### H: Harmony & Tonality

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous harmonic quality |
| Mean | M1 | Prevailing harmonic character |
| Velocity | M8 | Harmonic rhythm rate (chord change speed) |
| Trend | M18 | Tonal trajectory (tension build/release) |
| Entropy | M20 | Harmonic uncertainty, tonal ambiguity |

### I: Information & Surprise

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous prediction error magnitude |
| Mean | M1 | Average information rate |
| Std | M2 | Uncertainty variation (predictability fluctuation) |
| Trend | M18 | Increasing/decreasing predictability over time |

### J: Timbre Extended

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous timbral quality |
| Mean | M1 | Average timbre over horizon |
| Std | M2 | Timbral variability |
| Velocity | M8 | Rate of timbral change |

### K: Modulation & Psychoacoustic

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous modulation rate |
| Mean | M1 | Average modulation depth |
| Trend | M18 | Modulation trajectory over sections |

### Morph Demand Summary

| Group | Morphs Used | Count | Dominant Category |
|-------|-------------|:-----:|-------------------|
| F | M0, M1, M2, M8, M14, M18 | 6 | Distribution + Dynamics |
| G | M0, M1, M2, M14, M18, M20 | 6 | Distribution + Rhythm |
| H | M0, M1, M8, M18, M20 | 5 | Distribution + Dynamics |
| I | M0, M1, M2, M18 | 4 | Distribution + Dynamics |
| J | M0, M1, M2, M8 | 4 | Distribution + Dynamics |
| K | M0, M1, M18 | 3 | Distribution + Dynamics |

New groups demand an average of ~4.7 morphs per group, compared to ~6.2 for v1 groups. This confirms the selective, parsimonious nature of v2 demand expansion.

---

## 7. Code Impact

### Components Requiring NO Changes

| Component | Path | Reason |
|-----------|------|--------|
| H3Extractor | `mi_beta/ear/h3/extractor.py` | `r3_idx` is an integer index; no range check. Operates on `R3_tensor[:, :, r3_idx]` regardless of index value. |
| DemandTree | `mi_beta/ear/h3/demand_tree.py` | Groups tuples by horizon. Horizon grouping is independent of `r3_idx` range. |
| MorphComputer | `mi_beta/ear/h3/morph_computer.py` | Morph operations (mean, std, velocity, etc.) are applied to 1D feature time-series. Feature identity is irrelevant. |
| AttentionKernel | `mi_beta/ear/h3/attention.py` | Kernel `A(dt) = exp(-3|dt|/H)` depends only on horizon H, not on feature content. |
| Constants | `mi_beta/core/constants.py` | `HORIZON_MS`, `MORPH_NAMES`, `LAW_NAMES` are feature-independent. `R3_DIM=128` is already set for v2. |

### Components Requiring Changes

| Component | Nature of Change |
|-----------|-----------------|
| C3 model `H3DemandSpec` tuples | Each model that consumes v2 features must add new `(r3_idx, horizon, morph, law)` tuples with `r3_idx` in [49:128]. |
| C3 model documentation | `h3_demand` sections in model docs must be extended with new tuple listings. |
| Demand validation scripts | Test harnesses should verify that new `r3_idx` values resolve to valid R3 features. |

### Summary

The H3 engine is fully insulated from the R3 expansion. All changes are localized to the C3 model layer, where `DemandSpec` declarations are extended. This validates the architectural decision to make H3 feature-agnostic -- the engine was designed to support arbitrary `r3_idx` values, and the v2 expansion exercises that design without requiring any engine modifications.

---

## 8. Migration Considerations

### Backward Compatibility

- All existing v1 demands (`r3_idx` in [0:49]) are **completely unchanged**.
- No v1 tuple is modified, removed, or reinterpreted.
- Models that do not adopt v2 features continue to function identically.

### Adoption Strategy

- New demands are **purely additive** -- each model extends its `h3_demand` tuple list with new entries.
- Models can adopt v2 features **incrementally**, adding tuples for one R3 group at a time.
- No ordering constraints: a model can adopt H group features before F group features, or vice versa.
- The recommended adoption order follows temporal priority: F/G/H first (HIGH), then I (MEDIUM-HIGH), then J/K (MEDIUM).

### Validation

For each new tuple `(r3_idx, horizon, morph, law)`:

1. Verify `r3_idx` maps to a valid v2 feature in the R3 FeatureCatalog.
2. Verify the horizon is appropriate for the feature's temporal dynamics.
3. Verify the morph is meaningful for the feature type.
4. Verify the law matches the model's causal perspective.

### Per-Unit Adoption Sequence

| Phase | Units | Groups | Rationale |
|-------|-------|--------|-----------|
| Phase 1 | STU, MPU | G | Rhythm features are mission-critical for timing units |
| Phase 2 | SPU, IMU, PCU | F, H | Pitch and harmony are core musical dimensions |
| Phase 3 | PCU, RPU, NDU | I | Information-theoretic features for prediction and novelty |
| Phase 4 | SPU, ASU | J | Extended timbre for spectral units |
| Phase 5 | STU, ARU | K | Modulation rates for timing and affect |

---

## 9. Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **H3 Master Index**: [../00-INDEX.md](../00-INDEX.md)
- **Demand Documentation**: [../Demand/00-INDEX.md](../Demand/00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **Registry / DemandAddressSpace**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **Law Catalog**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
- **Migration Guide**: [../Migration/V1-to-V2.md](../Migration/V1-to-V2.md)
- **Per-Group Files**:
  - [F-PitchChroma-Temporal.md](F-PitchChroma-Temporal.md)
  - [G-RhythmGroove-Temporal.md](G-RhythmGroove-Temporal.md)
  - [H-HarmonyTonality-Temporal.md](H-HarmonyTonality-Temporal.md)
  - [I-InformationSurprise-Temporal.md](I-InformationSurprise-Temporal.md)
  - [J-TimbreExtended-Temporal.md](J-TimbreExtended-Temporal.md)
  - [K-ModulationPsychoacoustic-Temporal.md](K-ModulationPsychoacoustic-Temporal.md)
- **Expansion Index**: [00-INDEX.md](00-INDEX.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial R3 v2 impact analysis (Phase 4G) |
