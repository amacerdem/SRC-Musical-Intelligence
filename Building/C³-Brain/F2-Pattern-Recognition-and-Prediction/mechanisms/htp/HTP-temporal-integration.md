# HTP M-Layer — Temporal Integration (3D)

**Layer**: Memory (M)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | M0:latency_high | [0, 1] | Normalized 500ms lead time. sigma(0.50*E0 + 0.50*tonal_stability_mean_1s). Golesorkhi 2021: longer timescales in higher-level (DMN/FPN) regions. |
| 5 | M1:latency_mid | [0, 1] | Normalized 200ms lead time. sigma(0.50*E1 + 0.50*sharpness_mean_500ms). Belt cortex integration window. |
| 6 | M2:latency_low | [0, 1] | Normalized 110ms lead time. sigma(0.50*E2 + 0.50*onset_mean_50ms). Forseth 2020: HG timing prediction via low-freq phase. |

---

## Design Rationale

Each latency integrates the E-layer prediction lead with its corresponding sustained feature. Higher values indicate stronger prediction at that hierarchy level.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (60, 16, 1, 0) | tonal_stability mean H16 L0 | 1s context (reused) |
| (13, 8, 1, 0) | sharpness mean H8 L0 | 500ms context (reused) |
| (11, 1, 1, 2) | onset_strength mean H1 L2 | 50ms onset detection |

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/htp/temporal_integration.py`
