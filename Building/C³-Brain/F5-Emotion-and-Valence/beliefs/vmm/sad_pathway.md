# sad_pathway — Appraisal Belief (VMM)

**Category**: Appraisal (observe-only)
**Owner**: VMM (ARU-α3)

---

## Definition

"Limbic emotional circuit (minor/dissonant)." Tracks activation of the limbic pathway associated with minor mode and dissonant harmony. This is the hippocampus + amygdala + parahippocampal gyrus circuit that responds preferentially to sad-sounding music. This pathway enables "perceived sadness" -- the cognitive recognition of sad musical character -- and is the neural substrate for the sad music paradox: the limbic circuit processes sadness while the reward circuit simultaneously processes pleasure.

Unlike happy_pathway (striatal reward), sad_pathway engages the memory-emotion circuit. This overlap with F4 memory systems is not coincidental: the limbic pathway for sad music engages the same hippocampal structures used for autobiographical memory, which is why sad music is particularly effective at evoking nostalgia (Green 2008).

---

## Observation Formula

```
# Direct read from VMM R-layer:
sad_pathway = VMM.sad_pathway[R1]  # index [4]

# R1 = sigma(0.40×(1−consonance_valence) + 0.30×(1−mode_signal) + 0.30×arousal_modulator)
# HIP + AMY activation for minor/dissonant music
# Mitterschiffthaler 2007: HIP t=4.88
# Koelsch 2006: AMY t=4.7, HIP t=6.9
```

No prediction -- observe-only appraisal. The value is directly read from the VMM mechanism's R-layer sad pathway composite. It integrates dissonance (40%, inverted consonance), minor mode (30%, inverted mode signal), and arousal modulation (30%, louder sad music activates the limbic circuit more strongly per Trost 2012).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM R1 | sad_pathway [4] | Limbic emotional circuit composite |
| VMM V1 | mode_signal [1] | Upstream: major/minor mode (inverted, 30% weight) |
| VMM V2 | consonance_valence [2] | Upstream: consonance pleasantness (inverted, 40% weight) |
| H³ (14, 22, 0, 2) | brightness_section | Section brightness at 15s (inverted for darkness) |
| H³ (4, 19, 0, 2) | consonance_state | Phrase-level consonance (inverted for dissonance) |

---

## Kernel Usage

The sad_pathway appraisal feeds emotion and reward computation:

```python
# Available in BeliefStore for downstream consumers:
# - F6 Reward: limbic activation feeds nostalgia/beauty reward pathway
#   sad_pathway × perceived_sad → beauty-in-sadness modulator
# - F5 Internal: perceived_sad Core belief integrates this as context
# - F4 Memory: limbic overlap with hippocampal memory system
#   sad_pathway × autobiographical_retrieval → nostalgia amplification
```

Unlike the perceived_sad Core belief (which undergoes Bayesian PE and integrates implicit H3 signals), sad_pathway is a pure mechanism read -- it reports the limbic circuit activation computed by VMM's R-layer without kernel-level integration.

---

## Scientific Foundation

- **Mitterschiffthaler 2007**: Sad music -> HIP t=4.88. Double dissociation from happy pathway (fMRI, N=16)
- **Koelsch 2006**: Dissonant -> AMY (t=4.7), HIP (t=6.9), PHG (t=5.7) (fMRI, N=11)
- **Green 2008**: Minor -> limbic BEYOND dissonance alone -- PHG, ventral ACC, mPFC (fMRI)
- **Brattico 2011**: Perceived sad -> bilateral AMY + PHG (Z>=3.5). Separate from felt pleasure circuits (fMRI, N=15)
- **Sachs 2015**: Liked sad music -> Caudate z=6.27 (reward). Disliked -> Amygdala z=4.11. Separate circuits resolve the paradox (fMRI)
- **Trost 2012**: Nostalgia -> R.HIP z=5.62, sgACC z=6.15. Limbic pathway drives nostalgic experience (fMRI, N=15)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/extraction.py`
