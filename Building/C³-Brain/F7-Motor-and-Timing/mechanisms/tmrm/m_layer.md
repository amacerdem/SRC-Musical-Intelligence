# TMRM — Temporal Integration

**Model**: Tempo Memory Reproduction Method
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | method_dissociation | Adjusting − tapping pathway difference. Sensory vs motor pathway dominance index. High values indicate sensory pathway (adjusting) dominates; low values indicate motor pathway (tapping) dominates. Vigl 2024: method × expertise interaction r=.04, p=.001 — expertise advantage is stronger for tapping. Formula: σ(f01 − motor_state). |
| 4 | tempo_deviation | Distance from optimal 120 BPM. Inverted f02 signal: 0 = at 120 BPM optimum, 1 = far from optimal tempo zone. Vigl 2024: quadratic peak at 120–125 BPM (χ²(1)=152.57). Foster 2021: DJs 120-139 BPM error 3.10% vs untrained 7.91%. Formula: 1 − f02. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 11 | M15 (smoothness) | L0 | Smoothness of beat pattern |
| 1 | 22 | 11 | M8 (velocity) | L0 | Rhythmic energy dynamics |
| 2 | 22 | 11 | M14 (periodicity) | L0 | Energy periodicity |
| 3 | 7 | 11 | M4 (max) | L0 | Peak amplitude at tempo scale |
| 4 | 9 | 11 | M1 (mean) | L0 | Mean brightness at meter level |

---

## Computation

The M-layer integrates E-layer signals into unified tempo memory metrics:

1. **Method dissociation** (idx 3): Difference between sensory and motor pathway activation. When f01 (adjusting advantage) exceeds motor_state, the sensory pathway dominates — consistent with the d=2.76 advantage. The motor_state is computed from amplitude max × energy velocity at H11 (500ms).

2. **Tempo deviation** (idx 4): Simple inversion of optimal tempo signal (1 − f02). Provides a "distance from 120 BPM" metric that tracks how far current tempo is from the psychophysically optimal zone. High deviation reduces reproduction accuracy.

Both outputs are bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02 | Adjusting advantage and optimal tempo |
| P-layer | motor_state | Motor pathway activation for dissociation |
| R³ [7] | amplitude | Peak intensity at tempo scale |
| R³ [8] | loudness | Smoothness of beat pattern |
| R³ [22] | energy_change | Velocity and periodicity for tempo dynamics |
| H³ | 5 tuples (see above) | Motor-level features at H11 (500ms) |
