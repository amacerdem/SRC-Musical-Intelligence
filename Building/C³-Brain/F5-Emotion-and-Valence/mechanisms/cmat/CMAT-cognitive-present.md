# CMAT P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [6:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid | tanh

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:multi_sens_salien | [0, 1] | Multi-sensory salience signal. multi_salience = sigma(0.5 * aud_arousal + 0.5 * affect_mean). Combines direct arousal (loudness) with H3 affect dynamics to produce the overall multi-sensory attention capture signal. In multi-modal contexts, this reflects the combined salience of all modalities. Petrini 2010: audio-visual integration enhances perceptual salience. |
| 7 | P1:aud_valence_contr | [-1, 1] | Auditory valence contribution. aud_val_contrib = tanh(0.5 * aud_valence + 0.5 * integration_state). The auditory modality's contribution to the unified affective experience — combines the direct auditory valence with the cognitive-projection H3 integration state. Taruffi 2021: vmPFC centrality mediates auditory valence transfer. |

---

## Design Rationale

1. **Multi-Sensory Salience (P0)**: The present-moment salience signal reflecting the attention-capturing power of the multi-sensory input. In audio-only mode, this combines loudness-based arousal with temporal affect dynamics. In multi-modal mode, it would additionally incorporate visual and tactile salience. This output feeds the kernel's salience computation for attention allocation.

2. **Auditory Valence Contribution (P1)**: The auditory modality's contribution to the overall emotional experience. Uses tanh for bidirectional range — negative auditory valence (dissonant, rough) reduces the overall affective experience while positive auditory valence (consonant, pleasant) enhances it. The cognitive-projection integration state provides temporal context for the valence estimation.

---

## Kernel Relay Export

P-layer outputs feed the kernel relay for cross-function integration:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `multi_sens_salien` | P0 [6] | Salience: multi-modal attention capture |
| `aud_valence_contr` | P1 [7] | Emotion: auditory valence for unified affect |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 6, 0, 2) | loudness value H6 L2 | Current arousal for salience |
| (4, 11, 1, 0) | sensory_pleasantness mean H11 L0 | Cognitive-projection integration state |
| (4, 6, 0, 2) | sensory_pleasantness value H6 L2 | Instant affect for valence contribution |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P1: inverse consonance for auditory valence |
| [4] | sensory_pleasantness | P1: hedonic quality for auditory valence |
| [10] | loudness | P0: arousal for multi-sensory salience |

---

## Scientific Foundation

- **Petrini et al. 2010**: Audio-visual drumming integration enhances perceptual salience and temporal binding (behavioral, N=18, Experimental Brain Research)
- **Taruffi et al. 2021**: vmPFC/mOFC centrality mediates auditory valence transfer; trait empathy modulates cross-modal affect (fMRI, N=24, Cognitive, Affective, & Behavioral Neuroscience)
- **Spence 2011**: Cross-modal correspondences: auditory features systematically map to visual/spatial affect (tutorial review, Attention, Perception, & Psychophysics)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/cmat/cognitive_present.py`
