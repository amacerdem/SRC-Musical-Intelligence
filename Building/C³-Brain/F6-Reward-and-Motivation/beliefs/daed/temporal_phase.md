# temporal_phase — Appraisal Belief (DAED)

**Category**: Appraisal (observe-only)
**Owner**: DAED (RPU-a1)

---

## Definition

"Currently in anticipation / experience phase." Observes the relative balance between anticipatory and consummatory dopamine, yielding a continuous phase indicator. Values near 1.0 indicate pure anticipation (caudate-dominant), values near 0.0 indicate pure consummation (NAcc-dominant), and values near 0.5 indicate a balanced transition state.

---

## Observation Formula

```
# Direct read from DAED M-layer:
temporal_phase = DAED.temporal_phase[M1]  # index [5]

# Formula: f01 / (f01 + f02 + epsilon)
# where epsilon = 1e-8
#   f01 = anticipatory DA (caudate proxy)
#   f02 = consummatory DA (NAcc proxy)
```

No prediction -- observe-only appraisal. The value is a normalized ratio that tracks the listener's position in the anticipation-consummation cycle.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DAED M1 | temporal_phase [5] | Normalized anticipation/consummation ratio |
| DAED E0 | f01_anticipatory_da [0] | Numerator -- caudate DA level |
| DAED E1 | f02_consummatory_da [1] | Denominator component -- NAcc DA level |
| H3 | (8, 16, 8, 0) | Loudness velocity at 1s -- upstream to f01 |
| H3 | (4, 16, 1, 2) | Mean pleasantness at 1s -- upstream to f02 |

---

## Kernel Usage

The temporal_phase appraisal modulates how the reward system interprets incoming signals:

```python
# Phase 5 in scheduler:
phase = daed_relay['temporal_phase']  # f01 / (f01 + f02 + eps)
# phase > 0.5 -> anticipation-dominant -> weight caudate signals
# phase < 0.5 -> consummation-dominant -> weight NAcc signals
```

This provides a continuous gating signal for phase-appropriate reward processing. During anticipation (phase > 0.5), prediction-based reward signals are emphasized. During consummation (phase < 0.5), hedonic pleasure signals dominate.

---

## Scientific Foundation

- **Salimpoor 2011**: Caudate DA release 15-30s BEFORE peak moment (anticipation), NAcc DA release AT peak moment (consummation) -- temporal dissociation is the core DAED finding
- **Berridge 2007**: Wanting (anticipatory, dopaminergic) vs Liking (consummatory, opioid/DA) framework maps to phase > 0.5 vs phase < 0.5
- **Cheung 2019**: NAcc reflects anticipatory uncertainty; amygdala reflects uncertainty x surprise interaction -- phase tracking needed to distinguish these roles

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/daed_relay.py` (planned)
Source model: `Musical_Intelligence/brain/functions/f6/mechanisms/daed/`
