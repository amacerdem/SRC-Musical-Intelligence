# MCCN — Extraction

**Model**: Musical Chills Cortical Network
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_theta_prefrontal | Right prefrontal theta power increase during chills. σ(0.35 * theta_periodicity_100ms + 0.30 * mean_coupling_1s). Chabin 2020: RPF theta F(2,15) = 3.28, p = 0.049; post hoc p = 0.046. Prefrontal theta increase is the excitatory signature of musical chills (HD-EEG, N = 18). |
| 1 | f02_theta_central | Central theta power decrease (inverse) during chills. σ(0.40 * (1 - theta_periodicity_100ms) + 0.30 * roughness_std_1s). Chabin 2020: RC theta F(2,15) = 4.09, p = 0.025; RT theta F(2,15) = 5.88, p = 0.006. Central/temporal theta decrease contrasts with prefrontal increase. |
| 2 | f03_arousal_index | Physiological arousal index from beta/alpha ratio proxy. σ(0.35 * energy_velocity_500ms + 0.30 * rms_energy_100ms). Chabin 2020: beta/alpha ratio F(2,15) = 4.77, p = 0.014. Increased arousal reflects sympathetic activation during chills (goosebumps, heart rate). |
| 3 | f04_chills_magnitude | Peak chills magnitude. σ(0.35 * peak_loudness_500ms + 0.30 * f01 * f03). Combines peak pleasure intensity with reward-arousal coupling. Chills magnitude is high only when both prefrontal reward (f01) and physiological arousal (f03) are co-active. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 3 | M0 (value) | L2 (bidi) | Low-band coupling at 100ms — theta proxy |
| 1 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Theta periodicity at 100ms — oscillation tracking |
| 2 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Low-band periodicity at 1s — sustained theta |
| 3 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean low-band coupling over 1s |
| 4 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — instantaneous intensity |
| 5 | 8 | 8 | M4 (max) | L2 (bidi) | Peak loudness over 500ms — chills trigger peak |
| 6 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s — baseline |
| 7 | 7 | 8 | M8 (velocity) | L2 (bidi) | Amplitude velocity at 500ms — crescendo rate |
| 8 | 7 | 16 | M2 (std) | L2 (bidi) | Amplitude variability over 1s — dynamic range |
| 9 | 9 | 3 | M0 (value) | L2 (bidi) | RMS energy at 100ms — arousal correlate |
| 10 | 9 | 8 | M8 (velocity) | L2 (bidi) | Energy velocity at 500ms — arousal buildup |
| 11 | 9 | 16 | M1 (mean) | L2 (bidi) | Mean energy over 1s — sustained activation |
| 12 | 0 | 8 | M1 (mean) | L2 (bidi) | Mean roughness over 500ms — tension tracking |
| 13 | 0 | 16 | M2 (std) | L2 (bidi) | Roughness variability over 1s — tension dynamics |
| 14 | 21 | 8 | M0 (value) | L2 (bidi) | Spectral deviation at 500ms — surprise event |
| 15 | 22 | 8 | M8 (velocity) | L2 (bidi) | Energy change velocity at 500ms — dynamic shift |

---

## Computation

The E-layer extracts four features characterizing the cortical chills network from Chabin et al. (2020). Two parallel pathways compute theta oscillation signatures and physiological arousal, which are then integrated into a chills magnitude signal.

1. **Theta pathway (f01, f02)**: Captures the characteristic theta oscillation contrast of chills — right prefrontal theta increase (f01) simultaneous with central/temporal theta decrease (f02). Theta is proxied through x_l0l5 periodicity at 100ms (theta timescale ~5 Hz). Source localization showed OFC (p < 1e-05), insula (p < 1e-06), SMA (p < 1e-07) co-activate with this theta pattern.

2. **Arousal pathway (f03)**: Tracks physiological arousal via energy dynamics. Beta/alpha ratio increase during chills (F(2,15) = 4.77, p = 0.014) is proxied by RMS energy velocity and instantaneous energy level.

3. **Integration (f04)**: Chills magnitude combines peak loudness (acoustic trigger at resolution) with the f01 * f03 product, ensuring chills require co-activation of reward (theta prefrontal) and arousal. Peak loudness captures crescendo peaks that precipitate chills.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [0] | roughness | Tension level (inverse chills) |
| R³ [7] | amplitude | Peak intensity proxy / crescendo detection |
| R³ [8] | loudness | Peak pleasure intensity / chills trigger |
| R³ [9] | rms_energy | Arousal correlate / physiological activation |
| R³ [21] | spectral_change | Musical deviation / surprise events |
| R³ [22] | energy_change | Dynamic shift / crescendo-decrescendo |
| R³ [25:33] | x_l0l5 | Theta oscillation proxy / low-band correlations |
| H³ | 16 tuples (see above) | Multi-scale temporal dynamics for theta + arousal + peaks |
| Chabin 2020 | HD-EEG theta + source localization | Primary electrophysiological evidence (N = 18) |
| Putkinen 2025 | OFC + amygdala MOR during chills | Supporting opioid chills network (PET, N = 15) |
| Salimpoor 2011 | Caudate → NAcc DA during chills | Supporting dopamine mechanism (PET, N = 8) |
