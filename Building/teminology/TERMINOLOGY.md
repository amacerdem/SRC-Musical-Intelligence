# MI C³ Terminology

**Version**: 1.0.0
**Date**: 2026-02-15
**Status**: ACTIVE — All code, docs, and communication must use these terms.

---

## 1. The Problem This Solves

The word "model" was used for all 96 components, implying they are independent peers.
They are not. They form a **5-depth hierarchy** where a Relay's output feeds an Encoder,
whose output feeds an Associator, and so on. Calling them all "model" hides this
structure. The new terminology makes the hierarchy **visible from the name alone**.

---

## 2. The Five Roles

Every component in the C³ brain has exactly one **role**. The role determines:
- What it can read (input signature)
- Where it sits in the execution order (processing depth)
- Its base class in code
- Its directory location
- Its single-letter code in naming conventions

### 2.1 Relay (R) — Depth 0

| Property | Value |
|----------|-------|
| **Full name** | Relay |
| **Code** | R |
| **Processing depth** | 0 |
| **Count** | 9 (one per unit) |
| **Reads** | R³ + H³ only — no other components |
| **Neuroscience basis** | First-order thalamic/brainstem relay nucleus. Converts raw sensory signal into the unit's foundational representation. Like LGN for vision, MGN for audition, cochlear nucleus for spectral analysis. |
| **Defining property** | The ONLY role that touches raw R³/H³ input directly. All other roles receive processed signals. |

**Examples**:
| Unit | Relay | What it does |
|------|-------|-------------|
| SPU | BCH | Raw spectral → consonance hierarchy (12D) |
| STU | HMCE | Raw temporal → hierarchical context encoding (13D) |
| IMU | MEAMN | Raw features → autobiographical memory network (12D) |
| ASU | SNEM | Raw features → selective neural entrainment (12D) |
| NDU | MPG | Raw features → melodic processing gradient (10D) |
| MPU | PEOM | Raw features → period entrainment optimization (11D) |
| PCU | HTP | Raw features → hierarchical temporal prediction (12D) |
| ARU | SRP | Pathway inputs + R³/H³ → striatal reward pathway (19D) |
| RPU | DAED | Pathway inputs + R³/H³ → dopamine anticipation-experience (8D) |

**Note**: ARU.SRP and RPU.DAED are special Relays — they also receive cross-unit
pathway inputs because they sit at the head of dependent units. They are still Relays
because they are the foundational transformation within their unit.

---

### 2.2 Encoder (E) — Depth 1

