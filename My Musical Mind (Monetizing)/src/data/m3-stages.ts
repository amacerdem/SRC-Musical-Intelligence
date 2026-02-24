/* ── M³ Growth Stages & Tiers ───────────────────────────────────────
 *  Constants for the M³ developmental system.
 *  Stages follow real neurodevelopment: sensory → reward/emotion →
 *  prediction/memory → attention/motor → learning/social → meta.
 *  ──────────────────────────────────────────────────────────────── */

import type { M3Stage, M3Tier } from "@/types/m3";
import type { NeuralFamily } from "@/types/mind";

/* ── Stage Definitions ─────────────────────────────────────────── */

export interface StageDefinition {
  key: M3Stage;
  functions: number[];         // Which F1-F9 are active
  color: string;
  icon: string;
}

export const M3_STAGES: Record<M3Stage, StageDefinition> = {
  seed: {
    key: "seed",
    functions: [],
    color: "#94A3B8",
    icon: "◦",
  },
  sprout: {
    key: "sprout",
    functions: [1],
    color: "#84CC16",
    icon: "⌇",
  },
  sapling: {
    key: "sapling",
    functions: [1, 5, 6],
    color: "#22D3EE",
    icon: "⌘",
  },
  branch: {
    key: "branch",
    functions: [1, 2, 4, 5, 6],
    color: "#A855F7",
    icon: "⊛",
  },
  bloom: {
    key: "bloom",
    functions: [1, 2, 3, 4, 5, 6, 7],
    color: "#EC4899",
    icon: "✦",
  },
  canopy: {
    key: "canopy",
    functions: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    color: "#FBBF24",
    icon: "◈",
  },
  ancient: {
    key: "ancient",
    functions: [1, 2, 3, 4, 5, 6, 7, 8, 9],
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

/* ── C³ Function Metadata ──────────────────────────────────────── */

export interface FunctionMeta {
  id: number;
  abbr: string;
  name: string;
  color: string;
}

export const C3_FUNCTIONS: FunctionMeta[] = [
  { id: 1, abbr: "F1", name: "Sensory",    color: "#C084FC" },
  { id: 2, abbr: "F2", name: "Prediction", color: "#38BDF8" },
  { id: 3, abbr: "F3", name: "Attention",  color: "#84CC16" },
  { id: 4, abbr: "F4", name: "Memory",     color: "#F472B6" },
  { id: 5, abbr: "F5", name: "Emotion",    color: "#FB923C" },
  { id: 6, abbr: "F6", name: "Reward",     color: "#FBBF24" },
  { id: 7, abbr: "F7", name: "Motor",      color: "#EF4444" },
  { id: 8, abbr: "F8", name: "Learning",   color: "#22D3EE" },
  { id: 9, abbr: "F9", name: "Social",     color: "#A78BFA" },
];

/* ── Family Parameter Biases ─────────────────────────────────────
 *  Instead of temperament, initial M³ parameters are biased by
 *  the birth persona's neural family.
 *  ──────────────────────────────────────────────────────────────── */

export interface FamilyParamBias {
  timbral: number;
  temporal: number;
  reward: number;
  precision: number;
  attention: number;
}

export const FAMILY_PARAM_BIASES: Record<NeuralFamily, FamilyParamBias> = {
  Alchemists:  { timbral: 1.0, temporal: 0.9, reward: 1.4, precision: 0.8, attention: 1.1 },
  Architects:  { timbral: 1.4, temporal: 0.9, reward: 1.1, precision: 1.3, attention: 0.8 },
  Explorers:   { timbral: 1.2, temporal: 0.8, reward: 0.9, precision: 0.7, attention: 1.3 },
  Anchors:     { timbral: 0.9, temporal: 1.0, reward: 1.3, precision: 1.0, attention: 0.9 },
  Kineticists: { timbral: 0.8, temporal: 1.4, reward: 1.0, precision: 0.9, attention: 1.0 },
};

/* ── Tier Definitions ──────────────────────────────────────────── */

export interface TierDefinition {
  key: M3Tier;
  color: string;
  updateInterval: string | null;
  features: string[];
  price: number;
}

export const M3_TIERS: Record<M3Tier, TierDefinition> = {
  free: {
    key: "free",
    color: "#94A3B8",
    updateInterval: null,
    features: ["m3.tier.free.f1", "m3.tier.free.f2", "m3.tier.free.f3"],
    price: 0,
  },
  basic: {
    key: "basic",
    color: "#22D3EE",
    updateInterval: "weekly",
    features: ["m3.tier.basic.f1", "m3.tier.basic.f2", "m3.tier.basic.f3"],
    price: 9.99,
  },
  premium: {
    key: "premium",
    color: "#A855F7",
    updateInterval: "daily",
    features: ["m3.tier.premium.f1", "m3.tier.premium.f2", "m3.tier.premium.f3"],
    price: 19.99,
  },
  ultimate: {
    key: "ultimate",
    color: "#FBBF24",
    updateInterval: "realtime",
    features: ["m3.tier.ultimate.f1", "m3.tier.ultimate.f2", "m3.tier.ultimate.f3"],
    price: 49.99,
  },
};
