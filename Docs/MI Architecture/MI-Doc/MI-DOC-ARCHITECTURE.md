# MI Documentation Architecture

**Version**: 2.0.0
**Date**: 2026-02-13
**Total Files**: 395 markdown documents
**Validated**: Phase 6 complete, 0 remaining DOC-BUGs

---

## 1. Overview

MI (Musical Intelligence) documentation is organized as a 4-layer neural-computational architecture that mirrors the `mi_beta/` codebase. Each layer has its own documentation tree with standardized subdirectory patterns.

```
Audio Signal
    |
    v
 ┌──────────────────────────────────────────────────────┐
 │  R³ — Spectral Space (128D)                          │  Docs/R³/  (71 files)
 │  "What is the sound?"                                │
 │  11 feature groups (A-K), per-frame extraction        │
 └──────────────┬───────────────────────────────────────┘
                |
                v
 ┌──────────────────────────────────────────────────────┐
 │  H³ — Temporal Demand (294,912D address space)       │  Docs/H³/  (73 files)
 │  "How does it change over time?"                     │
 │  32 horizons × 24 morphs × 3 laws × 128 features    │
 └──────────────┬───────────────────────────────────────┘
                |
                v
 ┌──────────────────────────────────────────────────────┐
 │  C³ — Brain Models (96 models, 1026D output)         │  Docs/C³/  (162 files)
 │  "How does the brain process it?"                    │
 │  9 units, 10 mechanisms, 6 circuits, 5 pathways      │
 └──────────────┬───────────────────────────────────────┘
                |
                v
 ┌──────────────────────────────────────────────────────┐
 │  L³ — Semantic Space (104D)                          │  Docs/L³/  (73 files)
 │  "What does it mean?"                                │
 │  8 groups (α-θ), 12 axes, 96 vocabulary terms        │
 └──────────────────────────────────────────────────────┘
                |
                v
           MI-space output
```

**Supporting documentation:**

| Directory | Files | Purpose |
|-----------|:-----:|---------|
| `Docs/Beta/` | 15 | Upgrade plan, progress tracking, validation deliverables |
| `Docs/MI Architecture/` | — | This architecture document |
| **Total** | **395** | |

---

## 2. File Count Summary

| Layer | Root | Models | Infra | Registry | Pipeline | Contracts | Standards | Validation | Literature | Migration | Other | **Total** |
|:-----:|:----:|:------:|:-----:|:--------:|:--------:|:---------:|:---------:|:----------:|:----------:|:---------:|:-----:|:-------:|
| **C³** | 2 | 97 | 43 | — | — | 9 | — | — | — | — | 11 | **162** |
| **R³** | 4 | — | — | 4 | 5 | 6 | 3 | 3 | 2 | 3 | 41 | **71** |
| **H³** | 4 | — | — | 5 | 5 | 6 | 3 | 3 | 2 | 3 | 42 | **73** |
| **L³** | 8 | — | — | 4 | 5 | 6 | 3 | 3 | 2 | 3 | 39 | **73** |
| **Beta** | 15 | — | — | — | — | — | — | — | — | — | — | **15** |
| | | | | | | | | | | | | **394** |

Note: +1 for this architecture document = 395 total.

---

## 3. Standardized Subdirectory Pattern

All architectural layers (R³, H³, L³) share a common subdirectory structure:

```
{Layer}/
├── 00-INDEX.md              ← Master index (every dir has one)
├── {Layer}-ARCHITECTURE.md  ← Definitive architecture document
├── CHANGELOG.md             ← Version history
├── EXTENSION-GUIDE.md       ← How to add new components
│
├── Registry/                ← Catalogs, dimension maps, naming
│   ├── 00-INDEX.md
│   └── *.md
│
├── Contracts/               ← Interface specifications (ABCs)
│   ├── 00-INDEX.md
│   └── *.md
│
├── Pipeline/                ← Execution model, dependencies, performance
│   ├── 00-INDEX.md
│   └── *.md
│
├── Standards/               ← Quality tiers, compliance rules
│   ├── 00-INDEX.md
│   └── *.md
│
├── Validation/              ← Benchmark plans, acceptance criteria
│   ├── 00-INDEX.md
│   └── *.md
│
├── Literature/              ← Academic references
│   ├── 00-INDEX.md
│   └── *.md
│
├── Migration/               ← Version migration guides
│   ├── 00-INDEX.md
│   └── *.md
│
└── {Layer-specific}/        ← Domain-specific subdirectories
```

C³ deviates from this pattern because it predates the standardization — it has its own infrastructure hierarchy (Units, Models, Mechanisms, etc.) instead of the shared pattern.

---

## 4. Index Convention

Every directory containing documentation files has a `00-INDEX.md` file that:
1. Lists all files in that directory with brief descriptions
2. Provides a summary table with metadata (counts, versions, status)
3. Cross-references related directories in other layers

**Current index count**: 58 total (55 pre-existing + 3 created in Phase 6)

| Layer | Index Files |
|:-----:|:-----------:|
| C³ | 11 (root + Units + Models + Mechanisms + Pathways + Regions + Neurochemicals + Circuits + Contracts + Tiers + Matrices) |
| R³ | 13 (root + Registry + 6 Domains + Contracts + Pipeline + Standards + Mappings + Validation + Literature + Migration) |
| H³ | 15 (root + Registry + Bands + 4 sub-bands + Morphology + Laws + Contracts + Pipeline + Demand + Expansion + Standards + Validation + Literature + Migration) |
| L³ | 13 (root + Registry + Groups + 2 sub-groups + Vocabulary + Contracts + Pipeline + Adapters + Standards + Validation + Literature + Migration + Archive + Epistemology) |
| Beta | 0 (working docs, no index) |

---

## 5. Version Alignment

| Component | Doc Version | Code Version | Status |
|-----------|:-----------:|:------------:|--------|
| C³ Models | v2.2.0 | v2.0.0 | Docs ahead (Phase 1 upgrades) |
| R³ Architecture | v2.0.0 | v1.0.0 (49D) | Docs ahead (128D expansion) |
| H³ Architecture | v2.0.0 | v1.0.0 (2304D) | Docs ahead (294,912D expansion) |
| L³ Architecture | v2.1.0 | v1.0.0 | Docs ahead (full redesign) |

All discrepancies are cataloged in `Docs/Beta/DISCREPANCY-REGISTRY.md`.

---

## 6. Cross-Layer References

Documentation maintains explicit cross-references between layers:

| From → To | Reference Type | Example |
|-----------|---------------|---------|
| C³ Model → R³ | Section 4: r3 indices | `r3_indices: [0, 1, 5, 7, 12]` |
| C³ Model → H³ | Section 5: h3 demand tuples | `(r3_idx=0, horizon=6, morph=0, law=0)` |
| C³ Unit → L³ | Adapter docs | `Docs/L³/Adapters/SPU-L3-ADAPTER.md` |
| R³ → H³ | Expansion impact | `Docs/H³/Expansion/F-PitchChroma-Temporal.md` |
| R³ → C³ | Per-unit mappings | `Docs/R³/Mappings/SPU-R3-MAP.md` |
| H³ → C³ | Per-unit demands | `Docs/H³/Demand/SPU-H3-DEMAND.md` |
| L³ → C³ | Per-unit adapters | `Docs/L³/Adapters/SPU-L3-ADAPTER.md` |

---

## 7. Naming Conventions

### Model Directory Pattern
```
{UNIT}-{tier}{n}-{ACRONYM}/
  └── {ACRONYM}.md
```
- **UNIT**: 3-letter unit code (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU)
- **tier**: Greek letter (α = alpha, β = beta, γ = gamma)
- **n**: Sequential number within tier (1-based)
- **ACRONYM**: Model acronym (uppercase, 2-6 chars)

Example: `PCU-β4-CHPI/CHPI.md`

### Per-Unit File Pattern
```
{UNIT}-{LAYER}-{TYPE}.md
```
Examples: `SPU-R3-MAP.md`, `SPU-H3-DEMAND.md`, `SPU-L3-ADAPTER.md`

---

---

# PART II — R³ Documentation Architecture

**Version**: 2.0.0
**Date**: 2026-02-13
**Total Files**: 71 markdown documents
**Layer**: R³ — Spectral Space ("What is the sound?")

---

## 8. R³ Overview

R³ is the spectral feature extraction layer of MI. It transforms raw audio into a 128-dimensional per-frame feature vector organized into 11 perceptual groups (A-K) across 6 psychoacoustic domains.

**Pipeline position:**

```
Audio → Cochlea → [R³ 128D spectral] → H³ → Brain → L³ → MI-space
```

**Key metrics:**
- **Dimensions**: 128D per frame (49D v1 existing + 79D v2 expansion)
- **Frame rate**: 172.27 Hz (hop_length=256 @ sr=44100)
- **Output range**: [0, 1] normalized
- **Real-time budget**: 2.5 ms amortized per frame (2.3× headroom)

---

## 9. R³ Directory Tree

```
Docs/R³/                                    (71 files total)
├── 00-INDEX.md                              Root index
├── R3-SPECTRAL-ARCHITECTURE.md              Definitive architecture document
├── CHANGELOG.md                             Version history
├── EXTENSION-GUIDE.md                       How to add new groups
│
├── Registry/                                (4 files)
│   ├── 00-INDEX.md
│   ├── FeatureCatalog.md                    All 128 features with metadata
│   ├── DimensionMap.md                      Index→name→group mapping
│   └── NamingConventions.md                 Feature/group/domain naming rules
│
├── Domains/                                 (17 files across 6 subdirectories)
│   ├── 00-INDEX.md                          Domain-level organization
│   │
│   ├── Psychoacoustic/                      (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── A-Consonance.md                  Group A [0:7] 7D
│   │   └── K-ModulationPerception.md        Group K [114:128] 14D
│   │
│   ├── Spectral/                            (4 files)
│   │   ├── 00-INDEX.md
│   │   ├── C-Timbre.md                      Group C [12:21] 9D
│   │   ├── D-Change.md                      Group D [21:25] 4D
│   │   └── J-TimbreExtended.md              Group J [94:114] 20D
│   │
│   ├── Tonal/                               (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── F-PitchChroma.md                 Group F [49:65] 16D
│   │   └── H-HarmonyTonality.md             Group H [75:87] 12D
│   │
│   ├── Temporal/                            (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── B-Energy.md                      Group B [7:12] 5D
│   │   └── G-RhythmGroove.md                Group G [65:75] 10D
│   │
│   ├── Information/                         (2 files)
│   │   ├── 00-INDEX.md
│   │   └── I-InformationSurprise.md         Group I [87:94] 7D
│   │
│   └── CrossDomain/                         (2 files)
│       ├── 00-INDEX.md
│       └── E-Interactions.md                Group E [25:49] 24D
│
├── Contracts/                               (6 files)
│   ├── 00-INDEX.md
│   ├── BaseSpectralGroup.md                 ABC for spectral groups
│   ├── R3FeatureRegistry.md                 Registry lifecycle
│   ├── R3FeatureSpec.md                     Per-feature dataclass
│   ├── R3Extractor.md                       Orchestrator contract
│   └── ExtensionProtocol.md                 Extension system
│
├── Pipeline/                                (5 files)
│   ├── 00-INDEX.md
│   ├── DependencyDAG.md                     3-stage extraction ordering
│   ├── Normalization.md                     [0,1] normalization contract
│   ├── Performance.md                       Frame-level budget
│   └── StateManagement.md                   Stateful features & warm-up
│
├── Standards/                               (3 files)
│   ├── 00-INDEX.md
│   ├── ComplianceMatrix.md                  ISO/AES/DIN/ITU mapping
│   └── QualityTiers.md                      Proxy/Approximate/Standard/Reference
│
├── Validation/                              (3 files)
│   ├── 00-INDEX.md
│   ├── BenchmarkPlan.md                     6 critical feature benchmarks
│   └── AcceptanceCriteria.md                Per-group quality gates
│
├── Literature/                              (2 files)
│   ├── 00-INDEX.md
│   └── R3-LITERATURE.md                     121 paper references
│
├── Migration/                               (3 files)
│   ├── 00-INDEX.md
│   ├── V1-to-V2.md                          49D→128D migration guide
│   └── BackwardCompatibility.md             Index 0-48 preservation
│
├── Mappings/                                (10 files)
│   ├── 00-INDEX.md
│   ├── SPU-R3-MAP.md
│   ├── STU-R3-MAP.md
│   ├── IMU-R3-MAP.md
│   ├── ASU-R3-MAP.md
│   ├── NDU-R3-MAP.md
│   ├── MPU-R3-MAP.md
│   ├── PCU-R3-MAP.md
│   ├── ARU-R3-MAP.md
│   └── RPU-R3-MAP.md
│
└── upgrade_beta/                            (13 files — design phase working docs)
    ├── R3-V2-DESIGN.md                      Definitive v2 architecture design
    ├── R3-CROSSREF.md                       Three-perspective synthesis
    ├── R3-DEMAND-MATRIX.md                  Bottom-up gap analysis (R1)
    ├── R3-DSP-SURVEY-THEORY.md              Literature survey (R2, 121 papers)
    ├── R3-DSP-SURVEY-TOOLS.md               Toolkit survey (R3, 6 MIR toolkits)
    ├── R3-GAP-LOG.md                        Master gap log
    ├── R3-GAP-LOG-ARU.md                    Per-unit gap logs
    ├── R3-GAP-LOG-ASU.md
    ├── R3-GAP-LOG-IMU.md
    ├── R3-GAP-LOG-MPU.md
    ├── R3-GAP-LOG-NDU.md
    ├── R3-GAP-LOG-PCU.md
    └── R3-GAP-LOG-RPU.md
```

