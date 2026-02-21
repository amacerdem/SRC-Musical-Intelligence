# C³ — 96 Model Functional Brain Map

**Perspective**: Classification by **brain function**, not by unit of origin
**Date**: 2026-02-21

> A model may appear in multiple categories — because the brain works that way.
> **Primary** = what the model actually computes, **Secondary** = other system it touches.
> Each model's original unit is shown as `[SPU]` etc.

---

## Functional Categories (12)

| # | Category | Description | Models |
|---|----------|-------------|:------:|
| F1 | Sensory Processing | Basic acoustic feature extraction: pitch, timbre, consonance, frequency | 14 |
| F2 | Pattern Recognition & Prediction | Expectation, prediction error, information content, statistical regularity | 18 |
| F3 | Attention & Salience | Resource allocation, filtering, selective focus, prominence detection | 14 |
| F4 | Memory Systems | Encoding, consolidation, retrieval, procedural/autobiographical memory | 12 |
| F5 | Emotion & Valence | Emotion generation, affective coloring, mode perception, nostalgia | 11 |
| F6 | Reward & Motivation | Dopamine, opioid, pleasure, wanting, consummation, chills | 16 |
| F7 | Motor & Timing | Entrainment, motor planning, synchronization, groove | 21 |
| F8 | Learning & Plasticity | Experience-dependent neural change, network reorganization, efficiency | 14 |
| F9 | Social Cognition | Group coordination, social reward, empathy | 4 |
| F10 | Clinical & Therapeutic | Rehabilitation, therapy, pathology, pain, neurodegeneration | 10 |
| F11 | Development & Evolution | Critical periods, early childhood, ontogeny, phylogeny | 6 |
| F12 | Cross-Modal Integration | Cross-modal transfer, shared codes, multimodal binding | 5 |

> **Note**: Total > 96 because many models span multiple categories.

---

## F1 — Sensory Processing (14 models)

