# M³ LOGOS — Vocabulary Specification v1.0

> **"The same truth, spoken at the depth you're ready to hear."**

## 1. Purpose

M³ LOGOS is the **semantic vocabulary layer** of My Musical Mind. It defines how the 131 internal C³ beliefs are translated into human language at four progressively technical depth levels:

| Tier | Domain | Audience | Dimensions | Subscription |
|------|--------|----------|------------|-------------|
| **Surface** | Psychology | Everyone | **6D** | Free |
| **Narrative** | Music Cognition | Curious listeners | **12D** | Basic |
| **Deep** | Neuroscience | Advanced users | **24D** | Premium |
| **Research** | C³ Internals | Scientists / API | **131D** | Special |

Each tier is a **zoom level** into the same underlying data — not a different measurement. A user at the Surface tier sees exactly the same musical reality as a researcher at 131D, just with different granularity and vocabulary.

### 1.1 Relationship to L³

L³ (Lexical LOGOS Lattice) is the 104D semantic interpretation layer in the MI pipeline (α→θ epistemological ladder). M³ LOGOS is the **consumer-facing subset** — it reads L³ output and presents it through the tier system defined here. L³ computes; LOGOS names.

### 1.2 Design Principles

1. **Observe, don't judge.** M³ never says "you are X." It describes its own state or reports data.
2. **Same data, different depth.** Each tier reveals the same underlying computation.
3. **Binary tree.** Every 6D node splits into exactly 2×12D, every 12D into 2×24D.
4. **Every term has a citation.** No dimension exists without published scientific grounding.
5. **Bilingual.** All Surface (6D) terms have Turkish and English canonical forms.

---

## 2. The Hierarchy

```
                    ┌─ Predictive Processing (5 beliefs)
         ┌─ Expectancy ─┤
         │              └─ Information Entropy (5 beliefs)
 DISCOVERY ─┤
 (Keşif)    │              ┌─ Sequence Learning (5 beliefs)
         └─ Information Rate ─┤
                           └─ Sensory Encoding (6 beliefs)

                    ┌─ Harmonic Tension (6 beliefs)
         ┌─ Tension Arc ─┤
         │               └─ Autonomic Arousal (6 beliefs)
INTENSITY ─┤
(Yoğunluk)  │              ┌─ Sensory Salience (6 beliefs)
         └─ Sonic Impact ─┤
                          └─ Aesthetic Appraisal (6 beliefs)

                    ┌─ Oscillation Coupling (5 beliefs)
         ┌─ Entrainment ─┤
         │               └─ Motor Period-Locking (5 beliefs)
  FLOW ────┤
  (Akış)    │         ┌─ Auditory-Motor Integration (5 beliefs)
         └─ Groove ─┤
                    └─ Hierarchical Context (5 beliefs)

                    ┌─ Valence-Mode Circuitry (5 beliefs)
           ┌─ Emotional Contagion ─┤
           │                       └─ Nostalgia Circuitry (5 beliefs)
  DEPTH ────┤
 (Derinlik)  │         ┌─ Dopaminergic Drive (5 beliefs)
           └─ Reward ─┤
                      └─ Hedonic Valuation (6 beliefs)

                    ┌─ Hippocampal Binding (7 beliefs)
              ┌─ Episodic Resonance ─┤
              │                      └─ Autobiographical Network (6 beliefs)
  TRACE ───────┤
   (İz)        │              ┌─ Pitch-Melody Processing (6 beliefs)
              └─ Recognition ─┤
                              └─ Perceptual Learning (7 beliefs)

                    ┌─ Structural Prediction (4 beliefs)
           ┌─ Synchrony ─┤
           │              └─ Expertise Network (5 beliefs)
 SHARING ───┤
(Paylaşım)  │           ┌─ Interpersonal Synchrony (5 beliefs)
           └─ Bonding ─┤
                       └─ Social Reward (5 beliefs)

Total: 6 → 12 → 24 → 131 beliefs
```

---

## 3. Surface Layer — 6D Psychology

The 6 experiential dimensions are self-evident: a user needs no musical training to understand them. Each is a 0–1 scalar per frame (172.27 Hz), presented as a radar chart.

### 3.1 Keşif (Discovery)

| Property | Value |
|----------|-------|
| Index | 0 |
| Key | `discovery` |
| EN | Discovery |
| TR | Keşif |
| Beliefs | 21 (F1 Sensory + F2 Prediction) |
| Gene affinity | entropy |
| Persona family | Explorers |

**What it measures:** How much music surprises, informs, and challenges expectations. High Discovery = the music is taking you somewhere new. Low Discovery = familiar, predictable territory.

**Scientific grounding:**
- **Musical expectancy** (Meyer 1956; Huron 2006 ITPRA theory) — emotion from violated/confirmed predictions
- **Information Dynamics of Music** (Pearce 2005 IDyOM) — statistical learning, information content, Shannon entropy
- **Predictive processing** (Clark 2013; Koelsch et al. 2019) — hierarchical prediction error as the brain's core computation

**High Discovery profile:**
> "Your mind is in exploration mode. The music is rich with unexpected turns — your prediction engine is working hard, generating surprise after surprise. This is where learning happens."

**Low Discovery profile:**
> "The music has become a familiar landscape. Your prediction system has mapped the terrain — there's comfort in knowing what comes next. Your mind is conserving energy."

---

### 3.2 Yoğunluk (Intensity)

| Property | Value |
|----------|-------|
| Index | 1 |
| Key | `intensity` |
| EN | Intensity |
| TR | Yoğunluk |
| Beliefs | 24 (F2 Prediction + F3 Attention + F5 Emotion) |
| Gene affinity | tension |
| Persona family | Alchemists |

**What it measures:** The combined force of harmonic tension, bodily arousal, and sensory impact. High Intensity = music is gripping, demanding, transformative. Low Intensity = calm, gentle, ambient.

**Scientific grounding:**
- **Tonal tension** (Lerdahl & Krumhansl 2007) — distance from tonal center, harmonic syntax
- **Autonomic arousal** (Koelsch 2014; Salimpoor et al. 2009) — heart rate, skin conductance, pupil dilation
- **Salience network** (Menon & Uddin 2010) — detecting what matters in the auditory stream
- **BRECVEMA: Brain stem reflex** (Juslin 2013) — sudden, loud, or dissonant events trigger autonomic response

**High Intensity profile:**
> "Your nervous system is fully engaged. The music is creating powerful tension — harmonic forces pulling in multiple directions, your body responding with heightened alertness."

**Low Intensity profile:**
> "The music creates a gentle field. Tension is minimal, the body is calm. This is a state of low arousal where subtle textures can emerge."

---

### 3.3 Akış (Flow)

| Property | Value |
|----------|-------|
| Index | 2 |
| Key | `flow` |
| EN | Flow |
| TR | Akış |
| Beliefs | 20 (F3 Attention + F7 Motor) |
| Gene affinity | plasticity |
| Persona family | Kineticists |

**What it measures:** How strongly the music locks into your body's sense of time and motion. High Flow = rhythmic entrainment, groove, movement urge. Low Flow = floating, unmetered, free.

**Scientific grounding:**
- **Neural entrainment** (Large & Palmer 2002; Large & Snyder 2009) — oscillatory coupling between auditory cortex and motor system
- **Groove** (Janata et al. 2012; Witek et al. 2014; Madison 2006) — the desire to move, related to moderate syncopation
- **Sensorimotor synchronization** (Repp & Su 2013) — period-locking of internal oscillators to external beat
- **BRECVEMA: Rhythmic entrainment** (Juslin 2013) — body rhythm adjusts to musical rhythm

**High Flow profile:**
> "Your motor system has locked onto the beat. Neural oscillators in your auditory and motor cortices are synchronized — this is entrainment, the basis of groove."

**Low Flow profile:**
> "The music resists rhythmic locking. Your temporal processing is in free mode — no strong beat pulls the body into sync. Time becomes elastic."

---

### 3.4 Derinlik (Depth)

| Property | Value |
|----------|-------|
| Index | 3 |
| Key | `depth` |
| EN | Depth |
| TR | Derinlik |
| Beliefs | 21 (F5 Emotion + F6 Reward) |
| Gene affinity | resonance (emotional) + tension (reward) |
| Persona family | Anchors / Alchemists |

**What it measures:** How deeply the music reaches into your emotional and reward systems. High Depth = strong emotional contagion, pleasure, wanting. Low Depth = emotionally neutral, passing through.

**Scientific grounding:**
- **Emotional contagion** (Juslin & Västfjäll 2004; Koelsch 2014) — perceiving emotion in music and "catching" it
- **Reward circuitry** (Salimpoor et al. 2011, 2013) — dopamine release in caudate (anticipation) → NAcc (consummation)
- **Wanting vs liking** (Berridge & Robinson 2003) — dissociable dopaminergic (wanting) and opioidergic (liking) systems
- **BRECVEMA: Evaluative conditioning + Contagion** (Juslin 2013) — learned emotional associations + mirroring perceived emotion
- **Nostalgia** (Barrett et al. 2010; Janata 2009 PEPAM) — bittersweet self-relevant emotional state triggered by familiar music

**High Depth profile:**
> "The music has penetrated deep. Your reward system is active — dopamine signals anticipation while endorphins color the experience with pleasure. Emotional contagion is strong."

**Low Depth profile:**
> "The music passes through without anchoring emotionally. The reward system is quiet — neither wanting nor avoiding. A neutral state."

---

### 3.5 İz (Trace)

| Property | Value |
|----------|-------|
| Index | 4 |
| Key | `trace` |
| EN | Trace |
| TR | İz |
| Beliefs | 26 (F1 Sensory + F4 Memory + F8 Learning) |
| Gene affinity | resonance (memory) |
| Persona family | Anchors |

**What it measures:** How strongly the music activates memory, recognition, and learned patterns. High Trace = "I know this" — familiarity, nostalgia, pattern recognition. Low Trace = unfamiliar territory, new learning.

**Scientific grounding:**
- **Episodic memory** (Janata 2009 PEPAM; Belfi et al. 2016) — music as cue for autobiographical memories
- **Musical memory** (Halpern & Zatorre 1999) — pitch patterns stored and recognized via hippocampal binding
- **Perceptual learning** (Näätänen et al. 2007 MMN; Pantev et al. 1998) — cortical plasticity from musical exposure
- **Statistical learning** (Saffran et al. 1999; Pearce & Wiggins 2012) — implicit extraction of distributional regularities
- **BRECVEMA: Episodic memory + Visual imagery** (Juslin 2013) — music triggers vivid personal memories and mental images

**High Trace profile:**
> "Strong memory traces are active. The music connects to stored patterns — your hippocampus is binding this moment to past experience. Recognition is high."

**Low Trace profile:**
> "This is new territory. No strong memory traces activate. Your learning system is in acquisition mode — building new representations from scratch."

---

### 3.6 Paylaşım (Sharing)

| Property | Value |
|----------|-------|
| Index | 5 |
| Key | `sharing` |
| EN | Sharing |
| TR | Paylaşım |
| Beliefs | 19 (F7 Motor + F8 Learning + F9 Social) |
| Gene affinity | plasticity + resonance |
| Persona family | Kineticists |

**What it measures:** How much the music invites connection with others — shared experience, synchrony, social bonding. High Sharing = music as social glue. Low Sharing = solitary, introspective experience.

**Scientific grounding:**
- **Social bonding through music** (Dunbar 2012; Tarr et al. 2014) — synchronous music-making releases endorphins, increases trust
- **Neural synchrony** (Abrams et al. 2013; Sachs et al. 2020) — inter-subject correlation of brain activity during shared listening
- **Interpersonal synchrony** (Novembre et al. 2012; Keller et al. 2014) — joint action, coordination, adaptive timing
- **Catchiness** (Jakubowski et al. 2017) — earworm-inducing properties: predictability + distinctive contour
- **BRECVEMA: Musical expectancy** (Juslin 2013) — shared cultural knowledge enables collective anticipation

**High Sharing profile:**
> "This music is built for connection. Its rhythmic and structural properties invite synchrony — your neural patterns would align with anyone listening alongside you."

**Low Sharing profile:**
> "A deeply personal listening space. The music's complexity or intimacy makes it resistant to shared entrainment. This is inner work."

---

## 4. Narrative Layer — 12D Music Cognition

Each 6D dimension splits into 2 music-cognition terms. These use the established vocabulary of music psychology research.

### 4.1 Discovery → Expectancy + Information Rate

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C0 | 0 | `expectancy` | Expectancy | discovery | 10 | Huron 2006 ITPRA; Narmour 1990 Implication-Realization |
| C1 | 1 | `information_rate` | Information Rate | discovery | 11 | Pearce 2005 IDyOM; Shannon 1948; Hansen & Pearce 2014 |

**Expectancy** = How strongly the music activates prediction mechanisms. Measured through prediction accuracy, prediction error magnitude, hierarchical prediction depth.
- ITPRA temporal sequence: Imagination → Tension → Prediction → Reaction → Appraisal
- High expectancy: music strongly engages the prediction engine (whether confirmed or violated)
- Low expectancy: music is either perfectly predictable or too chaotic for prediction

