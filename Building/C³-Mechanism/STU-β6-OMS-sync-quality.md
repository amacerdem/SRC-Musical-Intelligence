# Synchronization Quality (Geometric Mean)

**Source**: STU-β6-OMS (Oscillatory Motor Synchronization)
**Unit**: STU (Structural Temporal Unit)
**Tier**: β (Integrative)
**Score**: 8/10 — All-or-nothing synchronization gate

---

## Scientific Basis

- **Edagawa & Kawasaki (2017)**: Beta PSI frontal-temporal z=7.43, EEG N=14
- **Grahn & Brett (2007)**: Putamen Z=5.67
- **Bigand et al. (2025)**: Social coordination F=249.75, N=80
- **Scartozzi et al. (2024)**: Beta-musicality r=0.42, N=57

## Mechanism

Synchronization quality is the geometric mean of three network components:
predictive timing, sensorimotor coupling, and interpersonal sync.
Any single network failure collapses overall sync (all-or-nothing property).

### Formula

```
Sync_Quality = (Predictive × Sensorimotor × Interpersonal) ^ (1/3)

Where:
  Predictive = fronto-striatal beta-band beat anticipation
  Sensorimotor = temporo-parietal gamma-band rhythmic locking
  Interpersonal = social coordination coupling
```

### Key Property

Geometric mean vs arithmetic mean:
- Arithmetic: (1.0 + 0.0 + 0.0) / 3 = 0.33 (still responds)
- Geometric: (1.0 × 0.0 × 0.0) ^ (1/3) = 0.00 (collapses)

This models the empirical finding that synchronization requires ALL three
networks to be active — failure of any one destroys sync.

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Predictive | H³ onset/flux at H6, cross-coupling at H11 | PFC-striatum beta timing |
| Sensorimotor | H³ loudness/periodicity at H11 | STG-IPL gamma locking |
| Interpersonal | H³ long-range coupling at H20 | Social coordination |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| sync_quality | [0, 1] | Overall synchronization quality |

## Why 8/10

- Geometric mean is a real computational mechanism (not weighted average)
- All-or-nothing property matches empirical synchronization data
- Multiple converging evidence sources (z=7.43, Z=5.67, F=249.75)
- No state needed
- Generalizable pattern: any all-or-nothing integration can use this
