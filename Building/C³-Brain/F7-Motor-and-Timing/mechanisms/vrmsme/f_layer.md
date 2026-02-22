# VRMSME — Forecast

**Model**: VR Music Stimulation Motor Enhancement
**Unit**: MPU-β3
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | enhancement_pred | Motor enhancement prediction. enhancement_pred = σ(0.5 * f16 + 0.5 * coupling_period_1s). Predicts near-future motor enhancement strength. Combines current music enhancement (f16) with sustained multi-modal coupling periodicity. Periodic auditory-motor coupling with strong current enhancement predicts continued VRMS advantage. Blasi et al. 2025: music/dance interventions produce structural + functional neuroplasticity (20 RCTs, N=718). Range [0, 1]. |
| 9 | connectivity_pred | Network connectivity prediction. connectivity_pred = σ(0.5 * f18 + 0.5 * sensorimotor_period_1s). Predicts near-future PM-DLPFC-M1 network connectivity. Combines current network connectivity (f18) with sustained sensorimotor binding periodicity. Strong current connectivity with regular sensorimotor binding predicts maintained network activation. Range [0, 1]. |
| 10 | bilateral_pred | Bilateral activation prediction. Predicts near-future bilateral sensorimotor activation balance. Integrates f17 (bilateral_activation) with sensorimotor binding stability to forecast whether bilateral M1 engagement will persist. Sustained bilateral activation depends on continued VR music stimulation input. Sarasso et al. 2019: appreciated musical intervals enhance N1/P2 and modulate bilateral motor cortex. Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands. It reuses tuples from E-layer:
- coupling_period_1s: H³ tuple (25, 16, M14, L2) from E-layer
- sensorimotor_period_1s: H³ tuple (33, 16, M14, L2) from E-layer

---

## Computation

The F-layer generates three forward-looking predictions about the state of the VR music stimulation system.

**enhancement_pred** predicts motor enhancement continuation. It averages the current music enhancement (f16) with the sustained coupling periodicity (1s timescale). The logic is that VRMS advantage is predicted by both the current enhancement state and the regularity of the underlying multi-modal coupling: periodic, sustained coupling with strong current enhancement predicts continued motor facilitation.

**connectivity_pred** predicts network connectivity maintenance. It averages the current network connectivity (f18) with the sustained sensorimotor binding periodicity. Strong PM-DLPFC-M1 connectivity with regular sensorimotor binding predicts continued network activation. This is clinically relevant: sustained network connectivity is the mechanism by which VRMS may produce lasting motor rehabilitation effects.

**bilateral_pred** predicts bilateral activation persistence. It integrates bilateral activation (f17) with sensorimotor binding stability, forecasting whether the bilateral M1 engagement that distinguishes VRMS will continue. This prediction is important because bilateral activation is the key differential feature versus VRMI (motor imagery produces less bilateral activation).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f16 | Music enhancement state | Current enhancement anchors motor facilitation forecast |
| E-layer f17 | Bilateral activation state | Current bilateral engagement anchors persistence forecast |
| E-layer f18 | Network connectivity state | Current connectivity anchors network maintenance forecast |
| H³ (25, 16, M14, L2) | Coupling period 1s | Sustained coupling regularity for enhancement prediction |
| H³ (33, 16, M14, L2) | Sensorimotor period 1s | Sustained binding regularity for connectivity prediction |
| Downstream: SPMC | Enhanced motor circuit | Enhancement predictions feed motor circuit planning |
| Downstream: DDSMI | Bilateral for social motor | Bilateral predictions feed social motor integration |
