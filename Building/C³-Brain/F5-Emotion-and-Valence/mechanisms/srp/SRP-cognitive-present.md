# SRP Cognitive Present — Psychological States (3D)

**Layer**: Cognitive Present (P)
**Indices**: [13:16]
**Scope**: exported (kernel relay)
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 13 | P0:wanting | [0, 1] | Berridge incentive salience. f13 = sigma(BETA_2 * da_caudate) where BETA_2=0.71. DA-dependent motivational "wanting" that ramps BEFORE event. Ferreri 2019: levodopa increases wanting, risperidone blocks it. Berridge 2007: wanting is computed de novo at each cue encounter. |
| 14 | P1:liking | [0, 1] | Berridge hedonic impact. f14 = sigma(BETA_1 * da_nacc) where BETA_1=0.84. Opioid + DA mediated hedonic experience that peaks AT event. Mallik 2017: naltrexone reduces emotional intensity. Berridge & Robinson 2003: dissociable from wanting. |
| 15 | P2:pleasure | [0, 1] | Composite subjective pleasure. f15 = clamp(BETA_1 * da_nacc + BETA_2 * da_caudate, 0, 1). P = 0.84*da_nacc + 0.71*da_caudate. Salimpoor 2011 coefficients directly used. Blood & Zatorre 2001: same regions respond across repeated exposure. |

---

## Design Rationale

1. **Wanting (P0)**: Berridge's incentive salience — the motivational "I want more of this" signal. Driven primarily by caudate DA (dorsal striatum). Ramps BEFORE the rewarding event, creating approach motivation. Critically dissociable from liking: you can want music you don't like (earworm you hate) and like music you didn't want (unexpected beauty). Ferreri 2019 pharmacological evidence: levodopa increases wanting, risperidone blocks it.

2. **Liking (P1)**: Berridge's hedonic impact — the in-the-moment "this feels good" signal. Driven primarily by NAcc DA (ventral striatum) + mu-opioid system. Peaks AT the rewarding event with 1-5s duration. The r=0.84 coefficient from Salimpoor 2011 PET study links NAcc binding potential to hedonic pleasure ratings.

3. **Pleasure (P2)**: The composite subjective pleasure experience that integrates both anticipatory (wanting/caudate) and consummatory (liking/NAcc) components. Uses Salimpoor 2011's exact correlation coefficients as weights. This is the primary reward output — the single-number answer to "how rewarding is this moment?" Broad temporal profile: builds during anticipation and peaks during consummation.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for the C3 kernel:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `wanting` | P0 [13] | Salience mixer: 0.35 x relay tension component |
| `liking` | P1 [14] | Reward formula: hedonic_contribution |
| `pleasure` | P2 [15] | Reward formula: 1.5 x surprise + 0.8 x resolution |

---

## Berridge Framework: Wanting vs Liking Dissociation

```
WANTING (Incentive Salience)          LIKING (Hedonic Impact)
Neurotransmitter: DOPAMINE            Neurotransmitter: mu-OPIOID + DA
Brain region: Caudate (dorsal)        Brain region: NAcc shell (ventral)
Timing: BEFORE the event             Timing: AT the event
Duration: 2-30s ramp                 Duration: 1-5s burst
Function: "I want more of this"      Function: "This feels good"
Can exist WITHOUT liking             Can exist WITHOUT wanting
Coefficient: r=0.71 (Salimpoor)      Coefficient: r=0.84 (Salimpoor)
Pharmacology: levodopa UP            Pharmacology: naltrexone DOWN
              risperidone DOWN                      levodopa UP (for music)
```

---

## H3 Dependencies (Cognitive Present)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| — | — | P-layer computes from N-layer + C-layer outputs (no direct H3 reads) |

P-layer is a pure transformation of upstream extraction outputs (da_caudate, da_nacc). All H3 dependencies flow through the N+C layer.

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| — | — | P-layer reads from N+C layer outputs only |

---

## Scientific Foundation

- **Berridge & Robinson 2003**: Wanting and liking are dissociable neural systems (review)
- **Berridge 2007**: Dopamine = incentive salience, NOT hedonic pleasure (review)
- **Salimpoor 2011**: Caudate r=0.71, NAcc r=0.84 — exact coefficients (PET, N=8)
- **Ferreri 2019**: DA causally modulates BOTH wanting AND liking in music (pharmacology, N=27)
- **Mallik 2017**: Naltrexone (opioid antagonist) reduces emotional intensity (N=15)
- **Mas-Herrero 2021**: Temporal dissociation: anticipation NAcc R2=0.47, experience R2=0.44 (TMS + fMRI, N=17)
- **Blood & Zatorre 2001**: Same reward regions respond to self-selected familiar music (PET, N=10)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/srp/cognitive_present.py`
