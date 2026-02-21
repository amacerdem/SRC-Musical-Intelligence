# BCH M-Layer — Temporal Integration (4D)

**Layer**: M (Memory/Temporal)
**Dimensions**: 4D (indices 4–7 of BCH 16D output)
**Input**: H³ tuples (L2 present + L0 past) + R³ direct
**Character**: Multi-scale temporal consolidation — H³ provides sliding-window morphologies

---

## Overview

The M-layer integrates H³ temporal morphologies to transform instantaneous E-layer snapshots into temporally grounded representations. Each M output is a weighted sum of H³ features at multiple brainstem timescales (H0=5.8ms, H3=23ms, H6=200ms, H12=525ms, H16=1s).

BCH is a relay — it has no internal memory. All temporal integration is performed by H³'s stateless window operators.

---

## M0: Consonance Memory

**Range**: [0, 1]
**Question answered**: "Over the recent past, how consonant has this sound been?"

### Formula

```python
M0_consonance_memory = (
    0.20 * (1 - H3[0, H0, M0, L2])        # low roughness now
  + 0.15 * (1 - H3[0, H3, M1, L2])        # low roughness sustained 23ms
  + 0.10 * (1 - H3[0, H6, M18, L0])       # roughness not increasing (200ms trend)
  + 0.10 * R3[4]                            # sensory_pleasantness
  + 0.10 * coupling                         # consonance×timbre (internal)
  + 0.05 * H3[0, H6, M14, L2]             # roughness periodicity (replaced coupling_per)
  + 0.15 * H3[39, H3, M0, L2]             # pitch salience sustained 23ms
  + 0.15 * (1 - H3[38, H0, M0, L2])       # low chroma entropy = tonal clarity
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 0 | roughness | 0 | M0 | L2 | 0.20 |
| 0 | roughness | 3 | M1 | L2 | 0.15 |
| 0 | roughness | 6 | M18 | L0 | 0.10 |
| 39 | pitch_salience | 3 | M0 | L2 | 0.15 |
| 38 | pitch_class_entropy | 0 | M0 | L2 | 0.15 |

### Logic

Consonance memory integrates: low roughness (3 timescales) + spectral pleasantness + consonance-timbre coupling + pitch salience + tonal clarity. This captures "has the sound been consonant over the last ~200ms?"

---

## M1: Pitch Memory

**Range**: [0, 1]
**Question answered**: "Over the recent past, how clear and stable has the pitch been?"

### Formula

```python
M1_pitch_memory = (
    0.25 * H3[39, H0, M0, L2]             # pitch salience now
  + 0.20 * H3[39, H3, M0, L2]             # pitch salience 23ms
  + 0.15 * H3[39, H6, M0, L2]             # pitch salience 200ms
  + 0.15 * (1 - H3[5, H0, M0, L2])        # low inharmonicity now
  + 0.10 * (1 - H3[5, H3, M18, L0])       # inharmonicity not increasing
  + 0.15 * (1 - H3[38, H3, M1, L2])       # sustained low chroma entropy
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 39 | pitch_salience | 0 | M0 | L2 | 0.25 |
| 39 | pitch_salience | 3 | M0 | L2 | 0.20 |
| 39 | pitch_salience | 6 | M0 | L2 | 0.15 |
| 5 | inharmonicity | 0 | M0 | L2 | 0.15 |
| 5 | inharmonicity | 3 | M18 | L0 | 0.10 |
| 38 | pitch_class_entropy | 3 | M1 | L2 | 0.15 |

### Logic

Pitch memory tracks pitch salience at 3 temporal scales (instant, onset, phrase) + low inharmonicity + tonal clarity. Feeds P-layer's neural_pitch computation and PSCL downstream.

---

## M2: Tonal Memory

**Range**: [0, 1]
**Question answered**: "Over the recent past, how clear has the tonal context been?"

### Formula

```python
M2_tonal_memory = (
    0.20 * H3[51, H3, M0, L2]             # key clarity 23ms
  + 0.20 * H3[51, H3, M1, L2]             # sustained key clarity 23ms
  + 0.20 * H3[51, H6, M0, L2]             # key clarity 200ms
  + 0.20 * H3[60, H3, M0, L2]             # tonal stability 23ms
  + 0.20 * H3[60, H6, M1, L0]             # sustained tonal stability 200ms
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 51 | key_clarity | 3 | M0 | L2 | 0.20 |
| 51 | key_clarity | 3 | M1 | L2 | 0.20 |
| 51 | key_clarity | 6 | M0 | L2 | 0.20 |
| 60 | tonal_stability | 3 | M0 | L2 | 0.20 |
| 60 | tonal_stability | 6 | M1 | L0 | 0.20 |

### Logic

Tonal memory aggregates key clarity and tonal stability at onset (23ms) and phrase (200ms) scales. Equal weighting reflects that both key and stability are equally important for tonal context.

---

## M3: Spectral Memory

**Range**: [0, 1]
**Question answered**: "Over the recent past, how spectrally coherent has the sound been?"

### Formula

```python
trist1_h0 = H3[18, H0, M0, L2]
trist2_h0 = H3[19, H0, M0, L2]
trist3_h0 = H3[20, H0, M0, L2]
trist_balance_h = 1.0 - std(trist1_h0, trist2_h0, trist3_h0)

M3_spectral_memory = (
    0.25 * trist_balance_h                  # balanced harmonic energy
  + 0.25 * (1 - H3[6, H0, M0, L2])        # low harmonic deviation now
  + 0.25 * (1 - H3[6, H3, M1, L0])        # sustained low deviation 23ms
  + 0.25 * (1 - H3[5, H12, M1, L0])       # low inharmonicity 525ms
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 18 | tristimulus1 | 0 | M0 | L2 | via trist_balance |
| 19 | tristimulus2 | 0 | M0 | L2 | via trist_balance |
| 20 | tristimulus3 | 0 | M0 | L2 | via trist_balance |
| 6 | harmonic_deviation | 0 | M0 | L2 | 0.25 |
| 6 | harmonic_deviation | 3 | M1 | L0 | 0.25 |
| 5 | inharmonicity | 12 | M1 | L0 | 0.25 |

### Logic

Spectral memory captures harmonic spectral coherence: balanced tristimulus (energy distribution across harmonic bands) + low harmonic deviation + low inharmonicity at extended timescales.

---

## Layer Summary

| Idx | Name | Range | Key H³ Scales | Purpose |
|-----|------|-------|---------------|---------|
| M0 | consonance_memory | [0, 1] | H0, H3, H6 | Temporal consonance context |
| M1 | pitch_memory | [0, 1] | H0, H3, H6 | Temporal pitch clarity context |
| M2 | tonal_memory | [0, 1] | H3, H6 | Temporal tonal context |
| M3 | spectral_memory | [0, 1] | H0, H3, H12 | Temporal spectral coherence |

**Total M-layer H³ tuples**: ~20 (subset of BCH's 48 total)
