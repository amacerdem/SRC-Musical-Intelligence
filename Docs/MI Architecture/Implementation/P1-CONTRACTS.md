# Phase 1: Contracts — Interfaces & Data Types

**Phase**: P1
**Depends on**: Nothing (first phase)
**Output**: 14 Python files in `Musical_Intelligence/contracts/`
**Gate**: G1 — all contracts importable, `validate_constants()` callable

---

## Overview

Contracts define the type system for the entire MI codebase. Every subsequent phase depends on these interfaces. There are two categories:

1. **Frozen dataclasses** (P1.1): Immutable value types with validation
2. **Abstract base classes** (P1.2): Interface contracts with abstract methods

Implementation order: dataclasses first (no dependencies), then ABCs (depend on dataclasses).

---

## P1.1 — Frozen Dataclasses

### `contracts/dataclasses/__init__.py`

**Purpose**: Re-export all dataclasses for convenient import.
**Exports**: All 8 dataclass types.
**No primary docs** — pure re-export module.

---

### `contracts/dataclasses/citation.py`

**Purpose**: Single empirical finding with effect size.

**Primary Docs**:
- `Docs/C³/Contracts/ModelMetadata.md` — Citation subsection: fields, computed properties

**Related Docs**:
- Any model doc Section 13 (References) — see actual citation usage patterns

**Depends On**: Nothing (leaf type).

**Exports**: `Citation`

**Key Constraints**:
- Frozen dataclass (immutable after creation)
- Fields: `author` (str), `year` (int), `finding` (str), `effect_size` (str)
- Computed property: `short_ref` → `"Author YEAR"` format
- `effect_size` may be empty string if N/A

**Verification Checklist**:
- [ ] All 4 fields present with correct types
- [ ] `short_ref` property returns `f"{self.author} {self.year}"`
- [ ] Frozen (cannot mutate after init)
- [ ] Matches `Docs/C³/Contracts/ModelMetadata.md` Citation section exactly

---

### `contracts/dataclasses/layer_spec.py`

**Purpose**: Defines a single E/M/P/F output layer — a contiguous slice of model output.

**Primary Docs**:
- `Docs/C³/Contracts/LayerSpec.md` — all fields, validation rules, layer code convention

**Related Docs**:
- Any model doc Section 6 (Output Space) — see actual LayerSpec usage
- `Docs/C³/Models/SPU-α1-BCH/BCH.md` Section 6 — concrete example

**Depends On**: Nothing (leaf type).

**Exports**: `LayerSpec`

**Key Constraints**:
- Frozen dataclass
- Fields: `code` (str), `name` (str), `start` (int), `end` (int), `dim_names` (Tuple[str, ...])
- Computed property: `dim` → `end - start`
- Validation in `__post_init__`:
  - `len(dim_names) == end - start` (ValueError if not)
  - `start >= 0`
  - `end > start`
- Layer codes: E (Extraction/Neurochemical), M (Mechanism/Circuit), P (Psychological), F (Forecast)

**Verification Checklist**:
- [ ] 5 fields match doc exactly
- [ ] `dim` property works correctly
- [ ] Validation raises ValueError on mismatched dim_names length
- [ ] Validation raises ValueError on start < 0 or end <= start
- [ ] Indexing: `output[..., layer.start:layer.end]` extracts layer

---

### `contracts/dataclasses/demand_spec.py`

**Purpose**: Typed declaration of a single H3 temporal demand (4-tuple address).

**Primary Docs**:
- `Docs/C³/Contracts/H3DemandSpec.md` — all fields, as_tuple(), law semantics

**Related Docs**:
- `Docs/H³/Registry/HorizonCatalog.md` — valid horizon values (0-31)
- `Docs/H³/Registry/MorphCatalog.md` — valid morph values (0-23)
- `Docs/H³/Registry/LawCatalog.md` — law semantics (0=memory, 1=prediction, 2=integration)
- Any model doc Section 5 — see actual H3DemandSpec usage patterns