> Sound → neural signal conversion, basic acoustic feature extraction

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| SPU-α1-BCH | [SPU] | Consonance hierarchy via harmonic template matching | — |
| SPU-α2-PSCL | [SPU] | Cortical representation of pitch salience | — |
| SPU-α3-PCCR | [SPU] | Octave-equivalent chroma encoding | — |
| SPU-γ1-SDNPS | [SPU] | Limits of FFR-consonance relationship (synthetic vs natural) | — |
| SPU-γ3-SDED | [SPU] | Universal early dissonance detection (152-258ms) | — |
| IMU-α2-PNH | [IMU] | Interval complexity hierarchy via Pythagorean ratios | — |
| IMU-β8-TPRD | [IMU] | Tonotopic frequency map vs perceptual pitch representation dissociation | — |
| NDU-α1-MPG | [NDU] | Posterior-to-anterior cortical gradient for melodic sequences (onset → contour) | F2 |
| ASU-α3-CSG | [ASU] | Consonance-dissonance level modulating the salience network | F3 |
| SPU-β3-MIAA | [SPU] | Musical imagery during silence → auditory cortex activation | F4 |
| STU-α3-MDNS | [STU] | Melody decoding from EEG (perception + imagery share substrate) | F4 |
| STU-β2-TPIO | [STU] | Timbre perception and imagery share same neural substrate | F4, F7 |
| IMU-β6-MSPBA | [IMU] | Musical syntax violation detection (Broca's area, ERAN) | F2 |
| RPU-γ1-LDAC | [RPU] | Liking gates sensory cortex gain (pleasure feedback to auditory cortex) | F6 |

---

## F2 — Pattern Recognition & Prediction (18 models)

> Expectation formation, prediction error, information content, statistical regularity

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| PCU-α1-HTP | [PCU] | Hierarchical temporal prediction (abstract 500ms, concrete 110ms) | — |
| PCU-α2-SPH | [PCU] | Spatiotemporal prediction hierarchy via feedforward-feedback loops | F4 |
| PCU-α3-ICEM | [PCU] | Information content (IC) peaks → physiological emotional response | F5 |
| PCU-β1-PWUP | [PCU] | Precision-weighting of PE based on contextual uncertainty | — |
| PCU-γ3-PSH | [PCU] | Correct predictions silence higher-level representations | — |
| RPU-α3-RPEM | [RPU] | Reward prediction error (surprising+liked vs surprising+disliked) | F6 |
| RPU-β1-IUCP | [RPU] | Inverted-U complexity preference (IC × entropy) | F6 |
| RPU-γ3-SSPS | [RPU] | Saddle-shaped preference surface (IC × entropy, 2 optimal zones) | F6 |
| ARU-β1-PUPF | [ARU] | Pleasure from uncertainty-surprise interaction (Goldilocks) | F6 |
| PCU-β3-UDP | [PCU] | Correct prediction under high uncertainty → larger reward | F6 |
| IMU-β2-PMIM | [IMU] | ERAN + MMN parallel prediction → hippocampal learning | F4, F8 |
| ASU-γ1-PWSM | [ASU] | Precision-weighted salience (stable context → MMN present) | F3 |
| NDU-α2-SDD | [NDU] | Supramodal deviance detection (IFG hub) | F3 |
| NDU-β2-CDMR | [NDU] | Context-dependent mismatch response (complex melodic contexts only) | F8 |
| STU-α1-HMCE | [STU] | Hierarchical context encoding (short → long temporal windows) | F4 |
| PCU-β4-CHPI | [PCU] | Cross-modal harmonic prediction integration | F12 |
| IMU-β6-MSPBA | [IMU] | Musical syntax violation detection (Broca's = prediction error) | F1 |
| NDU-β3-SLEE | [NDU] | Statistical learning for regularity extraction | F8 |

---

## F3 — Attention & Salience (14 models)

> Resource allocation, filtering, selective focus, prominence detection

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| ASU-α1-SNEM | [ASU] | Selective neural entrainment — oscillation boost at beat frequency | F7 |
| ASU-α2-IACM | [ASU] | Inharmonic sounds capture attention (P3a response) | — |
| ASU-α3-CSG | [ASU] | Consonance level modulates salience network | F1 |
| ASU-β1-BARM | [ASU] | Individual beat ability modulates entrainment tendency | F7 |
| ASU-β2-STANM | [ASU] | Brain network topology reconfigures by attention target | — |
| ASU-β3-AACM | [ASU] | Aesthetic liking → attention capture + motor inhibition (savoring) | F6 |
| ASU-γ1-PWSM | [ASU] | PE weighting by context stability (MMN gating) | F2 |
| ASU-γ2-DGTP | [ASU] | Domain-general temporal processing across music and speech | — |
| ASU-γ3-SDL | [ASU] | Hemispheric lateralization dynamically shifts by attention demand | — |
| STU-β1-AMSS | [STU] | Attention-modulated stream segregation in polyphonic music | F1 |
| STU-β4-ETAM | [STU] | Entrainment + tempo + attention multi-scale modulation | F7 |
| NDU-α2-SDD | [NDU] | Supramodal deviance detection mechanism | F2 |
| PCU-γ1-IGFE | [PCU] | Individual gamma frequency stimulation → memory + executive control | F4 |
| STU-γ2-NEWMD | [STU] | Entrainment vs working memory independence (paradox) | F2, F7 |

---

## F4 — Memory Systems (12 models)

> Encoding, consolidation, retrieval, procedural/autobiographical memory

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| IMU-α1-MEAMN | [IMU] | Music-evoked autobiographical memory network | F5 |
| IMU-α3-MMP | [IMU] | Musical memory preservation mechanism in Alzheimer's | F10 |
| IMU-β4-HCMC | [IMU] | Hippocampal-cortical memory consolidation circuit | — |
| IMU-γ1-DMMS | [IMU] | Early childhood music memory scaffolds (0-5 years) | F11 |
| IMU-γ3-CDEM | [IMU] | Context-dependent emotional memory (mood congruence) | F5 |
| IMU-β2-PMIM | [IMU] | Prediction error → hippocampal new pattern learning | F2 |
| STU-α1-HMCE | [STU] | Hierarchical context encoding (short → long windows) | F2 |
| STU-γ1-TMRM | [STU] | Tempo memory reproduction accuracy (120 BPM reference) | F7 |
| RPU-β3-MEAMR | [RPU] | Familiar music → dMPFC autobiographical memory + reward | F6 |
| ARU-β4-NEMAC | [ARU] | "My music" nostalgia circuit (self-selected > other-selected) | F5 |
| PCU-α2-SPH | [PCU] | Spatiotemporal prediction → memory recognition loops | F2 |
| SPU-β3-MIAA | [SPU] | Musical imagery → memory-based auditory activation | F1 |

---

## F5 — Emotion & Valence (11 models)

> Emotion generation, affective coloring, mode perception, nostalgia, autonomic responses

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| ARU-α3-VMM | [ARU] | Major/minor → separate neural circuits → happy/sad perception | — |
| ARU-α2-AAC | [ARU] | Skin conductance, heart rate, respiration → dopamine coupling | F6 |
| PCU-α3-ICEM | [PCU] | Information content peaks → arousal, skin conductance, pulse changes | F2 |
| IMU-α1-MEAMN | [IMU] | Music → autobiographical memory → nostalgia, melancholy, longing | F4 |
| IMU-γ3-CDEM | [IMU] | Listening context + mood congruence → emotional memory encoding | F4 |
| ARU-β4-NEMAC | [ARU] | Self-selected music → nostalgia + well-being circuit | F4 |
| ARU-β2-CLAM | [ARU] | EEG emotion reading → real-time music → emotion regulation | F10 |
| ARU-γ2-CMAT | [ARU] | Cross-modal emotional transfer (sound→color, tempo→arousal) | F12 |
| PCU-γ2-MAA | [PCU] | Atonal appreciation = personality + aesthetic framework + exposure | F8 |
| SPU-β1-STAI | [SPU] | Spectral+temporal integration → aesthetic perception → reward | F6 |
| ARU-γ3-TAR | [ARU] | Acoustic parameter manipulation → anxiety/depression/stress therapy | F10 |

---

## F6 — Reward & Motivation (16 models)

> Dopamine, opioid, pleasure, wanting, consummation, chills, preference

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| ARU-α1-SRP | [ARU] | Wanting / liking / pleasure triple dopamine pathway | — |
| RPU-α1-DAED | [RPU] | Caudate (anticipation) vs NAcc (consummation) dopamine dissociation | — |
| RPU-α2-MORMR | [RPU] | Endogenous opioid μ-receptor binding = pleasure mechanism | — |
| RPU-α3-RPEM | [RPU] | Reward prediction error (surprising×liked / surprising×disliked) | F2 |
| RPU-β1-IUCP | [RPU] | Inverted-U complexity preference (medium complexity = peak pleasure) | F2 |
| RPU-β2-MCCN | [RPU] | Chills cortical network: OFC + insula + SMA + STG (theta) | F7 |
| RPU-β3-MEAMR | [RPU] | Familiar music → dMPFC nostalgia + reward integration | F4 |
| RPU-β4-SSRI | [RPU] | Group music → social synchrony → reward amplification | F9 |
| RPU-γ1-LDAC | [RPU] | Liking → sensory cortex gating (pleasure feedback) | F1 |
| RPU-γ2-IOTMS | [RPU] | Individual μ-opioid receptor tone → music reward sensitivity | — |
| RPU-γ3-SSPS | [RPU] | IC × entropy saddle surface (2 optimal pleasure zones) | F2 |
| ARU-β1-PUPF | [ARU] | Uncertainty × surprise → Goldilocks pleasure function | F2 |
| PCU-β3-UDP | [PCU] | Correct prediction under high uncertainty → larger reward | F2 |
| SPU-β1-STAI | [SPU] | Spectral-temporal aesthetic integration → reward regions | F5 |
| ASU-β3-AACM | [ASU] | Aesthetic liking → attention + inhibition (savoring pleasure) | F3 |
| ARU-β3-MAD | [ARU] | Reward pathway disconnection → musical anhedonia | F10 |

---

## F7 — Motor & Timing (21 models)

> Entrainment, motor planning, synchronization, groove, tempo, rhythm

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| MPU-α1-PEOM | [MPU] | Period entrainment → kinematic optimization | — |
| MPU-α2-MSR | [MPU] | Musician auditory-motor functional reorganization | F8 |
| MPU-α3-GSSM | [MPU] | Gait-phase synchronized SMA+M1 stimulation → balance control | F10 |
| MPU-β1-ASAP | [MPU] | Motor beat simulation → auditory "when" prediction | F2 |
| MPU-β2-DDSMI | [MPU] | Dyadic dance: music + self + partner + social coordination | F9 |
| MPU-β3-VRMSME | [MPU] | VR music → sensorimotor network strengthening (rehabilitation) | F10 |
| MPU-β4-SPMC | [MPU] | SMA→PMC→M1 hierarchical motor planning circuit | — |
| MPU-γ2-CTBB | [MPU] | Cerebellar theta-burst → temporal precision improvement | — |
| MPU-γ3-STC | [MPU] | Singing training → insula-sensorimotor connectivity increase | F8 |
| STU-α2-AMSC | [STU] | Auditory gamma → 110ms delayed motor cortex propagation | F1 |
| STU-β3-EDTA | [STU] | Domain-specific tempo accuracy (DJ 120-139, percussionist 100-139 BPM) | F8 |
| STU-β4-ETAM | [STU] | Beat entrainment delta-theta + attention modulation | F3 |
| STU-β5-HGSIC | [STU] | Groove: pSTG gamma → motor cortex hierarchical integration | F6 |
| STU-β6-OMS | [STU] | Orchestral synchronization across 4 oscillatory networks | F9 |
| STU-γ1-TMRM | [STU] | Tempo memory reproduction accuracy (120 BPM reference) | F4 |
| STU-γ2-NEWMD | [STU] | Automatic entrainment vs working memory paradox | F2, F3 |
| STU-γ5-MPFS | [STU] | Motor automaticity × structural mastery → flow state | F8 |
| ASU-α1-SNEM | [ASU] | Selective neural oscillation boost at beat/metric frequency | F3 |
| ASU-β1-BARM | [ASU] | Beat ability → entrainment tendency modulation | F3 |
| RPU-β2-MCCN | [RPU] | SMA motor component within chills network | F6 |
| PCU-β2-WMED | [PCU] | Entrainment ↔ working memory dissociation in rhythm production | F2 |

---

## F8 — Learning & Plasticity (14 models)

> Experience-dependent neural change, network reorganization, neural efficiency

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| SPU-β2-TSCP | [SPU] | Instrument timbre → cortical plasticity (proportional to training duration) | F1 |
| SPU-γ2-ESME | [SPU] | Training-domain selective MMN enhancement | F1 |
| NDU-α3-EDNR | [NDU] | Expertise → within-network connectivity ↑, between-network ↓ → specialization | — |
| NDU-β2-CDMR | [NDU] | Selective mismatch response development in complex contexts | F2 |
| NDU-β3-SLEE | [NDU] | Statistical learning → multi-sensory regularity extraction | F2 |
| NDU-γ3-ECT | [NDU] | Specialization ↔ flexibility trade-off (compartmentalization) | — |
| STU-β3-EDTA | [STU] | Domain-specific sensorimotor specialization | F7 |
| STU-γ3-MTNE | [STU] | Music training → neural efficiency (better behavior + stable neural) | — |
| STU-γ4-PTGMP | [STU] | Piano training → DLPFC + cerebellum grey matter increase | — |
| STU-γ5-MPFS | [STU] | Flow state propensity as prodigy marker | F7 |
| MPU-α2-MSR | [MPU] | Musician auditory-motor circuit reorganization | F7 |
| MPU-γ3-STC | [MPU] | Singing training → insula-sensorimotor persistent connectivity | F7 |
| IMU-β3-OII | [IMU] | Brain oscillations (theta+gamma) ↔ fluid intelligence link | — |
| PCU-γ2-MAA | [PCU] | Atonal appreciation = personality + exposure + aesthetic framework | F5 |

---

## F9 — Social Cognition (4 models)

> Group coordination, social reward, interpersonal synchronization

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| RPU-β4-SSRI | [RPU] | Group music → endorphin/oxytocin → reward 1.3-1.8× amplification | F6 |
| MPU-β2-DDSMI | [MPU] | Dyadic dance: 4 parallel social-motor process coordination | F7 |
| STU-β6-OMS | [STU] | Orchestral synchronization: 4 oscillatory networks (prefrontal, temporo-parietal, limbic, brainstem) | F7 |
| MPU-γ1-NSCP | [MPU] | Inter-subject neural synchrony → commercial success prediction | — |

---

## F10 — Clinical & Therapeutic (10 models)

> Rehabilitation, therapy, pathology, pain, neurodegeneration, anhedonia

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| IMU-α3-MMP | [IMU] | Musical memory preservation in Alzheimer's (SMA/ACC atrophy resistance) | F4 |
| IMU-β1-RASN | [IMU] | RAS rhythmic stimulus → SMA/cerebellum synchronization → motor recovery | F7, F8 |
| IMU-β5-RIRI | [IMU] | RAS + VR + robotics → accelerated motor rehabilitation | F7 |
| IMU-β7-VRIAP | [IMU] | Music + active motor interaction → analgesia (S1 connectivity decrease) | F7 |
| MPU-α3-GSSM | [MPU] | Gait-synchronized stimulation → balance + walking improvement | F7 |
| MPU-β3-VRMSME | [MPU] | VR music stimulation → sensorimotor network strengthening | F7 |
| ARU-β2-CLAM | [ARU] | EEG closed-loop → emotion regulation (anxiety/depression) | F5 |
| ARU-β3-MAD | [ARU] | Auditory cortex ↔ NAcc disconnection = musical anhedonia | F6 |
| ARU-γ3-TAR | [ARU] | Acoustic parameter manipulation → therapeutic music prescription | F5 |
| NDU-β1-DSP | [NDU] | Parental singing → preterm infant auditory plasticity | F11 |

---

## F11 — Development & Evolution (6 models)

> Critical periods, early childhood, ontogeny, phylogeny

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| ARU-γ1-DAP | [ARU] | 0-5 year music exposure → auditory-limbic connectivity shaping | F6 |
| IMU-γ1-DMMS | [IMU] | Early childhood lullaby/music → permanent memory scaffold formation | F4 |
| IMU-γ2-CSSL | [IMU] | Cross-species song learning (zebra finch ↔ human shared mechanism) | F4 |
| NDU-β1-DSP | [NDU] | Preterm infants: parental singing → auditory plasticity | F10 |
| NDU-γ1-SDDP | [NDU] | Sex-dependent music intervention responses (preterm) | F10 |
| NDU-γ2-ONI | [NDU] | Music intervention → improvement beyond expected correction | F10 |

---

## F12 — Cross-Modal Integration (5 models)

> Cross-modal transfer, shared codes, multimodal binding

| Model | Origin | Computation | Secondary |
|-------|--------|-------------|-----------|
| ARU-γ2-CMAT | [ARU] | Visual-tactile-auditory emotional transfer (mPFC/OFC/insula) | F5 |
| IMU-β9-CMAPCC | [IMU] | Modality-independent sequence representation in premotor cortex (shared code) | F7 |
| PCU-β4-CHPI | [PCU] | Visual+motor+auditory → harmonic prediction accuracy increase | F2 |
| ASU-γ2-DGTP | [ASU] | Shared temporal processing mechanism across music and speech | F3 |
| NDU-α2-SDD | [NDU] | Supramodal deviance detection (cross-sensory shared mechanism) | F2, F3 |

---

## Cross-Intersection Matrix

> How many functional categories each model touches

### Single-Function Models (Pure — 1 category only)

| Model | Category | What It Does |
|-------|----------|--------------|
| SPU-α1-BCH | F1 | Consonance hierarchy |
| SPU-α2-PSCL | F1 | Pitch salience |
| SPU-α3-PCCR | F1 | Chroma encoding |
| SPU-γ1-SDNPS | F1 | FFR limits |
| SPU-γ3-SDED | F1 | Early dissonance detection |
| IMU-α2-PNH | F1 | Pythagorean interval hierarchy |
| IMU-β8-TPRD | F1 | Tonotopy/pitch dissociation |
| IMU-β4-HCMC | F4 | Memory consolidation circuit |
| ARU-α3-VMM | F5 | Valence-mode mapping |
| ARU-α1-SRP | F6 | Dopamine reward pathway |
| RPU-α1-DAED | F6 | Anticipation/consummation dopamine dissociation |
| RPU-α2-MORMR | F6 | Opioid pleasure mechanism |
| RPU-γ2-IOTMS | F6 | Individual opioid sensitivity |
| MPU-α1-PEOM | F7 | Period entrainment |
| MPU-β4-SPMC | F7 | SMA→PMC→M1 motor circuit |
| MPU-γ2-CTBB | F7 | Cerebellar timing |
| PCU-α1-HTP | F2 | Hierarchical temporal prediction |
| PCU-β1-PWUP | F2 | PE precision weighting |
| PCU-γ3-PSH | F2 | Prediction silencing |
| ASU-α2-IACM | F3 | Inharmonic attention capture |
| ASU-β2-STANM | F3 | Network topology reconfiguration |
| ASU-γ3-SDL | F3 | Dynamic lateralization |
| NDU-α3-EDNR | F8 | Expertise network reorganization |
| NDU-γ3-ECT | F8 | Specialization-flexibility trade-off |
| STU-γ3-MTNE | F8 | Neural efficiency |
| STU-γ4-PTGMP | F8 | Grey matter plasticity |
| IMU-β3-OII | F8 | Oscillation-intelligence link |
| MPU-γ1-NSCP | F9 | Population synchrony → commercial prediction |

> 28 models are single-function (pure models)

### Dual-Function Models (touching 2 categories)

| Model | Primary | Secondary | Bridge |
|-------|---------|-----------|--------|
| SPU-β1-STAI | F5 Emotion | F6 Reward | aesthetic → reward |
| SPU-β3-MIAA | F1 Sensory | F4 Memory | imagery → memory |
| STU-α3-MDNS | F1 Sensory | F4 Memory | perception = imagery |
| STU-α2-AMSC | F7 Motor | F1 Sensory | auditory → motor |
| STU-β1-AMSS | F3 Attention | F1 Sensory | attention → stream segregation |
| STU-γ1-TMRM | F7 Motor | F4 Memory | tempo memory |
| ARU-α2-AAC | F5 Emotion | F6 Reward | autonomic → dopamine |
| ARU-β2-CLAM | F5 Emotion | F10 Clinical | emotion regulation → therapy |
| ARU-β4-NEMAC | F5 Emotion | F4 Memory | nostalgia → memory |
| ARU-γ1-DAP | F11 Development | F6 Reward | critical period → reward capacity |
| ARU-γ2-CMAT | F12 Cross-Modal | F5 Emotion | cross-modal → emotion |
| ARU-γ3-TAR | F10 Clinical | F5 Emotion | therapy → emotion regulation |
| ASU-α3-CSG | F3 Attention | F1 Sensory | consonance → salience |
| ASU-β3-AACM | F3 Attention | F6 Reward | aesthetic liking → attention |
| ASU-γ1-PWSM | F3 Attention | F2 Prediction | precision → salience |
| NDU-α1-MPG | F1 Sensory | F2 Prediction | onset → contour gradient |
| NDU-β2-CDMR | F2 Prediction | F8 Learning | context → mismatch |
| NDU-β3-SLEE | F2 Prediction | F8 Learning | statistical learning |
| NDU-γ1-SDDP | F11 Development | F10 Clinical | sex + preterm |
| NDU-γ2-ONI | F11 Development | F10 Clinical | over-normalization |
| PCU-α3-ICEM | F2 Prediction | F5 Emotion | IC → emotion |
| PCU-β3-UDP | F2 Prediction | F6 Reward | uncertainty → pleasure |
| PCU-γ2-MAA | F5 Emotion | F8 Learning | exposure + personality |
| RPU-α3-RPEM | F6 Reward | F2 Prediction | reward PE |
| RPU-β1-IUCP | F6 Reward | F2 Prediction | inverted-U preference |
| RPU-γ1-LDAC | F6 Reward | F1 Sensory | liking → sensory gating |
| RPU-γ3-SSPS | F6 Reward | F2 Prediction | saddle surface |
| ARU-β3-MAD | F6 Reward | F10 Clinical | anhedonia |
| IMU-α1-MEAMN | F4 Memory | F5 Emotion | autobiographical → emotion |
| IMU-γ3-CDEM | F4 Memory | F5 Emotion | context → emotional memory |
| IMU-γ1-DMMS | F4 Memory | F11 Development | childhood memory scaffold |
| IMU-α3-MMP | F4 Memory | F10 Clinical | Alzheimer's resistance |
| IMU-β6-MSPBA | F1 Sensory | F2 Prediction | syntax → prediction |
| MPU-α2-MSR | F7 Motor | F8 Learning | reorganization |
| MPU-γ3-STC | F7 Motor | F8 Learning | singing → connectivity increase |
| STU-β3-EDTA | F7 Motor | F8 Learning | domain-specific specialization |
| STU-γ5-MPFS | F7 Motor | F8 Learning | flow state |
| PCU-α2-SPH | F2 Prediction | F4 Memory | prediction → recognition |
| RPU-β3-MEAMR | F6 Reward | F4 Memory | nostalgia reward |
| RPU-β2-MCCN | F6 Reward | F7 Motor | chills network motor component |
| NDU-α2-SDD | F2 Prediction | F3 Attention | supramodal deviance |
| PCU-γ1-IGFE | F3 Attention | F4 Memory | gamma → memory |
| MPU-β1-ASAP | F7 Motor | F2 Prediction | beat simulation → prediction |
| PCU-β2-WMED | F2 Prediction | F7 Motor | entrainment ↔ memory |
| ASU-α1-SNEM | F3 Attention | F7 Motor | selective entrainment |
| ASU-β1-BARM | F3 Attention | F7 Motor | BAT → entrainment |
| STU-β2-TPIO | F1 Sensory | F7 Motor | timbre perception → motor |
| ASU-γ2-DGTP | F3 Attention | F12 Cross-Modal | music-speech shared |
| NDU-β1-DSP | F10 Clinical | F11 Development | preterm + plasticity |
| IMU-γ2-CSSL | F4 Memory | F11 Development | evolutionary shared mechanism |
| IMU-β9-CMAPCC | F12 Cross-Modal | F7 Motor | shared code → motor |
| PCU-β4-CHPI | F2 Prediction | F12 Cross-Modal | cross-modal prediction |

### Triple+ Function Models (touching 3 or more categories)

| Model | Categories | Description |
|-------|------------|-------------|
| STU-β4-ETAM | F3+F7+F2 | Attention + motor + prediction combined |
| STU-β5-HGSIC | F7+F6+F1 | Motor groove + reward pleasure + sensory gamma |
| STU-β6-OMS | F7+F9+F3 | Motor synchronization + social + attention |
| STU-γ2-NEWMD | F7+F2+F3 | Motor + prediction + attention paradox |
| IMU-β1-RASN | F10+F7+F8 | Clinical + motor + plasticity |
| IMU-β2-PMIM | F2+F4+F8 | Prediction + memory + learning |
| IMU-β5-RIRI | F10+F7+F8 | Clinical + motor + plasticity (multimodal) |
| IMU-β7-VRIAP | F10+F7+F1 | Clinical + motor + sensory (analgesia) |
| MPU-α3-GSSM | F7+F10 | Motor + clinical (gait) |
| MPU-β2-DDSMI | F7+F9 | Motor + social (dyadic dance) |
| MPU-β3-VRMSME | F7+F10 | Motor + clinical (VR rehabilitation) |
| RPU-β4-SSRI | F6+F9 | Reward + social synchronization |
| NDU-α2-SDD | F2+F3+F12 | Prediction + attention + cross-modal |
| ARU-β1-PUPF | F6+F2 | Reward + prediction (Goldilocks) |

---

## Summary: Functional Distribution

```
F7  Motor & Timing         ████████████████████░  21 models
F2  Prediction & Pattern   ██████████████████░░░  18 models
F6  Reward & Motivation    ████████████████░░░░░  16 models
F1  Sensory Processing     ██████████████░░░░░░░  14 models
F3  Attention & Salience   ██████████████░░░░░░░  14 models
F8  Learning & Plasticity  ██████████████░░░░░░░  14 models
F4  Memory Systems         ████████████░░░░░░░░░  12 models
F5  Emotion & Valence      ███████████░░░░░░░░░░  11 models
F10 Clinical & Therapeutic ██████████░░░░░░░░░░░  10 models
F11 Development & Evol.    ██████░░░░░░░░░░░░░░░   6 models
F12 Cross-Modal            █████░░░░░░░░░░░░░░░░   5 models
F9  Social Cognition       ████░░░░░░░░░░░░░░░░░   4 models
```

### Unit → Function Distribution Table

> How many models each unit contributes to each function

| Unit | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| SPU(9) | **7** | — | — | 1 | 1 | 1 | — | 2 | — | — | — | — |
| STU(14) | 3 | 2 | 3 | 2 | — | 1 | **10** | 4 | 1 | — | — | — |
| IMU(15) | 3 | 2 | — | **6** | 2 | — | 2 | 1 | — | 4 | 2 | 1 |
| ARU(10) | — | 1 | — | 1 | **6** | **4** | — | — | — | 2 | 1 | 1 |
| ASU(9) | 1 | 1 | **8** | — | — | 1 | 3 | — | — | — | — | 1 |
| NDU(9) | 1 | 3 | 1 | — | — | — | — | **4** | — | 1 | 2 | 1 |
| MPU(10) | — | 1 | — | — | — | — | **9** | 2 | 2 | 2 | — | — |
| PCU(10) | — | **7** | 1 | 2 | 2 | 2 | 1 | 1 | — | — | — | 1 |
| RPU(10) | 1 | 4 | — | 1 | — | **9** | 1 | — | 1 | 1 | — | — |

> **Bold** = strongest unit-function alignment. Note the significant cross-contributions.

### Key Observations

1. **Motor (F7)** is the most populated category — 21 models. The motor system is central to music brain modeling.
2. **Prediction (F2)** is second with 18 models — prediction error cuts across all units (PCU, RPU, NDU, IMU, ASU, STU).
3. **Reward (F6)** spans 16 models — beyond ARU and RPU, even SPU, ASU, and PCU touch reward.
4. **SPU → F1 alignment is strong** (7/9 models are pure sensory), but STU, IMU, ARU are highly distributed.
5. **IMU is the most heterogeneous unit**: 15 models scattered across 9 different categories — memory (6) + clinical (4) + development (2) + sensory (3) + prediction (2) + emotion (2) + motor (2) + learning (1) + cross-modal (1).
6. **Clinical (F10)** models come from 4 different units: IMU(4), MPU(2), ARU(2), NDU(2) — no single unit owns this function.
7. **Social (F9)** is the least represented (4 models) — future expansion area.
