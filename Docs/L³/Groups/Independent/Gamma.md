# L³ Groups — Gamma (Psychology Semantics)

**Version**: 2.1.0
**Symbol**: γ
**Level**: 3
**Dimensions**: 13 (fixed)
**Phase**: 1 (Independent, Stateless)
**Output Range**: [0, 1]
**Code**: `mi_beta/language/groups/gamma.py` (134 lines)
**Updated**: 2026-02-13

---

## Overview

Gamma answers the question: **WHAT does it mean subjectively?**

Gamma maps Brain outputs to psychological constructs across five subcategories: reward processing, ITPRA tension-resolution dynamics, aesthetic experience, core affect (valence/arousal), and chill/frisson phenomena. It provides the primary bridge between computational neuroscience and subjective musical experience.

**Audience**: Psychologists, music cognition researchers, affective computing.

---

## 5 Subcategories

| Subcategory | Dim | Indices | Primary Theory |
|-------------|:---:|:-------:|----------------|
| Reward | 3 | 0--2 | Berridge wanting/liking, Salimpoor DA phases |
| ITPRA | 2 | 3--4 | Huron 2006 expectation theory |
| Aesthetics | 3 | 5--7 | Blood & Zatorre, Konecni, Janata |
| Emotion | 2 | 8--9 | Russell circumplex model |
| Chills | 3 | 10--12 | de Fleurian & Pearce, Sloboda, Grewe |

---

## Dimension Table

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 0 | `reward_intensity` | [0,1] | `pleasure` | Salimpoor et al. 2011 |
| 1 | `reward_type` | [0,1] | `(liking - wanting) * 0.5 + 0.5` | Berridge 2003 |
| 2 | `reward_phase` | [0,1] | `(da_nacc - da_caudate) * 0.5 + 0.5` | Salimpoor et al. 2011 |
| 3 | `itpra_tension_resolution` | [0,1] | `(1 - tension) * harmonic_context` | Huron 2006 |
| 4 | `itpra_surprise_evaluation` | [0,1] | `|prediction_error| * emotional_arc` | Huron 2006 |
| 5 | `beauty` | [0,1] | `beauty` (passthrough) | Blood & Zatorre 2001 |
| 6 | `sublime` | [0,1] | `pleasure * arousal` | Konecni 2005 |
| 7 | `groove` | [0,1] | `arousal * harmonic_context` | Janata et al. 2012 |
| 8 | `valence` | [0,1] | `valence` (passthrough from Brain) | Russell 1980 |
| 9 | `arousal` | [0,1] | `arousal` (passthrough from Brain) | Yang et al. 2025 |
| 10 | `chill_probability` | [0,1] | `SCR * (1 - HR)` | de Fleurian & Pearce 2021 |
| 11 | `chill_intensity` | [0,1] | `chills_intensity` (passthrough) | Sloboda 1991, Guhn et al. 2007 |
| 12 | `chill_phase` | [0,1] | `sigmoid(chills_intensity - tension)` | Grewe et al. 2009 |

---

## Formulas

### Reward (3D)

```python
# Reward intensity: direct pleasure signal
reward_intensity = pleasure  # [0,1]

# Reward type: liking-dominant (>0.5) vs wanting-dominant (<0.5)
reward_type = (liking - wanting) * 0.5 + 0.5  # [-1,1] -> [0,1]

# Reward phase: consummation (>0.5, NAcc-dominant) vs anticipation (<0.5, Caudate-dominant)
reward_phase = (da_nacc - da_caudate) * 0.5 + 0.5  # [-1,1] -> [0,1]
```

**Reward type** captures the Berridge wanting/liking dissociation: values above 0.5 indicate liking (hedonic pleasure) dominates, while values below 0.5 indicate wanting (incentive salience) dominates.

**Reward phase** captures the Salimpoor finding that Caudate activates during anticipation and NAcc during peak pleasure (consummation).

### ITPRA (2D)

```python
# Tension-resolution: high when tension is low AND harmonic context supports resolution
itpra_tension_resolution = (1.0 - tension) * harmonic_context

# Surprise-evaluation: high when prediction error is large AND emotional arc is active
itpra_surprise_evaluation = abs(prediction_error) * emotional_arc
```

