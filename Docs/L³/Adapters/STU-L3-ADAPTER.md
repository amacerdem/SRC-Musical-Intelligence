# STU L³ Adapter — Structure & Timing

Maps STU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/stu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Structure & Timing (14 models: α1-3 / β1-5 / γ1-6)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class STUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "STU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| beat_strength | γ | groove | direct |
| tempo_estimate | ζ | arousal | tempo_norm to bipolar |
| meter_clarity | ζ | stability | 2x-1 to bipolar |
| sync_quality | ζ | engagement | 2x-1 to bipolar |
| phrase_position | θ | predicate | phase classification |
| rhythmic_complexity | ζ | complexity | 2x-1 to bipolar |

## Primary Semantic Contributions

Groove, temporal engagement — the rhythmic backbone of musical experience.

## Cross-References

- **Unit doc**: `Docs/C³/Units/STU.md`
- **Models**: `Docs/C³/Models/STU-*/`
- **Code**: `mi_beta/brain/units/stu/`
- **Adapter code**: `mi_beta/language/adapters/stu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
