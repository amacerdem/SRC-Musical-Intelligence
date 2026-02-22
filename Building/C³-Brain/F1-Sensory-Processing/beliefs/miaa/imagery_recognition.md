# imagery_recognition — Anticipation Belief

**Category**: Anticipation (forward prediction, no PE)
**Function**: F1 (Sensory Processing)
**Mechanism**: MIAA (Musical Imagery Auditory Activation)

---

## Definition

> "Recognition probability when real sound arrives."

## Observe Formula

```
observe = 1.0 × F2:recognition_pred
```

| Source Dim | MIAA Index | Weight | Rationale |
|-----------|-----------|--------|-----------|
| F2:recognition_pred | 10 | 1.0 | Direct F-layer forecast output |

Single-source anticipation — the MIAA's recognition prediction
is the forward-looking signal that feeds into Core beliefs' predict()
methods as context.

---

## Dependency Chain

```
R³/H³ → MIAA (Depth 0, Relay) → imagery_recognition
```

No upstream mechanism dependency. MIAA reads R³/H³ directly.

---

## Downstream Consumers

- Core belief context: feeds into predict() methods of:
  - timbral_character (MIAA): recognition context modulates timbre prediction
  - pitch_identity (PCCR): recognition affects pitch identification confidence
- Anticipation beliefs do NOT generate prediction errors.

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/miaa/imagery_recognition.py`
