# MCCN — Cognitive Present

**Model**: Musical Chills Cortical Network
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | network_state | Distributed cortical network activation level. σ(0.5 * f04 + 0.5 * f03). Integrates chills magnitude and arousal to estimate overall OFC + insula + SMA + STG network activation. Chabin 2020: all four regions co-activated during chills (LAURA source localization, all p < 1e-05). High values indicate the full chills circuit is engaged. |
| 1 | theta_pattern | Prefrontal-central theta contrast. σ(0.5 * f01 + 0.5 * f02). Captures the characteristic theta oscillation signature: simultaneous prefrontal increase + central decrease. Chabin 2020: RPF theta up (p = 0.049) while central/temporal theta down (p = 0.006). This is the EEG biomarker of chills, distinct from overall network magnitude. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Theta periodicity 100ms — via f01, f02 |
| 1 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean coupling 1s — via f01 |
| 2 | 8 | 8 | M4 (max) | L2 (bidi) | Peak loudness 500ms — via f04 |
| 3 | 9 | 8 | M8 (velocity) | L2 (bidi) | Energy velocity 500ms — via f03 |
| 4 | 9 | 3 | M0 (value) | L2 (bidi) | RMS energy 100ms — via f03 |
| 5 | 0 | 16 | M2 (std) | L2 (bidi) | Roughness variability 1s — via f02 |

---

## Computation

The P-layer produces two complementary signals characterizing the current chills state:

1. **Network State (P0)**: Overall activation of the distributed cortical chills network (OFC + bilateral insula + SMA + bilateral STG). Combines chills magnitude (f04, integrating peak pleasure and reward-arousal coupling) with arousal index (f03, physiological activation). High network_state means the full cortical circuit is currently engaged. Relevant for downstream reward computation and clinical monitoring.

2. **Theta Pattern (P1)**: The defining electrophysiological biomarker of chills — the theta oscillation contrast (prefrontal increase + central/temporal decrease). Combines f01 (theta prefrontal, excitatory) and f02 (theta central, already inverted). Distinct from network state: theta_pattern tracks the oscillatory signature specifically, while network_state tracks activation magnitude. Theta pattern is the more specific chill identification biomarker.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f01_theta_prefrontal | Prefrontal theta component for theta_pattern |
| E-layer [1] | f02_theta_central | Central theta (inverse) for theta_pattern |
| E-layer [2] | f03_arousal_index | Arousal component for network_state |
| E-layer [3] | f04_chills_magnitude | Peak chills for network_state |
| R³ [25:33] | x_l0l5 | Theta proxy (via f01, f02) |
| R³ [8] | loudness | Peak pleasure (via f04) |
| R³ [9] | rms_energy | Arousal (via f03) |
| R³ [0] | roughness | Tension modulation (via f02) |
| Chabin 2020 | OFC + insula + SMA + STG co-activation | All p < 1e-05 (LAURA, N = 18) |
