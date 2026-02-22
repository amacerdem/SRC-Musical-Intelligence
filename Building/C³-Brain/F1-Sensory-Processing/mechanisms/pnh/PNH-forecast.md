# PNH F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [8:11]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:dissonance_res_fc | [0, 1] | Dissonance resolution prediction (0.5-2s). sigma(0.40*(1-roughness_trend) + 0.30*helmholtz_mean + 0.30*P1). Decreasing roughness trend + high consonance = expected resolution. |
| 9 | F1:pref_judgment_fc | [0, 1] | Preference judgment prediction (1-3s). sigma(0.40*pleasant_stab + 0.30*P2 + 0.30*stumpf_mean). Consonance stability predicts upcoming aesthetic pleasure. Sarasso 2019. |
| 10 | F2:expertise_mod_fc | [0, 1] | Expertise modulation forecast. sigma(0.50*H2 + 0.50*M0). Training-dependent sensitivity prediction. |

---

## Design Rationale

Three forward predictions for ratio hierarchy processing:

1. **Dissonance Resolution (F0)**: Based on roughness trajectory over phrase (inverted trend: decreasing roughness = approaching consonance), harmonic template context (Helmholtz mean over phrase), and current conflict monitoring (P1). Predicts whether the current dissonant context will resolve within 0.5-2s.

2. **Preference Judgment (F1)**: Consonance stability over phrase (pleasantness stability H18) combined with current consonance preference (P2) and tonal fusion trend (Stumpf mean H14). Predicts the aesthetic appreciation response before it occurs.

3. **Expertise Modulation Forecast (F2)**: Training-dependent encoding (H2) plus ratio complexity (M0) predict expertise-dependent processing differences. Musicians should show higher F2 modulation than non-musicians (Crespo-Bojorque 2018: 5 vs 1 ROI).

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 14, 1, 0) | roughness mean H14 L0 | Avg dissonance over progression |
| (0, 18, 18, 0) | roughness trend H18 L0 | Dissonance trajectory over phrase |
| (4, 18, 19, 0) | pleasantness stability H18 L0 | Consonance stability over phrase |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Avg complexity over progression |
| (3, 14, 1, 2) | stumpf mean H14 L2 | Fusion stability over progression |
| (14, 14, 3, 0) | tonalness std H14 L0 | Purity variation over progression |
| (2, 18, 1, 0) | helmholtz mean H18 L0 | Harmonic template over phrase |

---

## Belief Consumption

PNH has 0 beliefs at this time. May gain beliefs as integration matures.

---

## Scientific Foundation

- **Tabas 2019**: POR latency consonant < dissonant (up to 36ms) — predicts resolution timing
- **Sarasso 2019**: Consonance stability -> aesthetic appreciation (eta2p=0.685)
- **Crespo-Bojorque 2018**: Musicians show consonance pattern in 5 ROIs; non-musicians in 1

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/pnh/forecast.py`
