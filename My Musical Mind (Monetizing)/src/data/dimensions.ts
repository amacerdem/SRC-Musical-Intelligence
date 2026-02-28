/* ── Dimension Hierarchy — 6D → 12D → 24D (canonical tree.py port) ──
 *  Binary tree mirroring Musical_Intelligence/brain/dimensions/tree.py.
 *  24D leaf nodes: each aggregates 5-7 beliefs by mean.
 *  12D nodes: mean of 2 child 24D values.
 *  6D nodes:  mean of 2 child 12D values.
 *  All 131 beliefs are covered exactly once.
 *
 *  6D  Psychology    (experiential, free tier)
 *  12D Cognition     (music cognition, basic tier)
 *  24D Neuroscience  (neural, premium tier)
 *  ──────────────────────────────────────────────────────────────────── */

import type { DimensionProfile, DimensionKey6D } from "@/types/dimensions";
import type { MindGenes } from "@/types/m3";

// =====================================================================
// LabDimension — the universal dimension descriptor
// =====================================================================

export interface LabDimension {
  index: number;
  key: string;
  name: string;
  nameTr: string;
  beliefIndices: number[];     // indices into beliefs[131] — mean aggregated
  color: string;
  parentKey: string | null;    // parent at layer above
}

// =====================================================================
// 24D — NEUROSCIENCE LAYER (leaf nodes, each maps to belief indices)
// =====================================================================

export const ALL_NEUROSCIENCE: LabDimension[] = [
  // Curiosity > Anticipation children
  { index: 0,  key: "predictive_processing", name: "Pattern Sense",     nameTr: "Örüntü Algısı",     beliefIndices: [20,21,28,84,85],               color: "#38BDF8",   parentKey: "expectancy" },
  { index: 1,  key: "information_entropy",   name: "Wonder",            nameTr: "Hayret",             beliefIndices: [3,7,17,19,30],                 color: "#38BDF8CC", parentKey: "expectancy" },
  // Curiosity > Surprise children
  { index: 2,  key: "sequence_learning",     name: "Learning",          nameTr: "Öğrenme",            beliefIndices: [18,24,25,29,31],               color: "#38BDF899", parentKey: "information_rate" },
  { index: 3,  key: "sensory_encoding",      name: "Sound Awareness",   nameTr: "Ses Farkındalığı",   beliefIndices: [0,13,16,33,35,39],             color: "#38BDF877", parentKey: "information_rate" },
  // Energy > Tension children
  { index: 4,  key: "harmonic_tension",      name: "Harmonic Pull",     nameTr: "Harmonik Çekim",     beliefIndices: [4,5,6,80,82,88],               color: "#EF4444",   parentKey: "tension_arc" },
  { index: 5,  key: "autonomic_arousal",     name: "Chills",            nameTr: "Tüyler Diken",       beliefIndices: [22,23,26,60,62,63],            color: "#EF4444CC", parentKey: "tension_arc" },
  // Energy > Impact children
  { index: 6,  key: "sensory_salience",      name: "Attention Grab",    nameTr: "Dikkat Çekme",       beliefIndices: [15,34,36,37,38,61],            color: "#EF444499", parentKey: "sonic_impact" },
  { index: 7,  key: "aesthetic_appraisal",   name: "Beauty Sense",      nameTr: "Güzellik Hissi",     beliefIndices: [11,12,14,27,40,41],            color: "#EF444477", parentKey: "sonic_impact" },
  // Rhythm > Sync children
  { index: 8,  key: "oscillation_coupling",  name: "Beat Lock",         nameTr: "Ritim Kilidi",       beliefIndices: [42,43,44,45,46],               color: "#22C55E",   parentKey: "entrainment" },
  { index: 9,  key: "motor_period_locking",  name: "Body Pulse",        nameTr: "Beden Nabzı",        beliefIndices: [96,97,98,99,100],              color: "#22C55ECC", parentKey: "entrainment" },
  // Rhythm > Groove children
  { index: 10, key: "auditory_motor",        name: "Movement Urge",     nameTr: "Hareket Dürtüsü",    beliefIndices: [90,91,92,93,95],               color: "#22C55E99", parentKey: "groove" },
  { index: 11, key: "hierarchical_context",  name: "Musical Story",     nameTr: "Müzikal Hikaye",     beliefIndices: [94,101,102,103,105],           color: "#22C55E77", parentKey: "groove" },
  // Emotion > Empathy children
  { index: 12, key: "valence_mode",          name: "Mood Color",        nameTr: "Duygu Rengi",        beliefIndices: [64,65,66,67,68],               color: "#A855F7",   parentKey: "contagion" },
  { index: 13, key: "nostalgia_circuitry",   name: "Time Travel",       nameTr: "Zaman Yolculuğu",    beliefIndices: [69,70,71,72,73],               color: "#A855F7CC", parentKey: "contagion" },
  // Emotion > Pleasure children
  { index: 14, key: "dopaminergic_drive",    name: "Craving",           nameTr: "Özlem",              beliefIndices: [74,75,76,77,78],               color: "#A855F799", parentKey: "reward" },
  { index: 15, key: "hedonic_valuation",     name: "Bliss",             nameTr: "Keyif",              beliefIndices: [79,81,83,86,87,89],            color: "#A855F777", parentKey: "reward" },
  // Memory > Nostalgia children
  { index: 16, key: "hippocampal_binding",   name: "Déjà Vu",           nameTr: "Déjà Vu",            beliefIndices: [47,48,49,54,57,58,59],         color: "#FBBF24",   parentKey: "episodic_resonance" },
  { index: 17, key: "autobiographical",      name: "Life Story",        nameTr: "Yaşam Öyküsü",       beliefIndices: [50,51,52,53,55,56],            color: "#FBBF24CC", parentKey: "episodic_resonance" },
  // Memory > Familiarity children
  { index: 18, key: "pitch_melody",          name: "Melodic Ear",       nameTr: "Melodik Kulak",      beliefIndices: [1,2,8,9,10,32],                color: "#FBBF2499", parentKey: "recognition" },
  { index: 19, key: "perceptual_learning",   name: "Trained Ear",       nameTr: "Eğitimli Kulak",     beliefIndices: [107,108,109,110,111,112,113],   color: "#FBBF2477", parentKey: "recognition" },
  // Connection > Togetherness children
  { index: 20, key: "structural_prediction", name: "Musical Intuition", nameTr: "Müzikal Sezgi",      beliefIndices: [104,106,114,115],               color: "#EC4899",   parentKey: "synchrony" },
  { index: 21, key: "expertise_network",     name: "Mastery",           nameTr: "Ustalık",            beliefIndices: [116,117,118,119,120],           color: "#EC4899CC", parentKey: "synchrony" },
  // Connection > Bonding children
  { index: 22, key: "interpersonal_sync",    name: "Shared Pulse",      nameTr: "Ortak Nabız",        beliefIndices: [122,123,124,128,130],           color: "#EC489999", parentKey: "bonding" },
  { index: 23, key: "social_reward",         name: "Together Joy",      nameTr: "Birlikte Neşe",      beliefIndices: [121,125,126,127,129],           color: "#EC489977", parentKey: "bonding" },
];

