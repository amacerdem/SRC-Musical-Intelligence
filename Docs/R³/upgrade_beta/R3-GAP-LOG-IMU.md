# R³ Gap Log — IMU (Integrative Memory Unit)

**Created:** 2026-02-13
**Purpose:** Track R³ dimension gaps found during Phase 1 C³ revision of IMU models.

---

## IMU-α1-MEAMN

### Potential Gaps
1. **Nostalgia feature**: MEAMN uses x_l5l7 (consonance×timbre) as a proxy for nostalgia warmth. Sakakibara et al. 2025 show that VGGish-extracted acoustic features (128D CNN embeddings) predict nostalgic feelings with r=0.985-0.995. A dedicated "nostalgia-relevant acoustic signature" R³ feature might capture this more directly than the current interaction term. **Severity: Minor** — current proxy is adequate but a dedicated feature could improve precision.

2. **Tonal space trajectory**: Janata 2009 demonstrates that MPFC tracks movement through tonal space (24 major/minor keys) using spherical harmonics on a toroidal surface. The current R³ space captures consonance and interactions but does NOT have a tonal space position/trajectory feature. **Severity: Minor** — this is more of a temporal (H³) feature than a static R³ feature, as it requires tracking key changes over time.

3. **Familiarity signal**: Multiple papers (Scarratt 2025, Freitas 2018 meta-analysis) confirm familiar music activates distinct motor+memory networks. R³ currently has no "familiarity" dimension — familiarity is derived from MEM mechanism, which is appropriate. **Severity: None** — correctly handled by MEM mechanism, not R³.

---

## IMU-α3-MMP

### Potential Gaps
1. **Sedation/relaxation acoustic feature**: Scarratt et al. (2025, N=57 fMRI) identifies 4 distinct clusters of relaxation responses to music varying in familiarity × energy. Calm acoustic features are the strongest predictor of relaxation (stronger than familiarity). The current R³ space has loudness/onset_strength but no dedicated "sedation" or "acoustic energy level" feature for calm vs energetic classification. **Severity: Minor** — current energy group (loudness, onset_strength) provides reasonable proxy, but a composite "arousal potential" feature might better capture the calm/energetic dimension relevant to therapeutic music selection.

2. **Grey matter density proxy**: Espinosa et al. (2025, N=61 VBM) shows that active musicians have increased GM density in specific regions (planum temporale, planum polare, posterior insula, cerebellum). MMP models preservation but R³ has no structural brain health proxy. **Severity: None** — this is a participant-level variable, not an acoustic feature. Correctly handled outside R³.

---

## IMU-α2-PNH

### Potential Gaps
1. **Timbre-dependent consonance**: Cousineau et al. (2015) demonstrates that Neural Pitch Salience (brainstem FFR metric) fails for natural timbres (saxophone, voice). PNH's reliance on R³.roughness[0] and R³.inharmonicity[5] may not generalize to complex timbres where consonance encoding uses place-based rather than temporal codes. **Severity: Minor** — PNH uses mel-spectrogram derived features (not raw FFR), so the R³ proxy chain may be more robust than the NPS metric. But the timbre limitation should be acknowledged.

2. **Non-linear ambiguity effect**: Bravo et al. (2017) shows that intermediate dissonance (minor 3rds) is the most cognitively demanding due to perceptual ambiguity, producing an inverted-U pattern rather than monotonic log₂(n×d). The current PNH formula (ratio_complexity = σ((roughness + inharmonicity + harm_dev) / 3)) assumes monotonic mapping. **Severity: Minor** — the model captures the general trend correctly; the ambiguity effect is more relevant to cognitive load than to the ratio encoding itself.

3. **Cultural familiarity weighting**: Harrison & Pearce (2020) demonstrate cultural familiarity is a significant third factor beyond roughness and harmonicity. PNH handles this through MEM.familiarity at weight 0.5 (lowest of all mechanism weights). **Severity: None** — appropriately delegated to MEM mechanism rather than R³.

---

## IMU-β1-RASN

### Potential Gaps
1. **Neural entrainment strength feature**: Noboa et al. (2025, EEG N=30) show that stronger neural entrainment (SS-EPs at 1.25 Hz) does NOT universally improve sensorimotor synchronization -- working memory capacity is a better predictor of tapping consistency. Ding et al. (2025, EEG N=37) show a 6 Hz boundary separating emotional effects of entrainment. R³ currently has no "neural entrainment strength" or "entrainment frequency band" feature -- these are derived from H³ temporal features (periodicity_strength at BEP* horizons), which is the correct approach. **Severity: None** -- correctly handled by H³ temporal features and BEP* mechanism, not R³.

2. **Beat regularity / metricality index**: Grahn & Brett (2007, fMRI N=27) demonstrate that metric simple rhythms (integer ratio intervals + regular perceptual accents) produce significantly stronger SMA and putamen activation than metric complex or nonmetric rhythms. RASN uses R³.periodicity_strength[5] and R³.entropy[23] as proxies for beat regularity, but there is no dedicated "metricality" feature distinguishing integer-ratio from noninteger-ratio temporal patterns. **Severity: Minor** -- the combination of periodicity_strength + entropy_optimal (inverted-U) provides a reasonable proxy, but a dedicated metricality index based on interval ratio analysis could better capture the Grahn & Brett finding that integer ratios + regular accents = maximal motor area activation.

