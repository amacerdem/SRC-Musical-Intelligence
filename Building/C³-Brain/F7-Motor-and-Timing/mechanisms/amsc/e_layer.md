# AMSC — Extraction

**Model**: Auditory-Motor Stream Coupling
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_auditory_gamma | pSTG high-gamma activity (70-170 Hz). Tracks sound intensity at r = 0.49 (Potes 2012, ECoG, N=8). Computed from amplitude × loudness × tonalness at H6 (200ms). Maps to posterior superior temporal gyrus. Formula: σ(0.49 × amp_val × loud_val × tonal_val). |
| 1 | f02_motor_gamma | Motor cortex gamma coupling. Premotor response delayed 110ms from pSTG via the dorsal auditory stream. Potes 2012: cross-correlation r = 0.70 at 110ms lag (N=4). Lazzari 2025: right dPMC causally necessary for beat perception (TMS, N=40+42). Formula: σ(0.70 × f01 × energy_vel). |
| 2 | f03_coupling_delay | Auditory-motor coupling delay strength. Models the r = 0.70 cross-correlation at 110ms latency. Combines f01 auditory gamma with x_l0l5 coupling smoothness at H11. Represents the dorsal stream pathway quality. Formula: 0.70 × f01 × x_smooth. |
| 3 | f04_intensity_corr | Sound intensity → gamma correlation proxy. Continuous intensity-tracking strength combining auditory and motor gamma. Formula: 0.49 × (f01 + f02) / 2. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 6 | M0 (value) | L2 | Amplitude at beat level — current intensity |
| 1 | 7 | 6 | M4 (max) | L2 | Peak intensity at beat level |
| 2 | 8 | 6 | M0 (value) | L0 | Loudness at beat level — perceptual intensity |
| 3 | 10 | 6 | M0 (value) | L0 | Spectral flux — onset detection |
| 4 | 10 | 6 | M17 (peaks) | L0 | Beat count per window |
| 5 | 11 | 6 | M0 (value) | L0 | Onset strength — event onset |
| 6 | 22 | 6 | M8 (velocity) | L0 | Energy change velocity — intensity dynamics |
| 7 | 14 | 6 | M0 (value) | L2 | Tonalness — gamma band proxy |

---

## Computation

The E-layer implements the auditory-motor coupling pathway (Potes 2012; Lazzari 2025):

1. **Auditory gamma** (f01): pSTG high-gamma intensity tracking at beat level (H6). The r = 0.49 coefficient directly maps the intensity-gamma correlation. Sturm 2014 extends this to multiple music features beyond intensity.

2. **Motor gamma** (f02): Premotor cortex response with 110ms delay from pSTG. The r = 0.70 coefficient represents the cross-correlation at delay. Lazzari 2025 (TMS, preregistered) confirms right caudal dPMC is causally necessary.

3. **Coupling delay** (f03): Pathway quality measure combining auditory gamma with interaction coupling smoothness. Represents the dorsal auditory stream integrity.

4. **Intensity correlation** (f04): Continuous tracking strength as mean of auditory + motor gamma scaled by r = 0.49.

All sigmoid-bounded outputs in [0, 1]. α-tier: ECoG direct measurement + TMS causal evidence + cross-species (Ito 2022).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Sound intensity signal — primary energy proxy |
| R³ [8] | loudness | Perceptual intensity (Stevens power law) |
| R³ [10] | spectral_flux | Onset dynamics — sound change detection |
| R³ [11] | onset_strength | Onset sharpness — motor anticipation cue |
| R³ [14] | tonalness | Harmonic-to-noise proxy — gamma correlation |
| R³ [22] | energy_change | Intensity acceleration — motor preparation trigger |
| H³ | 8 tuples (see above) | Beat-level features at H6 (200ms) |
