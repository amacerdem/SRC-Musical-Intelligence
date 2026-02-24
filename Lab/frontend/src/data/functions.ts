/** MI-Lab Static Registry: 9 C³ Functions */

export interface FunctionDef {
  id: string
  index: number
  name: string
  unit: string
  color: string
  description: string
  beliefCounts: { core: number; appraisal: number; anticipation: number; total: number }
  mechanismCount: number
  relay: string | null
  depthRange: [number, number]
}

export const FUNCTIONS: FunctionDef[] = [
  {
    id: 'f1', index: 1, name: 'Sensory Processing', unit: 'SPU', color: '#3b82f6',
    description: 'Primary auditory encoding — spectral, harmonic, and timbral feature extraction from cochlear input',
    beliefCounts: { core: 5, appraisal: 7, anticipation: 5, total: 17 },
    mechanismCount: 11, relay: 'BCH', depthRange: [0, 2],
  },
  {
    id: 'f2', index: 2, name: 'Pattern Recognition & Prediction', unit: 'PCU', color: '#8b5cf6',
    description: 'Hierarchical temporal prediction — sequence matching, information content, precision-weighted surprise',
    beliefCounts: { core: 4, appraisal: 6, anticipation: 5, total: 15 },
    mechanismCount: 10, relay: 'HTP', depthRange: [0, 5],
  },
  {
    id: 'f3', index: 3, name: 'Attention & Salience', unit: 'ASU', color: '#f97316',
    description: 'Selective attention and salience computation — beat entrainment, novelty detection, precision weighting',
    beliefCounts: { core: 4, appraisal: 7, anticipation: 4, total: 15 },
    mechanismCount: 12, relay: 'SNEM', depthRange: [0, 2],
  },
  {
    id: 'f4', index: 4, name: 'Memory & Retrieval', unit: 'IMU', color: '#14b8a6',
    description: 'Episodic and autobiographical memory — familiarity, emotional coloring, nostalgia, hippocampal binding',
    beliefCounts: { core: 4, appraisal: 7, anticipation: 2, total: 13 },
    mechanismCount: 15, relay: 'MEAMN', depthRange: [0, 2],
  },
  {
    id: 'f5', index: 5, name: 'Emotion', unit: 'ARU', color: '#ec4899',
    description: 'Affective evaluation — arousal, valence, mode detection, nostalgia-affect circuit',
    beliefCounts: { core: 4, appraisal: 8, anticipation: 2, total: 14 },
    mechanismCount: 12, relay: 'SRP', depthRange: [0, 2],
  },
  {
    id: 'f6', index: 6, name: 'Reward & Motivation', unit: 'RPU', color: '#f59e0b',
    description: 'Dopaminergic reward — wanting/liking/pleasure, prediction error, tension-resolution dynamics',
    beliefCounts: { core: 5, appraisal: 7, anticipation: 4, total: 16 },
    mechanismCount: 10, relay: 'DAED', depthRange: [0, 2],
  },
  {
    id: 'f7', index: 7, name: 'Motor & Timing', unit: 'MPU', color: '#22c55e',
    description: 'Sensorimotor coupling — period entrainment, groove, hierarchical context encoding, timing precision',
    beliefCounts: { core: 4, appraisal: 9, anticipation: 4, total: 17 },
    mechanismCount: 12, relay: 'PEOM', depthRange: [0, 2],
  },
  {
    id: 'f8', index: 8, name: 'Learning & Expertise', unit: 'NDU', color: '#6366f1',
    description: 'Long-term plasticity — statistical learning, expertise enhancement, neural specialization',
    beliefCounts: { core: 4, appraisal: 8, anticipation: 2, total: 14 },
    mechanismCount: 6, relay: 'EDNR', depthRange: [0, 2],
  },
  {
    id: 'f9', index: 9, name: 'Social Cognition', unit: '\u2014', color: '#06b6d4',
    description: 'Social coordination — neural synchrony, group flow, social bonding (pure belief layer, zero mechanisms)',
    beliefCounts: { core: 2, appraisal: 6, anticipation: 2, total: 10 },
    mechanismCount: 0, relay: null, depthRange: [0, 0],
  },
]

export function getFunctionById(id: string): FunctionDef | undefined {
  return FUNCTIONS.find(f => f.id === id)
}
