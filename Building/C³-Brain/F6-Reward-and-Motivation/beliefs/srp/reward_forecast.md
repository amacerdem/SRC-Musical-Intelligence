# reward_forecast -- Anticipation Belief (SRP)

**Category**: Anticipation (prediction)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Upcoming reward estimate." Predicts the expected reward magnitude in the next 2-8 seconds based on the current musical buildup trajectory, harmonic tension, and energy trajectory. This is Huron's Imagination (I) response: a longer-range anticipatory signal that projects forward to estimate how rewarding the upcoming musical passage will be.

Reward forecast operates at section timescale (Salimpoor anticipation window: 15-30s), providing the "headline" signal that drives approach/avoidance motivation. High reward forecast ("this is about to get really good") drives wanting and caudate DA ramp; low reward forecast ("this passage is losing steam") reduces engagement.

---

## Observation Formula

```
# From SRP F-layer (Forecast):
reward_forecast = SRP.reward_forecast[F16]  # index [16]

# Range: [0, 1]
# 0 = no reward expected (flat, predictable, low energy)
# 1 = maximum reward expected (building toward climax, high tension+energy)

# Formula:
# reward_forecast = sigma(0.4*tension_trajectory + 0.3*energy_buildup + 0.2*harmonic_progression
#                         + 0.1*prediction_confidence)
# where:
#   tension_trajectory = SRP.tension trend (H3 M18 forward slope of tension)
#   energy_buildup = R3[7] (amplitude) -> H3(H22, M8, L0) -- section-level energy velocity
#   harmonic_progression = harmonic_tension building toward expected resolution
#   prediction_confidence = pi_pred from precision engine (confident predictions = higher forecast)

# The forecast operates at section timescale (2-8s forward):
# - During verse: moderate forecast (stable, moderate reward expected)
# - During pre-chorus buildup: rising forecast (approaching chorus)
# - At chorus arrival: forecast peaks, then transitions to experienced reward
# - During bridge/breakdown: forecast drops, then rebuilds
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted reward magnitude mismatches the actual experienced reward.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP F16 | reward_forecast [16] | Expected reward in 2-8s |
| SRP T9 | tension [9] | Tension trajectory (building toward reward?) |
| SRP M14 | dynamic_intensity [14] | Energy trajectory (crescendo buildup) |
| SRP M13 | harmonic_tension [13] | Harmonic progression (approaching resolution?) |
| SRP N0 | da_caudate [0] | Caudate DA ramp (anticipatory value signal) |
| H3 (H22, M8, L0) | amplitude velocity | Section-level energy change rate |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 wanting | Forecast feeds wanting prediction (reward magnitude scaling) |
| F6 da_caudate (DAED) | Expected reward magnitude scales caudate DA ramp height |
| Output | Upcoming reward estimate for behavioral planning and experiential logging |
| Precision engine | pi_pred estimation via forecast accuracy over time |

---

## Scientific Foundation

- **Huron 2006**: Imagination (I) response -- longer-range anticipatory signal that projects forward (Sweet Anticipation, MIT Press)
- **Salimpoor 2011**: Caudate DA ramps 2-30s before peak, implying forward reward estimation (PET, N=8)
- **Salimpoor 2013**: NAcc-STG connectivity predicts how much listeners would PAY -- implies forward valuation (Science, N=19)
- **Mas-Herrero 2021**: Pre-experience NAcc predicts motivation R2=0.47 -- brain estimates upcoming reward before it arrives (TMS+fMRI, N=17)
- **Howe 2013**: DA proximity signal scales with both distance AND magnitude of expected reward (in vivo rodent)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
