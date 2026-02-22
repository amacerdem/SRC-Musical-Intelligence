# savoring_effect — Appraisal Belief (AACM)

**Category**: Appraisal (observe-only)
**Owner**: AACM (ASU-b3)

---

## Definition

"Liking leads to attention leads to slower response leads to sustained engagement." Observes the behavioral savoring chain: aesthetic preference captures attention, which inhibits motor responses, producing measurable RT slowing. This RT slowing is itself the signature of deep aesthetic engagement.

---

## Observation Formula

```
# Direct read from AACM M-layer and E-layer:
savoring_effect = observe(
    AACM.rt_appreciation[M1]       # index [4]
  + AACM.savoring_effect[E2]       # index [2]
)

# Kernel usage: appraisal monitoring
# Tracks liking -> attention -> RT slowing chain
```

No prediction — observe-only appraisal. The value captures the behavioral manifestation of aesthetic engagement: how much the listener's response is slowed by preference-driven attentional capture.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AACM M1 | rt_appreciation [4] | RT-derived appreciation index |
| AACM E2 | savoring_effect [2] | Raw RT slowing from attention*inhibition |
| AACM E0 | attentional_engage [0] | Attention capture component |
| AACM E1 | motor_inhibition [1] | Motor pause component |

---

## Kernel Usage

The savoring_effect appraisal monitors the behavioral consequence of aesthetic engagement:

```python
# Phase 1 in scheduler:
savoring_effect = observe(aacm_relay['rt_appreciation'],
                           aacm_relay['savoring_effect'])
```

This provides a graded signal of how strongly the listener is "savoring" the current stimulus. High values indicate the liking-attention-RT chain is active: the listener finds the stimulus pleasant, attention is captured, motor responses are inhibited, and the experience is sustained.

---

## Scientific Foundation

- **Foo 2016**: RT slowing proportional to aesthetic preference
- **Sarasso 2019**: N2/P3 motor inhibition linked to appreciation (EEG, d=2.008)
- **Kim 2019**: vmPFC slow activation during aesthetic appreciation (fMRI, T=6.852)
- **Salimpoor 2011**: Caudate/NAcc dopamine during pleasurable music (PET, r=0.71)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/aacm_relay.py`
