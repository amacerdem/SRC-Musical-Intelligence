# Dopamine (DA) -- Mesolimbic Reward and Anticipatory Signalling

> **Code**: `mi_beta/brain/neurochemicals/dopamine.py`
> **NeurochemicalType**: `DOPAMINE`
> **Manager methods**: `write_da()`, `read_da()`, `da_keys`

## Overview

Dopamine is THE central neurochemical for musical reward. Two distinct DA subsystems operate in parallel during music listening:

1. **Anticipatory DA** (caudate/dorsal striatum): Released 10-15 seconds BEFORE peak pleasure. Encodes expected future reward based on learned musical expectations. Correlates with "wanting" / motivation (Salimpoor 2011, r=0.71).

2. **Consummatory DA** (NAcc/ventral striatum): Released AT the moment of peak pleasure. Encodes experienced hedonic value. Correlates with "liking" (Salimpoor 2011, r=0.84).

3. **VTA drive**: Dopaminergic cell bodies fire in response to reward prediction error (RPE) -- bursts for better-than-expected, pauses for worse-than-expected (Schultz 1997).

---

## Region Specifications (`DA_REGIONS`)

| Region Key | Full Name | Pathway | Role | Citation |
|------------|-----------|---------|------|----------|
| `caudate` | Caudate Nucleus | nigrostriatal / mesolimbic overlap | Anticipatory reward; DA release peaks 10-15s before consummatory pleasure, encoding expected future reward value | Salimpoor 2011, r=0.71 |
| `nacc` | Nucleus Accumbens | mesolimbic | Consummatory pleasure; DA release at peak hedonic moments encodes experienced reward magnitude | Salimpoor 2011, r=0.84 |
| `vta` | Ventral Tegmental Area | mesolimbic (origin) | DA cell body source; phasic firing encodes reward prediction error (RPE) -- bursts for positive surprise, pauses for negative surprise | Schultz 1997; Ferreri 2019 |

---

## Tonic vs Phasic Classification

**Phasic threshold**: `DA_PHASIC_THRESHOLD = 0.6`

| Classification | Value Range | DA Mode | Meaning |
|---------------|-------------|---------|---------|
| Tonic | `< 0.6` | Sustained background | Slow baseline encoding average expected reward in current musical context. Modulates sensitivity to phasic bursts (Niv 2007) |
| Phasic | `>= 0.6` | Transient burst | Fast event-locked bursts encoding reward prediction error -- difference between received and expected reward (Schultz 1997) |

Helper functions:
- `is_tonic(value: float) -> bool` -- returns `True` if below threshold
- `is_phasic(value: float) -> bool` -- returns `True` if at or above threshold

Normalised [0, 1] scale where 0.5 = expected reward level.

---

## Reference Values from Literature (`DA_REFERENCE_VALUES`)

These anchors enable calibration of the deterministic DA model. Computed DA values should reproduce the relative ordering and approximate magnitude of empirical observations.

| Description | Region | Normalised Value | Original Metric | Citation |
|-------------|--------|-----------------|-----------------|----------|
| Peak anticipatory DA during chill-inducing music | caudate | 0.78 | BP_ND decrease 5.7% vs neutral (p<0.003) | Salimpoor 2011 |
| Peak consummatory DA at chill moment | nacc | 0.88 | BP_ND decrease 8.4% vs neutral (p<0.001) | Salimpoor 2011 |
| DA during neutral (non-preferred) music | nacc | 0.35 | Baseline BP_ND (no significant change) | Salimpoor 2011 |
| DA enhancement (levodopa) increases pleasure rating | nacc | 0.92 | Pleasure rating +14.7% vs placebo (p=0.017) | Ferreri 2019 |
| DA blockade (risperidone) decreases pleasure | nacc | 0.28 | Pleasure rating -10.2% vs placebo (p=0.033) | Ferreri 2019 |
| Anticipatory caudate response during familiar excerpt | caudate | 0.70 | Temporal dissociation: caudate peaks before NAcc | Zatorre & Salimpoor 2013 |

---

## Interaction with Other Systems

- **Opioid**: DA "wanting" and opioid "liking" are dissociable (Berridge 2003). DA drives anticipation; opioids drive hedonic impact. Both converge in NAcc.
- **Serotonin**: 5-HT2C receptors on VTA neurons inhibit DA release; 5-HT1B on NAcc terminals facilitate DA. Mood state (5-HT) gates reward sensitivity (DA).
- **Norepinephrine**: LC phasic bursts can trigger VTA DA phasic responses. Arousal (NE) gates reward sensitivity (DA). Unexpected events -> NE burst -> enhanced DA RPE.

---

## Models That Write/Read DA

**Writers** (models that produce DA signals):
- ARU models (SRP, AAC) -- write `da_caudate`, `da_nacc`, `da_vta`

**Readers** (models that consume DA signals):
- ARU models (AAC, VMM) -- read DA for affect computation
- PCU, RPU models -- read DA for reward-related processing

---

## Key Papers

| Paper | Finding |
|-------|---------|
| Salimpoor et al. 2011 | PET [11C]raclopride: DA release in caudate (anticipation) and NAcc (consummation) during music |
| Ferreri et al. 2019 | Causal link: levodopa enhances, risperidone diminishes musical pleasure |
| Zatorre & Salimpoor 2013 | Review of reward, prediction, and DA in music |
| Berridge 2003 | Wanting vs liking dissociation framework |
| Schultz 1997 | Reward prediction error theory of DA neuron firing |