---

## 10. R³ File Count Summary

| Directory | Files | Content |
|-----------|:-----:|---------|
| Root | 4 | 00-INDEX, Architecture, Changelog, Extension Guide |
| Registry/ | 4 | Feature catalog, dimension map, naming conventions |
| Domains/ | 17 | 6 domain subdirs (1 root index + 6×(index + group docs)) |
| Contracts/ | 6 | 5 interface contracts + index |
| Pipeline/ | 5 | DAG, normalization, performance, state mgmt |
| Standards/ | 3 | Compliance matrix, quality tiers |
| Validation/ | 3 | Benchmark plan, acceptance criteria |
| Literature/ | 2 | 121-paper bibliography |
| Migration/ | 3 | V1→V2 guide, backward compatibility |
| Mappings/ | 10 | 9 per-unit consumption maps + index |
| upgrade_beta/ | 13 | Design phase working documents |
| **Total** | **71** | |

---

## 11. R3-SPECTRAL-ARCHITECTURE.md — Definitive Architecture Document

Section headings (13 sections):

1. **Design Philosophy** — Psychoacoustic grounding, domain taxonomy, backward compatibility
2. **Pipeline Overview** — Audio → mel → groups → normalize → (B,T,128) tensor
3. **128D Dimension Inventory** — Complete 11-group table with indices and dimensions
4. **Domain Taxonomy** — 6 perceptual domains organizing 11 groups
5. **Input Contract** — Mel spectrogram shape, sample rate, hop length
6. **Output Contract** — [0,1] normalized (B, T, 128) tensor
7. **Auto-Discovery Mechanism** — Dynamic group registration at startup
8. **Extension Model** — How to add new spectral groups
9. **Dependency Graph** — 3-stage extraction ordering
10. **Code Structure Mapping** — `mi_beta/ear/r3/` package layout
11. **Real-Time Feasibility** — Per-group cost and total budget
12. **Warm-up Behavior** — 344-688 frames for stateful features
13. **References** — Academic citations

---

## 12. The 128D Feature Space

### 11 Feature Groups (A-K)

| Group | Name | Indices | Dim | Domain | Status |
|:-----:|------|:-------:|:---:|:------:|:------:|
| A | Consonance | [0:7] | 7 | Psychoacoustic | v1 ✓ |
| B | Energy | [7:12] | 5 | Temporal | v1 ✓ |
| C | Timbre | [12:21] | 9 | Spectral | v1 ✓ |
| D | Change | [21:25] | 4 | Spectral | v1 ✓ |
| E | Interactions | [25:49] | 24 | CrossDomain | v1 ✓ |
| F | Pitch & Chroma | [49:65] | 16 | Tonal | v2 new |
| G | Rhythm & Groove | [65:75] | 10 | Temporal | v2 new |
| H | Harmony & Tonality | [75:87] | 12 | Tonal | v2 new |
| I | Information & Surprise | [87:94] | 7 | Information | v2 new |
| J | Timbre Extended | [94:114] | 20 | Spectral | v2 new |
| K | Modulation Perception | [114:128] | 14 | Psychoacoustic | v2 new |

**v1 total**: 49D (Groups A-E, indices 0-48)
**v2 expansion**: 79D (Groups F-K, indices 49-127)
**Combined**: 128D

### 6 Perceptual Domains

| Domain | Groups | Total Dim | Focus |
|--------|:------:|:---------:|-------|
| Psychoacoustic | A, K | 21D | Roughness, consonance, modulation |
| Temporal | B, G | 15D | Energy, rhythm, groove, tempo |
| Spectral | C, D, J | 33D | Timbre, change, MFCC, contrast |
| CrossDomain | E | 24D | Interaction products |
| Tonal | F, H | 28D | Pitch, chroma, harmony, tonality |
| Information | I | 7D | Entropy, surprise, ambiguity |

---

## 13. R³ Registry (4 files)

The Registry provides canonical reference tables for the 128D feature space.

| File | Content | Scope |
|------|---------|-------|
| **FeatureCatalog.md** | All 128 features: index, name, group, domain, psychoacoustic basis, quality tier | Definitive feature list |
| **DimensionMap.md** | Index-to-name-to-group mapping, group boundaries, domain boundaries, backward compat | Programmatic reference |
| **NamingConventions.md** | Feature, group, domain naming rules and standards | Governance |

---

## 14. R³ Domains (17 files across 6 subdirectories)

Each domain subdirectory contains per-group specification documents.

### Psychoacoustic/ (3 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| A-Consonance.md | A | [0:7] | Plomp-Levelt roughness, Sethares dissonance, consonance ratios |
| K-ModulationPerception.md | K | [114:128] | Modulation rates, Zwicker sharpness, eGeMAPS features |

### Spectral/ (4 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| C-Timbre.md | C | [12:21] | Warmth, sharpness, tonalness, clarity, tristimulus |
| D-Change.md | D | [21:25] | Spectral flux, entropy, flatness, concentration |
| J-TimbreExtended.md | J | [94:114] | MFCC (1-13) + spectral contrast (7D) |

### Tonal/ (3 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| F-PitchChroma.md | F | [49:65] | 12 chroma classes + pitch height/entropy/salience/inharmonicity |
| H-HarmonyTonality.md | H | [75:87] | Key clarity, tonnetz (6D), voice-leading, harmony change, diatonicity |

### Temporal/ (3 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| B-Energy.md | B | [7:12] | Amplitude, velocity, acceleration, loudness, onset strength |
| G-RhythmGroove.md | G | [65:75] | Tempo, beat strength, pulse clarity, syncopation, groove, metricality |

### Information/ (2 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| I-InformationSurprise.md | I | [87:94] | Melodic/harmonic/rhythmic entropy, spectral surprise, tonal ambiguity |

### CrossDomain/ (2 files)

| File | Group | Indices | Features |
|------|:-----:|:-------:|----------|
| E-Interactions.md | E | [25:49] | Energy×Consonance, Change×Consonance, Consonance×Timbre products |

---

## 15. R³ Contracts (6 files)

| Contract | Type | Purpose |
|----------|:----:|---------|
| **BaseSpectralGroup** | ABC | Abstract base class for all spectral groups |
| **R3FeatureRegistry** | Class | Registry lifecycle: register, freeze, query operations |
| **R3FeatureSpec** | Dataclass | Per-feature registration with name, group, domain, range |
| **R3Extractor** | Class | Top-level orchestrator: discovery → registration → extraction |
| **ExtensionProtocol** | Protocol | Extension system for adding new groups dynamically |

---

## 16. R³ Pipeline (5 files)

| File | Content |
|------|---------|
| **DependencyDAG.md** | 3-stage extraction ordering with GPU parallelization |
| **Normalization.md** | [0,1] normalization contract, per-group methods |
| **Performance.md** | Frame-level cost budget (2.5 ms amortized, 5.8 ms available) |
| **StateManagement.md** | Stateful vs stateless features, warm-up (344-688 frames), running statistics, reset |

### 3-Stage Extraction Pipeline

```
Stage 1: A, B, C, D, F, G, H  (7 groups in parallel — no dependencies)
Stage 2: I, J, K              (3 groups — may depend on Stage 1 outputs)
Stage 3: E                    (1 group — interaction products from A×B, A×C, C×D)
```

---

## 17. R³ Standards (3 files)

| File | Content |
|------|---------|
| **ComplianceMatrix.md** | ISO/AES/DIN/ITU standard mapping for 128 features |
| **QualityTiers.md** | 4-tier quality system: Proxy → Approximate → Standard → Reference |

---

## 18. R³ Validation (3 files)

| File | Content |
|------|---------|
| **BenchmarkPlan.md** | Experimental benchmarks for 6 critical features (mel-chroma, syncopation, etc.) |
| **AcceptanceCriteria.md** | Per-group quality gates: output shape, value range, NaN/Inf, performance budgets |

---

## 19. R³ Mappings (10 files)

One mapping document per C³ unit, showing which R³ features that unit's models consume.

| File | Unit | Content |
|------|:----:|---------|
| SPU-R3-MAP.md | SPU | 9 models' spectral feature consumption |
| STU-R3-MAP.md | STU | 14 models' temporal feature consumption |
| IMU-R3-MAP.md | IMU | 15 models' memory-relevant feature consumption |
| ASU-R3-MAP.md | ASU | 9 models' salience feature consumption |
| NDU-R3-MAP.md | NDU | 9 models' novelty feature consumption |
| MPU-R3-MAP.md | MPU | 10 models' motor feature consumption |
| PCU-R3-MAP.md | PCU | 10 models' prediction feature consumption |
| ARU-R3-MAP.md | ARU | 10 models' affective feature consumption |
| RPU-R3-MAP.md | RPU | 10 models' reward feature consumption |

---

## 20. R³ Migration (3 files)

| File | Content |
|------|---------|
| **V1-to-V2.md** | 49D→128D migration guide, 3-layer strategy, phase timeline |
| **BackwardCompatibility.md** | Indices 0-48 guaranteed unchanged, formula stability, rollback plan |

**Key guarantee**: All v1 feature indices [0:48] remain identical in v2.

---

## 21. R³ upgrade_beta/ — Design Phase Working Documents (13 files)

These are design-phase artifacts from the R³ v2 expansion work:

| File | Purpose |
|------|---------|
| **R3-V2-DESIGN.md** | Definitive v2 architecture design (Phase 3B primary source) |
| **R3-CROSSREF.md** | Three-perspective synthesis (demands + literature + tools) |
| **R3-DEMAND-MATRIX.md** | Bottom-up gap analysis from 96 C³ models (R1 perspective) |
| **R3-DSP-SURVEY-THEORY.md** | Literature survey — 121 papers (R2 perspective) |
| **R3-DSP-SURVEY-TOOLS.md** | Toolkit survey — 6 MIR toolkits (R3 perspective) |
| **R3-GAP-LOG.md** | Master gap log across all units |
| **R3-GAP-LOG-{UNIT}.md** (×7) | Per-unit gap logs (ARU, ASU, IMU, MPU, NDU, PCU, RPU) |

---

## 22. R³ Literature (2 files)

| File | Content |
|------|---------|
| **R3-LITERATURE.md** | 121-paper cross-reference: feature index, name, primary paper, DSP reference |

