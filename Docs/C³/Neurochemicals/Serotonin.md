# Serotonin (5-HT) -- Mood Regulation and Emotional Valence Modulation

> **Code**: `mi_beta/brain/neurochemicals/serotonin.py`
> **NeurochemicalType**: `SEROTONIN`
> **Manager methods**: `write_serotonin()`, `read_serotonin()`, `serotonin_keys`

## Overview

The serotonergic system originates from the raphe nuclei in the brainstem and projects widely to cortical and subcortical targets. In musical cognition, 5-HT modulates:

1. **Emotional valence**: Background mood state that colours emotional interpretation. Low 5-HT biases toward negative valence (sadness), high 5-HT toward positive (Koelsch 2014).
2. **Social bonding**: Mediates pro-social effects of group music-making, contributing to connection and trust (Tarr et al. 2014).
3. **Anxiety modulation**: 5-HT1A receptor activation in amygdala and PFC reduces anxiety, enabling relaxation responses to calming music (Chanda & Levitin 2013).

Unlike dopamine, serotonin operates primarily as a **slow neuromodulator** (seconds to minutes) rather than encoding discrete events.

---

## Region Specifications (`SEROTONIN_REGIONS`)

| Region Key | Full Name | Receptor | Timescale | Role | Citation |
|------------|-----------|----------|-----------|------|----------|
| `raphe` | Dorsal Raphe Nucleus | 5-HT1A (autoreceptor), 5-HT2A (post-synaptic) | Slow (tonic, seconds to minutes) | Primary 5-HT source; provides tonic serotonergic drive that sets overall emotional valence bias and mood state. Firing rate modulates sensitivity to musical affect | Koelsch 2014; Chanda & Levitin 2013 |
| `amygdala` | Amygdala | 5-HT1A (inhibitory), 5-HT2A (excitatory) | Slow (seconds) | 5-HT modulates amygdala reactivity to emotionally salient musical stimuli. High 5-HT reduces threat/anxiety response, enabling nuanced emotional processing of minor mode, dissonance, and tension | Koelsch 2014; Trost 2012 |
| `pfc` | Prefrontal Cortex | 5-HT2A (cortical layer V pyramidal cells) | Slow (seconds to minutes) | Supports cognitive reappraisal of musical emotions and top-down regulation of affective state. Mediates transition from raw affect to conscious aesthetic judgement | Koelsch 2014; Ferreri 2019 |

---

## Mood Modulation Role

Serotonin's primary role in musical cognition is as a background modulator of emotional processing. It does NOT encode discrete musical events (that is DA's role) but sets the tonic "emotional colour" through which music is interpreted.

Three primary mechanisms:

1. **Valence bias**: High 5-HT -> positive interpretation (raphe -> PFC)
2. **Anxiety reduction**: 5-HT1A activation -> reduced amygdala reactivity
3. **Social bonding**: Group music -> oxytocin/5-HT interaction -> trust

Evidence: Koelsch 2014 model; Chanda & Levitin 2013 review; Kreutz et al. 2012 (choral singing increases 5-HT metabolites).

---

## Interaction with Dopamine (`SEROTONIN_DA_INTERACTION`)

5-HT and DA interact bidirectionally in the reward circuit:

| Receptor | Location | Effect on DA | Net Impact |
|----------|----------|-------------|------------|
| 5-HT2C | VTA DA neurons | **Inhibits** DA release | Negative gate on reward |
| 5-HT1B | NAcc terminals | **Facilitates** DA release | Positive gate on reward |

Net effect depends on receptor balance and tonic 5-HT level. Positive mood (high 5-HT) can either amplify or dampen musical reward depending on which receptor pathway dominates. Ferreri 2019 showed levodopa (DA+) and 5-HT interact for musical pleasure.

---

## Interaction with Other Systems

- **Dopamine**: Bidirectional modulation via 5-HT2C (inhibits VTA DA) and 5-HT1B (facilitates NAcc DA). Mood state gates reward sensitivity.
- **Opioid**: 5-HT modulates the background mood that colours hedonic evaluation. Low 5-HT may blunt opioid-mediated pleasure.
- **Norepinephrine**: 5-HT and NE share some receptor targets in amygdala and PFC. Both contribute to emotional regulation but on different timescales (5-HT slower, NE faster).

---

## Models That Write/Read Serotonin

**Writers** (models that produce 5-HT signals):
- ARU models (AAC) -- write mood/valence modulation signals
- PCU models -- write emotional state signals

**Readers** (models that consume 5-HT signals):
- ARU models -- read for affect computation and valence bias
- RPU models -- read for reward sensitivity modulation

---

## Key Papers

| Paper | Finding |
|-------|---------|
| Koelsch 2014 | Serotonin in music-evoked emotion model: valence modulation |
| Chanda & Levitin 2013 | Neurochemistry of music review: 5-HT role in mood/anxiety |
| Tarr et al. 2014 | Social bonding through group music-making involves 5-HT |
| Kreutz et al. 2012 | Choral singing increases 5-HT metabolites |
| Ferreri et al. 2019 | DA/5-HT interaction in musical pleasure (pharmacological) |