**Depends On**: Nothing (leaf type).

**Exports**: `H3DemandSpec`

**Key Constraints**:
- Frozen dataclass
- Address fields: `r3_idx` (int), `horizon` (int), `morph` (int), `law` (int)
- Label fields: `r3_name` (str), `horizon_label` (str), `morph_name` (str), `law_name` (str)
- Justification: `purpose` (str), `citation` (str)
- Method: `as_tuple()` → `(r3_idx, horizon, morph, law)`
- Law indices: 0=Memory, 1=Prediction, 2=Integration

**Verification Checklist**:
- [ ] 10 fields (4 int indices + 4 str labels + 2 justification)
- [ ] `as_tuple()` returns correct 4-tuple
- [ ] All fields documented match doc exactly
- [ ] Frozen

---

### `contracts/dataclasses/feature_spec.py`

**Purpose**: Per-feature metadata for R3 feature registration.

**Primary Docs**:
- `Docs/R³/Contracts/R3FeatureSpec.md` — fields, validation

**Related Docs**:
- `Docs/R³/Registry/FeatureCatalog.md` — see all 128 feature entries

**Depends On**: Nothing (leaf type).

**Exports**: `R3FeatureSpec`

**Key Constraints**:
- Frozen dataclass
- Fields: `name` (str), `group` (str), `index` (int), `description` (str), `citation` (str), `unit` (str)
- Validation: `0 <= index < 128` (v2 range)

**Verification Checklist**:
- [ ] 6 fields match doc
- [ ] Index validation with v2 upper bound (128, not 49)
- [ ] Frozen

---

### `contracts/dataclasses/pathway_spec.py`

**Purpose**: Directed data dependency between models in different cognitive units.

**Primary Docs**:
- `Docs/C³/Contracts/CrossUnitPathway.md` — all fields, computed properties

**Related Docs**:
- `Docs/C³/Pathways/00-INDEX.md` — see all 5 pathway definitions
- `Docs/C³/Pathways/P1-SPU-ARU.md` — concrete example

**Depends On**: Nothing (leaf type).

**Exports**: `CrossUnitPathway`

**Key Constraints**:
- Frozen dataclass
- Fields: `pathway_id` (str), `name` (str), `source_unit` (str), `source_model` (str),
  `source_dims` (Tuple[str, ...]), `target_unit` (str), `target_model` (str),
  `correlation` (str), `citation` (str)
- Computed: `is_intra_unit`, `is_inter_unit`, `edge` → (source_unit, target_unit)
- Topological constraint: no cycles allowed in unit dependency graph

**Verification Checklist**:
- [ ] 9 fields match doc exactly
- [ ] `is_intra_unit` returns True when source_unit == target_unit
- [ ] `edge` returns correct 2-tuple
- [ ] Frozen

---

### `contracts/dataclasses/brain_region.py`

**Purpose**: Neuroanatomical identity with MNI152 coordinates.

**Primary Docs**:
- `Docs/C³/Contracts/BrainRegion.md` — fields, MNI convention, validation

**Related Docs**:
- `Docs/C³/Regions/Cortical.md` — cortical regions with Brodmann areas
- `Docs/C³/Regions/Subcortical.md` — subcortical without Brodmann
- `Docs/C³/Regions/Brainstem.md` — brainstem structures

**Depends On**: Nothing (leaf type).

**Exports**: `BrainRegion`

**Key Constraints**:
- Frozen dataclass
- Fields: `name` (str), `abbreviation` (str), `hemisphere` (str),
  `mni_coords` (Tuple[int, int, int]), `brodmann_area` (Optional[int]),
  `function` (str, default=""), `evidence_count` (int, default=0)
- Validation: hemisphere in {"L", "R", "bilateral"}; mni_coords is 3-tuple
- Computed: `is_cortical` (has brodmann_area), `is_subcortical` (no brodmann_area)
- MNI convention: x (L-/R+), y (P-/A+), z (I-/S+)