Categories: psychoacoustics, DSP, music information retrieval, spectral analysis, tonal theory.

---

## 23. R³ Cross-Layer References

| From R³ → | Reference Type | Location |
|-----------|---------------|----------|
| → C³ | Per-unit consumption mappings | `Docs/R³/Mappings/{UNIT}-R3-MAP.md` |
| → H³ | Temporal expansion impact | `Docs/H³/Expansion/R3v2-H3-Impact.md` |
| → H³ | Per-group temporal behavior | `Docs/H³/Expansion/{Group}-Temporal.md` |
| ← C³ | Model r3_indices (Section 4) | `Docs/C³/Models/{ID}/{ACRONYM}.md` |

---

---

# PART III — C³ Documentation Architecture

**Version**: 2.0.0
**Date**: 2026-02-13
**Total Files**: 162 markdown documents
**Layer**: C³ — Brain Models ("How does the brain process it?")

---

## 24. C³ Overview

C³ is the neural modelling layer of MI. It contains 96 computational models organized into 9 cognitive units, supported by 10 mechanisms, 6 circuits, 5 pathways, and associated infrastructure. The documentation mirrors the `mi_beta/brain/` code hierarchy.

**Pipeline position:**

```
R³ (128D spectral) → H³ (294,912D temporal) → [C³ Brain] → L³ (104D semantic)
```

**Total brain output**: 1,026D per frame (9 units concatenated)

---

## 25. C³ Directory Tree

```
Docs/C³/                                    (162 files total)
├── 00-INDEX.md                              Root index
├── C3-ARCHITECTURE.md                       Definitive architecture document
│
├── Models/                                  (97 files: 1 index + 96 model dirs)
│   ├── 00-INDEX.md
│   ├── SPU-α1-BCH/BCH.md
│   ├── SPU-α2-PSCL/PSCL.md
│   ├── ... (96 model directories, each with one .md file)
│
├── Units/                                   (10 files: 1 index + 9 unit docs)
│   ├── 00-INDEX.md
│   ├── SPU.md
│   ├── STU.md
│   ├── IMU.md
│   ├── ASU.md
│   ├── NDU.md
│   ├── MPU.md
│   ├── PCU.md
│   ├── ARU.md
│   └── RPU.md
│
├── Mechanisms/                              (11 files: 1 index + 10 mechanism docs)
│   ├── 00-INDEX.md
│   ├── AED.md
│   ├── ASA.md
│   ├── BEP.md
│   ├── C0P.md
│   ├── CPD.md
│   ├── MEM.md
│   ├── PPC.md
│   ├── SYN.md
│   ├── TMH.md
│   └── TPC.md
│
├── Pathways/                                (6 files: 1 index + 5 pathway docs)
│   ├── 00-INDEX.md
│   ├── P1-SPU-ARU.md
│   ├── P2-STU-INTERNAL.md
│   ├── P3-IMU-ARU.md
│   ├── P4-STU-INTERNAL.md
│   └── P5-STU-ARU.md
│
├── Regions/                                 (4 files: 1 index + 3 category docs)
│   ├── 00-INDEX.md
│   ├── Brainstem.md
│   ├── Cortical.md
│   └── Subcortical.md
│
├── Neurochemicals/                          (5 files: 1 index + 4 system docs)
│   ├── 00-INDEX.md
│   ├── Dopamine.md
│   ├── Norepinephrine.md
│   ├── Opioid.md
│   └── Serotonin.md
│
├── Circuits/                                (7 files: 1 index + 6 circuit docs)
│   ├── 00-INDEX.md
│   ├── Imagery.md
│   ├── Mesolimbic.md
│   ├── Mnemonic.md
│   ├── Perceptual.md
│   ├── Salience.md
│   └── Sensorimotor.md
│
├── Contracts/                               (9 files: 1 index + 8 contract docs)
│   ├── 00-INDEX.md
│   ├── BaseCognitiveUnit.md
│   ├── BaseMechanism.md
│   ├── BaseModel.md
│   ├── BrainRegion.md
│   ├── CrossUnitPathway.md
│   ├── H3DemandSpec.md
│   ├── LayerSpec.md
│   └── ModelMetadata.md
│
├── Tiers/                                   (4 files: 1 index + 3 tier docs)
│   ├── 00-INDEX.md
│   ├── Alpha.md
│   ├── Beta.md
│   └── Gamma.md
│
└── Matrices/                                (6 files: 1 index + 5 aggregate docs)
    ├── 00-INDEX.md
    ├── H3-Demand.md
    ├── Mechanism-Map.md
    ├── Output-Space.md
    ├── R3-Usage.md
    └── Region-Atlas.md
```

---

## 26. C³ File Count Summary

| Directory | Files | Content |
|-----------|:-----:|---------|
| Root | 2 | 00-INDEX.md, C3-ARCHITECTURE.md |
| Models/ | 97 | 00-INDEX.md + 96 model directories (1 .md each) |
| Units/ | 10 | 00-INDEX.md + 9 unit documents |
| Mechanisms/ | 11 | 00-INDEX.md + 10 mechanism documents |
| Pathways/ | 6 | 00-INDEX.md + 5 pathway documents |
| Regions/ | 4 | 00-INDEX.md + 3 region category documents |
| Neurochemicals/ | 5 | 00-INDEX.md + 4 neurochemical system documents |
| Circuits/ | 7 | 00-INDEX.md + 6 circuit documents |
| Contracts/ | 9 | 00-INDEX.md + 8 contract specifications |
| Tiers/ | 4 | 00-INDEX.md + 3 tier documents |
| Matrices/ | 6 | 00-INDEX.md + 5 aggregate matrix documents |
| **Total** | **162** | |

---

## 27. C3-ARCHITECTURE.md — Definitive Architecture Document

The root architecture document defines the complete C³ pipeline. Section headings:

1. **Overview** — Pipeline architecture (Audio → Cochlea → R³ → H³ → Brain → L³ → MI-space)
2. **Pipeline Stages** — Cochlea, R³, H³, Brain, L³ stage descriptions
3. **5-Phase Execution Model**:
   - Phase 1: Mechanisms (10 mechanisms compute in parallel)
   - Phase 2: Independent Units (SPU, STU, IMU, ASU, NDU, MPU, PCU)
   - Phase 3: Pathways (P1-P5 route signals)
   - Phase 4: Dependent Units (ARU, RPU)
   - Phase 5: Assembly (concatenate all unit outputs)
4. **Dependency Graph** — Visual DAG of unit dependencies
5. **Unit Execution Order** — `UNIT_EXECUTION_ORDER` constant
6. **Dimensionality Summary** — Per-unit output dimensions
7. **Core-4 vs Experimental-5** — Evidence strength classification
8. **Model Tiers** — Alpha / Beta / Gamma definitions
9. **Data Flow** — Signal flow diagram
10. **Neural Circuits** — 5 operational circuits
11. **Code-to-Documentation Reference** — Package-to-doc mapping
12. **Output Types** — BrainOutput, UnitOutput dataclasses
13. **Cross-References** — Links to R³, H³, L³

---

## 28. C³ Units (9 units, 10 files)

Each unit document contains:
- Property table (UNIT_NAME, FULL_NAME, CIRCUIT, POOLED_EFFECT, Evidence, Model Count, Total Output)
- Description of neural function
- Model Roster (Alpha / Beta / Gamma tiers with OUTPUT_DIM and Mechanisms)
- Mechanisms Used (with circuit assignments)
- Cross-Unit Pathways participation
- Code Reference paths
- Model Documentation links

### Unit Roster

| Unit | Full Name | Circuit | Pooled *d* | Models | Output | Dependency |
|:----:|-----------|---------|:----------:|:------:|:------:|:----------:|
| SPU | Spectral Processing Unit | perceptual | 0.84 | 9 | 99D | Independent |
| STU | Sensorimotor Timing Unit | sensorimotor | 0.67 | 14 | 148D | Independent |
| IMU | Integrative Memory Unit | mnemonic | 0.53 | 15 | 159D | Independent |
| ASU | Auditory Salience Unit | salience | 0.60 | 9 | 94D | Independent |
| NDU | Novelty Detection Unit | salience | 0.55 | 9 | 94D | Independent |
| MPU | Motor Planning Unit | sensorimotor | 0.62 | 10 | 104D | Independent |
| PCU | Predictive Coding Unit | mnemonic | 0.58 | 10 | 104D | Independent |
| ARU | Affective Resonance Unit | mesolimbic | 0.83 | 10 | 120D | Dependent |
| RPU | Reward Processing Unit | mesolimbic | 0.70 | 10 | 104D | Dependent |

**Total: 96 models, 1,026D brain output**

### Execution Order

```
Phase 2 (Independent):  SPU → STU → IMU → ASU → NDU → MPU → PCU
Phase 3 (Pathways):     P1(SPU→ARU), P2(STU→STU), P3(IMU→ARU), P4(STU→STU), P5(STU→ARU)
Phase 4 (Dependent):    ARU → RPU
```

### Evidence Classification

**Core-4** (k ≥ 10, >90% confidence): SPU (0.84), ARU (0.83), STU (0.67), IMU (0.53)
**Experimental-5** (k < 10): RPU (0.70), MPU (0.62), ASU (0.60), PCU (0.58), NDU (0.55)

---

## 29. C³ Models (96 models, 97 files)

### Model Document Structure (14 sections per model)

Each model `.md` file follows a standardized 14-section template:

| Section | Content |
|:-------:|---------|
| 1 | Identity (FULL_NAME, ACRONYM, UNIT, TIER) |
| 2 | Overview (1-paragraph description) |
| 3 | Scientific Foundation (12+ papers with DOIs) |
| 4 | R³ Spectral Indices (which R³ features the model reads) |
| 5 | H³ Temporal Demand (4-tuple specifications) |
| 6 | Output Dimensions (E/M/P/F layers with dimension names) |
| 7 | Mechanism Integration (BEP and/or ASA usage) |
| 8 | Brain Regions (MNI152 coordinates, abbreviations, Brodmann areas) |
| 9 | Evidence Strength (meta-analytic effect size, confidence interval) |
| 10 | Computational Notes (implementation details) |
| 11 | Cross-References (links to related models, mechanisms, docs) |
| 12 | Literature (expanded bibliography) |
| 13 | Brain Regions Extended (detailed region descriptions) |
| 14 | Version History (document version tracking) |

### All 96 Models by Unit

#### SPU — Spectral Processing Unit (9 models, 99D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | BCH | SPU-α1-BCH | Brainstem Cochlear Hub | α | 12D |
| 2 | PSCL | SPU-α2-PSCL | Primary Spectral Coding Loop | α | 11D |
| 3 | PCCR | SPU-α3-PCCR | Pitch-Chroma Cortical Representation | α | 11D |
| 4 | STAI | SPU-β1-STAI | Spectral-Temporal Attention Integration | β | 11D |
| 5 | TSCP | SPU-β2-TSCP | Timbral Shape Coding Pathway | β | 11D |
| 6 | MIAA | SPU-β3-MIAA | Multisensory Integration & Auditory Awareness | β | 11D |
| 7 | SDNPS | SPU-γ1-SDNPS | Spectral Deviation & Novelty Processing System | γ | 10D |
| 8 | ESME | SPU-γ2-ESME | Enhanced Spectral Modulation Encoding | γ | 10D |
| 9 | SDED | SPU-γ3-SDED | Spectral Density Estimation & Detection | γ | 10D |

