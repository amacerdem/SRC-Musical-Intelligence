/* ── Dimension Hierarchy Data — 6D → 12D → 24D → 131 beliefs ─────
 *  Complete binary tree mirroring Musical_Intelligence/brain/dimensions/tree.py
 *
 *  6 Psychology nodes  (experiential, free tier)
 *  12 Cognition nodes  (music cognition, basic tier)
 *  24 Neuroscience nodes (neuroscience, premium tier)
 *
 *  Each 6D → 2×12D, each 12D → 2×24D, each 24D → disjoint belief subset.
 *  All 131 beliefs (0-130) appear exactly once across the 24 leaf nodes.
 *  ──────────────────────────────────────────────────────────────────── */

import type { DimensionNode, DimensionProfile, DimensionKey6D } from "@/types/dimensions";
import type { MindGenes } from "@/types/m3";

// =====================================================================
// 24D — NEUROSCIENCE LAYER (leaf nodes, each maps to belief indices)
// =====================================================================

// --- Discovery / Expectancy ---
const PREDICTIVE_PROCESSING: DimensionNode = {
  index: 0, key: "predictive_processing",
  name: "Predictive Processing", nameTr: "Tahminsel İşleme",
  layer: "neuroscience", parentKey: "expectancy",
  beliefIndices: [20, 21, 28, 84, 85],
};
const INFORMATION_ENTROPY: DimensionNode = {
  index: 1, key: "information_entropy",
  name: "Information Entropy", nameTr: "Bilgi Entropisi",
  layer: "neuroscience", parentKey: "expectancy",
  beliefIndices: [3, 7, 17, 19, 30],
};

// --- Discovery / Information Rate ---
const SEQUENCE_LEARNING: DimensionNode = {
  index: 2, key: "sequence_learning",
  name: "Sequence Learning", nameTr: "Dizi Öğrenme",
  layer: "neuroscience", parentKey: "information_rate",
  beliefIndices: [18, 24, 25, 29, 31],
};
const SENSORY_ENCODING: DimensionNode = {
  index: 3, key: "sensory_encoding",
  name: "Sensory Encoding", nameTr: "Duyusal Kodlama",
  layer: "neuroscience", parentKey: "information_rate",
  beliefIndices: [0, 13, 16, 33, 35, 39],
};

// --- Intensity / Tension Arc ---
const HARMONIC_TENSION: DimensionNode = {
  index: 4, key: "harmonic_tension",
  name: "Harmonic Tension", nameTr: "Harmonik Gerilim",
  layer: "neuroscience", parentKey: "tension_arc",
  beliefIndices: [4, 5, 6, 80, 82, 88],
};
const AUTONOMIC_AROUSAL: DimensionNode = {
  index: 5, key: "autonomic_arousal",
  name: "Autonomic Arousal", nameTr: "Otonom Uyarılma",
  layer: "neuroscience", parentKey: "tension_arc",
  beliefIndices: [22, 23, 26, 60, 62, 63],
};

// --- Intensity / Sonic Impact ---
const SENSORY_SALIENCE: DimensionNode = {
  index: 6, key: "sensory_salience",
  name: "Sensory Salience", nameTr: "Duyusal Belirginlik",
  layer: "neuroscience", parentKey: "sonic_impact",
  beliefIndices: [15, 34, 36, 37, 38, 61],
};
const AESTHETIC_APPRAISAL: DimensionNode = {
  index: 7, key: "aesthetic_appraisal",
  name: "Aesthetic Appraisal", nameTr: "Estetik Değerlendirme",
  layer: "neuroscience", parentKey: "sonic_impact",
  beliefIndices: [11, 12, 14, 27, 40, 41],
};

// --- Flow / Entrainment ---
const OSCILLATION_COUPLING: DimensionNode = {
  index: 8, key: "oscillation_coupling",
  name: "Oscillation Coupling", nameTr: "Osilasyon Eşleşmesi",
  layer: "neuroscience", parentKey: "entrainment",
  beliefIndices: [42, 43, 44, 45, 46],
};
const MOTOR_PERIOD_LOCKING: DimensionNode = {
  index: 9, key: "motor_period_locking",
  name: "Motor Period-Locking", nameTr: "Motor Periyot Kilidi",
  layer: "neuroscience", parentKey: "entrainment",
  beliefIndices: [96, 97, 98, 99, 100],
};

