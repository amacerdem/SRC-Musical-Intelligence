export type MechanismType = 'relay' | 'encoder' | 'associator' | 'integrator' | 'hub'

export interface MechanismDef {
  name: string          // uppercase abbreviation (e.g. "BCH")
  fullName: string      // full name (e.g. "Brainstem Consonance Hierarchy")
  type: MechanismType
  functionId: string    // f1-f9
  unit: string          // SPU, ASU, etc. or '\u2014' if not listed
  depth: number         // 0-5
  outputDim: number     // e.g. 16 (just the number, D suffix stripped)
}

export const MECHANISMS: MechanismDef[] = [
  // ── F1: Sensory Processing — 11 mechanisms ──────────────────────────
  { name: 'BCH',   fullName: 'Brainstem Consonance Hierarchy',            type: 'relay',      functionId: 'f1', unit: 'SPU', depth: 0, outputDim: 16 },
  { name: 'CSG',   fullName: 'Consonance-Salience Gradient',             type: 'relay',      functionId: 'f1', unit: 'ASU', depth: 0, outputDim: 12 },
  { name: 'MIAA',  fullName: 'Musical Imagery Auditory Activation',      type: 'relay',      functionId: 'f1', unit: 'SPU', depth: 0, outputDim: 11 },
  { name: 'MPG',   fullName: 'Melodic Processing Gradient',              type: 'relay',      functionId: 'f1', unit: 'NDU', depth: 0, outputDim: 10 },
  { name: 'PNH',   fullName: 'Pythagorean Neural Hierarchy',             type: 'relay',      functionId: 'f1', unit: 'IMU', depth: 0, outputDim: 11 },
  { name: 'SDNPS', fullName: 'Stimulus-Dependent NPS',                   type: 'relay',      functionId: 'f1', unit: 'SPU', depth: 0, outputDim: 10 },
  { name: 'SDED',  fullName: 'Sensory Dissonance Early Detection',       type: 'relay',      functionId: 'f1', unit: 'SPU', depth: 0, outputDim: 10 },
  { name: 'TPIO',  fullName: 'Timbre Perception-Imagery Overlap',        type: 'relay',      functionId: 'f1', unit: 'SPU', depth: 0, outputDim: 10 },
  { name: 'PSCL',  fullName: 'Pitch Salience in Cortical Lateralization', type: 'encoder',   functionId: 'f1', unit: 'SPU', depth: 1, outputDim: 16 },
  { name: 'PCCR',  fullName: 'Pitch Chroma Cortical Representation',     type: 'associator', functionId: 'f1', unit: 'SPU', depth: 2, outputDim: 11 },
  { name: 'STAI',  fullName: 'Spectral-Temporal Aesthetic Integration',  type: 'encoder',    functionId: 'f1', unit: 'SPU', depth: 1, outputDim: 12 },

  // ── F2: Pattern Recognition & Prediction — 10 mechanisms ────────────
  { name: 'HTP',   fullName: 'Hierarchical Temporal Prediction',         type: 'relay',      functionId: 'f2', unit: '\u2014', depth: 0, outputDim: 12 },
  { name: 'SPH',   fullName: 'Sequence Prediction Hierarchy',            type: 'relay',      functionId: 'f2', unit: '\u2014', depth: 0, outputDim: 14 },
  { name: 'ICEM',  fullName: 'Information Content & Emotional Modulation', type: 'relay',    functionId: 'f2', unit: '\u2014', depth: 0, outputDim: 13 },
  { name: 'PWUP',  fullName: 'Precision-Weighted Uncertainty Processing', type: 'encoder',   functionId: 'f2', unit: '\u2014', depth: 1, outputDim: 10 },
  { name: 'WMED',  fullName: 'Working Memory Expectation Dynamics',      type: 'associator', functionId: 'f2', unit: '\u2014', depth: 2, outputDim: 11 },
  { name: 'UDP',   fullName: 'Uncertainty-Driven Pleasure',              type: 'integrator', functionId: 'f2', unit: '\u2014', depth: 3, outputDim: 10 },
  { name: 'CHPI',  fullName: 'Cross-Modal Harmonic Predictive Integration', type: 'integrator', functionId: 'f2', unit: '\u2014', depth: 3, outputDim: 11 },
  { name: 'IGFE',  fullName: 'Information-Gain Feature Extraction',      type: 'integrator', functionId: 'f2', unit: '\u2014', depth: 3, outputDim: 9 },
  { name: 'MAA',   fullName: 'Musical Appreciation of Atonality',        type: 'hub',        functionId: 'f2', unit: '\u2014', depth: 4, outputDim: 10 },
  { name: 'PSH',   fullName: 'Prediction Surprise Hierarchy',            type: 'hub',        functionId: 'f2', unit: '\u2014', depth: 5, outputDim: 10 },

  // ── F3: Attention & Salience — 12 mechanisms ────────────────────────
  { name: 'SNEM',  fullName: 'Sensory Novelty & Expectation Model',      type: 'relay',      functionId: 'f3', unit: 'ASU', depth: 0, outputDim: 12 },
  { name: 'IACM',  fullName: 'Inharmonic Attention Capture Model',       type: 'relay',      functionId: 'f3', unit: 'ASU', depth: 0, outputDim: 11 },
  { name: 'BARM',  fullName: 'Beat-Aligned Resource Model',              type: 'encoder',    functionId: 'f3', unit: 'ASU', depth: 1, outputDim: 10 },
  { name: 'STANM', fullName: 'Sustained Tonal Attention Network Model',  type: 'encoder',    functionId: 'f3', unit: 'ASU', depth: 1, outputDim: 11 },
  { name: 'AACM',  fullName: 'Aesthetic Attention Coupling Model',       type: 'encoder',    functionId: 'f3', unit: 'ASU', depth: 1, outputDim: 10 },
  { name: 'AMSS',  fullName: 'Attentional Modulation of Sound Streams',  type: 'encoder',    functionId: 'f3', unit: 'STU', depth: 1, outputDim: 11 },
  { name: 'ETAM',  fullName: 'Entrainment-Triggered Attention Model',    type: 'encoder',    functionId: 'f3', unit: 'STU', depth: 1, outputDim: 11 },
  { name: 'DGTP',  fullName: 'Dynamic Gain & Timing Precision',          type: 'associator', functionId: 'f3', unit: 'ASU', depth: 2, outputDim: 9 },
  { name: 'SDL',   fullName: 'Sensory Discrimination Learning',          type: 'associator', functionId: 'f3', unit: 'ASU', depth: 2, outputDim: 9 },
  { name: 'NEWMD', fullName: 'Neural Event-Window Model of Deviance',    type: 'associator', functionId: 'f3', unit: 'STU', depth: 2, outputDim: 10 },
  { name: 'IGFE',  fullName: 'Information-Gain Feature Extraction',      type: 'associator', functionId: 'f3', unit: 'PCU', depth: 2, outputDim: 9 },
  { name: 'PWSM',  fullName: 'Precision-Weighted Salience Mixer',        type: 'associator', functionId: 'f3', unit: 'ASU', depth: 2, outputDim: 9 },

  // ── F4: Memory & Retrieval — 15 mechanisms ──────────────────────────
  { name: 'MEAMN', fullName: 'Music-Evoked Autobiographical Memory Network', type: 'relay',   functionId: 'f4', unit: '\u2014', depth: 0, outputDim: 12 },
  { name: 'MMP',   fullName: 'Multi-Modal Perceptual Processing',        type: 'relay',      functionId: 'f4', unit: '\u2014', depth: 0, outputDim: 12 },
  { name: 'PNH',   fullName: 'Pythagorean Neural Hierarchy',             type: 'relay',      functionId: 'f4', unit: '\u2014', depth: 0, outputDim: 11 },
  { name: 'HCMC',  fullName: 'Hippocampal-Cortical Memory Circuit',      type: 'encoder',    functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'RASN',  fullName: 'Rhythmic Auditory Stimulation Neuroplasticity', type: 'encoder', functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'PMIM',  fullName: 'Predictive Memory Integration Model',      type: 'encoder',    functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'OII',   fullName: 'Oscillatory Intelligence Integration',     type: 'encoder',    functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 10 },
  { name: 'RIRI',  fullName: 'RAS-Intelligent Rehabilitation Integration', type: 'encoder',  functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 10 },
  { name: 'MSPBA', fullName: 'Musical Syntax Processing in Broca\'s Area', type: 'encoder',  functionId: 'f4', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'DMMS',  fullName: 'Developmental Music Memory Scaffold',      type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'CSSL',  fullName: 'Cross-Species Song Learning',              type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'CDEM',  fullName: 'Context-Dependent Emotional Memory',       type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'TPRD',  fullName: 'Tonotopy-Pitch Representation Dissociation', type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'CMAPCC', fullName: 'Cross-Modal Action-Perception Common Code', type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'VRIAP', fullName: 'VR-Integrated Analgesia Paradigm',         type: 'associator', functionId: 'f4', unit: '\u2014', depth: 2, outputDim: 10 },

  // ── F5: Emotion — 12 mechanisms ─────────────────────────────────────
  { name: 'SRP',   fullName: 'Salience-Reward Pathway',                  type: 'relay',      functionId: 'f5', unit: '\u2014', depth: 0, outputDim: 19 },
  { name: 'AAC',   fullName: 'Affective Attentional Coupling',           type: 'relay',      functionId: 'f5', unit: '\u2014', depth: 0, outputDim: 14 },
  { name: 'VMM',   fullName: 'Valence-Mood Modulation',                  type: 'relay',      functionId: 'f5', unit: '\u2014', depth: 0, outputDim: 12 },
  { name: 'PUPF',  fullName: 'Pleasure-Uncertainty Prediction Function', type: 'encoder',    functionId: 'f5', unit: '\u2014', depth: 1, outputDim: 12 },
  { name: 'CLAM',  fullName: 'Closed-Loop Affective Modulation',         type: 'encoder',    functionId: 'f5', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'MAD',   fullName: 'Musical Anhedonia Disconnection',          type: 'encoder',    functionId: 'f5', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'NEMAC', fullName: 'Nostalgia-Evoked Memory-Affect Circuit',   type: 'encoder',    functionId: 'f5', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'STAI',  fullName: 'Spectral-Temporal Aesthetic Integration',  type: 'encoder',    functionId: 'f5', unit: '\u2014', depth: 1, outputDim: 12 },
  { name: 'DAP',   fullName: 'Developmental Affective Plasticity',       type: 'associator', functionId: 'f5', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'CMAT',  fullName: 'Cross-Modal Affective Transfer',           type: 'associator', functionId: 'f5', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'TAR',   fullName: 'Therapeutic Affective Resonance',          type: 'associator', functionId: 'f5', unit: '\u2014', depth: 2, outputDim: 10 },
  { name: 'MAA',   fullName: 'Musical Appreciation of Atonality',        type: 'associator', functionId: 'f5', unit: '\u2014', depth: 2, outputDim: 10 },

  // ── F6: Reward & Motivation — 10 mechanisms ─────────────────────────
  { name: 'DAED',  fullName: 'Dopamine Anticipation-Experience Dissociation', type: 'relay',  functionId: 'f6', unit: '\u2014', depth: 0, outputDim: 8 },
  { name: 'MORMR', fullName: 'Mesolimbic Opioid-Reward Modulation Route', type: 'relay',     functionId: 'f6', unit: '\u2014', depth: 0, outputDim: 7 },
  { name: 'RPEM',  fullName: 'Reward Prediction Error Modulation',       type: 'relay',      functionId: 'f6', unit: '\u2014', depth: 0, outputDim: 8 },
  { name: 'IUCP',  fullName: 'Inverted-U Complexity Preference',         type: 'encoder',    functionId: 'f6', unit: '\u2014', depth: 1, outputDim: 6 },
  { name: 'MCCN',  fullName: 'Musical Chills Cortical Network',          type: 'encoder',    functionId: 'f6', unit: '\u2014', depth: 1, outputDim: 7 },
  { name: 'MEAMR', fullName: 'Music-Evoked Autobiographical Memory Reward', type: 'encoder', functionId: 'f6', unit: '\u2014', depth: 1, outputDim: 6 },
  { name: 'SSRI',  fullName: 'Social Synchrony Reward Integration',      type: 'encoder',    functionId: 'f6', unit: '\u2014', depth: 1, outputDim: 11 },
  { name: 'LDAC',  fullName: 'Liking-Dependent Auditory Cortex',         type: 'associator', functionId: 'f6', unit: '\u2014', depth: 2, outputDim: 6 },
  { name: 'IOTMS', fullName: 'Individual Opioid Tone Music Sensitivity', type: 'associator', functionId: 'f6', unit: '\u2014', depth: 2, outputDim: 5 },
  { name: 'SSPS',  fullName: 'Saddle-Shaped Preference Surface',         type: 'associator', functionId: 'f6', unit: '\u2014', depth: 2, outputDim: 6 },

  // ── F7: Motor & Timing — 12 mechanisms ──────────────────────────────
  { name: 'PEOM',  fullName: 'Period Entrainment Optimization Model',    type: 'relay',      functionId: 'f7', unit: 'MPU', depth: 0, outputDim: 11 },
  { name: 'MSR',   fullName: 'Motor Synchronization Response',           type: 'relay',      functionId: 'f7', unit: 'MPU', depth: 0, outputDim: 11 },
  { name: 'GSSM',  fullName: 'Groove State Sensorimotor Mapping',        type: 'relay',      functionId: 'f7', unit: 'MPU', depth: 0, outputDim: 11 },
  { name: 'HMCE',  fullName: 'Hierarchical Musical Context Encoding',    type: 'relay',      functionId: 'f7', unit: 'STU', depth: 0, outputDim: 11 },
  { name: 'ASAP',  fullName: 'Action Simulation for Auditory Prediction', type: 'encoder',   functionId: 'f7', unit: 'MPU', depth: 1, outputDim: 11 },
  { name: 'DDSMI', fullName: 'Dyadic Dance Social Motor Integration',    type: 'encoder',    functionId: 'f7', unit: 'MPU', depth: 1, outputDim: 11 },
  { name: 'VRMSME', fullName: 'VR Music Stimulation Motor Enhancement',  type: 'encoder',    functionId: 'f7', unit: 'MPU', depth: 1, outputDim: 11 },
  { name: 'SPMC',  fullName: 'SMA-Premotor-M1 Motor Circuit',            type: 'encoder',    functionId: 'f7', unit: 'MPU', depth: 1, outputDim: 11 },
  { name: 'HGSIC', fullName: 'Hierarchical Groove State Integration Circuit', type: 'encoder', functionId: 'f7', unit: 'STU', depth: 1, outputDim: 11 },
  { name: 'NSCP',  fullName: 'Neural Synchrony Commercial Prediction',   type: 'associator', functionId: 'f7', unit: 'MPU', depth: 2, outputDim: 11 },
  { name: 'CTBB',  fullName: 'Cerebellar Theta-Burst Balance',           type: 'associator', functionId: 'f7', unit: 'MPU', depth: 2, outputDim: 11 },
  { name: 'STC',   fullName: 'Singing Training Connectivity',            type: 'associator', functionId: 'f7', unit: 'MPU', depth: 2, outputDim: 11 },

  // ── F8: Learning & Expertise — 6 mechanisms ─────────────────────────
  { name: 'EDNR',  fullName: 'Error-Driven Neural Refinement',           type: 'relay',      functionId: 'f8', unit: 'NDU', depth: 0, outputDim: 10 },
  { name: 'TSCP',  fullName: 'Temporal Synaptic Consolidation Processor', type: 'encoder',   functionId: 'f8', unit: 'SPU', depth: 1, outputDim: 10 },
  { name: 'CDMR',  fullName: 'Context-Dependent Mismatch Response',      type: 'encoder',    functionId: 'f8', unit: 'NDU', depth: 1, outputDim: 11 },
  { name: 'SLEE',  fullName: 'Synaptic Long-term Encoding Engine',       type: 'encoder',    functionId: 'f8', unit: 'NDU', depth: 1, outputDim: 13 },
  { name: 'ESME',  fullName: 'Error-Signal Modulated Encoding',          type: 'associator', functionId: 'f8', unit: 'SPU', depth: 2, outputDim: 11 },
  { name: 'ECT',   fullName: 'Expertise Compartmentalization Trade-off', type: 'associator', functionId: 'f8', unit: 'NDU', depth: 2, outputDim: 12 },

  // ── F9: Social Cognition — 0 mechanisms ─────────────────────────────
  // F9 is a pure belief layer with zero mechanisms.
  // All 10 beliefs source from cross-function mechanisms:
  // SSRI (F6 Encoder), NSCP (F7 Associator), DDSMI (F7 Encoder).
]

export function getMechanismsByFunction(fId: string): MechanismDef[] {
  return MECHANISMS.filter(m => m.functionId === fId)
}
