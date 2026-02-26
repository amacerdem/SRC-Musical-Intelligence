/* ── M³ — My Musical Mind Types ─────────────────────────────────────
 *  The learnable parameter layer that sits on top of C³.
 *  C³ = physics (universal, frozen). M³ = individual (personal, growing).
 *  M³ growth IS persona evolution — not a parallel system.
 *  5 Mind Genes (Entropy, Resolution, Tension, Resonance, Plasticity)
 *  determine your Mind Type. Each learning session shifts all 5 genes.
 *  ──────────────────────────────────────────────────────────────────── */

import type { NeuralFamily } from "./mind";
export type { NeuralFamily } from "./mind";
export type { DimensionLayer, DimensionProfile, DimensionState } from "./dimensions";

/* ── Growth Stages (Human Development) ─────────────────────────────── */

/** 7 developmental stages, following human neurodevelopment */
export type M3Stage =
  | "embryo"      // Born — no functions active
  | "newborn"     // F1 (Sensory) awakens
  | "infant"      // +F5 (Emotion) +F6 (Reward)
  | "toddler"     // +F2 (Prediction) +F4 (Memory)
  | "child"       // +F3 (Attention) +F7 (Motor)
  | "adolescent"  // +F8 (Learning) +F9 (Social)
  | "adult";      // Full consciousness + meta-awareness

export const M3_STAGE_ORDER: M3Stage[] = [
  "embryo", "newborn", "infant", "toddler", "child", "adolescent", "adult",
];

/* ── Persona Level (1-12) ────────────────────────────────────────── */

/** 12 evolution levels from embryo to sage */
export type PersonaLevel = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

/** Maps persona level → M³ stage */
export function levelToStage(level: PersonaLevel): M3Stage {
  if (level <= 1) return "embryo";     // L1: Embryonic Mind
  if (level <= 2) return "newborn";    // L2: Newborn Mind
  if (level <= 4) return "infant";     // L3-4: Infant/Toddler Mind
  if (level <= 6) return "toddler";    // L5-6: Child/Tween Mind
  if (level <= 8) return "child";      // L7-8: Teen/Young Mind
  if (level <= 10) return "adolescent"; // L9-10: Adult/Master Mind
  return "adult";                       // L11-12: Elder/Sage Mind
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

/* ── Mind Genes ────────────────────────────────────────────────────── */

/** 5 genes that define the mind's DNA. Updated on every learning session. */
export interface MindGenes {
  entropy: number;      // 0-1 — Explorers gene (chaos/novelty)
  resolution: number;   // 0-1 — Architects gene (structure/order)
  tension: number;      // 0-1 — Alchemists gene (transformation/intensity)
  resonance: number;    // 0-1 — Anchors gene (connection/emotion)
  plasticity: number;   // 0-1 — Kineticists gene (adaptability/rhythm)
}

export const GENE_NAMES = ["entropy", "resolution", "tension", "resonance", "plasticity"] as const;
export type GeneName = (typeof GENE_NAMES)[number];

export const DEFAULT_GENES: MindGenes = {
  entropy: 0.2,
  resolution: 0.2,
  tension: 0.2,
  resonance: 0.2,
  plasticity: 0.2,
};

/** Maps each gene to its associated Mind Type */
export const GENE_TO_TYPE: Record<GeneName, NeuralFamily> = {
  entropy: "Explorers",
  resolution: "Architects",
  tension: "Alchemists",
  resonance: "Anchors",
  plasticity: "Kineticists",
};

/** Maps each Mind Type back to its dominant gene */
export const TYPE_TO_GENE: Record<NeuralFamily, GeneName> = {
  Explorers: "entropy",
  Architects: "resolution",
  Alchemists: "tension",
  Anchors: "resonance",
  Kineticists: "plasticity",
};

/** Gene colors (matches Mind Type colors) */
export const GENE_COLORS: Record<GeneName, string> = {
  entropy: "#84CC16",     // Explorers — Lime/Neon
  resolution: "#38BDF8",  // Architects — Sky blue
  tension: "#A855F7",     // Alchemists — Purple
  resonance: "#FBBF24",   // Anchors — Amber
  plasticity: "#EF4444",  // Kineticists — Red
};

/** Get the dominant Mind Type from genes */
export function getDominantType(genes: MindGenes): NeuralFamily {
  let maxGene: GeneName = "entropy";
  let maxVal = -1;
  for (const g of GENE_NAMES) {
    if (genes[g] > maxVal) {
      maxVal = genes[g];
      maxGene = g;
    }
  }
  return GENE_TO_TYPE[maxGene];
}

/** Get the dominant gene name */
export function getDominantGene(genes: MindGenes): GeneName {
  let maxGene: GeneName = "entropy";
  let maxVal = -1;
  for (const g of GENE_NAMES) {
    if (genes[g] > maxVal) {
      maxVal = genes[g];
      maxGene = g;
    }
  }
  return maxGene;
}

/** Convert genes to FamilyAffinity format for backward compat */
export function genesToAffinity(genes: MindGenes): FamilyAffinity {
  return {
    Explorers: genes.entropy,
    Architects: genes.resolution,
    Alchemists: genes.tension,
    Anchors: genes.resonance,
    Kineticists: genes.plasticity,
  };
}

/* ── Family Affinity (backward compat) ─────────────────────────────── */

/** Per-family affinity scores — derived from genes */
export type FamilyAffinity = Record<NeuralFamily, number>;

/** All 5 families in order */
export const FAMILY_NAMES: NeuralFamily[] = [
  "Alchemists", "Architects", "Explorers", "Anchors", "Kineticists",
];

/* ── Family Morphology ───────────────────────────────────────────── */

/** Visual style of the organism canvas per Mind Type */
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

/* ── Observation Types ─────────────────────────────────────────────── */

/** Stage-gated observation categories */
export type ObservationType =
  | "mood_landscape"          // Level 2+ (Newborn)
  | "daily_reflection"        // Level 3+ (Infant)
  | "pattern_discovery"       // Level 5+ (Toddler)
  | "music_recommendation"    // Level 5+ (Toddler)
  | "predictive_insight"      // Level 7+ (Child)
  | "therapeutic_observation" // Level 7+ (Child)
  | "musical_counseling"      // Level 9+ (Adolescent)
  | "cross_m3_insight"        // Level 9+ (Adolescent)
  | "meta_awareness";         // Level 11+ (Adult)

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

  /* Mind Genes + Persona */
  genes: MindGenes;               // 5 genes, updated on every learning
  activePersonaId: number;        // Derived from genes
  previousPersonaIds: number[];   // History of persona shifts

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
  | "type_change"
  | "insight";

export interface M3Milestone {
  type: M3MilestoneType;
  timestamp: string;
  stage?: M3Stage;
  level?: PersonaLevel;
  fromPersonaId?: number;
  toPersonaId?: number;
  fromType?: NeuralFamily;
  toType?: NeuralFamily;
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

/* ── Track Features (for learning) ─────────────────────────────────── */

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