// --- Flow / Groove ---
const AUDITORY_MOTOR: DimensionNode = {
  index: 10, key: "auditory_motor",
  name: "Auditory-Motor Integration", nameTr: "İşitsel-Motor Entegrasyon",
  layer: "neuroscience", parentKey: "groove",
  beliefIndices: [90, 91, 92, 93, 95],
};
const HIERARCHICAL_CONTEXT: DimensionNode = {
  index: 11, key: "hierarchical_context",
  name: "Hierarchical Context", nameTr: "Hiyerarşik Bağlam",
  layer: "neuroscience", parentKey: "groove",
  beliefIndices: [94, 101, 102, 103, 105],
};

// --- Depth / Contagion ---
const VALENCE_MODE: DimensionNode = {
  index: 12, key: "valence_mode",
  name: "Valence-Mode Circuitry", nameTr: "Valans-Mod Devresi",
  layer: "neuroscience", parentKey: "contagion",
  beliefIndices: [64, 65, 66, 67, 68],
};
const NOSTALGIA_CIRCUITRY: DimensionNode = {
  index: 13, key: "nostalgia_circuitry",
  name: "Nostalgia Circuitry", nameTr: "Nostalji Devresi",
  layer: "neuroscience", parentKey: "contagion",
  beliefIndices: [69, 70, 71, 72, 73],
};

// --- Depth / Reward ---
const DOPAMINERGIC_DRIVE: DimensionNode = {
  index: 14, key: "dopaminergic_drive",
  name: "Dopaminergic Drive", nameTr: "Dopaminerjik Dürtü",
  layer: "neuroscience", parentKey: "reward",
  beliefIndices: [74, 75, 76, 77, 78],
};
const HEDONIC_VALUATION: DimensionNode = {
  index: 15, key: "hedonic_valuation",
  name: "Hedonic Valuation", nameTr: "Hedonik Değerleme",
  layer: "neuroscience", parentKey: "reward",
  beliefIndices: [79, 81, 83, 86, 87, 89],
};

// --- Trace / Episodic Resonance ---
const HIPPOCAMPAL_BINDING: DimensionNode = {
  index: 16, key: "hippocampal_binding",
  name: "Hippocampal Binding", nameTr: "Hipokampal Bağlama",
  layer: "neuroscience", parentKey: "episodic_resonance",
  beliefIndices: [47, 48, 49, 54, 57, 58, 59],
};
const AUTOBIOGRAPHICAL: DimensionNode = {
  index: 17, key: "autobiographical",
  name: "Autobiographical Network", nameTr: "Otobiyografik Ağ",
  layer: "neuroscience", parentKey: "episodic_resonance",
  beliefIndices: [50, 51, 52, 53, 55, 56],
};

// --- Trace / Recognition ---
const PITCH_MELODY: DimensionNode = {
  index: 18, key: "pitch_melody",
  name: "Pitch-Melody Processing", nameTr: "Perde-Melodi İşleme",
  layer: "neuroscience", parentKey: "recognition",
  beliefIndices: [1, 2, 8, 9, 10, 32],
};
const PERCEPTUAL_LEARNING: DimensionNode = {
  index: 19, key: "perceptual_learning",
  name: "Perceptual Learning", nameTr: "Algısal Öğrenme",
  layer: "neuroscience", parentKey: "recognition",
  beliefIndices: [107, 108, 109, 110, 111, 112, 113],
};

// --- Sharing / Synchrony ---
const STRUCTURAL_PREDICTION: DimensionNode = {
  index: 20, key: "structural_prediction",
  name: "Structural Prediction", nameTr: "Yapısal Tahmin",
  layer: "neuroscience", parentKey: "synchrony",
  beliefIndices: [104, 106, 114, 115],
};
const EXPERTISE_NETWORK: DimensionNode = {
  index: 21, key: "expertise_network",
  name: "Expertise Network", nameTr: "Uzmanlık Ağı",
  layer: "neuroscience", parentKey: "synchrony",
  beliefIndices: [116, 117, 118, 119, 120],
};

