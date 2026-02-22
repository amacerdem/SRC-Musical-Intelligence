# STC — Cognitive Present

**Model**: Singing Training Connectivity
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | insula_activity | Temporal-context interoceptive monitoring level. Represents the current level of insula engagement in interoceptive monitoring at the cognitive present, synthesizing E-layer interoceptive coupling with M-layer connectivity dynamics. Higher values indicate stronger interoceptive awareness, consistent with the right anterior insula's role as an interoceptive hub (Kleber 2013: right AIC MNI 48, 0, -3; F = 22.08 expertise x anesthesia interaction). |
| 7 | vocal_motor | Beat-entrainment vocal motor output level. Captures the current state of vocal motor output in the context of rhythmic entrainment, integrating speech sensorimotor activation with voice-body coupling. Higher values indicate more active vocal motor engagement. Zarate 2010: involuntary pitch correction supports automatic interoceptive-motor loop. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | P-layer uses no additional H3 tuples beyond E and M layers |

---

## Computation

The P-layer computes the cognitive present state of interoceptive-motor integration by integrating E-layer and M-layer outputs into two summary dimensions that capture the "now" of singing-related sensorimotor processing.

1. **insula_activity**: Synthesizes interoceptive coupling (f28) with connectivity strength from the M-layer. This represents the instantaneous engagement of the anterior insula in monitoring vocal and respiratory states. In music listening, this tracks how actively the interoceptive system is monitoring the body's response to musical input. Kleber 2013's causal anesthesia evidence shows that disrupting somatosensory feedback differentially modulates right AIC activity in singers vs nonsingers, confirming the insula as the central hub.

2. **vocal_motor**: Integrates speech sensorimotor activation (f30) with voice-body coupling from the M-layer. This captures the current level of vocal motor engagement during music processing. Even in passive listening, the vocal motor system shows subthreshold activation in response to singing (Zarate 2010), and this dimension tracks that implicit motor response.

The P-layer consumes no additional H3 tuples, relying entirely on the E-layer and M-layer computations to construct the cognitive present representation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f28 | Interoceptive coupling | Core interoceptive signal for insula_activity |
| E-layer f30 | Speech sensorimotor | Core motor signal for vocal_motor |
| M-layer connectivity_strength | Temporal connectivity dynamics | Temporal context for insula_activity |
| M-layer voice_body_coupling | Voice-body integration | Integration context for vocal_motor |
