# R3 v2 Backward Compatibility Strategy

**Phase**: 3C -- Migration Documentation
**Source**: R3-V2-DESIGN.md Section 1 (Decision 7), R3-CROSSREF.md Sections 5, 7.3

---

## 1. Index Preservation Guarantee

**Invariant**: Feature indices [0:49] never change meaning across R3 v1 and v2.

All 49 existing features retain their index position:
- A: Consonance [0:7] -- roughness[0], sethares_dissonance[1], helmholtz_kang[2], stumpf_fusion[3], sensory_pleasantness[4], inharmonicity[5], harmonic_deviation[6]
- B: Energy [7:12] -- amplitude[7], velocity_A[8], acceleration_A[9], loudness[10], onset_strength[11]
- C: Timbre [12:21] -- warmth[12] through tristimulus3[20]
- D: Change [21:25] -- spectral_flux[21] through distribution_concentration[24]
- E: Interactions [25:49] -- 24D cross-products (unchanged)

Any code referencing `r3[:, :, 0]` for roughness will continue to receive roughness in v2.
New features are strictly appended at indices [49:128].

---

## 2. Phase 6 Formula Changes

Phase 6 will update computation formulas for some [0:49] features while preserving their
semantic meaning and index position. This is Layer 3 of the migration strategy.

### Bug Fixes (Critical)

| Feature | Index | Current Bug | Phase 6 Fix |
|---------|:-----:|-------------|------------|
| distribution_concentration | [24] | Uniform and concentrated both yield 1.0 due to `(sum(p^2)) * N` | Correct HHI: `(HHI - 1/N) / (1 - 1/N)` -> 0=uniform, 1=concentrated |
| loudness | [10] | Stevens law applied to log-mel = double compression | Apply Stevens law to `exp(log_mel)` or use linear power spectrum |

### Duplication Resolution

| Feature | Index | Current Issue | Phase 6 Fix |
|---------|:-----:|--------------|------------|
| stumpf_fusion | [3] | Identical formula to warmth[12] | Replace with Parncutt subharmonic matching |
| spectral_smoothness | [16] | Complement of sethares[1]: `1 - [1]` | Replace with spectral_spread (2nd central moment) |
| spectral_autocorrelation | [17] | Identical to helmholtz_kang[2] | Replace with spectral_kurtosis (4th central moment) |

### Proxy Upgrades

| Feature | Index | Current Proxy | Phase 6 Standard |
|---------|:-----:|--------------|-----------------|
| roughness | [0] | `var(mel) / mean(mel)` | Critical band pairwise comparison within ERB bands |
| sethares_dissonance | [1] | Adjacent mel bin mean abs diff | Real Sethares timbre-dependent `d(fi, fj, ai, aj)` |

### Impact on Model Code

When Phase 6 formula changes take effect:

- **Semantic meaning preserved**: roughness[0] still measures roughness, just more accurately.
- **Numerical values change**: Model weights trained on v1 roughness values will need recalibration.
- **96 model doc updates**: Section 12.1 note: "Phase 6 formula change, retraining required."
- **Index references remain valid**: `r3[0]` still accesses roughness.

---

## 3. Model Code Migration

### Current Model R3 References

96 C3 models reference R3 features via index in their Section 4 (Computational Formalization).
Example pattern:

```python
# In mi_beta/brain/units/pcu/models/htp.py
roughness = r3[:, :, 0]          # A: roughness
onset = r3[:, :, 11]             # B: onset_strength
spectral_flux = r3[:, :, 21]    # D: spectral_flux
```

### v2 Migration Impact on Models

| Migration Layer | Model Code Impact | Action Required |
|:--------------:|-------------------|-----------------|
| Layer 1 (docs) | None | No code changes |
| Layer 2 (code unlock) | Models can optionally access [49:128] | Add new `r3[:, :, idx]` references where beneficial |
| Layer 3 (formula fix) | Values at [0:49] may change numerically | Retrain models that depend on exact v1 values |

### Model Update Strategy

For the 96 C3 models:

1. **Phase 3E (doc update)**: Add new R3 v2 feature references to Section 4 of each model doc.
   These are "potential" references -- the model does not use them yet.

2. **Phase 6.7 (code update)**: After all groups are implemented and benchmarks pass:
   - Models that benefit from new features add `r3[:, :, 49:128]` access.
   - Models affected by formula changes get retrained or recalibrated.
   - Each model update is a separate commit for reviewability.

### Safe Access Pattern

Recommended pattern for models during transition:

```python
# Safe: works in both v1 (49D) and v2 (128D)
roughness = r3[:, :, 0]

# v2 only: guard with dimension check
if r3.shape[-1] >= 128:
    chroma = r3[:, :, 49:61]     # F: chroma_C..chroma_B
    key_clarity = r3[:, :, 75]   # H: key_clarity
```

---

## 4. Constants.py Migration Path

### Current State (`mi_beta/core/constants.py`)

```python
R3_DIM: int = 49
R3_CONSONANCE: tuple[int, int] = (0, 7)
R3_ENERGY: tuple[int, int] = (7, 12)
R3_TIMBRE: tuple[int, int] = (12, 21)
R3_CHANGE: tuple[int, int] = (21, 25)
R3_INTERACTIONS: tuple[int, int] = (25, 49)
```

