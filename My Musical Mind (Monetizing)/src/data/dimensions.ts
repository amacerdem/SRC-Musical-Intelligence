/* ── Dimension System — 6D + 12D + 24D Independent Tiers ──────────────
 *  Ported from Musical_Intelligence/brain/dimensions/ (Python backend).
 *  Each tier is independently computed from 131 C³ beliefs via weighted sums.
 *  NO tier derives from another tier's output.
 *
 *  6D  Psychology    (experiential, free tier)
 *  12D Cognition     (music cognition, basic tier)
 *  24D Neuroscience  (neural, premium tier)
 *
 *  Display groupings (parentKey) provide drill-down structure for UI
 *  but do NOT affect computation.
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
  beliefIndices: number[];     // indices into beliefs[131]
  color: string;
  parentKey: string | null;    // display parent for UI drill-down
}

// =====================================================================
// 24D — NEUROSCIENCE LAYER (leaf level, each a weighted sum of beliefs)
// 6 domains × 4 parameters
// parentKey = 12D display-parent for sunburst/panel drill-down
// =====================================================================

export const ALL_NEUROSCIENCE: LabDimension[] = [
  // Predictive Processing (0-3)
  { index: 0,  key: "prediction_error",     name: "Prediction Error",  nameTr: "Tahmin Hatas\u0131",       beliefIndices: [25, 34, 84],             color: "#38BDF8",   parentKey: "melodic_hook" },
  { index: 1,  key: "precision",            name: "Precision",         nameTr: "Hassasiyet",           beliefIndices: [20, 39, 46],             color: "#38BDF8CC", parentKey: "harmonic_depth" },
  { index: 2,  key: "information_content",  name: "Information",       nameTr: "Bilgi \u0130\u00e7eri\u011fi",     beliefIndices: [25],                     color: "#38BDF899", parentKey: "surprise" },
  { index: 3,  key: "model_uncertainty",    name: "Uncertainty",       nameTr: "Belirsizlik",          beliefIndices: [20, 31, 46],             color: "#38BDF877", parentKey: "harmonic_depth" },
  // Sensorimotor (4-7)
  { index: 4,  key: "oscillation_coupling", name: "Beat Coupling",     nameTr: "Ritim Ba\u011f\u0131",          beliefIndices: [42, 44],                 color: "#22C55E",   parentKey: "rhythmic_drive" },
  { index: 5,  key: "motor_period_lock",    name: "Period Lock",       nameTr: "Periyot Kilidi",       beliefIndices: [96, 98, 99],             color: "#22C55ECC", parentKey: "rhythmic_drive" },
  { index: 6,  key: "auditory_motor_bind",  name: "Motor Binding",     nameTr: "Motor Ba\u011flama",         beliefIndices: [90, 92, 95, 99],         color: "#22C55E99", parentKey: "timbral_color" },
  { index: 7,  key: "timing_precision",     name: "Timing",            nameTr: "Zamanlama",            beliefIndices: [100],                    color: "#22C55E77", parentKey: "timbral_color" },
  // Emotion Circuitry (8-11)
  { index: 8,  key: "valence_mode",         name: "Valence Mode",      nameTr: "Duygu Modu",           beliefIndices: [66, 67, 68],             color: "#A855F7",   parentKey: "emotional_arc" },
  { index: 9,  key: "autonomic_arousal",    name: "ANS Arousal",       nameTr: "Otonom Uyar\u0131lma",      beliefIndices: [35, 60, 63],             color: "#A855F7CC", parentKey: "emotional_arc" },
  { index: 10, key: "nostalgia_circuit",    name: "Nostalgia",         nameTr: "Nostalji",             beliefIndices: [50, 53, 55, 70],         color: "#A855F799", parentKey: "narrative" },
  { index: 11, key: "chills_pathway",       name: "Chills",            nameTr: "T\u00fcylenme",             beliefIndices: [60, 61, 62, 79, 83],     color: "#A855F777", parentKey: "pleasure" },
  // Reward System (12-15)
  { index: 12, key: "da_anticipation",      name: "DA Anticipation",   nameTr: "DA Beklenti",          beliefIndices: [74, 77, 78],             color: "#F59E0B",   parentKey: "momentum" },
  { index: 13, key: "da_consummation",      name: "DA Consummation",   nameTr: "DA T\u00fcketim",           beliefIndices: [74, 75, 83, 89],         color: "#F59E0BCC", parentKey: "momentum" },
  { index: 14, key: "hedonic_tone",         name: "Hedonic Tone",      nameTr: "Hedonik Ton",          beliefIndices: [40, 61, 81, 83],         color: "#F59E0B99", parentKey: "pleasure" },
  { index: 15, key: "reward_pe",            name: "Reward PE",         nameTr: "\u00d6d\u00fcl TH",              beliefIndices: [75, 84, 85],             color: "#F59E0B77", parentKey: "surprise" },
  // Memory & Learning (16-19)
  { index: 16, key: "episodic_encoding",    name: "Episodic Memory",   nameTr: "Epizodik Haf\u0131za",      beliefIndices: [51, 57, 59],             color: "#FBBF24",   parentKey: "melodic_hook" },
  { index: 17, key: "autobiographical",     name: "Life Story",        nameTr: "Ya\u015fam \u00d6yk\u00fcs\u00fc",       beliefIndices: [50, 51, 55],             color: "#FBBF24CC", parentKey: "narrative" },
  { index: 18, key: "statistical_learning", name: "Pattern Learning",  nameTr: "\u00d6r\u00fcnt\u00fc \u00d6\u011frenme",    beliefIndices: [20, 31, 109],            color: "#FBBF2499", parentKey: "familiarity" },
  { index: 19, key: "expertise_effect",     name: "Expertise",         nameTr: "Uzmanl\u0131k",             beliefIndices: [111, 114, 119, 120],     color: "#FBBF2477", parentKey: "familiarity" },
  // Social Cognition (20-23)
  { index: 20, key: "neural_synchrony",     name: "Neural Sync",       nameTr: "N\u00f6ral Senkron",        beliefIndices: [122, 128],               color: "#EC4899",   parentKey: "space" },
  { index: 21, key: "social_bonding",       name: "Social Bond",       nameTr: "Sosyal Ba\u011f",           beliefIndices: [55, 123, 124, 126],      color: "#EC4899CC", parentKey: "space" },
  { index: 22, key: "social_prediction",    name: "Social Prediction", nameTr: "Sosyal Tahmin",        beliefIndices: [122, 125, 130],          color: "#EC489999", parentKey: "repetition" },
  { index: 23, key: "collective_reward",    name: "Collective Joy",    nameTr: "Kolektif \u00d6d\u00fcl",        beliefIndices: [83, 121, 126],           color: "#EC489977", parentKey: "repetition" },
];

// =====================================================================
// 12D — COGNITION LAYER (each a weighted sum of beliefs)
// parentKey = 6D display-parent for UI drill-down
// =====================================================================

export const ALL_COGNITION: LabDimension[] = [
  { index: 0,  key: "melodic_hook",   name: "Melody",      nameTr: "Melodi",     beliefIndices: [8, 10, 13, 47, 48],        color: "#38BDF8",   parentKey: "groove" },
  { index: 1,  key: "harmonic_depth", name: "Harmony",     nameTr: "Armoni",     beliefIndices: [4, 5, 6, 21, 80],          color: "#F59E0B",   parentKey: "tension" },
  { index: 2,  key: "rhythmic_drive", name: "Rhythm",      nameTr: "Ritim",      beliefIndices: [42, 44, 90, 92, 94],       color: "#22C55E",   parentKey: "tempo" },
  { index: 3,  key: "timbral_color",  name: "Timbre",      nameTr: "T\u0131n\u0131",       beliefIndices: [11, 13, 15, 16, 111],      color: "#EF4444",   parentKey: "energy" },
  { index: 4,  key: "emotional_arc",  name: "Emotion",     nameTr: "Duygu",      beliefIndices: [63, 64, 67, 68, 70],       color: "#A855F7",   parentKey: "valence" },
  { index: 5,  key: "surprise",       name: "Surprise",    nameTr: "S\u00fcrpriz",    beliefIndices: [21, 25, 75, 84],           color: "#F59E0BCC", parentKey: "tension" },
  { index: 6,  key: "momentum",       name: "Momentum",    nameTr: "\u0130vme",        beliefIndices: [78, 79, 82, 88, 89],       color: "#38BDF8CC", parentKey: "groove" },
  { index: 7,  key: "narrative",      name: "Story",       nameTr: "Hikaye",     beliefIndices: [17, 58, 101, 104, 106],    color: "#EC4899",   parentKey: "complexity" },
  { index: 8,  key: "familiarity",    name: "Familiarity", nameTr: "Tan\u0131d\u0131kl\u0131k", beliefIndices: [20, 31, 51, 54, 109],      color: "#EC4899CC", parentKey: "complexity" },
  { index: 9,  key: "pleasure",       name: "Pleasure",    nameTr: "Haz",        beliefIndices: [74, 75, 81, 83, 89],       color: "#A855F7CC", parentKey: "valence" },
  { index: 10, key: "space",          name: "Space",       nameTr: "Mekan",      beliefIndices: [13, 16, 35, 36, 60],       color: "#EF4444CC", parentKey: "energy" },
  { index: 11, key: "repetition",     name: "Repetition",  nameTr: "Tekrar",     beliefIndices: [20, 25, 31, 85],           color: "#22C55ECC", parentKey: "tempo" },
];

// =====================================================================
// 6D — PSYCHOLOGY LAYER (gut-level experiential dimensions)
// =====================================================================

export const ALL_PSYCHOLOGY: LabDimension[] = [
  { index: 0, key: "energy",     name: "Energy",   nameTr: "Enerji",     beliefIndices: [16, 34, 35, 63],       color: "#EF4444", parentKey: null },
  { index: 1, key: "valence",    name: "Valence",  nameTr: "Duygu Tonu", beliefIndices: [4, 67, 68, 81, 89],    color: "#A855F7", parentKey: null },
  { index: 2, key: "tempo",      name: "Tempo",    nameTr: "H\u0131z",        beliefIndices: [42, 95, 98],           color: "#22C55E", parentKey: null },
  { index: 3, key: "tension",    name: "Tension",  nameTr: "Gerilim",    beliefIndices: [34, 60, 63, 80, 88],   color: "#F59E0B", parentKey: null },
  { index: 4, key: "groove",     name: "Groove",   nameTr: "Hareket",    beliefIndices: [42, 90, 92, 95, 99],   color: "#38BDF8", parentKey: null },
  { index: 5, key: "complexity", name: "Density",  nameTr: "Yo\u011funluk",   beliefIndices: [16, 35, 36, 101],      color: "#EC4899", parentKey: null },
];

// =====================================================================
// Display-group lookups (for UI drill-down, NOT computation)
// =====================================================================

/** 6D key → its 12D display children */
export const COGNITION_DISPLAY_GROUPS: Record<string, LabDimension[]> = {};
for (const psych of ALL_PSYCHOLOGY) {
  COGNITION_DISPLAY_GROUPS[psych.key] = ALL_COGNITION.filter(
    (c) => c.parentKey === psych.key,
  );
}

