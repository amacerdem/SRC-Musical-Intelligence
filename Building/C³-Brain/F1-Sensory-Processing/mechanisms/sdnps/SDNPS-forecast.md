# SDNPS F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:behavioral_consonance_pred | [0, 1] | Consonance prediction gated by stimulus dependency. sigma(0.60*M0 + 0.40*P1). Valid when M0 is high (simple timbre); degrades for complex timbres. |
| 8 | F1:roughness_response_pred | [0, 1] | Roughness response prediction (stimulus-invariant). sigma(0.57*P2 + 0.43*P0). Always valid: NPS ↔ roughness r=-0.57 holds universally. |
| 9 | F2:generalization_limit | [0, 1] | NPS generalization to novel timbres. sigma(0.50*E1 + 0.50*tonalness_mean). Predicts how far NPS can transfer from training timbre. |

---

## Design Rationale

Three forward predictions for stimulus-dependent pitch salience:

1. **Behavioral Consonance (F0)**: M0 (NPS×dependency) weighted 0.60 plus harmonicity proxy (P1) at 0.40. This prediction is only valid when M0 is high, i.e., for spectrally simple stimuli. For natural sounds, F0 regresses toward sigmoid(0) ≈ 0.50.

2. **Roughness Response (F1)**: Combines roughness interference (P2, 0.57 — matching the empirical r=-0.57) and FFR encoding (P0, 0.43). Unlike F0, this prediction is stimulus-invariant: roughness always predicts the neural response regardless of timbre.

3. **Generalization Limit (F2)**: Stimulus dependency (E1) plus tonalness trend (H3 L0) predict how far NPS can generalize. High tonalness across context suggests the signal is clean enough for NPS transfer.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 3, 1, 0) | tonalness mean H3 L0 | Pitch clarity trend for generalization |

---

## Belief Consumption

SDNPS has 0 beliefs at this time. May gain beliefs as integration matures.

---

## Scientific Foundation

- **Cousineau 2015**: NPS predicts consonance for synthetic (r=0.34) but not natural sounds; NPS ↔ roughness r=-0.57 is universal
- **Penagos 2004**: Pitch salience in alHG, not subcortical IC
- **Tabas 2019**: POR latency shorter for consonant than dissonant in alHG

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sdnps/forecast.py`
