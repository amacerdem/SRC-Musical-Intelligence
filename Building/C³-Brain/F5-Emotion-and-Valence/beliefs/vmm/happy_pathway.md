# happy_pathway — Appraisal Belief (VMM)

**Category**: Appraisal (observe-only)
**Owner**: VMM (ARU-α3)

---

## Definition

"Striatal reward circuit (major/consonant)." Tracks activation of the reward pathway associated with major mode and consonant harmony. This is the ventral striatum (NAcc) + dorsal striatum (caudate) + ACC circuit that responds preferentially to happy-sounding music. The pathway overlaps with SRP's reward computation at the neural level, reflecting that happy music is inherently more rewarding at the circuit level (Mitterschiffthaler 2007).

This appraisal tracks the PERCEIVED reward circuit activation, not the FELT reward -- it is a bottom-up signal about how strongly the current acoustic content engages the striatal reward pathway based on mode and consonance alone.

---

## Observation Formula

```
# Direct read from VMM R-layer:
happy_pathway = VMM.happy_pathway[R0]  # index [3]

# R0 = sigma(0.50×consonance_valence + 0.30×mode_signal + 0.20×brightness_section)
# VS + DS activation for major/consonant music
# Mitterschiffthaler 2007: VS t=4.58, DS z=3.80
# Trost 2012: Joy -> L.VS z=5.44
```

No prediction -- observe-only appraisal. The value is directly read from the VMM mechanism's R-layer happy pathway composite. It integrates consonance-derived pleasantness (50%, the strongest driver), mode signal (30%, major mode enhances), and section brightness (20%, bright timbre confirms positive valence).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM R0 | happy_pathway [3] | Striatal reward circuit composite |
| VMM V1 | mode_signal [1] | Upstream: major/minor mode (30% weight) |
| VMM V2 | consonance_valence [2] | Upstream: consonance pleasantness (50% weight) |
| H³ (14, 22, 0, 2) | brightness_section | Section brightness at 15s (20% weight) |
| H³ (4, 19, 0, 2) | consonance_state | Phrase-level consonance for V2 |

---

## Kernel Usage

The happy_pathway appraisal feeds reward computation:

```python
# Available in BeliefStore for downstream consumers:
# - F6 Reward: striatal activation modulates wanting/liking
#   happy_pathway × prediction_match → reward amplification
# - F5 Internal: perceived_happy Core belief integrates this as context
# - DAED relay: reward circuit activation feeds dopaminergic computation
```

Unlike the perceived_happy Core belief (which undergoes Bayesian PE and integrates implicit H3 signals), happy_pathway is a pure mechanism read -- it reports the striatal circuit activation computed by VMM's R-layer without kernel-level integration.

---

## Scientific Foundation

- **Mitterschiffthaler 2007**: Happy music -> VS t=4.58, DS z=3.80, ACC z=3.39 (fMRI, N=16)
- **Trost 2012**: Joy -> L.VS z=5.44, confirming striatal reward circuit for positive valence (fMRI, N=15)
- **Koelsch 2006**: Consonant -> VS (t=5.1), consonance activates reward circuit regardless of mode context (fMRI, N=11)
- **Salimpoor 2011**: Caudate DA during anticipation, NAcc DA during peak pleasure (PET, N=8)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/extraction.py`
