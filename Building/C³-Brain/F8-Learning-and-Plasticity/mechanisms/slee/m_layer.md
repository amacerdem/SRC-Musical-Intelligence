# SLEE — Temporal Integration

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | exposure_model | Statistical model building over time. Tracks the accumulation of the internal distribution representation through exponential moving average of f01 over session timescale. Reflects how repeated exposure to statistical regularities builds a robust model (Bridwell 2017: cortical sensitivity to guitar note patterns at 4 Hz). |
| 5 | pattern_memory | Pattern accumulation over time. Tracks the build-up of pitch stability patterns through EMA with tau = 3s, reflecting the persistence of learned statistical regularities in working memory. Billig 2022: hippocampus supports sequence binding and statistical learning memory. |
| 6 | expertise_state | Long-term expertise consolidation. Uses the pattern binding trend over 1s as a training proxy, reflecting how expertise-level specialization develops through sustained engagement with statistical patterns. Doelling & Poeppel 2015: years of training correlate with entrainment strength (PLV). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 24 | 3 | M0 (value) | L2 (bidi) | Pitch stability 100ms for pattern memory |
| 1 | 24 | 16 | M2 (std) | L2 (bidi) | Stability variability 1s for memory dynamics |
| 2 | 33 | 16 | M18 (trend) | L0 (fwd) | Pattern binding trend over 1s for expertise state |

---

## Computation

The M-layer tracks temporal dynamics of statistical learning across three timescales: session-level model building, working-memory pattern accumulation, and long-term expertise consolidation.

1. **exposure_model**: Exponential moving average of f01 (statistical model) over the session timescale. This captures how the internal distribution representation strengthens with repeated exposure, reflecting the cortical sensitivity buildup observed by Bridwell 2017.

2. **pattern_memory**: EMA of pitch stability with tau = 3s. This integrates pitch stability at 100ms with its variability over 1s to estimate how reliably the system retains learned patterns. The hippocampal sequence binding mechanism (Billig 2022) supports this working-memory timescale.

3. **expertise_state**: Uses the pattern binding trend over 1s (H³ tuple: x_l4l5[0], H16, M18, L0) as a direct proxy for expertise consolidation. Increasing trend indicates specialization deepening; stable trend indicates plateau.

The M-layer dimensions accumulate over time, providing the temporal context that distinguishes brief exposure from sustained expertise.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Statistical model strength | Input to exposure_model EMA |
| R³[24] pitch_stability | Pitch regularity | Statistical baseline for pattern memory |
| R³[33:41] x_l4l5 | Pattern-feature binding | Binding trend as expertise proxy |
| H³ (3 tuples) | Multi-scale temporal morphology | Stability dynamics and binding trend at 100ms-1s |
