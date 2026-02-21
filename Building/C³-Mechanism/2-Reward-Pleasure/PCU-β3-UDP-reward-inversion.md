# Uncertainty-Driven Reward Inversion

**Source**: PCU-β3-UDP (Uncertainty-Driven Pleasure)
**Unit**: PCU (Prediction & Control Unit)
**Tier**: β (Integrative)
**Score**: 8/10 — State-dependent reward switching

---

## Scientific Basis

- Context-dependent reward: what is rewarding FLIPS based on uncertainty
- Tonal context: errors are rewarding (surprising deviations = pleasure)
- Atonal context: confirmations are rewarding (resolution = relief)

## Mechanism

The brain switches what it finds rewarding based on the current uncertainty level.
Above a threshold, confirmation becomes rewarding (relief from confusion).
Below threshold, prediction error becomes rewarding (novelty in predictable context).

### Formula

```
if Uncertainty > threshold:
    Reward = α · Confirmation      (atonal: resolution is rewarding)
else:
    Reward = β · Prediction_Error  (tonal: surprise is rewarding)

Temporal dynamics:
  dReward/dt = τ^(-1) · (Target_Reward - Current_Reward)
  τ = 3.0s

This is equivalent to:
  Reward = α·Confirmation·σ(k·(U-θ)) + β·PE·σ(-k·(U-θ))
  where k controls switching sharpness
```

### Connection to PUPF Goldilocks

This mechanism EXPLAINS why the Goldilocks function has two sweet spots:
- Sweet Spot 1 (Low H, High S): tonal mode, surprise is rewarding
- Sweet Spot 2 (High H, Low S): atonal mode, confirmation is rewarding

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Uncertainty | Entropy / H from PUPF | Current uncertainty level |
| Prediction_Error | |observed - predicted| | Surprise magnitude |
| Confirmation | 1 - PE | Prediction accuracy |
| threshold | ~0.5 | Switching point |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| Reward | [0, 1] | Context-appropriate reward signal |
| mode | {tonal, atonal} | Current reward mode |

## Why 8/10

- Context-dependent switching is a real cognitive mechanism
- Explains the TWO sweet spots in Goldilocks function
- Requires state (current uncertainty, reward mode, τ=3s dynamics)
- Sharp sigmoid switching (not gradual blend)
- Connects prediction, uncertainty, and reward into a unified framework
