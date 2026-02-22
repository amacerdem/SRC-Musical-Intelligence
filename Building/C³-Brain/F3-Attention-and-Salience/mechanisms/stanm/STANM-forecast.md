# STANM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid / tanh

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:network_state_pred_1.5s | [0, 1] | Network clustering prediction 1-2s ahead. sigma(0.5*local_clustering + 0.5*f15). Predicts whether the attention network will maintain or reconfigure its topology. Jin 2024: network state transitions predictable from clustering (eta2p=0.526). |
| 9 | F1:lateral_pred_0.75s | [-1, 1] | Hemisphere engagement prediction ~0.75s ahead. lateralization (direct copy). Predicts whether processing will shift toward temporal (left) or spectral (right) dominance. Quasi-static within musical phrases. |
| 10 | F2:compensation_pred_2s | [0, 1] | Processing efficiency prediction ~2s ahead. sigma(0.5*local_clustering + 0.5*coupling_mean_1s). Forecasts compensatory network reconfiguration when one stream is overloaded. Kim 2019: compensation predictable from clustering + coupling (T=6.852). |

---

## Design Rationale

1. **Network State Prediction (F0)**: Forecasts the attention network's topology 1-2s ahead. Combines current local clustering with E-layer network topology to predict whether the network will maintain its current configuration or transition. High values predict stable, efficient clustering; low values predict reconfiguration. Feeds the precision engine for attention-related pi_pred.

2. **Lateral Prediction (F1)**: A direct copy of M-layer lateralization, serving as a hemisphere-engagement forecast. Uses tanh activation for the [-1,1] range. This is quasi-static within musical phrases — large shifts in lateralization occur primarily at phrase boundaries. Used by the kernel for anticipatory resource allocation.

3. **Compensation Prediction (F2)**: Forecasts processing efficiency ~2s ahead by combining local clustering with motor-auditory coupling. When one attention stream is overloaded, the network compensates by recruiting additional resources. High values predict efficient compensation; low values predict degraded processing. Uses coupling_mean_1s as a 1s-horizon integration signal.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 16, 1, 2) | x_l0l5[0] mean H16 L2 | Coupling mean at 1s — compensation forecast |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Coupling periodicity — network stability |
| (25, 3, 0, 2) | x_l0l5[0] value H3 L2 | Coupling value at 100ms — fast dynamics |
| (8, 3, 20, 2) | loudness entropy H3 L2 | Loudness entropy — complexity signal |
| (8, 16, 1, 2) | loudness mean H16 L2 | Mean loudness at 1s — baseline context |

F-layer primarily reuses E+M outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:network_state_pred_1.5s | Precision engine | pi_pred for attention-related beliefs |
| F1:lateral_pred_0.75s | Kernel scheduler | Anticipatory L/R resource allocation |
| F2:compensation_pred_2s | F8 Learning | Efficiency prediction for plasticity gating |

---

## Scientific Foundation

- **Jin et al. 2024**: Network state transitions predictable from clustering topology (eta2p=0.526, fMRI)
- **Kim et al. 2019**: Compensation predictable from clustering + coupling strength (T=6.852)
- **Zatorre et al. 2022**: Lateralization shifts at phrase boundaries (review)
- **Norman-Haignere et al. 2022**: Frequency-selective attention dynamics in real-time (iEEG, F=104.71)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/stanm/forecast.py`
