# phrase_boundary_pred — Anticipation Belief (HMCE)

**Category**: Anticipation (prediction)
**Owner**: HMCE (STU-α1)

---

## Definition

"Phrase boundary approaching." Predicts that a musical phrase boundary is imminent based on entropy-driven cues in the medium-context encoding. When energy and pitch dynamics become unpredictable (high entropy) at the phrase timescale, the hierarchical encoding system anticipates a structural boundary — the end of one phrase and the beginning of the next.

---

## Observation Formula

```
# From HMCE F-layer:
phrase_boundary_pred = HMCE.phrase_expect[F1]  # index [11]

# Formula: sigma(w_entropy * entropy_energy + w_pitch * pitch_variability
#                + w_trend * loudness_trend)
# where entropy_energy   = H3[(22, 14, 13, 0)]   energy_change entropy at H14
#       pitch_variability = H3[(23, 14, 3, 0)]    pitch_change std at H14
#       loudness_trend    = H3[(7, 14, 18, 0)]    amplitude trend at H14
```

Anticipation beliefs are forward-looking predictions that generate context for Core Beliefs' predict() methods. Phrase boundary prediction feeds the context_depth Core Belief by signaling when hierarchical reorganization is needed — at boundaries, short context resets while medium/long context persists.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE F1 | phrase_expect [11] | Phrase boundary expectation |
| H³ | (22, 14, 13, 0) | Energy change entropy at H14 (unpredictability) |
| H³ | (23, 14, 3, 0) | Pitch change std at H14 (variability) |
| H³ | (7, 14, 18, 0) | Amplitude trend at H14 (intensity trajectory) |
| HMCE E1 | f02_medium_context [1] | Medium context encoding (STG) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F4 Memory | Episodic boundary detection — phrase ends trigger encoding |
| F2 Prediction | Sequence completion signal — prediction hierarchy resets |
| F7 Motor (context_depth) | Hierarchical reorganization at boundaries |
| Precision engine | pi_pred estimation via boundary prediction accuracy |

---

## Scientific Foundation

- **Mischler 2025**: STG medium-context encoding (layers 5-9) tracks phrase-level structure; boundary detection implicit in context transitions (ECoG, N=26)
- **Norman-Haignere 2022**: Integration window transitions at ~136ms correspond to phrase-level processing boundaries (iEEG, 18 patients)
- **Wöhrle 2024**: Context accumulates over chord progressions; N1m divergence signals boundary approach (MEG, N=30, eta_p^2=0.101)
- **Kim 2021**: STG handles perceptual ambiguity at boundaries; IFG handles syntactic irregularity (MEG, N=19, F=12.37)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
