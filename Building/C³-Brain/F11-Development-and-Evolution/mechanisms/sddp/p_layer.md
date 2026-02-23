# SDDP — Cognitive Present

**Model**: Sex-Dependent Developmental Plasticity
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | attention_modulation | Sex x attention interaction. Captures the current-frame attentional engagement modulated by sex-dependent plasticity. Combines onset detection at 100ms with instantaneous intensity, gated by the hormonal state proxy from M-layer. sigma(0.35 * onset_100ms + 0.35 * intensity_25ms) * hormonal_gate. Scholkmann 2024: prefrontal StO2 increase +2.4% (p=0.008) during CMT reflects attention engagement. Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Onset detection at 100ms alpha for syllable boundaries |
| 1 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch change at 100ms for melodic tracking |
| 2 | 21 | 3 | M2 (std) | L2 (bidi) | Spectral variation at 100ms for processing complexity |

---

## Computation

The P-layer computes a single dimension representing the current-frame attentional state modulated by sex-dependent factors:

1. **Attention modulation** (idx 7): Combines onset detection (spectral flux at 100ms) with pitch change dynamics at the alpha timescale to capture the infant's moment-to-moment attentional engagement with the singing stimulus. The output is gated by the hormonal state proxy from the M-layer, implementing the sex x attention interaction.

The rationale for a single P-dimension is that SDDP is a meta-layer model (F11, evidence-only) focused on documenting the sex-dependent modulation of a developmental process. The cognitive present state is captured as the sex-modulated attentional engagement at each frame, which feeds forward into the F-layer's developmental trajectory predictions.

Scholkmann 2024 provides the neural correlate: prefrontal cortex StO2 increased during creative music therapy sessions, with sex-dependent subgrouping (females predominantly in the positive-response subgroup). The attention_modulation dimension captures this sex-dependent attentional engagement pattern.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [10] | spectral_flux | Onset detection for syllable boundary tracking |
| R3 [21] | spectral_change | Spectral dynamics for processing complexity |
| R3 [23] | pitch_change | Pitch contour for melodic attention tracking |
| H3 | 3 tuples (see above) | Temporal onset, pitch, and spectral dynamics at 100ms |
| M-layer | hormonal_state | Sex-dependent gating of attention |