// --- Sharing / Bonding ---
const INTERPERSONAL_SYNC: DimensionNode = {
  index: 22, key: "interpersonal_sync",
  name: "Interpersonal Synchrony", nameTr: "Kişilerarası Senkronizasyon",
  layer: "neuroscience", parentKey: "bonding",
  beliefIndices: [122, 123, 124, 128, 130],
};
const SOCIAL_REWARD: DimensionNode = {
  index: 23, key: "social_reward",
  name: "Social Reward", nameTr: "Sosyal Ödül",
  layer: "neuroscience", parentKey: "bonding",
  beliefIndices: [121, 125, 126, 127, 129],
};

// =====================================================================
// 12D — MUSIC COGNITION LAYER (each aggregates 2 neuroscience children)
// =====================================================================

const EXPECTANCY: DimensionNode = {
  index: 0, key: "expectancy",
  name: "Expectancy", nameTr: "Beklenti",
  layer: "cognition", parentKey: "discovery",
  beliefIndices: [...PREDICTIVE_PROCESSING.beliefIndices, ...INFORMATION_ENTROPY.beliefIndices],
};
const INFORMATION_RATE: DimensionNode = {
  index: 1, key: "information_rate",
  name: "Information Rate", nameTr: "Bilgi Hızı",
  layer: "cognition", parentKey: "discovery",
  beliefIndices: [...SEQUENCE_LEARNING.beliefIndices, ...SENSORY_ENCODING.beliefIndices],
};

const TENSION_ARC: DimensionNode = {
  index: 2, key: "tension_arc",
  name: "Tension Arc", nameTr: "Gerilim Yayı",
  layer: "cognition", parentKey: "intensity",
  beliefIndices: [...HARMONIC_TENSION.beliefIndices, ...AUTONOMIC_AROUSAL.beliefIndices],
};
const SONIC_IMPACT: DimensionNode = {
  index: 3, key: "sonic_impact",
  name: "Sonic Impact", nameTr: "Sonik Etki",
  layer: "cognition", parentKey: "intensity",
  beliefIndices: [...SENSORY_SALIENCE.beliefIndices, ...AESTHETIC_APPRAISAL.beliefIndices],
};

const ENTRAINMENT: DimensionNode = {
  index: 4, key: "entrainment",
  name: "Entrainment", nameTr: "Senkronizasyon",
  layer: "cognition", parentKey: "flow",
  beliefIndices: [...OSCILLATION_COUPLING.beliefIndices, ...MOTOR_PERIOD_LOCKING.beliefIndices],
};
const GROOVE: DimensionNode = {
  index: 5, key: "groove",
  name: "Groove", nameTr: "Groove",
  layer: "cognition", parentKey: "flow",
  beliefIndices: [...AUDITORY_MOTOR.beliefIndices, ...HIERARCHICAL_CONTEXT.beliefIndices],
};

const CONTAGION: DimensionNode = {
  index: 6, key: "contagion",
  name: "Emotional Contagion", nameTr: "Duygusal Bulaşma",
  layer: "cognition", parentKey: "depth",
  beliefIndices: [...VALENCE_MODE.beliefIndices, ...NOSTALGIA_CIRCUITRY.beliefIndices],
};
const REWARD: DimensionNode = {
  index: 7, key: "reward",
  name: "Reward", nameTr: "Ödül",
  layer: "cognition", parentKey: "depth",
  beliefIndices: [...DOPAMINERGIC_DRIVE.beliefIndices, ...HEDONIC_VALUATION.beliefIndices],
};

const EPISODIC_RESONANCE: DimensionNode = {
  index: 8, key: "episodic_resonance",
  name: "Episodic Resonance", nameTr: "Epizodik Rezonans",
  layer: "cognition", parentKey: "trace",
  beliefIndices: [...HIPPOCAMPAL_BINDING.beliefIndices, ...AUTOBIOGRAPHICAL.beliefIndices],
};
const RECOGNITION: DimensionNode = {
  index: 9, key: "recognition",
  name: "Recognition", nameTr: "Tanıma",
  layer: "cognition", parentKey: "trace",
  beliefIndices: [...PITCH_MELODY.beliefIndices, ...PERCEPTUAL_LEARNING.beliefIndices],
};

