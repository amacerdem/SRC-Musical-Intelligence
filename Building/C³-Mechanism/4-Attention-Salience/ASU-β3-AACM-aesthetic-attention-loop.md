# Aesthetic-Attention Feedback Loop

**Source**: ASU-β3-AACM (Aesthetic-Attention Coupling Model)
**Unit**: ASU (Attentional Salience Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — Feedback loop with empirical ERP correlations

---

## Scientific Basis

- Consonant > Dissonant appreciation (d=2.008, p<0.001)
- N1/P2 amplitude correlates with aesthetic rating
- RT slowing with appreciation ("savoring")

## Mechanism

Attention and aesthetics form a feedback loop:
Attention (N1/P2) → Appreciation → Inhibition (N2/P3) → Savoring (RT slowing) → back to Attention

### Formula

```
ERP-Behavior Loop:
  N1P2_amplitude ∝ Aesthetic_Rating    (more beautiful → more attention)
  N2P3_amplitude ∝ Aesthetic_Rating    (more beautiful → more inhibition)
  RT ∝ Aesthetic_Rating                (more beautiful → slower response = savoring)

Savoring dynamics:
  Savoring_Effect = β · Appreciation + ε
  τ = 2.0s (aesthetic judgment window)

Feedback:
  Attention[t+1] = f(Appreciation[t])
  Appreciation[t+1] = g(Attention[t+1], Consonance[t+1])
```

### Key Insight: Savoring = Slowing Down

More appreciated music → SLOWER behavioral responses.
This is NOT a deficit — it's active savoring (inhibition to prolong experience).

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Consonance | BCH consonance signal | Current consonance level |
| Aesthetic_Rating | Hedonic evaluation | Current appreciation |
| Appreciation[t-1] | State | Previous appreciation |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| N1P2 | [0, 1] | Attention amplitude |
| N2P3 | [0, 1] | Inhibition amplitude |
| savoring | [0, 1] | RT slowing (pleasure prolongation) |

## Why 7/10

- Feedback loop: real dynamical system (attention → appreciation → attention)
- Savoring = active inhibition (not passive)
- d=2.008 for consonance effect
- Requires state (previous appreciation)
- But linear proportionality relationships (not full nonlinear dynamics)
