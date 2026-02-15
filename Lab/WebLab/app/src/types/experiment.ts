/** Experiment metadata from meta.json */
export interface ExperimentMeta {
  slug: string;
  title: string;
  duration_s: number;
  total_frames: number;
  lod_frames: number;
  lod_stride: number;
  frame_rate: number;
  nuclei: string[];
  r3_dim: number;
  created_at: string;
}

/** Per-nucleus layer structure */
export interface LayerInfo {
  code: string;
  name: string;
  start: number;
  end: number;
  scope: "internal" | "external" | "hybrid";
  dim_names: string[];
}

/** RegionLink metadata */
export interface RegionLinkInfo {
  dim_name: string;
  region: string;
  weight: number;
  citation: string;
}

/** NeuroLink metadata */
export interface NeuroLinkInfo {
  dim_name: string;
  channel: number;
  channel_name: string;
  effect: "produce" | "amplify" | "inhibit";
  weight: number;
  citation: string;
}

/** H³ demand spec */
export interface H3DemandInfo {
  r3_idx: number;
  r3_name: string;
  horizon: number;
  horizon_label: string;
  morph: number;
  morph_name: string;
  law: number;
  law_name: string;
  purpose: string;
  citation: string;
}

/** Citation entry */
export interface CitationInfo {
  author: string;
  year: number;
  finding: string;
  effect_size: string;
}

/** Nucleus evidence metadata */
export interface NucleusMetadata {
  evidence_tier: "alpha" | "beta" | "gamma";
  confidence_range: [number, number];
  version: string;
  paper_count: number;
  citations: CitationInfo[];
  falsification_criteria: string[];
}

/** Full per-nucleus data (from nuclei/{name}.json) */
export interface NucleusData {
  name: string;
  full_name: string;
  unit: string;
  role: string;
  depth: number;
  output_dim: number;
  output: number[][];
  dimension_names: string[];
  layers: LayerInfo[];
  region_links: RegionLinkInfo[];
  neuro_links: NeuroLinkInfo[];
  h3_demands: H3DemandInfo[];
  metadata: NucleusMetadata;
}

/** R³ group boundary */
export interface R3Group {
  letter: string;
  name: string;
  start: number;
  end: number;
  dim: number;
  stage: number;
}

/** Brain region info */
export interface RegionInfo {
  index: number;
  name: string;
  abbreviation: string;
  hemisphere: string;
  mni_coords: [number, number, number];
  brodmann_area: number | null;
  group: "cortical" | "subcortical" | "brainstem";
}

/** Ψ³ PsiState data */
export interface PsiData {
  affect: number[][];
  emotion: number[][];
  aesthetic: number[][];
  bodily: number[][];
  cognitive: number[][];
  temporal: number[][];
}

/** H³ sparse features keyed by "r3_h_m_l" string */
export type H3Features = Record<string, number[]>;