#### STU — Sensorimotor Timing Unit (14 models, 148D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | HMCE | STU-α1-HMCE | Hierarchical Metric Cycle Extraction | α | 12D |
| 2 | AMSC | STU-α2-AMSC | Auditory-Motor Synchronization Circuit | α | 11D |
| 3 | MDNS | STU-α3-MDNS | Metric Deviation & Novelty Signaling | α | 11D |
| 4 | AMSS | STU-β1-AMSS | Auditory-Motor Sequence Segmentation | β | 11D |
| 5 | TPIO | STU-β2-TPIO | Temporal Prediction & Interval Optimization | β | 10D |
| 6 | EDTA | STU-β3-EDTA | Entrainment-Driven Temporal Attention | β | 10D |
| 7 | ETAM | STU-β4-ETAM | Entrainment-to-Affect Mapping | β | 10D |
| 8 | HGSIC | STU-β5-HGSIC | Hierarchical Groove Structure Integration Circuit | β | 10D |
| 9 | OMS | STU-β6-OMS | Oscillatory Motor Synchronization | β | 10D |
| 10 | TMRM | STU-γ1-TMRM | Temporal Micro-Rhythm Modeling | γ | 10D |
| 11 | NEWMD | STU-γ2-NEWMD | Neural Entrainment & Working Memory Dynamics | γ | 10D |
| 12 | MTNE | STU-γ3-MTNE | Multiscale Temporal Novelty Encoding | γ | 10D |
| 13 | PTGMP | STU-γ4-PTGMP | Predictive Timing & Groove Motor Planning | γ | 10D |
| 14 | MPFS | STU-γ5-MPFS | Motor-Predictive Feedback Sequencing | γ | 10D |

#### IMU — Integrative Memory Unit (15 models, 159D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | MEAMN | IMU-α1-MEAMN | Musical Episodic & Autobiographical Memory Network | α | 12D |
| 2 | PNH | IMU-α2-PNH | Predictive Neural Hierarchy | α | 11D |
| 3 | MMP | IMU-α3-MMP | Musical Memory Persistence | α | 11D |
| 4 | RASN | IMU-β1-RASN | Retrieval-Activated Salience Network | β | 11D |
| 5 | PMIM | IMU-β2-PMIM | Predictive Memory Integration Module | β | 11D |
| 6 | OII | IMU-β3-OII | Oscillatory Integration & Inhibition | β | 10D |
| 7 | HCMC | IMU-β4-HCMC | Hippocampal-Cortical Memory Consolidation | β | 10D |
| 8 | RIRI | IMU-β5-RIRI | Retrieval-Induced Reconsolidation & Interference | β | 10D |
| 9 | MSPBA | IMU-β6-MSPBA | Musical Schema & Predictive Brain Architecture | β | 10D |
| 10 | VRIAP | IMU-β7-VRIAP | Veridical Retrieval & Involuntary Auditory Playback | β | 10D |
| 11 | TPRD | IMU-β8-TPRD | Temporal Pattern Recognition & Decay | β | 10D |
| 12 | CMAPCC | IMU-β9-CMAPCC | Cross-Modal Auditory Prediction & Cortical Coupling | β | 10D |
| 13 | DMMS | IMU-γ1-DMMS | Dynamic Musical Memory Segmentation | γ | 10D |
| 14 | CSSL | IMU-γ2-CSSL | Context-Sensitive Statistical Learning | γ | 10D |
| 15 | CDEM | IMU-γ3-CDEM | Cortical Dynamics of Expectation Mapping | γ | 10D |

#### ASU — Auditory Salience Unit (9 models, 94D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | SNEM | ASU-α1-SNEM | Salience Network Engagement Model | α | 12D |
| 2 | IACM | ASU-α2-IACM | Insula-ACC Coupling Model | α | 11D |
| 3 | CSG | ASU-α3-CSG | Cortical Salience Gating | α | 11D |
| 4 | BARM | ASU-β1-BARM | Bottom-Up Attentional Resource Model | β | 10D |
| 5 | STANM | ASU-β2-STANM | Spectro-Temporal Auditory Novelty Model | β | 10D |
| 6 | AACM | ASU-β3-AACM | Adaptive Attention Control Mechanism | β | 10D |
| 7 | PWSM | ASU-γ1-PWSM | Perceptual Weighting & Salience Model | γ | 10D |
| 8 | DGTP | ASU-γ2-DGTP | Dynamic Gain & Temporal Prediction | γ | 10D |
| 9 | SDL | ASU-γ3-SDL | Salience-Driven Learning | γ | 10D |

#### NDU — Novelty Detection Unit (9 models, 94D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | MPG | NDU-α1-MPG | Mismatch & Prediction Gateway | α | 12D |
| 2 | SDD | NDU-α2-SDD | Statistical Deviance Detection | α | 11D |
| 3 | EDNR | NDU-α3-EDNR | Expectation-Driven Novelty Response | α | 11D |
| 4 | DSP | NDU-β1-DSP | Deviance Salience Propagation | β | 10D |
| 5 | CDMR | NDU-β2-CDMR | Context-Dependent Mismatch Response | β | 10D |
| 6 | SLEE | NDU-β3-SLEE | Statistical Learning & Expectation Engine | β | 10D |
| 7 | SDDP | NDU-γ1-SDDP | Spectral Deviance & Detection Processing | γ | 10D |
| 8 | ONI | NDU-γ2-ONI | Oscillatory Novelty Integration | γ | 10D |
| 9 | ECT | NDU-γ3-ECT | Expectancy & Contextual Tracking | γ | 10D |

#### MPU — Motor Planning Unit (10 models, 104D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | PEOM | MPU-α1-PEOM | Predictive Error & Oscillatory Motor | α | 12D |
| 2 | MSR | MPU-α2-MSR | Motor Sequence Representation | α | 11D |
| 3 | GSSM | MPU-α3-GSSM | Groove-Synchronized Sensorimotor Model | α | 11D |
| 4 | ASAP | MPU-β1-ASAP | Auditory-Somatosensory Action Planning | β | 10D |
| 5 | DDSMI | MPU-β2-DDSMI | Dynamic & Discrete Sensorimotor Integration | β | 10D |
| 6 | VRMSME | MPU-β3-VRMSME | Vestibular-Rhythmic Motor Simulation & Motion Encoding | β | 10D |
| 7 | SPMC | MPU-β4-SPMC | Sensorimotor Prediction & Motor Coupling | β | 10D |
| 8 | NSCP | MPU-γ1-NSCP | Neural Sequence & Chunking Processor | γ | 10D |
| 9 | CTBB | MPU-γ2-CTBB | Cerebellar Timing & Basal-ganglia Bridge | γ | 10D |
| 10 | STC | MPU-γ3-STC | Sensorimotor Temporal Chunking | γ | 10D |

#### PCU — Predictive Coding Unit (10 models, 104D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | HTP | PCU-α1-HTP | Harmonic Tension Prediction | α | 12D |
| 2 | SPH | PCU-α2-SPH | Spectral Pitch Height | α | 11D |
| 3 | ICEM | PCU-α3-ICEM | Imagery-Cognition Emotion Mapping | α | 11D |
| 4 | PWUP | PCU-β1-PWUP | Pitch-Weight Uncertainty Processing | β | 10D |
| 5 | WMED | PCU-β2-WMED | Working Memory Emotion Dynamics | β | 10D |
| 6 | UDP | PCU-β3-UDP | Uncertainty-Driven Prediction | β | 10D |
| 7 | CHPI | PCU-β4-CHPI | Cross-Modal Harmonic Predictive Integration | β | 10D |
| 8 | IGFE | PCU-γ1-IGFE | Imagery-Guided Feature Enhancement | γ | 10D |
| 9 | MAA | PCU-γ2-MAA | Musical Agentic Attention | γ | 10D |
| 10 | PSH | PCU-γ3-PSH | Perceptual Salience Hierarchy | γ | 10D |

#### ARU — Affective Resonance Unit (10 models, 120D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | SRP | ARU-α1-SRP | Spectral Reward Prediction | α | 14D |
| 2 | AAC | ARU-α2-AAC | Affective-Autonomic Coupling | α | 13D |
| 3 | VMM | ARU-α3-VMM | Valence-Mode Mapping | α | 13D |
| 4 | PUPF | ARU-β1-PUPF | Prediction Uncertainty & Pleasure Function | β | 12D |
| 5 | CLAM | ARU-β2-CLAM | Chill-Linked Affect Model | β | 12D |
| 6 | MAD | ARU-β3-MAD | Musical Aesthetic Dynamics | β | 11D |
| 7 | NEMAC | ARU-β4-NEMAC | Neural Entrainment & Musical Affect Circuit | β | 11D |
| 8 | DAP | ARU-γ1-DAP | Dynamic Affect Prediction | γ | 10D |
| 9 | CMAT | ARU-γ2-CMAT | Cross-Modal Affect Transfer | γ | 10D |
| 10 | TAR | ARU-γ3-TAR | Tension-to-Affect Resolution | γ | 10D |

#### RPU — Reward Processing Unit (10 models, 104D)

| # | ID | Dir Name | Full Name | Tier | Dim |
|:-:|:--:|----------|-----------|:----:|:---:|
| 1 | DAED | RPU-α1-DAED | Dopaminergic Anticipation & Expectation Dynamics | α | 12D |
| 2 | MORMR | RPU-α2-MORMR | Mu-Opioid Reward & Musical Reward | α | 11D |
| 3 | RPEM | RPU-α3-RPEM | Reward Prediction Error Modulation | α | 11D |
| 4 | IUCP | RPU-β1-IUCP | Incentive-Uncertainty & Curiosity Processing | β | 10D |
| 5 | MCCN | RPU-β2-MCCN | Musical Compulsion & Craving Network | β | 10D |
| 6 | MEAMR | RPU-β3-MEAMR | Musical Episodic-Autobiographical Memory Reward | β | 10D |
| 7 | SSRI | RPU-β4-SSRI | Social Synchrony Reward Integration | β | 10D |
| 8 | LDAC | RPU-γ1-LDAC | Learned DA Contingency | γ | 10D |
| 9 | IOTMS | RPU-γ2-IOTMS | Inter-Opioid Tonic Modulation System | γ | 10D |
| 10 | SSPS | RPU-γ3-SSPS | Serotonergic Satiation & Pleasure Signaling | γ | 10D |

### Tier Distribution

| Tier | Criteria | Count | Output Range |
|:----:|----------|:-----:|:-----------:|
| Alpha (α) | k ≥ 10 studies, >90% confidence | 27 | 11-14D |
| Beta (β) | 5 ≤ k < 10, 70-90% confidence | 40 | 10-12D |
| Gamma (γ) | k < 5, <70% confidence | 29 | 10D |
| **Total** | | **96** | **1,026D** |

---

## 30. C³ Mechanisms (10 mechanisms, 11 files)

Each mechanism document defines a shared computational module used by multiple models across units.

| Mechanism | Full Name | Circuit | Output | Key Horizons |
|:---------:|-----------|:-------:|:------:|:------------:|
| PPC | Pitch Processing Chain | perceptual | 30D | H0, H3, H6 |
| TPC | Timbre Processing Chain | perceptual | 30D | H6, H12, H16 |
| BEP | Beat Entrainment Processing | sensorimotor | 30D | H6, H9, H11 |
| TMH | Temporal Memory Hierarchy | sensorimotor | 30D | H16, H18, H20, H22 |
| MEM | Memory Encoding / Retrieval | mnemonic | 30D | H18, H20, H22, H25 |
| SYN | Syntactic Processing | mnemonic | 30D | H12, H16, H18 |
| ASA | Auditory Scene Analysis | salience | 30D | H3, H6, H9 |
| AED | Affective Entrainment Dynamics | mesolimbic | 30D | H6, H16 |
| CPD | Chills & Peak Detection | mesolimbic | 30D | H9, H16, H18 |
| C0P | Cognitive Projection | mesolimbic | 30D | H18, H19, H20 |

### Mechanism-to-Unit Usage

| Unit | Mechanisms Used | Source Circuits |
|:----:|----------------|:---------------:|
| SPU | PPC, TPC | perceptual |
| STU | BEP, TMH | sensorimotor |
| IMU | MEM, TMH | mnemonic + sensorimotor |
| ASU | BEP, ASA | sensorimotor + salience |
| NDU | PPC, ASA | perceptual + salience |
| MPU | BEP, TMH | sensorimotor |
| PCU | PPC, TPC, MEM | perceptual + mnemonic |
| ARU | AED, CPD | mesolimbic |
| RPU | AED, CPD, C0P | mesolimbic |

