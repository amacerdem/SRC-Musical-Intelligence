/* ── 12-Level Persona Evolution × 5 Family Templates ────────────────
 *  24 personas × 12 levels = 288 evolution states.
 *  Each family has a distinct visual morphology.
 *  Each persona inherits its family template + own color/name overlay.
 *  ──────────────────────────────────────────────────────────────────── */

import type { NeuralFamily } from "@/types/mind";
import type { PersonaLevel, FamilyMorphology } from "@/types/m3";

/* ── Level Visual Config ─────────────────────────────────────────── */

export interface LevelVisualConfig {
  level: PersonaLevel;
  organismStage: 1 | 2 | 3;
  tendrilCount: number;
  nucleiCount: number;
  bloomEnabled: boolean;
  chromaticEnabled: boolean;
  particleCap: number;
  breathRate: number;        // seconds per cycle
  intensity: number;         // 0-1
  /** Visual decorations */
  glowIntensity: number;     // 0-1
  colorSaturation: number;   // 0-1 (low levels = muted, high = vivid)
  hasAura: boolean;
  hasCrown: boolean;         // level 11-12 only
  hasWings: boolean;         // level 12 only
}

/** 12 levels of organism complexity — shared across all families */
export const LEVEL_VISUAL_CONFIGS: LevelVisualConfig[] = [
  // Level 1: Barely visible seed
  { level: 1,  organismStage: 1, tendrilCount: 3,  nucleiCount: 2,  bloomEnabled: false, chromaticEnabled: false, particleCap: 0,   breathRate: 8,   intensity: 0.2, glowIntensity: 0.05, colorSaturation: 0.2, hasAura: false, hasCrown: false, hasWings: false },
  // Level 2: First shoots
  { level: 2,  organismStage: 1, tendrilCount: 5,  nucleiCount: 3,  bloomEnabled: false, chromaticEnabled: false, particleCap: 5,   breathRate: 7,   intensity: 0.3, glowIntensity: 0.1,  colorSaturation: 0.3, hasAura: false, hasCrown: false, hasWings: false },
  // Level 3: Young sapling
  { level: 3,  organismStage: 1, tendrilCount: 7,  nucleiCount: 4,  bloomEnabled: false, chromaticEnabled: false, particleCap: 10,  breathRate: 6,   intensity: 0.35, glowIntensity: 0.15, colorSaturation: 0.4, hasAura: false, hasCrown: false, hasWings: false },
  // Level 4: Growing sapling
  { level: 4,  organismStage: 1, tendrilCount: 9,  nucleiCount: 4,  bloomEnabled: true,  chromaticEnabled: false, particleCap: 15,  breathRate: 5.5, intensity: 0.4, glowIntensity: 0.2,  colorSaturation: 0.5, hasAura: false, hasCrown: false, hasWings: false },
  // Level 5: Branch emerging
  { level: 5,  organismStage: 2, tendrilCount: 12, nucleiCount: 5,  bloomEnabled: true,  chromaticEnabled: false, particleCap: 25,  breathRate: 5,   intensity: 0.5, glowIntensity: 0.3,  colorSaturation: 0.6, hasAura: false, hasCrown: false, hasWings: false },
  // Level 6: Full branches
  { level: 6,  organismStage: 2, tendrilCount: 14, nucleiCount: 6,  bloomEnabled: true,  chromaticEnabled: false, particleCap: 35,  breathRate: 4.5, intensity: 0.55, glowIntensity: 0.35, colorSaturation: 0.65, hasAura: false, hasCrown: false, hasWings: false },
  // Level 7: First bloom
  { level: 7,  organismStage: 2, tendrilCount: 16, nucleiCount: 7,  bloomEnabled: true,  chromaticEnabled: false, particleCap: 50,  breathRate: 4,   intensity: 0.6, glowIntensity: 0.4,  colorSaturation: 0.7, hasAura: false, hasCrown: false, hasWings: false },
  // Level 8: Full bloom
  { level: 8,  organismStage: 2, tendrilCount: 18, nucleiCount: 8,  bloomEnabled: true,  chromaticEnabled: true,  particleCap: 60,  breathRate: 3.5, intensity: 0.7, glowIntensity: 0.5,  colorSaturation: 0.8, hasAura: false, hasCrown: false, hasWings: false },
  // Level 9: Canopy forming
  { level: 9,  organismStage: 3, tendrilCount: 20, nucleiCount: 9,  bloomEnabled: true,  chromaticEnabled: true,  particleCap: 75,  breathRate: 3.5, intensity: 0.75, glowIntensity: 0.6,  colorSaturation: 0.85, hasAura: true,  hasCrown: false, hasWings: false },
  // Level 10: Dense canopy
  { level: 10, organismStage: 3, tendrilCount: 22, nucleiCount: 10, bloomEnabled: true,  chromaticEnabled: true,  particleCap: 85,  breathRate: 3,   intensity: 0.8, glowIntensity: 0.7,  colorSaturation: 0.9, hasAura: true,  hasCrown: false, hasWings: false },
  // Level 11: Ancient presence
  { level: 11, organismStage: 3, tendrilCount: 24, nucleiCount: 11, bloomEnabled: true,  chromaticEnabled: true,  particleCap: 100, breathRate: 2.5, intensity: 0.9, glowIntensity: 0.85, colorSaturation: 0.95, hasAura: true,  hasCrown: true,  hasWings: false },
  // Level 12: Transcendent form
  { level: 12, organismStage: 3, tendrilCount: 28, nucleiCount: 12, bloomEnabled: true,  chromaticEnabled: true,  particleCap: 120, breathRate: 2,   intensity: 1.0, glowIntensity: 1.0,  colorSaturation: 1.0, hasAura: true,  hasCrown: true,  hasWings: true },
];

