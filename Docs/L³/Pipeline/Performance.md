# L³ Pipeline — Performance

**Version**: 2.1.0
**Scope**: Per-group compute cost, memory analysis, and optimization opportunities
**Code**: `mi_beta/language/groups/__init__.py` (L3Orchestrator)
**Updated**: 2026-02-13

---

## 1. Overview

All L³ groups operate without learned parameters -- every output dimension is a deterministic formula applied to the Brain output tensor. The computational cost is therefore dominated by tensor operations, not gradient computation. Epsilon is the clear bottleneck due to its frame-by-frame loop.

---

## 2. Per-Group Compute Cost

| Group | Phase | Complexity | Description |
|-------|:-----:|:----------:|-------------|
| alpha | 1 | O(N_units) | Linear scan of active unit outputs; one mean per unit |
| beta | 1 | O(N_regions) | Linear scan of unique brain region activations |
| gamma | 1 | O(1) | Fixed 13D extraction from Brain dims; vectorized |
| delta | 1 | O(1) | Fixed 12D extraction from Brain dims; vectorized |
| epsilon | 1b | **O(T x N_STATES^2)** | Frame loop with Markov transition + EMA per frame |
| zeta | 2a | O(1) | Fixed 12D bipolar mapping; vectorized |
| eta | 2b | O(1) | Fixed 12D quantization; vectorized |
| theta | 2c | O(1) | Fixed 16D with softmax competition; vectorized |

### Detailed Epsilon Cost

Epsilon's `compute()` contains a `for t in range(T)` loop. Within each iteration:

| Operation | Cost | Notes |
|-----------|------|-------|
| EMA update (3 timescales) | 3 x O(B x D_TRACK) | Simple multiply-add |
| Variance update (3 timescales) | 3 x O(B x D_TRACK) | Square + multiply-add |
| Welford update | O(B x D_TRACK) | Division + multiply |
| Markov state quantization | O(B) | Multiply + clamp |
| Transition probability row | O(B x N_STATES) | Row extraction + normalize |
| Surprise computation | O(B) | Log + division |
| Entropy computation | O(B x N_STATES) | Sum of p*log(p) |
| Transition count update | O(B) | Indexed increment |
| Prediction errors (3 timescales) | 3 x O(B) | tanh of normalized PE |
| Precision (2 timescales) | 2 x O(B) | Inverse of (1 + var) |
| Bayesian surprise | O(B) | Sigmoid |
| Information rate | O(B) | Multiply |
| Ring buffer write | O(B) | Indexed write |
| Compression progress | O(B x BUFFER_SIZE) | Only when buffer full; histogram entropy |
| Derived dimensions (ITPRA, reward, Wundt, familiarity) | O(B x N_STATES) | Simple formulas |
| Output assembly | O(B x 19) | Indexed write into output tensor |

**Total per frame**: approximately O(B x N_STATES) = O(B x 8) = O(B)
**Total per compute()**: O(T x B x N_STATES) = O(T x B x 8)

With N_STATES=8, the Markov operations dominate (8x8 matrix row normalization, 8-bin entropy sum).

---

## 3. Memory Analysis

### 3.1 Per-Group Output Tensors

| Group | Output Shape | Bytes (f32, B=1, T=100) |
|-------|:------------:|:-----------------------:|
| alpha | (B, T, 6) | 2,400 |
| beta | (B, T, 14) | 5,600 |
| gamma | (B, T, 13) | 5,200 |
| delta | (B, T, 12) | 4,800 |
| epsilon | (B, T, 19) | 7,600 |
| zeta | (B, T, 12) | 4,800 |
| eta | (B, T, 12) | 4,800 |
| theta | (B, T, 16) | 6,400 |
| **combined** | **(B, T, 104)** | **41,600** |

### 3.2 Epsilon State Memory

Epsilon is the only group with persistent state between `compute()` calls:

| Component | Per Batch Element | Total (B=1) |
|-----------|:-----------------:|:-----------:|
| EMA accumulators (6 x 2 floats) | 48 bytes | 48 bytes |
| EMA variance (6 x 2 floats) | 48 bytes | 48 bytes |
| Welford (4 floats + 1 int) | 20 bytes | 20 bytes |
| Markov (64 floats + 1 long) | 264 bytes | 264 bytes |
| Ring buffer (50 floats + 2 ints) | 208 bytes | 208 bytes |
| Previous pleasure (1 float) | 4 bytes | 4 bytes |
| **Total** | **~592 bytes** | **~592 bytes** |

