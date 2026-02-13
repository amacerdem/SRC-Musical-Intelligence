# Shape Domain — M₁₆-M₂₃ (Geometric Patterns)

**Index Range**: 16-23
**Parameters**: 8
**Question**: WHAT pattern does the signal form?
**Function**: Geometric and information-theoretic characteristics

---

## Overview

The Shape domain captures the **structural properties** of a signal — its curvature, periodicity, trend, and complexity. These parameters answer "what pattern does the signal form?" independently of its absolute level.

---

## Parameters

| Index | Name | Symbol | Formula | Description |
|-------|------|--------|---------|-------------|
| [M₁₆](m16-curvature.md) | curvature | κ | \|d²x/dt²\| / (1+(dx/dt)²)^1.5 | Geometric curvature |
| [M₁₇](m17-periodicity.md) | periodicity | P | max(autocorr) / autocorr(0) | Autocorrelation peak |
| [M₁₈](m18-trend.md) | trend | T | linear regression slope | Overall direction |
| [M₁₉](m19-stability.md) | stability | Φ | 1 / (1 + σ_δ²) | Inverse velocity variance |
| [M₂₀](m20-entropy.md) | entropy | H | -Σp_i × log(p_i) | Shannon entropy |
| [M₂₁](m21-zero-crossings.md) | zero_crossings | Z | count(sign changes) / n | Rate of zero crossings |
| [M₂₂](m22-peaks.md) | peaks | N_p | count(local maxima) | Number of peaks |
| [M₂₃](m23-troughs.md) | troughs | N_t | count(local minima) | Number of troughs |

---

## Shape Categories

```
GEOMETRIC                    STRUCTURAL                  COMPLEXITY
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ M₁₆ curvature │           │ M₁₈ trend     │           │ M₂₀ entropy   │
│ M₁₇ periodicity│          │ M₁₉ stability │           │ M₂₁ zero_cross│
└───────────────┘           │ M₂₂ peaks     │           └───────────────┘
                            │ M₂₃ troughs   │
                            └───────────────┘
```

---

## Musical Interpretation

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| **curvature** | Linear/straight | Curved/arced |
| **periodicity** | Aperiodic/noise | Highly periodic |
| **trend** | Descending overall | Ascending overall |
| **stability** | Changing rapidly | Very stable |
| **entropy** | Predictable/simple | Complex/random |
| **zero_crossings** | Few oscillations | Many oscillations |
| **peaks** | Few climax points | Many climax points |
| **troughs** | Few nadir points | Many nadir points |

---

## Musical Examples

| Texture | periodicity | entropy | peaks/troughs |
|---------|-------------|---------|---------------|
| **Drone** | Low | Low | Few |
| **Tremolo** | High | Low | Many |
| **Melody** | Medium | Medium | Medium |
| **Noise/texture** | Low | High | Many |
| **Phrase arc** | Low | Low | 1/1 |

---

## Implementation

```python
def compute_shape_domain(signal: np.ndarray, dt: float) -> np.ndarray:
    """Compute Shape domain parameters M₁₆-M₂₃."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)

    # Curvature: |a| / (1 + v²)^1.5
    curvature_vals = np.abs(acceleration) / (1 + velocity**2)**1.5

    # Periodicity via autocorrelation
    autocorr = np.correlate(signal - np.mean(signal), signal - np.mean(signal), 'full')
    autocorr = autocorr[len(autocorr)//2:]
    periodicity = np.max(autocorr[1:]) / (autocorr[0] + 1e-10)

    # Trend via linear regression
    t = np.arange(len(signal)) * dt
    trend = np.polyfit(t, signal, 1)[0]

    # Stability
    stability = 1 / (1 + np.var(velocity))

    # Entropy
    hist, _ = np.histogram(signal, bins=32, density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log(hist + 1e-10))

    # Zero crossings
    zero_crossings = np.sum(np.diff(np.sign(signal - np.mean(signal))) != 0) / len(signal)

    # Peaks and troughs
    peaks = len(scipy.signal.find_peaks(signal)[0])
    troughs = len(scipy.signal.find_peaks(-signal)[0])

    return np.array([
        np.mean(curvature_vals),  # M₁₆: curvature
        periodicity,               # M₁₇: periodicity
        trend,                     # M₁₈: trend
        stability,                 # M₁₉: stability
        entropy,                   # M₂₀: entropy
        zero_crossings,            # M₂₁: zero_crossings
        peaks,                     # M₂₂: peaks
        troughs,                   # M₂₃: troughs
    ])
```

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain.py`
