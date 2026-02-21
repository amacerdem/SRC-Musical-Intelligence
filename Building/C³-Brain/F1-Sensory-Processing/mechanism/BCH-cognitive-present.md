# BCH P-Layer — Cognitive Present (4D)

**Layer**: P (Present/Cognitive)
**Dimensions**: 4D (indices 8–11 of BCH 16D output)
**Input**: R³ direct + H³ tuples + E-layer outputs
**Character**: Cognitive-level integration — the "perceptual present" of consonance experience

---

## Overview

The P-layer integrates E-layer extractions, R³ features, and H³ temporal morphologies into cognitive-level representations. These outputs are the closest thing BCH produces to "what the listener perceives right now." Two of these (P0, P1) directly feed the `harmonic_stability` Core belief. P2 feeds PSCL for cortical pitch processing.

---

## P0: Consonance Signal

**Range**: [0, 1]
**Question answered**: "Right now, how consonant does this sound perceived?"

### Formula

```python
P0_consonance_signal = (
    0.20 * (1 - R3[0])                     # low roughness
  + 0.15 * (1 - R3[1])                     # low sethares dissonance
  + 0.15 * (1 - H3[0, H3, M1, L2])        # sustained low roughness 23ms
  + 0.10 * R3[4]                            # sensory_pleasantness
  + 0.10 * (1 - R3[6])                     # low harmonic_deviation
  + 0.10 * (1 - H3[0, H6, M18, L0])       # roughness not increasing (200ms)
  + 0.10 * H3[51, H6, M0, L2]             # key clarity at phrase (200ms)
  + 0.10 * (1 - H3[38, H3, M1, L2])       # sustained tonal clarity (23ms)
)
```

### R³ and H³ Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| R³ | [0] | roughness (inv) | 0.20 |
| R³ | [1] | sethares_dissonance (inv) | 0.15 |
| H³ | (0, H3, M1, L2) | roughness mean 23ms (inv) | 0.15 |
| R³ | [4] | sensory_pleasantness | 0.10 |
| R³ | [6] | harmonic_deviation (inv) | 0.10 |
| H³ | (0, H6, M18, L0) | roughness trend 200ms (inv) | 0.10 |
| H³ | (51, H6, M0, L2) | key_clarity at 200ms | 0.10 |
| H³ | (38, H3, M1, L2) | pitch_class_entropy mean 23ms (inv) | 0.10 |

### Logic

Consonance signal combines three aspects:
1. **Roughness-based** (45%): Low roughness + low sethares + sustained low roughness + stable roughness trend
2. **Spectral regularity** (20%): Pleasantness + low harmonic deviation
3. **Tonal context** (20%): Key clarity at phrase level + tonal clarity (low chroma entropy)

This is the **primary contributor** to `harmonic_stability` (50% weight in observe formula).

---

## P1: Template Match

**Range**: [0, 1]
**Question answered**: "How well do the current partials fit a harmonic series template?"

### Formula

```python
P1_template_match = (
    0.15 * H3[2, H0, M0, L2]              # helmholtz now
  + 0.15 * H3[2, H3, M1, L2]             # helmholtz mean 23ms
  + 0.15 * H3[3, H0, M0, L2]             # stumpf now
  + 0.10 * H3[3, H6, M1, L0]             # stumpf mean 200ms
  + 0.15 * (1 - H3[6, H0, M0, L2])       # low harmonic_deviation now
  + 0.10 * (1 - R3[6])                    # low harmonic_deviation (R³ direct)
  + 0.10 * H3[51, H3, M0, L2]            # key clarity at 23ms
  + 0.10 * R3[60]                          # tonal_stability
)
```

