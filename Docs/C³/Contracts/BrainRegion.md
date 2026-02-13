# BrainRegion -- Brain Region with MNI Coordinates

> **Code**: `mi_beta/contracts/brain_region.py`
> **Kind**: Frozen Dataclass (hashable)
> **Imports from**: (none -- leaf type)

## Purpose

Every cognitive model and mechanism is grounded in specific brain regions. `BrainRegion` captures the neuroanatomical identity of each region so that models can declare their biological substrate and visualisation tools can render activations in MNI152 standard space.

---

## Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | (required) | Full anatomical name (e.g. `"Nucleus Accumbens"`) |
| `abbreviation` | `str` | (required) | Short label (e.g. `"NAcc"`) |
| `hemisphere` | `str` | (required) | `"L"`, `"R"`, or `"bilateral"` |
| `mni_coords` | `Tuple[int, int, int]` | (required) | `(x, y, z)` centroid in MNI152 space (mm) |
| `brodmann_area` | `Optional[int]` | `None` | Brodmann area number if applicable (cortical only) |
| `function` | `str` | `""` | Brief functional description |
| `evidence_count` | `int` | `0` | Number of studies in the C³ database citing this region |

---

## MNI152 Coordinate Convention

Coordinates follow the Montreal Neurological Institute standard:

| Axis | Negative | Positive |
|------|----------|----------|
| **x** | Left | Right |
| **y** | Posterior | Anterior |
| **z** | Inferior | Superior |

---

## Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `is_cortical` | `bool` | `True` if the region has a Brodmann area designation |
| `is_subcortical` | `bool` | `True` if the region lacks a Brodmann area (subcortical structure) |

---

## Validation Rules (`__post_init__`)

Enforced at construction time:

1. `hemisphere` must be one of `"L"`, `"R"`, `"bilateral"`; raises `ValueError` otherwise
2. `mni_coords` must be a 3-tuple `(x, y, z)`; raises `ValueError` if length is not 3

---

## Note on Brodmann Areas

Brodmann areas are optional because subcortical structures (NAcc, VTA, amygdala, hippocampus, thalamus) and brainstem structures (IC, CN, SOC, PAG) do not have Brodmann designations. The `is_cortical` / `is_subcortical` properties use the presence/absence of `brodmann_area` to classify regions.

---

## Usage Example

```python
# Cortical region with Brodmann area
A1_HG = BrainRegion(
    name="Primary Auditory Cortex (Heschl's Gyrus)",
    abbreviation="A1/HG",
    hemisphere="bilateral",
    mni_coords=(48, -18, 8),
    brodmann_area=41,
    function="Tonotopic frequency analysis...",
    evidence_count=42,
)

# Subcortical region without Brodmann area
VTA = BrainRegion(
    name="Ventral Tegmental Area",
    abbreviation="VTA",
    hemisphere="bilateral",
    mni_coords=(0, -16, -8),
    function="Dopaminergic source nucleus...",
    evidence_count=18,
)
```
