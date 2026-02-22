# ESME — Forecast

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | feature_enhancement_pred | Predicted MMN enhancement level for upcoming features. Estimates the degree to which the next auditory event will receive expertise-enhanced processing, based on the current unified MMN-expertise function and present deviance levels. Mischler et al. 2025: deeper transformer layers more predictive of neural responses in musicians, suggesting hierarchical prediction enhancement. |
| 9 | expertise_transfer_pred | Cross-domain transfer prediction. Estimates how much expertise in one domain transfers to detection in another. expertise_transfer_pred = σ(0.3 * f01 + 0.3 * f02 + 0.4 * f03). Criscuolo et al. 2022: all musicians show some general enhancement over non-musicians (bilateral STG + L IFG), suggesting partial cross-domain transfer. Martins et al. 2022 constraint: no clean dissociation at salience level — some transfer exists. |
| 10 | developmental_trajectory | Long-term plasticity trajectory. Estimates the expertise accumulation trend based on enhancement magnitude and unified expertise function. developmental_trajectory = σ(0.6 * f04 + 0.4 * mmn_expertise_function). Bucher et al. 2023: Heschl's Gyrus 130% larger in professional musicians; OFC co-activation 25-40ms faster. Bonetti et al. 2024: hierarchical auditory memory AC to hippocampus to cingulate develops with expertise. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

No additional H³ demands beyond those consumed by the E-layer and P-layer. The F-layer operates on derived features from earlier layers.

---

## Computation

The F-layer generates three forward predictions about expertise-dependent processing, ranging from immediate enhancement expectations to long-term developmental trajectories.

1. **feature_enhancement_pred**: Predicts the expected enhancement level for the next incoming feature based on the current expertise state (M-layer mmn_expertise_function) and the present deviance pattern (P-layer). When deviance is detected in the trained domain, enhancement prediction increases; in untrained domains, prediction reflects the baseline general enhancement.

2. **expertise_transfer_pred**: Predicts cross-domain transfer by weighting all three domain-specific MMNs (pitch 0.3, rhythm 0.3, timbre 0.4 — slightly higher weight on timbre reflecting spectral richness of transfer). The ALE meta-analysis (Criscuolo et al. 2022) confirms that musicians show general enhancement across domains, but the Martins et al. 2022 constraint warns against expecting clean dissociation.

3. **developmental_trajectory**: Predicts the long-term plasticity trajectory by combining expertise enhancement (f04, weight 0.6) with the unified expertise function (weight 0.4). This captures the structural and functional changes that accumulate with years of training: enlarged Heschl's Gyrus (Bucher et al. 2023), faster OFC co-activation, and strengthened hierarchical memory pathways (Bonetti et al. 2024).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Pitch MMN | Transfer prediction input |
| E-layer f02 | Rhythm MMN | Transfer prediction input |
| E-layer f03 | Timbre MMN | Transfer prediction input (highest weight) |
| E-layer f04 | Expertise enhancement | Enhancement and trajectory predictions |
| M-layer mmn_expertise_function | Unified expertise metric | Enhancement prediction and trajectory base |
| P-layer deviance signals | Current detection state | Context for enhancement prediction |