const SYNCHRONY: DimensionNode = {
  index: 10, key: "synchrony",
  name: "Synchrony", nameTr: "Senkroni",
  layer: "cognition", parentKey: "sharing",
  beliefIndices: [...STRUCTURAL_PREDICTION.beliefIndices, ...EXPERTISE_NETWORK.beliefIndices],
};
const BONDING: DimensionNode = {
  index: 11, key: "bonding",
  name: "Bonding", nameTr: "Bağlanma",
  layer: "cognition", parentKey: "sharing",
  beliefIndices: [...INTERPERSONAL_SYNC.beliefIndices, ...SOCIAL_REWARD.beliefIndices],
};

// =====================================================================
// 6D — PSYCHOLOGY LAYER (experiential, each aggregates 2 cognition)
// =====================================================================

const DISCOVERY: DimensionNode = {
  index: 0, key: "discovery",
  name: "Curiosity", nameTr: "Merak",
  layer: "psychology", parentKey: null,
  beliefIndices: [...EXPECTANCY.beliefIndices, ...INFORMATION_RATE.beliefIndices],
};
const INTENSITY: DimensionNode = {
  index: 1, key: "intensity",
  name: "Energy", nameTr: "Enerji",
  layer: "psychology", parentKey: null,
  beliefIndices: [...TENSION_ARC.beliefIndices, ...SONIC_IMPACT.beliefIndices],
};
const FLOW: DimensionNode = {
  index: 2, key: "flow",
  name: "Groove", nameTr: "Ritim",
  layer: "psychology", parentKey: null,
  beliefIndices: [...ENTRAINMENT.beliefIndices, ...GROOVE.beliefIndices],
};
const DEPTH: DimensionNode = {
  index: 3, key: "depth",
  name: "Emotion", nameTr: "Duygu",
  layer: "psychology", parentKey: null,
  beliefIndices: [...CONTAGION.beliefIndices, ...REWARD.beliefIndices],
};
const TRACE: DimensionNode = {
  index: 4, key: "trace",
  name: "Memory", nameTr: "Hafıza",
  layer: "psychology", parentKey: null,
  beliefIndices: [...EPISODIC_RESONANCE.beliefIndices, ...RECOGNITION.beliefIndices],
};
const SHARING: DimensionNode = {
  index: 5, key: "sharing",
  name: "Connection", nameTr: "Bağ",
  layer: "psychology", parentKey: null,
  beliefIndices: [...SYNCHRONY.beliefIndices, ...BONDING.beliefIndices],
};

// =====================================================================
// Ordered arrays — canonical order by index
// =====================================================================

export const ALL_PSYCHOLOGY: DimensionNode[] = [
  DISCOVERY, INTENSITY, FLOW, DEPTH, TRACE, SHARING,
];

export const ALL_COGNITION: DimensionNode[] = [
  EXPECTANCY, INFORMATION_RATE, TENSION_ARC, SONIC_IMPACT,
  ENTRAINMENT, GROOVE, CONTAGION, REWARD,
  EPISODIC_RESONANCE, RECOGNITION, SYNCHRONY, BONDING,
];

export const ALL_NEUROSCIENCE: DimensionNode[] = [
  PREDICTIVE_PROCESSING, INFORMATION_ENTROPY,
  SEQUENCE_LEARNING, SENSORY_ENCODING,
  HARMONIC_TENSION, AUTONOMIC_AROUSAL,
  SENSORY_SALIENCE, AESTHETIC_APPRAISAL,
  OSCILLATION_COUPLING, MOTOR_PERIOD_LOCKING,
  AUDITORY_MOTOR, HIERARCHICAL_CONTEXT,
  VALENCE_MODE, NOSTALGIA_CIRCUITRY,
  DOPAMINERGIC_DRIVE, HEDONIC_VALUATION,
  HIPPOCAMPAL_BINDING, AUTOBIOGRAPHICAL,
  PITCH_MELODY, PERCEPTUAL_LEARNING,
  STRUCTURAL_PREDICTION, EXPERTISE_NETWORK,
  INTERPERSONAL_SYNC, SOCIAL_REWARD,
];

/** All 42 dimension nodes */
export const ALL_DIMENSIONS: DimensionNode[] = [
  ...ALL_PSYCHOLOGY,
  ...ALL_COGNITION,
  ...ALL_NEUROSCIENCE,
];

