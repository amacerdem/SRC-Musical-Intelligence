# TPRD F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:pitch_percept_fc | [0, 1] | Pitch percept prediction (50-200ms). sigma(0.40*P1 + 0.30*stumpf_mean_h6 + 0.30*M1). Current pitch state + fusion + coherence -> future pitch percept. |
| 8 | F1:tonotopic_adpt_fc | [0, 1] | Tonotopic adaptation prediction (200-700ms). sigma(0.40*P0 + 0.30*(1-roughness_mean) + 0.30*(1-harm_dev)). Tonotopic state + decreasing roughness/deviation -> adaptation. |
| 9 | F2:dissociation_fc | [0, 1] | Dissociation evolution forecast (0.5-2s). sigma(0.35*T2 + 0.35*M0 + 0.30*pleasant_stab). Current dissociation + index + consonance stability -> evolution. |

---

## Design Rationale

Three forward predictions for tonotopy-pitch processing:

1. **Pitch Percept (F0)**: Pitch state (P1, 0.40) combined with beat-level fusion (stumpf mean H6) and spectral-pitch coherence (M1). Predicts the upcoming pitch percept quality. When pitch state is high and streams are coherent, the prediction is confident.

2. **Tonotopic Adaptation (F1)**: Tonotopic state (P0, 0.40) combined with inverted roughness trend (decreasing roughness = less spectral load) and inverted harmonic deviation (low mismatch). Predicts tonotopic adaptation over 200-700ms. High values = expected adaptation (neural fatigue of spectral channel).

3. **Dissociation Evolution (F2)**: Current dissociation degree (T2) and dissociation index (M0) project forward, stabilized by pleasantness stability over phrase. Predicts whether the tonotopy-pitch dissociation will increase or decrease over 0.5-2s.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 14, 1, 0) | roughness mean H14 L0 | Avg tonotopic load over progression |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Avg conflict over progression |
| (3, 6, 1, 0) | stumpf mean H6 L0 | Beat-level fusion stability |
| (22, 14, 1, 0) | entropy mean H14 L0 | Avg spectral complexity |
| (4, 18, 19, 0) | pleasantness stability H18 L0 | Consonance stability over phrase |
| (6, 10, 0, 2) | harmonic_dev value H10 L2 | Template mismatch at chord level |
| (7, 6, 8, 0) | amplitude velocity H6 L0 | Energy change rate at beat level |
| (8, 10, 0, 2) | velocity_D value H10 L2 | Loudness at chord level |

---

## Belief Consumption

TPRD has 0 beliefs at this time. May gain beliefs as integration matures.

---

## Scientific Foundation

- **Briley 2013**: Tonotopic vs pitch dissociation is the fundamental organizing principle of HG
- **Foo 2016**: Tonotopic processing relates to roughness; lateral HG to pitch
- **Tabas 2019**: Decoder-sustainer model in alHG; POR latency differences

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/tprd/forecast.py`
