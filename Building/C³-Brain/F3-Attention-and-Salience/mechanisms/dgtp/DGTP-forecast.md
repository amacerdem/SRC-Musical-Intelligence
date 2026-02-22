# DGTP F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: ASU-gamma2, Domain-General Temporal Processing (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:cross_domain_pred | [0, 1] | Speech-to-music transfer prediction. sigma(0.5*f24 + 0.5*coupling_mean_1s). Predicts how well timing skills in one domain will transfer to the other. Dalla Bella 2024: ML models predict cross-domain timing ability. |
| 8 | F1:training_transfer_pred | [0, 1] | Intervention plasticity prediction. sigma(0.5*f24 + 0.5*domain_correlation). Predicts whether rhythmic training will generalize across modalities. Di Stefano 2025: training transfer depends on shared mechanism strength. |

---

## Design Rationale

1. **Cross-Domain Prediction (F0)**: Forecasts the degree of speech-to-music (or music-to-speech) timing transfer. Combines the shared mechanism (f24, geometric mean) with sustained coupling baseline. This predicts: "given current shared timing, how much will improving one domain improve the other?"

2. **Training Transfer Prediction (F1)**: Forecasts plasticity of the domain-general system under intervention. Combines the shared mechanism with domain correlation — high values predict that rhythmic training (e.g., musical training) will produce broad temporal processing improvements across speech, motor, and cognitive timing tasks.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 16, 1, 0) | x_l0l5[0] mean H16 L0 | Coupling mean 1s — baseline for transfer prediction |

F-layer primarily reuses E+M outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:cross_domain_pred | F8 Learning | Transfer learning estimation |
| F0:cross_domain_pred | F9 Social | Communication timing prediction |
| F1:training_transfer_pred | F8 Learning | Plasticity estimation for training protocols |
| F1:training_transfer_pred | F11 Development (meta) | Developmental timing trajectories |

---

## Full H3 Demand (9 tuples, all layers)

| Tuple | Feature | Layer |
|-------|---------|-------|
| (10, 3, 0, 2) | spectral_flux value H3 L2 | E |
| (10, 3, 17, 2) | spectral_flux periodicity H3 L2 | E |
| (10, 16, 17, 2) | spectral_flux periodicity H16 L2 | E |
| (11, 13, 8, 0) | onset_strength velocity H13 L0 | E |
| (11, 13, 11, 0) | onset_strength trend H13 L0 | E |
| (25, 16, 1, 0) | x_l0l5[0] mean H16 L0 | M, F |
| (25, 16, 2, 0) | x_l0l5[0] std H16 L0 | M |
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | E, M, P |
| (25, 3, 17, 2) | x_l0l5[0] periodicity H3 L2 | E |

---

## Scientific Foundation

- **Dalla Bella 2024**: ML classifiers predict cross-domain timing ability from shared features
- **Di Stefano 2025**: Training transfer depends on shared mechanism strength
- **Liu 2025**: D2-MSNs in striatum encode domain-general timing — pharmacological manipulation affects both domains
- **Rathcke 2024**: Domain-general timing mechanisms — theoretical framework for transfer

## Brain Regions

SMA/Pre-SMA, Putamen, R dPMC (causal TMS), IFG, IPL, Cerebellum, STG, ACC

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/dgtp/forecast.py` (pending)
