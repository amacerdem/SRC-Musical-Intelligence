# MEAMR — Extraction

**Model**: Music-Evoked Autobiographical Memory Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_familiarity_index | Musical familiarity level. σ(0.35 * pleasantness_trend_1s + 0.30 * mean_warmth_1s). Janata 2009: familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81), SFG, thalamus, STG (P < 0.001 uncorr, fMRI, N = 13). Pleasantness trend and timbral warmth are recognition cues for familiar musical patterns. |
| 1 | f02_autobio_salience | Autobiographical salience from music-evoked memories. σ(0.35 * memory_struct_trend_1s + 0.30 * f01). Janata 2009: dMPFC (BA 8/9) correlates with autobiographical salience (P < 0.001, FDR P < 0.025 in MPFC ROI). Memory-structure coupling trend captures buildup of autobiographical associations. Requires familiarity (f01) as prerequisite. |
| 2 | f03_dmpfc_tracking | Dorsal medial prefrontal cortex tonal space tracking. σ(0.35 * mean_centroid_1s + 0.35 * mean_pleasantness_500ms + 0.30 * structural_entropy_500ms). Janata 2009: dMPFC tracks tonal space (P < 0.005, 40-voxel cluster). Brightness, pleasantness, and structural complexity feed tonal trajectory encoding. |
| 3 | f04_positive_affect | Positive affect from familiar music. σ(... + 0.30 * f02 * f01). Janata 2009: combined FAV (familiarity + autobio + valence) in MPFC (FDR P < 0.025). Maps onto vACC + SN/VTA positive affect integration. Positive affect requires both familiarity and autobiographical salience. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness over 500ms — tonal quality |
| 1 | 4 | 16 | M18 (trend) | L2 (bidi) | Pleasantness trend over 1s — recognition ramp |
| 2 | 8 | 8 | M1 (mean) | L2 (bidi) | Mean loudness over 500ms — intensity context |
| 3 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s — sustained intensity |
| 4 | 12 | 16 | M1 (mean) | L2 (bidi) | Mean warmth over 1s — timbral familiarity cue |
| 5 | 13 | 16 | M1 (mean) | L2 (bidi) | Mean brightness over 1s — tonal register |
| 6 | 21 | 8 | M20 (entropy) | L2 (bidi) | Structural entropy 500ms — complexity context |
| 7 | 21 | 16 | M1 (mean) | L2 (bidi) | Mean structural change 1s |
| 8 | 22 | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms — temporal pattern |
| 9 | 22 | 16 | M18 (trend) | L0 (fwd) | Energy change trend 1s — dynamic trajectory |
| 10 | 41 | 8 | M1 (mean) | L2 (bidi) | Memory-structure coupling 500ms |
| 11 | 41 | 16 | M1 (mean) | L2 (bidi) | Mean memory-structure coupling 1s |
| 12 | 41 | 16 | M18 (trend) | L2 (bidi) | Memory-structure trend 1s — autobio buildup |
| 13 | 41 | 16 | M5 (range) | L0 (fwd) | Memory-structure range 1s — coupling dynamic range |

---

## Computation

The E-layer extracts four features characterizing the music-evoked autobiographical memory reward pathway from Janata (2009). The computation follows a hierarchical structure where familiarity is prerequisite for autobiographical salience, which feeds positive affect.

1. **Familiarity Index (f01)**: Estimates degree of musical recognition from pleasantness trend (rising hedonic response as recognition develops) and mean warmth (timbral recognition cue). Janata 2009 showed familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81), and bilateral STG.

2. **Autobiographical Salience (f02)**: Captures strength of music-evoked autobiographical memories. Memory-structure coupling trend from x_l5l6 interactions tracks the temporal buildup of autobiographical associations. The f01 dependency ensures unfamiliar music does not trigger autobiographical memories. dMPFC (BA 8/9) activation is proportional to this signal (P < 0.001, FDR P < 0.025).

3. **dMPFC Tracking (f03)**: Models continuous tonal space tracking by dorsal medial prefrontal cortex (P < 0.005, 40-voxel cluster). Spectral centroid provides brightness (tonal register), pleasantness provides harmonic quality, and structural entropy provides complexity context.

4. **Positive Affect (f04)**: Integrates familiarity and autobiographical salience into a reward-related positive affect signal. The f02 * f01 product ensures pleasure requires both recognition AND personal associations, mapping onto vACC + SN/VTA integration.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule). τ_decay = 10.0s reflects the extended nature of autobiographical memory retrieval.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [4] | sensory_pleasantness | Familiarity cue / tonal recognition |
| R³ [8] | loudness | Familiarity dynamics / familiar loudness patterns |
| R³ [12] | warmth | Timbre familiarity / brightness recognition |
| R³ [13] | spectral_centroid | Brightness familiarity / tonal space tracking |
| R³ [21] | spectral_change | Structural complexity / memory accessibility |
| R³ [22] | energy_change | Temporal patterns / time signature cues |
| R³ [41:49] | x_l5l6 | Memory-structure binding / autobiographical salience |
| H³ | 14 tuples (see above) | Long-range temporal dynamics for memory assessment |
| Janata 2009 | dMPFC autobio + tonal tracking | Primary fMRI evidence (N = 13) |
| Salimpoor 2011 | DA release during familiar music chills | Supporting PET evidence (N = 8, r = 0.71) |
