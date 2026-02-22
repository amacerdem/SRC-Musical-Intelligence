# PCCR E-Layer — Extraction (4D)

**Layer**: E (Extraction)
**Dimensions**: 4D (indices 0–3 of PCCR 11D output)
**Input**: R³ direct features only (no H³, no upstream)
**Character**: Instantaneous chroma features — frame-local, no temporal integration

---

## Overview

The E-layer extracts raw pitch-class (chroma) information from R³'s 12-bin chroma vector and associated pitch features. It answers: "What does the chroma distribution look like right now?"

All 4 outputs are gated by pitch presence — if there is no clear pitch (low pitch_salience, high inharmonicity), chroma extraction produces near-zero values.

---

## Outputs

### E0: Chroma Energy — [0, 0.95]

Peak energy in the dominant chroma bin, gated by pitch salience.

```
chroma = R³[25:37]                           # 12 chroma bins (C, C#, D, ..., B)
chroma_peak = max(chroma, dim=-1)            # strongest pitch class
E0 = 0.95 × chroma_peak × R³[39]            # gate by pitch_salience
```

**Interpretation**: High E0 = a single pitch class has strong, salient energy.
Low E0 = either no clear pitch or chroma energy is distributed/weak.

**Ceiling**: 0.95 (leaves headroom for theoretical maximum)

### E1: Chroma Clarity — [0, 0.90]

How clearly does one chroma class dominate the distribution?

```
E1 = 0.90 × (1 − R³[38]) × R³[14]
#          (1 − PCE)      × tonalness
```

**Interpretation**: Low pitch_class_entropy means energy is concentrated in fewer pitch classes. High tonalness means the sound is tonal (vs noise). Together: "one pitch class dominates in a tonal sound."

**Ceiling**: 0.90 (practical maximum for real signals)

### E2: Octave Coherence — [0, 0.85]

Do harmonics agree on a single chroma class (octave-invariant alignment)?

```
E2 = 0.85 × (1 − R³[5]) × R³[17]
#          (1 − inharmonicity) × spectral_autocorrelation
```

**Interpretation**: Harmonic sounds (low inharmonicity) with strong spectral periodicity (high autocorrelation) have partials that naturally fall on octave-equivalent positions. Inharmonic sounds (bells, metallic) break this octave alignment.

**Scientific basis**: Octave equivalence requires harmonicity — Shepard 1964, Patterson 2002.

**Ceiling**: 0.85 (inharmonic timbres prevent full coherence)

### E3: Pitch Class Confidence — [0, 0.90]

Overall confidence in chroma class assignment from multiple indicators.

```
E3 = 0.90 × (
    0.40 × R³[39]            # pitch_salience (is there a clear pitch?)
  + 0.30 × (1 − R³[38])     # 1 − PCE (is energy concentrated?)
  + 0.30 × R³[14]            # tonalness (is the sound tonal?)
)
```

**Interpretation**: Three complementary quality checks:
1. **Pitch salience** (40%): Is there a pitch to assign a class to?
2. **Concentration** (30%): Is chroma energy focused on one class?
3. **Tonalness** (30%): Is the sound tonal enough for pitch-class encoding?

---

## R³ Features Consumed

| # | R³ Index | Feature | Group | Role in E-Layer |
|---|----------|---------|-------|-----------------|
| 1 | **[5]** | inharmonicity | A: Consonance | E2: harmonic quality for octave coherence |
| 2 | **[14]** | tonalness | C: Timbre | E1, E3: tonal quality gate |
| 3 | **[17]** | spectral_autocorrelation | C: Timbre | E2: harmonic periodicity |
| 4 | **[25:37]** | chroma_bins (12D) | F: Pitch/Chroma | E0: pitch class energy distribution |
| 5 | **[38]** | pitch_class_entropy | F: Pitch/Chroma | E1, E3: chroma concentration |
| 6 | **[39]** | pitch_salience | F: Pitch/Chroma | E0, E3: pitch presence gate |

Total unique R³ indices: 16 (12 chroma + 4 scalar)

---

## Downstream Routing

| Output | → Layer | How It's Used |
|--------|---------|---------------|
| E0 | → P0, P2 | Chroma energy feeds identity signal and salience |
| E1 | → P0, P1 | Chroma clarity feeds identity and octave equivalence |
| E2 | → P1 | Octave coherence is primary input to octave equivalence |
| E3 | → P0 | Confidence feeds identity signal |
| E0 | → `pitch_identity` observe | Via P0 (indirect) |
| E1 | → `pitch_identity` observe | 20% direct weight |
| E2 | → `octave_equivalence` observe | Via P1 (indirect) |