Following Huron's ITPRA theory, tension_resolution captures the Tension and Resolution stages, while surprise_evaluation captures the Imagination/Prediction and Reaction/Appraisal stages.

### Aesthetics (3D)

```python
# Beauty: opioid-mediated hedonic pleasure (direct passthrough)
beauty = beauty_val

# Sublime: awe/transcendence as interaction of pleasure and arousal
sublime = pleasure * arousal

# Groove: motor-harmonic coupling pleasure
groove = arousal * harmonic_context
```

### Emotion (2D)

```python
# Valence: direct passthrough from Brain's valence dimension
valence = valence  # [0,1], already in correct range

# Arousal: direct passthrough from Brain's arousal dimension
arousal = arousal  # [0,1]
```

Follows Russell's (1980) circumplex model of affect with valence and arousal as orthogonal core affect dimensions.

### Chills (3D)

```python
# Chill probability: ANS signature (high SCR + low HR = sympathetic + parasympathetic co-activation)
chill_probability = SCR * (1.0 - HR)

# Chill intensity: passthrough from Brain's chills signal
chill_intensity = chills_intensity

# Chill phase: buildup (<0.5) vs peak/afterglow (>0.5)
chill_phase = sigmoid(chills_intensity - tension)
```

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| `_safe_get_dim` helper | `_safe_get_dim(brain_output, name, default=0.5)` | gamma.py:45-55 |
| Pleasure signal | `pleasure = _safe_get_dim(brain_output, "pleasure")` | gamma.py:80 |
| Wanting signal | `wanting = _safe_get_dim(brain_output, "wanting")` | gamma.py:81 |
| Liking signal | `liking = _safe_get_dim(brain_output, "liking")` | gamma.py:82 |
| DA Caudate | `da_caudate = _safe_get_dim(brain_output, "da_caudate")` | gamma.py:83 |
| DA NAcc | `da_nacc = _safe_get_dim(brain_output, "da_nacc")` | gamma.py:84 |
| Tension | `tension = _safe_get_dim(brain_output, "tension")` | gamma.py:91 |
| Harmonic context | `harmonic_ctx = _safe_get_dim(brain_output, "harmonic_context")` | gamma.py:92 |
| Prediction error | `pred_error = _safe_get_dim(brain_output, "prediction_error", default=0.0)` | gamma.py:93 |
| Emotional arc | `emotional_arc = _safe_get_dim(brain_output, "emotional_arc")` | gamma.py:94 |
| SCR | `scr = _safe_get_dim(brain_output, "scr")` | gamma.py:112 |
| HR | `hr = _safe_get_dim(brain_output, "hr")` | gamma.py:113 |
| Chills | `chills = _safe_get_dim(brain_output, "chills_intensity")` | gamma.py:114 |
| OUTPUT_DIM | `OUTPUT_DIM = 13` (class constant) | gamma.py:62 |

---

## Graceful Degradation

Gamma uses `_safe_get_dim()` throughout. When a Brain dimension is missing:

- **Default = 0.5**: Most signals (pleasure, wanting, liking, tension, arousal, etc.)
- **Default = 0.0**: `prediction_error` — zero PE is the neutral state
- **Result**: All formulas produce meaningful (if neutral) values even with incomplete Brain output

---

## Design Notes

- **Fixed 13D**: Unlike Alpha/Beta, Gamma always outputs exactly 13 dimensions
- **No learned parameters**: All formulas are deterministic
- **Psychological grounding**: Every dimension maps to a published psychological construct
- **Interaction terms**: Sublime and groove are explicit two-factor interactions, capturing emergent phenomena
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)`

---

## Parent / See Also

- **Parent**: [Independent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Psychology.md](../../Epistemology/Psychology.md) — Level 3 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Vocabulary**: [Vocabulary/TermCatalog.md](../../Vocabulary/TermCatalog.md) — terms for eta quantization of gamma-related axes
- **Code**: `mi_beta/language/groups/gamma.py`
