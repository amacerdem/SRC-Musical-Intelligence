# H3-Demand -- Temporal Demand Patterns Across All Models

> **Scope**: 96 models across 9 units
> **H3 Space**: v1: 112,896 theoretical (49 R3 x 32 horizons x 24 morphs x 3 laws); v2: 294,912 (128 R3)
> **Actual Usage**: Sparse — v1: ~5,200 tuples (~4.6%); v2 projected: ~8,600 tuples (~2.9%)
> **Data Source**: Model `h3_demand` properties, mechanism `HORIZONS` declarations, `mi_beta.core.constants`
> **Definitive H³ reference**: [Docs/H³/00-INDEX.md](../../H³/00-INDEX.md)
> **Last Updated**: 2026-02-13

---

## H3 Architecture Overview

The H3 temporal analysis system transforms each R3 spectral feature into temporal morphological descriptors at multiple time horizons. With R3 v1 (49D), this covers features [0:48]; with R3 v2 (128D), this extends to [0:127]. Each H3 demand tuple is a 4-tuple:

```
(r3_idx, horizon, morph, law)
```

| Field | Range | Description |
|-------|-------|-------------|
| `r3_idx` | 0--48 (v1) / 0--127 (v2) | Which R3 spectral feature to analyze temporally |
| `horizon` | 0--31 | Temporal window index (maps to specific duration in ms) |
| `morph` | 0--23 | Which morphological statistic to compute |
| `law` | 0--2 | Temporal perspective (0=memory, 1=prediction, 2=integration) |

**Theoretical space**: v1: 49 x 32 x 24 x 3 = 112,896 possible tuples; v2: 128 x 32 x 24 x 3 = 294,912.
**Actual usage**: Each model typically requests 10--150 tuples. v1 total: ~5,200 tuples (~4.6%); v2 projected: ~8,600 tuples (~2.9%).

---

## Horizon Definitions

The 32 horizons span from sub-beat (~6ms) to full-piece (~16min) timescales. They are grouped into four bands:

### Micro Band (H0--H7): Sensory Processing (~6ms -- 250ms)

| Horizon | Duration (ms) | Frames | Musical Scale |
|---------|--------------|--------|---------------|
| H0 | 5.8 | 1 | Sub-neural (single frame) |
| H1 | 11.6 | 2 | Neural integration (~10ms) |
| H2 | 17.4 | 3 | Onset detection window |
| H3 | 23.2 | 4 | Phoneme boundary (~25ms) |
| H4 | 34.8 | 6 | Pitch period (~35ms) |
| H5 | 46.4 | 8 | Pitch integration (~50ms) |
| H6 | 200 | 34 | Beat subdivision (~200ms) |
| H7 | 250 | 43 | Short note (~250ms) |

**Primary consumers**: SPU (PPC mechanism, H0--H6), ASU (ASA mechanism, H3--H6), NDU (ASA mechanism, H3--H6)

### Meso Band (H8--H15): Beat/Phrase Level (~300ms -- 1.5s)

| Horizon | Duration (ms) | Frames | Musical Scale |
|---------|--------------|--------|---------------|
| H8 | 300 | 52 | Eighth note at 100 BPM |
| H9 | 350 | 60 | Quarter note at ~170 BPM |
| H10 | 400 | 69 | Quarter note at 150 BPM |
| H11 | 450 | 78 | Quarter note at ~130 BPM |
| H12 | 525 | 90 | Half note at ~115 BPM |
| H13 | 600 | 103 | Beat at 100 BPM |
| H14 | 700 | 121 | Dotted quarter at 130 BPM |
| H15 | 800 | 138 | Two beats at 150 BPM |

**Primary consumers**: STU (BEP mechanism, H6--H11), MPU (BEP mechanism, H6--H11), SPU (TPC mechanism, H6--H12)

### Macro Band (H16--H23): Section Level (~1s -- 25s)

