# BaseSemanticGroup — Abstract Base Class

The foundational contract for all 8 L³ semantic groups.

**Code**: `mi_beta/contracts/base_semantic_group.py`

## Class Constants

Every subclass MUST override these four constants:

| Constant | Type | Range | Description |
|----------|------|-------|-------------|
| `LEVEL` | `int` | 1–8 | Epistemological level |
| `GROUP_NAME` | `str` | — | Canonical name: `"alpha"` .. `"theta"` |
| `DISPLAY_NAME` | `str` | — | Greek letter display name |
| `OUTPUT_DIM` | `int` | > 0 | Number of output dimensions |

## Abstract Methods

### `compute(brain_output, **kwargs) → SemanticGroupOutput`

Compute semantic interpretation from the Brain output.

- **brain_output**: `BrainOutput` (26D in mi v2, variable in mi_beta)
- **kwargs**: Optional outputs from earlier groups (e.g., `epsilon_output`, `zeta_output`)
- **Returns**: `SemanticGroupOutput` with tensor shape `(B, T, OUTPUT_DIM)`

### `dimension_names` (property) → `List[str]`

Ordered names for each output dimension. `len(dimension_names)` MUST equal `OUTPUT_DIM`.

## Validation

The `validate()` method checks:
1. `LEVEL` in `[1, 8]`
2. `GROUP_NAME` is non-empty
3. `DISPLAY_NAME` is non-empty
4. `OUTPUT_DIM > 0`
5. `len(dimension_names) == OUTPUT_DIM`

Returns a list of error messages (empty if valid).

## Implementation Table

| Level | Group | Class | OUTPUT_DIM | Phase | Stateful |
|-------|-------|-------|------------|-------|----------|
| 1 | alpha | `AlphaGroup` | Variable | 1 | No |
| 2 | beta | `BetaGroup` | Variable | 1 | No |
| 3 | gamma | `GammaGroup` | 13 | 1 | No |
| 4 | delta | `DeltaGroup` | 12 | 1 | No |
| 5 | epsilon | `EpsilonGroup` | 19 | 1b | **Yes** |
| 6 | zeta | `ZetaGroup` | 12 | 2a | No |
| 7 | eta | `EtaGroup` | 12 | 2b | No |
| 8 | theta | `ThetaGroup` | 16 | 2c | No |

## Usage Pattern

```python
class NewGroup(BaseSemanticGroup):
    LEVEL = 9
    GROUP_NAME = "iota"
    DISPLAY_NAME = "iota"
    OUTPUT_DIM = 8

    @property
    def dimension_names(self) -> List[str]:
        return ["dim_0", "dim_1", ..., "dim_7"]

    def compute(self, brain_output, **kwargs) -> SemanticGroupOutput:
        tensor = ...  # (B, T, 8)
        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor,
            dimension_names=tuple(self.dimension_names),
        )
```

---

**Parent**: [00-INDEX.md](00-INDEX.md)
