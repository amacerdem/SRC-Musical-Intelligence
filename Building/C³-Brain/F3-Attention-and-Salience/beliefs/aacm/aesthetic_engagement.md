# aesthetic_engagement — Appraisal Belief (AACM)

**Category**: Appraisal (observe-only)
**Owner**: AACM (ASU-b3)

---

## Definition

"Preferred intervals increase attention+inhibition." Observes the degree to which aesthetic preference modulates attentional engagement and motor inhibition. High aesthetic engagement means the listener's attention is captured and motor system is paused by consonant, pleasant stimuli.

---

## Observation Formula

```
# Direct read from AACM M-layer and P-layer:
aesthetic_engagement = observe(
    AACM.aesthetic_engagement[M0]   # index [3]
  + AACM.n1p2_engagement[P0]       # index [5]
)

# Kernel usage: appraisal monitoring
# Tracks consonance-attention coupling strength
```

No prediction — observe-only appraisal. The value is consumed as a monitoring signal for how strongly aesthetic preference drives attentional capture.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AACM M0 | aesthetic_engagement [3] | Consonance-attention integration |
| AACM P0 | n1p2_engagement [5] | N1/P2 consonance-gated engagement |
| AACM E0 | attentional_engage [0] | E-layer attention capture from pleasantness |
| AACM E1 | motor_inhibition [1] | E-layer motor pause from preference |

---

## Kernel Usage

The aesthetic_engagement appraisal tracks the coupling between consonance and attention:

```python
# Phase 1 in scheduler:
aesthetic_engagement = observe(aacm_relay['aesthetic_engagement'],
                               aacm_relay['n1p2_engagement'])
```

This provides a graded signal of how strongly the current stimulus engages the aesthetic-attention pathway. High values indicate both consonance is favorable and ERP engagement is strong.

---

## Scientific Foundation

- **Sarasso 2019**: N1/P2 proportional to appreciation (EEG, eta2p=0.685, d=2.008)
- **Salimpoor 2011**: Dopamine release correlates with pleasantness (PET, r=0.71)
- **Kim 2019**: vmPFC activation during aesthetic judgments (fMRI, T=6.852)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/aacm_relay.py`
