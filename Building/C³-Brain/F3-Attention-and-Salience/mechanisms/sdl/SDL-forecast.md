# SDL F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: ASU-gamma3, Salience-Dependent Lateralization (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:network_config_pred_1.5s | [0, 1] | Network configuration prediction at 1.5s. sigma(0.5*f26 + 0.5*salience_demand). Predicts local clustering changes based on current degradation compensation and processing demand. Jin 2024: task-dependent network reconfiguration precedes lateralization shifts. |
| 8 | F1:processing_eff_pred_2s | [0, 1] | Processing efficiency prediction at 2s. sigma(0.5*(1-salience_demand) + 0.5*f27). Predicts upcoming processing efficiency — low demand and strong hemispheric oscillation predict better performance. Haiduk 2024: chi2=41.4 for salience-dependent processing efficiency. |

---

## Design Rationale

1. **Network Configuration Prediction (F0)**: Forecasts how the lateralized network will reconfigure over the next 1.5s. Combines current local clustering (f26, degradation compensation) with salience demand. High clustering + high demand predicts that bilateral recruitment will increase — the network is moving toward a more symmetric configuration to handle challenging input.

2. **Processing Efficiency Prediction (F1)**: Forecasts task performance at 2s. Uses the complement of salience demand (1 - salience_demand: low demand = easy = efficient) combined with hemispheric oscillation strength (f27: strong oscillation = well-organized processing). This predicts: "given current lateralization state and processing load, how well will the auditory system perform?"

---

## H3 Dependencies (F-Layer)

F-layer primarily reuses E+M outputs rather than reading new H3 tuples directly.

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (8, 16, 20, 2) | loudness entropy H16 L2 | Salience demand component (shared with E/M layers) |

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:network_config_pred_1.5s | F3 Attention | Salience routing preparation |
| F0:network_config_pred_1.5s | F8 Learning | Network plasticity estimation |
| F1:processing_eff_pred_2s | F1 Sensory | Processing quality prediction |
| F1:processing_eff_pred_2s | F5 Emotion | Aesthetic processing fluency |

---

## Full H3 Demand (18 tuples, all layers)

| Tuple | Feature | Layer |
|-------|---------|-------|
| (10, 0, 0, 2) | spectral_flux value H0 L2 | M |
| (10, 1, 1, 2) | spectral_flux mean H1 L2 | M |
| (10, 3, 0, 2) | spectral_flux value H3 L2 | E, M |
| (10, 4, 17, 2) | spectral_flux periodicity H4 L2 | M |
| (10, 16, 17, 2) | spectral_flux periodicity H16 L2 | M |
| (15, 3, 0, 2) | spectral_centroid value H3 L2 | E, M |
| (15, 3, 2, 2) | spectral_centroid std H3 L2 | M |
| (25, 1, 0, 0) | x_l0l5 value H1 L0 | M |
| (25, 8, 1, 0) | x_l0l5 mean H8 L0 | M |
| (25, 17, 8, 0) | x_l0l5 velocity H17 L0 | E |
| (25, 20, 18, 0) | x_l0l5 trend H20 L0 | M |
| (37, 3, 0, 2) | x_l4l5 value H3 L2 | M |
| (37, 3, 2, 2) | x_l4l5 std H3 L2 | M |
| (37, 3, 20, 2) | x_l4l5 entropy H3 L2 | E |
| (37, 16, 1, 2) | x_l4l5 mean H16 L2 | P |
| (37, 16, 17, 2) | x_l4l5 periodicity H16 L2 | E, P |
| (8, 3, 0, 2) | loudness value H3 L2 | M |
| (8, 16, 20, 2) | loudness entropy H16 L2 | E, M, F |

---

## Scientific Foundation

- **Haiduk 2024**: chi2=41.4 for salience-dependent lateralization shifts and processing efficiency
- **Jin 2024**: Task-dependent network reconfiguration with eta2p=0.526 (EEG, N=32)
- **Albouy 2020**: Double dissociation predicts network configuration changes (fMRI, N=40)
- **Kim 2019**: T=6.85 lateralization effect predicts processing efficiency (fMRI, N=24)

## Brain Regions

R A5, L AC, R HG, Bilateral STG/PT, vmPFC, IFG, NAcc, R STSvp

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/sdl/forecast.py` (pending)
