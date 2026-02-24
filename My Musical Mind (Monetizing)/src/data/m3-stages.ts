/* ── M³ Growth Stages, Temperaments & Tiers ────────────────────────
 *  Constants for the M³ developmental system.
 *  Stages follow real neurodevelopment: sensory → reward/emotion →
 *  prediction/memory → attention/motor → learning/social → meta.
 *  ──────────────────────────────────────────────────────────────── */

import type { M3Stage, M3Temperament, M3Tier } from "@/types/m3";

/* ── Stage Definitions ─────────────────────────────────────────── */

export interface StageDefinition {
  key: M3Stage;
  functions: number[];         // Which F1-F9 are active
  threshold: number;           // Total listens to reach this stage
  organismStage: 1 | 2 | 3;   // Maps to MindOrganismCanvas stage
  color: string;
  icon: string;                // Emoji/symbol
}

export const M3_STAGES: Record<M3Stage, StageDefinition> = {
  seed: {
    key: "seed",
    functions: [],
    threshold: 0,
    organismStage: 1,
    color: "#94A3B8",
    icon: "◦",
  },
  sprout: {
    key: "sprout",
    functions: [1],               // F1 Sensory
    threshold: 10,
    organismStage: 1,
    color: "#84CC16",
    icon: "⌇",
  },
  sapling: {
    key: "sapling",
    functions: [1, 5, 6],         // +F5 Emotion, +F6 Reward
    threshold: 50,
    organismStage: 1,
    color: "#22D3EE",
    icon: "⌘",
  },
  branch: {
    key: "branch",
    functions: [1, 2, 4, 5, 6],   // +F2 Prediction, +F4 Memory
    threshold: 150,
    organismStage: 2,
    color: "#A855F7",
    icon: "⊛",
  },
  bloom: {
    key: "bloom",
    functions: [1, 2, 3, 4, 5, 6, 7], // +F3 Attention, +F7 Motor
    threshold: 400,
    organismStage: 2,
    color: "#EC4899",
    icon: "✦",
  },
  canopy: {
    key: "canopy",
    functions: [1, 2, 3, 4, 5, 6, 7, 8, 9], // +F8 Learning, +F9 Social
    threshold: 1000,
    organismStage: 3,
    color: "#FBBF24",
    icon: "◈",
  },
  ancient: {
    key: "ancient",
    functions: [1, 2, 3, 4, 5, 6, 7, 8, 9], // All + meta-awareness
    threshold: 3000,
    organismStage: 3,
    color: "#F1F5F9",
    icon: "⬡",
  },
};

/** Ordered stage keys for progression lookups */
export const STAGE_ORDER: M3Stage[] = [
  "seed", "sprout", "sapling", "branch", "bloom", "canopy", "ancient",
];

/** Get the next stage (or null if already ancient) */
export function getNextStage(current: M3Stage): M3Stage | null {
  const idx = STAGE_ORDER.indexOf(current);
  return idx < STAGE_ORDER.length - 1 ? STAGE_ORDER[idx + 1] : null;
}

/** Get listen threshold for the next stage */
export function getNextThreshold(current: M3Stage): number {
  const next = getNextStage(current);
  return next ? M3_STAGES[next].threshold : Infinity;
}

/* ── C³ Function Metadata ──────────────────────────────────────── */

export interface FunctionMeta {
  id: number;
  abbr: string;
  color: string;
}

export const C3_FUNCTIONS: FunctionMeta[] = [
  { id: 1, abbr: "F1", color: "#C084FC" },  // Sensory — purple
  { id: 2, abbr: "F2", color: "#38BDF8" },  // Prediction — sky
  { id: 3, abbr: "F3", color: "#84CC16" },  // Attention — lime
  { id: 4, abbr: "F4", color: "#F472B6" },  // Memory — pink
  { id: 5, abbr: "F5", color: "#FB923C" },  // Emotion — orange
  { id: 6, abbr: "F6", color: "#FBBF24" },  // Reward — amber
  { id: 7, abbr: "F7", color: "#EF4444" },  // Motor — red
  { id: 8, abbr: "F8", color: "#22D3EE" },  // Learning — cyan
  { id: 9, abbr: "F9", color: "#A78BFA" },  // Social — violet
];

/* ── Temperament Definitions ───────────────────────────────────── */

export interface TemperamentDefinition {
  key: M3Temperament;
  color: string;
  icon: string;
  /** Bias multipliers applied to initial M³ parameters */
  paramBias: {
    timbral: number;     // timbralMap sensitivity
    temporal: number;    // temporalPrefs sensitivity
    reward: number;      // rewardWeights boost
    precision: number;   // precisionWeights boost
    attention: number;   // attentionBiases boost
  };
}

export const M3_TEMPERAMENTS: Record<M3Temperament, TemperamentDefinition> = {
  explorer: {
    key: "explorer",
    color: "#A3E635",
    icon: "◇",
    paramBias: { timbral: 1.2, temporal: 0.8, reward: 0.9, precision: 0.7, attention: 1.3 },
  },
  deep_diver: {
    key: "deep_diver",
    color: "#6366F1",
    icon: "◆",
    paramBias: { timbral: 0.9, temporal: 1.0, reward: 1.3, precision: 1.2, attention: 0.8 },
  },
  rhythmic: {
    key: "rhythmic",
    color: "#F97316",
    icon: "◎",
    paramBias: { timbral: 0.8, temporal: 1.4, reward: 1.0, precision: 0.9, attention: 1.0 },
  },
  harmonic: {
    key: "harmonic",
    color: "#C084FC",
    icon: "◐",
    paramBias: { timbral: 1.4, temporal: 0.9, reward: 1.1, precision: 1.1, attention: 0.8 },
  },
  emotive: {
    key: "emotive",
    color: "#FB7185",
    icon: "◉",
    paramBias: { timbral: 1.0, temporal: 0.9, reward: 1.4, precision: 0.8, attention: 1.1 },
  },
};

/* ── Tier Definitions ──────────────────────────────────────────── */

export interface TierDefinition {
  key: M3Tier;
  color: string;
  updateInterval: string | null; // null = no updates (frozen)
  features: string[];            // i18n keys for feature list
  price: number;                 // USD/month
}

export const M3_TIERS: Record<M3Tier, TierDefinition> = {
  free: {
    key: "free",
    color: "#94A3B8",
    updateInterval: null,
    features: [
      "m3.tier.free.f1",  // M³ born
      "m3.tier.free.f2",  // Surface layer only
      "m3.tier.free.f3",  // View-only profile
    ],
    price: 0,
  },
  basic: {
    key: "basic",
    color: "#22D3EE",
    updateInterval: "weekly",
    features: [
      "m3.tier.basic.f1", // Weekly growth
      "m3.tier.basic.f2", // Surface + Narrative
      "m3.tier.basic.f3", // Resonance score
    ],
    price: 9.99,
  },
  premium: {
    key: "premium",
    color: "#A855F7",
    updateInterval: "daily",
    features: [
      "m3.tier.premium.f1", // Daily growth
      "m3.tier.premium.f2", // All 3 layers
      "m3.tier.premium.f3", // Duo Mind + Garden
    ],
    price: 19.99,
  },
  ultimate: {
    key: "ultimate",
    color: "#FBBF24",
    updateInterval: "realtime",
    features: [
      "m3.tier.ultimate.f1", // Real-time growth
      "m3.tier.ultimate.f2", // All layers + API
      "m3.tier.ultimate.f3", // Full social + Echo
    ],
    price: 49.99,
  },
};
