# ASAP — Cognitive Present

**Model**: Action Simulation for Auditory Prediction
**Unit**: MPU-β1
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | motor_to_auditory | Motor-to-auditory prediction signal (forward model). The beat-entrainment-driven motor prediction flowing from SMA/premotor to auditory cortex via dorsal pathway. Represents the "when" signal: the motor system's current temporal prediction being sent to auditory areas. Patel & Iversen 2014: motor system generates forward temporal prediction through parietal cortex. Range [0, 1]. |
| 7 | auditory_to_motor | Auditory-to-motor update signal (inverse model). The temporal-context-driven error correction flowing from auditory cortex back to motor areas. Represents the phase adjustment: auditory onset information correcting the motor simulation's timing estimate. Ross & Balasubramaniam 2022: bidirectional coupling — auditory input updates motor simulation. Range [0, 1]. |
| 8 | dorsal_activity | Dorsal pathway activation level. dorsal_activity = f12. The current activation of the posterior parietal cortex dorsal auditory pathway hub that mediates bidirectional motor-auditory coupling. Ross et al. 2018: cTBS to parietal cortex causally disrupts beat timing (double dissociation with cerebellum for interval timing). Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands beyond E-layer and M-layer tuples. All computation derives from upstream layer features.

---

## Computation

The P-layer represents the current-moment state of the bidirectional motor-auditory coupling system.

**motor_to_auditory** is the forward model signal — the motor system's temporal prediction flowing toward auditory cortex. This is computed from the interaction of prediction accuracy (M-layer) with simulation strength, representing the current "when" prediction being broadcast. In the ASAP framework, this is the core mechanism: the motor system actively predicts upcoming onsets and sends this prediction to auditory areas.

**auditory_to_motor** is the inverse model signal — auditory onset information flowing back to correct the motor simulation. This is computed from the difference between actual and predicted onset timing, modulated by coupling strength. When prediction error is low, this signal is weak (the motor simulation is accurate); when prediction error is high, this signal drives phase adjustment.

**dorsal_activity** directly inherits from f12 (dorsal_stream). It represents the current activation level of the posterior parietal cortex, which serves as the hub for bidirectional motor-auditory information flow. This is the anatomical substrate that the ASAP model posits as essential for beat perception.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f10, f11 | Beat prediction, motor simulation | Forward model derives from prediction and simulation |
| E-layer f12 | Dorsal stream | Dorsal activity is the pathway hub |
| M-layer prediction_accuracy | Prediction quality | Error correction depends on prediction accuracy |
| M-layer coupling_index | Coupling strength | Modulates both directional signals |
