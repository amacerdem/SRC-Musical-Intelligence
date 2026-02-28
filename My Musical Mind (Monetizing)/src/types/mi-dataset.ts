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
  };
}
