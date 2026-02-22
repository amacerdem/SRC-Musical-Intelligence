# TSCP — Extraction

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_trained_timbre_response | Trained instrument cortical enhancement. N1m amplitude for trained timbre based on tristimulus balance and harmonic purity. σ(0.35 * trist_balance + 0.35 * (1-inharmonicity) * tonalness). Pantev et al. 2001: timbre-specific N1m enhancement, double dissociation F(1,15)=28.55, p=.00008. Violinists: violin > trumpet > pure tone. |
| 1 | f02_timbre_specificity | Selectivity index for trained vs untrained instrument response. Spectral contrast between trained and untrained timbres via warmth/sharpness and temporal stability. σ(0.40 * warmth * sharpness_inv + 0.30 * timbre_stability + 0.30 * x_l5l7_mean). Pantev 2001: age-of-inception r=-0.634, p=.026. |
| 2 | f03_plasticity_magnitude | Degree of cortical reorganization. Training effect size proxy combining trained response strength with timbre flux variability. σ(0.50 * f01 * timbre_change_std). Santoyo et al. 2023: musicians show enhanced theta phase-locking for timbre-based streams. Whiteford et al. 2025: plasticity locus is cortical not subcortical (d=-0.064, BF=0.13). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 18 | 2 | M0 (value) | L2 (bidi) | F0 energy at 17ms |
| 1 | 19 | 2 | M0 (value) | L2 (bidi) | Mid-harmonic energy at 17ms |
| 2 | 20 | 2 | M0 (value) | L2 (bidi) | High-harmonic energy at 17ms |
| 3 | 5 | 5 | M0 (value) | L2 (bidi) | Inharmonicity at 46ms |
| 4 | 14 | 8 | M19 (stability) | L0 (fwd) | Tonalness stability over 300ms |
| 5 | 24 | 8 | M3 (std) | L0 (fwd) | Timbre flux variability 300ms |

---

## Computation

The E-layer extracts three explicit features that characterize timbre-specific cortical plasticity:

1. **Trained timbre response** (f01): Driven by tristimulus balance (1 - std of tristimulus1/2/3) and harmonic purity ((1-inharmonicity) * tonalness). The tristimulus triple captures the harmonic envelope signature of each instrument family. High f01 indicates a stimulus with clear, stable harmonic structure matching a trained instrument template. Maps to secondary auditory cortex (Pantev 2001: ECD posterior/lateral to HG).

2. **Timbre specificity** (f02): Driven by warmth/sharpness contrast, tonalness stability at 300ms, and consonance-timbre coupling (x_l5l7 mean). Captures the selectivity of cortical enhancement — how much the response is specific to the trained instrument timbre rather than general auditory enhancement. Maps to Planum Temporale (Bellmann & Asano 2024: ALE cluster R-pSTG/PT, 3128 mm³).

3. **Plasticity magnitude** (f03): Interaction of trained response (f01) with timbre change variability (H³ std of timbre_change at 300ms). Novel or varying timbres trigger greater plasticity-related activation. Maps to bilateral pSTG/HG (Bellmann & Asano 2024: ALE meta-analysis, k=18, N=338).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [18:21] | tristimulus1/2/3 | Harmonic envelope signature for instrument identity |
| R³ [5] | inharmonicity | Instrument character (piano=high, violin=low) |
| R³ [14] | tonalness | Harmonic-to-noise ratio for pitch clarity |
| R³ [12] | warmth | Low-frequency spectral balance for timbre contrast |
| R³ [13] | sharpness | High-frequency energy for brightness proxy |
| R³ [41:47] | x_l5l7 (partial) | Consonance-timbre coupling for binding strength |
| R³ [24] | timbre_change | Temporal timbre flux for plasticity trigger |
| H³ | 6 tuples (see above) | Fast spectral envelope and long-range stability dynamics |
