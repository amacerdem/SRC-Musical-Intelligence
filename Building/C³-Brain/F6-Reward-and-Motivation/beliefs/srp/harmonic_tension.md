# harmonic_tension -- Appraisal Belief (SRP)

**Category**: Appraisal (observe-only)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Harmony far from tonic, unresolved." Observes the tonal distance of the current harmonic state from the tonic -- how "unresolved" the music sounds right now. High harmonic tension means the listener perceives a dominant, applied chord, or remote key area that demands resolution. Low harmonic tension means the music is at rest on the tonic, resolved and stable.

Harmonic tension is the tonal component of the broader tension belief. While the Core `tension` belief integrates energy, uncertainty, and harmonic factors, `harmonic_tension` isolates the purely harmonic contribution: roughness trend, inverse consonance, and spectral entropy.

---

## Observation Formula

```
# From SRP M-layer (Musical meaning):
harmonic_tension = SRP.harmonic_tension[M13]  # index [13]

# Range: [0, 1]
# 0 = fully resolved (tonic, consonant)
# 1 = maximum tension (dominant, dissonant, remote key)

# Computed from:
harmonic_tension = sigma(0.5 * roughness_trend + 0.3 * inv_consonance + 0.2 * entropy)
# where:
#   roughness_trend = R3[0] (roughness) -> H3(H18, M18, L0) -- forward trend of roughness
#   inv_consonance = 1 - consonance_mean
#     where consonance_mean = mean(R3[0:7]) -> H3(H18, M0, L2) -- phrase-level consonance
#   entropy = R3[22] (distribution_entropy) -> H3(H18, M0, L2) -- spectral unpredictability

# The formula captures:
# - roughness_trend: is dissonance increasing? (approaching dominant)
# - inv_consonance: how far from consonant state? (tonal distance)
# - entropy: how unpredictable is the spectrum? (harmonic ambiguity)
```

No prediction -- observe-only appraisal.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP M13 | harmonic_tension [13] | Primary tonal distance state |
| R3 [0] | roughness | Dissonance level (Plomp-Levelt) |
| R3 [0:7] | consonance group | Overall consonance (inverted for tension) |
| R3 [22] | distribution_entropy | Spectral unpredictability |
| H3 (H18, M18, L0) | roughness trend | Forward roughness trajectory |
| H3 (H18, M0, L2) | consonance mean | Phrase-level consonance state |
| BCH | consonance_signal | Hierarchical consonance from SPU |

---

## Kernel Usage

The harmonic_tension appraisal feeds multiple downstream consumers:

```python
# In SRP mechanism computation:
# harmonic_tension directly modulates the tension Core belief
# and informs the resolution_expectation Anticipation belief

# Cross-function:
# F2 Prediction: tonal distance informs harmonic prediction confidence
# SRP internal: harmonic_tension + dynamic_intensity = musical buildup signal
```

1. **SRP tension belief**: harmonic_unresolved component (weight 0.3) in tension observe formula
2. **F2 Prediction**: Tonal distance modulates how confidently the system predicts harmonic resolution
3. **SRP resolution_expectation**: High harmonic tension implies resolution is expected soon

---

## Scientific Foundation

- **Lerdahl & Jackendoff 1983**: Tonal tension as hierarchical distance from tonic in prolongational reduction
- **Bigand & Parncutt 1999**: Perceived musical tension correlates with tonal distance (behavioral, N=20)
- **Farbood 2012**: Tension is multi-dimensional -- harmonic, dynamic, rhythmic components are separable
- **Koelsch 2014**: Music-evoked tension activates amygdala and hippocampus (meta-analysis)
- **Cheung 2019**: Uncertainty (related to harmonic ambiguity) drives NAcc and caudate activation (fMRI, N=39)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
