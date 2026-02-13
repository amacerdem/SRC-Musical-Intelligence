# SemanticGroupOutput — Output Dataclass Contract

**Scope**: The standard output dataclass returned by every `BaseSemanticGroup.compute()` call. Defines the fields, tensor shape convention, value ranges, and post-init validation.

**Code file**: `mi_beta/contracts/base_semantic_group.py` (same file as the ABC)

---

## 1. Dataclass Definition

```python
@dataclass
class SemanticGroupOutput:
    group_name: str
    level: int
    tensor: Tensor
    dimension_names: Tuple[str, ...]
```

---

## 2. Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `group_name` | `str` | Lowercase group identifier | `"gamma"` |
| `level` | `int` | Epistemological level (1--8) | `3` |
| `tensor` | `Tensor` | Computed output tensor, shape `(B, T, D)` | `torch.zeros(2, 100, 13)` |
| `dimension_names` | `Tuple[str, ...]` | Ordered names for each dimension in the tensor | `("reward_intensity", "reward_type", ...)` |

---

## 3. Tensor Shape Convention

All output tensors follow the shape `(B, T, D)`:

| Axis | Symbol | Meaning |
|:----:|:------:|---------|
| 0 | B | Batch size (number of audio files processed in parallel) |
| 1 | T | Time frames (at 172.27 Hz, i.e., 5.8 ms per frame) |
| 2 | D | Group output dimensionality (must equal `OUTPUT_DIM` of the group) |

This convention is inherited from the pipeline: R³ produces `(B, T, 128)`, C³ produces `(B, T, 1006)`, and L³ groups each produce `(B, T, D)` where D varies by group.

---

## 4. Post-Init Validation

The `__post_init__` method performs a runtime check immediately after construction:

```python
def __post_init__(self) -> None:
    dim = self.tensor.shape[-1]
    if len(self.dimension_names) != dim:
        raise ValueError(
            f"SemanticGroupOutput '{self.group_name}': "
            f"dimension_names has {len(self.dimension_names)} entries "
            f"but tensor has {dim} dimensions"
        )
```

**Rule**: `len(dimension_names)` must exactly equal `tensor.shape[-1]`. A mismatch raises `ValueError` at construction time, preventing silent dimension misalignment.

---

## 5. Value Ranges

| Group | Output Range | Notes |
|-------|:----------:|-------|
| alpha | [0, 1] | Computation attribution and certainty |
| beta | [0, 1] | Brain region activations |
| gamma | [0, 1] | Psychological constructs |
| delta | [0, 1] | Validation predictions |
| epsilon | [0, 1] | Learning dynamics |
| **zeta** | **[-1, +1]** | **Bipolar polarity axes (clamped in compute)** |
| eta | [0, 1] | Vocabulary gradation indices (normalized) |
| theta | [0, 1] | Narrative structure |

Zeta is the only group with output in [-1, +1]. All other groups produce values in [0, 1]. The range is not enforced by the dataclass itself -- each group's `compute()` method is responsible for clamping its output to the documented range.

---

## 6. Usage in the Pipeline

### Created by groups

Each group's `compute()` method constructs and returns a `SemanticGroupOutput`:

```python
def compute(self, brain_output, **kwargs):
    tensor = ...  # (B, T, self.OUTPUT_DIM)
    return SemanticGroupOutput(
        group_name=self.GROUP_NAME,
        level=self.LEVEL,
        tensor=tensor,
        dimension_names=tuple(self.dimension_names),
    )
```

### Consumed by L3Orchestrator

The orchestrator collects all group outputs, extracts their tensors, and concatenates:

```python
tensors = [group_output.tensor for group_output in all_outputs]
combined = torch.cat(tensors, dim=-1)  # (B, T, 104)
```

### Stored in L3Output

The final `L3Output` dataclass holds both the per-group outputs and the concatenated tensor:

```python
@dataclass
class L3Output:
    model_name: str                           # "Brain"
    groups: Dict[str, SemanticGroupOutput]     # keyed by group_name
    tensor: Tensor                            # (B, T, total_dim)
```

---

## 7. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| [BaseSemanticGroup](BaseSemanticGroup.md) | Return type of `compute()` method |
| [L3Orchestrator](L3Orchestrator.md) | Collects and concatenates all group outputs |
| [EpsilonStateContract](EpsilonStateContract.md) | Epsilon's output tensor is passed to dependent groups |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
