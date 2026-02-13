# R3 v1 to v2 Migration Guide (49D to 128D)

**Phase**: 3C -- Migration Documentation
**Source**: R3-V2-DESIGN.md Sections 5, 8; R3-CROSSREF.md Section 7.3

---

## 1. What Changes

### Dimension Expansion

| Property | v1 | v2 |
|----------|:--:|:--:|
| Total dimensions | 49 | 128 |
| Number of groups | 5 (A-E) | 11 (A-K) |
| Output tensor shape | (B, T, 49) | (B, T, 128) |
| Computation stages | 1 (all parallel) | 3 (dependency DAG) |

### New Group Boundaries

| Group | Name | Range | Dim | Status |
|-------|------|:-----:|:---:|:------:|
| A | Consonance | [0:7] | 7 | Existing |
| B | Energy | [7:12] | 5 | Existing |
| C | Timbre | [12:21] | 9 | Existing |
| D | Change | [21:25] | 4 | Existing |
| E | Interactions | [25:49] | 24 | Existing |
| **F** | **Pitch & Chroma** | **[49:65]** | **16** | **New** |
| **G** | **Rhythm & Groove** | **[65:75]** | **10** | **New** |
| **H** | **Harmony & Tonality** | **[75:87]** | **12** | **New** |
| **I** | **Information & Surprise** | **[87:94]** | **7** | **New** |
| **J** | **Timbre Extended** | **[94:114]** | **20** | **New** |
| **K** | **Modulation & Psychoacoustic** | **[114:128]** | **14** | **New** |

### New Feature Names (79 features, [49:128])

Canonical names are defined in R3-V2-DESIGN.md Section 2 and will be registered
in `mi_beta/ear/r3/_registry.py`. The complete list:

- **F** [49:65]: chroma_C, chroma_Db, chroma_D, chroma_Eb, chroma_E, chroma_F, chroma_Gb, chroma_G, chroma_Ab, chroma_A, chroma_Bb, chroma_B, pitch_height, pitch_class_entropy, pitch_salience, inharmonicity_index
- **G** [65:75]: tempo_estimate, beat_strength, pulse_clarity, syncopation_index, metricality_index, isochrony_nPVI, groove_index, event_density, tempo_stability, rhythmic_regularity
- **H** [75:87]: key_clarity, tonnetz_fifth_x, tonnetz_fifth_y, tonnetz_minor_x, tonnetz_minor_y, tonnetz_major_x, tonnetz_major_y, voice_leading_distance, harmonic_change, tonal_stability, diatonicity, syntactic_irregularity
- **I** [87:94]: melodic_entropy, harmonic_entropy, rhythmic_information_content, spectral_surprise, information_rate, predictive_entropy, tonal_ambiguity
- **J** [94:114]: mfcc_1 through mfcc_13, spectral_contrast_1 through spectral_contrast_7
- **K** [114:128]: modulation_0_5Hz, modulation_1Hz, modulation_2Hz, modulation_4Hz, modulation_8Hz, modulation_16Hz, modulation_centroid, modulation_bandwidth, sharpness_zwicker, fluctuation_strength, loudness_a_weighted, alpha_ratio, hammarberg_index, spectral_slope_0_500

---

## 2. What Stays the Same

- **Indices [0:49]**: All 49 existing features retain their index, name, and formula.
- **Existing formulas**: No computation changes until Phase 6.
- **Model code references**: `r3[0]` through `r3[48]` continue to work identically.
- **Input format**: mel spectrogram (B, 128, T) at sr=44100, hop=256, n_mels=128.
- **Output normalization**: All features in [0, 1].
- **Frame rate**: 172.27 Hz (5.8 ms per frame).

---

## 3. Code Changes Required (Phase 6)

Six files contain hardcoded "49" constraints. From R3-V2-DESIGN.md Section 5:

### 3.1 `mi_beta/core/constants.py` -- R3_DIM and Group Boundaries

**Current**:
```python
R3_DIM: int = 49
R3_CONSONANCE: tuple[int, int] = (0, 7)
R3_ENERGY: tuple[int, int] = (7, 12)
R3_TIMBRE: tuple[int, int] = (12, 21)
R3_CHANGE: tuple[int, int] = (21, 25)
R3_INTERACTIONS: tuple[int, int] = (25, 49)
```

**Target**:
```python
R3_DIM_V1: int = 49                                    # legacy backward compat
R3_DIM: int = 128                                      # v2 default
R3_PITCH_CHROMA: tuple[int, int] = (49, 65)            # new
R3_RHYTHM_GROOVE: tuple[int, int] = (65, 75)           # new
R3_HARMONY_TONALITY: tuple[int, int] = (75, 87)        # new
R3_INFORMATION_SURPRISE: tuple[int, int] = (87, 94)    # new
R3_TIMBRE_EXTENDED: tuple[int, int] = (94, 114)        # new
R3_MODULATION_PSYCHOACOUSTIC: tuple[int, int] = (114, 128)  # new
```

### 3.2 `mi_beta/core/dimension_map.py` -- Feature Names

**Current**: Hardcoded 49-element `_R3_FEATURE_NAMES` tuple.

**Target**: Registry-based `get_r3_feature_names()` returning 128 names. Legacy tuple preserved as `_R3_FEATURE_NAMES_V1`.

### 3.3 `mi_beta/contracts/feature_spec.py` -- Index Validation

**Current**: `assert 0 <= index < 49`

**Target**: `assert 0 <= index < R3_DIM` (imports R3_DIM from constants)

### 3.4 `mi_beta/contracts/base_spectral_group.py` -- Docstrings

