# IOTMS — Extraction

**Model**: Individual Opioid Tone Music Sensitivity
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_mor_baseline_proxy | MOR availability proxy (trait). Sigmoid-compressed estimate of baseline mu-opioid receptor availability derived from sustained hedonic quality and consonance. Higher values indicate greater trait-level opioid tone. f01 = sigma(0.35 * mean_pleasantness_1s + 0.30 * (1 - roughness_skew_1s)). Putkinen 2025: baseline MOR predicted pleasure-BOLD in insula, ACC, SMA, STG, NAcc, thalamus. |
| 1 | f02_pleasure_bold_slope | Pleasure-BOLD coupling slope. Measures the steepness of the relationship between subjective pleasure and neural BOLD response, modulated by MOR baseline and loudness. f02 = sigma(0.40 * f01 + 0.30 * mean_loudness_1s). Putkinen 2025: MOR BPND correlated with pleasure-BOLD slope (d = 1.16). |
| 2 | f03_reward_propensity | Music reward propensity index. Trait-level propensity for experiencing music-induced reward, combining pleasure-BOLD coupling with sustained opioid-perceptual interaction. f03 = sigma(0.35 * f02 + 0.35 * sustained_coupling_1s). Mas-Herrero 2014: BMRQ predicted music pleasure (R^2 = 0.30). |
| 3 | f04_music_reward_index | Overall music reward sensitivity. Integrates reward propensity with temporal coupling trend and harmonic richness to yield a composite individual sensitivity score. f04 = sigma(0.40 * f03 + 0.30 * coupling_trend_1s + 0.30 * mean_tristimulus_1s). Martinez-Molina 2016: BMRQ predicted pleasure ratings (R^2 = 0.40). |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 8 | M1 (mean) | L2 (bidi) | Mean sensory pleasantness at 500ms |
| 1 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean sensory pleasantness at 1s |
| 2 | 4 | 16 | M2 (std) | L2 (bidi) | Pleasantness variability at 1s |
| 3 | 0 | 8 | M1 (mean) | L2 (bidi) | Mean roughness at 500ms |
| 4 | 0 | 16 | M6 (skew) | L2 (bidi) | Roughness skewness at 1s |
| 5 | 8 | 8 | M1 (mean) | L2 (bidi) | Mean loudness at 500ms |
| 6 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness at 1s |
| 7 | 33 | 8 | M1 (mean) | L2 (bidi) | Sustained coupling (x_l4l5[0]) at 500ms |
| 8 | 33 | 16 | M1 (mean) | L2 (bidi) | Sustained coupling (x_l4l5[0]) at 1s |
| 9 | 33 | 16 | M18 (trend) | L2 (bidi) | Coupling trend at 1s |
| 10 | 14 | 16 | M1 (mean) | L2 (bidi) | Mean tristimulus1 at 1s |
| 11 | 14 | 16 | M2 (std) | L2 (bidi) | Tristimulus1 variability at 1s |

---

## Computation

The E-layer extracts four explicit features representing individual opioid-reward sensitivity from sustained acoustic properties. IOTMS is the smallest model in the entire C3 system (5D total output, 12 H3 tuples).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule). The computation is sequential -- f01 feeds f02, f02 feeds f03, f03 feeds f04 -- forming a cascaded trait estimation:

1. **f01** (MOR baseline proxy): Estimates trait-level mu-opioid receptor availability from sustained hedonic quality (mean pleasantness at 1s) and consonance quality (inverse roughness skewness at 1s). This is the anchor feature for the entire model.

2. **f02** (pleasure-BOLD slope): Derives the pleasure-to-neural-response coupling strength from f01 and mean loudness at 1s. Captures the Putkinen 2025 finding that higher MOR baseline produces steeper pleasure-BOLD slopes.

3. **f03** (reward propensity): Combines the pleasure-BOLD slope with sustained opioid-perceptual coupling (x_l4l5 interaction at 1s). This captures the trait-level tendency to experience music reward.

4. **f04** (music reward index): Final composite integrating reward propensity with the temporal trend of coupling and harmonic richness (tristimulus). This is the broadest individual sensitivity measure.

H3 tuples are concentrated at H8 (500ms) and H16 (1s) horizons with L2 (bidirectional) law, reflecting the trait-level nature of opioid tone -- short timescales are irrelevant for stable individual differences.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3[0] roughness | Consonance quality (inverse) | Feeds roughness skewness for MOR baseline estimation |
| R3[4] sensory_pleasantness | Hedonic quality | Primary pleasure signal for MOR baseline proxy |
| R3[8] loudness | Perceptual intensity | Modulates pleasure-BOLD slope computation |
| R3[14:17] tristimulus | Harmonic structure | Musical quality signal for composite reward index |
| R3[33:41] x_l4l5 | Sustained opioid-perceptual coupling | Prolonged interaction features for reward propensity |
| H3 (12 tuples) | Temporal morphology at H8/H16 | Sustained dynamics for trait-level estimation |
