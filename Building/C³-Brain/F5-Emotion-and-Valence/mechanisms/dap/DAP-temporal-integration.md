# DAP D-Layer — Temporal Integration (4D)

**Layer**: Developmental Markers (D)
**Indices**: [1:5]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 1 | D0:critical_period | [0, 1] | Critical period indicator. Equals plasticity coefficient — high for ages 0-5, exponentially declining thereafter. P(age) = P_max * exp(-age / tau_critical), tau_critical ~ 5 years. Trainor 2012: musical training before age 7 produces lasting structural changes. |
| 2 | D1:plasticity_coeff | [0, 1] | Age-adjusted learning rate for affect circuits. plasticity = 1.0 - maturation. Inversely tracks neural maturation — high plasticity = still in critical period, low plasticity = mature circuits. Qiu 2025: prenatal musical intervention increases dendritic complexity in mPFC/amygdala. |
| 3 | D2:exposure_history | [0, 1] | Musical enrichment proxy estimated from response characteristics. Inferred from the strength and variability of the hedonic response to music — enriched individuals show stronger, more differentiated responses. Nguyen 2023: early social communication through music shapes affective development. |
| 4 | D3:neural_maturation | [0, 1] | Myelination + synaptic pruning index. High = mature (post-critical period). Tracks the completion of auditory-limbic pathway development. Mature circuits have stable, efficient connections but reduced plasticity for new associations. Scholkmann 2024: preterm infants show distinct immature response patterns. |

---

## Design Rationale

1. **Critical Period (D0)**: Binary-like indicator of whether the listener is within the auditory-affective critical period. Based on the exponential decay model of neural plasticity with a time constant of approximately 5 years. During the critical period, musical exposure has maximal impact on forming permanent auditory-limbic connections.

2. **Plasticity Coefficient (D1)**: The current capacity for new auditory-affective learning. Computed as the complement of neural maturation (1 - maturation). This captures the well-established principle that neural plasticity decreases with development — young brains form new connections readily, while mature brains are more resistant to modification.

3. **Exposure History (D2)**: An indirect estimate of prior musical enrichment. Since we cannot directly observe developmental history from audio alone, this is inferred from the quality and variability of the listener's hedonic response patterns. Enriched exposure produces more differentiated, stronger responses to musical features.

4. **Neural Maturation (D3)**: Tracks the completion of auditory-limbic circuit development. Combines myelination progress (conduction efficiency) and synaptic pruning (circuit refinement). High maturation indicates stable adult-like processing but reduced capacity for new affective learning.

---

## H3 Dependencies (D-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Response strength — maturation marker |
| (4, 16, 2, 2) | sensory_pleasantness std H16 L2 | Response variability — plasticity indicator |
| (22, 16, 20, 2) | entropy entropy H16 L2 | Predictability — learned pattern depth |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | D0/D1: consonance discrimination maturity |
| [4] | sensory_pleasantness | D2: hedonic response strength for exposure estimation |
| [22] | distribution_entropy | D3: predictability as pattern acquisition depth |
| [25:33] | x_l0l5 | D2: energy-consonance affective learning pattern |

---

## Scientific Foundation

- **Trainor & Unrau 2012**: Musical training before age 7 produces lasting structural changes in auditory cortex (review, Springer Handbook)
- **Scholkmann et al. 2024**: Preterm infants show 2 distinct immature response patterns to music; sex differences in cerebral oxygenation (fNIRS, N=17)
- **Qiu et al. 2025**: Prenatal musical intervention increases dendritic complexity in mPFC/amygdala, upregulates MAP2 (mouse model, Translational Psychiatry)
- **Nguyen et al. 2023**: Early social communication through music shapes affective bonding and development (review, Developmental Cognitive Neuroscience)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/dap/temporal_integration.py`
