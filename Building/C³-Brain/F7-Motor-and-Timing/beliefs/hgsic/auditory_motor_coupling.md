# auditory_motor_coupling -- Appraisal Belief (HGSIC)

**Category**: Appraisal (observe-only)
**Owner**: HGSIC (STU-beta5)

---

## Definition

"Auditory-motor coupling tight/loose." Observes the strength of coupling between auditory processing in pSTG and motor preparation in premotor/motor cortex via the dorsal auditory-motor pathway. High values indicate tight coupling -- the auditory signal efficiently drives motor system activation with minimal lag. The 110ms propagation delay from pSTG to motor cortex (r=0.70) is the characteristic timescale of this coupling.

---

## Observation Formula

```
# From HGSIC M-layer:
auditory_motor_coupling = HGSIC.coupling_strength[M1]  # index [4]

# coupling_strength = sigma(0.50 * amp_smoothness * energy_periodicity)
# amp_smoothness = H3 (7, 16, 15, 0)  -- amplitude smoothness at 1s
# energy_periodicity = H3 (22, 11, 14, 2)  -- energy periodicity at 500ms
```

No prediction -- observe-only appraisal. The value quantifies current auditory-to-motor signal transfer efficiency.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HGSIC M1 | coupling_strength [4] | Auditory-motor coupling magnitude |
| H3 | (7, 16, 15, 0) | Amplitude smoothness at H16 (1s bar level) |
| H3 | (22, 11, 14, 2) | Energy change periodicity at H11 (500ms motor level) |

---

## Kernel Usage

The auditory_motor_coupling appraisal serves two roles:

1. **groove_quality input**: coupling_strength contributes 20% weight to groove observe()
2. **F8 Learning feed**: coupling strength modulates sensorimotor learning rate

```python
# groove_quality observe():
# 0.50*groove_index + 0.30*f03 + 0.20*coupling_strength
```

---

## Scientific Foundation

- **Potes et al. 2012**: Auditory-motor cross-correlation r=0.70 at 110ms lag; dorsal stream propagation (ECoG, N=4 motor electrodes)
- **Grahn & Brett 2007**: SMA Z=5.03, premotor PMd Z=5.30/5.24 for beat rhythms (fMRI, N=27)
- **Thaut et al. 2009b**: Distinct cortico-cerebellar activations in rhythmic auditory-motor synchronization (fMRI, N=12)
- **Zatorre et al. 2007**: Auditory-motor circuit architecture for rhythm processing (Review, Nature Rev Neurosci)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
