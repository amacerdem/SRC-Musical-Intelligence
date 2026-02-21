# Precision-Weighted Prediction Error

**Source**: ASU-γ1-PWSM (Precision-Weighted Salience Model), also in ASU-α2-IACM
**Unit**: ASU (Attentional Salience Unit)
**Tier**: γ (Speculative) / α (Core)
**Score**: 8/10 — Bayesian framework with empirical MMN validation

---

## Scientific Basis

- Predictive coding framework (Friston)
- MMN presence/abolition as function of context stability
- Stable context: MMN present (d=-1.37 for inharmonicity)
- Unstable context: MMN abolished (d=0.01, n.s.)

## Mechanism

The brain weights prediction errors by precision (inverse variance of context).
In stable contexts, PEs are amplified (high precision → "trust the error").
In unstable contexts, PEs are suppressed (low precision → "ignore the error").

### Formula

```
PE_weighted = PE_raw × Precision

Precision = 1 / (1 + σ²_context)

Where:
  PE_raw = |observed - predicted|
  σ²_context = variance of recent context (e.g., inter-onset intervals)

Stable context (low variance):
  Precision → 1.0 → PE fully weighted → MMN present
Unstable context (high variance):
  Precision → 0.0 → PE suppressed → MMN abolished
```

### Bayesian Interpretation

```
Posterior ∝ Likelihood × Prior
PE_weighted ∝ PE × Precision

The brain "ignores" prediction errors in uncertain contexts.
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| PE_raw | |observed - predicted| | Raw prediction error |
| σ²_context | Variance of recent H³ features | Context stability |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| PE_weighted | [0, 1] | Precision-weighted prediction error |
| Precision | [0, 1] | Context reliability estimate |

## Why 8/10

- Core Bayesian predictive coding mechanism
- Empirically validated: MMN present (d=-1.37) vs abolished (d=0.01)
- Clean formula: PE × (1/(1+σ²))
- Requires state (context variance from recent history)
- Foundational for entire C³ kernel (every belief update needs this)
- Appears in TWO separate models (IACM + PWSM) — convergent evidence
