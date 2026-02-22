# CSG F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [9:12]
**Scope**: external
**Activation**: tanh (F0), sigmoid (F1, F2)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:valence_pred | [-1, 1] | Predicted valence (tanh). tanh(0.50*E2 + 0.30*pleas_mean_1s + 0.20*spectral_auto_h16). Cheung 2019: amygdala/hippocampus integrate uncertainty x surprise. |
| 10 | F1:processing_pred | [0, 1] | Predicted processing load. sigma(0.40*E1 + 0.30*ambiguity + 0.30*roughness_mean). Bravo 2017: intermediate dissonance = highest processing demand. |
| 11 | F2:aesthetic_pred | [0, 1] | Predicted aesthetic appreciation. sigma(0.50*M2 + 0.50*consonance). Sarasso 2019: consonance -> aesthetic preference (d=2.008). |

---

## Design Rationale

Three forward predictions:

1. **Valence Prediction (F0)**: Uses **tanh** for [-1, 1] range. Inherits consonance-valence mapping from E2, adds sustained pleasantness (1s) for tonic context and long-range spectral autocorrelation for structural prediction. The 1s timescales (H16) provide the stable baseline from which valence deviations can be predicted.

2. **Processing Load Prediction (F1)**: Predicts how much cognitive processing the next segment will require. E1 (sensory evidence at intermediate levels) is the strongest predictor. Ambiguity captures the inverted-U. Roughness mean (100ms) adds the local dissonance context.

3. **Aesthetic Prediction (F2)**: Predicts appreciation level. M2 (aesthetic appreciation from temporal integration) provides the accumulated aesthetic signal, combined with raw consonance. The 50/50 split balances temporal context with instantaneous quality.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 1, 2) | sensory_pleasantness mean H16 L2 | Sustained pleasantness (reused) |
| (17, 16, 1, 2) | spectral_autocorrelation mean H16 L2 | Long-range structural coupling |
| (0, 3, 1, 2) | roughness mean H3 L2 | Roughness context (reused) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 4 | sensory_pleasantness | F2: consonance proxy for aesthetic prediction |

---

## Scientific Foundation

- **Cheung 2019**: Amygdala/hippocampus reflect uncertainty x surprise; NAc reflects uncertainty; harmonic expectancy salience integration (fMRI, N=79)
- **Bravo 2017**: Intermediate dissonance -> highest processing demand and longest RT
- **Sarasso 2019**: Consonance -> aesthetic preference (d=2.008, EEG N=22)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/csg/forecast.py`
