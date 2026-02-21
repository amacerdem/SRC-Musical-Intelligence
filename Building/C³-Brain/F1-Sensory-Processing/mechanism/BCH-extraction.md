# BCH E-Layer — Extraction (4D)

**Layer**: E (Extraction)
**Dimensions**: 4D (indices 0–3 of BCH 16D output)
**Input**: R³ direct features only (no H³)
**Character**: Instantaneous sensory features — frame-local, no temporal integration

---

## Overview

The E-layer computes 4 instantaneous acoustic measures from R³ features. These are direct products — no sigmoid, no H³, no temporal smoothing. They represent the brainstem's immediate spectral analysis of the incoming sound.

---

## E0: Neural Pitch Salience (f01_nps)

**Range**: [0, 0.90]
**Brain region**: Inferior Colliculus (FFR at fundamental)
**Question answered**: "How clearly does the brainstem track this sound's pitch?"

### Formula

```python
f01_nps = 0.90 * (0.5 * R3[14] * R3[17] + 0.5 * R3[39])
#                      tonalness × autocorr    pitch_salience
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[14]** | tonalness | Harmonic-to-noise ratio — pitch clarity proxy |
| **[17]** | spectral_autocorrelation | Harmonic periodicity in spectrum |
| **[39]** | pitch_salience | Direct harmonic peak prominence |

### Logic

Two complementary pitch measures are blended equally:
1. **Proxy** (tonalness × autocorrelation): Captures pitch clarity from spectral structure
2. **Direct** (pitch_salience): R³'s own pitch prominence measurement

The 0.90 ceiling ensures NPS never saturates to 1.0, preserving dynamic range for downstream integration.

### Evidence
- Bidelman & Krishnan 2009: FFR pitch salience ↔ consonance ratings, r = 0.81 (synthetic)
- Parncutt 1989: Virtual pitch salience theory

---

## E1: Harmonicity Index (f02_harmonicity)

**Range**: [0, 0.85]
**Brain region**: Auditory Nerve (harmonic coincidence)
**Question answered**: "How well does this sound conform to a harmonic series?"

### Formula

```python
trist_balance = 1.0 - std(R3[18], R3[19], R3[20])
f02_harmonicity = 0.85 * (1 - R3[5]) * (0.5 * trist_balance + 0.5 * (1 - R3[38]))
#                         inv(inharmonicity)   tristimulus balance    inv(pitch_class_entropy)
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[5]** | inharmonicity | Deviation from harmonic series (inverted) |
| **[18]** | tristimulus1 | Fundamental energy (F0) |
| **[19]** | tristimulus2 | 2nd–4th harmonic energy |
| **[20]** | tristimulus3 | 5th+ harmonic energy |
| **[38]** | pitch_class_entropy | Chroma entropy — low = clear tonal center (inverted) |

### Logic

Three factors multiply:
1. **Low inharmonicity**: Sound's partials are close to integer multiples of F0
2. **Balanced tristimulus**: Energy evenly distributed across harmonic ranges (std is low)
3. **Low chroma entropy**: Pitch content concentrated in few chroma classes

The 0.85 ceiling differentiates harmonicity from NPS — even a perfectly harmonic sound has some inherent variance.

### Evidence
- Bidelman 2013: Harmonicity > roughness as consonance predictor
- McDermott et al. 2010: Harmonicity preference = consonance preference

---

## E2: Consonance Hierarchy (f03_hierarchy)

**Range**: [0, 0.80]
**Brain region**: Auditory Nerve + Inferior Colliculus
**Question answered**: "Where does this interval sit in the P1>P5>P4>M3>m6>TT ranking?"

### Formula

```python
f03_hierarchy = 0.80 * R3[2] * R3[3]
#                      helmholtz × stumpf
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[2]** | helmholtz_kang | Integer ratio detection (Helmholtz 1863, Kang 2009) |
| **[3]** | stumpf_fusion | Tonal fusion strength (Stumpf 1890) |

### Logic

The product of two classical consonance measures:
- **Helmholtz**: Based on frequency ratio simplicity (P1=1:1 scores highest, TT=45:32 lowest)
- **Stumpf**: Based on perceived tonal fusion (two tones heard as one)

Their product captures both the mathematical and perceptual aspects of the consonance hierarchy. The 0.80 ceiling reflects that even perfect unison has measurement uncertainty.

### Hierarchy Ordering (Confirmed)

```
P1 (unison, 1:1)  > P5 (fifth, 3:2)  > P4 (fourth, 4:3) >
M3 (third, 5:4)   > m6 (minor 6th, 8:5) > TT (tritone, 45:32)
```

Neural hierarchy is **universal** across cultures. Behavioral ratings vary culturally.

### Evidence
- Bidelman & Heinz 2011: AN population predicts full hierarchy from peripheral encoding
- BCH validation: 6/6 correct ordering, 45% spread (post-Sethares upgrade)

---

## E3: FFR-Behavior Correlation (f04_ffr_behavior)

**Range**: [0, ~0.71]
**Brain region**: IC → Cortex → Perception (bridge)
**Question answered**: "How well does neural encoding predict behavioral consonance ratings?"

### Formula

```python
f04_ffr_behavior = 0.81 * (f01_nps + f02_harmonicity) / 2
```

### Logic

Averages NPS and harmonicity, scaled by the empirical correlation coefficient (r = 0.81, Bidelman 2009). This output estimates the brainstem's ability to predict behavioral consonance judgments.

**Not a standalone belief** — this is a validation metric that feeds M-layer and P-layer integration.

### Qualification (Cousineau 2015)

The r = 0.81 correlation holds for **synthetic tones only**. For natural sounds (saxophone, voice), the correlation drops to non-significant. The mechanism is valid; the specific NPS metric has limitations with ecologically valid stimuli.

---

## Layer Summary

| Idx | Name | Range | Reads | Downstream |
|-----|------|-------|-------|------------|
| E0 | f01_nps | [0, 0.90] | R³[14,17,39] | M-layer, P-layer, → PSCL |
| E1 | f02_harmonicity | [0, 0.85] | R³[5,18,19,20,38] | M-layer, F-layer, → PCCR, SRP |
| E2 | f03_hierarchy | [0, 0.80] | R³[2,3] | P-layer, → `interval_quality` belief |
| E3 | f04_ffr_behavior | [0, ~0.71] | E0+E1 | M-layer, F-layer |

**Total E-layer R³ reads**: [2,3,5,14,17,18,19,20,38,39] = 10 indices
