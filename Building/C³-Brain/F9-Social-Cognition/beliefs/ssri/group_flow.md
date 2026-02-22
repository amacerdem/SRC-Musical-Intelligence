# group_flow — Appraisal Belief (SSRI)

**Category**: Appraisal (observe-only)
**Owner**: SSRI (RPU-beta4)

---

## Definition

"Shared flow state." Observes the degree of collective absorption during group musical interaction. High group flow indicates that participants have entered a shared state of effortless coordination, where entrainment, shared affect, and challenge-skill balance converge to produce a qualitatively distinct collective experience that amplifies hedonic reward beyond what any individual listener achieves alone.

---

## Observation Formula

```
# Direct read from SSRI E-layer + M-layer:
group_flow = 0.60 * SSRI.f03_group_flow_state[E2]        # index [2]
           + 0.40 * SSRI.synchrony_amplification[M1]      # index [6]

# f03 = sigma(0.25 * f01_synchrony_reward
#            + 0.25 * mean_loudness_500ms
#            + 0.20 * onset_periodicity_500ms
#            + 0.15 * mean_amplitude_500ms
#            + 0.15 * spectral_entropy_500ms)
# synchrony_amplification = 1.0 + f01 * (f04 + f02), range [1.0, ~3.0]
```

No prediction -- observe-only appraisal. Group flow is a composite state reflecting the product of synchrony, bonding, and entrainment quality.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SSRI E2 | f03_group_flow_state [2] | Group flow composite |
| SSRI M1 | synchrony_amplification [6] | Social-to-solo reward ratio |
| SSRI E0 | f01_synchrony_reward [0] | Synchrony reward (input to f03) |
| H3 | (10, 8, 14, 2) | Onset periodicity at 500ms |
| H3 | (7, 8, 1, 2) | Mean amplitude at 500ms |
| H3 | (21, 8, 20, 2) | Spectral entropy at 500ms |

---

## Kernel Usage

Group flow amplifies hedonic reward in the F6 reward aggregator:

```python
# Phase 3 in scheduler:
# Group flow state amplifies hedonic experience
flow_amplification = ssri_relay['group_flow']
# Flow_Group = alpha * Entrainment * beta * SharedAffect * gamma * ChallengeSkilBalance
# alpha=0.40, beta=0.35, gamma=0.25
```

---

## Scientific Foundation

- **Bigand et al. 2025**: Novel neural marker of social coordination encodes spatiotemporal alignment between dancers; surpasses self/partner kinematics alone (EEG mTRFs, N=70)
- **Gold et al. 2019**: Intermediate predictive complexity maximizes musical pleasure; inverted-U for IC; quadratic b=-3.167 (behavioral, N=43)
- **Williamson & Bonshor 2019**: Flow, cognitive engagement, social identity reported in brass band group music (survey, N=346)
- **Dunbar 2012**: Synchronized music-making increases endorphin release; social bonding via endorphin pathway (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ssri.py`
