# HGSIC — Forecast

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | groove_prediction | Predicted groove state (110ms ahead). Extrapolates motor groove from f03 and amplitude trend at bar level (H16). When motor groove is strong and intensity trend is positive, groove is predicted to continue. Maps to premotor anticipatory activation. Potes 2012: 110ms auditory-motor delay. Formula: σ(0.5 × f03 + 0.4 × amp_trend). |
| 9 | beat_expectation | Next beat timing prediction. Combines beat induction (f01) with spectral centroid periodicity at bar level (H16). Strong beat induction plus stable periodicity enables confident next-beat timing. Maps to SMA/putamen beat-strength encoding (Hoddinott & Grahn 2024: C-Score model). Formula: σ(0.5 × f01 + 0.5 × centroid_period). |
| 10 | motor_anticipation | Motor system anticipatory activation. Combines bar-level amplitude smoothness, trend, and pitch periodicity. Smooth, trending intensity with periodic pitch contour drives motor anticipation for upcoming groove events. Grahn & Brett 2007: SMA Z=5.03 for beat anticipation. Formula: σ(0.4 × amp_smooth + 0.3 × amp_trend + 0.3 × pitch_period). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 9 | 16 | M14 (periodicity) | L2 | Bar-level energy periodicity |
| 1 | 7 | 16 | M15 (smoothness) | L0 | Groove quality — amplitude smoothness |
| 2 | 7 | 16 | M18 (trend) | L0 | Intensity trajectory at bar level |
| 3 | 23 | 16 | M14 (periodicity) | L2 | Melodic periodicity at bar level |
| 4 | 24 | 16 | M1 (mean) | L0 | Timbral dynamics over bar |

---

## Computation

The F-layer generates predictions about upcoming groove states:

1. **Groove prediction** (idx 8): Extrapolates motor groove from current f03 state and amplitude trend. When motor groove is high and intensity trend is rising or stable, groove continuation is predicted. If f03 is low or trend is falling, groove decline is expected. The 110ms auditory-motor delay (Potes 2012) means predictions target the near future.

2. **Beat expectation** (idx 9): Predicts next beat timing from beat induction strength (f01) and bar-level centroid periodicity. Stable periodicity at bar level (H16) indicates regular beat structure amenable to anticipation. Maps to the putamen/SMA continuous beat-strength encoding (Hoddinott & Grahn 2024).

3. **Motor anticipation** (idx 10): Combines amplitude smoothness, trend, and pitch periodicity at bar level. Smooth, predictable intensity patterns with periodic melodic contour drive anticipatory motor system activation — the motor system "prepares" for upcoming groove events.

All outputs are sigmoid-bounded to [0, 1] and represent confidence in future groove states.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_beat_gamma, f03_motor_groove | Current groove state for extrapolation |
| R³ [7] | amplitude | Smoothness and trend for groove quality |
| R³ [9] | spectral_centroid_energy | Bar-level periodicity for beat expectation |
| R³ [23] | pitch_change | Melodic periodicity for motor anticipation |
| R³ [24] | timbre_change | Timbral dynamics for prediction context |
| H³ | 5 tuples (see above) | Bar-level features at H16 (1000ms) |