// =====================================================================
// 12D — COGNITION LAYER (each aggregates 2 neuroscience children)
// =====================================================================

export const ALL_COGNITION: LabDimension[] = [
  // Curiosity children
  { index: 0,  key: "expectancy",         name: "Anticipation",    nameTr: "Önsezi",        beliefIndices: [20,21,28,84,85, 3,7,17,19,30],                                    color: "#38BDF8",   parentKey: "discovery" },
  { index: 1,  key: "information_rate",   name: "Surprise",        nameTr: "Sürpriz",       beliefIndices: [18,24,25,29,31, 0,13,16,33,35,39],                                color: "#38BDF8B0", parentKey: "discovery" },
  // Energy children
  { index: 2,  key: "tension_arc",        name: "Tension",         nameTr: "Gerilim",       beliefIndices: [4,5,6,80,82,88, 22,23,26,60,62,63],                               color: "#EF4444",   parentKey: "intensity" },
  { index: 3,  key: "sonic_impact",       name: "Impact",          nameTr: "Etki",          beliefIndices: [15,34,36,37,38,61, 11,12,14,27,40,41],                             color: "#EF4444B0", parentKey: "intensity" },
  // Rhythm children
  { index: 4,  key: "entrainment",        name: "Sync",            nameTr: "Senkron",       beliefIndices: [42,43,44,45,46, 96,97,98,99,100],                                  color: "#22C55E",   parentKey: "flow" },
  { index: 5,  key: "groove",             name: "Groove",          nameTr: "Groove",        beliefIndices: [90,91,92,93,95, 94,101,102,103,105],                               color: "#22C55EB0", parentKey: "flow" },
  // Emotion children
  { index: 6,  key: "contagion",          name: "Empathy",         nameTr: "Empati",        beliefIndices: [64,65,66,67,68, 69,70,71,72,73],                                  color: "#A855F7",   parentKey: "depth" },
  { index: 7,  key: "reward",             name: "Pleasure",        nameTr: "Haz",           beliefIndices: [74,75,76,77,78, 79,81,83,86,87,89],                               color: "#A855F7B0", parentKey: "depth" },
  // Memory children
  { index: 8,  key: "episodic_resonance", name: "Nostalgia",       nameTr: "Nostalji",      beliefIndices: [47,48,49,54,57,58,59, 50,51,52,53,55,56],                         color: "#FBBF24",   parentKey: "trace" },
  { index: 9,  key: "recognition",        name: "Familiarity",     nameTr: "Tanıdıklık",    beliefIndices: [1,2,8,9,10,32, 107,108,109,110,111,112,113],                      color: "#FBBF24B0", parentKey: "trace" },
  // Connection children
  { index: 10, key: "synchrony",          name: "Togetherness",    nameTr: "Birliktelik",   beliefIndices: [104,106,114,115, 116,117,118,119,120],                             color: "#EC4899",   parentKey: "sharing" },
  { index: 11, key: "bonding",            name: "Bonding",         nameTr: "Bağlanma",      beliefIndices: [122,123,124,128,130, 121,125,126,127,129],                         color: "#EC4899B0", parentKey: "sharing" },
];

