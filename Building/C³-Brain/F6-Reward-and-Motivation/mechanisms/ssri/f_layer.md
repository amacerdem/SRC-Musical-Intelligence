# SSRI — Forecast

**Model**: Social Synchrony Reward Integration
**Unit**: RPU-β4
**Function**: F6 Reward & Motivation
**Tier**: β (Bridging)
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | bonding_trajectory_pred | Predicted social bonding direction. bonding_traj_pred = σ(0.50 * f02 + 0.30 * coupling_trend_1s + 0.20 * loudness_trend_5s). Forecasts whether social bonding is strengthening or weakening based on current bonding state and long-range trend signals. High values predict continued or increasing social connection. tau_bonding = 120.0s. Range [0, 1]. |
| 10 | flow_sustain_pred | Predicted group flow sustainability. flow_sustain_pred = σ(0.40 * f03 + 0.30 * f04 + 0.30 * arousal). Forecasts whether the current group flow state can be maintained. Depends on both the current flow level and the entrainment precision that sustains it, modulated by arousal as an energetic resource. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M18 (trend) | L2 (bidi) | Coupling trend 1s — direction of consonance-energy interaction |
| 1 | 8 | 20 | M18 (trend) | L0 (fwd) | Loudness trend 5s LTI — long-range dynamic trajectory |

---

## Computation

The F-layer generates two predictions about the near-future trajectory of social musical experience.

**bonding_trajectory_pred** forecasts the direction of social bonding accumulation. It weights the current social_bonding_index (f02, weight 0.50) most heavily as the best predictor of near-future bonding state, supplemented by coupling_trend_1s (weight 0.30) indicating whether interpersonal coordination is strengthening or weakening, and loudness_trend_5s (weight 0.20) capturing shared dynamic trajectory over a longer window. The prediction operates on the slow bonding timescale (tau_bonding = 120.0s), reflecting that social bonds accumulate over minutes of shared musical experience.

**flow_sustain_pred** forecasts whether group flow can be maintained. It combines the current group_flow_state (f03, weight 0.40) with entrainment_quality (f04, weight 0.30) as the coordination precision that sustains flow, and an arousal signal (weight 0.30) as the energetic resource needed to maintain coordinated performance. Flow requires both coordination and appropriate activation level — too little arousal leads to disengagement, while excessive arousal disrupts the relaxed focus characteristic of flow states (Gold et al. 2019: optimal complexity maximizes musical pleasure via inverted-U).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f02 | social_bonding_index | Current bonding state as strongest predictor |
| E-layer f03 | group_flow_state | Current flow level for sustainability forecast |
| E-layer f04 | entrainment_quality | Coordination precision sustaining flow |
| H³ (25, 16, 18, 2) | coupling_trend_1s | Direction of consonance-energy coupling |
| H³ (8, 20, 18, 0) | loudness_trend_5s | Long-range dynamic trajectory for bonding prediction |
| Belief state | arousal | Energetic resource for flow sustainability |
