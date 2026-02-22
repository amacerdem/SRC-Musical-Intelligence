# SSRI — Cognitive Present

**Model**: Social Synchrony Reward Integration
**Unit**: RPU-β4
**Function**: F6 Reward & Motivation
**Tier**: β (Bridging)
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | prefrontal_coupling | Current rDLPFC/rTPJ synchronization state. prefrontal_coupling = σ(0.40 * f04 + 0.30 * coupling_500ms). Estimates the degree of inter-brain prefrontal synchronization from the acoustic correlates of coordinated music-making. Ni et al. 2024: social bonding increases rDLPFC neural synchronization (fNIRS hyperscanning, N=528, d = 0.85). Range [0, 1]. |
| 8 | endorphin_proxy | Endorphin release estimate from sustained coordinated activity. endorphin_proxy = σ(0.40 * f02 + 0.30 * f03 + 0.30 * coupling_mean_5s). Models the slow-building beta-endorphin release associated with synchronized group music-making, which mediates social bonding and pain threshold elevation. Dunbar 2012: synchronized music-making increases endorphin release (pain threshold proxy, d ~ 0.60-0.80). tau_endorphin = 30.0s. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 8 | M0 (value) | L2 (bidi) | Coupling at 500ms — current consonance-energy interaction state |
| 1 | 25 | 20 | M1 (mean) | L0 (fwd) | Coupling mean 5s LTI — sustained coordination for endorphin dynamics |

---

## Computation

The P-layer estimates two present-moment neural states that characterize the social reward experience.

**prefrontal_coupling** models the current level of inter-brain prefrontal synchronization. It combines entrainment_quality (f04, weight 0.40) as the primary driver of neural alignment, with the current consonance-energy coupling state at 500ms (weight 0.30). This reflects the fNIRS hyperscanning finding that coordinated music-making produces measurable inter-brain synchronization in rDLPFC and rTPJ, with leader-to-follower unidirectional alignment at +1 to +6s lag (Ni et al. 2024).

**endorphin_proxy** models the slow-building beta-endorphin release from sustained synchronized activity. It combines social_bonding_index (f02, weight 0.40) as the primary driver, group_flow_state (f03, weight 0.30) as a flow-dependent amplifier, and coupling_mean_5s (weight 0.30) as a long-range sustained coordination signal. The endorphin dynamics operate with tau_endorphin = 30.0s, reflecting the slow timescale of opioid release compared to dopaminergic reward (Tarr, Launay & Dunbar 2014: synchronized dancing elevates pain threshold, d ~ 0.62).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f02 | social_bonding_index | Primary driver of endorphin release |
| E-layer f03 | group_flow_state | Flow-dependent amplification of endorphin dynamics |
| E-layer f04 | entrainment_quality | Primary driver of prefrontal coupling |
| H³ (25, 8, 0, 2) | coupling_500ms | Current consonance-energy interaction state |
| H³ (25, 20, 1, 0) | coupling_mean_5s | Sustained coordination for slow endorphin buildup |
