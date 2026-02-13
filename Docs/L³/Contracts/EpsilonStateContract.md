# EpsilonStateContract — Stateful Group State Management

**Scope**: Documents the state lifecycle, state components, hyperparameters, memory budget, and reset protocol for the EpsilonGroup -- the only stateful group in L³.

**Code file**: `mi_beta/language/groups/epsilon.py`

---

## 1. Lifecycle

Epsilon's state follows a three-phase lifecycle:

```
[Lazy Init]  ──>  [Accumulate]  ──>  [Reset]
     |                  |                |
     |                  |                +-- _state_initialized = False
     |                  |                    (next compute triggers fresh init)
     |                  |
     |                  +-- each compute() call updates all state
     |                      for each frame t in the input
     |
     +-- _init_state(B, device, dtype)
         triggered on first compute() when _state_initialized is False
```

### Lazy Initialization

State is not allocated in `__init__()`. Instead, `_init_state(B, device, dtype)` is called on the first `compute()` invocation. This defers memory allocation until the batch size, device, and dtype are known from the actual input tensor.

### Accumulation

Each `compute()` call processes all T frames in the input tensor. For each frame t, all state components are updated: EMA accumulators shift, Markov transitions are counted, Welford statistics accumulate, and the ring buffer advances.

### Reset

`reset()` sets `_state_initialized = False`. The next `compute()` call triggers a fresh `_init_state()`, allocating clean state tensors. The old state is released for garbage collection.

**When to reset**: Between audio files. The `L3Orchestrator.reset()` method delegates to `epsilon.reset()`.

---

## 2. State Components

### 2.1 EMA Accumulators (3 timescales x 2 tracked dims)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_ema_short` | `(B, 2)` | 0.5 | `alpha * x + (1 - alpha) * ema` with alpha=0.1 |
| `_ema_medium` | `(B, 2)` | 0.5 | `alpha * x + (1 - alpha) * ema` with alpha=0.01 |
| `_ema_long` | `(B, 2)` | 0.5 | `alpha * x + (1 - alpha) * ema` with alpha=0.001 |

Tracks exponential moving averages of pleasure and arousal at three timescales.

### 2.2 EMA Variance (3 timescales x 2 tracked dims)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_var_short` | `(B, 2)` | 0.1 | `alpha * (x - ema)^2 + (1 - alpha) * var` |
| `_var_medium` | `(B, 2)` | 0.1 | `alpha * (x - ema)^2 + (1 - alpha) * var` |
| `_var_long` | `(B, 2)` | 0.1 | `alpha * (x - ema)^2 + (1 - alpha) * var` |

Running variance estimates used for prediction error normalization and precision computation.

### 2.3 Welford Online Variance (3 components)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_welford_count` | scalar (int) | 0 | `+1` per frame |
| `_welford_mean` | `(B, 2)` | 0.5 | Welford's online algorithm |
| `_welford_m2` | `(B, 2)` | 0.0 | Welford's online algorithm |

Numerically stable online mean and variance computation using Welford's algorithm. Used for global statistics independent of the EMA timescales.

### 2.4 Markov Transition Model (2 components)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_prev_state` | `(B,)` long | 0 | Current quantized pleasure bin |
| `_transition_counts` | `(B, 8, 8)` | 1.0 (Laplace smoothing) | `counts[b, prev, curr] += 1` |

An 8-state Markov chain for modeling transition probabilities. Pleasure is quantized to bins 0--7. The transition matrix is Laplace-smoothed (initialized to ones) to avoid zero-probability transitions. Used for computing surprise and entropy.

### 2.5 Ring Buffer (3 components)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_buffer` | `(B, 50)` | 0.5 | Circular write at `_buffer_idx` |
| `_buffer_idx` | scalar (int) | 0 | `(idx + 1) % 50` |
| `_buffer_count` | scalar (int) | 0 | `min(count + 1, 50)` |

A ring buffer of size 50 used for computing compression progress (Schmidhuber 2009). The buffer stores recent entropy values. Compression progress is the difference between the mean of the older half and the newer half.

### 2.6 Previous Pleasure (1 component)

| Attribute | Shape | Initial Value | Update Rule |
|-----------|:-----:|:------------:|-------------|
| `_prev_pleasure` | `(B,)` | 0.5 | Set to current frame's pleasure |

Stores the previous frame's pleasure value for computing frame-to-frame reward prediction error.

---

## 3. Hyperparameters

| Name | Value | Effective Timescale | Purpose |
|------|:-----:|:------------------:|---------|
| `ALPHA_SHORT` | 0.1 | ~10 frames (~58 ms) | Short-term EMA decay -- single onset/attack |
| `ALPHA_MEDIUM` | 0.01 | ~100 frames (~580 ms) | Medium-term EMA decay -- one beat at ~103 BPM |
| `ALPHA_LONG` | 0.001 | ~1000 frames (~5.8 s) | Long-term EMA decay -- musical phrase/passage |
| `N_STATES` | 8 | -- | Markov chain quantization bins (0--7) |
| `BUFFER_SIZE` | 50 | ~290 ms | Ring buffer length for compression progress |
| `D_TRACK` | 2 | -- | Number of tracked signals (pleasure + arousal) |
| `EPS` | 1e-8 | -- | Numerical stability epsilon for division/log |