**Information Rate** = How much new information the music delivers per unit time. Measured through sequence complexity, spectral novelty, sensory encoding demand.
- IDyOM information content (IC): − log₂ P(event | context)
- Entropy: average uncertainty across possible continuations
- High information rate: dense, complex, high-novelty signal
- Low information rate: sparse, repetitive, low-novelty signal

---

### 4.2 Intensity → Tension Arc + Sonic Impact

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C2 | 2 | `tension_arc` | Tension Arc | intensity | 12 | Lerdahl & Krumhansl 2007; Koelsch 2014; Farbood 2012 |
| C3 | 3 | `sonic_impact` | Sonic Impact | intensity | 12 | Menon & Uddin 2010 salience; Juslin 2013 brainstem reflex |

**Tension Arc** = The temporal trajectory of harmonic and emotional tension. Builds, sustains, releases. The narrative shape of intensity.
- Harmonic tension: tonal distance, dissonance, unresolved suspensions
- Emotional arousal: autonomic nervous system activation
- Peak detection: climax moments in the tension trajectory

**Sonic Impact** = The immediate, moment-by-moment force of sound on the perceptual system. Not narrative — instantaneous.
- Sensory salience: what captures attention RIGHT NOW
- Aesthetic appraisal: beauty/awe/savoring response
- Timbral character: brightness, roughness, spectral density

---

### 4.3 Flow → Entrainment + Groove

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C4 | 4 | `entrainment` | Entrainment | flow | 10 | Large & Palmer 2002; Grahn & Brett 2007 |
| C5 | 5 | `groove` | Groove | flow | 10 | Janata et al. 2012; Witek et al. 2014; Madison 2006 |

**Entrainment** = Neural oscillation coupling to musical rhythm. The involuntary locking of internal timing to the beat.
- Beat perception: extracting the pulse from the audio stream
- Meter hierarchy: strong vs weak beats, time signature awareness
- Period-locking: motor system synchronizing to tempo

**Groove** = The desire to move. The felt experience of motor engagement with rhythm. Related to but distinct from entrainment.
- Auditory-motor coupling: connection between what you hear and what your body wants to do
- Syncopation sweet spot: moderate complexity drives groove (Witek 2014 inverted-U)
- Context: how the current moment fits into the larger rhythmic structure

---

### 4.4 Depth → Emotional Contagion + Reward

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C6 | 6 | `contagion` | Emotional Contagion | depth | 10 | Juslin & Västfjäll 2004; Koelsch 2014; Barrett et al. 2010 |
| C7 | 7 | `reward` | Reward | depth | 11 | Salimpoor et al. 2011, 2013; Berridge 2003 |

**Emotional Contagion** = Perceiving and "catching" the emotion expressed by the music. Mode detection (happy/sad), nostalgia activation, empathic response.
- Valence-mode circuitry: major/minor mode → happy/sad pathway activation
- Nostalgia: bittersweet self-referential emotion (Barrett et al. 2010)
- BRECVEMA contagion mechanism: music mimics vocal expression → listener mirrors

**Reward** = The brain's pleasure and motivation circuitry responding to music. Wanting (anticipatory) vs liking (consummatory).
- Dopaminergic anticipation: caudate ramp-up before a peak (Salimpoor 2011)
- Hedonic pleasure: NAcc + opioid release at the moment of fulfillment
- Tension-resolution reward: the cycle of wanting → getting → wanting more

---

### 4.5 Trace → Episodic Resonance + Recognition

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C8 | 8 | `episodic_resonance` | Episodic Resonance | trace | 13 | Janata 2009 PEPAM; Belfi et al. 2016 |
| C9 | 9 | `recognition` | Recognition | trace | 13 | Näätänen et al. 2007; Pantev et al. 1998; Saffran 1999 |

**Episodic Resonance** = Music activating personal memories. The PEPAM (Perisylvian Episodic Autobiographical Memory) network connects familiar melodies to specific life episodes.
- Hippocampal binding: linking current sensory input to stored memory traces
- Autobiographical retrieval: vivid recall of personal events, contexts, emotions
- Nostalgia intensity: strength of the self-relevant temporal displacement

**Recognition** = Pattern matching against learned musical knowledge. From pitch identification to trained timbre recognition.
- Pitch-melody processing: contour tracking, interval recognition, octave equivalence
- Perceptual learning: expertise-dependent enhancement (MMN amplitude, cortical representation)
- Statistical model: implicit knowledge of style-specific distributions

---

### 4.6 Sharing → Synchrony + Bonding

| Dim | Index | Key | Name | Parent | Beliefs | Scientific Basis |
|-----|-------|-----|------|--------|---------|-----------------|
| C10 | 10 | `synchrony` | Synchrony | sharing | 9 | Keller et al. 2014; Patel 2014 SSIRH |
| C11 | 11 | `bonding` | Bonding | sharing | 10 | Dunbar 2012; Tarr et al. 2014; Savage et al. 2021 |

**Synchrony** = The music's capacity to align multiple minds in time. Structural predictability, expertise engagement, shared temporal framework.
- Structural prediction: phrase boundaries and form as shared reference points
- Expertise network: MMN, trained responses, shared musical knowledge
- Patel's SSIRH: Speech and Song share an Interlocking Resource Hierarchy

**Bonding** = Music as social glue. The endorphin-mediated warmth of shared musical experience.
- Interpersonal synchrony: moving together, feeling together, neural coupling
- Social reward: pleasure from coordinated action (synchrony reward, group flow)
- Dunbar's endorphin hypothesis: rhythmic synchrony → endorphin release → bonding

---

## 5. Deep Layer — 24D Neuroscience

Each 12D dimension splits into 2 neuroscience terms. These reference specific neural circuits, neurotransmitters, and brain regions.

