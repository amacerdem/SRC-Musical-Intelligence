/* ── Dimension Types — Hierarchical 131 → 24 → 12 → 6 ────────────
 *  Binary tree structure mapping C³ beliefs to user-facing dimensions.
 *  Three tiers: Psychology (6D, free) → Cognition (12D, basic) →
 *  Neuroscience (24D, premium) → Research (131D, ultimate).
 *
 *  Source of truth: Musical_Intelligence/brain/dimensions/
 *  Vocabulary spec: Docs/L³/M3-LOGOS.md
 *  ──────────────────────────────────────────────────────────────── */

/** The three user-facing dimension layers + raw research layer */
export type DimensionLayer = "psychology" | "cognition" | "neuroscience" | "research";

/** A single node in the dimension hierarchy */
export interface DimensionNode {
  /** Position within its layer tensor (0-based) */
  index: number;
  /** Machine key (e.g. "discovery", "expectancy", "predictive_processing") */
  key: string;
  /** English display name */
  name: string;
  /** Turkish display name */
  nameTr: string;
  /** Which layer this node belongs to */
  layer: DimensionLayer;
  /** Parent node key (null for 6D roots) */
  parentKey: string | null;
  /** Which of the 131 belief indices aggregate into this node */
  beliefIndices: number[];
}

/** 6D radar profile — one value per psychology dimension */
export interface DimensionProfile {
  discovery: number;    // 0-1 — Keşif
  intensity: number;    // 0-1 — Yoğunluk
  flow: number;         // 0-1 — Akış
  depth: number;        // 0-1 — Derinlik
  trace: number;        // 0-1 — İz
  sharing: number;      // 0-1 — Paylaşım
}

export const DIMENSION_KEYS_6D = [
  "discovery", "intensity", "flow", "depth", "trace", "sharing",
] as const;

export type DimensionKey6D = (typeof DIMENSION_KEYS_6D)[number];

/** Tier → which dimension layers are visible */
export const TIER_DIMENSION_ACCESS: Record<string, DimensionLayer[]> = {
  free:     ["psychology"],
  basic:    ["psychology", "cognition"],
  premium:  ["psychology", "cognition", "neuroscience"],
  ultimate: ["psychology", "cognition", "neuroscience", "research"],
};

/** Computed dimension state at a given moment */
export interface DimensionState {
  /** 6D psychology values (always available) */
  psychology: number[];   // length 6
  /** 12D music cognition values (basic+) */
  cognition: number[];    // length 12
  /** 24D neuroscience values (premium+) */
  neuroscience: number[]; // length 24
}
