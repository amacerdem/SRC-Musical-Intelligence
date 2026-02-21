# SS-EP Neural Entrainment

**Source**: ASU-α1-SNEM (Selective Neural Entrainment Model)
**Unit**: ASU (Attentional Salience Unit)
**Tier**: α (Core)
**Score**: 7/10 — Active construction with temporal dynamics

---

## Scientific Basis

- Steady-State Evoked Potential (SS-EP) literature
- Beat/meter salience exceeds envelope tracking (active, not passive)

## Mechanism

Neural entrainment to beat and meter is ACTIVE — it exceeds what the acoustic
envelope alone would predict. The brain constructs rhythmic salience beyond
the physical stimulus (SS-EP enhancement > envelope).

### Formula

```
SS-EP_enhancement(f) = α·BeatSalience(f) + β·MeterSalience(f) - γ·Envelope(f)

BeatSalience(f) = exp(-(f - f_beat)^2 / (2·σ_beat^2))
MeterSalience(f) = Σ_i w_i · exp(-(f - f_meter_i)^2 / (2·σ_meter^2))

Enhancement_Index = (SS-EP_beat - SS-EP_envelope) / (SS-EP_envelope + ε)

α = 1.0, β = 0.8, γ = 0.5
```

### Temporal Dynamics (dSS-EP/dt)

```
dSS-EP/dt = τ^(-1) · (Target_Enhancement - Current_SS-EP)
τ = 2.5s (integration window)

Discrete: SS-EP[t] = SS-EP[t-1] + (1/τ) · (Target[t] - SS-EP[t-1])
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| f_beat | Beat tracking (onset periodicity) | Beat frequency |
| f_meter | Meter inference | Metrical frequencies |
| Envelope | R³ energy features | Acoustic envelope power |
| SS-EP[t-1] | State | Previous entrainment level |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| SS-EP_enhancement | unbounded | Enhancement above envelope |
| Enhancement_Index | [0, inf) | Ratio of active to passive |
| SS-EP_current | [0, 1] | Current entrainment state |

## Why 7/10

- Active construction (not passive tracking) — real cognitive mechanism
- Gaussian frequency selectivity with empirical coefficients
- Temporal dynamics with differential equation (requires state)
- Enhancement Index separates active from passive
- But exact σ_beat, σ_meter parameters need calibration
