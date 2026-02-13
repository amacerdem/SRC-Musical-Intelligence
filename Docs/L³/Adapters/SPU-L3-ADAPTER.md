# SPU L³ Adapter — Spectral Processing

Maps SPU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/spu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Spectral Processing (9 models: α1-3 / β1-3 / γ1-3)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class SPUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "SPU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| consonance_global | γ | beauty | direct |
| spectral_complexity | ζ | complexity | 2x-1 to bipolar |
| pitch_salience | ε | surprise (via Brain) | feed to Markov |
| timbre_brightness | ζ | novelty | 2x-1 to bipolar |
| harmonic_tension | ζ | tension | 2x-1 to bipolar |
| roughness | γ | groove (inverse) | 1-x |

## Primary Semantic Contributions

Beauty, complexity, tension — the spectral foundation of aesthetic judgment.

## Cross-References

- **Unit doc**: `Docs/C³/Units/SPU.md`
- **Models**: `Docs/C³/Models/SPU-*/`
- **Code**: `mi_beta/brain/units/spu/`
- **Adapter code**: `mi_beta/language/adapters/spu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
