# self_relevance — Appraisal Belief (MEAMN)

**Category**: Appraisal (observe-only)
**Owner**: MEAMN (IMU-α1)

---

## Definition

"This is MY music." vmPFC self-referential processing. Tracks whether the listener has entered the self-referential processing mode where music is no longer just heard but is experienced as personally meaningful — connected to identity, life narrative, and self-concept. This is the mPFC-mediated "about me" signal that distinguishes generic musical enjoyment from deeply personal engagement.

---

## Observation Formula

```
# Direct read from MEAMN F-layer:
self_relevance = MEAMN.self_ref_fc[F2]  # index [10]

# self_ref_fc = sigma(mPFC activation trajectory)
# Based on H24 (36s) long-term window
# Predicts whether the listener is in self-referential mode
```

No prediction — observe-only appraisal. The value is read from the MEAMN F-layer's self-referential prediction output. Although F2:self_ref_fc is technically a "prediction" within the mechanism (it forecasts sustained self-referential engagement over 5-10s), at the belief level it is consumed as a present-state appraisal of current vmPFC activation.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN F2 | self_ref_fc [10] | mPFC self-referential activation |
| H³ | (10, 24, 3, 0) loudness std H24 L0 | Arousal variability over 36s (upstream) |
| H³ | (22, 24, 19, 0) entropy stability H24 L0 | Pattern stability over 36s (upstream) |

---

## Kernel Usage

The self_relevance appraisal feeds multiple downstream systems:

```python
# Available in BeliefStore for downstream consumers:
# - autobiographical_retrieval observe: 0.15 weight in explicit pathway
#   explicit = 0.60×memory_state + 0.25×emotional_color + 0.15×self_ref
# - Precision engine: 0.2 weight in pi_obs for autobiographical_retrieval
#   + MEAMN: 0.3×(memory×nostalgia) + 0.2×self_ref + 0.1×vividness
# - F6 Reward: self-referential processing boosts hedonic value
```

Self-relevance is a key moderator: when high, it amplifies both the observed autobiographical retrieval signal and its precision, creating a positive feedback loop where personally meaningful music receives more confident memory processing.

---

## Scientific Foundation

- **Janata 2009**: mPFC (BA 8/9) self-referential processing tracks autobiographical salience; left-lateralized response to personally meaningful tonal movement (fMRI 3T, N=13, t(12)=2.96, p=0.012)
- **Janata 2009**: Self-referential processing predicts imagery vividness and emotional evocation (t(9)=5.784 and t(9)=3.442 respectively)
- **Tulving 2002**: Episodic memory requires autonoetic consciousness — self-referential processing is necessary for full autobiographical recall (review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/meamn_relay.py`
