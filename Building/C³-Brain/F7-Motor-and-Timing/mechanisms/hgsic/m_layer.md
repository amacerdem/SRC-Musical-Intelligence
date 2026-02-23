# HGSIC — Temporal Integration

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | groove_index | Integrated groove state index. Weighted hierarchical combination of beat, meter, and motor groove levels: (1×f01 + 2×f02 + 3×f03) / 6. Progressive weighting emphasizes motor-level groove (f03) over beat-level (f01), reflecting that groove perception requires hierarchical integration across timescales. Maps to the full pSTG → premotor → motor cortex cascade. |
| 4 | coupling_strength | Auditory-motor coupling strength at 110ms delay. Measures the quality of the dorsal stream pathway from pSTG to motor cortex. Computed from amplitude smoothness × energy periodicity at bar level (H16). Potes 2012: cross-correlation r = 0.70 at 110ms lag. Formula: σ(0.50 × amp_smooth × energy_period). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 22 | 11 | M1 (mean) | L0 | Mean energy dynamics over motor window |
| 1 | 22 | 11 | M14 (periodicity) | L2 | Accent regularity — energy periodicity |
| 2 | 21 | 11 | M1 (mean) | L0 | Mean spectral dynamics |
| 3 | 8 | 11 | M1 (mean) | L0 | Mean loudness over motor window |

---

## Computation

The M-layer integrates the three E-layer groove hierarchy levels into unified groove metrics:

1. **Groove index** (idx 3): Weighted hierarchical combination: (1×f01 + 2×f02 + 3×f03) / 6. The progressive weighting (motor groove 3× beat gamma) reflects that groove emerges from full hierarchical integration. A strong beat alone (high f01, low f02/f03) produces low groove; full hierarchical activation produces maximum groove.

2. **Coupling strength** (idx 4): Auditory-motor pathway quality measured by amplitude smoothness and energy periodicity at bar level. When intensity patterns are smooth and periodic at the bar timescale, the dorsal stream coupling is strong. Maps to the 110ms delay pathway (Potes 2012).

Both outputs are bounded to [0, 1]. Groove index uses arithmetic bounding; coupling strength uses sigmoid.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Three groove hierarchy levels feed integration |
| R³ [8] | loudness | Mean loudness for coupling assessment |
| R³ [21] | spectral_change | Spectral dynamics for motor window integration |
| R³ [22] | energy_change | Energy dynamics and periodicity for accent regularity |
| H³ | 4 tuples (see above) | Motor-window integration features at H11 (500ms) |
