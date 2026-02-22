# MAD E-Layer — Extraction (2D)

**Layer**: Extraction (E)
**Indices**: [0:2]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f10_anhedonia | [0, 1] | Auditory-reward disconnection probability. f10 = 1 - sigma(10 * (FA_STG_NAcc - 0.3)). FA < 0.3 yields f10 near 1.0 (anhedonic); FA > 0.3 yields f10 near 0.0 (normal). Loui 2017: BMRQ d=-5.89; Martinez-Molina 2016: FA correlates with reward r=0.61. |
| 1 | E1:dissociation_idx | [0, 1] | Music vs general hedonic dissociation index. DI = R_general - R_music. DI > 0.5 confirms musical anhedonia with preserved general reward. Mas-Herrero 2014: dissociation between music and monetary reward. Martinez-Molina 2016: 90.9% sound-specific. |

---

## Design Rationale

1. **Anhedonia Marker (E0)**: The primary MAD extraction feature. Models the probability that the auditory-reward pathway (STG to NAcc via uncinate fasciculus) is disconnected. Uses a steep sigmoid (k=10) centered at FA=0.3 as the anhedonia threshold. Below this threshold, white matter integrity is insufficient for music signals to reach reward circuitry. Loui 2017 DTI showed extremely large deficits (d=-5.89) in BMRQ scores for anhedonics, and Martinez-Molina 2016 demonstrated that fractional anisotropy of the STG-NAcc tract directly predicts music reward capacity (r=0.61).

2. **Dissociation Index (E1)**: Quantifies the double dissociation that defines musical anhedonia: general hedonic capacity is preserved while music-specific reward is absent. Computed as the difference between general reward responsiveness and music reward responsiveness. A high DI (>0.5) with high general reward (>0.7) confirms the selective deficit. This distinguishes musical anhedonia from depression-related anhedonia (which impairs all reward) and from deafness (which impairs perception). Martinez-Molina 2016 found 90.9% of anhedonic items were sound-specific.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 0) | sensory_pleasantness value H16 L0 | 1s hedonic signal — absent reward coupling in anhedonia |
| (4, 6, 8, 0) | sensory_pleasantness velocity H6 L0 | Instantaneous hedonic change rate — flat in anhedonia |
| (10, 16, 20, 0) | loudness entropy H16 L0 | 1s affect entropy — low in anhedonia (no reward variability) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: valence signal (preserved perception, absent reward) |
| [4] | sensory_pleasantness | E0: hedonic signal — ABSENT reward coupling in anhedonia |
| [10] | loudness | E1: arousal signal (preserved auditory processing) |
| [11] | onset_strength | E1: event detection (preserved) |

---

## Scientific Foundation

- **Loui et al. 2017**: BMRQ anhedonics vs controls (DTI + behavioral, N=17, d=-5.89); white matter correlates of musical anhedonia
- **Martinez-Molina et al. 2016**: NAcc-STG tract FA correlates with music reward (fMRI + DTI, N=45, r=0.61); 90.9% sound-specific items; NAcc connectivity deficit (d=3.6-7.0)
- **Mas-Herrero et al. 2014**: Dissociation between music and monetary reward — double dissociation (behavioral, significant)
- **Putkinen et al. 2025**: Pleasurable music activates mu-opioid receptors in NAcc, VS, OFC (PET-fMRI, significant)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/mad/extraction.py`
