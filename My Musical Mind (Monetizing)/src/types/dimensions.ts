/* ── Dimension Types — Hierarchical 6D → 12D → 24D ───────────────
 *  Binary tree: 6 Psychology → 12 Cognition → 24 Neuroscience.
 *  Each leaf (24D) aggregates 5-7 beliefs by mean.
 *  Parents = mean of their 2 children.
 *
 *  6D:  Discovery, Intensity, Flow, Depth, Trace, Sharing
 *  12D: 2 children per 6D parent
 *  24D: 2 children per 12D parent
 *
 *  Source of truth: Musical_Intelligence/brain/dimensions/tree.py
 *  ──────────────────────────────────────────────────────────────── */

/** The three user-facing dimension layers + raw research layer */
export type DimensionLayer = "psychology" | "cognition" | "neuroscience" | "research";

/** 6D radar profile — one value per psychology dimension */
export interface DimensionProfile {
  discovery: number;    // 0-1 — Keşif
  intensity: number;    // 0-1 — Gerilim
  flow: number;         // 0-1 — Ritim
  depth: number;        // 0-1 — Duygu
  trace: number;        // 0-1 — Hafıza
  sharing: number;      // 0-1 — Bağ
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
