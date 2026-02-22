# DSP — Cognitive Present

**Model**: Developmental Singing Plasticity
**Unit**: NDU
**Function**: F10 Clinical & Therapeutic
**Tier**: beta
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | auditory_orienting | Current infant attention state. Real-time orienting response combining amplitude onset detection at 25ms gamma with mean intensity at 100ms alpha, reflecting whether the infant is currently attending to the singing stimulus. Edalati 2023: premature neonates (32+/-2.59 wGA) show selective beat and meter enhancement, demonstrating active auditory orienting at prematurity. Scholkmann 2024: PFC StO2 increase during CMT reflects attention network engagement. |
| 8 | vocal_learning | Current vocal encoding state. Captures active voice-specific learning from brightness at 100ms (pitch tracking) and brightness velocity at 125ms theta (pitch contour dynamics). High values indicate the infant is actively encoding pitch features of the parental voice. Kaminska 2025: age-dependent gamma oscillation increase and voice lateralization shift leftward with maturation, reflecting progressive vocal learning. Yu 2015: MMN plasticity tracks auditory learning of regularities. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 12 | 7 | 3 | M1 (mean) | L2 (bidi) | Mean vocal intensity at 100ms alpha |
| 13 | 10 | 0 | M0 (value) | L2 (bidi) | Onset detection at 25ms gamma |
| 14 | 13 | 3 | M0 (value) | L2 (bidi) | Pitch brightness at 100ms alpha |
| 15 | 13 | 4 | M8 (velocity) | L0 (fwd) | Pitch velocity at 125ms theta |

---

## Computation

The P-layer computes the real-time cognitive state of the infant during singing exposure:

1. **Auditory orienting** (idx 7): Combines onset detection at 25ms gamma (spectral flux instantaneous value) with mean vocal intensity at 100ms alpha (amplitude mean). Onset detection captures sudden acoustic changes that trigger the orienting reflex in preterm neonates — phrase beginnings, consonant onsets, and dynamic shifts in singing. The 100ms mean intensity provides a smoothed measure of whether the singing is within the infant's auditory engagement range. Together, these reflect the moment-to-moment attentional engagement that Edalati 2023 showed is present even in 32-week premature neonates responding to auditory rhythms with selective beat and meter enhancement.

2. **Vocal learning** (idx 8): Driven by brightness at 100ms (pitch tracking) and brightness velocity at 125ms theta (pitch contour dynamics). Brightness at 100ms captures the spectral centroid of the singing voice — a key voice identity feature for pitch discrimination. The velocity morph (M8, edge difference) at 125ms theta tracks how rapidly pitch features are changing, reflecting the dynamic melodic contours that drive vocal learning. The L0 (forward) law on velocity is appropriate because vocal learning is incremental and causal. Kaminska 2025 found that gamma oscillations and voice lateralization develop progressively with age, and Yu 2015 established MMN as an indicator of auditory regularity learning — both supporting active encoding of vocal patterns during the preterm period.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_attention_engagement | Attention level gates orienting response strength |
| M-layer | cumulative_plasticity | Accumulated plasticity modulates learning rate |
| M-layer | voice_recognition | Voice familiarity context for vocal learning |
| R3 [7] | amplitude | Vocal intensity for orienting response |
| R3 [10] | spectral_flux | Onset detection for orienting reflex trigger |
| R3 [13] | brightness | Pitch tracking for vocal learning |
| H3 | 4 tuples (see above) | Intensity mean, onset value, pitch brightness, pitch velocity |
