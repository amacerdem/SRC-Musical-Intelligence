# M₂₃: troughs (N_t) — Count of Local Minima

**Index**: 23
**Domain**: Shape
**Symbol**: N_t
**Formula**: `N_t = count(local minima)`
**Range**: [0, n/2]

---

## Overview

The number of local minima (troughs) in the signal within the window. Indicates how many "nadir points" exist in the signal's trajectory.

---

## Computation

```python
def compute_troughs(signal: np.ndarray) -> float:
    """Compute M₂₃: count of local minima."""
    from scipy.signal import find_peaks
    # Find peaks of inverted signal = troughs of original
    troughs, _ = find_peaks(-signal)
    return len(troughs)
```

---

## Relationship to M₂₂ (peaks)

```
Typically: N_t ≈ N_p (peaks and troughs alternate)

A "complete oscillation" = 1 peak + 1 trough
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | none | No troughs | 0 |
| 1 | single | One trough | 1 |
| 2 | few | 2-3 troughs | 2-3 |
| 3 | several | 4-6 troughs | 4-6 |
| 4 | moderate | 7-10 troughs | 7-10 |
| 5 | many | 11-15 troughs | 11-15 |
| 6 | numerous | 16-25 troughs | 16-25 |
| 7 | dense | 25+ troughs | 25+ |

---

## Musical Interpretation

- Few troughs: Single phrase arc, sustained passage
- Many troughs: Rapid oscillation, busy texture
- Used by PST mechanism for phrase structure analysis

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m23_troughs.py`
