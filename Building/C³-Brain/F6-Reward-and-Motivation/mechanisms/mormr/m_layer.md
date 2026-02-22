# MORMR — Temporal Integration

**Model**: mu-Opioid Receptor Music Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | opioid_tone | Overall opioid system tone. σ(0.5 * f01 + 0.5 * f02). Represents the integrated state of the endogenous opioid system — a weighted average of opioid release magnitude and chills frequency. High opioid tone indicates sustained opioid-mediated pleasure. Putkinen 2025: baseline MOR availability modulates the strength of pleasure-BOLD coupling across brain regions. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — instantaneous intensity |
| 1 | 8 | 8 | M1 (mean) | L2 (bidi) | Mean loudness at 500ms — medium-term intensity |
| 2 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness at 1s — sustained intensity context |
| 3 | 0 | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms — instantaneous consonance |
| 4 | 4 | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms — instantaneous hedonic |

---

## Computation

The M-layer computes a single integrated opioid tone signal:

```
opioid_tone = σ(0.5 * f01_opioid_release + 0.5 * f02_chills_count)
```

This represents the overall state of the endogenous opioid system during music listening. Unlike DAED's M-layer which computes a dissociation (difference), MORMR's M-layer computes an integration (average). This reflects the pharmacological reality: while dopamine has fast, phasic release patterns (DAED), the opioid system operates on a slower, more tonic timescale.

The opioid tone captures:
- **Tonic component** (from f01): Sustained MOR activation from consonant, warm, pleasant music
- **Phasic component** (from f02): Burst MOR activation during chills/frisson events

The sigmoid ensures the output remains in [0,1]. The equal weighting (0.5/0.5) reflects the finding that both sustained pleasure and peak chills events contribute to overall opioid engagement.

The M-layer H³ demands provide the multi-scale loudness, roughness, and pleasantness context that feeds the upstream E-layer computations.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_opioid_release | Tonic opioid component |
| E-layer | f02_chills_count | Phasic opioid component (chills) |
| H³ | 5 tuples (see above) | Multi-scale temporal context for E-layer |
