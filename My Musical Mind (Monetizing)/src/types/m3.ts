/* ── M³ — My Musical Mind Types ─────────────────────────────────────
 *  The learnable parameter layer that sits on top of C³.
 *  C³ = physics (universal, frozen). M³ = individual (personal, growing).
 *  M³ growth IS persona evolution — not a parallel system.
 *  ──────────────────────────────────────────────────────────────────── */

import type { NeuralFamily, MindAxes } from "./mind";

/* ── Growth Stages ─────────────────────────────────────────────────── */

/** 7 developmental stages, following real neurodevelopment order */
export type M3Stage =
  | "seed"     // Born — no functions active
  | "sprout"   // F1 (Sensory) awakens
  | "sapling"  // +F6 (Reward) +F5 (Emotion)
  | "branch"   // +F2 (Prediction) +F4 (Memory)
  | "bloom"    // +F3 (Attention) +F7 (Motor)
  | "canopy"   // +F8 (Learning) +F9 (Social)
  | "ancient"; // Full consciousness + meta-awareness

export const M3_STAGE_ORDER: M3Stage[] = [
  "seed", "sprout", "sapling", "branch", "bloom", "canopy", "ancient",
];

/* ── Persona Level (1-12) ────────────────────────────────────────── */

/** 12 evolution levels from birth to maturity */
export type PersonaLevel = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

/** Maps persona level → M³ stage */
export function levelToStage(level: PersonaLevel): M3Stage {
  if (level <= 1) return "seed";
  if (level <= 2) return "sprout";
  if (level <= 4) return "sapling";
  if (level <= 6) return "branch";
  if (level <= 8) return "bloom";
  if (level <= 10) return "canopy";
  return "ancient";
}

/** Maps persona level → organism canvas stage (1-3) */
export function levelToOrganismStage(level: PersonaLevel): 1 | 2 | 3 {
  if (level <= 4) return 1;
  if (level <= 8) return 2;
  return 3;
}

/** Listen thresholds to reach each level */
export const LEVEL_THRESHOLDS: Record<PersonaLevel, number> = {
  1: 0, 2: 10, 3: 30, 4: 60, 5: 100, 6: 170,
  7: 270, 8: 400, 9: 600, 10: 900, 11: 1400, 12: 2200,
};

/* ── Family Affinity ─────────────────────────────────────────────── */

/** Per-family affinity scores (0-1 each). Updated on every listen. */
export type FamilyAffinity = Record<NeuralFamily, number>;

/** Default affinity for all families */
export const DEFAULT_FAMILY_AFFINITY: FamilyAffinity = {
  Architects: 0.1,
  Alchemists: 0.1,
  Explorers: 0.1,
  Anchors: 0.1,
  Kineticists: 0.1,
};

/** All 5 families in order */
export const FAMILY_NAMES: NeuralFamily[] = [
  "Alchemists", "Architects", "Explorers", "Anchors", "Kineticists",
];

/* ── Family Morphology ───────────────────────────────────────────── */

/** Visual style of the organism canvas per family */
export type FamilyMorphology =
  | "volatile"     // Alchemists — jagged, electric, flickering
  | "crystalline"  // Architects — geometric, angular, structured
  | "fluid"        // Explorers — chaotic, morphing, amoeba
  | "organic"      // Anchors — smooth, warm, clustered
  | "rhythmic";    // Kineticists — pulsing, orbital, beating

export const FAMILY_MORPHOLOGY: Record<NeuralFamily, FamilyMorphology> = {
  Alchemists: "volatile",
  Architects: "crystalline",
  Explorers: "fluid",
  Anchors: "organic",
  Kineticists: "rhythmic",
};

/* ── Subscription Tiers ────────────────────────────────────────────── */

export type M3Tier = "free" | "basic" | "premium" | "ultimate";

/* ── Presentation Layers ───────────────────────────────────────────── */

/** 3-layer depth system: same data, different reading level */
export type PresentationLayer = "surface" | "narrative" | "deep";

/* ── Observation Types (M3-SPEC §5.2) ────────────────────────────── */