/** 12D key → its 24D display children */
export const NEUROSCIENCE_DISPLAY_GROUPS: Record<string, LabDimension[]> = {};
for (const cog of ALL_COGNITION) {
  NEUROSCIENCE_DISPLAY_GROUPS[cog.key] = ALL_NEUROSCIENCE.filter(
    (n) => n.parentKey === cog.key,
  );
}

// =====================================================================
// Color & name lookups
// =====================================================================

/** 6D key → color */
export const PSYCHOLOGY_COLORS: Record<string, string> = {};
for (const d of ALL_PSYCHOLOGY) PSYCHOLOGY_COLORS[d.key] = d.color;

export const PSYCHOLOGY_NAMES: string[] = ALL_PSYCHOLOGY.map((d) => d.name);
export const PSYCHOLOGY_NAMES_TR: string[] = ALL_PSYCHOLOGY.map((d) => d.nameTr);
export const COGNITION_NAMES: string[] = ALL_COGNITION.map((d) => d.name);
export const NEUROSCIENCE_NAMES: string[] = ALL_NEUROSCIENCE.map((d) => d.name);

// =====================================================================
// Dimension computation — independent weighted sums from beliefs
// Ported from Musical_Intelligence/brain/dimensions/models/*.py
// =====================================================================

/** Clamp value to [0, 1] */
function clamp01(v: number): number {
  return Math.max(0, Math.min(1, v));
}