---

## 31. C³ Circuits (6 circuits, 7 files)

Two circuit registries exist in `constants.py`:
- **`CIRCUIT_NAMES`** (6): Full conceptual set including imagery
- **`CIRCUITS`** (5): Operational set for pathway routing (excludes imagery)

| Circuit | Description | Mechanisms | Units | Key Brain Regions |
|---------|-------------|:----------:|:-----:|-------------------|
| **Mesolimbic** | Reward & Pleasure | AED, CPD, C0P | ARU, RPU | NAcc, VTA, Amygdala, vmPFC, OFC |
| **Perceptual** | Hearing & Pattern | PPC, TPC | SPU | Heschl's Gyrus, PT, PP, IC |
| **Sensorimotor** | Rhythm & Movement | BEP, TMH | STU, MPU | SMA, PMC, Cerebellum, BG |
| **Mnemonic** | Memory & Familiarity | MEM, SYN | IMU, PCU | Hippocampus, mPFC, IFG, dlPFC |
| **Salience** | Attention & Novelty | ASA | ASU, NDU | aInsula, dACC, TPJ, IFG |
| **Imagery** | Simulation & Prediction | (PPC, TPC, MEM)* | PCU* | AC, IFG, STS, Hipp |

*Imagery reuses mechanisms from perceptual and mnemonic circuits.

### Temporal Coverage by Circuit

```
        5.8ms    23ms    200ms   350ms   525ms    1s     2s     5s    15s    60s
          |       |       |       |       |       |      |      |      |      |
PERCEPT:  H0------H3------H6                                                    PPC
                          H6--------------H12-----H16                            TPC
SENSORI:                  H6------H9------H11                                    BEP
                                                  H16----H18----H20----H22       TMH
MNEMONIC:                                 H12-----H16----H18                     SYN
                                                         H18----H20----H22--H25  MEM
SALIENCE:         H3------H6------H9                                             ASA
MESOLIMB:                 H6                      H16----H18                     AED
                                  H9              H16----H18                     CPD
                                                         H18----H19----H20       C0P
```

---

## 32. C³ Pathways (5 pathways, 6 files)

| Pathway | Route | Signal | Direction |
|:-------:|-------|--------|:---------:|
| P1 | SPU → ARU | Spectral features modulate affect | Cross-unit |
| P2 | STU → STU (HMCE → AMSC) | Beat → motor sync | Internal |
| P3 | IMU → ARU | Memory/familiarity modulates affect | Cross-unit |
| P4 | STU → STU (context hierarchy) | Context → prediction | Internal |
| P5 | STU → ARU | Temporal structure modulates affect | Cross-unit |

Independent units (Phase 2) → Pathways (Phase 3) → Dependent units (Phase 4)

---

## 33. C³ Regions (26 brain regions, 4 files)

| Category | Count | Regions |
|----------|:-----:|---------|
| **Brainstem** | 5 | IC, AN, CN, SOC, PAG |
| **Cortical** | 12 | A1/HG, STG, STS, IFG, dlPFC, vmPFC, OFC, ACC, SMA, PMC, AG, TP |
| **Subcortical** | 9 | VTA, NAcc, caudate, amygdala, hippocampus, putamen, MGB, hypothalamus, insula |

All regions defined in MNI152 coordinate space with Brodmann areas where applicable.

---

## 34. C³ Neurochemicals (4 systems, 5 files)

| System | Role in Music Processing |
|--------|------------------------|
| **Dopamine** | Reward prediction error, anticipation, pleasure |
| **Opioid** | Hedonic liking, consummatory pleasure |
| **Serotonin** | Mood regulation, emotional valence bias |
| **Norepinephrine** | Arousal, attentional gating, orienting |

The `NeurochemicalState` registry provides write-once-per-pass signaling between models:
- Write: `state.write(NeurochemicalType.DOPAMINE, "NAcc", tensor)`
- Read: `state.read(NeurochemicalType.DOPAMINE, "NAcc")` → `Optional[Tensor]`

---

## 35. C³ Contracts (8 contracts, 9 files)

| Contract | Type | Purpose |
|----------|:----:|---------|
| BaseModel | ABC | Abstract base for all 96 cognitive models |
| BaseMechanism | ABC | Abstract base for all 10 mechanisms |
| BaseCognitiveUnit | ABC | Abstract base for all 9 cognitive units |
| LayerSpec | Dataclass | E/M/P/F output layer slice definitions |
| H3DemandSpec | Dataclass | Typed H³ temporal demand 4-tuples |
| CrossUnitPathway | ABC | Inter-unit data dependency routing |
| BrainRegion | Dataclass | MNI152 anatomical region specifications |
| ModelMetadata | Dataclass | Evidence provenance, citations, tier, confidence |

### Model Output Layer Convention (E/M/P/F)

Every model's output is sliced into 4 functional layers:

| Layer | Name | Purpose | Typical Dims |
|:-----:|------|---------|:------------:|
| E | Encoding | Raw feature extraction | 3-4D |
| M | Modulation | Contextual modulation | 2-3D |
| P | Prediction | Forward prediction signals | 2-3D |
| F | Feedback | Error / correction signals | 2-3D |

---

## 36. C³ Matrices (5 aggregate views, 6 files)

| Matrix | Content | Dimensions |
|--------|---------|:----------:|
| **R3-Usage** | Which R³ features each model reads | 96 × 128 |
| **H3-Demand** | H³ demand tuple aggregation per unit | 9 units × ~8,600 tuples |
| **Mechanism-Map** | Which mechanisms each model uses | 96 × 10 |
| **Output-Space** | E/M/P/F layer dimensions per model | 96 × 4 |
| **Region-Atlas** | Which brain regions each model activates | 96 × 26 |

---

## 37. C³ Index Files (11 total)

| Directory | 00-INDEX.md | Key Content |
|-----------|:-----------:|-------------|
| Root | ✓ | 11 subdirectory listing, architecture overview |
| Models/ | ✓ | 96 models by unit with tier counts |
| Units/ | ✓ | 9 units with pooled effects, execution order |
| Mechanisms/ | ✓ | 10 mechanisms with circuit assignments |
| Pathways/ | ✓ | 5 pathways with routing flow |
| Regions/ | ✓ | 26 regions in MNI152 atlas |
| Neurochemicals/ | ✓ | 6 neurochemical systems |
| Circuits/ | ✓ | 6 circuits with unit/mechanism assignments |
| Contracts/ | ✓ | 8 contracts with dependency graph |
| Tiers/ | ✓ | Alpha(27), Beta(40), Gamma(29) = 96 |
| Matrices/ | ✓ | 5 aggregate cross-reference matrices |

---

## 38. C³ Code Correspondence

| Documentation | Code Package |
|---------------|-------------|
| `Docs/C³/Models/{UNIT}-{tier}{n}-{ACRONYM}/` | `mi_beta/brain/units/{unit}/models/{acronym}.py` |
| `Docs/C³/Units/{UNIT}.md` | `mi_beta/brain/units/{unit}/_unit.py` |
| `Docs/C³/Mechanisms/{MECH}.md` | `mi_beta/brain/mechanisms/{mech}.py` |
| `Docs/C³/Pathways/P{n}-*.md` | `mi_beta/brain/pathways/p{n}_*.py` |
| `Docs/C³/Regions/*.md` | `mi_beta/brain/regions/*.py` |
| `Docs/C³/Neurochemicals/*.md` | `mi_beta/brain/neurochemicals/*.py` |
| `Docs/C³/Contracts/*.md` | `mi_beta/contracts/*.py` |

---

## 39. C³ Cross-Layer References

| From C³ → | Reference Type | Location |
|-----------|---------------|----------|
| → R³ | Per-model r3_indices (Section 4) | `Docs/R³/Mappings/{UNIT}-R3-MAP.md` |
| → H³ | Per-model h3_demand tuples (Section 5) | `Docs/H³/Demand/{UNIT}-H3-DEMAND.md` |
| → L³ | Per-unit semantic adapters | `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` |

---

---

# PART IV — H³ Documentation Architecture

**Version**: 2.0.0
**Date**: 2026-02-13
**Total Files**: 73 markdown documents
**Layer**: H³ — Temporal Demand ("How does it change over time?")

---

## 40. H³ Overview

H³ is the temporal analysis layer of MI. It computes statistical descriptors of how R³ spectral features evolve across multiple time horizons, producing a sparse subset of a 294,912-dimensional theoretical address space.

**Pipeline position:**

```
Audio → Cochlea → R³ (128D) → [H³ temporal demand] → Brain → L³ → MI-space
```

**Key metrics:**
- **Address space**: 128 features × 32 horizons × 24 morphs × 3 laws = 294,912 theoretical
- **Actual demand**: ~8,600 tuples (~2.9% occupancy)
- **Address format**: 4-tuple `(r3_idx, horizon, morph, law)`
- **Computation**: Demand-driven sparse evaluation (only compute what C³ models request)

---

## 41. H³ Directory Tree

```
Docs/H³/                                    (73 files total)
├── 00-INDEX.md                              Root index
├── H3-TEMPORAL-ARCHITECTURE.md              Definitive architecture document
├── CHANGELOG.md                             Version history
├── EXTENSION-GUIDE.md                       How to add morphs/horizons
│
├── Registry/                                (5 files)
│   ├── 00-INDEX.md
│   ├── HorizonCatalog.md                    All 32 horizons with metadata
│   ├── MorphCatalog.md                      All 24 morphs with formulas
│   ├── LawCatalog.md                        All 3 laws with kernels
│   └── DemandAddressSpace.md                4-tuple addressing + sparsity
│
├── Bands/                                   (12 files across 4 sub-bands)
│   ├── 00-INDEX.md                          Cross-band comparison
│   │
│   ├── Micro/                               (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── H0-H5-SubBeat.md                H0-H5: 5.8ms-120ms
│   │   └── H6-H7-BeatSubdivision.md        H6-H7: 175ms-250ms
│   │
│   ├── Meso/                                (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── H8-H11-BeatPeriod.md             H8-H11: 300ms-525ms
│   │   └── H12-H15-Phrase.md                H12-H15: 600ms-800ms
│   │
│   ├── Macro/                               (3 files)
│   │   ├── 00-INDEX.md
│   │   ├── H16-H17-Measure.md               H16-H17: 1s-1.5s
│   │   └── H18-H23-Section.md               H18-H23: 2s-25s
│   │
│   └── Ultra/                               (3 files)
│       ├── 00-INDEX.md
│       ├── H24-H28-Movement.md              H24-H28: 36s-280s
│       └── H29-H31-Piece.md                 H29-H31: 407s-981s
│
├── Morphology/                              (7 files)
│   ├── 00-INDEX.md
│   ├── Distribution.md                      M0-M7: Central tendency, spread, shape
│   ├── Dynamics.md                          M8-M13, M15, M18, M21: Derivatives, trend
│   ├── Rhythm.md                            M14, M17, M22: Periodicity, peaks
│   ├── Information.md                       M20: Entropy
│   ├── Symmetry.md                          M16, M19, M23: Curvature, stability
│   └── MorphScaling.md                      MORPH_SCALE (gain, bias) calibration
│
├── Laws/                                    (4 files)
│   ├── 00-INDEX.md
│   ├── L0-Memory.md                         Past → Present
│   ├── L1-Prediction.md                     Present → Future
│   └── L2-Integration.md                    Past ↔ Future
│
├── Contracts/                               (6 files)
│   ├── 00-INDEX.md
│   ├── H3Extractor.md                       Top-level entry point
│   ├── DemandTree.md                        Demand aggregation/deduplication
│   ├── EventHorizon.md                      Horizon lookup/conversion
│   ├── MorphComputer.md                     24-morph dispatch table
│   └── AttentionKernel.md                   Exponential decay computation
│
├── Pipeline/                                (5 files)
│   ├── 00-INDEX.md
│   ├── ExecutionModel.md                    End-to-end execution flow
│   ├── SparsityStrategy.md                  97.1% computation savings
│   ├── Performance.md                       Per-horizon cost model
│   └── WarmUp.md                            Horizon-dependent warm-up
│
├── Demand/                                  (10 files)
│   ├── 00-INDEX.md
│   ├── SPU-H3-DEMAND.md                     ~450 tuples
│   ├── STU-H3-DEMAND.md                     ~900 tuples
│   ├── IMU-H3-DEMAND.md                     ~1,200 tuples (largest)
│   ├── ASU-H3-DEMAND.md                     ~360 tuples
│   ├── NDU-H3-DEMAND.md                     ~400 tuples
│   ├── MPU-H3-DEMAND.md                     ~500 tuples
│   ├── PCU-H3-DEMAND.md                     ~500 tuples
│   ├── ARU-H3-DEMAND.md                     ~500 tuples
│   └── RPU-H3-DEMAND.md                     ~400 tuples
│
├── Expansion/                               (8 files)
│   ├── 00-INDEX.md
│   ├── R3v2-H3-Impact.md                    Master impact analysis
│   ├── F-PitchChroma-Temporal.md            Group F [49:65] temporal demand
│   ├── G-RhythmGroove-Temporal.md           Group G [65:75] temporal demand
│   ├── H-HarmonyTonality-Temporal.md        Group H [75:87] temporal demand
│   ├── I-InformationSurprise-Temporal.md    Group I [87:94] temporal demand
│   ├── J-TimbreExtended-Temporal.md         Group J [94:114] temporal demand
│   └── K-ModulationPsychoacoustic-Temporal.md  Group K [114:128] temporal demand
│
├── Standards/                               (3 files)
│   ├── 00-INDEX.md
│   ├── MorphQualityTiers.md                 24-morph × 4-band quality matrix
│   └── TemporalResolutionStandards.md       Minimum window sizes
│
├── Validation/                              (3 files)
│   ├── 00-INDEX.md
│   ├── AcceptanceCriteria.md                Per-morph/horizon pass/fail tests
│   └── BenchmarkPlan.md                     Synthetic test corpus
│
├── Literature/                              (2 files)
│   ├── 00-INDEX.md
│   └── H3-LITERATURE.md                     Annotated bibliography
│
└── Migration/                               (3 files)
    ├── 00-INDEX.md
    ├── V1-to-V2.md                          Main migration guide
    └── DemandSpec-Update.md                 Detailed update procedure
```

