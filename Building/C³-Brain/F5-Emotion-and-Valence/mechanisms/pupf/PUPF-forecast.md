# PUPF F-Layer — Forecast (2D)

**Layer**: Forecast (F)
**Indices**: [10:12]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 10 | F0:next_event_prob | [0, 1] | Confidence in next event prediction. next_event_prob = 1 - H (high certainty = high probability). 0.5-1s ahead lookahead. Pearce 2005: IDyOM provides probabilistic event predictions. Feeds anticipation ramp in SRP. |
| 11 | F1:pleasure_forecast | [0, 1] | Predicted pleasure response 1-2s ahead. sigma(P + 0.5 * goldilocks_zone). Based on current P(H,S) trajectory and Goldilocks zone position. Gold 2023: VS reflects anticipated musical pleasure. |

---

## Design Rationale

1. **Next Event Probability (F0)**: The inverse of uncertainty — how confident the listener is about what comes next. When H is low (predictable context), next_event_prob approaches 1.0, meaning the brain has a strong prediction. When H is high, the probability drops, reflecting genuine uncertainty. This signal feeds SRP's anticipation ramp: strong predictions generate stronger wanting (because the prediction can be confirmed or violated). Pearce 2005 IDyOM provides the computational basis for probabilistic melodic prediction.

2. **Pleasure Forecast (F1)**: Predicts the hedonic outcome 1-2 seconds ahead based on the current trajectory through H x S space. If the listener is currently in or approaching the Goldilocks zone, pleasure_forecast is high. Uses the current pleasure value P plus a zone bonus (0.5 * goldilocks_zone) to project forward. Gold 2023 fMRI showed that the ventral striatum reflects anticipated pleasure from musical expectations, validating a forward-looking pleasure signal.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 12, 18, 0) | distribution_entropy trend H12 L0 | Entropy trajectory for event probability prediction |
| (21, 12, 18, 0) | spectral_flux trend H12 L0 | Surprise trajectory for pleasure forecast |
| (22, 15, 18, 0) | distribution_entropy trend H15 L0 | Longer entropy trend for 1-2s forecast |
| (4, 15, 18, 0) | sensory_pleasantness trend H15 L0 | Hedonic trajectory for pleasure forecast |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [22] | distribution_entropy | F0: entropy basis for event probability (1 - H) |
| [21] | spectral_flux | F1: surprise trajectory input |
| [4] | sensory_pleasantness | F1: hedonic trajectory for pleasure forecast |
| [14] | tonalness | F0: tonal predictability context |

---

## Scientific Foundation

- **Pearce 2005**: IDyOM entropy provides probabilistic event predictions (computational model, melodic sequences)
- **Gold et al. 2023**: VS reflects musical surprise pleasure; STG-VS coupling increases with pleasure (fMRI, N=24, significant)
- **Harding et al. 2025**: Psilocybin vs escitalopram: dissociable musical surprise processing — prediction-pleasure pathway modulated by serotonergic system (fMRI + RCT, N=41 MDD, significant)
- **Huron 2006**: ITPRA framework — imagination and tension responses precede the event (theoretical)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/pupf/forecast.py`
