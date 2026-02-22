# ASAP — Temporal Integration

**Model**: Action Simulation for Auditory Prediction
**Unit**: MPU-β1
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | prediction_accuracy | Temporal prediction error (inverse). prediction_accuracy = f10. How accurately the motor simulation predicts upcoming beat timing. Higher values indicate the motor system has locked onto the rhythmic pattern with low prediction error. Grahn & Brett 2007: beat-inducing rhythms activate putamen + SMA (F(2,38)=20.67, p<.001). Range [0, 1]. |
| 4 | simulation_strength | Motor simulation amplitude. simulation_strength = f11. The vigor of the ongoing motor simulation process. Reflects how strongly the motor system is engaged in generating temporal predictions. Barchet et al. 2024: finger-tapping optimal at ~2 Hz (β=0.31 for perception prediction). Range [0, 1]. |
| 5 | coupling_index | Bidirectional motor-auditory coupling strength. coupling_index = σ(0.5 * f11 + 0.5 * f12). Integrates simulation strength with dorsal pathway activity to produce an overall coupling measure. This reflects the tightness of the motor-auditory loop: strong simulation with active dorsal pathway yields high coupling. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 4 | M8 (velocity) | L0 (fwd) | Tempo velocity 125ms — rate of tempo change |
| 1 | 21 | 16 | M1 (mean) | L0 (fwd) | Mean tempo change 1s — sustained tempo dynamics |
| 2 | 25 | 16 | M14 (periodicity) | L0 (fwd) | Coupling periodicity 1s — sustained coupling regularity |

---

## Computation

The M-layer derives three mathematical quantities from E-layer features, transforming explicit features into integrated measures of the action simulation system.

**prediction_accuracy** directly inherits from f10 (beat_prediction). The rationale is that beat prediction strength IS prediction accuracy — when the motor system successfully predicts upcoming beats, the periodicity signals are strong, yielding high f10.

**simulation_strength** directly inherits from f11 (motor_simulation). The ongoing simulation amplitude at fast timescales directly reflects how vigorously the motor system is generating temporal predictions.

**coupling_index** combines f11 and f12 through sigmoid with equal weights. This produces a joint measure of how tightly the motor and auditory systems are coupled: both simulation strength (f11) and dorsal pathway activity (f12) must be high for strong coupling. The equal weighting reflects the bidirectional nature — motor-to-auditory and auditory-to-motor contribute equally.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f10 | Beat prediction signal | Prediction accuracy derives from beat prediction strength |
| E-layer f11 | Motor simulation signal | Simulation strength is the direct motor engagement measure |
| E-layer f12 | Dorsal stream signal | Coupling requires active dorsal pathway |
| R³[21] spectral_change | Tempo dynamics | Rate of tempo change modulates coupling demands |
| R³[25] x_l0l5[0] | Motor-auditory coupling | Sustained coupling periodicity at 1s |
| H³ (3 tuples) | Temporal dynamics | Tempo velocity (125ms) and sustained integration (1s) |
