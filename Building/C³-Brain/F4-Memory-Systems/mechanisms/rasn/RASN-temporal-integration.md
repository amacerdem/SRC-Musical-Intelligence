# RASN M-Layer — Temporal Integration (2D)

**Layer**: Mathematical / Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:neuroplasticity_index | [0, 1] | Composite plasticity metric. f(entrainment_quality x duration_proxy x complexity). neuroplasticity_idx = sigma(0.35 * beat.mean * encoding.mean + 0.35 * complexity_optimal + 0.30 * motor_entrainment.mean * stumpf). Zhao 2025: repeated entrainment promotes neuroplasticity (4 meta-analyses, n=968+). |
| 4 | M1:motor_recovery | [0, 1] | Motor recovery potential. sigma(0.40 * f10_entrainment * motor_engagement + 0.35 * beat_induction.mean * amplitude + 0.25 * ...). Wang 2022: RAS improves walking function across stroke populations (22 studies, positive gait velocity/stride). |

---

## Design Rationale

1. **Neuroplasticity Index (M0)**: Integrates entrainment quality, encoding success, and optimal complexity to produce a composite plasticity score. The key insight is that plasticity requires both stable entrainment (beat x encoding) AND moderate complexity challenge (inverted-U entropy). Too simple = no learning; too complex = no stable entrainment. Binding quality (stumpf fusion) confirms that the entrainment creates stable neural binding suitable for long-term plasticity.

2. **Motor Recovery (M1)**: Quantifies the potential for motor function improvement based on entrainment strength, motor engagement level, and beat energy. This captures the clinical evidence that RAS produces measurable gait improvements (velocity, stride length, cadence) through beat-movement coupling. The entrainment-motor pathway runs through SMA and cerebellum.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (23, 11, 0, 2) | entropy value H11 L2 | Current complexity at 500ms |
| (23, 16, 1, 0) | entropy mean H16 L0 | Average complexity over 1s |
| (23, 20, 1, 0) | entropy mean H20 L0 | Complexity over 5s consolidation |
| (23, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s |
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at 1s |
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding over consolidation window |
| (3, 24, 1, 0) | stumpf_fusion mean H24 L0 | Long-term binding context |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [3] | stumpf_fusion | Binding quality for plasticity integration |
| [23] | entropy | Complexity for inverted-U plasticity demand |
| [7] | amplitude | Beat energy for motor recovery |

---

## Scientific Foundation

- **Zhao 2025**: Systematic review, 968+ patients, 4 meta-analyses — RAS promotes neuroplasticity through entrainment and sensorimotor integration
- **Wang 2022**: Meta-analysis, 22 studies — RAS improves walking function (gait velocity, stride) across neurological conditions
- **Ghai & Ghai 2019**: Systematic review, 968 patients — RAS improves gait parameters in neurological conditions
- **Blasi et al. 2025**: 20 RCTs N=718, hippocampal volume increases, GMV changes, WM integrity improvements

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/rasn/temporal_integration.py`
