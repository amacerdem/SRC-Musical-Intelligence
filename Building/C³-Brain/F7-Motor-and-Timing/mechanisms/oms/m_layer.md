# OMS — Temporal Integration

**Model**: Oscillatory Motor Synchronization
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | sync_quality | Overall synchronization quality. Geometric mean of the three network signals — all three must contribute for synchronization to succeed. If any network fails, overall sync collapses. Formula: (f01 × f02 × f03) ^ (1/3). Maps to the hierarchical organization where fronto-striatal, temporo-parietal, and limbic networks must all operate. |
| 4 | hierarchical_coordination | Hierarchical coordination strength. Weighted mean emphasizing higher-level networks: (1×f01 + 2×f02 + 3×f03) / 6. Interpersonal synchronization (f03) is weighted highest because bar-level ensemble coordination subsumes beat-level and motor-level processing. Hoddinott & Grahn 2024: C-Score model in SMA/putamen encodes beat strength continuously. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 11 | M1 (mean) | L0 | Mean loudness over motor window |
| 1 | 22 | 11 | M14 (periodicity) | L2 | Intensity regularity |
| 2 | 25 | 11 | M0 (value) | L2 | Predictive coupling signal |
| 3 | 33 | 11 | M0 (value) | L2 | Sensorimotor coupling signal |
| 4 | 33 | 11 | M17 (peaks) | L0 | Sensorimotor peak events |

---

## Computation

The M-layer integrates the three E-layer network signals into unified synchronization metrics:

1. **Sync quality** (idx 3): Geometric mean ensures all three networks must contribute — a single failing network drives sync_quality toward zero. This reflects the neuroscience finding that orchestral synchronization requires coordinated operation across fronto-striatal, temporo-parietal, and limbic pathways.

2. **Hierarchical coordination** (idx 4): Weighted mean where interpersonal (×3) > sensorimotor (×2) > predictive (×1). Higher-level coordination subsumes lower levels, reflecting the hierarchical timescale organization: H6 (beat) → H11 (motor) → H16 (bar/ensemble).

Both outputs are bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Three network signals for integration |
| R³ [8] | loudness | Mean intensity over motor window |
| R³ [22] | energy_change | Periodicity for rhythmic regularity |
| R³ [25] | x_l0l5 | Predictive coupling at motor scale |
| R³ [33] | x_l4l5 | Sensorimotor coupling and peak events |
| H³ | 5 tuples (see above) | Motor-level features at H11 (500ms) |
