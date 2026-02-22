# structure_pred — Anticipation Belief (HMCE)

**Category**: Anticipation (prediction)
**Owner**: HMCE (STU-α1)

---

## Definition

"Formal section will transform like this." Predicts long-range structural transformations based on autocorrelation-based section return detection. When the long-context encoding detects self-similarity patterns at the section timescale, the system anticipates how the formal structure will unfold — whether a section will return (recapitulation), depart (development), or transform (variation).

---

## Observation Formula

```
# From HMCE F-layer:
structure_pred = HMCE.structure_predict[F2]  # index [12]

# Formula: sigma(w_autocorr * long_autocorr + w_stability * stability_long
#                + w_context * f03_long_context)
# where long_autocorr  = H3[(25, 20, 22, 0)]   x_l0l5 autocorrelation at H20
#       stability_long = H3[(33, 20, 19, 0)]   x_l4l5 stability at H20
#       f03            = HMCE.f03_long_context  long context encoding (MTG)
```

Anticipation beliefs are forward-looking predictions that generate context for Core Beliefs' predict() methods. Structure prediction feeds the context_depth Core Belief by signaling long-range expectations — when the system predicts section return, context_depth should maintain deep encoding; when departure is predicted, the system prepares for new encoding patterns.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE F2 | structure_predict [12] | Long-range structural prediction |
| H³ | (25, 20, 22, 0) | x_l0l5 autocorrelation at H20 (section repetition) |
| H³ | (33, 20, 19, 0) | x_l4l5 stability at H20 (temporal stability) |
| H³ | (33, 20, 22, 0) | x_l4l5 autocorrelation at H20 (self-similarity) |
| HMCE E2 | f03_long_context [2] | Long context encoding (MTG) |
| HMCE E4 | f05_expertise [4] | Expertise modulation of deep structure |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F2 Prediction | Hierarchical prediction — abstract future structure |
| F4 Memory | Long-range structural expectations feed episodic encoding |
| F6 Reward | Structural predictions generate PE when violated/confirmed |
| F7 Motor (context_depth) | Deep-layer prediction for hierarchical integration |
| Precision engine | pi_pred estimation via structural prediction accuracy |

---

## Scientific Foundation

- **Mischler 2025**: MTG and temporal pole encode 100-300+ notes context; musicians integrate to layer 13 (d=0.32, p=3.8e-08; ECoG+EEG, N=26)
- **Bonetti 2024**: Hierarchical feedforward AC to hippocampus to cingulate supports long-range structural predictions; expertise modulates contextual encoding (BOR=2.91e-07; MEG, N=83)
- **Golesorkhi 2021**: DMN/FPN temporal hierarchy enables long-range prediction (d=-0.66 to -2.03; core-periphery ACW; MEG, N=89)
- **Fedorenko 2012**: Bilateral temporal regions sensitive to musical structure; intact vs scrambled structure detection (fMRI, N=12)
- **Honey 2012**: Slow cortical dynamics accumulate information over long timescales enabling structural prediction (fMRI, inter-subject correlation)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
