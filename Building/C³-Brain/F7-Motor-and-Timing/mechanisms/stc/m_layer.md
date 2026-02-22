# STC — Temporal Integration

**Model**: Singing Training Connectivity
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | connectivity_strength | Insula-sensorimotor connectivity strength over time. Integrates interoceptive coupling (f28) with the raw interoceptive periodicity signal to produce a temporally smoothed connectivity estimate. connectivity_strength = sigma(0.5 * f28 + 0.5 * interoceptive_period_1s). Zamorano 2023: accumulated singing training predicts enhanced resting-state connectivity between insula and speech/respiratory sensorimotor areas. |
| 4 | respiratory_index | Respiratory control quality index. Directly propagates f29 (respiratory integration) as the temporal respiratory control estimate, providing a smoothed breath-phrase coupling metric over time. Zarate 2008: ACC + pSTS + anterior insula network for compensatory vocal control. respiratory_index = f29. |
| 5 | voice_body_coupling | Voice-body integration index. Combines interoceptive coupling (f28) with speech sensorimotor activation (f30) to estimate the overall voice-body integration quality. voice_body_coupling = sigma(0.5 * f28 + 0.5 * f30). Kleber 2013: right AIC connectivity with M1, S1, auditory cortex reflects integrated vocal sensorimotor control. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 8 | M1 (mean) | L2 (bidi) | Mean vocal intensity 500ms |

---

## Computation

The M-layer performs temporal integration of the E-layer features to derive time-evolving estimates of singing training connectivity. It bridges the instantaneous interoceptive-motor extractions with the slower plasticity dynamics that characterize training-induced connectivity changes.

1. **connectivity_strength**: Averages interoceptive coupling (f28) with the raw interoceptive periodicity signal at 1s. This dual integration ensures the connectivity estimate reflects both the processed coupling state and the underlying interoceptive rhythm. Zamorano 2023's resting-state fMRI finding that training predicts connectivity is the primary motivation for this temporally integrated metric.

2. **respiratory_index**: Directly propagates f29 as the respiratory control quality. The M-layer treats respiratory integration as already temporally integrated by the E-layer's combination of slow periodicity (1s) and fast entropy (100ms), so no additional temporal processing is applied. This preserves the natural respiratory rhythm dynamics.

3. **voice_body_coupling**: Averages interoceptive coupling (f28) with speech sensorimotor activation (f30) to capture the holistic voice-body integration. This reflects Kleber 2013's finding that the right anterior insula is connected to both somatosensory (S1) and motor (M1) cortex during vocal production, forming an integrated sensorimotor loop.

The single additional H3 tuple (amplitude mean at 500ms) provides the vocal intensity baseline for temporal integration. All other temporal information is inherited from the E-layer.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f28 | Interoceptive coupling | Primary input for connectivity_strength and voice_body_coupling |
| E-layer f29 | Respiratory integration | Direct propagation as respiratory_index |
| E-layer f30 | Speech sensorimotor | Input for voice_body_coupling computation |
| H3 (33, 16, M14, L2) | Interoceptive period 1s | Shared with E-layer for connectivity_strength |
| R3[7] amplitude | Vocal intensity | Mean vocal intensity at 500ms for temporal baseline |
| H3 (1 tuple) | Amplitude temporal morphology | Mean vocal intensity at 500ms |
