# consonance_salience_gradient — Appraisal Belief (CSG, F1)

**Type**: Appraisal (observe-only)
**Mechanism**: CSG (Relay, Depth 0)
**Function**: F1 Sensory Processing

---

## Definition

"The current consonance level is modulating salience network activation."

---

## Observation Formula

```
observe = 0.40 * P0:salience_network[6]
        + 0.30 * E0:salience_activation[0]
        + 0.30 * M0:salience_response[3]
```

**Range**: [0, 1] — weighted sum of [0,1] bounded CSG outputs (all three source dims use sigmoid activation).

---

## Source Dimensions

| Weight | CSG Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.40 | [6] | P0:salience_network | Attention-gated salience — the core integration output |
| 0.30 | [0] | E0:salience_activation | ACC/AI dissonance-driven activation — early salience |
| 0.30 | [3] | M0:salience_response | Graded salience response with temporal context |

---

## Design Rationale

The consonance-salience gradient belief is high when:
- Salience network is active (P0 > 0.5): consonance level is driving attention
- Salience activation is strong (E0 > 0.5): dissonance is engaging ACC/AI
- Salience response is elevated (M0 > 0.5): temporal context confirms sustained salience

The 40/30/30 weighting emphasizes the present-layer integration (P0) as the most informative signal, while balancing early extraction (E0) and temporal integration (M0). P0 is preferred because it incorporates attention gating — salience is not just about the signal but about whether the salience network is allocating resources.

Note: P1:affective_evaluation and E2:consonance_valence (tanh, [-1,1]) are intentionally excluded from this belief. Those dimensions carry valence information, not salience magnitude.

---

## No Predict/Update Cycle

As an Appraisal belief, consonance_salience_gradient is observe-only:
- No prior (tau), no baseline
- No Bayesian update
- No prediction error

It provides a moment-by-moment assessment of how strongly consonance/dissonance is modulating salience network activation without maintaining temporal expectations.

---

## Scientific Foundation

- **Bravo 2017**: Strong dissonance -> ACC/bilateral AI (d=5.16); graded salience across consonance levels (fMRI, N=12)
- **Koelsch 2006**: Dissonant -> amygdala/hippocampus; consonant -> AI/HG/ventral striatum (fMRI, N=11)
- **Cheung 2019**: Uncertainty modulates salience (amygdala/hippocampus, fMRI, N=79)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/csg/consonance_salience_gradient.py`