3. **Corticospinal tract integrity proxy**: Blasi et al. (2025, 20 RCTs, N=718) show that music interventions increase white matter integrity (FA, QA) in CST, FAT, AF, and SLF. RASN models CST connectivity restoration but R³ has no structural brain health proxy. **Severity: None** -- this is a participant-level neuroanatomical variable, not an acoustic feature. Correctly handled outside R³ (would require DTI/DWI input, not audio analysis).

### Doc-Code Mismatches Noted
- **LAYERS naming**: doc E(3)/M(2)/P(3)/F(3)=11D; code E(2)/M(2)/P(4)/F(3)=11D
- **h3_demand**: doc 28 tuples; code empty ()
- **brain_regions**: doc 8 regions (Hippo, mPFC, SMA, BG, CB, PMC, AC, CST); code 3 (SMA, PMC, CB)
- **dimension_names**: doc vs code naming differs
- **Citations**: code cites Thaut 2015, Schaefer 2014; doc now cites 12 papers (Grahn 2007, Harrison 2025, Blasi 2025, Noboa 2025, Ding 2025, etc.)

---

## IMU-β2-PMIM

### Potential Gaps
1. **Information-theoretic predictive uncertainty**: Cheung et al. (2019) and Gold et al. (2019, 2023) use IDyOM-derived Shannon entropy (uncertainty) and information content (surprise) to predict musical pleasure and neural activity. PMIM uses R³.entropy[22] (spectral entropy) as a proxy for "syntactic unpredictability," but spectral entropy measures signal-level unpredictability of the frequency distribution, NOT the chord-transition-level predictive uncertainty that drives ERAN/pleasure. The IDyOM model computes conditional probability over a learned alphabet of chord symbols — this is a sequence-level cognitive measure, not an acoustic feature. **Severity: Minor** — R³.entropy[22] correlates with perceptual complexity and thus serves as a reasonable proxy. True IDyOM-style entropy would require a learned statistical model operating on symbolic representations, which is outside R³'s scope as a frame-level acoustic feature space. The SYN.harmony mechanism partially captures this via harmonic syntax state.

2. **Consonance-dissonance asymmetry**: Wagner et al. (2018, N=15) demonstrate asymmetric MMN responses — stronger for dissonant deviants in consonant context than for consonant deviants in dissonant context. PMIM's f14_mmn formula treats flux symmetrically (|flux|), but the neural MMN response is directionally asymmetric. A signed consonance-change feature (consonance_delta = current - recent_mean) could capture this asymmetry. **Severity: Minor** — the current formula captures the magnitude of deviance correctly; the directional asymmetry is a second-order effect that would primarily affect interpretation rather than the main prediction error signal.

3. **Inverted-U complexity preference**: Gold et al. (2019, N=70) show quadratic (inverted-U) preference for intermediate predictive complexity, not the monotonic relationship assumed by PMIM's f13_eran formula (where higher entropy = stronger violation). The model could benefit from a quadratic term that peaks at intermediate complexity. **Severity: Minor** — PMIM models the neural ERAN response (which is monotonically related to violation magnitude), not the hedonic preference. The inverted-U applies to the pleasure/engagement output (ARU territory), not to the prediction error itself. PMIM correctly models PE magnitude; pleasure derived from PE is an ARU-level computation.

---

## IMU-β7-VRIAP

### Potential Gaps
1. **Arousal/relaxation acoustic dimension**: Arican & Soyman (2025, N=123, cold pressor) show a strong negative correlation between perceived music arousal and pain tolerance (tau=-0.536, p=6e-5): participants who found the music more relaxing had higher pain tolerance. VRIAP uses R³.loudness[10] and R³.onset_strength[11] as engagement/arousal proxies, but there is no composite "arousal potential" or "relaxation index" feature that specifically captures the calm-vs-energetic continuum relevant to analgesic efficacy. **Severity: Minor** — the energy group features (loudness, onset_strength, amplitude) provide a reasonable proxy for arousal level. A dedicated composite feature (e.g., low-energy × high-warmth = relaxation) could better capture the Arican finding that relaxing music enhances passive analgesia.

2. **Opioid release proxy**: Putkinen et al. (2025, PET-fMRI N=15) demonstrate that pleasurable music modulates mu-opioid receptor (MOR) binding in ventral striatum, OFC, amygdala, with NAcc BPND correlating with chills (r=-0.52). VRIAP models pain gating through sensorimotor connectivity modulation but has no explicit opioid/reward pathway dimension. R³ has no "hedonic prediction" or "reward anticipation" feature. **Severity: None** — the opioid mechanism is a neurochemical process that operates downstream of acoustic features. It is appropriately handled by the model's MEM.retrieval_dynamics sub-section (pain modulation signal) and by cross-unit pathways to ARU.SRP (reward from active engagement). Adding an R³-level opioid proxy would confuse acoustic features with neural outcomes.

