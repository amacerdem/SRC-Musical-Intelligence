# VMM Extraction — Valence Core + Regional Pathways (7D)

**Layer**: Extraction (V+R)
**Indices**: [0:7]
**Scope**: internal
**Activation**: tanh (f03_valence) / sigmoid (all others)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | V0:f03_valence | [-1, 1] | Bipolar emotional valence. f00 = tanh(0.50 * happy_pathway - 0.50 * sad_pathway). +1 = maximum positive (happy, joyful), -1 = maximum negative (sad, somber), 0 = neutral/ambiguous. Mitterschiffthaler 2007: double dissociation — VS/DS/ACC (happy) vs HIP/AMY (sad). |
| 1 | V1:mode_signal | [0, 1] | Major/minor mode detection. f01 = sigma(0.40 * brightness_section_H22 + 0.30 * consonance_state_H19 + 0.30 * consonance_mean_H19). 1.0 = strong major, 0.0 = strong minor, 0.5 = ambiguous/atonal. Fritz 2009: cross-cultural (Mafa, N=41, F(2,39)=15.48). |
| 2 | V2:consonance_valence | [0, 1] | Consonance-derived pleasantness. f02 = sigma(0.50 * consonance_state_H19 + 0.30 * spectral_smoothness + 0.20 * warmth). High = consonant, resolved, smooth. Koelsch 2006: consonant music activates VS (t=5.1). |
| 3 | R0:happy_pathway | [0, 1] | Striatal reward circuit composite. f03 = sigma(0.50 * consonance_valence + 0.30 * mode_signal + 0.20 * brightness_section). VS + DS activation for major/consonant music. Mitterschiffthaler 2007: VS t=4.58, DS z=3.80. Trost 2012: Joy -> L.VS z=5.44. |
| 4 | R1:sad_pathway | [0, 1] | Limbic-emotional circuit composite. f04 = sigma(0.40 * (1 - consonance_valence) + 0.30 * (1 - mode_signal) + 0.30 * arousal_modulator). HIP + AMY activation for minor/dissonant music. Mitterschiffthaler 2007: HIP t=4.88. Koelsch 2006: AMY t=4.7, HIP t=6.9. |
| 5 | R2:parahippocampal | [0, 1] | Context processing for BOTH pathways. f05 = sigma(0.40 * consonance_var_H19 + 0.30 * sad_pathway + 0.30 * harmonic_ambiguity). Active for happy AND sad, stronger for contemplative/ambiguous music. Green 2008: minor > major in PHG beyond dissonance. |
| 6 | R3:reward_evaluation | [0, 1] | ACC reward evaluation + affect monitoring. f06 = sigma(0.40 * happy_pathway + 0.30 * mode_signal + 0.30 * coherence_signal). Strongest for confirmed positive valence. Mitterschiffthaler 2007: z=3.39. Trost 2012: sgACC z=6.15 (nostalgia). |

---

## Design Rationale

1. **Valence (V0)**: The primary bipolar valence output — "is this happy or sad?" Computed as the signed difference between happy and sad pathway activations, passed through tanh for [-1,1] normalization. Equal weights (alpha=0.50 for each pathway) reflect Mitterschiffthaler 2007's finding that both pathways contribute equally to the dissociation. Computed AFTER pathways (indices R0, R1) despite lower output index.

2. **Mode Signal (V1)**: Major/minor mode detection requiring phrase-level harmonic context (Krumhansl & Kessler 1982: 2-3 chords minimum). Uses section-level brightness (H22 15s), phrase-level consonance state and mean (H19 3s). Major mode = brighter + more consonant + more resolved. Fritz 2009: both Mafa (Cameroon, no Western exposure) and Germans rely on brightness + consonance for mode classification, confirming biological (not learned) basis.

3. **Consonance Valence (V2)**: Direct consonance-derived pleasantness independent of mode. Consonant music activates the ventral striatum (Koelsch 2006: t=5.1) regardless of major/minor context. Uses consonance state at phrase level combined with spectral smoothness (instrument-like = pleasant) and warmth (low-frequency balance).

4. **Happy Pathway (R0)**: The striatal reward circuit — ventral striatum (NAcc) + dorsal striatum (caudate) + ACC. Activated by consonant + major-mode music. This circuit overlaps with SRP's reward pathway, reflecting that happy music is inherently more rewarding at the neural circuit level.

5. **Sad Pathway (R1)**: The limbic-emotional circuit — hippocampus + amygdala + parahippocampal gyrus. Activated by dissonant + minor-mode music. Arousal modulates intensity: louder sad music activates the limbic circuit more strongly (Trost 2012). This is the circuit that enables "perceived sadness" — the cognitive recognition of sad musical character.

6. **Parahippocampal (R2)**: Context processing region active for BOTH happy and sad music, but particularly elevated for ambiguous or contemplative passages. Green 2008 showed minor activates PHG beyond what dissonance alone explains. Consonance variability (harmonic ambiguity) at H19 drives this — when harmonic context is unstable, context processing increases.

7. **Reward Evaluation (R3)**: ACC reward evaluation — affect monitoring and value judgment. Strongest for confirmed positive valence (happy music that resolves satisfyingly). Trost 2012 found sgACC z=6.15 for nostalgia/tenderness, suggesting this region evaluates the reward value of the current affective state. Coherence signal from cross-feature integration feeds the evaluation.

---

## H3 Dependencies (Extraction)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 19, 0, 2) | sensory_pleasantness value H19 L2 | consonance_state — att.-weighted consonance at 3s |
| (4, 19, 1, 2) | sensory_pleasantness mean H19 L2 | consonance_mean — baseline consonance at 3s |
| (4, 19, 2, 2) | sensory_pleasantness std H19 L2 | consonance_var — harmonic ambiguity at 3s |
| (14, 22, 0, 2) | tonalness value H22 L2 | brightness_section — section brightness at 15s |
| (12, 19, 0, 2) | warmth value H19 L2 | warmth — affective warmth for consonance valence |
| (16, 19, 0, 2) | spectral_smoothness value H19 L2 | smoothness — spectral regularity for consonance valence |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | V2: inverse consonance component |
| [4] | sensory_pleasantness | V1+V2: consonance state and mean for mode + valence |
| [12] | warmth | V2: affective warmth for consonance valence |
| [14] | tonalness | V1: brightness proxy for mode detection (section-level) |
| [16] | spectral_smoothness | V2: instrument-like spectral regularity |

---

## Scientific Foundation

- **Mitterschiffthaler 2007**: Double dissociation — Happy: VS t=4.58, DS z=3.80, ACC z=3.39. Sad: HIP t=4.88 (fMRI, N=16)
- **Koelsch 2006**: Consonant -> VS (t=5.1), Dissonant -> AMY (t=4.7), HIP (t=6.9), PHG (t=5.7) (fMRI, N=11)
- **Trost 2012**: Joy -> L.VS z=5.44, Nostalgia -> R.HIP z=5.62, sgACC z=6.15 (fMRI, N=15)
- **Fritz 2009**: Cross-cultural mode-valence — Mafa (no Western exposure), F(2,39)=15.48 (behavioral, N=41+20)
- **Green 2008**: Minor -> limbic BEYOND dissonance alone — PHG, ventral ACC, mPFC (fMRI)
- **Carraturo 2025**: k=70 meta-analysis confirms major=positive, minor=negative direction across modalities
- **Brattico 2011**: Perceived != felt emotion — separable neural circuits (fMRI, N=15)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/extraction.py`
