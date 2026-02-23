# PWUP E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:tonal_precision | [0, 1] | Tonal context precision. sigma(0.40*tonalness_mean_1s + 0.35*consonance_mean_1s + 0.25*tonalness_500ms). Mencke 2019: tonal contexts show d=3 larger PE responses. High tonalness + consonance = high precision. |
| 1 | E1:rhythmic_precision | [0, 1] | Rhythmic context precision. sigma(0.40*periodicity_1s + 0.30*flux_periodicity_100ms + 0.30*periodicity_500ms). Regular rhythmic patterns increase precision, enabling stronger PE responses. |
| 2 | E2:weighted_error | [0, 1] | Precision-weighted prediction error. sigma(0.50*raw_pe*tonal_precision + 0.50*raw_pe*rhythmic_precision). Attenuated in low-precision (atonal) contexts. Cheung 2019: uncertainty × surprise interaction. |
| 3 | E3:uncertainty_index | [0, 1] | Contextual uncertainty level. sigma(0.50*consonance_entropy_1s + 0.50*coupling_entropy_1s). High entropy = high uncertainty = low precision = attenuated PE. |

---

## Design Rationale

1. **Tonal Precision (E0)**: Tonalness and consonance at bar level establish the precision of harmonic predictions. High precision → strong PE responses to unexpected events. Maps to IFG precision estimation.

2. **Rhythmic Precision (E1)**: Periodicity at multiple scales establishes temporal prediction precision. Maps to BG/SMA beat-based timing.

3. **Weighted Error (E2)**: Raw PE modulated by both tonal and rhythmic precision. In atonal/arrhythmic contexts, PE is attenuated despite more deviant events. Mencke 2019: d=3 between tonal and atonal PE.

4. **Uncertainty Index (E3)**: Consonance and coupling entropy at bar level measure contextual uncertainty. High uncertainty → low precision → PE attenuation.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 3 | M0 (value) | L2 | Current consonance at 100ms |
| 1 | 4 | 16 | M1 (mean) | L0 | Mean consonance over bar |
| 2 | 4 | 16 | M20 (entropy) | L0 | Consonance entropy at bar level |
| 3 | 14 | 8 | M1 (mean) | L0 | Tonalness mean at 500ms |
| 4 | 14 | 16 | M1 (mean) | L0 | Tonalness mean over bar |
| 5 | 5 | 8 | M1 (mean) | L0 | Periodicity at 500ms |
| 6 | 5 | 16 | M14 (periodicity) | L2 | Periodicity regularity at bar |
| 7 | 21 | 3 | M0 (value) | L2 | Raw spectral change PE |
| 8 | 21 | 3 | M2 (std) | L2 | PE variability at 100ms |
| 9 | 10 | 3 | M0 (value) | L2 | Spectral flux at 100ms |
| 10 | 10 | 3 | M14 (periodicity) | L2 | Flux periodicity at 100ms |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [4] | sensory_pleasantness | Consonance for tonal precision |
| R³ [5] | periodicity | Rhythmic regularity for precision |
| R³ [10] | spectral_flux | Onset periodicity for rhythmic precision |
| R³ [14] | tonalness | Tonal context clarity |
| R³ [21] | spectral_change | Raw prediction error signal |
| H³ | 11 tuples (see above) | Multi-scale precision and PE features |
