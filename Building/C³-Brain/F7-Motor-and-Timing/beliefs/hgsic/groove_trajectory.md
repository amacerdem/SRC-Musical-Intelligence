# groove_trajectory -- Anticipation Belief (HGSIC)

**Category**: Anticipation (prediction)
**Owner**: HGSIC (STU-beta5)

---

## Definition

"Groove will continue/change within 110ms." Predicts the groove state trajectory approximately one auditory-motor propagation delay (110ms) into the future. This is the motor system's groove prediction: based on current beat x meter x motor integration and the amplitude trend, will the groove intensify, sustain, or diminish? The 110ms prediction horizon matches the characteristic pSTG-to-motor cortex delay.

---

## Observation Formula

```
# From HGSIC F-layer:
groove_trajectory = HGSIC.groove_prediction[F0]  # index [8]

# Formula: sigma(0.5 * f03_motor_groove + 0.4 * amplitude_trend)
# where f03 = current motor groove state
# amplitude_trend = H3 (7, 16, 18, 0)  -- amplitude trend at 1s
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted groove trajectory mismatches the observed groove evolution.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HGSIC F0 | groove_prediction [8] | Predicted groove state (110ms ahead) |
| HGSIC E2 | f03_motor_groove [2] | Current motor groove state |
| H3 | (7, 16, 18, 0) | Amplitude trend at H16 (1s bar level) |
| H3 | (7, 16, 15, 0) | Amplitude smoothness (groove quality proxy) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | Groove prediction PE feeds anticipatory reward signal |
| groove_quality (Core) | Groove trajectory feeds predict() as context |
| Precision engine | pi_pred estimation for groove predictions |

---

## Scientific Foundation

- **Potes et al. 2012**: 110ms auditory-motor delay defines prediction horizon; r=0.70 cross-correlation (ECoG, N=4)
- **Spiech et al. 2022**: Groove inverted-U with syncopation, chi2(1)=14.643 -- groove trajectories follow dynamic path (Pupillometry+behavioral, N=30)
- **Large et al. 2023**: Dynamical systems model -- groove oscillator generates forward predictions (Review)
- **Ayyildiz et al. 2025**: Micro-timing (SD=4ms) affects groove-adjacent engagement, Odds=100.69 (Behavioral, N=100)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