/** Safe belief accessor */
function b(beliefs: number[], i: number): number {
  return beliefs[i] ?? 0;
}

// ── 6D Psychology (from models/psychology.py) ──────────────────────

function computeEnergy(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 34) + 0.25 * b(beliefs, 63) +
    0.25 * b(beliefs, 35) + 0.25 * b(beliefs, 16),
  );
}

function computeValence(beliefs: number[]): number {
  const mood =
    0.30 * b(beliefs, 67) - 0.20 * b(beliefs, 68) +
    0.15 * b(beliefs, 4) + 0.15 * b(beliefs, 89) +
    0.10 * b(beliefs, 81);
  return clamp01(mood + 0.20);
}

function computeTempo(beliefs: number[]): number {
  return clamp01(
    0.40 * b(beliefs, 98) + 0.30 * b(beliefs, 42) +
    0.30 * b(beliefs, 95),
  );
}

function computeTension(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 88) + 0.20 * b(beliefs, 63) +
    0.20 * b(beliefs, 80) + 0.15 * b(beliefs, 60) +
    0.15 * b(beliefs, 34),
  );
}

function computeGroove(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 92) + 0.20 * b(beliefs, 42) +
    0.20 * b(beliefs, 90) + 0.15 * b(beliefs, 95) +
    0.15 * b(beliefs, 99),
  );
}

