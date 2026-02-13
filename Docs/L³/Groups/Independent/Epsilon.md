# L³ Groups — Epsilon (Learning Dynamics)

**Version**: 2.1.0
**Symbol**: ε
**Level**: 5
**Dimensions**: 19 (fixed)
**Phase**: 1b (Independent, **STATEFUL**)
**Output Range**: [0, 1]
**Code**: `mi_beta/language/groups/epsilon.py` (336 lines)
**Updated**: 2026-02-13

---

## Overview

Epsilon answers the question: **HOW does the listener learn from the music over time?**

Epsilon is the **only stateful group** in L³. It maintains online statistics across frames to compute surprise, prediction errors at multiple timescales, precision (inverse uncertainty), information-theoretic quantities, Huron ITPRA dynamics, and reward aesthetics. It tracks two signals from BrainOutput: **pleasure** and **arousal** (with fallback to mean activation and variance respectively).

**Audience**: Information theorists, predictive processing researchers, music cognition.

**Critical**: Epsilon must be **reset between audio files** to clear accumulated state.

---

## 7 Subcategories

| Subcategory | Dim | Indices | Primary Theory |
|-------------|:---:|:-------:|----------------|
| Surprise & Entropy | 2 | 0--1 | Pearce 2005 IDyOM, Shannon 1948 |
| Prediction Errors | 3 | 2--4 | Koelsch 2019 (multi-timescale) |
| Precision | 2 | 5--6 | Friston 2010 (free energy) |
| Information Dynamics | 3 | 7--9 | Itti & Baldi 2009, Dubnov 2008, Schmidhuber 2009 |
| Interaction | 1 | 10 | Cheung et al. 2019 |
| ITPRA | 5 | 11--15 | Huron 2006 (5-stage model) |
| Reward & Aesthetics | 3 | 16--18 | Gold et al. 2019, Berlyne 1971, Zajonc 1968 |

---

## Dimension Table

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 0 | `surprise` | [0,1] | `-log2(P(state|prev)) / log2(8)` | Pearce 2005 |
| 1 | `entropy` | [0,1] | `-sum(p * log2(p)) / log2(8)` | Shannon 1948 |
| 2 | `pe_short` | [0,1] | `tanh((x - EMA_short) / sqrt(Var_short + eps)) * 0.5 + 0.5` | Koelsch 2019 |
| 3 | `pe_medium` | [0,1] | `tanh((x - EMA_medium) / sqrt(Var_medium + eps)) * 0.5 + 0.5` | Koelsch 2019 |
| 4 | `pe_long` | [0,1] | `tanh((x - EMA_long) / sqrt(Var_long + eps)) * 0.5 + 0.5` | Koelsch 2019 |
| 5 | `precision_short` | [0,1] | `1 / (1 + Var_short)` | Friston 2010 |
| 6 | `precision_long` | [0,1] | `1 / (1 + Var_long)` | Friston 2010 |
| 7 | `bayesian_surprise` | [0,1] | `sigmoid(|PE_med| * prec_long * 5)` | Itti & Baldi 2009 |
| 8 | `information_rate` | [0,1] | `entropy * (1 - autocorr)` | Dubnov 2008 |
| 9 | `compression_progress` | [0,1] | `sigmoid((H_old - H_new) * 5)` | Schmidhuber 2009 |
| 10 | `entropy_x_surprise` | [0,1] | `entropy * surprise` | Cheung et al. 2019 |
| 11 | `imagination` | [0,1] | `EMA_long[0]` (pleasure baseline) | Huron 2006 ITPRA-I |
| 12 | `tension_uncertainty` | [0,1] | `entropy` (alias) | Huron 2006 ITPRA-T |
| 13 | `prediction_reward` | [0,1] | `exp(-|PE| / sigma_medium)` | Huron 2006 ITPRA-P |
| 14 | `reaction_magnitude` | [0,1] | `(|PE_med| * prec_long).clamp(0,1)` | Huron 2006 ITPRA-R |
| 15 | `appraisal_learning` | [0,1] | `compression_progress` (alias) | Huron 2006 ITPRA-A |
| 16 | `reward_pe` | [0,1] | `tanh(x - EMA_med) * 0.5 + 0.5` | Gold et al. 2019 |
| 17 | `wundt_position` | [0,1] | `4 * surprise * (1 - surprise)` | Berlyne 1971 |
| 18 | `familiarity` | [0,1] | `log(transitions) / log(total)` | Zajonc 1968 |

