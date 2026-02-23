# SDD — Temporal Integration

**Model**: Supramodal Deviance Detection
**Unit**: NDU
**Function**: F12 Cross-Modal Integration
**Tier**: alpha
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | multilinks_function | Edge correlation measure capturing temporally integrated cross-network binding. Combines E-layer multilink count (f02) with cross-level integration at 100ms alpha (H3 x_l5l7 value), providing a smoothed estimate of how strongly deviance detection networks are coupled across modalities. sigma(0.50 * f02 + 0.50 * integration_100ms). Paraskevopoulos 2022: multilinks between deviance networks (47 non-musicians, 15 musicians) define the supramodal mechanism; the M-layer temporally integrates these edge correlations to produce a stable binding measure. |
| 5 | supramodal_ratio | Deviance-to-standard ratio capturing the temporal integration of supramodal dominance. Derived from the E-layer supramodal index (f03) modulated by integration periodicity at 1s beat timescale (H3 x_l5l7 periodicity), ensuring that the ratio reflects sustained cross-modal integration patterns rather than transient fluctuations. sigma(0.50 * f03 + 0.50 * integration_periodicity_1s). Paraskevopoulos 2022: deviance networks show stronger between-network correlation than standard networks; this ratio quantifies the temporal stability of that dominance. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 14 | 41 | 3 | M0 (value) | L2 (bidi) | Cross-level integration at 100ms alpha |
| 15 | 41 | 16 | M14 (periodicity) | L2 (bidi) | Integration periodicity at 1s beat |

---

## Computation

The M-layer performs temporal integration of the E-layer's deviance and multilink features:

1. **Multilinks function** (idx 4): Temporally smoothed edge correlation measure. The E-layer's multilink count (f02) captures instantaneous cross-network coupling; the M-layer integrates this with the raw cross-level integration signal (x_l5l7 at 100ms) from H3. This dual-source computation ensures that the multilinks function reflects both the computed multilink statistic and the underlying cross-level binding dynamics. The 100ms alpha timescale matches the auditory cortex integration window where cross-modal binding is established.

2. **Supramodal ratio** (idx 5): Temporally integrated deviance dominance. The E-layer's supramodal index (f03) is a multiplicative interaction of deviance and multilinks; the M-layer stabilizes this by incorporating the periodicity of cross-level integration at the 1s beat timescale. Periodic integration patterns indicate sustained supramodal processing rather than sporadic cross-modal coincidences. When integration periodicity is high, the supramodal ratio reflects a stable cross-modal deviance detection regime.

Both dimensions use sigmoid activation with coefficient sums = 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_multilink_count | Instantaneous multilink level for temporal smoothing |
| E-layer | f03_supramodal_index | Supramodal dominance for ratio stabilization |
| R3 [41] | x_l5l7[0] | Cross-level integration signal |
| H3 | 2 tuples (see above) | Integration value and periodicity at two timescales |