---

## 42. H³ File Count Summary

| Directory | Files | Content |
|-----------|:-----:|---------|
| Root | 4 | 00-INDEX, Architecture, Changelog, Extension Guide |
| Registry/ | 5 | Horizon, Morph, Law catalogs + demand address space |
| Bands/ | 12 | 4 sub-bands × 3 files (index + 2 horizon docs) |
| Morphology/ | 7 | 5 morph categories + scaling guide |
| Laws/ | 4 | 3 temporal laws + index |
| Contracts/ | 6 | 5 interface contracts + index |
| Pipeline/ | 5 | Execution, sparsity, performance, warm-up |
| Demand/ | 10 | 9 per-unit demand docs + index |
| Expansion/ | 8 | R³ v2 impact analysis + 6 per-group temporal docs |
| Standards/ | 3 | Morph quality tiers, resolution standards |
| Validation/ | 3 | Acceptance criteria, benchmark plan |
| Literature/ | 2 | Annotated bibliography |
| Migration/ | 3 | V1→V2 guide, DemandSpec update |
| **Total** | **73** | |

---

## 43. H3-TEMPORAL-ARCHITECTURE.md — Definitive Architecture Document

Section headings (13 sections + appendix):

1. **Design Philosophy** — Demand-driven sparsity, orthogonal space, musical grounding, lazy evaluation
2. **Pipeline Position** — Where H³ sits in the MI audio processing chain
3. **The 4-Tuple Address System** — `(r3_idx, horizon, morph, law)` canonical format
4. **Axis 1: Horizons (32 Temporal Scales)** — Complete horizon table, frame progression
5. **Axis 2: Morphs (24 Statistical Descriptors)** — Complete morph table, MORPH_SCALE
6. **Axis 3: Laws (3 Temporal Perspectives)** — Window definitions, kernel formulas
7. **Attention Kernel** — `A(dt) = exp(-3|dt|/H)`, half-life = 0.231×H
8. **Mechanism Integration** — How 10 C³ mechanisms access H³ horizon bands
9. **Demand Aggregation** — DemandTree grouping, per-unit summaries
10. **Sparsity Analysis** — Theoretical vs actual (97.1% savings)
11. **R³ v2 Expansion Impact** — Space grows 2.61×, demand grows ~65%
12. **Code Architecture** — File structure, module responsibilities
13. **Cross-References** — Links to all related docs
14. **Appendix A**: Quick Reference Card

---

## 44. The Three Axes

### Axis 1: Horizons (32 temporal scales)

| Band | Horizons | Duration Range | Frames | Musical Scale | Mechanisms |
|:----:|:--------:|:--------------:|:------:|:-------------:|:----------:|
| **Micro** | H0-H7 | 5.8ms - 250ms | 1-43 | Onset, attack, note | PPC, ASA, TPC, BEP, AED |
| **Meso** | H8-H15 | 300ms - 800ms | 52-138 | Beat, quarter note, motif | BEP, TPC, SYN, ASA, CPD |
| **Macro** | H16-H23 | 1s - 25s | 172-4,307 | Measure, section, passage | TMH, MEM, C0P, SYN, AED, CPD, TPC |
| **Ultra** | H24-H31 | 36s - 981s | 6,202-168,999 | Movement, piece, full work | MEM (sparse) |

**Macro band** contains ~49% of all H³ tuples (dominant band).

### Axis 2: Morphs (24 statistical descriptors)

| Category | Morphs | Count | Description |
|----------|:------:|:-----:|-------------|
| **Distribution** | M0-M7 | 8 | Mean, median, std, var, skew, kurtosis, min, max |
| **Dynamics** | M8-M13, M15, M18, M21 | 9 | Velocity, acceleration, jerk, momentum, trend, smoothness |
| **Rhythm** | M14, M17, M22 | 3 | Periodicity, dominant cycle, peak count |
| **Information** | M20 | 1 | Entropy |
| **Symmetry** | M16, M19, M23 | 3 | Curvature, stability, time-reversal |

Each morph has a `MORPH_SCALE` entry: `(gain, bias)` for output normalization.

### Axis 3: Laws (3 temporal perspectives)

| Law | Name | Direction | Window | Kernel |
|:---:|------|:---------:|--------|--------|
| L0 | Memory | Past → Present | `[t-H, t]` | `A(dt) = exp(-3|dt|/H)` |
| L1 | Prediction | Present → Future | `[t, t+H]` | `A(dt) = exp(-3|dt|/H)` |
| L2 | Integration | Past ↔ Future | `[t-H, t+H]` | `A(dt) = exp(-3|dt|/H)` |

**Shared attention kernel**: `A(dt) = exp(-3|dt|/H)` with `ATTENTION_DECAY = 3.0`
- Peak at current frame: 1.0
- Boundary at |dt|=H: ~5%
- Half-life: 0.231 × H

---

## 45. H³ Registry (5 files)

| File | Content | Canonical Data |
|------|---------|:-------------:|
| **HorizonCatalog.md** | All 32 horizons: duration, frames, band, musical scale, neuroscience basis, mechanism mappings | HORIZON_MS[32] |
| **MorphCatalog.md** | All 24 morphs: formula, category, min window, output range, MORPH_SCALE values | MORPH_NAMES[24] |
| **LawCatalog.md** | All 3 laws: direction, window, kernel formula, neuroscience basis, per-unit usage | LAW_NAMES[3] |
| **DemandAddressSpace.md** | 4-tuple format, flat index formula, theoretical vs actual space, sparsity metrics | Address system spec |

---

## 46. H³ Bands (12 files across 4 sub-bands)

Each sub-band directory documents the horizons within that temporal range.

### Micro/ (H0-H7: 5.8ms - 250ms)
- **H0-H5-SubBeat.md**: Sensory processing — onset detection, transient analysis, cochlear timescales
- **H6-H7-BeatSubdivision.md**: Beat subdivision — sixteenth/eighth note durations

### Meso/ (H8-H15: 300ms - 800ms)
- **H8-H11-BeatPeriod.md**: Beat period — quarter note, typical beat duration
- **H12-H15-Phrase.md**: Phrase level — short motifs, musical phrases

### Macro/ (H16-H23: 1s - 25s)
- **H16-H17-Measure.md**: Measure level — bar-length temporal patterns
- **H18-H23-Section.md**: Section level — verse, chorus, bridge durations

### Ultra/ (H24-H31: 36s - 981s)
- **H24-H28-Movement.md**: Movement level — multi-section spans
- **H29-H31-Piece.md**: Piece level — full work duration (H29-H31 reserved for future)

---

## 47. H³ Morphology (7 files)

| File | Morphs | Content |
|------|:------:|---------|
| **Distribution.md** | M0-M7 | Central tendency, spread, shape statistics |
| **Dynamics.md** | M8-M13, M15, M18, M21 | First/second/third derivatives, trend, momentum, smoothness |
| **Rhythm.md** | M14, M17, M22 | Periodicity via autocorrelation, dominant cycle, peak detection |
| **Information.md** | M20 | Shannon entropy of binned distribution |
| **Symmetry.md** | M16, M19, M23 | Curvature (second derivative sign), stability, time-reversal symmetry |
| **MorphScaling.md** | All 24 | `MORPH_SCALE` calibration: `(gain, bias)` pairs for [0,1] normalization |

---

## 48. H³ Laws (4 files)

| File | Law | Direction | Usage |
|------|:---:|:---------:|:-----:|
| **L0-Memory.md** | L0 | Past → Present | 8/9 units |
| **L1-Prediction.md** | L1 | Present → Future | 6/9 units |
| **L2-Integration.md** | L2 | Past ↔ Future | 8/9 units |

---

## 49. H³ Contracts (6 files)

| Contract | Purpose |
|----------|---------|
| **H3Extractor** | Top-level class: orchestrates computation, returns sparse `dict{4-tuple: Tensor}` |
| **DemandTree** | Aggregates/deduplicates/groups H³ demands by horizon from all C³ models |
| **EventHorizon** | Manages 32 horizon definitions, frame conversion, band lookup |
| **MorphComputer** | 24-method dispatch table for all morph statistical functions |
| **AttentionKernel** | Computes exponential decay weights: `A(dt) = exp(-3|dt|/H)` |

---

## 50. H³ Demand (10 files)

One demand document per C³ unit, specifying the H³ 4-tuples that unit's models request.

| File | Unit | Models | Mechanisms | Approx. Tuples |
|------|:----:|:------:|:----------:|:--------------:|
| SPU-H3-DEMAND.md | SPU | 9 | PPC, TPC | ~450 |
| STU-H3-DEMAND.md | STU | 14 | BEP, TMH, TPC | ~900 |
| IMU-H3-DEMAND.md | IMU | 15 | MEM, TMH | ~1,200 |
| ASU-H3-DEMAND.md | ASU | 9 | ASA | ~360 |
| NDU-H3-DEMAND.md | NDU | 9 | ASA, PPC | ~400 |
| MPU-H3-DEMAND.md | MPU | 10 | BEP, TMH | ~500 |
| PCU-H3-DEMAND.md | PCU | 10 | PPC, TPC, MEM (6 mech) | ~500 |
| ARU-H3-DEMAND.md | ARU | 10 | AED, CPD | ~500 |
| RPU-H3-DEMAND.md | RPU | 10 | AED, CPD, C0P (7 mech) | ~400 |

**Grand total**: 96 models, 10 mechanisms, ~5,210 tuples (v1) → ~8,610 tuples (v2)

---

## 51. H³ Expansion (8 files)

