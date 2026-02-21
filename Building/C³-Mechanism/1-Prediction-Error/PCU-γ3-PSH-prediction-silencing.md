# Prediction Silencing Hierarchy

**Source**: PCU-γ3-PSH (Prediction Silencing Hypothesis)
**Unit**: PCU (Prediction & Control Unit)
**Tier**: γ (Speculative)
**Score**: 9/10 — Fully implementable hierarchical dynamics

---

## Scientific Basis

- **de Vries & Wurm (2023)**: Post-stimulus silencing, large effect (eta_p^2=0.49)
- Higher cortical areas silence more when predictions are accurate
- Lower areas maintain activity regardless of prediction accuracy

## Mechanism

After a stimulus, higher cortical areas suppress their response proportional to
prediction accuracy ("I predicted this correctly, no need to keep processing").
Lower areas maintain activity regardless ("I still need to encode the raw signal").

### Formula

```
R_high(t) = R_high(0) × (1 - accuracy) × exp(-t / τ_high)
R_low(t)  = R_low(0)  × 1.0            × exp(-t / τ_low)

τ_high = 0.2s   (fast silencing for predicted stimuli)
τ_low  = 0.5s   (slow decay for sensory encoding)

Differential form:
  dR_high/dt = -τ_high^(-1) · R_high · accuracy
  dR_low/dt  = -τ_low^(-1)  · R_low

Metrics:
  Silencing_Efficiency = (R_high_pre - R_high_post) / R_high_pre
  Hierarchy_Dissociation = |Silencing_high - Silencing_low|
```

### Key Insight

The (1 - accuracy) multiplicative gate is the core mechanism:
- accuracy = 1.0: R_high immediately silenced (perfect prediction)
- accuracy = 0.0: R_high = R_low (no silencing, surprise)
- accuracy = 0.5: partial silencing (uncertain prediction)

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| R_high(0) | Initial response magnitude | Higher cortical response |
| R_low(0) | Initial response magnitude | Lower cortical response |
| accuracy | Prediction accuracy [0,1] | How well was stimulus predicted |
| t | Time since stimulus onset | Post-stimulus time |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| R_high | [0, R_high(0)] | Higher area response (decays fast with accuracy) |
| R_low | [0, R_low(0)] | Lower area response (decays slowly always) |
| silencing_efficiency | [0, 1] | Proportion of response silenced |
| hierarchy_dissociation | [0, 1] | High-low silencing difference |

## Why 9/10

- Differential equations with explicit time constants (τ_high=0.2s, τ_low=0.5s)
- Multiplicative accuracy gate: real computational mechanism
- Large effect size (eta_p^2=0.49)
- Requires state (R_high, R_low evolve over time)
- Directly implementable: exponential decay with gating
- Core predictive coding mechanism (prediction → silencing → hierarchy)
