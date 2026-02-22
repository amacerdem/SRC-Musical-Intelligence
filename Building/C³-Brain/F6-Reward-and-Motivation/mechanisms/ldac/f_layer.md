# LDAC — Forecast

**Model**: Liking-Dependent Auditory Cortex
**Unit**: RPU-γ1
**Function**: F6 Reward & Motivation
**Tier**: γ (Integrative)
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | sensory_gating_pred | Predicted sensory gating state. sensory_gating_pred = σ(0.5 * f01 + 0.5 * f03). Forecasts the near-future state of pleasure-dependent sensory gating by combining the STG-liking coupling (f01) with the IC x liking interaction (f03). When liking is high and IC is low, gating is predicted to remain open (enhanced processing); when IC is high and liking is low, gating is predicted to suppress (reduced processing). Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

No dedicated H³ tuples for F-layer. This layer operates entirely on E-layer outputs (f01, f03). Prediction is based on the current pleasure state and IC-liking interaction as indicators of the near-future gating trajectory.

---

## Computation

The F-layer generates a single prediction about the near-future sensory gating state.

**sensory_gating_pred** combines STG-liking coupling (f01, weight 0.50) with IC x liking interaction (f03, weight 0.50) through sigmoid activation. The rationale is that the predicted gating state depends on two factors:

1. **Current liking level (f01)**: If pleasure is high, sensory processing is predicted to remain enhanced in the near future, as liking tends to be temporally autocorrelated during naturalistic listening.

2. **IC x liking interaction (f03)**: If the current moment shows high IC in disliked music (high f03, meaning suppression is active), the prediction is that gating will tighten further. Conversely, if IC is low or music is liked, suppression is minimal and the prediction favors open gating.

This prediction enables downstream systems (notably F3 Attention via ASU.sensory_gain) to anticipate changes in auditory cortex responsiveness, supporting proactive allocation of attentional resources. The prediction horizon is short (~0.5-1s), consistent with the rapid tau_decay = 0.5s of LDAC's temporal dynamics.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | stg_liking_coupling | Current pleasure state predicts future gating openness |
| E-layer f03 | ic_liking_interaction | Current IC x liking state predicts future suppression |
| Downstream: ASU | sensory_gain | Prediction consumed for proactive attention allocation |
