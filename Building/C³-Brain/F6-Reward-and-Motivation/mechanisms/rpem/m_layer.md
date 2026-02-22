# RPEM — Temporal Integration

**Model**: Reward Prediction Error in Music
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | rpe_magnitude | Absolute RPE magnitude. max(f03_positive_rpe, f04_negative_rpe). Captures the unsigned strength of the prediction error regardless of valence. High values indicate strongly unexpected events (either positively or negatively surprising). This drives attention and learning — large RPE signals update the internal model. Gold 2023: VS BOLD scales with RPE magnitude. |
| 5 | vs_response | Ventral striatum BOLD response proxy. clamp(f03 - f04 + 0.5, 0, 1). Signed RPE signal centered at 0.5: values > 0.5 indicate positive RPE (VS activation), values < 0.5 indicate negative RPE (VS deactivation). Directly models the crossover interaction pattern observed in Gold (2023, d = 1.07): Surprise x Liked = VS up, Surprise x Disliked = VS down. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 8 | M8 (velocity) | L0 (fwd) | Spectral velocity at 500ms — surprise dynamics |
| 1 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms — event boundary detection |
| 2 | 10 | 4 | M0 (value) | L2 (bidi) | Onset at 125ms — event boundary (theta band) |
| 3 | 10 | 8 | M2 (std) | L2 (bidi) | Onset variability at 500ms — event regularity |
| 4 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — salience weighting |

---

## Computation

The M-layer computes two derived mathematical quantities from the E-layer RPE signals:

1. **RPE Magnitude**: The maximum of positive and negative RPE captures the unsigned prediction error strength. This is analogous to the absolute value of the TD error in reinforcement learning. Large magnitudes drive model updating and attention regardless of whether the surprise was pleasant or unpleasant.

```
rpe_magnitude = max(f03_positive_rpe, f04_negative_rpe)
```

2. **VS Response**: The signed RPE signal that directly models the ventral striatum BOLD response. The subtraction f03 - f04 produces the signed error, and the +0.5 offset centers the output at neutral (no RPE). This implements the crossover interaction pattern from Gold (2023): when surprise co-occurs with liking, VS activates (> 0.5); when surprise co-occurs with disliking, VS deactivates (< 0.5).

```
vs_response = clamp(f03_positive_rpe - f04_negative_rpe + 0.5, 0.0, 1.0)
```

The M-layer H³ demands provide the event detection and salience context that feeds into the E-layer computations.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_positive_rpe | Positive RPE for magnitude and VS response |
| E-layer | f04_negative_rpe | Negative RPE for magnitude and VS response |
| H³ | 5 tuples (see above) | Event detection and salience context |