All other groups are stateless and allocate only temporary tensors within `compute()`.

### 3.3 Peak Memory During Compute

During `compute()`, the orchestrator holds references to all 8 `SemanticGroupOutput` objects plus the `tensors` list. Peak memory occurs at the `torch.cat()` call, where both the individual tensors and the concatenated result exist simultaneously:

```
Peak = sum(group_outputs) + combined_tensor
     = (B x T x 104 x 4) + (B x T x 104 x 4)
     = 2 x (B x T x 104 x 4) bytes
```

For B=1, T=1000 (about 5.8 seconds of audio): approximately 832 KB. This is negligible.

---

## 4. Bottleneck Analysis

### 4.1 Epsilon Frame Loop

The critical bottleneck is epsilon's `for t in range(T)` Python loop. Unlike all other groups that process the full `(B, T, D)` tensor in vectorized operations, epsilon must iterate frame-by-frame because each frame's Markov state depends on the previous frame's result.

**Profiling estimate** (T=1000, B=1, CPU):
- Phase 1 (4 groups): < 1 ms total
- Phase 1b (epsilon): ~10-50 ms (dominated by Python loop overhead + per-frame tensor ops)
- Phase 2 (3 groups): < 1 ms total
- Assembly (torch.cat): < 0.1 ms

Epsilon accounts for approximately 90-95% of total L³ compute time.

### 4.2 Scaling with T

| T (frames) | Audio Duration | Estimated L³ Time |
|:----------:|:--------------:|:------------------:|
| 172 | ~1 second | ~2-10 ms |
| 1,000 | ~5.8 seconds | ~10-50 ms |
| 10,000 | ~58 seconds | ~100-500 ms |
| 50,000 | ~4.8 minutes | ~500 ms - 2.5 s |

These are rough estimates for CPU execution. GPU execution would shift the bottleneck to Python loop overhead and CPU-GPU synchronization rather than arithmetic.

---

## 5. Optimization Opportunities

### 5.1 Epsilon Vectorization (High Impact)

The EMA, variance, and Welford updates within epsilon could theoretically be vectorized using `torch.cumsum` or scan operations. However, the Markov transition model creates a true sequential dependency (current state depends on previous state), preventing full vectorization.

Partial vectorization could separate:
- **Vectorizable**: EMA updates, variance updates, Welford (if done separately from Markov)
- **Sequential**: Markov state quantization, transition count update, surprise/entropy

### 5.2 Phase 1 Parallelism (Low Impact)

Alpha, beta, gamma, and delta could be computed in parallel. However, each is individually very fast (sub-millisecond), so the parallelization overhead would likely exceed the benefit.

### 5.3 JIT Compilation (Medium Impact)

Epsilon's frame loop could benefit from `torch.jit.script` compilation, which would eliminate Python loop overhead. The current implementation uses standard Python, so each of the T iterations incurs interpreter overhead.

### 5.4 Fused Kernel (High Impact, High Effort)

A custom CUDA kernel for epsilon's frame loop would eliminate all Python overhead and enable hardware-level parallelism across the batch dimension. This is the highest-impact optimization but requires significant implementation effort.

---

## 6. Summary

| Property | Value |
|----------|-------|
| Total groups | 8 |
| Stateful groups | 1 (epsilon) |
| Learned parameters | 0 |
| Compute bottleneck | epsilon (frame loop) |
| Memory bottleneck | None (all allocations are negligible) |
| Epsilon state per batch | ~592 bytes |
| Peak output memory | 2 x B x T x 104 x 4 bytes |
| Scaling | Linear in T (from epsilon); constant for all others |

---

## 7. Cross-References

| Related Document | Path |
|-----------------|------|
| Dependency DAG | [DependencyDAG.md](DependencyDAG.md) |
| Execution model | [ExecutionModel.md](ExecutionModel.md) |
| State management | [StateManagement.md](StateManagement.md) |
| Epsilon group spec | [../Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md) |
| Epsilon state contract | [../Contracts/EpsilonStateContract.md](../Contracts/EpsilonStateContract.md) |
| Orchestrator code | `mi_beta/language/groups/__init__.py` |
| Epsilon code | `mi_beta/language/groups/epsilon.py` |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
