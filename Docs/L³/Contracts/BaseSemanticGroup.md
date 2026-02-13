# BaseSemanticGroup — ABC Contract

**Scope**: Abstract base class that all 8 L³ semantic groups must implement. Defines the interface for group constants, the `compute()` method, the `dimension_names` property, and runtime validation.

**Code file**: `mi_beta/contracts/base_semantic_group.py`

---

## 1. Class Constants

Every `BaseSemanticGroup` subclass must declare four class-level constants:

| Constant | Type | Constraint | Description |
|----------|:----:|------------|-------------|
| `LEVEL` | `int` | 1--8 | Epistemological level in the 8-group hierarchy |
| `GROUP_NAME` | `str` | non-empty | Lowercase group identifier (`"alpha"`, `"beta"`, ..., `"theta"`) |
| `DISPLAY_NAME` | `str` | non-empty | Display-friendly name (may include Greek letter or full name) |
| `OUTPUT_DIM` | `int` | > 0 | Number of output dimensions for this group |

### Default Values (in ABC)

```python
LEVEL: int = 0
GROUP_NAME: str = ""
DISPLAY_NAME: str = ""
OUTPUT_DIM: int = 0
```

All defaults are invalid and will fail `validate()`. Subclasses must override every constant.

---

## 2. Abstract Methods

### 2.1 `compute(brain_output, **kwargs) -> SemanticGroupOutput`

The primary computation method. Takes the Brain output and optional keyword arguments (used by dependent groups to receive upstream tensors), and returns a `SemanticGroupOutput`.

```python
@abstractmethod
def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
    ...
```

**Parameters**:
- `brain_output` -- `BrainOutput` tensor from C³. All groups receive this.
- `**kwargs` -- Dependency injection for Phase 2 groups:
  - `epsilon_output` -- Tensor from epsilon (used by zeta, theta)
  - `zeta_output` -- Tensor from zeta (used by eta, theta)

**Returns**: `SemanticGroupOutput` with the group's computed tensor.

**Contract**:
- Output tensor shape must be `(B, T, OUTPUT_DIM)`
- `dimension_names` in the output must match `self.dimension_names`
- Phase 1 groups must ignore `**kwargs`
- Phase 2 groups must declare required kwargs in their signature

### 2.2 `dimension_names` property

Returns the ordered list of dimension names for this group.

```python
@property
@abstractmethod
def dimension_names(self) -> List[str]:
    ...
```

**Contract**:
- Must return exactly `OUTPUT_DIM` names
- Names must be `snake_case` strings
- Names should be semantically descriptive (e.g., `"reward_intensity"`, not `"dim_0"`)
- Order must be stable across calls

---

## 3. Concrete Methods

### 3.1 `validate() -> list[str]`

Runtime validation that checks all class constants and the dimension_names property. Returns a list of error messages (empty list = valid).

**Checks performed**:

| # | Check | Error if |
|:-:|-------|----------|
| 1 | `LEVEL in [1, 8]` | LEVEL is 0 or outside 1--8 |
| 2 | `GROUP_NAME != ""` | GROUP_NAME is empty string |
| 3 | `DISPLAY_NAME != ""` | DISPLAY_NAME is empty string |
| 4 | `OUTPUT_DIM > 0` | OUTPUT_DIM is 0 or negative |
| 5 | `len(dimension_names) == OUTPUT_DIM` | Dimension names count mismatch |

### 3.2 `__repr__() -> str`

Returns a human-readable string representation including group name, level, and output dimensionality.

---

## 4. Implementations

All 8 L³ groups implement this ABC:

| Group Class | LEVEL | GROUP_NAME | DISPLAY_NAME | OUTPUT_DIM | Phase | Code File |
|-------------|:-----:|------------|--------------|:----------:|:-----:|-----------|
| `AlphaGroup` | 1 | `"alpha"` | `"alpha"` | 6* | 1 | `mi_beta/language/groups/alpha.py` |
| `BetaGroup` | 2 | `"beta"` | `"beta"` | 14* | 1 | `mi_beta/language/groups/beta.py` |
| `GammaGroup` | 3 | `"gamma"` | `"gamma"` | 13 | 1 | `mi_beta/language/groups/gamma.py` |
| `DeltaGroup` | 4 | `"delta"` | `"delta"` | 12 | 1 | `mi_beta/language/groups/delta.py` |
| `EpsilonGroup` | 5 | `"epsilon"` | `"epsilon"` | 19 | 1b | `mi_beta/language/groups/epsilon.py` |
| `ZetaGroup` | 6 | `"zeta"` | `"zeta"` | 12 | 2a | `mi_beta/language/groups/zeta.py` |
| `EtaGroup` | 7 | `"eta"` | `"eta"` | 12 | 2b | `mi_beta/language/groups/eta.py` |
| `ThetaGroup` | 8 | `"theta"` | `"theta"` | 16 | 2c | `mi_beta/language/groups/theta.py` |

*Alpha and Beta have variable dimensionality in mi_beta -- they auto-configure `OUTPUT_DIM` and `dimension_names` on first `compute()` call based on active units/regions.

---

## 5. Usage Pattern

To create a new group subclass:

```python
from mi_beta.contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput

class NewGroup(BaseSemanticGroup):
    LEVEL = 9                      # epistemological level
    GROUP_NAME = "iota"            # lowercase identifier
    DISPLAY_NAME = "iota"          # display name
    OUTPUT_DIM = 8                 # number of dimensions

    @property
    def dimension_names(self):
        return [
            "dim_a", "dim_b", "dim_c", "dim_d",
            "dim_e", "dim_f", "dim_g", "dim_h",
        ]

    def compute(self, brain_output, **kwargs):
        # Compute (B, T, 8) tensor from brain_output
        tensor = ...
        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor,
            dimension_names=tuple(self.dimension_names),
        )
```

**Validation check** (optional but recommended):

```python
group = NewGroup()
errors = group.validate()
assert errors == [], f"Validation failed: {errors}"
```

---

## 6. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| [SemanticGroupOutput](SemanticGroupOutput.md) | Return type of `compute()` |
| [L3Orchestrator](L3Orchestrator.md) | Calls `compute()` on all groups in phase order |
| [EpsilonStateContract](EpsilonStateContract.md) | Additional state protocol for EpsilonGroup |
| [BaseModelSemanticAdapter](BaseModelSemanticAdapter.md) | Maps unit outputs to group inputs (upstream) |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
