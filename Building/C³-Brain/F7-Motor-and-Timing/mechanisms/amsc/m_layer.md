# AMSC — Temporal Integration

**Model**: Auditory-Motor Stream Coupling
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | gamma_power | High-gamma band power proxy. Aggregated measure of beat-level intensity tracking through the pSTG gamma system. Represents the overall strength of auditory encoding driving motor coupling. Maps to pSTG 70-170 Hz activity. |
| 5 | coupling_strength | Cross-correlation strength at 110ms delay. Computed from x_l0l5 coupling signal × energy periodicity at H11 (500ms). Represents the quality of the dorsal auditory stream pathway from pSTG to premotor cortex. Potes 2012: r = 0.70 coupling. Edagawa 2017: beta PSI frontal-temporal z=7.43. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 11 | M1 (mean) | L0 | Mean loudness over motor window — sustained intensity |
| 1 | 22 | 11 | M14 (periodicity) | L2 | Energy periodicity — accent regularity at motor scale |
| 2 | 25 | 11 | M0 (value) | L2 | x_l0l5 coupling signal — auditory-motor binding |
| 3 | 25 | 11 | M15 (smoothness) | L0 | x_l0l5 smoothness — coupling quality |
| 4 | 33 | 11 | M0 (value) | L2 | x_l4l5 dynamics coupling — motor binding signal |

---

## Computation

The M-layer integrates E-layer auditory-motor signals into unified coupling metrics:

1. **Gamma power** (idx 4): Aggregated high-gamma band power from beat induction level. Represents the overall strength of the pSTG intensity-tracking system that drives the entire auditory-motor coupling cascade.

2. **Coupling strength** (idx 5): Cross-correlation strength at the 110ms auditory-motor delay. Computed from x_l0l5 (foundation × perceptual) coupling signal multiplied by energy periodicity at the motor window (H11 = 500ms). When both signals are strong, the dorsal auditory stream pathway is operating efficiently. Formula: σ(x_coupling × periodicity).

Both outputs are bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03, f04 | Auditory-motor gamma signals for power computation |
| R³ [8] | loudness | Sustained intensity at motor window |
| R³ [22] | energy_change | Periodicity for accent regularity |
| R³ [25] | x_l0l5 | Auditory-motor coupling signal and smoothness |
| R³ [33] | x_l4l5 | Dynamics coupling — motor binding |
| H³ | 5 tuples (see above) | Motor-window features at H11 (500ms) |
