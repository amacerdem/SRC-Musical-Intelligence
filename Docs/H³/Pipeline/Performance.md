# H3 Performance Characteristics

> Version 2.0.0 | Updated 2026-02-13

## 1. Per-Horizon Cost Model

The dominant computational cost in H3 is the morph computation loop. For a single horizon `h` with frame count `n_frames`:

### 1.1 Attention Weights

```
Cost: O(n_frames)
Frequency: once per horizon
```

Computed via `torch.linspace` + `torch.exp`. This is a one-time setup cost per horizon and is negligible relative to the morph loop.

### 1.2 Window Selection

```
Cost: O(1) per frame per tuple
```

Window boundaries are determined by the law (L0/L1/L2) and the current frame index. This is a simple index calculation.

### 1.3 Morph Computation

```
Cost: O(n_frames) per frame per tuple
```

Most of the 24 morph functions are linear in window size: weighted mean, weighted variance, weighted slope, etc. A few morphs (e.g., peak count, zero-crossing rate) involve additional operations but remain O(n_frames).

### 1.4 Total Per-Horizon Cost

```
Cost_h = T * |tuples_at_h| * O(n_frames_h)
```

where:
- `T` = total frames in the sequence
- `|tuples_at_h|` = number of unique (r3_idx, morph, law) tuples demanded at horizon `h`
- `n_frames_h` = window size for horizon `h`

---

## 2. Cost by Band

The four temporal bands have vastly different cost profiles:

| Band | Horizons | n_frames Range | Typical Tuples | Relative Cost | Character |
|------|----------|----------------|----------------|---------------|-----------|
| Micro | H0--H7 | 1--43 | ~3,500 | Low | Small windows, many tuples |
| Meso | H8--H15 | 52--138 | ~2,000 | Moderate | Medium windows, medium tuples |
| Macro | H16--H23 | 172--4,307 | ~2,600 | High | Large windows, moderate tuples |
| Ultra | H24--H31 | 6,202--168,999 | ~500 | Very High | Huge windows, few tuples |

### Cost Breakdown Example (T = 17,227 frames, 100s audio)

| Band | Approx. FLOPs per Frame | Approx. Total FLOPs | % of Total |
|------|------------------------|---------------------|------------|
| Micro | 3,500 * 22 = 77K | 1.33G | ~3% |
| Meso | 2,000 * 95 = 190K | 3.27G | ~8% |
| Macro | 2,600 * 2,240 = 5.8M | 100G | ~40% |
| Ultra | 500 * 87,600 = 43.8M | 754G | ~49% (but sparse in time) |

Note: Ultra-band costs are theoretical maximums. In practice, Ultra horizons with n_frames > T contribute proportionally less because the window cannot exceed the sequence length.

---

## 3. Mechanism Cost Profiles

Each of the 10 mechanisms operates at specific horizons, giving each a distinct cost profile:

| Mechanism | Horizons | Band(s) | Cost Character |
|-----------|----------|---------|----------------|
| PPC | H0, H3, H6 | Micro | Cheapest. Small windows, fast iteration. |
| ASA | H3, H6, H9 | Micro--Meso | Low. Crosses into Meso at H9. |
| BEP | H6, H9, H11 | Micro--Meso | Low--Moderate. H11 at 114 frames. |
| TPC | H6, H12, H16 | Cross-band | Moderate. H16 at 172 frames adds cost. |
| SYN | H12, H16, H18 | Meso--Macro | Moderate--High. H18 at 517 frames. |
| AED | H6, H16 | Micro+Macro | Bimodal. H6 is cheap, H16 is moderate. |
| CPD | H9, H16, H18 | Meso--Macro | Moderate--High. Similar to SYN. |
| C0P | H18, H19, H20 | Macro | High. All three horizons >500 frames. |
| TMH | H16, H18, H20, H22 | Macro | High. H22 at 2,456 frames. |
| MEM | H18, H20, H22, H25 | Macro--Ultra | Highest. H25 at 8,902 frames. |

---

## 4. GPU Strategy

### 4.1 Current Implementation

All H3 operations use PyTorch tensors and are GPU-compatible:

| Operation | Implementation | GPU Status |
|-----------|---------------|------------|
| R3 feature indexing | `tensor[:, :, r3_idx]` | Native |
| Attention weights | `torch.exp`, `torch.linspace` | Native |
| Window extraction | Tensor slicing | Native |
| Morph computation | Torch arithmetic ops | Native |
| Result storage | Python dict of tensors | Tensors on GPU, dict on CPU |

### 4.2 Current Bottleneck

The primary bottleneck is the **Python loop over time frames** (`t` in `range(T)`) within `_compute_morph_series`. Each iteration:

1. Computes window boundaries
2. Extracts a window slice from the R3 tensor
3. Applies attention weights
4. Calls the morph function
5. Stores the result

