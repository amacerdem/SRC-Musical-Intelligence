# collective_pleasure_pred — Anticipation Belief (SSRI)

**Category**: Anticipation (prediction)
**Owner**: SSRI (RPU-beta4)

---

## Definition

"We will experience pleasure together." Predicts whether the current trajectory of group musical interaction will produce shared hedonic experience. High collective pleasure prediction indicates that synchrony, bonding, and flow are converging toward a shared peak moment -- a collective crescendo of pleasure that amplifies individual reward through social resonance.

---

## Observation Formula

```
# From SSRI F-layer + E-layer:
collective_pleasure_pred = 0.50 * SSRI.flow_sustain_pred[F1]     # index [10]
                         + 0.50 * SSRI.f05_collective_pleasure[E4] # index [4]

# flow_sustain_pred = sigma(0.40 * f03_group_flow + 0.30 * f04_entrainment + 0.30 * arousal)
# f05 = sigma(0.25 * mean_pleasantness_500ms
#            + 0.25 * mean_roughness_500ms_inv
#            + 0.20 * f03_group_flow
#            + 0.15 * f02_social_bonding)
```

Anticipation beliefs are forward-looking predictions. collective_pleasure_pred generates PE when predicted shared pleasure mismatches observed group hedonic state.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SSRI F1 | flow_sustain_pred [10] | Predicted group flow sustainability |
| SSRI E4 | f05_collective_pleasure [4] | Current shared hedonic state |
| SSRI E2 | f03_group_flow_state [2] | Group flow (input to flow_sustain) |
| SSRI E3 | f04_entrainment_quality [3] | Entrainment (input to flow_sustain) |
| H3 | (4, 8, 1, 2) | Mean pleasantness at 500ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | PE from collective pleasure prediction feeds reward signal |
| neural_synchrony (Core) | Predicted shared pleasure informs synchrony anticipation |
| Precision engine | pi_pred estimation via prediction accuracy |

---

## Scientific Foundation

- **Mori & Zatorre 2024**: Pre-listening auditory-reward RSFC predicts chills duration; r=0.53 (fMRI+ML, N=49)
- **Salimpoor et al. 2011**: DA release in caudate (anticipation) -> NAcc (consummation); r=0.71 chills intensity vs pleasure (PET, N=8)
- **Williamson & Bonshor 2019**: Flow, cognitive engagement, social identity in group music-making (survey, N=346)
- **Tarr, Launay & Dunbar 2014**: Synchronized dancing increases social bonding + endorphin release (behavioral, N=94)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ssri.py`
