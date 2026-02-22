# STAI E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid | clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f01_spectral_integrity | [0, 1] | Consonance preservation index. Tracks STG/planum temporale activation. f01 = sigma(0.40 * helmholtz * stumpf + 0.30 * pleasantness + 0.30 * (1 - roughness)). Kim 2019: spectral disruption reduces bilateral STG (max T=6.852 ACC interaction, N=23); Sarasso 2019: consonance drives aesthetic judgment (eta2_p=0.685, F=45.682, p<0.001). |
| 1 | E1:f02_temporal_integrity | [0, 1] | Forward temporal direction quality. Tracks NAcc/putamen/GP activation. f02 = sigma(0.40 * spec_chg_mean * enrg_chg_vel). Kim 2019: temporal disruption (reversal) reduces NAcc, putamen, GP activation (behavioral d=-1.433 to -1.635); Singer 2023: temporal predictability positively predicts valence (4/5 sections). |
| 2 | E2:f03_aesthetic_integration | [0, 1] | Combined spectral x temporal aesthetic value. vmPFC integration network. f03 = sigma(0.40 * f01 * f02 + 0.30 * x_l4l5_mean + 0.30 * aesthetic_periodicity). Kim 2019: interaction in vmPFC, NAc, caudate, putamen, ACC, thalami (d=0.709 Exp I, d=0.735 Exp II). |
| 3 | E3:f04_vmpfc_ifg_connectivity | [0, 1] | vmPFC-IFG functional connectivity strength. Marker of aesthetic integration pathway. f04 = 0.72 * f03, where 0.72 = mean(d=0.709, d=0.735) from Kim 2019. Kim 2019: vmPFC-IFG connectivity reduced when both spectral+temporal disrupted (PPI analysis). |

---

## Design Rationale

1. **Spectral Integrity (E0)**: The primary spectral quality signal. Combines three consonance measures: helmholtz_kang x stumpf_fusion (harmonic consonance product), sensory pleasantness (spectral regularity), and inverse roughness (sensory dissonance). This triple-consonance extraction maps to bilateral STG and planum temporale, which show additive effects of spectral disruption in Kim 2019's 2x2 factorial design. When consonance is preserved, STG activation is full; when disrupted, activation drops proportionally.

2. **Temporal Integrity (E1)**: The temporal direction quality signal. Uses the product of spectral change mean (300ms) and energy change velocity (300ms) to detect forward temporal flow. Reversed playback disrupts both spectral and energy change patterns, reducing this signal. Maps to NAcc, putamen, and globus pallidus, which show reduced activation under temporal disruption. Supported by Singer 2023 showing temporal predictability predicts valence.

3. **Aesthetic Integration (E2)**: The critical interaction term. The multiplicative binding f01 * f02 captures the finding that aesthetic preference requires both spectral and temporal integrity. Neither dimension alone suffices. The x_l4l5 binding signal and aesthetic periodicity provide additional binding evidence from R3 interactions and H3 temporal structure. This is the vmPFC integration that creates the full aesthetic response.

4. **vmPFC-IFG Connectivity (E3)**: A scaled derivative of aesthetic integration, representing the functional connectivity strength between vmPFC and IFG. The scaling factor 0.72 is the mean of the two behavioral interaction effect sizes from Kim 2019 (d=0.709 and d=0.735). When both dimensions are disrupted, this connectivity drops, reflecting loss of the aesthetic integration pathway.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 0, 0, 2) | roughness value H0 L2 | Current dissonance at 25ms |
| (0, 3, 1, 2) | roughness mean H3 L2 | Mean dissonance over 100ms |
| (2, 0, 0, 2) | helmholtz_kang value H0 L2 | Current consonance at 25ms |
| (2, 3, 1, 2) | helmholtz_kang mean H3 L2 | Mean consonance over 100ms |
| (4, 3, 0, 2) | pleasantness value H3 L2 | Pleasantness at 100ms |
| (21, 8, 1, 0) | spectral_change mean H8 L0 | Mean spectral flux over 300ms |
| (22, 8, 8, 0) | energy_change velocity H8 L0 | Energy change rate over 300ms |
| (33, 8, 0, 2) | x_l4l5[0] value H8 L2 | Aesthetic binding at 300ms |
| (33, 8, 14, 2) | x_l4l5[0] periodicity H8 L2 | Binding periodicity over 300ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: spectral integrity (inverse dissonance) |
| [1] | sethares_dissonance | E0: dissonance proxy |
| [2] | helmholtz_kang | E0: consonance measure |
| [3] | stumpf_fusion | E0: tonal fusion |
| [4] | sensory_pleasantness | E0: spectral regularity |
| [7] | amplitude | E1: energy level baseline |
| [8] | loudness | E1: perceptual loudness |
| [11] | onset_strength | E1: attack clarity (forward/reversed cue) |
| [21] | spectral_change | E1: spectral flux for temporal direction |
| [22] | energy_change | E1: energy dynamics for temporal direction |
| [33:41] | x_l4l5 (8D) | E2: aesthetic binding signal |

---

## Scientific Foundation

- **Kim et al. 2019**: 2x2 factorial (consonant/dissonant x forward/reversed). Interaction in vmPFC, NAc, caudate, putamen, ACC, thalami. R ACC T=6.852 p<10^-5; behavioral interaction d=0.709 (Exp I, N=16), d=0.735 (Exp II, N=23); vmPFC-IFG connectivity reduced for both-disrupted (fMRI PPI)
- **Sarasso et al. 2019**: Consonance drives aesthetic judgment; N1-P2 enhanced for appreciated intervals (EEG, N=22+22, eta2_p=0.685, F=45.682, p<0.001)
- **Singer et al. 2023**: Temporal predictability positively predicts valence across 1780-song database (behavioral, N=40, positive correlation 4/5 sections)
- **Alluri et al. 2012**: Timbral features -> STG/HG; rhythmic -> motor/limbic; tonal -> prefrontal. Brightness -> putamen Z=3.63; fullness -> STG Z=7.35 (fMRI naturalistic, N=11)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/stai/extraction.py`
