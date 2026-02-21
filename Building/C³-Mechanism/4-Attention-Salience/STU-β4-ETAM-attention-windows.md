# Three-Window Attention Modulation

**Source**: STU-β4-ETAM (Entrainment, Tempo & Attention Modulation)
**Unit**: STU (Structural Temporal Unit)
**Tier**: β (Integrative)
**Score**: 8/10 — Hierarchical delay windows with empirical coefficients

---

## Scientific Basis

- **Hausfeld et al. (2021)**: EEG N=14, d=0.60-0.68 attended > unattended
- Three delay windows at 150-220ms, 320-360ms, 410-450ms
- Bassoon = 3 windows, cello = 1 window (instrument asymmetry)

## Mechanism

Attention modulates envelope tracking through three hierarchical delay windows.
Each window captures a different level of auditory processing.

### Formula

```
Early window (150-220ms):
  f01 = σ(0.35·amp·loud + 0.35·onset + 0.30·amp_peak)

Middle window (320-360ms):
  f02 = σ(0.40·flux + 0.30·spec_change_mean + 0.30·energy_vel)

Late window (410-450ms):
  f03 = σ(0.35·x_coupling + 0.35·x_l5l7_mean + 0.30·entropy)

Attention gain:
  Gain = 0.60 · (f01 + f02 + f03) / 3
  0.60 = d from Hausfeld 2021

Key constraint:
  Low-frequency entrainment does NOT persist without attention
  (Pesnot Lerousseau 2021)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| amp, loud, onset | H³ at H6 (200ms) | Early auditory features |
| flux, spec_change, energy_vel | H³ at H8-H11 | Middle spectral features |
| x_coupling, entropy | H³ at H14-H16 | Late cross-domain features |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| f01 | [0, 1] | Early attention window |
| f02 | [0, 1] | Middle attention window |
| f03 | [0, 1] | Late attention window |
| attention_gain | [0, 0.60] | Overall modulation gain |

## Why 8/10

- Three distinct delay windows at validated latencies
- Hierarchical progression (early → middle → late)
- d=0.60-0.68 empirical coefficients
- Instrument asymmetry provides additional validation
- Late window weighted highest (deeper processing = stronger attention)
