# BaseModelSemanticAdapter — Per-Unit Adapter ABC

**Scope**: Abstract base class for per-unit semantic adapters. Each adapter maps a C³ unit's output dimensions to named inputs that L³ semantic groups can consume. This decouples the unit-specific output layout from the group computation logic.

**Code file**: `mi_beta/language/adapters/_base_adapter.py`

---

## 1. Class Definition

```python
class BaseModelSemanticAdapter(ABC):
    UNIT_NAME: str

    @abstractmethod
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        """Map unit output dimensions to semantic group inputs."""
```

---

## 2. Class Constant

| Constant | Type | Description | Example |
|----------|:----:|-------------|---------|
| `UNIT_NAME` | `str` | Uppercase unit identifier matching the C³ unit name | `"SPU"`, `"IMU"`, `"ARU"` |

---

## 3. Abstract Method

### `adapt(unit_output: UnitOutput) -> Dict[str, Tensor]`

Maps a unit's output tensor to a dictionary of named semantic inputs.

**Parameters**:
- `unit_output` -- The `UnitOutput` from a C³ unit, containing the unit's tensor and metadata

**Returns**: `Dict[str, Tensor]` where:
- Keys are semantic dimension names (e.g., `"pleasure"`, `"arousal"`, `"tension"`)
- Values are tensors extracted or derived from the unit output

**Contract**:
- Must return a dictionary (may be empty if no mappings are defined)
- Keys should use `snake_case` names matching the semantic vocabulary used by L³ groups
- Values should be tensors with shape compatible for group consumption
- The adapter must not modify the input `unit_output`

---

## 4. Purpose and Design Rationale

L³ semantic groups compute formulas using named Brain dimensions (e.g., `pleasure`, `arousal`, `tension`). However, C³ units produce output tensors with unit-specific layouts (e.g., SPU's 10 models each with E/M/P/F layers). Adapters bridge this gap:

```
C³ Unit Output                    Adapter                     L³ Group Input
(unit-specific layout)    -->     adapt()     -->     (named semantic dimensions)

SPU output (B,T,40)       -->   SPU Adapter   -->     {"pleasure": ..., "arousal": ...}
IMU output (B,T,60)       -->   IMU Adapter   -->     {"tension": ..., "prediction_error": ...}
```

This separation means:
- Groups never need to know unit-specific dimension layouts
- Adding a new unit requires only a new adapter, no group changes
- Adapter logic can evolve independently from group formulas

---

## 5. Implementations

Currently 9 stub adapters exist, one per C³ unit:

| Adapter Class | UNIT_NAME | Code File | Status |
|--------------|-----------|-----------|:------:|
| `SPUAdapter` | `"SPU"` | `mi_beta/language/adapters/spu_adapter.py` | Stub |
| `STUAdapter` | `"STU"` | `mi_beta/language/adapters/stu_adapter.py` | Stub |
| `IMUAdapter` | `"IMU"` | `mi_beta/language/adapters/imu_adapter.py` | Stub |
| `ASUAdapter` | `"ASU"` | `mi_beta/language/adapters/asu_adapter.py` | Stub |
| `NDUAdapter` | `"NDU"` | `mi_beta/language/adapters/ndu_adapter.py` | Stub |
| `MPUAdapter` | `"MPU"` | `mi_beta/language/adapters/mpu_adapter.py` | Stub |
| `PCUAdapter` | `"PCU"` | `mi_beta/language/adapters/pcu_adapter.py` | Stub |
| `ARUAdapter` | `"ARU"` | `mi_beta/language/adapters/aru_adapter.py` | Stub |
| `RPUAdapter` | `"RPU"` | `mi_beta/language/adapters/rpu_adapter.py` | Stub |

All 9 adapters are currently stubs that return minimal or pass-through mappings. Full adapter implementations are planned for a future phase.

---

## 6. Adapter Registry

The adapter registry (`mi_beta/language/adapters/__init__.py`) collects all adapters and provides lookup by unit name:

```python
# Conceptual usage
adapter = adapter_registry.get("SPU")
semantic_inputs = adapter.adapt(spu_unit_output)
```

---

## 7. Usage Pattern

### Creating a new adapter

```python
from mi_beta.language.adapters._base_adapter import BaseModelSemanticAdapter

class NewUnitAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "XYZ"

    def adapt(self, unit_output):
        return {
            "pleasure": unit_output.tensor[..., 0:1],
            "arousal": unit_output.tensor[..., 1:2],
        }
```

### Documentation requirement

Each adapter should have a corresponding documentation file at `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` describing:
- Which unit output dimensions map to which semantic names
- The scientific rationale for each mapping
- Current implementation status (stub / partial / full)

---

## 8. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| [BaseSemanticGroup](BaseSemanticGroup.md) | Groups consume the named tensors that adapters produce |
| [L3Orchestrator](L3Orchestrator.md) | Orchestrator may use adapters to prepare group inputs |
| [SemanticGroupOutput](SemanticGroupOutput.md) | Adapters operate upstream of group output |

---

## 9. Cross-References

| Related Document | Path |
|-----------------|------|
| Per-unit adapter docs | [../Adapters/00-INDEX.md](../Adapters/00-INDEX.md) |
| C³ unit architecture | [../../C³/C3-ARCHITECTURE.md](../../C³/C3-ARCHITECTURE.md) |
| C³ output space | [../../C³/Matrices/Output-Space.md](../../C³/Matrices/Output-Space.md) |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