// =====================================================================
// 6D — PSYCHOLOGY LAYER (experiential, each aggregates 2 cognition)
// =====================================================================

export const ALL_PSYCHOLOGY: LabDimension[] = [
  { index: 0, key: "discovery",  name: "Curiosity",   nameTr: "Merak",    beliefIndices: [], color: "#38BDF8", parentKey: null },
  { index: 1, key: "intensity",  name: "Energy",      nameTr: "Enerji",   beliefIndices: [], color: "#EF4444", parentKey: null },
  { index: 2, key: "flow",       name: "Rhythm",      nameTr: "Ritim",    beliefIndices: [], color: "#22C55E", parentKey: null },
  { index: 3, key: "depth",      name: "Emotion",     nameTr: "Duygu",    beliefIndices: [], color: "#A855F7", parentKey: null },
  { index: 4, key: "trace",      name: "Memory",      nameTr: "Hafıza",   beliefIndices: [], color: "#FBBF24", parentKey: null },
  { index: 5, key: "sharing",    name: "Connection",  nameTr: "Bağ",      beliefIndices: [], color: "#EC4899", parentKey: null },
];

// =====================================================================
// Pre-computed child index maps (built once at module load)
// =====================================================================

/** 12D index → [child_24D_0, child_24D_1] */
const _NEURO_CHILDREN: [number, number][] = ALL_COGNITION.map((cog) => {
  const kids = ALL_NEUROSCIENCE.filter((n) => n.parentKey === cog.key);
  return [kids[0].index, kids[1].index];
});

/** 6D index → [child_12D_0, child_12D_1] */
const _COG_CHILDREN: [number, number][] = ALL_PSYCHOLOGY.map((psy) => {
  const kids = ALL_COGNITION.filter((c) => c.parentKey === psy.key);
  return [kids[0].index, kids[1].index];
});

// =====================================================================
// Parent-child lookups (for consumer components)
// =====================================================================

/** 6D → its 2 child 12D nodes */
export const COGNITION_CHILDREN: Record<string, [LabDimension, LabDimension]> = {};
for (const psych of ALL_PSYCHOLOGY) {
  const kids = ALL_COGNITION.filter((c) => c.parentKey === psych.key);
  if (kids.length === 2) COGNITION_CHILDREN[psych.key] = [kids[0], kids[1]];
}

/** 12D → its 2 child 24D nodes */
export const NEUROSCIENCE_CHILDREN: Record<string, [LabDimension, LabDimension]> = {};
for (const cog of ALL_COGNITION) {
  const kids = ALL_NEUROSCIENCE.filter((n) => n.parentKey === cog.key);
  if (kids.length === 2) NEUROSCIENCE_CHILDREN[cog.key] = [kids[0], kids[1]];
}

// =====================================================================
// Color lookups
// =====================================================================

/** 6D key → color */
export const PSYCHOLOGY_COLORS: Record<string, string> = {};
for (const d of ALL_PSYCHOLOGY) PSYCHOLOGY_COLORS[d.key] = d.color;

