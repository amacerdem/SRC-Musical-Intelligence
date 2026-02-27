/* ── M³ Mind Types ────────────────────────────────────────────── */

/** Neural Families (The Synaptic Pentad) */
export type NeuralFamily =
  | "Architects"   // Structure / Order (Blue)
  | "Alchemists"   // Transformation / Tension (Purple)
  | "Explorers"    // Novelty / Chaos (Neon)
  | "Anchors"      // Emotion / Memory (Amber)
  | "Kineticists"; // Drive / Rhythm (Red)

export type Rarity = "Common" | "Rare" | "Legendary" | "Anomalous";

/** Focus Artifact: A reward object bridging digital and real worlds */
export interface FocusArtifact {
  id: string;
  name: string;
  description: string;
  family: NeuralFamily;
  rarity: Rarity;
  visualAssetUrl: string; // URL to image/video
  unlockCondition?: string; // Narrative description of how to unlock
}

/** Real Context: The environment the user is playing in */
export interface RealContext {
  timeOfDay: 'dawn' | 'day' | 'dusk' | 'night';
  weather?: 'clear' | 'rain' | 'cloudy' | 'storm';
  activity?: 'still' | 'walking' | 'running' | 'driving';
  audioEnvironment?: 'quiet' | 'noisy' | 'harmonic' | 'dissonant';
}

/** Social Metrics: Resonance from the "Echo" layer (Instagram) */
export interface SocialMetrics {
  platform: 'instagram';
  shareId: string;
  views: number;
  likes: number;
  comments: number;
  resonanceScore: number; // Calculated currency
}

/** 5-axis mind profile — values in [0, 1] */
export interface MindAxes {
  entropyTolerance: number;    // chaos vs order
  resolutionCraving: number;   // need for closure
  monotonyTolerance: number;   // repetition acceptance
  salienceSensitivity: number; // attention to drama
  tensionAppetite: number;     // build-up desire
}

/** Evolution stages */
export type EvolutionStage = 1 | 2 | 3;
export type SubTrait = "analytical" | "emotional" | "creative" | null;

export const STAGE_NAMES: Record<EvolutionStage, string> = {
  1: "Awakened",
  2: "Resonant",
  3: "Transcendent",
};

/** Persona definition */
export interface Persona {
  id: number;
  name: string;
  family: NeuralFamily; // [NEW] Primary alignment
  tagline: string;
  color: string;
  axes: MindAxes;
  genes: import("./m3").MindGenes; // Canonical 5-gene fingerprint
  description: string;
  strengths: string[];
  compatibleWith: number[];   // persona IDs
  famousMinds: string[];      // e.g. "Beethoven"
  populationPct: number;      // % of users
  starterArtifact?: FocusArtifact; // [NEW] The artifact they begin with
  dimensionProfile?: import("./dimensions").DimensionProfile; // [NEW] 6D radar fingerprint
}

/** A user's mind profile */
export interface MindProfile {
  personaId: number;
  axes: MindAxes;
  stage: EvolutionStage;
  subTrait: SubTrait;
  /** M³ integration — 5 mind genes */
  genes?: import("./m3").MindGenes;
  /** M³ integration — 12-level persona evolution */
  personaLevel?: import("./m3").PersonaLevel;
}

/** Belief trace point (for timeline charts) */
export interface BeliefTrace {
  time: number;
  consonance: number;
  tempo: number;
  salience: number;
  familiarity: number;
  reward: number;
}
