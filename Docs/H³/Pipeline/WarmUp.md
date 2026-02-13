# H3 Warm-Up Behavior

> Version 2.0.0 | Updated 2026-02-13

## 1. Problem Statement

Temporal morphs require a context window of `n_frames` to produce fully meaningful values. At the boundaries of a sequence, the attention window is only partially filled. This partially-filled region is the **warm-up zone**.

During warm-up, morph values are valid (not NaN or garbage) but are based on shorter-than-nominal windows, making them less reliable representations of the temporal pattern they are designed to capture.

---

## 2. Per-Law Warm-Up Patterns

The location of the warm-up zone depends on the causal direction (law):

| Law | Name | Warm-Up Location | Affected Region |
|-----|------|------------------|-----------------|
| L0 | Memory | Start of sequence | First `n_frames` frames have incomplete past context |
| L1 | Prediction | End of sequence | Last `n_frames` frames have incomplete future context |
| L2 | Integration | Both boundaries | First and last `n_frames // 2` frames have incomplete context |

### L0 (Memory) -- Past Context

```
Sequence:  [===========================================================]
Warm-up:   [####]
Full:            [=====================================================]

Frame 0: window contains only 1 frame (self)
Frame 1: window contains 2 frames
...
Frame n_frames-1: first frame with full window
```

The morph at frame 0 is computed from a single value. At frame `n_frames - 1`, the window is fully populated for the first time.

### L1 (Prediction) -- Future Context

```
Sequence:  [===========================================================]
Warm-up:                                                          [####]
Full:      [=====================================================]

Frame T-1: window contains only 1 frame (self)
Frame T-2: window contains 2 frames
...
Frame T-n_frames: last frame with full window
```

This is the mirror of L0. Output degrades toward the end of the sequence.

### L2 (Integration) -- Bidirectional

```
Sequence:  [===========================================================]
Warm-up:   [##]                                                    [##]
Full:          [===================================================]

Frame 0: half-window missing on the left
Frame T-1: half-window missing on the right
```

Both boundaries are affected, but each warm-up zone is half the size of L0 or L1.

---

## 3. Warm-Up Duration by Band

| Band | Horizons | n_frames Range | Warm-Up Duration | Musical Context |
|------|----------|----------------|------------------|-----------------|
| Micro | H0--H7 | 1--43 frames | 5.8--250 ms | Onset, attack, transient |
| Meso | H8--H15 | 52--138 frames | 300--800 ms | Beat period, quarter note |
| Macro | H16--H23 | 172--4,307 frames | 1--25 s | Measure, section, passage |
| Ultra | H24--H31 | 6,202--168,999 frames | 36 s--16 min | Movement, full work |

### Warm-Up as Fraction of Typical Audio

| Band | Warm-Up (max) | 10s Clip | 30s Clip | 3 min Song | 10 min Work |
|------|---------------|----------|----------|------------|-------------|
| Micro | 250 ms | 2.5% | 0.8% | 0.1% | <0.1% |
| Meso | 800 ms | 8.0% | 2.7% | 0.4% | 0.1% |
| Macro | 25 s | 100%* | 83%* | 14% | 4.2% |
| Ultra | 16 min | 100%* | 100%* | 100%* | 100%* |

(*) Warm-up exceeds sequence length -- the horizon never fully warms.

---

## 4. Warm-Up Handling in Code

### 4.1 Initialization

`H3Extractor._compute_morph_series()` initializes the output tensor with zeros:

```python
result = torch.zeros(B, T)
```

Frames within the warm-up zone that have empty or too-short windows default to zero or are computed from whatever context is available.

### 4.2 Attention Weight Normalization

When the window extends beyond sequence boundaries, it is truncated. The attention weights are truncated to match and then re-normalized:

```python
w = weights[:actual_window_size]
w = w / w.sum()  # re-normalize to sum=1
```

This means warm-up frames receive valid morph values, but the effective attention profile is compressed. A morph nominally spanning 100 frames of context might be computed from only 10 frames during early warm-up, causing it to behave more like a shorter-horizon morph.

### 4.3 No Explicit Warm-Up Flag

The current implementation does not emit a per-frame warm-up flag or confidence score. Consumers (C3 models) must be aware of warm-up effects based on the horizons they demand.

---

## 5. Musical Implications

### 5.1 Onset Region (First Few Seconds)

The first few seconds of any audio analysis are the most affected:

