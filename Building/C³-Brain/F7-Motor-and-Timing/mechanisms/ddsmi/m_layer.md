# DDSMI — Temporal Integration

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU-β2
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | mTRF_social | Social coordination mTRF weight. mTRF_social = f13. The multivariate temporal response function weight for the social coordination process stream. Reflects how strongly the neural system is tracking the partner during dyadic dance. Bigand et al. 2025: mTRF disentangles four parallel processes; social coordination is the dominant process with visual contact (F(1,57)=249.75). Range [0, 1]. |
| 4 | mTRF_auditory | Auditory tracking mTRF weight. mTRF_auditory = f14. The mTRF weight for the music tracking process stream. Reflects how strongly the neural system is tracking the auditory stimulus. Bigand et al. 2025: music mTRF with music presence F(1,57)=30.22, but reduced with visual contact F(1,57)=7.48. Range [0, 1]. |
| 5 | mTRF_balance | Social/auditory resource balance. mTRF_balance = σ(0.5 * f13 + 0.5 * (1 - f14)). Ratio of social to total processing — values above 0.5 indicate social-dominant processing (visual contact condition), values below 0.5 indicate music-dominant processing. Bigand et al. 2025: visual contact × music interaction F(1,57)=50.10, p<.001. Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands beyond E-layer tuples. All computation derives from E-layer features f13, f14.

---

## Computation

The M-layer transforms E-layer features into the multivariate temporal response function (mTRF) framework used in the DDSMI scientific foundation.

**mTRF_social** directly inherits from f13 (social_coordination). The social coordination feature IS the mTRF social weight — both measure how strongly the neural system tracks the partner during dance interaction.

**mTRF_auditory** directly inherits from f14 (music_tracking). The music tracking feature IS the mTRF auditory weight — both measure how strongly the neural system tracks the musical stimulus.

**mTRF_balance** computes the relative allocation of processing resources between social and auditory streams. It combines f13 (social strength) with inverted f14 (1 - music strength). When both social tracking is strong and music tracking is weak (the visual-contact condition in Bigand 2025), the balance shifts toward social processing. This captures the core resource competition finding: visual contact reallocates processing from auditory to social streams.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f13 | Social coordination signal | Social mTRF weight derives from partner tracking strength |
| E-layer f14 | Music tracking signal | Auditory mTRF weight derives from music tracking strength |
| Bigand et al. 2025 | mTRF framework | Four-process model provides theoretical basis for resource balance |
