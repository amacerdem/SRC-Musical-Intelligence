# CLAM E-Layer — Extraction (2D)

**Layer**: Extraction (E)
**Indices**: [0:2]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f09_affective_mod | [0, 1] | BCI modulation success metric. f09 = clamp(1 - \|target - current\| / scale, 0, 1). Ehrlich 2019: arousal tracking r=0.74, valence tracking r=0.52. Measures how well the closed-loop controller drives affective state toward target. |
| 1 | E1:loop_coherence | [0, 1] | Closed-loop synchronization quality. Granger causality strength in both directions (music to gamma, gamma to music). 1.0 = perfect bidirectional causality. Ehrlich 2019: bidirectional Granger causality p<0.01 in 3/5 participants. |

---

## Design Rationale

1. **Affective Modulation Success (E0)**: The primary CLAM extraction feature. Measures the real-time success of the closed-loop BCI in steering affective state toward the therapeutic or user-defined target. Computed as the inverse of the normalized error between target and decoded affect. Ehrlich 2019 demonstrated arousal tracking at r=0.74 and valence tracking at r=0.52, showing that music-based BCI can achieve moderate-to-strong affect modulation. This feeds clinical applications via TAR (Therapeutic Affective Resonance).

2. **Loop Coherence (E1)**: Tracks the bidirectional causal coupling between generated music and brain state. A coherent loop means music causally affects brain gamma power AND brain state causally influences music generation parameters. Ehrlich 2019 established bidirectional Granger causality (p<0.01) as the gold standard for confirming a true closed loop, distinguishing BCI control from mere correlation. Low coherence indicates the loop has broken down (non-responder or system failure).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 20, 0) | loudness entropy H16 L0 | 1s entropy of arousal signal for affect decode |
| (10, 7, 8, 0) | loudness velocity H7 L0 | Instantaneous arousal change rate |
| (0, 16, 0, 0) | roughness value H16 L0 | 1s valence baseline for loop comparison |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: inverse pleasantness for valence decoding |
| [4] | sensory_pleasantness | E0: hedonic signal for target comparison |
| [10] | loudness | E0: energy level for arousal estimation |
| [21] | spectral_flux | E1: frame-to-frame change for real-time feedback |

---

## Scientific Foundation

- **Ehrlich et al. 2019**: Arousal target correlates with perceived arousal (EEG-BCI + music gen, N=11, r=0.74); valence tracking (r=0.52); bidirectional Granger causality (N=5, p<0.01)
- **Daly et al. 2016**: Brain activity + acoustic features predict emotion (EEG + music, significant)
- **Sayal et al. 2025**: Music-based neurofeedback: reward-system coupling critical for success; music improves NF engagement vs standard feedback (systematic review, N=20+ studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/clam/extraction.py`
