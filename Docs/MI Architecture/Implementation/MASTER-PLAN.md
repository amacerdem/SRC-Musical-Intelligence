# Master Implementation Plan

**Version**: 1.0.0
**Date**: 2026-02-14
**Purpose**: Convert 395 documentation files into ~297 Python code files with zero information loss.

---

## §1. Architecture Overview

### 1.1 System Pipeline

```
Audio (waveform, 44100 Hz)
  │
  ▼
Cochlea (128-mel spectrogram @ 172.27 Hz, hop=256)
  │
  ▼
R³ Spectral Space (128D, 11 groups A-K, 3-stage DAG)
  │
  ▼
H³ Temporal Morphology (~8,600 sparse 4-tuples from 294,912D theoretical)
  │
  ▼
C³ Brain Models (96 models → 10 mechanisms → 9 units → 1,006D output)
  │
  ▼
L³ Semantic Space (104D, 8 groups α-θ, 96 vocabulary terms)
  │
  ▼
MI-space output: 1,366D per frame (128 + 128 + 1,006 + 104)
```

### 1.2 Package Structure

Root package: `Musical_Intelligence/`

```
Musical_Intelligence/
├── contracts/           P1: Interfaces (14 files)
│   ├── dataclasses/     Frozen dataclass value types
│   └── bases/           Abstract base classes
├── ear/                 P2: Signal processing
│   ├── cochlea/         Mel spectrogram (3 files)
│   ├── r3/              R³ spectral (62 files)
│   └── h3/              H³ temporal (38 files)
├── brain/               P3: Cognitive models (156 files)
│   ├── mechanisms/      10 shared mechanisms
│   ├── units/           9 cognitive units (96 models)
│   ├── pathways/        5 cross-unit pathways
│   ├── circuits/        6 circuit definitions
│   ├── regions/         26 brain regions
│   └── neurochemicals/  4 neurochemical systems
├── semantics/           P4: L³ semantic (25 files)
│   ├── groups/          8 semantic groups
│   ├── adapters/        9 unit adapters
│   └── vocabulary/      96-term vocabulary
├── pipeline/            P5: End-to-end (3 files)
└── validation/          P6: Lossless verification (6 files)
```

### 1.3 Design Principles

1. **Contracts-first**: All ABCs and dataclasses exist before any implementation
2. **Doc-driven**: Every line of code traces to a documentation source
3. **Max 1000 lines**: No code file exceeds ~1000 lines
4. **Deterministic**: All models are zero-parameter, deterministic functions
5. **White-box**: Every output dimension has a name, formula, citation, and range

---

## §2. Phase Sequencing

### Phase 1: Contracts (No Dependencies)

**Goal**: Establish all interfaces before any implementation.
**Input docs**: `Docs/C³/Contracts/`, `Docs/R³/Contracts/`, `Docs/H³/Contracts/`, `Docs/L³/Contracts/`
**Output**: 14 Python files in `contracts/`
**Detail**: See [P1-CONTRACTS.md](P1-CONTRACTS.md)

Sub-phases:
- P1.1: Leaf dataclasses (no cross-dependencies)
- P1.2: ABC base classes (depend on P1.1 dataclasses)
- P1.3: Contract validation tests

### Phase 2: Ear — R³ + H³ (Depends on P1)

**Goal**: Complete signal processing pipeline from mel to temporal features.
**Parallelizable**: R³ and H³ can be implemented in parallel.

- **P2-R3**: 62 files. See [P2-EAR-R3.md](P2-EAR-R3.md)
- **P2-H3**: 38 files. See [P2-EAR-H3.md](P2-EAR-H3.md)
- **P2-Cochlea**: 3 files (included in P5-PIPELINE.md)

Sub-phases:
- P2.1: Constants and registries (both layers)
- P2.2: Core components (R³ groups, H³ morphology/attention/demand)
- P2.3: Pipeline orchestrators (R3Extractor, H3Extractor)
- P2.4: Integration tests

### Phase 3: Brain — C³ (Depends on P1 + P2)

**Goal**: Implement all 96 cognitive models with scientific fidelity.
**Detail**: See [P3-BRAIN.md](P3-BRAIN.md)

Sub-phases:
- P3.1: 10 Mechanisms (shared sub-computations)
- P3.2: MechanismRunner (cache and dispatch)
- P3.3: Supporting infrastructure (circuits, regions, neurochemicals)
- P3.4: 9 Unit shells (BaseCognitiveUnit subclasses)
- P3.5: 96 Models (batch by unit, starting with SPU)
- P3.6: 5 Pathways + PathwayRunner
- P3.7: BrainOrchestrator (5-phase execution)

