# AMSC — Forecast

**Model**: Auditory-Motor Stream Coupling
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | motor_prediction | Predicted motor activation (110ms ahead). Extrapolates motor coupling from f02 motor gamma and groove trend at bar level (H16). Represents the dorsal stream's anticipatory motor engagement. Formula: σ(0.6 × f02 + 0.4 × groove_trend). |
| 10 | movement_timing | Beat-interval motor prediction. Combines meter state with bar-level periodicity from x_l4l5 coupling at H16. Predicts when the next motor synchronization event should occur. Maps to SMA/putamen beat-timing circuit (Hoddinott & Grahn 2024). |
| 11 | groove_response | Groove-driven motor engagement prediction. Combines amplitude smoothness, groove trend, and motor gamma at bar level. Predicts the degree to which the motor system will be engaged by upcoming musical content. Maps to the reward-motor pathway (ARU cross-unit). Formula: σ(0.5 × amp_smooth + 0.3 × groove_trend + 0.2 × f02). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 16 | M14 (periodicity) | L2 | x_l4l5 bar-level periodicity — movement timing |
| 1 | 33 | 16 | M18 (trend) | L0 | x_l4l5 dynamics trend — groove trajectory |
| 2 | 7 | 16 | M15 (smoothness) | L0 | Amplitude smoothness — groove quality |

---

## Computation

The F-layer generates predictions about upcoming auditory-motor coupling states:

1. **Motor prediction** (idx 9): Extrapolates motor activation from current motor gamma (f02) and dynamics trend at bar level. Positive trend + strong motor gamma = increasing motor engagement predicted. The 110ms delay means predictions target near-future motor state.

2. **Movement timing** (idx 10): Predicts next beat-interval motor event from meter state and bar-level periodicity. Strong periodicity at H16 (1s) enables confident prediction of upcoming beat timing. Maps to the continuous beat-strength representation in SMA/putamen.

3. **Groove response** (idx 11): Predicts motor system engagement level from amplitude smoothness, groove trajectory, and motor gamma. Smooth, trending intensity patterns with strong motor coupling predict high groove-driven motor engagement.

All outputs are sigmoid-bounded to [0, 1] and represent confidence in future motor states.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_motor_gamma | Current motor coupling for extrapolation |
| M-layer | coupling_strength | Pathway quality context |
| P-layer | motor_preparation | Current motor readiness |
| R³ [7] | amplitude | Smoothness for groove quality |
| R³ [33] | x_l4l5 | Bar-level periodicity and trend for timing |
| H³ | 3 tuples (see above) | Bar-level features at H16 (1000ms) |
