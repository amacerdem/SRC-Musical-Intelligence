# ONI — Cognitive Present

**Model**: Over-Normalization in Intervention
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | enhanced_mmr | Current mismatch response strength. Represents the current-frame magnitude of deviance detection, combining spectral flux deviance with onset strength at multiple timescales. sigma(0.35 * deviance_std_100ms + 0.35 * onset_100ms). When this exceeds fullterm_reference (M-layer), the system is in an over-normalized state. Partanen 2022: singing group showed enhanced oddball MMR (eta^2=0.229). Range [0, 1]. |
| 8 | attentional_state | Heightened attention level. Captures the current attentional engagement of the developing auditory system, reflecting the enhanced orienting response that may underlie the over-normalization phenomenon. sigma(0.35 * tonal_entropy_100ms + 0.35 * spectral_velocity_125ms). Scholkmann 2024: prefrontal cortex shows increased oxygenation during music therapy (StO2 +2.4%, p=0.008). Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 22 | 3 | M0 (value) | L2 (bidi) | Energy change at 100ms alpha for intensity tracking |
| 1 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch change at 100ms alpha for deviance detection |
| 2 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch change over 1s beat for context |

---

## Computation

The P-layer computes two dimensions representing the current-frame state of the over-normalization process:

1. **Enhanced MMR** (idx 7): Estimates the current mismatch response magnitude by combining deviance variability (spectral flux std at 100ms) with onset strength at the alpha timescale. This dimension directly represents the phenomenon that ONI models -- when enhanced_mmr consistently exceeds the M-layer fullterm_reference, the system is exhibiting over-normalization. The E-layer provides the deviance detection signals; the P-layer integrates them into a single current-state estimate.

2. **Attentional state** (idx 8): Captures the heightened attentional orienting that represents one of the leading explanations for over-normalization. Uses tonal entropy (information-theoretic measure of tonal complexity) and spectral velocity (rate of spectral change) at short timescales. The hypothesis is that singing intervention trains the preterm auditory system to be hyper-attentive to acoustic changes, producing larger MMR not through deeper processing but through enhanced attentional capture. Kaminska 2025 shows that auditory cortex in preterm infants exhibits stimulus-specific processing networks, supporting the idea that attention can be selectively enhanced.

The P-layer serves as the bridge between the E-layer's feature extraction and the F-layer's outcome predictions. By separating the MMR magnitude (what is happening) from the attentional state (why it may be happening), the model can represent both the phenomenon and its potential mechanism simultaneously.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [22] | energy_change | Energy dynamics for intensity tracking |
| R3 [23] | pitch_change | Pitch dynamics for deviance detection |
| H3 | 3 tuples (see above) | Energy change, pitch change, and mean pitch context |
| E-layer | f01, f03 | Over-normalization index and attention enhancement feed into present state |
| M-layer | fullterm_reference | Comparison target for determining over-normalized state |
