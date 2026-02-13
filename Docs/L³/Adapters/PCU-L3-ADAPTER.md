# PCU L³ Adapter — Prediction & Control

Maps PCU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/pcu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Prediction & Control (10 models: α1-3 / β1-3 / γ1-4)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class PCUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "PCU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| prediction_error | ε | pe_short/medium/long | timescale routing |
| certainty | ε | precision_short/long | direct |
| prediction_accuracy | ε | prediction_reward | direct |
| control_signal | ζ | power | 2x-1 to bipolar |
| model_confidence | ζ | stability | 2x-1 to bipolar |

## Primary Semantic Contributions

Prediction error, precision, stability — the brain's predictive machinery.

## Cross-References

- **Unit doc**: `Docs/C³/Units/PCU.md`
- **Models**: `Docs/C³/Models/PCU-*/`
- **Code**: `mi_beta/brain/units/pcu/`
- **Adapter code**: `mi_beta/language/adapters/pcu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
