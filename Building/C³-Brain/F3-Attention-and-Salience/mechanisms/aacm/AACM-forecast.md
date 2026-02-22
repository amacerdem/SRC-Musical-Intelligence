# AACM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:behavioral_pred_0.75s | [0, 1] | RT slowing prediction 0.75s ahead. sigma(0.5*f18_savoring + 0.5*integration_mean_1s). Predicts whether the listener will show behavioral slowing — motor system inhibition from aesthetic engagement. Foo 2016: RT predicts preference. |
| 8 | F1:n2p3_pred_0.4s | [0, 1] | Motor pause prediction 0.4s ahead. Predicts N2/P3 motor inhibition — whether the motor system will pause in response to upcoming aesthetic content. Sarasso 2019: N2/P3 linked to motor inhibition during preferred intervals. |
| 9 | F2:aesthetic_pred_1.5s | [0, 1] | Aesthetic rating prediction 1.5s ahead. sigma(0.5*aesthetic_engagement + 0.5*pleasant_velocity_1s). Predicts the listener's ongoing aesthetic evaluation trajectory. Kim 2019: vmPFC slow fluctuation during aesthetic appreciation. |

---

## Design Rationale

1. **Behavioral Prediction (F0)**: The behavioral forecast — "will the listener slow down?" Combines current savoring effect with sustained integration context to predict RT slowing 0.75s ahead. This prediction horizon matches the typical aesthetic response lag. Feeds downstream for precision engine pi_pred estimation.

2. **N2/P3 Prediction (F1)**: The motor inhibition forecast — "will the motor system pause?" Predicts N2/P3 ERP amplitude 0.4s ahead, corresponding to the typical N2/P3 latency. Motor inhibition is an automatic response to preferred stimuli.

3. **Aesthetic Prediction (F2)**: The evaluation forecast — "will aesthetic engagement increase?" Combines the M-layer aesthetic engagement with hedonic velocity to predict the trajectory of aesthetic experience 1.5s ahead. This is the longest prediction horizon, reflecting the slow fluctuation of aesthetic judgment.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 16, 1, 0) | integration mean H16 L0 | Sustained integration context for behavioral prediction |
| (3, 16, 8, 2) | pleasant velocity H16 L2 | Hedonic change rate for aesthetic trajectory |
| (25, 8, 0, 2) | integration value H8 L2 | Mid-range integration for motor prediction |
| (25, 3, 0, 2) | integration value H3 L2 | Short-range integration at 100ms |

F-layer also integrates E+M outputs for prediction computations.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:behavioral_pred_0.75s | F6 Reward | PE from behavioral prediction |
| F1:n2p3_pred_0.4s | F7 Motor | Motor preparation timing |
| F2:aesthetic_pred_1.5s | F5 Emotion | Aesthetic trajectory context |
| F2:aesthetic_pred_1.5s | Precision engine | pi_pred estimation |

---

## H3 Full Demand (12 tuples, all layers)

```
(0, 3, 0, 2)     roughness value H3 L2
(0, 16, 1, 2)    roughness mean H16 L2
(3, 3, 0, 2)     pleasant value H3 L2
(3, 6, 6, 2)     pleasant periodicity H6 L2
(3, 16, 8, 2)    pleasant velocity H16 L2
(8, 3, 0, 2)     loudness value H3 L2
(8, 3, 2, 2)     loudness std H3 L2
(8, 16, 20, 2)   loudness entropy H16 L2
(25, 3, 0, 2)    integration value H3 L2
(25, 8, 0, 2)    integration value H8 L2
(25, 16, 1, 0)   integration mean H16 L0
(25, 16, 8, 0)   integration velocity H16 L0
```

---

## Brain Regions

STG/HG, IFG, vmPFC, NAcc, Caudate, Amygdala, ACC, Motor Cortex

---

## Scientific Foundation

- **Sarasso 2019**: N1/P2 and N2/P3 proportional to aesthetic preference (EEG, eta2p=0.685, d=2.008)
- **Salimpoor 2011**: Dopaminergic reward during pleasurable music (PET, r=0.71)
- **Kim 2019**: vmPFC activation during aesthetic judgments (fMRI, T=6.852)
- **Foo 2016**: RT slowing as behavioral marker of appreciation

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/aacm/forecast.py`
