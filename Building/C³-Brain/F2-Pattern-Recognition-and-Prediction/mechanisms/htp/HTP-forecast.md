# HTP F-Layer — Forecast (2D)

**Layer**: Forecast (F)
**Indices**: [10:12]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 10 | F0:abstract_future_500ms | [0, 1] | High-level structural prediction. sigma(0.50*E0 + 0.50*tonal_stability_mean_1s). Cheung 2019: amygdala/hippocampus integrate uncertainty x surprise. |
| 11 | F1:midlevel_future_200ms | [0, 1] | Mid-level feature prediction. sigma(0.50*E1 + 0.50*sharpness_velocity_125ms). Belt cortex extrapolation. |

---

## Design Rationale

Forward predictions serve two purposes:
1. **abstract_future**: Feeds prediction_hierarchy.predict() as context. Also feeds F4 (Memory) autobiographical retrieval and F8 (Learning) statistical model.
2. **midlevel_future**: Feeds F7 (Motor) period_entrainment as context for rhythmic prediction.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (60, 16, 1, 0) | tonal_stability mean H16 L0 | 1s context (reused) |
| (13, 4, 8, 0) | sharpness velocity H4 L0 | Brightness dynamics (reused) |

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/htp/forecast.py`