### Phase 4: Semantics — L³ (Depends on P1 + P3)

**Goal**: Map brain outputs to 104D semantic interpretation.
**Detail**: See [P4-SEMANTICS.md](P4-SEMANTICS.md)

Sub-phases:
- P4.1: 8 Semantic groups (α through θ, respecting dependency order)
- P4.2: 9 Unit adapters
- P4.3: Vocabulary system (96 terms, 12 axes, 64 gradations)
- P4.4: L3Orchestrator

### Phase 5: Pipeline (Depends on P1-P4)

**Goal**: End-to-end Audio → MI-space.
**Detail**: See [P5-PIPELINE.md](P5-PIPELINE.md)

### Phase 6: Validation (Depends on P1-P5)

**Goal**: Verify zero information loss from docs to code.
**Detail**: See [P6-VALIDATION.md](P6-VALIDATION.md)

---

## §3. Agent Protocol — MANDATORY

Every implementing agent MUST follow this protocol for EACH code file.

### 3.1 The READ → ANALYZE → IMPLEMENT → VERIFY Cycle

```
┌─────────────────────────────────────────────────────┐
│  For each code file in the sub-plan:                │
│                                                     │
│  1. READ primary doc(s)                             │
│     • Open and fully read every doc listed under    │
│       "Primary Docs" for that file                  │
│     • Do NOT skip any section                       │
│                                                     │
│  2. ANALYZE related docs                            │
│     • Read docs listed under "Related Docs"         │
│     • Understand cross-references and dependencies  │
│     • Check DISCREPANCY-REGISTRY.md for known gaps  │
│                                                     │
│  3. IMPLEMENT                                       │
│     • Write code that captures ALL extractable info │
│     • Use exact values from docs (coefficients,     │
│       indices, dimension names, ranges)             │
│     • Include docstrings from doc Section 1 text    │
│     • Follow the contract ABCs from P1              │
│                                                     │
│  4. VERIFY                                          │
│     • Run the file-specific verification checklist  │
│     • Confirm: all constants match docs             │
│     • Confirm: all formulas match docs              │
│     • Confirm: file is under 1000 lines             │
│                                                     │
│  ⚠ NEVER implement from memory or assumptions.     │
│    ALWAYS re-read the docs for each file.           │
└─────────────────────────────────────────────────────┘
```

### 3.2 Documentation Path Convention

All doc paths in sub-plans are relative to project root:
`/Volumes/SRC-9/SRC Musical Intelligence/`

Example: `Docs/C³/Contracts/BaseModel.md` means:
`/Volumes/SRC-9/SRC Musical Intelligence/Docs/C³/Contracts/BaseModel.md`

### 3.3 Code Path Convention

All code paths are relative to package root:
`/Volumes/SRC-9/SRC Musical Intelligence/Musical_Intelligence/`

Example: `contracts/dataclasses/layer_spec.py` means:
`/Volumes/SRC-9/SRC Musical Intelligence/Musical_Intelligence/contracts/dataclasses/layer_spec.py`

### 3.4 What "Lossless" Means

Every piece of **extractable information** from docs must appear in code or data:

| Doc Information Type | Code Representation |
|---------------------|---------------------|
| Class constants (NAME, OUTPUT_DIM, ...) | Python class attributes |
| Mathematical formulas | `compute()` method body |
| Coefficient values (0.40, 0.85, ...) | Named constants or inline values with comments |
| H3 demand tuples | `h3_demand` property returning tuple of H3DemandSpec |
| R3 input indices | Class constant (tuple of ints) |
| LayerSpec (E/M/P/F) | `LAYERS` class constant |
| Dimension names | `dimension_names` property |
| Brain regions + MNI | `brain_regions` property returning BrainRegion instances |
| Citations | `metadata` property returning ModelMetadata |
| Falsification criteria | `ModelMetadata.falsification_criteria` |
| "What does this model simulate?" | Class docstring |
| Feature catalog entries | Constants module + R3FeatureSpec instances |
| Horizon/morph/law catalogs | Constants modules with full metadata |
| Cross-unit pathways | CrossUnitPathway dataclass instances |
| Vocabulary terms (96 words) | Python dict/tuple in vocabulary module |

**NOT converted to code** (stays in docs only):
- CHANGELOGs, Migration guides, Extension guides
- Historical design rationale (upgrade_beta/ files)
- Process tracking (Beta_upgrade.md, PROGRESS files)
- Discrepancy registry (temporary Phase tracking)

### 3.5 Known Discrepancies

