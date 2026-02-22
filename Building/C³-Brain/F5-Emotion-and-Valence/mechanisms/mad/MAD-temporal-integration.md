# MAD D+A-Layers — Temporal Integration (5D)

**Layer**: Temporal Integration (D: Disconnection Markers + A: Anhedonia Assessment)
**Indices**: [2:7]
**Scope**: internal (D) + exported (A: kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 2 | D0:stg_nacc_connect | [0, 1] | White matter tract integrity (fractional anisotropy). The uncinate fasciculus connecting STG to NAcc. Martinez-Molina 2016: FA correlates with music reward r=0.61. Estimated from reward-response coupling over H16 (1s) integration. |
| 3 | D1:nacc_music_resp | [0, 1] | Music-specific NAcc activation. sigma(0.5 * sensory_pleasantness[4] * reward_signal + 0.5 * auditory * connectivity). IMPAIRED in anhedonia — the core deficit. Martinez-Molina 2016: NAcc deficit d=3.6-7.0. |
| 4 | D2:nacc_general_resp | [0, 1] | Non-music NAcc activation. sigma(reward_signal * 2.0). PRESERVED in anhedonia — the double dissociation. VTA-NAcc pathway intact; only STG-NAcc disconnected. Mas-Herrero 2014: monetary reward preserved. |
| 5 | A0:bmrq_estimate | [0, 1] | Barcelona Music Reward Questionnaire proxy. bmrq = 1.0 - f10_anhedonia. Low BMRQ corresponds to high anhedonia score. Loui 2017: BMRQ is the primary screening tool for musical anhedonia (d=-5.89 deficit). |
| 6 | A1:sound_specificity | [0, 1] | Sound-specific anhedonia index. sigma(0.5 * dissociation + 0.5 * (1.0 - affect_entropy)). Measures how selectively the deficit targets auditory reward. Martinez-Molina 2016: 90.9% of anhedonic items are sound-specific. |

---

## Design Rationale

1. **STG-NAcc Connectivity (D0)**: Estimates the functional integrity of the white matter tract connecting auditory cortex (STG) to reward circuitry (NAcc) via the uncinate fasciculus. In clinical DTI, this is measured as fractional anisotropy (FA). In the real-time model, connectivity is estimated from the coupling strength between auditory features and reward responses over the H16 (1s) integration window. Martinez-Molina 2016 showed this tract's FA directly predicts music reward capacity (r=0.61).

2. **Music-Specific NAcc Response (D1)**: The core deficit marker. In normal listeners, pleasant music activates NAcc; in musical anhedonia, the auditory signal reaches STG normally but fails to propagate to NAcc. This dimension combines the hedonic signal (sensory_pleasantness) with the reward signal, modulated by connectivity. Low D1 with high D2 (general reward) is the pathognomonic pattern.

3. **General NAcc Response (D2)**: The preservation marker. This dimension tracks NAcc activation through non-auditory pathways (VTA-NAcc), which remain intact in musical anhedonia. Elevated D2 alongside depressed D1 confirms the disconnection is pathway-specific, not a global reward deficit. Mas-Herrero 2014 demonstrated this dissociation with monetary rewards.

4. **BMRQ Estimate (A0)**: A real-time proxy for the Barcelona Music Reward Questionnaire score. Simply the inverse of the anhedonia marker — higher values indicate greater music reward capacity. The BMRQ is the gold-standard behavioral screening tool (Loui 2017), and this dimension provides a continuous, frame-rate estimate of where the listener falls on the BMRQ spectrum.

5. **Sound Specificity (A1)**: Quantifies the selectivity of the hedonic deficit for auditory stimuli. High specificity means only sound-related rewards are affected; low specificity would suggest broader anhedonia. Uses the dissociation index combined with the inverse of affect entropy — in anhedonia, affect entropy is low because reward-driven variability is absent, producing a flat affective signal. Martinez-Molina 2016 found 90.9% of anhedonic questionnaire items were sound-specific.

---

## H3 Dependencies (D+A-Layers)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 0) | sensory_pleasantness value H16 L0 | 1s hedonic state for NAcc music response |
| (4, 11, 8, 0) | sensory_pleasantness velocity H11 L0 | Reward dynamics at 500ms — flat in anhedonia |
| (10, 16, 0, 0) | loudness value H16 L0 | 1s arousal for general NAcc response |
| (10, 11, 2, 0) | loudness std H11 L0 | Reward variability — low std in anhedonia |
| (0, 16, 20, 0) | roughness entropy H16 L0 | Affect entropy — low in anhedonia |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | D1: valence signal (preserved perception) |
| [2] | harmonic_ratio | D1: consonance perception (preserved) |
| [4] | sensory_pleasantness | D1: hedonic signal for music NAcc response |
| [10] | loudness | D2: arousal for general NAcc response |
| [33:41] | x_l4l5 (8D) | D0: dynamics x consonance — the DISRUPTED coupling link |

---

## Scientific Foundation

- **Martinez-Molina et al. 2016**: NAcc-STG tract FA correlates with music reward (fMRI + DTI, N=45, r=0.61); NAcc connectivity deficit (d=3.6-7.0); 90.9% sound-specific items
- **Loui et al. 2017**: BMRQ screening for musical anhedonia (DTI + behavioral, N=17, d=-5.89)
- **Mas-Herrero et al. 2014**: Dissociation music vs monetary reward — double dissociation confirms pathway specificity (behavioral, significant)
- **Jin et al. 2025**: Congenital amusia shows lower music reward across all 5 BMRQ subscales (behavioral, N=88, significant)
- **Putkinen et al. 2025**: Pleasurable music activates mu-opioid receptors in NAcc, VS, OFC — opioid mechanism absent in anhedonia (PET-fMRI, significant)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/mad/temporal_integration.py`
