# Reward Prediction Error (RPE)

**Source**: RPU-α3-RPEM (Reward Prediction Error Model)
**Unit**: RPU (Reward Processing Unit)
**Tier**: α (Core)
**Score**: 8/10 — Classic RL formulation with musical validation

---

## Scientific Basis

- **Schultz (1997)**: Dopamine neurons encode RPE
- **Gold et al. (2023)**: VS reflects musical surprise pleasure, d=1.07
- **Salimpoor et al. (2011)**: DA release during musical anticipation

## Mechanism

The brain computes reward prediction error: the difference between received
and expected reward. Positive RPE → learning/pleasure, negative RPE → aversion.

### Formula

```
RPE(t) = Reward(t) - Expected_Reward(t)

VS_Response = β1·IC + β2·Liking + β3·(IC × Liking)

Where:
  RPE > 0: positive surprise → DA release → pleasure
  RPE < 0: negative surprise → DA dip → aversion
  RPE = 0: fully predicted → no learning signal

Temporal dynamics:
  dExpected/dt = α · RPE(t)     (learning rate α)
  τ_decay = 1.0s

Crossover: IC × Liking interaction means:
  High IC + Liked    → strong positive RPE
  High IC + Disliked → strong negative RPE
  Low IC  + any      → weak RPE (boring, predicted)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Reward(t) | Hedonic evaluation | Actual reward received |
| Expected_Reward(t) | State (running estimate) | Predicted reward |
| IC | Information content | Surprise magnitude |
| Liking | Preference signal | Current liking state |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| RPE | unbounded | Signed prediction error |
| VS_response | continuous | Ventral striatum response |
| Expected_update | continuous | Updated expectation |

## Why 8/10

- Classic RL formulation (Schultz 1997) — one of most replicated findings in neuroscience
- Musical validation: Gold 2023 (d=1.07), Salimpoor 2011
- IC × Liking crossover interaction is a real nonlinearity
- Requires state (Expected_Reward evolves via learning)
- Signed error (positive vs negative RPE) separates pleasure from aversion
- τ_decay = 1.0s gives temporal dynamics
