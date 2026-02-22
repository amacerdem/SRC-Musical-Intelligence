# processing_load_pred — Anticipation Belief (CSG)

**Category**: Anticipation (prediction)
**Owner**: CSG (ASU-a3)

---

## Definition

"Upcoming sensory load estimate." Predicts the processing resource demand 0.75s ahead. Uses current processing state and ambiguity to forecast whether Heschl's gyrus will face high or low processing load in the near future. This is an Anticipation belief — it generates predictions that can produce prediction errors.

---

## Observation Formula

```
# Direct read from CSG F-layer:
processing_load_pred = CSG.processing_pred_0.75s[F1]   # index [10], [0,1]

# Computation:
# sigma(0.5 * f08 + 0.5 * ambiguity)
#
# f08 = current processing state from E-layer
# ambiguity = 1 - |consonance - 0.5| * 2
#
# Predicts Heschl's processing load 0.75s ahead
```

As an Anticipation belief, this generates a prediction that is compared against actual processing load when it arrives, producing prediction error for learning.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| CSG F1 | processing_pred_0.75s [10] | Processing load prediction |
| CSG E-layer | f08 processing state | Current processing context |
| CSG P2 | sensory_load [8] | Current actual processing load (for PE) |

---

## Kernel Usage

The processing_load_pred Anticipation belief generates forward-looking predictions:

```python
# Phase 2 in scheduler:
# Predict processing load 0.75s ahead
processing_pred = observe(csg_relay['processing_pred_0.75s'])

# When 0.75s elapses, compare with actual sensory_load
# PE = actual_sensory_load - processing_pred
```

This prediction-comparison cycle allows the system to learn regularities in processing demand. Predictable passages (e.g., sustained consonance) produce low PE; unexpected complexity changes produce high PE.

---

## Scientific Foundation

- **Bravo 2017**: Processing demand predictable from consonance trajectory
- **Koelsch 2011**: Heschl's gyrus processing load scales with auditory complexity
- **Sarasso 2019**: ERP latency reflects processing anticipation (EEG)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/csg_relay.py`