/** Lookup by key */
export const DIM_BY_KEY: Record<string, DimensionNode> = {};
for (const d of ALL_DIMENSIONS) {
  DIM_BY_KEY[d.key] = d;
}

/** Psychology dimension display names (EN) — ordered */
export const PSYCHOLOGY_NAMES: string[] = ALL_PSYCHOLOGY.map((d) => d.name);
export const PSYCHOLOGY_NAMES_TR: string[] = ALL_PSYCHOLOGY.map((d) => d.nameTr);
export const COGNITION_NAMES: string[] = ALL_COGNITION.map((d) => d.name);
export const NEUROSCIENCE_NAMES: string[] = ALL_NEUROSCIENCE.map((d) => d.name);

/** Dimension colors for psychology layer */
export const PSYCHOLOGY_COLORS: Record<DimensionKey6D, string> = {
  discovery: "#38BDF8",   // Sky blue — exploration, novelty
  intensity: "#EF4444",   // Red — tension, impact
  flow:      "#22C55E",   // Green — rhythm, movement
  depth:     "#A855F7",   // Purple — emotion, reward
  trace:     "#FBBF24",   // Amber — memory, recognition
  sharing:   "#EC4899",   // Pink — social, bonding
};

/** Parent→children mapping for tree traversal */
export const COGNITION_CHILDREN: Record<string, [DimensionNode, DimensionNode]> = {
  discovery: [EXPECTANCY, INFORMATION_RATE],
  intensity: [TENSION_ARC, SONIC_IMPACT],
  flow:      [ENTRAINMENT, GROOVE],
  depth:     [CONTAGION, REWARD],
  trace:     [EPISODIC_RESONANCE, RECOGNITION],
  sharing:   [SYNCHRONY, BONDING],
};

export const NEUROSCIENCE_CHILDREN: Record<string, [DimensionNode, DimensionNode]> = {
  expectancy:         [PREDICTIVE_PROCESSING, INFORMATION_ENTROPY],
  information_rate:   [SEQUENCE_LEARNING, SENSORY_ENCODING],
  tension_arc:        [HARMONIC_TENSION, AUTONOMIC_AROUSAL],
  sonic_impact:       [SENSORY_SALIENCE, AESTHETIC_APPRAISAL],
  entrainment:        [OSCILLATION_COUPLING, MOTOR_PERIOD_LOCKING],
  groove:             [AUDITORY_MOTOR, HIERARCHICAL_CONTEXT],
  contagion:          [VALENCE_MODE, NOSTALGIA_CIRCUITRY],
  reward:             [DOPAMINERGIC_DRIVE, HEDONIC_VALUATION],
  episodic_resonance: [HIPPOCAMPAL_BINDING, AUTOBIOGRAPHICAL],
  recognition:        [PITCH_MELODY, PERCEPTUAL_LEARNING],
  synchrony:          [STRUCTURAL_PREDICTION, EXPERTISE_NETWORK],
  bonding:            [INTERPERSONAL_SYNC, SOCIAL_REWARD],
};

// =====================================================================
// Dimension computation — aggregates 131 beliefs into layers
// =====================================================================

/** Compute mean of array values at given indices */
function meanAtIndices(values: number[], indices: number[]): number {
  if (indices.length === 0) return 0;
  let sum = 0;
  for (const i of indices) {
    sum += Math.abs(values[i] ?? 0);
  }
  return sum / indices.length;
}

/**
 * Compute all three dimension layers from 131 belief values.
 * Mirrors Musical_Intelligence.brain.dimensions.DimensionInterpreter.
 *
 * @param beliefs — Array of 131 float values (beliefPriors, rewardWeights, etc.)
 * @returns DimensionState with psychology (6), cognition (12), neuroscience (24)
 */
