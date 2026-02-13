# MPU L³ Adapter — Motor Planning

Maps MPU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/mpu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Motor Planning (10 models: α1-3 / β1-3 / γ1-4)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class MPUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "MPU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| groove_strength | γ | groove | direct |
| entrainment_quality | ζ | engagement | 2x-1 to bipolar |
| motor_prediction | ε | prediction_reward | direct |
| movement_impulse | θ | motion_salience | softmax input |
| body_sway | ζ | groove | 2x-1 to bipolar |

## Primary Semantic Contributions

Groove, motor engagement — the body's response to rhythm.

## Cross-References

- **Unit doc**: `Docs/C³/Units/MPU.md`
- **Models**: `Docs/C³/Models/MPU-*/`
- **Code**: `mi_beta/brain/units/mpu/`
- **Adapter code**: `mi_beta/language/adapters/mpu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
