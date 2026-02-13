# Spectral Domain -- Groups C + D + J (33D)

**Domain**: Spectral shape analysis
**Groups**: C:Timbre [12:21] 9D, D:Change [21:25] 4D, J:TimbreExtended [94:114] 20D
**Total Dimensions**: 33D
**Code Directory**: `mi_beta/ear/r3/domains/spectral/`

---

## Domain Description

The Spectral domain characterizes the shape, distribution, and temporal
evolution of the frequency spectrum. These features describe "what the sound
looks like" in the spectral domain, without interpreting it through
psychoacoustic or tonal lenses.

Group C (Timbre) provides fundamental timbral descriptors: warmth (low-frequency
balance), sharpness (high-frequency emphasis), tonalness (peak dominance),
clarity (spectral centroid), spectral smoothness, spectral autocorrelation,
and the tristimulus energy distribution across spectral thirds.

Group D (Change) measures frame-to-frame spectral evolution: spectral flux
(L2 change magnitude), Shannon entropy, Wiener flatness, and Herfindahl
concentration. These features feed the prediction error pathway.

Group J (Timbre Extended) adds 20D of evidence-based timbral features:
MFCC coefficients 1-13 (cepstral timbre representation) and spectral
contrast in 7 octave sub-bands (harmonic vs. noisy texture discrimination).
These are the most widely validated features in MIR research.

## Computation Characteristics

All three groups are Stage 1 (mel-only, no inter-group dependencies).

| Property | Group C | Group D | Group J |
|----------|---------|---------|---------|
| Stage | 1 (parallel) | 1 (parallel) | 1 (parallel) |
| Input | mel (B, 128, T) | mel (B, 128, T) | mel (B, 128, T) |
| Dependencies | None | None | None |
| Cost | <0.1 ms | <0.1 ms | ~0.5 ms |
| Warm-up | None | None | None |
| Status | EXISTING | EXISTING | NEW (Phase 3) |

## Group Specifications

- [C-Timbre.md](C-Timbre.md) -- 9D timbral shape features
- [D-Change.md](D-Change.md) -- 4D spectral change/distribution features
- [J-TimbreExtended.md](J-TimbreExtended.md) -- 20D MFCC + spectral contrast

## Domain-Level Phase 6 Notes

- Group C has 3 cross-group duplicates: [12]=[3], [16]=1-[1], [17]=[2].
  Effective independent dimensionality is ~4 out of 9.
- Group D has a normalization bug in [24] concentration where both uniform
  and concentrated distributions map to 1.0.
- Group J is entirely new and does not require Phase 6 revision.
- After Phase 6, Groups C and D will have their duplicates replaced with
  spectral_spread, spectral_kurtosis, and corrected concentration.

## Key Literature

- Krimphoff, J. et al. (1994). Characterization of the timbre of complex sounds. JASA 95(5), 3684-3695.
- Pollard, H. F. & Jansson, E. V. (1982). A tristimulus method for the specification of musical timbre. Acustica 51(3), 162-171.
- Jiang, D. N. et al. (2002). Music type classification by spectral contrast feature. ICME 2002.
- Davis, S. & Mermelstein, P. (1980). Comparison of parametric representations for monosyllabic word recognition. IEEE Trans. ASSP 28(4), 357-366.
