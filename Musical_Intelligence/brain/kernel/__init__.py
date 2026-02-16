"""C³ Belief Kernel — minimal predictive coding engine.

Implements the 5-belief architecture from C3-ARCHITECTURE-RFC v1.0.0:
  Phase 0: perceived_consonance, tempo_state  (sensory)
  Phase 1: salience_state                     (gate)
  Phase 2a: familiarity_state                 (recognize)
  Phase 2b: PE + precision                    (meta)
  Phase 3: reward_valence                     (value)

All R³ access goes through the semantic FeatureRegistry.
No numeric indices. No dissolved group access.
"""