export function computeDimensions(beliefs: number[]): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  // 24D: mean of belief subsets per neuroscience dimension
  const neuro = ALL_NEUROSCIENCE.map((d) => meanAtIndices(beliefs, d.beliefIndices));

  // 12D: mean of 2 child 24D values
  const cog = ALL_COGNITION.map((d) => {
    const children = NEUROSCIENCE_CHILDREN[d.key];
    if (!children) return 0;
    return (neuro[children[0].index] + neuro[children[1].index]) / 2;
  });

  // 6D: mean of 2 child 12D values
  const psych = ALL_PSYCHOLOGY.map((d) => {
    const children = COGNITION_CHILDREN[d.key];
    if (!children) return 0;
    return (cog[children[0].index] + cog[children[1].index]) / 2;
  });

  return { psychology: psych, cognition: cog, neuroscience: neuro };
}

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
 * Derive 6D psychological dimensions from the user's 5-gene DNA profile.
 * Used as fallback when beliefPriors haven't accumulated from listening.
 *
 * Mapping rationale (gene → primary dimension):
 *   entropy    → discovery  (novelty seeking drives exploration)
 *   tension    → intensity  (arousal preference drives tension response)
 *   plasticity → flow       (adaptability drives entrainment/groove)
 *   resonance  → depth      (emotional resonance drives reward/contagion)
 *   resolution → trace      (pattern completion drives memory/recognition)
 *   sharing    ← mean(resonance, plasticity)  (empathy + adaptability → social bonding)
 *
 * Each gene also feeds into 12D and 24D via the tree structure:
 *   6D[i] splits into 2×12D children (slight jitter for shape variety)
 *   12D[j] splits into 2×24D children (further jitter)
 */
export function genesToDimensions(genes: MindGenes): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  // 6D psychology from genes
  const psych = [
    genes.entropy,                              // discovery
    genes.tension,                              // intensity
    genes.plasticity,                           // flow
    genes.resonance,                            // depth
    genes.resolution,                           // trace
    (genes.resonance + genes.plasticity) / 2,   // sharing
  ];

  // 12D cognition: split each 6D into 2 children with ±8% variation
  const cog: number[] = [];
  for (const v of psych) {
    cog.push(Math.min(1, v * 1.08), Math.max(0, v * 0.92));
  }

  // 24D neuroscience: split each 12D into 2 children with ±5% variation
  const neuro: number[] = [];
  for (const v of cog) {
    neuro.push(Math.min(1, v * 1.05), Math.max(0, v * 0.95));
  }

  return { psychology: psych, cognition: cog, neuroscience: neuro };
}

/**
 * Convert an ordered 6D array to a named DimensionProfile.
 */
export function arrayToProfile(values: number[]): DimensionProfile {
  return {
    discovery: values[0] ?? 0,
    intensity: values[1] ?? 0,
    flow:      values[2] ?? 0,
    depth:     values[3] ?? 0,
    trace:     values[4] ?? 0,
    sharing:   values[5] ?? 0,
  };
}

// =====================================================================
// LAB DIMENSIONS — Direct belief mapping (no averaging)
// Each dimension = exactly one belief value from the 131 C³ beliefs.
// Tree: 6D(experiential) → 12D(cognitive) → 24D(neural)
// =====================================================================

export interface LabDimension {
  index: number;
  key: string;
  name: string;
  nameTr: string;
  beliefIndex: number;       // index into beliefs[131]
  color: string;
  parentKey: string | null;  // parent at layer above
}

// ── 6D — "What is this music doing to you?" ────────────────────────

export const LAB_6D: LabDimension[] = [
  { index: 0, key: "harmony",   name: "Harmony",   nameTr: "Harmoni", beliefIndex: 3,  color: "#38BDF8", parentKey: null },
  { index: 1, key: "melody",    name: "Melody",    nameTr: "Melodi",  beliefIndex: 8,  color: "#EF4444", parentKey: null },
  { index: 2, key: "attention", name: "Attention", nameTr: "Dikkat",  beliefIndex: 34, color: "#22C55E", parentKey: null },
  { index: 3, key: "feeling",   name: "Feeling",   nameTr: "Duygu",   beliefIndex: 63, color: "#A855F7", parentKey: null },
  { index: 4, key: "pleasure",  name: "Pleasure",  nameTr: "Haz",     beliefIndex: 83, color: "#FBBF24", parentKey: null },
  { index: 5, key: "groove",    name: "Groove",    nameTr: "Ritim",   beliefIndex: 92, color: "#EC4899", parentKey: null },
];