3. **Active engagement detection**: Arican & Soyman (2025) show that passive music alone does not significantly reduce pain vs silence (p=0.101), but task engagement (whether attending to music or attending to pain) does (p=0.001). VRIAP's active-passive differential depends on R³.onset × R³.x_l0l5 as "motor engagement" proxies, but there is no R³ feature that captures whether a listener is actively engaged vs passively hearing. **Severity: None** — active vs passive engagement is a listener-state variable, not an acoustic property. It is correctly modeled as the difference between engagement and familiarity in the VRIAP output (active_passive dimension) rather than as an R³ input.

### Doc-Code Mismatches Noted
- **FULL_NAME**: doc "VR-Integrated Analgesia Paradigm"; code "VR-Induced Analgesia Paradigm"
- **LAYERS**: doc E(0:3)/M(3:5)/P(5:7)/F(7:10); code E(0:2)/M(2:4)/P(4:7)/F(7:10) with different feature names
- **h3_demand**: doc 18 tuples; code empty ()
- **brain_regions**: doc 9 regions (S1, PM&SMA, M1, DLPFC, Insula, ACC, NAcc, mPFC, Hippo); code 2 (ACC, Insula)
- **dimension_names**: completely different between doc and code
- **Citations**: code cites Hoffman 2011, Wiederhold 2014 (unverifiable); doc now cites 8 verified papers

---

## IMU-β3-OII

### Potential Gaps
1. **Neural entrainment intensity feature**: Ding et al. (2025, EEG N=31) measures ITPC (inter-trial phase coherence) as a proxy for neural entrainment strength at specific frequencies (1-12 Hz). The extraction proposes `r3:X43.neural_entrainment_intensity` (0-1 normalized coherence). The current R³ space has no direct "phase coherence" or "entrainment strength" feature; OII approximates entrainment potential through onset_strength[11] and spectral_flux[21] as mode switching triggers, and periodicity[5] as oscillatory regularity. **Severity: Minor** — current R³ proxies (onset_strength, spectral_flux, periodicity) capture the acoustic drivers of entrainment, while the neural entrainment response itself is a brain-side computation that correctly lives in the model output, not R³ input.

2. **Cross-frequency coupling strength**: Borderie et al. (2024, iEEG) and Samiee et al. (2022, MEG N=16) demonstrate that theta-gamma and delta-beta PAC strength predicts cognitive performance and pitch processing. OII computes integration-segregation dynamics internally but R³ has no input feature that directly captures "cross-frequency energy ratio" or "spectral nesting potential" of the audio signal. **Severity: Minor** — this is fundamentally a neural/cognitive variable, not an acoustic feature. The acoustic correlates (periodicity, roughness, onset patterns) are already captured in R³. The cross-frequency coupling is a brain-level mechanism correctly modeled by the OII compute function.

3. **GABA-mediated inhibition proxy**: Dobri et al. (2023, MEG+MRS) shows gamma synchrony correlates with cortical GABA levels in auditory cortex. OII models gamma segregation but has no individual-differences parameter for inhibitory tone. **Severity: None** — this is a participant-level neurochemical variable, not an acoustic feature or model parameter. Correctly outside R³ scope.

4. **Emotional valence-dominance from oscillatory rate**: Ding et al. (2025) identifies a 6 Hz boundary (theta-alpha transition) separating emotional effects: below 6 Hz decreases valence, above 6 Hz increases valence. R³ has no dedicated "oscillatory rate" dimension for rhythmic stimuli. **Severity: Minor** — current R³ captures this indirectly through spectral_flux[21] and onset_strength[11] rate patterns. The 6 Hz boundary is more relevant to ARU (affective response) than IMU. The temporal (H³) features at appropriate horizons can capture repetition rate effects.

### Doc-Code Mismatches Noted
- **MECHANISM_NAMES**: doc says `("SYN", "MEM")`; code says `("MEM",)` — missing SYN
- **LAYERS**: doc E(3)/M(2)/P(3)/F(2)=10D; code E(2)/M(2)/P(3)/F(3)=10D — different structure and names
- **h3_demand**: doc 24 tuples; code empty `()`
- **brain_regions**: doc 10 regions (SFG, DLPFC, SMA, STG, MTG, IFG, Hippocampus, Parahippocampal, Parietal, Cingulate); code 2 (PFC, Parietal — code mentions Parietal not in original doc)
- **dimension_names**: completely different between doc and code
- **Citations**: code cites Thut 2012, Roux & Uhlhaas 2014; doc now cites 12 papers (Bruzzone 2022, Samiee 2022, Borderie 2024, etc.)
- **paper_count**: code says 4; doc says 12

---

## IMU-β8-TPRD

### Potential Gaps
1. **Pitch chroma (cyclical) feature**: Briley et al. (2013) demonstrate that pitch perception has two dimensions: pitch height (monotonic) and pitch chroma (cyclical -- the cycle of notes C, D, E, etc. repeating across octaves). The EEG adaptation effect mirrors pitch chroma cyclicality, with nonmonotonic adaptation functions showing a dip at octave separations. The current R³ space captures pitch-related features (tonalness[14], spectral_autocorrelation[17]) but has NO dedicated pitch chroma feature -- these features track pitch salience/periodicity, not the cyclical octave-equivalence dimension. A "pitch chroma distance" or "octave equivalence strength" R³ feature could better model the Briley finding that notes separated by an octave share greater neural representation overlap than notes separated by a tritone. **Severity: Minor** -- the current tonalness x spectral_autocorrelation product captures pitch clarity, and the PPC*.chroma_processing[20:30] mechanism output explicitly models chroma abstraction, which is the appropriate level for this cyclical representation.