This loop runs `T` times per tuple, and Python loop overhead dominates for small windows (Micro band) where the per-iteration torch computation is minimal.

### 4.3 Future Optimization: Batched Unfold

The time-frame loop can be eliminated using `torch.Tensor.unfold()`:

```python
# Current: loop over T frames
for t in range(T):
    window = r3_feature[t - n_frames + 1 : t + 1]  # (B, n_frames)
    result[t] = morph_fn(window, weights)

# Future: batch all frames at once
windows = r3_feature.unfold(dim=1, size=n_frames, step=1)  # (B, T-n+1, n_frames)
results = morph_fn_batched(windows, weights)                 # (B, T-n+1)
```

This would move the entire inner loop to GPU, providing substantial speedup especially for Micro and Meso bands where the Python overhead is the dominant cost.

### 4.4 Additional GPU Optimizations

| Optimization | Benefit | Complexity |
|-------------|---------|------------|
| Unfold-based batching | Eliminate Python time loop | Medium |
| Fused attention + morph kernels | Reduce memory bandwidth | High |
| Pre-sorted demand by r3_idx | Better cache locality on R3 tensor | Low |
| Shared memory for attention weights | Reduce redundant GPU transfers | Low |

---

## 5. Memory Footprint

### 5.1 Per-Frame Memory

| Component | Size (B=1) | Notes |
|-----------|------------|-------|
| R3 input | 128 * 4 = 512 bytes | Input tensor, one frame |
| H3 output (sparse) | ~8,600 * 4 = ~33.6 KB | All demanded tuples, one frame |
| Attention weights (all horizons) | SUM(n_frames_h) * 4 = ~760 KB | Cached, not per-frame |
| Working memory (largest window) | 128 * 4 = 512 bytes | One window at a time |

### 5.2 Total Memory by Sequence Length

| Duration | Frames (T) | R3 Input | H3 Output | Attention Cache | Total |
|----------|------------|----------|-----------|-----------------|-------|
| 10s | 1,723 | 0.84 MB | 56.6 MB | 0.76 MB | ~58 MB |
| 30s | 5,168 | 2.52 MB | 169.8 MB | 0.76 MB | ~173 MB |
| 100s | 17,227 | 8.39 MB | 566 MB | 0.76 MB | ~575 MB |
| 300s | 51,681 | 25.2 MB | 1.70 GB | 0.76 MB | ~1.73 GB |

All values are for B=1. Multiply by batch size for larger batches.

### 5.3 Peak Memory

Peak memory occurs during morph computation of the largest demanded window. For Ultra-band horizons, the window tensor can be large:

```
Peak window: (B, n_frames_max) = (B, 168999) for H31
           = 168,999 * 4 bytes = ~660 KB per batch element
```

This is manageable because only one window is materialized at a time.

---

## 6. Batching Considerations

The batch dimension `B` is free in all morph operations: every torch operation (mean, var, matmul, etc.) broadcasts naturally over the batch dimension. No special handling is needed.

| Property | Value |
|----------|-------|
| Batch overhead | O(1) -- no additional loops |
| Memory scaling | Linear in B |
| GPU utilization | Improves with larger B (more parallelism) |
| Recommended B | 8--32 (limited by H3 output memory) |

For B=32 with T=17,227 frames:

```
H3 output memory = 32 * 8,600 * 17,227 * 4 bytes = ~18.1 GB
```

This is the primary memory constraint for large batches.

---

## 7. Profiling Guidance

When profiling H3 performance, focus on:

1. **Time per horizon**: Identifies which horizons dominate runtime
2. **Time per band**: Macro and Ultra bands should dominate
3. **Python loop overhead**: Compare wall time to torch-only time to estimate loop overhead
4. **Memory peak**: Monitor during Ultra-band computation
5. **GPU utilization**: Should be high during Macro/Ultra computation, potentially low during Micro (Python loop bound)

---

## 8. Code References

| Component | File | Key Function |
|-----------|------|--------------|
| Main loop | `mi_beta/ear/h3/__init__.py` | `H3Extractor._compute_morph_series()` |
| Attention | `mi_beta/ear/h3/attention.py` | `compute_attention_weights()` |
| Morph functions | `mi_beta/ear/h3/morph.py` | `MorphComputer.compute()` |
| Horizon params | `mi_beta/ear/h3/horizon.py` | `EventHorizon.n_frames` |

---

## 9. Cross-References

- [ExecutionModel.md](ExecutionModel.md) -- Full execution flow and pseudocode
- [SparsityStrategy.md](SparsityStrategy.md) -- How sparsity reduces the workload by 34x
- [WarmUp.md](WarmUp.md) -- Performance implications of warm-up (shorter effective windows at boundaries)
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Design rationale for horizon frame counts
