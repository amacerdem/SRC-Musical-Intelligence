# Statistical Learning Model Persistence

**Source**: NDU-β3-SLEE (Statistical Learning Expertise Enhancement)
**Unit**: NDU (Novelty Detection Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Differential equation with long persistence

---

## Scientific Basis

- Statistical learning: implicit acquisition of distributional patterns
- d=-1.09 effect size for enhanced detection
- τ=3.0s persistence window

## Mechanism

The brain builds a statistical model of recent stimulus distributions.
This model persists with τ=3.0s decay and enables deviance detection
against the learned distribution.

### Formula

```
dModel/dt = τ^(-1) · (Current_Distribution - Statistical_Model)
τ = 3.0s (persistence window)

StatisticalLearning(t) = DistributionModel(t) × DetectionGating(t) × ExpertiseBoost(t)

Discrete-time:
  Model[t] = Model[t-1] + (1/τ) · (Distribution[t] - Model[t-1])
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Current_Distribution | R³/H³ features | Current spectral/temporal distribution |
| Model[t-1] | State | Previous statistical model |
| ExpertiseBoost | Training level | Expertise enhancement factor |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| Statistical_Model | continuous | Running distributional model |
| Detection | [0, 1] | Deviance from learned model |

## Why 7/10

- Differential equation with τ=3.0s (longer than CDMR's 0.4s)
- State variable: Statistical_Model evolves with exposure
- Captures implicit learning of musical regularities
- Expertise enhancement is multiplicative
- Long persistence enables phrase-level pattern learning