---

## Internal State

Epsilon maintains the following state tensors across frames. All are initialized lazily on the first `compute()` call.

### EMA Accumulators (3 timescales x 2D)

| Timescale | Alpha | Effective Window | State Variable |
|-----------|:-----:|:----------------:|----------------|
| Short | 0.1 | ~10 frames (~58ms) | `_ema_short` (B, 2) |
| Medium | 0.01 | ~100 frames (~580ms) | `_ema_medium` (B, 2) |
| Long | 0.001 | ~1000 frames (~5.8s) | `_ema_long` (B, 2) |

Each EMA tracks 2 dimensions: `[pleasure, arousal]`.

### EMA Variance (3 timescales x 2D)

| State Variable | Shape | Initial Value |
|----------------|:-----:|:------------:|
| `_var_short` | (B, 2) | 0.1 |
| `_var_medium` | (B, 2) | 0.1 |
| `_var_long` | (B, 2) | 0.1 |

Variance is updated with the same alpha as the corresponding EMA: `Var = alpha * diff^2 + (1 - alpha) * Var`.

### Welford Online Statistics

| State Variable | Shape | Purpose |
|----------------|:-----:|---------|
| `_welford_count` | scalar | Number of frames seen |
| `_welford_mean` | (B, 2) | Running mean |
| `_welford_m2` | (B, 2) | Running sum of squared deviations |

### Markov Transition Matrix

| State Variable | Shape | Purpose |
|----------------|:-----:|---------|
| `_transition_counts` | (B, 8, 8) | Count of state-to-state transitions |
| `_prev_state` | (B,) | Previous quantized state index |

The Markov model quantizes pleasure into 8 states (bins 0--7) via `(x * 7).long().clamp(0, 7)`. The transition count matrix is initialized with Laplace prior (all 1s).

### Ring Buffer

| State Variable | Shape | Purpose |
|----------------|:-----:|---------|
| `_buffer` | (B, 50) | Circular buffer of pleasure values |
| `_buffer_idx` | scalar | Current write position |
| `_buffer_count` | scalar | Number of values written (max 50) |

Used for compression progress: compares entropy of old half vs new half of the buffer.

### Previous Frame Cache

| State Variable | Shape | Purpose |
|----------------|:-----:|---------|
| `_prev_pleasure` | (B,) | Previous frame's pleasure value (for autocorrelation) |

---

## Hyperparameters

| Parameter | Value | Purpose |
|-----------|:-----:|---------|
| `ALPHA_SHORT` | 0.1 | EMA decay rate, short timescale |
| `ALPHA_MEDIUM` | 0.01 | EMA decay rate, medium timescale |
| `ALPHA_LONG` | 0.001 | EMA decay rate, long timescale |
| `N_STATES` | 8 | Markov quantization bins |
| `BUFFER_SIZE` | 50 | Ring buffer length for compression progress |
| `D_TRACK` | 2 | Number of tracked signals (pleasure, arousal) |
| `EPS` | 1e-8 | Numerical stability epsilon |

---

## Formulas

### EMA Update

```python
EMA_new = alpha * x + (1 - alpha) * EMA_old
Var_new = alpha * (x - EMA_new)^2 + (1 - alpha) * Var_old
```

### Surprise & Entropy (from Markov model)

```python
# Transition probability for observed state given previous state
tp_row = transition_counts[prev_state] / sum(transition_counts[prev_state])
tp_observed = tp_row[current_state]

# Surprise: normalized negative log probability
surprise = -log2(tp_observed + eps) / log2(8)  # [0, 1]

# Entropy: normalized Shannon entropy of transition row
entropy = -sum(tp_row * log2(tp_row + eps)) / log2(8)  # [0, 1]
```

Both are normalized by `log2(N_STATES)` = `log2(8)` to ensure [0,1] output range.

### Prediction Errors (3 timescales)

