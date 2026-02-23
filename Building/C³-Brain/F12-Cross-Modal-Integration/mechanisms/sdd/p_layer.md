# SDD — Cognitive Present

**Model**: Supramodal Deviance Detection
**Unit**: NDU
**Function**: F12 Cross-Modal Integration
**Tier**: alpha
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | deviance_signal | Current irregularity detection state. Real-time deviance magnitude combining E-layer deviance (f01) with spectral change entropy at 1s beat timescale, reflecting the moment-to-moment strength of the supramodal deviance response. sigma(0.50 * f01 + 0.50 * change_entropy_1s). Carbajal & Malmierca 2018: the deviance signal propagates through IC -> MGB -> AC hierarchy with NMDA-dependent mechanisms at each level; the P-layer captures the instantaneous output of this cascade. |
| 7 | multilink_activation | Current cross-modal binding state. Instantaneous multilink engagement derived from temporal integration (M-layer multilinks_function) and E-layer multilink count (f02). sigma(0.50 * multilinks_function + 0.50 * f02). Captures whether the cross-modal deviance network is currently active -- high values indicate simultaneous deviance detection across multiple sensory channels. Paraskevopoulos 2022: 47 multilinks (non-musicians) vs 15 (musicians) reflects the degree of cross-network activation in the cognitive present. |
| 8 | ifg_state | Current IFG hub integration state. Real-time engagement of the central supramodal hub (IFG area 47m) derived from E-layer IFG hub activation (f04), modulated by loudness entropy at 100ms alpha capturing perceptual salience fluctuation. sigma(0.50 * f04 + 0.50 * loudness_entropy_100ms). Paraskevopoulos 2022: area 47m left is highest degree node in 5/6 network layers; Kim 2021: IFG connectivity indexes syntactic irregularity processing in real-time. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 16 | 8 | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy at 100ms alpha |

---

## Computation

The P-layer computes the real-time cognitive state of supramodal deviance detection:

1. **Deviance signal** (idx 6): The moment-to-moment deviance detection output, combining the E-layer's deviance magnitude (f01) with the spectral change entropy that drives it. This dual combination ensures that the present-moment deviance signal reflects both the computed magnitude and the raw statistical irregularity in the acoustic input. The 1s change entropy (from E-layer H3 tuple #5) provides the longer-horizon context: is the current deviance occurring within a generally predictable or unpredictable acoustic environment? Carbajal & Malmierca 2018 established that deviance detection operates as a hierarchical cascade -- the P-layer captures the output of this complete processing chain at the current moment.

2. **Multilink activation** (idx 7): The current cross-modal binding state, combining the M-layer's temporally smoothed multilinks function with the E-layer's instantaneous multilink count. This ensures that present-moment activation reflects both sustained binding (M-layer) and immediate coupling (E-layer). High multilink activation indicates that the listener's brain is currently computing cross-modal deviance relationships -- the same unexpected event is being detected across multiple sensory processing streams simultaneously.

3. **IFG state** (idx 8): The real-time engagement level of the central supramodal hub (IFG area 47m). Modulated by loudness entropy (H3) to account for perceptual salience fluctuation -- the IFG hub activates more strongly when the acoustic environment has fluctuating salience (high loudness entropy) combined with strong deviance signals. Paraskevopoulos 2022 identified area 47m as the dominant node across all network layers; this P-layer dimension tracks its moment-to-moment engagement.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_deviance_magnitude | Deviance strength for present-moment signal |
| E-layer | f02_multilink_count | Multilink level for current binding state |
| E-layer | f04_ifg_hub_activation | Hub engagement for IFG state |
| M-layer | multilinks_function | Temporally smoothed binding for stable activation |
| R3 [8] | loudness | Perceptual salience for IFG modulation |
| H3 | 1 tuple (see above) | Loudness entropy at 100ms |
