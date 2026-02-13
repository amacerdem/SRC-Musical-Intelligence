# Norepinephrine (NE) -- Arousal, Attentional Gating, and Orienting Response

> **Code**: `mi_beta/brain/neurochemicals/norepinephrine.py`
> **NeurochemicalType**: `NOREPINEPHRINE`
> **Manager methods**: `write_ne()`, `read_ne()`, `ne_keys`

## Overview

The noradrenergic system originates from the locus coeruleus (LC) in the brainstem and projects to virtually every cortical and subcortical region. In musical cognition, NE mediates:

1. **Arousal regulation**: Sets global arousal level determining the intensity of musical experience. LC firing rate tracks stimulus salience and surprise (Aston-Jones & Cohen 2005).
2. **Attentional gating**: Modulates signal-to-noise ratio in auditory cortex, enabling selective attention to musically relevant events (Menon & Levitin 2005).
3. **Orienting response**: Novel or unexpected musical events trigger NE release, producing autonomic orienting (pupil dilation, skin conductance increase, heart rate deceleration).
4. **Memory consolidation**: Enhances encoding of emotionally salient musical events in hippocampus and amygdala (McGaugh 2004).

---

## Tonic vs Phasic Modes

NE operates on two timescales:

| Mode | LC Firing | Function | Musical Context |
|------|-----------|----------|-----------------|
| **Tonic** | Sustained baseline | Sets global alertness and arousal level | Background arousal during listening |
| **Phasic** | Brief event-triggered bursts | Signals salient stimuli, drives orienting | Sudden dynamics, unexpected harmonies, timbral surprises, rhythmic violations |

**Tonic mode effects**:
- High tonic NE -> broad, exploratory attention
- Low tonic NE -> focused, exploitative attention

**Phasic mode effects**:
- Produces autonomic orienting response (pupil dilation, SCR)
- Enhances signal-to-noise ratio in auditory cortex
- Triggers downstream VTA DA responses for reward processing

---

## Region Specifications (`NE_REGIONS`)

| Region Key | Full Name | NE Mode | Receptor | Role | Citation |
|------------|-----------|---------|----------|------|----------|
| `locus_coeruleus` | Locus Coeruleus | both | alpha-2 (autoreceptor), alpha-1/beta-1 (post-synaptic) | Primary NE source (~50,000 neurons in humans) projecting to entire brain. Tonic firing sets global arousal; phasic bursts signal salient events. Implements adaptive gain control amplifying task-relevant stimulus processing | Aston-Jones & Cohen 2005; Sara 2009 |
| `amygdala` | Amygdala (Basolateral Complex) | phasic | beta-1 (post-synaptic excitatory) | NE amplifies emotional processing in basolateral amygdala, enhancing encoding of emotionally arousing musical events. Beta-adrenergic activation increases synaptic plasticity for affectively salient stimuli | McGaugh 2004; Menon & Levitin 2005 |
| `pfc` | Prefrontal Cortex | tonic | alpha-2A (strengthens PFC), alpha-1 (weakens at high NE) | Optimises PFC function in inverted-U dose-response: moderate NE enhances working memory and attentional control; excessive NE impairs PFC. Alpha-2A strengthens network connectivity for sustained attention to musical structure | Arnsten 2011; Menon & Levitin 2005 |

---

## PFC Inverted-U Dose Response

NE's effect on prefrontal cortex follows an inverted-U curve:

```
PFC Performance
     ^
     |        *****
     |      **     **
     |    **         **
     |  **             **
     | *                 *
     |*                   *
     +-----------------------> NE Level
     Low    Optimal    High
```

- **Low NE**: Drowsy, unfocused -- poor musical attention
- **Optimal NE**: Alert, focused -- best working memory for tonal context
- **High NE** (stress): Anxious, distracted -- PFC function impaired, emotional hijack

Receptor mechanism: alpha-2A receptors strengthen PFC at moderate NE; alpha-1 receptors weaken PFC at high NE (Arnsten 2011).

---

## Interaction with Dopamine (`NE_DA_INTERACTION`)

NE and DA systems interact for musical reward processing:

| Interaction | Mechanism | Musical Effect |
|-------------|-----------|----------------|
| LC -> VTA triggering | Phasic NE bursts to salient events trigger downstream VTA DA phasic responses | Unexpected musical events -> NE burst -> enhanced DA RPE |
| NAcc modulation | NE modulates DA release in NAcc via alpha-1 receptors | Arousal state (NE) gates reward sensitivity (DA) |
| Amplification | High arousal + positive prediction error | Amplified pleasure if surprise resolves positively |

Reference: Devoto & Flore 2006 (LC-VTA interaction).

---

## Interaction with Other Systems

- **Dopamine**: NE phasic bursts trigger VTA DA responses; NE modulates DA release in NAcc via alpha-1 receptors. Arousal gates reward sensitivity.
- **Serotonin**: Both modulate amygdala and PFC but on different timescales. NE provides fast phasic arousal; 5-HT provides slow tonic mood bias.
- **Opioid**: NE-driven arousal amplifies the salience of hedonic moments, potentially enhancing the subjective impact of opioid-mediated pleasure.

---

## Models That Write/Read NE

**Writers** (models that produce NE signals):
- ASU models (SNEM) -- write arousal and salience signals
- NDU models -- write novelty-driven NE responses

**Readers** (models that consume NE signals):
- ARU models -- read NE for arousal-gated reward computation
- PCU models -- read NE for attentional modulation of imagery
- IMU models -- read NE for memory consolidation gating

---

## Key Papers

| Paper | Finding |
|-------|---------|
| Aston-Jones & Cohen 2005 | LC-NE adaptive gain theory: tonic/phasic modes for exploration/exploitation |
| Menon & Levitin 2005 | Distributed neural response to music involves NE-mediated attentional gating |
| Chanda & Levitin 2013 | Neurochemistry of music review: NE role in arousal and attention |
| McGaugh 2004 | NE and emotional memory consolidation in amygdala/hippocampus |
| Sara 2009 | LC-NE system and cognitive function: alertness, attention, memory |
| Arnsten 2011 | Inverted-U NE effect on PFC via alpha-2A / alpha-1 receptor balance |
