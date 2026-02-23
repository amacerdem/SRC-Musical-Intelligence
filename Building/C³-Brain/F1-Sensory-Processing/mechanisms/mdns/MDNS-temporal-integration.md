# MDNS M-Layer — Temporal Integration (2D)

**Layer**: M (Memory/Temporal)
**Dimensions**: 2D (indices 4–5 of MDNS 12D output)
**Input**: H³ tuples + E-layer features
**Character**: Multi-scale temporal consolidation — TRF response and melodic contour

---

## Overview

The M-layer transforms E-layer snapshots into temporally grounded representations. Two outputs capture the TRF response strength (how well the neural signal tracks the melody) and the melodic contour slope (direction and speed of pitch change). Both rely on H³ temporal morphologies at the motif and motor coupling scales.

---

## M0: TRF Response (trf_response)

**Range**: [0, 1]
**Question answered**: "How strongly does the neural signal track the melody at this moment?"

### Formula

```python
beat_lock = H3[(25, 11, 14, 2)]   # x_l0l5 periodicity at H11 (500ms), bidi
dyn_couple = H3[(33, 11, 0, 2)]   # x_l4l5 value at H11, bidirectional
trf_response = σ(0.50 * beat_lock + 0.50 * dyn_couple)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 25 | x_l0l5[0] | 11 | M14 (periodicity) | L2 | 0.50 |
| 33 | x_l4l5[0] | 11 | M0 (value) | L2 | 0.50 |

### Logic

TRF response integrates two motor-coupling features at the 500ms horizon:
1. **Time-pitch coupling regularity** (x_l0l5 periodicity): How periodic the TRF basis function is — high regularity = strong neural tracking
2. **Dynamics-onset coupling** (x_l4l5 value): How well intensity dynamics couple with note onsets

Equal weighting reflects that both temporal and dynamic coupling contribute equally to TRF quality. Coefficient sum = 1.0.

---

## M1: Contour Slope (contour_slope)

**Range**: [0, 1]
**Question answered**: "What is the current melodic direction and speed of pitch change?"

### Formula

```python
pitch_vel = H3[(23, 8, 8, 0)]   # pitch_change velocity at H8 (300ms)
contour_slope = σ(pitch_vel)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 23 | pitch_change | 8 | M8 (velocity) | L0 | 1.0 |

### Logic

Direct sigmoid of pitch change velocity at the motif scale (300ms). High velocity = rapid pitch movement (ascending or descending runs). Low velocity = sustained notes or small intervals. This captures the melodic contour "shape" that is critical for TRF-based decoding — the rate of change drives neural tracking quality.

---

## Layer Summary

| Idx | Name | Range | Key H³ Scales | Purpose |
|-----|------|-------|---------------|---------|
| M0 | trf_response | [0, 1] | H11 (500ms) | TRF-based neural tracking strength |
| M1 | contour_slope | [0, 1] | H8 (300ms) | Melodic contour direction/speed |

**Total M-layer H³ tuples**: 3 (of MDNS's 18 total)