/* ── Family Visual Templates ─────────────────────────────────────── */

export interface FamilyLevelName {
  level: PersonaLevel;
  name: string;          // EN name for this level in this family
  nameTr: string;        // TR name
  description: string;   // Brief narrative
}

export interface FamilyVisualTemplate {
  morphology: FamilyMorphology;
  colorShift: string;    // Describes color progression (birth → maturity)
  levels: FamilyLevelName[];
}

export const FAMILY_VISUAL_TEMPLATES: Record<NeuralFamily, FamilyVisualTemplate> = {
  Alchemists: {
    morphology: "volatile",
    colorShift: "warm-to-hot",
    levels: [
      { level: 1,  name: "Ember Seed",        nameTr: "Kor Tohumu",         description: "A dim, flickering ember waiting to ignite" },
      { level: 2,  name: "First Spark",        nameTr: "İlk Kıvılcım",      description: "Sparks emerge — the first chemical reaction" },
      { level: 3,  name: "Kindling Flame",     nameTr: "Tutuşan Alev",       description: "A small but persistent fire takes hold" },
      { level: 4,  name: "Rising Fire",        nameTr: "Yükselen Ateş",      description: "The flame grows confident, feeding on new fuel" },
      { level: 5,  name: "Crucible Born",      nameTr: "Pota Doğumu",        description: "The alchemical vessel begins to glow" },
      { level: 6,  name: "Molten Core",        nameTr: "Erimiş Çekirdek",    description: "Raw transmutation — metal turns to gold" },
      { level: 7,  name: "Volatile Bloom",     nameTr: "Uçucu Çiçeklenme",   description: "Explosive beauty in transformation" },
      { level: 8,  name: "Chain Reaction",      nameTr: "Zincirleme Tepkime", description: "Each transformation triggers the next" },
      { level: 9,  name: "Elemental Storm",    nameTr: "Elementel Fırtına",   description: "All elements in furious harmony" },
      { level: 10, name: "Philosopher's Fire",  nameTr: "Filozofun Ateşi",    description: "The fire that transmutes understanding itself" },
      { level: 11, name: "Phoenix Rising",     nameTr: "Anka Yükselişi",     description: "Reborn through destruction, eternal through change" },
      { level: 12, name: "Phoenix Eternal",    nameTr: "Ebedi Anka",         description: "The flame that cannot be extinguished — pure transformation" },
    ],
  },

  Architects: {
    morphology: "crystalline",
    colorShift: "cool-to-bright",
    levels: [
      { level: 1,  name: "Crystal Seed",       nameTr: "Kristal Tohum",       description: "A single point of perfect order in the void" },
      { level: 2,  name: "First Facet",        nameTr: "İlk Yüzey",          description: "The first geometric surface catches light" },
      { level: 3,  name: "Growing Lattice",    nameTr: "Büyüyen Kafes",       description: "A structure begins to repeat and expand" },
      { level: 4,  name: "Symmetry Born",      nameTr: "Simetri Doğuşu",     description: "Mirror planes emerge — beauty in balance" },
      { level: 5,  name: "Prismatic Form",     nameTr: "Prizmatik Form",      description: "Light splits through the growing crystal" },
      { level: 6,  name: "Harmonic Matrix",    nameTr: "Harmonik Matris",     description: "Every node resonates with every other" },
      { level: 7,  name: "Perfect Structure",  nameTr: "Kusursuz Yapı",       description: "The blueprint reveals itself in full clarity" },
      { level: 8,  name: "Living Geometry",    nameTr: "Canlı Geometri",      description: "The crystal breathes — structure becomes life" },
      { level: 9,  name: "Cathedral Mind",     nameTr: "Katedral Zihin",      description: "Vast arches of thought, impossible precision" },
      { level: 10, name: "Diamond Lattice",    nameTr: "Elmas Kafesi",        description: "Unbreakable, brilliant, perfectly ordered" },
      { level: 11, name: "Celestial Grid",     nameTr: "Göksel Ağ",           description: "The architecture of the universe itself" },
      { level: 12, name: "Eternal Blueprint",  nameTr: "Ebedi Plan",          description: "The mind that contains all possible structures" },
    ],
  },

  Explorers: {
    morphology: "fluid",
    colorShift: "neon-shift",
    levels: [
      { level: 1,  name: "Chaos Seed",        nameTr: "Kaos Tohumu",         description: "A point of infinite potential, zero structure" },
      { level: 2,  name: "First Drift",        nameTr: "İlk Sürüklenme",     description: "Movement begins — no direction, all direction" },
      { level: 3,  name: "Morphing Cloud",     nameTr: "Dönüşen Bulut",      description: "Shape-shifting, never the same twice" },
      { level: 4,  name: "Current Runner",     nameTr: "Akıntı Koşucusu",    description: "Following invisible rivers of novelty" },
      { level: 5,  name: "Boundary Walker",    nameTr: "Sınır Yürüyücüsü",   description: "Testing every edge, pushing every limit" },
      { level: 6,  name: "Dimensional Shift",  nameTr: "Boyutsal Kayma",      description: "Perception bends — new dimensions open" },
      { level: 7,  name: "Neon Bloom",         nameTr: "Neon Çiçeklenme",     description: "Exploding colors in impossible combinations" },
      { level: 8,  name: "Void Dancer",        nameTr: "Boşluk Dansçısı",    description: "Dancing in the space between known and unknown" },
      { level: 9,  name: "Infinite Horizon",   nameTr: "Sonsuz Ufuk",        description: "Every direction leads to new worlds" },
      { level: 10, name: "Quantum Mind",       nameTr: "Kuantum Zihin",      description: "Existing in all states simultaneously" },
      { level: 11, name: "Cosmic Wanderer",    nameTr: "Kozmik Gezgin",      description: "The explorer of explorers — home is everywhere" },
      { level: 12, name: "Eternal Frontier",   nameTr: "Ebedi Sınır",        description: "The edge that keeps expanding — infinite novelty" },
    ],
  },

  Anchors: {
    morphology: "organic",
    colorShift: "warm-deepening",
    levels: [
      { level: 1,  name: "Heartbeat Seed",    nameTr: "Kalp Atışı Tohumu",   description: "The first emotional pulse, barely audible" },
      { level: 2,  name: "First Warmth",       nameTr: "İlk Sıcaklık",       description: "A gentle warmth begins to spread" },
      { level: 3,  name: "Root Tendril",       nameTr: "Kök Filizi",          description: "Reaching down into memory, finding ground" },
      { level: 4,  name: "Deep Root",          nameTr: "Derin Kök",           description: "Anchored — the foundation grows strong" },
      { level: 5,  name: "Memory Bloom",       nameTr: "Hafıza Çiçeği",      description: "Memories begin to flower into feeling" },
      { level: 6,  name: "Empathy Weave",      nameTr: "Empati Örgüsü",      description: "Connecting emotions across time and space" },
      { level: 7,  name: "Golden Heart",       nameTr: "Altın Kalp",          description: "The emotional core glows with accumulated warmth" },
      { level: 8,  name: "Living Memory",      nameTr: "Canlı Hafıza",       description: "Every moment preserved in amber light" },
      { level: 9,  name: "Ancient Root",       nameTr: "Kadim Kök",           description: "Roots deeper than time, wider than the self" },
      { level: 10, name: "Wisdom Well",        nameTr: "Bilgelik Kuyusu",    description: "Drawing from the deepest wells of experience" },
      { level: 11, name: "Eternal Garden",     nameTr: "Ebedi Bahçe",        description: "A garden that grows from every memory ever held" },
      { level: 12, name: "Soul Tree",          nameTr: "Ruh Ağacı",          description: "The tree that holds all hearts — infinite empathy" },
    ],
  },

  Kineticists: {
    morphology: "rhythmic",
    colorShift: "warm-to-electric",
    levels: [
      { level: 1,  name: "Pulse Seed",        nameTr: "Nabız Tohumu",        description: "The first beat — a heartbeat in the dark" },
      { level: 2,  name: "First Beat",         nameTr: "İlk Vuruş",          description: "A rhythm emerges from silence" },
      { level: 3,  name: "Sync Pulse",         nameTr: "Senkron Nabız",      description: "Beginning to lock in — body and beat as one" },
      { level: 4,  name: "Groove Lock",        nameTr: "Ritim Kilidi",        description: "The pocket found — deep in the groove" },
      { level: 5,  name: "Kinetic Burst",      nameTr: "Kinetik Patlama",    description: "Energy explodes outward in rhythmic waves" },
      { level: 6,  name: "Polyrhythm",         nameTr: "Poliritem",           description: "Multiple rhythms, one unified motion" },
      { level: 7,  name: "Thunder Bloom",      nameTr: "Gök Gürültüsü",     description: "The bloom of pure physical power" },
      { level: 8,  name: "Perpetual Motion",   nameTr: "Sürekli Hareket",    description: "Energy that feeds itself — unstoppable" },
      { level: 9,  name: "Orbital Drive",      nameTr: "Yörünge Sürüşü",    description: "Orbiting the beat like planets around a star" },
      { level: 10, name: "Supernova Pulse",    nameTr: "Süpernova Nabzı",    description: "Every pulse creates a shockwave of energy" },
      { level: 11, name: "Cosmic Rhythm",      nameTr: "Kozmik Ritim",       description: "Synchronized with the heartbeat of the universe" },
      { level: 12, name: "Eternal Engine",     nameTr: "Ebedi Motor",        description: "The rhythm that drives all motion — pure kinesis" },
    ],
  },
};

/* ── Helpers ──────────────────────────────────────────────────────── */

/** Get the visual config for a given level */
export function getLevelVisualConfig(level: PersonaLevel): LevelVisualConfig {
  return LEVEL_VISUAL_CONFIGS[level - 1];
}

/** Get the family template for a given family */
export function getFamilyTemplate(family: NeuralFamily): FamilyVisualTemplate {
  return FAMILY_VISUAL_TEMPLATES[family];
}

/** Get the level name for a specific family and level */
export function getLevelName(family: NeuralFamily, level: PersonaLevel): FamilyLevelName {
  return FAMILY_VISUAL_TEMPLATES[family].levels[level - 1];
}

/** Get the family morphology string */
export function getFamilyMorphology(family: NeuralFamily): FamilyMorphology {
  return FAMILY_VISUAL_TEMPLATES[family].morphology;
}

/** All 5 family colors (primary) for the affinity ring */
export const FAMILY_COLORS: Record<NeuralFamily, string> = {
  Alchemists:  "#A855F7",  // Purple
  Architects:  "#38BDF8",  // Sky blue
  Explorers:   "#84CC16",  // Lime/Neon
  Anchors:     "#FBBF24",  // Amber
  Kineticists: "#EF4444",  // Red
};
