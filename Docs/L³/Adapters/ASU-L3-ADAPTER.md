# ASU L³ Adapter — Auditory Salience

Maps ASU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/asu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Auditory Salience (9 models: α1-3 / β1-3 / γ1-3)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class ASUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "ASU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| novelty_response | ε | surprise | direct |
| attention_capture | ζ | engagement | 2x-1 to bipolar |
| salience_magnitude | θ | intensity | direct |
| pop_out_score | ε | reaction_magnitude | direct |
| attentional_blink | ε | precision_short (inv) | 1-x |

## Primary Semantic Contributions

Surprise, attention, engagement — what grabs the listener's ear.

## Cross-References

- **Unit doc**: `Docs/C³/Units/ASU.md`
- **Models**: `Docs/C³/Models/ASU-*/`
- **Code**: `mi_beta/brain/units/asu/`
- **Adapter code**: `mi_beta/language/adapters/asu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
