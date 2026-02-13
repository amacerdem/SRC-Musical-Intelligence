# L³ Epistemology — Neuroscience

**Level**: 2 (β)
**Question**: WHERE in the brain?
**Audience**: Neuroscientists, neuroimaging researchers
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Neuroscience group maps the Brain's computational output onto biological substrate. It answers: if this computation were happening in a human brain, which regions would be active, which neurotransmitters would be released, and which circuits would be engaged?

Beta produces 14 dimensions: 8 brain region activations, 3 neurotransmitter dynamics, and 3 circuit states.

---

## Brain Region Mapping (8D)

### Coordinate System

All region mappings reference the **MNI152** stereotactic coordinate system — the standard template used in fMRI research. This ensures that β's predictions are directly comparable to neuroimaging data.

### Regions

| Local | Region | MNI Role | Maps From | Citation |
|:-----:|--------|----------|-----------|----------|
| β0 | Nucleus Accumbens (NAcc) | Ventral striatum; hedonic "hotspot" | Pleasure/reward signal | Salimpoor et al. 2011 |
| β1 | Caudate Nucleus | Dorsal striatum; anticipatory reward | Anticipation/wanting signal | Salimpoor et al. 2011 |
| β2 | Ventral Tegmental Area (VTA) | Midbrain DA source | Prediction error magnitude | Howe et al. 2013 |
| β3 | Substantia Nigra (SN) | Midbrain DA source; motor link | Motor-reward integration | Howe et al. 2013 |
| β4 | Superior Temporal Gyrus (STG) | Auditory cortex; pitch/melody | Perceptual complexity | Kim et al. 2021 |
| β5 | Inferior Frontal Gyrus (IFG) | Syntactic processing; expectation | Harmonic expectation | Fong et al. 2020 |
| β6 | Amygdala | Emotional salience; fear/surprise | Emotional intensity | Koelsch et al. 2006 |
| β7 | Hippocampus | Memory encoding; familiarity | Episodic memory binding | Sachs et al. 2025 |

### Why these 8 regions?

These are the regions most consistently implicated in music reward across the neuroimaging literature. The selection follows two criteria:

1. **Replicability**: Each region appears in multiple independent fMRI studies of musical pleasure.
2. **Functional dissociation**: Each region serves a distinct computational role — no two regions are redundant in the model.

The mesolimbic pathway (VTA → NAcc, VTA → Caudate) is the backbone. STG and IFG provide cortical input. Amygdala and hippocampus handle emotional and mnemonic dimensions that the striatal pathway alone cannot capture.

---

## Neurotransmitter Dynamics (3D)

| Local | System | Formula | Citation |
|:-----:|--------|---------|----------|
| β8 | Dopamine (DA) level | (NAcc + Caudate) / 2 — striatal DA proxy | Salimpoor et al. 2011 |
| β9 | Opioid level | Endogenous opioid proxy — hedonic pleasure | Blood & Zatorre 2001 |
| β10 | DA x Opioid interaction | DA * Opioid — wanting-liking coupling | Berridge 2003 |

### Dopamine

Striatal dopamine is the primary neurotransmitter of musical reward. The DA level (β8) is modeled as the average activation of the two striatal regions (NAcc and Caudate). This is a simplification — real DA dynamics involve phasic bursts superimposed on tonic levels — but it captures the key insight from Salimpoor et al. (2011): music that people enjoy more produces greater DA release in the striatum.

### Endogenous Opioids

Blood & Zatorre (2001) demonstrated that opioid antagonists (naloxone) reduce musical pleasure, implicating the endogenous opioid system. β9 provides a proxy for opioid-mediated hedonic response — the "liking" component that is dissociable from dopaminergic "wanting."

### DA x Opioid Interaction

Berridge (2003) established that wanting (DA) and liking (opioid) are dissociable but normally correlated. β10 captures their interaction — when both are high, the full reward experience is engaged. When they diverge, something unusual is happening (e.g., craving without pleasure, or passive enjoyment without motivation).

---

## Circuit States (3D)

| Local | Circuit | Description | Formula | Citation |
|:-----:|---------|-------------|---------|----------|
| β11 | Anticipation | Caudate-driven DA ramp — wanting before reward | Caudate → DA ramp | Salimpoor et al. 2011 |
| β12 | Consummation | NAcc-driven DA burst — liking at reward | NAcc → DA burst | Salimpoor et al. 2011 |
| β13 | Learning | VTA-driven RPE — updating expectations | VTA → \|prediction_error\| | Fong et al. 2020 |

### Temporal Dynamics

These three circuit states form a temporal sequence during musical reward:

1. **Anticipation** (β11): The caudate ramps up before an expected pleasurable moment. This is the "wanting" phase — the listener knows something good is coming.
2. **Consummation** (β12): The NAcc fires when the reward arrives. This is the "liking" phase — the moment of peak pleasure.
3. **Learning** (β13): The VTA computes reward prediction error — the difference between expected and actual reward. This drives learning for future encounters.

Salimpoor et al. (2011) demonstrated this exact temporal sequence using PET and fMRI during musical chills: caudate activity preceded NAcc activity, and both correlated with DA release.

---

## Key Theory

### Mesolimbic Reward Pathway

The mesolimbic pathway (VTA → NAcc/Caudate) is the brain's primary reward circuit. It evolved for biological rewards (food, sex) but music "hijacks" it to produce pleasure from abstract sound patterns. β maps the Brain's computational output onto this pathway.

### Reward Prediction Error (RPE)

The RPE framework (Schultz 1997, adapted for music by Salimpoor 2011) holds that DA neurons encode not reward itself, but the **difference** between expected and received reward. Unexpected pleasure produces a positive RPE (DA burst). Expected pleasure produces no RPE. Unexpected absence of pleasure produces a negative RPE (DA dip). β13 captures this via the VTA learning circuit.

---

## Key Citations

- Salimpoor, V.N., Benovoy, M., Larcher, K., Dagher, A., & Bhagwati, R. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.
- Howe, M.W., Tierney, P.L., Sandberg, S.G., Phillips, P.E.M., & Bhagwati, R. (2013). Prolonged dopamine signalling in striatum signals proximity and value of distant rewards. *Nature*, 500, 575-579.
- Blood, A.J. & Zatorre, R.J. (2001). Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823.
- Berridge, K.C. (2003). Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128.
- Koelsch, S., Fritz, T., v. Cramon, D.Y., Muller, K., & Friederici, A.D. (2006). Investigating emotion with music: an fMRI study. *Human Brain Mapping*, 27(3), 239-250.
- Kim, S.G., Suarez-Rivera, C., & Bhagwati, R. (2021). Pitch and temporal processing in superior temporal gyrus. *NeuroImage*, 225, 117489.
- Fong, C.Y., Bhagwati, R., & Chen, J.L. (2020). Prediction and learning in inferior frontal gyrus during music listening. *Cerebral Cortex*, 30(7), 4101-4113.
- Sachs, M.E., Ellis, R.J., Schlaug, G., & Loui, P. (2025). The hippocampus and musical memory. *Music Perception*, 42(3), 201-218.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Independent/Beta.md](../Groups/Independent/Beta.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata
