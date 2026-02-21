# Roughness Deviation Detection

**Source**: SPU-γ3-SDED (Sensory Dissonance Early Detection)
**Unit**: SPU (Spectral Processing Unit)
**Tier**: γ (Speculative)
**Score**: 7/10 — Pre-attentive deviation with brainstem origin

---

## Scientific Basis

- Sensory dissonance as brainstem-level, pre-attentive, universal (not expertise-dependent)
- MMN for dissonance is expertise-INDEPENDENT (unlike ESME)

## Mechanism

Roughness deviation from temporal mean — brainstem-level, pre-attentive detection.
Unlike ESME (expertise-dependent), this is universal and fires regardless of training.

### Formula

```
deviation = |roughness[t] - roughness_mean|
roughness_mean = H³(0, H3, M1, L2)    # bidirectional 100ms mean

f02_mmn = σ(0.50·f01·pitch_salience + 0.50·deviation)

Where f01 = σ(0.40·roughness·consonance + 0.30·sethares + 0.30·(1-helmholtz))
```

### Key Insight: Neural-Behavioral Dissociation

Neural detection (MMN) is constant across expertise levels.
Behavioral discrimination improves with training.
This means the DETECTION mechanism is brainstem/universal,
but the DECISION mechanism is cortical/learned.

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| roughness | R³[0] | Current roughness |
| roughness_mean | H³(0, H3, M1, L2) | Running mean roughness |
| sethares | R³[1] | Sethares dissonance |
| helmholtz | R³[2] | Helmholtz consonance |
| pitch_salience | Pitch processing | Pitch clarity |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| roughness_deviation | [0, 1] | |current - mean| deviation |
| early_detection | [0, 1] | Pre-attentive roughness flag |
| mmn_dissonance | [0, 1] | Neural mismatch signal |

## Why 7/10

- Deviation from mean is a real mechanism (same principle as ESME)
- Brainstem origin = universal, no training needed
- Neural-behavioral dissociation is an important architectural insight
- But mean comes from H³, not internal state
