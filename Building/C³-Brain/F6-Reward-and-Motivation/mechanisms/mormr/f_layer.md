# MORMR — Forecast

**Model**: mu-Opioid Receptor Music Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | chills_onset_pred | Chills onset prediction (2-5s ahead). Forecasts the probability of an upcoming chills/frisson event based on the current opioid state trajectory and musical build-up dynamics. When the anticipatory opioid state is rising (increasing f01, sustained beauty coupling, energy velocity positive), the model predicts an impending chills event. Putkinen 2025: chills frequency correlates with NAcc MOR binding (r = -0.52). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

The F-layer primarily reuses E-layer and M-layer outputs rather than reading new H³ tuples directly. Its prediction is derived from the trajectory of existing features.

---

## Computation

The F-layer produces a forward-looking prediction of chills onset:

**Chills Onset Prediction**: Combines the current opioid release trajectory with chills-predictive features. The key predictive signals are:
- Rising opioid release (f01 increasing over time) signals approach to a pleasure peak
- Rising beauty coupling entropy signals increasing aesthetic complexity preceding a peak
- Energy velocity indicates dynamic build-up

This prediction operates on a 2-5s forward horizon, corresponding to the anticipatory window observed in Salimpoor (2011) where caudate DA release precedes peak emotion. The opioid system's contribution to this prediction captures the longer-timescale hedonic anticipation that complements DAED's dopaminergic anticipation.

The chills onset prediction feeds:
- ARU arousal predictions (autonomic preparation for chills)
- F4 Memory episodic encoding (chills events are preferentially encoded)
- Precision engine (pi_pred for upcoming hedonic events)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_opioid_release | Current opioid level — rising f01 predicts chills |
| E-layer | f02_chills_count | Recent chills history for prediction context |
| E-layer | f04_reward_sensitivity | Individual sensitivity modulates prediction threshold |
| M-layer | opioid_tone | Integrated opioid state trajectory |
| P-layer | current_opioid_state | Present-moment hedonic level |
