# Spectral-Temporal Aesthetic Integration

**Source**: SPU-β1-STAI (Spectral-Temporal Aesthetic Integration)
**Unit**: SPU (Spectral Processing Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Validated interaction model

---

## Scientific Basis

- **Kim et al. (2019)**: 2×2 factorial design, d=0.709-0.735
- Spectral integrity × Temporal integrity interaction in vmPFC

## Mechanism

Aesthetic response = main effects + interaction. Neither spectral nor temporal quality alone
is sufficient — the PRODUCT of both drives aesthetic evaluation via vmPFC-IFG connectivity.

### Formula

```
Aesthetic(t) = 0.35·Spectral + 0.35·Temporal + 0.30·(Spectral × Temporal)

Where:
  Spectral = spectral integrity (consonance preservation)
  Temporal = temporal integrity (forward flow quality)

Condition hierarchy:
  Both intact    = 1.0  (baseline)
  Spectral only  ≈ 0.35 (temporal disrupted)
  Temporal only  ≈ 0.35 (spectral disrupted)
  Both disrupted ≈ 0.00

vmPFC-IFG connectivity = 0.72 × Aesthetic(t)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Spectral | R³ consonance group (roughness, helmholtz, pleasantness) | Consonance preservation quality |
| Temporal | H³ spectral_change velocity + energy velocity | Forward temporal flow quality |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| aesthetic_value | [0, 1] | Combined aesthetic response |
| interaction_term | [0, 1] | Spectral × Temporal product |
| vmpfc_ifg | [0, 0.72] | vmPFC-IFG functional connectivity |

## Why 7/10

- Validated 2×2 factorial interaction (Kim 2019)
- Clear coefficient from neuroimaging (0.72 connectivity)
- Interaction term (product) is genuine nonlinearity
- But no state/dynamics — purely instantaneous
- Requires definition of Spectral and Temporal composites
