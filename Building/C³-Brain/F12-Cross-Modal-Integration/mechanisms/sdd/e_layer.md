# SDD — Extraction

**Model**: Supramodal Deviance Detection
**Unit**: NDU
**Function**: F12 Cross-Modal Integration
**Tier**: alpha
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_deviance_magnitude | Statistical irregularity strength. Driven by spectral change entropy at 1s beat timescale (capturing long-term regularity violations) and roughness entropy at 100ms alpha (capturing fast sensory dissonance fluctuation). sigma(0.35 * change_entropy_1s + 0.35 * flux_std_100ms + 0.30 * roughness_entropy). Paraskevopoulos 2022: supramodal deviance networks show significantly more multilinks than standard networks. Carbajal & Malmierca 2018: SSA and MMN are micro/macroscopic manifestations of the same deviance detection mechanism along IC to MGB to AC hierarchy (NMDA-dependent). |
| 1 | f02_multilink_count | Cross-network edge correlations reflecting supramodal binding. Driven by cross-band coupling variability at 100ms alpha (fluctuating coupling = active multilinks) and cross-level integration at the same timescale. sigma(0.35 * coupling_std_100ms + 0.35 * integration_100ms + 0.30 * flux_periodicity_1s). Paraskevopoulos 2022: non-musicians show 47 multilinks across deviance networks vs 15 for musicians (p < 0.001 FDR). |
| 2 | f03_supramodal_index | Cross-modal integration ratio capturing the degree to which deviance detection operates across modalities rather than within single modalities. Multiplicative interaction of deviance magnitude and multilink count, modulated by integration periodicity and loudness entropy. sigma(0.40 * f01 * f02 + 0.30 * integration_periodicity_1s + 0.30 * loudness_entropy). Paraskevopoulos 2022: deviance multilinks > standard multilinks, confirming supramodal mechanism. |
| 3 | f04_ifg_hub_activation | Central hub engagement indexing IFG (area 47m) activation as the dominant node across network layers. Driven by deviance magnitude and multilink count. sigma(0.35 * f01 + 0.35 * f02 + 0.30 * amplitude_100ms). Paraskevopoulos 2022: area 47m left is highest node degree in 5/6 network layers. Kim 2021: IFG-LTDMI enhanced for syntactic irregularity F(2,36)=6.526, p=0.024. Porfyri 2025: left IFJa/IFJp are central neuroplasticity hubs (p < 0.001 FDR). |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 0 | M0 (value) | L2 (bidi) | Instantaneous deviance at 25ms gamma |
| 1 | 10 | 1 | M1 (mean) | L2 (bidi) | Mean deviance over 50ms gamma |
| 2 | 10 | 3 | M2 (std) | L2 (bidi) | Deviance variability at 100ms alpha |
| 3 | 21 | 3 | M0 (value) | L2 (bidi) | Spectral change at 100ms alpha |
| 4 | 21 | 4 | M8 (velocity) | L0 (fwd) | Change velocity at 125ms theta |
| 5 | 21 | 16 | M20 (entropy) | L2 (bidi) | Change entropy at 1s beat |
| 6 | 22 | 3 | M0 (value) | L2 (bidi) | Energy change at 100ms alpha |
| 7 | 22 | 3 | M2 (std) | L2 (bidi) | Energy variability at 100ms alpha |
| 8 | 0 | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms alpha |
| 9 | 0 | 3 | M20 (entropy) | L2 (bidi) | Roughness entropy at 100ms alpha |
| 10 | 7 | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms alpha |
| 11 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms alpha |
| 12 | 25 | 3 | M0 (value) | L2 (bidi) | Cross-band coupling at 100ms alpha |
| 13 | 25 | 3 | M2 (std) | L2 (bidi) | Coupling variability at 100ms alpha |

---

## Computation

The E-layer extracts four explicit features characterizing supramodal deviance detection:

1. **Deviance magnitude** (f01): The primary irregularity strength signal. Driven by spectral change entropy over the 1s beat timescale (capturing whether the pattern of spectral changes itself is unpredictable, not merely whether spectral flux is high) and roughness entropy at 100ms (capturing fluctuation in sensory dissonance). Entropy measures are used rather than raw values because deviance detection responds to statistical irregularity -- departures from learned regularity patterns -- not to absolute signal magnitude. This aligns with predictive coding models (Carbajal & Malmierca 2018) where the auditory neuraxis from IC to MGB to AC maintains hierarchical predictions, and deviance is the mismatch between prediction and observation.

2. **Multilink count** (f02): Indexes the cross-network edge correlations that define supramodal binding. Cross-band coupling variability (std of x_l0l5 at 100ms) captures fluctuating inter-feature correlations that indicate active multilinks -- when coupling variability is high, the system is actively computing cross-modal relationships. Cross-level integration (x_l5l7 at 100ms) captures the supramodal binding across feature hierarchies. Paraskevopoulos 2022 found 47 multilinks in non-musicians vs 15 in musicians, indicating that musical expertise compartmentalizes deviance networks into more specialized, less cross-coupled modules.

3. **Supramodal index** (f03): The cross-modal integration ratio, computed as a multiplicative interaction of deviance magnitude and multilink count. This multiplicative gating ensures that high supramodal index requires both strong deviance detection AND active cross-modal binding -- neither alone is sufficient. Modulated by integration periodicity at 1s (capturing regular cross-modal binding patterns) and loudness entropy at 100ms (capturing perceptual salience fluctuation). This maps to the finding that deviance networks show stronger between-network correlation than standard networks.

4. **IFG hub activation** (f04): Indexes the engagement of the central supramodal hub, identified as IFG area 47m (left) by Paraskevopoulos 2022. This region had the highest node degree in 5 of 6 network layers, confirming its role as the convergence point for cross-modal deviance information. Driven by both deviance magnitude and multilink count, reflecting that the IFG hub activates proportionally to both the strength of the irregularity and the degree of cross-modal engagement. Kim 2021 confirmed that IFG connectivity specifically indexes syntactic (structural) irregularity, dissociable from perceptual ambiguity (which maps to STG).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [0] | roughness | Sensory dissonance for deviance detection |
| R3 [7] | amplitude | Intensity changes for deviance magnitude |
| R3 [8] | loudness | Perceptual loudness for attention capture and entropy |
| R3 [10] | spectral_flux | Frame-to-frame spectral change for deviance |
| R3 [21] | spectral_change | Rate of spectral change for statistical irregularity |
| R3 [22] | energy_change | Dynamic contrast for energy deviation |
| R3 [25:33] | x_l0l5 | Cross-band coupling for multilink computation |
| H3 | 14 tuples (see above) | Multi-scale deviance tracking, entropy, coupling variability |
