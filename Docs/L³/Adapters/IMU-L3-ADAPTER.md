# IMU L³ Adapter — Imagery & Memory

Maps IMU model outputs to L³ semantic dimensions.

**Code**: `mi_beta/language/adapters/imu_adapter.py`
**Base class**: `BaseModelSemanticAdapter`
**Unit**: Imagery & Memory (15 models: α1-3 / β1-6 / γ1-6)

## Current Status

> **Stub** — passes raw tensor through without semantic mapping.

```python
class IMUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "IMU"
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
```

## Planned Semantic Mapping

| Unit Output Dimension | Target L³ Group | Target Dimension | Transform |
|----------------------|-----------------|------------------|-----------|
| familiarity_score | ε | familiarity | direct |
| memory_strength | ζ | stability | 2x-1 to bipolar |
| imagery_vividness | θ | beauty_salience | softmax input |
| recall_confidence | ζ | engagement | 2x-1 to bipolar |
| schema_match | ε | prediction_reward | direct |

## Primary Semantic Contributions

Familiarity, stability, imagination — the memory-based foundation of musical expectation.

## Cross-References

- **Unit doc**: `Docs/C³/Units/IMU.md`
- **Models**: `Docs/C³/Models/IMU-*/`
- **Code**: `mi_beta/brain/units/imu/`
- **Adapter code**: `mi_beta/language/adapters/imu_adapter.py`

---

**Parent**: [00-INDEX.md](00-INDEX.md)
