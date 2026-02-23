# WMED E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:entrainment_strength | [0, 1] | SS-EP entrainment strength. sigma(0.35*beat_periodicity_1s + 0.35*onset_periodicity_1s + 0.30*amp_std_100ms). Neural entrainment at beat frequencies. Noboa 2025: SS-EP p<0.001; PARADOX: stronger entrainment → worse tapping (p=0.015). |
| 1 | E1:wm_contribution | [0, 1] | Working memory contribution to rhythm production. sigma(0.40*wm_coupling_mean_1s + 0.30*wm_entropy_1s + 0.30*wm_coupling_500ms). WM capacity aids motor adaptation. Noboa 2025: WM → better tapping (p=0.043); Yuan 2025: alpha-band WM marker BFincl>3. |
| 2 | E2:tapping_accuracy | [0, 1] | Rhythm production accuracy. sigma(0.40*timing_stability_1s + 0.30*(1-timing_std_1s) + 0.30*flux_periodicity_100ms). Combined metric of timing precision. Lu 2022: SMA motor timing, right precentral BA4/6. |
| 3 | E3:dissociation_index | [0, 1] | Entrainment-WM route dissociation. sigma(0.50*|entrainment-wm| + 0.50*phase_resets). Measures independence between automatic entrainment and controlled WM routes. Noboa 2025: no interaction term significant — routes are independent. |

---

## Design Rationale

1. **Entrainment Strength (E0)**: Automatic SS-EP at beat frequencies from periodicity of beats and onsets. Paradoxically, high entrainment predicts worse tapping — over-synchronization reduces motor flexibility.

2. **WM Contribution (E1)**: Controlled cognitive pathway from cross-feature coupling (proxy for WM load). Higher WM engagement predicts better tapping through cognitive control and flexibility.

3. **Tapping Accuracy (E2)**: Combined timing quality from stability, low variability, and beat regularity. The outcome that both routes independently influence.

4. **Dissociation Index (E3)**: Quantifies the independence of the two routes. Large differences between entrainment and WM signals + phase resets indicate strong dissociation.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 | Spectral flux at 100ms |
| 1 | 10 | 3 | M14 (periodicity) | L2 | Flux periodicity at 100ms |
| 2 | 10 | 16 | M14 (periodicity) | L2 | Beat periodicity at bar |
| 3 | 11 | 3 | M0 (value) | L2 | Onset strength at 100ms |
| 4 | 11 | 16 | M14 (periodicity) | L2 | Onset periodicity at bar |
| 5 | 7 | 3 | M2 (std) | L2 | Amplitude variability at 100ms |
| 6 | 7 | 16 | M1 (mean) | L2 | Mean amplitude at bar level |
| 7 | 25 | 3 | M14 (periodicity) | L2 | Foundation coupling periodicity |
| 8 | 25 | 16 | M14 (periodicity) | L2 | Bar-level coupling periodicity |
| 9 | 25 | 16 | M21 (zero_crossings) | L2 | Phase reset events |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Intensity dynamics for entrainment |
| R³ [10] | spectral_flux | Beat-frequency SS-EP tracking |
| R³ [11] | onset_strength | Onset periodicity for entrainment |
| R³ [25] | x_l0l5 | Foundation-perceptual coupling periodicity |
| H³ | 10 tuples (see above) | Multi-scale entrainment and coupling features |
