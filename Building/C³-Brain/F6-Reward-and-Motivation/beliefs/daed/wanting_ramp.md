# wanting_ramp — Anticipation Belief (DAED)

**Category**: Anticipation (prediction)
**Owner**: DAED (RPU-a1)

---

## Definition

"Expectation increases as reward approaches." Predicts the trajectory of anticipatory motivation -- the wanting_index (f03) serves as a forward-looking signal that ramps up as acoustic features indicate an approaching reward moment. This is the dopaminergic "wanting" ramp: coupling entropy and anticipatory DA jointly predict that pleasure is imminent.

---

## Observation Formula

```
# From DAED E-layer (forward-looking signal):
wanting_ramp = DAED.f03_wanting_index[E2]  # index [2]

# Formula: sigma(0.40 * f01 + 0.30 * coupling_entropy_1s)
# where:
#   f01 = anticipatory DA (caudate proxy)
#   coupling_entropy_1s = H3 (25, 16, 20, 2) -- foundation x perceptual uncertainty
```

Anticipation beliefs are forward-looking predictions. wanting_ramp generates PE when the predicted reward approach mismatches the actual consummatory outcome -- a ramping wanting signal that fails to culminate in pleasure produces negative reward PE.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DAED E2 | f03_wanting_index [2] | Anticipatory motivation level |
| DAED E0 | f01_anticipatory_da [0] | Caudate DA input (w=0.40) |
| H3 | (25, 16, 20, 2) | Coupling entropy at 1s (w=0.30) -- prediction uncertainty |
| H3 | (8, 16, 8, 0) | Loudness velocity at 1s -- upstream to f01 |
| H3 | (21, 4, 20, 0) | Spectral uncertainty at 125ms -- upstream to f01 |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 wanting (Core) | Wanting_ramp feeds the wanting Core Belief's predict() as anticipatory context |
| F6 tension (Core) | Rising wanting_ramp increases tension -- "something about to happen" |
| F6 Reward | PE from wanting_ramp vs actual consummation feeds reward signal (surprise component) |
| Precision engine | pi_pred estimation via wanting prediction accuracy history |

---

## Scientific Foundation

- **Salimpoor 2011**: Caudate DA release during anticipation (r = 0.71 with chills count) -- the "wanting" system ramps before pleasure, validated with PET [11C]raclopride
- **Berridge 2007**: Incentive salience ("wanting") is dissociable from hedonic impact ("liking") -- wanting_ramp captures the dopaminergic incentive approach signal
- **Cheung 2019**: Uncertainty x surprise jointly predict musical pleasure -- coupling_entropy captures the uncertainty component that modulates anticipatory wanting
- **Mohebi 2024**: DA transients in dorsal striatum (caudate) follow longer reward time horizons, supporting the gradual ramp-up of anticipatory wanting

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/daed_relay.py` (planned)
Source model: `Musical_Intelligence/brain/functions/f6/mechanisms/daed/`
