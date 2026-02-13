# MI-CODE-ARCHITECTURE.md

> **Scope**: Complete code-level architecture of the `mi_beta/` implementation.
> **Version**: 1.0.0 | **Date**: 2026-02-13 | **Status**: Phase 6 (pre-implementation reference)
> **Counterpart**: `MI-Doc/MI-DOC-ARCHITECTURE.md` (documentation-level architecture)

---

## Table of Contents

| # | Section | Scope | Lines |
|---|---------|-------|-------|
| 0 | [Document Metadata](#0-document-metadata) | Purpose, conventions, versioning | ~20 |
| 1 | [System Overview](#1-system-overview) | Pipeline, file tree, dependency graph | ~80 |
| 2 | [Core Module](#2-core-module) | constants.py, types.py, config.py, dimension_map.py | ~200 |
| 3 | [Cochlea](#3-cochlea) | Audio preprocessing, mel spectrogram | ~40 |
| 4 | [R3 Spectral Analysis](#4-r3-spectral-analysis) | R3Extractor, registry, 5 groups (49D) | ~200 |
| 5 | [H3 Temporal Context](#5-h3-temporal-context) | H3Extractor, morphs, horizons, attention, demand | ~180 |
| 6 | [Brain Orchestration](#6-brain-orchestration) | BrainOrchestrator, 5-phase pipeline | ~80 |
| 7 | [Contract ABCs](#7-contract-abcs) | BaseModel, BaseMechanism, BaseCognitiveUnit, etc. | ~200 |
| 8 | [Cognitive Units](#8-cognitive-units) | 9 units, 94 models, execution order | ~250 |
| 9 | [Mechanisms](#9-mechanisms) | 10 shared mechanisms (30D each) | ~80 |
| 10 | [Pathways](#10-pathways) | 5 cross-unit routes, PathwayRunner | ~60 |
| 11 | [Brain Regions & Neurochemicals](#11-brain-regions--neurochemicals) | RegionAtlas (26), NeurochemicalStateManager (4) | ~80 |
| 12 | [L3 Semantic Interpretation](#12-l3-semantic-interpretation) | L3Orchestrator, 8 groups (variable D) | ~200 |
| 13 | [Adapters](#13-adapters) | 9 unit-to-L3 adapter stubs | ~50 |
| 14 | [Pipeline](#14-pipeline) | MIBetaPipeline end-to-end | ~60 |
| 15 | [Tests](#15-tests) | Test directory structure | ~40 |
| 16 | [Known Discrepancies](#16-known-discrepancies) | Code vs docs delta (EXPECTED, CODE-BUG) | ~60 |
| 17 | [Phase 7 Roadmap](#17-phase-7-roadmap) | Implementation targets | ~40 |

---

## 0. Document Metadata

**Purpose**: This document is the single source of truth for `mi_beta/` code architecture. Every class, constant, signature, and data flow is documented here with exact values verified against the source code. During Phase 7 implementation, every code change must be traceable to a section in this document.

**Conventions**:
- All tensor shapes follow `(B, T, D)` unless noted: Batch, Time-frames, Dimensions
- File paths are relative to `/Volumes/SRC-9/SRC Musical Intelligence/`
- `[start:end)` denotes half-open intervals (start inclusive, end exclusive)
- Code blocks show exact class constants and method signatures from source
- "EXPECTED" = code intentionally behind docs (fix in Phase 7)
- "CODE-BUG" = code inconsistency to fix in Phase 7

**File Count**: 94 model files + ~40 infrastructure files = ~134 Python files total

---

## 1. System Overview

### 1.1 End-to-End Pipeline

```
Audio Waveform (B, samples)
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│  COCHLEA  audio_to_mel()                                 │
│  MelSpectrogram(sr=44100, n_fft=2048, hop=256, mels=128) │
│  → log1p → normalize                                     │
└────────────────────┬─────────────────────────────────────┘
                     │ (B, 128, T) mel
                     ▼
┌──────────────────────────────────────────────────────────┐
│  R3 EXTRACTOR  5 groups, auto-discovered                 │
│  A:Consonance(7) B:Energy(5) C:Timbre(9) D:Change(4)    │
│  E:Interactions(24)  = 49D total                         │
└────────────────────┬─────────────────────────────────────┘
                     │ (B, T, 49) R3
                     ▼
┌──────────────────────────────────────────────────────────┐
│  H3 EXTRACTOR  sparse, demand-driven                     │
│  32 horizons × 24 morphs × 3 laws = 2304 theoretical    │
│  Only demanded 4-tuples are computed                     │
└────────────────────┬─────────────────────────────────────┘
                     │ {(r3_idx, h, m, l): (B, T)} sparse dict
                     ▼
┌──────────────────────────────────────────────────────────┐
│  BRAIN ORCHESTRATOR  5-phase execution                   │
│  Phase 1: Mechanisms (skipped in current impl)           │
│  Phase 2: 7 independent units (SPU→PCU)                  │
│  Phase 3: 5 pathways route cross-unit signals            │
│  Phase 4: 2 dependent units (ARU, RPU)                   │
│  Phase 5: Assembly → BrainOutput                         │
│  94 models across 9 units                                │
└────────────────────┬─────────────────────────────────────┘
                     │ (B, T, brain_dim) variable
                     ▼
┌──────────────────────────────────────────────────────────┐
│  L3 ORCHESTRATOR  8 semantic groups                      │
│  α(var) β(var) γ(13) δ(12) ε(19) ζ(12) η(12) θ(16)     │
│  Phase 1: α,β,γ,δ → Phase 1b: ε → Phase 2: ζ→η→θ      │
└────────────────────┬─────────────────────────────────────┘
                     │ (B, T, l3_dim) variable
                     ▼
┌──────────────────────────────────────────────────────────┐
│  MI-SPACE ASSEMBLY                                       │
│  [cochlea(128) | r3(49) | brain(var) | l3(var)]          │
│  → MIBetaOutput with section ranges                      │
└──────────────────────────────────────────────────────────┘
```

### 1.2 File Tree

```
mi_beta/
├── __init__.py                    # __version__ = "0.1.0-beta"
├── __main__.py                    # CLI entry: python -m mi_beta
├── run.py                         # Quick-start runner
│
├── core/
│   ├── __init__.py
│   ├── constants.py               # SINGLE SOURCE OF TRUTH for all numerical constants
│   ├── types.py                   # Pipeline output dataclasses (B, T, D)
│   ├── config.py                  # MIBetaConfig dataclass + MI_BETA_CONFIG singleton
│   ├── dimension_map.py           # DimensionMap: name → global MI-space index
│   └── registry.py                # ModelRegistry: auto-discovers all models
│
├── ear/
│   ├── __init__.py
│   ├── cochlea.py                 # audio_to_mel() → CochleaOutput
│   ├── r3/
│   │   ├── __init__.py            # R3Extractor (orchestrator)
│   │   ├── _registry.py           # R3FeatureRegistry, R3FeatureMap, R3GroupInfo
│   │   ├── psychoacoustic/
│   │   │   ├── __init__.py        # exports: ConsonanceGroup
│   │   │   └── consonance.py      # Group A: 7D [0:7]
│   │   ├── dsp/
│   │   │   ├── __init__.py        # exports: EnergyGroup, TimbreGroup, ChangeGroup
│   │   │   ├── energy.py          # Group B: 5D [7:12]
│   │   │   ├── timbre.py          # Group C: 9D [12:21]
│   │   │   └── change.py          # Group D: 4D [21:25]
│   │   ├── cross_domain/
│   │   │   ├── __init__.py        # exports: InteractionsGroup
│   │   │   └── interactions.py    # Group E: 24D [25:49]
│   │   └── extensions/
│   │       ├── __init__.py        # __all__ = [] (empty, extensible)
│   │       └── _template.py       # Template for custom groups
│   └── h3/
│       ├── __init__.py            # H3Extractor (orchestrator)
│       ├── morph.py               # MorphComputer: 24 morphological features
│       ├── horizon.py             # EventHorizon: 32 time scales
│       ├── attention.py           # compute_attention_weights(): A(dt)=exp(-3|dt|/H)
│       └── demand.py              # DemandTree: sparse routing by horizon
│
├── contracts/
│   ├── __init__.py                # Re-exports all ABCs and dataclasses
│   ├── base_model.py              # BaseModel (ABC) — central model contract
│   ├── base_mechanism.py          # BaseMechanism (ABC)
│   ├── base_unit.py               # BaseCognitiveUnit (ABC)
│   ├── base_semantic_group.py     # BaseSemanticGroup (ABC)
│   ├── base_spectral_group.py     # BaseSpectralGroup (ABC)
│   ├── layer_spec.py              # LayerSpec (frozen dataclass)
│   ├── pathway_spec.py            # CrossUnitPathway (frozen dataclass)
│   ├── demand_spec.py             # H3DemandSpec (frozen dataclass)
│   ├── model_metadata.py          # Citation, ModelMetadata (frozen dataclasses)
│   ├── brain_region.py            # BrainRegion (frozen dataclass)
│   ├── neurochemical.py           # NeurochemicalType (Enum), NeurochemicalState
│   └── feature_spec.py            # R3FeatureSpec (frozen dataclass)
│
├── brain/
│   ├── __init__.py
│   ├── units/
│   │   ├── __init__.py            # UnitRunner, UNIT_CLASSES, ALL_UNIT_NAMES
│   │   ├── spu/                   # Spectral Processing Unit
│   │   │   ├── __init__.py
│   │   │   ├── _unit.py           # SPUUnit(BaseCognitiveUnit)
│   │   │   └── models/            # 9 models: BCH, PSCL, PCCR, STAI, TSCP, MIAA, SDNPS, ESME, SDED
│   │   │       ├── __init__.py
│   │   │       └── *.py           # (9 files)
│   │   ├── stu/                   # Sensorimotor Timing Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 14 models: HMCE, AMSC, MDNS, AMSS, TPIO, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MTNE, PTGMP, MPFS
│   │   │       └── *.py           # (14 files)
│   │   ├── imu/                   # Integrative Memory Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 15 models: MEAMN, PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, MSPBA, VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM
│   │   │       └── *.py           # (15 files)
│   │   ├── asu/                   # Auditory Salience Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 9 models: SNEM, IACM, CSG, BARM, STANM, AACM, PWSM, DGTP, SDL
│   │   │       └── *.py           # (9 files)
│   │   ├── ndu/                   # Novelty Detection Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 9 models: MPG, SDD, EDNR, DSP_, CDMR, SLEE, SDDP, ONI, ECT
│   │   │       └── *.py           # (9 files)
│   │   ├── mpu/                   # Motor Planning Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 10 models: PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC
│   │   │       └── *.py           # (10 files)
│   │   ├── pcu/                   # Predictive Coding Unit
│   │   │   ├── _unit.py
│   │   │   └── models/            # 9 models: SPH, ICEM, PWUP, WMED, UDP, IGFE, MAA, PSH, HTP
│   │   │       └── *.py           # (9 files)
│   │   ├── aru/                   # Affective Resonance Unit (DEPENDENT)
│   │   │   ├── _unit.py
│   │   │   └── models/            # 10 models: SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR
│   │   │       └── *.py           # (10 files)
│   │   └── rpu/                   # Reward Processing Unit (DEPENDENT)
│   │       ├── _unit.py
│   │       └── models/            # 9 models: DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, IOTMS, SSPS
│   │           └── *.py           # (9 files)
│   │
│   ├── mechanisms/
│   │   ├── __init__.py            # MechanismRunner, registry
│   │   ├── aed.py                 # Affective Entrainment Dynamics
│   │   ├── asa.py                 # Auditory Scene Analysis
│   │   ├── bep.py                 # Beat Entrainment Processing
│   │   ├── c0p.py                 # Cognitive Projection
│   │   ├── cpd.py                 # Chills & Peak Detection
│   │   ├── mem.py                 # Memory Encoding / Retrieval
│   │   ├── ppc.py                 # Pitch Processing Chain
│   │   ├── syn.py                 # Syntactic Processing
│   │   ├── tmh.py                 # Temporal Memory Hierarchy
│   │   └── tpc.py                 # Timbre Processing Chain
│   │
│   ├── pathways/
│   │   ├── __init__.py            # PathwayRunner, ALL_PATHWAYS
│   │   ├── p1_spu_aru.py
│   │   ├── p2_stu_internal.py
│   │   ├── p3_imu_aru.py
│   │   ├── p4_stu_internal.py
│   │   └── p5_stu_aru.py
│   │
│   ├── regions/
│   │   ├── __init__.py            # RegionAtlas, ATLAS singleton
│   │   ├── subcortical.py         # 9 subcortical regions
│   │   ├── cortical.py            # 12 cortical regions
│   │   └── brainstem.py           # 5 brainstem regions
│   │
│   └── neurochemicals/
│       ├── __init__.py            # NeurochemicalStateManager
│       ├── dopamine.py
│       ├── opioid.py
│       ├── serotonin.py
│       └── norepinephrine.py
│
├── language/
│   ├── __init__.py
│   ├── groups/
│   │   ├── __init__.py            # L3Orchestrator
│   │   ├── alpha.py               # AlphaGroup: Unit Attribution (variable D)
│   │   ├── beta.py                # BetaGroup: Region Activation (variable D)
│   │   ├── gamma.py               # GammaGroup: Psychological (13D)
│   │   ├── delta.py               # DeltaGroup: Observable (12D)
│   │   ├── epsilon.py             # EpsilonGroup: Learning (19D, STATEFUL)
│   │   ├── zeta.py                # ZetaGroup: Polarity (12D, [-1,+1])
│   │   ├── eta.py                 # EtaGroup: Vocabulary (12D, 64-gradation)
│   │   └── theta.py               # ThetaGroup: Narrative (16D)
│   └── adapters/
│       ├── __init__.py
│       ├── _base_adapter.py       # BaseModelSemanticAdapter (ABC)
│       ├── aru_adapter.py         # stub
│       ├── asu_adapter.py         # stub
│       ├── imu_adapter.py         # stub
│       ├── mpu_adapter.py         # stub
│       ├── ndu_adapter.py         # stub
│       ├── pcu_adapter.py         # stub
│       ├── rpu_adapter.py         # stub
│       ├── spu_adapter.py         # stub
│       └── stu_adapter.py         # stub
│
├── pipeline/
│   ├── __init__.py                # exports: BrainOrchestrator, MIBetaPipeline
│   ├── brain_runner.py            # BrainOrchestrator (5-phase)
│   └── mi_beta.py                 # MIBetaPipeline (end-to-end)
│
tests/
├── __init__.py
├── conftest.py                    # pytest fixtures
├── unit/
│   ├── core/
│   │   ├── test_config.py
│   │   └── test_constants.py
│   ├── ear/
│   │   ├── test_cochlea.py
│   │   ├── test_r3.py
│   │   └── test_h3.py
│   ├── brain/
│   │   └── test_musical_brain.py
│   └── language/
│       └── test_brain_semantics.py
├── integration/
│   └── test_pipeline.py
└── validation/
    └── test_chill_test.py
```

### 1.3 Dependency Graph

```
core/constants.py ◄── core/types.py
       │                    │
       ▼                    ▼
core/config.py ◄── contracts/*.py ◄── ear/r3/ ◄── ear/h3/
       │                    │                         │
       │                    ▼                         │
       │            brain/units/*/models/*.py ◄───────┘
       │                    │
       │                    ▼
       │            brain/units/*/_unit.py
       │                    │
       │                    ▼
       │            brain/mechanisms/*.py
       │                    │
       │                    ▼
       └──────────► pipeline/brain_runner.py
                            │
                            ▼
                    language/groups/__init__.py (L3Orchestrator)
                            │
                            ▼
                    pipeline/mi_beta.py (MIBetaPipeline)
                            │
                            ▼
                    core/dimension_map.py (DimensionMap)
```

### 1.4 Key Numerical Summary

| Component | Count | Dimension |
|-----------|------:|----------:|
| Model files (.py) | 94 | — |
| Cognitive units | 9 | — |
| Mechanisms | 10 | 30D each |
| Pathways | 5 | — |
| Brain regions | 26 | — |
| Neurochemical systems | 4 | — |
| R3 spectral groups | 5 | 49D total |
| H3 horizons | 32 | 5.8ms–981s |
| H3 morphs | 24 | — |
| H3 laws | 3 | — |
| L3 semantic groups | 8 | variable |
| L3 adapters | 9 | stub |
| Contracts (ABCs) | 5 | — |
| Spec dataclasses | 7 | — |
| Output dataclasses | 9 | — |

---

## 2. Core Module

**Location**: `mi_beta/core/`

### 2.1 constants.py — Single Source of Truth

All numerical constants for the MI-Beta system. Changing a value here propagates everywhere.

#### Audio Constants

| Constant | Value | Description |
|----------|------:|-------------|
| `SAMPLE_RATE` | 44,100 | Hz |
| `HOP_LENGTH` | 256 | samples per frame |
| `FRAME_RATE` | 172.265625 | Hz (SAMPLE_RATE / HOP_LENGTH) |
| `FRAME_DURATION_MS` | ~5.805 | ms per frame |
| `N_FFT` | 2,048 | FFT window size |
| `N_MELS` | 128 | mel filterbank bins |

#### R3 Spectral Constants

| Constant | Value | Description |
|----------|------:|-------------|
| `R3_DIM` | 49 | Total R3 features per frame |
| `R3_CONSONANCE` | (0, 7) | Group A: 7D |
| `R3_ENERGY` | (7, 12) | Group B: 5D |
| `R3_TIMBRE` | (12, 21) | Group C: 9D |
| `R3_CHANGE` | (21, 25) | Group D: 4D |
| `R3_INTERACTIONS` | (25, 49) | Group E: 24D |

#### H3 Temporal Constants

| Constant | Value | Description |
|----------|------:|-------------|
| `N_HORIZONS` | 32 | Number of temporal horizons |
| `N_MORPHS` | 24 | Number of morphological features |
| `N_LAWS` | 3 | Temporal perspectives (memory, prediction, integration) |
| `H3_TOTAL_DIM` | 2,304 | 32 × 24 × 3 theoretical space |
| `ATTENTION_DECAY` | 3.0 | Exponential decay constant |

#### HORIZON_MS (32 horizons, exact values)

```python
HORIZON_MS = (
    5.8, 11.6, 17.4, 23.2, 34.8, 46.4,       # H0-H5:   sub-beat
    200, 250, 300, 350, 400, 450,               # H6-H11:  beat
    525, 600, 700, 800, 1000, 1500,             # H12-H17: beat-phrase
    2000, 3000, 5000, 8000, 15000, 25000,       # H18-H23: phrase-section
    36000, 60000, 120000, 200000, 414000,       # H24-H28: section-form
    600000, 800000, 981000,                      # H29-H31: piece
)
```

#### MORPH_NAMES (24 morphs, exact values)

| M# | Name | Description |
|---:|------|-------------|
| 0 | `value` | Attention-weighted mean |
| 1 | `mean` | Unweighted mean |
| 2 | `std` | Standard deviation |
| 3 | `median` | Median |
| 4 | `max` | Maximum |
| 5 | `range` | Max - Min |
| 6 | `skewness` | Distribution skew |
| 7 | `kurtosis` | Distribution peakedness |
| 8 | `velocity` | First derivative (dR3/dt) |
| 9 | `velocity_mean` | Mean of velocity |
| 10 | `velocity_std` | Velocity variance (jerk proxy) |
| 11 | `acceleration` | Second derivative |
| 12 | `acceleration_mean` | Mean acceleration |
| 13 | `acceleration_std` | Acceleration variance |
| 14 | `periodicity` | Autocorrelation peak |
| 15 | `smoothness` | 1/(1+\|jerk\|/sigma) |
| 16 | `curvature` | Spectral curvature |
| 17 | `shape_period` | Oscillation period |
| 18 | `trend` | Linear regression slope |
| 19 | `stability` | 1/(1+var/sigma^2) |
| 20 | `entropy` | Shannon entropy |
| 21 | `zero_crossings` | Sign change count |
| 22 | `peaks` | Local maxima count |
| 23 | `symmetry` | Forward/backward symmetry |

#### LAW_NAMES (3 laws)

| L# | Name | Window Direction |
|---:|------|-----------------|
| 0 | `memory` | Past → Now (causal) |
| 1 | `prediction` | Now → Future |
| 2 | `integration` | Past ↔ Future (bidirectional) |

#### MORPH_SCALE (24 × (gain, bias) pairs)

```python
MORPH_SCALE = (
    (6.0, 0.5),      # M0  value         [0,1] level
    (6.0, 0.5),      # M1  mean           [0,1] level
    (40.0, 0.0),     # M2  std            small positive
    (6.0, 0.5),      # M3  median         [0,1] level
    (6.0, 0.5),      # M4  max            [0,1] level
    (10.0, 0.25),    # M5  range          [0, ~0.5]
    (3.0, 0.0),      # M6  skewness       centered ~0
    (1.5, 0.0),      # M7  kurtosis       centered ~0
    (300.0, 0.0),    # M8  velocity       ~±0.003 std
    (300.0, 0.0),    # M9  velocity_mean  ~±0.003 std
    (200.0, 0.0),    # M10 velocity_std   small positive
    (500.0, 0.0),    # M11 acceleration   ~±0.001 std
    (500.0, 0.0),    # M12 accel_mean     near-zero
    (400.0, 0.0),    # M13 accel_std      near-zero positive
    (6.0, 0.5),      # M14 periodicity    [0,1] level
    (6.0, 0.5),      # M15 smoothness     (0,1]
    (200.0, 0.0),    # M16 curvature      small positive
    (6.0, 0.5),      # M17 shape_period   sigmoid-mapped
    (1000.0, 0.0),   # M18 trend          ~±0.0005 std slope
    (6.0, 0.5),      # M19 stability      (0,1]
    (6.0, 0.5),      # M20 entropy        [0,1]
    (6.0, 0.5),      # M21 zero_crossings [0,1]
    (6.0, 0.5),      # M22 peaks          [0,1]
    (6.0, 0.5),      # M23 symmetry       (0,1]
)
```

**Scaling formula**: `scale_h3_value(value, morph) = gain * (value - bias)`

#### Brain Architecture Constants

| Constant | Value | Description |
|----------|------:|-------------|
| `MECHANISM_DIM` | 30 | Standard mechanism output size |
| `UNIT_EXECUTION_ORDER` | `("SPU","STU","IMU","ASU","NDU","MPU","PCU","ARU","RPU")` | Dependency-resolved order |
| `ALL_UNIT_NAMES` | same as above | Alias |
| `MODEL_TIERS` | `("alpha","beta","gamma")` | Evidence confidence levels |

#### Circuit Constants

| Constant | Type | Values | Note |
|----------|------|--------|------|
| `CIRCUIT_NAMES` | 6-tuple | mesolimbic, perceptual, sensorimotor, mnemonic, salience, **imagery** | |
| `CIRCUITS` | 5-tuple | perceptual, sensorimotor, mnemonic, mesolimbic, salience | **Missing "imagery"** |
| `N_CIRCUITS` | int | 5 | Based on `CIRCUITS` |

> **CODE-BUG**: `CIRCUIT_NAMES` has 6 entries (includes "imagery"), `CIRCUITS` has 5 (excludes "imagery"). Phase 7A will reconcile.

#### Neuroscience Coefficients

| Constant | Value | Source |
|----------|------:|--------|
| `BETA_NACC` | 0.84 | NAcc binding potential ↔ pleasure (Salimpoor 2011) |
| `BETA_CAUDATE` | 0.71 | Caudate binding potential ↔ chills (Salimpoor 2011) |

#### Helper Functions

```python
def h3_flat_index(horizon: int, morph: int, law: int) -> int:
    """Flat index into 2304D H3 space: h*72 + m*3 + l."""

def scale_h3_value(value: Tensor, morph: int) -> Tensor:
    """Scale H3 value by morph's gain and bias. (B, T) → (B, T)"""
```

### 2.2 types.py — Pipeline Output Dataclasses

All tensors follow `(B, T, D)` convention unless noted.

#### Ear Outputs

| Dataclass | Fields | Shape |
|-----------|--------|-------|
| `CochleaOutput` | `mel`, `sample_rate`, `hop_length` | mel: `(B, 128, T)` |
| `R3Output` | `features`, `feature_names` | features: `(B, T, 49)` |
| `H3Output` | `features: Dict[4-tuple, Tensor]` | per-entry: `(B, T)` |
| `EarOutput` | `cochlea`, `r3`, `h3` | compound |

#### Brain Outputs

| Dataclass | Fields | Shape |
|-----------|--------|-------|
| `ModelOutput` | `name`, `unit`, `tier`, `tensor`, `dimension_names`, `h3_demand` | tensor: `(B, T, output_dim)` |
| `UnitOutput` | `unit_name`, `tensor`, `model_outputs`, `model_ranges`, `dimension_names` | tensor: `(B, T, unit_dim)` |
| `BrainOutput` | `tensor`, `unit_outputs`, `unit_ranges`, `dimension_names` | tensor: `(B, T, brain_dim)` |

**BrainOutput accessor methods**:
- `get_unit(unit_name) → Tensor` — extract unit slice
- `get_model(unit_name, model_name) → Tensor` — extract model slice (computes global offset)
- `get_dim(name) → Tensor` — extract single dimension by name

#### Language Outputs

| Dataclass | Fields | Shape |
|-----------|--------|-------|
| `SemanticGroupOutput` | `group_name`, `level`, `tensor`, `dimension_names` | tensor: `(B, T, dim)` |
| `L3Output` | `model_name`, `groups`, `tensor` | tensor: `(B, T, total_dim)` |

#### Pipeline Output

```python
@dataclass
class MIBetaOutput:
    mi_space: Tensor                              # (B, T, total_dim)
    cochlea_range: Tuple[int, int]                # always (0, 128)
    r3_range: Tuple[int, int]                     # (128, 128+r3_dim)
    brain_range: Tuple[int, int]                  # (r3_end, r3_end+brain_dim)
    l3_range: Optional[Tuple[int, int]] = None    # (brain_end, total) or None
    brain: Optional[BrainOutput] = None
    semantics: Optional[L3Output] = None
    ear: Optional[EarOutput] = None
```

**MIBetaOutput accessor properties**: `cochlea`, `r3`, `brain_tensor`, `l3`, `total_dim`

### 2.3 config.py — Runtime Configuration

```python
@dataclass
class MIBetaConfig:
    # Audio
    sample_rate: int = 44_100
    hop_length: int = 256
    n_fft: int = 2048
    n_mels: int = 128

    # R3 groups
    r3_groups: Tuple[str, ...] = ("consonance", "energy", "timbre", "change", "interactions")

    # Brain control
    active_units: Optional[Tuple[str, ...]] = None    # None = all 9 units
    active_models: Optional[Tuple[str, ...]] = None   # None = all models

    # Mechanism
    mechanism_dim: int = 30

    # Device
    device: str = "cpu"

    # Streaming
    streaming: bool = False
    chunk_size: Optional[int] = None

# Singleton
MI_BETA_CONFIG = MIBetaConfig()
```

**Validation**: `__post_init__` validates `active_units` against `UNIT_EXECUTION_ORDER`.

**Computed properties**: `frame_rate`, `r3_dim`, `cochlea_dim`, `is_unit_active()`, `is_model_active()`

### 2.4 dimension_map.py — MI-Space Index Tracking

Maps every named dimension to its global index in the assembled MI-space vector.

#### _R3_FEATURE_NAMES (49 canonical names)

```python
_R3_FEATURE_NAMES = (
    # Group A: Consonance (7D)
    "perfect_fifth_ratio", "euler_gradus", "harmonicity",
    "stumpf_fusion", "sensory_pleasantness", "roughness_total", "consonance_mean",
    # Group B: Energy (5D)
    "velocity_A", "velocity_D", "loudness", "onset_strength", "rms_energy",
    # Group C: Timbre (9D)
    "warmth", "sharpness", "brightness_kuttruff",
    "brightness", "spectral_centroid", "spectral_bandwidth",
    "tristimulus1", "tristimulus2", "tristimulus3",
    # Group D: Change (4D)
    "spectral_flux", "spectral_flatness", "zero_crossing_rate", "tonalness",
    # Group E: Interactions (24D)
    "cons_x_energy", "cons_x_timbre", "cons_x_change",
    "energy_x_timbre", "energy_x_change", "timbre_x_change",
    "cons_x_energy_x_timbre", "cons_x_energy_x_change",
    "cons_x_timbre_x_change", "energy_x_timbre_x_change",
    "cons_x_energy_x_timbre_x_change",
    "cons_variance", "energy_variance", "timbre_variance", "change_variance",
    "consonance_delta", "energy_delta", "timbre_delta", "change_delta",
    "cons_energy_ratio", "cons_timbre_ratio", "energy_timbre_ratio",
    "harmonic_tension", "spectral_complexity",
)
```

> **Note**: These names differ from R3 group `feature_names` properties (which use computational names like `roughness`, `sethares_dissonance`, etc.). The dimension_map names are the _canonical MI-space names_, while the R3 group names are the _internal computational names_. This is a known discrepancy documented in DISCREPANCY-REGISTRY.md.

#### DimensionMap class

```python
class DimensionMap:
    def __init__(self, registry, assembler, r3_feature_names=None, l3_dimension_names=None)

    # Index queries
    def index_of(self, name: str) -> int
    def indices_of(self, names: List[str]) -> List[int]

    # Range queries
    def range_of(self, model_name: str) -> Tuple[int, int]       # model range
    def range_of_unit(self, unit_name: str) -> Tuple[int, int]   # unit range
    def range_of_section(self, section: str) -> Tuple[int, int]  # cochlea/r3/brain/l3

    # Name queries
    def all_names(self) -> List[str]
    def names_of_model(self, model_name: str) -> List[str]
    def names_of_unit(self, unit_name: str) -> List[str]
    def search(self, pattern: str) -> List[Tuple[str, int]]      # substring search
```

**Naming convention in MI-space**: `{section}_{model}_{dim}` e.g., `r3_stumpf_fusion`, `aru_pupf_pleasure`

**MI-space layout**: `[mel_0..mel_127 | r3_name_0..r3_name_48 | brain_dims... | l3_dims...]`

---

## 3. Cochlea

**File**: `mi_beta/ear/cochlea.py`

### 3.1 audio_to_mel()

```python
def audio_to_mel(
    waveform: Tensor,                       # (B, samples) or (samples,)
    config: MIBetaConfig = MI_BETA_CONFIG,
) -> CochleaOutput:
```

**Pipeline**:
1. **Input normalization**: Ensure batch dimension `(B, samples)`, enforce mono by averaging channels
2. **MelSpectrogram**: `torchaudio.transforms.MelSpectrogram(sample_rate=44100, n_fft=2048, hop_length=256, n_mels=128, power=2.0)`
3. **Log normalization**: `torch.log1p(mel)`
4. **Per-batch normalization**: Divide by max across `(F, T)` to `[0, 1]`

**Output**: `CochleaOutput(mel=(B, 128, T), sample_rate=44100, hop_length=256)`

**Frame rate**: 172.27 Hz → ~5.805 ms per frame

---

## 4. R3 Spectral Analysis

**Location**: `mi_beta/ear/r3/`

### 4.1 R3Extractor (Orchestrator)

**File**: `mi_beta/ear/r3/__init__.py`

```python
class R3Extractor:
    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None
    def extract(self, mel: Tensor) -> R3Output        # (B, 128, T) → R3Output(B, T, 49)
    @property
    def feature_map(self) -> R3FeatureMap              # frozen metadata
    @property
    def feature_names(self) -> List[str]               # 49 names from groups
    @property
    def total_dim(self) -> int                         # 49
```

**Auto-discovery process**:
1. Scans subdirectories in order: `("psychoacoustic", "dsp", "cross_domain", "extensions")`
2. Imports each subdir's `__init__.py`
3. Collects `BaseSpectralGroup` subclasses from `__all__` list
4. Instantiates each group → registers in R3FeatureRegistry
5. `freeze()` assigns contiguous INDEX_RANGE to each group

**Extract flow**: Iterates registered groups, calls `group.compute(mel)`, concatenates along dim=-1.

### 4.2 R3FeatureRegistry

**File**: `mi_beta/ear/r3/_registry.py`

```python
class R3FeatureRegistry:
    def register(self, group: BaseSpectralGroup) -> None  # append; raises if frozen
    def freeze(self) -> R3FeatureMap                      # assign INDEX_RANGEs, return map
    @property
    def groups(self) -> List[BaseSpectralGroup]

@dataclass(frozen=True)
class R3GroupInfo:
    name: str                  # "consonance"
    dim: int                   # 7
    start: int                 # 0
    end: int                   # 7
    feature_names: Tuple[str, ...]

@dataclass(frozen=True)
class R3FeatureMap:
    total_dim: int             # 49
    groups: Tuple[R3GroupInfo, ...]
```

### 4.3 BaseSpectralGroup (Contract)

**File**: `mi_beta/contracts/base_spectral_group.py`

```python
class BaseSpectralGroup(ABC):
    GROUP_NAME: str                        # "consonance"
    DOMAIN: str                            # "psychoacoustic"
    OUTPUT_DIM: int                        # 7
    INDEX_RANGE: Tuple[int, int]           # (0, 7) — assigned by registry.freeze()

    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor:   # (B, N_MELS, T) → (B, T, OUTPUT_DIM)
    @property
    @abstractmethod
    def feature_names(self) -> List[str]:        # len == OUTPUT_DIM

    @property
    def start_index(self) -> int
    @property
    def end_index(self) -> int
    def validate(self) -> list[str]
```

### 4.4 Group A: ConsonanceGroup (7D) [0:7]

**File**: `mi_beta/ear/r3/psychoacoustic/consonance.py`

| # | Feature Name | Algorithm |
|--:|-------------|-----------|
| 0 | `roughness` | `sigmoid(var(high_bins) / mean - 0.5)` where high_bins = mel[N/2:] |
| 1 | `sethares_dissonance` | `mean(\|diff\|) / max` — adjacent bin interference |
| 2 | `helmholtz_kang` | Spectral autocorrelation at lag-1 (normalized, clamped [0,1]) |
| 3 | `stumpf_fusion` | `sum(low_bins) / sum(all)` — low-freq energy ratio |
| 4 | `sensory_pleasantness` | `0.6 * smoothness + 0.4 * stumpf` |
| 5 | `inharmonicity` | `1.0 - helmholtz` |
| 6 | `harmonic_deviation` | `0.5 * sethares + 0.5 * inharmonicity` |

All outputs clamped to [0, 1]. Helper: `_spectral_autocorrelation()` for lag-1 centered autocorrelation.

### 4.5 Group B: EnergyGroup (5D) [7:12]

**File**: `mi_beta/ear/r3/dsp/energy.py`

| # | Feature Name | Algorithm |
|--:|-------------|-----------|
| 0 | `amplitude` | `sqrt(mean(mel^2))` normalized by max across time |
| 1 | `velocity_A` | `sigmoid(5.0 * diff(amplitude))` |
| 2 | `acceleration_A` | `sigmoid(5.0 * diff(velocity, lag=2))` |
| 3 | `loudness` | `amplitude^0.3` (Stevens' power law), normalized |
| 4 | `onset_strength` | `sum(max(0, diff(mel)))` normalized |

### 4.6 Group C: TimbreGroup (9D) [12:21]

**File**: `mi_beta/ear/r3/dsp/timbre.py`

| # | Feature Name | Algorithm |
|--:|-------------|-----------|
| 0 | `warmth` | `sum(mel[:N/4]) / total` |
| 1 | `sharpness` | `sum(mel[3N/4:]) / total` |
| 2 | `tonalness` | `max(mel) / total` |
| 3 | `clarity` | `(mel * bin_idx).sum() / total / N` (spectral centroid) |
| 4 | `spectral_smoothness` | `1 - (mean_diff / max_diff)` |
| 5 | `spectral_autocorrelation` | Lag-1 centered autocorrelation [0,1] |
| 6 | `tristimulus1` | Energy in [0, N/3) |
| 7 | `tristimulus2` | Energy in [N/3, 2N/3) |
| 8 | `tristimulus3` | Energy in [2N/3, N) |

### 4.7 Group D: ChangeGroup (4D) [21:25]

**File**: `mi_beta/ear/r3/dsp/change.py`

| # | Feature Name | Algorithm |
|--:|-------------|-----------|
| 0 | `spectral_flux` | `norm(mel[t] - mel[t-1])` normalized by max |
| 1 | `distribution_entropy` | `-(prob * log(prob)).sum()` normalized by log(N) |
| 2 | `distribution_flatness` | `exp(mean(log(prob))) / mean(prob)` (Wiener entropy) |
| 3 | `distribution_concentration` | `sum(prob^2) * N` (Herfindahl index) clamped [0,1] |

### 4.8 Group E: InteractionsGroup (24D) [25:49]

**File**: `mi_beta/ear/r3/cross_domain/interactions.py`

3 blocks of 8 features = 24D total. All are element-wise products of proxy features from other groups, clamped [0, 1].

**Block 1: Energy × Consonance (8D) [25:33]**

| # | Feature Name |
|--:|-------------|
| 0 | `x_amp_roughness` |
| 1 | `x_amp_sethares` |
| 2 | `x_amp_helmholtz` |
| 3 | `x_amp_stumpf` |
| 4 | `x_vel_roughness` |
| 5 | `x_vel_sethares` |
| 6 | `x_vel_helmholtz` |
| 7 | `x_vel_stumpf` |

**Block 2: Change × Consonance (8D) [33:41]**

| # | Feature Name |
|--:|-------------|
| 0 | `x_flux_roughness` |
| 1 | `x_flux_sethares` |
| 2 | `x_flux_helmholtz` |
| 3 | `x_flux_stumpf` |
| 4 | `x_entropy_roughness` |
| 5 | `x_entropy_sethares` |
| 6 | `x_entropy_helmholtz` |
| 7 | `x_entropy_stumpf` |

**Block 3: Consonance × Timbre (8D) [41:49]**

| # | Feature Name |
|--:|-------------|
| 0 | `x_roughness_warmth` |
| 1 | `x_roughness_sharpness` |
| 2 | `x_sethares_warmth` |
| 3 | `x_sethares_sharpness` |
| 4 | `x_helmholtz_tonalness` |
| 5 | `x_helmholtz_clarity` |
| 6 | `x_stumpf_smoothness` |
| 7 | `x_stumpf_autocorr` |

### 4.9 R3 Extension Mechanism

**File**: `mi_beta/ear/r3/extensions/_template.py`

To add a custom R3 group:
1. Create new `.py` file in any R3 subdirectory (or `extensions/`)
2. Subclass `BaseSpectralGroup`
3. Define `GROUP_NAME`, `OUTPUT_DIM`, `feature_names`, `compute()`
4. Export from subdirectory `__init__.py` via `__all__`
5. R3Extractor auto-discovers and registers at init time
6. `INDEX_RANGE` assigned automatically by `freeze()`

---

## 5. H3 Temporal Context

**Location**: `mi_beta/ear/h3/`

### 5.1 H3Extractor (Orchestrator)

**File**: `mi_beta/ear/h3/__init__.py`

```python
class H3Extractor:
    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None
    def extract(
        self,
        r3: Tensor,                                     # (B, T, 49)
        demand: Set[Tuple[int, int, int, int]],          # {(r3_idx, h, m, l), ...}
    ) -> H3Output                                        # {4-tuple: (B, T)}
```

**Demand format**: Each 4-tuple `(r3_idx, horizon, morph, law)` specifies:
- `r3_idx`: Which R3 feature to track (0-48)
- `horizon`: Time scale index (0-31)
- `morph`: Morphological feature (0-23)
- `law`: Temporal perspective (0=memory, 1=prediction, 2=integration)

**Algorithm**:
1. Build `DemandTree`: group 4-tuples by horizon index
2. For each horizon:
   - Compute `EventHorizon(h).frames` → window size
   - Compute `attention_weights(n_frames)` → `(n_frames,)` exponential weights
   - For each `(r3_idx, m, l)` triple in this horizon:
     - Extract scalar time series: `r3[..., r3_idx]` → `(B, T)`
     - Call `_compute_morph_series()` → `(B, T)`
3. Return `H3Output` dict mapping 4-tuple to `(B, T)` tensor

### 5.2 _compute_morph_series() — Core Windowed Computation

```python
def _compute_morph_series(
    self, r3_scalar, B, T, n_frames, m_idx, l_idx, weights, device, dtype
) -> Tensor:  # (B, T)
```

For each frame `t` in `[0, T)`:

**Window selection by law**:

| Law | Window | Range |
|-----|--------|-------|
| L0 (Memory) | Past → Now | `[max(0, t - n_frames + 1), t + 1)` |
| L1 (Prediction) | Now → Future | `[t, min(T, t + n_frames))` |
| L2 (Integration) | Bidirectional | `[max(0, t - half), min(T, t + n_frames - half))` |

Then:
1. Extract window: `r3_scalar[:, start:end]` → `(B, win_len)`
2. Truncate attention weights to window length, normalize to sum=1
3. Call `morph_computer.compute(window, weights, m_idx)` → `(B,)`
4. Store in result tensor at position `t`

### 5.3 MorphComputer (24 Morphological Features)

**File**: `mi_beta/ear/h3/morph.py`

```python
class MorphComputer:
    def compute(
        self,
        window: Tensor,        # (B, win_len)
        weights: Tensor,       # (win_len,) normalized attention weights
        morph_idx: int,        # 0-23
    ) -> Tensor:               # (B,)
```

Dispatches to `_m{idx}_{name}` methods:

| M# | Method | Formula |
|---:|--------|---------|
| 0 | `_m0_value` | `(w * weights).sum()` |
| 1 | `_m1_mean` | `w.mean()` |
| 2 | `_m2_std` | `w.std()` |
| 3 | `_m3_median` | `w.median()` |
| 4 | `_m4_max` | `w.max()` |
| 5 | `_m5_range` | `w.max() - w.min()` |
| 6 | `_m6_skewness` | `((w - mean) / std)^3.mean()` |
| 7 | `_m7_kurtosis` | `((w - mean) / std)^4.mean() - 3.0` |
| 8 | `_m8_velocity` | `w[:, -1] - w[:, -2]` (latest derivative) |
| 9 | `_m9_velocity_mean` | `mean(w[t+1] - w[t])` |
| 10 | `_m10_velocity_std` | `std(diff(w))` |
| 11 | `_m11_acceleration` | `vel[-1] - vel[-2]` (latest 2nd derivative) |
| 12 | `_m12_acceleration_mean` | `mean(diff^2(w))` |
| 13 | `_m13_acceleration_std` | `std(diff^2(w))` |
| 14 | `_m14_periodicity` | Lag-1 autocorrelation [0, 1] |
| 15 | `_m15_smoothness` | `1 / (1 + mean(\|jerk\|) / sigma)` |
| 16 | `_m16_curvature` | `mean(\|acceleration\|)` |
| 17 | `_m17_shape_period` | `sigmoid(2*len / zero_crossings / len - 0.5)` |
| 18 | `_m18_trend` | Linear regression slope |
| 19 | `_m19_stability` | `1 / (1 + var / mean^2)` |
| 20 | `_m20_entropy` | Shannon entropy of 16-bin histogram [0, 1] |
| 21 | `_m21_zero_crossings` | `zero_crossing_count / (len - 1)` |
| 22 | `_m22_peaks` | `local_maxima_count / (len - 2)` |
| 23 | `_m23_symmetry` | `1 / (1 + mean_sq_diff(forward, backward) / var)` |

### 5.4 EventHorizon (32 Time Scales)

**File**: `mi_beta/ear/h3/horizon.py`

```python
class EventHorizon:
    def __init__(self, index: int) -> None    # assert 0 <= index < 32
    @property
    def frames(self) -> int                   # HORIZON_FRAMES[index]
    @property
    def ms(self) -> float                     # HORIZON_MS[index]
    @property
    def seconds(self) -> float                # ms / 1000.0
```

**32 Horizon Bands**:

| Band | Horizons | Duration Range | Musical Level |
|------|----------|---------------|---------------|
| Sub-beat | H0-H5 | 5.8–46.4 ms | Onset, attack |
| Beat | H6-H11 | 200–450 ms | Tactus, pulse |
| Beat-phrase | H12-H17 | 525 ms–1.5 s | Bar, phrase fragment |
| Phrase-section | H18-H23 | 2–25 s | Phrase, section |
| Section-form | H24-H28 | 36 s–6.9 min | Section, movement |
| Piece | H29-H31 | 10–16.35 min | Full piece |

`HORIZON_FRAMES` computed as `max(1, round(ms / 1000.0 * 172.265625))`:
- H0=1, H1=2, H2=3, H3=4, H4=6, H5=8, H6=34, H7=43, ..., H31=169,000+

### 5.5 Attention Weighting

**File**: `mi_beta/ear/h3/attention.py`

```python
def compute_attention_weights(
    window_size: int,
    device: torch.device = torch.device("cpu"),
    decay: float = ATTENTION_DECAY,          # default 3.0
) -> Tensor:                                 # (window_size,)
```

**Algorithm**:
1. `positions = linspace(0, 1, window_size)` — oldest to newest
2. `weights = exp(-decay * (1.0 - positions))`
3. Result: `[low, ..., high]` — recent frames weighted more

**Weight profile** (decay=3.0):
- Position 0 (oldest): weight ≈ 0.05 (5%)
- Position 1 (newest): weight ≈ 1.0 (100%)

### 5.6 DemandTree (Sparse Routing)

**File**: `mi_beta/ear/h3/demand.py`

```python
class DemandTree:
    @staticmethod
    def build(
        demand: Set[Tuple[int, int, int, int]]
    ) -> Dict[int, Set[Tuple[int, int, int]]]:
        """Group 4-tuples by horizon: {h: {(r3_idx, m, l), ...}}"""

    @staticmethod
    def summary(demand: Set[Tuple[int, int, int, int]]) -> str:
        """Human-readable summary of H3 demand."""
```

**Purpose**: Groups demands by horizon index so all demands at the same time scale share the same window size and attention weights. This avoids redundant computation.

---

## 6. Brain Orchestration

**File**: `mi_beta/pipeline/brain_runner.py`

### 6.1 BrainOrchestrator

```python
class BrainOrchestrator:
    def __init__(self, active_units: Optional[Tuple[str, ...]] = None) -> None:
        self.unit_runner = UnitRunner(active_units=active_units)
        self.pathway_runner = PathwayRunner()
        self.neurochemical_state = NeurochemicalStateManager()

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],  # sparse H3 dict
        r3_features: Tensor,                                     # (B, T, 49)
    ) -> BrainOutput:

    @property
    def active_unit_names(self) -> List[str]
    @property
    def total_dim(self) -> int
    def reset(self) -> None             # reset neurochemical state between files
    def summary(self) -> Dict[str, object]
```

### 6.2 Five-Phase Execution Model

```
Input: h3_features {(r3_idx, h, m, l): (B, T)}, r3_features (B, T, 49)

PHASE 1: Mechanisms
  Skipped in current implementation. When implemented, MechanismRunner
  will pre-compute 10 shared mechanisms and cache outputs for reuse
  across models.

PHASE 2: Independent Units (7 units, parallel-eligible)
  SPU.compute(h3, r3) → (B, T, 99D)
  STU.compute(h3, r3) → (B, T, 148D)
  IMU.compute(h3, r3) → (B, T, 159D)
  ASU.compute(h3, r3) → (B, T, 94D)
  NDU.compute(h3, r3) → (B, T, 94D)
  MPU.compute(h3, r3) → (B, T, 104D)
  PCU.compute(h3, r3) → (B, T, 94D)
  Output: {unit_name → (B, T, unit_dim)}

PHASE 3: Pathways (routing layer)
  PathwayRunner.route(independent_outputs)
  → cross_inputs: {pathway_id → (B, T, D)}

PHASE 4: Dependent Units (2 units)
  ARU.compute(h3, r3, cross_unit_inputs) → (B, T, 120D)
  RPU.compute(h3, r3, cross_unit_inputs) → (B, T, 94D)

PHASE 5: Assembly
  Concatenate all unit tensors in UNIT_EXECUTION_ORDER
  Build unit_ranges mapping
  Return BrainOutput(tensor, unit_outputs, unit_ranges, dimension_names)
  Total: (B, T, 1006D) with all 94 models active
```

### 6.3 _assemble() — Assembly Logic

Iterates `ALL_UNIT_NAMES` in order, concatenates present tensors, builds `unit_ranges` dict and `dimension_names` tuple. Returns `BrainOutput` with combined tensor.

---

## 7. Contract ABCs

**Location**: `mi_beta/contracts/`

### 7.1 BaseModel — Central Model Contract

**File**: `mi_beta/contracts/base_model.py`

```python
class BaseModel(ABC):
    # ── CLASS CONSTANTS ──
    NAME: str = ""                              # "BCH", "SRP", etc.
    FULL_NAME: str = ""                         # "Brainstem Consonance Hierarchy"
    UNIT: str = ""                              # "SPU", "ARU", etc.
    TIER: str = ""                              # "alpha", "beta", "gamma"
    OUTPUT_DIM: int = 0                         # sum of LAYERS dims
    MECHANISM_NAMES: Tuple[str, ...] = ()       # ("PPC",), ("AED", "CPD"), etc.
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()
    LAYERS: Tuple[LayerSpec, ...] = ()          # E/M/P/F output structure

    # ── ABSTRACT PROPERTIES ──
    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """All H3 temporal demands needed by this model."""

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for every output dimension. len == OUTPUT_DIM"""

    @property
    @abstractmethod
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        """Brain regions associated with this model's computation."""

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Evidence provenance: citations, tier, confidence, falsification."""

    # ── ABSTRACT METHOD — THE CORE COMPUTATION ──
    @abstractmethod
    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],              # {mech_name: (B,T,30)}
        h3_features: Dict[Tuple[int,int,int,int], Tensor], # {4-tuple: (B,T)}
        r3_features: Tensor,                                # (B, T, 49)
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:                                            # (B, T, OUTPUT_DIM)

    # ── COMPUTED HELPERS ──
    def h3_demand_tuples(self) -> Set[Tuple[int, int, int, int]]
    @property
    def layer_dim_names(self) -> Tuple[str, ...]
    @property
    def cross_unit_dependency_units(self) -> FrozenSet[str]
    def validate_constants(self) -> List[str]
```

**Current state**: All 94 models return `torch.zeros(B, T, OUTPUT_DIM)` from `compute()`. All return empty `h3_demand = ()`. These are EXPECTED discrepancies for Phase 7.

### 7.2 BaseMechanism

**File**: `mi_beta/contracts/base_mechanism.py`

```python
class BaseMechanism(ABC):
    NAME: str = ""                              # "AED", "PPC", etc.
    FULL_NAME: str = ""
    OUTPUT_DIM: int = 30                        # standard size
    HORIZONS: Tuple[int, ...] = ()              # which horizons this mechanism uses

    @property
    @abstractmethod
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int,int,int,int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:                                # (B, T, OUTPUT_DIM)

    @property
    def demand_count(self) -> int
    @property
    def horizons_used(self) -> Set[int]
    @property
    def r3_indices_used(self) -> Set[int]
    def validate(self) -> list[str]
```

### 7.3 BaseCognitiveUnit

**File**: `mi_beta/contracts/base_unit.py`

```python
class BaseCognitiveUnit(ABC):
    UNIT_NAME: str = ""                         # "SPU", "ARU", etc.
    FULL_NAME: str = ""
    CIRCUIT: str = ""                           # "perceptual", "mesolimbic", etc.
    POOLED_EFFECT: float = 0.0                  # Cohen's d from meta-analysis

    @property
    @abstractmethod
    def models(self) -> List[BaseModel]:
    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int,int,int,int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:                                # (B, T, total_dim)

    @property
    def active_models(self) -> List[BaseModel]
    @property
    def total_dim(self) -> int
    @property
    def model_names(self) -> Tuple[str, ...]
    @property
    def mechanism_names(self) -> Tuple[str, ...]
    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]  # union of all models
    @property
    def dimension_names(self) -> Tuple[str, ...]
    @property
    def is_validated(self) -> bool              # pooled_effect > 0
    @property
    def model_ranges(self) -> Dict[str, Tuple[int, int]]
    def validate(self) -> list[str]
```

### 7.4 Specification Dataclasses

#### LayerSpec

```python
@dataclass(frozen=True)
class LayerSpec:
    code: str                    # "E", "M", "P", "F" (or custom)
    name: str                    # "Neurochemical Signals"
    start: int                   # start index (inclusive)
    end: int                     # end index (exclusive)
    dim_names: Tuple[str, ...]   # dimension names for this layer
    @property
    def dim(self) -> int         # end - start
```

**Standard layer codes**:
- **E** — Extraction / Explicit / Neurochemical signals (raw quantities)
- **M** — Mechanism / Mathematical / Model (neural pathway states)
- **P** — Psychological / Processing / Present (subjective states)
- **F** — Forecast / Future (predictive signals)
- Custom codes: **N** (Neurochemical), **C** (Circuit), **T** (Temporal)

#### H3DemandSpec

```python
@dataclass(frozen=True)
class H3DemandSpec:
    r3_idx: int                  # [0-48]
    r3_name: str                 # human-readable R3 feature name
    horizon: int                 # [0-31]
    horizon_label: str           # e.g., "200ms beat"
    morph: int                   # [0-23]
    morph_name: str              # e.g., "velocity"
    law: int                     # [0-2]
    law_name: str                # "memory" / "prediction" / "integration"
    purpose: str                 # WHY this demand exists
    citation: str                # justifying paper
    def as_tuple(self) -> Tuple[int, int, int, int]  # (r3_idx, h, m, l)
```

#### CrossUnitPathway

```python
@dataclass(frozen=True)
class CrossUnitPathway:
    pathway_id: str              # "P1_SPU_ARU"
    name: str                    # human-readable
    source_unit: str             # "SPU"
    source_model: str            # "BCH"
    source_dims: Tuple[str, ...] # dimension names provided
    target_unit: str             # "ARU"
    target_model: str            # "SRP"
    correlation: str             # "r=0.81"
    citation: str                # justifying paper
    @property
    def is_intra_unit(self) -> bool
    @property
    def is_inter_unit(self) -> bool
    @property
    def edge(self) -> Tuple[str, str]
```

#### Citation & ModelMetadata

```python
@dataclass(frozen=True)
class Citation:
    author: str                  # "Bidelman"
    year: int                    # 2009
    finding: str                 # one-line summary
    effect_size: str = ""        # "r=0.84", "d=0.67", etc.
    @property
    def short_ref(self) -> str   # "Author YEAR"

@dataclass(frozen=True)
class ModelMetadata:
    citations: Tuple[Citation, ...]
    evidence_tier: str           # "alpha" / "beta" / "gamma"
    confidence_range: Tuple[float, float]  # (low, high) in [0, 1]
    falsification_criteria: Tuple[str, ...]
    version: str = "1.0.0"
    paper_count: Optional[int] = None
    @property
    def effective_paper_count(self) -> int
    @property
    def is_mechanistic(self) -> bool   # alpha-tier
```

#### BrainRegion

```python
@dataclass(frozen=True)
class BrainRegion:
    name: str                    # "Nucleus Accumbens"
    abbreviation: str            # "NAcc"
    hemisphere: str              # "L", "R", "bilateral"
    mni_coords: Tuple[int, int, int]  # (x, y, z) MNI152 space
    brodmann_area: Optional[int] = None
    function: str = ""
    evidence_count: int = 0
    @property
    def is_cortical(self) -> bool
    @property
    def is_subcortical(self) -> bool
```

#### NeurochemicalType & NeurochemicalState

```python
@unique
class NeurochemicalType(Enum):
    DOPAMINE = "dopamine"
    OPIOID = "opioid"
    SEROTONIN = "serotonin"
    NOREPINEPHRINE = "norepinephrine"
    GABA = "gaba"
    GLUTAMATE = "glutamate"

class NeurochemicalState:
    def write(self, chemical, region, value) -> None
    def read(self, chemical, region) -> Optional[Tensor]
    def reset(self) -> None
    def keys(self) -> list[Tuple[NeurochemicalType, str]]
```

---

## 8. Cognitive Units

**Location**: `mi_beta/brain/units/`

### 8.1 Unit Registry and Execution Order

**File**: `mi_beta/brain/units/__init__.py`

```python
UNIT_CLASSES: Dict[str, Type[BaseCognitiveUnit]] = {
    "SPU": SPUUnit, "STU": STUUnit, "IMU": IMUUnit,
    "ASU": ASUUnit, "NDU": NDUUnit, "MPU": MPUUnit,
    "PCU": PCUUnit, "ARU": ARUUnit, "RPU": RPUUnit,
}

INDEPENDENT_UNITS = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU")
DEPENDENT_UNITS = ("ARU", "RPU")
ALL_UNIT_NAMES = INDEPENDENT_UNITS + DEPENDENT_UNITS
```

### 8.2 Unit Implementation Pattern

Each unit follows identical structure:

```python
class {UNIT}Unit(BaseCognitiveUnit):
    UNIT_NAME = "{UNIT}"
    FULL_NAME = "..."
    CIRCUIT = "..."
    POOLED_EFFECT = ...

    def __init__(self) -> None:
        self._models = [cls() for cls in ALL_{UNIT}_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(self, h3_features, r3_features, cross_unit_inputs=None) -> Tensor:
        outputs = []
        for model in self.active_models:
            out = model.compute(mechanism_outputs={}, h3_features=h3_features,
                                r3_features=r3_features, cross_unit_inputs=None)
            outputs.append(out)
        return torch.cat(outputs, dim=-1) if outputs else torch.zeros(B, T, 0)
```

### 8.3 Complete Unit Profiles (9 Units, 94 Models)

#### SPU — Spectral Processing Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `perceptual` |
| Pooled Effect | d=0.84 (Core-4, k>=10) |
| Total Output | 99D |
| Model Count | 9 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | BCH | Brainstem Consonance Hierarchy | 12 |
| alpha | PSCL | Pitch-Space Cortical Lateralization | 12 |
| alpha | PCCR | Pitch Chroma Cortical Representation | 11 |
| beta | STAI | Spectral-Temporal Auditory Integration | 12 |
| beta | TSCP | Timbre-Specific Cortical Plasticity | 10 |
| beta | MIAA | Musical Imagery Auditory Activation | 11 |
| gamma | SDNPS | Stimulus-Dependent Neural Pitch Scaling | 10 |
| gamma | ESME | Expertise-Specific MMN Enhancement | 11 |
| gamma | SDED | Sensory Dissonance Early Detection | 10 |

#### STU — Sensorimotor Timing Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `sensorimotor` |
| Pooled Effect | d=0.67 (Core-4, k>=10) |
| Total Output | 148D |
| Model Count | 14 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | HMCE | Hierarchical Musical Context Encoding | 13 |
| alpha | AMSC | Auditory-Motor Stream Coupling | 12 |
| alpha | MDNS | Melody Decoding Neural Signals | 12 |
| beta | AMSS | Attention-Modulated Stream Segregation | 11 |
| beta | TPIO | Timbre Perception-Imagery Overlap | 10 |
| beta | EDTA | Expertise-Dependent Tempo Adaptation | 10 |
| beta | ETAM | Entrainment Tempo Attention Modulation | 11 |
| beta | HGSIC | Hierarchical Groove State Integration | 11 |
| beta | OMS | Oscillatory Motor Synchronization | 10 |
| gamma | TMRM | Tempo Memory Reproduction Matrix | 10 |
| gamma | NEWMD | Neural Entrainment-Working Memory Diss. | 10 |
| gamma | MTNE | Music Training Neural Efficiency | 10 |
| gamma | PTGMP | Piano Training Grey Matter Plasticity | 10 |
| gamma | MPFS | Musical Prodigy Flow State | 10 |

#### IMU — Integrative Memory Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `mnemonic` |
| Pooled Effect | d=0.53 (Core-4, k>=10) |
| Total Output | 159D |
| Model Count | 15 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | MEAMN | Music-Evoked Autobiographical Memory | 12 |
| alpha | PNH | Pythagorean Neural Hierarchy | 11 |
| alpha | MMP | Musical Mnemonic Preservation | 12 |
| beta | RASN | Rhythmic Auditory Stimulation Network | 11 |
| beta | PMIM | Predictive Memory Integration Matrix | 11 |
| beta | OII | Oscillatory Intelligence Integration | 10 |
| beta | HCMC | Hippocampal-Cortical Memory Consolidation | 11 |
| beta | RIRI | Recognition-Recall Integration Recency | 10 |
| beta | MSPBA | Musical Syntax Processing Broca's Area | 11 |
| beta | VRIAP | VR-Induced Analgesia Paradigm | 10 |
| beta | TPRD | Tonotopy-Pitch Representation Density | 10 |
| beta | CMAPCC | Cross-Modal Action-Perception Coupling | 10 |
| gamma | DMMS | Developmental Music Memory Schema | 10 |
| gamma | CSSL | Cross-Species Song Learning | 10 |
| gamma | CDEM | Context-Dependent Emotional Memory | 10 |

#### ASU — Auditory Salience Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `salience` |
| Pooled Effect | d=0.60 (experimental) |
| Total Output | 94D |
| Model Count | 9 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | SNEM | Salience Network Engagement Model | 12 |
| alpha | IACM | Interaural Attention Capture Model | 11 |
| alpha | CSG | Cortical Salience Gating | 11 |
| beta | BARM | Bottom-up Attention Reflex Model | 10 |
| beta | STANM | Spectro-Temporal Attention Network Model | 10 |
| beta | AACM | Auditory Attention Control Model | 10 |
| gamma | PWSM | Pop-out Warning Salience Model | 10 |
| gamma | DGTP | Deviance-Gated Temporal Processing | 10 |
| gamma | SDL | Stimulus-Driven Listening | 10 |

> **EXPECTED discrepancy (ASU-specific)**: All 9 ASU models have `MECHANISM_NAMES=("ASA",)` in code vs `("BEP","ASA")` in docs. Phase 7B will fix.

#### NDU — Novelty Detection Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `salience` |
| Pooled Effect | d=0.55 (experimental) |
| Total Output | 94D |
| Model Count | 9 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | MPG | Mismatch Prediction Gate | 12 |
| alpha | SDD | Spectral Deviance Detection | 11 |
| alpha | EDNR | Expectation-Dependent Novelty Response | 11 |
| beta | DSP_ | Deviance Salience Processing | 10 |
| beta | CDMR | Context-Dependent Mismatch Response | 10 |
| beta | SLEE | Statistical Learning Expectation Engine | 10 |
| gamma | SDDP | Sensory-Driven Deviance Processing | 10 |
| gamma | ONI | Oddball Novelty Index | 10 |
| gamma | ECT | Error Correction Trace | 10 |

> **Note**: DSP_ uses trailing underscore to avoid collision with Python's `dsp` namespace.

#### MPU — Motor Planning Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `sensorimotor` |
| Pooled Effect | d=0.62 (experimental) |
| Total Output | 104D |
| Model Count | 10 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | PEOM | Predictive Error Optimization Model | 12 |
| alpha | MSR | Motor Sequence Representation | 11 |
| alpha | GSSM | Groove-State Sensorimotor Model | 11 |
| beta | ASAP | Anticipatory Sequence Action Planning | 10 |
| beta | DDSMI | Dynamic Dual-Stream Motor Integration | 10 |
| beta | VRMSME | VR Motor Skill Music Enhancement | 10 |
| beta | SPMC | Sensory-Predictive Motor Coupling | 10 |
| gamma | NSCP | Neural Substrate Choreographic Planning | 10 |
| gamma | CTBB | Cerebello-Thalamic Beat Binding | 10 |
| gamma | STC | Sensorimotor Timing Calibration | 10 |

#### PCU — Predictive Coding Unit (INDEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `mnemonic` |
| Pooled Effect | d=0.58 (experimental) |
| Total Output | 94D |
| Model Count | 9 |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | HTP | Harmonic Tension Prediction | 12 |
| alpha | SPH | Spectral Pitch Height | 11 |
| alpha | ICEM | Imagery-Cognition Emotion Mapping | 11 |
| beta | PWUP | Pitch-Weight Uncertainty Processing | 10 |
| beta | WMED | Working Memory Emotion Dynamics | 10 |
| beta | UDP | Uncertainty-Driven Prediction | 10 |
| gamma | IGFE | Imagery-Guided Feature Enhancement | 10 |
| gamma | MAA | Musical Agentic Attention | 10 |
| gamma | PSH | Perceptual Salience Hierarchy | 10 |

#### ARU — Affective Resonance Unit (DEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `mesolimbic` |
| Pooled Effect | d=0.83 (Core-4, k>=10) |
| Total Output | 120D |
| Model Count | 10 |
| Cross-unit inputs | P1 (SPU→ARU), P3 (IMU→ARU), P5 (STU→ARU) |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | SRP | Striatal Reward Pathway | 19 |
| alpha | AAC | Autonomic-Affective Coupling | 14 |
| alpha | VMM | Valence-Mode Mapping | 12 |
| beta | PUPF | Pleasure-Uncertainty-Prediction | 12 |
| beta | CLAM | Cognitive-Load-Arousal Modulation | 11 |
| beta | MAD | Musical Anhedonia Disconnection | 11 |
| beta | NEMAC | Nostalgia-Enhanced Memory-Affect | 11 |
| gamma | DAP | Developmental Affective Plasticity | 10 |
| gamma | CMAT | Cross-Modal Affective Transfer | 10 |
| gamma | TAR | Therapeutic Affective Resonance | 10 |

#### RPU — Reward Processing Unit (DEPENDENT)

| Property | Value |
|----------|-------|
| Circuit | `mesolimbic` |
| Pooled Effect | d=0.70 (experimental) |
| Total Output | 94D |
| Model Count | 9 |
| Cross-unit inputs | from independent units via pathways |

| Tier | Model | Full Name | D |
|------|-------|-----------|--:|
| alpha | DAED | DA-Expectation Dynamics | 12 |
| alpha | MORMR | Model-Optimal Reward Modulation Relay | 11 |
| alpha | RPEM | Reward Prediction Error Model | 11 |
| beta | IUCP | Information-Uncertainty Coupling Process | 10 |
| beta | MCCN | Musical Context Coupling Network | 10 |
| beta | MEAMR | Memory-Affect Modulated Reward | 10 |
| gamma | LDAC | Listener-Dependent Aesthetic Computation | 10 |
| gamma | IOTMS | Individual Optimal Tempo Matching System | 10 |
| gamma | SSPS | Social Signal Processing System | 10 |

### 8.4 Unit Dimension Summary

| Unit | Type | Circuit | d | Models | α | β | γ | Total D |
|------|------|---------|---:|-------:|--:|--:|--:|--------:|
| SPU | Independent | perceptual | 0.84 | 9 | 3 | 3 | 3 | 99 |
| STU | Independent | sensorimotor | 0.67 | 14 | 3 | 6 | 5 | 148 |
| IMU | Independent | mnemonic | 0.53 | 15 | 3 | 9 | 3 | 159 |
| ASU | Independent | salience | 0.60 | 9 | 3 | 3 | 3 | 94 |
| NDU | Independent | salience | 0.55 | 9 | 3 | 3 | 3 | 94 |
| MPU | Independent | sensorimotor | 0.62 | 10 | 3 | 4 | 3 | 104 |
| PCU | Independent | mnemonic | 0.58 | 9 | 3 | 3 | 3 | 94 |
| ARU | Dependent | mesolimbic | 0.83 | 10 | 3 | 4 | 3 | 120 |
| RPU | Dependent | mesolimbic | 0.70 | 9 | 3 | 3 | 3 | 94 |
| **Total** | | | | **94** | **27** | **38** | **29** | **1,006** |

### 8.5 Evidence Tiers

| Tier | Criteria | Models | Confidence |
|------|----------|-------:|------------|
| Alpha (mechanistic) | k>=10 studies, causal evidence | 27 | >90% |
| Beta (correlational) | 5<=k<10, correlational | 38 | 70-90% |
| Gamma (exploratory) | k<5, theoretical | 29 | <70% |

**Core-4 Validated Units** (k>=10, meta-analytic evidence):
- SPU: d=0.84 | ARU: d=0.83 | STU: d=0.67 | IMU: d=0.53

**Experimental-5 Units** (k<10):
- RPU: d=0.70 | MPU: d=0.62 | ASU: d=0.60 | PCU: d=0.58 | NDU: d=0.55

---

## 9. Mechanisms

**Location**: `mi_beta/brain/mechanisms/`

### 9.1 Mechanism Registry

All mechanisms follow `BaseMechanism` contract. Standard `OUTPUT_DIM = 30`.

| Mechanism | Full Name | Neural Circuit | Horizons |
|-----------|-----------|---------------|----------|
| AED | Affective Entrainment Dynamics | Mesolimbic | H6, H16 |
| ASA | Auditory Scene Analysis | Salience | H3, H6, H9 |
| BEP | Beat Entrainment Processing | Sensorimotor | H6, H9, H11 |
| C0P | Cognitive Projection | Mesolimbic | H18, H19, H20 |
| CPD | Chills & Peak Detection | Mesolimbic | H9, H16, H18 |
| MEM | Memory Encoding / Retrieval | Mnemonic | H18, H20, H22, H25 |
| PPC | Pitch Processing Chain | Perceptual | H0, H3, H6 |
| SYN | Syntactic Processing | Perceptual | H12, H16, H18 |
| TMH | Temporal Memory Hierarchy | Sensorimotor | H16, H18, H20, H22 |
| TPC | Timbre Processing Chain | Perceptual | H6, H12, H16 |

### 9.2 MechanismRunner

```python
class MechanismRunner:
    def __init__(self, registry: ModelRegistry):
        # Scans active models' MECHANISM_NAMES
        # Instantiates each unique mechanism once
        self._mechanisms: Dict[str, BaseMechanism] = {}
        self._cache: Dict[str, Tensor] = {}

    def run(
        self,
        h3_features: Dict[Tuple[int,int,int,int], Tensor],
        r3_features: Tensor,
    ) -> Dict[str, Tensor]:
        # Computes all mechanisms, caches outputs
        # If multiple models need PPC, computed once
```

### 9.3 Mechanism-to-Unit Usage Map

| Mechanism | Used By (units) |
|-----------|-----------------|
| PPC | SPU |
| TPC | SPU, STU |
| BEP | STU, MPU, ASU (in docs; code has ASU with ASA only) |
| ASA | ASU, NDU |
| AED | ARU |
| CPD | ARU |
| C0P | PCU |
| MEM | IMU |
| SYN | IMU, STU |
| TMH | NDU, PCU |

---

## 10. Pathways

**Location**: `mi_beta/brain/pathways/`

### 10.1 Declared Pathways (5)

| ID | Route | Correlation | Citation |
|----|-------|-------------|----------|
| P1 | SPU → ARU | r=0.81 | Bidelman 2009 (consonance → pleasure) |
| P2 | STU → STU (internal) | r=0.70 | Grahn & Brett 2007 (beat → motor sync) |
| P3 | IMU → ARU | r=0.55 | Janata 2009 (memory → affect) |
| P4 | STU → STU (internal) | r=0.99 | Mischler 2025 (context → prediction) |
| P5 | STU → ARU | r=0.60 | Juslin & Vastfjall 2008 (tempo → emotion) |

### 10.2 PathwayRunner

```python
class PathwayRunner:
    def __init__(self) -> None:
        self._pathways = ALL_PATHWAYS

    @property
    def pathways(self) -> Tuple[CrossUnitPathway, ...]

    def route(self, unit_outputs: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """Route signals from independent units to dependent units.

        Currently passthrough: passes full unit tensors as cross-unit inputs.
        Phase 7F will extract specific source_dims from source models.

        Returns:
            {pathway_id → (B, T, D)} cross-unit input dict
        """
```

---

## 11. Brain Regions & Neurochemicals

### 11.1 RegionAtlas

**File**: `mi_beta/brain/regions/__init__.py`

```python
class RegionAtlas:
    """Unified atlas of 26 brain regions in MNI152 space."""
    def __init__(self):
        self.subcortical: Tuple[BrainRegion, ...]  # 9 regions
        self.cortical: Tuple[BrainRegion, ...]     # 12 regions
        self.brainstem: Tuple[BrainRegion, ...]    # 5 regions
    @property
    def all(self) -> Tuple[BrainRegion, ...]       # 26 total

ATLAS = RegionAtlas()  # module-level singleton
```

**Subcortical (9)**: VTA, NAcc, Caudate, Amygdala, Hippocampus, Putamen, Thalamus_MGB, Hypothalamus, Insula

**Cortical (12)**: A1/HG, STG, STS, IFG, DLPFC, vMPFC, OFC, ACC, SMA, PMC, Angular Gyrus, Temporal Pole

**Brainstem (5)**: IC, AN, CN, SOC, PAG

### 11.2 NeurochemicalStateManager

**File**: `mi_beta/brain/neurochemicals/__init__.py`

```python
class NeurochemicalStateManager:
    """High-level manager for 4 primary neurochemical systems."""

    # Per-system read/write/keys methods:
    def write_da(self, region, value) -> None
    def read_da(self, region) -> Optional[Tensor]
    def write_opioid(self, region, value) -> None
    def read_opioid(self, region) -> Optional[Tensor]
    def write_serotonin(self, region, value) -> None
    def read_serotonin(self, region) -> Optional[Tensor]
    def write_ne(self, region, value) -> None
    def read_ne(self, region) -> Optional[Tensor]

    def reset(self) -> None
    @property
    def all_signals(self) -> Dict[str, List[str]]
```

**4 Neurochemical Systems**:

| System | Abbreviation | Role | File |
|--------|-------------|------|------|
| Dopamine | DA | Reward prediction, incentive salience | dopamine.py |
| Opioid | — | Hedonic "liking", consummatory pleasure | opioid.py |
| Serotonin | 5-HT | Mood regulation, emotional valence | serotonin.py |
| Norepinephrine | NE | Arousal, attentional gating | norepinephrine.py |

---

## 12. L3 Semantic Interpretation

**Location**: `mi_beta/language/groups/`

### 12.1 L3Orchestrator

**File**: `mi_beta/language/groups/__init__.py`

```python
class L3Orchestrator:
    def __init__(self, registry: Any = None) -> None:
        self.groups: OrderedDict[str, Any] = OrderedDict([
            ("alpha", AlphaGroup()),
            ("beta", BetaGroup(registry=registry)),
            ("gamma", GammaGroup()),
            ("delta", DeltaGroup()),
            ("epsilon", EpsilonGroup()),
            ("zeta", ZetaGroup()),
            ("eta", EtaGroup()),
            ("theta", ThetaGroup()),
        ])

    def compute(self, brain_output: BrainOutput) -> L3Output:
        """Dependency-ordered semantic computation."""

    def reset(self) -> None:
        """Reset stateful groups (epsilon). Call between audio files."""

    @property
    def total_dim(self) -> int
```

### 12.2 Computation Phases (Dependency Order)

```
Phase 1 (Independent — read only BrainOutput):
  alpha.compute(brain_output)     → (B, T, n_units+2)
  beta.compute(brain_output)      → (B, T, n_regions)
  gamma.compute(brain_output)     → (B, T, 13)
  delta.compute(brain_output)     → (B, T, 12)

Phase 1b (Stateful — read only BrainOutput, maintains state):
  epsilon.compute(brain_output)   → (B, T, 19)

Phase 2 (Dependent chain):
  zeta.compute(brain_output, epsilon_output=eps)        → (B, T, 12)
  eta.compute(brain_output, zeta_output=zeta)           → (B, T, 12)
  theta.compute(brain_output, epsilon_output=eps,
                              zeta_output=zeta)         → (B, T, 16)

Final: torch.cat([α, β, γ, δ, ε, ζ, η, θ], dim=-1)
```

### 12.3 BaseSemanticGroup (Contract)

**File**: `mi_beta/contracts/base_semantic_group.py`

```python
class BaseSemanticGroup(ABC):
    LEVEL: int = 0                   # 1-8 epistemological level
    GROUP_NAME: str = ""             # "alpha", "beta", ..., "theta"
    DISPLAY_NAME: str = ""           # "a", "b", ..., "th"
    OUTPUT_DIM: int = 0

    @abstractmethod
    def compute(self, brain_output: Any, **kwargs) -> SemanticGroupOutput:
    @property
    @abstractmethod
    def dimension_names(self) -> List[str]:
    def validate(self) -> list[str]
```

### 12.4 Semantic Group Profiles (8 Groups)

#### Alpha — Unit Attribution (variable D)

**File**: `mi_beta/language/groups/alpha.py`

| Property | Value |
|----------|-------|
| Level | 1 |
| OUTPUT_DIM | n_units + 2 (variable, typically 11) |
| Range | [0, 1] per dim |

**Dimensions**: One per active cognitive unit (softmax attribution) + 2 global dims.
Auto-configures on first compute call based on BrainOutput structure.

#### Beta — Region Activation (variable D)

**File**: `mi_beta/language/groups/beta.py`

| Property | Value |
|----------|-------|
| Level | 2 |
| OUTPUT_DIM | n_regions (variable, typically ~30) |
| Range | [0, 1] per dim |

**Dimensions**: One per unique brain region across all active models.
Requires registry to discover region set. Auto-configures from BrainOutput.

#### Gamma — Psychological State (13D)

**File**: `mi_beta/language/groups/gamma.py`

| Property | Value |
|----------|-------|
| Level | 3 |
| OUTPUT_DIM | 13 |
| Range | [0, 1] per dim |

**Dimensions (13)** _(authoritative source: L3-SEMANTIC-ARCHITECTURE.md §6)_:

| # | Block | Dimension |
|--:|-------|-----------|
| 0 | Reward (3D) | reward_intensity |
| 1 | | reward_type |
| 2 | | reward_phase |
| 3 | ITPRA (2D) | itpra_tension_resolution |
| 4 | | itpra_surprise_evaluation |
| 5 | Aesthetics (3D) | beauty |
| 6 | | sublime |
| 7 | | groove |
| 8 | Emotion (2D) | valence |
| 9 | | arousal |
| 10 | Chills (3D) | chill_probability |
| 11 | | chill_intensity |
| 12 | | chill_phase |

#### Delta — Observable Correlates (12D)

**File**: `mi_beta/language/groups/delta.py`

| Property | Value |
|----------|-------|
| Level | 4 |
| OUTPUT_DIM | 12 |
| Range | [0, 1] per dim |

**Dimensions (12)** _(authoritative source: L3-SEMANTIC-ARCHITECTURE.md §7)_:

| # | Block | Dimension |
|--:|-------|-----------|
| 0 | Physiological (4D) | skin_conductance |
| 1 | | heart_rate |
| 2 | | pupil_diameter |
| 3 | | piloerection |
| 4 | Neural (3D) | fmri_nacc_bold |
| 5 | | fmri_caudate_bold |
| 6 | | eeg_frontal_alpha |
| 7 | Behavioral (2D) | willingness_to_pay |
| 8 | | button_press_rating |
| 9 | Temporal (3D) | wanting_leads_liking |
| 10 | | rpe_latency |
| 11 | | refractory_state |

#### Epsilon — Learning & Adaptation (19D, STATEFUL)

**File**: `mi_beta/language/groups/epsilon.py`

| Property | Value |
|----------|-------|
| Level | 5 |
| OUTPUT_DIM | 19 |
| Range | [0, 1] per dim |
| **Stateful** | Yes — maintains running state across frames |

**Dimensions (19)** _(authoritative source: L3-SEMANTIC-ARCHITECTURE.md §8)_:

| # | Block | Dimension |
|--:|-------|-----------|
| 0 | Surprise & Entropy (2D) | surprise |
| 1 | | entropy |
| 2 | Prediction Errors (3D) | pe_short |
| 3 | | pe_medium |
| 4 | | pe_long |
| 5 | Precision (2D) | precision_short |
| 6 | | precision_long |
| 7 | Information Dynamics (3D) | bayesian_surprise |
| 8 | | information_rate |
| 9 | | compression_progress |
| 10 | Interaction (1D) | entropy_x_surprise |
| 11 | ITPRA Mapping (5D) | imagination |
| 12 | | tension_uncertainty |
| 13 | | prediction_reward |
| 14 | | reaction_magnitude |
| 15 | | appraisal_learning |
| 16 | Reward & Aesthetics (3D) | reward_pe |
| 17 | | wundt_position |
| 18 | | familiarity |

**Stateful components**: 3 EMA accumulators (short α=0.1, medium α=0.01, long α=0.001), Welford online stats, Markov transition matrix (B,8,8), ring buffer (B,50).
**reset()** clears all internal state between audio files.

#### Zeta — Polarity Axes (12D, [-1,+1])

**File**: `mi_beta/language/groups/zeta.py`

| Property | Value |
|----------|-------|
| Level | 6 |
| OUTPUT_DIM | 12 |
| Range | **[-1, +1]** bipolar |
| Dependency | epsilon_output |

**12 Bipolar Axes** (POLARITY_AXES constant):

| # | Axis | Negative Pole | Positive Pole |
|--:|------|--------------|---------------|
| 0 | valence | miserable | euphoric |
| 1 | arousal | comatose | explosive |
| 2 | tension | dissolved | crushing |
| 3 | power | whisper | overwhelming |
| 4 | wanting | satiated | craving |
| 5 | liking | displeasure | satisfaction |
| 6 | novelty | familiar | novel |
| 7 | complexity | simple | complex |
| 8 | beauty | discordant | harmonious |
| 9 | groove | rigid | flowing |
| 10 | stability | chaotic | stable |
| 11 | engagement | detached | absorbed |

**Axis categories**: Reward (0-5), Learning (6-8, from epsilon), Aesthetic (9-11).

#### Eta — Vocabulary (12D, 64-Gradation)

**File**: `mi_beta/language/groups/eta.py`

| Property | Value |
|----------|-------|
| Level | 7 |
| OUTPUT_DIM | 12 |
| Range | [0, 1] (quantized from [-1,+1]) |
| Dependency | zeta_output |

**Constants**:
- `AXIS_NAMES`: 12 axes (same as zeta)
- `N_GRADATIONS`: 64 discrete levels
- `N_BANDS`: 8 vocabulary bands per axis
- `GRADATIONS_PER_BAND`: 8
- `AXIS_TERMS`: 12 × 8 = 96 vocabulary terms

**Vocabulary Terms** (8 bands per axis, negative→positive):

| Axis | Band 0 | Band 1 | Band 2 | Band 3 | Band 4 | Band 5 | Band 6 | Band 7 |
|------|--------|--------|--------|--------|--------|--------|--------|--------|
| valence | devastating | melancholic | wistful | subdued | neutral | content | happy | euphoric |
| arousal | comatose | lethargic | drowsy | calm | neutral | alert | energized | explosive |
| tension | dissolved | slack | easy | mild | neutral | taut | strained | crushing |
| power | whisper | fragile | gentle | moderate | neutral | strong | forceful | overwhelming |
| wanting | fulfilled | content | settled | mild | neutral | interested | eager | desperate |
| liking | aversive | unpleasant | bland | indifferent | neutral | pleasant | delightful | ecstatic |
| novelty | habitual | routine | known | expected | neutral | fresh | surprising | shocking |
| complexity | trivial | basic | clear | moderate | neutral | elaborate | intricate | labyrinthine |
| beauty | harsh | grating | rough | plain | neutral | pleasing | beautiful | sublime |
| groove | mechanical | stiff | stilted | measured | neutral | swinging | grooving | transcendent |
| stability | turbulent | erratic | unsteady | wavering | neutral | steady | anchored | immovable |
| engagement | oblivious | indifferent | distracted | aware | neutral | attentive | immersed | entranced |

**Quantization**: `polarity_to_gradation(value)` converts [-1,+1] → [0,63]. `gradation_to_band(grad)` converts [0,63] → [0,7].

**get_terms(zeta_output)** returns human-readable vocabulary terms for each axis.

#### Theta — Narrative (16D)

**File**: `mi_beta/language/groups/theta.py`

| Property | Value |
|----------|-------|
| Level | 8 |
| OUTPUT_DIM | 16 |
| Range | [0, 1] per dim |
| Dependencies | epsilon_output, zeta_output |

**Dimensions (16)** — "Musical sentence" structure:

| # | Block | Dimension | Meaning |
|--:|-------|-----------|---------|
| 0 | Subject (4D) | reward_salience | Reward/pleasure dominates |
| 1 | | tension_salience | Tension/conflict dominates |
| 2 | | motion_salience | Movement/energy dominates |
| 3 | | beauty_salience | Beauty/harmony dominates |
| 4 | Predicate (4D) | rising | Subject is increasing |
| 5 | | peaking | Subject is at climax |
| 6 | | falling | Subject is decreasing |
| 7 | | stable | Subject is holding steady |
| 8 | Modifier (4D) | intensity | How strongly |
| 9 | | certainty | How confidently |
| 10 | | novelty | How surprisingly |
| 11 | | speed | How quickly |
| 12 | Connector (4D) | continuing | Same thread continues |
| 13 | | contrasting | Opposing element |
| 14 | | resolving | Tension resolves |
| 15 | | transitioning | Moving to new section |

**Computation**: Subject from softmax competition between Brain pathways. Predicate from epsilon temporal dynamics. Modifier from Brain + epsilon signals. Connector from zeta polarity temporal relations.

### 12.5 L3 Output Dimension Summary

| Group | Level | Dim | Range | Stateful | Dependencies |
|-------|------:|----:|-------|----------|-------------|
| Alpha | 1 | var | [0,1] | No | — |
| Beta | 2 | var | [0,1] | No | — |
| Gamma | 3 | 13 | [0,1] | No | — |
| Delta | 4 | 12 | [0,1] | No | — |
| Epsilon | 5 | 19 | [0,1] | **Yes** | — |
| Zeta | 6 | 12 | [-1,+1] | No | epsilon |
| Eta | 7 | 12 | [0,1] | No | zeta |
| Theta | 8 | 16 | [0,1] | No | epsilon, zeta |
| **Fixed total** | | **84** | | | |
| **Variable total** | | n_units+2 + n_regions | | | |

**Typical total**: With 9 units + ~30 regions = 11 + 30 + 84 = **125D**

---

## 13. Adapters

**Location**: `mi_beta/language/adapters/`

### 13.1 BaseModelSemanticAdapter (Contract)

**File**: `mi_beta/language/adapters/_base_adapter.py`

```python
class BaseModelSemanticAdapter(ABC):
    UNIT_NAME: str

    @abstractmethod
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        """Map unit output dimensions to semantic group inputs."""
```

### 13.2 Adapter Stubs (9)

All 9 adapters follow identical stub pattern:

```python
class {UNIT}Adapter(BaseModelSemanticAdapter):
    UNIT_NAME = "{UNIT}"

    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

| File | Class | Unit |
|------|-------|------|
| aru_adapter.py | ARUAdapter | ARU |
| asu_adapter.py | ASUAdapter | ASU |
| imu_adapter.py | IMUAdapter | IMU |
| mpu_adapter.py | MPUAdapter | MPU |
| ndu_adapter.py | NDUAdapter | NDU |
| pcu_adapter.py | PCUAdapter | PCU |
| rpu_adapter.py | RPUAdapter | RPU |
| spu_adapter.py | SPUAdapter | SPU |
| stu_adapter.py | STUAdapter | STU |

> **EXPECTED**: All adapters are stubs. Phase 7E will implement real semantic mapping per unit (e.g., SPU: consonance→beauty, timbre→complexity).

---

## 14. Pipeline

**Location**: `mi_beta/pipeline/`

### 14.1 MIBetaPipeline — End-to-End

**File**: `mi_beta/pipeline/mi_beta.py`

```python
class MIBetaPipeline:
    def __init__(
        self,
        config: Optional[MIBetaConfig] = None,
        active_units: Optional[Tuple[str, ...]] = None,
    ) -> None:
        self.config = config or MI_BETA_CONFIG
        self.r3_extractor = R3Extractor(self.config)
        self.h3_extractor = H3Extractor(self.config)
        self.brain = BrainOrchestrator(active_units=active_units)
        # TODO: L3 orchestrator

    def process(
        self,
        waveform: Tensor,            # (B, samples) or (samples,)
        return_ear: bool = False,
    ) -> MIBetaOutput:

    @property
    def total_dim(self) -> int       # cochlea + r3 + brain (L3 not yet)
    @property
    def cochlea_dim(self) -> int     # 128
    @property
    def r3_dim(self) -> int          # 49
    @property
    def brain_dim(self) -> int       # variable
    def summary(self) -> dict
```

### 14.2 Pipeline Data Flow (process method)

```
1. COCHLEA: audio_to_mel(waveform, config) → CochleaOutput(mel=(B,128,T))
2. R3:      r3_extractor.extract(cochlea.mel) → R3Output(features=(B,T,49))
3. H3:      h3_extractor.extract(r3.features, demand=set()) → H3Output({})
              NOTE: demand is currently empty (all model h3_demand=())
4. BRAIN:   brain.compute(h3.features, r3.features) → BrainOutput(B,T,brain_dim)
5. ASSEMBLE:
   mel_t = cochlea.mel.transpose(1, 2)         # (B, T, 128)
   mi_space = cat([mel_t, r3.features, brain.tensor], dim=-1)
   → MIBetaOutput with section ranges:
     cochlea_range = (0, 128)
     r3_range      = (128, 177)
     brain_range   = (177, 177 + brain_dim)
     l3_range      = None (L3 not yet integrated)
```

### 14.3 Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `mi_beta/run.py` | Quick-start CLI runner | `python -m mi_beta` |
| `mi_beta/__main__.py` | CLI entry point | delegates to `run.main()` |
| `mi_beta/__init__.py` | Package metadata | `__version__ = "0.1.0-beta"` |

---

## 15. Tests

**Location**: `tests/`

### 15.1 Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared pytest fixtures
├── unit/
│   ├── core/
│   │   ├── test_config.py         # MIBetaConfig validation
│   │   └── test_constants.py      # Constants consistency
│   ├── ear/
│   │   ├── test_cochlea.py        # audio_to_mel() output shapes
│   │   ├── test_r3.py             # R3Extractor, group outputs
│   │   └── test_h3.py             # H3Extractor, morph computation
│   ├── brain/
│   │   └── test_musical_brain.py  # Unit instantiation, compute shapes
│   └── language/
│       └── test_brain_semantics.py # L3Orchestrator, group outputs
├── integration/
│   └── test_pipeline.py           # End-to-end MIBetaPipeline
└── validation/
    └── test_chill_test.py         # Chill detection validation
```

### 15.2 Test Coverage (Current State)

| Area | Tests | Status |
|------|-------|--------|
| Core constants | Boundary checks, dimension sums | Basic |
| Cochlea | Output shape, normalization | Basic |
| R3 extraction | 49D output, group dimensions | Basic |
| H3 extraction | Sparse computation, morph methods | Basic |
| Brain units | Instantiation, output shapes | Basic |
| L3 groups | Group output shapes | Basic |
| Pipeline e2e | Full waveform→MI-space | Basic |

> **Phase 7G** will expand test suite with comprehensive unit, integration, and benchmark tests.

---

## 16. Known Discrepancies

Code vs documentation delta from DISCREPANCY-REGISTRY.md. Three categories:

### 16.1 EXPECTED (Code Intentionally Behind Docs — Fix in Phase 7)

| # | Category | Code | Docs | Phase 7 Fix |
|--:|----------|------|------|-------------|
| 1 | h3_demand | ALL 94 models return `()` empty | Each model has 8-24 H3DemandSpec tuples | 7B |
| 2 | R3_DIM | 49 | 128 (v2.0.0 with groups F-K) | 7C |
| 3 | H3_TOTAL_DIM | 2304 (49×32×24×3 effective) | 294,912 (128×32×24×3) | 7D (after R3 v2) |
| 4 | ASU MECHANISM_NAMES | `("ASA",)` for all 9 | `("BEP","ASA")` for all 9 | 7B |
| 5 | Gamma OUTPUT_DIM | 10 (all gamma models) | 9 (docs specify 9D) | 7B |
| 6 | FULL_NAME mismatches | Various models | Different names in docs | 7B |
| 7 | Model compute() | Returns zeros | Should compute real outputs | 7B+ |
| 8 | L3 adapters | All stubs (return raw tensor) | Should map unit→semantic | 7E |
| 9 | Missing models | 94 files | 96 in docs (CHPI, SSRI doc-only) | 7A |
| 10 | L3 integration | Not wired in MIBetaPipeline | Should be included in MI-space | 7E |
| 11 | Mechanism caching | Skipped (Phase 1) | MechanismRunner should pre-compute | 7B |
| 12 | Pathway routing | Passthrough (full tensors) | Should extract specific dims | 7F |

### 16.2 CODE-BUG (Code Inconsistency — Fix in Phase 7)

| # | Bug | Details | Fix |
|--:|-----|---------|-----|
| 1 | CIRCUITS vs CIRCUIT_NAMES | `CIRCUITS` has 5 entries, `CIRCUIT_NAMES` has 6 (includes "imagery") | 7A: Add "imagery" to CIRCUITS |

### 16.3 DOC-BUG (Documentation Errors — Already Fixed in Phase 6)

7 documentation bugs were identified and fixed during Phase 6 validation. See `Docs/Beta/DISCREPANCY-REGISTRY.md` for details.

---

## 17. Phase 7 Roadmap

Implementation targets organized by sub-phase:

| Sub-Phase | Description | Files | Depends On |
|:---------:|-------------|------:|:----------:|
| **7A** | Foundation: CHPI.py + SSRI.py, fix CIRCUITS | 4 | — |
| **7B** | C3 Model Sync: h3_demand + attribute fixes (94 models) | 94 | 7A |
| **7C** | R3 v2 Expansion: 49D→128D, new groups F-K | ~15 | 7A |
| **7D** | H3 Updates: demand aggregation for R3 v2 range | ~5 | 7C |
| **7E** | L3 Adapter Implementation: 9 stubs → real mapping | 9 | 7B |
| **7F** | Cross-Unit: pathways, regions, neurochemical updates | ~10 | 7B |
| **7G** | Test Suite: unit + integration + benchmark | ~10 | 7A-7F |
| **7H** | Validation Run: pytest + full pipeline | — | 7G |

**Dependency graph**:
```
7A → 7B → 7E ─┐
          └→ 7F ┤→ 7G → 7H
7A → 7C → 7D ──┘
```

**Quality gates** (9):
1. 96 model files exist (94 updated + CHPI + SSRI)
2. All 94 h3_demand properties populated
3. All OUTPUT_DIM / MECHANISM_NAMES / FULL_NAME match docs
4. R3_DIM=128 with 0-48 backward-compatible
5. All 6 new R3 groups (F-K) produce correct output
6. L3 9 adapters produce meaningful semantic mappings
7. CIRCUITS constant reconciled (5→6)
8. `pytest tests/ -v` — 100% pass
9. `python -m mi_beta` — end-to-end without errors

---

**End of MI-CODE-ARCHITECTURE.md** | v1.0.0 | 2026-02-13
