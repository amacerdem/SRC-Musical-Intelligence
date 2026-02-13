# R3 Dimension Map

**Version**: 2.0.0
**Source**: R3-V2-DESIGN.md Section 2, R3-CROSSREF.md Section 4
**Updated**: 2026-02-13

---

## Table of Contents

1. [Complete Index-to-Feature Mapping](#1-complete-index-to-feature-mapping)
2. [Group Boundary Table](#2-group-boundary-table)
3. [Domain Boundary Table](#3-domain-boundary-table)
4. [Backward Compatibility Notes](#4-backward-compatibility-notes)

---

## 1. Complete Index-to-Feature Mapping

### Index 0-24: Groups A-D (Existing)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 0 | roughness | A | Psychoacoustic | [0, 1] |
| 1 | sethares_dissonance | A | Psychoacoustic | [0, 1] |
| 2 | helmholtz_kang | A | Psychoacoustic | [0, 1] |
| 3 | stumpf_fusion | A | Psychoacoustic | [0, 1] |
| 4 | sensory_pleasantness | A | Psychoacoustic | [0, 1] |
| 5 | inharmonicity | A | Psychoacoustic | [0, 1] |
| 6 | harmonic_deviation | A | Psychoacoustic | [0, 1] |
| 7 | amplitude | B | Spectral | [0, 1] |
| 8 | velocity_A | B | Spectral | [0, 1] |
| 9 | acceleration_A | B | Spectral | [0, 1] |
| 10 | loudness | B | Spectral | [0, 1] |
| 11 | onset_strength | B | Spectral | [0, 1] |
| 12 | warmth | C | Spectral | [0, 1] |
| 13 | sharpness | C | Spectral | [0, 1] |
| 14 | tonalness | C | Spectral | [0, 1] |
| 15 | clarity | C | Spectral | [0, 1] |
| 16 | spectral_smoothness | C | Spectral | [0, 1] |
| 17 | spectral_autocorrelation | C | Spectral | [0, 1] |
| 18 | tristimulus1 | C | Spectral | [0, 1] |
| 19 | tristimulus2 | C | Spectral | [0, 1] |
| 20 | tristimulus3 | C | Spectral | [0, 1] |
| 21 | spectral_flux | D | Temporal | [0, 1] |
| 22 | distribution_entropy | D | Temporal | [0, 1] |
| 23 | distribution_flatness | D | Temporal | [0, 1] |
| 24 | distribution_concentration | D | Temporal | [0, 1] |

### Index 25-48: Group E (Existing)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 25 | x_l0l5_0 | E | CrossDomain | [0, 1] |
| 26 | x_l0l5_1 | E | CrossDomain | [0, 1] |
| 27 | x_l0l5_2 | E | CrossDomain | [0, 1] |
| 28 | x_l0l5_3 | E | CrossDomain | [0, 1] |
| 29 | x_l0l5_4 | E | CrossDomain | [0, 1] |
| 30 | x_l0l5_5 | E | CrossDomain | [0, 1] |
| 31 | x_l0l5_6 | E | CrossDomain | [0, 1] |
| 32 | x_l0l5_7 | E | CrossDomain | [0, 1] |
| 33 | x_l4l5_0 | E | CrossDomain | [0, 1] |
| 34 | x_l4l5_1 | E | CrossDomain | [0, 1] |
| 35 | x_l4l5_2 | E | CrossDomain | [0, 1] |
| 36 | x_l4l5_3 | E | CrossDomain | [0, 1] |
| 37 | x_l4l5_4 | E | CrossDomain | [0, 1] |
| 38 | x_l4l5_5 | E | CrossDomain | [0, 1] |
| 39 | x_l4l5_6 | E | CrossDomain | [0, 1] |
| 40 | x_l4l5_7 | E | CrossDomain | [0, 1] |
| 41 | x_l5l7_0 | E | CrossDomain | [0, 1] |
| 42 | x_l5l7_1 | E | CrossDomain | [0, 1] |
| 43 | x_l5l7_2 | E | CrossDomain | [0, 1] |
| 44 | x_l5l7_3 | E | CrossDomain | [0, 1] |
| 45 | x_l5l7_4 | E | CrossDomain | [0, 1] |
| 46 | x_l5l7_5 | E | CrossDomain | [0, 1] |
| 47 | x_l5l7_6 | E | CrossDomain | [0, 1] |
| 48 | x_l5l7_7 | E | CrossDomain | [0, 1] |

### Index 49-64: Group F (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 49 | chroma_C | F | Tonal | [0, 1] |
| 50 | chroma_Db | F | Tonal | [0, 1] |
| 51 | chroma_D | F | Tonal | [0, 1] |
| 52 | chroma_Eb | F | Tonal | [0, 1] |
| 53 | chroma_E | F | Tonal | [0, 1] |
| 54 | chroma_F | F | Tonal | [0, 1] |
| 55 | chroma_Gb | F | Tonal | [0, 1] |
| 56 | chroma_G | F | Tonal | [0, 1] |
| 57 | chroma_Ab | F | Tonal | [0, 1] |
| 58 | chroma_A | F | Tonal | [0, 1] |
| 59 | chroma_Bb | F | Tonal | [0, 1] |
| 60 | chroma_B | F | Tonal | [0, 1] |
| 61 | pitch_height | F | Tonal | [0, 1] |
| 62 | pitch_class_entropy | F | Tonal | [0, 1] |
| 63 | pitch_salience | F | Tonal | [0, 1] |
| 64 | inharmonicity_index | F | Tonal | [0, 1] |

### Index 65-74: Group G (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 65 | tempo_estimate | G | Temporal | [0, 1] |
| 66 | beat_strength | G | Temporal | [0, 1] |
| 67 | pulse_clarity | G | Temporal | [0, 1] |
| 68 | syncopation_index | G | Temporal | [0, 1] |
| 69 | metricality_index | G | Temporal | [0, 1] |
| 70 | isochrony_nPVI | G | Temporal | [0, 1] |
| 71 | groove_index | G | Temporal | [0, 1] |
| 72 | event_density | G | Temporal | [0, 1] |
| 73 | tempo_stability | G | Temporal | [0, 1] |
| 74 | rhythmic_regularity | G | Temporal | [0, 1] |

### Index 75-86: Group H (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 75 | key_clarity | H | Tonal | [0, 1] |
| 76 | tonnetz_fifth_x | H | Tonal | [0, 1] |
| 77 | tonnetz_fifth_y | H | Tonal | [0, 1] |
| 78 | tonnetz_minor_x | H | Tonal | [0, 1] |
| 79 | tonnetz_minor_y | H | Tonal | [0, 1] |
| 80 | tonnetz_major_x | H | Tonal | [0, 1] |
| 81 | tonnetz_major_y | H | Tonal | [0, 1] |
| 82 | voice_leading_distance | H | Tonal | [0, 1] |
| 83 | harmonic_change | H | Tonal | [0, 1] |
| 84 | tonal_stability | H | Tonal | [0, 1] |
| 85 | diatonicity | H | Tonal | [0, 1] |
| 86 | syntactic_irregularity | H | Tonal | [0, 1] |

### Index 87-93: Group I (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 87 | melodic_entropy | I | Information | [0, 1] |
| 88 | harmonic_entropy | I | Information | [0, 1] |
| 89 | rhythmic_information_content | I | Information | [0, 1] |
| 90 | spectral_surprise | I | Information | [0, 1] |
| 91 | information_rate | I | Information | [0, 1] |
| 92 | predictive_entropy | I | Information | [0, 1] |
| 93 | tonal_ambiguity | I | Information | [0, 1] |

### Index 94-113: Group J (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 94 | mfcc_1 | J | Spectral | [0, 1] |
| 95 | mfcc_2 | J | Spectral | [0, 1] |
| 96 | mfcc_3 | J | Spectral | [0, 1] |
| 97 | mfcc_4 | J | Spectral | [0, 1] |
| 98 | mfcc_5 | J | Spectral | [0, 1] |
| 99 | mfcc_6 | J | Spectral | [0, 1] |
| 100 | mfcc_7 | J | Spectral | [0, 1] |
| 101 | mfcc_8 | J | Spectral | [0, 1] |
| 102 | mfcc_9 | J | Spectral | [0, 1] |
| 103 | mfcc_10 | J | Spectral | [0, 1] |
| 104 | mfcc_11 | J | Spectral | [0, 1] |
| 105 | mfcc_12 | J | Spectral | [0, 1] |
| 106 | mfcc_13 | J | Spectral | [0, 1] |
| 107 | spectral_contrast_1 | J | Spectral | [0, 1] |
| 108 | spectral_contrast_2 | J | Spectral | [0, 1] |
| 109 | spectral_contrast_3 | J | Spectral | [0, 1] |
| 110 | spectral_contrast_4 | J | Spectral | [0, 1] |
| 111 | spectral_contrast_5 | J | Spectral | [0, 1] |
| 112 | spectral_contrast_6 | J | Spectral | [0, 1] |
| 113 | spectral_contrast_7 | J | Spectral | [0, 1] |

### Index 114-127: Group K (New)

| Index | Feature Name | Group | Domain | Range |
|:-----:|-------------|:-----:|--------|:-----:|
| 114 | modulation_0_5Hz | K | Psychoacoustic | [0, 1] |
| 115 | modulation_1Hz | K | Psychoacoustic | [0, 1] |
| 116 | modulation_2Hz | K | Psychoacoustic | [0, 1] |
| 117 | modulation_4Hz | K | Psychoacoustic | [0, 1] |
| 118 | modulation_8Hz | K | Psychoacoustic | [0, 1] |
| 119 | modulation_16Hz | K | Psychoacoustic | [0, 1] |
| 120 | modulation_centroid | K | Psychoacoustic | [0, 1] |
| 121 | modulation_bandwidth | K | Psychoacoustic | [0, 1] |
| 122 | sharpness_zwicker | K | Psychoacoustic | [0, 1] |
| 123 | fluctuation_strength | K | Psychoacoustic | [0, 1] |
| 124 | loudness_a_weighted | K | Psychoacoustic | [0, 1] |
| 125 | alpha_ratio | K | Psychoacoustic | [0, 1] |
| 126 | hammarberg_index | K | Psychoacoustic | [0, 1] |
| 127 | spectral_slope_0_500 | K | Psychoacoustic | [0, 1] |

---

## 2. Group Boundary Table

| Group | Letter | Full Name | Start | End | Dim | Slice Notation | Pipeline Stage |
|:-----:|:------:|-----------|:-----:|:---:|:---:|:--------------:|:--------------:|
| A | A | Consonance | 0 | 7 | 7 | `[0:7]` | 1 |
| B | B | Energy | 7 | 12 | 5 | `[7:12]` | 1 |
| C | C | Timbre | 12 | 21 | 9 | `[12:21]` | 1 |
| D | D | Change | 21 | 25 | 4 | `[21:25]` | 1 |
| E | E | Interactions | 25 | 49 | 24 | `[25:49]` | 2 |
| F | F | Pitch & Chroma | 49 | 65 | 16 | `[49:65]` | 1 |
| G | G | Rhythm & Groove | 65 | 75 | 10 | `[65:75]` | 2 |
| H | H | Harmony & Tonality | 75 | 87 | 12 | `[75:87]` | 2 |
| I | I | Information & Surprise | 87 | 94 | 7 | `[87:94]` | 3 |
| J | J | Timbre Extended | 94 | 114 | 20 | `[94:114]` | 1 |
| K | K | Modulation & Psychoacoustic | 114 | 128 | 14 | `[114:128]` | 1 |

**Properties**:
- All groups are contiguous: no gaps between group boundaries
- No overlap: each index belongs to exactly one group
- Total: 7 + 5 + 9 + 4 + 24 + 16 + 10 + 12 + 7 + 20 + 14 = 128

### Python Slice Access

```python
# Constants (mi_beta/core/constants.py):
R3_CONSONANCE           = (0, 7)
R3_ENERGY               = (7, 12)
R3_TIMBRE               = (12, 21)
R3_CHANGE               = (21, 25)
R3_INTERACTIONS         = (25, 49)
R3_PITCH_CHROMA         = (49, 65)
R3_RHYTHM_GROOVE        = (65, 75)
R3_HARMONY_TONALITY     = (75, 87)
R3_INFORMATION_SURPRISE = (87, 94)
R3_TIMBRE_EXTENDED      = (94, 114)
R3_MODULATION_PSYCHO    = (114, 128)

# Usage:
r3_features = extractor.extract(mel).features  # (B, T, 128)
chroma = r3_features[:, :, 49:65]              # Group F (16D)
rhythm = r3_features[:, :, 65:75]              # Group G (10D)
```

---

## 3. Domain Boundary Table

| Domain | Groups | Index Ranges | Total Dim | Contiguous? |
|--------|--------|-------------|:---------:|:-----------:|
| Psychoacoustic | A, K | [0:7], [114:128] | 21 | No (split) |
| Spectral | B, C, J | [7:12], [12:21], [94:114] | 34 | No (split) |
| Tonal | F, H | [49:65], [75:87] | 28 | No (split) |
| Temporal | D, G | [21:25], [65:75] | 14 | No (split) |
| Information | I | [87:94] | 7 | Yes |
| CrossDomain | E | [25:49] | 24 | Yes |

**Note**: Domains are not contiguous in the index space because backward compatibility requires preserving the original group order (A-E at [0:49]). The new groups (F-K) are appended sequentially. Domain-based access should use the group constants, not contiguous slices.

### Domain Access Pattern

```python
# To access all Tonal features (F + H = 28D):
tonal = torch.cat([
    r3_features[:, :, 49:65],   # Group F: Pitch & Chroma (16D)
    r3_features[:, :, 75:87],   # Group H: Harmony & Tonality (12D)
], dim=-1)  # (B, T, 28)

# To access all Spectral features (B + C + J = 34D):
spectral = torch.cat([
    r3_features[:, :, 7:12],    # Group B: Energy (5D)
    r3_features[:, :, 12:21],   # Group C: Timbre (9D)
    r3_features[:, :, 94:114],  # Group J: Timbre Extended (20D)
], dim=-1)  # (B, T, 34)
```

---

## 4. Backward Compatibility Notes

### 4.1 Index Preservation

The first 49 dimensions ([0:49]) are fully preserved from R3 v1:

| Range | Group | v1 Status | v2 Status | Change |
|-------|-------|-----------|-----------|--------|
| [0:7] | A: Consonance | Present | Preserved | None (formulas unchanged) |
| [7:12] | B: Energy | Present | Preserved | None (formulas unchanged) |
| [12:21] | C: Timbre | Present | Preserved | None (formulas unchanged) |
| [21:25] | D: Change | Present | Preserved | None (formulas unchanged) |
| [25:49] | E: Interactions | Present | Preserved | None (formulas unchanged) |
| [49:128] | F-K | Not present | New | Appended (79 new dimensions) |

**Guarantee**: Any code or documentation referencing indices [0:48] continues to be valid in v2. The R3 v2 output tensor is a strict superset of the v1 output: `v2_output[:, :, :49] == v1_output`.

### 4.2 Three-Layer Compatibility Strategy

The backward compatibility strategy operates in three layers across project phases:

| Layer | Phase | Change Scope | Impact |
|:-----:|:-----:|-------------|--------|
| 1 | 3B (current) | Indices [0:49] unchanged, [49:128] appended | C3 model docs remain valid |
| 2 | 6 | Formulas at [0:49] revised (bug fixes, dedup) | Code needs updating |
| 3 | 6+ | `R3_DIM=128`, registry-based names, E expansion | Full refactor |

### 4.3 Layer 1 Details (Current -- Phase 3B)

**What does not change**:
- Feature indices [0:48]
- Feature names for indices [0:48]
- Computation formulas for indices [0:48]
- Group boundaries for A-E
- Output range [0, 1] contract

**What is added**:
- 79 new features at indices [49:127]
- 6 new groups (F-K)
- New dependency DAG (3-stage execution)
- New auto-discovery mechanism for extensions

### 4.4 Layer 2 Details (Planned -- Phase 6)

**Formulas that will change** (same indices, different computations):

| Index | Feature | Current Formula | Planned Formula |
|:-----:|---------|----------------|-----------------|
| 0 | roughness | `sigmoid(var/mean)` | Real Plomp-Levelt critical band roughness |
| 1 | sethares_dissonance | `mean(abs(diff))` | Real Sethares pairwise `d(fi,fj,ai,aj)` |
| 3 | stumpf_fusion | `mel[:N/4].sum()/total` | Parncutt subharmonic matching |
| 10 | loudness | `(RMS_logmel)^0.3` | `exp(logmel).pow(0.3)` or Zwicker ISO 532-1 |
| 16 | spectral_smoothness | `1 - sethares[1]` | spectral_spread (2nd central moment) |
| 17 | spectral_autocorrelation | `lag-1 autocorr` (dup of [2]) | spectral_kurtosis (4th central moment) |
| 24 | distribution_concentration | `HHI * N` (buggy) | `(HHI - 1/N) / (1 - 1/N)` |
| 25-48 | E group interactions | Proxy-based products | Real A-D output products |

### 4.5 Layer 3 Details (Planned -- Phase 6+)

**Code-level changes**:

| File | Current | Target |
|------|---------|--------|
| `constants.py` | `R3_DIM = 49` | `R3_DIM = 128` |
| `dimension_map.py` | Hardcoded 49-element tuple | Registry-based `get_r3_feature_names()` |
| `feature_spec.py` | `assert index < 49` | `assert index < R3_DIM` |
| `base_spectral_group.py` | "49-D" in docstrings | Dynamic dimensionality |
| `__init__.py` (R3) | Order-independent concat | Stage-ordered extraction |
| `_registry.py` | No validation | `assert total_dim == R3_DIM` |

### 4.6 C3 Model Documentation Impact

96 C3 model documentation files reference R3 feature indices in their Section 4. The compatibility strategy ensures:

- **Phase 3B (now)**: No documentation changes needed for existing references. New features can be optionally referenced.
- **Phase 6**: Section 12.1 "doc-code mismatch" notes added where formulas change. Feature names at changed indices updated.
- **Phase 6+**: Section 4 rewritten to use registry-based names instead of hardcoded indices.
