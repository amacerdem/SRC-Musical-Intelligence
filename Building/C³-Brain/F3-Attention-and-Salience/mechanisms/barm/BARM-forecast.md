# BARM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:beat_accuracy_pred_0.75s | [0, 1] | Veridical perception prediction ~0.75s ahead. sigma(0.5*f11 + 0.5*beat_period_1s). Predicts how accurately the listener will perceive the next beat based on current alignment ability and beat periodicity. |
| 8 | F1:sync_benefit_pred | [0, 1] | Movement benefit prediction. sigma(0.5*f12 + 0.5*coupling_period_1s). Forecasts whether upcoming motor synchronization will enhance perception. Hoddinott & Grahn 2024: sync benefit predictable from coupling strength. |
| 9 | F2:individual_diff_pred | [0, 1] | Session-level BAT screening prediction. f11 (direct copy). Stable individual-difference estimate — does not change rapidly within a piece. Niarchou 2022: h²=0.13-0.16 confirms trait-level stability. |

---

## Design Rationale

1. **Beat Accuracy Prediction (F0)**: Predicts veridical perception quality ~0.75s ahead. Combines current beat alignment (f11) with beat periodicity at 1s to forecast whether the next beat will be accurately perceived. This feeds the precision engine — high predicted accuracy means low expected prediction error.

2. **Sync Benefit Prediction (F1)**: Forecasts motor-synchronization benefit. Combines current sync benefit (f12) with motor-auditory coupling periodicity to predict whether upcoming movement will enhance beat perception. Feeds F7 Motor for anticipatory movement planning.

3. **Individual Difference Prediction (F2)**: A direct copy of f11 (beat alignment), serving as a stable session-level estimate of beat ability. This is quasi-static — it changes very slowly across a musical piece, reflecting the trait-like nature of BAT. Used by the kernel for individual-difference modulation of processing parameters.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Beat periodicity for accuracy extrapolation |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Coupling periodicity for sync benefit forecast |
| (25, 16, 21, 2) | x_l0l5[0] zero_crossings H16 L2 | Phase resets in coupling — boundary detection |
| (25, 3, 14, 2) | x_l0l5[0] periodicity H3 L2 | Fast coupling periodicity for short-term prediction |

F-layer primarily reuses E+M outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:beat_accuracy_pred_0.75s | Precision engine | pi_pred estimation for beat-related beliefs |
| F1:sync_benefit_pred | F7 Motor | Anticipatory movement planning |
| F2:individual_diff_pred | Kernel scheduler | Session-level BAT modulation parameter |

---

## Scientific Foundation

- **Hoddinott & Grahn 2024**: Sync benefit predictable from motor-auditory coupling (7T RSA)
- **Niarchou et al. 2022**: Beat synchronization heritability h²=0.13-0.16, confirming trait stability (GWAS, N=606k)
- **Lazzari et al. 2025**: R dPMC TMS shows causal role of premotor cortex in beat prediction (OR=22.16)
- **Grahn & Brett 2007**: Individual differences in beat prediction linked to putamen + SMA (fMRI, N=27)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/barm/forecast.py`
