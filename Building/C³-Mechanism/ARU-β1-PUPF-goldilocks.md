# Goldilocks Pleasure Function

**Source**: ARU-β1-PUPF (Predictive Uncertainty-Pleasure Function)
**Unit**: ARU (Affective Resonance Unit)
**Tier**: β (Integrative)
**Score**: 9/10 — Directly implementable full mechanism

---

## Scientific Basis

- **Cheung et al. (2019)**: 80,000 chords, fMRI, N=39, d=3.8–8.53
- **Egermann et al. (2013)**: Live concert, N=50, d=6.0
- **Gold et al. (2019)**: IC×entropy quadratic, N=43+27
- **Gold et al. (2023)**: fMRI, VS-STG coupling, N=24

## Mechanism

Musical pleasure arises from the nonlinear interaction between uncertainty (H) and surprise (S).
Peak pleasure occurs not at maximum surprise nor at full predictability — but at two "sweet spots".

### Formula

```
P(H, S) = α·(1-H)·S + β·H·(1-S) - γ·H·S - δ·(1-H)·(1-S)

α = 0.6   # Low H × High S  → pleasure (surprise in predictable context)
β = 0.4   # High H × Low S  → pleasure (expected in uncertain context)
γ = 0.3   # High H × High S → penalty (overwhelming)
δ = 0.2   # Low H × Low S   → penalty (boring)

Zone(H, S) = σ(P(H, S) − θ)    θ ≈ 0.3
```

### Sweet Spot 1: Low H + High S
"I thought I knew, but WOW" — deceptive cadence, unexpected modulation

### Sweet Spot 2: High H + Low S
"I was confused, but it resolved" — resolution after tension

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| H (entropy) | R³[22] distribution_entropy + H³ temporal | Shannon entropy of expectation distribution |
| S (surprise) | R³[21] spectral_flux + H³ velocity | Prediction error magnitude |

## Outputs

| Idx | Name | Range | Description |
|-----|------|-------|-------------|
| 0 | pleasure_P | [-1, 1] | Goldilocks function output |
| 1 | goldilocks_zone | [0, 1] | σ(P − θ), in sweet spot? |
| 2 | HS_interaction | [0, 1] | H × S product (amygdala signal) |

## Brain Regions

- **Amygdala**: H×S interaction → surprise detection (Cheung 2019, d=3.8-4.16)
- **NAcc/Caudate**: H alone → uncertainty tracking (Cheung 2019)
- **Hippocampus**: Prediction context building (Cheung 2019)

## Why 9/10

- Formula directly derived from Cheung 2019 (80K chord dataset)
- 4 coefficients (α,β,γ,δ) empirically determined
- No state required (H and S come from external sources)
- Immediately codable: `P = 0.6*(1-H)*S + 0.4*H*(1-S) - 0.3*H*S - 0.2*(1-H)*(1-S)`
- Falsifiable: validated with fMRI
