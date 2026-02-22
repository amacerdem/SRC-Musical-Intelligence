# STAI M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [4:6]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | M0:aesthetic_value | [0, 1] | Composite aesthetic function. Aesthetic(t) = alpha * Spectral(t) + beta * Temporal(t) + gamma * (Spectral x Temporal). alpha=0.35, beta=0.35, gamma=0.30 (sum=1.0). Kim 2019: both-intact = full response, one-disrupted = partial (~0.35), both-disrupted = minimal (~0). Cheung 2019: uncertainty x surprise interaction predicts pleasure (R2=0.476). |
| 5 | M1:spectral_temporal_interaction | [0, 1] | Pure interaction term: f01 * f02. Multiplicative binding strength between spectral and temporal integrity. Kim 2019: interaction loci at R ACC (T=6.852), R Caudate/NAc (T=6.603), L Thalamus (T=5.964), R PCC (T=5.663), all p<10^-5. The interaction explains variance beyond additive spectral + temporal main effects. |

---

## Design Rationale

1. **Aesthetic Value (M0)**: The core mathematical model of spectral-temporal aesthetic integration. Implements the linear combination: `Aesthetic = 0.35*Spectral + 0.35*Temporal + 0.30*Interaction`. The equal weighting of spectral and temporal main effects (0.35 each) reflects the Kim 2019 finding that neither dimension dominates. The interaction weight (0.30) captures the essential finding that the combined disruption effect exceeds the sum of individual disruptions. The condition hierarchy maps to: both-intact (1.0), one-disrupted (~0.35), both-disrupted (~0).

2. **Spectral-Temporal Interaction (M1)**: The isolated interaction term (f01 * f02) provides the pure multiplicative binding strength. This is the critical component that distinguishes STAI from simple additive models. When both dimensions are intact, this term is high; when either is disrupted, it collapses toward zero. Maps to the fMRI interaction contrasts in vmPFC, ACC, caudate/NAc, thalamus, and PCC. This term drives the downstream aesthetic response and connectivity predictions.

---

## Mathematical Formulation

```
Aesthetic Integration Model (Kim 2019):
  Aesthetic(t) = alpha * Spectral(t) + beta * Temporal(t) + gamma * (Spectral(t) x Temporal(t))

Parameters:
  alpha = 0.35   (spectral weight)
  beta  = 0.35   (temporal weight)
  gamma = 0.30   (interaction weight)
  alpha + beta + gamma = 1.0

Condition hierarchy:
  Both intact:     A = 0.35 + 0.35 + 0.30 = 1.0  (maximum)
  Spectral only:   A = 0.35 + 0.0  + 0.0  = 0.35 (partial)
  Temporal only:   A = 0.0  + 0.35 + 0.0  = 0.35 (partial)
  Both disrupted:  A = 0.0  + 0.0  + 0.0  = 0.0  (minimal)

Connectivity function:
  vmPFC_IFG(t) = 0.72 * Aesthetic(t)
  where 0.72 = mean(d=0.709, d=0.735) from Kim et al. 2019

Brain region mapping:
  STG(t)      proportional to Spectral(t)        -- auditory cortex (additive)
  NAcc(t)     proportional to Temporal(t)         -- reward circuit (additive)
  vmPFC-IFG(t) proportional to Spectral x Temporal -- integration (interaction)
```

---

## H3 Dependencies (M-Layer)

No additional H3 tuples beyond those consumed by the E-layer. The M-layer operates on E-layer outputs (f01, f02) to compute the aesthetic function and interaction term.

| Source | Feature | Purpose |
|--------|---------|---------|
| E0:f01 | spectral_integrity | Spectral main effect input |
| E1:f02 | temporal_integrity | Temporal main effect input |
| E0 x E1 | f01 * f02 | Interaction computation |

---

## Scientific Foundation

- **Kim et al. 2019**: 2x2 factorial interaction in vmPFC, NAc, caudate, putamen, ACC, thalami. R ACC T=6.852, R Caudate/NAc T=6.603, L Thalamus T=5.964, R PCC T=5.663 (fMRI, N=23, all p<10^-5). Behavioral interaction d=0.709 (Exp I), d=0.735 (Exp II)
- **Cheung et al. 2019**: Uncertainty x surprise interaction predicts pleasure beyond main effects; amygdala, hippocampus, auditory cortex reflect interaction (fMRI, N=39+40, R2_marginal=0.476)
- **Gold et al. 2023**: VS integrates uncertainty x surprise x liking interactions; R STG + VS reflect pleasure (fMRI, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/stai/temporal_integration.py`