**Verification Checklist**:
- [ ] 7 fields match doc
- [ ] Validation raises ValueError on invalid hemisphere
- [ ] Validation raises ValueError on non-3-tuple mni_coords
- [ ] `is_cortical` / `is_subcortical` properties work
- [ ] Frozen

---

### `contracts/dataclasses/model_metadata.py`

**Purpose**: Evidence provenance, confidence, and falsification criteria.

**Primary Docs**:
- `Docs/C³/Contracts/ModelMetadata.md` — ModelMetadata fields, validation, tier definitions

**Related Docs**:
- `Docs/C³/Tiers/Alpha.md`, `Beta.md`, `Gamma.md` — tier criteria details
- Any model doc Section 3 (Scientific Foundation) — see actual evidence data
- Any model doc Section 10 (Falsification Criteria) — see criteria format

**Depends On**: `citation.py` (uses Citation type).

**Exports**: `ModelMetadata`

**Key Constraints**:
- Frozen dataclass
- Fields: `citations` (Tuple[Citation, ...]), `evidence_tier` (str),
  `confidence_range` (Tuple[float, float]), `falsification_criteria` (Tuple[str, ...]),
  `version` (str, default="1.0.0"), `paper_count` (Optional[int])
- Validation:
  - `evidence_tier` in {"alpha", "beta", "gamma"}
  - `0 <= low <= high <= 1` for confidence_range
  - `falsification_criteria` non-empty (Popper 1959: every model must be falsifiable)
- Computed: `effective_paper_count`, `is_mechanistic`
- Tier thresholds: alpha (k≥10, >90%), beta (5≤k<10, >70%), gamma (k<5, <70%)

**Verification Checklist**:
- [ ] All fields match doc
- [ ] 3 validation rules raise ValueError correctly
- [ ] `effective_paper_count` counts unique (author, year) pairs
- [ ] `is_mechanistic` returns True only for alpha tier
- [ ] Citation import works
- [ ] Frozen

---

### `contracts/dataclasses/semantic_output.py`

**Purpose**: Immutable output container for a single L³ semantic group.

**Primary Docs**:
- `Docs/L³/Contracts/SemanticGroupOutput.md` — fields, validation

**Related Docs**:
- `Docs/L³/Groups/Independent/Alpha.md` — see output format example

**Depends On**: Nothing (leaf type, uses torch.Tensor at runtime).

**Exports**: `SemanticGroupOutput`

**Key Constraints**:
- Frozen dataclass
- Fields: `group_name` (str), `level` (int), `tensor` (Tensor, shape (B,T,D)),
  `dimension_names` (Tuple[str, ...])
- Validation: `len(dimension_names) == tensor.shape[-1]`
- Range convention: α-ε,η,θ = [0,1]; ζ = [-1,+1]

**Verification Checklist**:
- [ ] 4 fields match doc
- [ ] Post-init validation checks dimension_names length vs tensor shape
- [ ] Frozen

---

## P1.2 — Abstract Base Classes

### `contracts/bases/__init__.py`

**Purpose**: Re-export all ABCs.
**Exports**: All 5 ABC types.

---

### `contracts/bases/base_mechanism.py`

**Purpose**: ABC for model-internal sub-computations (10 mechanisms, each 30D).