Documents the impact of the R³ v2 expansion (49D→128D) on H³ temporal demand.

| File | Group | New Features | New Dim | Priority |
|------|:-----:|:------------:|:-------:|:--------:|
| **R3v2-H3-Impact.md** | All F-K | Master impact analysis | — | — |
| F-PitchChroma-Temporal.md | F | [49:65] | 16D | HIGH |
| G-RhythmGroove-Temporal.md | G | [65:75] | 10D | HIGH |
| H-HarmonyTonality-Temporal.md | H | [75:87] | 12D | HIGH |
| I-InformationSurprise-Temporal.md | I | [87:94] | 7D | MEDIUM-HIGH |
| J-TimbreExtended-Temporal.md | J | [94:114] | 20D | MEDIUM |
| K-ModulationPsychoacoustic-Temporal.md | K | [114:128] | 14D | MEDIUM |

**Impact summary**: Space grows 2.61× (112K → 294K), actual demand grows ~65% (~5.2K → ~8.6K). **ZERO code changes** to H³ engine itself — only C³ model DemandSpec tuples update.

---

## 52. H³ Pipeline (5 files)

| File | Content |
|------|---------|
| **ExecutionModel.md** | End-to-end flow with pseudocode and tensor shapes |
| **SparsityStrategy.md** | 97.1% savings, DemandTree structure, memory footprint |
| **Performance.md** | Per-horizon cost model, cost-by-band table, GPU strategy |
| **WarmUp.md** | Horizon-dependent warm-up: Micro(1-43 frames) → Ultra(168,999 frames) |

---

## 53. H³ Standards, Validation, Literature, Migration

### Standards/ (3 files)
- **MorphQualityTiers.md** — 24-morph × 4-band quality matrix (Reliable / Marginal / Unstable)
- **TemporalResolutionStandards.md** — Minimum frame counts per morph for numerical stability

### Validation/ (3 files)
- **AcceptanceCriteria.md** — Output range, per-morph synthetic inputs, law symmetry, kernel verification
- **BenchmarkPlan.md** — Synthetic test corpus, golden reference, regression suite, latency/memory targets

### Literature/ (2 files)
- **H3-LITERATURE.md** — Annotated bibliography: temporal processing, statistics, music time, attention, predictive coding

### Migration/ (3 files)
- **V1-to-V2.md** — H³ engine code unchanged v1→v2 (only DemandSpec tuples change)
- **DemandSpec-Update.md** — Detailed procedure for adding new r3_idx [49:127] to model demands

---

## 54. H³ Cross-Layer References

| From H³ → | Reference Type | Location |
|-----------|---------------|----------|
| → R³ | Feature indices consumed | `Docs/R³/Domains/{group}.md` |
| → C³ | Per-model demand tuples | `Docs/C³/Models/{ID}/{ACRONYM}.md` Section 5 |
| ← R³ | Expansion impact | `Docs/H³/Expansion/R3v2-H3-Impact.md` |
| ← C³ | Per-unit demand aggregation | `Docs/H³/Demand/{UNIT}-H3-DEMAND.md` |

---

---

# PART V — L³ Documentation Architecture

**Version**: 2.1.0
**Date**: 2026-02-13
**Total Files**: 73 markdown documents
**Layer**: L³ — Semantic Space ("What does it mean?")

---

## 55. L³ Overview

L³ is the semantic interpretation layer of MI. It transforms Brain output (1,026D) into a 104-dimensional semantic space organized into 8 epistemological groups (α-θ), producing human-interpretable descriptions of music perception.

**Pipeline position:**

```
Audio → Cochlea → R³ (128D) → H³ → Brain (1,026D) → [L³ 104D semantic] → MI-space
```

**Key metrics:**
- **Dimensions**: 104D total (α:6 + β:14 + γ:13 + δ:12 + ε:19 + ζ:12 + η:12 + θ:16)
- **Groups**: 8 (Greek letters α through θ)
- **Vocabulary**: 12 bipolar axes × 8 band terms = 96 unique terms
- **Gradation**: 64-level quantization per axis (72 bits total)
- **Learned parameters**: Zero (all computations are formula-based)
- **Stateful**: Only ε (epsilon) maintains state across frames

---

## 56. L³ Directory Tree

```
Docs/L³/                                    (73 files total)
├── 00-INDEX.md                              Root index
├── L3-SEMANTIC-ARCHITECTURE.md              Definitive architecture document
├── CHANGELOG.md                             Version history
├── EXTENSION-GUIDE.md                       How to add groups/axes
├── L³-AAC-SEMANTIC-SPACE.md                 Legacy root-level reference
├── L³-BRAIN-SEMANTIC-SPACE.md               Legacy root-level reference
├── L³-SRP-SEMANTIC-SPACE.md                 Legacy root-level reference
├── L³-VMM-SEMANTIC-SPACE.md                 Legacy root-level reference
│
├── Registry/                                (4 files)
│   ├── 00-INDEX.md
│   ├── DimensionCatalog.md                  All 104 dimensions with formulas
│   ├── GroupMap.md                           8 groups with index ranges
│   └── NamingConventions.md                 Dimension naming rules
│
├── Epistemology/                             (9 files)
│   ├── 00-INDEX.md                          8-level framework structure
│   ├── Computation.md                       Level 1 (α): Bayesian precision
│   ├── Neuroscience.md                      Level 2 (β): Mesolimbic pathway
│   ├── Psychology.md                        Level 3 (γ): ITPRA, circumplex
│   ├── Validation.md                        Level 4 (δ): Physiological prediction
│   ├── Learning.md                          Level 5 (ε): Free energy, stats learning
│   ├── Polarity.md                          Level 6 (ζ): Semantic differential
│   ├── Vocabulary.md                        Level 7 (η): Prototype theory, JND
│   └── Narrative.md                         Level 8 (θ): Musical narrative
│
├── Groups/                                  (10 files across 2 subdirs)
│   ├── 00-INDEX.md                          Master groups index
│   │
│   ├── Independent/                         (6 files)
│   │   ├── 00-INDEX.md
│   │   ├── Alpha.md                         α: Computation (6D)
│   │   ├── Beta.md                          β: Neuroscience (14D)
│   │   ├── Gamma.md                         γ: Psychology (13D)
│   │   ├── Delta.md                         δ: Validation (12D)
│   │   └── Epsilon.md                       ε: Learning (19D, STATEFUL)
│   │
│   └── Dependent/                           (4 files)
│       ├── 00-INDEX.md
│       ├── Zeta.md                          ζ: Polarity (12D, [-1,+1])
│       ├── Eta.md                           η: Vocabulary (12D)
│       └── Theta.md                         θ: Narrative (16D)
│
├── Vocabulary/                              (4 files)
│   ├── 00-INDEX.md
│   ├── AxisDefinitions.md                   12 bipolar axes
│   ├── GradationSystem.md                   64-level quantization design
│   └── TermCatalog.md                       12×8 = 96 unique terms
│
├── Contracts/                               (6 files)
│   ├── 00-INDEX.md
│   ├── BaseSemanticGroup.md                 ABC for all semantic groups
│   ├── SemanticGroupOutput.md               Output dataclass
│   ├── BaseModelSemanticAdapter.md          Per-unit adapter ABC
│   ├── L3Orchestrator.md                    Orchestrator contract
│   └── EpsilonStateContract.md              Stateful group lifecycle
│
├── Pipeline/                                (5 files)
│   ├── 00-INDEX.md
│   ├── DependencyDAG.md                     Phase 1→2 dependency graph
│   ├── ExecutionModel.md                    Step-by-step orchestrator flow
│   ├── Performance.md                       Per-group compute cost
│   └── StateManagement.md                   Epsilon state lifecycle
│
├── Adapters/                                (11 files)
│   ├── 00-INDEX.md
│   ├── SPU-L3-ADAPTER.md                    Spectral → beauty, complexity
│   ├── STU-L3-ADAPTER.md                    Timing → groove, arousal
│   ├── IMU-L3-ADAPTER.md                    Memory → stability
│   ├── ASU-L3-ADAPTER.md                    Salience → surprise
│   ├── NDU-L3-ADAPTER.md                    Novelty → surprise, tension
│   ├── MPU-L3-ADAPTER.md                    Motor → groove, motion
│   ├── PCU-L3-ADAPTER.md                    Prediction → surprise, stability
│   ├── ARU-L3-ADAPTER.md                    Affect → valence, tension
│   └── RPU-L3-ADAPTER.md                    Reward → wanting, liking
│
├── Standards/                               (3 files)
│   ├── 00-INDEX.md
│   ├── CitationQuality.md                   Per-dimension citation audit
│   └── PsychometricAlignment.md             GEMS, Russell, Osgood alignment
│
├── Validation/                              (3 files)
│   ├── 00-INDEX.md
│   ├── AcceptanceCriteria.md                Automated per-group validation
│   └── BenchmarkPlan.md                     Empirical validation plan
│
├── Literature/                              (2 files)
│   ├── 00-INDEX.md
│   └── L3-LITERATURE.md                     40+ references bibliography
│
├── Migration/                               (3 files)
│   ├── 00-INDEX.md
│   ├── V1-to-V2.md                          Per-model → unified Brain migration
│   └── DeprecatedFiles.md                   Archive inventory
│
└── Archive/                                 (5 files)
    ├── 00-INDEX.md
    ├── L3-AAC-SEMANTIC-SPACE.md             v1.2.0 (deprecated)
    ├── L3-BRAIN-SEMANTIC-SPACE.md           v2.0.0 (superseded)
    ├── L3-SRP-SEMANTIC-SPACE.md             v1.1.0 (deprecated)
    └── L3-VMM-SEMANTIC-SPACE.md             v1.0.0 (deprecated)
```

---

## 57. L³ File Count Summary

| Directory | Files | Content |
|-----------|:-----:|---------|
| Root | 8 | 00-INDEX, Architecture, Changelog, Extension Guide + 4 legacy refs |
| Registry/ | 4 | Dimension catalog, group map, naming conventions |
| Epistemology/ | 9 | 8-level framework (1 index + 8 per-level docs) |
| Groups/ | 10 | Master index + Independent(6) + Dependent(4) |
| Vocabulary/ | 4 | Axis definitions, gradation system, term catalog |
| Contracts/ | 6 | 5 interface contracts + index |
| Pipeline/ | 5 | DAG, execution, performance, state management |
| Adapters/ | 11 | 9 per-unit adapters + index + base adapter doc |
| Standards/ | 3 | Citation quality, psychometric alignment |
| Validation/ | 3 | Acceptance criteria, benchmark plan |
| Literature/ | 2 | 40+ references bibliography |
| Migration/ | 3 | V1→V2 guide, deprecated files |
| Archive/ | 5 | 4 deprecated semantic space docs + index |
| **Total** | **73** | |

---

## 58. L3-SEMANTIC-ARCHITECTURE.md — Definitive Architecture Document

Section headings (17 major sections):

1. **Design Philosophy** — Epistemological grounding, zero learned parameters, cascaded dependency
2. **Pipeline Position** — Brain (1,026D) → L³ (104D) → MI-space
3. **The 8 Semantic Groups** — Overview table, index ranges, audience map
4. **Group 1: Alpha (6D)** — Computation: Bayesian precision, attribution
5. **Group 2: Beta (14D)** — Neuroscience: Brain regions, neurotransmitter dynamics
6. **Group 3: Gamma (13D)** — Psychology: Reward, ITPRA, aesthetics, emotion, chills
7. **Group 4: Delta (12D)** — Validation: Physiological, neural, behavioral predictions
8. **Group 5: Epsilon (19D, STATEFUL)** — Learning: Surprise, prediction errors, precision
9. **Group 6: Zeta (12D)** — Polarity: 12 bipolar axes, [-1,+1] output
10. **Group 7: Eta (12D)** — Vocabulary: 64-gradation quantization, 96 terms
11. **Group 8: Theta (16D)** — Narrative: Subject/predicate/modifier/connector
12. **Computation Phases** — Phase 1 (α-ε) → Phase 2 (ζ→η→θ) cascade
13. **Unique Characteristics** — Stateful epsilon, linguistic pipeline, zero parameters
14. **Key Constants** — Architectural, state, vocabulary, theta constants
15. **Code Architecture** — File structure, module responsibilities
16. **References** — 10 core + 30 supplementary citations
17. **Cross-References** — Links to all L³ docs