function computeComplexity(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 16) + 0.25 * b(beliefs, 101) +
    0.25 * b(beliefs, 35) + 0.20 * b(beliefs, 36),
  );
}

// ── 12D Cognition (from models/cognition.py) ──────────────────────

function computeMelodicHook(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 8) + 0.20 * b(beliefs, 10) +
    0.25 * b(beliefs, 48) + 0.15 * b(beliefs, 47) +
    0.15 * b(beliefs, 13),
  );
}

function computeHarmonicDepth(beliefs: number[]): number {
  return clamp01(
    0.25 * (1.0 - b(beliefs, 4)) + 0.20 * (1.0 - b(beliefs, 5)) +
    0.20 * b(beliefs, 6) + 0.15 * b(beliefs, 80) +
    0.20 * b(beliefs, 21),
  );
}

function computeRhythmicDrive(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 42) + 0.20 * b(beliefs, 44) +
    0.20 * b(beliefs, 94) + 0.20 * b(beliefs, 90) +
    0.15 * b(beliefs, 92),
  );
}

function computeTimbre(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 15) + 0.20 * b(beliefs, 16) +
    0.15 * b(beliefs, 11) + 0.15 * b(beliefs, 111) +
    0.20 * b(beliefs, 13),
  );
}

function computeEmotionalArc(beliefs: number[]): number {
  const happy = b(beliefs, 67);
  const sad = b(beliefs, 68);
  const nostalgia = b(beliefs, 70);
  const emoMax = Math.max(Math.max(happy, sad), nostalgia);
  return clamp01(
    0.30 * emoMax + 0.25 * b(beliefs, 63) +
    0.20 * b(beliefs, 64) + 0.25 * nostalgia,
  );
}

function computeSurprise(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 84) + 0.25 * b(beliefs, 25) +
    0.20 * b(beliefs, 75) + 0.25 * b(beliefs, 21),
  );
}

function computeMomentum(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 88) + 0.20 * b(beliefs, 82) +
    0.20 * b(beliefs, 79) + 0.15 * b(beliefs, 89) +
    0.20 * b(beliefs, 78),
  );
}

function computeNarrative(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 101) + 0.20 * b(beliefs, 106) +
    0.20 * b(beliefs, 104) + 0.15 * b(beliefs, 58) +
    0.20 * b(beliefs, 17),
  );
}

