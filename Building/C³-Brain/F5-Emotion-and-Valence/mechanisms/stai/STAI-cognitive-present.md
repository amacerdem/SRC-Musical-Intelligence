# STAI P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [6:9]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:spectral_quality | [0, 1] | Real-time consonance evaluation. Consonance-encoding aggregation from brainstem through auditory cortex. Alluri 2012: timbral features recruit STG/HG (fullness -> STG Z=7.35); Bellmann 2024: timbre processing in BA41/42/22/40/13 (ALE meta-analysis, 18 studies). |
| 7 | P1:temporal_quality | [0, 1] | Real-time temporal direction quality assessment. Spectral-envelope aggregation tracking forward vs reversed flow. Singer 2023: temporal predictability positively predicts valence (behavioral, N=40, 1780 songs); Alluri 2012: pulse clarity negatively correlated with amygdala, hippocampus (r=0.51-0.80). |
| 8 | P2:aesthetic_response | [0, 1] | Integrated aesthetic signal in the present moment. H3 binding quality combining spectral and temporal streams. aesthetic_response = sigma(0.5 * f03 + 0.5 * x_l4l5_binding). Kim 2019: full aesthetic response requires both dimensions intact (d=0.709-0.735); Gold 2023: VS integrates uncertainty x surprise x liking. |

---

## Design Rationale

1. **Spectral Quality (P0)**: The moment-to-moment consonance evaluation signal. Aggregates the consonance encoding from brainstem processing (BCH upstream) through cortical auditory areas. This is the "how consonant is this right now?" signal that feeds into the aesthetic integration. Maps to STG and Heschl's gyrus activation for timbral features, with the dual-stream architecture (ventral object recognition + dorsal temporal processing) from Bellmann 2024.

2. **Temporal Quality (P1)**: The moment-to-moment temporal direction quality. Aggregates spectral envelope tracking to assess whether the current temporal flow is forward (intact) or disrupted (reversed). When temporal predictability is high, this signal is strong, reflecting the Singer 2023 finding that temporal predictability predicts valence. Maps to the motor/limbic pathway that Alluri 2012 identified for rhythmic features.

3. **Aesthetic Response (P2)**: The integrated present-moment aesthetic judgment. Combines the aesthetic integration signal (f03) with the x_l4l5 binding quality to produce the summary aesthetic state. This is the signal that would feed downstream to reward circuitry (ARU) via cross-unit pathways. It represents the "how aesthetically valuable is this moment?" evaluation.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (12, 2, 0, 2) | warmth value H2 L2 | Current spectral warmth at 17ms |
| (14, 5, 1, 0) | tonalness mean H5 L0 | Mean tonalness over 46ms |
| (18, 2, 0, 2) | tristimulus1 value H2 L2 | F0 energy at 17ms |
| (19, 2, 0, 2) | tristimulus2 value H2 L2 | Mid-harmonic energy at 17ms |
| (20, 2, 0, 2) | tristimulus3 value H2 L2 | High-harmonic energy at 17ms |
| (33, 8, 0, 2) | x_l4l5[0] value H8 L2 | Aesthetic binding at 300ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [12] | warmth | P0: spectral warmth for consonance evaluation |
| [14] | tonalness | P0: harmonic-to-noise ratio for pitch clarity |
| [18] | tristimulus1 | P0: fundamental energy (F0) |
| [19] | tristimulus2 | P0: mid-harmonic energy |
| [20] | tristimulus3 | P0: high-harmonic energy |
| [33:41] | x_l4l5 (8D) | P2: aesthetic binding for integrated response |

---

## Scientific Foundation

- **Alluri et al. 2012**: Timbral -> STG/HG (fullness Z=7.35); rhythmic -> motor/limbic; tonal -> prefrontal. Brightness -> putamen Z=3.63. Pulse clarity negatively correlated with amygdala/hippocampus (fMRI naturalistic, N=11, r=0.51-0.80)
- **Bellmann & Asano 2024**: Timbre processing in BA41/42/22/40/13; dual-stream model (ventral object + dorsal temporal) (ALE meta-analysis, 18 studies)
- **Singer et al. 2023**: Temporal predictability positively predicts valence; confirmed in 1780-song database (behavioral, N=40, positive correlation 4/5 sections)
- **Kim et al. 2019**: Full aesthetic response requires both spectral + temporal intact; behavioral interaction d=0.709-0.735 (fMRI, N=16+23)
- **Gold et al. 2023**: R STG + VS reflect liking; VS integrates uncertainty x surprise x liking interactions (fMRI, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/stai/cognitive_present.py`