| Horizon | Duration (ms) | Frames | Musical Scale |
|---------|--------------|--------|---------------|
| H16 | 1,000 | 172 | 1 second / 1 measure at 240 BPM |
| H17 | 1,500 | 259 | 1.5 measures at 100 BPM |
| H18 | 2,000 | 345 | 2 measures at 120 BPM |
| H19 | 3,000 | 517 | 3 measures at 120 BPM |
| H20 | 5,000 | 861 | Short phrase (5s) |
| H21 | 8,000 | 1,378 | Long phrase (8s) |
| H22 | 15,000 | 2,584 | Period/section (15s) |
| H23 | 25,000 | 4,307 | Extended section (25s) |

**Primary consumers**: ARU (AED mechanism, H6+H16; CPD mechanism, H9+H16+H18), IMU (MEM mechanism, H18--H25), PCU (C0P mechanism, H18--H20)

### Ultra Band (H24--H31): Movement/Piece Level (~36s -- 16min)

| Horizon | Duration (ms) | Frames | Musical Scale |
|---------|--------------|--------|---------------|
| H24 | 36,000 | 6,202 | Movement exposition (~36s) |
| H25 | 60,000 | 10,336 | One minute |
| H26 | 120,000 | 20,672 | Two minutes |
| H27 | 200,000 | 34,453 | Short movement (~3.3 min) |
| H28 | 414,000 | 71,319 | Standard movement (~7 min) |
| H29 | 600,000 | 103,359 | Long movement (10 min) |
| H30 | 800,000 | 137,812 | Extended form (~13 min) |
| H31 | 981,000 | 168,999 | Full piece (~16 min) |

**Primary consumers**: IMU (MEM mechanism, H25), TMH (H22), and models requiring piece-level context. Ultra horizons are the most sparsely populated.

---

## Morphological Statistics (24 Morphs)

Each morph computes a different statistical descriptor of the R3 feature within the temporal window:

| Morph | Name | Description | Category |
|-------|------|-------------|----------|
| M0 | value | Attention-weighted mean | Level |
| M1 | mean | Unweighted mean | Level |
| M2 | std | Standard deviation | Dispersion |
| M3 | median | Median value | Level |
| M4 | max | Maximum value | Level |
| M5 | range | Max minus min | Dispersion |
| M6 | skewness | Distribution asymmetry | Shape |
| M7 | kurtosis | Distribution peakedness | Shape |
| M8 | velocity | First derivative (dR3/dt) | Dynamics |
| M9 | velocity_mean | Mean velocity | Dynamics |
| M10 | velocity_std | Velocity variance (jerk proxy) | Dynamics |
| M11 | acceleration | Second derivative | Dynamics |
| M12 | acceleration_mean | Mean acceleration | Dynamics |
| M13 | acceleration_std | Acceleration variance | Dynamics |
| M14 | periodicity | Autocorrelation peak | Rhythm |
| M15 | smoothness | 1/(1+\|jerk\|/sigma) | Dynamics |
| M16 | curvature | Spectral curvature | Shape |
| M17 | shape_period | Oscillation period | Rhythm |
| M18 | trend | Linear regression slope | Dynamics |
| M19 | stability | 1/(1+var/sigma^2) | Dispersion |
| M20 | entropy | Shannon entropy | Information |
| M21 | zero_crossings | Sign change count | Dynamics |
| M22 | peaks | Local maxima count | Rhythm |
| M23 | symmetry | Forward/backward symmetry | Shape |

### Morph Category Distribution

| Category | Morphs | Count | Usage Pattern |
|----------|--------|-------|---------------|
| Level | M0, M1, M3, M4 | 4 | Universal -- used by all units |
| Dispersion | M2, M5, M19 | 3 | SPU, PCU, IMU -- variance tracking |
| Shape | M6, M7, M16, M23 | 4 | NDU, PCU -- distributional features |
| Dynamics | M8--M13, M15, M18, M21 | 9 | STU, MPU -- temporal derivatives |
| Rhythm | M14, M17, M22 | 3 | STU, MPU -- periodicity detection |
| Information | M20 | 1 | PCU, NDU -- entropy/uncertainty |

