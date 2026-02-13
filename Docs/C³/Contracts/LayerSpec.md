# LayerSpec -- E/M/P/F Output Layer System

> **Code**: `mi_beta/contracts/layer_spec.py`
> **Kind**: Frozen Dataclass (hashable)
> **Imports from**: (none -- leaf type)

## Purpose

Every `BaseModel` organises its output dimensions into semantically meaningful layers. `LayerSpec` defines a single layer: a contiguous slice of the model's flat output tensor with a named code, descriptive label, and ordered dimension names.

The layer codes follow the convention used across C³ model documents:

| Code | Name | Semantics |
|------|------|-----------|
| **E** | Extraction / Neurochemical | Raw biophysical quantities (e.g. dopamine levels, opioid signals) |
| **M** | Mechanism / Circuit | Neural pathway activation states (e.g. VTA drive, coupling strength) |
| **P** | Psychological / Subjective | Subjective psychological states (e.g. Berridge wanting/liking) |
| **F** | Forecast / Predictive | Future-oriented estimates (e.g. prediction error, expected reward) |

Not every model uses all four layers. A simple model may have only E and P. Complex models (like SRP) may use all four plus additional domain-specific layers (T for Temporal, N for Neurochemical, etc.).

---

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Short code for the layer type: `"E"`, `"M"`, `"P"`, `"F"`, or custom |
| `name` | `str` | Full descriptive name (e.g. `"Neurochemical Signals"`) |
| `start` | `int` | Start index in the model's flat output tensor (inclusive) |
| `end` | `int` | End index in the model's flat output tensor (exclusive) |
| `dim_names` | `Tuple[str, ...]` | Ordered tuple of dimension names within this layer; `len(dim_names)` must equal `end - start` |

---

## Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `dim` | `int` | Number of dimensions in this layer (`end - start`) |

---

## Validation Rules (`__post_init__`)

The dataclass enforces at construction time:

1. `len(dim_names)` must equal `end - start`; raises `ValueError` if mismatched
2. `start` must be >= 0
3. `end` must be > `start` (no zero-width or negative-width layers)

---

## Usage in BaseModel

```python
LAYERS = (
    LayerSpec("E", "Neurochemical", 0, 3, ("da_caudate", "da_nacc", "opioid_proxy")),
    LayerSpec("M", "Circuit",       3, 6, ("vta_drive", "stg_nacc_coupling", "prediction_error")),
    LayerSpec("P", "Psychological",  6, 9, ("wanting", "liking", "arousal")),
    LayerSpec("F", "Forecast",       9, 12, ("expected_reward", "surprise", "uncertainty")),
)
```

The union of all layer ranges must cover `[0, OUTPUT_DIM)` without gaps or overlaps. This is validated by `BaseModel.validate_constants()`.

---

## Indexing Convention

The `(start, end)` range is a half-open interval into the model's flat output tensor:

```python
output[..., layer.start:layer.end]  # extracts this layer's dimensions
```
