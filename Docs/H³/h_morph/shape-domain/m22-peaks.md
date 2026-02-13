# M₂₂: peaks (N_p) — Count of Local Maxima

**Index**: 22
**Domain**: Shape
**Symbol**: N_p
**Formula**: `N_p = count(local maxima)`
**Range**: [0, n/2]

---

## Overview

The number of local maxima (peaks) in the signal within the window. Indicates how many "climax points" exist in the signal's trajectory.

---

## Computation

```python
def compute_peaks(signal: np.ndarray) -> float:
    """Compute M₂₂: count of local maxima."""
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(signal)
    return len(peaks)
```

---

## Relationship to M₂₃ (troughs)

```
Typically: N_p ≈ N_t (peaks and troughs alternate)

N_p + N_t ≈ 2 × (number of oscillations)
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | none | No peaks | 0 |
| 1 | single | One peak | 1 |
| 2 | few | 2-3 peaks | 2-3 |
| 3 | several | 4-6 peaks | 4-6 |
| 4 | moderate | 7-10 peaks | 7-10 |
| 5 | many | 11-15 peaks | 11-15 |
| 6 | numerous | 16-25 peaks | 16-25 |
| 7 | dense | 25+ peaks | 25+ |

---

## Musical Interpretation

- Few peaks: Single phrase arc, sustained passage
- Many peaks: Tremolo, rapid oscillation, busy texture
- Used by PST mechanism for phrase boundary detection

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m22_peaks.py`
