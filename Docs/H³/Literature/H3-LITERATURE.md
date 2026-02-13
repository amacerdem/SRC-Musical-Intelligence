# H3 Literature -- Annotated Bibliography

> Version 2.0.0 | Updated 2026-02-13

## Overview

This document collects the academic references that inform the design of the H3 temporal morphology layer. Each entry includes a standard citation and a brief note on its specific relevance to H3 architecture, organized by topic area. References are not exhaustive but represent the primary theoretical foundations for the horizon hierarchy, morph descriptor set, attention kernel, law system, and temporal scaling decisions.

---

## 1. Temporal Processing in Auditory Perception

**Poeppel, D.** (2003). The analysis of speech in different temporal integration windows: Cerebral lateralization as "asymmetric sampling in time." *Speech Communication*, 41(1), 245--261.
> Dual temporal integration windows at ~25-50 ms and ~200-300 ms in auditory cortex. These two scales map directly to H3 Micro band (H0-H7, 5.8-250 ms) and lower Meso band (H8-H11, 300-600 ms), providing neurophysiological support for the band boundary placement.

**Giraud, A.-L., & Poeppel, D.** (2012). Cortical oscillations and speech processing: Emerging computational principles and operations. *Nature Reviews Neuroscience*, 13(10), 694--706.
> Theta oscillations (4-8 Hz, 125-250 ms period) and gamma oscillations (25-40 Hz, 25-40 ms period) as fundamental temporal sampling rates in auditory cortex. Theta maps to H5-H7 (Micro/Meso boundary); gamma maps to H0-H3 (sub-beat Micro). The dual-oscillation framework supports the logarithmic spacing of H3 horizon frame counts.

**Ding, N., Patel, A. D., Chen, L., Butler, H., Luo, C., & Poeppel, D.** (2017). Temporal modulations in speech and music. *Neuroscience & Biobehavioral Reviews*, 81, 181--187.
> Modulation spectrum analysis reveals that speech and music share temporal modulation energy concentrated at 1-8 Hz (Meso band) with distinct profiles at faster and slower rates. Supports the dense horizon sampling in Meso (H8-H15) where perceptual sensitivity peaks.

**Lerner, Y., Honey, C. J., Silbert, L. J., & Hasson, U.** (2011). Topographic mapping of a hierarchy of temporal receptive windows using a narrated story. *Journal of Neuroscience*, 31(8), 2906--2915.
> Hierarchical temporal receptive windows in cortex ranging from <1 s in early auditory cortex to minutes in prefrontal cortex. This cortical hierarchy maps to the H3 band progression: Micro (sensory) through Ultra (integrative), with increasing window sizes corresponding to ascending cortical processing stages.

**Theunissen, F. E., & Elie, J. E.** (2014). Neural processing of natural sounds. *Nature Reviews Neuroscience*, 15(6), 355--366.
> Spectro-temporal receptive fields (STRFs) in auditory cortex encode joint spectral-temporal modulations. The separation of spectral features (R3) and temporal morphology (H3) reflects this factored representation, with H3 morphs capturing the temporal modulation axis.

---

## 2. Temporal Statistics and Morphology

**McDermott, J. H., & Simoncelli, E. P.** (2011). Sound texture perception via statistics of the auditory periphery: Evidence from sound synthesis. *Neuron*, 71(5), 926--940.
> Temporal statistics -- mean, variance, modulation power, and cross-band correlations -- are perceptually sufficient for texture recognition. Direct inspiration for H3 morph categories: M0-M7 (distribution statistics) capture the mean/variance/skewness/kurtosis substrate; M14(periodicity) captures modulation structure.

**McWalter, R., & McDermott, J. H.** (2018). Adaptive and selective time averaging of auditory scenes. *Current Biology*, 28(9), 1405--1415.
> Listeners average auditory features with exponential kernels whose time constants adapt to signal statistics. Directly supports the H3 attention kernel design `A(dt) = exp(-3|dt|/H)`, where the decay rate scales with the horizon, implementing multi-scale exponential averaging.

**Nelken, I.** (2004). Processing of complex stimuli and natural scenes in the auditory cortex. *Current Opinion in Neurobiology*, 14(4), 474--480.
> Temporal contrast and gain control in auditory cortex operate over multiple time scales. Supports the multi-horizon architecture where each horizon captures a distinct temporal contrast scale, and the morph descriptors (velocity, acceleration) quantify temporal change relative to horizon-specific baselines.

**Elhilali, M., Fritz, J. B., Chi, T. S., & Shamma, S. A.** (2007). Auditory cortical receptive fields: Stable entities with plastic abilities. *Journal of Neuroscience*, 27(39), 10372--10382.
> Cortical receptive fields have stable spectro-temporal structure but adapt their modulation preferences. The fixed H3 horizon structure (stable temporal scales) with flexible morph selection (adaptive statistical descriptors) mirrors this design principle.

---

## 3. Musical Time Perception and Hierarchy

