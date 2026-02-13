# R3 v2 Domain Taxonomy

**Version**: 2.0
**Date**: 2026-02-13
**Source**: R3-V2-DESIGN.md, R3-CROSSREF.md
**Total Dimensionality**: 128D (11 groups, 6 domains)

---

## 1. Domain Architecture

The 128D R3 spectral vector is organized into 6 perceptual domains. Each domain
groups features that share a common psychoacoustic processing pathway and
conceptual foundation. The domain structure maps directly to the code directory
hierarchy under `mi_beta/ear/r3/domains/`.

```
R3 128D Spectral Vector
=========================
Domain               Groups              Indices     Dims   Stage
-----------------------------------------------------------------
Psychoacoustic       A:Consonance        [0:7]        7D    1
                     K:ModPerception     [114:128]   14D    1
                     -------------------------------- 21D

Spectral             C:Timbre            [12:21]      9D    1
                     D:Change            [21:25]      4D    1
                     J:TimbreExtended    [94:114]    20D    1
                     -------------------------------- 33D

Tonal                F:PitchChroma       [49:65]     16D    1
                     H:HarmonyTonality   [75:87]     12D    2
                     -------------------------------- 28D

Temporal             B:Energy            [7:12]       5D    1
                     G:RhythmGroove      [65:75]     10D    2
                     -------------------------------- 15D

Information          I:InfoSurprise      [87:94]      7D    3
                     --------------------------------  7D

CrossDomain          E:Interactions      [25:49]     24D    2
                     -------------------------------- 24D

TOTAL                                    [0:128]    128D
```

## 2. Domain Rationale

### Psychoacoustic (21D) -- Groups A + K
Human auditory perception models rooted in Zwicker/Fastl and Plomp-Levelt
traditions. Group A captures consonance/dissonance judgments; Group K adds
modulation spectrum perception, sharpness (DIN 45692), fluctuation strength,
and A-weighted loudness. Together they represent "how the ear processes sound."

### Spectral (33D) -- Groups C + D + J
Spectral shape and texture analysis. Group C provides basic timbral descriptors
(warmth, sharpness, tonalness, tristimulus). Group D measures spectral change
and distribution statistics. Group J extends with MFCC (cepstral timbre) and
spectral contrast (harmonic-vs-noise texture). This domain answers "what does
the sound look like spectrally?"

### Tonal (28D) -- Groups F + H
Pitch and harmony analysis. Group F extracts chroma vectors (12D pitch class
profiles), pitch height, pitch class entropy, pitch salience, and inharmonicity.
Group H builds on F's chroma output to compute key clarity, tonnetz coordinates,
voice-leading distance, harmonic change, tonal stability, diatonicity, and
syntactic irregularity. This domain answers "what notes and chords are present?"

### Temporal (15D) -- Groups B + G
Energy dynamics and rhythmic structure. Group B tracks amplitude, velocity,
acceleration, loudness, and onset strength. Group G uses onset autocorrelation
to derive tempo, beat strength, pulse clarity, syncopation, metricality,
groove, and rhythmic regularity. This domain answers "when do events happen
and how do they relate temporally?"

### Information (7D) -- Group I
Information-theoretic measures of predictability and surprise. Melodic entropy,
harmonic entropy, rhythmic information content, spectral surprise, information
rate, predictive entropy, and tonal ambiguity. Depends on F (chroma), G (onset),
and H (key). This domain answers "how surprising is this moment?"

### CrossDomain (24D) -- Group E
Inter-group interaction terms capturing cross-feature coupling. Currently
24D of element-wise products across Energy x Consonance, Change x Consonance,
and Consonance x Timbre. Phase 6 will fix proxy mismatches and Phase 6+ may
extend to F-K cross-products. This domain answers "how do features modulate
each other?"

## 3. Code Directory Mapping