| # | Key | Name (EN) | Name (TR) | Parent | Beliefs | Neural Correlate |
|---|-----|-----------|-----------|--------|---------|-----------------|
| N0 | `predictive_processing` | Predictive Processing | Tahminsel İşleme | expectancy | 5 | dlPFC, IFG → hierarchical prediction (Koelsch 2019) |
| N1 | `information_entropy` | Information Entropy | Bilgi Entropisi | expectancy | 5 | STG, IFG → statistical model (Pearce 2005; IDyOM) |
| N2 | `sequence_learning` | Sequence Learning | Dizi Öğrenme | information_rate | 5 | IFG, SMA → gamma oscillation, sequence completion |
| N3 | `sensory_encoding` | Sensory Encoding | Duyusal Kodlama | information_rate | 6 | A1/HG, MGB → tonotopic encoding, salience filtering |
| N4 | `harmonic_tension` | Harmonic Tension | Harmonik Gerilim | tension_arc | 6 | OFC, amygdala → tonal syntax violation (Koelsch 2014) |
| N5 | `autonomic_arousal` | Autonomic Arousal | Otonom Uyarılma | tension_arc | 6 | Hypothalamus, PAG, NE system → fight-or-flight cascade |
| N6 | `sensory_salience` | Sensory Salience | Duyusal Belirginlik | sonic_impact | 6 | ACC, insula → salience network (Menon & Uddin 2010) |
| N7 | `aesthetic_appraisal` | Aesthetic Appraisal | Estetik Değerlendirme | sonic_impact | 6 | vmPFC, OFC → beauty/reward integration (Ishizu & Zeki 2011) |
| N8 | `oscillation_coupling` | Oscillation Coupling | Osilasyon Eşleşmesi | entrainment | 5 | A1, SMA → beta/gamma phase-locking (Large & Snyder 2009) |
| N9 | `motor_period_locking` | Motor Period-Locking | Motor Periyot Kilidi | entrainment | 5 | Putamen, SMA, PMC → period correction (Repp & Su 2013) |
| N10 | `auditory_motor` | Auditory-Motor Integration | İşitsel-Motor Entegrasyon | groove | 5 | Putamen → SMA → PMC pathway (Grahn & Rowe 2009) |
| N11 | `hierarchical_context` | Hierarchical Context | Hiyerarşik Bağlam | groove | 5 | IFG, AG → hierarchical temporal structure |
| N12 | `valence_mode` | Valence-Mode Circuitry | Valans-Mod Devresi | contagion | 5 | vmPFC, NAcc → major/minor mode processing |
| N13 | `nostalgia_circuitry` | Nostalgia Circuitry | Nostalji Devresi | contagion | 5 | Hippocampus, vmPFC, OPI system → PEPAM (Janata 2009) |
| N14 | `dopaminergic_drive` | Dopaminergic Drive | Dopaminerjik Dürtü | reward | 5 | VTA → caudate → NAcc, DA system (Salimpoor 2011) |
| N15 | `hedonic_valuation` | Hedonic Valuation | Hedonik Değerleme | reward | 6 | NAcc, OFC, OPI system → liking/pleasure (Berridge 2003) |
| N16 | `hippocampal_binding` | Hippocampal Binding | Hipokampal Bağlama | episodic_resonance | 7 | Hippocampus → fast binding, episodic encoding |
| N17 | `autobiographical` | Autobiographical Network | Otobiyografik Ağ | episodic_resonance | 6 | vmPFC, hippocampus, TP → self-referential memory |
| N18 | `pitch_melody` | Pitch-Melody Processing | Perde-Melodi İşleme | recognition | 6 | A1/HG, STG → tonotopic maps, pitch templates |
| N19 | `perceptual_learning` | Perceptual Learning | Algısal Öğrenme | recognition | 7 | A1/HG expansion, STG → MMN (Näätänen 2007) |
| N20 | `structural_prediction` | Structural Prediction | Yapısal Tahmin | synchrony | 4 | IFG, dlPFC → phrase structure, form awareness |
| N21 | `expertise_network` | Expertise Network | Uzmanlık Ağı | synchrony | 5 | Bilateral STG, PMC → expertise-dependent cortical plasticity |
| N22 | `interpersonal_sync` | Interpersonal Synchrony | Kişilerarası Senkronizasyon | bonding | 5 | mPFC, TPJ → inter-brain coupling (Novembre 2012) |
| N23 | `social_reward` | Social Reward | Sosyal Ödül | bonding | 5 | NAcc, VTA, OPI → endorphin-mediated bonding (Dunbar 2012) |

---

## 6. Research Layer — 131D C³ Beliefs

The full 131 beliefs organized by C³ function. This layer is accessible only with special permission and presents raw system internals.

### 6.1 F1: Sensory Processing (17 beliefs, indices 0–16)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 0 | consonance_salience_gradient | Appraisal | CSG | sensory_encoding |
| 1 | contour_continuation | Anticipation | MPG | pitch_melody |
| 2 | melodic_contour_tracking | Appraisal | MPG | pitch_melody |
| 3 | consonance_trajectory | Anticipation | BCH | information_entropy |
| 4 | harmonic_stability | Core | BCH | harmonic_tension |
| 5 | harmonic_template_match | Appraisal | BCH | harmonic_tension |
| 6 | interval_quality | Appraisal | BCH | harmonic_tension |
| 7 | pitch_continuation | Anticipation | PSCL | information_entropy |
| 8 | pitch_prominence | Core | PSCL | pitch_melody |
| 9 | octave_equivalence | Appraisal | PCCR | pitch_melody |
| 10 | pitch_identity | Core | PCCR | pitch_melody |
| 11 | aesthetic_quality | Core | STAI | aesthetic_appraisal |
| 12 | reward_response_pred | Anticipation | STAI | aesthetic_appraisal |
| 13 | spectral_temporal_synergy | Appraisal | STAI | sensory_encoding |
| 14 | imagery_recognition | Anticipation | MIAA | aesthetic_appraisal |
| 15 | timbral_character | Core | MIAA | sensory_salience |
| 16 | spectral_complexity | Appraisal | SDED | sensory_encoding |

### 6.2 F2: Pattern Recognition & Prediction (15 beliefs, indices 17–31)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 17 | abstract_future | Anticipation | HTP | information_entropy |
| 18 | hierarchy_coherence | Appraisal | HTP | sequence_learning |
| 19 | midlevel_future | Anticipation | HTP | information_entropy |
| 20 | prediction_accuracy | Core | HTP | predictive_processing |
| 21 | prediction_hierarchy | Core | HTP | predictive_processing |
| 22 | arousal_change_pred | Anticipation | ICEM | autonomic_arousal |
| 23 | arousal_scaling | Appraisal | ICEM | autonomic_arousal |
| 24 | defense_cascade | Appraisal | ICEM | sequence_learning |
| 25 | information_content | Core | ICEM | sequence_learning |
| 26 | valence_inversion | Appraisal | ICEM | autonomic_arousal |
| 27 | valence_shift_pred | Anticipation | ICEM | aesthetic_appraisal |
| 28 | error_propagation | Appraisal | SPH | predictive_processing |
| 29 | oscillatory_signature | Appraisal | SPH | sequence_learning |
| 30 | sequence_completion | Anticipation | SPH | information_entropy |
| 31 | sequence_match | Core | SPH | sequence_learning |