**London, J.** (2012). *Hearing in Time: Psychological Aspects of Musical Meter* (2nd ed.). Oxford University Press.
> Metric hierarchy at multiple temporal levels (beat, measure, phrase, section) with inter-level coupling. Maps to H3 bands: beat subdivisions (Micro), beat period (Meso), measure/phrase (Macro), large-scale form (Ultra). London's "metric well-formedness" constraints inform why certain horizons cluster around perceptually privileged durations.

**Fraisse, P.** (1982). Rhythm and tempo. In D. Deutsch (Ed.), *The Psychology of Music* (1st ed., pp. 149--180). Academic Press.
> Preferred tempo range of 500-700 ms and preferred subdivision ratios. The H9 horizon (69 frames = ~400 ms) and H10 (86 frames = ~500 ms) straddle the preferred beat period, placing the densest H3 sampling at the perceptual tempo sweet spot.

**Drake, C., & Botte, M.-C.** (1993). Tempo sensitivity in auditory sequences: Evidence for a multiple-look model. *Perception & Psychophysics*, 54(3), 277--286.
> Weber fraction for tempo discrimination ~5%, decreasing with multiple observations. Relevant to M2(std) and M8(velocity) on rhythmic R3 features at Meso horizons: these morphs quantify the variability that the perceptual system is sensitive to detecting.

**Lerdahl, F., & Jackendoff, R.** (1983). *A Generative Theory of Tonal Music*. MIT Press.
> Hierarchical metric and grouping structure from surface to deep levels. The H3 hierarchy is a computational realization of the grouping hierarchy: Micro captures note-level grouping, Meso captures metric grouping, Macro captures phrase/section grouping, Ultra captures large-scale form.

**Palmer, C., & Krumhansl, C. L.** (1990). Mental representations for musical meter. *Journal of Experimental Psychology: Human Perception and Performance*, 16(4), 728--741.
> Hierarchical mental representations of musical meter with periodic reinforcement at multiple levels. Supports M14(periodicity) and M17(shape_period) morphs, which quantify periodic structure at each horizon level.

---

## 4. Temporal Attention and Memory

**Jones, M. R.** (1976). Time, our lost dimension: Toward a new theory of perception, attention, and memory. *Psychological Review*, 83(5), 323--355.
> Dynamic attending theory: temporal attention operates as oscillatory resonance at preferred rates, with attention strength decaying as a function of temporal distance from expected events. Foundational for the H3 law system, where L0 (memory) attends backward, L1 (prediction) attends forward, and L2 (integration) attends symmetrically.

**Large, E. W., & Jones, M. R.** (1999). The dynamics of attending: How people track time-varying events. *Psychological Review*, 106(1), 119--159.
> Oscillatory model of dynamic attending with exponential decay in attention strength as temporal distance increases. Direct mathematical foundation for the attention kernel `A(dt) = exp(-3|dt|/H)`, where the oscillator period corresponds to the horizon and the decay constant (3.0) sets the boundary weight.

**Baddeley, A.** (2003). Working memory: Looking back and looking forward. *Nature Reviews Neuroscience*, 4(10), 829--839.
> Phonological loop capacity of ~2 s constrains sequential auditory processing. The Meso/Macro band boundary at H15 (345 frames = ~2 s) corresponds to this working memory limit, beyond which processing shifts from sequential to integrative.

**Nobre, A. C., & van Ede, F.** (2018). Anticipated moments: Temporal structure in attention. *Nature Reviews Neuroscience*, 19(1), 34--48.
> Temporal expectations guide attention at multiple scales. The H3 law system differentiates between retrospective (L0), prospective (L1), and integrated (L2) temporal attention, corresponding to distinct neural mechanisms for temporal expectation.

---

## 5. Predictive Coding and Temporal Prediction

**Friston, K.** (2005). A theory of cortical responses. *Philosophical Transactions of the Royal Society B*, 360(1456), 815--836.
> Free energy principle: cortical processing minimizes prediction error at multiple temporal scales through hierarchical generative models. Foundational for the L1 (Prediction) law and the multi-horizon architecture, where each horizon level maintains predictions at its characteristic time scale.

