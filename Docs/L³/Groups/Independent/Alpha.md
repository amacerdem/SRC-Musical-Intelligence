# L³ Groups — Alpha (Computation Semantics)

**Version**: 2.1.0
**Symbol**: α
**Level**: 1
**Dimensions**: Variable (N_active_units + 2)
**Phase**: 1 (Independent, Stateless)
**Output Range**: [0, 1]
**Code**: `mi_beta/language/groups/alpha.py` (98 lines)
**Updated**: 2026-02-13

---

## Overview

Alpha answers the question: **HOW was this computed?**

Alpha provides computational transparency by tracing every Brain output dimension back to its source unit. It produces one attribution dimension per active unit (mean activation), plus two global dimensions: **computation_certainty** (Bayesian precision of the full output) and **bipolar_activation** (net direction of the signed dimensions).

**Audience**: Engineers, system debuggers, white-box interpretability.

---

## Dimensionality

Alpha has **variable dimensionality** that depends on the number of active Brain units:

- **mi_beta (current)**: N_active_units + 2 (auto-discovered at runtime)
- **mi v2 design spec (26D input)**: 6D fixed (shared_attribution, reward_attribution, affect_attribution, autonomic_attribution, computation_certainty, bipolar_activation)

In mi_beta, the `_configure()` method discovers unit names from the `BrainOutput.unit_outputs` dictionary on the first call to `compute()`.

---

## Dimension Table

| Local Index | Name | Range | Formula | Source |
|:-----------:|------|:-----:|---------|--------|
| 0..N-1 | `{unit}_attribution` | [0,1] | `mean(unit_tensor, dim=-1)` | Per-unit mean activation |
| N | `computation_certainty` | [0,1] | `1 / (1 + Var(full_output))` | Bayesian precision |
| N+1 | `bipolar_activation` | [0,1] | `(mean(brain) - 0.5) * 2 * 0.5 + 0.5` | Net signed direction |

Where N = number of active units.

---

## Formulas

### Per-Unit Attribution

```python
# For each active unit:
unit_tensor = brain_output.get_unit(unit_name)  # (B, T, unit_dim)
attribution = unit_tensor.mean(dim=-1, keepdim=True)  # (B, T, 1)
```

Mean activation across all model output dimensions within a unit. Higher values indicate the unit is producing stronger activations on average.

### Computation Certainty

```python
full = brain_output.tensor  # (B, T, brain_dim)
certainty = 1.0 / (1.0 + full.var(dim=-1, keepdim=True))  # (B, T, 1)
```

Inverse variance of the full Brain output vector. Derived from Bayesian precision: high certainty means the Brain is producing consistent activations across all dimensions. When variance is 0, certainty = 1.0 (maximum). When variance is 1.0, certainty = 0.5.

### Bipolar Activation

```python
bipolar = (full.mean(dim=-1, keepdim=True) - 0.5) * 2.0  # [-1, +1]
bipolar = bipolar * 0.5 + 0.5  # remap to [0, 1]
```

The mean of all Brain dimensions, centered around the neutral point (0.5 in [0,1] space). The intermediate [-1,+1] representation captures net direction, then is remapped to [0,1] for output consistency. Values > 0.5 indicate net positive activation; values < 0.5 indicate net suppression.

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| Per-unit attribution | `attr = unit_tensor.mean(dim=-1, keepdim=True)` | alpha.py:76 |
| Computation certainty | `certainty = 1.0 / (1.0 + full.var(dim=-1, keepdim=True))` | alpha.py:81 |
| Bipolar activation | `bipolar = (full.mean(...) - 0.5) * 2.0` then `* 0.5 + 0.5` | alpha.py:86-87 |
| Auto-configuration | `_configure(brain_output)` reads `brain_output.unit_outputs.keys()` | alpha.py:47-50 |
| Unit names | `self._unit_names = sorted(brain_output.unit_outputs.keys())` | alpha.py:49 |
| Output dim | `self._output_dim = len(self._unit_names) + 2` | alpha.py:50 |
| Dimension names | `[f"{u.lower()}_attribution" for u in self._unit_names] + [certainty, bipolar]` | alpha.py:58-59 |

---

## Auto-Configuration Protocol

Alpha is unique among L³ groups: it does not know its output dimensionality until it receives its first BrainOutput. The protocol:

1. `__init__()` sets `_output_dim = 2` (minimum: certainty + bipolar)
2. On first `compute()` call, if `_unit_names` is empty, calls `_configure(brain_output)`
3. `_configure()` reads `brain_output.unit_outputs.keys()`, sorts them, stores as `_unit_names`
4. `_output_dim` is updated to `len(_unit_names) + 2`
5. Subsequent calls use the cached configuration

This lazy initialization ensures Alpha adapts to whatever units are active without hardcoded assumptions.

---

## Design Notes

- **White-box principle**: Alpha enables tracing any L³ output back through gamma/beta to the specific C³ unit that produced it
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)` to enforce range
- **Sorted unit names**: Guarantees deterministic dimension ordering across runs
- **No learned parameters**: Pure algebraic computation from BrainOutput

---

## Parent / See Also

- **Parent**: [Independent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Computation.md](../../Epistemology/Computation.md) — Level 1 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Code**: `mi_beta/language/groups/alpha.py`
