# PSCL P-Layer — Cognitive Present (4D)

**Layer**: P (Present/Cognitive)
**Dimensions**: 4D (indices 8–11 of PSCL 16D output)
**Input**: R³ direct + H³ tuples + E-layer + M-layer outputs
**Character**: Cognitive-level pitch salience integration — what the listener perceives NOW about pitch prominence

---

## Overview

The P-layer integrates E-layer extractions, M-layer temporal consolidations, and additional H³/R³ features into cognitive-level representations. These outputs represent what the anterolateral HG computes as the "perceptual present" of pitch salience.

P0 (pitch_prominence_sig) is the **primary contributor** to the `pitch_prominence` Core belief (60% weight). P1 (hg_cortical_response) contributes 25%. P3 (salience_hierarchy) contributes 15%.

---

## P0: Pitch Prominence Signal

**Range**: [0, 1]
**Question answered**: "Right now, how prominent is the pitch in this sound?"

### Formula

```python
P0_pitch_prominence_sig = (
    0.25 * E0                         # pitch salience raw (E-layer)
  + 0.25 * M0                         # salience sustained (M-layer)
  + 0.20 * M3                         # BCH integration
  + 0.15 * R3[39]                     # direct pitch_salience
  + 0.15 * H3[39, H6, M0, L2]        # pitch_salience at 200ms (present)
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| E-layer | E0 | pitch_salience_raw | 0.25 |
| M-layer | M0 | salience_sustained | 0.25 |
| M-layer | M3 | bch_integration | 0.20 |
| R³ | [39] | pitch_salience | 0.15 |
| H³ | (39, H6, M0, L2) | pitch_salience at 200ms | 0.15 |

### Logic

Pitch prominence signal integrates four perspectives:
1. **Instantaneous** (25%): E0's frame-local pitch salience assessment
2. **Sustained** (25%): M0's 200ms temporal integration — pitch has been clear
3. **Brainstem** (20%): M3's BCH upstream — subcortical pitch analysis confirms cortical
4. **Direct + temporal** (30%): R³ pitch_salience at both instant and 200ms — redundancy ensures robustness

This is the **primary contributor** to `pitch_prominence` (60% in observe formula). It captures what Penagos 2004 measured: parametric cortical response to pitch salience.

### Evidence
- Penagos 2004: alHG activation scales with pitch salience (p<0.01, 9/10 hemispheres)
- Allen 2022: Pitch-tuned voxels concentrated anterolateral to HG (7T fMRI, N=10)

---

## P1: HG Cortical Response

**Range**: [0, 1]
**Question answered**: "How strongly is the anterolateral HG region responding?"

### Formula

```python
P1_hg_cortical_response = (
    0.30 * E1                         # hg_activation_proxy
  + 0.25 * M1                         # spectral coherence
  + 0.20 * H3[39, H3, M0, L2]        # pitch_salience at 23ms
  + 0.15 * (1 - H3[5, H3, M0, L2])   # low inharmonicity at 23ms
  + 0.10 * H3[15, H3, M0, L2]        # clarity at 23ms
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| E-layer | E1 | hg_activation_proxy | 0.30 |
| M-layer | M1 | spectral_coherence | 0.25 |
| H³ | (39, H3, M0, L2) | pitch_salience at 23ms | 0.20 |
| H³ | (5, H3, M0, L2) | inharmonicity at 23ms (inv) | 0.15 |
| H³ | (15, H3, M0, L2) | clarity at 23ms | 0.10 |

### Logic

HG cortical response is a region-specific activation estimate:
1. **E1 proxy** (30%): Instantaneous HG activation from spectral features
2. **Spectral coherence** (25%): Consistent spectral structure supports cortical pitch extraction
3. **Pitch salience + harmonicity + clarity** (45%): Three fast-timescale (23ms) H³ features confirm cortical activation

This output represents the fMRI-measured BOLD signal: higher for strong pitch, lower for weak pitch, near zero for noise.

### Evidence
- Penagos 2004: MNI-equivalent coordinates: R(48,-11,3), L(-55,-5,3)
- Schonwiesner 2008: Lateral HG = pitch onset (double dissociation with medial HG)
- Bravo 2017: Right HG(48,-10,7) upregulated for low-salience stimuli

---

## P2: Periodicity Clarity

**Range**: [0, 1]
**Question answered**: "How clear is the periodicity of the pitch signal?"

### Formula

```python
P2_periodicity_clarity = (
    0.30 * E3                         # spectral focus
  + 0.25 * H3[24, H6, M14, L0]       # concentration periodicity 200ms
  + 0.25 * H3[17, H3, M0, L2]        # autocorrelation at 23ms
  + 0.20 * R3[14]                     # tonalness
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| E-layer | E3 | spectral_focus | 0.30 |
| H³ | (24, H6, M14, L0) | concentration periodicity 200ms | 0.25 |
| H³ | (17, H3, M0, L2) | autocorrelation at 23ms | 0.25 |
| R³ | [14] | tonalness | 0.20 |

### Logic

Periodicity clarity captures the temporal regularity of pitch:
1. **Spectral focus** (30%): Concentrated energy → clean pitch signal
2. **Concentration periodicity** (25%): Spectral concentration shows periodic pattern over 200ms — the pitch repeats reliably
3. **Autocorrelation** (25%): Current harmonic periodicity confirms spectral regularity
4. **Tonalness** (20%): Harmonic-to-noise ratio as baseline quality measure

This is critical for the Penagos 2004 finding: pitch salience was dissociated from temporal regularity. P2 specifically captures periodicity QUALITY (not just presence), enabling PSCL to model that dissociation.

### Qualification
- Penagos 2004 controlled for temporal regularity: HG responds to pitch salience BEYOND temporal regularity
- P2 complements E2 (salience gradient): E2 captures the parametric ordering, P2 captures why it exists

---

## P3: Salience Hierarchy

**Range**: [0, 1]
**Question answered**: "What is the hierarchical ranking of this pitch's salience?"

### Formula

```python
P3_salience_hierarchy = (
    0.35 * E2                         # salience gradient (E-layer)
  + 0.25 * M2                         # tonal salience context (M-layer)
  + 0.25 * M0                         # salience sustained (M-layer)
  + 0.15 * E0                         # pitch salience raw (E-layer)
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| E-layer | E2 | salience_gradient | 0.35 |
| M-layer | M2 | tonal_salience_ctx | 0.25 |
| M-layer | M0 | salience_sustained | 0.25 |
| E-layer | E0 | pitch_salience_raw | 0.15 |

### Logic

Salience hierarchy ranks the current stimulus in the Strong > Weak > Noise ordering with temporal and tonal context:
1. **E2 gradient** (35%): Instantaneous parametric ranking
2. **Tonal context** (25%): Which pitch class dominates, what register — enriches the ranking with "what"
3. **Sustained salience** (25%): Temporal stability of the ranking over 200ms
4. **Raw salience** (15%): Baseline pitch prominence

This output contributes 15% to `pitch_prominence` observe formula, providing the hierarchical context.

---

## Layer Summary

| Idx | Name | Range | Reads | Downstream |
|-----|------|-------|-------|------------|
| P0 | pitch_prominence_sig | [0, 1] | E0, M0, M3, R³[39], H³(1) | → `pitch_prominence` belief (60%) |
| P1 | hg_cortical_response | [0, 1] | E1, M1, H³(3) | → `pitch_prominence` belief (25%) |
| P2 | periodicity_clarity | [0, 1] | E3, R³[14], H³(2) | → PCCR, downstream models |
| P3 | salience_hierarchy | [0, 1] | E0, E2, M0, M2 | → `pitch_prominence` belief (15%) |

**H³ tuples consumed by P-layer**: 6 (1 in P0 + 3 in P1 + 2 in P2)
**E/M-layer reads**: P0(E0,M0,M3), P1(E1,M1), P2(E3), P3(E0,E2,M0,M2)
