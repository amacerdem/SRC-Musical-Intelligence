# NSCP — Temporal Integration

**Model**: Neural Synchrony Commercial Prediction
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | isc_magnitude | Raw ISC magnitude estimate. Directly derived from the neural synchrony extraction (f22). Represents the overall inter-subject correlation level as a continuous [0,1] signal. Leeuwis 2021: ISC computed across 64 EEG channels with strongest effects at frontocentral and temporal electrodes. |
| 4 | sync_consistency | Synchrony consistency over time. Tracks how stable the inter-subject correlation remains across the duration of the stimulus. sync_consistency = σ(0.5 * coherence_period_1s + 0.5 * binding_period_1s). Leeuwis 2021: early ISC (R² = 0.404) vs late ISC (R² = 0.393) both predict streams, indicating temporal stability. |
| 5 | popularity_estimate | Normalized popularity prediction. Directly derived from the commercial prediction extraction (f23). Provides a continuous [0,1] popularity proxy that maps neural synchrony to commercial success. Berns 2010: neural activity in NAcc predicted future song sales. Leeuwis 2021: combined ISC model achieves R² = 0.619. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coherence periodicity 1s for sync consistency |
| 1 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Binding periodicity 1s for sync consistency |
| 2 | 33 | 8 | M14 (periodicity) | L2 (bidi) | Binding periodicity 500ms for temporal integration |

---

## Computation

The M-layer computes three mathematical model outputs that temporally integrate the raw ISC signals:

1. **ISC Magnitude (dim 3)**: A direct passthrough of f22 (neural synchrony) into the mathematical layer. This preserves the raw ISC estimate for downstream consumers that need the unprocessed synchrony signal. The identity mapping ensures no information loss from E to M.

2. **Sync Consistency (dim 4)**: Measures temporal stability of inter-subject correlation. Combines coherence periodicity (how regularly cross-layer coupling oscillates) with binding periodicity (how regularly multi-feature patterns recur) at the 1s horizon. High consistency means the ISC signal is sustained rather than transient -- Leeuwis 2021 showed that ISC stability across early and late listening (R² drop of only 0.011) is a key commercial predictor.

3. **Popularity Estimate (dim 5)**: A direct passthrough of f23 (commercial prediction) into the mathematical layer. This provides the normalized popularity proxy for integration with other C³ functions. The mapping from ISC to streams (1% ISC increase = ~2.4M streams) is captured in the E-layer formula.

The M-layer bridges the extraction features with the present and future layers, providing both raw signals (dims 3, 5) and a temporally integrated consistency measure (dim 4).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f22_neural_synchrony | Raw ISC for magnitude passthrough |
| E-layer [1] | f23_commercial_prediction | Commercial prediction for popularity passthrough |
| R³ [25:33] | x_l0l5 | Cross-layer coherence for sync consistency |
| R³ [33:41] | x_l4l5 | Multi-feature binding for sync consistency |
| H³ | 3 tuples (see above) | Periodicity at 500ms-1s for temporal integration |