2. **Harmonic resolvability feature**: Norman-Haignere et al. (2013) and Briley et al. (2013) both show that resolved harmonics (individually separable by cochlear filters) drive cortical pitch responses much more strongly than unresolved harmonics (which produce only a weak pitch percept via temporal cues). The current R³ space has inharmonicity[5] and harmonic_deviation[6] which capture deviations from ideal harmonic structure, but NO feature that captures the degree to which a sound's harmonics are spectrally resolved vs unresolved. A "harmonic resolvability index" based on the ratio of spectral peak spacing to estimated auditory filter bandwidth could improve TPRD's ability to model the resolved/unresolved dissociation. **Severity: Minor** -- the current mel-spectrogram (128 bins) implicitly captures resolvability since resolved harmonics produce distinct spectral peaks while unresolved ones do not. The tonalness feature partially captures this since resolved harmonics produce higher tonal quality. But an explicit resolvability index could be more precise.

3. **High-gamma power proxy**: Foo et al. (2016) demonstrate that ECoG high-gamma (70-150 Hz) power in STG tracks consonance/dissonance processing and correlates with stimulus roughness. This is a neural measure, not an acoustic feature. **Severity: None** -- correctly handled as a brain-level output variable. The correlation between high-gamma and roughness suggests that R³.roughness[0] already serves as the appropriate acoustic proxy for the neural process.

### Doc-Code Mismatches Noted
- **FULL_NAME**: doc "Tonotopy-Pitch Representation Dissociation"; code "Tonotopy-Pitch Representation Density"
- **MECHANISM_NAMES**: doc `("SYN",)` with `CROSS_CIRCUIT = ("PPC",)`; code `("PPC",)` with no cross-circuit
- **LAYERS**: doc T(3)/M(2)/P(2)/F(3)=10D; code E(2)/M(2)/P(3)/F(3)=10D
- **h3_demand**: doc 18 tuples; code empty `()`
- **brain_regions**: doc 6 regions (medial HG, anterolateral HG, lateral HG, R-STG, bilateral STG, PT); code 2 (medial HG at 44,-20,6; lateral HG at 52,-14,4)
- **MNI coords**: doc Talairach from Briley 2013 (L:-41.9,-18.8,15.8 / R:44.2,-13.4,13.4); code 44,-20,6
- **dimension_names**: completely different between doc and code
- **Citations**: code cites Moerel 2012, Formisano 2003 (paper_count=4); doc now cites 12 verified papers

---

## IMU-β4-HCMC

### Potential Gaps
1. **Expectation uncertainty feature**: Cheung et al. (2019, N=79) demonstrate that chord-level Shannon entropy (uncertainty) and information content (surprise) jointly predict hippocampal/amygdala BOLD activation (beta = -0.140, p = 0.002). The current R³ space has `entropy[22]` which captures spectral entropy (a signal-level measure), but NOT information-theoretic predictive uncertainty about upcoming musical events. The model uses entropy as an "encoding difficulty" proxy, but Cheung's uncertainty is a cognitive-predictive measure derived from chord transition statistics, not from the acoustic spectrum. **Severity: Minor** — R³.entropy[22] provides a reasonable low-level proxy since spectral entropy correlates with perceptual complexity. However, a true sequence-level predictive entropy would require a learned statistical model (like IDyOM), which is outside R³'s scope as a frame-level acoustic feature space. The MEM.encoding_state mechanism partially captures this via novelty detection.

2. **Theta-gamma coupling feature**: Borderie et al. (2024, SEEG) shows theta-gamma phase-amplitude coupling in hippocampus and STS is the binding mechanism for sequential auditory memory. The current R³/H³ pipeline captures temporal features via morphological statistics (mean, std, range, autocorrelation) but has no explicit oscillatory coupling measure. **Severity: None** — theta-gamma PAC is a neural (brain-level) mechanism, not an acoustic feature. It is appropriately captured by the MEM mechanism's encoding_state sub-section rather than R³.

3. **Replay detection feature**: Liu et al. (2024, N=33) demonstrate that memory replay events trigger heightened hippocampal-mPFC-DMN connectivity, with replay probability decodable from EEG patterns. HCMC's consolidation model uses H³ windows (H20, H24) as proxies for hippocampal consolidation time windows, but replay is a stochastic neural event, not an acoustic feature. **Severity: None** — correctly modeled as a neural-level process via MEM.retrieval_dynamics rather than R³.

---

## IMU-β5-RIRI

### Potential Gaps
1. **Haptic/proprioceptive feedback channel**: RIRI models multi-modal rehabilitation integration (auditory + visual + haptic), but R³ only captures the auditory channel. The haptic and visual modalities that drive the integration synergy (VR environments, robotic feedback forces) have no representation in R³. **Severity: None** — R³ is by design an audio-only feature space. RIRI correctly uses the auditory features (onset, flux, entrainment coupling) as the "master clock" that phase-locks the other modalities. The non-auditory modalities are modeled through the MEM/BEP mechanism abstraction rather than R³ dimensions.

