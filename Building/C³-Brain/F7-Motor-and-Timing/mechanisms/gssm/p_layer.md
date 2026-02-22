# GSSM — Cognitive Present

**Model**: Gait-Synchronized Stimulation Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | phase_lock_strength | Current gait-phase lock activity. Measures how strongly the gait cycle is currently locked to the stimulation rhythm. Higher values indicate tighter phase alignment between heel strike and stimulation trigger. Grahn & Brett 2007: putamen Z=5.67 for beat period locking; SMA Z=5.03 for sequence timing. |
| 8 | variability_level | Current stride variability. Instantaneous assessment of stride-to-stride timing variability. Lower variability (higher regularity) reflects successful therapeutic intervention. Yamashita 2025: stride time CV as primary outcome measure; CV stance time correlates with Mini-BESTest (r = 0.62). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s — lock disruptions |
| 1 | 22 | 8 | M8 (velocity) | L0 (fwd) | Energy dynamics 500ms — gait energy fluctuation |

---

## Computation

The P-layer assesses the real-time state of gait-synchronized stimulation at the current moment:

1. **Phase lock strength** (idx 7): Evaluates the instantaneous quality of gait-stimulation phase alignment. Incorporates coupling phase resets at 1s (zero_crossings) as a negative indicator — more phase resets indicate weaker phase lock, meaning the gait cycle is drifting out of sync with stimulation. This maps to the real-time monitoring in Yamashita 2025 where stimulation was continuously phase-locked to heel strike detected by pressure sensors. The putamen (Grahn & Brett 2007: Z=5.67) and SMA (Z=5.03) underlie this gait rhythm generation and sequencing.

2. **Variability level** (idx 8): Tracks instantaneous stride variability using energy dynamics at 500ms (half-stride interval). Energy velocity captures the rate of change in gait energy — higher velocity indicates more variable gait. This dimension directly inherits from stride_cv (M-layer) but provides a present-moment snapshot. Yamashita 2025 measured CV from 20 stride steps; this provides a frame-by-frame continuous version.

Both outputs are sigmoid-bounded to [0, 1] and represent instantaneous present-state assessments.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer | stride_cv | Stride variability feeds present-state variability assessment |
| R³ [22] | energy_change | Energy dynamics for gait energy fluctuation tracking |
| R³ [25:33] | x_l0l5 | Coupling phase resets for lock disruption detection |
| H³ | 2 tuples (see above) | Phase resets and energy velocity for present-state evaluation |
