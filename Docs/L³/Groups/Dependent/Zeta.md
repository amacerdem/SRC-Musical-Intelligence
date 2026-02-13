# L³ Groups — Zeta (Polarity)

**Version**: 2.1.0
**Symbol**: ζ
**Level**: 6
**Dimensions**: 12 (fixed)
**Phase**: 2 (Dependent, Stateless)
**Output Range**: [-1, +1] (bipolar -- only group with this range)
**Dependencies**: BrainOutput, epsilon_output
**Code**: `mi_beta/language/groups/zeta.py` (145 lines)
**Updated**: 2026-02-13

---

## Overview

Zeta answers the question: **WHICH direction?**

Zeta maps Brain and epsilon outputs to 12 **bipolar semantic axes**, each spanning [-1, +1] with named negative and positive poles. This is the only L³ group that outputs bipolar values — all others output [0, 1]. The bipolar representation enables natural linguistic interpretation: "sad vs joyful", "calm vs excited", "familiar vs novel", etc.

**Audience**: Semanticists, linguistic researchers, affective computing.

---

## Theoretical Basis

- **Semantic Differential Theory** (Osgood, Suci, & Tannenbaum 1957): Evaluation, Potency, Activity factor structure
- **Circumplex Model of Affect** (Russell 1980): Valence-arousal bipolar space
- **Wanting/Liking Dissociation** (Berridge 2003): Incentive salience vs hedonic pleasure

---

## POLARITY_AXES Constant

The `POLARITY_AXES` constant defines all 12 axes with their named poles:

| Index | Axis Name | Negative Pole | Positive Pole | Category |
|:-----:|-----------|:-------------:|:-------------:|----------|
| 0 | `valence` | sad | joyful | Reward |
| 1 | `arousal` | calm | excited | Reward |
| 2 | `tension` | relaxed | tense | Reward |
| 3 | `power` | delicate | powerful | Reward |
| 4 | `wanting` | satiated | craving | Reward |
| 5 | `liking` | displeasure | satisfaction | Reward |
| 6 | `novelty` | familiar | novel | Learning |
| 7 | `complexity` | simple | complex | Learning |
| 8 | `beauty` | discordant | harmonious | Aesthetic |
| 9 | `groove` | rigid | flowing | Aesthetic |
| 10 | `stability` | chaotic | stable | Aesthetic |
| 11 | `engagement` | detached | absorbed | Aesthetic |

---

## 3 Axis Categories

### Reward Axes (6D, indices 0--5)

Derived from Brain [0,1] signals via the `2x - 1` transform:

| Index | Name | Formula | Source Signal |
|:-----:|------|---------|:------------:|
| 0 | `valence` | `2 * valence - 1` | `brain.valence` |
| 1 | `arousal` | `2 * arousal - 1` | `brain.arousal` |
| 2 | `tension` | `2 * tension - 1` | `brain.tension` |
| 3 | `power` | `2 * arousal - 1` (proxy) | `brain.arousal` |
| 4 | `wanting` | `2 * wanting - 1` | `brain.wanting` |
| 5 | `liking` | `2 * liking - 1` | `brain.liking` |

**Note**: Power currently uses arousal as a proxy when `ans_composite` is unavailable.

### Learning Axes (3D, indices 6--7, 10)

Derived from epsilon output signals via the `2x - 1` transform:

| Index | Name | Formula | Source Signal |
|:-----:|------|---------|:------------:|
| 6 | `novelty` | `2 * epsilon[0] - 1` | ε surprise |
| 7 | `complexity` | `2 * epsilon[1] - 1` | ε entropy |
| 10 | `stability` | `2 * epsilon[6] - 1` | ε precision_long |

When `epsilon_output` is `None`, all learning axes default to 0 (neutral polarity).

### Aesthetic Axes (3D, indices 8--9, 11)

Derived from Brain signals, some via interaction terms:

| Index | Name | Formula | Source Signal |
|:-----:|------|---------|:------------:|
| 8 | `beauty` | `2 * beauty - 1` | `brain.beauty` |
| 9 | `groove` | `2 * (arousal * harmonic_context) - 1` | Interaction term |
| 11 | `engagement` | `2 * (pleasure * arousal) - 1` | Interaction term |

---

## Formulas

### Core Transform: [0,1] to [-1,+1]

```python
# For Brain dimensions in [0,1]:
polarity = 2 * value - 1  # maps [0,1] -> [-1,+1]
```

### Reward Axes

```python
valence_pol = 2 * _safe_get_dim(brain_output, "valence") - 1
arousal_pol = 2 * _safe_get_dim(brain_output, "arousal") - 1
tension_pol = 2 * _safe_get_dim(brain_output, "tension") - 1
power_pol   = 2 * _safe_get_dim(brain_output, "arousal") - 1  # proxy
wanting_pol = 2 * _safe_get_dim(brain_output, "wanting") - 1
liking_pol  = 2 * _safe_get_dim(brain_output, "liking") - 1
```