### 6.3 F3: Attention & Salience (15 beliefs, indices 32–46)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 32 | consonance_valence_mapping | Appraisal | CSG | pitch_melody |
| 33 | processing_load_pred | Anticipation | CSG | sensory_encoding |
| 34 | salience_network_activation | Core | CSG | sensory_salience |
| 35 | sensory_load | Appraisal | CSG | sensory_encoding |
| 36 | attention_capture | Core | IACM | sensory_salience |
| 37 | attention_shift_pred | Anticipation | IACM | sensory_salience |
| 38 | object_segregation | Appraisal | IACM | sensory_salience |
| 39 | precision_weighting | Appraisal | IACM | sensory_encoding |
| 40 | aesthetic_engagement | Appraisal | AACM | aesthetic_appraisal |
| 41 | savoring_effect | Appraisal | AACM | aesthetic_appraisal |
| 42 | beat_entrainment | Core | SNEM | oscillation_coupling |
| 43 | beat_onset_pred | Anticipation | SNEM | oscillation_coupling |
| 44 | meter_hierarchy | Core | SNEM | oscillation_coupling |
| 45 | meter_position_pred | Anticipation | SNEM | oscillation_coupling |
| 46 | selective_gain | Appraisal | SNEM | oscillation_coupling |

### 6.4 F4: Memory & Retrieval (13 beliefs, indices 47–59)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 47 | melodic_recognition | Appraisal | MMP | hippocampal_binding |
| 48 | memory_preservation | Appraisal | MMP | hippocampal_binding |
| 49 | memory_scaffold_pred | Anticipation | MMP | hippocampal_binding |
| 50 | autobiographical_retrieval | Core | MEAMN | autobiographical |
| 51 | emotional_coloring | Core | MEAMN | autobiographical |
| 52 | memory_vividness | Appraisal | MEAMN | autobiographical |
| 53 | nostalgia_intensity | Core | MEAMN | autobiographical |
| 54 | retrieval_probability | Appraisal | MEAMN | hippocampal_binding |
| 55 | self_relevance | Appraisal | MEAMN | autobiographical |
| 56 | vividness_trajectory | Anticipation | MEAMN | autobiographical |
| 57 | consolidation_strength | Appraisal | HCMC | hippocampal_binding |
| 58 | episodic_boundary | Appraisal | HCMC | hippocampal_binding |
| 59 | episodic_encoding | Core | HCMC | hippocampal_binding |

### 6.5 F5: Emotion (14 beliefs, indices 60–73)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 60 | ans_dominance | Appraisal | AAC | autonomic_arousal |
| 61 | chills_intensity | Appraisal | AAC | sensory_salience |
| 62 | driving_signal | Appraisal | AAC | autonomic_arousal |
| 63 | emotional_arousal | Core | AAC | autonomic_arousal |
| 64 | emotion_certainty | Appraisal | VMM | valence_mode |
| 65 | happy_pathway | Appraisal | VMM | valence_mode |
| 66 | mode_detection | Appraisal | VMM | valence_mode |
| 67 | perceived_happy | Core | VMM | valence_mode |
| 68 | perceived_sad | Core | VMM | valence_mode |
| 69 | sad_pathway | Appraisal | VMM | nostalgia_circuitry |
| 70 | nostalgia_affect | Core | NEMAC | nostalgia_circuitry |
| 71 | nostalgia_peak_pred | Anticipation | NEMAC | nostalgia_circuitry |
| 72 | self_referential_nostalgia | Appraisal | NEMAC | nostalgia_circuitry |
| 73 | wellbeing_enhancement | Anticipation | NEMAC | nostalgia_circuitry |

### 6.6 F6: Reward & Motivation (16 beliefs, indices 74–89)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 74 | da_caudate | Appraisal | DAED | dopaminergic_drive |
| 75 | da_nacc | Appraisal | DAED | dopaminergic_drive |
| 76 | dissociation_index | Appraisal | DAED | dopaminergic_drive |
| 77 | temporal_phase | Appraisal | DAED | dopaminergic_drive |
| 78 | wanting_ramp | Anticipation | DAED | dopaminergic_drive |
| 79 | chills_proximity | Anticipation | SRP | hedonic_valuation |
| 80 | harmonic_tension | Appraisal | SRP | harmonic_tension |
| 81 | liking | Core | SRP | hedonic_valuation |
| 82 | peak_detection | Appraisal | SRP | harmonic_tension |
| 83 | pleasure | Core | SRP | hedonic_valuation |
| 84 | prediction_error | Core | SRP | predictive_processing |
| 85 | prediction_match | Appraisal | SRP | predictive_processing |
| 86 | resolution_expectation | Anticipation | SRP | hedonic_valuation |
| 87 | reward_forecast | Anticipation | SRP | hedonic_valuation |
| 88 | tension | Core | SRP | harmonic_tension |
| 89 | wanting | Core | SRP | hedonic_valuation |

### 6.7 F7: Motor & Timing (17 beliefs, indices 90–106)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 90 | auditory_motor_coupling | Appraisal | HGSIC | auditory_motor |
| 91 | beat_prominence | Appraisal | HGSIC | auditory_motor |
| 92 | groove_quality | Core | HGSIC | auditory_motor |
| 93 | groove_trajectory | Anticipation | HGSIC | auditory_motor |
| 94 | meter_structure | Appraisal | HGSIC | hierarchical_context |
| 95 | motor_preparation | Appraisal | HGSIC | auditory_motor |
| 96 | kinematic_efficiency | Core | PEOM | motor_period_locking |
| 97 | next_beat_pred | Anticipation | PEOM | motor_period_locking |
| 98 | period_entrainment | Core | PEOM | motor_period_locking |
| 99 | period_lock_strength | Appraisal | PEOM | motor_period_locking |
| 100 | timing_precision | Appraisal | PEOM | motor_period_locking |
| 101 | context_depth | Core | HMCE | hierarchical_context |
| 102 | long_context | Appraisal | HMCE | hierarchical_context |
| 103 | medium_context | Appraisal | HMCE | hierarchical_context |
| 104 | phrase_boundary_pred | Anticipation | HMCE | structural_prediction |
| 105 | short_context | Appraisal | HMCE | hierarchical_context |
| 106 | structure_pred | Anticipation | HMCE | structural_prediction |

