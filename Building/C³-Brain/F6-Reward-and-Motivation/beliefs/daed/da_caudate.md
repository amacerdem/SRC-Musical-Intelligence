# da_caudate — Appraisal Belief (DAED)

**Category**: Appraisal (observe-only)
**Owner**: DAED (RPU-a1)

---

## Definition

"Reward approaching, caudate DA ramp." Observes the current level of anticipatory dopamine activity in the caudate nucleus. This reflects the build-up phase before a musical peak: rising loudness, increasing spectral uncertainty, and roughness velocity create an anticipatory DA ramp that signals "reward is coming." The caudate DA level peaks 15-30 seconds before the consummatory moment.

---

## Observation Formula

```
# Direct read from DAED P-layer:
da_caudate = DAED.caudate_activation[P0]  # index [6]

# Upstream formula (f01_anticipatory_da):
# f01 = sigma(0.35 * loudness_velocity_1s
#             + 0.20 * spectral_uncertainty_125ms
#             + 0.15 * roughness_velocity_500ms)
#
# caudate_activation tracks f01 as the present-state representation
# of anticipatory DA level in caudate nucleus.
```

No prediction -- observe-only appraisal. The value is consumed by the reward formula as the anticipatory DA component.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DAED P0 | caudate_activation [6] | Present anticipatory DA level |
| DAED E0 | f01_anticipatory_da [0] | Upstream E-layer anticipatory signal |
| H3 | (8, 16, 8, 0) | Loudness velocity at 1s (w=0.35) -- crescendo tracking |
| H3 | (21, 4, 20, 0) | Spectral uncertainty at 125ms (w=0.20) -- prediction uncertainty |
| H3 | (0, 8, 8, 0) | Roughness velocity at 500ms (w=0.15) -- tension build-up |

---

## Kernel Usage

The da_caudate appraisal feeds the reward computation's DA gain mechanism:

```python
# Phase 5 in scheduler (reward.py):
# da_caudate contributes to anticipatory reward weighting
caudate_da = daed_relay['caudate_activation']
# Used in: da_gain = 0.5 * caudate_da + 0.5 * nacc_da
```

High caudate DA amplifies approach motivation and prediction-based reward signals. This is the "wanting" side of the reward system -- the expectation that something pleasurable is about to happen.

---

## Scientific Foundation

- **Salimpoor 2011**: PET [11C]raclopride binding potential decrease in caudate correlates with chills count (r = 0.71, p < 0.05), indicating DA release during anticipation phase
- **Salimpoor 2011**: Caudate activation peaks 15-30s BEFORE the peak emotional moment, establishing the temporal lead of anticipatory DA
- **Mohebi 2024**: Dorsal striatum (caudate) DA transients follow longer time horizons than ventral (NAcc), supporting caudate's role in anticipatory processing
- **Cheung 2019**: Uncertainty modulates anticipatory pleasure -- maps to spectral_uncertainty driving the f01 formula

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/daed_relay.py` (planned)
Source model: `Musical_Intelligence/brain/functions/f6/mechanisms/daed/`
