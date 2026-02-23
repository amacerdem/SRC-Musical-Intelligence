# HMCE — Temporal Integration

**Model**: Hierarchical Musical Context Encoding
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | context_depth | Integrated context depth estimate. Weighted combination of short/medium/long context levels indicating how much temporal structure the system has captured. Higher values = deeper structural comprehension. Maps to MTG→anterior temporal hierarchy. Norman-Haignere 2022: receptive field duration increases along cortical hierarchy. |
| 4 | structure_regularity | Global regularity of hierarchical structure. Measures how predictable the context hierarchy is: high = stable tonal/rhythmic framework, low = chromatic or free-form. Maps to hippocampus-cingulate circuit. Bonetti 2024: memorized sequences activate HG→Hippocampus→Cingulate chain. |
| 5 | transition_dynamics | Rate of structural change across context levels. Tracks whether the piece is in a stable section (low) or transitioning between sections (high). Uses spectral flux trend and key clarity entropy. Maps to ACC prediction error evaluation. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 60 | 8 | M18 (trend) | L0 | Tonal stability trend 500ms — context change direction |
| 1 | 60 | 16 | M18 (trend) | L0 | Tonal stability trend 1s — long-range direction |
| 2 | 51 | 8 | M1 (mean) | L0 | Mean key clarity 500ms — tonal grounding |
| 3 | 17 | 16 | M1 (mean) | L0 | Mean spectral autocorrelation 1s — long-range regularity |
| 4 | 11 | 16 | M14 (periodicity) | L0 | Onset periodicity 1s — phrase regularity |

---

## Computation

The M-layer integrates the three E-layer context levels into unified context metrics:

1. **Context depth** (idx 3): Weighted sum of f01 (25%), f02 (35%), f03 (40%). Longer contexts contribute more weight, reflecting that deeper comprehension requires accumulation. The progressive weighting mirrors the cortical hierarchy (HG→STG→MTG→anterior temporal).

2. **Structure regularity** (idx 4): Derived from tonal stability trends and key clarity. When trends are flat and key clarity is high, regularity is high. When trends are steep or key clarity entropy is high, the music is in structural flux. Maps to the hippocampal memory match signal (Bonetti 2024).

3. **Transition dynamics** (idx 5): First derivative of context depth + spectral flux trend. High values indicate the piece is moving between structural sections (key changes, phrase boundaries). Low values indicate structural stability.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Three context levels feed integration |
| R³ [51] | key_clarity | Tonal grounding for regularity |
| R³ [60] | tonal_stability | Harmonic context trends |
| H³ | 5 tuples (see above) | Multi-scale trends and periodicity for integration |
