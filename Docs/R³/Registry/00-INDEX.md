# R3 Registry -- Index

**Version**: 2.0.0
**Purpose**: Definitive reference for all 128 R3 feature dimensions
**Updated**: 2026-02-13

---

## Overview

The Registry directory contains the canonical reference documents for the R3 feature vector. These documents define the complete mapping between feature indices, names, groups, and domains.

---

## Documents

| Document | Purpose | Key Content |
|----------|---------|-------------|
| [FeatureCatalog.md](FeatureCatalog.md) | Complete 128-feature catalog | Index, name, group, domain, psychoacoustic basis, quality tier, status |
| [DimensionMap.md](DimensionMap.md) | Dimension mapping tables | Index-to-name-to-group, group boundaries, domain boundaries, backward compatibility |
| [NamingConventions.md](NamingConventions.md) | Naming rules and standards | Feature names, group names, domain names, canonical name resolution, reserved prefixes |

---

## Quick Reference

### Group Boundaries

| Group | Name | Range | Dim | Domain |
|-------|------|-------|:---:|--------|
| A | Consonance | [0:7] | 7 | Psychoacoustic |
| B | Energy | [7:12] | 5 | Spectral |
| C | Timbre | [12:21] | 9 | Spectral |
| D | Change | [21:25] | 4 | Temporal |
| E | Interactions | [25:49] | 24 | CrossDomain |
| F | Pitch & Chroma | [49:65] | 16 | Tonal |
| G | Rhythm & Groove | [65:75] | 10 | Temporal |
| H | Harmony & Tonality | [75:87] | 12 | Tonal |
| I | Information & Surprise | [87:94] | 7 | Information |
| J | Timbre Extended | [94:114] | 20 | Spectral |
| K | Modulation & Psychoacoustic | [114:128] | 14 | Psychoacoustic |
| | **Total** | **[0:128]** | **128** | |

### Domain Boundaries

| Domain | Groups | Range(s) | Total Dim |
|--------|--------|----------|:---------:|
| Psychoacoustic | A, K | [0:7], [114:128] | 21 |
| Spectral | B, C, J | [7:12], [12:21], [94:114] | 34 |
| Tonal | F, H | [49:65], [75:87] | 28 |
| Temporal | D, G | [21:25], [65:75] | 14 |
| Information | I | [87:94] | 7 |
| CrossDomain | E | [25:49] | 24 |
| **Total** | **11 groups** | **[0:128]** | **128** |

---

## Code Correspondence

| Registry Document | Code File | Relationship |
|-------------------|-----------|-------------|
| FeatureCatalog.md | `mi_beta/ear/r3/_registry.py` | Registry assigns names/indices |
| DimensionMap.md | `mi_beta/core/dimension_map.py` | Feature name lookup |
| NamingConventions.md | `mi_beta/contracts/base_spectral_group.py` | Naming enforced by contract |

---

## Usage Notes

- All feature indices in this directory are **authoritative**. If a discrepancy exists between these documents and code, file a bug.
- Feature indices [0:49] are preserved from R3 v1. See [DimensionMap.md](DimensionMap.md) for backward compatibility details.
- The canonical feature name for any index is determined by the `R3FeatureRegistry` at runtime via `freeze()`. These documents reflect the expected output of that process.