**Clark, A.** (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181--204.
> Hierarchical predictive processing with temporal depth: higher levels make slower, more abstract predictions. Maps to the H3 band hierarchy where Ultra-band predictions (MEM, TMH mechanisms) operate at abstract section/piece scales while Micro-band predictions (PPC, ASA) operate at immediate sensory scales.

**Koelsch, S., Vuust, P., & Friston, K.** (2019). Predictive processes and the peculiar case of music. *Trends in Cognitive Sciences*, 23(1), 63--77.
> Predictive coding applied to music: temporal prediction at beat, phrase, and section levels with distinct prediction error signatures. Directly supports the PCU (Predictive Coding Unit) mechanism assignments: PPC at Micro, TPC at cross-band, and C0P at Macro horizons.

**Pearce, M. T.** (2005). *The construction and evaluation of statistical models of melodic structure in music perception and composition*. PhD thesis, City University London.
> IDyOM (Information Dynamics of Music): statistical learning generates expectations for melodic continuation based on sequential probabilities. Foundation for I-group R3 features (information_rate, predictive_entropy) and their temporal morphology at phrase-level horizons (H12-H16).

**Vuust, P., Dietz, M. J., Witek, M., & Kringelbach, M. L.** (2018). Now you hear it: A predictive coding model for understanding rhythmic incongruity. *Annals of the New York Academy of Sciences*, 1423(1), 19--29.
> Rhythmic prediction error at multiple metric levels. Supports the STU and MPU mechanism designs where BEP (Beat-Entrained Prediction) operates at Micro-Meso horizons tracking beat-level prediction errors.

---

## 6. Exponential Decay Kernels

**Hawkes, A. G.** (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83--90.
> Exponential decay kernels `k(t) = alpha * exp(-beta * t)` in self-exciting temporal point processes. Theoretical foundation for the H3 attention kernel form, where the decay parameter `beta = 3/H` scales with the horizon to maintain consistent boundary weighting (~4.98%) across all temporal scales.

**Ogata, Y.** (1988). Statistical models for earthquake occurrences and residual analysis for point processes. *Journal of the American Statistical Association*, 83(401), 9--27.
> Self-exciting processes with exponential decay parameterized by characteristic time scales. The H3 attention kernel extends this framework to multi-scale temporal analysis, where each horizon defines a distinct decay scale with `H` as the characteristic time.

**Tsodyks, M. V., & Markram, H.** (1997). The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability. *Proceedings of the National Academy of Sciences*, 94(2), 719--723.
> Synaptic depression with exponential recovery time constants. Provides biophysical grounding for the exponential attention kernel: neural temporal integration follows exponential decay dynamics with time constants matching the H3 horizon durations.

---

## 7. Temporal Resolution and Window Functions

**Allen, J. B.** (1977). Short term spectral analysis, synthesis, and modification by discrete Fourier transform. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 25(3), 235--238.
> Uncertainty principle: time resolution and frequency resolution trade off inversely. In H3, small horizons (Micro) achieve fine temporal resolution but limited statistical reliability, while large horizons (Ultra) achieve robust statistics but coarse temporal resolution. This tradeoff is quantified in the MorphQualityTiers framework.

**Oppenheim, A. V., & Schafer, R. W.** (2009). *Discrete-Time Signal Processing* (3rd ed.). Pearson.
> Window function design: exponential windows (matching the H3 attention kernel) have specific sidelobe characteristics and mainlobe widths. The exponential kernel's 6-dB bandwidth is inversely proportional to the horizon, giving each horizon a distinct temporal selectivity profile.

**Harris, F. J.** (1978). On the use of windows for harmonic analysis with the discrete Fourier transform. *Proceedings of the IEEE*, 66(1), 51--83.
> Comprehensive comparison of window functions. The exponential window used in H3 has moderate sidelobe suppression (~13 dB) but optimal noise bandwidth for real-time temporal averaging, supporting the design choice over Hann, Hamming, or Blackman alternatives.

---

## 8. Information Theory and Temporal Dynamics

**Shannon, C. E.** (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379--423.
> Shannon entropy `H = -SUM(p * log(p))` as a measure of information content and uncertainty. Foundation for M20(entropy), which quantifies the information content of the windowed R3 feature distribution at each horizon. Higher entropy indicates more uniform (less predictable) temporal behavior.

**Wiener, N.** (1949). *Extrapolation, Interpolation, and Smoothing of Stationary Time Series*. MIT Press.
> Optimal linear prediction and temporal smoothing of stochastic processes. Foundation for M15(smoothness), which measures the predictability of the R3 feature trajectory within the attention window. Also relates to the L1 (Prediction) law's forward-looking attention design.

**Dubnov, S.** (2004). Generalization of spectral flatness measure for non-Gaussian linear processes. *IEEE Signal Processing Letters*, 11(8), 698--701.
> Information rate in audio as a generalization of spectral flatness. Relevant to the I-group R3 features (information_rate, spectral_flatness) and their H3 temporal morphology, where information rate at multiple horizons captures the multi-scale predictability structure of audio.

**Abdallah, S. A., & Plumbley, M. D.** (2009). Information dynamics: Patterns of expectation and surprise in the perception of music. *Connection Science*, 21(2-3), 89--117.
> Information-theoretic framework for musical expectation: surprisal and entropy at multiple temporal resolutions. Supports the I-group feature design and the choice of M0(value), M1(mean), and M18(trend) as primary morphs for information features, capturing instantaneous surprise, average predictability, and predictability trajectory.

**Cover, T. M., & Thomas, J. A.** (2006). *Elements of Information Theory* (2nd ed.). Wiley.
> Entropy rate of stochastic processes, conditional entropy, and mutual information. Provides the mathematical framework for temporal entropy computations in M20, where entropy is computed over discretized (8-bin) windowed distributions with consistent bin widths across horizons.

---

## 9. Cross-References

| Related Document | Location |
|-----------------|----------|
| H3 architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Horizon catalog | [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md) |
| Morph catalog | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| Law catalog | [../Registry/LawCatalog.md](../Registry/LawCatalog.md) |
| Attention kernel contract | [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md) |
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| Literature index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial annotated bibliography (Phase 4H) |
