/* ── MI Dataset Types — matches JSON schema from generate_dataset.py ── */

/** 8 signal fields derived from C³ outputs */
export interface MISignal {
  energy: number;
  valence: number;
  tempo: number;
  danceability: number;
  acousticness: number;
  harmonicComplexity: number;
  timbralBrightness: number;
  duration: number;
}

/** 5 mind genes from MI analysis */
export interface MIGenes {
  entropy: number;
  resolution: number;
  tension: number;
  resonance: number;
  plasticity: number;
}

/** Per-track summary in catalog.json */
export interface MICatalogTrack {
  id: string;
  filename: string;
  artist: string;
  title: string;
  categories: string[];
  duration_s: number;
  signal: MISignal;
  genes: MIGenes;
  dimensions_6d: number[];
  dominant_family: string;
  dominant_gene: string;
}

/** Root catalog.json structure */
export interface MICatalog {
  version: string;
  generated: string;
  pipeline: string;
  total_tracks: number;
  categories: Record<string, number>;
  overlaps: number;
  processing_time_s: number;
  tracks: MICatalogTrack[];
}

/** Full per-track analysis (tracks/{id}.json) */
export interface MITrackDetail {
  id: string;
  filename: string;
  artist: string;
  title: string;
  categories: string[];
  duration_s: number;
  n_frames: number;
  fps: number;
  signal: MISignal;
  genes: MIGenes;
  dominant_gene: string;
  dominant_family: string;
  beliefs: {
    means: number[];   // 131
    stds: number[];    // 131
  };
  dimensions: {
    psychology_6d: number[];
    cognition_12d: number[];
    neuroscience_24d: number[];
  };
  functions: Record<string, number>; // F1-F9
  ram_26d: {
    means: number[];
    stds: number[];
  };
  neuro_4d: {
    DA: number;
    NE: number;
    OPI: number;
    "5HT": number;
  };
  temporal_profile: {
    segments: number;
    belief_means_per_segment: number[][];  // segments × 131
    neuro_per_segment?: number[][];        // segments × 4 (DA, NE, OPI, 5HT)
    ram_per_segment?: number[][];          // segments × 26
    reward_per_segment?: number[];         // segments × 1 scalar
  };
}

/* ── Full Beliefs JSON (_beliefs_full.json) ─────────────────────── */

/** Single belief entry in the full beliefs file */
export interface MIBeliefEntry {
  index: number;           // 0-130, position in 131-belief vector
  mechanism: string;       // e.g. "BCH", "CSG"
  type: string;            // "Core" | "Appraisal" | "Anticipation"
  frames: number[];        // one value per frame (n_frames length)
}

/** Function group in full beliefs file */
export interface MIFunctionBeliefs {
  beliefs: Record<string, MIBeliefEntry>;
}

/** Root structure of _beliefs_full.json */
export interface MIBeliefsFull {
  track_id: string;
  artist: string;
  title: string;
  n_frames: number;
  fps: number;
  duration_s: number;
  frame_interval_ms: number;
  functions: Record<string, MIFunctionBeliefs>;
}
