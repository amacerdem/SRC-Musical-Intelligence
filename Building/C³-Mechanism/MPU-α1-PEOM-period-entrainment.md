# Period Entrainment (dP/dt)

**Source**: MPU-α1-PEOM (Period Entrainment Optimization Model)
**Unit**: MPU (Motor Processing Unit)
**Tier**: α (Core)
**Score**: 7/10 — Differential equation with state

---

## Scientific Basis

- Motor period converges to auditory period during beat synchronization
- Phase-locking literature (Large & Jones, Dynamic Attending Theory)

## Mechanism

The motor system's internal period P(t) converges toward the auditory
stimulus period T through exponential attraction.

### Formula

```
dP/dt = α · (T - P(t))

Where:
  P(t) = current motor period (state variable)
  T = auditory stimulus period (from beat tracking)
  α = coupling strength / convergence rate

Discrete-time:
  P[t] = P[t-1] + α · (T[t] - P[t-1])

CV reduction:
  CV_entrained / CV_self_paced < 1.0  (entrainment reduces variability)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| T | Beat tracking / onset periodicity | Target auditory period |
| P[t-1] | State | Previous motor period |
| α | Coupling parameter | Convergence rate |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| P[t] | continuous | Updated motor period |
| dP/dt | continuous | Rate of period change |
| CV_reduction | [0, 1] | Variability reduction ratio |

## Why 7/10

- Genuine differential equation (state variable P(t))
- Exponential convergence to target — well-studied dynamical system
- Described in PEOM doc but NOT implemented in pseudocode
- α parameter needs calibration from tapping data
- Foundation for all beat synchronization mechanisms
