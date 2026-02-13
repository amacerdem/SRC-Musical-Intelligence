# H⁰ — Temporal Foundation

**Position**: [256:2560] in 8,192D Manifold
**Dimension**: 2,304D (32 × 24 × 3)
**Role**: Shared temporal infrastructure for C⁰ and R⁰

---

## Overview

H⁰ is the **shared temporal foundation** of the SRC⁹-Composer framework. It provides multi-scale temporal context spanning **5 orders of magnitude** (25ms to 981s) and serves as the **common input** for both the cognitive (C⁰) and resonance (R⁰) processing branches.

```
H⁰ = H ⊗ M ⊗ L = 2,304D

where:
  H = Event Horizon (32 temporal windows)
  M = H-Morph (24 morphological parameters)
  L = H-Law (3 causal attention modes)
```

---

## Architecture

```
                S⁰ SPECTRAL (256D) [0:256]
                         │
                         ▼
              ┌─────────────────────┐
              │    H⁰ TEMPORAL      │
              │    (2,304D)         │
              │    [256:2560]       │
              └──────────┬──────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
           ▼                           ▼
    ┌─────────────┐             ┌─────────────┐
    │ C⁰ COGNITIVE│             │ R⁰ RESONANCE│
    │ (2,048D)    │             │ (1,024D)    │
    │ [2560:4608] │             │ [4608:5632] │
    └─────────────┘             └─────────────┘
```

---

## Documentation Structure

| Directory | Files | Description |
|-----------|-------|-------------|
| [event_horizon/](event_horizon/) | 46 | 32 temporal windows across 9 cognitive scales |
| [h_morph/](h_morph/) | 28 | 24 morphological parameters in 3 domains |
| [h_law/](h_law/) | 7 | 3 causal attention modes |
| [tensor/](tensor/) | 5 | Tensor math and downstream mapping |

---

## Quick Reference

### Event Horizon (H) — 32 Windows

| Scale | Windows | Duration | Count |
|-------|---------|----------|-------|
| Gamma | H₀-H₁ | 25-50ms | 2 |
| Alpha-Beta | H₂-H₄ | 75-125ms | 3 |
| Theta | H₅-H₇ | 150-250ms | 3 |
| Syllable | H₈-H₁₁ | 300-500ms | 4 |
| Beat | H₁₂-H₁₆ | 525-1000ms | 5 |
| Phrase | H₁₇-H₂₀ | 1.25-5s | 4 |
| Section | H₂₁-H₂₄ | 7.5-36s | 4 |
| Structural | H₂₅-H₂₈ | 100-414s | 4 |
| Piece | H₂₉-H₃₁ | 500-981s | 3 |

### H-Morph (M) — 24 Parameters

| Domain | Index | Parameters |
|--------|-------|------------|
| **Value** | M₀-M₇ | value, mean, std, min, max, range, skew, kurtosis |
| **Derivative** | M₈-M₁₅ | velocity, velocity_mean, velocity_std, acceleration, acceleration_mean, jerk, jerk_mean, smoothness |
| **Shape** | M₁₆-M₂₃ | curvature, periodicity, trend, stability, entropy, zero_crossings, peaks, troughs |

### H-Law (L) — 3 Modes

| Mode | Symbol | Direction | Mechanisms |
|------|--------|-----------|------------|
| Forward | L_F | Past → Present | TIH, PTM, ITM, HRM, SGM, EFC, C0P |
| Backward | L_B | Present → Future | HRM |
| Bidirectional | L_Bi | Past ↔ Future | OSC, TGC, ATT, NPL, GRV, BND, AED, ASA, CPD |

---

## Implementation

**Pipeline Location**: `Pipeline/D0/h0/`

| Component | File |
|-----------|------|
| Main Extractor | `h0_extractor.py` |
| Event Horizon | `event_horizon.py` |
| H-Morph | `h_morph/h_morph_calculator.py` |
| H-Law | `h_law/h_law_calculator.py` |

---

## Scientific Basis

H⁰ is grounded in **120+ peer-reviewed neuroscience papers** covering:
- Neural oscillations (Giraud 2012, Lakatos 2019)
- Theta-gamma coupling (Lisman 2013, Canolty 2010)
- Timing and memory (Fujioka 2012, Bonetti 2024)
- Striatal gradients (Hamid 2024)

---

## Related Documentation

- [H⁰-OVERVIEW.md](H⁰-OVERVIEW.md) — Full architectural specification
- [../C⁰/](../C⁰/) — C⁰ Cognitive Layer (consumes H⁰ via HC⁰)
- [../R⁰/](../R⁰/) — R⁰ Resonance Layer (consumes H⁰ via HR⁰)
- [../S⁰/](../S⁰/) — S⁰ Spectral Layer (input to H⁰)

---

**Version**: 2.0.0
**Last Updated**: 2026-02-05
