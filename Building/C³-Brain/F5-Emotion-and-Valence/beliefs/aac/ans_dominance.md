# ans_dominance — Appraisal Belief (AAC)

**Category**: Appraisal (observe-only)
**Owner**: AAC (F5)

---

## Definition

"Sympathetic/parasympathetic dominance." Continuous value: 0 = parasympathetic dominance (rest-and-digest, calm), 1 = sympathetic dominance (fight-or-flight, activated). Tracks the autonomic nervous system balance during music listening. At rest, the value hovers near 0.5 (autonomic equilibrium). During emotional peaks, co-activation can occur (both systems active simultaneously), placing the response in Berntson's co-activation quadrant rather than a simple bipolar axis.

---

## Observation Formula

```
# Direct read from AAC E-layer:
ans_dominance = (AAC.f06_ans_response[E1] + 1.0) / 2.0  # remap [-1,1] -> [0,1]

# f06_ans_response = tanh(0.35 * scr_z + 0.40 * (1 - hr_z) + 0.25 * respr_z)
# Positive = sympathetic dominance, negative = parasympathetic dominance
# Remapped to [0,1] for belief store compatibility
```

No prediction — observe-only appraisal. The value is directly read from the AAC extraction layer's ANS composite response, remapped from the bipolar [-1, 1] range to the unipolar [0, 1] belief range. It represents the summary present-moment autonomic balance.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AAC E1 | f06_ans_response [1] | Primary ANS balance signal (bipolar) |
| AAC A0 | scr [2] | Sympathetic component (eccrine sweat glands) |
| AAC A1 | hr [3] | Cardiac component (vagal brake modulation) |
| AAC A2 | respr [4] | Respiratory component (entrainment + arousal) |

---

## Kernel Usage

The ans_dominance appraisal serves as an autonomic state diagnostic:

```python
# Available in BeliefStore for downstream consumers:
# - F7 Motor: autonomic state modulates motor readiness
# - F6 Reward: sympathetic dominance gates reward magnitude
# - F3 Attention: high sympathetic → heightened vigilance
# - Precision engine: extreme autonomic states → higher pi_obs for arousal beliefs
```

Unlike the emotional_arousal Core belief (which tracks felt intensity), ans_dominance captures the specific autonomic balance — whether the listener's body is in an activated or calm state. This distinction matters because high arousal can occur with either sympathetic or parasympathetic dominance (e.g., chills involve co-activation).

---

## Scientific Foundation

- **Berntson 1991**: 2D autonomic space model — sympathetic and parasympathetic are independent dimensions, not endpoints of a single continuum; co-activation quadrant explains chills physiology (Psychophysiology)
- **Peng 2022**: PEP shortened (d=-0.45) + RSA increased (d=+0.38) simultaneously during music = cardiac co-activation (impedance cardiography)
- **Fancourt 2020**: Meta-pooled ANS effect sizes: SCR d=0.85, HR d=0.8-1.5, RespR d=0.45 (meta-analysis, k=26)
- **Gomez & Danuser 2007**: SCR, HR, RespR, Temp all respond to music; arousal dominance factor structure (multi-ANS, N=48)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/aac_relay.py`
