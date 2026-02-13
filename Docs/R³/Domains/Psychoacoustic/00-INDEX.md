# Psychoacoustic Domain -- Groups A + K (21D)

**Domain**: Human perception models
**Groups**: A:Consonance [0:7] 7D, K:ModulationPerception [114:128] 14D
**Total Dimensions**: 21D
**Code Directory**: `mi_beta/ear/r3/domains/psychoacoustic/`

---

## Domain Description

The Psychoacoustic domain contains features grounded in human auditory
perception research. These features model how the ear and auditory cortex
process spectral information, rather than describing raw acoustic properties.

Group A (Consonance) captures sensory consonance and dissonance -- the
immediate pleasantness or roughness of simultaneous spectral components.
It draws on the Plomp-Levelt critical band beating model and Sethares'
timbre-dependent dissonance framework.

Group K (Modulation & Psychoacoustic) captures temporal modulation perception
(amplitude modulation at cortically relevant rates from 0.5-16 Hz), perceptual
sharpness (DIN 45692 Zwicker model), fluctuation strength, A-weighted loudness,
and spectral shape measures from the eGeMAPS standard. These features bridge
spectral analysis with psychoacoustic perception models.

## Computation Characteristics

Both groups are Stage 1 (mel-only, no inter-group dependencies).

| Property | Group A | Group K |
|----------|---------|---------|
| Stage | 1 (parallel) | 1 (parallel) |
| Input | mel (B, 128, T) | mel (B, 128, T) |
| Dependencies | None | None (K[123] uses K[117] internally) |
| Cost | <0.1 ms/frame | ~3.0 ms/frame (amortized ~0.5 ms) |
| Warm-up | None | 344 frames (2.0s) for modulation features |
| Status | EXISTING | NEW (Phase 3) |

## Group Specifications

- [A-Consonance.md](A-Consonance.md) -- 7D consonance/dissonance features
- [K-ModulationPerception.md](K-ModulationPerception.md) -- 14D modulation and psychoacoustic features

## Domain-Level Phase 6 Notes

- Group A has ~3 effective independent dimensions (out of 7 nominal).
  Duplicates [3]=[12], derived features [4],[5],[6] reduce true dimensionality.
  Phase 6 will replace proxies with real psychoacoustic models.
- Group K is entirely new and does not require Phase 6 revision.
- After Phase 6 revision, the Psychoacoustic domain will represent genuine
  perceptual models rather than spectral statistic proxies.

## Key Literature

- Plomp, R. & Levelt, W. J. M. (1965). Tonal consonance and critical bandwidth.
- Sethares, W. A. (1993). Local consonance and the relationship between timbre and scale.
- Zwicker, E. & Fastl, H. (1999). Psychoacoustics: Facts and Models.
- Chi, T. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis.
- DIN 45692:2009. Measurement technique for the simulation of the auditory sensation of sharpness.
- ISO 226:2003. Normal equal-loudness-level contours.
- Eyben, F. et al. (2015). The Geneva Minimalistic Acoustic Parameter Set (eGeMAPS).
