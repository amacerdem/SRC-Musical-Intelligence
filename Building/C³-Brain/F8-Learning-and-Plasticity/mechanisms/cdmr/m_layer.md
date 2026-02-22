# CDMR — Temporal Integration

**Model**: Context-Dependent Mismatch Response
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | melodic_expectation | Pattern expectation state. Exponential moving average of context modulation (f02) over a context window (RTI_WINDOW = 2.5s), tracking the accumulation of melodic context that modulates mismatch sensitivity. Tervaniemi 2022: genre-specific MMN modulation by expertise reflects accumulated musical syntax knowledge. Koelsch: ERAN (150-250ms) reflects long-term music-syntactic regularities distinct from on-line MMN memory. |
| 5 | deviance_history | Recent deviance memory. Exponential moving average of mismatch amplitude (f01) with tau=0.4s decay, maintaining a running estimate of recent deviance levels. Fong 2020: MMN as prediction error signal under predictive coding framework — deviance history forms the prediction baseline. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 8 | 10 | 16 | M1 (mean) | L2 (bidi) | Mean deviance over 1s |
| 9 | 23 | 4 | M2 (std) | L2 (bidi) | Pitch variability at 125ms |
| 10 | 21 | 3 | M0 (value) | L2 (bidi) | Spectral deviance at 100ms |
| 11 | 21 | 4 | M18 (trend) | L0 (fwd) | Spectral trend at 125ms |

---

## Computation

The M-layer integrates E-layer outputs over time to maintain context memory:

1. **Melodic expectation** (idx 4): Temporal smoothing of context modulation (f02) over a 2.5-second melodic context window. This maintains a running estimate of the melodic context richness that modulates mismatch sensitivity. In predictive coding terms, this represents the precision of melodic predictions — richer contexts produce more precise expectations and therefore stronger mismatch responses to violations. Uses spectral trend at 125ms (theta timescale) aligned with the MMN latency window.

2. **Deviance history** (idx 5): Exponential moving average of mismatch amplitude (f01) with tau=0.4s decay constant (derived from Rupp 2022 MMN temporal dynamics). This memory trace adapts mismatch sensitivity — if recent deviance is high, the threshold for eliciting a strong mismatch response increases (habituation). If recent deviance is low, sensitivity increases (oddball enhancement). Uses mean deviance at 1s for baseline calibration.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_mismatch_amplitude | Input to deviance history EMA |
| E-layer | f02_context_modulation | Input to melodic expectation EMA |
| R³ [21] | spectral_change | Spectral context dynamics for trend computation |
| R³ [23] | pitch_change | Pitch variability for context complexity |
| H³ | 4 tuples (see above) | Mean deviance, pitch variability, and spectral trend dynamics |
