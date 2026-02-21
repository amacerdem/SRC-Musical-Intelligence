# Mismatch Memory Dynamics

**Source**: NDU-β2-CDMR (Context-Dependent Mismatch Response)
**Unit**: NDU (Novelty Detection Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Differential equation with decay

---

## Scientific Basis

- MMN literature: Mismatch Negativity as prediction error signal
- Context-dependent: stable context amplifies MMN, unstable context suppresses

## Mechanism

The brain maintains a mismatch memory that tracks recent deviance. This memory
decays exponentially (τ=0.4s), creating a temporal window for deviance detection.

### Formula

```
CDMR(t) = MismatchAmplitude(t) × ContextModulation(t) × SubadditivityGating(t)

Mismatch memory dynamics:
  dMismatch/dt = τ^(-1) · (Current_Deviance - Mismatch_Memory)
  τ = 0.4s

Discrete-time:
  Mismatch[t] = Mismatch[t-1] + (1/τ) · (Deviance[t] - Mismatch[t-1])
```

### Connection to Precision-Weighted PE (PWSM)

Context modulation is precision weighting:
- Stable context → high precision → MMN amplified
- Unstable context → low precision → MMN suppressed

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Current_Deviance | |observed - expected| | Frame-level deviance |
| Mismatch[t-1] | State | Previous mismatch memory |
| Context_Precision | Variance-based | Context stability |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| Mismatch_Memory | [0, 1] | Running mismatch state |
| CDMR | [0, 1] | Context-modulated mismatch response |

## Why 7/10

- Differential equation with explicit τ=0.4s
- State variable (Mismatch_Memory evolves)
- Context modulation via precision weighting
- Connects to PWSM precision-weighted PE mechanism
- τ=0.4s matches MMN temporal window in ERP literature
