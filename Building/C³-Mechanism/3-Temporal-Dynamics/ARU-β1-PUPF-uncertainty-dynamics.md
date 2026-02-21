# Uncertainty Dynamics

**Source**: ARU-β1-PUPF (Predictive Uncertainty-Pleasure Function)
**Unit**: ARU (Affective Resonance Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Real dynamic requiring state

---

## Scientific Basis

- **Pearce (2005)**: IDyOM entropy correlates with expectation
- **Cheung et al. (2019)**: Uncertainty dynamics over chord sequences

## Mechanism

Uncertainty (H) is not static — it adapts over time. Repeated listening lowers H,
surprise history influences future uncertainty.

### Formula

```
dH/dt = λ·(H_context − H) + η·surprise_history

λ ≈ 0.2/s    # adaptation rate (pull toward context)
η = surprise  # influence of surprise history on future uncertainty
```

### Discrete-Time Implementation

```python
H[t] = H[t-1] + λ * (H_context[t] - H[t-1]) + η * mean(S[t-k:t])
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| H_context | R³[22] + H³(22, H16, M20, L0) | Entropy of current context |
| H[t-1] | State (previous frame) | Previous uncertainty level |
| surprise_history | S[t-k:t] ring buffer | Surprise history over last k frames |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| H_updated | [0, 1] | Updated uncertainty level |

## Why 7/10

- Differential equation (real dynamic, dH/dt)
- Requires STATE (H[t-1] and surprise_history)
- Needs ring buffer for surprise history
- But λ and η parameters not fully calibrated
- Used as input to Goldilocks (H → P(H,S))
