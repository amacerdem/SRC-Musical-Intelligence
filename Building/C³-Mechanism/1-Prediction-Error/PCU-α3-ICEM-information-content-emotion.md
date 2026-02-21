# Information Content → Emotion Mapping

**Source**: PCU-α3-ICEM (Information Content Emotion Model)
**Unit**: PCU (Prediction & Control Unit)
**Tier**: α (Core)
**Score**: 8/10 — Linear emotion mappings with IC as single predictor

---

## Scientific Basis

- **Egermann et al. (2013)**: IC predicts arousal, valence, SCR, HR
- **Pearce & Wiggins (2012)**: IDyOM information content framework

## Mechanism

Information Content (IC = -log2(P(event|context))) directly predicts emotional
responses: higher IC → higher arousal, lower valence, stronger SCR, lower HR.

### Formula

```
IC(event) = -log2(P(event|context))

Arousal = α · IC + β       (positive: surprise → arousal)
Valence = -γ · IC + δ      (negative: surprise → negative valence)
SCR     = ε · IC + ζ       (positive: surprise → skin conductance)
HR      = -η · IC + θ      (negative: surprise → HR deceleration)
```

### Defense Cascade

```
High IC → Orienting Response → Threat Appraisal
         (arousal ↑)          (valence ↓)
         (SCR ↑)              (HR ↓)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| IC | -log2(P(event\|context)) | Information content of musical event |
| P(event\|context) | Context model / H³ entropy | Probability from predictive model |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| arousal | continuous | Arousal response to surprise |
| valence | continuous | Valence shift from surprise |
| scr | continuous | Skin conductance response |
| hr | continuous | Heart rate change |

## Why 8/10

- IC = -log2(P) is a well-defined information-theoretic quantity
- Linear mappings empirically validated (Egermann 2013, live concert N=50, d=6.0)
- Requires context model for P(event|context) (state needed)
- Four parallel output channels with clear sign relationships
- Foundational: IC feeds into PUPF Goldilocks, reward, and salience
