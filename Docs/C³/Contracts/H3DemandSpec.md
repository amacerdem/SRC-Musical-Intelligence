# H3DemandSpec -- Temporal Demand Specification

> **Code**: `mi_beta/contracts/demand_spec.py`
> **Kind**: Frozen Dataclass (hashable)
> **Imports from**: (none -- leaf type)

## Purpose

Each cognitive model declares EXACTLY which H3 features it needs via a set of `H3DemandSpec` instances. Every spec maps to one scalar time series: a specific R3 feature, observed through a specific temporal horizon, summarised by a specific morphological statistic, and viewed under a specific causal law.

The 4-tuple `(r3_idx, horizon, morph, law)` is the canonical address in H3 space. The remaining fields (names, purpose, citation) are metadata for auditability -- every demand must justify its existence with a scientific citation.

---

## Fields

### H3 Address (the 4-tuple)

| Field | Type | Description |
|-------|------|-------------|
| `r3_idx` | `int` | Index into the R3 feature vector: v1 (0-48, 49D); v2 (0-127, 128D) |
| `r3_name` | `str` | Human-readable name of the R3 feature (e.g. `"stumpf_fusion"`) |
| `horizon` | `int` | Horizon index (0-31); maps to `HORIZON_MS[horizon]` |
| `horizon_label` | `str` | Human-readable horizon label (e.g. `"2s phrase"`) |
| `morph` | `int` | Morph index (0-23); maps to `MORPH_NAMES[morph]` |
| `morph_name` | `str` | Human-readable morph name (e.g. `"value"`, `"velocity"`) |
| `law` | `int` | Temporal law index (0-2): 0=memory, 1=prediction, 2=integration |
| `law_name` | `str` | Human-readable law name (e.g. `"memory"`, `"prediction"`) |

### Justification

| Field | Type | Description |
|-------|------|-------------|
| `purpose` | `str` | One-line description of WHY this demand exists in the model |
| `citation` | `str` | Short-form citation justifying the demand (e.g. `"Salimpoor 2011"`) |

---

## Methods

### `as_tuple() -> Tuple[int, int, int, int]`

Returns the canonical `(r3_idx, horizon, morph, law)` 4-tuple. This is the key used by `H3Output.features` and `DemandTree`.

---

## Temporal Law Semantics

| Index | Law | Meaning |
|-------|-----|---------|
| 0 | Memory | How the feature has behaved in the recent past (exponential decay) |
| 1 | Prediction | Expected future trajectory based on learned patterns |
| 2 | Integration | Combined memory + prediction (convolution) |

---

## R³ v2 Expansion Note

With R³ v2 (128D), the valid `r3_idx` range extends from `[0:48]` to `[0:127]`. The 79 new features in groups F--K ([49:127]) create new H³ demand targets. The 4-tuple address space grows from 112,896 to 294,912. See [Docs/H³/Expansion/R3v2-H3-Impact.md](../../H³/Expansion/R3v2-H3-Impact.md) and [Docs/H³/Migration/DemandSpec-Update.md](../../H³/Migration/DemandSpec-Update.md) for migration details.

---

## Cross-References

- `mi.core.constants` -- `MORPH_NAMES`, `LAW_NAMES`, `HORIZON_MS`
- `mi.ear.h3` -- `DemandTree`, `HorizonEngine`, `MorphEngine`
- [Docs/H³/00-INDEX.md](../../H³/00-INDEX.md) -- H³ modular architecture (definitive reference)
- [Docs/H³/Contracts/](../../H³/Contracts/) -- H3Extractor, DemandTree, MorphComputer specifications
- [Docs/H³/Registry/DemandAddressSpace.md](../../H³/Registry/DemandAddressSpace.md) -- 4-tuple address system

---

## Usage Example

```python
H3DemandSpec(
    r3_idx=10,
    r3_name="spectral_flux",
    horizon=9,
    horizon_label="350ms event",
    morph=4,
    morph_name="velocity",
    law=2,
    law_name="integration",
    purpose="Tracks rapid spectral changes for timbral surprise detection",
    citation="Salimpoor 2011",
)
```

The model collects all its `H3DemandSpec` instances in its `h3_demand` property. The pipeline calls `h3_demand_tuples()` on the model to get the deduplicated set of 4-tuples for the DemandTree.