Agents MUST read `Docs/Beta/DISCREPANCY-REGISTRY.md` before starting.

Key rules:
- Use **doc values** (v2), not old code values (v1), for all new implementations
- R3_DIM = 128 (not 49)
- H3 total theoretical = 294,912 (not 2,304)
- All models get populated h3_demand (not empty tuples)
- Gamma OUTPUT_DIM follows doc (9), not old code (10)
- MECHANISM_NAMES follows doc values
- FULL_NAME follows doc Section 1 header

---

## §4. Information Taxonomy

The 395 markdown files contain 6 types of information:

### Type 1: Executable Specification → PYTHON CODE
Sections 4-7, 11 of model docs; contract docs; pipeline docs.

### Type 2: Scientific Metadata → DATACLASS INSTANCES
Sections 3, 8, 10, 13 of model docs; region/circuit/neurochemical docs.

### Type 3: Constants/Registry → PYTHON CONSTANTS MODULES
Registry docs (FeatureCatalog, HorizonCatalog, MorphCatalog, etc.)

### Type 4: Validation Criteria → TEST ASSERTIONS
Standards, Validation docs; Section 10 falsification criteria.

### Type 5: Narrative/Explanation → DOCSTRINGS
Sections 1, 2, 9 of model docs; architecture overview texts.

### Type 6: Process/Historical → NOT IN CODE
CHANGELOGs, Migration, Extension guides, Beta tracking.

---

## §5. Verification Gates

Each phase has a verification gate that must pass before the next phase starts.

| Gate | Criteria | Automated? |
|------|----------|:----------:|
| **G1** (after P1) | All contracts importable, `validate_constants()` runs, type checks pass | Yes |
| **G2** (after P2) | R3Extractor produces (B,T,128), H3Extractor produces sparse dict | Yes |
| **G3** (after P3) | All 96 models instantiate, `validate_constants()` passes for each | Yes |
| **G4** (after P4) | L3Orchestrator produces (B,T,104) | Yes |
| **G5** (after P5) | MIPipeline produces (B,T,1366) from audio | Yes |
| **G6** (after P6) | Traceability matrix covers 100% of Type 1-4 doc information | Yes |

---

## §6. Sub-Plan File Format

Each sub-plan (P1 through P6) follows this format for every code file:

```markdown
### `path/to/file.py`

**Purpose**: One-line description.

**Primary Docs** (MUST read fully before implementing):
- `Docs/path/to/primary.md` — what to extract

**Related Docs** (read for context and cross-references):
- `Docs/path/to/related.md` — why it matters

**Depends On** (code files that must exist first):
- `contracts/dataclasses/layer_spec.py`

**Exports**:
- `ClassName` or `function_name`

**Key Constraints**:
- Specific rules for this file

**Verification Checklist**:
- [ ] Specific thing to verify
```

---

## §7. Batch Strategy for 96 Models (P3)

Models are implemented in unit batches. Order follows dependency graph:

```
Batch 1 (Independent units, parallelizable):
  SPU (9 models)  — perceptual baseline
  STU (14 models) — sensorimotor timing
  IMU (15 models) — integrative memory

Batch 2 (Independent units, parallelizable):
  ASU (9 models)  — auditory salience
  NDU (9 models)  — novelty detection
  MPU (10 models) — motor planning
  PCU (10 models) — predictive coding

Batch 3 (Dependent units, AFTER Batch 1+2):
  ARU (10 models) — needs SPU, IMU, STU via pathways P1, P3, P5
  RPU (10 models) — needs ARU via CROSS_UNIT_READS
```

Within each unit, implement in tier order: α → β → γ
(Alpha models are foundational; beta/gamma build on alpha patterns.)

---

## §8. File Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Package init | `__init__.py` | `contracts/__init__.py` |
| Dataclass | `snake_case.py` | `layer_spec.py` |
| ABC base | `base_*.py` | `base_model.py` |
| R³ group | `group.py` inside `groups/{letter}_{name}/` | `groups/a_consonance/group.py` |
| R³ feature | `descriptive_name.py` | `roughness.py` |
| H³ morph category | `category_name.py` | `distribution.py` |
| Mechanism | `three_letter.py` | `ppc.py` |
| Unit | `unit.py` inside `units/{unit_code}/` | `units/spu/unit.py` |
| Model | `acronym_lower.py` inside `models/` | `units/spu/models/bch.py` |
| Pathway | `p{n}_{source}_{target}.py` | `p1_spu_aru.py` |
| Semantic group | `greek_name.py` | `epsilon.py` |
| Adapter | `{unit}_adapter.py` | `spu_adapter.py` |
