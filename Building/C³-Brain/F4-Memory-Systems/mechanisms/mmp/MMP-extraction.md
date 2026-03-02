# MMP R-Layer — Extraction (3D)

**Layer**: Recognition & Preservation (R)
**Indices**: [0:3]
**Scope**: internal
**Activation**: linear+clamp (BCH-style, no sigmoid cascade)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | R0:f07_preserved | [0, 1] | Preserved memory index. Angular/lingual gyrus pathway. 0.90 * (0.35*familiarity*stumpf + 0.35*warmth*preservation + 0.30*cortical_strength). BCH-style additive pairwise — no sigmoid cascade. High even in moderate AD because angular gyrus is among last regions to atrophy. Jacobsen et al. 2015: SMA/pre-SMA and ACC show least cortical atrophy in AD (VBM, N=32). |
| 1 | R1:f08_melodic | [0, 1] | Melodic recognition accuracy. STG + Angular Gyrus pathway. 0.90 * (0.35*familiarity*tonalness + 0.35*trist*preservation + 0.30*tonalness*trist). BCH-style additive pairwise. Preserved through moderate AD because melodic templates are cortically stored. Sikka et al. 2015: older adults shift to L-angular + L-superior-frontal gyrus for melody recognition (fMRI, N=40). |
| 2 | R2:f09_scaffold | [0, 1] | Memory scaffold efficacy. Music as cognitive aid. 0.85 * (0.35*retrieval*x_l5l7 + 0.35*x_l5l7*preservation + 0.30*retrieval*inv_entropy_norm). BCH-style additive pairwise. Therapeutic intervention metric — how effectively music can scaffold access to otherwise locked memories. Derks-Dijkman et al. 2024: 28/37 studies show musical mnemonic benefit (systematic review). |

---

## Design Rationale

1. **Preserved Memory Index (R0)**: Measures how much of the current musical memory response is mediated by AD-resistant cortical pathways (angular gyrus, lingual gyrus). Uses familiarity, tonal fusion (stumpf), and timbre warmth as the three primary signals of cortical music memory, weighted by the preservation factor (hippocampal independence). This is the primary metric for assessing whether a patient's music-memory pathway remains functional.

2. **Melodic Recognition (R1)**: Tracks the accuracy of familiar melody identification. Melodic templates stored in STG and angular gyrus are relatively spared in AD. Uses tonalness (harmonic-to-noise ratio) and tristimulus (instrument/voice identity) as the acoustic bases for melody recognition, modulated by familiarity strength.

3. **Memory Scaffold (R2)**: Quantifies how effectively music serves as a cognitive bridge to otherwise inaccessible memories. Uses the consonance-timbre interaction (x_l5l7) as the warmth-familiarity signal and inverse entropy (familiar = low entropy = easier to process). This directly informs music therapy protocol design — select music that maximizes scaffold efficacy.

---

## H3 Dependencies (R-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 0, 2) | stumpf_fusion value H16 L2 | Current binding integrity (1s) |
| (12, 16, 0, 2) | warmth value H16 L2 | Current timbre warmth (1s) |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained warmth = familiarity (5s) |
| (14, 16, 0, 2) | tonalness value H16 L2 | Melody recognition state (1s) |
| (18, 16, 0, 2) | tristimulus1 value H16 L2 | Instrument fundamental (1s) |
| (22, 16, 0, 2) | entropy value H16 L2 | Current pattern complexity (1s) |
| (0, 16, 0, 2) | roughness value H16 L2 | Current valence proxy (1s) |

## R3 Dependencies

| Index | Feature | Usage | Preservation Level |
|-------|---------|-------|--------------------|
| [0] | roughness | R2: valence proxy (emotional tag) | Partially preserved |
| [3] | stumpf_fusion | R0: binding integrity | Preserved |
| [4] | sensory_pleasantness | R0: memory valence | Preserved |
| [12] | warmth | R0+R1: familiar sound character | **Highly preserved** |
| [14] | tonalness | R1: melody tracking | **Highly preserved** |
| [18:21] | tristimulus1-3 | R1: instrument/voice ID | **Highly preserved** |
| [22] | entropy | R2: pattern familiarity (inverse) | Vulnerable |
| [41:49] | x_l5l7 | R2: timbre warmth (nostalgia) | **Preserved** |

---

## Scientific Foundation

- **Jacobsen et al. 2015**: SMA/pre-SMA and ACC show least cortical atrophy in AD; musical memory regions spared (fMRI+VBM, N=32)
- **Sikka et al. 2015**: Older adults shift to L-angular + L-superior-frontal gyrus for melody recognition (fMRI sparse-sampling, N=40)
- **Derks-Dijkman et al. 2024**: 28/37 studies show musical mnemonic benefit; familiarity key contributor (systematic review, 37 studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/extraction.py`