### R³ and H³ Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| H³ | (2, H0, M0, L2) | helmholtz_kang value | 0.15 |
| H³ | (2, H3, M1, L2) | helmholtz_kang mean 23ms | 0.15 |
| H³ | (3, H0, M0, L2) | stumpf_fusion value | 0.15 |
| H³ | (3, H6, M1, L0) | stumpf_fusion mean 200ms | 0.10 |
| H³ | (6, H0, M0, L2) | harmonic_deviation value (inv) | 0.15 |
| R³ | [6] | harmonic_deviation (inv) | 0.10 |
| H³ | (51, H3, M0, L2) | key_clarity at 23ms | 0.10 |
| R³ | [60] | tonal_stability | 0.10 |

### Logic

Template matching evaluates structural consonance:
1. **Helmholtz + Stumpf** (55%): Multi-scale integer ratio detection + tonal fusion
2. **Low harmonic deviation** (25%): Partials close to ideal harmonic positions
3. **Tonal context** (20%): Key clarity + tonal stability ground the template in musical context

**Feeds both**: `harmonic_stability` (30% weight) AND `harmonic_template_match` appraisal belief.

### Distinction from P0 (Consonance Signal)

- **P0** is about *perceptual experience*: "Does this sound pleasant/smooth?" (roughness, pleasantness)
- **P1** is about *structural fit*: "Do the partials match a harmonic series?" (helmholtz, stumpf, deviation)

Both contribute to `harmonic_stability` but capture different aspects.

---

## P2: Neural Pitch

**Range**: [0, ~0.97]
**Question answered**: "How clearly does the brainstem resolve a pitch from this sound?"

### Formula

```python
P2_neural_pitch = (
    0.25 * E0_nps                           # f01_nps (E-layer)
  + 0.15 * R3[14]                           # tonalness
  + 0.15 * (1 - H3[5, H0, M0, L2])        # low inharmonicity now
  + 0.10 * R3[17]                           # spectral_autocorrelation
  + 0.10 * (1 - H3[5, H3, M18, L0])       # inharmonicity not increasing
  + 0.15 * H3[39, H0, M0, L2]             # pitch salience instant (H0)
  + 0.10 * (1 - R3[38])                    # low pitch_class_entropy
)
```

### Logic

Neural pitch clarity from brainstem perspective:
1. **NPS-based** (25%): E-layer NPS computation
2. **Spectral harmonicity** (25%): Tonalness + autocorrelation
3. **Low inharmonicity** (25%): Current + trend-stable
4. **Pitch salience + tonal clarity** (25%): Direct salience + low entropy

### Downstream

**P2 does NOT feed a BCH belief.** It feeds **PSCL (SPU-α2)** for cortical pitch salience processing. PSCL owns the `pitch_prominence` Core belief.

---

## P3: Tonal Context

**Range**: [0, 1]
**Question answered**: "How strong is the current tonal context supporting consonance perception?"

### Formula

```python
P3_tonal_context = (
    0.25 * H3[51, H3, M0, L2]             # key clarity 23ms
  + 0.25 * H3[51, H6, M0, L2]             # key clarity 200ms
  + 0.25 * H3[60, H3, M0, L2]             # tonal stability 23ms
  + 0.25 * R3[60]                           # tonal_stability direct
)
```

### Logic

Pure tonal context aggregation — key clarity and tonal stability at onset and phrase scales. This output enriches all other P-layer and F-layer computations with musical key information.

### Downstream

**P3 does NOT feed a standalone belief.** It serves as a **context enrichment** signal that modulates how consonance_signal and template_match are interpreted within a musical key context.

---

## Layer Summary

| Idx | Name | Range | → Belief | → External |
|-----|------|-------|----------|------------|
| P0 | consonance_signal | [0, 1] | `harmonic_stability` (50%) | → SRP, MEAMN, STAI |
| P1 | template_match | [0, 1] | `harmonic_stability` (30%), `harmonic_template_match` | — |
| P2 | neural_pitch | [0, ~0.97] | — | → PSCL (pitch_prominence) |
| P3 | tonal_context | [0, 1] | — | Context enrichment |

**Belief-producing outputs**: P0, P1 (+ E2 from E-layer)
**Cross-model outputs**: P0, P2
