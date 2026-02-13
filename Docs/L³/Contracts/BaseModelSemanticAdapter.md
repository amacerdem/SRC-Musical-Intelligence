# BaseModelSemanticAdapter — Per-Unit Adapter ABC

Maps unit-specific output dimensions to semantic group input names.

**Code**: `mi_beta/language/adapters/_base_adapter.py`

## Class Constant

| Constant | Type | Description |
|----------|------|-------------|
| `UNIT_NAME` | `str` | Unit identifier (e.g., `"SPU"`, `"ARU"`) |

## Abstract Method

### `adapt(unit_output: UnitOutput) → Dict[str, Tensor]`

Maps a unit's raw model outputs to named tensors consumable by semantic groups.

- **unit_output**: `UnitOutput` containing the unit's concatenated model tensors
- **Returns**: Dictionary mapping semantic dimension names to tensors

## Current Implementations

All 9 adapters are currently **stubs** that pass the raw tensor through:

| Adapter Class | Unit | Code File | Status |
|---------------|------|-----------|--------|
| `SPUAdapter` | SPU | `spu_adapter.py` | Stub |
| `STUAdapter` | STU | `stu_adapter.py` | Stub |
| `IMUAdapter` | IMU | `imu_adapter.py` | Stub |
| `ASUAdapter` | ASU | `asu_adapter.py` | Stub |
| `NDUAdapter` | NDU | `ndu_adapter.py` | Stub |
| `MPUAdapter` | MPU | `mpu_adapter.py` | Stub |
| `PCUAdapter` | PCU | `pcu_adapter.py` | Stub |
| `ARUAdapter` | ARU | `aru_adapter.py` | Stub |
| `RPUAdapter` | RPU | `rpu_adapter.py` | Stub |

All stubs return: `{"tensor": unit_output.tensor}`

## Planned Behavior

When fully implemented, each adapter will:
1. Read specific dimensions from `UnitOutput` by name
2. Apply any necessary scaling or transformation
3. Return a dict mapping semantic labels to tensors (e.g., `{"pleasure": tensor[..., 3], "arousal": tensor[..., 7]}`)

See [../Adapters/00-INDEX.md](../Adapters/00-INDEX.md) for per-unit semantic mapping plans.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
