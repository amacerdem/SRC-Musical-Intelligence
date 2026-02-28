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
