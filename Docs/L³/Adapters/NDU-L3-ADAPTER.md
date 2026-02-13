# NDU L³ Adapter — Novelty & Deviation

Maps NDU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/ndu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Novelty & Deviation (9 models: α1-3 / β1-3 / γ1-3)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class NDUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "NDU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| deviation_magnitude | ε | surprise | direct |
| prediction_error | ζ | tension | 2x-1 to bipolar |
| entropy_estimate | ζ | complexity | 2x-1 to bipolar |
| expectation_violation | θ | contrasting | direct |
| novelty_score | ζ | novelty | 2x-1 to bipolar |

## Primary Semantic Contributions

Surprise, tension, complexity — deviation from the expected.

## Cross-References

- **Unit doc**: `Docs/C³/Units/NDU.md`
- **Models**: `Docs/C³/Models/NDU-*/`
- **Code**: `mi_beta/brain/units/ndu/`
- **Adapter code**: `mi_beta/language/adapters/ndu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
