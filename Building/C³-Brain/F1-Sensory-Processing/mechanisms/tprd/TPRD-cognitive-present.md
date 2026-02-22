# TPRD P-Layer — Cognitive Present (2D)

**Layer**: Present (P)
**Indices**: [5:7]
**Scope**: hybrid
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:tonotopic_state | [0, 1] | Current tonotopic activation level. sigma(0.40*T0*roughness + 0.30*(1-stumpf_h0) + 0.30*(1-stumpf_mean)). Spectral processing dominance when pitch fusion is low. Briley 2013: primary HG encodes frequency, not pitch. |
| 6 | P1:pitch_state | [0, 1] | Current pitch representation level. sigma(0.35*tonalness_mean_h6*autocorr_period_h6 + 0.35*tonalness*M1 + 0.30*stumpf_mean). F0 extraction quality modulated by coherence and fusion. Norman-Haignere 2013: pitch-sensitive regions in anterior auditory cortex. |

---

## Design Rationale

Two present-processing dimensions for tonotopy-pitch state:

1. **Tonotopic State (P0)**: Tonotopic encoding (T0) weighted by roughness captures spectral processing dominance. (1-stumpf) at both cochlear (H0) and brainstem (H3) levels inverts tonal fusion: when fusion is low, spectral (tonotopic) processing is dominant. The 0.40/0.30/0.30 weighting prioritizes current encoding over fusion context.

2. **Pitch State (P1)**: Three pitch-relevant signals: tonalness at beat level times harmonic periodicity captures sustained pitch clarity; tonalness*M1 (coherence ratio) provides a pitch-coherence interaction; stumpf_mean gives brainstem-level fusion stability. Higher P1 = more robust F0 representation.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 0, 0, 2) | stumpf value H0 L2 | Immediate pitch fusion (cochlear) |
| (3, 3, 1, 2) | stumpf mean H3 L2 | Brainstem pitch fusion mean |
| (14, 6, 1, 0) | tonalness mean H6 L0 | Beat-level pitch clarity |
| (17, 6, 14, 0) | spectral_auto period H6 L0 | Beat-level harmonic periodicity |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | P0: tonotopic activation proxy |
| 14 | tonalness | P1: pitch state proxy |

---

## Scientific Foundation

- **Briley 2013**: Tonotopic adaptation (pure-tone) in medial HG; pitch chroma in anterolateral HG
- **Norman-Haignere 2013**: Pitch-sensitive regions respond to resolved harmonics in anterior cortex
- **Stumpf 1890**: Tonal fusion as foundational consonance perception measure

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/tprd/cognitive_present.py`