/** Stage-gated observation categories */
export type ObservationType =
  | "mood_landscape"          // Level 2+ (Sprout)
  | "daily_reflection"        // Level 3+ (Sapling)
  | "pattern_discovery"       // Level 5+ (Branch)
  | "music_recommendation"    // Level 5+ (Branch)
  | "predictive_insight"      // Level 7+ (Bloom)
  | "therapeutic_observation" // Level 7+ (Bloom)
  | "musical_counseling"      // Level 9+ (Canopy)
  | "cross_m3_insight"        // Level 9+ (Canopy)
  | "meta_awareness";         // Level 11+ (Ancient)

/** Minimum persona level required for each observation type */
export const OBSERVATION_LEVEL_GATE: Record<ObservationType, PersonaLevel> = {
  mood_landscape: 2,
  daily_reflection: 3,
  pattern_discovery: 5,
  music_recommendation: 5,
  predictive_insight: 7,
  therapeutic_observation: 7,
  musical_counseling: 9,
  cross_m3_insight: 9,
  meta_awareness: 11,
};

/* ── M³ Parameters ─────────────────────────────────────────────────── */

/** ~1,295 floats per user — the learnable "synaptic weights" */
export interface M3Parameters {
  beliefPriors: number[];        // 131 — each belief's personal baseline
  precisionWeights: number[];    // 131 — what the user is sensitive to
  rewardWeights: number[];       // 131 — personal pleasure/displeasure map
  predictionCoeffs: number[];    // 524 (131×4: τ, w_trend, w_period, w_ctx)
  attentionBiases: number[];     // 131 — where attention naturally falls
  temporalPrefs: number[];       //  50 — tempo, rhythm, timing profile
  timbralMap: number[];          //  97 — sensitivity per R³ dimension
  crossCorrelations: number[];   // 100 — personal belief interactions
}

/** Total float count across all parameter groups */
export const M3_PARAM_COUNT = 131 + 131 + 131 + 524 + 131 + 50 + 97 + 100; // = 1,295

/* ── M³ State ──────────────────────────────────────────────────────── */

/** The complete state of a user's Musical Mind */
export interface M3Mind {
  /* Growth */
  stage: M3Stage;
  level: PersonaLevel;            // 1-12
  stageProgress: number;          // 0-1 toward next level
  totalListens: number;
  totalMinutes: number;

  /* Persona integration */
  familyAffinity: FamilyAffinity; // Updated on every listen
  activePersonaId: number;        // Derived from affinity × axes
  previousPersonaIds: number[];   // History of persona shifts
  axes: MindAxes;                 // Live evolving axes

  /* Parameters */
  parameters: M3Parameters;
  activeFunctions: number[];      // Which F1-F9 are "awake"

  /* Subscription */
  tier: M3Tier;
  frozen: boolean;                // true for free tier after birth

  /* Timestamps */
  bornAt: string;                 // ISO date
  lastUpdated: string | null;
}

/* ── Milestones ────────────────────────────────────────────────────── */

export type M3MilestoneType =
  | "birth"
  | "level_up"
  | "stage_up"
  | "persona_shift"
  | "function_unlock"
  | "insight";

export interface M3Milestone {
  type: M3MilestoneType;
  timestamp: string;
  stage?: M3Stage;
  level?: PersonaLevel;
  fromPersonaId?: number;
  toPersonaId?: number;
  detail: string;
}

/* ── Observations ──────────────────────────────────────────────────── */

/**
 * M³ output following the "observe, don't judge" language policy.
 * M³ NEVER says "you are X". It describes its own state or reports data.
 */
export interface M3Observation {
  id: string;
  type: ObservationType;
  layer: PresentationLayer;
  text: string;
  belief?: string;
  intensity: number;              // 0-1
  functionSource?: number;        // Which F (1-9) generated this
  neuroChem?: "DA" | "NE" | "OPI" | "5HT";
}

/* ── Track Features (for feeding M³) ──────────────────────────────── */

/** Extended track features used to update M³ parameters */
export interface M3TrackSignal {
  energy: number;
  valence: number;
  tempo: number;
  danceability: number;
  acousticness: number;
  harmonicComplexity: number;
  timbralBrightness: number;
  duration: number;
  isRepeat: boolean;
  wasSkipped: boolean;
}