### Phase 6 Target State

```python
R3_DIM_V1: int = 49                                        # legacy
R3_DIM: int = 128                                          # v2 active

# Existing group boundaries preserved
R3_CONSONANCE: tuple[int, int] = (0, 7)                   # unchanged
R3_ENERGY: tuple[int, int] = (7, 12)                      # unchanged
R3_TIMBRE: tuple[int, int] = (12, 21)                     # unchanged
R3_CHANGE: tuple[int, int] = (21, 25)                     # unchanged
R3_INTERACTIONS: tuple[int, int] = (25, 49)               # unchanged

# New group boundaries
R3_PITCH_CHROMA: tuple[int, int] = (49, 65)
R3_RHYTHM_GROOVE: tuple[int, int] = (65, 75)
R3_HARMONY_TONALITY: tuple[int, int] = (75, 87)
R3_INFORMATION_SURPRISE: tuple[int, int] = (87, 94)
R3_TIMBRE_EXTENDED: tuple[int, int] = (94, 114)
R3_MODULATION_PSYCHOACOUSTIC: tuple[int, int] = (114, 128)
```

Any code importing `R3_DIM` will receive the new value. Code needing the old value
uses `R3_DIM_V1` explicitly.

### Downstream Imports

Files that import from `constants.py` and require attention:

| File | Import | Migration Action |
|------|--------|-----------------|
| `mi_beta/core/dimension_map.py` | `R3_DIM` | Validation `len(names) == R3_DIM` auto-updates |
| `mi_beta/contracts/feature_spec.py` | (hardcoded 49) | Change to `from constants import R3_DIM` |
| `mi_beta/contracts/base_spectral_group.py` | (docstring only) | Update "49-D" references |
| `mi_beta/ear/r3/__init__.py` | (implicit via concat) | Output shape changes automatically |
| `mi_beta/ear/r3/_registry.py` | `R3_DIM` (potential) | Add `assert total == R3_DIM` |

---

## 5. Dimension Map Migration

**Current**: Hardcoded `_R3_FEATURE_NAMES` tuple with 49 entries (see `mi_beta/core/dimension_map.py` lines 43-65).

**Phase 6 Target**: Original tuple preserved as `_R3_FEATURE_NAMES_V1`. New `get_r3_feature_names()` function returns 128 names from `R3FeatureRegistry.freeze()`. The `DimensionMap.__init__` validation changes from `len(names) == 49` to `len(names) == R3_DIM`. See V1-to-V2.md Section 3.2 for full code details.

---

## 6. Testing Strategy for Compatibility Verification

### Unit Tests

| Test | Assertion | File |
|------|-----------|------|
| v1 names preserved | `get_r3_feature_names()[:49] == _R3_FEATURE_NAMES_V1` | `tests/core/test_dimension_map.py` |
| Total dimension | `len(get_r3_feature_names()) == 128` | Same |
| Name uniqueness | `len(set(names)) == 128` | Same |
| Group contiguity | All boundaries connect without gaps or overlaps | `tests/core/test_constants.py` |
| R3_DIM_V1 preserved | `R3_DIM_V1 == 49` | Same |

### Integration Tests

| Test | Assertion | File |
|------|-----------|------|
| v1 output identity | `v2_output[:,:,:49] == v1_output` for same mel input | `tests/ear/r3/test_regression_v2.py` |
| Full pipeline shape | `extractor.extract(mel).shape[-1] == 128` | Same |
| DimensionMap consistency | `dim_map.range_of_section("r3") == (128, 256)` for 128-mel + 128-r3 | `tests/core/test_dimension_map.py` |
| Model access pattern | `r3[:, :, 0]` returns same values pre- and post-migration | `tests/brain/test_model_compat.py` |

### Smoke Tests (Pre-merge Gate)

Run on every PR that touches `mi_beta/ear/r3/` or `mi_beta/core/constants.py`:

1. `pytest tests/ear/r3/ -x` -- all R3 tests pass
2. `pytest tests/core/ -x` -- all core tests pass
3. `python -c "from mi_beta.core.constants import R3_DIM; assert R3_DIM in (49, 128)"` -- import check

---

## 7. 96 Model Doc Update Strategy

Each of the 96 C3 model documents has a Section 4 (Computational Formalization) that references
R3 feature indices. The update strategy:

| Phase | Section 4 Change | Type |
|-------|-----------------|:----:|
| 3E | Add new `R3[idx]` references for features [49:128] that benefit the model | Additive |
| 3E | Add "Potential R3 v2 usage" note for each model | Additive |
| 6.7 | Update model code to use new features | Code change |
| 6.7 | Add "Phase 6 formula change" note to Section 12.1 for affected features | Additive |

No existing Section 4 content is deleted or modified. All changes are strictly additive until Phase 6.7 model code updates, which are tested individually per model.

---

*Source: R3-V2-DESIGN.md Section 1 (Decision 7), Section 5, Section 8; R3-CROSSREF.md Sections 5, 7.3*
