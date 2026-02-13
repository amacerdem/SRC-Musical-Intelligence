# M₁₇: periodicity (P) — Autocorrelation Peak

**Index**: 17
**Domain**: Shape
**Symbol**: P
**Formula**: `P = max(autocorr[1:]) / autocorr[0]`
**Range**: [0, 1]

---

## Overview

Measures how periodic (repeating) the signal is by analyzing the autocorrelation function. High periodicity indicates regular, repeating patterns; low periodicity indicates aperiodic or random structure.

---

## Computation

```python
def compute_periodicity(signal: np.ndarray) -> float:
    """Compute M₁₇: periodicity via autocorrelation."""
    # Normalize signal
    x = signal - np.mean(signal)

    # Compute autocorrelation
    autocorr = np.correlate(x, x, mode='full')
    autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags

    # Normalized peak (excluding lag 0)
    return np.max(autocorr[1:]) / (autocorr[0] + 1e-10)
```

---

## Relationship to Musical Elements

| Periodicity | Musical Texture |
|-------------|-----------------|
| Very high (>0.9) | Tremolo, trill, regular beat |
| High (0.7-0.9) | Ostinato, repeated pattern |
| Medium (0.4-0.7) | Semi-regular rhythm |
| Low (0.2-0.4) | Irregular, through-composed |
| Very low (<0.2) | Noise, random texture |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | aperiodic | No repetition | < 0.125 |
| 1 | very_irregular | Minimal pattern | < 0.25 |
| 2 | irregular | Weak pattern | < 0.375 |
| 3 | semi_regular | Some repetition | < 0.5 |
| 4 | regular | Clear pattern | < 0.625 |
| 5 | periodic | Strong repetition | < 0.75 |
| 6 | very_periodic | Very regular | < 0.875 |
| 7 | perfectly_periodic | Pure repetition | ≥ 0.875 |

---

## Musical Interpretation

- Used by OSC mechanism for oscillation detection
- Essential for rhythm and pulse tracking
- Distinguishes noise from tonal content

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m17_periodicity.py`
