# ONI — Temporal Integration

**Model**: Over-Normalization in Intervention
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | dosage_accumulation | Cumulative intervention exposure. EMA of f03_attention_enhancement over session timescale, tracking the accumulated effect of musical intervention. Higher values indicate more sustained exposure. Range [0, 1]. |
| 5 | preterm_baseline | Starting point reference. Pitch-processing baseline strength proxy derived from onset strength and spectral flux at the alpha timescale. Represents the infant's auditory processing capacity before intervention begins. Edalati 2023: preterm neonates (32+/-2.6 wGA) show beat frequency responses above noise floor, establishing a measurable baseline. Range [0, 1]. |
| 6 | fullterm_reference | Normalization target. External reference constant representing typical full-term MMR amplitude. This serves as the denominator in the over-normalization ratio (f01). When intervention response exceeds this reference, over-normalization is occurring. Partanen 2022: intervention group exceeded full-term control norms. Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 4 | M8 (velocity) | L0 (fwd) | Spectral velocity at 125ms theta for processing rate |
| 1 | 33 | 3 | M0 (value) | L2 (bidi) | Dynamic-percept coupling at 100ms alpha |
| 2 | 33 | 3 | M2 (std) | L2 (bidi) | Coupling variability at 100ms alpha |
| 3 | 33 | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s beat |

---

## Computation

The M-layer integrates the temporal dynamics of intervention-driven over-normalization across three dimensions:

1. **Dosage accumulation** (idx 4): Tracks cumulative musical intervention exposure using an exponential moving average of the E-layer's attention enhancement signal. This captures the progressive buildup of intervention effects over time. The EMA formulation reflects the observation that both recent and historical exposure contribute to the over-normalization effect, with recent sessions weighted more heavily.

2. **Preterm baseline** (idx 5): Establishes the starting auditory processing capacity of the preterm infant. Computed from onset strength and spectral flux dynamics at the 100ms alpha timescale. Edalati 2023 demonstrated that preterm neonates at 32 weeks GA already show beat frequency responses above noise floor, confirming that a measurable auditory processing baseline exists even in the preterm period. Saadatmehr 2024 further showed that this baseline matures progressively with age (phase-age correlation Rc=0.47, p=0.007).

3. **Full-term reference** (idx 6): Provides the normalization target against which over-normalization is measured. This is modeled as a relatively stable reference derived from dynamic-percept coupling at the 1s timescale. In the ONI framework, this reference represents what "normal" full-term auditory processing looks like, and the over-normalization finding is defined by the intervention group exceeding this reference.

The M-layer provides the temporal context that enables the P-layer to assess current MMR strength relative to both baseline and reference, and the F-layer to predict long-term developmental trajectories.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [21] | spectral_change | Spectral processing rate for baseline estimation |
| R3 [33] | x_l4l5[0] | Dynamic-percept coupling for reference and variability |
| H3 | 4 tuples (see above) | Multi-scale coupling and spectral velocity dynamics |
| E-layer | f03_attention_enhancement | Input signal for dosage accumulation EMA |
