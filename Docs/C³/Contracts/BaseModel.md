# BaseModel -- The Central Contract for All Cognitive Models

> **Code**: `mi_beta/contracts/base_model.py`
> **Kind**: Abstract Base Class (ABC)
> **Imports from**: `BrainRegion`, `H3DemandSpec`, `LayerSpec`, `ModelMetadata`, `CrossUnitPathway`

## Purpose

`BaseModel` is THE central contract for the MI-Beta architecture. A cognitive model is a deterministic, zero-parameter function that transforms H3 temporal features, R3 spectral features, and optional cross-unit inputs into a fixed-dimensional output tensor. Every output dimension must have a human-readable name, a scientific citation, a defined value range, and assignment to one of the E/M/P/F output layers.

Models are grouped into cognitive units (ARU, SPU, STU, IMU, etc.). Each model belongs to exactly one unit and one evidence tier (alpha/beta/gamma).

---

## Class Constants (must override in every subclass)

| Constant | Type | Description |
|----------|------|-------------|
| `NAME` | `str` | Short model identifier (e.g. `"SRP"`, `"AAC"`, `"VMM"`) |
| `FULL_NAME` | `str` | Full descriptive name (e.g. `"Striatal Reward Pathway"`) |
| `UNIT` | `str` | Parent cognitive unit (e.g. `"ARU"`, `"SPU"`, `"STU"`) |
| `TIER` | `str` | Evidence tier: `"alpha"` (>=10 studies), `"beta"` (5-9), `"gamma"` (<5) |
| `OUTPUT_DIM` | `int` | Total output dimensionality; must equal the sum of all LAYERS dims |
| `MECHANISM_NAMES` | `Tuple[str, ...]` | Names of internal mechanisms (e.g. `("AED", "CPD")`). Empty tuple if none |
| `CROSS_UNIT_READS` | `Tuple[CrossUnitPathway, ...]` | Declared cross-unit data dependencies. Empty if the model only reads H3/R3 |
| `LAYERS` | `Tuple[LayerSpec, ...]` | Output layer structure; each `LayerSpec` defines a semantic slice of the output tensor |

---

## Abstract Properties (must implement in every subclass)

### `h3_demand -> Tuple[H3DemandSpec, ...]`

All H3 temporal demands needed by this model. Each `H3DemandSpec` maps to a single scalar time series. The set of `as_tuple()` values is passed to the DemandTree for efficient H3 computation. May be empty for models that only read R3 features directly.

### `dimension_names -> Tuple[str, ...]`

Ordered names for every output dimension. `len(dimension_names)` MUST equal `OUTPUT_DIM`. Names must be unique within the model and follow `snake_case` convention.

### `brain_regions -> Tuple[BrainRegion, ...]`

Brain regions associated with this model's computation. Used for MNI152 visualisation and anatomical grounding.

### `metadata -> ModelMetadata`

Evidence provenance: citations, tier, confidence range, falsification criteria.

---

## Abstract Method

### `compute(mechanism_outputs, h3_features, r3_features, cross_unit_inputs) -> Tensor`

The core computation. Transforms inputs into the model's output tensor.

| Parameter | Type | Shape | Description |
|-----------|------|-------|-------------|
| `mechanism_outputs` | `Dict[str, Tensor]` | `{name: (B, T, mechanism_dim)}` | Outputs from this model's internal mechanisms. Empty dict if `MECHANISM_NAMES` is empty |
| `h3_features` | `Dict[Tuple[int,int,int,int], Tensor]` | `{4-tuple: (B, T)}` | Per-demand H3 scalar time series, keyed by `(r3_idx, horizon, morph, law)` |
| `r3_features` | `Tensor` | `(B, T, 49)` | R3 spectral feature tensor |
| `cross_unit_inputs` | `Optional[Dict[str, Tensor]]` | `{pathway_id: Tensor}` | Named tensors from other models, keyed by `pathway_id`. `None` if no cross-unit dependencies |

**Returns**: `(B, T, OUTPUT_DIM)` output tensor with dimensions ordered as declared in `dimension_names` and structured according to `LAYERS`.

---

## Computed Helpers

| Method / Property | Return Type | Description |
|-------------------|-------------|-------------|
| `h3_demand_tuples()` | `Set[Tuple[int,int,int,int]]` | Set of raw 4-tuples consumed by `DemandTree.build()` and `H3Output`. Deduplicates via set semantics |
| `layer_dim_names` | `Tuple[str, ...]` | Flat tuple of dimension names derived from `LAYERS`; must match `dimension_names` (cross-check) |
| `cross_unit_dependency_units` | `FrozenSet[str]` | Set of cognitive unit names this model depends on |

---

## Validation Rules (`validate_constants()`)

Returns a list of error messages (empty if valid). Checks:

1. `NAME` must be non-empty
2. `FULL_NAME` must be non-empty
3. `UNIT` must be non-empty
4. `TIER` must be one of `"alpha"`, `"beta"`, `"gamma"`
5. `OUTPUT_DIM` must be > 0
6. `LAYERS` must cover `[0, OUTPUT_DIM)` without gaps or overlaps -- each index in range must be covered exactly once
7. `LAYERS` `dim_names` concatenated must match `dimension_names` (if implemented)

---

## Example Subclass

```python
class SRP(BaseModel):
    NAME = "SRP"
    FULL_NAME = "Striatal Reward Pathway"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 19
    MECHANISM_NAMES = ("AED", "CPD", "C0P")
    CROSS_UNIT_READS = ()
    LAYERS = (
        LayerSpec("E", "Neurochemical", 0, 3, ("da_caudate", "da_nacc", "opioid_proxy")),
        LayerSpec("M", "Circuit", 3, 6, ("vta_drive", "stg_nacc_coupling", "prediction_error")),
        ...
    )
```