---

## 59. The 8 Semantic Groups

### Computation Phases

```
brain_output ─────────┬──→ α (6D)
                      ├──→ β (14D)         Phase 1: Independent
                      ├──→ γ (13D)         (read only BrainOutput)
                      ├──→ δ (12D)
                      ├──→ ε (19D) ──┬──→ ζ (12D) ──┬──→ η (12D)
                      │     STATEFUL │               │         Phase 2: Dependent
                      │              └──────┬────────┘         (cascaded)
                      │                     ↓
                      └─────────────────→ θ (16D)
```

### Group Summary

| Group | Name | Dim | Phase | Audience | Key Theory |
|:-----:|------|:---:|:-----:|----------|------------|
| α | Computation | 6D | 1 | Engineers | Bayesian precision |
| β | Neuroscience | 14D | 1 | Neuroscientists | Mesolimbic pathway |
| γ | Psychology | 13D | 1 | Psychologists | ITPRA, circumplex affect |
| δ | Validation | 12D | 1 | Experimentalists | Physiological predictions |
| ε | Learning | 19D | 1b | Theorists | Free energy, statistical learning |
| ζ | Polarity | 12D | 2 | All | Semantic differential theory |
| η | Vocabulary | 12D | 2 | All | Prototype theory, JND |
| θ | Narrative | 16D | 2 | All | Musical narrative, cohesion |

### Group Details

**Alpha (α) — Computation (6D, variable in mi_beta)**
- Per-unit attribution scores
- Auto-configures dimension count from active model set
- Bayesian precision-weighted attribution

**Beta (β) — Neuroscience (14D, variable in mi_beta)**
- Brain region activation profiles
- Neurotransmitter dynamics (DA, 5-HT, opioid, NE)
- Circuit state indicators
- Auto-configures from registry

**Gamma (γ) — Psychology (13D)**
- Reward/punishment signals
- ITPRA (Imagination, Tension, Prediction, Reaction, Appraisal) mapping
- Aesthetic judgment, emotional valence/arousal
- Chills probability

**Delta (δ) — Validation (12D)**
- Testable physiological predictions (SCR, heart rate, pupil)
- Neural predictions (ERP components)
- Behavioral predictions (tapping deviation, attention shift)
- Temporal predictions (onset, peak, offset timing)

**Epsilon (ε) — Learning (19D, STATEFUL)**
- Surprise and entropy tracking
- Prediction errors across modalities
- Precision estimation
- Information dynamics (mutual info, conditional entropy)
- Uses EMA (exponential moving average) — **only stateful group**
- Requires `reset()` between audio files

**Zeta (ζ) — Polarity (12D, output [-1,+1])**
- Converts epsilon dimensions to 12 bipolar semantic axes
- Formula: `zeta_k = sign × (2 × epsilon_source - 1)`
- Unique: only group with [-1,+1] output (others are [0,1])

**Eta (η) — Vocabulary (12D)**
- Quantizes zeta's [-1,+1] to 64-gradation vocabulary terms
- 12 axes × 8 bands = 96 unique terms
- Band terms from negative to positive pole (e.g., "desolate" → "ecstatic")
- `get_terms()` method returns human-readable descriptors

**Theta (θ) — Narrative (16D)**
- Assembles words into sentences: Subject + Predicate + Modifier + Connector
- Subject (4D): What is being described
- Predicate (4D): What it is doing
- Modifier (4D): How/to what degree
- Connector (4D): Relationship to context

---

## 60. L³ Epistemology (9 files)

The epistemological framework provides the theoretical foundation for each group.

| File | Level | Group | Question | Audience |
|------|:-----:|:-----:|----------|----------|
| Computation.md | 1 | α | "How much does each unit contribute?" | Engineers |
| Neuroscience.md | 2 | β | "Which brain systems are active?" | Neuroscientists |
| Psychology.md | 3 | γ | "What emotional/aesthetic response?" | Psychologists |
| Validation.md | 4 | δ | "What measurable predictions follow?" | Experimentalists |
| Learning.md | 5 | ε | "What has the listener learned so far?" | Theorists |
| Polarity.md | 6 | ζ | "Is it positive or negative on each axis?" | All |
| Vocabulary.md | 7 | η | "What word describes each axis?" | All |
| Narrative.md | 8 | θ | "How can we describe the whole experience?" | All |

**Design principles**: Separation of concerns (each level independent), dependency ordering (Phase 1→2), audience targeting, falsifiability (δ exists solely for testable predictions).

---

## 61. L³ Vocabulary (4 files)

### The 12 Bipolar Axes

| # | Negative Pole | Positive Pole | Source Formula |
|:-:|:-------------:|:-------------:|----------------|
| 1 | harsh | beautiful | Consonance-weighted |
| 2 | simple | complex | Spectral centroid + entropy |
| 3 | still | groovy | Beat entrainment strength |
| 4 | calm | intense | Energy + arousal integration |
| 5 | stable | surprising | Prediction error magnitude |
| 6 | familiar | novel | Memory match score (inverted) |
| 7 | tense | resolved | Harmonic tension trajectory |
| 8 | sad | joyful | Valence + mode |
| 9 | static | dynamic | Spectral flux + change rate |
| 10 | forgettable | memorable | Distinctiveness score |
| 11 | repulsive | attractive | Approach motivation |
| 12 | boring | engaging | Attention capture + curiosity |

### 64-Gradation System

- **Bits per axis**: 6 (2⁶ = 64 levels)
- **Total bits**: 72 (12 axes × 6 bits)
- **JND rationale**: 64 levels ≈ 1.5% per step, below typical perceptual JND
- **Band structure**: 8 bands per axis (4 negative, 4 positive), each with a unique term
- **Total terms**: 12 × 8 = 96 unique vocabulary words

---

## 62. L³ Contracts (6 files)

| Contract | Type | Purpose |
|----------|:----:|---------|
| **BaseSemanticGroup** | ABC | Abstract base: LEVEL, GROUP_NAME, OUTPUT_DIM, `compute()` |
| **SemanticGroupOutput** | Dataclass | Output with tensor, dimension names, metadata |
| **BaseModelSemanticAdapter** | ABC | Per-unit adapter for semantic mapping |
| **L3Orchestrator** | Class | Dependency-ordered computation of all 8 groups |
| **EpsilonStateContract** | Spec | State lifecycle: accumulate, query, reset protocol |

### Orchestrator Execution Sequence

1. Phase 1 (parallel): α, β, γ, δ
2. Phase 1b: ε (stateful, reads only brain_output)
3. Phase 2a: ζ (reads ε output)
4. Phase 2b: η (reads ζ output)
5. Phase 2c: θ (reads ε + ζ outputs)
6. Concatenate: `torch.cat([α, β, γ, δ, ε, ζ, η, θ], dim=-1)` → (B, T, 104)

---

## 63. L³ Adapters (11 files)

Per-unit semantic adapters map model outputs to L³ interpretation vocabulary.

| File | Unit | Semantic Focus | Status |
|------|:----:|----------------|:------:|
| SPU-L3-ADAPTER.md | SPU | Consonance → beauty, timbre → complexity | Stub |
| STU-L3-ADAPTER.md | STU | Beat → groove, tempo → arousal | Stub |
| IMU-L3-ADAPTER.md | IMU | Familiarity → stability, recall → imagination | Stub |
| ASU-L3-ADAPTER.md | ASU | Novelty → surprise, attention → engagement | Stub |
| NDU-L3-ADAPTER.md | NDU | Deviation → surprise, PE → tension | Stub |
| MPU-L3-ADAPTER.md | MPU | Groove → groove, movement → motion | Stub |
| PCU-L3-ADAPTER.md | PCU | Prediction error → surprise, certainty → stability | Stub |
| ARU-L3-ADAPTER.md | ARU | Pleasure → valence, tension → tension, chills → beauty | Stub |
| RPU-L3-ADAPTER.md | RPU | DA → wanting, opioid → liking, reward PE → reward_pe | Stub |

All 9 adapters are currently stubs (return raw tensor). Real semantic mapping implementation is planned for Phase 7E.

---

## 64. L³ Pipeline (5 files)

| File | Content |
|------|---------|
| **DependencyDAG.md** | Phase 1 (α-δ parallel) → Phase 1b (ε) → Phase 2 (ζ→η→θ cascade) |
| **ExecutionModel.md** | Step-by-step orchestrator execution with tensor shapes |
| **Performance.md** | Per-group compute cost and memory analysis |
| **StateManagement.md** | Epsilon state lifecycle, reset protocol, memory footprint |

---

## 65. L³ Standards, Validation, Literature, Migration, Archive

### Standards/ (3 files)
- **CitationQuality.md** — Per-dimension citation audit (40+ unique citations across 4 evidence levels)
- **PsychometricAlignment.md** — Alignment with GEMS, Russell circumplex, Osgood EPA, ITPRA, Berlyne

### Validation/ (3 files)
- **AcceptanceCriteria.md** — Automated per-group output validation (shape, range, invariants)
- **BenchmarkPlan.md** — Empirical validation against human data (physiology, ratings, psychometrics)

Priority levels: P0 (shape/range), P1 (physiology), P2 (emotion), P3 (vocabulary), P4 (chills), P5 (learning)

### Literature/ (2 files)
- **L3-LITERATURE.md** — Per-dimension citation map + complete bibliography (40+ references across 9 categories)

### Migration/ (3 files)
- **V1-to-V2.md** — Per-model L³ (v1.x) → unified Brain L³ (v2.x) migration guide
- **DeprecatedFiles.md** — Archive inventory of old files and their replacements

Version history: v1.0.0 (VMM) → v1.1.0 (SRP) → v1.2.0 (AAC) → v2.0.0 (BRAIN) → v2.1.0 (Modular)

### Archive/ (5 files)
- **L3-VMM-SEMANTIC-SPACE.md** — v1.0.0 per-model semantic space (deprecated)
- **L3-SRP-SEMANTIC-SPACE.md** — v1.1.0 per-model semantic space (deprecated)
- **L3-AAC-SEMANTIC-SPACE.md** — v1.2.0 per-model semantic space (deprecated)
- **L3-BRAIN-SEMANTIC-SPACE.md** — v2.0.0 unified semantic space (superseded by modular docs)

---

## 66. L³ Code Correspondence

| Documentation | Code Package |
|---------------|-------------|
| `Docs/L³/Groups/Independent/*.md` | `mi_beta/language/groups/{alpha,beta,gamma,delta,epsilon}.py` |
| `Docs/L³/Groups/Dependent/*.md` | `mi_beta/language/groups/{zeta,eta,theta}.py` |
| `Docs/L³/Contracts/L3Orchestrator.md` | `mi_beta/language/groups/__init__.py` |
| `Docs/L³/Contracts/BaseSemanticGroup.md` | `mi_beta/contracts/base_semantic_group.py` |
| `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` | `mi_beta/language/adapters/{unit}_adapter.py` |
| `Docs/L³/Vocabulary/TermCatalog.md` | `mi_beta/language/groups/eta.py` (AXIS_TERMS) |
| `Docs/L³/Vocabulary/AxisDefinitions.md` | `mi_beta/language/groups/zeta.py` (POLARITY_AXES) |

---

## 67. L³ Cross-Layer References

| From L³ → | Reference Type | Location |
|-----------|---------------|----------|
| ← C³ | Per-unit brain output (input to L³) | `Docs/C³/Units/{UNIT}.md` |
| → C³ | Per-unit adapter mapping | `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` |
| ← Brain | BrainOutput dataclass | `mi_beta/core/types.py` |