2. **Groove/movement-inducing quality**: Li et al. (2025) demonstrate that musical groove modulates locomotion biomechanics through auditory-motor coupling. The current R³ space captures onset_strength and spectral_flux but lacks a composite "groove" or "movement-inducing quality" feature. Groove is a perceptual dimension that combines syncopation, bass energy, and rhythmic predictability. **Severity: Minor** — the interaction terms x_l0l5 (consonance x timbre) and BEP*.motor_entrainment provide a reasonable proxy for groove-related auditory-motor coupling. A dedicated groove feature could improve precision but is not strictly required.

3. **Basal ganglia bypass signal**: Huang & Qi (2025) and Harrison et al. (2025) show that music therapy bypasses dysfunctional basal ganglia via auditory-motor neural networks (reticulospinal and CTC pathways). There is no R³ feature that directly indexes the "bypass potential" of a rhythmic stimulus (i.e., how well it can substitute for impaired internal timing). **Severity: None** — this is a neural circuit property of the listener, not an acoustic feature. The bypass efficacy depends on beat clarity (onset_strength) and regularity (periodicity), both already captured in RIRI's H³ demand.

4. **Session-to-session temporal scale**: RIRI models session-to-session consolidation (MEM.encoding binds motor memories across sessions), but H³ horizons max out at H16 (1000ms). Cross-session learning operates on timescales of hours to weeks, far beyond H³ range. **Severity: None** — correctly delegated to MEM mechanism (which abstracts session-level consolidation) rather than H³ temporal features. Blasi et al. (2025) confirms neuroplastic changes accumulate over weeks of music/dance rehabilitation, supporting MEM as the right abstraction level.

### Doc-Code Mismatches Noted
- **FULL_NAME**: doc "RAS-Intelligent Rehabilitation Integration"; code "Recognition-Recall Integration Recency Index" — entirely different model concept
- **LAYERS**: doc E(3: f01_multimodal_entrainment/f02_sensorimotor/f03_enhanced_recovery)/M(2)/P(2)/F(3)=10D; code E(2: recognition/recall)/M(2)/P(3)/F(3)=10D — completely different features
- **h3_demand**: doc 16 tuples; code empty `()`
- **CROSS_UNIT_READS**: doc `("BEP",)`; code `()` — missing cross-circuit read
- **brain_regions**: doc 10 regions (SMA, Premotor, Cerebellum, IPL, Hippocampus, Putamen, M1, Auditory Cortex, mPFC, STS/TPJ); code 2 (Hippocampus, Perirhinal Cortex)
- **Citations**: code cites Dowling 2008, Dalla Bella 2009; doc now cites 15 verified papers (Thaut 2015, Harrison 2025, Blasi 2025, etc.)
- **compute()**: doc has full formula implementation; code returns zeros (stub)
- **version**: doc 2.1.0; code 2.0.0

---

## IMU-γ1-DMMS

### Potential Gaps
1. **Melodic contour direction feature**: Sena Moore et al. (2025) define Musical Contour Regulation Facilitation (MCRF), where ascending vs descending melodic contour direction is a key mechanism for emotion regulation scaffolding in early childhood. DMMS uses R³.x_l5l7 (consonance x timbre interaction) as a "familiarity template" proxy for melodic imprinting, but this interaction term captures the *co-occurrence* of consonance and timbre features, not the *direction of pitch change*. A dedicated "contour direction" or "pitch trajectory" R³ feature (ascending/descending/flat) could better capture the MCRF mechanism. **Severity: Minor** — the current proxy captures melodic stability but not directionality. Contour direction is partially captured by H³ morphological features (M2=range, M19=stability) on tonalness, so the gap is mitigated by the temporal pipeline.

2. **Subcortical encoding fidelity**: Strait et al. (2012, N=31) show that early musical training enhances brainstem frequency-following response (FFR) fidelity for speech harmonics. However, Whiteford et al. (2025, N>260) failed to replicate this in a preregistered multi-site study. DMMS reads R³ consonance/timbre features which are derived from mel-spectrogram (cochlea model), not from brainstem FFR. The R³ features therefore bypass the contested subcortical enhancement and operate at a cortical-equivalent level. **Severity: None** — DMMS's R³ feature chain does not depend on brainstem FFR. The counterevidence actually supports DMMS's design: scaffold formation likely operates at cortical/hippocampal levels, not subcortical.

3. **Dopaminergic reward prediction**: Qiu et al. (2025, N=48 mice) show that fetal-infant music exposure upregulates dopaminergic signaling pathways (Slc6a3, Drd4, Th genes) in mPFC. DMMS models scaffold formation but has no explicit reward/dopamine proxy in R³. **Severity: None** — dopaminergic signaling is a neurochemical process downstream of acoustic features. The reward dimension is appropriately delegated to ARU (specifically ARU.SRP) rather than included in DMMS's R³ inputs. The cross-unit pathway DMMS -> ARU.DAP correctly captures this relationship.