**Primary Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` — constants, abstract methods, validation

**Related Docs**:
- `Docs/C³/Mechanisms/00-INDEX.md` — see all 10 mechanisms
- `Docs/C³/Mechanisms/PPC.md` — concrete example of mechanism spec

**Depends On**: `demand_spec.py` (H3DemandSpec type).

**Exports**: `BaseMechanism`

**Key Constraints**:
- ABC (cannot instantiate directly)
- Class constants to override: `NAME`, `FULL_NAME`, `OUTPUT_DIM` (default 30), `HORIZONS`
- Abstract property: `h3_demand` → Set[Tuple[int,int,int,int]]
- Abstract method: `compute(h3_features, r3_features)` → Tensor (B, T, OUTPUT_DIM)
- Computed helpers: `demand_count`, `horizons_used`, `r3_indices_used`
- Validation: NAME/FULL_NAME non-empty, OUTPUT_DIM > 0, HORIZONS matches h3_demand

**Verification Checklist**:
- [ ] Cannot instantiate BaseMechanism directly
- [ ] Subclass must override NAME, FULL_NAME, OUTPUT_DIM, HORIZONS
- [ ] Subclass must implement h3_demand property and compute() method
- [ ] Validation rules from doc all implemented
- [ ] All computed helpers work

---

### `contracts/bases/base_model.py`

**Purpose**: THE central contract for all 96 cognitive models.

**Primary Docs**:
- `Docs/C³/Contracts/BaseModel.md` — THE definitive specification

**Related Docs**:
- `Docs/C³/Contracts/LayerSpec.md` — LayerSpec used in LAYERS
- `Docs/C³/Contracts/H3DemandSpec.md` — H3DemandSpec used in h3_demand
- `Docs/C³/Contracts/CrossUnitPathway.md` — used in CROSS_UNIT_READS
- `Docs/C³/Contracts/BrainRegion.md` — used in brain_regions
- `Docs/C³/Contracts/ModelMetadata.md` — used in metadata
- `Docs/C³/Models/SPU-α1-BCH/BCH.md` — concrete alpha model example
- `Docs/C³/Models/SPU-β1-STAI/STAI.md` — concrete beta model example

**Depends On**: All P1.1 dataclasses (layer_spec, demand_spec, pathway_spec, brain_region, model_metadata).

**Exports**: `BaseModel`

**Key Constraints**:
- ABC (cannot instantiate directly)
- Class constants: `NAME`, `FULL_NAME`, `UNIT`, `TIER`, `OUTPUT_DIM`,
  `MECHANISM_NAMES` (Tuple[str, ...]), `CROSS_UNIT_READS` (Tuple[CrossUnitPathway, ...]),
  `LAYERS` (Tuple[LayerSpec, ...])
- Abstract properties: `h3_demand`, `dimension_names`, `brain_regions`, `metadata`
- Abstract method: `compute(mechanism_outputs, h3_features, r3_features, cross_unit_inputs)` → Tensor
- Computed: `h3_demand_tuples()`, `layer_dim_names`, `cross_unit_dependency_units`
- `validate_constants()`:
  1. NAME, FULL_NAME, UNIT non-empty
  2. TIER in {"alpha", "beta", "gamma"}
  3. OUTPUT_DIM > 0
  4. LAYERS covers [0, OUTPUT_DIM) without gaps/overlaps
  5. LAYERS dim_names concatenated == dimension_names

**Verification Checklist**:
- [ ] All 8 class constants defined
- [ ] All 4 abstract properties defined
- [ ] compute() signature matches doc exactly
- [ ] validate_constants() implements all 5 rules
- [ ] h3_demand_tuples() deduplicates correctly
- [ ] Cannot instantiate BaseModel directly

---

### `contracts/bases/base_unit.py`

**Purpose**: ABC for cognitive unit grouping related models.

**Primary Docs**:
- `Docs/C³/Contracts/BaseCognitiveUnit.md` — constants, abstract members, computed properties

**Related Docs**:
- `Docs/C³/Units/00-INDEX.md` — all 9 units
- `Docs/C³/Units/SPU.md` — concrete unit example

**Depends On**: `base_model.py`.

**Exports**: `BaseCognitiveUnit`

**Key Constraints**:
- ABC
- Constants: `UNIT_NAME`, `FULL_NAME`, `CIRCUIT`, `POOLED_EFFECT` (float, 0.0 for experimental)
- Abstract: `models` property → List[BaseModel], `compute()` method
- Computed: `active_models`, `total_dim`, `model_names`, `mechanism_names`,
  `h3_demand`, `dimension_names`, `is_validated`, `model_ranges`
- Validation: 6 rules (see doc)

**Verification Checklist**:
- [ ] 4 constants, 2 abstract members, 8 computed properties
- [ ] 6 validation rules
- [ ] `model_ranges` returns correct start/end per model

---

### `contracts/bases/base_spectral_group.py`

**Purpose**: ABC for R³ spectral feature groups (11 groups A-K).

**Primary Docs**:
- `Docs/R³/Contracts/BaseSpectralGroup.md` — constants, compute(), validation

**Related Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` — 3-stage DAG context
- `Docs/R³/Registry/DimensionMap.md` — group boundaries

