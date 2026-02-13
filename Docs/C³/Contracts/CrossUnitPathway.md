# CrossUnitPathway -- Pathway Declaration

> **Code**: `mi_beta/contracts/pathway_spec.py`
> **Kind**: Frozen Dataclass (hashable)
> **Imports from**: (none -- leaf type)

## Purpose

In the MI-Beta architecture, cognitive units (ARU, SPU, STU, IMU, etc.) are NOT fully independent. Some models within one unit read outputs from models in another unit. These cross-unit dependencies must be declared explicitly so that:

1. The pipeline can topologically sort unit execution order.
2. The demand aggregator knows which units must run first.
3. Auditors can trace every data flow to a scientific citation.

`CrossUnitPathway` is the declaration record. It does NOT carry data -- it describes the contract that a source model promises to fulfill and a target model depends on.

---

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `pathway_id` | `str` | Unique identifier (e.g. `"ARU_SRP__SPU_STAI__arousal"`) |
| `name` | `str` | Human-readable pathway name (e.g. `"Arousal -> Spectral Gating"`) |
| `source_unit` | `str` | Source cognitive unit name (e.g. `"ARU"`) |
| `source_model` | `str` | Source model name within that unit (e.g. `"SRP"`) |
| `source_dims` | `Tuple[str, ...]` | Dimension names or indices provided by the source (e.g. `("arousal", "prediction_error")`) |
| `target_unit` | `str` | Target cognitive unit name (e.g. `"SPU"`) |
| `target_model` | `str` | Target model name within that unit (e.g. `"STAI"`) |
| `correlation` | `str` | Expected correlation strength from literature (e.g. `"r=0.71"`, `"d=0.53"`). Empty string if theoretical |
| `citation` | `str` | Scientific citation justifying this pathway |

---

## Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `is_intra_unit` | `bool` | `True` if source and target are in the same cognitive unit |
| `is_inter_unit` | `bool` | `True` if source and target are in different cognitive units |
| `edge` | `Tuple[str, str]` | `(source_unit, target_unit)` for dependency graph construction |

---

## Usage in BaseModel

Models declare their cross-unit dependencies as a tuple of `CrossUnitPathway` instances:

```python
class SomeModel(BaseModel):
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="ARU_SRP__SPU_STAI__arousal",
            name="Arousal -> Spectral Gating",
            source_unit="ARU",
            source_model="SRP",
            source_dims=("arousal",),
            target_unit="SPU",
            target_model="STAI",
            correlation="r=0.71",
            citation="Salimpoor 2011",
        ),
    )
```

The pipeline uses `BaseModel.cross_unit_dependency_units` (which extracts the `source_unit` from each pathway) to determine execution order.

---

## Topological Sorting

Cross-unit pathways define directed edges in the unit dependency graph. The pipeline must execute units in topological order so that source outputs are available before target models need them. Cycles are not allowed and would indicate a design error.

```
ARU.SRP[arousal] -> SPU.STAI    # ARU must run before SPU
IMU.MEAMN[familiarity] -> ARU.AAC  # IMU must run before ARU
```