function computeFamiliarity(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 31) + 0.25 * b(beliefs, 20) +
    0.20 * b(beliefs, 109) + 0.15 * b(beliefs, 54) +
    0.15 * b(beliefs, 51),
  );
}

function computePleasure(beliefs: number[]): number {
  return clamp01(
    0.20 * b(beliefs, 89) + 0.20 * b(beliefs, 81) +
    0.20 * b(beliefs, 83) + 0.20 * b(beliefs, 75) +
    0.20 * b(beliefs, 74),
  );
}

function computeSpace(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 16) + 0.20 * b(beliefs, 35) +
    0.15 * b(beliefs, 36) + 0.20 * b(beliefs, 13) +
    0.20 * b(beliefs, 60),
  );
}

function computeRepetition(beliefs: number[]): number {
  const infoInv = 1.0 - b(beliefs, 25);
  return clamp01(
    0.30 * b(beliefs, 85) + 0.25 * b(beliefs, 20) +
    0.25 * b(beliefs, 31) + 0.20 * infoInv,
  );
}

// ── 24D Neuroscience (from models/neuroscience.py) ────────────────

function computePredictionError(beliefs: number[]): number {
  return clamp01(0.40 * b(beliefs, 84) + 0.25 * b(beliefs, 25) + 0.35 * b(beliefs, 34));
}
function computePrecision(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 39) + 0.30 * b(beliefs, 20) + 0.35 * b(beliefs, 46));
}
function computeInformationContent(beliefs: number[]): number {
  return clamp01(b(beliefs, 25));
}
function computeModelUncertainty(beliefs: number[]): number {
  return clamp01(
    0.40 * (1.0 - b(beliefs, 20)) + 0.35 * (1.0 - b(beliefs, 31)) +
    0.25 * (1.0 - b(beliefs, 46)),
  );
}
function computeOscillationCoupling(beliefs: number[]): number {
  return clamp01(0.55 * b(beliefs, 42) + 0.45 * b(beliefs, 44));
}
function computeMotorPeriodLock(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 98) + 0.30 * b(beliefs, 96) + 0.35 * b(beliefs, 99));
}
function computeAuditoryMotorBind(beliefs: number[]): number {
  return clamp01(
    0.35 * b(beliefs, 90) + 0.25 * b(beliefs, 95) +
    0.20 * b(beliefs, 99) + 0.20 * b(beliefs, 92),
  );
}
function computeTimingPrecision(beliefs: number[]): number {
  return clamp01(b(beliefs, 100));
}
function computeValenceMode(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 67) + 0.30 * b(beliefs, 68) + 0.35 * b(beliefs, 66));
}
function computeAutonomicArousal(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 60) + 0.30 * b(beliefs, 63) + 0.35 * b(beliefs, 35));
}
function computeNostalgiaCircuit(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 53) + 0.25 * b(beliefs, 70) +
    0.25 * b(beliefs, 50) + 0.25 * b(beliefs, 55),
  );
}
function computeChillsPathway(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 61) + 0.20 * b(beliefs, 79) +
    0.20 * b(beliefs, 60) + 0.15 * b(beliefs, 62) +
    0.20 * b(beliefs, 83),
  );
}
function computeDaAnticipation(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 74) + 0.30 * b(beliefs, 78) + 0.35 * b(beliefs, 77));
}
function computeDaConsummation(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 75) + 0.25 * b(beliefs, 89) +
    0.25 * b(beliefs, 83) + 0.20 * b(beliefs, 74),
  );
}
function computeHedonicTone(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 81) + 0.25 * b(beliefs, 83) +
    0.20 * b(beliefs, 61) + 0.25 * b(beliefs, 40),
  );
}
function computeRewardPE(beliefs: number[]): number {
  const pe = b(beliefs, 84);
  const match = b(beliefs, 85);
  const rpe = pe * (1.0 - match);
  return clamp01(0.40 * rpe + 0.25 * pe + 0.35 * b(beliefs, 75));
}
function computeEpisodicEncoding(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 59) + 0.30 * b(beliefs, 57) + 0.35 * b(beliefs, 51));
}
function computeAutobiographical(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 50) + 0.30 * b(beliefs, 55) + 0.35 * b(beliefs, 51));
}
function computeStatisticalLearning(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 109) + 0.30 * b(beliefs, 31) + 0.35 * b(beliefs, 20));
}
function computeExpertiseEffect(beliefs: number[]): number {
  return clamp01(
    0.30 * b(beliefs, 114) + 0.25 * b(beliefs, 119) +
    0.25 * b(beliefs, 120) + 0.20 * b(beliefs, 111),
  );
}
function computeNeuralSynchrony(beliefs: number[]): number {
  return clamp01(0.60 * b(beliefs, 128) + 0.40 * b(beliefs, 122));
}
function computeSocialBonding(beliefs: number[]): number {
  return clamp01(
    0.25 * b(beliefs, 124) + 0.25 * b(beliefs, 123) +
    0.25 * b(beliefs, 55) + 0.25 * b(beliefs, 126),
  );
}
function computeSocialPrediction(beliefs: number[]): number {
  return clamp01(0.35 * b(beliefs, 125) + 0.35 * b(beliefs, 130) + 0.30 * b(beliefs, 122));
}
function computeCollectiveReward(beliefs: number[]): number {
  return clamp01(0.30 * b(beliefs, 126) + 0.35 * b(beliefs, 121) + 0.35 * b(beliefs, 83));
}