// ── 12D — "How is this happening?" (2 per 6D parent) ──────────────

export const LAB_12D: LabDimension[] = [
  // harmony children
  { index: 0,  key: "stability",  name: "Stability",  nameTr: "Denge",        beliefIndex: 4,   color: "#38BDF8",   parentKey: "harmony" },
  { index: 1,  key: "intervals",  name: "Intervals",  nameTr: "Aralıklar",    beliefIndex: 6,   color: "#38BDF8B0", parentKey: "harmony" },
  // melody children
  { index: 2,  key: "contour",    name: "Contour",    nameTr: "Kontur",       beliefIndex: 2,   color: "#EF4444",   parentKey: "melody" },
  { index: 3,  key: "complexity", name: "Complexity", nameTr: "Karmaşıklık",  beliefIndex: 16,  color: "#EF4444B0", parentKey: "melody" },
  // attention children
  { index: 4,  key: "prediction", name: "Prediction", nameTr: "Öngörü",      beliefIndex: 20,  color: "#22C55E",   parentKey: "attention" },
  { index: 5,  key: "beat_lock",  name: "Beat Lock",  nameTr: "Ritim Kilidi", beliefIndex: 42,  color: "#22C55EB0", parentKey: "attention" },
  // feeling children
  { index: 6,  key: "happiness",  name: "Happiness",  nameTr: "Mutluluk",     beliefIndex: 67,  color: "#A855F7",   parentKey: "feeling" },
  { index: 7,  key: "sadness",    name: "Sadness",    nameTr: "Hüzün",        beliefIndex: 69,  color: "#A855F7B0", parentKey: "feeling" },
  // pleasure children
  { index: 8,  key: "wanting",    name: "Wanting",    nameTr: "İstek",        beliefIndex: 89,  color: "#FBBF24",   parentKey: "pleasure" },
  { index: 9,  key: "resolution", name: "Resolution", nameTr: "Çözülme",      beliefIndex: 86,  color: "#FBBF24B0", parentKey: "pleasure" },
  // groove children
  { index: 10, key: "rhythm_lock", name: "Rhythm Lock", nameTr: "Periyot Kilidi", beliefIndex: 99,  color: "#EC4899",   parentKey: "groove" },
  { index: 11, key: "sync",        name: "Sync",        nameTr: "Senkron",        beliefIndex: 122, color: "#EC4899B0", parentKey: "groove" },
];

// ── 24D — "Where in the brain?" (2 per 12D parent) ────────────────