### Doc-Code Mismatches Noted
- **FULL_NAME**: doc "Developmental Music Memory Scaffold"; code "Developmental Music Memory Schema"
- **LAYERS**: doc E(0:3)/M(3:5)/P(5:7)/F(7:10); code E(0:2)/M(2:4)/P(4:7)/F(7:10) with completely different feature names
- **h3_demand**: doc 15 tuples; code empty ()
- **brain_regions**: doc 6 regions (Hippocampus, Amygdala, A1/STG, mPFC, R-PFC, Auditory brainstem); code 2 (Auditory Cortex, Hippocampus)
- **dimension_names**: doc uses f37_early_binding, f38_dev_plasticity, etc.; code uses f01_scaffold_strength, f02_exposure_history, etc.
- **Citations**: code cites Trainor 2005, Trehub 2001; doc now cites 12 papers with different authors/years

---

## IMU-γ2-CSSL

### Potential Gaps
1. **Isochrony / rhythmic regularity feature**: Burchardt et al. (2025, N=54, *Scientific Reports*) show zebra finch IOI beats range 8.6-26.4 Hz with CV = 0.57 (sd 0.15), and the degree of isochrony (nPVI) is a key predictor of tutor-tutee rhythmic similarity (D = -0.35 for nPVI between tutor vs tutee). Ravignani (2021, *Behavioral and Brain Sciences*) argues isochrony is the fundamental scaffold for cross-species vocal learning. The current R³ space uses onset_strength[11] and spectral_flux[21] as rhythm proxies but has no dedicated "isochrony" or "rhythmic regularity" metric (e.g., nPVI of onset intervals). **Severity: Minor** — onset_strength + the H³ periodicity morph (M17) at H20 provides a reasonable proxy for regularity, but a direct nPVI-like feature would better capture the isochrony dimension critical to cross-species comparisons.

2. **Vocal learning capacity feature**: Zhang et al. (2024, *PNAS* 121(9):e2313831121, N=21 across 3 primate species) demonstrate that dorsal auditory pathway strength (arcuate fasciculus) varies across species and predicts vocal learning capacity. The current R³ space has no acoustic proxy for "vocal learnability" — i.e., how easily a given auditory pattern could be imitated. **Severity: None** — this is a species-level / participant-level trait, not an acoustic feature. Correctly outside R³ scope.

3. **Corollary discharge / sensorimotor prediction signal**: Eliades et al. (2024, *Nature Communications* 15:3093, N=3285 units from 5 marmosets) show dual timescale vocal suppression (phasic gating + tonic prediction) in auditory cortex during vocalization. This motor-to-auditory feedback signal is not represented in R³, which is purely acoustic. **Severity: None** — corollary discharge is a brain-internal computation, not an acoustic feature. Correctly handled by the MEM mechanism's encoding_state and the motor-auditory coupling in the CSSL model formulas.

### Doc-Code Mismatches Noted
- **LAYERS**: doc E(3)/M(2)/P(2)/F(3)=10D; code E(2)/M(2)/P(3)/F(3)=10D with completely different feature names
- **h3_demand**: doc 15 tuples; code empty `()`
- **brain_regions**: doc 6 regions (Hippo, STG, BG, IFG, Premotor, AF); code 2 (STG, Hippo)
- **TIER**: doc "gamma2"; code "gamma" (missing sub-tier)
- **dimension_names**: completely different between doc and code
- **compute()**: doc has full formulas; code returns zeros (stub)
- **Citations**: code has 2; doc now has 12 verified papers
- **version**: doc 2.1.0; code 2.0.0

---

## IMU-β9-CMAPCC

### Doc-Code Mismatches
1. **FULL_NAME**: doc="Cross-Modal Action-Perception Common Code" vs code="Cross-Modal Action-Perception Coupling Circuit". **Severity: Minor** — naming inconsistency only; model function is the same.
2. **LAYERS E feature count**: doc has 3 features (f01_common_code, f02_cross_modal_binding, f03_sequence_generalization) vs code has 2 (f01_cross_modal_transfer, f02_common_code). **Severity: Moderate** — code defines 2D E-layer but doc specifies 3D; output dimension allocation differs.
3. **LAYERS M feature names**: doc=(common_code_strength, transfer_probability) vs code=(action_perception_coupling, classification_accuracy). **Severity: Minor** — naming only.
4. **LAYERS P feature count**: doc has 2 features (pmc_activation, mirror_coupling) vs code has 3 (perception_encoding, action_encoding, code_alignment). **Severity: Moderate** — code defines 3D P-layer but doc specifies 2D.
5. **LAYERS F feature names**: doc=(transfer_pred, motor_seq_pred, perceptual_seq_pred) vs code=(transfer_forecast, coupling_stability_pred, cross_modal_predict). **Severity: Minor** — naming only.
6. **Right PMC MNI coordinates**: doc v2.0.0=(48,2,52) vs code=(46,0,50). v2.1.0 doc now uses Bianco 2016 verified coordinates: rIFG BA44=(44,6,26), BA45=(44,34,2). **Severity: Minor** — all values are in vicinity of right premotor/IFG; code should be updated to match verified MNI.
7. **MECHANISM_NAMES order**: doc=("MEM","BEP") vs code=("BEP","MEM"). **Severity: Trivial** — ordering difference only.
8. **h3_demand**: doc specifies 20 tuples vs code returns empty tuple (). **Severity: Moderate** — code stub does not implement H3 demand; needs implementation.
9. **Citations**: doc (v2.1.0) now has 12 named papers vs code has only Lahav 2007 and Bangert 2006. **Severity: Minor** — code metadata should be updated with paper_count=12.
10. **paper_count**: code metadata says paper_count=4 but code citations list only 2 papers (Lahav, Bangert). **Severity: Minor** — internal code inconsistency.
11. **Confidence range**: doc (v2.1.0)=70-85% vs code=(0.70, 0.85). **Severity: None** — now aligned after v2.1.0 update.

