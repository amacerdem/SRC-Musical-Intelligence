# meter_position_pred — Anticipation Belief (SNEM)

**Category**: Anticipation (prediction)
**Owner**: SNEM (ASU-α1)

---

## Definition

"Currently at position X in metric hierarchy." Predicts the listener's position within the metric structure (0=weak beat, 1=downbeat). Strong beats (downbeats) are predicted to be more salient.

---

## Observation Formula

```
# From SNEM F-layer:
meter_position_pred = SNEM.meter_position_pred[F1]  # index [10]

# Formula: sigma(0.5 * f02_meter + 0.5 * coupling_periodicity_1s)
# where f02_meter = SNEM E1:meter_entrainment
# coupling_periodicity_1s = H³ (25, 16, 14, 2)
```

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SNEM F1 | meter_position_pred [10] | Metric position prediction |
| SNEM E1 | meter_entrainment [1] | Meter-frequency entrainment |
| H³ | (25, 16, 14, 2) | Coupling periodicity at 1s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F4 Memory | Episodic boundary context — downbeats mark phrase boundaries |
| Salience mixer | Relay component: meter position contributes to salience weight |

---

## Scientific Foundation

- **Nozaradan 2012**: Metric hierarchy creates nested periodicities — bars group beats
- **Large & Palmer 2002**: Hierarchical oscillator models predict strong/weak positions
- **Aparicio-Terres et al. 2025**: 1.65 Hz > 2.85 Hz for optimal entrainment

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/snem_relay.py`
