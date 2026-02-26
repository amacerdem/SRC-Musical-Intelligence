/* ── Neural Viz: Data-driven constants for 3D visualization ─────── */

/** Belief colors from design tokens — used for orbs, particles, relays */
export const BELIEF_COLORS = {
  consonance: { hex: "#C084FC", rgb: [192 / 255, 132 / 255, 252 / 255] as [number, number, number] },
  tempo:      { hex: "#F97316", rgb: [249 / 255, 115 / 255, 22 / 255] as [number, number, number] },
  salience:   { hex: "#84CC16", rgb: [132 / 255, 204 / 255, 22 / 255] as [number, number, number] },
  familiarity:{ hex: "#38BDF8", rgb: [56 / 255, 189 / 255, 248 / 255] as [number, number, number] },
  reward:     { hex: "#FBBF24", rgb: [251 / 255, 191 / 255, 36 / 255] as [number, number, number] },
} as const;

/** R3 group colors — used for terrain rings */
export const R3_GROUP_COLORS: Record<string, { hex: string; rgb: [number, number, number] }> = {
  A_consonance: { hex: "#C084FC", rgb: [0.753, 0.518, 0.988] },
  B_energy:     { hex: "#EF4444", rgb: [0.937, 0.267, 0.267] },
  C_timbre:     { hex: "#06B6D4", rgb: [0.024, 0.714, 0.831] },
  D_change:     { hex: "#F97316", rgb: [0.976, 0.451, 0.086] },
  F_pitch:      { hex: "#8B5CF6", rgb: [0.545, 0.361, 0.965] },
  G_rhythm:     { hex: "#84CC16", rgb: [0.518, 0.800, 0.086] },
  H_harmony:    { hex: "#3B82F6", rgb: [0.231, 0.510, 0.965] },
  J_ext_timbre: { hex: "#EC4899", rgb: [0.925, 0.282, 0.600] },
  K_modulation: { hex: "#FBBF24", rgb: [0.984, 0.749, 0.141] },
};

export const R3_GROUP_NAMES = [
  "A_consonance", "B_energy", "C_timbre", "D_change",
  "F_pitch", "G_rhythm", "H_harmony", "J_ext_timbre", "K_modulation",
] as const;

/** Belief orb configuration */
export const BELIEF_ORBS = [
  { key: "consonance", radius: 3.0, baseHeight: 2, color: BELIEF_COLORS.consonance },
  { key: "tempo",      radius: 4.0, baseHeight: 1.5, color: BELIEF_COLORS.tempo },
  { key: "salience",   radius: 5.0, baseHeight: 3, color: BELIEF_COLORS.salience },
  { key: "familiarity",radius: 3.5, baseHeight: 1, color: BELIEF_COLORS.familiarity },
  { key: "reward",     radius: 2.0, baseHeight: 4, color: BELIEF_COLORS.reward },
] as const;

/** RAM region 3D positions (schematic neuroanatomical layout) */
export const RAM_POSITIONS: Record<string, [number, number, number]> = {
  // Cortical (upper arc)
  A1_HG:   [-2.0, 5.0, 0.0],
  STG:     [-1.5, 5.5, 1.0],
  STS:     [-1.0, 5.0, 1.5],
  IFG:     [ 1.5, 5.5, 0.5],
  dlPFC:   [ 2.0, 6.0, -0.5],
  vmPFC:   [ 0.5, 5.5, -1.5],
  OFC:     [ 0.0, 5.0, -2.0],
  ACC:     [ 0.0, 6.0, 0.0],
  SMA:     [ 1.0, 5.5, -1.0],
  PMC:     [ 2.0, 5.0, 0.0],
  AG:      [-2.0, 5.5, -1.0],
  TP:      [-2.5, 4.5, 0.5],
  // Subcortical (middle ring)
  VTA:     [ 0.3, 2.0, 0.0],
  NAcc:    [ 0.8, 2.5, 0.5],
  caudate: [-0.5, 2.5, 0.8],
  amygdala:[-1.0, 2.0, -0.5],
  hippocampus: [-0.8, 1.5, -1.0],
  putamen: [ 1.0, 2.0, -0.3],
  MGB:     [-1.5, 2.5, 0.0],
  hypothalamus: [0.0, 1.5, 0.5],
  insula:  [ 1.5, 2.5, -0.8],
  // Brainstem (lower)
  IC:      [ 0.0, 0.0, 0.0],
  AN:      [-0.5, -0.5, 0.3],
  CN:      [ 0.5, -0.5, 0.3],
  SOC:     [ 0.0, -0.5, -0.3],
  PAG:     [ 0.0, 0.5, -0.5],
};

/** RAM region edges (relay → region links for constellation lines) */
export const RAM_EDGES: [string, string][] = [
  // BCH pathway
  ["IC", "MGB"], ["MGB", "STG"], ["MGB", "A1_HG"],
  // HMCE pathway
  ["A1_HG", "STG"], ["STG", "STS"], ["STS", "hippocampus"],
  // SNEM pathway
  ["STG", "SMA"], ["SMA", "putamen"],
  // MMP pathway
  ["hippocampus", "STG"], ["hippocampus", "IFG"],
  // DAED pathway
  ["VTA", "NAcc"], ["NAcc", "caudate"], ["VTA", "OFC"],
  // MPG pathway
  ["STG", "IFG"], ["IFG", "PMC"],
  // Cross-connections
  ["ACC", "dlPFC"], ["ACC", "vmPFC"], ["amygdala", "OFC"],
  ["insula", "ACC"], ["AG", "STS"], ["TP", "amygdala"],
];

/** Relay configuration for animated tubes */
export const RELAY_CONFIG = [
  { key: "bch_consonance_signal", from: "IC", to: "STG", color: BELIEF_COLORS.consonance.hex },
  { key: "hmce_a1_encoding", from: "A1_HG", to: "STS", color: BELIEF_COLORS.tempo.hex },
  { key: "snem_entrainment", from: "SMA", to: "putamen", color: BELIEF_COLORS.salience.hex },
  { key: "mmp_familiarity", from: "hippocampus", to: "STG", color: BELIEF_COLORS.familiarity.hex },
  { key: "daed_wanting", from: "VTA", to: "NAcc", color: BELIEF_COLORS.reward.hex },
  { key: "mpg_onset", from: "STG", to: "IFG", color: "#EC4899" },
] as const;