### 6.8 F8: Learning & Expertise (14 beliefs, indices 107–120)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 107 | detection_accuracy | Appraisal | SLEE | perceptual_learning |
| 108 | multisensory_binding | Appraisal | SLEE | perceptual_learning |
| 109 | statistical_model | Core | SLEE | perceptual_learning |
| 110 | plasticity_magnitude | Appraisal | TSCP | perceptual_learning |
| 111 | trained_timbre_recognition | Core | TSCP | perceptual_learning |
| 112 | compartmentalization_cost | Appraisal | ECT | perceptual_learning |
| 113 | transfer_limitation | Anticipation | ECT | perceptual_learning |
| 114 | expertise_enhancement | Core | ESME | structural_prediction |
| 115 | expertise_trajectory | Anticipation | ESME | structural_prediction |
| 116 | pitch_mmn | Appraisal | ESME | expertise_network |
| 117 | rhythm_mmn | Appraisal | ESME | expertise_network |
| 118 | timbre_mmn | Appraisal | ESME | expertise_network |
| 119 | network_specialization | Core | EDNR | expertise_network |
| 120 | within_connectivity | Appraisal | EDNR | expertise_network |

### 6.9 F9: Social Cognition (10 beliefs, indices 121–130)

| Index | Name | Type | Mechanism | 24D Cluster |
|-------|------|------|-----------|-------------|
| 121 | collective_pleasure_pred | Anticipation | SSRI | social_reward |
| 122 | entrainment_quality | Appraisal | SSRI | interpersonal_sync |
| 123 | group_flow | Appraisal | SSRI | interpersonal_sync |
| 124 | social_bonding | Appraisal | SSRI | interpersonal_sync |
| 125 | social_prediction_error | Appraisal | SSRI | social_reward |
| 126 | synchrony_reward | Appraisal | SSRI | social_reward |
| 127 | catchiness_pred | Anticipation | NSCP | social_reward |
| 128 | neural_synchrony | Core | NSCP | interpersonal_sync |
| 129 | resource_allocation | Appraisal | DDSMI | social_reward |
| 130 | social_coordination | Core | DDSMI | interpersonal_sync |

---

## 7. Persona–Dimension Mapping

Each of the 24 personas has a characteristic 6D radar shape. The persona is determined by which gene is dominant, but the radar shape reveals the full cognitive profile.

### 7.1 Five Families and Their Dimension Signatures

| Family | Dominant Gene | Primary 6D | Secondary 6D | Defining Trait |
|--------|--------------|-----------|-------------|----------------|
| **Alchemists** | tension | Intensity | Depth | Transformation — lives for the build-up and release |
| **Architects** | resolution | Discovery | Trace | Structure — maps the blueprint of sound |
| **Explorers** | entropy | Discovery | Intensity | Novelty — thrives in the unknown |
| **Anchors** | resonance | Depth | Trace | Connection — feels the emotional thread |
| **Kineticists** | plasticity | Flow | Sharing | Motion — the beat is the brain |

### 7.2 All 24 Personas with 6D Profiles

Profiles are approximate characteristic shapes (0–1 scale). Individual users will vary.

| ID | Name | Family | Discovery | Intensity | Flow | Depth | Trace | Sharing |
|----|------|--------|-----------|-----------|------|-------|-------|---------|
| 1 | Dopamine Seeker | Alchemists | 0.50 | 0.90 | 0.45 | 0.75 | 0.30 | 0.35 |
| 6 | Tension Architect | Alchemists | 0.55 | 0.95 | 0.35 | 0.55 | 0.40 | 0.25 |
| 7 | Contrast Addict | Alchemists | 0.60 | 0.80 | 0.45 | 0.50 | 0.35 | 0.40 |
| 18 | Dramatic Arc | Alchemists | 0.45 | 0.85 | 0.30 | 0.70 | 0.50 | 0.20 |
| 2 | Harmonic Purist | Architects | 0.70 | 0.30 | 0.25 | 0.55 | 0.75 | 0.20 |
| 4 | Minimal Zen | Architects | 0.35 | 0.15 | 0.25 | 0.50 | 0.60 | 0.20 |
| 5 | Resolution Junkie | Architects | 0.75 | 0.55 | 0.25 | 0.45 | 0.65 | 0.15 |
| 9 | Pattern Hunter | Architects | 0.80 | 0.30 | 0.30 | 0.25 | 0.70 | 0.30 |
| 20 | Precision Mind | Architects | 0.65 | 0.30 | 0.40 | 0.20 | 0.75 | 0.35 |
| 3 | Chaos Explorer | Explorers | 0.92 | 0.80 | 0.35 | 0.20 | 0.25 | 0.30 |
| 10 | Sonic Nomad | Explorers | 0.85 | 0.65 | 0.45 | 0.20 | 0.25 | 0.40 |
| 19 | Curious Wanderer | Explorers | 0.70 | 0.45 | 0.35 | 0.40 | 0.35 | 0.30 |
| 23 | Edge Runner | Explorers | 0.88 | 0.75 | 0.30 | 0.15 | 0.20 | 0.25 |
| 24 | Renaissance Mind | Explorers | 0.65 | 0.65 | 0.50 | 0.50 | 0.50 | 0.50 |
| 8 | Structural Romantic | Anchors | 0.40 | 0.55 | 0.30 | 0.80 | 0.70 | 0.25 |
| 11 | Emotional Anchor | Anchors | 0.30 | 0.45 | 0.25 | 0.90 | 0.65 | 0.25 |
| 13 | Tonal Dreamer | Anchors | 0.25 | 0.15 | 0.20 | 0.70 | 0.55 | 0.20 |
| 15 | Quiet Observer | Anchors | 0.30 | 0.30 | 0.20 | 0.65 | 0.55 | 0.15 |
| 17 | Ambient Flow | Anchors | 0.20 | 0.10 | 0.25 | 0.75 | 0.50 | 0.20 |
| 22 | Nostalgic Soul | Anchors | 0.20 | 0.20 | 0.25 | 0.80 | 0.85 | 0.25 |
| 12 | Rhythmic Pulse | Kineticists | 0.40 | 0.50 | 0.85 | 0.30 | 0.30 | 0.55 |
| 14 | Dynamic Storm | Kineticists | 0.65 | 0.85 | 0.70 | 0.25 | 0.20 | 0.50 |
| 16 | Groove Mechanic | Kineticists | 0.35 | 0.30 | 0.88 | 0.25 | 0.35 | 0.55 |
| 21 | Raw Energy | Kineticists | 0.55 | 0.55 | 0.75 | 0.20 | 0.20 | 0.45 |

### 7.3 Persona Determination

A user's active persona is determined by their **dominant gene** (highest of the 5 Mind Genes). Within a family, the specific persona is selected by the full gene profile using nearest-neighbor matching against the canonical gene values.

