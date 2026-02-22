# da_nacc — Appraisal Belief (DAED)

**Category**: Appraisal (observe-only)
**Owner**: DAED (RPU-a1)

---

## Definition

"Reward happening now, NAcc DA burst." Observes the current level of consummatory dopamine activity in the nucleus accumbens. This reflects the experience phase at a musical peak: high pleasantness, strong loudness, and resolved harmonic tension converge to produce a DA burst that signals "this is pleasurable right now." The NAcc DA level peaks AT the consummatory moment.

---

## Observation Formula

```
# Direct read from DAED P-layer:
da_nacc = DAED.nacc_activation[P1]  # index [7]

# Upstream formula (f02_consummatory_da):
# f02 = sigma(0.35 * mean_pleasantness_1s
#             + 0.15 * mean_loudness_1s)
#
# nacc_activation tracks f02 as the present-state representation
# of consummatory DA level in nucleus accumbens.
```

No prediction -- observe-only appraisal. The value is consumed by the reward formula as the consummatory DA component.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DAED P1 | nacc_activation [7] | Present consummatory DA level |
| DAED E1 | f02_consummatory_da [1] | Upstream E-layer consummatory signal |
| H3 | (4, 16, 1, 2) | Mean pleasantness at 1s (w=0.35) -- hedonic quality |
| H3 | (8, 16, 1, 2) | Mean loudness at 1s (w=0.15) -- intensity at peak |
| H3 | (4, 3, 0, 2) | Pleasantness at 100ms -- fast hedonic read (used in f04) |

---

## Kernel Usage

The da_nacc appraisal feeds the reward computation's DA gain mechanism:

```python
# Phase 5 in scheduler (reward.py):
# da_nacc contributes to consummatory reward weighting
nacc_da = daed_relay['nacc_activation']
# Used in: da_gain = 0.5 * caudate_da + 0.5 * nacc_da
```

High NAcc DA amplifies hedonic pleasure and consummatory reward signals. This is the "liking" side of the reward system -- the direct experience of musical pleasure at the peak moment.

---

## Scientific Foundation

- **Salimpoor 2011**: PET [11C]raclopride binding potential decrease in NAcc correlates with pleasure rating (r = 0.84, p < 0.01), indicating DA release during consummation phase
- **Salimpoor 2011**: NAcc activation peaks AT the peak emotional moment, temporally distinct from caudate anticipatory DA (t = 2.8)
- **Putkinen 2025**: NAcc mu-opioid receptor (MOR) binding correlates with chills count, showing convergent neurochemical evidence for NAcc as hedonic hotspot
- **Gold 2023**: VS (including NAcc) activity shows liking x surprise interaction -- consummatory pleasure modulated by prediction outcome

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/daed_relay.py` (planned)
Source model: `Musical_Intelligence/brain/functions/f6/mechanisms/daed/`
