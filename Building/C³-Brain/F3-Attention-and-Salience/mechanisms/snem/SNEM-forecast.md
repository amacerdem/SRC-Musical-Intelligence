# SNEM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [9:12]
**Scope**: exported (kernel relay: beat_onset_pred)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:beat_onset_pred | [0, 1] | Next beat onset prediction (~0.5s ahead). sigma(0.5*f01_beat + 0.5*beat_periodicity_1s). Entrainment generates temporal expectations — next beat time extrapolated from current period. |
| 10 | F1:meter_position_pred | [0, 1] | Current position in metric hierarchy (0=weak beat, 1=downbeat). sigma(0.5*f02_meter + 0.5*coupling_periodicity_1s). Meter hierarchy nests beats into bars. |
| 11 | F2:enhancement_pred | [0, 1] | Predicted SS-EP magnitude 0.75s ahead. sigma(0.5*ssep_enhancement + 0.5*f03_selective). Predicts whether upcoming events will receive strong or weak selective enhancement. |

---

## Design Rationale

1. **Beat Onset Prediction (F0)**: The temporal prediction — "when will the next beat arrive?" This is the fundamental output of entrainment: a periodic internal clock synchronized to external rhythm. Feeds the Anticipation belief `beat_onset_pred` and downstream F7 Motor for preparation.

2. **Meter Position Prediction (F1)**: The hierarchical prediction — "where am I in the bar?" Strong beats (downbeats) are predicted to be more salient. This feeds `meter_position_pred` Anticipation belief and helps F4 Memory with episodic boundary detection.

3. **Enhancement Prediction (F2)**: The magnitude prediction — "how strong will enhancement be?" Combines current enhancement state with selective gain to forecast whether the listener will be strongly or weakly attending. Used by the precision engine for pi_pred estimation.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Beat periodicity for next-beat extrapolation |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Coupling periodicity for meter position |

F-layer primarily reuses E+M outputs rather than reading new H³ tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:beat_onset_pred | F6 Reward | PE from temporal prediction |
| F0:beat_onset_pred | F7 Motor | Motor preparation timing |
| F1:meter_position_pred | F4 Memory | Episodic boundary context |
| F2:enhancement_pred | Precision engine | pi_pred estimation |

---

## Scientific Foundation

- **Large & Palmer 2002**: Temporal regularity perception — oscillator-based beat tracking
- **Nozaradan 2011**: Neuronal entrainment tagging validates prediction-based enhancement
- **Saadatmehr et al.**: Even premature neonates (32 wGA) show beat/meter prediction

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/snem/forecast.py`
