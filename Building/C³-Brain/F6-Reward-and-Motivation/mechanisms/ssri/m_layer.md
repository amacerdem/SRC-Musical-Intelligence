# SSRI — Temporal Integration

**Model**: Social Synchrony Reward Integration
**Unit**: RPU-β4
**Function**: F6 Reward & Motivation
**Tier**: β (Bridging)
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | social_prediction_error | Social reward prediction error (SPE). Coordination quality vs expectation. SPE = f04 - mean(expect_surprise[10:20]). Positive SPE indicates better-than-expected coordination producing a reward surge; negative SPE signals coordination breakdown and reward suppression. Extends RPEM's individual RPE to interpersonal coordination. Cheung et al. 2019: uncertainty x surprise interaction predicts musical pleasure. Range [-1, 1]. |
| 6 | synchrony_amplification | Ratio of social reward to solo listening baseline. SA = 1.0 + f01 * (f04 + f02). Captures the multiplicative reward boost from successful group coordination. Ranges from 1.0 (no amplification, solo baseline) to approximately 3.0 (maximum social amplification). Estimated from the 1.3-1.8x range reported for group vs solo music-making (kappa_social = 0.60). Range [0, 3]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

No dedicated H³ tuples for M-layer. This layer operates entirely on E-layer outputs (f01, f02, f04) and upstream belief state (expect_surprise). All temporal dynamics are inherited from the E-layer's H³ demands.

---

## Computation

The M-layer computes two mathematical model outputs that quantify the social reward dynamics.

**social_prediction_error** implements a social extension of reward prediction error. It subtracts the expected coordination quality (derived from the anticipation belief expect_surprise[10:20] mean) from the actual entrainment quality (f04). The result passes through tanh to bound it to [-1, 1]. Positive SPE triggers a reward surge in downstream mesolimbic targets (NAcc, VTA); negative SPE suppresses reward. This extends RPEM's individual prediction error framework to interpersonal coordination.

**synchrony_amplification** provides a multiplicative scaling factor. Starting from a solo baseline of 1.0, it adds the product of synchrony_reward (f01) with the sum of entrainment_quality (f04) and social_bonding_index (f02). This captures the key empirical finding that group music-making amplifies hedonic reward by 1.3-1.8x compared to solitary listening, implemented with kappa_social = 0.60.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | synchrony_reward | Core reward signal for amplification computation |
| E-layer f02 | social_bonding_index | Bonding contribution to amplification ratio |
| E-layer f04 | entrainment_quality | Actual coordination quality for SPE computation |
| Belief state | expect_surprise[10:20] | Expected coordination quality for SPE baseline |
