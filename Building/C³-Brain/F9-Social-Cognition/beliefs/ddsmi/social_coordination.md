# social_coordination — Core Belief (DDSMI)

**Category**: Core (full Bayesian PE)
**tau**: 0.60
**Owner**: DDSMI (MPU-beta2)
**Multi-Scale**: single-scale in v1.0, T_char = 8s

---

## Definition

"Tracking partner's movements." Tracks how effectively the brain maintains simultaneous neural representations of self-movement, partner observation, and social coordination during dyadic musical interaction. High values indicate tight partner tracking with strong social coordination mTRF responses -- the brain is successfully integrating auditory, motor, and visual streams to coordinate with another person.

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. When activated (waves 3-5):

```
T_char = 8s (Macro band)
```

T_char = 8s reflects the characteristic timescale of partner coordination accumulation. Dyadic coordination builds over musical phrases as partners progressively align their motor plans, gestural timing, and intentional states.

---

## Observation Formula

```
# DDSMI mechanism outputs:
value = 0.50 * f13_social_coordination + 0.30 * partner_sync + 0.20 * mTRF_social

# f13 = sigma(0.40 * social_period_1s + 0.30 * social_period_500ms + 0.30 * social_coupling_100ms)
# partner_sync = P-layer social synchronization level
# mTRF_social = social coordination mTRF weight

# Precision: 1/(std(f13, partner_sync, mTRF_social) + 0.1)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DDSMI E0 | f13_social_coordination [0] | Primary social coordination |
| DDSMI P0 | partner_sync [6] | Partner synchronization level |
| DDSMI M0 | mTRF_social [3] | Social coordination mTRF weight |
| H3 | (33, 16, 14, 2) | Social coupling periodicity at 1s (x_l4l5) |
| H3 | (33, 8, 14, 2) | Social coupling periodicity at 500ms |
| H3 | (33, 3, 0, 2) | Social coupling value at 100ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F7 Motor | Partner tracking feeds motor planning for coordination |
| F6 Reward | PE from social coordination feeds reward formula |
| F3 Attention | Social coordination modulates attentional resource allocation |
| Precision engine | pi_pred estimation from coordination stability |

---

## Scientific Foundation

- **Bigand et al. 2025**: mTRF disentangles 4 parallel processes during dyadic dance; social coordination with visual contact F(1,57)=249.75, p<.001 (dual-EEG, N=70)
- **Kohler et al. 2025**: Self-produced actions in left M1, other-produced in right PMC during joint piano; MVPA above chance (fMRI, N=36)
- **Wohltjen et al. 2023**: Beat entrainment predicts social synchrony; d=1.37 (behavioral+pupillometry, N=198)
- **Yoneta et al. 2022**: Leader/follower roles modulate inter-brain coupling in cooperative music (MEG hyperscanning)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/beliefs/social_coordination.py`
