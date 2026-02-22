# MEAMR — Cognitive Present

**Model**: Music-Evoked Autobiographical Memory Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | memory_activation_state | Current autobiographical memory activation level. σ(0.5 * f02 + 0.5 * f01). Integrates familiarity and autobiographical salience into a single memory activation signal. Janata 2009: dMPFC activation proportional to autobiographical salience (P < 0.001); familiarity is prerequisite for memory activation. High values indicate strong autobiographical memory retrieval in progress. τ_decay = 10.0s reflects the extended nature of memory retrieval. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 16 | M18 (trend) | L2 (bidi) | Pleasantness trend 1s — via f01 recognition ramp |
| 1 | 12 | 16 | M1 (mean) | L2 (bidi) | Mean warmth 1s — via f01 timbral familiarity |
| 2 | 41 | 16 | M18 (trend) | L2 (bidi) | Memory-structure trend 1s — via f02 autobio buildup |

---

## Computation

The P-layer collapses the 4D extraction space into a single real-time memory activation signal. It combines familiarity (f01) and autobiographical salience (f02) with equal weighting.

The balanced 0.5/0.5 combination ensures music must be both familiar AND autobiographically salient for strong memory activation — either alone produces only moderate activation. This mirrors the dMPFC response pattern where activation requires both familiarity and autobiographical relevance (Janata 2009).

The memory activation signal has a long sustain (τ_decay = 10.0s) reflecting the extended nature of autobiographical memory retrieval, which unfolds over seconds. This feeds downstream to:
- The kernel for familiarity modulation
- IMU for memory consolidation (encoding_strength)
- RPEM for familiarity-modulated prediction error

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f01_familiarity_index | Familiarity component for memory activation |
| E-layer [1] | f02_autobio_salience | Autobiographical salience component |
| R³ [4] | sensory_pleasantness | Recognition cue (via f01) |
| R³ [12] | warmth | Timbral familiarity (via f01) |
| R³ [41:49] | x_l5l6 | Memory-structure binding (via f02) |
| Janata 2009 | dMPFC requires familiarity + autobio | FDR P < 0.025 (fMRI, N = 13) |
| Salimpoor 2011 | DA release during familiar music | r = 0.71 (PET, N = 8) |
