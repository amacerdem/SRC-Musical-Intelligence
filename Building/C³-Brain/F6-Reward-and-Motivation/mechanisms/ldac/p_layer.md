# LDAC — Cognitive Present

**Model**: Liking-Dependent Auditory Cortex
**Unit**: RPU-γ1
**Function**: F6 Reward & Motivation
**Tier**: γ (Integrative)
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | stg_modulation_state | Current STG modulation level. stg_modulation = σ(0.5 * f04 + 0.5 * f02). Summarizes the present-moment state of pleasure-dependent auditory cortex modulation by equally weighting the continuous tracking signal (f04) and the pleasure gating signal (f02). High values indicate strong reward-driven enhancement of sensory processing; low values indicate suppressed or neutral auditory cortex response. tau_decay = 0.5s reflects rapid continuous tracking (Gold 2023a continuous joystick data). Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

No dedicated H³ tuples for P-layer. This layer operates entirely on E-layer outputs (f02, f04). All temporal dynamics are inherited from the E-layer's H³ demands.

---

## Computation

The P-layer computes a single present-moment summary of the STG modulation state.

**stg_modulation_state** combines the moment-to-moment tracking signal (f04, weight 0.50) with pleasure gating (f02, weight 0.50) through sigmoid activation. The equal weighting reflects that the present modulation state is determined both by the integrated tracking output (which already incorporates liking coupling, gating, and deviation) and by the direct pleasure gating pathway.

The temporal dynamics of this signal follow tau_decay = 0.5s, consistent with Gold et al. 2023a's continuous joystick paradigm showing rapid (sub-second) tracking of liking-dependent auditory cortex modulation. This rapid time constant distinguishes LDAC from slower reward processes (e.g., SSRI endorphin dynamics at tau = 30s).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f02 | pleasure_gating | Direct reward-to-perception pathway strength |
| E-layer f04 | moment_to_moment | Integrated tracking signal combining all E-layer features |