// =====================================================================
// computeDimensions — independent weighted sums, all 42 dimensions
// =====================================================================

/**
 * Compute all three dimension layers from 131 belief values.
 * Each dimension is an independent weighted sum (no tier derives from another).
 */
export function computeDimensions(beliefs: number[]): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  const psychology = [
    computeEnergy(beliefs),       // 0
    computeValence(beliefs),      // 1
    computeTempo(beliefs),        // 2
    computeTension(beliefs),      // 3
    computeGroove(beliefs),       // 4
    computeComplexity(beliefs),   // 5
  ];

  const cognition = [
    computeMelodicHook(beliefs),     // 0
    computeHarmonicDepth(beliefs),   // 1
    computeRhythmicDrive(beliefs),   // 2
    computeTimbre(beliefs),          // 3
    computeEmotionalArc(beliefs),    // 4
    computeSurprise(beliefs),        // 5
    computeMomentum(beliefs),        // 6
    computeNarrative(beliefs),       // 7
    computeFamiliarity(beliefs),     // 8
    computePleasure(beliefs),        // 9
    computeSpace(beliefs),           // 10
    computeRepetition(beliefs),      // 11
  ];

  const neuroscience = [
    computePredictionError(beliefs),     // 0
    computePrecision(beliefs),           // 1
    computeInformationContent(beliefs),  // 2
    computeModelUncertainty(beliefs),    // 3
    computeOscillationCoupling(beliefs), // 4
    computeMotorPeriodLock(beliefs),     // 5
    computeAuditoryMotorBind(beliefs),   // 6
    computeTimingPrecision(beliefs),     // 7
    computeValenceMode(beliefs),         // 8
    computeAutonomicArousal(beliefs),    // 9
    computeNostalgiaCircuit(beliefs),    // 10
    computeChillsPathway(beliefs),       // 11
    computeDaAnticipation(beliefs),      // 12
    computeDaConsummation(beliefs),      // 13
    computeHedonicTone(beliefs),         // 14
    computeRewardPE(beliefs),            // 15
    computeEpisodicEncoding(beliefs),    // 16
    computeAutobiographical(beliefs),    // 17
    computeStatisticalLearning(beliefs), // 18
    computeExpertiseEffect(beliefs),     // 19
    computeNeuralSynchrony(beliefs),     // 20
    computeSocialBonding(beliefs),       // 21
    computeSocialPrediction(beliefs),    // 22
    computeCollectiveReward(beliefs),    // 23
  ];

  return { psychology, cognition, neuroscience };
}

// Alias for backward compat with Lab store
export const computeLabDimensions = computeDimensions;

// =====================================================================
// Profile conversion helpers
// =====================================================================

