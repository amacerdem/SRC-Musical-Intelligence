# MSPBA F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:resolution_fc | [0, 1] | Harmonic resolution prediction (0.5-2s ahead). Based on struct_expect trajectory at H18 (2s). Predicts return to tonic after violation -- the resolution of syntactic tension. Wohrle et al. 2024: N1m amplitude at resolution chord reflects preceding dissonance. |
| 9 | F1:eran_trajectory_fc | [0, 1] | mERAN trajectory prediction (200-700ms ahead). Predicts upcoming violation strength based on context depth and dissonance trajectory. Context-dependent: later position = larger predicted mERAN. Maess et al. 2001: 2:1 position ratio. |
| 10 | F2:syntax_repair_fc | [0, 1] | Syntactic repair prediction (1-3s ahead). Broca's area re-analysis of violated structure. Predicts whether the harmonic parse can integrate the violation or must reset. Koelsch review: ERAN reflects long-term memory based syntactic processing. |

---

## Design Rationale

1. **Resolution Forecast (F0)**: Predicts whether harmonic resolution (return to tonic) will occur in the near future (0.5-2s). Uses structural expectation trajectory at the phrase level (H18, 2s). After a violation, the resolution signal indicates when syntactic tension will be resolved. Wohrle et al. 2024 showed that N1m at the resolution chord reflects preceding dominant chord dissonance.

2. **ERAN Trajectory Forecast (F1)**: Predicts the magnitude of the next mERAN response based on current context depth and dissonance trends (H14, 700ms). As more chords accumulate in a progression, the predicted mERAN for any future violation grows larger. This is the anticipatory component of the SSIRH -- the brain pre-allocates syntactic resources.

3. **Syntax Repair Forecast (F2)**: Predicts whether Broca's area will successfully integrate the violation into the ongoing harmonic parse (repair) or will need to reset the syntactic structure. Uses roughness and entropy trends at the progression level. Long violations that persist may trigger a parse reset rather than local repair.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 18, 18, 0) | roughness trend H18 L0 | Dissonance trajectory over phrase for repair forecast |
| (22, 18, 18, 0) | entropy trend H18 L0 | Complexity trajectory over phrase for resolution |
| (4, 18, 19, 0) | sensory_pleasantness stability H18 L0 | Consonance stability over phrase for resolution |
| (1, 14, 8, 0) | sethares_dissonance velocity H14 L0 | Rate of dissonance change for ERAN trajectory |

F-layer primarily uses long-horizon trend features combined with E+M outputs.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:resolution_fc | F6 Reward | Harmonic resolution predicts pleasure/reward |
| F0:resolution_fc | F5 Emotion | Resolution produces emotional satisfaction |
| F1:eran_trajectory_fc | F3 Attention | Anticipated violation allocates attentional resources |
| F1:eran_trajectory_fc | Precision engine | pi_pred estimation for syntactic beliefs |
| F2:syntax_repair_fc | F2 Prediction | Parse repair vs reset decision |

---

## Scientific Foundation

- **Wohrle et al. 2024**: N1m at resolution chord reflects preceding dissonance (MEG, N=30, eta-p2=0.101)
- **Maess et al. 2001**: 2:1 mERAN ratio -- position 5 vs position 3 shows context accumulation (MEG, N=28)
- **Koelsch (in press)**: ERAN reflects long-term memory based syntactic processing, 150-250ms, IFG generators (review)
- **Egermann et al. 2013**: Expectation violation predicts psychophysiological emotional responses (N=50)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mspba/forecast.py`