```python
# Standardized PE: deviation from EMA normalized by standard deviation
PE = tanh((x - EMA[pleasure]) / (sqrt(Var[pleasure] + eps))) * 0.5 + 0.5
```

The `tanh()` normalizes to [-1,+1], then `* 0.5 + 0.5` maps to [0,1]. Values > 0.5 indicate positive PE (better than expected), < 0.5 indicate negative PE.

### Precision

```python
precision = 1.0 / (1.0 + Var[pleasure])
```

Bayesian precision: inverse of variance plus 1. High precision = low uncertainty = stable predictions.

### Bayesian Surprise

```python
bayesian_surprise = sigmoid(|PE_medium| * precision_long * 5.0)
```

Combines medium-term prediction error magnitude with long-term confidence. Large PE under high precision = high Bayesian surprise.

### Information Rate

```python
autocorr = clamp(x * prev_pleasure, 0, 1)
information_rate = entropy * (1.0 - autocorr)
```

Mutual information proxy: high entropy with low autocorrelation = high information rate.

### Compression Progress

```python
# Uses ring buffer of 50 pleasure values
old_half = buffer[0:25]   # older values
new_half = buffer[25:50]  # newer values
H_old = buffer_entropy(old_half)   # histogram-based entropy over 8 bins
H_new = buffer_entropy(new_half)
compression_progress = sigmoid((H_old - H_new) * 5.0)
```

Following Schmidhuber's compression progress theory: if the new half has lower entropy than the old half, the listener is successfully compressing (learning) the musical structure. Returns 0.5 when buffer is not yet full.

### ITPRA Components

```python
# I: Imagination = long-term pleasure baseline
imagination = EMA_long[pleasure]

# T: Tension = entropy (uncertainty is tension)
tension_uncertainty = entropy

# P: Prediction reward = exponential decay of PE
prediction_reward = exp(-|PE_med| / (sigma_medium + eps))

# R: Reaction magnitude = precision-weighted PE
reaction_magnitude = clamp(|PE_med| * precision_long, 0, 1)

# A: Appraisal = compression progress (learning)
appraisal_learning = compression_progress
```

### Reward & Aesthetics

```python
# Reward PE: unsigned tanh PE (same formula as pe_medium but without variance normalization)
reward_pe = tanh(x - EMA_medium) * 0.5 + 0.5

# Wundt inverted-U: peaks at surprise = 0.5 (moderate arousal)
wundt_position = 4.0 * surprise * (1.0 - surprise)

# Familiarity: log-ratio of current-state transitions to total transitions
familiarity = log1p(sum(transitions[current_state])) / log1p(welford_count + 1)
```

The **Wundt curve** `4x(1-x)` is the simplest quadratic with peak at x=0.5, capturing Berlyne's inverted-U hypothesis: moderate surprise is maximally pleasant.

---

## Reset Protocol

Epsilon state must be reset between audio files to prevent state leakage:

```python
epsilon_group.reset()  # Sets _state_initialized = False
# Next compute() call will lazily re-initialize all state
```

The `reset()` method sets `_state_initialized = False`. On the next `compute()` call, `_init_state(B, device, dtype)` is called, re-creating all state tensors from scratch.

