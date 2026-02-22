# HTP E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:high_level_lead | [0, 1] | Abstract prediction (~500ms). sigma(0.40*trist_mean + 0.35*tonal_stability_mean_1s + 0.25*tonal_stability_500ms). de Vries & Wurm 2023: view-invariant features predicted ~500ms ahead in aIPL/LOTC. |
| 1 | E1:mid_level_lead | [0, 1] | Perceptual prediction (~200ms). sigma(0.40*sharpness_mean_500ms + 0.30*sharpness_velocity_125ms + 0.30*pitch_salience_velocity). de Vries & Wurm 2023: view-dependent features at ~200ms in V3/V4 / belt cortex. |
| 2 | E2:low_level_lead | [0, 1] | Sensory prediction (~110ms). sigma(0.40*amplitude_H0 + 0.35*onset_periodicity_100ms + 0.25*spectral_auto_100ms). de Vries & Wurm 2023: optical flow / sensory at ~110ms in A1/V1. |
| 3 | E3:hierarchy_gradient | [0, 1] | Gradient strength. sigma(0.50*(E0-E2)). Strong when high-level leads > low-level (ηp² = 0.49). |

---

## Design Rationale

1. **High-Level Lead (E0)**: Abstract features — harmonic balance (tristimulus mean) + tonal stability over long windows. These are the "what" of prediction. STG/aIPL region.

2. **Mid-Level Lead (E1)**: Perceptual dynamics — brightness trajectory + pitch salience velocity. These capture the "shape" of prediction. Belt cortex.

3. **Low-Level Lead (E2)**: Sensory features — amplitude + onset periodicity + spectral coupling. These are the "when" of prediction. A1/HG.

4. **Hierarchy Gradient (E3)**: The difference between high and low level leads. Maximal when the prediction hierarchy is engaged (abstract features well-predicted, sensory features less so).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (60, 16, 1, 0) | tonal_stability mean H16 L0 | Long-range abstract context (replaces x_l5l7) |
| (60, 8, 0, 0) | tonal_stability value H8 L0 | High-level structure at 500ms |
| (13, 4, 8, 0) | sharpness velocity H4 L0 | Brightness change at 125ms |
| (13, 8, 1, 0) | sharpness mean H8 L0 | Sustained brightness over 500ms |
| (7, 0, 0, 2) | amplitude value H0 L2 | Instant amplitude at 25ms |
| (11, 3, 14, 2) | onset_strength periodicity H3 L2 | Onset regularity at 100ms |
| (17, 3, 0, 2) | spectral_auto value H3 L2 | Cross-band coupling (replaces x_l0l5) |
| (39, 4, 8, 0) | pitch_salience velocity H4 L0 | Pitch change (replaces x_l4l5) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 18:21 | tristimulus1-3 | E0: mean of 3 for abstract harmonic balance |

---

## Scientific Foundation

- **de Vries & Wurm 2023**: ηp²=0.49, F(2)=19.9, p=8.3e-7 — hierarchical prediction timing (MEG, N=22)
- **Norman-Haignere 2022**: Hierarchical integration 50-400ms in auditory cortex (iEEG, N=7)
- **Golesorkhi 2021**: Intrinsic timescales follow core-periphery (η²=0.86, MEG, N=89)

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/htp/extraction.py`
