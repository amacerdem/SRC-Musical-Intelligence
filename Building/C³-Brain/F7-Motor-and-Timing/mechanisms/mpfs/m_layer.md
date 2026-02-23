# MPFS — Temporal Integration

**Model**: Musical Prodigy Flow State
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | challenge_skill_balance | Challenge-skill balance index (Csikszentmihalyi 1990). Flow occurs when challenge ≈ skill. Challenge = musical complexity (entropy + pitch variability); Skill = (automaticity + mastery) / 2. Value of 1 = perfect balance (flow gateway); 0 = extreme mismatch (anxiety or boredom). Formula: 1 − |challenge − skill|, where challenge = σ(0.50 × ctx_entropy + 0.50 × pitch_var) and skill = (f01 + f02) / 2. |
| 4 | hypofrontality_proxy | DLPFC deactivation proxy. Transient hypofrontality (Dietrich 2004): when both motor automaticity and context mastery are high, executive control is unnecessary and DLPFC deactivates — enabling the loss of self-consciousness characteristic of flow. Limb & Braun 2008: DLPFC deactivation during jazz improvisation; Liao 2024: DMN suppression during structured improvisation. Formula: f01 × f02. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 23 | 14 | M1 (mean) | L0 | Melodic contour rate |
| 1 | 23 | 20 | M3 (std) | L0 | Long-range pitch variability |
| 2 | 21 | 8 | M1 (mean) | L0 | Short-context dynamics |
| 3 | 21 | 8 | M3 (std) | L0 | Short-context variability |
| 4 | 22 | 14 | M1 (mean) | L0 | Medium-context energy dynamics |

---

## Computation

The M-layer integrates E-layer signals into flow-relevant mathematical constructs:

1. **Challenge-skill balance** (idx 3): Quantifies the distance between musical complexity (challenge) and processing capacity (skill). Challenge is measured from context entropy and pitch variability — high entropy and variable pitch indicate complex music. Skill is measured from automaticity and mastery — high values indicate effortless processing. The closer challenge equals skill, the nearer to flow.

2. **Hypofrontality proxy** (idx 4): Product of automaticity × mastery. When both are high, executive monitoring (DLPFC) becomes unnecessary. This maps to Dietrich's transient hypofrontality theory and Limb & Braun's finding of DLPFC deactivation during jazz improvisation. The product ensures BOTH conditions must be met — automaticity alone is insufficient without structural knowledge.

Both outputs are bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02 | Automaticity and mastery for integration |
| R³ [21] | spectral_change | Short-context dynamics and variability |
| R³ [22] | energy_change | Medium-context energy dynamics |
| R³ [23] | pitch_change | Melodic contour rate and long-range variability |
| H³ | 5 tuples (see above) | Context features at H8/H14/H20 |
