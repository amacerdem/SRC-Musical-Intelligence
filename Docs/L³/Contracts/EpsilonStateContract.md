# EpsilonStateContract — Stateful Group Management

Epsilon (ε) is the only stateful group in L³. This document specifies its state management contract.

**Code**: `mi_beta/language/groups/epsilon.py`

## Lifecycle

```
┌─── Construction ───→ _state_initialized = False
│
├─── First compute() ──→ _init_state(B, device, dtype)
│                         _state_initialized = True
│
├─── Subsequent compute() ──→ Accumulate state per frame
│        ↑ (loop)              EMA update, Markov transition,
│        └────────────────────  Welford variance, ring buffer
│
├─── reset() ──→ _state_initialized = False
│                 Next compute() triggers fresh _init_state()
│
└─── Batch size change ──→ Re-initialize state for new B
```

## Hyperparameters

| Parameter | Value | Effective Timescale | Purpose |
|-----------|-------|---------------------|---------|
| `ALPHA_SHORT` | 0.1 | ~10 frames (~58 ms) | Short-term EMA decay |
| `ALPHA_MEDIUM` | 0.01 | ~100 frames (~580 ms) | Medium-term EMA decay |
| `ALPHA_LONG` | 0.001 | ~1000 frames (~5.8 s) | Long-term EMA decay |
| `N_STATES` | 8 | — | Markov quantization bins |
| `BUFFER_SIZE` | 50 | ~290 ms window | Ring buffer for compression progress |
| `D_TRACK` | 2 | — | Tracked features (pleasure, arousal) |
| `EPS` | 1e-8 | — | Numerical stability epsilon |

## State Components

### 1. EMA Accumulators (6 tensors)

| Tensor | Shape | Init | Description |
|--------|-------|------|-------------|
| `_ema_short` | `(B, 2)` | 0.5 | Short-term exponential moving average |
| `_ema_medium` | `(B, 2)` | 0.5 | Medium-term EMA |
| `_ema_long` | `(B, 2)` | 0.5 | Long-term EMA |
| `_var_short` | `(B, 2)` | 0.1 | Short-term EMA variance |
| `_var_medium` | `(B, 2)` | 0.1 | Medium-term EMA variance |
| `_var_long` | `(B, 2)` | 0.1 | Long-term EMA variance |

### 2. Welford Online Variance (3 components)

| Component | Type/Shape | Init | Description |
|-----------|-----------|------|-------------|
| `_welford_count` | `int` | 0 | Total frames processed |
| `_welford_mean` | `(B, 2)` | 0.5 | Running global mean |
| `_welford_m2` | `(B, 2)` | 0.0 | Running sum of squared deviations |

### 3. Markov Transition Model (2 components)

| Component | Shape | Init | Description |
|-----------|-------|------|-------------|
| `_prev_state` | `(B,)` long | 0 | Previous quantized state |
| `_transition_counts` | `(B, 8, 8)` | 1.0 | Transition counts (Laplace-smoothed) |

### 4. Ring Buffer (3 components)

| Component | Type/Shape | Init | Description |
|-----------|-----------|------|-------------|
| `_buffer` | `(B, 50)` | 0.5 | Circular buffer of pleasure values |
| `_buffer_idx` | `int` | 0 | Current write position |
| `_buffer_count` | `int` | 0 | Fill count (max 50) |

### 5. Previous Frame (1 tensor)

| Component | Shape | Init | Description |
|-----------|-------|------|-------------|
| `_prev_pleasure` | `(B,)` | 0.5 | Previous frame's pleasure value |

## Memory Budget

Per batch element: ~143 floats + 2 integers
- EMA: 6 × 2 = 12 floats
- Variance: 6 × 2 = 12 floats
- Welford: 2 + 2 = 4 floats + 1 int
- Markov: 8 × 8 + 1 = 65 floats
- Buffer: 50 floats + 2 ints
- Previous: 1 float
- **Total**: 144 floats + 3 ints ≈ 588 bytes/batch element

## Tracked Features

Epsilon tracks 2 features from `BrainOutput` (with fallback):
- **pleasure**: `brain_output.get_dim("pleasure")` or mean activation
- **arousal**: `brain_output.get_dim("arousal")` or tensor variance

## Thread Safety

None. Single-threaded execution assumed. Concurrent access to state tensors is undefined behavior.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [../Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md), [../Pipeline/StateManagement.md](../Pipeline/StateManagement.md)
