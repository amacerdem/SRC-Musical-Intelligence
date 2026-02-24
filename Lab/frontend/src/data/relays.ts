/** MI-Lab Static Registry: 9 C³ Relays (one per processing unit) */

export interface RelayDimDef {
  name: string
  layer: 'E' | 'M' | 'P' | 'F' | 'N+C' | 'T+M'
  visibility: 'internal' | 'hybrid' | 'external'
}

export interface RelayDef {
  name: string
  fullName: string
  functionId: string
  unit: string
  outputDim: number
  dims: RelayDimDef[]
}

export const RELAYS: RelayDef[] = [
  {
    name: 'BCH', fullName: 'Brainstem Consonance Hierarchy', functionId: 'f1', unit: 'SPU', outputDim: 16,
    dims: [
      { name: 'salience_activation', layer: 'E', visibility: 'internal' },
      { name: 'sensory_evidence', layer: 'E', visibility: 'internal' },
      { name: 'hierarchy', layer: 'E', visibility: 'internal' },
      { name: 'consonance_core', layer: 'E', visibility: 'internal' },
      { name: 'roughness_memory', layer: 'M', visibility: 'internal' },
      { name: 'brightness_memory', layer: 'M', visibility: 'internal' },
      { name: 'harmonic_memory', layer: 'M', visibility: 'internal' },
      { name: 'spectral_memory', layer: 'M', visibility: 'internal' },
      { name: 'consonance_signal', layer: 'P', visibility: 'hybrid' },
      { name: 'template_match', layer: 'P', visibility: 'hybrid' },
      { name: 'stability_index', layer: 'P', visibility: 'hybrid' },
      { name: 'binding_strength', layer: 'P', visibility: 'hybrid' },
      { name: 'consonance_forecast', layer: 'F', visibility: 'external' },
      { name: 'harmonic_forecast', layer: 'F', visibility: 'external' },
      { name: 'template_forecast', layer: 'F', visibility: 'external' },
      { name: 'trend_fc', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'HTP', fullName: 'Hierarchical Temporal Prediction', functionId: 'f2', unit: 'PCU', outputDim: 12,
    dims: [
      { name: 'high_level_lead', layer: 'E', visibility: 'internal' },
      { name: 'mid_level_lead', layer: 'E', visibility: 'internal' },
      { name: 'low_level_lead', layer: 'E', visibility: 'internal' },
      { name: 'hierarchy_gradient', layer: 'E', visibility: 'internal' },
      { name: 'match_history', layer: 'M', visibility: 'internal' },
      { name: 'prediction_stability', layer: 'M', visibility: 'internal' },
      { name: 'error_magnitude', layer: 'M', visibility: 'internal' },
      { name: 'sensory_match', layer: 'P', visibility: 'hybrid' },
      { name: 'pitch_prediction', layer: 'P', visibility: 'hybrid' },
      { name: 'abstract_prediction', layer: 'P', visibility: 'hybrid' },
      { name: 'abstract_future_500ms', layer: 'F', visibility: 'external' },
      { name: 'midlevel_future_200ms', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'SNEM', fullName: 'Sensory Novelty & Expectation Model', functionId: 'f3', unit: 'ASU', outputDim: 12,
    dims: [
      { name: 'beat_entrainment', layer: 'E', visibility: 'internal' },
      { name: 'meter_entrainment', layer: 'E', visibility: 'internal' },
      { name: 'selective_enhancement', layer: 'E', visibility: 'internal' },
      { name: 'ssep_enhancement', layer: 'M', visibility: 'internal' },
      { name: 'enhancement_index', layer: 'M', visibility: 'internal' },
      { name: 'beat_salience', layer: 'M', visibility: 'internal' },
      { name: 'beat_locked_activity', layer: 'P', visibility: 'hybrid' },
      { name: 'entrainment_strength', layer: 'P', visibility: 'hybrid' },
      { name: 'selective_gain', layer: 'P', visibility: 'hybrid' },
      { name: 'beat_onset_pred', layer: 'F', visibility: 'external' },
      { name: 'meter_position_pred', layer: 'F', visibility: 'external' },
      { name: 'enhancement_pred', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'MEAMN', fullName: 'Music-Evoked Autobiographical Memory Network', functionId: 'f4', unit: 'IMU', outputDim: 12,
    dims: [
      { name: 'f01_retrieval', layer: 'E', visibility: 'internal' },
      { name: 'f02_nostalgia', layer: 'E', visibility: 'internal' },
      { name: 'f03_emotion', layer: 'E', visibility: 'internal' },
      { name: 'meam_retrieval', layer: 'M', visibility: 'internal' },
      { name: 'p_recall', layer: 'M', visibility: 'internal' },
      { name: 'memory_state', layer: 'P', visibility: 'hybrid' },
      { name: 'emotional_color', layer: 'P', visibility: 'hybrid' },
      { name: 'nostalgia_link', layer: 'P', visibility: 'hybrid' },
      { name: 'mem_vividness_fc', layer: 'F', visibility: 'external' },
      { name: 'emo_response_fc', layer: 'F', visibility: 'external' },
      { name: 'self_ref_fc', layer: 'F', visibility: 'external' },
      { name: 'reserved', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'SRP', fullName: 'Salience-Reward Pathway', functionId: 'f5', unit: 'ARU', outputDim: 19,
    dims: [
      { name: 'da_caudate', layer: 'N+C', visibility: 'internal' },
      { name: 'da_nacc', layer: 'N+C', visibility: 'internal' },
      { name: 'opioid_proxy', layer: 'N+C', visibility: 'internal' },
      { name: 'vta_drive', layer: 'N+C', visibility: 'internal' },
      { name: 'stg_nacc_coupling', layer: 'N+C', visibility: 'internal' },
      { name: 'prediction_error', layer: 'N+C', visibility: 'internal' },
      { name: 'tension', layer: 'T+M', visibility: 'internal' },
      { name: 'prediction_match', layer: 'T+M', visibility: 'internal' },
      { name: 'reaction', layer: 'T+M', visibility: 'internal' },
      { name: 'appraisal', layer: 'T+M', visibility: 'internal' },
      { name: 'harmonic_tension', layer: 'T+M', visibility: 'internal' },
      { name: 'dynamic_intensity', layer: 'T+M', visibility: 'internal' },
      { name: 'peak_detection', layer: 'T+M', visibility: 'internal' },
      { name: 'wanting', layer: 'P', visibility: 'hybrid' },
      { name: 'liking', layer: 'P', visibility: 'hybrid' },
      { name: 'pleasure', layer: 'P', visibility: 'hybrid' },
      { name: 'reward_forecast', layer: 'F', visibility: 'external' },
      { name: 'chills_proximity', layer: 'F', visibility: 'external' },
      { name: 'resolution_expect', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'DAED', fullName: 'Dopamine Anticipation-Experience Dissociation', functionId: 'f6', unit: 'RPU', outputDim: 8,
    dims: [
      { name: 'anticipatory_da', layer: 'E', visibility: 'internal' },
      { name: 'consummatory_da', layer: 'E', visibility: 'internal' },
      { name: 'wanting_index', layer: 'E', visibility: 'internal' },
      { name: 'liking_index', layer: 'E', visibility: 'internal' },
      { name: 'dissociation_index', layer: 'M', visibility: 'internal' },
      { name: 'temporal_phase', layer: 'M', visibility: 'internal' },
      { name: 'caudate_activation', layer: 'P', visibility: 'hybrid' },
      { name: 'nacc_activation', layer: 'P', visibility: 'hybrid' },
    ],
  },
  {
    name: 'PEOM', fullName: 'Period Entrainment Optimization Model', functionId: 'f7', unit: 'MPU', outputDim: 11,
    dims: [
      { name: 'period_entrainment', layer: 'E', visibility: 'internal' },
      { name: 'velocity_optimization', layer: 'E', visibility: 'internal' },
      { name: 'variability_reduction', layer: 'E', visibility: 'internal' },
      { name: 'motor_period', layer: 'M', visibility: 'internal' },
      { name: 'velocity', layer: 'M', visibility: 'internal' },
      { name: 'acceleration', layer: 'M', visibility: 'internal' },
      { name: 'cv_reduction', layer: 'M', visibility: 'internal' },
      { name: 'period_lock_strength', layer: 'P', visibility: 'hybrid' },
      { name: 'kinematic_smoothness', layer: 'P', visibility: 'hybrid' },
      { name: 'next_beat_pred_T', layer: 'F', visibility: 'external' },
      { name: 'velocity_profile_pred', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'HMCE', fullName: 'Hierarchical Musical Context Encoding', functionId: 'f7', unit: 'STU', outputDim: 11,
    dims: [
      { name: 'short_context', layer: 'E', visibility: 'internal' },
      { name: 'medium_context', layer: 'E', visibility: 'internal' },
      { name: 'long_context', layer: 'E', visibility: 'internal' },
      { name: 'context_depth', layer: 'M', visibility: 'internal' },
      { name: 'structure_regularity', layer: 'M', visibility: 'internal' },
      { name: 'transition_dynamics', layer: 'M', visibility: 'internal' },
      { name: 'a1_stg_encoding', layer: 'P', visibility: 'hybrid' },
      { name: 'context_predict', layer: 'P', visibility: 'hybrid' },
      { name: 'phrase_expect', layer: 'P', visibility: 'hybrid' },
      { name: 'phrase_boundary_pred', layer: 'F', visibility: 'external' },
      { name: 'structure_pred', layer: 'F', visibility: 'external' },
    ],
  },
  {
    name: 'EDNR', fullName: 'Error-Driven Neural Refinement', functionId: 'f8', unit: 'NDU', outputDim: 10,
    dims: [
      { name: 'network_specialization', layer: 'E', visibility: 'internal' },
      { name: 'within_connectivity', layer: 'E', visibility: 'internal' },
      { name: 'between_connectivity', layer: 'E', visibility: 'internal' },
      { name: 'plasticity_rate', layer: 'M', visibility: 'internal' },
      { name: 'efficiency_gain', layer: 'M', visibility: 'internal' },
      { name: 'consolidation_index', layer: 'M', visibility: 'internal' },
      { name: 'current_expertise', layer: 'P', visibility: 'hybrid' },
      { name: 'learning_trajectory', layer: 'P', visibility: 'hybrid' },
      { name: 'expertise_forecast', layer: 'F', visibility: 'external' },
      { name: 'efficiency_forecast', layer: 'F', visibility: 'external' },
    ],
  },
]

export function getRelayByFunction(fId: string): RelayDef | undefined {
  return RELAYS.find(r => r.functionId === fId)
}

export function getRelayByName(name: string): RelayDef | undefined {
  return RELAYS.find(r => r.name === name)
}