**Warning**: Failing to reset between files will cause the Markov model, EMA accumulators, and ring buffer to carry over learned statistics from the previous file, contaminating all 19 output dimensions.

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| Tracked signals | `pleasure = _safe_get_dim(brain_output, "pleasure")` | epsilon.py:150 |
| | `arousal = _safe_get_dim(brain_output, "arousal")` | epsilon.py:151 |
| EMA short alpha | `ALPHA_SHORT = 0.1` | epsilon.py:76 |
| EMA medium alpha | `ALPHA_MEDIUM = 0.01` | epsilon.py:77 |
| EMA long alpha | `ALPHA_LONG = 0.001` | epsilon.py:78 |
| N_STATES | `N_STATES = 8` | epsilon.py:79 |
| BUFFER_SIZE | `BUFFER_SIZE = 50` | epsilon.py:80 |
| D_TRACK | `D_TRACK = 2` | epsilon.py:81 |
| EPS | `EPS = 1e-8` | epsilon.py:82 |
| State init | `_init_state(B, device, dtype)` | epsilon.py:104-134 |
| EMA update | `self._ema_short = ALPHA * tracked + (1-ALPHA) * self._ema_short` | epsilon.py:162-173 |
| Variance update | `self._var_short = ALPHA * diff^2 + (1-ALPHA) * self._var_short` | epsilon.py:176-190 |
| Welford update | `delta_w, delta2_w` pattern | epsilon.py:193-197 |
| Markov state | `current_state = (x * 7).long().clamp(0, 7)` | epsilon.py:200-201 |
| Transition probability | `tp_row = counts[prev] / sum(counts[prev])` | epsilon.py:203-208 |
| Surprise | `(-log2(tp + eps) / log2_n).clamp(0,1)` | epsilon.py:211 |
| Entropy | `-(tp_row * log2(tp_row + eps)).sum(-1) / log2_n` | epsilon.py:213-214 |
| PE short | `tanh((x - EMA_short[0]) / (sigma_s + eps)) * 0.5 + 0.5` | epsilon.py:228-230 |
| Precision short | `1.0 / (1.0 + Var_short[0])` | epsilon.py:239 |
| Bayesian surprise | `sigmoid(|PE_med| * prec_l * 5.0)` | epsilon.py:244 |
| Autocorrelation | `(x * prev_pleasure).clamp(0, 1)` | epsilon.py:247 |
| Info rate | `entropy * (1 - autocorr)` | epsilon.py:248 |
| Buffer write | `buffer[:, buffer_idx] = x` | epsilon.py:252 |
| Compression progress | `sigmoid((old_ent - new_ent) * 5.0)` | epsilon.py:266 |
| Buffer entropy | `_buffer_entropy(values)` helper | epsilon.py:321-335 |
| Wundt | `4.0 * surprise * (1.0 - surprise)` | epsilon.py:281 |
| Familiarity | `log1p(transitions[current].sum()) / log1p(count+1)` | epsilon.py:282-291 |
| Reset | `reset()` sets `_state_initialized = False` | epsilon.py:100-102 |
| Lazy init | `if not self._state_initialized: _init_state(...)` | epsilon.py:146-147 |
| OUTPUT_DIM | `OUTPUT_DIM = 19` (class constant) | epsilon.py:73 |

---

## Frame-by-Frame Processing

Unlike all other L³ groups, Epsilon iterates over frames within `compute()`:

```python
for t in range(T):
    x = pleasure[:, t]          # (B,)
    x_ar = arousal[:, t]        # (B,)
    tracked = stack([x, x_ar])  # (B, 2)

    # Update all state, compute all 19 dims for this frame
    output[:, t, :] = ...       # (B, 19)
```

This is necessary because each frame's computation depends on the state accumulated from all previous frames. The temporal loop makes Epsilon the most computationally expensive L³ group.

---

## Design Notes

- **Only stateful group**: All other L³ groups are stateless and can be parallelized freely
- **19D is the largest fixed-dim group**: More dimensions than any other single group
- **Two tracked signals**: Only pleasure and arousal drive the 19 outputs
- **Three timescales**: Short/medium/long EMA provide hierarchical temporal context
- **Schmidhuber learning**: Compression progress is the only dimension requiring a ring buffer
- **Wundt optimality**: The inverted-U captures the aesthetic sweet spot of moderate surprise
- **Normalized outputs**: All Markov quantities normalized by log2(8) for [0,1] range
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)`

---

## Parent / See Also

- **Parent**: [Independent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Learning.md](../../Epistemology/Learning.md) — Level 5 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Pipeline**: [Pipeline/StateManagement.md](../../Pipeline/StateManagement.md) — epsilon lifecycle and reset protocol
- **Contracts**: [Contracts/EpsilonStateContract.md](../../Contracts/EpsilonStateContract.md) — stateful group interface
- **Consumers**: [Dependent/Zeta.md](../Dependent/Zeta.md) (reads eps[0,1,6]), [Dependent/Theta.md](../Dependent/Theta.md) (reads eps[0,2,5])
- **Code**: `mi_beta/language/groups/epsilon.py`
