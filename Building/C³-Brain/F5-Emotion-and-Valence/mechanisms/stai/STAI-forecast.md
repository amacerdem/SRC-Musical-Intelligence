# STAI F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [9:12]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:aesthetic_rating_pred | [0, 1] | Predicted end-of-piece aesthetic rating from accumulated integration. f_rating = sigma(0.5 * aesthetic_value + 0.5 * f03). Cheung 2019: accumulated uncertainty x surprise interaction drives overall pleasure judgment (R2_marginal=0.476); Gold 2019: end-of-piece liking predicted by IC x entropy trajectory (p<0.05). |
| 10 | F1:reward_response_pred | [0, 1] | NAcc/putamen activation prediction (2-5s ahead). Predicts reward circuit engagement from temporal integrity trajectory. f_reward = sigma(0.6 * f02 + 0.4 * f04). Kim 2019: temporal disruption reduces NAcc/putamen/GP; temporal integrity trajectory predicts reward response (behavioral d=-1.433 to -1.635). |
| 11 | F2:connectivity_pred | [0, 1] | vmPFC-IFG coupling prediction (1-3s ahead). Predicts aesthetic integration pathway strength. f_connect = sigma(0.5 * f04 + 0.5 * aesthetic_periodicity). Kim 2019: vmPFC-IFG connectivity varies with spectral x temporal integrity (PPI analysis); Teixeira Borges 2019: cortical scaling dynamics predict pleasure trajectory (r=0.37-0.42). |

---

## Design Rationale

1. **Aesthetic Rating Prediction (F0)**: Forecasts the overall aesthetic rating that would emerge from the accumulated integration over the piece. Combines the mathematical aesthetic value (M0) with the E-layer integration (f03). As the listener accumulates evidence about both spectral quality and temporal flow, this prediction converges toward the end-of-piece judgment. Maps to the Cheung 2019 finding that accumulated uncertainty x surprise determines overall pleasure.

2. **Reward Response Prediction (F1)**: Predicts upcoming NAcc/putamen engagement. Weighted toward temporal integrity (f02, 0.6) over connectivity (f04, 0.4) because the reward circuit is primarily driven by temporal predictability in Kim 2019. When temporal flow is intact and consistent, reward circuit engagement is predicted to be high. Conversely, temporal disruption predicts reduced reward response.

3. **Connectivity Prediction (F2)**: Forecasts the strength of vmPFC-IFG functional connectivity over the next few seconds. Uses the current connectivity estimate (f04) and the aesthetic periodicity (H3 binding periodicity) to predict whether the integration pathway will strengthen or weaken. When aesthetic binding shows periodic structure, connectivity is predicted to remain stable. Maps to the PPI analysis finding from Kim 2019 and the cortical scaling dynamics from Teixeira Borges 2019.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (33, 8, 14, 2) | x_l4l5[0] periodicity H8 L2 | Binding periodicity for connectivity trajectory |

F-layer primarily reuses E-layer and M-layer outputs (f01-f04, aesthetic_value) rather than reading new H3 tuples directly. The binding periodicity tuple provides the temporal structure needed for connectivity prediction.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:aesthetic_rating_pred | ARU.SRP | Pleasure modulation from aesthetic prediction |
| F1:reward_response_pred | ARU.SRP | Reward circuit engagement prediction for PE estimation |
| F2:connectivity_pred | Precision engine | pi_pred for aesthetic integration processing |

---

## Scientific Foundation

- **Cheung et al. 2019**: Accumulated uncertainty x surprise interaction drives pleasure; amygdala/hippocampus reflect trajectory (fMRI, N=39+40, R2_marginal=0.476)
- **Gold et al. 2019**: End-of-piece liking predicted by IC x entropy trajectory; inverted-U maintained across repetitions (behavioral + IDyOM, N=43+27, p<0.05)
- **Kim et al. 2019**: Temporal disruption reduces NAcc/putamen/GP; vmPFC-IFG connectivity varies with spectral x temporal integrity (fMRI, N=16+23, PPI analysis; behavioral d=-1.433 to -1.635)
- **Teixeira Borges et al. 2019**: 1/f scaling in temporal cortex predicts pleasure; music-induced cortical scaling dynamics mediate pleasure trajectory (EEG+ECG, N=28, r=0.37-0.42)
- **Gold et al. 2023**: VS integrates uncertainty x surprise x liking interactions; R STG reflects liking trajectory (fMRI, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/stai/forecast.py`
