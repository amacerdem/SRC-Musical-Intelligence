# retrieval_probability — Appraisal Belief (MEAMN)

**Category**: Appraisal (observe-only)
**Owner**: MEAMN (IMU-α1)

---

## Definition

"My probability of accessing this memory is X." Direct read from MEAMN memory_state. Tracks the real-time probability that the current musical input will successfully trigger an autobiographical memory retrieval. This is the raw retrieval activation level before it is combined with emotional and contextual factors in the Core beliefs.

---

## Observation Formula

```
# Direct read from MEAMN P-layer:
retrieval_probability = MEAMN.memory_state[P0]  # index [5]

# memory_state = retrieval_dynamics aggregation
# Aggregation of hippocampus-mPFC-PCC hub engagement
```

No prediction — observe-only appraisal. The value is directly read from the MEAMN relay's memory_state output. It represents the summary present-moment retrieval activation.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN P0 | memory_state [5] | Primary retrieval activation level |
| MEAMN E0 | f01_retrieval [0] | E-layer retrieval (upstream of P0) |
| MEAMN M0 | meam_retrieval [3] | M-layer retrieval function (upstream of P0) |

---

## Kernel Usage

The retrieval_probability appraisal serves as a diagnostic signal:

```python
# Available in BeliefStore for downstream consumers:
# - F5 Emotion: gates emotional processing of memories
# - F6 Reward: retrieval probability modulates reward magnitude
# - Precision engine: high retrieval → higher pi_obs for memory beliefs
```

Unlike the autobiographical_retrieval Core belief (which combines implicit H³ and explicit MEAMN signals), retrieval_probability is a pure mechanism read — it reports exactly what the MEAMN model computes without any kernel-level integration.

---

## Scientific Foundation

- **Janata 2009**: Dorsal MPFC parametrically tracks autobiographical salience (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Janata et al. 2007**: 30-80% MEAM trigger rate — retrieval probability varies systematically with familiarity, arousal, and valence (behavioral, N~300)
- **Derks-Dijkman et al. 2024**: 28/37 studies show musical mnemonics improve retrieval probability (systematic review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/meamn_relay.py`
