# TSCP — Forecast

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | timbre_continuation | Note-by-note timbre prediction. H³ trend-based expectation of upcoming timbre characteristics using warmth and tonalness means at 46ms. σ(0.50 * warmth_mean_46ms + 0.50 * tonalness_mean_46ms). Halpern et al. 2004: timbre imagery activates posterior PT overlapping with perception (R STG imagery t=4.66, perception t=6.89). Zatorre & Halpern 2005: auditory cortex supports veridical timbre representation during imagery. |
| 8 | cortical_enhancement_pred | Long-term plasticity prediction. ATT x practice accumulation — expected enhancement trajectory based on current plasticity magnitude and timbre change trends. σ(0.60 * f03 + 0.40 * timbre_change_mean_300ms). Leipold et al. 2021: robust musicianship effects on functional/structural networks replicable across AP/non-AP (n=153). |
| 9 | generalization_pred | Transfer to related timbres. Predicts how much trained instrument enhancement generalizes to acoustically similar timbres. σ(0.50 * recognition_quality + 0.30 * x_l5l7_300ms + 0.20 * timbre_identity). Pantev 2001: trained > similar > dissimilar > pure tone hierarchy implies graded generalization. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 8 | 12 | 5 | M1 (mean) | L0 (fwd) | Mean warmth over 46ms |
| 9 | 14 | 5 | M1 (mean) | L0 (fwd) | Mean tonalness over 46ms |
| 10 | 24 | 8 | M1 (mean) | L0 (fwd) | Mean timbre flux over 300ms |
| 11 | 41 | 8 | M0 (value) | L2 (bidi) | Consonance x Timbre coupling 300ms |

---

## Computation

The F-layer generates predictions about upcoming timbre processing:

1. **Timbre continuation** (idx 7): Uses warmth and tonalness means at 46ms (alpha-beta timescale) to predict upcoming timbre characteristics on a note-by-note basis. This implements the imagery-perception overlap mechanism from Halpern et al. 2004 — the same cortical regions that process timbre also generate timbre predictions. Maps to right posterior STG and left PT (conjunction site).

2. **Cortical enhancement prediction** (idx 8): Combines current plasticity magnitude (f03) with timbre change mean at 300ms to predict the trajectory of cortical enhancement over longer timescales. Higher values indicate that ongoing experience is expected to drive further cortical reorganization. Based on the expansion-renormalization model from Olszewska & Marchewka 2021.

3. **Generalization prediction** (idx 9): Combines recognition quality, consonance-timbre coupling (x_l5l7 at 300ms), and timbre identity to predict how much the current enhancement will transfer to acoustically similar timbres. The graded generalization hierarchy (trained > similar > dissimilar > pure) is modeled via the weighted combination of template match quality and spectral similarity. Maps to auditory association cortex BA22 (generalization pathway).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_plasticity_magnitude | Current plasticity level for enhancement trajectory |
| P-layer | recognition_quality | Template match quality for generalization prediction |
| P-layer | timbre_identity | Bound identity for generalization basis |
| R³ [41:47] | x_l5l7 | Consonance-timbre coupling for spectral similarity |
| H³ | 4 tuples (see above) | Mid-range and long-range timbre dynamics for prediction |
