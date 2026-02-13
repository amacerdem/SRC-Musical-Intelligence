# Tonal Domain -- Groups F + H (28D)

**Domain**: Pitch & harmony analysis
**Groups**: F:PitchChroma [49:65] 16D, H:HarmonyTonality [75:87] 12D
**Total Dimensions**: 28D
**Code Directory**: `mi_beta/ear/r3/domains/tonal/`

---

## Domain Description

The Tonal domain analyzes pitch content and harmonic structure. Group F extracts
the fundamental pitch representation -- a 12-dimensional chroma vector encoding
the energy distribution across pitch classes (C through B), plus pitch height,
pitch class entropy, pitch salience, and inharmonicity. Group H builds on F's
chroma output to compute higher-level harmonic features: key clarity (tonal
center strength), tonnetz coordinates (6D tonal space embedding), voice-leading
distance, harmonic change, tonal stability, diatonicity, and syntactic
irregularity.

This domain answers two fundamental questions: "what notes are present?" (F)
and "what key/chord context do they form?" (H).

## Computation Characteristics

Group F is Stage 1 (mel-only). Group H is Stage 2 (depends on F's chroma).

| Property | Group F | Group H |
|----------|---------|---------|
| Stage | 1 (parallel) | 2 (after F) |
| Input | mel (B, 128, T) | F[49:61] chroma (B, T, 12) |
| Dependencies | None | F chroma output |
| Cost | ~1.0 ms/frame | ~1.0 ms/frame |
| Warm-up | None | None |
| Status | NEW (Phase 3) | NEW (Phase 3) |

## Dependency Chain

```
mel (B, 128, T)
  |
  v
Group F: PitchChroma [49:65]
  |-- chroma (12D) [49:60]
  |-- pitch_height [61]
  |-- pitch_class_entropy [62]
  |-- pitch_salience [63]
  |-- inharmonicity_index [64]
  |
  v  (chroma output passed to Stage 2)
Group H: HarmonyTonality [75:87]
  |-- key_clarity [75]
  |-- tonnetz (6D) [76:81]
  |-- voice_leading_distance [82]
  |-- harmonic_change [83]
  |-- tonal_stability [84]
  |-- diatonicity [85]
  |-- syntactic_irregularity [86]
```

Additionally, Group I (Information domain) depends on F chroma and H key
correlations for melodic_entropy, harmonic_entropy, and tonal_ambiguity.

## Group Specifications

- [F-PitchChroma.md](F-PitchChroma.md) -- 16D pitch and chroma features
- [H-HarmonyTonality.md](H-HarmonyTonality.md) -- 12D harmony and tonality features

## Mel-to-Chroma Quality Note

The chroma computation uses mel-to-frequency-to-pitch-class folding with
Gaussian soft assignment (sigma = 0.5 semitone). This is approximate: below
200 Hz, mel bins span more than one semitone, reducing pitch class resolution.
Quality is MEDIUM -- adequate for key estimation (>=85% accuracy) but inferior
to CQT-based chroma. See F-PitchChroma.md for the full algorithm.

## Key Literature

- Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch. Oxford UP.
- Shepard, R. N. (1964). Circularity in judgments of relative pitch. JASA 36(12).
- Krumhansl, C. L. & Kessler, E. J. (1982). Tracing the dynamic changes in perceived tonal organization. Psychological Review 89(4).
- Harte, C. et al. (2006). Detecting harmonic change in musical audio. ACM MM.
- Tymoczko, D. (2011). A Geometry of Music. Oxford UP.
- Lerdahl, F. (2001). Tonal Pitch Space. Oxford UP.
- Parncutt, R. (1989). Harmony: A Psychoacoustical Approach. Springer.
