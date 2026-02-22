# CDMR — Cognitive Present

**Model**: Context-Dependent Mismatch Response
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | mismatch_signal | Current expectation violation. Real-time mismatch detection combining instantaneous deviance with context-modulated sensitivity. The core MMN-like signal that reflects the discrepancy between predicted and observed acoustic input. Rupp/Hansen 2022: context-dependent MMR in musicians at MEG. Crespo-Bojorque 2018: consonance condition MMN at 172-250ms, dissonance condition late MMN at 232-314ms. |
| 7 | context_state | Current context integration level. Reflects the complexity and richness of the current melodic context that gates expertise-dependent mismatch enhancement. High values indicate complex melodic context where expertise effects emerge. Rupp/Hansen 2022: musicians = non-musicians in oddball (low context) but musicians > non-musicians in melodic (high context). |
| 8 | binding_state | Multi-feature integration state. Degree of cross-feature binding that produces subadditive responses. Reflects the integration of multiple deviant dimensions (pitch, timbre, intensity) into a unified mismatch representation. Maps to fronto-central distribution (Crespo-Bojorque 2018: Fz). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 12 | 13 | 3 | M0 (value) | L2 (bidi) | Tonal context at 100ms |
| 13 | 13 | 3 | M20 (entropy) | L2 (bidi) | Tonal entropy at 100ms |
| 14 | 33 | 3 | M0 (value) | L2 (bidi) | Pattern coupling at 100ms |

---

## Computation

The P-layer computes the real-time cognitive state of mismatch processing:

1. **Mismatch signal** (idx 6): Combines E-layer mismatch amplitude (f01) with M-layer melodic expectation to produce a context-sensitive violation signal. When melodic expectation is strong (rich context), the mismatch signal is amplified for experts. When expectation is weak (simple oddball), the signal reflects only basic deviance detection without expertise modulation. The brightness entropy at 100ms provides a tonal context quality measure that further gates the signal.

2. **Context state** (idx 7): Real-time assessment of melodic context richness computed from context modulation (f02), melodic expectation (M-layer), and tonal context features (brightness at 100ms). This serves as the gate that determines whether expertise effects are expressed — the key finding of Rupp/Hansen 2022. Low context_state (simple sequences) yields no expertise advantage; high context_state (complex melodies) enables expertise-dependent enhancement.

3. **Binding state** (idx 8): Reflects the current degree of multi-feature integration from subadditivity index (f03) and pattern coupling (x_l4l5 at 100ms). High binding indicates that multiple deviant features are being processed as an integrated whole rather than independently. This subadditive integration is the hallmark of expert auditory processing. Maps to the interaction of IFG and auditory cortex generators.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_mismatch_amplitude | Base deviance signal for mismatch computation |
| E-layer | f02_context_modulation | Context complexity for state assessment |
| E-layer | f03_subadditivity_index | Integration level for binding state |
| M-layer | melodic_expectation | Accumulated context for sensitivity modulation |
| R³ [13] | brightness | Tonal context quality |
| R³ [33:41] | x_l4l5 | Pattern-feature coupling for binding computation |
| H³ | 3 tuples (see above) | Tonal context, entropy, and pattern coupling at 100ms |
