# Anticipation-Experience Dissociation

**Source**: RPU-α1-DAED (Dopamine Anticipation-Experience Dissociation)
**Unit**: RPU (Reward Processing Unit)
**Tier**: α (Core)
**Score**: 7/10 — State-dependent temporal phase tracking

---

## Scientific Basis

- **Salimpoor et al. (2011)**: PET, DA release in caudate (anticipation) vs NAcc (experience)
- Wanting (anticipation) and liking (experience) are neurochemically dissociable

## Mechanism

Dopamine release occurs in different brain regions depending on the temporal phase:
- ANTICIPATION phase: caudate DA driven by expected pleasure + uncertainty
- EXPERIENCE phase: NAcc DA driven by actual pleasure + prediction error

### Formula

```
Anticipation (caudate):
  DA_caudate = α · E[Pleasure] + β · Uncertainty
  α = 0.84, β = 0.71

Experience (NAcc):
  DA_nacc = α · Actual_Pleasure + β · (Actual - Expected)
  α = 0.84, β = 0.71

Dissociation Index:
  DI = |DA_caudate - DA_nacc|

Temporal Phase:
  Phase = DA_caudate / (DA_caudate + DA_nacc + ε)
  Phase → 1.0: anticipation dominant
  Phase → 0.0: experience dominant

Decay: τ = 3.0s
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| E[Pleasure] | Predicted reward | Expected hedonic response |
| Uncertainty | Entropy H | Current uncertainty level |
| Actual_Pleasure | Hedonic evaluation | Real-time pleasure |
| Expected | State | Previous expectation |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| DA_caudate | [0, 1] | Anticipatory DA (wanting) |
| DA_nacc | [0, 1] | Experiential DA (liking) |
| dissociation_index | [0, 1] | Wanting-liking dissociation |
| temporal_phase | [0, 1] | Anticipation vs experience |

## Why 7/10

- Berridge wanting/liking dissociation — major neuroscience framework
- Temporal phase tracking requires state
- Dissociation index and phase ratio are genuine nonlinearities
- PET-validated coefficients (α=0.84, β=0.71)
- But base signals (E[Pleasure], Actual_Pleasure) need definition
