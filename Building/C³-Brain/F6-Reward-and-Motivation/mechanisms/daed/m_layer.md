# DAED — Temporal Integration

**Model**: Dopamine Anticipation-Experience Dissociation
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | dissociation_index | Temporal-anatomical dissociation magnitude. |f01 - f02| normalized. Quantifies how strongly the current moment favors anticipation (caudate) vs consummation (NAcc). High values indicate clear phase separation; low values indicate transition. Salimpoor 2011: caudate and NAcc show temporally distinct DA release patterns. |
| 5 | temporal_phase | Anticipation vs consummation phase indicator. f01 / (f01 + f02 + epsilon). Range [0,1]: values near 1.0 indicate pure anticipation phase (caudate dominant), values near 0.0 indicate pure consummation phase (NAcc dominant), ~0.5 indicates transition. Mohebi 2024: DA transients follow a striatal gradient of reward time horizons. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — current intensity state |
| 1 | 8 | 8 | M1 (mean) | L0 (fwd) | Mean loudness over 500ms — medium-term context |
| 2 | 7 | 8 | M0 (value) | L2 (bidi) | Amplitude at 500ms — energy envelope |
| 3 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean amplitude over 1s — sustained energy |
| 4 | 0 | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms — instantaneous tension |
| 5 | 10 | 4 | M0 (value) | L2 (bidi) | Onset at 125ms — event detection |
| 6 | 10 | 8 | M14 (periodicity) | L2 (bidi) | Peak periodicity at 500ms — rhythmic regularity |

---

## Computation

The M-layer computes two derived mathematical quantities from the E-layer outputs:

1. **Dissociation Index**: The absolute difference between anticipatory and consummatory DA signals. This is the core model output — the temporal-anatomical dissociation that Salimpoor (2011) demonstrated with PET imaging. When dissociation is high, the listener is clearly in either an anticipation or consummation phase. When low, they are in a transitional state.

```
dissociation_index = |f01_anticipatory_da - f02_consummatory_da|
```

2. **Temporal Phase**: A continuous phase indicator that smoothly transitions between anticipation (1.0) and consummation (0.0). This implements the temporal gradient found by Mohebi (2024) showing DA transients follow a ventral-to-dorsal striatal gradient corresponding to reward time horizons.

```
temporal_phase = f01 / (f01 + f02 + 1e-8)
```

Both outputs are deterministic functions of E-layer features. The M-layer H³ demands provide the multi-scale temporal context that feeds into the E-layer computations upstream.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_anticipatory_da | Numerator and first operand for both M-layer computations |
| E-layer | f02_consummatory_da | Second operand for dissociation and phase computation |
| H³ | 7 tuples (see above) | Temporal context supporting E-layer feature extraction |
