# MDNS P-Layer — Cognitive Present (3D)

**Layer**: P (Present)
**Dimensions**: 3D (indices 6–8 of MDNS 12D output)
**Input**: H³ tuples + R³ direct + E-layer features
**Character**: Real-time melody processing state — onset detection, pitch identification, phrase position

---

## Overview

The P-layer represents the current cognitive state of melody processing. Three outputs capture what the auditory system is doing right now: detecting note boundaries, identifying pitches, and tracking position within the current phrase. These are the "present-tense" representations that belief systems observe.

---

## P0: Onset Detection (onset_detection)

**Range**: [0, 1]
**Brain region**: Bilateral STG (real-time note boundary detection)
**Question answered**: "Is a note onset occurring right now?"

### Formula

```python
flux_val = H3[(10, 6, 0, 0)]    # spectral_flux value at H6
onset_val = H3[(11, 6, 0, 0)]   # onset_strength value at H6
onset_detection = σ(flux_val * onset_val)
```

### Logic

Product of spectral flux and onset strength at the beat-entrainment horizon. Similar to E0 but without the α=0.80 scaling — this is the raw onset state, not the tracking quality. High when both spectral change and onset energy coincide → note boundary.

---

## P1: Pitch Tracking (pitch_tracking)

**Range**: [0, 1]
**Brain region**: Heschl's Gyrus / PT (real-time pitch identification)
**Question answered**: "How clearly is the current pitch being tracked?"

### Formula

```python
tonalness = R3[14]
autocorr = R3[17]
trist = R3[18:21]                # tristimulus 1-3
trist_consistency = 1.0 - std(trist)
pitch_tracking = σ(tonalness * autocorr * trist_consistency)
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[14]** | tonalness | Harmonic-to-noise ratio — pitch clarity |
| **[17]** | spectral_autocorrelation | Harmonic periodicity |
| **[18:21]** | tristimulus1-3 | Harmonic energy distribution consistency |

### Logic

Triple product of tonal clarity, harmonic periodicity, and spectral consistency. When all three are high, the system is confidently tracking a clear pitch. Low tristimulus std means balanced harmonic energy → stable pitch identity. Uses R³ direct (frame-level) for real-time state.

---

## P2: Phrase Position (phrase_position)

**Range**: [0, 1]
**Brain region**: STG → frontal (phrase boundary detection)
**Question answered**: "Where within the current melodic phrase are we?"

### Formula

```python
phrase_entropy = H3[(25, 14, 13, 0)]   # x_l0l5 entropy at H14 (700ms)
phrase_position = σ(phrase_entropy)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 14 | M13 (entropy) | L0 | Phrase-level unpredictability |

### Logic

Entropy of the TRF basis function at the phrase horizon (700ms). High entropy = middle of phrase (many possible continuations). Low entropy = near phrase boundary (predictable cadence or ending). This maps to the intuitive sense of "where are we in the melody."

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| P0 | onset_detection | [0, 1] | H³ flux×onset at H6 | F-layer, → AMSS phrase context |
| P1 | pitch_tracking | [0, 1] | R³ tonalness×autocorr×trist | F-layer, → TPIO pitch basis |
| P2 | phrase_position | [0, 1] | H³ entropy at H14 | F-layer, → beliefs phrase tracking |

**Total P-layer H³ tuples**: 1 unique (reuses E-layer tuples for P0)