- **Beat tracking** (BEP at H6, H9, H11): Reliable after ~800 ms. The first beat in a piece may be poorly characterized, but steady-state beat tracking is unaffected.
- **Pitch tracking** (PPC at H0, H3, H6): Reliable within 250 ms. Micro-band warm-up is negligible for most use cases.
- **Onset detection** (ASA at H3, H6, H9): Reliable after ~300 ms. The very first onset in a piece has less context.

### 5.2 Section-Level Analysis

- **Section boundaries** (TMH at H16, H18, H20, H22): The longest horizon (H22, 2,456 frames = 14.3 s) means section-level analysis does not stabilize until ~15 s into the piece.
- **Memory processes** (MEM at H18, H20, H22, H25): H25 at 8,902 frames = 51.7 s. Full-piece memory analysis requires >1 minute of audio.

### 5.3 Full-Work Analysis

- **Ultra-band features** (H24--H31): These are meaningful only for long-form audio. A 3-minute pop song never fully warms an H25 demand (51.7 s warm-up out of 180 s), and H28+ horizons (>5 min warm-up) are effectively meaningless for anything shorter than an orchestral movement.

---

## 6. Recommendations for C3 Model Consumers

### 6.1 Ignore Early Output for Critical Decisions

For models that make discrete decisions (onset detection, beat marking, section segmentation), the first `n_frames` of H3 output for the relevant horizons should be excluded or down-weighted:

```python
# Example: ignore first n_frames for a Macro-band demand
confidence_mask = torch.ones(T)
confidence_mask[:n_frames] = 0.0  # or a ramp from 0 to 1
output = model_output * confidence_mask
```

### 6.2 Weight Early Outputs Lower in Training

For models trained with gradient descent, the loss function can incorporate a warm-up mask:

```python
# Ramp from 0 to 1 over the warm-up zone
warmup_weight = torch.clamp(torch.arange(T).float() / n_frames, 0.0, 1.0)
loss = (prediction - target) ** 2 * warmup_weight
```

This prevents the model from learning to fit the degraded warm-up values.

### 6.3 Ultra-Band Demands: Long-Form Only

Models that demand Ultra-band horizons (H24--H31) should only be applied to audio longer than 2 minutes. For shorter clips:

- Ultra-band morph values will be based on severely truncated windows
- The values are technically valid but do not represent the temporal scale they are designed for
- A model demanding H25 (51.7 s) on a 30 s clip will never receive a morph computed from more than 58% of the nominal window

### 6.4 Per-Mechanism Warm-Up Summary

| Mechanism | Max Horizon | Warm-Up Time | Recommendation |
|-----------|-------------|-------------|----------------|
| PPC | H6 (37 frames) | 215 ms | Negligible for most audio |
| ASA | H9 (62 frames) | 360 ms | Safe to ignore for clips >2 s |
| BEP | H11 (114 frames) | 662 ms | First beat may be unreliable |
| TPC | H16 (172 frames) | 1.0 s | Mask first 1 s for tonal analysis |
| AED | H16 (172 frames) | 1.0 s | Same as TPC |
| SYN | H18 (517 frames) | 3.0 s | Mask first 3 s |
| CPD | H18 (517 frames) | 3.0 s | Same as SYN |
| C0P | H20 (1,400 frames) | 8.1 s | Mask first 8 s |
| TMH | H22 (2,456 frames) | 14.3 s | Mask first 15 s |
| MEM | H25 (8,902 frames) | 51.7 s | Long-form audio only (>2 min) |

---

## 7. Code References

| Component | File | Key Element |
|-----------|------|-------------|
| Morph series loop | `mi_beta/ear/h3/__init__.py` | `H3Extractor._compute_morph_series()` |
| Weight normalization | `mi_beta/ear/h3/attention.py` | `compute_attention_weights()` |
| Horizon frame counts | `mi_beta/ear/h3/horizon.py` | `EventHorizon.n_frames` |

---

## 8. Cross-References

- [ExecutionModel.md](ExecutionModel.md) -- How windows are selected and attention weights applied (Phases 4--5)
- [Performance.md](Performance.md) -- Warm-up zones have lower computational cost (shorter effective windows)
- [SparsityStrategy.md](SparsityStrategy.md) -- Warm-up is orthogonal to sparsity; all demanded tuples experience it
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Design rationale for the 32 horizon values
- [H3-HORIZON-TABLE.md](../H3-HORIZON-TABLE.md) -- Complete table of horizon frame counts and durations
