/* ── Track Library — Real MI Dataset Tracks for M³ ──────────────────
 *  138 tracks from Repetuare, analyzed through the full R³→H³→C³
 *  pipeline. Each track has R³ perceptual and C³ cognitive profiles
 *  derived from real MI analysis.
 *
 *  Populated dynamically from MIDataService at app init.
 *  ──────────────────────────────────────────────────────────────── */

import type { NeuralFamily } from "@/types/mind";
import { miDataService, MIDataService } from "@/services/MIDataService";

/* ── Types ────────────────────────────────────────────────────── */

export interface R3Profile {
  roughness: number;        // A — Consonance (0=smooth, 1=rough)
  spectralFlux: number;     // D — Change (0=static, 1=rapid change)
  loudness: number;         // B — Energy (0=quiet, 1=loud)
  keyClarity: number;       // H — Harmony (0=atonal, 1=strong key)
  onsetStrength: number;    // B — Energy (0=smooth, 1=percussive)
  melodicClarity: number;   // F — Pitch (0=noise, 1=clear melody)
  brightness: number;       // C — Timbre (0=dark, 1=bright)
  tempoStability: number;   // G — Rhythm (0=free, 1=steady)
  tonalness: number;        // A — Consonance (0=noise, 1=tonal)
  grooveStrength: number;   // G+K — Rhythm (0=no groove, 1=heavy)
}

export interface C3Profile {
  harmonicConsonance: number;    // F1 Sensory (0=dissonant, 1=consonant)
  rhythmicSync: number;          // F3 Attention (0=no sync, 1=entrained)
  patternPredictability: number; // F2 Prediction (0=surprising, 1=predictable)
  memoryRecognition: number;     // F4 Memory (0=novel, 1=familiar)
  wanting: number;               // F6 Reward (0=indifferent, 1=strong desire)
}

export interface AudioFeatures {
  energy: number;
  valence: number;
  tempo: number;
  danceability: number;
  acousticness: number;
  harmonicComplexity: number;
  timbralBrightness: number;
}

export interface LibraryTrack {
  id: string;
  name: string;
  artist: string;
  genre: string;
  bpm: number;
  key: string;
  mode: "major" | "minor";
  durationSec: number;
  dominantFamily: NeuralFamily;
  audioFeatures: AudioFeatures;
  r3Profile: R3Profile;
  c3Profile: C3Profile;
  audioFile: string;
}

/* ── Dynamic Library (populated at init) ─────────────────────── */

export const LIBRARY_TRACKS: LibraryTrack[] = [];

/** Called from App.tsx after miDataService.init() */
export function initLibraryTracks(): void {
  LIBRARY_TRACKS.length = 0;
  if (miDataService.isReady()) {
    LIBRARY_TRACKS.push(
      ...miDataService.getAllTracks().map(MIDataService.toLibraryTrack)
    );
  }
}

/* ── Utilities ───────────────────────────────────────────────── */

/** Get a track by ID */
export function getLibraryTrack(id: string): LibraryTrack | undefined {
  return LIBRARY_TRACKS.find((t) => t.id === id);
}

/** Get all tracks for a specific genre */
export function getTracksByGenre(genre: string): LibraryTrack[] {
  return LIBRARY_TRACKS.filter((t) => t.genre === genre);
}

/** Get all tracks for a specific NeuralFamily */
export function getTracksByFamily(family: NeuralFamily): LibraryTrack[] {
  return LIBRARY_TRACKS.filter((t) => t.dominantFamily === family);
}

/** All unique genres in the library (computed dynamically) */
export const LIBRARY_GENRES: string[] = [];

export function refreshGenres(): void {
  LIBRARY_GENRES.length = 0;
  LIBRARY_GENRES.push(...new Set(LIBRARY_TRACKS.map((t) => t.genre)));
}
