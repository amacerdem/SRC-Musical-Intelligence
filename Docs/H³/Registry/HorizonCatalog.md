# H3 Registry -- Horizon Catalog

**Version**: 2.0.0
**Count**: 32 horizons (H0-H31) across 4 bands
**Frame rate**: 172.27 Hz (5.804 ms/frame)
**Code reference**: `mi_beta.core.constants.HORIZON_MS`
**Updated**: 2026-02-13

---

## Complete Horizon Table

| Index | Duration (ms) | Frames | Band | Musical Scale | BPM Equivalent | Primary Mechanisms | Primary Units |
|:-----:|--------------:|-------:|------|---------------|:--------------:|-------------------|---------------|
| H0 | 5.8 | 1 | Micro | Sub-neural | -- | PPC | SPU |
| H1 | 11.6 | 2 | Micro | Neural integration | -- | PPC | SPU |
| H2 | 17.4 | 3 | Micro | Onset detection | -- | PPC | SPU |
| H3 | 23.2 | 4 | Micro | Phoneme boundary | -- | PPC, ASA | SPU, ASU, NDU |
| H4 | 34.8 | 6 | Micro | Pitch period | -- | PPC | SPU |
| H5 | 46.4 | 8 | Micro | Pitch integration | -- | PPC | SPU |
| H6 | 200 | 34 | Micro | Beat subdivision | 300 | PPC, TPC, BEP, ASA, AED | SPU, STU, MPU, ASU, PCU, ARU |
| H7 | 250 | 43 | Micro | Short note | 240 | -- | -- |
| H8 | 300 | 52 | Meso | Eighth note @100BPM | 200 | -- | -- |
| H9 | 350 | 60 | Meso | Quarter @170BPM | 171 | BEP, ASA, CPD | MPU, ASU, NDU, ARU, RPU |
| H10 | 400 | 69 | Meso | Quarter @150BPM | 150 | -- | -- |
| H11 | 450 | 78 | Meso | Quarter @130BPM | 133 | BEP | MPU, STU |
| H12 | 525 | 90 | Meso | Half note @115BPM | 114 | TPC, SYN | SPU, STU, IMU |
| H13 | 600 | 103 | Meso | Beat @100BPM | 100 | -- | -- |
| H14 | 700 | 121 | Meso | Dotted quarter @130BPM | 86 | -- | -- |
| H15 | 800 | 138 | Meso | Two beats @150BPM | 75 | -- | -- |
| H16 | 1,000 | 172 | Macro | 1 measure @240BPM | 60 | TPC, TMH, AED, CPD, SYN | SPU, STU, IMU, PCU, ARU, RPU |
| H17 | 1,500 | 259 | Macro | 1.5 measures @100BPM | 40 | -- | -- |
| H18 | 2,000 | 345 | Macro | 2 measures @120BPM | 30 | TMH, MEM, CPD, C0P, SYN | STU, IMU, ARU, PCU, RPU |
| H19 | 3,000 | 517 | Macro | 3 measures @120BPM | 20 | C0P | PCU, ARU |
| H20 | 5,000 | 861 | Macro | Short phrase (5s) | 12 | TMH, MEM, C0P | STU, IMU, PCU |
| H21 | 8,000 | 1,378 | Macro | Long phrase (8s) | 7.5 | TMH | STU |
| H22 | 15,000 | 2,584 | Macro | Period/section (15s) | 4 | TMH, MEM | STU, IMU |
| H23 | 25,000 | 4,307 | Macro | Extended section (25s) | 2.4 | -- | -- |
| H24 | 36,000 | 6,202 | Ultra | Movement exposition | 1.7 | -- | -- |
| H25 | 60,000 | 10,336 | Ultra | One minute | 1 | MEM | IMU |
| H26 | 120,000 | 20,672 | Ultra | Two minutes | 0.5 | -- | -- |
| H27 | 200,000 | 34,453 | Ultra | Short movement | 0.3 | -- | -- |
| H28 | 414,000 | 71,319 | Ultra | Standard movement | 0.14 | -- | -- |
| H29 | 600,000 | 103,359 | Ultra | Long movement | 0.1 | -- | -- |
| H30 | 800,000 | 137,812 | Ultra | Extended form | 0.075 | -- | -- |
| H31 | 981,000 | 168,999 | Ultra | Full piece | 0.061 | -- | -- |

**Frame calculation**: `frames = ceil(duration_ms / 5.804)` where 5.804 ms = 1/172.27 Hz

---

## Band Summary

