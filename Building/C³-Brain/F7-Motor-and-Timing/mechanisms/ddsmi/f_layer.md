# DDSMI — Forecast

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU-β2
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | coordination_pred | Social coordination prediction. coordination_pred = σ(0.5 * f13 + 0.5 * social_period_1s). Predicts near-future social coordination quality. Combines current social tracking (f13) with sustained social periodicity. When both are high, the dyadic dance coordination is predicted to continue successfully. Sabharwal et al. 2024: Granger causality directional coupling predicts leader/follower dynamics. Range [0, 1]. |
| 9 | music_pred | Music tracking prediction. music_pred = σ(0.5 * f14 + 0.5 * music_period_1s). Predicts near-future music tracking strength. Combines current music tracking (f14) with sustained music coupling periodicity. Regular rhythmic patterns with strong current tracking predict continued auditory entrainment. Range [0, 1]. |
| 10 | social_pred | Social process prediction. Predicts the overall social processing state including both direct partner coordination and the visual modulation effect. Integrates f13 (social coordination) with f15 (visual modulation) to forecast whether social processing will dominate in the near future. Yoneta et al. 2022: leader/follower roles modulate inter-brain coupling dynamics in cooperative music. Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands. It reuses tuples from E-layer:
- social_period_1s: H³ tuple (33, 16, M14, L2) from E-layer
- music_period_1s: H³ tuple (25, 16, M14, L2) from E-layer

---

## Computation

The F-layer generates three forward-looking predictions about the state of the dyadic dance system.

**coordination_pred** predicts social coordination quality. It averages the current social coordination state (f13) with the sustained social periodicity (1s timescale). The logic is that interpersonal coordination is predicted by both the current state of partner tracking and the regularity of the social coupling signal — consistent, periodic social coupling predicts continued coordination.

**music_pred** predicts music tracking strength. It averages the current music tracking state (f14) with the sustained music coupling periodicity. Highly periodic music with strong current entrainment predicts continued auditory tracking. This prediction is important because it interacts with the resource competition: if music_pred is strong but coordination_pred is also strong, the system faces a resource allocation challenge.

**social_pred** predicts the overall social processing dominance. It integrates social coordination (f13) with visual modulation (f15), forecasting whether the system will be in a socially-dominant or musically-dominant processing state. When both social coordination is strong and visual modulation indicates resource shift toward social processing, the system predicts continued social dominance.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f13 | Social coordination state | Current social tracking anchors coordination forecast |
| E-layer f14 | Music tracking state | Current music tracking anchors music forecast |
| E-layer f15 | Visual modulation | Resource shift status anchors social dominance forecast |
| H³ (33, 16, M14, L2) | Social period 1s | Sustained social regularity for coordination prediction |
| H³ (25, 16, M14, L2) | Music period 1s | Sustained music regularity for music prediction |
| Downstream: PEOM | Dance tempo entrainment | Music predictions feed PEOM for tempo locking |
| Downstream: VRMSME | Multi-modal coordination | Social coordination predictions feed VR integration |
