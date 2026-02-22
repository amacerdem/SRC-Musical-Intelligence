# SDL M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: mixed (tanh for lateralization index, sigmoid for salience demand)
**Model**: ASU-gamma3, Salience-Dependent Lateralization (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:lateralization_index | [-1, 1] | Hemispheric balance index. tanh(0.5*f25 + 0.5*(centroid_value - flux_value)). Combines E-layer dynamic lateralization with raw spectral-temporal contrast. Positive = right hemisphere dominant (spectral), negative = left hemisphere dominant (temporal). Kim 2019: T=6.85 for lateralization in pitch vs rhythm tasks. |
| 4 | M1:salience_demand | [0, 1] | Processing challenge level. sigma(0.5*loudness_entropy_1s). Quantifies how much processing demand the current stimulus places on the auditory system. High entropy = degraded/complex signal requiring bilateral recruitment. Albouy 2020: degradation drives bilateral compensation. |

---

## Design Rationale

1. **Lateralization Index (M0)**: The integrated hemispheric balance — combines the E-layer f25 signal with a direct spectral-temporal contrast (centroid_value - flux_value). The tanh activation maintains the signed [-1, 1] range. This is the core computational model: at each moment, the auditory scene's spectral/temporal balance determines which hemisphere leads processing. Kim 2019 showed T=6.85 effect for pitch (right) vs rhythm (left) lateralization.

2. **Salience Demand (M1)**: Quantifies the processing challenge. Uses loudness entropy at 1s as a proxy for signal degradation and complexity. When salience demand is high, the lateralization pattern shifts toward bilateral processing (clustering compensation). This modulates the lateralization index — high demand reduces lateralization magnitude.

---

## Mathematical Formulation

```
lateralization_index = tanh(0.5 * f25 + 0.5 * (centroid_value - flux_value))

  f25 = dynamic_lateral (E-layer)
  centroid_value from H3 tuple (15, 3, 0, 2)
  flux_value from H3 tuple (10, 3, 0, 2)

salience_demand = sigma(0.5 * loudness_entropy_1s)

  loudness_entropy_1s from H3 tuple (8, 16, 20, 2)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (15, 3, 0, 2) | spectral_centroid value H3 L2 | Centroid for spectral-temporal contrast (shared with E-layer) |
| (10, 3, 0, 2) | spectral_flux value H3 L2 | Flux for spectral-temporal contrast (shared with E-layer) |
| (8, 16, 20, 2) | loudness entropy H16 L2 | Loudness entropy 1s for salience demand (shared with E-layer) |

---

## Scientific Foundation

- **Kim 2019**: T=6.85 for lateralization differences in pitch vs rhythm tasks (fMRI, N=24)
- **Albouy 2020**: Double dissociation — degradation drives bilateral compensation (fMRI, N=40)
- **Zatorre 2022**: AST model — lateralization determined by spectral/temporal feature balance

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/sdl/temporal_integration.py` (pending)