```
mi_beta/ear/r3/
  domains/
    psychoacoustic/
      consonance.py          # Group A [0:7]    EXISTING
      modulation.py          # Group K [114:128] NEW (Phase 3)
    spectral/
      timbre.py              # Group C [12:21]   EXISTING
      change.py              # Group D [21:25]   EXISTING
      timbre_extended.py     # Group J [94:114]  NEW (Phase 3)
    tonal/
      pitch_chroma.py        # Group F [49:65]   NEW (Phase 3)
      harmony_tonality.py    # Group H [75:87]   NEW (Phase 3)
    temporal/
      energy.py              # Group B [7:12]    EXISTING
      rhythm_groove.py       # Group G [65:75]   NEW (Phase 3)
    information/
      info_surprise.py       # Group I [87:94]   NEW (Phase 3)
    cross_domain/
      interactions.py        # Group E [25:49]   EXISTING
```

Note: Current code is located in the v1 directory structure
(`mi_beta/ear/r3/psychoacoustic/`, `mi_beta/ear/r3/dsp/`, etc.).
The domain-organized directory structure above is the Phase 6 target layout.

## 4. Computation Pipeline (3-Stage DAG)

```
mel (B, 128, T) @ 172.27 Hz
         |
Stage 1 (parallel, ~3.0ms):
  [A] [B] [C] [D] [F] [J] [K]
         |
Stage 2 (parallel, ~1.0ms):
  [E] <- A,B,C,D
  [G] <- B[11] onset_strength
  [H] <- F[49:61] chroma
         |
Stage 3 (~0.5ms):
  [I] <- F chroma, G onset, H key
         |
Concat: torch.cat([A..K], dim=-1) -> (B, T, 128)
```

Amortized total latency: ~2.5 ms/frame (2.3x real-time headroom at 172 Hz).

## 5. Group Status Summary

| Group | Domain        | Status   | Phase 6 Action               |
|-------|---------------|----------|-------------------------------|
| A     | Psychoacoustic| EXISTING | Formula revision (Plomp-Levelt, Sethares) |
| B     | Temporal      | EXISTING | Loudness double-compression fix |
| C     | Spectral      | EXISTING | Duplicate resolution ([16],[17]) |
| D     | Spectral      | EXISTING | Concentration [24] bug fix    |
| E     | CrossDomain   | EXISTING | Proxy fix + potential expansion |
| F     | Tonal         | NEW      | Phase 3 implementation        |
| G     | Temporal      | NEW      | Phase 3 implementation        |
| H     | Tonal         | NEW      | Phase 3 implementation        |
| I     | Information   | NEW      | Phase 3 implementation        |
| J     | Spectral      | NEW      | Phase 3 implementation        |
| K     | Psychoacoustic| NEW      | Phase 3 implementation        |

## 6. Document Index

| File | Content |
|------|---------|
| `Psychoacoustic/00-INDEX.md` | Domain overview for Groups A + K |
| `Psychoacoustic/A-Consonance.md` | Group A spec [0:7] 7D |
| `Psychoacoustic/K-ModulationPerception.md` | Group K spec [114:128] 14D |
| `Spectral/00-INDEX.md` | Domain overview for Groups C + D + J |
| `Spectral/C-Timbre.md` | Group C spec [12:21] 9D |
| `Spectral/D-Change.md` | Group D spec [21:25] 4D |
| `Spectral/J-TimbreExtended.md` | Group J spec [94:114] 20D |
| `Tonal/00-INDEX.md` | Domain overview for Groups F + H |
| `Tonal/F-PitchChroma.md` | Group F spec [49:65] 16D |
| `Tonal/H-HarmonyTonality.md` | Group H spec [75:87] 12D |
| `Temporal/00-INDEX.md` | Domain overview for Groups B + G |
| `Temporal/B-Energy.md` | Group B spec [7:12] 5D |
| `Temporal/G-RhythmGroove.md` | Group G spec [65:75] 10D |
| `Information/00-INDEX.md` | Domain overview for Group I |
| `Information/I-InformationSurprise.md` | Group I spec [87:94] 7D |
| `CrossDomain/00-INDEX.md` | Domain overview for Group E |
| `CrossDomain/E-Interactions.md` | Group E spec [25:49] 24D |
