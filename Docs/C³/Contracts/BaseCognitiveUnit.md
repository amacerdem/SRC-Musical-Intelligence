# BaseCognitiveUnit -- Unit Interface

> **Code**: `mi_beta/contracts/base_unit.py`
> **Kind**: Abstract Base Class (ABC)
> **Imports from**: `BaseModel`

## Purpose

`BaseCognitiveUnit` groups related models that share a neural circuit and cognitive function. The nine units from the C³ meta-analysis are:

**Core-4 VALIDATED** (k >= 10 studies):

| Unit | Full Name | Circuit | Pooled d |
|------|-----------|---------|----------|
| SPU | Spectral Processing Unit | perceptual | 0.84 |
| STU | Sensorimotor Timing Unit | sensorimotor | 0.67 |
| IMU | Integrative Memory Unit | mnemonic | 0.53 |
| ARU | Affective Resonance Unit | mesolimbic | 0.83 |

**Experimental-5** (k < 10):

| Unit | Full Name | Circuit |
|------|-----------|---------|
| ASU | Auditory Salience Unit | salience |
| NDU | Novelty Detection Unit | -- |
| MPU | Motor Planning Unit | -- |
| PCU | Imagery / Emotion Unit | imagery |
| RPU | Reward / Salience Unit | -- |

A unit contains one or more `BaseModel` subclasses. The unit's `compute()` method runs its models in declared order and concatenates their outputs into a single tensor.

---

## Class Constants (must override in every subclass)

| Constant | Type | Description |
|----------|------|-------------|
| `UNIT_NAME` | `str` | Short unit identifier (e.g. `"ARU"`, `"SPU"`) |
| `FULL_NAME` | `str` | Full descriptive name (e.g. `"Affective Resonance Unit"`) |
| `CIRCUIT` | `str` | Primary neural circuit: `"mesolimbic"`, `"perceptual"`, `"sensorimotor"`, `"mnemonic"`, `"salience"`, `"imagery"` |
| `POOLED_EFFECT` | `float` | Pooled effect size (Cohen's d) from C³ meta-analysis. `0.0` for experimental units without meta-analytic estimates |

---

## Abstract Members

### `models -> List[BaseModel]` (property)

Ordered list of models in this unit. Models are executed in this order. The output of each model is concatenated along the last dimension to form the unit output.

### `compute(h3_features, r3_features, cross_unit_inputs) -> Tensor`

Compute the unit's concatenated output.

| Parameter | Type | Shape | Description |
|-----------|------|-------|-------------|
| `h3_features` | `Dict[Tuple[int,int,int,int], Tensor]` | `{4-tuple: (B, T)}` | Temporal features covering the union of all model demands |
| `r3_features` | `Tensor` | `(B, T, 49)` | R3 spectral features |
| `cross_unit_inputs` | `Optional[Dict[str, Tensor]]` | `{pathway_id: Tensor}` | Named tensors from other units' models |

**Returns**: `(B, T, total_dim)` concatenated output of all models.

---

## Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `active_models` | `List[BaseModel]` | Models currently active (default: all). Subclasses can override for conditional activation (e.g. disabling gamma-tier during validation) |
| `total_dim` | `int` | Sum of all active model `OUTPUT_DIM` values |
| `model_names` | `Tuple[str, ...]` | Names of all models in execution order |
| `mechanism_names` | `Tuple[str, ...]` | Flat tuple of all mechanism names across all models |
| `h3_demand` | `Set[Tuple[int,int,int,int]]` | Union of all H3 demands across all active models |
| `dimension_names` | `Tuple[str, ...]` | Flat tuple of all dimension names across all active models |
| `is_validated` | `bool` | `True` if `POOLED_EFFECT > 0.0` (has meta-analytic validation) |
| `model_ranges` | `Dict[str, Tuple[int, int]]` | Map from model name to `(start, end)` index range in the concatenated unit output |

---

## Validation Rules (`validate()`)

Returns a list of error messages (empty if valid). Checks:

1. `UNIT_NAME` must be non-empty
2. `FULL_NAME` must be non-empty
3. `CIRCUIT` must be non-empty
4. Every model must declare `UNIT == self.UNIT_NAME` (ownership check)
5. No duplicate model names within the unit
6. Delegates to each model's `validate_constants()` for per-model consistency

---

## Example Subclass

```python
class ARUnit(BaseCognitiveUnit):
    UNIT_NAME = "ARU"
    FULL_NAME = "Affective Resonance Unit"
    CIRCUIT = "mesolimbic"
    POOLED_EFFECT = 0.83

    @property
    def models(self) -> List[BaseModel]:
        return [self._srp, self._aac, self._vmm]
```
