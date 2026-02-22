# CLAM P-Layer — Cognitive Present (2D)

**Layer**: Cognitive Present (P)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid (idx 7), tanh (idx 8)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:arousal_modulation | [0, 1] | Current arousal-driven modulation strength. sigma(0.5 * arousal_dynamics.mean + 0.5 * trigger_features.mean). Tracks how strongly the BCI is currently modulating arousal. Ehrlich 2019: arousal tracking r=0.74 (strongest control dimension). |
| 8 | P1:valence_tracking | [-1, 1] | Current valence tracking quality. tanh(decoded_affect * loop_coherence). Valence signal scaled by loop coherence — meaningful only when loop is functional. Ehrlich 2019: valence tracking r=0.52 (weaker than arousal). |

---

## Design Rationale

1. **Arousal Modulation (P0)**: Captures the real-time strength of arousal control in the BCI loop. Arousal is the dominant controllable dimension — Ehrlich 2019 showed r=0.74 tracking quality versus only r=0.52 for valence. This asymmetry likely reflects the tight coupling between tempo/dynamics (easily manipulated musical parameters) and arousal (directly reflected in gamma power and ANS). Uses a weighted combination of arousal dynamics (energy tracking) and trigger features (onset detection) to estimate modulation effectiveness.

2. **Valence Tracking (P1)**: Measures the quality of valence control in the current moment. Valence is harder to modulate because it depends on mode, harmony, and timbral features that are less directly linked to simple musical parameter adjustments. The signal is gated by loop coherence — when the loop is incoherent, valence tracking is meaningless (tanh product collapses toward zero). This reflects the clinical reality that valence modulation requires a well-functioning BCI loop as a prerequisite.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 7, 8, 0) | loudness velocity H7 L0 | Instantaneous arousal change for modulation tracking |
| (8, 7, 8, 0) | velocity_A velocity H7 L0 | Dynamic rate for arousal modulation estimate |
| (4, 12, 0, 0) | sensory_pleasantness value H12 L0 | Half-beat hedonic state for valence tracking |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [8] | velocity_A | P0: arousal dynamics rate |
| [10] | loudness | P0: energy-level arousal estimation |
| [11] | onset_strength | P0: trigger features for arousal modulation |
| [4] | sensory_pleasantness | P1: valence signal basis |

---

## Scientific Foundation

- **Ehrlich et al. 2019**: Arousal tracking r=0.74 (strongest BCI dimension); valence tracking r=0.52 (weaker); asymmetry reflects arousal-tempo coupling vs valence-mode complexity (EEG-BCI, N=11)
- **Ehrlich et al. 2019**: 3/5 participants showed successful bidirectional Granger causality — individual differences in loop responsiveness (N=5, p<0.01)
- **Sayal et al. 2025**: Music improves neurofeedback engagement vs standard auditory/visual feedback — reward-system coupling enhances loop (systematic review, N=20+ studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/clam/cognitive_present.py`