/**
 * Convert a DimensionProfile (named 6D object) to an ordered array.
 */
export function profileToArray(profile: DimensionProfile): number[] {
  return [
    profile.energy,
    profile.valence,
    profile.tempo,
    profile.tension,
    profile.groove,
    profile.complexity,
  ];
}

/**
 * Convert an ordered 6D array to a named DimensionProfile.
 */
export function arrayToProfile(values: number[]): DimensionProfile {
  return {
    energy:     values[0] ?? 0,
    valence:    values[1] ?? 0,
    tempo:      values[2] ?? 0,
    tension:    values[3] ?? 0,
    groove:     values[4] ?? 0,
    complexity: values[5] ?? 0,
  };
}

// =====================================================================
// Gene → Dimension mapping (fallback when beliefs haven't accumulated)
// =====================================================================

/**
 * Derive 6D psychological dimensions from the user's 5-gene DNA profile.
 * Multi-gene weighted formulas: each dimension blends multiple genes.
 *
 * Mapping rationale:
 *   energy:     tension + entropy + plasticity (intense, dense, active music)
 *   valence:    resonance + plasticity + resolution (emotional positivity/depth)
 *   tempo:      plasticity + entropy + tension (speed/motor sensitivity)
 *   tension:    tension + entropy + resonance (strain tolerance)
 *   groove:     plasticity + resonance + tension (body movement + emotional engagement)
 *   complexity: entropy + resolution + tension (density tolerance + pattern processing)
 */
export function genesToDimensions(genes: MindGenes): {
  psychology: number[];
  cognition: number[];
  neuroscience: number[];
} {
  const psych = [
    clamp01(0.40 * genes.tension + 0.30 * genes.entropy + 0.30 * genes.plasticity),       // energy
    clamp01(0.50 * genes.resonance + 0.25 * genes.plasticity + 0.25 * genes.resolution),   // valence
    clamp01(0.45 * genes.plasticity + 0.30 * genes.entropy + 0.25 * genes.tension),        // tempo
    clamp01(0.50 * genes.tension + 0.25 * genes.entropy + 0.25 * genes.resonance),         // tension
    clamp01(0.45 * genes.plasticity + 0.30 * genes.resonance + 0.25 * genes.tension),      // groove
    clamp01(0.45 * genes.entropy + 0.35 * genes.resolution + 0.20 * genes.tension),        // complexity
  ];

  // 12D: split each 6D into 2 children with slight variation
  const cog: number[] = [];
  for (const v of psych) {
    cog.push(clamp01(v * 1.08), clamp01(v * 0.92));
  }

  // 24D: split each 12D into 2 children with slight variation
  const neuro: number[] = [];
  for (const v of cog) {
    neuro.push(clamp01(v * 1.05), clamp01(v * 0.95));
  }

  return { psychology: psych, cognition: cog, neuroscience: neuro };
}

/** Get dimension info for a given depth and index */
export function getLabDim(depth: 6 | 12 | 24, index: number): LabDimension | undefined {
  if (depth === 6) return ALL_PSYCHOLOGY[index];
  if (depth === 12) return ALL_COGNITION[index];
  return ALL_NEUROSCIENCE[index];
}

// =====================================================================
// ACOUSTIC DIMENSIONS — Direct R3 perceptual signals (unchanged)
// =====================================================================

export interface AcousticDimension {
  index: number;
  key: string;
  name: string;
  nameTr: string;
  r3Index: number;
  color: string;
}

export const ACOUSTIC_R3_6D  = [10, 7, 0, 61, 21, 51];
export const ACOUSTIC_R3_12D = [...ACOUSTIC_R3_6D, 12, 39, 37, 11, 22, 93];
export const ACOUSTIC_R3_24D = [...ACOUSTIC_R3_12D, 4, 3, 17, 14, 59, 5, 23, 95, 60, 91, 94, 16];

