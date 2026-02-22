# attention_shift_pred — Anticipation Belief (IACM)

**Category**: Anticipation (prediction)
**Owner**: IACM (ASU-alpha2)

---

## Definition

"Frontal attention shift within ~400ms." Predicts whether involuntary frontal attention switching will occur in the near future (~400ms ahead). This is the predictive component of the P3a mechanism: spectral unpredictability in the current frame forecasts an upcoming attention reorientation event.

---

## Observation Formula

```
# From IACM F-layer:
attention_shift_pred = IACM.attention_shift_pred_0.4s[F1]  # index [9]

# Formula: sigma(0.5 * f04_inharmonic_capture + 0.5 * p3a_capture)
# where f04_inharmonic_capture = IACM E0:inharmonic_capture
# p3a_capture = IACM P0:p3a_capture
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted attention shift mismatches the observed capture state.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| IACM F1 | attention_shift_pred_0.4s [9] | Frontal attention shift prediction |
| IACM E0 | inharmonic_capture [0] | Current inharmonic detection |
| IACM P0 | p3a_capture [6] | Current P3a attention state |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | PE from attention prediction feeds reward signal |
| F5 Emotion | Surprise from unexpected attention capture |
| Precision engine | pi_pred estimation via prediction accuracy |

---

## Scientific Foundation

- **Basinski 2025**: P3a latency and amplitude predict attention reorientation (EEG, N=35)
- **Koelsch 1999**: P3a in musical context reflects involuntary attention switching
- **Friston 2005**: Precision-weighted predictions generate anticipatory signals
- **Alain 2007**: ORN predicts subsequent attention capture in auditory scenes

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/iacm_relay.py` (pending)