| Band | Horizons | Duration Range | Frame Range | Count | Musical Domain | Primary Use |
|------|----------|---------------:|----------:|:-----:|----------------|-------------|
| **Micro** | H0-H7 | 5.8ms - 250ms | 1 - 43 | 8 | Onset, attack, transient, short note | PPC, ASA, low-level feature tracking |
| **Meso** | H8-H15 | 300ms - 800ms | 52 - 138 | 8 | Beat period, quarter note, motif | BEP, TPC, SYN, rhythmic analysis |
| **Macro** | H16-H23 | 1s - 25s | 172 - 4,307 | 8 | Measure, phrase, section, passage | TMH, MEM, C0P, AED, CPD, structural analysis |
| **Ultra** | H24-H31 | 36s - 981s | 6,202 - 168,999 | 8 | Movement, piece, full work | MEM (sparse), long-term memory |

### Band Design Rationale

- **Micro**: Captures sub-beat phenomena. H0-H5 are sub-50ms for neural-level timing; H6-H7 bridge to beat subdivision. Densely sampled because onset/attack features change rapidly.
- **Meso**: Captures beat-level structure. Logarithmically spaced from 300ms to 800ms to cover the musically relevant beat period range (~60-200 BPM). Core band for rhythm processing.
- **Macro**: Captures phrase and section structure. Spans 1s to 25s, covering musical measures through extended sections. Primary band for tonal memory and structural analysis.
- **Ultra**: Captures movement and piece-level structure. Sparsely used (only MEM at H25 has confirmed demand). Enables whole-piece memory and form tracking.

---

## Neuroscience Correspondence

The horizon bands are designed to correspond to neural oscillation bands involved in auditory temporal processing:

| H3 Band | Neural Oscillation | Frequency Range | Temporal Scale | Function |
|---------|-------------------|----------------|---------------|----------|
| Micro (H0-H5) | Gamma | 30-150 Hz | 7-33 ms | Fine temporal structure, onset binding |
| Micro (H6-H7) | Beta | 13-30 Hz | 33-77 ms | Sensorimotor coupling, beat prediction |
| Meso (H8-H15) | Alpha/Theta | 4-13 Hz | 77-250 ms | Rhythmic attending, beat entrainment |
| Macro (H16-H23) | Theta/Delta | 0.5-4 Hz | 250ms-2s | Phrase segmentation, tonal working memory |
| Ultra (H24-H31) | Infra-slow | <0.5 Hz | >2s | Long-term memory consolidation, form |

### Key References
- Large & Jones (1999): Dynamic Attending Theory -- oscillatory attention at multiple timescales
- Giraud & Poeppel (2012): Cortical oscillations and speech processing
- Koelsch (2011): Toward a neural basis of music perception

---

## Mechanism-to-Horizon Mapping

Each mechanism operates at specific horizon ranges reflecting its temporal scope:

| Mechanism | Primary Horizons | Band Coverage | Description |
|-----------|-----------------|---------------|-------------|
| **PPC** (Pitch Period Computer) | H0, H3, H6 | Micro | Pitch period estimation from autocorrelation |
| **TPC** (Tonal Pitch Class) | H6, H12, H16 | Micro-Macro | Chroma and tonal center tracking |
| **BEP** (Beat Period) | H6, H9, H11 | Micro-Meso | Beat period estimation and tracking |
| **ASA** (Auditory Scene Analysis) | H3, H6, H9 | Micro-Meso | Stream segregation and grouping |
| **TMH** (Tonal Memory Hierarchy) | H16, H18, H20, H22 | Macro | Hierarchical tonal memory |
| **MEM** (Long-term Memory) | H18, H20, H22, H25 | Macro-Ultra | Long-term musical memory |
| **SYN** (Syntactic Processing) | H12, H16, H18 | Meso-Macro | Musical syntax and expectation |
| **AED** (Acoustic Event Detection) | H6, H16 | Micro+Macro | Event boundary detection |
| **CPD** (Change Point Detection) | H9, H16, H18 | Meso-Macro | Structural change detection |
| **C0P** (Context Operator) | H18, H19, H20 | Macro | Contextual integration over phrases |

---

## Horizon Spacing Visualization

```
Micro     |==|==|==|==|===|====|===========|=============|
          H0 H1 H2 H3 H4  H5   H6          H7

Meso      |======|=======|========|=========|==========|===========|============|=============|
          H8     H9      H10     H11       H12        H13         H14          H15

Macro     |==========|===============|===============|======================|
          H16        H17             H18             H19
          |====================================|
          H20
          |========================================================|
          H21
          |=================================================================================|
          H22                                                                              H23

Ultra     H24 ... H25 ... H26 ... H27 ... H28 ... H29 ... H30 ... H31
          36s     60s     2m      3.3m    6.9m    10m     13.3m   16.4m
```

**Note**: Spacing is approximately logarithmic within each band, reflecting the Weber-Fechner law of temporal perception (JND for duration is approximately proportional to duration).

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry index**: [../Registry/00-INDEX.md](00-INDEX.md)
