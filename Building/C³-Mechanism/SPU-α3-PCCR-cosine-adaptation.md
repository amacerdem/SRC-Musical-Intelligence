# Cosine Adaptation Curve

**Source**: SPU-α3-PCCR (Pitch Chroma Cortical Representation)
**Unit**: SPU (Spectral Processing Unit)
**Tier**: α (Core)
**Score**: 9/10 — Fully implementable scientific formula

---

## Scientific Basis

- **Briley et al. (2013)**: F(1,28)=29.865, p<0.001
- Non-monotonic adaptation: 1 octave adapts LESS than 0.5 octave (octave equivalence)

## Mechanism

Cortical adaptation follows a cosine function of pitch distance, reflecting octave equivalence
in auditory cortex. Adaptation is periodic in pitch space — repeating every octave.

### Formula

```
Response(Δpitch) = α + β · cos(2π · Δpitch / octave)

α = baseline adaptation level
β = adaptation depth (modulation amplitude)
Δpitch = pitch distance in semitones between current and adaptor
octave = 12 semitones
```

### Implementation

```python
response = alpha + beta * torch.cos(2 * pi * delta_pitch / 12.0)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Δpitch | Pitch tracking (F0 difference) | Pitch distance in semitones |
| α | Empirical | Baseline adaptation level |
| β | Empirical | Adaptation depth |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| adaptation_response | [α-β, α+β] | Non-monotonic adaptation magnitude |

## Why 9/10

- Fully specified cosine formula from Briley 2013 (large effect, F=29.865)
- Requires pitch tracking (available from R³ v2 F:Pitch group)
- Captures octave equivalence — a fundamental property of pitch perception
- Deterministic, no learned parameters needed
- Directly falsifiable with ERP measurements
