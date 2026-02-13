# L³ Groups — Theta (Narrative)

**Version**: 2.1.0
**Symbol**: θ
**Level**: 8
**Dimensions**: 16 (fixed)
**Phase**: 2 (Dependent, Stateless)
**Output Range**: [0, 1]
**Dependencies**: BrainOutput, epsilon_output, zeta_output
**Code**: `mi_beta/language/groups/theta.py` (155 lines)
**Updated**: 2026-02-13

---

## Overview

Theta answers the question: **HOW to describe this in language?**

Theta produces a sentence-level linguistic structure for generating natural language descriptions of musical moments. It decomposes each frame into four 4D slots — **Subject**, **Predicate**, **Modifier**, **Connector** — that together form a narrative sentence template. This is the highest-level interpretation group, closest to human language output.

**Audience**: Narrative researchers, NLG systems, music description, lay communication.

---

## 4 Slots (4D each = 16D total)

| Slot | Dim | Indices | Question | Mechanism |
|------|:---:|:-------:|----------|-----------|
| Subject | 4 | 0--3 | WHICH aspect dominates? | softmax competition |
| Predicate | 4 | 4--7 | WHAT is happening? | Temporal dynamics from ε |
| Modifier | 4 | 8--11 | HOW is it happening? | Intensity/certainty/novelty/speed |
| Connector | 4 | 12--15 | TEMPORAL relation? | Polarity-based from ζ |

---

## Dimension Table

### Subject (4D) — WHICH aspect dominates?

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 0 | `reward_salience` | [0,1] | `softmax(pleasure * 3.0)` | Salimpoor et al. 2011 |
| 1 | `tension_salience` | [0,1] | `softmax(tension * 3.0)` | Huron 2006 |
| 2 | `motion_salience` | [0,1] | `softmax(arousal * 3.0)` | Yang et al. 2025 |
| 3 | `beauty_salience` | [0,1] | `softmax(beauty * 3.0)` | Blood & Zatorre 2001 |

### Predicate (4D) — WHAT is happening?

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 4 | `rising` | [0,1] | `clamp(pe_short - 0.5, min=0) * 2` | Schubert 2004 |
| 5 | `peaking` | [0,1] | `pleasure * arousal` | Sloboda 1991 |
| 6 | `falling` | [0,1] | `clamp(0.5 - pe_short, min=0) * 2` | Schubert 2004 |
| 7 | `stable` | [0,1] | `1 - (rising + falling + peaking)` | Meyer 1956 |

### Modifier (4D) — HOW is it happening?

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 8 | `intensity` | [0,1] | `arousal` | Gabrielsson 2001 |
| 9 | `certainty` | [0,1] | `epsilon[5]` (precision_short) | Friston 2010 |
| 10 | `novelty` | [0,1] | `epsilon[0]` (surprise) | Berlyne 1971 |
| 11 | `speed` | [0,1] | `sigmoid(|prediction_error| * 3)` | Fong et al. 2020 |

### Connector (4D) — TEMPORAL relation?

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 12 | `continuing` | [0,1] | `1 / (1 + |val_pol| + |ten_pol|)` | Halliday & Hasan 1976 |
| 13 | `contrasting` | [0,1] | `(|val_pol| + |ten_pol|) / 2` | Almen 2008 |
| 14 | `resolving` | [0,1] | `clamp(-ten_pol, min=0)` | Huron 2006 |
| 15 | `transitioning` | [0,1] | `1 - (continuing + contrasting + resolving)` | Caplin 1998 |

---

## Formulas

### Subject: Softmax Competition (temp=3.0)

```python
# Four candidate aspects compete via softmax
subject_raw = cat([pleasure, tension, arousal, beauty], dim=-1)  # (B, T, 4)
subject = softmax(subject_raw * 3.0, dim=-1)                     # (B, T, 4)
```

The temperature parameter (3.0) controls competition sharpness. Higher temperature = more winner-take-all. At temp=3.0, a dominant aspect (e.g., pleasure=0.8, others~0.5) will get the majority of the probability mass.

**Interpretation**: The subject with the highest softmax weight is the "topic" of the current musical moment: "Reward is...", "Tension is...", "Motion is...", or "Beauty is...".

### Predicate: Temporal Dynamics

```python
# pe_short from epsilon: [0,1] with center at 0.5
pe_short = epsilon_output[..., 2:3]  # (B, T, 1)

# Rising: positive PE (increasing signal)
rising = clamp(pe_short - 0.5, min=0) * 2.0  # [0, 1]

# Falling: negative PE (decreasing signal)
falling = clamp(0.5 - pe_short, min=0) * 2.0  # [0, 1]

# Peaking: high pleasure AND high arousal simultaneously
peaking = (pleasure * arousal).clamp(0, 1)

# Stable: residual when no strong dynamic is present
stable = (1.0 - (rising + falling + peaking)).clamp(min=0)
```

**Interpretation**: "...is rising", "...is peaking", "...is falling", or "...is stable".

### Modifier: Quality Descriptors

```python
# Intensity: how strongly (from arousal)
intensity = arousal  # (B, T, 1)

# Certainty: how confidently (from epsilon precision_short)
certainty = epsilon_output[..., 5:6]  # eps[5] = precision_short

# Novelty: how surprisingly (from epsilon surprise)
novelty = epsilon_output[..., 0:1]  # eps[0] = surprise

# Speed: how quickly (from prediction error magnitude)
speed = sigmoid(|prediction_error| * 3.0)  # (B, T, 1)
```

**Interpretation**: "...intensely", "...confidently", "...surprisingly", "...quickly".

