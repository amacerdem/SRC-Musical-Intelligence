# DDSMI — Extraction

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU-β2
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f13_social_coordination | Partner tracking and social coordination strength. f13 = σ(0.40 * social_period_1s + 0.30 * social_period_500ms + 0.30 * social_coupling_100ms). Captures interpersonal neural coordination during dyadic dance, where social coupling periodicity at multiple timescales reflects the quality of partner synchronization. Bigand et al. 2025: social coordination mTRF with visual contact F(1,57)=249.75, p<.001. Range [0, 1]. |
| 1 | f14_music_tracking | Auditory entrainment strength during social movement. f14 = σ(0.40 * music_period_1s + 0.30 * music_period_500ms + 0.30 * music_onset_100ms). Captures neural tracking of the musical stimulus during dyadic dance. Competes with social coordination for processing resources. Bigand et al. 2025: music tracking mTRF with music presence F(1,57)=30.22, p<.001. Range [0, 1]. |
| 2 | f15_visual_modulation | Resource shift from music to social processing with visual contact. f15 = σ(0.35 * loudness_entropy_100ms + 0.35 * social_variability_100ms + 0.30 * (f13 - f14)). Models the resource competition between auditory and social processing — visual contact shifts resources from music tracking to social coordination. Bigand et al. 2025: visual contact reduces music tracking F(1,57)=7.48, p=.033 while increasing social coordination. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Music onset 100ms — fast auditory tracking |
| 1 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Music periodicity 1s — sustained auditory entrainment |
| 2 | 25 | 3 | M0 (value) | L2 (bidi) | Music coupling 100ms — fast motor-auditory link |
| 3 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Music coupling period 100ms — fast coupling regularity |
| 4 | 25 | 8 | M14 (periodicity) | L2 (bidi) | Music coupling period 500ms — mid-scale regularity |
| 5 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Music coupling period 1s — sustained coupling regularity |
| 6 | 33 | 3 | M0 (value) | L2 (bidi) | Social coupling 100ms — fast partner tracking |
| 7 | 33 | 3 | M2 (std) | L2 (bidi) | Social variability 100ms — partner tracking stability |
| 8 | 33 | 8 | M14 (periodicity) | L2 (bidi) | Social period 500ms — mid-scale social coordination |
| 9 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Social period 1s — sustained social coordination |
| 10 | 8 | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms — auditory complexity |

---

## Computation

The E-layer extracts three explicit features capturing the four parallel neural tracking processes of dyadic dance, compressed into the three most computationally distinct signals.

**f13 (social_coordination)** is the social tracking signal. It combines social coupling periodicity at three timescales: 1s (sustained partner coordination), 500ms (mid-range synchronization), and 100ms (fast partner tracking). The multi-scale combination reflects that social coordination in dance operates across temporal hierarchies — from micro-adjustments to sustained coupling.

**f14 (music_tracking)** is the auditory tracking signal. It combines music coupling periodicity at 1s and 500ms with music onset value at 100ms. This captures how strongly the neural system tracks the musical stimulus during social interaction. Self-movement tracking is not modeled separately because Bigand 2025 found it is autonomous (all ps>.224 for visual/music modulation).

**f15 (visual_modulation)** captures the resource competition. The difference term (f13 - f14) is the key innovation: when social coordination exceeds music tracking, the system has shifted resources to social processing (positive f15). Loudness entropy adds auditory complexity (more complex = harder to track), and social variability adds partner unpredictability (more variable = more demanding social tracking).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[10] spectral_flux | Music onset detection | Auditory entrainment anchor |
| R³[8] loudness | Perceptual intensity | Loudness entropy for resource demand |
| R³[25] x_l0l5[0] | Music-motor coupling | Auditory tracking pathway |
| R³[33] x_l4l5[0] | Social coupling | Partner coordination pathway |
| H³ (11 tuples) | Multi-scale temporal dynamics | Fast (100ms) to sustained (1s) social and music tracking |