---

## Temporal Laws (3 Perspectives)

| Law | Name | Constant | Description |
|-----|------|----------|-------------|
| L0 | memory | `LAW_NAMES[0]` | Forward/causal: analyzes past -> present. Attention kernel decays from present into past. |
| L1 | prediction | `LAW_NAMES[1]` | Backward: analyzes present -> future. Attention kernel projects forward. |
| L2 | integration | `LAW_NAMES[2]` | Bidirectional: past <-> future. Symmetric attention window centered on present. |

### Law Usage by Unit

| Unit | L0 (memory) | L1 (prediction) | L2 (integration) | Primary Law |
|------|:---:|:---:|:---:|-------------|
| SPU | X | . | X | L2 -- bidirectional spectral integration |
| STU | X | X | X | L0 -- causal beat tracking |
| IMU | X | . | X | L0 -- memory retrieval is inherently causal |
| ASU | . | . | X | L2 -- salience detection is time-symmetric |
| NDU | X | X | X | L1 -- novelty requires forward prediction |
| MPU | X | X | . | L1 -- motor planning is predictive |
| PCU | X | X | X | All three -- predictive coding uses all perspectives |
| ARU | X | X | X | All three -- affective integration is multi-temporal |
| RPU | X | X | X | All three -- reward spans anticipation and consummation |

---

## Mechanism-Driven H3 Demand

Models do not declare H3 demands in isolation -- most H3 access is mediated through mechanisms. Each mechanism defines its own set of horizons:

| Mechanism | Horizons Used | Band | H3 Tuples (est.) |
|-----------|--------------|------|------------------|
| PPC | H0, H3, H6 | Micro | ~60 per model |
| TPC | H6, H12, H16 | Micro--Macro | ~45 per model |
| BEP | H6, H9, H11 | Micro--Meso | ~50 per model |
| ASA | H3, H6, H9 | Micro--Meso | ~40 per model |
| TMH | H16, H18, H20, H22 | Macro | ~80 per model |
| MEM | H18, H20, H22, H25 | Macro--Ultra | ~100 per model |
| SYN | H12, H16, H18 | Meso--Macro | ~50 per model |
| AED | H6, H16 | Micro + Macro | ~30 per model |
| CPD | H9, H16, H18 | Meso--Macro | ~40 per model |
| C0P | H18, H19, H20 | Macro | ~45 per model |

### Horizon Demand Heatmap by Mechanism

```
           H0  H3  H6  H9  H11 H12 H16 H18 H19 H20 H22 H25
          +---+---+---+---+---+---+---+---+---+---+---+---+
  PPC     | X | X | X |   |   |   |   |   |   |   |   |   |  Micro
  TPC     |   |   | X |   |   | X | X |   |   |   |   |   |  Micro-Macro
  BEP     |   |   | X | X | X |   |   |   |   |   |   |   |  Micro-Meso
  ASA     |   | X | X | X |   |   |   |   |   |   |   |   |  Micro-Meso
  TMH     |   |   |   |   |   |   | X | X |   | X | X |   |  Macro
  MEM     |   |   |   |   |   |   |   | X |   | X | X | X |  Macro-Ultra
  SYN     |   |   |   |   |   | X | X | X |   |   |   |   |  Meso-Macro
  AED     |   |   | X |   |   |   | X |   |   |   |   |   |  Micro+Macro
  CPD     |   |   |   | X |   |   | X | X |   |   |   |   |  Meso-Macro
  C0P     |   |   |   |   |   |   |   | X | X | X |   |   |  Macro
          +---+---+---+---+---+---+---+---+---+---+---+---+
```

---

## Unit-Level Temporal Demand Summary