// =====================================================================
// Name arrays
// =====================================================================

export const PSYCHOLOGY_NAMES: string[] = ALL_PSYCHOLOGY.map((d) => d.name);
export const PSYCHOLOGY_NAMES_TR: string[] = ALL_PSYCHOLOGY.map((d) => d.nameTr);
export const COGNITION_NAMES: string[] = ALL_COGNITION.map((d) => d.name);
export const NEUROSCIENCE_NAMES: string[] = ALL_NEUROSCIENCE.map((d) => d.name);

// =====================================================================
// Dimension computation — hierarchical mean aggregation
// =====================================================================

/**
 * Mean of beliefs at given indices. Returns 0 for empty arrays.
 */
function meanAt(beliefs: number[], indices: number[]): number {
  if (indices.length === 0) return 0;
  let sum = 0;
  for (const idx of indices) sum += beliefs[idx] ?? 0;
  return sum / indices.length;
}

/**
 * Compute all three dimension layers from 131 belief values.
 * Follows tree.py:
 *   24D[i] = mean(beliefs at beliefIndices)
 *   12D[i] = mean(child_24D_0, child_24D_1)
 *   6D[i]  = mean(child_12D_0, child_12D_1)
 */
export function computeDimensions(beliefs: number[]): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  // 24D: mean of each node's belief subset
  const neuroscience = ALL_NEUROSCIENCE.map((d) => meanAt(beliefs, d.beliefIndices));

  // 12D: mean of 2 child 24D values
  const cognition = _NEURO_CHILDREN.map(([c0, c1]) =>
    (neuroscience[c0] + neuroscience[c1]) / 2
  );

  // 6D: mean of 2 child 12D values
  const psychology = _COG_CHILDREN.map(([c0, c1]) =>
    (cognition[c0] + cognition[c1]) / 2
  );

  return { psychology, cognition, neuroscience };
}

// Alias for backward compat with Lab store
export const computeLabDimensions = computeDimensions;

/**
 * Convert a DimensionProfile (named 6D object) to an ordered array.
 */
export function profileToArray(profile: DimensionProfile): number[] {
  return [
    profile.discovery,
    profile.intensity,
    profile.flow,
    profile.depth,
    profile.trace,
    profile.sharing,
  ];
}

/**
 * Convert an ordered 6D array to a named DimensionProfile.
 */
export function arrayToProfile(values: number[]): DimensionProfile {
  return {
    discovery:  values[0] ?? 0,
    intensity:  values[1] ?? 0,
    flow:       values[2] ?? 0,
    depth:      values[3] ?? 0,
    trace:      values[4] ?? 0,
    sharing:    values[5] ?? 0,
  };
}

/**
 * Derive 6D psychological dimensions from the user's 5-gene DNA profile.
 * Used as fallback when beliefPriors haven't accumulated from listening.
 *
 * Mapping:
 *   entropy    → discovery  (novelty-seeking)
 *   tension    → intensity  (tension appetite)
 *   plasticity → flow       (adaptive motor coupling)
 *   resonance  → depth      (emotional resonance)
 *   resolution → trace      (memory/recognition craving)
 *   sharing    ← mean(plasticity, resonance) (social connection)
 */
export function genesToDimensions(genes: MindGenes): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  // 6D
  const psych = [
    genes.entropy,                              // discovery
    genes.tension,                              // intensity
    genes.plasticity,                           // flow
    genes.resonance,                            // depth
    genes.resolution,                           // trace
    (genes.plasticity + genes.resonance) / 2,   // sharing
  ];

  // 12D: split each 6D into 2 children with ±8% variation
  const cog: number[] = [];
  for (const v of psych) {
    cog.push(Math.min(1, v * 1.08), Math.max(0, v * 0.92));
  }

  // 24D: split each 12D into 2 children with ±5% variation
  const neuro: number[] = [];
  for (const v of cog) {
    neuro.push(Math.min(1, v * 1.05), Math.max(0, v * 0.95));
  }

  return { psychology: psych, cognition: cog, neuroscience: neuro };
}

/** Get dimension info for a given depth and index */
export function getLabDim(depth: 6 | 12 | 24, index: number): LabDimension | undefined {
  if (depth === 6) return ALL_PSYCHOLOGY[index];
  if (depth === 12) return ALL_COGNITION[index];
  return ALL_NEUROSCIENCE[index];
}
