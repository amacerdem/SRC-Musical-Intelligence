# L³ Pipeline — State Management

**Version**: 2.1.0
**Scope**: Epsilon state lifecycle, reset protocol, memory budget, and threading constraints
**Code**: `mi_beta/language/groups/epsilon.py` (EpsilonGroup)
**Updated**: 2026-02-13

---

## 1. Overview

Epsilon is the **only stateful group** in L³. All other groups (alpha through delta, zeta, eta, theta) are pure functions -- they produce identical output for identical input regardless of call history. Epsilon, by contrast, maintains online statistics that accumulate across frames within an audio file and must be explicitly reset between files.

This document describes the complete state lifecycle: lazy initialization, per-frame accumulation, reset protocol, batch size change handling, memory budget, and thread safety constraints.

---

## 2. State Lifecycle

```
                  ┌──────────────────────────────────┐
                  │         UNINITIALIZED             │
                  │    _state_initialized = False      │
                  └──────────────┬───────────────────┘
                                 │
                    first compute() or after reset()
                                 │
                                 ▼
                  ┌──────────────────────────────────┐
                  │        LAZY INITIALIZATION        │
                  │    _init_state(B, device, dtype)  │
                  │    _state_initialized = True       │
                  └──────────────┬───────────────────┘
                                 │
                           each compute()
                                 │
                                 ▼
                  ┌──────────────────────────────────┐
                  │         ACCUMULATION              │◄──┐
                  │    for t in range(T):             │   │
                  │      update EMA, variance         │   │ next compute()
                  │      update Welford               │   │
                  │      update Markov transitions    │   │
                  │      advance ring buffer          │   │
                  │      store prev_pleasure          │───┘
                  └──────────────┬───────────────────┘
                                 │
                          reset() called
                          (between files)
                                 │
                                 ▼
                  ┌──────────────────────────────────┐
                  │            RESET                   │
                  │    _state_initialized = False       │
                  │    old tensors → garbage collection │
                  └──────────────┬───────────────────┘
                                 │
                                 └──→ back to UNINITIALIZED
```

---

## 3. Lazy Initialization

State is **not** allocated in `__init__()`. The constructor only sets:

```python
def __init__(self):
    self._state_initialized = False
```

On the first `compute()` call, the method checks:

```python
if not self._state_initialized or self._batch_size != B:
    self._init_state(B, device, dtype)
```

This defers memory allocation until the batch size `B`, device, and dtype are known from the actual input tensor. It also handles batch size changes mid-session (see Section 6).

---

## 4. State Components

### 4.1 EMA Accumulators (6 tensors)

Three timescales, each tracking 2 dimensions (pleasure, arousal):

| Attribute | Shape | Init Value | Alpha | Effective Window |
|-----------|:-----:|:----------:|:-----:|:----------------:|
| `_ema_short` | (B, 2) | 0.5 | 0.1 | ~10 frames (~58 ms) |
| `_ema_medium` | (B, 2) | 0.5 | 0.01 | ~100 frames (~580 ms) |
| `_ema_long` | (B, 2) | 0.5 | 0.001 | ~1000 frames (~5.8 s) |

Update rule: `EMA_new = alpha * tracked + (1 - alpha) * EMA_old`

### 4.2 EMA Variance (6 tensors)

Running variance estimates at the same three timescales:

| Attribute | Shape | Init Value | Update Rule |
|-----------|:-----:|:----------:|-------------|
| `_var_short` | (B, 2) | 0.1 | `alpha * (tracked - ema)^2 + (1 - alpha) * var` |
| `_var_medium` | (B, 2) | 0.1 | Same formula, alpha=0.01 |
| `_var_long` | (B, 2) | 0.1 | Same formula, alpha=0.001 |

Used for prediction error normalization (PE = deviation / sigma) and precision computation (precision = 1 / (1 + var)).

### 4.3 Welford Online Variance (3 components)

| Attribute | Shape | Init Value | Purpose |
|-----------|:-----:|:----------:|---------|
| `_welford_count` | scalar int | 0 | Frame counter |
| `_welford_mean` | (B, 2) | 0.5 | Running mean |
| `_welford_m2` | (B, 2) | 0.0 | Running sum of squared deviations |

Provides numerically stable global statistics independent of the EMA timescales. The count also serves as the denominator for the familiarity computation.

### 4.4 Markov Transition Model (2 components)

| Attribute | Shape | Init Value | Purpose |
|-----------|:-----:|:----------:|---------|
| `_prev_state` | (B,) long | 0 | Previous quantized state (0--7) |
| `_transition_counts` | (B, 8, 8) | 1.0 | State-to-state counts (Laplace prior) |

Pleasure is quantized to 8 states via `(x * 7).long().clamp(0, 7)`. The transition count matrix is initialized with Laplace smoothing (all ones) to avoid zero-probability transitions. Surprise and entropy are derived from normalized transition rows.

### 4.5 Ring Buffer (3 components)

| Attribute | Shape | Init Value | Purpose |
|-----------|:-----:|:----------:|---------|
| `_buffer` | (B, 50) | 0.5 | Circular buffer of pleasure values |
| `_buffer_idx` | scalar int | 0 | Current write position |
| `_buffer_count` | scalar int | 0 | Values written (max 50) |

Used for Schmidhuber compression progress: compares entropy of the older half vs the newer half. Returns default 0.5 until the buffer is full (50 frames).

