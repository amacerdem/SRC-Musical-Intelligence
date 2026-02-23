# MPFS — Extraction

**Model**: Musical Prodigy Flow State
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_motor_automaticity | Motor automaticity level. High = beat/meter processing is effortless (basal ganglia procedural memory). Computed from beat regularity across three horizons (H6/H11/H16) × beat/meter smoothness. When regularity is high and variability is low, motor processing has become automatic — freeing cognitive resources for flow. Marion-St-Onge 2020: prodigies achieve higher automaticity. Formula: σ(0.35 × beat_regularity × mean(beat_smoothness, meter_smoothness)). |
| 1 | f02_context_mastery | Structural mastery level. High = musical structure is fully predictable. Computed from inverted context entropy × coupling stability at H14/H20. Low entropy + high stability means the performer knows exactly where in the piece they are — a prerequisite for flow's "clear goals" characteristic. Liao 2024: DMN suppression during structured improvisation. Formula: σ(0.30 × (1 − ctx_entropy) × coupling_stability). |
| 2 | f03_flow_propensity | Flow state likelihood. Core MPFS signal combining motor automaticity × context mastery × cross-feature integration. r=0.47 coefficient from prodigy-flow correlation. Marion-St-Onge 2020: F(2,43)=3.62, p=.035; prodigies M=3.8 vs early-trained M=3.3. Salimpoor 2011: caudate r=0.71 (anticipation), NAcc r=0.84 (experience). Formula: σ(0.47 × f01 × f02 × integration_mean). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 6 | M14 (periodicity) | L0 | Beat regularity at 200ms |
| 1 | 10 | 11 | M14 (periodicity) | L0 | Meter regularity at 500ms |
| 2 | 10 | 16 | M14 (periodicity) | L0 | Groove regularity at 1s |
| 3 | 11 | 6 | M15 (smoothness) | L0 | Beat smoothness |
| 4 | 11 | 11 | M15 (smoothness) | L0 | Meter smoothness |
| 5 | 7 | 16 | M3 (std) | L0 | Intensity variability (low = automatic) |
| 6 | 22 | 14 | M13 (entropy) | L0 | Context unpredictability |

---

## Computation

The E-layer extracts the three components of the flow state gateway:

1. **Motor automaticity** (f01): Multi-scale beat regularity (H6 + H11 + H16 averaged) combined with smoothness. When beat processing is highly regular and smooth across all scales, motor control has become automatic — a prerequisite for flow. Maps to SMA + basal ganglia procedural memory.

2. **Context mastery** (f02): Inverted entropy × coupling stability. Low entropy means the musical structure is predictable; high coupling stability means cross-feature relationships are consistent. Together they indicate structural mastery. Maps to auditory cortex → frontal context hierarchy.

3. **Flow propensity** (f03): The core MPFS signal. Product of automaticity × mastery × cross-feature integration, scaled by r=0.47. Only when ALL three conditions are met does flow emerge — consistent with Csikszentmihalyi's challenge-skill balance theory.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Intensity variability for automaticity |
| R³ [10] | spectral_flux | Beat regularity across three horizons |
| R³ [11] | onset_strength | Smoothness for entrainment quality |
| R³ [22] | energy_change | Context entropy at H14 |
| R³ [41] | x_l5l7 | Integration mean for flow gate |
| H³ | 7 tuples (see above) | Multi-scale features at H6/H11/H14/H16 |