| Unit | Models | Mechanisms | Primary Horizons | Band Focus | Est. Total Tuples |
|------|--------|-----------|-----------------|------------|-------------------|
| SPU | 9 | PPC (6), TPC (3) | H0, H3, H6, H12, H16 | Micro--Macro | ~450 |
| STU | 14 | BEP (13), TMH (4), TPC (1) | H6, H9, H11, H16, H18, H20 | Micro--Macro | ~900 |
| IMU | 15 | MEM (13), TMH (2), BEP (2), SYN (1), PPC (1) | H6, H9, H18, H20, H22, H25 | Meso--Ultra | ~1,200 |
| ASU | 9 | ASA (9) | H3, H6, H9 | Micro--Meso | ~360 |
| NDU | 9 | ASA (9), PPC (1), TMH (1), MEM (1) | H0, H3, H6, H9, H16, H18 | Micro--Macro | ~400 |
| MPU | 10 | BEP (10) | H6, H9, H11 | Micro--Meso | ~500 |
| PCU | 9 | PPC (4), TPC (3), MEM (3), AED (2), C0P (2), ASA (1) | H0, H3, H6, H16, H18, H20 | All bands | ~500 |
| ARU | 10 | AED (10), CPD (4), C0P (2), ASA (1), MEM (1) | H6, H9, H16, H18, H19, H20 | Micro--Macro | ~500 |
| RPU | 9 | AED (6), CPD (2), C0P (2), TMH (1), MEM (1), BEP (1), ASA (1) | H6, H9, H16, H18, H19, H20 | All bands | ~400 |

**Grand total estimated H3 demand (v1)**: ~5,200 tuples across all 96 models (from 112,896 theoretical space = ~4.6% occupancy).
**v2 projected total**: ~8,600 tuples (from 294,912 theoretical space = ~2.9% occupancy). See [Docs/H³/Expansion/R3v2-H3-Impact.md](../../H³/Expansion/R3v2-H3-Impact.md).

---

## Temporal Coverage by Tier

| Tier | Models | Avg. Tuples/Model | Primary Bands | Notes |
|------|--------|-------------------|---------------|-------|
| Alpha | 27 | ~60--120 | All bands | Alpha models have the most detailed H3 specifications |
| Beta | 38 | ~40--80 | Micro--Macro | Growing H3 declarations as evidence accumulates |
| Gamma | 29 | ~30--50 | Primarily through mechanisms | Gamma models mostly inherit H3 via mechanism defaults |

---

## Concrete Example: HTP (PCU-alpha1) H3 Demand

The HTP model provides the most detailed declared H3 demand in the current codebase (18 tuples):

```python
h3_demand = (
    # PPC horizons (low-level prediction, Micro band)
    (7,  0,  0, 2),   # velocity_A, H0 (6ms), value, bidirectional
    (7,  3,  0, 2),   # velocity_A, H3 (23ms), value, bidirectional
    (7,  3,  2, 2),   # velocity_A, H3 (23ms), std, bidirectional
    (10, 0,  0, 2),   # onset_strength, H0 (6ms), value, bidirectional
    (10, 1,  1, 2),   # onset_strength, H1 (12ms), mean, bidirectional
    (10, 3, 14, 2),   # onset_strength, H3 (23ms), periodicity, bidirectional

    # TPC horizons (mid-level prediction, Micro-Meso band)
    (9,  3,  0, 2),   # loudness, H3 (23ms), value, bidirectional
    (9,  4,  8, 0),   # loudness, H4 (35ms), velocity, memory
    (9,  8,  1, 0),   # loudness, H8 (300ms), mean, memory
    (21, 3,  8, 0),   # spectral_flux, H3 (23ms), velocity, memory
    (21, 4,  0, 0),   # spectral_flux, H4 (35ms), value, memory

    # MEM horizons (high-level prediction, Macro band)
    (41, 8,  0, 0),   # interaction[16], H8 (300ms), value, memory
    (41, 8,  1, 0),   # interaction[16], H8 (300ms), mean, memory
    (41, 16, 1, 0),   # interaction[16], H16 (1s), mean, memory
    (41, 16, 20, 0),  # interaction[16], H16 (1s), entropy, memory

    # Cross-level coupling
    (25, 3,  0, 2),   # cons_x_energy, H3 (23ms), value, bidirectional
    (25, 3,  2, 2),   # cons_x_energy, H3 (23ms), std, bidirectional
    (33, 4,  8, 0),   # interaction[8], H4 (35ms), velocity, memory
)
```