export const LAB_24D: LabDimension[] = [
  // stability children
  { index: 0,  key: "template_match",    name: "Template Match",    nameTr: "Şablon Eşleşmesi",  beliefIndex: 5,   color: "#38BDF8",   parentKey: "stability" },
  { index: 1,  key: "consonance_map",    name: "Consonance Map",    nameTr: "Uyum Haritası",      beliefIndex: 0,   color: "#38BDF8CC", parentKey: "stability" },
  // intervals children
  { index: 2,  key: "pitch_continue",    name: "Pitch Continue",    nameTr: "Perde Devamı",       beliefIndex: 7,   color: "#38BDF899", parentKey: "intervals" },
  { index: 3,  key: "octave_equiv",      name: "Octave Equiv.",     nameTr: "Oktav Eşleniği",     beliefIndex: 9,   color: "#38BDF877", parentKey: "intervals" },
  // contour children
  { index: 4,  key: "pitch_identity",    name: "Pitch Identity",    nameTr: "Perde Kimliği",      beliefIndex: 10,  color: "#EF4444",   parentKey: "contour" },
  { index: 5,  key: "contour_continue",  name: "Contour Continue",  nameTr: "Kontur Devamı",      beliefIndex: 1,   color: "#EF4444CC", parentKey: "contour" },
  // complexity children
  { index: 6,  key: "spectral_synergy",  name: "Spectral Synergy",  nameTr: "Spektral Sinerji",   beliefIndex: 13,  color: "#EF444499", parentKey: "complexity" },
  { index: 7,  key: "valence_bridge",    name: "Mood Bridge",       nameTr: "Duygu Köprüsü",      beliefIndex: 32,  color: "#EF444477", parentKey: "complexity" },
  // prediction children
  { index: 8,  key: "abstract_future",   name: "Abstract Future",   nameTr: "Soyut Gelecek",      beliefIndex: 17,  color: "#22C55E",   parentKey: "prediction" },
  { index: 9,  key: "sensory_load",      name: "Sensory Load",      nameTr: "Duyusal Yük",        beliefIndex: 35,  color: "#22C55ECC", parentKey: "prediction" },
  // beat_lock children
  { index: 10, key: "selective_gain",    name: "Selective Gain",    nameTr: "Seçici Kazanç",      beliefIndex: 46,  color: "#22C55E99", parentKey: "beat_lock" },
  { index: 11, key: "multisensory",      name: "Multisensory",      nameTr: "Çoklu-Duyu",         beliefIndex: 108, color: "#22C55E77", parentKey: "beat_lock" },
  // happiness children
  { index: 12, key: "happy_path",        name: "Happy Pathway",     nameTr: "Mutluluk Yolu",      beliefIndex: 65,  color: "#A855F7",   parentKey: "happiness" },
  { index: 13, key: "nostalgia",         name: "Nostalgia",         nameTr: "Nostalji",            beliefIndex: 53,  color: "#A855F7CC", parentKey: "happiness" },
  // sadness children
  { index: 14, key: "nostalgia_affect",  name: "Nostalgia Affect",  nameTr: "Nostalji Etkisi",    beliefIndex: 70,  color: "#A855F799", parentKey: "sadness" },
  { index: 15, key: "memory",            name: "Memory Trace",      nameTr: "Hafıza İzi",          beliefIndex: 48,  color: "#A855F777", parentKey: "sadness" },
  // wanting children
  { index: 16, key: "tension",           name: "Tension",           nameTr: "Gerilim",             beliefIndex: 80,  color: "#FBBF24",   parentKey: "wanting" },
  { index: 17, key: "temporal_phase",    name: "Temporal Phase",    nameTr: "Zamansal Faz",        beliefIndex: 77,  color: "#FBBF24CC", parentKey: "wanting" },
  // resolution children
  { index: 18, key: "reward_forecast",   name: "Reward Forecast",   nameTr: "Ödül Tahmini",       beliefIndex: 87,  color: "#FBBF2499", parentKey: "resolution" },
  { index: 19, key: "prediction_match",  name: "Prediction Match",  nameTr: "Öngörü Eşleşmesi",  beliefIndex: 85,  color: "#FBBF2477", parentKey: "resolution" },
  // rhythm_lock children
  { index: 20, key: "medium_context",    name: "Musical Context",   nameTr: "Müzikal Bağlam",     beliefIndex: 103, color: "#EC4899",   parentKey: "rhythm_lock" },
  { index: 21, key: "motor_coupling",    name: "Motor Coupling",    nameTr: "Motor Bağlantı",     beliefIndex: 90,  color: "#EC4899CC", parentKey: "rhythm_lock" },
  // sync children
  { index: 22, key: "neural_sync",       name: "Neural Sync",       nameTr: "Nöral Senkron",      beliefIndex: 128, color: "#EC489999", parentKey: "sync" },
  { index: 23, key: "group_flow",        name: "Group Flow",        nameTr: "Grup Akışı",          beliefIndex: 123, color: "#EC489977", parentKey: "sync" },
];

/** Lab 6D color lookup */
export const LAB_6D_COLORS: Record<string, string> = {};
for (const d of LAB_6D) LAB_6D_COLORS[d.key] = d.color;

/**
 * Compute Lab dimensions from 131 belief values.
 * Each dimension = direct belief value (no averaging).
 */
export function computeLabDimensions(beliefs: number[]): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  return {
    psychology:   LAB_6D.map((d) => beliefs[d.beliefIndex] ?? 0),
    cognition:    LAB_12D.map((d) => beliefs[d.beliefIndex] ?? 0),
    neuroscience: LAB_24D.map((d) => beliefs[d.beliefIndex] ?? 0),
  };
}

/** Get Lab dimension info for a given depth and index */
export function getLabDim(depth: 6 | 12 | 24, index: number): LabDimension | undefined {
  if (depth === 6) return LAB_6D[index];
  if (depth === 12) return LAB_12D[index];
  return LAB_24D[index];
}
