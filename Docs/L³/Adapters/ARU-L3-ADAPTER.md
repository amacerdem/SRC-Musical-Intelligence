# ARU L³ Adapter — Affect Regulation

Maps ARU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/aru_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Affect Regulation (10 models: α1-3 / β1-3 / γ1-4)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class ARUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "ARU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| pleasure | γ | reward_intensity | direct |
| tension | γ | itpra_tension_resolution | direct |
| chill_probability | γ | chill_probability | direct |
| chill_intensity | γ | chill_intensity | direct |
| beauty | γ | beauty | direct |
| valence | ζ | valence | 2x-1 to bipolar |

## Primary Semantic Contributions

Pleasure, beauty, chills, valence — the affective core of musical experience.

## Cross-References

- **Unit doc**: `Docs/C³/Units/ARU.md`
- **Models**: `Docs/C³/Models/ARU-*/`
- **Code**: `mi_beta/brain/units/aru/`
- **Adapter code**: `mi_beta/language/adapters/aru_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