**Gene → Family mapping:**
- entropy → Explorers (4 personas: Chaos Explorer, Sonic Nomad, Curious Wanderer, Edge Runner, Renaissance Mind)
- resolution → Architects (5 personas: Harmonic Purist, Minimal Zen, Resolution Junkie, Pattern Hunter, Precision Mind)
- tension → Alchemists (4 personas: Dopamine Seeker, Tension Architect, Contrast Addict, Dramatic Arc)
- resonance → Anchors (6 personas: Structural Romantic, Emotional Anchor, Tonal Dreamer, Quiet Observer, Ambient Flow, Nostalgic Soul)
- plasticity → Kineticists (4 personas: Rhythmic Pulse, Dynamic Storm, Groove Mechanic, Raw Energy)

---

## 8. Observation Vocabulary

M³ communicates with users through **observations** — structured text that follows the "observe, don't judge" principle. Each observation references specific dimensions.

### 8.1 Template Structure

```
[Surface]     "Your {6D_name} is {high|low|rising|falling}."
[Narrative]   "The music's {12D_name} is {description}."
[Deep]        "Active {24D_name}: {neural_description}."
```

### 8.2 Polarity Descriptors

Each dimension has high/low verbal anchors:

| 6D | High | Low |
|----|------|-----|
| Discovery | "exploring new territory" | "in familiar waters" |
| Intensity | "fully charged" | "gentle and calm" |
| Flow | "locked in the groove" | "floating freely" |
| Depth | "deeply moved" | "emotionally neutral" |
| Trace | "strong memory echoes" | "new ground" |
| Sharing | "connected outward" | "turned inward" |

### 8.3 Tier-Gated Observation Examples

**Same moment, three depths:**

| Tier | Observation |
|------|-------------|
| Free (6D) | "Right now your Discovery is high and Flow is rising — the music is pulling you into unexplored rhythmic territory." |
| Basic (12D) | "The Expectancy channel is firing — your prediction engine keeps getting surprised. Entrainment is building as the beat locks in." |
| Premium (24D) | "Predictive Processing shows elevated prediction error (dlPFC active). Oscillation Coupling is increasing — beta-band phase-locking detected." |

---

## 9. Cross-Reference Tables

### 9.1 BRECVEMA → LOGOS Mapping

| BRECVEMA Mechanism (Juslin 2013) | 12D Cognition Dim | 6D Psychology Dim |
|----------------------------------|-------------------|-------------------|
| Brain stem reflex | Sonic Impact | Intensity |
| Rhythmic entrainment | Entrainment | Flow |
| Evaluative conditioning | Episodic Resonance | Trace |
| Emotional contagion | Emotional Contagion | Depth |
| Visual imagery | Episodic Resonance | Trace |
| Episodic memory | Episodic Resonance | Trace |
| Musical expectancy | Expectancy | Discovery |
| Aesthetic judgment | Reward | Depth |

### 9.2 GEMS-9 → LOGOS Mapping

| GEMS Factor (Zentner 2008) | Primary 6D | Secondary 6D |
|---------------------------|-----------|-------------|
| Wonder | Discovery | Depth |
| Transcendence | Depth | Trace |
| Tenderness | Depth | Trace |
| Nostalgia | Trace | Depth |
| Peacefulness | Flow | Depth |
| Power | Intensity | Flow |
| Joyful activation | Flow | Intensity |
| Tension | Intensity | Discovery |
| Sadness | Depth | Trace |

### 9.3 BMRQ → LOGOS Mapping

| BMRQ Factor (Mas-Herrero 2013) | Primary 6D | Gene |
|-------------------------------|-----------|------|
| Musical Seeking | Discovery | entropy |
| Emotion Evocation | Depth | resonance |
| Mood Regulation | Depth + Flow | resonance + plasticity |
| Social Reward | Sharing | plasticity |
| Sensory-Motor | Flow | plasticity |

### 9.4 MUSIC Model → LOGOS Mapping

| MUSIC Factor (Rentfrow 2011) | Primary 6D | Persona Family |
|------------------------------|-----------|---------------|
| Mellow | Depth (low Intensity) | Anchors |
| Unpretentious | Flow + Trace | Anchors/Kineticists |
| Sophisticated | Discovery + Trace | Architects |
| Intense | Intensity | Alchemists |
| Contemporary | Flow + Discovery | Explorers/Kineticists |

---

## 10. Validated Scale Alignments

The following established psychometric instruments map onto M³ LOGOS dimensions:

| Instrument | Ref | Dimensions | LOGOS Alignment |
|-----------|-----|------------|----------------|
| BMRQ | Mas-Herrero et al. 2013 | 5 factors | See §9.3 |
| GEMS-9 | Zentner et al. 2008 | 9 factors | See §9.2 |
| MUSIC | Rentfrow et al. 2011 | 5 factors | See §9.4 |
| Gold-MSI | Müllensiefen et al. 2014 | 5 factors | Trace (active engagement), Discovery (perceptual abilities) |
| Groove Scale | Witek et al. 2014 | 2 factors (wanting to move, pleasure) | Flow, Depth |
| MEC (chills) | Goldstein 1980; Craig 2005 | 1 factor | Intensity × Depth interaction |
| ASI (absorption) | Tellegen & Atkinson 1974 | 1 factor | Depth × Flow interaction |
| STOMP | Rentfrow & Gosling 2003 | 4 factors | Maps to persona families |

---

## 11. Implementation Reference

### 11.1 Code Location

```
Musical_Intelligence/brain/dimensions/
├── _dimension.py        — Dimension dataclass (frozen)
├── tree.py              — 42 dimension definitions (6 + 12 + 24)
├── registry.py          — ALL_PSYCHOLOGY, ALL_COGNITION, ALL_NEUROSCIENCE
├── interpreter.py       — DimensionInterpreter: beliefs(B,T,131) → DimensionState
└── __init__.py          — Public API

Musical_Intelligence/contracts/dataclasses/brain_output.py
└── DimensionState       — psychology(B,T,6), cognition(B,T,12), neuroscience(B,T,24)
```

### 11.2 Aggregation Formula

```
24D[i] = mean(beliefs[j] for j in neuroscience_dim[i].belief_indices)
12D[i] = mean(24D[child_0], 24D[child_1])
 6D[i] = mean(12D[child_0], 12D[child_1])
```

### 11.3 Computation Cost

- Input: (B, T, 131) float32
- Output: (B, T, 6) + (B, T, 12) + (B, T, 24) = (B, T, 42)
- Cost: ~42 gather + mean operations per frame. Negligible vs C³ kernel.

---

## 12. References

### Core Frameworks
- Juslin, P. N. (2013). From everyday emotions to aesthetic emotions: Towards a unified theory of musical emotions. *Physics of Life Reviews*, 10(3), 235–266. **[BRECVEMA]**
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press. **[ITPRA]**
- Pearce, M. T. (2005). *The Construction and Evaluation of Statistical Models of Melodic Structure in Music Perception and Composition*. City University London. **[IDyOM]**
- Koelsch, S. (2014). Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15, 170–180.

