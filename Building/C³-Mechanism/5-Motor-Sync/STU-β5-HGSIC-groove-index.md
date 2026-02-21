# Hierarchical Groove Index

**Source**: STU-β5-HGSIC (Hierarchical Groove State Integration Circuit)
**Unit**: STU (Structural Temporal Unit)
**Tier**: β (Integrative)
**Score**: 8/10 — Validated hierarchical integration

---

## Scientific Basis

- **Potes et al. (2012)**: r=0.49 pSTG high-gamma, ECoG N=8
- **Spiech et al. (2022)**: Inverted-U syncopation, N=30, chi2=14.643
- **Grahn & Brett (2007)**: Putamen Z=5.67
- **Ayyildiz et al. (2025)**: Micro-timing sensitivity Odds=100.69

## Mechanism

Groove emerges from hierarchical integration of beat, meter, and motor coupling.
Later (deeper) levels are weighted more heavily. Motor groove requires both
beat AND meter to be active (multiplicative gate).

### Formula

```
Beat_Gamma = σ(0.49 · amplitude · loudness · onset · beat_induction)
Motor_Groove = σ(0.70 · Beat_Gamma · Meter · motor_entrainment)

Groove_Index = (1·Beat + 2·Meter + 3·Motor) / 6

Where:
  0.49 = pSTG high-gamma correlation (Potes 2012)
  0.70 = auditory→motor coupling at 110ms delay (Potes 2012)
  Weights 1,2,3 = hierarchical depth scaling
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| amplitude, loudness, onset | H³ at H6 (200ms) | Beat-level features |
| meter | H³ at H11-H14 | Phrase-level metrical structure |
| motor_entrainment | H³ cross-coupling | Auditory-motor synchronization |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| beat_gamma | [0, 1] | pSTG beat tracking (70-170 Hz) |
| motor_groove | [0, 1] | Motor entrainment gate |
| groove_index | [0, 1] | Integrated hierarchical groove |

## Why 8/10

- Empirical coefficients from ECoG (0.49, 0.70)
- Hierarchical weighting validated across 7 methods
- Motor groove is multiplicative (genuine gate, not additive)
- Inverted-U syncopation curve replicated
- No internal state needed (H³ provides temporal context)
