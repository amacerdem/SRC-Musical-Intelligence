# Inverted-U Preference Function

**Source**: RPU-β1-IUCP (Inverted-U Complexity Preference)
**Unit**: RPU (Reward Processing Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Quadratic preference with interaction

---

## Scientific Basis

- **Gold et al. (2019)**: Quadratic IC×entropy effects, R^2=41.6%, N=43+27
- Wundt curve / Berlyne optimal arousal theory
- Intermediate complexity preferred over too simple or too complex

## Mechanism

Musical preference follows an inverted-U as a function of information content
and entropy. Peak liking occurs at intermediate complexity. The IC × Entropy
interaction shifts the peak location.

### Formula

```
Liking(IC, Entropy) = β1·IC + β2·IC^2 + β3·Entropy + β4·Entropy^2 + β5·(IC × Entropy)

Where:
  β2 < 0  (inverted-U for IC: too much surprise → dislike)
  β4 < 0  (inverted-U for entropy: too much uncertainty → dislike)
  β5 < 0  (interaction: both high → overwhelming)

Quadratic peak (simplified):
  IC_optimal = -β1 / (2·β2)
  Entropy_optimal = -β3 / (2·β4)

Implementable proxy:
  ic_quadratic = 4.0 · IC · (1.0 - IC)    # peaks at IC=0.5
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| IC | Information content | Surprise level [0,1] |
| Entropy | Context entropy | Uncertainty level [0,1] |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| liking | continuous | Predicted preference |
| ic_quadratic | [0, 1] | Inverted-U complexity term |
| interaction | [0, 1] | IC × Entropy product |

## Why 7/10

- Quadratic model with interaction — real nonlinearity
- Empirically validated (Gold 2019, R^2=41.6%)
- Explains Wundt curve computationally
- No state needed (instantaneous preference)
- β coefficients need fitting but signs are constrained
- Connects directly to PUPF Goldilocks and UDP reward inversion