This demonstrates the hierarchical temporal prediction pattern: low-level features at fast horizons (H0--H3), mid-level features at moderate horizons (H3--H8), and high-level features at slow horizons (H8--H16).

---

## Architectural Observations

1. **The Micro band is the most densely populated**: Nearly all models consume H3 features at H0--H6 through their mechanisms, reflecting the frame-rate processing of the pipeline.

2. **The Macro band is the most functionally important for higher cognition**: IMU (memory), ARU (emotion), and PCU (prediction) all require multi-second temporal context.

3. **The Ultra band is the most sparsely populated**: Only IMU (via MEM at H25) and TMH (at H22) extend into piece-level timescales. This is a known limitation -- long-form musical structure processing is an active research area.

4. **Laws follow functional logic**: Memory-encoding models (IMU) prefer L0 (causal/memory), prediction models (PCU, NDU) prefer L1 (predictive), and integration models (ARU, RPU) use all three.

5. **H3 sparsity is by design**: The theoretical space (112,896 v1; 294,912 v2) is intentionally sparse. Each model requests only the tuples it needs, and the H3 engine lazily computes only demanded tuples. This keeps computation tractable.

---

## R³ v2 Expansion Impact

R³ v2 adds 79 new features [49:127] organized in 6 groups. Each creates new temporal demand targets:

| R³ Group | Features | Temporal Priority | Key H³ Horizons | Est. New Tuples |
|----------|:--------:|:-----------------:|:---------------:|:---------------:|
| F: Pitch/Chroma [49:65] | 16D | HIGH | H3-H16 (meso-macro) | ~800-1,200 |
| G: Rhythm/Groove [65:75] | 10D | HIGH | H12-H22 (meso-macro) | ~400-600 |
| H: Harmony/Tonality [75:87] | 12D | HIGH | H12-H22 (meso-macro) | ~500-800 |
| I: Information/Surprise [87:94] | 7D | MEDIUM-HIGH | H6-H22 (meso-macro) | ~300-500 |
| J: Timbre Extended [94:114] | 20D | MEDIUM | H6-H18 (meso) | ~400-700 |
| K: Modulation/Psychoacoustic [114:128] | 14D | MEDIUM | H16-H25 (macro) | ~200-400 |
| **Total new** | **79D** | | | **~2,600-4,200** |

For detailed per-group temporal analysis, see [Docs/H³/Expansion/](../../H³/Expansion/).
For per-model v2 projected expansion, see each model's Section 5.1 "R³ v2 Projected Expansion".

---

## Cross-References

- **H³ Definitive Reference**: [Docs/H³/00-INDEX.md](../../H³/00-INDEX.md) -- modular temporal architecture (73 files)
- **H³ Demand per Unit**: [Docs/H³/Demand/](../../H³/Demand/) -- per-unit H³ demand analysis
- **H³ R³ v2 Impact**: [Docs/H³/Expansion/R3v2-H3-Impact.md](../../H³/Expansion/R3v2-H3-Impact.md) -- expansion impact analysis
- **H3 Constants**: `mi_beta.core.constants` -- HORIZON_MS, MORPH_NAMES, LAW_NAMES, MORPH_SCALE
- **R3 Feature Map**: [R3-Usage.md](R3-Usage.md) -- which R3 indices are analyzed temporally
- **R³ Feature Catalog**: [Docs/R³/Registry/FeatureCatalog.md](../../R³/Registry/FeatureCatalog.md) -- all 128 features
- **Mechanism H3 Demands**: [Mechanisms/00-INDEX.md](../Mechanisms/00-INDEX.md) -- per-mechanism horizon declarations
- **Unit Docs**: [Units/](../Units/) -- model rosters with mechanism assignments
