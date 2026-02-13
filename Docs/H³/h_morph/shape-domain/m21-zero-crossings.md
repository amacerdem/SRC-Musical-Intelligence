# M₂₁: zero_crossings (Z) — Rate of Zero Crossings

**Index**: 21
**Domain**: Shape
**Symbol**: Z
**Formula**: `Z = count(sign changes) / n`
**Range**: [0, 1]

---

## Overview

The rate at which the signal (relative to its mean) crosses zero. High zero-crossing rate indicates rapid oscillation; low rate indicates slow changes or sustained values.

---

## Computation

```python
def compute_zero_crossings(signal: np.ndarray) -> float:
    """Compute M₂₁: zero-crossing rate."""
    # Center the signal
    centered = signal - np.mean(signal)
    # Count sign changes
    sign_changes = np.sum(np.diff(np.sign(centered)) != 0)
    # Normalize by length
    return sign_changes / len(signal)
```

---

## Relationship to Frequency

```
For a sine wave: Z ≈ 2f/sample_rate

Higher frequency → More zero crossings
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | very_slow | Minimal oscillation | < 0.125 |
| 1 | slow | Few crossings | < 0.25 |
| 2 | moderate_slow | Some crossings | < 0.375 |
| 3 | moderate | Medium rate | < 0.5 |
| 4 | moderate_fast | Above average | < 0.625 |
| 5 | fast | Many crossings | < 0.75 |
| 6 | very_fast | Rapid oscillation | < 0.875 |
| 7 | ultrafast | Maximum crossings | ≥ 0.875 |

---

## Musical Interpretation

- Low Z: Sustained note, slow melody, bass register
- High Z: Tremolo, trill, high-frequency content
- Used by XTI and NPL mechanisms

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m21_zero_crossings.py`
