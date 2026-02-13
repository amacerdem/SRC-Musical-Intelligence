# SemanticGroupOutput — Output Dataclass

Immutable container for the output of a single L³ semantic group.

**Code**: `mi_beta/contracts/base_semantic_group.py`

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `group_name` | `str` | Canonical group name (e.g., `"alpha"`, `"theta"`) |
| `level` | `int` | Epistemological level (1–8) |
| `tensor` | `Tensor` | Semantic output, shape `(B, T, D)` |
| `dimension_names` | `Tuple[str, ...]` | Ordered dimension labels |

## Shape Convention

All tensors follow the `(B, T, D)` convention:
- **B** — batch size
- **T** — time frames
- **D** — group output dimensionality (`OUTPUT_DIM`)

## Range Convention

| Groups | Range | Notes |
|--------|-------|-------|
| α, β, γ, δ, ε, η, θ | `[0, 1]` | Standard sigmoid range |
| ζ | `[-1, +1]` | Bipolar polarity axes, clamped in `compute()` |

## Post-Init Validation

```python
def __post_init__(self) -> None:
    dim = self.tensor.shape[-1]
    if len(self.dimension_names) != dim:
        raise ValueError(...)
```

This ensures `len(dimension_names)` always matches `tensor.shape[-1]`. Any mismatch raises `ValueError` immediately at construction time.

## Usage

```python
output = SemanticGroupOutput(
    group_name="gamma",
    level=3,
    tensor=tensor,                    # (B, T, 13)
    dimension_names=("reward_intensity", "reward_type", ...),
)

# Access
output.tensor[..., 0]           # reward_intensity slice
output.dimension_names[0]       # "reward_intensity"
```

---

**Parent**: [00-INDEX.md](00-INDEX.md)
