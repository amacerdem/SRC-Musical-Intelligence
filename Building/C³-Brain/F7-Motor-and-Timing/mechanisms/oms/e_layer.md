# OMS — Extraction

**Model**: Oscillatory Motor Synchronization
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_predictive_timing | Fronto-striatal predictive timing. PFC-striatum beta-band (13–30 Hz) beat anticipation from spectral flux × onset strength at H6 (200ms) plus foundation-perceptual coupling. Edagawa & Kawasaki 2017: beta PSI frontal-temporal z=7.43; Scartozzi 2024: beta-musicality r=0.42. Formula: σ(0.35 × flux_val × onset_val + 0.35 × x_l0l5_coupling + 0.30 × energy_velocity). |
| 1 | f02_sensorimotor_coupling | Temporo-parietal sensorimotor coupling. STG-IPL gamma-band (30–100 Hz) rhythmic locking from loudness mean, dynamics-perceptual coupling, and energy periodicity at H11 (500ms). Potes 2012: pSTG-motor coupling r=0.70; Pierrieau 2025: beta × speed F=8.1, d=−1.21. Formula: σ(0.35 × loudness_mean + 0.35 × x_l4l5_coupling + 0.30 × periodicity). |
| 2 | f03_interpersonal_sync | Limbic interpersonal synchronization. NAcc-VTA-amygdala social coordination from perceptual-crossband coupling mean, balance periodicity, and f01 × f02 interaction at H16 (1000ms). Bigand 2025: coordination F(1,57)=249.75; music × vision F=50.10. Formula: σ(0.35 × x_l5l7_mean + 0.35 × balance_periodicity + 0.30 × f01 × f02). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 6 | M0 (value) | L0 | Spectral flux — current onset detection |
| 1 | 10 | 6 | M17 (peaks) | L0 | Beat count per window |
| 2 | 11 | 6 | M0 (value) | L0 | Onset strength — event onset precision |
| 3 | 7 | 6 | M0 (value) | L2 | Current ensemble intensity |
| 4 | 22 | 6 | M8 (velocity) | L0 | Intensity dynamics |

---

## Computation

The E-layer extracts the three core network signals of oscillatory motor synchronization:

1. **Predictive timing** (f01): Fronto-striatal beat anticipation from onset detection and foundation-perceptual coupling at beat level (H6). Sharp onsets with strong coupling indicate reliable predictive timing. Maps to PFC → striatum beta-band top-down prediction.

2. **Sensorimotor coupling** (f02): Temporo-parietal rhythmic locking from loudness, dynamics-perceptual coupling, and energy periodicity at motor level (H11). Maps to STG ↔ IPL gamma-band bottom-up tracking.

3. **Interpersonal synchronization** (f03): Limbic social coordination from orchestral balance coupling and the interaction of predictive timing with sensorimotor coupling at bar level (H16). Maps to NAcc-VTA-amygdala coordination.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Ensemble intensity dynamics |
| R³ [10] | spectral_flux | Onset detection for beat boundary |
| R³ [11] | onset_strength | Event boundary marking precision |
| R³ [22] | energy_change | Intensity rate of change |
| H³ | 5 tuples (see above) | Beat-level features at H6 (200ms) |
