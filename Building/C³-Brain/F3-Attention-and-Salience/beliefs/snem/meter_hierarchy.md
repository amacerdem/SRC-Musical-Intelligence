# meter_hierarchy — Core Belief (SNEM)

**Category**: Core (full Bayesian PE)
**τ**: 0.4
**Owner**: SNEM (ASU-α1)
**Multi-Scale**: 4 horizons, T_char = 1s

---

## Definition

"Beats grouped in metric structure." Tracks the hierarchical organization of beats into bars and phrases. High values indicate clear metric structure perception (e.g., strong-weak-weak in 3/4 time).

---

## Multi-Scale Horizons

```
H10(400ms)  H13(600ms)  H16(1s)  H18(2s)
```

T_char = 1s reflects bar-level organization. H10 captures beat-to-beat grouping; H13–H16 capture bar structure; H18 captures multi-bar phrasing. Longer timescales than beat_entrainment because meter emerges from beat grouping.

---

## Observation Formula

```
# Meter observation from SNEM E-layer + P-layer:
meter_obs = 0.40 × SNEM.meter_entrainment[E1]
          + 0.35 × SNEM.entrainment_strength[P1]
          + 0.25 × SNEM.meter_position_pred[F1]

# Precision: from coupling periodicity stability
pi_obs = (0.5 × coupling_periodicity_1s + 0.5 × beat_salience) × 10
         clamped [0.5, 10]
```

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SNEM E1 | meter_entrainment [1] | SS-EP at meter frequency |
| SNEM P1 | entrainment_strength [7] | Phase-locking coupling |
| SNEM F1 | meter_position_pred [10] | Metric position prediction |
| SNEM M2 | beat_salience [5] | Gaussian beat salience |
| H³ | (25, 16, 14, 2) | Coupling periodicity at 1s |

---

## Scientific Foundation

- **Nozaradan 2012**: Metric hierarchy creates nested periodicities in SS-EPs (N=9)
- **Large & Palmer 2002**: Hierarchical oscillator models of meter perception
- **Aparicio-Terres et al. 2025**: 1.65 Hz > 2.85 Hz for entrainment strength
- **Saadatmehr et al.**: Premature neonates (32 wGA) show beat/meter prediction

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/beat_entrainment.py` (meter_hierarchy computed alongside beat_entrainment)
