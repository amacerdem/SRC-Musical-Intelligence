# HGSIC — Extraction

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_beat_gamma | pSTG high-gamma beat tracking (70-170 Hz). Intensity → gamma correlation at beat level. Driven by amplitude, loudness, and onset at H6 (200ms). Potes 2012: pSTG gamma ↔ sound intensity r = 0.49 (ECoG, N=8). Formula: σ(0.49 × amp_val × loud_val × onset_val). |
| 1 | f02_meter_integration | Metric structure from accent grouping. Syncopation and accent pattern detection at H11 (500ms). Hierarchically builds on f01 beat-level signals. Spiech 2022: groove inverted-U with syncopation (χ²=14.643). Formula: σ(0.51 × f01 × energy_periodicity). |
| 2 | f03_motor_groove | Motor entrainment groove state at H16 (1000ms). Hierarchical beat × meter → motor coupling through the dorsal auditory-motor pathway. Potes 2012: auditory → motor cross-correlation r = 0.70 at 110ms delay. Formula: σ(0.70 × f01 × f02). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 6 | M0 (value) | L0 | Amplitude at beat level — current sound intensity |
| 1 | 7 | 6 | M4 (max) | L0 | Peak intensity at beat level |
| 2 | 8 | 6 | M0 (value) | L0 | Loudness at beat level — perceptual intensity |
| 3 | 10 | 6 | M0 (value) | L0 | Spectral flux at beat level — onset detection |
| 4 | 10 | 6 | M17 (peaks) | L0 | Beat count per window |
| 5 | 11 | 6 | M0 (value) | L0 | Onset strength at beat level — event onset |

---

## Computation

The E-layer extracts three hierarchical levels of groove-related signals from the intensity envelope:

1. **Beat gamma** (idx 0): pSTG high-gamma tracking of sound intensity at beat level (H6 = 200ms). Uses amplitude × loudness × onset product scaled by r = 0.49 (Potes 2012 pSTG-intensity correlation). Maps to HG/pSTG high-gamma 70-170 Hz.

2. **Meter integration** (idx 1): Accent-pattern grouping at motor window (H11 = 500ms). Combines f01 beat signal with energy periodicity. The inverted-U groove-syncopation relationship (Spiech 2022) emerges from moderate syncopation maximizing this dimension. Maps to pSTG + premotor cortex.

3. **Motor groove** (idx 2): Hierarchical integration of beat × meter into motor entrainment at bar level (H16 = 1000ms). The r = 0.70 coefficient reflects the Potes 2012 auditory-motor cross-correlation at 110ms lag. Maps to motor cortex groove state.

All outputs are sigmoid-bounded to [0, 1]. The hierarchical cascade f01 → f02 → f03 mirrors the cortical hierarchy: pSTG → premotor → motor cortex.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Sound intensity signal (pSTG gamma ↔ intensity r=0.49) |
| R³ [8] | loudness | Perceptual intensity (Stevens 1957 power law) |
| R³ [10] | spectral_flux | Onset dynamics — beat boundary detection |
| R³ [11] | onset_strength | Event onset sharpness — motor anticipation cue |
| H³ | 6 tuples (see above) | Beat-level features at H6 (200ms) |