### Reward and Dopamine
- Salimpoor, V. N., et al. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14, 257–262.
- Salimpoor, V. N., et al. (2013). Interactions between the nucleus accumbens and auditory cortices predict music reward value. *Science*, 340, 216–219.
- Berridge, K. C., & Robinson, T. E. (2003). Parsing reward. *Trends in Neurosciences*, 26(9), 507–513. **[Wanting vs Liking]**

### Entrainment and Groove
- Large, E. W., & Palmer, C. (2002). Perceiving temporal regularity in music. *Cognitive Science*, 26, 1–37.
- Large, E. W., & Snyder, J. S. (2009). Pulse and meter as neural resonance. *Annals of the New York Academy of Sciences*, 1169, 46–57.
- Witek, M. A. G., et al. (2014). Syncopation, body-movement and pleasure in groove music. *PLoS ONE*, 9(4), e94446.
- Janata, P., et al. (2012). Sensorimotor coupling in music and the psychology of the groove. *Journal of Experimental Psychology: General*, 141(1), 54–75.
- Grahn, J. A., & Rowe, J. B. (2009). Feeling the beat: Premotor and striatal interactions in musicians and nonmusicians during beat perception. *Journal of Neuroscience*, 29, 7540–7548.

### Memory and Nostalgia
- Janata, P. (2009). The neural architecture of music-evoked autobiographical memories. *Cerebral Cortex*, 19, 2579–2594. **[PEPAM]**
- Barrett, F. S., et al. (2010). Music-evoked nostalgia: Affect, memory, and personality. *Emotion*, 10(3), 390–403.
- Belfi, A. M., et al. (2016). Rapid timing of musical aesthetic judgments. *Journal of Experimental Psychology: General*, 145, 1531–1543.

### Social and Bonding
- Dunbar, R. I. M. (2012). On the evolutionary function of song and dance. In N. Bannan (Ed.), *Music, Language, and Human Evolution*. Oxford University Press.
- Tarr, B., Launay, J., & Dunbar, R. I. M. (2014). Music and social bonding: "Self-other" merging and neurohormonal mechanisms. *Frontiers in Psychology*, 5, 1096.
- Novembre, G., et al. (2012). Empathy and interpersonal synchronization in joint musical performance. *Social Cognitive and Affective Neuroscience*, 7, 895–903.

### Scales and Measurement
- Mas-Herrero, E., et al. (2013). Dissociation between musical and monetary reward responses in specific musical anhedonia. *Current Biology*, 23, 1–6. **[BMRQ]**
- Zentner, M., Grandjean, D., & Scherer, K. R. (2008). Emotions evoked by the sound of music: Characterization, classification, and measurement. *Emotion*, 8, 494–521. **[GEMS]**
- Rentfrow, P. J., Goldberg, L. R., & Levitin, D. J. (2011). The structure of musical preferences: A five-factor model. *Journal of Personality and Social Psychology*, 100(6), 1139–1157. **[MUSIC model]**
- Müllensiefen, D., et al. (2014). The musicality of non-musicians: An index for assessing musical sophistication in the general population. *PLoS ONE*, 9(2), e89642. **[Gold-MSI]**
- Näätänen, R., et al. (2007). The mismatch negativity (MMN) in basic research of central auditory processing. *Clinical Neurophysiology*, 118, 2544–2590. **[MMN/Perceptual Learning]**

### Prediction and Information
- Meyer, L. B. (1956). *Emotion and Meaning in Music*. University of Chicago Press.
- Narmour, E. (1990). *The Analysis and Cognition of Basic Melodic Structures*. University of Chicago Press. **[Implication-Realization]**
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36, 181–204.
- Hansen, N. C., & Pearce, M. T. (2014). Predictive uncertainty in auditory sequence processing. *Frontiers in Psychology*, 5, 1052.

### Aesthetic Experience
- Ishizu, T., & Zeki, S. (2011). Toward a brain-based theory of beauty. *PLoS ONE*, 6(7), e21852.
- Menninghaus, W., et al. (2019). What are aesthetic emotions? *Psychological Review*, 126(2), 171–195.
- Lerdahl, F., & Krumhansl, C. L. (2007). Modeling tonal tension. *Music Perception*, 24(4), 329–366.

### Neural Architecture
- Menon, V., & Uddin, L. Q. (2010). Saliency, switching, attention and control: A network model of insula function. *Brain Structure and Function*, 214, 655–667.
- Repp, B. H., & Su, Y.-H. (2013). Sensorimotor synchronization: A review of recent research. *Psychonomic Bulletin & Review*, 20, 403–452.
- Patel, A. D. (2014). The evolutionary biology of musical rhythm: Was Darwin wrong? *PLoS Biology*, 12(3), e1001821. **[SSIRH]**

---

## Appendix A: Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-27 | Initial specification. 6→12→24→131 hierarchy, 24 personas, observation vocabulary. |

## Appendix B: Glossary

| Term | Definition |
|------|-----------|
| **Belief** | One of 131 C³ internal state variables, updated per-frame via Bayesian or observe-only cycle. |
| **Core belief** | Full Bayesian predict→observe→update cycle with τ (time constant) and β₀ (baseline). |
| **Appraisal belief** | Observe-only — no prediction or update. |
| **Anticipation belief** | Forward prediction — forecasts future state. |
| **Gene** | One of 5 learnable parameters (entropy, resolution, tension, resonance, plasticity) that define a user's M³ profile. |
| **Persona** | One of 24 canonical listening personality types, determined by gene profile. |
| **Family** | One of 5 persona groups (Alchemists, Architects, Explorers, Anchors, Kineticists). |
| **Observation** | M³'s structured text output to the user, following "observe, don't judge" policy. |
| **Tier** | Subscription-gated depth level (Free=6D, Basic=12D, Premium=24D, Research=131D). |
| **BRECVEMA** | Juslin's 8-mechanism model: Brainstem reflex, Rhythmic entrainment, Evaluative conditioning, Contagion, Visual imagery, Episodic memory, Musical expectancy, Aesthetic judgment. |
| **ITPRA** | Huron's temporal model: Imagination → Tension → Prediction → Reaction → Appraisal. |
| **IDyOM** | Information Dynamics of Music — computational model of auditory expectation using variable-order Markov chains. |
| **PEPAM** | Perisylvian Episodic-Autobiographical Memory network — music-specific memory retrieval circuit (Janata 2009). |
| **MMN** | Mismatch Negativity — ERP component reflecting automatic prediction error, larger in trained musicians. |
