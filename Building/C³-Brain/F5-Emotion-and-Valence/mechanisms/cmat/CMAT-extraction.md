# CMAT E-Layer — Extraction (1D)

**Layer**: Extraction (E)
**Indices**: [0:1]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f13_cross_modal | [0, 1] | Cross-modal transfer strength. f13 = cross_modal_quality * sigma(0.5 * abs(aud_valence) + 0.5 * affect_mean). Product of supramodal quality (brightness-warmth cross-modal features) and absolute affective intensity. High when auditory-visual affect aligns and both modalities carry strong emotional content. Spence 2011: systematic cross-modal correspondences between pitch and brightness, tempo and arousal. |

---

## Design Rationale

1. **Cross-Modal Transfer (E0)**: The single extraction feature measures the overall strength of affective transfer between auditory and other sensory modalities. Computed as the product of cross-modal quality (how well the auditory signal maps to supramodal features like brightness and warmth) and affective intensity (how strongly the current audio carries emotional content). In audio-only mode, this provides a baseline estimate of cross-modal transfer potential based on the acoustic features that systematically correspond to other modalities. The multiplicative gate ensures transfer is strong only when both the cross-modal feature quality AND the affective content are present.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 6, 0, 2) | sensory_pleasantness value H6 L2 | Instant affect state for cross-modal mapping |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Sustained affect for transfer estimation |
| (0, 6, 0, 2) | roughness value H6 L2 | Instant dissonance for valence computation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: inverse consonance for auditory valence |
| [4] | sensory_pleasantness | E0: direct hedonic for auditory valence |
| [10] | loudness | E0: arousal signal for affective intensity |
| [15] | brightness | E0: supramodal brightness — auditory-visual correspondence |
| [16] | warmth | E0: supramodal warmth — auditory-thermal/color correspondence |

---

## Scientific Foundation

- **Spence 2011**: Systematic cross-modal correspondences: high pitch maps to brightness, fast tempo to high arousal visuals, major mode to warm colors (tutorial review, Attention, Perception, & Psychophysics, 73(4), 971-995)
- **Molholm et al. 2002**: Early auditory-visual interactions at 46ms — cross-modal binding begins in primary sensory areas (ERP, N=10)
- **Tsuji & Cristia 2025**: Cross-modal affect transfer demonstrated in infant speech and music perception — habituation transfers across modalities (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/cmat/extraction.py`