| Property | Value |
|----------|-------|
| **Full name** | Encoder |
| **Code** | E |
| **Processing depth** | 1 |
| **Count** | ~23 |
| **Reads** | R³ + H³ + Relay output from same unit |
| **Neuroscience basis** | Primary cortical feature detector. Like orientation columns in V1, frequency-tuned neurons in A1, pitch-selective cells in auditory belt. Extracts specific features from the Relay's foundational representation. |
| **Defining property** | Depends on exactly ONE upstream role (the unit's Relay). |

**Examples**:
| Unit | Encoder | Reads from | What it does |
|------|---------|-----------|-------------|
| SPU | PSCL | BCH.f01_nps | Cortical pitch salience localization |
| SPU | STAI | BCH.consonance_signal + PSCL.pitch_salience | Spectral timbre aesthetic integration |
| STU | AMSC | HMCE.context_depth | Auditory-motor stream coupling |
| STU | MDNS | HMCE.context_depth | Melody decoding neural substrate |
| IMU | PNH | MEAMN (familiarity context) | Pythagorean neural hierarchy |
| IMU | MMP | MEAMN (memory pathways) | Musical mnemonic preservation |
| ASU | IACM | BEP/ASA (shared with SNEM) | Inharmonic attention capture |
| ASU | CSG | BEP/ASA (shared with SNEM) | Consonance salience gradient |
| NDU | SDD | MPG.gradient_ratio | Supramodal deviance detection |
| MPU | MSR | PEOM (synchrony baseline) | Motor sensorimotor reorganization |
| PCU | SPH | HTP.hierarchy_gradient | Spatiotemporal prediction hierarchy |
| PCU | ICEM | HTP.hierarchy_gradient + SPH.prediction_error | Information content emotion model |
| ARU | AAC | SRP (AED+CPD shared) | Autonomic-affective coupling |
| ARU | VMM | SRP (AED+C0P shared) | Valence-mode mapping |
| RPU | MORMR | DAED (chills → DA coupling) | Mu-opioid receptor music reward |
| RPU | RPEM | DAED (RPE → caudate learning) | Reward prediction error model |
| RPU | IUCP | DAED (preference → DA anticipation) | Inverted-U complexity preference |
| RPU | MCCN | DAED + MORMR.network_state | Musical chills cortical network |
| STU | AMSS | HMCE.structure_predict | Auditory multi-stream segregation |
| STU | ETAM | HMCE.context_depth + AMSC.auditory_activatn | Envelope tracking attention modulation |
| STU | OMS | HMCE.context_depth + AMSC.motor_preparation | Oscillatory motor synchronization |
| STU | NEWMD | HMCE.context_depth + AMSC.motor_coupling | Neural entrainment WM dual-route |
| STU | MTNE | HMCE.context_depth | Musical training neural efficiency |
| STU | MPFS | HMCE.context_depth + AMSC.motor_coupling | Musical prodigy flow state |
| NDU | EDNR | MPG (processing efficiency context) | Expertise-dependent network reorganization |
| NDU | DSP | PPC/ASA mechanisms (shared with MPG) | Developmental singing plasticity |
| MPU | GSSM | PEOM (variability baseline) | Gait-synchronized stimulation model |
| MPU | ASAP | PEOM (prediction for entrainment) | Auditory-motor simulation & action prediction |
| IMU | PMIM | MEAMN.memory_state + PNH.ratio_enc | Predictive memory integration model |
| IMU | HCMC | MEAMN (retrieval triggers) | Hippocampal-cortical memory circuit |
| IMU | CDEM | MEAMN (autobiographical memory) | Context-dependent emotional memory |
| IMU | DMMS | MEAMN (bidirectional) | Developmental memory music scaffold |
| ASU | BARM | SNEM (entrainment strength) | Beat alignment regularization model |
| ASU | STANM | SNEM + IACM (spectral attention) | Spectral-temporal attention network model |

---

### 2.3 Associator (A) — Depth 2

| Property | Value |
|----------|-------|
| **Full name** | Associator |
| **Code** | A |
| **Processing depth** | 2 |
| **Count** | ~30 |
| **Reads** | R³ + H³ + Relay output + Encoder outputs from same unit |
| **Neuroscience basis** | Association cortex. Like auditory parabelt, temporal-parietal junction, Wernicke's area. Combines multiple encoded features into higher-order representations. "Cell assemblies" (Hebb 1949) — coordinated groups that bind features. |
| **Defining property** | Reads from TWO OR MORE upstream roles (Relay + Encoder, or multiple Encoders). |

**Examples**:
| Unit | Associator | Reads from | What it does |
|------|-----------|-----------|-------------|
| SPU | PCCR | BCH.f02_harmonicity + PSCL.f01_salience | Pitch chroma cortical representation |
| SPU | TSCP | BCH.f02_harmonicity + PCCR.chroma_tuning | Timbre-specific cortical plasticity |
| SPU | SDNPS | BCH.f01_nps (challenges BCH universality) | Stimulus-dependent NPS |
| STU | TPIO | HMCE + AMSC.motor_coupling | Timbre perception-imagery overlap |
| STU | EDTA | AMSC.groove_response | Expertise-dependent tempo accuracy |
| STU | HGSIC | AMSC.auditory_activatn + ETAM.entrainment | High-gamma sensorimotor integration |
| STU | TMRM | AMSC + EDTA | Tempo reproduction motor model |
| STU | PTGMP | AMSC + TPIO | Piano training grey matter plasticity |
| IMU | RASN | MEAMN (through BEP* cross-circuit) | Rhythmic auditory stimulation neuroplasticity |
| IMU | OII | MEAMN + PMIM + PNH + HCMC | Oscillatory intelligence integration |
| IMU | MSPBA | PNH.ratio_enc + PMIM | Musical syntax processing in Broca's area |
| IMU | TPRD | PNH + PMIM + MSPBA | Tonotopy-pitch representation dissociation |
| IMU | CSSL | MEAMN + DMMS + HCMC + PMIM | Cross-species song learning |
| ASU | AACM | CSG + STANM + IACM.precision | Aesthetic appreciation cognitive model |
| ASU | PWSM | IACM.precision + SNEM.stability + CSG | Precision-weighted surprise model |
| ASU | DGTP | BARM.regularization + SNEM.timing | Domain-general timing precision |
| ASU | SDL | STANM + PWSM + IACM.demand | Spectral dynamic lateralization |
| NDU | CDMR | MPG.melodic_context + SDD.deviance | Context-dependent mismatch response |
| NDU | SLEE | SDD.supramodal_index + EDNR | Statistical learning expertise effect |
| NDU | SDDP | DSP.sex_modulation | Sex-dependent developmental plasticity |
| NDU | ONI | DSP.plasticity + SDDP.intervention | Over-normalization intervention |
| MPU | SPMC | MSR.efficiency + ASAP.motor_simulation | Sensorimotor planning motor circuit |
| MPU | DDSMI | ASAP.dorsal_stream + PEOM | Dance-DJ social motor integration |
| MPU | NSCP | PEOM + GSSM + DDSMI | Neural synchrony catchiness prediction |
| MPU | CTBB | SPMC + PEOM + ASAP | Cerebellar timing brain-body |
| PCU | PWUP | HTP.hierarchy_gradient + ICEM.information | Precision-weighted uncertainty processing |
| PCU | CHPI | HTP + PWUP.tonal_precision + ICEM | Cross-modal harmonic prediction integration |
| ARU | PUPF | SRP + AAC + VMM | Prediction-uncertainty-pleasure framework |
| ARU | CLAM | SRP + AAC + PUPF.entropy | Closed-loop affective modulation |
| ARU | MAD | SRP + AAC + PUPF | Musical anhedonia deficit |
| ARU | NEMAC | SRP + AAC + PUPF | Nostalgia-enhanced musical affect circuit |
| RPU | MEAMR | RPEM + DAED + MORMR | Music-evoked autobiographical memory reward |
| RPU | SSRI | DAED + MORMR + RPEM + MCCN | Social synchrony reward integration |
| RPU | LDAC | RPEM + IUCP + MORMR + DAED | Liking-driven auditory cortex |
| RPU | IOTMS | MORMR + DAED + RPEM + MCCN | Individual opioid trait music sensitivity |

---

### 2.4 Integrator (I) — Depth 3

| Property | Value |
|----------|-------|
| **Full name** | Integrator |
| **Code** | I |
| **Processing depth** | 3 |
| **Count** | ~28 |
| **Reads** | R³ + H³ + all upstream outputs (R + E + A) from same unit + optional cross-unit |
| **Neuroscience basis** | Connector hub in connectomics. Like angular gyrus (cross-modal), anterior insula (interoception-emotion), dlPFC (executive integration). High betweenness centrality, bridges sub-networks. |
| **Defining property** | Reads from Associator outputs. Deepest intra-unit processing before convergence. Often produces the unit's "signature" outputs for cross-unit pathways. |

**Examples**:
| Unit | Integrator | Reads from | What it does |
|------|-----------|-----------|-------------|
| SPU | MIAA | TSCP.timbre_identity + BCH.f01_nps | Musical imagery auditory activation |
| SPU | ESME | BCH.f01_nps + TSCP.plasticity + SDED | Expertise-specific MMN enhancement |
| SPU | SDED | BCH.consonance + SDNPS.roughness_corr | Sensory dissonance early detection |
| IMU | RIRI | RASN + MEAMN + MMP + HCMC | RAS-intelligent rehabilitation integration |
| IMU | VRIAP | HCMC + MEAMN + RIRI | VR immersive analgesia protocol |
| IMU | CMAPCC | MEAMN + MMP + RASN + RIRI | Cross-modal action-perception common code |
| NDU | ECT | EDNR.network + SLEE.detection | Efficiency-connectivity trade-off |
| MPU | VRMSME | SPMC + DDSMI | VR music-synchronized motor enhancement |
| MPU | STC | MSR + SPMC + VRMSME | Singing-training connectivity |
| PCU | WMED | PWUP.precision_weight | Working memory entrainment dissociation |
| PCU | UDP | PWUP.uncertainty + WMED.wm_contribution | Uncertainty-driven pleasure |
| PCU | IGFE | WMED.wm_contribution + HTP.hierarchy | Isochronous gamma frequency enhancement |
| ARU | DAP | SRP + NEMAC + PUPF | Developmental affective plasticity |
| ARU | CMAT | SRP + CLAM + DAP | Cross-modal affective transfer |
| RPU | SSPS | IUCP + RPEM + DAED + LDAC | Saddle surface preference structure |

---

### 2.5 Hub (H) — Depth 4-5

| Property | Value |
|----------|-------|
| **Full name** | Hub |
| **Code** | H |
| **Processing depth** | 4 or 5 |
| **Count** | ~6 |
| **Reads** | Everything — full intra-unit + cross-unit inputs |
| **Neuroscience basis** | Rich-club node in connectomics. Like vmPFC (value convergence), posterior cingulate (default mode hub), precuneus (global integration). Highest degree, highest betweenness, most metabolically expensive. |
| **Defining property** | Reads from Integrator outputs. Sits at the TOP of its unit's hierarchy. Produces the unit's most abstract, integrated outputs. Rare — most units have 0-2 Hubs. |

**Examples**:
| Unit | Hub | Reads from | What it does |
|------|-----|-----------|-------------|
| PCU | MAA | UDP.pleasure + PWUP.uncertainty + IGFE.gamma | Musical aesthetic appreciation — convergence of prediction, uncertainty, and pleasure |
| PCU | PSH | HTP + PWUP + UDP + WMED + MAA + SPH | Predictive silencing hypothesis — deepest PCU integration, reads ALL other PCU components |
| ARU | TAR | ALL other ARU components | Therapeutic affective resonance — system-wide clinical integration, reads every ARU signal |

---

## 3. Naming Convention

### 3.1 Full Reference Format

```
{UNIT}-{ROLE_CODE}-{ACRONYM}
```

| Component | Old Name | New Name |
|-----------|----------|----------|
| Brainstem Consonance Hierarchy | SPU-α1-BCH | **SPU-R-BCH** |
| Pitch Salience Cortical Local. | SPU-α2-PSCL | **SPU-E-PSCL** |
| Pitch Chroma Cortical Repr. | SPU-α3-PCCR | **SPU-A-PCCR** |
| Musical Imagery Auditory Act. | SPU-β3-MIAA | **SPU-I-MIAA** |
| Musical Aesthetic Appreciation | PCU-γ2-MAA | **PCU-H-MAA** |
| Therapeutic Affective Resonance | ARU-γ3-TAR | **ARU-H-TAR** |

### 3.2 Reading the Name

`SPU-E-PSCL` reads as: "PSCL is an **Encoder** in the **SPU** unit."

You know instantly:
- **SPU** = Spectral Processing Unit
- **E** = Encoder = Depth 1 = reads Relay output + R³/H³
- **PSCL** = Pitch Salience Cortical Localization

### 3.3 Short Forms

| Context | Format | Example |
|---------|--------|---------|
| Full reference | `SPU-R-BCH` | In docs, cross-references |
| Within unit | `R:BCH` | When unit is obvious from context |
| In code (class) | `BCH` | The Python class name stays short |
| In code (attr) | `BCH.ROLE = "relay"` | Role is a class constant |
| In paths | `units/spu/relays/bch.py` | Directory = role |
| In diagrams | `R.BCH → E.PSCL → A.PCCR` | Data flow |

---

## 4. Tier (Evidence Quality) — Still Exists, Different Axis

**Role** (R/E/A/I/H) = computational position in the processing hierarchy.
**Tier** (alpha/beta/gamma) = strength of scientific evidence.

These are independent axes:

| Tier | Meaning | Where it lives |
|------|---------|---------------|
| **alpha** | Direct neural measurement, k ≥ 10 studies | `metadata.evidence_tier` |
| **beta** | Indirect/computational evidence, k = 3-9 | `metadata.evidence_tier` |
| **gamma** | Theoretical/single-study, k < 3 | `metadata.evidence_tier` |

Tier is NOT in the name anymore. It is metadata — queryable, filterable, but not a structural axis.

**Cross-reference**: A beta-tier component can be any role. STAI is beta-1 (evidence)
but an Encoder (role). These are different things — evidence quality vs processing position.

---

## 5. Data Types Inside a Component

Every Relay/Encoder/Associator/Integrator/Hub file contains these **7 data categories**:

### 5.1 Identity (static)

```python
NAME = "BCH"                        # Short identifier
FULL_NAME = "Brainstem Consonance Hierarchy"
UNIT = "SPU"                        # Parent unit
ROLE = "relay"                      # R/E/A/I/H
PROCESSING_DEPTH = 0                # 0-5
OUTPUT_DIM = 12                     # Total tensor dimensions (all scopes combined)
```

OUTPUT_DIM is the total. The scope breakdown per layer (Section 5.3) tells you
how many dims are internal, external, and hybrid.

### 5.2 Scientific Constants (static)

```python
ALPHA = 0.90          # NPS weight — Bidelman & Krishnan 2009
FFR_BEHAVIOR_CORR = 0.81  # r=0.81, p<0.01, N=10
```

Calibration coefficients. Every constant cites its source paper and effect size.

### 5.3 Output Structure (static)

```python
LAYERS = (
    LayerSpec("E", "Extraction",    0, 4,  ("f01_nps", "f02_harmonicity", ...), scope="internal"),
    LayerSpec("M", "Mechanism",     4, 6,  ("nps_t", "harm_interval"),          scope="internal"),
    LayerSpec("P", "Cognitive",      6, 9,  ("consonance_signal", ...),          scope="external"),
    LayerSpec("F", "Forecast",      9, 12, ("consonance_pred", ...),            scope="hybrid"),
)
```

E/M/P/F output layers define the tensor schema. Every dimension has a semantic name
and a **scope** label:

| Scope | Meaning | Routed to |
|-------|---------|-----------|
| `internal` | Intermediate processing signal | Downstream nuclei only |
| `external` | Semantic meaning for final output | Coordinator only (→ L³, HYBRID) |
| `hybrid` | Serves both purposes | Downstream nuclei + coordinator |

The tensor itself is NOT split — `compute()` still returns a single `(B, T, OUTPUT_DIM)`.
Scope is **metadata** that tells the orchestrator what each dimension is for. The
orchestrator uses scope labels for routing decisions:
- Downstream nuclei receive: `internal` + `hybrid` dims
- Final output assembly uses: `external` + `hybrid` dims
- RAM/NeuroLink can reference ANY dim (scope does not restrict them)

**Common pattern** (not a rule — each nucleus declares its own):
- E layer → `internal` (raw feature extraction, intermediate signal)
- M layer → `internal` (mechanism computations, processing artifacts)
- P layer → `external` (cognitive constructs, semantic meaning)
- F layer → `hybrid` (predictions feed downstream + carry external meaning)

### 5.4 Temporal Demand (static)

```python
@property
def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
    return (
        H3DemandSpec(0, "roughness_sethares", 0, "25ms", 0, "value", 2, "bidi",
                     "Instantaneous dissonance", "Plomp & Levelt 1965"),
        ...
    )
```

H³ temporal features this component needs. Defines the multi-scale temporal requests.

### 5.5 Region Links (static)

```python
@property
def region_links(self) -> Tuple[RegionLink, ...]:
    return (
        RegionLink("IC", output_dims=(0, 1, 2), weight=0.85,
                   citation="Coffey 2016"),
        RegionLink("A1_HG", output_dims=(3, 4, 5), weight=0.70,
                   citation="Patterson 2002"),
    )
```

Maps this nucleus's output dimensions to brain regions for the Region Activation
Map (RAM). MNI coordinates live in the global `REGION_REGISTRY`, not per-nucleus.
See Section 14 for full RAM specification.

### 5.5b Neuro Links (static, optional)

```python
@property
def neuro_links(self) -> Tuple[NeuroLink, ...]:
    return (
        NeuroLink("da",  output_dims=(0, 1, 2), effect="produce",
                  weight=0.85, citation="Salimpoor 2011"),
        NeuroLink("opi", output_dims=(5, 6),    effect="produce",
                  weight=0.70, citation="Pecina & Berridge 2005"),
    )
```

Maps this nucleus's output dimensions to neurochemical effects. Only ~10 nuclei
(concentrated in ARU, RPU, ASU) have non-empty neuro_links. Most nuclei return `()`.
See Section 12.7 for NeuroLink specification.

### 5.6 Evidence (static)

```python
@property
def metadata(self) -> ModelMetadata:
    return ModelMetadata(
        citations=(...),              # All papers with findings + effect sizes
        evidence_tier="alpha",        # Tier (alpha/beta/gamma)
        confidence_range=(0.90, 0.95),
        falsification_criteria=(...), # Testable predictions
        version="3.0.0",
    )
```

Scientific provenance: papers, confidence, falsifiability, version.

### 5.7 Connectivity (static)

```python
# What this component reads from OTHER units (cross-unit)
CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()

# What this component reads from SAME unit (intra-unit) — NEW
UPSTREAM_READS: Tuple[str, ...] = ("BCH",)  # Encoder reads its Relay
```

Declared dependencies. Determines execution order and data flow.

### 5.8 Computation (runtime)

```python
def compute(self, h3_features, r3_features, upstream_outputs=None,
            cross_unit_inputs=None) -> Tensor:
    # The actual neural computation
    # Every operation traces to a citation
    # Returns (B, T, OUTPUT_DIM) in [0, 1]
```

The transformation itself. Input signature varies by role:

| Role | Input signature |
|------|----------------|
| Relay | `compute(h3, r3)` |
| Encoder | `compute(h3, r3, relay_outputs)` |
| Associator | `compute(h3, r3, upstream_outputs)` |
| Integrator | `compute(h3, r3, upstream_outputs, cross_unit_inputs)` |
| Hub | `compute(h3, r3, upstream_outputs, cross_unit_inputs)` |

---

## 6. How Roles Map to the Execution Engine

### 6.1 Intra-Unit Execution Order

Within each unit, execution proceeds by depth:

```
DEPTH 0:  Run Relay           (1 component)
          ↓ output
DEPTH 1:  Run all Encoders    (2-8 components, parallel within depth)
          ↓ outputs
DEPTH 2:  Run all Associators (2-6 components, parallel within depth)
          ↓ outputs
DEPTH 3:  Run all Integrators (1-3 components, parallel within depth)
          ↓ outputs
DEPTH 4+: Run all Hubs        (0-2 components, parallel within depth)
```

Each depth receives the outputs of ALL lower depths as `upstream_outputs`.

**Scope-aware routing**: When the orchestrator passes `upstream_outputs` to a
nucleus, it exposes only the `internal` + `hybrid` dims of each upstream tensor
(masking `external` dims). External dims exist in the tensor but are not routed
to downstream consumers — they are reserved for the final output assembly.

### 6.2 Cross-Unit Execution Order

```
Phase 1: All 7 independent unit Relays in parallel
Phase 2: Forward pathway routing (Relay → Relay)
Phase 3: Each unit runs Depth 1→2→3→4 in order
Phase 4: Cross-unit pathway routing (all 12 pathways)
Phase 5: Dependent units (ARU, RPU) run Depth 0→1→2→3→4
Phase 6: Assembly (scope-aware):
         - internal dims   → discarded (already consumed by downstream nuclei)
         - external dims   → concatenated into output tensor
         - hybrid dims     → concatenated into output tensor
         → (B, T, N_ext) where N_ext = sum of external + hybrid dims across 96 nuclei
```

---

## 7. Directory Structure

```
Musical_Intelligence/brain/units/
  spu/
    relays/
      bch.py              # SPU-R-BCH
    encoders/
      pscl.py             # SPU-E-PSCL
      stai.py             # SPU-E-STAI
    associators/
      pccr.py             # SPU-A-PCCR
      tscp.py             # SPU-A-TSCP
      sdnps.py            # SPU-A-SDNPS
    integrators/
      miaa.py             # SPU-I-MIAA
      esme.py             # SPU-I-ESME
      sded.py             # SPU-I-SDED
    unit.py               # SPUUnit — orchestrates R→E→A→I→H
    __init__.py
```

This replaces the current flat `models/` directory:
```
# CURRENT (flat — no hierarchy visible):
spu/models/bch.py
spu/models/pscl.py
spu/models/pccr.py
...

# NEW (hierarchy in directory structure):
spu/relays/bch.py
spu/encoders/pscl.py
spu/associators/pccr.py
...
```

---

## 8. Class Hierarchy

```python
# contracts/bases/nucleus.py (replaces base_model.py)

class Nucleus(ABC):
    """Base class for all 96 C³ brain components."""
    NAME: str
    FULL_NAME: str
    UNIT: str
    ROLE: str                        # "relay"|"encoder"|"associator"|"integrator"|"hub"
    PROCESSING_DEPTH: int            # 0-5
    OUTPUT_DIM: int                  # Total dims (all scopes)
    LAYERS: Tuple[LayerSpec, ...]    # Each layer has scope: internal|external|hybrid
    UPSTREAM_READS: Tuple[str, ...]  # Same-unit dependencies
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...]

    # Derived from LAYERS — scope-based dim indices
    @property
    def internal_dims(self) -> Tuple[int, ...]: ...   # dims routed to downstream only
    @property
    def external_dims(self) -> Tuple[int, ...]: ...   # dims routed to final output only
    @property
    def hybrid_dims(self) -> Tuple[int, ...]: ...     # dims routed to both
    @property
    def routable_dims(self) -> Tuple[int, ...]: ...   # internal + hybrid (what downstream sees)
    @property
    def exportable_dims(self) -> Tuple[int, ...]: ... # external + hybrid (what goes to output)

# contracts/bases/relay.py
class Relay(Nucleus):
    """Depth 0 — foundation transformation from raw R³/H³."""
    ROLE = "relay"
    PROCESSING_DEPTH = 0
    UPSTREAM_READS = ()              # Relays read nothing from same unit

    @abstractmethod
    def compute(self, h3_features, r3_features) -> Tensor: ...

# contracts/bases/encoder.py
class Encoder(Nucleus):
    """Depth 1 — feature extraction from Relay output."""
    ROLE = "encoder"
    PROCESSING_DEPTH = 1

    @abstractmethod
    def compute(self, h3_features, r3_features,
                relay_outputs: Dict[str, Tensor]) -> Tensor: ...

# contracts/bases/associator.py
class Associator(Nucleus):
    """Depth 2 — combines Relay + Encoder outputs."""
    ROLE = "associator"
    PROCESSING_DEPTH = 2

    @abstractmethod
    def compute(self, h3_features, r3_features,
                upstream_outputs: Dict[str, Tensor]) -> Tensor: ...

# contracts/bases/integrator.py
class Integrator(Nucleus):
    """Depth 3 — cross-stream integration within unit."""
    ROLE = "integrator"
    PROCESSING_DEPTH = 3

    @abstractmethod
    def compute(self, h3_features, r3_features,
                upstream_outputs: Dict[str, Tensor],
                cross_unit_inputs: Optional[Dict[str, Tensor]] = None) -> Tensor: ...

# contracts/bases/hub.py
class Hub(Nucleus):
    """Depth 4-5 — highest-level convergence."""
    ROLE = "hub"
    PROCESSING_DEPTH = 4  # or 5

    @abstractmethod
    def compute(self, h3_features, r3_features,
                upstream_outputs: Dict[str, Tensor],
                cross_unit_inputs: Optional[Dict[str, Tensor]] = None) -> Tensor: ...
```

---

## 9. Complete Mapping: All 96 Components

### SPU — Spectral Processing Unit (9 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Brainstem Consonance Hierarchy | BCH | SPU-α1-BCH | 12D |
| Encoder | E | Pitch Salience Cortical Localization | PSCL | SPU-α2-PSCL | 12D |
| Encoder | E | Spectral Timbre Aesthetic Integration | STAI | SPU-β1-STAI | 12D |
| Associator | A | Pitch Chroma Cortical Representation | PCCR | SPU-α3-PCCR | 11D |
| Associator | A | Timbre-Specific Cortical Plasticity | TSCP | SPU-β2-TSCP | 10D |
| Associator | A | Stimulus-Dependent NPS | SDNPS | SPU-γ1-SDNPS | 10D |
| Integrator | I | Musical Imagery Auditory Activation | MIAA | SPU-β3-MIAA | 11D |
| Integrator | I | Expertise-Specific MMN Enhancement | ESME | SPU-γ2-ESME | 11D |
| Integrator | I | Sensory Dissonance Early Detection | SDED | SPU-γ3-SDED | 10D |

### STU — Sensorimotor Temporal Unit (14 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Hierarchical Musical Context Encoding | HMCE | STU-α1-HMCE | 13D |
| Encoder | E | Auditory-Motor Stream Coupling | AMSC | STU-α2-AMSC | 12D |
| Encoder | E | Melody Decoding Neural Substrate | MDNS | STU-α3-MDNS | 9D |
| Encoder | E | Auditory Multi-Stream Segregation | AMSS | STU-β1-AMSS | 12D |
| Encoder | E | Envelope Tracking Attention Modulation | ETAM | STU-β4-ETAM | 10D |
| Encoder | E | Oscillatory Motor Synchronization | OMS | STU-β6-OMS | 9D |
| Encoder | E | Neural Entrainment WM Dual-Route | NEWMD | STU-γ2-NEWMD | 10D |
| Encoder | E | Musical Training Neural Efficiency | MTNE | STU-γ3-MTNE | 10D |
| Encoder | E | Musical Prodigy Flow State | MPFS | STU-γ5-MPFS | 10D |
| Associator | A | Timbre Perception-Imagery Overlap | TPIO | STU-β2-TPIO | 11D |
| Associator | A | Expertise-Dependent Tempo Accuracy | EDTA | STU-β3-EDTA | 10D |
| Associator | A | High-Gamma Sensorimotor Integration | HGSIC | STU-β5-HGSIC | 10D |
| Associator | A | Tempo Reproduction Motor Model | TMRM | STU-γ1-TMRM | 10D |
| Associator | A | Piano Training Grey Matter Plasticity | PTGMP | STU-γ4-PTGMP | 10D |

### IMU — Integrative Memory Unit (15 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Music-Evoked Autobiographical Memory Net. | MEAMN | IMU-α1-MEAMN | 12D |
| Encoder | E | Pythagorean Neural Hierarchy | PNH | IMU-α2-PNH | 11D |
| Encoder | E | Musical Mnemonic Preservation | MMP | IMU-α3-MMP | 10D |
| Encoder | E | Predictive Memory Integration Model | PMIM | IMU-β2-PMIM | 11D |
| Encoder | E | Hippocampal-Cortical Memory Circuit | HCMC | IMU-β4-HCMC | 10D |
| Encoder | E | Context-Dependent Emotional Memory | CDEM | IMU-γ3-CDEM | 9D |
| Encoder | E | Developmental Memory Music Scaffold | DMMS | IMU-γ1-DMMS | 9D |
| Associator | A | Rhythmic Auditory Stim. Neuroplasticity | RASN | IMU-β1-RASN | 12D |
| Associator | A | Oscillatory Intelligence Integration | OII | IMU-β3-OII | 11D |
| Associator | A | Musical Syntax Processing (Broca's) | MSPBA | IMU-β6-MSPBA | 10D |
| Associator | A | Tonotopy-Pitch Repr. Dissociation | TPRD | IMU-β8-TPRD | 10D |
| Associator | A | Cross-Species Song Learning | CSSL | IMU-γ2-CSSL | 9D |
| Integrator | I | RAS-Intelligent Rehab. Integration | RIRI | IMU-β5-RIRI | 11D |
| Integrator | I | VR Immersive Analgesia Protocol | VRIAP | IMU-β7-VRIAP | 10D |
| Integrator | I | Cross-Modal Action-Perception Code | CMAPCC | IMU-β9-CMAPCC | 10D |

### ASU — Attention & Salience Unit (9 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Selective Neural Entrainment Model | SNEM | ASU-α1-SNEM | 12D |
| Encoder | E | Inharmonic Attention Capture Model | IACM | ASU-α2-IACM | 12D |
| Encoder | E | Consonance Salience Gradient | CSG | ASU-α3-CSG | 10D |
| Encoder | E | Beat Alignment Regularization Model | BARM | ASU-β1-BARM | 11D |
| Encoder | E | Spectral-Temporal Attention Network | STANM | ASU-β2-STANM | 11D |
| Associator | A | Aesthetic Appreciation Cognitive Model | AACM | ASU-β3-AACM | 11D |
| Associator | A | Precision-Weighted Surprise Model | PWSM | ASU-γ1-PWSM | 10D |
| Associator | A | Domain-General Timing Precision | DGTP | ASU-γ2-DGTP | 10D |
| Associator | A | Spectral Dynamic Lateralization | SDL | ASU-γ3-SDL | 10D |

### NDU — Neurodevelopmental Unit (9 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Melodic Processing Gradient | MPG | NDU-α1-MPG | 10D |
| Encoder | E | Supramodal Deviance Detection | SDD | NDU-α2-SDD | 11D |
| Encoder | E | Expertise-Dependent Network Reorg. | EDNR | NDU-α3-EDNR | 10D |
| Encoder | E | Developmental Singing Plasticity | DSP | NDU-β1-DSP | 11D |
| Associator | A | Context-Dependent Mismatch Response | CDMR | NDU-β2-CDMR | 11D |
| Associator | A | Statistical Learning Expertise Effect | SLEE | NDU-β3-SLEE | 10D |
| Associator | A | Sex-Dependent Dev. Plasticity | SDDP | NDU-γ1-SDDP | 10D |
| Associator | A | Over-Normalization Intervention | ONI | NDU-γ2-ONI | 10D |
| Integrator | I | Efficiency-Connectivity Trade-off | ECT | NDU-γ3-ECT | 10D |

### MPU — Motor Processing Unit (10 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Period Entrainment Optimization Model | PEOM | MPU-α1-PEOM | 11D |
| Encoder | E | Motor Sensorimotor Reorganization | MSR | MPU-α2-MSR | 10D |
| Encoder | E | Gait-Synchronized Stimulation Model | GSSM | MPU-α3-GSSM | 11D |
| Encoder | E | Auditory-Motor Sim. & Action Pred. | ASAP | MPU-β1-ASAP | 11D |
| Associator | A | Sensorimotor Planning Motor Circuit | SPMC | MPU-β4-SPMC | 10D |
| Associator | A | Dance-DJ Social Motor Integration | DDSMI | MPU-β2-DDSMI | 11D |
| Associator | A | Neural Synchrony Catchiness Prediction | NSCP | MPU-γ1-NSCP | 10D |
| Associator | A | Cerebellar Timing Brain-Body | CTBB | MPU-γ2-CTBB | 10D |
| Integrator | I | VR Music-Synchronized Motor Enh. | VRMSME | MPU-β3-VRMSME | 11D |
| Integrator | I | Singing-Training Connectivity | STC | MPU-γ3-STC | 10D |

### PCU — Predictive Coding Unit (10 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Hierarchical Temporal Prediction | HTP | PCU-α1-HTP | 12D |
| Encoder | E | Spatiotemporal Prediction Hierarchy | SPH | PCU-α2-SPH | 11D |
| Encoder | E | Information Content Emotion Model | ICEM | PCU-α3-ICEM | 10D |
| Associator | A | Precision-Weighted Uncertainty Proc. | PWUP | PCU-β1-PWUP | 12D |
| Associator | A | Cross-Modal Harmonic Pred. Integration | CHPI | PCU-β4-CHPI | 10D |
| Integrator | I | Working Memory Entrainment Dissociation | WMED | PCU-β2-WMED | 10D |
| Integrator | I | Uncertainty-Driven Pleasure | UDP | PCU-β3-UDP | 10D |
| Integrator | I | Isochronous Gamma Frequency Enh. | IGFE | PCU-γ1-IGFE | 10D |
| Hub | H | Musical Aesthetic Appreciation | MAA | PCU-γ2-MAA | 10D |
| Hub | H | Predictive Silencing Hypothesis | PSH | PCU-γ3-PSH | 10D |

### ARU — Affective Response Unit (10 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Striatal Reward Pathway | SRP | ARU-α1-SRP | 19D |
| Encoder | E | Autonomic-Affective Coupling | AAC | ARU-α2-AAC | 14D |
| Encoder | E | Valence-Mode Mapping | VMM | ARU-α3-VMM | 12D |
| Associator | A | Prediction-Uncertainty-Pleasure | PUPF | ARU-β1-PUPF | 11D |
| Associator | A | Closed-Loop Affective Modulation | CLAM | ARU-β2-CLAM | 10D |
| Associator | A | Musical Anhedonia Deficit | MAD | ARU-β3-MAD | 10D |
| Associator | A | Nostalgia-Enhanced Musical Affect | NEMAC | ARU-β4-NEMAC | 10D |
| Integrator | I | Developmental Affective Plasticity | DAP | ARU-γ1-DAP | 10D |
| Integrator | I | Cross-Modal Affective Transfer | CMAT | ARU-γ2-CMAT | 10D |
| Hub | H | Therapeutic Affective Resonance | TAR | ARU-γ3-TAR | 10D |

### RPU — Reward Processing Unit (10 components)

| Role | Code | Name | Acronym | Old Name | Dim |
|------|------|------|---------|----------|-----|
| Relay | R | Dopamine Anticipation-Experience Dissoc. | DAED | RPU-α1-DAED | 8D |
| Encoder | E | Mu-Opioid Receptor Music Reward | MORMR | RPU-α2-MORMR | 10D |
| Encoder | E | Reward Prediction Error Model | RPEM | RPU-α3-RPEM | 11D |
| Encoder | E | Inverted-U Complexity Preference | IUCP | RPU-β1-IUCP | 11D |
| Encoder | E | Musical Chills Cortical Network | MCCN | RPU-β2-MCCN | 11D |
| Associator | A | Music-Evoked Autobiog. Memory Reward | MEAMR | RPU-β3-MEAMR | 10D |
| Associator | A | Social Synchrony Reward Integration | SSRI | RPU-β4-SSRI | 10D |
| Associator | A | Liking-Driven Auditory Cortex | LDAC | RPU-γ1-LDAC | 10D |
| Associator | A | Individual Opioid Trait Music Sens. | IOTMS | RPU-γ2-IOTMS | 10D |
| Integrator | I | Saddle Surface Preference Structure | SSPS | RPU-γ3-SSPS | 10D |

---

## 10. Role Distribution Summary

| Role | R | E | A | I | H | Total |
|------|---|---|---|---|---|-------|
| **SPU** | 1 | 2 | 3 | 3 | 0 | **9** |
| **STU** | 1 | 8 | 5 | 0 | 0 | **14** |
| **IMU** | 1 | 6 | 5 | 3 | 0 | **15** |
| **ASU** | 1 | 4 | 4 | 0 | 0 | **9** |
| **NDU** | 1 | 3 | 4 | 1 | 0 | **9** |
| **MPU** | 1 | 3 | 4 | 2 | 0 | **10** |
| **PCU** | 1 | 2 | 2 | 3 | 2 | **10** |
| **ARU** | 1 | 2 | 4 | 2 | 1 | **10** |
| **RPU** | 1 | 4 | 4 | 1 | 0 | **10** |
| **Total** | **9** | **34** | **35** | **15** | **3** | **96** |

---

## 11. Brain Regions as Anatomical Evidence (Not a Separate Space)

### 11.1 Why Not Use Anatomical Names Instead of R-E-A-I-H?

If brain regions and the hierarchy are the same gradient, why not name roles
anatomically ("Brainstem", "Primary Cortical", etc.) instead of abstractly
("Relay", "Encoder", etc.)?

**Because the anatomy varies per unit while the computational role is invariant:**

```
              UNIT      RELAY ANATOMY           ROLE (same everywhere)
              ────      ──────────────          ──────────────────────
              SPU       Brainstem (AN,IC,CN)    Raw R³/H³ → foundation
              STU       Cortical (A1,STG)       Raw R³/H³ → foundation
              IMU       Hippocampus             Raw R³/H³ → foundation
              MPU       Motor cortex (SMA,PMC)  Raw R³/H³ → foundation
              ARU       Subcortical (VTA,NAcc)  Raw R³/H³ → foundation
                        ↑                       ↑
                        Different per unit       Same everywhere
```

If we called Depth 0 "Brainstem" — STU, IMU, MPU, ARU Relays are NOT in the
brainstem. If we called it "Subcortical" — SPU and STU Relays involve cortical
regions (A1/HG). No single anatomical term works across all 9 units.

**R-E-A-I-H captures what is INVARIANT**: the computational function.
**Brain regions capture what is VARIANT**: where each unit does that function.

### 11.2 Each Unit Has Its Own Anatomical Gradient

Every unit ascends from peripheral/specialized → central/convergent, but through
DIFFERENT brain regions:

```
DEPTH    SPU (spectral)    STU (temporal)    ARU (affect)      MPU (motor)
─────    ──────────────    ──────────────    ────────────      ───────────
  0  R   AN, IC, CN        A1/HG, STG        VTA, NAcc         SMA, PMC
  1  E   STG, A1/HG        SMA, PMC          amygdala          SMA, PMC
  2  A   STG, STS          SMA, PMC          insula, ACC       SMA, putamen
  3  I   dlPFC             AG, dlPFC         vmPFC, OFC        PMC
 4-5 H   —                 —                 vmPFC, OFC        —
```

The DIRECTION is the same (peripheral → abstract → evaluative).
The REGIONS are different.

### 11.3 What Brain Regions ARE in This System

`brain_regions` is a property of each nucleus — but it is **anatomical evidence**,
not a separate computational dimension:

```python
@property
def brain_regions(self) -> Tuple[BrainRegion, ...]:
    """Anatomical evidence for this nucleus's processing depth.

    NOT a separate computational dimension.
    Used for:
    - Visualization (MNI coordinates for 3D brain rendering)
    - Validation (region type should match role depth)
    - Scientific grounding (citations linking region to function)
    """
```

### 11.4 Validation Rule

The regions listed for a nucleus should be CONSISTENT with its depth:
- A Relay listing vmPFC or OFC → suspicious (those are value regions = Hub depth)
- A Hub listing only brainstem regions → suspicious (those are Relay depth)
- Mismatch = either the depth assignment or the region list needs review

---

## 12. Neurochemicals: Semi-Orthogonal Modulatory Overlay

### 12.1 Why Neurochemicals Are Different From Brain Regions

Brain regions and processing depth are ONE gradient (Section 11). Neurochemicals
are genuinely DIFFERENT — but not as separate as initially assumed.

**The key distinction** is transmission mechanism:

| | Processing Hierarchy | Neurochemicals |
|---|---|---|
| **Mechanism** | Wired (point-to-point synapses) | Volume (broadcast diffusion) |
| **Specificity** | Precise: A1 → STG → STS | Broad: VTA → entire prefrontal cortex |
| **Speed** | ms (spike propagation) | Seconds to minutes (diffusion) |
| **Metaphor** | Roads + traffic | Street lighting (adjustable) |
| **Affects** | Which signals go where | HOW MUCH those signals matter |

**Volume transmission** (Agnati et al. 2010): Neurochemicals are released into
extracellular space and diffuse to affect ALL nearby neurons with matching receptors.
This is fundamentally different from point-to-point wired transmission of the
tensor pathway. A single VTA dopamine burst modulates millions of target neurons.

### 12.2 Semi-Orthogonal, Not Fully Independent

Neurochemicals are SEMI-orthogonal to the hierarchy, not fully parallel:

**Evidence of correlation** (not independence):
- Receptor densities correlate with hierarchy level (D1 receptors dense in PFC, sparse in brainstem)
- Neurochemical SOURCE nuclei are at the bottom of the hierarchy (VTA, LC, raphe = brainstem/subcortical)
- Higher-order regions have richer receptor diversity (more modulation channels)

**Evidence of partial independence**:
- A single neurochemical system spans ALL hierarchy levels simultaneously
- The SAME DA signal modulates both A1 (Relay level) and vmPFC (Hub level)
- Neurochemical state can change WITHOUT the hierarchy changing, and vice versa

**Model**: Think of it as a **gain knob on each floor of a building**. The building
(hierarchy) determines what rooms exist and how they connect. The lighting system
(neurochemicals) adjusts brightness on every floor simultaneously, and different
floors respond differently to the same brightness setting.

### 12.3 Neurochemical Writers (Not Only Relays)

Initial production comes from Relay-level nuclei (consistent with anatomy — source
nuclei are brainstem/subcortical). But downstream nuclei also modulate neurochemical
levels via feedback loops, local metabolism, and cross-modulation:

| Nucleus | Role | Writes | Effect | Citation |
|---------|------|--------|--------|----------|
| ARU-R-SRP | **Relay** | DA, OPI | **produce** — sets initial values | Salimpoor 2011, Pecina 2005 |
| RPU-R-DAED | **Relay** | DA | **produce** — anticipation/experience dissociation | Salimpoor 2011 |
| ASU-R-SNEM | **Relay** | NE | **produce** — arousal/salience baseline | Aston-Jones 2005 |
| ARU-E-AAC | **Encoder** | DA, 5-HT | **amplify/produce** — autonomic-affective feedback | Ferreri 2019, Nummenmaa 2025 |
| RPU-E-MORMR | **Encoder** | OPI | **amplify** — mu-opioid consummatory signal | Pecina & Berridge 2005 |
| NDU-*-* | **various** | NE | **amplify** — developmental arousal modulation | — |

**Key correction**: neuro_state is NOT set once by Relays and then frozen. It is a
**running accumulation** — each writer nucleus updates the state as processing
progresses through the depth hierarchy. Depth 2 nuclei see a different neuro_state
than Depth 1 nuclei, because Depth 1 writers have already modified it.

### 12.4 How Neurochemicals Modulate the Hierarchy

```
R-E-A-I-H HIERARCHY (wired, point-to-point)
═══════════════════════════════════════════════════
  R³/H³ ──► Relay ──► Encoder ──► Associator ──► Integrator ──► Hub
              │W        │W          │R             │R           │R
              ▼         ▼           │              │            │
         ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
         NEURO STATE (accumulates through depth)
         Depth 0: {da:0.75, ne:0.65, opi:0.40, 5ht:0.50}  ← Relays set
         Depth 1: {da:0.79, ne:0.65, opi:0.52, 5ht:0.55}  ← Encoders adjust
         Depth 2: {da:0.79, ne:0.65, opi:0.52, 5ht:0.55}  ← (no writers here)
         Depth 3+: continues...
         ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
         W = writes (has neuro_links)    R = reads only
```

neuro_state is a running accumulation, not a static broadcast. Each depth
receives the version updated by ALL previous writers. The orchestrator manages
this update loop — nuclei never mutate neuro_state directly.

### 12.5 Doya Metalearning Framework (Computational Interpretation)

Doya 2002 provides the cleanest computational interpretation of what each
neurochemical controls:

| Neurochemical | Computational Role | Controls | Analogy |
|---------------|-------------------|----------|---------|
| **DA** | Reward prediction error | Learning rate for reward-related signals | "How surprising was that?" |
| **5-HT** | Temporal discount rate | Patience vs impulsivity tradeoff | "How much do I care about later?" |
| **NE** | Exploration-exploitation | Signal-to-noise ratio, attentional breadth | "Should I focus or wander?" |
| **OPI** | Hedonic evaluation | Raw pleasure magnitude | "How good does this feel?" |

These four knobs adjust HOW the hierarchy processes, not WHAT it processes.

### 12.6 Neurochemical × Unit Matrix

| | DA | NE | Opioid | 5-HT |
|---|:---:|:---:|:---:|:---:|
| **SPU** | — | — | — | — |
| **STU** | — | read | — | — |
| **IMU** | — | read | — | — |
| **ASU** | — | **write** | — | — |
| **NDU** | — | write | — | — |
| **MPU** | — | — | — | — |
| **PCU** | read | read | read | read |
| **ARU** | **write** | read | **write** | write |
| **RPU** | **write** | — | read | read |

**Writers** = produce the signal (Relay-level operation)
**Readers** = consume the signal (all depths, via volume transmission)

### 12.7 NeuroLink: Declarative Neurochemical Mapping

Just as `RegionLink` maps output dims → brain regions (Section 14), `NeuroLink`
maps output dims → neurochemical effects:

```python
@dataclass(frozen=True)
class NeuroLink:
    neurochemical: str           # "da" | "ne" | "opi" | "5ht"
    output_dims: Tuple[int, ...]  # which output dims drive this effect
    effect: str                  # "produce" | "amplify" | "inhibit"
    weight: float                # effect magnitude [0, 1]
    citation: str                # scientific basis
```

**Effect types**:

| Effect | What it does | Formula | When to use |
|--------|-------------|---------|-------------|
| `produce` | Sets the value (source nuclei) | `neuro[nc] = mean(dims) * weight` | Relays that are the origin of a neurochemical |
| `amplify` | Increases current value | `neuro[nc] += mean(dims) * weight * 0.2` | Downstream nuclei that enhance via feedback |
| `inhibit` | Decreases current value | `neuro[nc] -= mean(dims) * weight * 0.2` | Nuclei that suppress (e.g., 5-HT2C → DA inhibition) |

The 0.2 scaling on amplify/inhibit ensures downstream effects are smaller deltas,
not full overrides. Source nuclei (`produce`) set the baseline; downstream nuclei
make adjustments.

### 12.8 Accumulating neuro_state Through the Hierarchy

neuro_state is **not static**. It updates as each writer nucleus computes:

```
neuro_state = {da: 0.5, ne: 0.5, opi: 0.5, 5ht: 0.5}    ← baseline

DEPTH 0 (Relays):
  SRP.compute()  → tensor + neuro_links: da=produce(0.78), opi=produce(0.40)
  DAED.compute() → tensor + neuro_links: da=produce(0.72)
  SNEM.compute() → tensor + neuro_links: ne=produce(0.65)
  ──► neuro_state = {da: 0.75, ne: 0.65, opi: 0.40, 5ht: 0.5}

DEPTH 1 (Encoders) — receive updated neuro_state:
  AAC.compute(neuro_state)  → tensor + neuro_links: da=amplify(+0.04), 5ht=produce(0.55)
  MORMR.compute(neuro_state) → tensor + neuro_links: opi=amplify(+0.12)
  ──► neuro_state = {da: 0.79, ne: 0.65, opi: 0.52, 5ht: 0.55}

DEPTH 2 (Associators) — see the Depth-1-updated state:
  ... nuclei at Depth 2 receive da=0.79, not da=0.75

DEPTH 3+ — continues accumulating
```

When multiple nuclei `produce` the same neurochemical (e.g., SRP and DAED both
produce DA), the orchestrator takes their **weighted average** for the initial set.
Subsequent `amplify`/`inhibit` effects accumulate additively.

### 12.9 Compute Signatures (Updated)

Every nucleus receives the **current** neuro_state. Writer nuclei additionally
declare `neuro_links`:

| Role | Compute signature |
|------|------------------|
| Relay | `compute(h3, r3) → Tensor` |
| Encoder | `compute(h3, r3, relay_outputs, neuro_state) → Tensor` |
| Associator | `compute(h3, r3, upstream_outputs, neuro_state) → Tensor` |
| Integrator | `compute(h3, r3, upstream_outputs, cross_unit, neuro_state) → Tensor` |
| Hub | `compute(h3, r3, upstream_outputs, cross_unit, neuro_state) → Tensor` |

**Note**: Relays do NOT receive neuro_state (they are at Depth 0, nothing has
been produced yet). They produce the initial neuro_state via their `neuro_links`.

The orchestrator handles the neuro_state update loop — nuclei do NOT directly
mutate neuro_state. Instead, the orchestrator:
1. Calls `nucleus.compute()` → gets tensor output
2. Checks `nucleus.neuro_links` — if non-empty, applies effects to neuro_state
3. Passes updated neuro_state to next depth

Most nuclei have `neuro_links = ()` (empty) — they only read, never write.
Only ~10 nuclei (concentrated in ARU, RPU, ASU) are writers.

### 12.10 Neurochemical × Unit Matrix (Updated)

| | DA | NE | Opioid | 5-HT |
|---|:---:|:---:|:---:|:---:|
| **SPU** | — | — | — | — |
| **STU** | — | read | — | — |
| **IMU** | — | read | — | — |
| **ASU** | — | **write** | — | — |
| **NDU** | — | write | — | — |
| **MPU** | — | — | — | — |
| **PCU** | read | read | read | read |
| **ARU** | **write** (R+E) | read | **write** (R) | **write** (E) |
| **RPU** | **write** (R) | — | **write** (E) | read |

**write (R)** = Relay produces, **write (E)** = Encoder amplifies/produces
**read** = consumes neuro_state, no neuro_links declared

### 12.8 The Four Neurochemicals as Runtime Signals

| Neurochemical | Abbrev | Value Range | Timescale | What it modulates |
|---------------|--------|-------------|-----------|------------------|
| **Dopamine** | DA | [0, 1] | Phasic: ms bursts, Tonic: seconds | Reward prediction error, wanting. Phasic ≥ 0.6, tonic < 0.6 |
| **Norepinephrine** | NE | [0, 1] | Phasic: ms, Tonic: seconds | Arousal, attentional gain, SNR. Inverted-U on PFC |
| **Opioid** | OPI | [0, 1] | Seconds | Hedonic liking, consummatory pleasure |
| **Serotonin** | 5HT | [0, 1] | Minutes (slow) | Mood valence, temporal discounting |

### 12.9 Neurochemical Interactions

The 4 neurochemicals interact — they are not independent channels:

```
        NE (arousal)
        │
        ▼ triggers
DA (wanting) ◄──── 5-HT gates via 5-HT2C (inhibits) / 5-HT1B (facilitates)
        │
        ▼ converges in NAcc
OPI (liking) ◄──── NE amplifies salience of hedonic moments
        │
        ▼ feeds back
5-HT (mood) ◄──── DA/OPI experience modulates background mood
```

| Interaction | Mechanism | Effect |
|-------------|-----------|--------|
| NE → DA | LC phasic burst triggers VTA DA phasic response | Unexpected event → arousal → enhanced reward signal |
| 5-HT ⊣ DA | 5-HT2C on VTA inhibits DA release | Negative mood gate on reward |
| 5-HT → DA | 5-HT1B on NAcc facilitates DA release | Positive mood gate on reward |
| NE → OPI | Arousal amplifies hedonic salience | Higher arousal = more intense pleasure |
| DA ⊥ OPI | DA = wanting (before), OPI = liking (at) | Temporally dissociated in caudate vs NAcc |

---

## 13. Complete System Ontology

Everything in C³, and how it relates:

```
C³ BRAIN
  │
  ├── 9 UNITS (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU)
  │     │
  │     ├── 96 NUCLEI across 5 ROLES:
  │     │     R (9) → E (34) → A (35) → I (15) → H (3)
  │     │     │
  │     │     ├── each has LAYERS (E/M/P/F output structure, each scoped: internal/external/hybrid)
  │     │     ├── each has BRAIN REGIONS (anatomical evidence, not separate space)
  │     │     ├── each has H³ DEMAND (temporal feature requests)
  │     │     ├── each has CITATIONS (scientific evidence)
  │     │     ├── each has CONSTANTS (calibrated coefficients)
  │     │     └── each has compute() (the transformation)
  │     │
  │     └── linked by INTRA-UNIT flow: R → E → A → I → H
  │
  ├── 12 PATHWAYS (cross-unit data routes)
  │     P1-P12, each typed: forward / backward / lateral
  │
  └── 4 NEUROCHEMICALS (semi-orthogonal modulatory overlay)
        DA, NE, OPI, 5HT — global state, volume transmission
        Produced by Relays, read by all depths as gain modulation
```

### What Was Removed

**CIRCUITS** (mesolimbic, perceptual, sensorimotor, mnemonic, salience, imagery):
Removed. Circuits were soft labels grouping units — no runtime function, no data
routing, no compute. The 12 PATHWAYS already define every cross-unit connection
explicitly. If a documentation-level grouping is ever needed, it can be a tag in
the unit metadata, not a first-class architectural concept.

**MECHANISMS** (BEP, ASA, PPC, TPC, TMH, MEM, AED, CPD, C0P):
Removed as a named architectural layer. In the old code, every nucleus declared
`MECHANISM_NAMES` and called generic mechanism classes. In the new architecture,
each nucleus's compute() contains 150-200 lines of specific science — the
"mechanism" logic is embedded in the compute, not delegated to a shared class.

If multiple nuclei need the same mathematical operation (e.g., Bayesian surprise),
that becomes a **shared utility function** in `utils/`, not a named "Mechanism"
with its own metadata. The distinction:

```python
# OLD: Mechanism as architectural layer
class BCH(BaseModel):
    MECHANISM_NAMES = ("PPC", "TPC")  # declared but opaque
    def compute(self, ...):
        ppc_out = self.mechanisms["PPC"].compute(x)  # black box
        tpc_out = self.mechanisms["TPC"].compute(x)  # black box

# NEW: Shared math as utility, science in compute()
from utils.bayesian import bayesian_surprise

class BCH(Relay):
    def compute(self, h3, r3):
        # Bidelman & Krishnan 2009: FFR amplitude predicts consonance
        nps = self._neural_periodicity_score(r3)
        # Bowling et al. 2018: harmonicity via spectral comparison
        harm = self._harmonicity_score(r3)
        # Bayesian surprise (shared utility, not a "mechanism")
        surprise = bayesian_surprise(predicted=..., observed=...)
```

### Conceptual Model: One Street, Adjustable Lighting

```
Brain regions are not a parallel highway.
Neurochemicals are not a parallel highway.

There is ONE highway: the R-E-A-I-H processing hierarchy.

Brain regions = the physical road surface (anatomy that DEFINES the hierarchy)
Neurochemicals = the lighting system (modulates how bright each section is)

The road and its surface are ONE thing, not two.
The lighting system is a genuinely different system — but it exists
to serve the road, not to run parallel to it.
```

### Data Flow Diagram

```
Audio
  │
  ▼
R³ (128D spectral features, per frame)
  │
  ▼
H³ (temporal demand, multi-scale 4-tuples)
  │
  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ C³ BRAIN                                                            │
│                                                                      │
│  R-E-A-I-H HIERARCHY (one gradient, wired transmission)             │
│  ═══════════════════════════════════════════════════════             │
│                                                                      │
│  neuro = {da:0.5, ne:0.5, opi:0.5, 5ht:0.5}  ← baseline           │
│                                                                      │
│  R³/H³ ──► 9 RELAYS (Depth 0) ────────────────────────►            │
│               │ outputs + neuro writers update neuro                 │
│               ▼                                                      │
│             34 ENCODERS (Depth 1) ──────────────────────►           │
│               │ outputs + neuro writers update neuro                 │
│               ▼                                                      │
│             35 ASSOCIATORS (Depth 2) ───────────────────►           │
│               │ outputs (read neuro)                                 │
│               ▼                                                      │
│    ◄──── 12 PATHWAYS (cross-unit routing) ─────────────►           │
│               │                                                      │
│               ▼                                                      │
│             15 INTEGRATORS (Depth 3) ──────────────────►            │
│               │ outputs (read neuro)                                 │
│               ▼                                                      │
│             3 HUBS (Depth 4-5) ─────────────────────────►           │
│                                                                      │
│  Assembly (scope-aware):                                             │
│    Tensor:  concat external+hybrid dims ──► (B, T, N_ext)           │
│    RAM:     aggregate region links      ──► (B, T, 26)              │
│    Neuro:   final neuro_state           ──► (B, T, 4)               │
│                                                                      │
│    Ψ³ Interpreter (inside C³):                                       │
│    tensor + ram + neuro ──► Psi (B, T, N_psi)                       │
│                                                                      │
│    Note: internal dims consumed by downstream nuclei only.           │
└─────────────────────────────────────────────────────────────────────┘
  │
  ├──► (B, T, N_ext)   Tensor  ──┐
  ├──► (B, T, 26)      RAM     ──┤──► L³ reads ALL of these + R³ + H³
  ├──► (B, T, 4)       Neuro   ──┤    → translates into Language
  ├──► (B, T, N_psi)   Psi     ──┘
  │
  ▼
L³ (Language — NOT Ψ³. L³ reads R³ + H³ + C³ and expresses in structured form)
```

---

## 14. Region Activation Map (RAM)

### 14.1 Purpose

The Region Activation Map produces a `(B, T, 26)` tensor — one activation value
per brain region per time frame. This is the **testable output** of C³:

| Validation Target | What RAM Enables |
|-------------------|-----------------|
| fMRI comparison | Compare RAM pattern to published contrasts (e.g., Salimpoor 2011, Grahn 2009) |
| Temporal dynamics | Track region activation over time — does NAcc peak at the right moment? |
| Lesion simulation | Zero out a region → does the model behavior change as predicted? |
| Cross-study consistency | Same music → same RAM pattern across runs |

Without RAM, the 1006D tensor is a black box. RAM makes C³ scientifically auditable.

### 14.2 How It Works

Each nucleus declares **RegionLinks** — which of its output dimensions contribute
to which brain region, with what weight:

```python
@property
def region_links(self) -> Tuple[RegionLink, ...]:
    return (
        RegionLink(
            region="IC",              # one of 26 canonical region abbreviations
            output_dims=(0, 1, 2),    # indices into this nucleus's (B, T, dim) output
            weight=0.85,              # contribution strength [0, 1]
            citation="Coffey 2016"    # why this mapping
        ),
        RegionLink(
            region="A1_HG",
            output_dims=(3, 4, 5),
            weight=0.70,
            citation="Patterson 2002"
        ),
    )
```

The **Region Aggregator** (part of the orchestrator) then:

```
For each of 26 regions:
    1. Find all nuclei that declare a RegionLink to this region
    2. For each nucleus:
       - Extract the specified output_dims from its (B, T, dim) tensor
       - Take mean across those dims → (B, T, 1) contribution
       - Multiply by weight
    3. Weighted average across all contributions → (B, T, 1)

Stack all 26 → (B, T, 26) = RAM
```

### 14.3 RegionLink Dataclass

```python
@dataclass(frozen=True)
class RegionLink:
    region: str                  # canonical abbreviation (one of 26)
    output_dims: Tuple[int, ...]  # which dims of this nucleus's output
    weight: float                # contribution strength [0, 1]
    citation: str                # scientific basis for this mapping
```

### 14.4 The 26 Canonical Regions

Every `RegionLink.region` must be one of these:

| # | Abbreviation | Full Name | Type |
|---|-------------|-----------|------|
| 0 | AN | Auditory Nerve | brainstem |
| 1 | CN | Cochlear Nucleus | brainstem |
| 2 | SOC | Superior Olivary Complex | brainstem |
| 3 | IC | Inferior Colliculus | brainstem |
| 4 | PAG | Periaqueductal Gray | brainstem |
| 5 | MGB | Medial Geniculate Body | subcortical |
| 6 | VTA | Ventral Tegmental Area | subcortical |
| 7 | NAcc | Nucleus Accumbens | subcortical |
| 8 | caudate | Caudate Nucleus | subcortical |
| 9 | amygdala | Amygdala | subcortical |
| 10 | hippocampus | Hippocampus | subcortical |
| 11 | putamen | Putamen | subcortical |
| 12 | hypothalamus | Hypothalamus | subcortical |
| 13 | insula | Insula | subcortical |
| 14 | A1_HG | Primary Auditory Cortex | cortical |
| 15 | STG | Superior Temporal Gyrus | cortical |
| 16 | STS | Superior Temporal Sulcus | cortical |
| 17 | IFG | Inferior Frontal Gyrus | cortical |
| 18 | dlPFC | Dorsolateral Prefrontal | cortical |
| 19 | vmPFC | Ventromedial Prefrontal | cortical |
| 20 | OFC | Orbitofrontal Cortex | cortical |
| 21 | ACC | Anterior Cingulate | cortical |
| 22 | SMA | Supplementary Motor Area | cortical |
| 23 | PMC | Premotor Cortex | cortical |
| 24 | AG | Angular Gyrus | cortical |
| 25 | TP | Temporal Pole | cortical |

### 14.5 Validation Examples

Known empirical results that RAM must reproduce:

| Stimulus | Expected High Regions | Expected Low Regions | Source |
|----------|----------------------|---------------------|--------|
| Chill-inducing music | VTA, NAcc, caudate | — | Salimpoor 2011 |
| Regular rhythm (vs irregular) | putamen, SMA | — | Grahn & Rowe 2009 |
| Dissonant chords | amygdala | NAcc | Koelsch 2014 |
| Familiar song (vs unfamiliar) | hippocampus, vmPFC | — | Janata 2009 |
| Harmonic violation (ERAN) | IFG, STG | — | Koelsch 2011 |
| Musical pleasure peak | NAcc (at peak), caudate (before peak) | — | Salimpoor 2011 |
| Passive listening (any music) | A1_HG, STG, SMA | — | Zatorre 2002 |

### 14.6 brain_regions → region_links Migration

The old `brain_regions` property (metadata only) is replaced by `region_links`
(metadata + activation mapping):

```python
# OLD: metadata only, no activation output
@property
def brain_regions(self) -> Tuple[BrainRegion, ...]:
    return (
        BrainRegion("Inferior Colliculus", "IC", "bilateral",
                     (0,-34,-8), 12, "FFR encoding"),
    )

# NEW: declares activation contribution
@property
def region_links(self) -> Tuple[RegionLink, ...]:
    return (
        RegionLink("IC", output_dims=(0, 1, 2), weight=0.85,
                   citation="Coffey 2016"),
    )
```

MNI coordinates move to a **global region registry** (since they're properties
of the 26 regions, not of individual nuclei):

```python
# brain/regions.py — single source of truth for all 26 regions
REGION_REGISTRY = {
    "IC": RegionInfo("Inferior Colliculus", "bilateral", (0,-34,-8)),
    "A1_HG": RegionInfo("Primary Auditory Cortex", "bilateral", (48,-18,8)),
    ...
}
```

---

## 15. Complete C³ Output

C³ produces **FOUR** outputs, not one:

| Output | Shape | Purpose |
|--------|-------|---------|
| **Tensor** | `(B, T, N_ext)` | External+hybrid dims — cognitive processing output |
| **RAM** | `(B, T, 26)` | Region Activation Map — neuroanatomical validation |
| **Neuro** | `(B, T, 4)` | Neurochemical state per frame — modulatory validation |
| **Psi** | `(B, T, N_psi)` | Cognitive interpretation — experiential readout |

`N_ext` = sum of `external` + `hybrid` dims across all 96 nuclei. This is less
than the total 1006 because `internal` dims are consumed by downstream nuclei
and excluded from the final output.

The neurochemical state is a `(B, T, 4)` tensor. Channel order: `[da, ne, opi, 5ht]`.

Psi is derived from the other three (tensor + ram + neuro) by the Ψ³ interpreter
(Section 16). It is computed INSIDE C³ — the brain's own cognitive readout.

```python
@dataclass
class BrainOutput:
    tensor: Tensor      # (B, T, N_ext)  — external+hybrid dims (cognitive output)
    ram: Tensor         # (B, T, 26)     — region activation map
    neuro: Tensor       # (B, T, 4)      — neurochemical state [da, ne, opi, 5ht]
    psi: PsiState       # (B, T, N_psi)  — cognitive interpretation
```

### 15.1 Neuro Channel Index

| Index | Neurochemical | Role (Doya 2002) |
|-------|--------------|------------------|
| 0 | DA (dopamine) | Reward prediction error |
| 1 | NE (norepinephrine) | Exploration–exploitation balance |
| 2 | OPI (endorphins) | Hedonic evaluation |
| 3 | 5HT (serotonin) | Temporal discount rate |

### 15.2 Neuro Lifecycle Per Frame

```
neuro[:, t, :] = 0.5  (baseline)
    ↓  Depth 0 (Relays)   — NeuroLinks with effect="produce" SET values
    ↓  Depth 1 (Encoders)  — NeuroLinks with any effect UPDATE values
    ↓  Depth 2 (Associators) — accumulate further
    ↓  Depth 3 (Integrators) — accumulate further
    ↓  Depth 4-5 (Hubs)   — final accumulation
neuro[:, t, :] = final state  (clamped to [0, 1])
```

Each nucleus's NeuroLinks are applied after its compute() runs, using
the nucleus's output tensor to derive the effect magnitude (Section 12.7).

---

## 16. Ψ³ — Cognitive Interpretation (Inside C³)

### 16.1 Still the Brain

Ψ³ is NOT after C³ — it is **inside** C³. The brain doesn't just compute; it
also generates cognitive experience. Ψ³ is the brain's own interpretive readout
of its computational state. It is the fourth output of C³, alongside tensor,
RAM, and neuro.

```
┌─────────────────────────── C³ BRAIN ───────────────────────────┐
│                                                                 │
│  R³/H³ → R → E → A → I → H                                    │
│                          │                                      │
│                          ▼                                      │
│              ┌─── Assembly ───┐                                 │
│              │ tensor (N_ext) │                                 │
│              │ ram    (26)    │──► Ψ³ Interpreter ──► psi (N_psi)│
│              │ neuro  (4)    │                                  │
│              └────────────────┘                                 │
│                                                                 │
│  OUTPUT: tensor + ram + neuro + psi   (all FOUR are C³ outputs) │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
L³ reads R³ + H³ + C³(all four) + ... → "Language" (separate space, NOT Ψ³)
```

### 16.2 The Interpretive Layers

| Layer | Domain | Language | Example | Where |
|-------|--------|----------|---------|-------|
| R³ | Physics | Spectral features | "roughness = 0.73" | Ear |
| H³ | Temporal | Multi-scale dynamics | "4-bar periodicity at 500ms" | Ear |
| C³.tensor | Neuroscience | Neural computation | "consonance hierarchy = 0.85" | Brain |
| C³.ram | Neuroanatomy | Region activation | "NAcc = 0.85" | Brain |
| C³.neuro | Neurochemistry | Modulatory state | "DA = 0.78" | Brain |
| **C³.psi** | **Cognitive Science** | **Human experience** | **"intense pleasure, chills"** | **Brain** |
| L³ | Semantics | **Language** | **Musical meaning in structured form** | **Separate** |

C³.psi is what the brain EXPERIENCES cognitively. L³ is how all of it gets expressed in Language.
They are fundamentally different: Ψ³ interprets the brain's own state; L³
translates the ENTIRE pipeline (R³ + H³ + C³) into a semantic/linguistic form.

### 16.3 Inputs — Internal C³ Outputs

Ψ³ reads the other three C³ outputs before they leave the brain:

| Input | What Ψ³ extracts from it |
|-------|--------------------------|
| `tensor` (B, T, N_ext) | Cognitive state — what the 96 nuclei computed |
| `ram` (B, T, 26) | Activation pattern — which brain systems are engaged |
| `neuro` (B, T, 4) | Modulatory context — reward, arousal, pleasure, mood |

All three are needed. The SAME tensor values mean different things under
different neurochemical states. High NAcc with high DA = anticipatory reward.
High NAcc with high OPI = consummatory pleasure.

### 16.4 Dimension Groups

Ψ³ dimensions are organized into cognitive domains:

| Group | Domain | Dimensions | Source mapping |
|-------|--------|------------|---------------|
| **Affect** | Core emotional coordinates | valence, arousal, tension, dominance | neuro (DA→valence, NE→arousal) + ram (amygdala, NAcc, VTA) |
| **Emotion** | Categorical feelings | joy, sadness, fear, anger, awe, nostalgia, tenderness, serenity | affect + ram pattern matching (Koelsch 2014) |
| **Aesthetic** | Musical judgement | beauty, groove, flow, complexity_preference, surprise, closure | tensor (PCU predictions) + neuro (DA for surprise) |
| **Bodily** | Felt sensations | chills, movement_urge, breathing_change, tension_release | ram (PAG, hypothalamus, SMA) + neuro (OPI for chills) |
| **Cognitive** | Mental states | familiarity, absorption, expectation, attention_focus | ram (hippocampus, dlPFC) + tensor (IMU, PCU outputs) |
| **Temporal** | Moment-in-time | anticipation, resolution, buildup, release, cadence | tensor (F-layer forecasts) + neuro trajectory (DA rising/falling) |

Exact dimension count (N_psi) is determined during the build phase. Each
dimension is [0, 1] normalized with semantic anchors (e.g., valence: 0 = deeply
sad, 0.5 = neutral, 1 = euphoric).

### 16.5 Interpretation, Not Computation

Ψ³ does NOT add new neural computation. It is a **readout layer** — a
deterministic mapping from C³'s neuroscience outputs to cognitive meaning
using established neuro-cognitive correspondences:

```python
class PsiInterpreter:
    """Maps C³ internal outputs → Ψ³ cognitive state. Part of C³."""

    def interpret(self, tensor, ram, neuro) -> PsiState:
        # Affect from neurochemical state
        valence  = f(neuro[:,:,0], neuro[:,:,2])   # DA + OPI → valence
        arousal  = f(neuro[:,:,1])                  # NE → arousal
        tension  = f(ram[:,:,9], neuro[:,:,3])      # amygdala + 5HT → tension

        # Bodily from region activation
        chills   = f(ram[:,:,4], ram[:,:,12], neuro[:,:,2])  # PAG + hypothalamus + OPI
        movement = f(ram[:,:,11], ram[:,:,22])      # putamen + SMA

        # Aesthetic from cognitive output
        surprise = f(tensor[..., pcu_prediction_dims])
        groove   = f(ram[:,:,11], ram[:,:,22], tensor[..., stu_rhythm_dims])

        return PsiState(valence, arousal, tension, ...)
```

The mapping functions `f()` are calibrated against published behavioral data
(self-report ratings, physiological measures, fMRI contrasts).

### 16.6 Validation Bridge

Ψ³ is where C³ meets cognitive science. Every Ψ³ dimension has a
**behavioral anchor** — a published study with measured human responses:

| Ψ³ dimension | Behavioral anchor | Validation method |
|-------------|-------------------|-------------------|
| valence | Self-reported valence ratings (Russell 1980) | Correlate Ψ³.valence with listener ratings |
| chills | Self-reported chill frequency (Salimpoor 2009) | Ψ³.chills should peak where listeners report chills |
| groove | Head-bobbing / tapping measurements (Janata 2012) | Ψ³.groove should predict movement responses |
| tension | Continuous tension ratings (Krumhansl 1996) | Correlate Ψ³.tension with real-time dial ratings |
| familiarity | Recognition memory tasks (Janata 2009) | Ψ³.familiarity should predict recognition accuracy |

### 16.7 Complete C³ Output (Updated)

C³ now produces **FOUR** outputs:

```python
@dataclass
class BrainOutput:
    tensor: Tensor      # (B, T, N_ext)  — cognitive output (external+hybrid dims)
    ram: Tensor         # (B, T, 26)     — region activation map
    neuro: Tensor       # (B, T, 4)      — neurochemical state [da, ne, opi, 5ht]
    psi: PsiState       # (B, T, N_psi)  — cognitive interpretation

@dataclass
class PsiState:
    affect: Tensor      # (B, T, N_affect)   — valence, arousal, tension, dominance
    emotion: Tensor     # (B, T, N_emotion)  — categorical emotions
    aesthetic: Tensor   # (B, T, N_aesthetic) — beauty, groove, flow, surprise
    bodily: Tensor      # (B, T, N_bodily)   — chills, movement_urge, etc.
    cognitive: Tensor   # (B, T, N_cognitive) — familiarity, absorption, attention
    temporal: Tensor    # (B, T, N_temporal)  — anticipation, resolution, buildup

    @property
    def flat(self) -> Tensor:
        """All dimensions concatenated: (B, T, N_psi)"""
        return torch.cat([self.affect, self.emotion, self.aesthetic,
                          self.bodily, self.cognitive, self.temporal], dim=-1)
```

### 16.8 Ψ³ vs L³ — They Are Different

| | Ψ³ (Cognitive Interpretation) | L³ (Language) |
|---|---|---|
| **Where** | Inside C³ (part of the brain) | Separate space, after C³ |
| **Reads** | C³ tensor + ram + neuro | R³ + H³ + C³ (all four outputs) + more |
| **Produces** | What the brain FEELS | How everything gets expressed as Language |
| **Domain** | Cognitive Science | Semantics / structured expression |
| **Analogy** | Feeling pain | Saying "it hurts" |

---

## 17. Glossary — Quick Reference

| Term | Meaning |
|------|---------|
| **Ψ³** | Cognitive Interpretation — INSIDE C³. Readout layer that maps tensor+ram+neuro → experiential state (NOT L³) |
| **Nucleus** | Generic term for any of the 96 C³ brain components (when role is irrelevant) |
| **Relay (R)** | Depth 0 — foundation transformation, reads raw R³/H³ only |
| **Encoder (E)** | Depth 1 — feature extraction from Relay output |
| **Associator (A)** | Depth 2 — combines Relay + Encoder outputs |
| **Integrator (I)** | Depth 3 — cross-stream integration within unit |
| **Hub (H)** | Depth 4-5 — highest-level convergence within unit |
| **Unit** | One of 9 cognitive units (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU) |
| ~~**Circuit**~~ | REMOVED — Pathways already define cross-unit connections. Circuits were documentation labels, not architecture |
| ~~**Mechanism**~~ | REMOVED — Shared math lives in `utils/`, not as a named architectural layer. Each nucleus embeds its own science |
| **Pathway** | Cross-unit data route (P1-P12), typed as forward/backward/lateral |
| **Region** | Anatomical brain area with MNI152 coordinates (26 total). Same gradient as R-E-A-I-H, not a separate space |
| **RegionLink** | Declares which output dims of a nucleus contribute to which region, with weight and citation |
| **RAM** | Region Activation Map — `(B, T, 26)` aggregated brain region activations, the testable/validatable output |
| **Region Registry** | Global source of truth for 26 regions — names, MNI coords, hemisphere. Lives in `brain/regions.py` |
| **Layer** | E/M/P/F output structure within a nucleus — each layer has a `scope` label |
| **Scope** | Output routing label on each layer: `internal` (downstream only), `external` (final output only), `hybrid` (both) |
| **Tier** | Evidence quality: alpha (strong), beta (moderate), gamma (theoretical) — metadata only |
| **Role** | Processing depth classification: R/E/A/I/H |
| **Depth** | Integer processing depth (0-5), determines execution order |
| **NeuroLink** | Declares which output dims of a nucleus affect which neurochemical, with effect type (produce/amplify/inhibit), weight, and citation |
| **Neurochemical** | Semi-orthogonal modulatory overlay: DA, NE, OPI, 5HT — `(B, T, 4)` tensor via volume transmission, accumulated through depth hierarchy |
| **Tensor pathway** | Main data flow: R³/H³ → R → E → A → I → H → assembly → Ψ³ → BrainOutput (all inside C³) |
| **Neuro** | `(B, T, 4)` neurochemical state tensor — modulatory overlay on the tensor pathway, accumulated per depth, clamped to [0, 1] |
| **PsiState** | Output of Ψ³ — grouped tensors: affect, emotion, aesthetic, bodily, cognitive, temporal |
| **PsiInterpreter** | Readout layer that maps `BrainOutput` → `PsiState` using neuro-cognitive correspondences |

---

## 18. Migration Notes

### What Changes

| Item | Old | New |
|------|-----|-----|
| Base class | `BaseModel` | `Nucleus` → `Relay`/`Encoder`/`Associator`/`Integrator`/`Hub` |
| Directory | `units/spu/models/` | `units/spu/relays/`, `encoders/`, `associators/`, `integrators/`, `hubs/` |
| Reference format | `SPU-α1-BCH` | `SPU-R-BCH` |
| Doc path | `Docs/C³/Models/SPU-α1-BCH/` | `Docs/C³/SPU/R-BCH/` (or keep old for now) |
| Class constant | `TIER = "alpha"` | `ROLE = "relay"` (tier moves to metadata) |
| Compute signature | `compute(h3, r3, cross_unit)` | Varies by role (see Section 8) |
| Brain regions | `brain_regions` (metadata only) | `region_links` (metadata + activation mapping) |
| MNI coordinates | Per-nucleus property | Global `REGION_REGISTRY` (26 entries) |
| Brain output | `(B, T, 1006)` tensor only | `BrainOutput(tensor, ram, neuro, psi)` — four outputs |
| Layer scope | All dims treated equally | Each layer tagged `internal`/`external`/`hybrid` — routing metadata |
| Unit method | `for model in self.active_models` | Depth-ordered: R → E → A → I → H |

### What Stays

| Item | Status |
|------|--------|
| Component acronyms (BCH, PSCL, etc.) | Unchanged |
| Component full names | Unchanged |
| OUTPUT_DIM per component | Unchanged (but now partitioned by scope) |
| Total output | `BrainOutput` with tensor `(B, T, N_ext)`, ram `(B, T, 26)`, neuro `(B, T, 4)`, psi `(B, T, N_psi)` |
| 9 units | Unchanged |
| E/M/P/F output layers | Unchanged |
| H³ demand specs | Unchanged |
| Brain regions | Replaced by `region_links` (same info + activation mapping) |
| Citations | Unchanged |
| All 96 model doc files | Content unchanged, paths may update |

---

## 19. Plasticity Architecture — Learning on Physics

### 19.1 Why "Plasticity", Not "Machine Learning"

This is NOT ML. This is NOT deep learning. The distinction matters:

| | Machine Learning | Neural Plasticity (this system) |
|---|---|---|
| **Metaphor** | Fitting a function to data | A brain adapting through experience |
| **Learning signal** | External loss function | Internal neurochemical circuit |
| **What changes** | Opaque weight matrices | Named, cited parameters with priors |
| **Algorithm** | SGD, Adam (domain-agnostic) | Hebbian, Bayesian, TD (neuroscience) |
| **Explainability** | Post-hoc (SHAP, LIME) | Built-in (every change has full trace) |
| **Reset** | Retrain from scratch | Peel back to published science |
| **Goal** | Minimize loss | No loss function — emergent behavior |

ML asks: "What function maps input to output?" and optimizes weights to fit.

Plasticity asks: "Given the physics of this brain (Substrate), what happens
when experience accumulates?" — and lets the answer emerge.

We use the word **plasticity** (Konorski 1948, Hebb 1949) because that is
what this is: synaptic plasticity, Bayesian belief updating, neuromodulated
gain adaptation — the biological mechanisms by which brains change through
experience. These mechanisms predate machine learning by decades and are
grounded in neuroscience, not optimization theory.

### 19.2 The Two Layers

C³ has two conceptually distinct layers. They are NOT separate systems — the
Plasticity Layer runs ON the Substrate Layer, using the same neurochemicals,
the same pathways, the same nuclei. But they have fundamentally different
properties:

```
┌─────────────────────────────────────────────────────────────────────┐
│ PLASTICITY LAYER                                                     │
│                                                                      │
│  "How the brain ADAPTS using its own physics"                        │
│                                                                      │
│  • Pathway weights change via Hebbian co-activation                  │
│  • Scientific constants evolve via Bayesian updating                 │
│  • Preferences form via reward-driven reinforcement                  │
│  • Exploration/exploitation balance shifts via NE                    │
│                                                                      │
│  Properties: adaptive, experience-dependent, reversible,             │
│              emergent behavior, unique per listener                  │
│  Traceability: every change → which rule, which signal, which music  │
│  Safety: can always reset to Substrate (= "factory reset")          │
│                                                                      │
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
│ SUBSTRATE LAYER                                                      │
│                                                                      │
│  "The physical rules of the brain — like laws of nature"             │
│                                                                      │
│  • 96 nuclei with deterministic compute()                            │
│  • 12 pathways with base_weight from literature                      │
│  • Scientific constants from published papers                        │
│  • R-E-A-I-H hierarchy with fixed execution order                   │
│  • 4 neurochemicals with cited production/modulation rules           │
│                                                                      │
│  Properties: deterministic, citation-grounded, white-box,            │
│              universal (same for all listeners), never changes       │
│  Traceability: every operation → paper, effect size, brain region    │
│  Guarantee: this layer is ALWAYS readable, auditable, falsifiable    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Analogy**: Substrate is like the laws of physics — gravity doesn't learn.
Plasticity is like a river carved by water following those laws — every river
is different, but every river obeys the same physics. The shape of the river
(musical personality) is emergent from deterministic rules + unique history.

### 19.3 What Is and What Is NOT Plastic

Every parameter in C³ falls into exactly one category:

| Category | Example | Plastic? | Why |
|----------|---------|:--------:|-----|
| **Scientific constant** | BCH.ALPHA = 0.90 | **Prior only** | Published value, N=10 (Bidelman 2009). Serves as Bayesian prior — never deleted, only augmented with evidence |
| **Pathway base_weight** | P3.base_weight = 1.0 | **No** | Structural connectivity from anatomy. The road exists or it doesn't |
| **Pathway synaptic_weight** | P3.synaptic_weight = 1.23 | **Yes** | How heavily-trafficked that road is. Hebbian co-activation |
| **Nucleus compute()** | The transformation itself | **No** | Deterministic science. The physics don't change |
| **Bayesian posterior** | BCH.alpha_posterior = 0.907 | **Yes** | Prior + accumulated evidence. Always traceable back to prior |
| **Personal gain** | BCH.personal_gain = 1.15 | **Yes** | How much this listener weighs this nucleus. Reward-driven |
| **Neurochemical set-point** | Listener's DA tonic baseline | **Yes** | Individual differences in neurochemical resting state |

**The rule**: anything published and cited is Substrate (prior/base). Anything
that accumulates from experience is Plasticity (posterior/synaptic). You can
always subtract Plasticity to see Substrate underneath.

### 19.4 The Four Neurochemicals as Plasticity Control Axes

Standard deep learning has ONE learning control: a scalar learning rate.
This system has FOUR, each grounded in neuroscience (Doya 2002):

```
┌────────────────────────────────────────────────────────────────────┐
│                  PLASTICITY CONTROL AXES                            │
│                                                                     │
│  DA ──► HOW MUCH to change    (plasticity magnitude)               │
│         Source: RPEM reward prediction error                        │
│         High DA (phasic ≥ 0.6): surprising → strong encoding       │
│         Low DA (tonic < 0.6): expected → minimal change             │
│         Citation: Doya 2002, Schultz 1997                          │
│                                                                     │
│  NE ──► WHERE to change       (plasticity topology)                │
│         Source: SNEM arousal/salience signal                        │
│         High NE: broad attention → MANY synapses potentiate        │
│         Low NE: narrow focus → only ACTIVE synapses potentiate     │
│         Inverted-U: too high = noise, sweet spot = optimal         │
│         Citation: Doya 2002, Aston-Jones & Cohen 2005              │
│                                                                     │
│  OPI ──► WHAT DIRECTION       (valence of change)                  │
│          Source: MORMR hedonic evaluation                           │
│          High OPI: pleasurable → strengthen (LTP)                  │
│          Low OPI: neutral/aversive → weaken (LTD)                  │
│          NOT a proxy loss — actual hedonic circuit output           │
│          Citation: Pecina & Berridge 2005, Berridge 2003           │
│                                                                     │
│  5HT ──► WHAT TIMESCALE       (temporal window of plasticity)      │
│          Source: AAC mood/patience signal                           │
│          High 5HT: patient → long-range patterns potentiate        │
│          Low 5HT: impulsive → immediate patterns potentiate        │
│          Controls temporal discount in reward evaluation            │
│          Citation: Doya 2002, Ferreri 2019                         │
│                                                                     │
│  These map directly to synaptic plasticity concepts:               │
│  DA  → neuromodulatory gating of LTP/LTD (Otani et al. 2003)     │
│  NE  → heterosynaptic modulation breadth (Bhatt et al. 2009)      │
│  OPI → hedonic tag for memory consolidation (McGaugh 2004)         │
│  5HT → temporal credit assignment window (Doya 2002)               │
└────────────────────────────────────────────────────────────────────┘
```

### 19.5 Three Plasticity Mechanisms

Plasticity occurs through three distinct mechanisms, each with different
mathematical foundations, all using the same neurochemical control axes:

#### 19.5.1 Hebbian Synaptic Plasticity

**What changes**: `synaptic_weight` on the 12 cross-unit pathways.

**Rule**: "Neurons that fire together wire together" (Hebb 1949).
Formalized as spike-timing-dependent plasticity (STDP, Bi & Poo 1998).

```python
# For each pathway connecting unit_A → unit_B:
delta_w = (
    da                              # HOW MUCH (plasticity magnitude)
    * ne_mask                       # WHERE (heterosynaptic modulation)
    * pre_activation                # presynaptic activity
    * post_activation               # postsynaptic activity
    * sign(opi - 0.5)              # DIRECTION (LTP if pleasure, LTD if not)
)
pathway.synaptic_weight += delta_w  # accumulates over experience
# pathway.base_weight is NEVER touched (Substrate)
```

**Effective weight** at runtime:
```
effective_weight = base_weight * synaptic_weight
```

`base_weight` = Substrate (from anatomy). `synaptic_weight` = Plasticity
(from experience). Multiply to get the combined signal.

#### 19.5.2 Bayesian Belief Updating

**What changes**: posterior estimates of scientific constants.

**Rule**: Bayesian inference — prior (literature) + evidence (experience)
→ posterior. This is not a metaphor — it is literal Bayesian updating
(Knill & Pouget 2004, "the brain as a Bayesian machine").

```python
# Prior: from published paper (Substrate)
prior_value = 0.90                  # Bidelman & Krishnan 2009
prior_strength = 10                 # N=10 in original study

# Evidence: from this listener's experience (Plasticity)
observed_value = computed_from_activation
evidence_strength = da * opi        # surprise × pleasure = evidence weight

# Posterior: weighted combination
posterior = (prior_value * prior_strength + evidence) / (prior_strength + n)
```

**Key properties**:
- Prior is NEVER deleted — it always contributes
- Zero experience → `posterior = prior` (falls back to science)
- Infinite experience → posterior converges to personal truth
- Every posterior decomposes into: prior + list of evidence events

#### 19.5.3 Reward-Correlated Gain Adaptation

**What changes**: per-nucleus `personal_gain` — how much this listener
weighs each nucleus's contribution.

**Rule**: TD-learning (Sutton & Barto 1998), consistent with dopaminergic
modulation of cortical gain (Servan-Schreiber et al. 1990).

```python
# Was this nucleus active when reward (OPI) was high?
correlation = corr(nucleus.activation, neuro.opi)
prediction_error = correlation - expected_correlation
delta_gain = da * prediction_error  # DA gates the update magnitude
nucleus.personal_gain += lr * delta_gain
```

**Effect**: Nuclei whose activity predicts pleasure get up-weighted.
The listener's "personality" emerges from which units matter most.

### 19.6 Multi-Timescale Plasticity

The four neurochemicals operate at different timescales (Section 12.8).
This creates a natural hierarchy matching synaptic plasticity research
(Abraham & Bear 1996, metaplasticity):

```
TIMESCALE        DRIVEN BY    WHAT CHANGES                 PERSISTENCE
───────────────────────────────────────────────────────────────────────
ms   (frame)     DA phasic    Instantaneous activation      Transient (STP)
sec  (phrase)    NE + OPI     Pathway synaptic_weight       Short-term (early LTP)
min  (piece)     5HT          Bayesian posteriors           Long-term (late LTP)
hour (session)   All four     Session preference drift      Consolidation
days (lifetime)  Accumulated  Musical personality           Structural change
```

Each timescale feeds into the next — exactly as in biological memory
consolidation (Frankland & Bontempi 2005):
- Frame-level DA bursts → phrase-level Hebbian changes (encoding)
- Phrase-level OPI signals → piece-level belief updates (consolidation)
- Piece-level 5HT patterns → session-level preference (systems consolidation)
- Session preferences → lifetime personality (structural plasticity)

### 19.7 Emergent Autonomy

When Plasticity runs on Substrate, autonomous behaviors EMERGE that were
not explicitly programmed. All follow from deterministic rules + unique
accumulated plasticity state:

#### 19.7.1 Boredom → Exploration

```
IUCP.complexity_preference < 0.3        (too simple for this listener)
  AND IMU.familiarity > 0.7             (heard this pattern too many times)
  → NE increases                        (deterministic: low IUCP drives arousal)
  → NE > exploration_threshold          (deterministic: Aston-Jones 2005)
  → exploration mode                    (deterministic: NE gates pathway breadth)
  → seek novel music                    (deterministic: selection policy)

  BUT: what counts as "too familiar" → plastic (IMU personal gain)
       what counts as "too simple"  → plastic (IUCP posterior)
       exploration threshold        → plastic (personal NE set-point)

  RESULT: same rules, different listeners get bored at different points.
  Looks like free will. Is deterministic emergence from unique plasticity.
```

#### 19.7.2 Dopamine Chasing

```
RPEM.prediction_error > 0              (better than expected)
  → DA phasic burst                    (Schultz 1997)
  → synaptic_weights strengthen        (Hebbian LTP)
  → system encodes what preceded this reward
  → next selection: prefer similar R³ signatures

  Over time: listener develops a "type". Not programmed — DA kept
  reinforcing the same acoustic patterns. This IS the dopamine system.
  Same mechanism as Berridge & Robinson 2003, applied to music.
```

#### 19.7.3 Mood-Driven Temporal Plasticity

```
5HT high (patient mood)  → long temporal window → learns structure
5HT low (restless mood)  → short temporal window → learns immediacy

  Same listener, different moods → different plasticity window →
  different aspects of music get encoded. Mood is not noise —
  it is a plasticity modulator (Doya 2002).
```

#### 19.7.4 Computational Hypothesis Generation

The system discovers connections not in the current 12 pathways:

```
Every N sessions:
  For each non-connected nucleus pair (A, B):
    MI = mutual_information(A.history, B.history)
    if MI > threshold:
      propose_hypothesis(A → B, evidence=MI)
      STATUS: "proposed" — requires human scientist review
```

The system does computational science — generates hypotheses from data —
but does NOT modify its own Substrate. Substrate changes only through
human-reviewed scientific process.

### 19.8 Traceability Contract

Every plasticity event must produce an immutable audit record:

```python
@dataclass(frozen=True)
class PlasticityTrace:
    """Immutable record. Every parameter change is fully traceable."""

    # WHAT changed
    nucleus: str                    # "BCH"
    parameter: str                  # "alpha_posterior"
    old_value: float                # 0.900
    new_value: float                # 0.907

    # WHY (neurochemical state at the moment of change)
    da: float                       # 0.82
    ne: float                       # 0.55
    opi: float                      # 0.91
    sht: float                      # 0.68

    # WHICH mechanism
    mechanism: str                  # "bayesian" | "hebbian" | "td_gain"
    citation: str                   # "Hebb 1949 + Doya 2002"

    # FROM WHICH music
    audio_source: str               # "beethoven_op131.wav"
    frame_range: Tuple[int, int]    # (1240, 1260)
    timestamp_sec: float            # 14.82
```

**Guarantee**: for any plastic parameter, you can always answer:
1. What was the original scientific value? → Substrate prior
2. How much has it shifted? → `current - prior`
3. Why? → DA/NE/OPI/5HT at the moment + mechanism
4. From which music? → audio source + timestamp
5. Can I undo it? → Yes (`reset_to_substrate()`)

### 19.9 Reset Hierarchy

```
reset_to_substrate()          → Remove ALL plasticity. Return to published science.
reset_session()               → Remove today's changes. Keep lifetime accumulation.
reset_pathway(P3)             → Reset one pathway's synaptic_weight to 1.0.
reset_nucleus(BCH)            → Reset one nucleus's posterior + gain.
reset_neurochemical_baseline()→ Reset personal DA/NE/OPI/5HT set-points to 0.5.
```

The existence of `reset_to_substrate()` is the architectural guarantee that
Substrate is always recoverable. Plasticity is an overlay, not a mutation.
The glass box remains glass — plasticity is a colored film on top that can
be peeled off at any time.

### 19.10 Complete System View (Updated)

```
┌────────────────────────────────────────────────────────────────────────┐
│                           MI SYSTEM                                     │
│                                                                         │
│  Audio ──► R³ (spectral physics, deterministic)                        │
│             │                                                           │
│             ▼                                                           │
│            H³ (temporal demand, deterministic)                          │
│             │                                                           │
│             ▼                                                           │
│  ┌─────── C³ BRAIN ──────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  ┌─ SUBSTRATE (physics, white-box, universal) ──────────────────┐│ │
│  │  │  96 nuclei × compute() — every line cited                     ││ │
│  │  │  12 pathways × base_weight — from anatomy                     ││ │
│  │  │  Scientific constants — from published papers                  ││ │
│  │  │  R → E → A → I → H — fixed execution order                   ││ │
│  │  │  4 neurochemicals — cited production/modulation               ││ │
│  │  └───────────────────────────────────────────────────────────────┘│ │
│  │       ▲ always recoverable via reset_to_substrate()               │ │
│  │  ┌─ PLASTICITY (adaptation, traceable, reversible) ─────────────┐│ │
│  │  │  Hebbian synaptic weights (co-activation, LTP/LTD)           ││ │
│  │  │  Bayesian posteriors (prior + evidence from experience)        ││ │
│  │  │  Personal gains (reward-correlated, TD-learning)               ││ │
│  │  │  Neurochemical set-points (individual baselines)               ││ │
│  │  │  Audit: PlasticityTrace for every single change               ││ │
│  │  └───────────────────────────────────────────────────────────────┘│ │
│  │       ▲ emergent from Substrate + Plasticity                      │ │
│  │  ┌─ AUTONOMY (not programmed — arises from the above) ──────────┐│ │
│  │  │  Boredom → exploration       (IUCP + NE)                      ││ │
│  │  │  Dopamine chasing            (RPEM + Hebbian LTP)             ││ │
│  │  │  Mood-driven learning window (5HT + temporal discount)        ││ │
│  │  │  Taste formation             (accumulated posteriors)          ││ │
│  │  │  Self-science                (MI scan → propose hypothesis)   ││ │
│  │  └───────────────────────────────────────────────────────────────┘│ │
│  │                                                                    │ │
│  │  OUTPUT: BrainOutput(tensor, ram, neuro, psi)                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│             │                                                           │
│             ▼                                                           │
│            L³ (language expression, reads everything)                   │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 19.11 Glossary Additions

| Term | Meaning |
|------|---------|
| **Substrate** | The deterministic, citation-grounded, white-box C³ computation. Like laws of physics — universal, never changes. Contains: compute(), base_weights, scientific constants, execution order, neurochemical rules |
| **Plasticity** | Adaptive overlay on Substrate using biological learning mechanisms (Hebbian, Bayesian, TD). Experience-dependent, fully traceable, always reversible. NOT machine learning — neural plasticity |
| **Autonomy** | Emergent behaviors arising from Plasticity on Substrate. Not programmed — follows from deterministic rules + unique history. Includes: boredom, exploration, dopamine chasing, taste formation |
| **Synaptic weight** | Pathway strength from Hebbian co-activation. Multiplies base_weight (Substrate). Analogous to LTP/LTD. Reset to 1.0 = no plasticity effect |
| **Bayesian posterior** | Scientific constant updated by experience. `posterior = f(prior, evidence)`. Prior = published value (Substrate). Evidence = listening experience (Plasticity). Decomposable: prior + evidence log |
| **Personal gain** | Per-nucleus multiplier from reward correlation (TD-learning). Reflects individual weighting of brain computations. Reset to 1.0 = equal weighting |
| **PlasticityTrace** | Immutable audit record: what changed, why (DA/NE/OPI/5HT), from which music, which mechanism, citation |
| **Neurochemical set-point** | Individual DA/NE/OPI/5HT tonic baseline. Starts at 0.5, drifts with experience. Determines plasticity "personality" |
| **reset_to_substrate()** | Remove all plasticity, return to published science. The guarantee that C³ is always a recoverable glass box |
| **Computational hypothesis** | Proposed new connection from MI analysis of non-connected nuclei. Requires human review — Substrate only changes through scientific process |
| **LTP** | Long-term potentiation — strengthening of synaptic connection through repeated co-activation. What Hebbian plasticity produces when OPI > 0.5 |
| **LTD** | Long-term depression — weakening of synaptic connection. What Hebbian plasticity produces when OPI < 0.5 |