### 4.6 Previous Pleasure (1 component)

| Attribute | Shape | Init Value | Purpose |
|-----------|:-----:|:----------:|---------|
| `_prev_pleasure` | (B,) | 0.5 | Previous frame pleasure for autocorrelation |

Used in information rate computation: `info_rate = entropy * (1 - autocorr)`.

---

## 5. Per-Frame Accumulation

Each `compute()` call processes all T frames sequentially:

```python
for t in range(T):
    x = pleasure[:, t]           # (B,)
    x_ar = arousal[:, t]         # (B,)
    tracked = stack([x, x_ar])   # (B, 2)

    # 1. EMA updates (3 timescales)
    # 2. Variance updates (3 timescales)
    # 3. Welford global update
    # 4. Markov transition: quantize x → state, update counts
    # 5. Compute all 19 output dimensions for frame t
    # 6. Ring buffer: append x, advance index
    # 7. Store prev_pleasure = x
```

**Ordering matters**: Each operation depends on the current state, and the state is updated before the next frame. The output dimensions for frame t are computed using state that includes updates from frames 0 through t (for surprise/entropy/PE/etc.) or 0 through t-1 (for dimensions using `_prev_pleasure`).

---

## 6. Batch Size Change Handling

If the batch size B changes between `compute()` calls (without an intervening `reset()`), the check at the top of `compute()` detects the mismatch:

```python
if not self._state_initialized or self._batch_size != B:
    self._init_state(B, device, dtype)
```

This triggers a fresh `_init_state()`, effectively resetting all state. This is a safety measure -- accumulated state from a different batch size would have incompatible tensor shapes and cannot be meaningfully reused.

---

## 7. Reset Protocol

### 7.1 Method

```python
def reset(self):
    self._state_initialized = False
```

### 7.2 Caller

The `L3Orchestrator.reset()` method delegates:

```python
def reset(self):
    self.groups["epsilon"].reset()
```

### 7.3 When to Call

Between audio files, before processing a new audio input. Typical usage:

```python
# Process file 1
l3_out_1 = orchestrator.compute(brain_output_1)

# Reset before file 2
orchestrator.reset()

# Process file 2
l3_out_2 = orchestrator.compute(brain_output_2)
```

### 7.4 Effect

Setting `_state_initialized = False` causes the next `compute()` call to call `_init_state()`, which:
1. Allocates fresh state tensors (EMA, variance, Welford, Markov, buffer, prev_pleasure)
2. Sets `_state_initialized = True`
3. Stores `_batch_size = B`

The old state tensors become unreferenced and are garbage collected by Python/PyTorch.

### 7.5 Consequences of Not Resetting

| State Component | Contamination Effect |
|-----------------|---------------------|
| EMA accumulators | Prediction errors reference previous file's baseline |
| EMA variance | Precision reflects previous file's variability |
| Welford statistics | Global mean/variance include previous file's data |
| Markov transitions | Surprise and entropy reflect cross-file transition history |
| Ring buffer | Compression progress compares cross-file segments |
| Previous pleasure | First-frame autocorrelation uses last frame of previous file |

All 19 epsilon dimensions and the 40 downstream dimensions (zeta 12 + eta 12 + theta 16) that depend on epsilon are affected.

---

## 8. Memory Budget

Per batch element at float32:

| Component | Floats | Ints | Bytes (f32) |
|-----------|:------:|:----:|:-----------:|
| EMA accumulators (3 x 2) | 6 | -- | 24 |
| EMA variance (3 x 2) | 6 | -- | 24 |
| Welford mean + M2 (2 x 2) | 4 | -- | 16 |
| Welford count | -- | 1 | 4 |
| Transition counts (8 x 8) | 64 | -- | 256 |
| Previous state | -- | 1 | 8 (long) |
| Ring buffer (50) | 50 | -- | 200 |
| Buffer idx + count | -- | 2 | 8 |
| Previous pleasure | 1 | -- | 4 |
| **Total** | **~131** | **4** | **~544** |

For batch size B=1: approximately 544 bytes of state. This is negligible relative to the input tensor (B x T x D_brain x 4 bytes) or the output tensor (B x T x 19 x 4 bytes).

For batch size B=32: approximately 17 KB of state.

**Note**: The scalar ints (`_welford_count`, `_buffer_idx`, `_buffer_count`) are shared across the batch (not per-element), so their contribution is constant.

---

## 9. Thread Safety

Epsilon assumes **single-threaded execution**. There are no locks, atomics, or synchronization primitives. Concurrent calls to `compute()` or `reset()` from multiple threads will cause state corruption.

This is a known design constraint. The L3Orchestrator is intended to be called from a single processing thread per audio stream. If parallel processing is needed, each thread should have its own `L3Orchestrator` instance.

---

## 10. Cross-References

| Related Document | Path |
|-----------------|------|
| Dependency DAG | [DependencyDAG.md](DependencyDAG.md) |
| Execution model | [ExecutionModel.md](ExecutionModel.md) |
| Performance analysis | [Performance.md](Performance.md) |
| Epsilon group spec | [../Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md) |
| Epsilon state contract | [../Contracts/EpsilonStateContract.md](../Contracts/EpsilonStateContract.md) |
| L3Orchestrator contract | [../Contracts/L3Orchestrator.md](../Contracts/L3Orchestrator.md) |
| Epsilon code | `mi_beta/language/groups/epsilon.py` |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
