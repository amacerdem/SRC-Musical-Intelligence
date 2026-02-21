# PSCL M-Layer — Temporal Integration (4D)

**Layer**: M (Memory/Temporal)
**Dimensions**: 4D (indices 4–7 of PSCL 16D output)
**Input**: H³ tuples (L2 present + L0 memory) + R³ direct + BCH relay output
**Character**: Multi-scale temporal consolidation at cortical pitch processing timescales

---

## Overview

The M-layer integrates H³ temporal morphologies to transform E-layer snapshots into temporally grounded representations. PSCL operates at cortical timescales (H3=23ms auditory processing, H6=200ms cortical evaluation), not brainstem timescales.

Critically, M3 is the **BCH integration channel**: PSCL is Depth 1 and reads BCH's relay output directly. This is where brainstem pitch salience meets cortical processing.

---

## M0: Salience Sustained

**Range**: [0, 1]
**Question answered**: "Over the recent 200ms, how salient has the pitch been?"

### Formula

```python
M0_salience_sustained = (
    0.25 * H3[14, H6, M1, L0]       # tonalness mean over 200ms
  + 0.25 * H3[39, H6, M1, L0]       # pitch_salience mean over 200ms
  + 0.20 * H3[17, H6, M1, L0]       # autocorrelation mean over 200ms
  + 0.15 * H3[18, H6, M1, L0]       # tristimulus1 mean over 200ms
  + 0.15 * H3[24, H6, M14, L0]      # concentration periodicity 200ms
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 14 | tonalness | 6 | M1 (mean) | L0 | 0.25 |
| 39 | pitch_salience | 6 | M1 (mean) | L0 | 0.25 |
| 17 | spectral_autocorrelation | 6 | M1 (mean) | L0 | 0.20 |
| 18 | tristimulus1 | 6 | M1 (mean) | L0 | 0.15 |
| 24 | distribution_concentration | 6 | M14 (periodicity) | L0 | 0.15 |

### Logic

Sustained salience captures "has the pitch been clear and prominent over the last 200ms?":
- **Tonalness + pitch_salience** (50%): Two primary salience indicators sustained over cortical evaluation window
- **Autocorrelation** (20%): Sustained harmonic periodicity
- **F0 strength** (15%): Sustained fundamental — stable pitch source
- **Concentration periodicity** (15%): Regular spectral focus pattern — not random energy fluctuation

---

## M1: Spectral Coherence

**Range**: [0, 1]
**Question answered**: "Is the spectral structure consistent right now?"

### Formula

```python
M1_spectral_coherence = (
    0.30 * H3[17, H3, M0, L2]       # autocorrelation at 23ms (present)
  + 0.30 * H3[14, H3, M0, L2]       # tonalness at 23ms (present)
  + 0.20 * H3[18, H3, M0, L2]       # tristimulus1 at 23ms (present)
  + 0.20 * (1 - H3[22, H6, M1, L0]) # low entropy sustained 200ms
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 17 | spectral_autocorrelation | 3 | M0 (value) | L2 | 0.30 |
| 14 | tonalness | 3 | M0 (value) | L2 | 0.30 |
| 18 | tristimulus1 | 3 | M0 (value) | L2 | 0.20 |
| 22 | distribution_entropy | 6 | M1 (mean) | L0 | 0.20 |

### Logic

Spectral coherence combines present-moment spectral quality with sustained spectral order:
- **Autocorrelation + tonalness** (60%): Current spectral structure quality at fast timescale (23ms)
- **F0 strength** (20%): Current fundamental energy — key pitch cue
- **Low sustained entropy** (20%): Spectrum has been ordered (not noise) over 200ms

This feeds P1 (HG cortical response) where spectral coherence modulates cortical activation.

---

## M2: Tonal Salience Context

**Range**: [0, 1]
**Question answered**: "What is the tonal context of the current pitch salience?"

### Formula

```python
chroma_peak = max(R3[25:37])         # strongest pitch class activation
M2_tonal_salience_ctx = (
    0.35 * chroma_peak               # dominant chroma
  + 0.30 * R3[39]                    # pitch salience
  + 0.20 * (1 - R3[22])             # low entropy = tonal
  + 0.15 * R3[37]                    # pitch height (register)
)
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[25:37]** | chroma_vector (12D) | Pitch class distribution — peak indicates tonal focus |
| **[39]** | pitch_salience | Direct pitch prominence |
| **[22]** | distribution_entropy (inv) | Low entropy = clear tonal structure |
| **[37]** | pitch_height | Register context (frequency range) |

### Logic

Tonal context enriches pitch salience with "what pitch" information:
- **Chroma peak** (35%): The strongest pitch class — tells which note dominates
- **Pitch salience** (30%): How prominent that pitch is
- **Tonal order** (20%): Whether the spectral environment is tonal (low entropy) or noisy
- **Register** (15%): Where in the frequency range — salience varies with register (Pressnitzer 2001)

This output feeds P3 (salience hierarchy) and F-layer melody/register predictions.

---

## M3: BCH Integration

**Range**: [0, 1]
**Question answered**: "What does the brainstem pitch analysis tell the cortex?"

### Formula

```python
M3_bch_integration = (
    0.40 * BCH.E0_nps                # brainstem neural pitch salience
  + 0.30 * BCH.E1_harmonicity        # harmonic series conformity
  + 0.20 * BCH.P0_consonance_signal  # perceptual consonance
  + 0.10 * BCH.F1_pitch_forecast     # brainstem pitch trajectory
)
```

### Upstream Inputs (BCH Relay, 16D)

| BCH Output | Layer | Weight | What It Provides |
|------------|-------|--------|------------------|
| E0:nps | E-layer | 0.40 | Brainstem pitch clarity (how well brainstem tracks F0) |
| E1:harmonicity | E-layer | 0.30 | Harmonic series conformity (partials = integer × F0?) |
| P0:consonance_signal | P-layer | 0.20 | Integrated perceptual consonance (roughness + tonal context) |
| F1:pitch_forecast | F-layer | 0.10 | Brainstem-level pitch trajectory (what BCH predicts) |

### Logic

BCH integration is the key architectural feature distinguishing PSCL from BCH:
- **BCH is brainstem**: Auditory nerve, inferior colliculus, FFR
- **PSCL is cortical**: Anterolateral Heschl's Gyrus, non-primary AC

M3 is the bridge: it takes BCH's brainstem analysis and makes it available for cortical processing. The dominant weight (40%) goes to NPS — this is the primary subcortical-to-cortical pitch signal.

### Evidence
- Penagos 2004: Subcortical processing (no salience differences) → alHG (parametric salience)
- Bidelman 2013: Brainstem FFR pitch salience predicts cortical consonance processing

---

## Layer Summary

| Idx | Name | Range | Reads | Downstream |
|-----|------|-------|-------|------------|
| M0 | salience_sustained | [0, 1] | H³: 5 tuples | P-layer |
| M1 | spectral_coherence | [0, 1] | H³: 4 tuples | P-layer |
| M2 | tonal_salience_ctx | [0, 1] | R³[22,25:37,37,39] | P-layer, F-layer |
| M3 | bch_integration | [0, 1] | BCH relay: E0,E1,P0,F1 | P-layer, F-layer |

**H³ tuples consumed by M-layer**: 9 (5 in M0 + 4 in M1)
**BCH relay fields consumed**: 4 (E0, E1, P0, F1)