const ALL_ACOUSTIC: AcousticDimension[] = [
  // 6D Essential Sound
  { index: 0,  key: "loudness",     name: "Loudness",      nameTr: "G\u00fcrl\u00fck",         r3Index: 10, color: "#FF6B35" },
  { index: 1,  key: "power",        name: "Power",         nameTr: "G\u00fc\u00e7",            r3Index: 7,  color: "#FFD166" },
  { index: 2,  key: "roughness",    name: "Roughness",     nameTr: "P\u00fcr\u00fcz",          r3Index: 0,  color: "#06D6A0" },
  { index: 3,  key: "tonality",     name: "Tonality",      nameTr: "Tonalite",       r3Index: 61, color: "#118AB2" },
  { index: 4,  key: "movement",     name: "Movement",      nameTr: "Hareket",        r3Index: 21, color: "#EF476F" },
  { index: 5,  key: "harmony",      name: "Harmony",       nameTr: "Harmoni",        r3Index: 51, color: "#7209B7" },
  // +6 → 12D Detailed Sound
  { index: 6,  key: "warmth",       name: "Warmth",        nameTr: "S\u0131cakl\u0131k",       r3Index: 12, color: "#FF8C61" },
  { index: 7,  key: "clarity",      name: "Clarity",       nameTr: "Netlik",         r3Index: 39, color: "#73D2DE" },
  { index: 8,  key: "pitch",        name: "Pitch",         nameTr: "Perde",          r3Index: 37, color: "#B388EB" },
  { index: 9,  key: "attack",       name: "Attack",        nameTr: "Atak",           r3Index: 11, color: "#FF4365" },
  { index: 10, key: "richness",     name: "Richness",      nameTr: "Zenginlik",      r3Index: 22, color: "#88D498" },
  { index: 11, key: "perceived_vol",name: "Perceived Vol",  nameTr: "Alg\u0131lanan Ses", r3Index: 93, color: "#F0C987" },
  // +12 → 24D Full Analysis
  { index: 12, key: "consonance",    name: "Consonance",    nameTr: "Uyum",           r3Index: 4,  color: "#FF9F43" },
  { index: 13, key: "fusion",        name: "Fusion",        nameTr: "Kayna\u015fma",       r3Index: 3,  color: "#45B7D1" },
  { index: 14, key: "harmonicity",   name: "Harmonicity",   nameTr: "Harmoniklik",    r3Index: 17, color: "#9B59B6" },
  { index: 15, key: "tonalness",     name: "Tonalness",     nameTr: "Tonallik",       r3Index: 14, color: "#E17055" },
  { index: 16, key: "chord_flow",    name: "Chord Flow",    nameTr: "Akor Ak\u0131\u015f\u0131",     r3Index: 59, color: "#2ECC71" },
  { index: 17, key: "inharmonicity", name: "Inharmonicity", nameTr: "\u0130nharmoniklik",  r3Index: 5,  color: "#F368E0" },
  { index: 18, key: "evenness",      name: "Evenness",      nameTr: "D\u00fczg\u00fcnl\u00fck",      r3Index: 23, color: "#FFA07A" },
  { index: 19, key: "voice_quality", name: "Voice Quality", nameTr: "Ses Kalitesi",   r3Index: 95, color: "#20B2AA" },
  { index: 20, key: "stability",     name: "Stability",     nameTr: "Kararl\u0131l\u0131k",     r3Index: 60, color: "#C39BD3" },
  { index: 21, key: "sharpness",     name: "Sharpness",     nameTr: "Keskinlik",      r3Index: 91, color: "#EB984E" },
  { index: 22, key: "bass_weight",   name: "Bass Weight",   nameTr: "Bas A\u011f\u0131rl\u0131\u011f\u0131",   r3Index: 94, color: "#5DADE2" },
  { index: 23, key: "smoothness",    name: "Smoothness",    nameTr: "P\u00fcr\u00fczs\u00fczl\u00fck",    r3Index: 16, color: "#58D68D" },
];

export const ALL_ACOUSTIC_6D:  AcousticDimension[] = ALL_ACOUSTIC.slice(0, 6);
export const ALL_ACOUSTIC_12D: AcousticDimension[] = ALL_ACOUSTIC.slice(0, 12);
export const ALL_ACOUSTIC_24D: AcousticDimension[] = ALL_ACOUSTIC;
