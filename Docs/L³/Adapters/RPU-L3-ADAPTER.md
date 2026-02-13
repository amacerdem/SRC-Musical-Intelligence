# RPU L³ Adapter — Reward Processing

Maps RPU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/rpu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Reward Processing (10 models: α1-3 / β1-3 / γ1-4)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class RPUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "RPU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| dopamine_level | β | dopamine_level | direct |
| opioid_level | β | opioid_level | direct |
| wanting_signal | ζ | wanting | 2x-1 to bipolar |
| liking_signal | ζ | liking | 2x-1 to bipolar |
| reward_pe | ε | reward_pe | direct |
| anticipation | γ | reward_phase | direct |

## Primary Semantic Contributions

Wanting, liking, reward PE — the neurochemical reward system.

## Cross-References

- **Unit doc**: `Docs/C³/Units/RPU.md`
- **Models**: `Docs/C³/Models/RPU-*/`
- **Code**: `mi_beta/brain/units/rpu/`
- **Adapter code**: `mi_beta/language/adapters/rpu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
