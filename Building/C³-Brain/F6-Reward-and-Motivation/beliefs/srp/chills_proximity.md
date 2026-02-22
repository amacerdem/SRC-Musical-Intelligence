# chills_proximity -- Anticipation Belief (SRP)

**Category**: Anticipation (prediction)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Proximity to chills moment." Predicts how close the listener is to a chills/frisson event based on the current buildup trajectory. This is the temporal proximity signal: as musical structure signals an approaching climax (crescendo, harmonic buildup, textural thickening), chills_proximity increases quasi-hyperbolically, mirroring the caudate DA ramp profile (Howe 2013).

The signal respects the behavioral refractory period (~10-30s between chills events, Grewe 2009). After a peak, chills_proximity drops to near-zero and cannot ramp again until the refractory period has elapsed and a new anticipatory buildup cycle begins.

---

## Observation Formula

```
# From SRP F-layer (Forecast):
chills_proximity = SRP.chills_proximity[F17]  # index [17]

# Range: [0, 1]
# 0 = no chills expected / refractory period
# 1 = chills imminent (high DA ramp, tension peak, resolution approaching)

# Formula:
# chills_proximity = sigma(0.4*da_caudate_ramp + 0.3*tension_buildup + 0.3*harmonic_progression)
#                    * refractory_gate
# where:
#   da_caudate_ramp = SRP.da_caudate trend (quasi-hyperbolic approach)
#   tension_buildup = SRP.tension trend (energy + harmonic unresolvedness increasing)
#   harmonic_progression = transition toward resolution (dominant -> tonic trajectory)
#   refractory_gate = sigma(5 * (time_since_last_peak - 10s))
#     -- near-zero for 10s after peak, ramps to 1.0 over ~10-30s
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted chills timing mismatches the actual peak event.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP F17 | chills_proximity [17] | Time-to-chills estimate |
| SRP N0 | da_caudate [0] | Caudate DA ramp (anticipatory approach) |
| SRP T9 | tension [9] | Tension buildup trajectory |
| SRP M13 | harmonic_tension [13] | Harmonic unresolvedness (resolution approaching?) |
| SRP M15 | peak_detection [15] | Last peak time (refractory gating) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Output | Time-to-chills estimate for experiential monitoring |
| F6 wanting | Chills proximity feeds wanting prediction (reward approaching) |
| Precision engine | pi_pred estimation via chills prediction accuracy |
| F10 Clinical | Chills frequency prediction for therapeutic engagement monitoring |

---

## Scientific Foundation

- **Salimpoor 2011**: Caudate DA ramps 2-30s before peak chills, matching quasi-hyperbolic proximity profile (PET, N=8)
- **Howe 2013**: DA proximity signal ramps quasi-hyperbolically toward expected reward (in vivo rodent)
- **Grewe 2009**: Inter-chill refractory ~10-30s -- not neural exhaustion, but prediction rebuild time (N=38)
- **Mori & Zatorre 2024**: Pre-listening auditory-reward connectivity predicts subsequent chills duration (fMRI+ML, N=49, r=0.53)
- **de Fleurian & Pearce 2021**: Chills prevalence 55-90%; temporal patterns suggest anticipatory buildup (systematic review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
