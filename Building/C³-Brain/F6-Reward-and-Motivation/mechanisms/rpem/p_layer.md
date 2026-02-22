# RPEM — Cognitive Present

**Model**: Reward Prediction Error in Music
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | current_rpe | Current signed reward prediction error. clamp(f03 - f04 + 0.5, 0, 1). The real-time RPE signal representing the listener's present prediction error state. Values > 0.5 indicate positive RPE (better than expected), values < 0.5 indicate negative RPE (worse than expected), 0.5 indicates matched expectations. This is the primary learning signal that drives preference updating. Gold 2023: VS RPE crossover (d = 1.07). Cheung 2019: uncertainty x surprise jointly predict pleasure. |
| 7 | vs_activation_state | Current ventral striatum activation level. σ(0.5 * current_rpe + 0.5 * rpe_magnitude). Represents the overall VS engagement regardless of RPE sign — a combination of the signed RPE and the unsigned magnitude. High values indicate strong striatal processing whether the prediction error is positive or negative. Gold 2023: VS shows IC x liking interaction; Salimpoor 2011: DA release in VS at emotional peaks. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 8 | M8 (velocity) | L0 (fwd) | RPE coupling velocity at 500ms — RPE dynamics |
| 1 | 25 | 8 | M1 (mean) | L2 (bidi) | Prediction mean at 500ms — expected reward baseline |

---

## Computation

The P-layer produces the "present-moment" RPE state that is exported to the C³ kernel scheduler. These are the relay fields that downstream beliefs and the reward computation read.

1. **Current RPE**: The signed prediction error centered at 0.5, computed identically to vs_response in the M-layer. This represents the real-time learning signal — the difference between what the listener expected and what occurred. It feeds the core C³ belief update mechanism: large positive RPE increases precision-weighted gain for beliefs, while negative RPE decreases it.

```
current_rpe = clamp(f03 - f04 + 0.5, 0.0, 1.0)
```

2. **VS Activation State**: Combines the signed RPE with unsigned magnitude via sigmoid to produce an overall striatal engagement signal. This captures the finding that VS shows elevated BOLD during any strong prediction error, even negative ones (though the pattern differs in sign). The sigmoid ensures bounded [0,1] output.

```
vs_activation_state = σ(0.5 * current_rpe + 0.5 * rpe_magnitude)
```

The P-layer outputs are critical for:
- The reward computation (RPE drives reward learning signal)
- Cross-relay interaction with DAED (RPE modulates anticipatory DA)
- IMU prediction update (RPE is the error signal for memory consolidation)
- Precision engine (RPE magnitude modulates pi_obs)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_positive_rpe | Positive component for signed RPE |
| E-layer | f04_negative_rpe | Negative component for signed RPE |
| M-layer | rpe_magnitude | Unsigned RPE for VS activation |
| M-layer | vs_response | Cross-validation with P-layer current_rpe |
| H³ | 2 tuples (see above) | RPE dynamics and prediction baseline context |
| RPEM relay (RPU) | positive_rpe, negative_rpe | Kernel export: feeds reward surprise component |
| RPEM relay (RPU) | vs_activation_state | Kernel export: feeds salience and precision |