### Potential R³ Gaps
1. **Visuomotor transformation feature**: Bianco et al. (2016) demonstrates that fronto-parietal (dorsal) networks for musical action rely on visuomotor transformations in bilateral SPL, distinct from fronto-temporal (ventral) networks for auditory perception. The current R³ space has no visual or visuomotor feature — all R³ features are derived from audio. CMAPCC models cross-modal common code but can only access the auditory side via R³. **Severity: Minor** — CMAPCC explicitly models the auditory pathway; the motor/visual side is handled by BEP* mechanism. However, a future multimodal MI extension might benefit from visual R³ features.

2. **White matter integrity proxy**: Moller et al. (2021) shows left IFOF FA correlates with cross-modal gain (t=3.38, p<0.001). Olszewska et al. (2021) shows arcuate fasciculus microstructure predicts musical learning. These are participant-level structural features, not acoustic features. **Severity: None** — correctly outside R³ scope; would be a participant-level covariate.

3. **Mu suppression index**: Tanaka (2021) and Ross & Balasubramaniam (2022) show that mu (alpha, 8-13Hz) suppression at sensorimotor cortex indexes mirror neuron / covert motor activity during music perception. R³ has no EEG-derived feature. **Severity: None** — this is a neural response measure, not an acoustic input feature. Correctly handled by BEP* mechanism output.

---

## IMU-γ3-CDEM

### Potential Gaps
1. **Emotional context valence feature**: Sachs et al. (2025, fMRI N=39) show that emotional context modulates brain-state transitions, with same-valence context shifts occurring 6.26s earlier than different-valence shifts. CDEM uses R³.roughness[0] (inverse) as a valence proxy and R³.x_l5l7[41:49] (consonance x timbre) as a mood congruency signal. These acoustic features approximate valence but do not capture the *emotional context* itself — context is a multi-modal, cognitive construct (visual, spatial, social), not an acoustic feature. A dedicated "contextual valence" R³ feature would require non-acoustic input. **Severity: None** — emotional context is correctly modeled via MEM mechanism (encoding_state tracks context novelty; familiarity_proxy estimates congruency) and AED* cross-circuit (arousal dynamics). The R³ acoustic features serve as the auditory component of context, while the full context representation is a brain-level computation.