**Current**: References to "49-D R3 vector"

**Target**: References to "R3 feature vector" (dimension-agnostic)

### 3.5 `mi_beta/ear/r3/__init__.py` -- R3Extractor

**Current**: Order-independent `torch.cat(parts, dim=-1)`

**Target**: Stage-ordered extraction with `STAGE_ORDER` dict and `compute_with_deps()`:
```
Stage 1: A, B, C, D, F, J, K  (parallel, mel-only)
Stage 2: E, G, H              (depend on Stage 1 outputs)
Stage 3: I                    (depends on F chroma, G onset, H key)
```

### 3.6 `mi_beta/ear/r3/_registry.py` -- R3FeatureRegistry

**Current**: No validation on freeze()

**Target**: `assert offset == R3_DIM` and feature name uniqueness check at freeze time

---

## 4. Three-Layer Migration Strategy

### Layer 1: Documentation Only (Phase 3 -- NOW)

**Scope**: Define all 128 indices, feature names, and group boundaries in documentation.

| Action | Files Affected | Impact |
|--------|---------------|--------|
| Define [49:128] feature specs | R3-V2-DESIGN.md | None (docs only) |
| Update 96 C3 model docs Section 4 | `Docs/C3/Models/*/*.md` | Additive: new R3 references |
| Create standards/validation/migration docs | `Docs/R3/Standards/`, `Validation/`, `Migration/` | None (docs only) |

**Rollback**: Delete new docs. No code impact.

### Layer 2: Code Unlock (Phase 6 early -- 6.1 through 6.3)

**Scope**: Update constants, add new groups, enable 128D pipeline.

| Action | Files Affected | Impact |
|--------|---------------|--------|
| R3_DIM = 128 | `mi_beta/core/constants.py` | All code importing R3_DIM |
| Feature names expansion | `mi_beta/core/dimension_map.py` | DimensionMap validation |
| Index validation update | `mi_beta/contracts/feature_spec.py` | Feature spec accepts [0:127] |
| 6 new group classes | `mi_beta/ear/r3/extensions/*.py` (6 files) | New code only |
| Stage-ordered extractor | `mi_beta/ear/r3/__init__.py` | R3Extractor.extract() |

**Rollback**: Revert R3_DIM to 49, remove new group files, revert extractor. First 49D remain intact.

### Layer 3: Formula Revision (Phase 6 late -- 6.4 through 6.5)

**Scope**: Fix bugs and duplications in existing [0:49] features.

| Action | Features Affected | Impact |
|--------|------------------|--------|
| Fix concentration[24] normalization | D[24] | Formula change |
| Fix loudness[10] double compression | B[10] | Formula change |
| Resolve duplications [3]=[12], [16]=1-[1], [17]=[2] | A[3], C[16], C[17] | Formula change |
| E group proxy fix | E[25:49] | Uses real A-D outputs |

**Rollback**: Revert individual formula changes. Index meanings preserved.

---

## 5. Phase-by-Phase File Production

From R3-V2-DESIGN.md Section 8.2:

| Phase | Files Produced/Updated | Count |
|-------|----------------------|:-----:|
| 3B | `Docs/R3/upgrade_beta/R3-V2-DESIGN.md` | 1 |
| 3C | Standards, Validation, Migration docs; model doc Section 4 previews | ~20 |
| 3E | `Docs/C3/Models/*/*.md` Section 4 updates (v2.2.0) | 96 |
| 6.1 | `constants.py`, `dimension_map.py`, `feature_spec.py` | 3 |
| 6.2 | `mi_beta/ear/r3/extensions/{pitch_chroma,rhythm_groove,harmony_tonality,information_surprise,timbre_extended,modulation_psychoacoustic}.py` | 6 |
| 6.3 | `mi_beta/ear/r3/__init__.py`, `_registry.py` | 2 |
| 6.4 | `mi_beta/ear/r3/{psychoacoustic,dsp,cross_domain}/*.py` | 5 |
| 6.5 | `mi_beta/ear/r3/cross_domain/interactions.py` | 1 |
| 6.6 | `tests/ear/r3/test_benchmark_*.py` | 6 |
| 6.7 | `mi_beta/brain/units/*/models/*.py` | 96 |

---

## 6. Rollback Plan

| Scenario | Rollback Procedure | Data Loss |
|----------|-------------------|:---------:|
| Layer 1 fails (doc errors) | Correct docs; no code impact | None |
| Layer 2 fails (code errors) | `git revert` Phase 6.1-6.3 commits; R3_DIM reverts to 49 | None |
| Layer 3 fails (formula regressions) | Revert individual formula commits; [0:49] returns to v1 behavior | None |
| Benchmark fails (Test 1 critical) | Block Layer 2; apply fallback from BenchmarkPlan.md | None |
| Performance regression | Profile and optimize; or reduce K group to amortized-only | None |

Key guarantee: **No irreversible changes at any layer.** Every migration step can be rolled back to the previous stable state.

---

## 7. Dependency Graph

```
Phase 3C docs ──────────┐
                        │
Phase 3E model docs ────┤
                        │
Phase 6.1 constants ────┤── 6.2 new groups ── 6.3 extractor ── 6.6 benchmarks
                        │                                          │
Phase 6.4 formula fixes ┘                    6.5 E redesign ──────┤
                                                                   │
                                                          6.7 integration
```

Phase 3C and 3E can run in parallel. Phase 6 sub-steps are sequential with the exception that 6.1 and 6.4 can prepare in parallel.

---

*Source: R3-V2-DESIGN.md Sections 5, 8; R3-CROSSREF.md Section 7.3*
