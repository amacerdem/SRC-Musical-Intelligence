# SSPS — Cognitive Present

**Model**: Saddle-Shaped Preference Surface
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | surface_position_state | Current position on the preference surface. Summarizes where the listener currently sits on the saddle-shaped IC x entropy surface as a single present-moment value. surface_position = sigma(0.5 * f03_saddle_position + 0.5 * f04_peak_proximity). Values near 1.0 indicate proximity to an optimal zone peak; values near 0.5 indicate the saddle trough; values near 0.0 indicate distance from both peaks. Cheung 2019: bilateral amygdala/hippocampus and auditory cortex show IC x entropy interaction reflecting surface position. |

---

## H3 Demands

The P-layer does not read additional H3 tuples beyond those consumed by the E-layer. It is computed entirely from E-layer outputs f03 and f04.

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No additional H3 demands (reuses E-layer outputs) |

---

## Computation

The P-layer produces a single present-moment summary of the listener's position on the saddle-shaped preference surface. It combines two E-layer features:

- **f03_saddle_position** (50% weight): Where on the saddle surface the current IC x entropy combination places the listener -- captures the interaction topology.
- **f04_peak_proximity** (50% weight): How close the current position is to an optimal zone peak -- captures the hedonic relevance of the current position.

```
surface_position = sigma(0.5 * f03 + 0.5 * f04)
```

The equal weighting reflects that both the surface position (which zone) and the peak proximity (how optimal) contribute equally to the present-state summary. Sigmoid activation bounds the output to [0, 1].

Unlike IOTMS's trait-level P-layer, SSPS's P-layer is event-driven and time-varying. It tracks the listener's real-time position on the preference surface as the music's IC and entropy properties change moment to moment. The preference assessment window (tau = 2.0s) governs how quickly the surface position updates in response to new acoustic events.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f03 | Saddle position | Which zone on the IC x entropy surface |
| E-layer f04 | Peak proximity | Distance to nearest optimal peak |
| IUCP (intra-unit) | Inverted-U saddle refinement | SSPS.saddle_position refines IUCP preference |
| RPEM (intra-unit) | IC-level for RPE | SSPS.ic_value feeds prediction error computation |
| DAED (intra-unit) | Peak proximity for DA | SSPS.peak_proximity modulates dopamine anticipation |
| LDAC (intra-unit) | Entropy for sensory gating | SSPS.entropy_value feeds sensory-reward gate |
