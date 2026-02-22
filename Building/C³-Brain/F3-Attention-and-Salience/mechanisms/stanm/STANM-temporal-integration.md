# STANM M-Layer — Temporal Integration (3D)

**Layer**: Mathematical Model (M)
**Indices**: [3:6]
**Scope**: internal
**Activation**: sigmoid / tanh

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:network_topology | [0, 1] | Full network configuration. sigma(0.4*f13 + 0.4*f14 + 0.2*f15). Integrates temporal attention, spectral attention, and local clustering into unified network state. Jin 2024: combined network topology predicts attention performance (eta2p=0.526). |
| 4 | M1:local_clustering | [0, 1] | Local clustering coefficient. sigma(0.5*f15 + 0.5*energy_var_500ms). Measures how tightly interconnected local processing nodes are — high values indicate efficient local computation with short-range connections. |
| 5 | M2:lateralization | [-1, 1] | Hemisphere balance. tanh(0.5*(f14-f13)). Positive = right-dominant (spectral/melodic), negative = left-dominant (temporal/rhythmic). Zatorre 2022: spectral-temporal dissociation maps to R/L hemispheres. |

---

## Design Rationale

1. **Network Topology (M0)**: The integrated network configuration combining all three E-layer streams. Temporal and spectral attention are weighted equally (0.4 each) while topology receives lower weight (0.2) as a modulatory input. This unified state captures the overall attentional configuration at any moment.

2. **Local Clustering (M1)**: Quantifies local network efficiency — how much processing happens through short-range connections vs long-range connections. High clustering means nearby nodes share information efficiently. Combines E-layer network topology with raw energy variability for a robust clustering estimate.

3. **Lateralization (M2)**: The hemisphere-balance signal. Uses tanh for the [-1,1] range where positive values indicate right-hemisphere dominance (spectral/melodic processing) and negative values indicate left-hemisphere dominance (temporal/rhythmic processing). The f14-f13 difference directly captures the spectral-vs-temporal attention balance.

---

## Mathematical Formulation

```
Network_Topology = sigma(alpha*Temporal_Attention + beta*Spectral_Attention + gamma*Local_Topology)

Parameters:
  alpha = 0.4 (temporal weight)
  beta  = 0.4 (spectral weight)
  gamma = 0.2 (topology weight)

Local_Clustering = sigma(delta*E2_topology + epsilon*energy_var)

Parameters:
  delta   = 0.5 (topology weight)
  epsilon = 0.5 (energy variability weight)

Lateralization = tanh(kappa * (Spectral_Attention - Temporal_Attention))

Parameters:
  kappa = 0.5 (scaling factor)

Properties:
  lateralization > 0: right-dominant (spectral/melodic)
  lateralization < 0: left-dominant (temporal/rhythmic)
  lateralization ~ 0: balanced bilateral processing
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 0, 0, 2) | spectral_flux value H0 L2 | Instantaneous onset at 25ms — fast temporal tracking |
| (10, 3, 1, 2) | spectral_flux mean H3 L2 | Mean onset at 100ms — sustained temporal |
| (21, 1, 8, 0) | spectral_change velocity H1 L0 | Spectral change velocity at 50ms — fast dynamics |
| (22, 8, 2, 0) | energy_change std H8 L0 | Energy variability at 500ms — clustering input |

---

## Scientific Foundation

- **Jin et al. 2024**: Network topology predicts attention performance (eta2p=0.526, fMRI)
- **Zatorre et al. 2022**: Spectral-temporal dissociation maps to R/L hemispheres (review)
- **Haiduk et al. 2024**: L AC temporal preference confirmed (fMRI, p<0.001)
- **Kim et al. 2019**: Network clustering correlates with attention efficiency (T=6.852)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/stanm/temporal_integration.py`
