/* ── M³ — My Musical Mind Types ─────────────────────────────────────
 *  The learnable parameter layer that sits on top of C³.
 *  C³ = physics (universal, frozen). M³ = individual (personal, growing).
 *  ──────────────────────────────────────────────────────────────────── */

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

/* ── Birth Temperament ─────────────────────────────────────────────── */

/** Determined from first listening data. Can shift over time. */
export type M3Temperament =
  | "explorer"    // High genre diversity, low repeat
  | "deep_diver"  // Few genres, high repeat, deep engagement
  | "rhythmic"    // Tempo/rhythm-driven preferences
  | "harmonic"    // Tonal/harmonic complexity sensitive
  | "emotive";    // Strong valence/emotional response

/* ── Subscription Tiers ────────────────────────────────────────────── */

export type M3Tier = "free" | "basic" | "premium" | "ultimate";

/* ── Presentation Layers ───────────────────────────────────────────── */

/** 3-layer depth system: same data, different reading level */
export type PresentationLayer = "surface" | "narrative" | "deep";

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
  stage: M3Stage;
  temperament: M3Temperament;
  tier: M3Tier;
  bornAt: string;               // ISO date
  lastUpdated: string | null;   // ISO date of last parameter update
  totalListens: number;         // Lifetime listen count
  parameters: M3Parameters;
  activeFunctions: number[];    // Which F1-F9 are "awake" (e.g. [1, 5, 6])
  stageProgress: number;        // 0-1 toward next stage
  frozen: boolean;              // true for free tier after birth
}

/* ── Milestones ────────────────────────────────────────────────────── */

export type M3MilestoneType =
  | "birth"
  | "stage_up"
  | "temperament_shift"
  | "function_unlock"
  | "insight";

export interface M3Milestone {
  type: M3MilestoneType;
  timestamp: string;            // ISO date
  stage?: M3Stage;
  detail: string;               // i18n key or pre-rendered text
}

/* ── Observations ──────────────────────────────────────────────────── */

/**
 * M³ output following the "observe, don't judge" language policy.
 * M³ NEVER says "you are X". It describes its own state or reports data.
 */
export interface M3Observation {
  id: string;
  layer: PresentationLayer;
  text: string;                 // The observation text (i18n-resolved)
  belief?: string;              // Related belief domain (optional)
  intensity: number;            // 0-1 significance
  functionSource?: number;      // Which F (1-9) generated this
}

/* ── Track Features (for feeding M³) ──────────────────────────────── */

/** Extended track features used to update M³ parameters */
export interface M3TrackSignal {
  energy: number;               // 0-1
  valence: number;              // 0-1
  tempo: number;                // BPM
  danceability: number;         // 0-1
  acousticness: number;         // 0-1
  harmonicComplexity: number;   // 0-1 (new for M³)
  timbralBrightness: number;    // 0-1 (new for M³)
  duration: number;             // seconds listened
  isRepeat: boolean;            // heard before?
  wasSkipped: boolean;          // skipped early?
}
