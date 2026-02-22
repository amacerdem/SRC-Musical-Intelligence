# social_bonding — Appraisal Belief (SSRI)

**Category**: Appraisal (observe-only)
**Owner**: SSRI (RPU-beta4)

---

## Definition

"Relationship deepening through music." Observes the degree to which sustained musical coordination strengthens interpersonal bonds. High social bonding indicates that prolonged synchronized activity is producing endorphin/oxytocin release, increasing trust, cohesion, and a sense of shared identity. Social bonding accumulates slowly (tau_bond = 120s) through sustained coordinated interaction.

---

## Observation Formula

```
# Direct read from SSRI E-layer + P-layer:
social_bonding = 0.60 * SSRI.f02_social_bonding_index[E1]  # index [1]
               + 0.40 * SSRI.endorphin_proxy[P1]            # index [8]

# f02 = sigma(0.25 * coupling_mean_5s
#            + 0.25 * mean_roughness_500ms_inv
#            + 0.20 * f01_synchrony_reward
#            + 0.15 * loudness_trend_5s
#            + 0.15 * mean_warmth_1s)
# endorphin_proxy = sigma(0.40 * f02 + 0.30 * f03 + 0.30 * coupling_mean_5s)
```

No prediction -- observe-only appraisal. The value tracks cumulative bonding strength over the course of musical interaction.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SSRI E1 | f02_social_bonding_index [1] | Social bonding strength proxy |
| SSRI P1 | endorphin_proxy [8] | Endorphin release estimate |
| H3 | (25, 20, 1, 0) | Coupling mean at 5s LTI |
| H3 | (8, 20, 18, 0) | Loudness trend at 5s LTI |
| H3 | (12, 16, 1, 2) | Mean warmth at 1s |

---

## Kernel Usage

Social bonding feeds downstream memory and emotion functions:

```python
# Phase 3 in scheduler:
# Bonding enhances social memory encoding
social_memory_boost = 0.3 * ssri_relay['social_bonding']
# Bonding modulates emotional valence
emotional_modulation = 0.2 * ssri_relay['social_bonding']
```

---

## Scientific Foundation

- **Ni, Yang & Ma 2024**: Social bonding selectively increases prefrontal neural synchronization in inter-status dyads; d=0.85 (fNIRS, N=528)
- **Tarr, Launay & Dunbar 2014**: Synchronized dancing increases social bonding + pain threshold vs. asynchronous; d~0.62 (behavioral, N=94)
- **Williamson & Bonshor 2019**: Brass band group music enhances physical, psychological, social wellbeing (survey, N=346)
- **Nguyen et al. 2023**: Music as earliest form of interpersonal communication; ID singing promotes co-regulation and bonding (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ssri.py`
