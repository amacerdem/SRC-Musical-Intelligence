/** F1–F9 Function Metadata for UI rendering */

export interface FunctionMeta {
  id: string
  index: number
  name: string
  unit: string
  color: string
  description: string
}

export const FUNCTIONS: Record<string, FunctionMeta> = {
  f1: { id: 'f1', index: 1, name: 'Sensory Processing', unit: 'SPU', color: '#3b82f6', description: 'Primary auditory encoding — spectral, harmonic, and timbral feature extraction from cochlear input' },
  f2: { id: 'f2', index: 2, name: 'Pattern Recognition & Prediction', unit: 'PCU', color: '#8b5cf6', description: 'Hierarchical temporal prediction — sequence matching, information content, precision-weighted surprise' },
  f3: { id: 'f3', index: 3, name: 'Attention & Salience', unit: 'ASU', color: '#f97316', description: 'Selective attention and salience computation — beat entrainment, novelty detection, precision weighting' },
  f4: { id: 'f4', index: 4, name: 'Memory & Retrieval', unit: 'IMU', color: '#14b8a6', description: 'Episodic and autobiographical memory — familiarity, emotional coloring, nostalgia, hippocampal binding' },
  f5: { id: 'f5', index: 5, name: 'Emotion', unit: 'ARU', color: '#ec4899', description: 'Affective evaluation — arousal, valence, mode detection, nostalgia-affect circuit' },
  f6: { id: 'f6', index: 6, name: 'Reward & Motivation', unit: 'RPU', color: '#f59e0b', description: 'Dopaminergic reward — wanting/liking/pleasure, prediction error, tension-resolution dynamics' },
  f7: { id: 'f7', index: 7, name: 'Motor & Timing', unit: 'MPU', color: '#22c55e', description: 'Sensorimotor coupling — period entrainment, groove, hierarchical context encoding, timing precision' },
  f8: { id: 'f8', index: 8, name: 'Learning & Expertise', unit: 'NDU', color: '#6366f1', description: 'Long-term plasticity — statistical learning, expertise enhancement, neural specialization' },
  f9: { id: 'f9', index: 9, name: 'Social Cognition', unit: '—', color: '#06b6d4', description: 'Social coordination — neural synchrony, group flow, social bonding (pure belief layer, zero mechanisms)' },
} as const

export const FUNCTION_IDS = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9'] as const
export type FunctionId = (typeof FUNCTION_IDS)[number]

export function getFunctionColor(fId: string): string {
  return FUNCTIONS[fId]?.color ?? '#888888'
}