### Timescale Correspondence

```
Timescale     Alpha     1/Alpha     Duration     Musical Scale
---------     -----     -------     --------     -------------
Short         0.1       ~10         ~58 ms       Single onset / attack
Medium        0.01      ~100        ~580 ms      One beat at 103 BPM
Long          0.001     ~1000       ~5.8 s       Musical phrase / passage
```

The frame rate is 172.27 Hz (inherited from the R³ pipeline), so 1/alpha frames corresponds to alpha-inverse * 5.8 ms.

---

## 4. Memory Budget

Per batch element:

| Component | Floats | Ints | Breakdown |
|-----------|:------:|:----:|-----------|
| EMA accumulators | 6 | -- | 3 timescales x 2 dims |
| EMA variance | 6 | -- | 3 timescales x 2 dims |
| Welford mean + M2 | 4 | -- | 2 tensors x 2 dims |
| Welford count | -- | 1 | scalar |
| Transition counts | 64 | -- | 8 x 8 matrix |
| Previous state | -- | 1 | scalar (long) |
| Ring buffer | 50 | -- | 50-element buffer |
| Buffer idx + count | -- | 2 | 2 scalars |
| Previous pleasure | 1 | -- | scalar |
| **Total** | **~131** | **4** | |

Total state memory per batch element: approximately 131 floats + 4 integers. For a batch size of 1 at float32, this is roughly 528 bytes of state -- negligible relative to the input tensor.

---

## 5. Tracked Features

Epsilon tracks two features from the Brain output:

| Index | Feature | Source | Fallback |
|:-----:|---------|--------|----------|
| 0 | Pleasure | `brain_output["pleasure"]` | Mean activation across all Brain dims |
| 1 | Arousal | `brain_output["arousal"]` | Variance across all Brain dims |

The fallbacks ensure epsilon can operate even when the Brain does not expose named pleasure/arousal dimensions (graceful degradation via `_safe_get_dim()`).

---

## 6. Initialization Detail

`_init_state(B, device, dtype)` allocates all state tensors:

```python
def _init_state(self, B, device, dtype):
    # EMA accumulators
    self._ema_short = torch.full((B, 2), 0.5, device=device, dtype=dtype)
    self._ema_medium = torch.full((B, 2), 0.5, device=device, dtype=dtype)
    self._ema_long = torch.full((B, 2), 0.5, device=device, dtype=dtype)

    # EMA variance
    self._var_short = torch.full((B, 2), 0.1, device=device, dtype=dtype)
    self._var_medium = torch.full((B, 2), 0.1, device=device, dtype=dtype)
    self._var_long = torch.full((B, 2), 0.1, device=device, dtype=dtype)

    # Welford
    self._welford_count = 0
    self._welford_mean = torch.full((B, 2), 0.5, device=device, dtype=dtype)
    self._welford_m2 = torch.zeros((B, 2), device=device, dtype=dtype)

    # Markov
    self._prev_state = torch.zeros(B, device=device, dtype=torch.long)
    self._transition_counts = torch.ones(B, 8, 8, device=device, dtype=dtype)

    # Ring buffer
    self._buffer = torch.full((B, 50), 0.5, device=device, dtype=dtype)
    self._buffer_idx = 0
    self._buffer_count = 0

    # Previous pleasure
    self._prev_pleasure = torch.full((B,), 0.5, device=device, dtype=dtype)

    self._state_initialized = True
```

---

## 7. Reset Protocol

```python
def reset(self):
    self._state_initialized = False
```

Setting `_state_initialized = False` causes the next `compute()` call to trigger a fresh `_init_state()`. All previous state tensors become unreferenced and are garbage collected.

**Caller**: `L3Orchestrator.reset()` delegates to `self.groups["epsilon"].reset()`.

**When**: Between audio files, before processing a new audio input.

**Thread safety**: None. Epsilon assumes single-threaded execution. If multiple threads call `compute()` or `reset()` concurrently, state corruption will occur. This is a known design constraint.

---

## 8. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| [BaseSemanticGroup](BaseSemanticGroup.md) | EpsilonGroup implements this ABC, adding stateful behavior |
| [SemanticGroupOutput](SemanticGroupOutput.md) | Epsilon returns this dataclass; its tensor is passed to zeta and theta |
| [L3Orchestrator](L3Orchestrator.md) | Orchestrator manages epsilon's position in the phase sequence and delegates `reset()` |
| [BaseModelSemanticAdapter](BaseModelSemanticAdapter.md) | Adapters prepare the Brain dimensions that epsilon tracks |

---

## 9. Cross-References

| Related Document | Path |
|-----------------|------|
| Epsilon group specification | [../Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md) |
| Learning epistemology | [../Epistemology/Learning.md](../Epistemology/Learning.md) |
| State management pipeline | [../Pipeline/StateManagement.md](../Pipeline/StateManagement.md) |
| L³ architecture (Section 8) | [../L3-SEMANTIC-ARCHITECTURE.md](../L3-SEMANTIC-ARCHITECTURE.md) |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
