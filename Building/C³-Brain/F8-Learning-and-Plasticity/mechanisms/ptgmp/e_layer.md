# PTGMP — Extraction

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_dlpfc_plasticity | DLPFC bilateral GMV increase proxy (d=0.34). Audio-motor planning complexity from amplitude trend × long-range dynamics coupling. σ(0.35 × amp_trend_H14 × x_l4l5_mean_H20). Espinosa 2025 SR: 6 RCTs N=555. CONSTRAINT: NOT found cross-sectionally (Espinosa 2025 VBM N=61). |
| 1 | f02_cerebellar_plast | Cerebellum right hemisphere GMV proxy (d=0.34). Motor coordination from spectral flux × onset strength at keystroke timescale (H8). σ(0.30 × flux_mean × onset_val). Espinosa 2025 VBM: L cerebellum p<0.0001 (active vs naive). Strongest cross-sectional support. |
| 2 | f03_frontal_theta | Frontal theta power increase proxy (d=0.27). Creative motor-perceptual integration from energy variability × pitch dynamics at phrase level (H14). σ(0.30 × energy_std × pitch_mean). Tachibana 2024: bilateral BA45 activation during improvisation. Liao 2024: ECN+NMR+limbic+memory systems in percussionists. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 8 | M0 (value) | L0 | Spectral flux current at 300ms |
| 1 | 10 | 8 | M1 (mean) | L0 | Mean flux at keystroke scale |
| 2 | 11 | 8 | M0 (value) | L0 | Onset strength current |
| 3 | 21 | 8 | M1 (mean) | L0 | Mean spectral dynamics |
| 4 | 7 | 14 | M18 (trend) | L0 | Amplitude trajectory at phrase |
| 5 | 22 | 14 | M3 (std) | L0 | Energy change variability |
| 6 | 23 | 14 | M1 (mean) | L0 | Mean pitch dynamics |

---

## Computation

The E-layer extracts three explicit plasticity features corresponding to three brain regions:

1. **DLPFC plasticity** (f01): Executive audio-motor planning demand. Amplitude trend (intensity trajectory) × long-range dynamics coupling (x_l4l5 mean at H20). When audio-motor planning is complex and sustained, DLPFC engagement drives structural plasticity. NOTE: DLPFC finding is training-specific (RCTs) and NOT confirmed cross-sectionally.

2. **Cerebellar plasticity** (f02): Motor timing precision from spectral flux × onset strength at H8 (300ms). This is the strongest-supported pathway — L cerebellum GM confirmed cross-sectionally (p<0.0001, Espinosa 2025). Keystroke-level timing demands drive cerebellar volume.

3. **Frontal theta** (f03): Improvisation/creative flexibility from energy variability × pitch dynamics at H14 (700ms). Bilateral BA45 (Broca's) activation during improvisation (Tachibana 2024) + ECN+limbic+memory engagement (Liao 2024) support creative motor-perceptual integration.

All sigmoid formulas satisfy coefficient saturation rule (|wᵢ| ≤ 1.0).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| H³ | 7 tuples at H8/H14 (see above) | Short + phrase features |
| R³ [10] | spectral_flux | Motor timing anchor |
| R³ [11] | onset_strength | Keystroke precision |
| R³ [7] | amplitude | Intensity trajectory |
| R³ [22] | energy_change | Motor variability |
| R³ [23] | pitch_change | Melodic dynamics |