### Learning Axes (from epsilon)

```python
if epsilon_output is not None:
    novelty    = 2 * epsilon_output[..., 0:1] - 1   # eps[0] = surprise
    complexity = 2 * epsilon_output[..., 1:2] - 1   # eps[1] = entropy
    stability  = 2 * epsilon_output[..., 6:7] - 1   # eps[6] = precision_long
else:
    novelty = complexity = stability = 0  # neutral polarity
```

### Aesthetic Axes

```python
beauty_pol     = 2 * beauty - 1
groove_pol     = 2 * (arousal * harmonic_context) - 1
engagement_pol = 2 * (pleasure * arousal) - 1
```

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| POLARITY_AXES | `POLARITY_AXES: Tuple[Dict[str, str], ...]` (12 entries) | zeta.py:41-54 |
| Valence polarity | `valence_pol = (2 * valence - 1).unsqueeze(-1)` | zeta.py:95-96 |
| Arousal polarity | `arousal = 2 * _safe_get_dim(..., "arousal") - 1` | zeta.py:98 |
| Tension polarity | `tension = 2 * _safe_get_dim(..., "tension") - 1` | zeta.py:99 |
| Power proxy | `power_val = _safe_get_dim(..., "arousal")` | zeta.py:102 |
| Wanting polarity | `wanting = 2 * _safe_get_dim(..., "wanting") - 1` | zeta.py:105 |
| Liking polarity | `liking = 2 * _safe_get_dim(..., "liking") - 1` | zeta.py:106 |
| Novelty (from ε) | `novelty = 2 * epsilon_output[..., 0:1] - 1` | zeta.py:110 |
| Complexity (from ε) | `complexity = 2 * epsilon_output[..., 1:2] - 1` | zeta.py:111 |
| Stability (from ε) | `stability = 2 * epsilon_output[..., 6:7] - 1` | zeta.py:112 |
| Beauty polarity | `beauty = (2 * beauty_val - 1).unsqueeze(-1)` | zeta.py:120 |
| Groove interaction | `groove_val = arousal * harmonic_context` | zeta.py:122-125 |
| Engagement interaction | `engagement_val = pleasure * arousal` | zeta.py:128-131 |
| Output clamp | `tensor.clamp(-1, 1)` | zeta.py:142 |
| Dimension names | `[ax["name"] for ax in POLARITY_AXES]` | zeta.py:78 |
| OUTPUT_DIM | `OUTPUT_DIM = 12` (class constant) | zeta.py:74 |
| Epsilon fallback | `zero = torch.zeros_like(...)` when epsilon_output is None | zeta.py:113-116 |

---

## Output Tensor Layout

The output tensor is ordered as:

```python
tensor = cat([
    valence_pol, arousal, tension, power, wanting, liking,  # Reward (6D)
    novelty, complexity,                                     # Learning (2D)
    beauty, groove,                                          # Aesthetic (2D)
    stability,                                               # Learning (1D)
    engagement,                                              # Aesthetic (1D)
], dim=-1)  # (B, T, 12) in [-1, +1]
```

**Note**: The ordering interleaves learning and aesthetic axes (stability at index 10, engagement at index 11) rather than grouping them contiguously. This matches the `POLARITY_AXES` constant ordering.

---

## Design Notes

- **Only bipolar group**: Output range [-1, +1] distinguishes ζ from all other L³ groups
- **12 axes**: Matches η's 12 vocabulary axes one-to-one
- **Named poles**: Each axis has human-readable negative/positive pole names
- **Epsilon dependency**: Learning axes (novelty, complexity, stability) require epsilon output
- **Graceful fallback**: Returns neutral polarity (0) when epsilon_output is None
- **Interaction terms**: Groove and engagement are multiplicative interactions
- **Power proxy**: Currently aliased to arousal (awaiting ans_composite signal)

---

## Parent / See Also

- **Parent**: [Dependent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Polarity.md](../../Epistemology/Polarity.md) — Level 6 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Vocabulary**: [Vocabulary/AxisDefinitions.md](../../Vocabulary/AxisDefinitions.md) — 12 axis definitions
- **Consumer**: [Dependent/Eta.md](Eta.md) — quantizes ζ polarity into vocabulary terms
- **Consumer**: [Dependent/Theta.md](Theta.md) — reads ζ for connector computation
- **Source**: [Independent/Epsilon.md](../Independent/Epsilon.md) — provides learning signals
- **Code**: `mi_beta/language/groups/zeta.py`
