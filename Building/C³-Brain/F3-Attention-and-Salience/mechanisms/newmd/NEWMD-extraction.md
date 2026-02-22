# NEWMD E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid
**Model**: STU-γ2 (Neural Entrainment-Working Memory Dissociation, 10D, γ-tier <70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:entrainment_strength | [0, 1] | Automatic entrainment (SS-EP proxy). f01 = sigma(0.30*onset_val*flux_peak + 0.20*periodicity). Paradoxical: beta=-0.060 (Sares 2023) — stronger entrainment does NOT improve WM. |
| 1 | E1:wm_capacity | [0, 1] | Working memory capacity proxy. f02 = sigma(0.25*energy_chg_mean + 0.20*pitch_std). WM engagement via spectral complexity. beta=+0.068 (Sares 2023). |
| 2 | E2:flexibility_cost | [0, 1] | Temporal flexibility cost. f03 = sigma(0.25*(1-f01)*motor_mean + 0.25*long_entropy). Flexibility requires overriding entrainment — cost scales with entrainment absence. |
| 3 | E3:dissociation_index | [0, 1] | Degree of route independence. f04 = |f01 - f02|. Large values indicate entrainment and WM operate independently; small values indicate coupling. |

---

## Design Rationale

1. **Entrainment Strength (E0)**: Tracks automatic neural entrainment to temporal structure via onset and spectral flux periodicity. The key finding from Sares 2023 is paradoxical: beta=-0.060, meaning stronger entrainment is weakly *negative* for WM performance. This dissociation is the core insight — entrainment and WM use independent neural routes.

2. **WM Capacity (E1)**: Tracks working memory engagement through energy change and pitch variability at medium horizons (H8). Higher spectral complexity demands more WM resources. beta=+0.068 (Sares 2023) confirms WM capacity independently predicts performance.

3. **Flexibility Cost (E2)**: Temporal flexibility — the ability to adapt to tempo changes — requires overriding automatic entrainment. Uses long-horizon entropy (H20) from motor-auditory coupling. Inversely modulated by entrainment strength: strong entrainment reduces flexibility.

4. **Dissociation Index (E3)**: The absolute difference between entrainment and WM capacity. This is the signature of the Sares 2023 finding: these two routes are independent (r~0 in their data). High dissociation = strong independence; low dissociation = possible coupling (e.g., in trained musicians).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 6, 0, 0) | onset_strength value H6 L0 | Onset detection for beat entrainment |
| (10, 6, 4, 0) | spectral_flux max H6 L0 | Peak spectral flux for beat entrainment |
| (11, 11, 14, 0) | onset_strength periodicity H11 L0 | Onset periodicity at ~350ms — beat period |
| (22, 8, 1, 0) | energy_change mean H8 L0 | Mean energy change over ~250ms — WM load |
| (23, 8, 3, 0) | pitch_change std H8 L0 | Pitch variability at ~250ms — WM complexity |
| (25, 20, 13, 0) | x_l0l5[0] entropy H20 L0 | Long-range coupling entropy — flexibility |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: beat amplitude envelope |
| [8] | loudness | E0: perceptual loudness for entrainment |
| [9] | spectral_centroid | E1: spectral complexity for WM |
| [10] | spectral_flux | E0: onset detection for entrainment |
| [11] | onset_strength | E0: event boundary for entrainment |
| [21] | spectral_change | E2: spectral change context |
| [22] | energy_change | E1: energy dynamics for WM |
| [23] | pitch_change | E1: pitch dynamics for WM |
| [25:33] | x_l0l5 | E2: motor-auditory coupling for flexibility |
| [33:41] | x_l4l5 | E2+E3: higher-order coupling |

---

## Scientific Foundation

- **Sares et al. 2023**: beta=-0.060 SS-EP (entrainment), beta=+0.068 WM capacity (N=48). Entrainment and WM are independent predictors of rhythmic performance.
- **Noboa et al. 2025**: EXACT REPLICATION of Sares betas (R²=0.316). Confirms dissociation across independent sample.
- **Scartozzi et al. 2024**: beta r=0.42 (N=57). Cross-validates entrainment-WM independence.
- **Grahn & Brett 2007**: Z=5.67 putamen activation for beat perception (fMRI, N=27).

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/newmd/extraction.py` (pending)
