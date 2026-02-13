# C³ Contracts -- Index

> **Module**: `mi_beta.contracts`
> **Role**: Foundational dependency layer -- every other `mi_beta` module imports from here.

The contracts package defines the abstract base classes and specification dataclasses that enforce architectural invariants across the entire MI-Beta system. Contracts are divided into two categories:

1. **Specification Dataclasses** (frozen, no dependencies on each other): define the data shapes and metadata that models, units, and mechanisms must declare.
2. **Abstract Base Classes** (depend on the dataclasses above): define the compute interfaces that all cognitive components must implement.

---

## Contract Inventory

| # | Contract | Class | Kind | Purpose | Code Reference |
|---|----------|-------|------|---------|----------------|
| 1 | [BaseModel](BaseModel.md) | `BaseModel` | ABC | Central contract for all cognitive models; enforces metadata, layers, demands, and compute signature | `mi_beta/contracts/base_model.py` |
| 2 | [BaseCognitiveUnit](BaseCognitiveUnit.md) | `BaseCognitiveUnit` | ABC | Groups related models sharing a neural circuit; manages execution order and output concatenation | `mi_beta/contracts/base_unit.py` |
| 3 | [BaseMechanism](BaseMechanism.md) | `BaseMechanism` | ABC | Model-internal sub-computation; reads H3/R3 features and produces a fixed-dimensional output | `mi_beta/contracts/base_mechanism.py` |
| 4 | [LayerSpec](LayerSpec.md) | `LayerSpec` | Dataclass | Defines E/M/P/F output layer slices within a model's output tensor | `mi_beta/contracts/layer_spec.py` |
| 5 | [H3DemandSpec](H3DemandSpec.md) | `H3DemandSpec` | Dataclass | Typed declaration of a single H3 temporal demand with scientific justification | `mi_beta/contracts/demand_spec.py` |
| 6 | [CrossUnitPathway](CrossUnitPathway.md) | `CrossUnitPathway` | Dataclass | Declares a directed data dependency between models in different cognitive units | `mi_beta/contracts/pathway_spec.py` |
| 7 | [BrainRegion](BrainRegion.md) | `BrainRegion` | Dataclass | Anatomical brain region with MNI152 coordinates and Brodmann area | `mi_beta/contracts/brain_region.py` |
| 8 | [ModelMetadata](ModelMetadata.md) | `ModelMetadata` + `Citation` | Dataclass | Evidence provenance: citations, tier, confidence range, falsification criteria | `mi_beta/contracts/model_metadata.py` |

---

## Additional Dataclasses

These supporting contracts are also exported from the package but do not have dedicated documentation pages:

| Contract | Class | Purpose | Code Reference |
|----------|-------|---------|----------------|
| R3FeatureSpec | `R3FeatureSpec` | Registration record for a single R3 spectral feature (index 0-48) | `mi_beta/contracts/feature_spec.py` |
| NeurochemicalType | `NeurochemicalType` | Enum of 6 neurotransmitter systems (DA, opioid, 5-HT, NE, GABA, glutamate) | `mi_beta/contracts/neurochemical.py` |
| NeurochemicalState | `NeurochemicalState` | Mutable write/read registry for region-specific neurochemical tensors | `mi_beta/contracts/neurochemical.py` |
| SemanticGroupOutput | `SemanticGroupOutput` | Output container for L3 semantic interpretation groups | `mi_beta/contracts/base_semantic_group.py` |
| BaseSemanticGroup | `BaseSemanticGroup` | ABC for L3 semantic groups (8 epistemological levels) | `mi_beta/contracts/base_semantic_group.py` |
| BaseSpectralGroup | `BaseSpectralGroup` | ABC for R3 spectral feature groups (5 groups, 49D total) | `mi_beta/contracts/base_spectral_group.py` |

---

## Dependency Graph

```
Dataclasses (leaf nodes, no dependencies):
  H3DemandSpec, R3FeatureSpec, LayerSpec, CrossUnitPathway,
  BrainRegion, NeurochemicalType, NeurochemicalState,
  ModelMetadata, Citation, SemanticGroupOutput

ABCs (depend on dataclasses above):
  BaseMechanism   -> (H3DemandSpec)
  BaseModel       -> (LayerSpec, H3DemandSpec, CrossUnitPathway, BrainRegion, ModelMetadata)
  BaseCognitiveUnit -> (BaseModel)
  BaseSpectralGroup -> ()
  BaseSemanticGroup -> (SemanticGroupOutput)
```
