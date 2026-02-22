# PUPF P-Layer — Cognitive Present (3D)

**Layer**: Cognitive Present (P)
**Indices**: [7:10]
**Scope**: exported (kernel relay)
**Activation**: tanh (idx 7-8), sigmoid (idx 9)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:surprise_pleasure | [-1, 1] | Surprise-pleasure coupling signal. tanh(S * unit_projection[20:24].mean()). Captures how current surprise maps to hedonic response via the reward pathway. Cheung 2019: striatal surprise processing (d=3.8-8.53). |
| 8 | P1:affective_outcome | [-1, 1] | Net valence from prediction outcome. tanh(P * expectancy_affect[14:18].mean()). Positive when prediction confirmed in high-H context; negative when overwhelmed. Huron 2006 ITPRA: prediction outcome drives emotion. |
| 9 | P2:tempo_pred_error | [0, 1] | Temporal prediction error at rhythm level. sigma(\|velocity_A[8] - arousal_dynamics[6]\| * 2.0). Deviation from expected beat timing. Singer 2023: pulse clarity correlates with valence (r=0.50). |

---

## Design Rationale

1. **Surprise-Pleasure Coupling (P0)**: Captures the real-time hedonic response to surprise events. Unlike the abstract Goldilocks computation in G0, this represents the felt experience of surprise — the "aha" moment or the "what?!" reaction. Uses the S signal modulated by the current unit projection state. The tanh activation allows both positive surprise (deceptive cadence delight) and negative surprise (jarring modulation). Cheung 2019 showed striatal encoding of this signal.

2. **Affective Outcome (P1)**: Represents the net emotional consequence of the prediction-observation cycle. When the listener is uncertain (high H) and the outcome is expected (low S), relief and resolution produce positive affect. When the listener is certain (low H) but surprised (high S), the violation can be thrilling or disturbing depending on context. This dimension captures the ITPRA "reaction" phase (Huron 2006).

3. **Tempo Prediction Error (P2)**: Temporal prediction operates at the rhythm level, separate from pitch/harmony prediction. Measures the deviation between expected beat timing (from arousal dynamics) and actual onset velocity. Singer 2023 showed pulse clarity is the strongest musical predictor of valence (r=0.50), confirming that temporal predictability has a direct hedonic pathway independent of harmonic content.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (8, 12, 8, 0) | velocity_A velocity H12 L0 | Tempo dynamics at half-beat for tempo_pred_error |
| (8, 16, 18, 0) | velocity_A trend H16 L0 | Tempo trend over 1s for prediction baseline |
| (11, 7, 8, 0) | onset_strength velocity H7 L0 | Beat onset rate for temporal surprise |
| (4, 12, 18, 0) | sensory_pleasantness trend H12 L0 | Hedonic trajectory for affective_outcome |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [8] | velocity_A | P2: rate of change for tempo prediction error |
| [10] | loudness | P0: arousal level modulating surprise response |
| [11] | onset_strength | P2: event onset timing for temporal prediction |
| [0] | roughness | P1: inverse pleasantness for affective outcome |
| [4] | sensory_pleasantness | P1: hedonic signal for affective outcome |

---

## Scientific Foundation

- **Cheung et al. 2019**: Striatal response to musical surprise (fMRI 3T, N=39, d=3.8-8.53)
- **Huron 2006**: ITPRA framework — prediction outcome drives temporal emotional response sequence (theoretical)
- **Singer et al. 2023**: Pulse clarity correlates with valence (behavioral, N=40, r=0.50); inverted-U for optimal tempo 80-160 BPM (N=34, d=0.69)
- **Egermann et al. 2013**: High information content increases arousal, decreases valence (live concert, N=50, d=6.0)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/pupf/cognitive_present.py`