### Connector: Temporal Relations

```python
# val_pol and ten_pol from zeta: [-1, +1]
val_pol = zeta_output[..., 0:1]  # valence polarity
ten_pol = zeta_output[..., 2:3]  # tension polarity

# Continuing: low polarity = same thread continues
continuing = 1.0 / (1.0 + |val_pol| + |ten_pol|)

# Contrasting: high polarity = opposing element
contrasting = (|val_pol| + |ten_pol|) / 2.0

# Resolving: negative tension polarity = tension resolving
resolving = clamp(-ten_pol, min=0)

# Transitioning: residual
transitioning = (1.0 - (continuing + contrasting + resolving)).clamp(min=0)
```

**Interpretation**: "...continuing the current thread", "...contrasting with what came before", "...resolving earlier tension", "...transitioning to something new".

---

## Example Sentence

Given a frame where:
- reward_salience = 0.65 (dominant subject)
- rising = 0.8 (predicate)
- intensity = 0.7 (modifier)
- continuing = 0.6 (connector)

The generated sentence template:

> **Reward** [0.65] is **rising** [0.8] **intensely** [0.7], **continuing** [0.6] the current thread.

Each slot's winning dimension provides the word; the value provides the confidence.

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| Pleasure (subject) | `pleasure = _safe_get_dim(brain_output, "pleasure").unsqueeze(-1)` | theta.py:94 |
| Tension (subject) | `tension = _safe_get_dim(brain_output, "tension").unsqueeze(-1)` | theta.py:95 |
| Arousal (subject) | `arousal = _safe_get_dim(brain_output, "arousal").unsqueeze(-1)` | theta.py:96 |
| Beauty (subject) | `beauty = _safe_get_dim(brain_output, "beauty").unsqueeze(-1)` | theta.py:97 |
| Softmax temp=3.0 | `subject = torch.softmax(subject_raw * 3.0, dim=-1)` | theta.py:100 |
| PE short | `pe_short = epsilon_output[..., 2:3]` | theta.py:104 |
| Rising | `rising = (pe_short - 0.5).clamp(min=0) * 2.0` | theta.py:108 |
| Falling | `falling = (0.5 - pe_short).clamp(min=0) * 2.0` | theta.py:109 |
| Peaking | `peaking = (pleasure * arousal).clamp(0, 1)` | theta.py:110 |
| Stable | `stable = (1.0 - (rising + falling + peaking)).clamp(min=0)` | theta.py:111 |
| Certainty (from ε) | `certainty = epsilon_output[..., 5:6]` | theta.py:119 |
| Novelty (from ε) | `novelty_mod = epsilon_output[..., 0:1]` | theta.py:120 |
| Speed | `speed = torch.sigmoid(pred_error.abs() * 3.0).unsqueeze(-1)` | theta.py:126 |
| Val polarity (from ζ) | `val_pol = zeta_output[..., 0:1]` | theta.py:132 |
| Ten polarity (from ζ) | `ten_pol = zeta_output[..., 2:3]` | theta.py:133 |
| Continuing | `continuing = 1.0 / (1.0 + val_pol.abs() + ten_pol.abs())` | theta.py:138 |
| Contrasting | `contrasting = (val_pol.abs() + ten_pol.abs()) * 0.5` | theta.py:139 |
| Resolving | `resolving = (-ten_pol).clamp(min=0)` | theta.py:140 |
| Transitioning | `transitioning = (1.0 - (cont + contr + resolv)).clamp(min=0)` | theta.py:141 |
| Epsilon fallback | `half = one * 0.5` when epsilon_output is None | theta.py:91, 106 |
| Zeta fallback | `val_pol = ten_pol = zeros` when zeta_output is None | theta.py:135-136 |
| OUTPUT_DIM | `OUTPUT_DIM = 16` (class constant) | theta.py:60 |

---

## Dependency Handling

Theta reads from three sources with graceful fallback:

| Source | Used For | Fallback When None |
|--------|----------|-------------------|
| BrainOutput | Subject (pleasure, tension, arousal, beauty), Speed (prediction_error) | `_safe_get_dim()` returns 0.5 |
| epsilon_output | Predicate (pe_short), Modifier (precision_short, surprise) | 0.5 (neutral PE, moderate certainty/novelty) |
| zeta_output | Connector (valence_polarity, tension_polarity) | 0.0 (neutral polarity, all connectors = ~0.33) |

---

## Slot Interactions

The four slots are designed to be **compositionally independent**:

- **Subject** depends only on Brain signals (which aspect is most active)
- **Predicate** depends only on epsilon (temporal dynamics)
- **Modifier** combines Brain and epsilon signals (quality descriptors)
- **Connector** depends only on zeta (temporal coherence)

This separation ensures that narrative descriptions remain interpretable even when individual sources degrade.

---

## Design Notes

- **16D is the second-largest fixed group** (after epsilon at 19D)
- **Softmax subject**: Competitive winner-take-all provides clear topic focus
- **Residual slots**: Both predicate and connector include a residual dimension (stable, transitioning) that absorbs unclassified states
- **Temperature 3.0**: Empirically tuned for readable narrative without over-sharpening
- **Three-source dependency**: Most complex dependency profile of any L³ group
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)`

---

## Parent / See Also

- **Parent**: [Dependent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Narrative.md](../../Epistemology/Narrative.md) — Level 8 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Source**: [Independent/Epsilon.md](../Independent/Epsilon.md) — provides PE, precision, surprise
- **Source**: [Dependent/Zeta.md](Zeta.md) — provides valence/tension polarity
- **Code**: `mi_beta/language/groups/theta.py`