**Depends On**: Nothing from P1.1 (uses torch.Tensor at runtime).

**Exports**: `BaseSpectralGroup`

**Key Constraints**:
- ABC
- Constants: `GROUP_NAME`, `DOMAIN`, `OUTPUT_DIM`, `INDEX_RANGE` (Tuple[int, int]),
  `STAGE` (int: 1, 2, or 3), `DEPENDENCIES` (Tuple[str, ...], group names needed)
- Abstract: `compute(mel)` → Tensor (B, T, OUTPUT_DIM) for Stage 1;
  `compute_with_deps(mel, deps)` for Stage 2-3
- Abstract property: `feature_names` → Tuple[str, ...]
- Validation: name uniqueness, dim consistency, index range contiguity

**Verification Checklist**:
- [ ] STAGE and DEPENDENCIES fields present (v2 addition)
- [ ] compute_with_deps() for dependent groups
- [ ] validate() checks all rules from doc

---

### `contracts/bases/base_semantic_group.py`

**Purpose**: ABC for L³ semantic groups (8 groups α-θ).

**Primary Docs**:
- `Docs/L³/Contracts/BaseSemanticGroup.md` — constants, compute(), validation

**Related Docs**:
- `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` — computation phases
- `Docs/L³/Groups/Independent/Alpha.md` — concrete example

**Depends On**: `semantic_output.py`.

**Exports**: `BaseSemanticGroup`

**Key Constraints**:
- ABC
- Constants: `LEVEL` (1-8), `GROUP_NAME`, `DISPLAY_NAME`, `OUTPUT_DIM`
- Abstract: `compute(brain_output, **kwargs)` → SemanticGroupOutput
- Abstract property: `dimension_names`
- Validation: LEVEL range, name non-empty, dimension_names length == OUTPUT_DIM

**Verification Checklist**:
- [ ] LEVEL field (1-8)
- [ ] compute() accepts **kwargs for dependency injection
- [ ] Validation rules from doc

---

## P1.3 — Package Init

### `contracts/__init__.py`

**Purpose**: Top-level contracts package init.
**Exports**: Re-export from dataclasses/ and bases/ sub-packages.

---

## Verification Gate G1

After completing all P1 files:

```python
# G1 verification script
from Musical_Intelligence.contracts import (
    LayerSpec, H3DemandSpec, R3FeatureSpec, CrossUnitPathway,
    BrainRegion, Citation, ModelMetadata, SemanticGroupOutput,
    BaseModel, BaseCognitiveUnit, BaseMechanism,
    BaseSpectralGroup, BaseSemanticGroup
)

# Test LayerSpec validation
try:
    LayerSpec(code="E", name="Test", start=0, end=3, dim_names=("a",))  # should raise
    assert False, "Should have raised ValueError"
except ValueError:
    pass

# Test BrainRegion validation
try:
    BrainRegion(name="Test", abbreviation="T", hemisphere="X",
                mni_coords=(0,0,0))  # should raise
    assert False, "Should have raised ValueError"
except ValueError:
    pass

# Test ModelMetadata validation
try:
    ModelMetadata(citations=(), evidence_tier="alpha",
                  confidence_range=(0.9, 0.95),
                  falsification_criteria=())  # should raise (empty criteria)
    assert False, "Should have raised ValueError"
except ValueError:
    pass

print("G1 PASSED: All contracts importable and validations work")
```
