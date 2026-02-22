# liking -- Core Belief (SRP)

**Category**: Core (full Bayesian PE)
**tau**: 0.65
**Owner**: SRP (ARU-alpha1)
**Multi-Scale**: single-scale (terminal, v1.0 kernel)

---

## Definition

"I like this (NAcc DA + opioid)." Tracks hedonic impact -- the opioid-mediated "liking" that peaks at the consummatory moment. This is Berridge's hedonic hotspot signal: it represents in-the-moment pleasure from NAcc shell activation. Liking can exist without wanting (unexpected beauty) and is primarily mediated by mu-opioid receptors, with dopamine as a modulator.

The liking belief captures the 1-5s hedonic burst at peak musical moments, driven by convergence of ventral striatal DA and opioid release. It is the strongest single correlate of subjective musical pleasure (r=0.84, Salimpoor 2011).

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. Multi-scale extension deferred.

When activated (future):
```
T_char = 3s (consummatory burst duration)
Candidate horizons: H18(2s)  H19(3s)  H20(5s)
```

The hedonic burst operates at phrase timescale (2-5s), matching the NAcc DA peak duration observed by Salimpoor 2011 and the mu-opioid release window measured by Nummenmaa 2025.

---

## Observation Formula

```
# Terminal: computed from SRP mechanism, not direct sensory observation
# Step 1: Opioid proxy (hedonic component)
opioid_proxy = sigma(0.4*consonance_mean + 0.3*resolution_signal + 0.3*smoothness)
# where:
#   consonance_mean = mean(R3[0:7]) -> H3(H18, M0, L2) -- phrase-level consonance
#   resolution_signal = transition from dissonance to consonance
#   smoothness = R3[16] (spectral_smoothness) -> H3(H18, M15, L2)

# Step 2: NAcc DA (phasic burst at peak moments)
# da_nacc = phasic burst driven by STG->NAcc connectivity (Salimpoor 2013)

# Step 3: Liking from NAcc DA
liking = sigma(BETA_1 * da_nacc)   # BETA_1 = 0.84 (Salimpoor 2011)

# Precision: opioid_proxy * stg_nacc_coupling / (da_nacc_variance + eps)
```

---

## Prediction Formula

```
predict = tau * prev + (1-tau) * baseline + trend + periodicity + context
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). Liking has slightly higher inertia than wanting (tau=0.65 vs 0.6), reflecting the slow hedonic afterglow following peak pleasure moments (Blood & Zatorre 2001).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP P7 | liking [7] | Primary hedonic impact state |
| SRP N1 | da_nacc [1] | NAcc DA phasic burst |
| SRP N2 | opioid_proxy [2] | Mu-opioid hedonic component |
| SRP C4 | stg_nacc_coupling [4] | STG-NAcc connectivity strength |
| R3 [0:7] | consonance group | Sensory pleasantness (opioid proxy) |
| R3 [16] | spectral_smoothness | Spectral regularity (opioid proxy) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Output | Final hedonic evaluation -- in-the-moment pleasure |
| RAM | NAcc shell region activation |
| F10 Clinical | Hedonic capacity marker (anhedonia = liking absent) |
| F5 Emotion | Liking modulates emotional valence perception |

---

## Scientific Foundation

- **Salimpoor 2011**: NAcc DA release at consummation correlates with pleasure (PET, N=8, r=0.84)
- **Nummenmaa 2025**: Pleasurable music activates mu-opioid receptors in ventral striatum (PET [11C]carfentanil)
- **Mallik 2017**: Naltrexone (opioid antagonist) reduces musical emotional intensity (N=15)
- **Berridge & Kringelbach 2008**: Hedonic hotspots in NAcc shell, ventral pallidum, parabrachial nucleus
- **Ferreri 2019**: Levodopa increases subjective pleasure ratings (N=27, Z=1.968, P<0.049)
- **Blood & Zatorre 2001**: Same striatal regions respond to familiar self-selected music across repeated exposure

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