2. **Valence transition rate feature**: Sachs et al. (2025) demonstrate that the *rate* of emotional transitions (not just static valence) is critical for context-dependent processing — brain-state transitions have a characteristic temporal profile (6.26s lead time). The current R³ has spectral_flux[21] for frame-level change detection, but no dedicated "valence change rate" or "emotional transition speed" feature computed over a sliding window. **Severity: Minor** — the H³ pipeline partially captures this through temporal morphology on roughness (roughness at H20, M18=trend, as specified in CDEM's h3_demand). The trend morph on roughness at 5s window approximates a valence trajectory. A dedicated valence-transition-rate R³ feature would be redundant with the H³ approach.

3. **Cross-modal binding strength feature**: Billig et al. (2022) review extensive evidence that hippocampal binding of auditory information with spatiotemporal context requires coherent multi-modal input. Borderie et al. (2024, iEEG) show theta-gamma CFC in hippocampus as the neural binding mechanism. CDEM uses R³.stumpf_fusion[3] as a "binding strength proxy" (tonal fusion = coherent input signal), which captures acoustic coherence but not multi-modal coherence. **Severity: None** — cross-modal binding is a brain-level computation (hippocampal trisynaptic loop) that operates on combined auditory + non-auditory inputs. The R³ space is intentionally audio-only; the cross-modal dimension is handled by the MEM mechanism's encoding_state and the model's context-binding formulas.

4. **Mood regulation individual differences**: Calabria et al. (2023, MCI patients) show that individual differences in mood regulation moderate the music-memory interaction — high mood regulators benefit from high-arousal background music, while low mood regulators show a negative pleasantness-performance relationship. R³ has no "mood regulation capacity" or "individual difference" feature. **Severity: None** — this is a participant-level trait variable, not an acoustic feature. Correctly outside R³ scope. Would be modeled as a listener parameter in a future individual-differences extension.

### Doc-Code Mismatches Noted
- **LAYERS structure**: doc C(3)/M(2)/P(2)/F(3)=10D; code E(2)/M(2)/P(3)/F(3)=10D — different layer names and dimension allocation
- **Dimension names**: completely different between doc and code (e.g., doc: f43_ctx_mod, f44_arousal_supp; code: f01_context_modulation, f02_emotional_encoding)
- **CROSS_UNIT_READS**: doc specifies `CROSS_CIRCUIT = ("AED",)`; code has empty `()`
- **h3_demand**: doc specifies 18 tuples; code returns empty `()`
- **brain_regions**: doc has 7 (Hippocampus, Amygdala, mPFC, ACC, STG/STS, Parahippocampal, V-Striatum); code has 3 (Hippocampus, Amygdala, STS)
- **Citations**: code has "Eschrich 2008" (not in literature catalog or doc); doc now has 12 verified papers
- **compute()**: code is stub returning zeros; doc specifies full computation
- **version**: doc 2.1.0; code 2.0.0

---

## IMU-β6-MSPBA

### Potential Gaps
1. **IFG effective connectivity feature**: Kim et al. (2021, MEG N=19) demonstrate that linearized time-delayed mutual information (LTDMI) between IFG and STG is significantly enhanced for syntactically irregular chord endings (F(2,36)=6.526, p=0.024 FDR). MSPBA uses R³.roughness[0], R³.entropy[22], and R³.inharmonicity[5] as inputs to syntactic violation detection, but the IFG-STG connectivity strength itself is a brain-level dynamic, not an acoustic feature. There is no R³ feature for "connectivity potential" or "syntactic integration demand" of a chord within its context. **Severity: Minor** — the current R³ inputs (roughness, entropy, inharmonicity) successfully predict the acoustic conditions under which IFG connectivity increases. The connectivity measure is a neural outcome, not an acoustic input. The SYN mechanism's pred_error and struct_expect sub-dimensions capture this at the model level, which is appropriate.

2. **Musical roundness / gestalt closure feature**: Wohrle et al. (2024, MEG N=30) show that N1m amplitude at the resolution chord (position 4) reflects the preceding dominant chord's dissonance, and "roundness" perception emerges progressively over a 4-chord progression (no difference at chords 1-2, segregation at chord 3, maximum at chord 4). MSPBA models context accumulation through the position 3 vs position 5 mERAN ratio (2:1), but R³ has no dedicated "gestalt closure" or "harmonic resolution potential" feature. **Severity: Minor** — the current H³ temporal features at phrase-level horizons (H10=400ms, H14=700ms) capture the temporal progression of harmonic context. The resolution effect is inherently a temporal/sequential phenomenon better modeled by H³ than R³. The model's context accumulation formula (using SYN.struct_expect over time) already addresses this finding.

3. **Long-term syntactic memory representation**: Koelsch (in press, review) distinguishes ERAN from MMN: ERAN relies on long-term memory representations of music-syntactic regularities (acquired through enculturation), while MMN uses on-line extraction of regularities from the immediate stimulus context. MSPBA's SYN mechanism operates on frame-level acoustic features, not on stored harmonic templates. **Severity: None** — this is correctly handled by the MEM mechanism (CROSS_UNIT_READS in the doc includes MEM for harmonic templates). The SYN+MEM architecture already captures the distinction between online prediction error (SYN) and long-term regularity representations (MEM). The doc-code mismatch notes that code has CROSS_UNIT_READS=() while doc specifies MEM — when code is updated, this gap is resolved.

4. **Information content / entropy at chord-transition level**: Egermann et al. (2013, N=50) use IDyOM-derived information content to predict psychophysiological responses to live concert music. MSPBA uses R³.entropy[22] (spectral entropy) as a proxy for "harmonic unpredictability," but spectral entropy is a signal-level measure of frequency distribution uniformity, NOT the chord-transition-level predictive uncertainty that drives ERAN responses. **Severity: Minor** — R³.entropy[22] correlates with perceptual complexity and serves as a reasonable proxy. True chord-level information content would require a learned statistical model (e.g., IDyOM) operating on symbolic chord representations, which is outside R³'s scope as a frame-level acoustic feature space. The SYN.pred_error mechanism partially addresses this by computing prediction errors based on harmonic context.

### Doc-Code Mismatches Noted
- **LAYERS naming**: doc S(3)/M(3)/P(3)/F(2)=11D; code E(2)/M(3)/P(3)/F(3)=11D — all dimension names differ
- **h3_demand**: doc 16 tuples; code empty `()`
- **brain_regions**: doc 7 regions (L-IFG BA44, R-IFG BA44, L-IFG BA45, R-IFG BA45, STG, Heschl's, auditory cortex); code 3 (BA44 at -48,14,16; rIFG at 48,18,4; STG at 60,-32,8) — code coords differ from both Maess 2001 and Kim 2021
- **CROSS_UNIT_READS**: doc specifies MEM (harmonic templates); code empty `()`
- **dimension_names**: completely different between doc and code
- **compute()**: doc has full formulas (mERAN, violation, context accumulation); code returns zeros (stub)
- **Citations**: code cites Koelsch 2005, Maess 2001 (paper_count=5); doc now cites 12 papers
- **MNI coords**: code BA44 (-48,14,16) vs doc MNI (-44,14,28) + Talairach (-40.8,18.5,15.6) from different sources
- **version**: doc 2.1.0; code 2.0.0

---
