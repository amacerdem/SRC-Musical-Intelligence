# R3 Spectral Architecture -- Master Index

**Version**: 2.0.0
**Dimensions**: 128D (11 groups, 6 domains)
**Status**: Active -- Phase 3B architecture design complete
**Updated**: 2026-02-13

---

## Overview

R3 (Representation Layer 3) is the spectral feature extraction subsystem of the MI (Musical Intelligence) pipeline. It transforms mel spectrograms into a dense 128-dimensional feature vector per frame, capturing psychoacoustic, spectral, tonal, temporal, informational, and cross-domain properties of the audio signal.

**Pipeline position**: Audio --> Cochlea (128-mel) --> **R3 (128D)** --> Brain (C3 models)

**Input**: mel spectrogram `(B, 128, T)` at 172.27 Hz frame rate
**Output**: feature tensor `(B, T, 128)` with values in `[0, 1]`

---

## Architecture Summary

| Group | Name | Range | Dim | Domain | Status | Stage |
|-------|------|-------|-----|--------|--------|-------|
| A | Consonance | [0:7] | 7D | Psychoacoustic | Existing | 1 |
| B | Energy | [7:12] | 5D | Spectral | Existing | 1 |
| C | Timbre | [12:21] | 9D | Spectral | Existing | 1 |
| D | Change | [21:25] | 4D | Temporal | Existing | 1 |
| E | Interactions | [25:49] | 24D | CrossDomain | Existing | 2 |
| **F** | **Pitch & Chroma** | **[49:65]** | **16D** | **Tonal** | **New (v2)** | 1 |
| **G** | **Rhythm & Groove** | **[65:75]** | **10D** | **Temporal** | **New (v2)** | 2 |
| **H** | **Harmony & Tonality** | **[75:87]** | **12D** | **Tonal** | **New (v2)** | 2 |
| **I** | **Information & Surprise** | **[87:94]** | **7D** | **Information** | **New (v2)** | 3 |
| **J** | **Timbre Extended** | **[94:114]** | **20D** | **Spectral** | **New (v2)** | 1 |
| **K** | **Modulation & Psychoacoustic** | **[114:128]** | **14D** | **Psychoacoustic** | **New (v2)** | 1 |
| | **Total** | **[0:128]** | **128D** | | | |

---

## Directory Structure

```
Docs/R3/
|-- 00-INDEX.md                          <-- You are here
|-- R3-SPECTRAL-ARCHITECTURE.md          Master architecture document
|-- CHANGELOG.md                         Version history (v1.0 -> v2.0)
|-- EXTENSION-GUIDE.md                   Developer guide for extending R3
|
|-- Registry/
|   |-- 00-INDEX.md                      Registry directory index
|   |-- FeatureCatalog.md                Complete 128-feature catalog
|   |-- DimensionMap.md                  Index-to-feature mapping
|   |-- NamingConventions.md             Naming rules and conventions
|
|-- Domains/
|   |-- Psychoacoustic/                  Groups A, K
|   |-- Spectral/                        Groups B, C, J
|   |-- Tonal/                           Groups F, H
|   |-- Temporal/                        Groups D, G
|   |-- Information/                     Group I
|   |-- CrossDomain/                     Group E
|
|-- Contracts/                           BaseSpectralGroup interface spec
|-- Pipeline/                            Dependency DAG and stage docs
|-- Standards/                           Normalization, output contracts
|-- Validation/                          Test coverage and benchmarks
|-- Literature/                          Psychoacoustic references
|-- Migration/                           v1 -> v2 migration guides
|
|-- upgrade_beta/                        Design phase working documents
    |-- R3-V2-DESIGN.md                  Definitive v2 architecture design
    |-- R3-CROSSREF.md                   Three-perspective synthesis (R1+R2+R3)
    |-- R3-DEMAND-MATRIX.md              Bottom-up gap analysis (R1)
    |-- R3-DSP-SURVEY-THEORY.md          Literature survey (R2)
    |-- R3-DSP-SURVEY-TOOLS.md           Toolkit survey (R3)
    |-- ...
```

---

## Key Documents

| Document | Purpose | Location |
|----------|---------|----------|
| Spectral Architecture | Master architecture, pipeline, dimension inventory | [R3-SPECTRAL-ARCHITECTURE.md](R3-SPECTRAL-ARCHITECTURE.md) |
| Feature Catalog | All 128 features with metadata | [Registry/FeatureCatalog.md](Registry/FeatureCatalog.md) |
| Dimension Map | Index-to-name-to-group mapping | [Registry/DimensionMap.md](Registry/DimensionMap.md) |
| Naming Conventions | Feature/group/domain naming rules | [Registry/NamingConventions.md](Registry/NamingConventions.md) |
| Extension Guide | How to add new groups/features | [EXTENSION-GUIDE.md](EXTENSION-GUIDE.md) |
| Changelog | Version history | [CHANGELOG.md](CHANGELOG.md) |
| V2 Design (source) | Definitive design decisions | [upgrade_beta/R3-V2-DESIGN.md](upgrade_beta/R3-V2-DESIGN.md) |
| Crossref (source) | Three-perspective synthesis | [upgrade_beta/R3-CROSSREF.md](upgrade_beta/R3-CROSSREF.md) |

---

## Code Mapping

| Documentation | Code |
|--------------|------|
| This index | `mi_beta/ear/r3/__init__.py` -- R3Extractor |
| Registry docs | `mi_beta/ear/r3/_registry.py` -- R3FeatureRegistry |
| BaseSpectralGroup contract | `mi_beta/contracts/base_spectral_group.py` |
| Extension template | `mi_beta/ear/r3/extensions/_template.py` |
| Constants | `mi_beta/core/constants.py` -- R3_DIM, group ranges |
| Dimension map | `mi_beta/core/dimension_map.py` -- feature names |

---

## Domain Distribution

| Domain | Groups | Total Dim | Coverage |
|--------|--------|-----------|----------|
| Psychoacoustic | A (7D), K (14D) | 21D | Consonance, roughness, sharpness, modulation |
| Spectral | B (5D), C (9D), J (20D) | 34D | Energy, timbre, MFCC, spectral contrast |
| Tonal | F (16D), H (12D) | 28D | Chroma, pitch, key, tonnetz, harmony |
| Temporal | D (4D), G (10D) | 14D | Spectral change, rhythm, groove, tempo |
| Information | I (7D) | 7D | Entropy, surprise, prediction error |
| CrossDomain | E (24D) | 24D | Cross-group interaction products |
| **Total** | **11 groups** | **128D** | |

---

## Version History

| Version | Date | Dimensions | Groups | Notes |
|---------|------|-----------|--------|-------|
| 1.0.0 | 2024 | 49D | A-E (5) | Original 5-group architecture |
| **2.0.0** | **2025** | **128D** | **A-K (11)** | **Expansion: +6 groups, +79 dimensions** |

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
