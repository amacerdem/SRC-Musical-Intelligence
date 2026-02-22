# IOTMS — Cognitive Present

**Model**: Individual Opioid Tone Music Sensitivity
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | individual_sensitivity_state | Current individual sensitivity state. Summarizes the listener's trait-level music reward sensitivity as a single present-moment value. individual_sensitivity = sigma(0.5 * f01_mor_baseline_proxy + 0.5 * f03_reward_propensity). Equal-weighted blend of MOR baseline (neurochemical trait) and reward propensity (behavioral trait). Putkinen 2025: individual MOR tone modulates pleasure response magnitude. |

---

## H3 Demands

The P-layer does not read additional H3 tuples beyond those consumed by the E-layer. It is computed entirely from E-layer outputs f01 and f03.

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No additional H3 demands (reuses E-layer outputs) |

---

## Computation

The P-layer produces a single present-moment summary of the individual's music reward sensitivity. It combines two E-layer features:

- **f01_mor_baseline_proxy** (50% weight): The neurochemical foundation -- how much endogenous opioid is available for music-induced pleasure.
- **f03_reward_propensity** (50% weight): The behavioral expression -- how strongly the individual tends to experience music reward given their coupling dynamics.

```
individual_sensitivity = sigma(0.5 * f01 + 0.5 * f03)
```

The equal weighting reflects that both neurochemical availability (MOR tone) and behavioral tendency (reward propensity) contribute equally to the current sensitivity state. Sigmoid activation bounds the output to [0, 1].

This is a trait-level feature that changes slowly -- it represents a stable individual difference in music reward sensitivity rather than a time-varying event signal. Frame-to-frame variation reflects only the slow temporal dynamics of the underlying H3 features at H8/H16 horizons.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | MOR baseline proxy | Neurochemical component of individual sensitivity |
| E-layer f03 | Reward propensity | Behavioral component of individual sensitivity |
| MORMR (intra-unit) | MOR-mediated opioid release scaling | IOTMS.mor_baseline modulates MORMR output |
| DAED (intra-unit) | DA coupling strength | IOTMS.pleasure_bold_slope feeds DAED anticipation |
| RPEM (intra-unit) | RPE magnitude | IOTMS.reward_propensity scales prediction error |
| MCCN (intra-unit) | Chills susceptibility | IOTMS.music_reward_index modulates chills threshold |
| ARU (cross-unit) | Affect gain | IOTMS.individual_sensitivity modulates ARU affect gain |
