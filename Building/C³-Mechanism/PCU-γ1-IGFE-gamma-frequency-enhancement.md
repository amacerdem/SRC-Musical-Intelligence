# Individual Gamma Frequency Enhancement

**Source**: PCU-γ1-IGFE (Individual Gamma Frequency Enhancement)
**Unit**: PCU (Prediction & Control Unit)
**Tier**: γ (Speculative)
**Score**: 8/10 — Dose-response with Gaussian frequency matching

---

## Scientific Basis

- Individual Gamma Frequency (IGF) varies 30-80 Hz across people
- Entrainment at IGF enhances cognition more than off-frequency stimulation

## Mechanism

Cognitive enhancement depends on matching stimulation frequency to the
individual's intrinsic gamma frequency (IGF). Enhancement follows a Gaussian
frequency match function combined with exponential dose-response accumulation.

### Formula

```
Enhancement(f) = Match(f, IGF) × Dose(t) × Intensity

Gaussian frequency match:
  Match(f, IGF) = exp(-(f - IGF)^2 / (2·σ_gamma^2))
  σ_gamma ≈ 5 Hz
  IGF ∈ [30, 80] Hz

Exponential dose response:
  Dose(t) = 1 - exp(-t / τ_dose)
  τ_dose = 300s (5 min half-life)

Gain functions:
  Memory_Gain    = α × Enhancement × WM_baseline
  Executive_Gain = β × Enhancement × Executive_baseline
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| f | Stimulation frequency | Current oscillation frequency |
| IGF | Individual parameter | Personal gamma frequency |
| t | Cumulative exposure time | State: accumulated exposure |
| WM_baseline | Working memory capacity | Individual baseline |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| enhancement | [0, 1] | Frequency-matched enhancement |
| dose | [0, 1] | Accumulated dose (saturates at 1) |
| memory_gain | continuous | WM improvement |
| executive_gain | continuous | Executive function improvement |

## Why 8/10

- Gaussian frequency matching: exp(-(f-IGF)^2/2σ^2) — precise parametric form
- Dose-response accumulation: 1-exp(-t/τ) — requires state (exposure time)
- Two distinct timescales: frequency matching (instantaneous) + dose (300s)
- Individual differences modeled via IGF parameter
- But γ-tier: less validated than α/β mechanisms
