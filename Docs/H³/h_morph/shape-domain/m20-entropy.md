# M₂₀: entropy (H) — Shannon Entropy

**Index**: 20
**Domain**: Shape
**Symbol**: H
**Formula**: `H = -Σ p_i × log(p_i)`
**Range**: [0, log(n_bins)]

---

## Overview

Shannon entropy of the signal's value distribution. High entropy indicates unpredictable, complex signals; low entropy indicates predictable, simple patterns.

---

## Computation

```python
def compute_entropy(signal: np.ndarray, n_bins: int = 32) -> float:
    """Compute M₂₀: Shannon entropy."""
    # Create histogram
    hist, _ = np.histogram(signal, bins=n_bins, density=True)
    # Remove zeros to avoid log(0)
    hist = hist[hist > 0]
    # Compute entropy
    return -np.sum(hist * np.log(hist + 1e-10))
```

---

## Entropy Interpretation

```
LOW ENTROPY                    HIGH ENTROPY
├────────────────────         ────────────────────
Single value (drone)          Uniform distribution

H ≈ 0 for constant            H ≈ log(n) for uniform
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | minimal | Nearly constant | < 0.125 |
| 1 | very_low | Very predictable | < 0.25 |
| 2 | low | Predictable | < 0.375 |
| 3 | moderate_low | Somewhat predictable | < 0.5 |
| 4 | moderate_high | Somewhat complex | < 0.625 |
| 5 | high | Complex | < 0.75 |
| 6 | very_high | Very complex | < 0.875 |
| 7 | maximal | Maximum complexity | ≥ 0.875 |

---

## Musical Interpretation

- Low entropy: Drone, pedal point, sustained note
- Medium entropy: Melodic line, structured harmony
- High entropy: Noise, texture, random elements
- Used by LTI and ATT mechanisms

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m20_entropy.py`
