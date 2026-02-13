# L³ Adapters — Index

Per-unit semantic adapters map C³ model outputs to L³ semantic group inputs.

## Adapter Registry

| Unit | Full Name | Adapter | Code File | Status | Semantic Focus |
|------|-----------|---------|-----------|--------|----------------|
| [SPU](SPU-L3-ADAPTER.md) | Spectral Processing | `SPUAdapter` | `spu_adapter.py` | Stub | consonance → beauty, timbre → complexity |
| [STU](STU-L3-ADAPTER.md) | Structure & Timing | `STUAdapter` | `stu_adapter.py` | Stub | beat → groove, tempo → arousal |
| [IMU](IMU-L3-ADAPTER.md) | Imagery & Memory | `IMUAdapter` | `imu_adapter.py` | Stub | familiarity → stability |
| [ASU](ASU-L3-ADAPTER.md) | Auditory Salience | `ASUAdapter` | `asu_adapter.py` | Stub | novelty → surprise |
| [NDU](NDU-L3-ADAPTER.md) | Novelty & Deviation | `NDUAdapter` | `ndu_adapter.py` | Stub | deviation → surprise, PE → tension |
| [MPU](MPU-L3-ADAPTER.md) | Motor Planning | `MPUAdapter` | `mpu_adapter.py` | Stub | groove → groove, movement → motion |
| [PCU](PCU-L3-ADAPTER.md) | Prediction & Control | `PCUAdapter` | `pcu_adapter.py` | Stub | PE → surprise, certainty → stability |
| [ARU](ARU-L3-ADAPTER.md) | Affect Regulation | `ARUAdapter` | `aru_adapter.py` | Stub | pleasure → valence, tension → tension |
| [RPU](RPU-L3-ADAPTER.md) | Reward Processing | `RPUAdapter` | `rpu_adapter.py` | Stub | DA → wanting, opioid → liking |

## Architecture

All adapters inherit from `BaseModelSemanticAdapter` (`mi_beta/language/adapters/_base_adapter.py`):

```python
class BaseModelSemanticAdapter(ABC):
    UNIT_NAME: str

    @abstractmethod
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        """Map unit output dimensions to semantic group inputs."""
```

## Current Status

> **All 9 adapters are stubs.** They pass raw tensors through without semantic mapping.
> Full implementation is planned for Phase 6 (mi_beta code update).

Current stub behavior:
```python
def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
    return {"tensor": unit_output.tensor}
```

## Design Principles

1. **One adapter per unit**: Each C³ unit has exactly one L³ adapter
2. **Semantic labeling**: Adapters translate raw tensor indices to named semantic dimensions
3. **Composability**: Multiple adapters' outputs merge via `BrainOutput` before reaching semantic groups
4. **Testability**: Each adapter can be unit-tested independently

---

**Parent**: [../00-INDEX.md](../00-INDEX.md)
**See also**: [../Contracts/BaseModelSemanticAdapter.md](../Contracts/BaseModelSemanticAdapter.md)
