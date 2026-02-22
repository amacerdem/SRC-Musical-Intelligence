# resolution_expectation -- Anticipation Belief (SRP)

**Category**: Anticipation (prediction)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Resolution expectation (deceptive -> extended)." Predicts when and how harmonic resolution will occur, on a spectrum from "imminent authentic cadence" to "deceptive/extended -- resolution delayed." This belief captures the listener's expectation about upcoming harmonic closure: high values indicate confident expectation of resolution within 0.5-2s (dominant -> tonic), while shifts in the signal indicate the system has detected a deceptive cadence pattern (V->vi) that will extend the tension-resolution arc.

Resolution expectation is the critical signal for the delayed gratification mechanism: when resolution is delayed (deceptive cadence), wanting EXTENDS instead of dropping, and the eventual resolution produces an ENHANCED pleasure burst. This is why delayed resolutions are more rewarding than immediate ones.

---

## Observation Formula

```
# From SRP F-layer (Forecast):
resolution_expectation = SRP.resolution_expect[F18]  # index [18]

# Range: [0, 1]
# 0 = no resolution expected (stable tonic, or maximally deceptive)
# 1 = resolution imminent (dominant held, strong cadential expectation)

# Formula:
# resolution_expectation = sigma(0.5*harmonic_tension_trajectory + 0.3*cadential_pattern + 0.2*energy_trend)
# where:
#   harmonic_tension_trajectory = harmonic_tension trend (is tension peaking?)
#   cadential_pattern = BCH consonance trajectory suggesting V->I motion
#   energy_trend = R3[7] (amplitude) -> H3(H18, M18, L0) -- energy building toward resolution

# For deceptive cadences:
# When V->vi detected (prediction_match = -1 at cadence point):
# resolution_expectation drops briefly then REBUILDS at higher level
# because the system now expects extended resolution
# wanting extends, eventual resolution yields enhanced DA burst
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted resolution timing mismatches the actual harmonic event.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP F18 | resolution_expect [18] | Harmonic resolution prediction |
| SRP M13 | harmonic_tension [13] | Current tonal distance (resolution needed?) |
| SRP T10 | prediction_match [10] | Recent match/violation (deceptive cadence detection) |
| BCH | consonance_signal | Hierarchical consonance trajectory |
| R3 [0:7] | consonance group | Consonance transition detection |
| H3 (H18, M18, L0) | roughness trend | Forward roughness trajectory (approaching resolution?) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F2 Prediction | Resolution prediction modulates harmonic expectation confidence |
| F6 tension | Resolution proximity modulates tension trajectory |
| F6 wanting | Delayed resolution extends wanting ramp |
| Precision engine | pi_pred estimation via resolution prediction accuracy |

---

## Scientific Foundation

- **Huron 2006**: Delayed resolution amplifies subsequent pleasure via extended tension (Sweet Anticipation, MIT Press)
- **Cheung 2019**: Low uncertainty + high surprise (unexpected resolution) yields peak pleasure (fMRI, N=39)
- **Sloboda 1991**: Appoggiaturas and deceptive cadences among top chill triggers (survey, N=83)
- **Meyer 1956**: Emotion in music arises from expectation and its violations/resolutions (Emotion and Meaning in Music)
- **Koelsch, Vuust & Friston 2019**: Predictive processes generate reward through resolution of prediction errors

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
