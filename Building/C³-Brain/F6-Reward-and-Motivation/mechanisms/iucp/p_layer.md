# IUCP — Cognitive Present

**Model**: Inverted-U Complexity Preference
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | current_preference_state | Real-time liking level. σ(0.5 * f01 + 0.5 * f02). Integrates IC liking and entropy liking curves into a unified preference signal. Equal weighting reflects comparable effect sizes: IC R² = 26.3% vs entropy R² = 19.1% (Gold 2019 Study 1), converging in Study 2 (41.6% vs 34.9%). High values = music is in the listener's optimal complexity zone. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 16 | M1 (mean) | L2 (bidi) | Mean IC over 1s — via f01 |
| 1 | 24 | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy 1s — via f02 |
| 2 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s — via f01 |

---

## Computation

The P-layer collapses the 4D extraction space into a single real-time preference signal. It combines the two independent inverted-U curves (IC liking and entropy liking) with equal weighting.

The balanced 0.5/0.5 combination reflects Gold 2019's finding that both IC and entropy independently predict liking with comparable effect sizes. High output indicates the music is in the listener's "sweet spot" of optimal complexity; low output indicates either boredom (too simple) or aversion (too complex).

This signal feeds downstream to DAED (preference drives DA anticipation), RPEM (preference modulates RPE), and the kernel reward computation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f01_ic_liking_curve | IC preference component |
| E-layer [1] | f02_entropy_liking_curve | Entropy preference component |
| R³ [21] | spectral_change | IC basis (via f01) |
| R³ [24] | concentration_change | Entropy basis (via f02) |
| R³ [4] | sensory_pleasantness | Hedonic modulation (via f01) |
| Gold 2019 | Liking jointly predicted by IC + entropy | Both dimensions independently contribute |
| Gold 2023b | VS reward signal tracks average liking | F(1,22) = 4.83, p = 0.039 |
