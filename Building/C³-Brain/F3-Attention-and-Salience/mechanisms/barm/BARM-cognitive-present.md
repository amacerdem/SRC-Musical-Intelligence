# BARM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:beat_alignment_accuracy | [0, 1] | Beat-entrainment beat-locked alignment. Real-time measure of how accurately the internal beat representation matches the external rhythm. Grahn & Brett 2007: STG beta correlation r=0.42 with alignment accuracy. |
| 6 | P1:regularization_strength | [0, 1] | Groove-driven regularization magnitude. sigma(...+0.5*f10). How strongly the system is currently regularizing — high values indicate the listener is "hearing" more regularity than the signal contains. Rathcke 2024: regularization tied to groove perception. |

---

## Design Rationale

1. **Beat Alignment Accuracy (P0)**: The present-moment alignment signal. This captures the instantaneous accuracy of beat tracking — how well-aligned the internal beat template is to the incoming rhythm. Feeds downstream to F7 Motor for movement timing and to the kernel scheduler for salience computation. High values indicate precise beat-locked perception.

2. **Regularization Strength (P1)**: The present-moment regularization signal. Combines E-layer regularization tendency (f10) with groove context. When regularization is high, the system is actively distorting temporal perception toward isochrony. This feeds the precision engine — high regularization reduces temporal prediction error because the internal model is simpler.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `beat_alignment_accuracy` | P0 [5] | Salience: contributes to beat-locked component |
| `regularization_strength` | P1 [6] | Precision engine: regularization modulates pi_pred |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 3, 1, 2) | onset_strength mean H3 L2 | Sustained onset for alignment measurement |
| (21, 8, 14, 0) | spectral_change periodicity H8 L0 | Tempo periodicity for regularization context |
| (7, 16, 1, 2) | amplitude mean H16 L2 | Mean amplitude over 1s — groove strength |

---

## Scientific Foundation

- **Grahn & Brett 2007**: STG beta oscillation r=0.42 correlation with beat alignment accuracy (fMRI, N=27)
- **Rathcke et al. 2024**: Regularization strength correlates with groove perception (N=87)
- **Hoddinott & Grahn 2024**: 7T RSA separates alignment accuracy from regularization in motor cortex
- **Lazzari et al. 2025**: R dPMC TMS disruption (OR=22.16) differentially affects alignment vs regularization

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/barm/cognitive_present.py`
