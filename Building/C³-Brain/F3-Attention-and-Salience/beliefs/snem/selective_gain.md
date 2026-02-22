# selective_gain — Appraisal Belief (SNEM)

**Category**: Appraisal (observe-only)
**Owner**: SNEM (ASU-α1)

---

## Definition

"Attention-gated amplification: beat frequencies boosted." Observes the degree to which attentional resources amplify processing of beat-aligned events. High selective gain means events on the beat receive substantially more neural processing than off-beat events.

---

## Observation Formula

```
# Direct read from SNEM P-layer:
selective_gain = SNEM.selective_gain[P2]  # index [8]

# Kernel usage: multiplicative gate
# salience *= 1 + 0.3 × selective_gain
```

No prediction — observe-only appraisal. The value is directly consumed by the salience mixer as a multiplicative attention gate.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SNEM P2 | selective_gain [8] | Multiplicative attention gate |
| SNEM E2 | selective_enhancement [2] | E-layer beat×meter interaction |
| SNEM M0 | ssep_enhancement [3] | Raw SS-EP level |

---

## Kernel Usage

The selective_gain appraisal directly modulates the salience mixer:

```python
# Phase 1 in scheduler:
value *= 1 + 0.3 * snem_relay['selective_gain']
```

This creates a multiplicative attention effect: events coinciding with beat positions are amplified, while off-beat events receive baseline processing.

---

## Scientific Foundation

- **Nozaradan 2012**: Selective enhancement goes beyond acoustic envelope (EEG, N=9, p<0.0001)
- **Nozaradan 2011**: Neuronal entrainment tagging — SS-EP magnitude at beat frequency exceeds acoustic energy
- **Yang et al. 2025**: PLV=0.76 frontal-parietal connectivity reflects attention gating

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/snem_relay.py`
