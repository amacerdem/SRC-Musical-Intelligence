/* ── Track Library — 48 Royalty-Free Tracks for M³ ──────────────────
 *  Diverse genres × 5 NeuralFamilies. Each track has R³ perceptual
 *  and C³ cognitive profiles used for playlist scoring and real-time
 *  visualization calibration.
 *
 *  Audio files live in public/music/lib-{nn}.mp3
 *  ──────────────────────────────────────────────────────────────── */

import type { NeuralFamily } from "../types/mind";

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

/* ── 48 Tracks ────────────────────────────────────────────────── */

export const LIBRARY_TRACKS: LibraryTrack[] = [
  // ═══ CLASSICAL / NEO-CLASSICAL / CINEMATIC (6) ═══════════════
  {
    id: "lib-01", name: "Distant Horizons", artist: "Piano Dreams", genre: "Classical",
    bpm: 72, key: "D", mode: "minor", durationSec: 180, dominantFamily: "Architects",
    audioFeatures: { energy: 0.2, valence: 0.15, tempo: 72, danceability: 0.05, acousticness: 0.95, harmonicComplexity: 0.7, timbralBrightness: 0.25 },
    r3Profile: { roughness: 0.05, spectralFlux: 0.15, loudness: 0.2, keyClarity: 0.9, onsetStrength: 0.2, melodicClarity: 0.85, brightness: 0.25, tempoStability: 0.6, tonalness: 0.95, grooveStrength: 0.05 },
    c3Profile: { harmonicConsonance: 0.9, rhythmicSync: 0.3, patternPredictability: 0.7, memoryRecognition: 0.5, wanting: 0.4 },
    audioFile: "/music/lib-01.mp3",
  },
  {
    id: "lib-02", name: "Solemn Strings", artist: "Ensemble Vox", genre: "Neo-Classical",
    bpm: 66, key: "G", mode: "minor", durationSec: 210, dominantFamily: "Architects",
    audioFeatures: { energy: 0.25, valence: 0.1, tempo: 66, danceability: 0.05, acousticness: 0.92, harmonicComplexity: 0.75, timbralBrightness: 0.3 },
    r3Profile: { roughness: 0.08, spectralFlux: 0.2, loudness: 0.25, keyClarity: 0.85, onsetStrength: 0.15, melodicClarity: 0.8, brightness: 0.3, tempoStability: 0.5, tonalness: 0.92, grooveStrength: 0.05 },
    c3Profile: { harmonicConsonance: 0.85, rhythmicSync: 0.2, patternPredictability: 0.65, memoryRecognition: 0.6, wanting: 0.5 },
    audioFile: "/music/lib-02.mp3",
  },
  {
    id: "lib-03", name: "Epic Dawn", artist: "Orchestra Noir", genre: "Cinematic",
    bpm: 100, key: "C", mode: "minor", durationSec: 195, dominantFamily: "Architects",
    audioFeatures: { energy: 0.65, valence: 0.2, tempo: 100, danceability: 0.1, acousticness: 0.7, harmonicComplexity: 0.8, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.15, spectralFlux: 0.45, loudness: 0.6, keyClarity: 0.75, onsetStrength: 0.5, melodicClarity: 0.7, brightness: 0.5, tempoStability: 0.7, tonalness: 0.85, grooveStrength: 0.2 },
    c3Profile: { harmonicConsonance: 0.7, rhythmicSync: 0.5, patternPredictability: 0.5, memoryRecognition: 0.4, wanting: 0.75 },
    audioFile: "/music/lib-03.mp3",
  },
  {
    id: "lib-04", name: "Winter Prelude", artist: "Liana Keys", genre: "Classical",
    bpm: 60, key: "Eb", mode: "major", durationSec: 165, dominantFamily: "Architects",
    audioFeatures: { energy: 0.15, valence: 0.3, tempo: 60, danceability: 0.05, acousticness: 0.98, harmonicComplexity: 0.65, timbralBrightness: 0.35 },
    r3Profile: { roughness: 0.03, spectralFlux: 0.1, loudness: 0.15, keyClarity: 0.92, onsetStrength: 0.15, melodicClarity: 0.9, brightness: 0.35, tempoStability: 0.45, tonalness: 0.96, grooveStrength: 0.02 },
    c3Profile: { harmonicConsonance: 0.95, rhythmicSync: 0.15, patternPredictability: 0.8, memoryRecognition: 0.65, wanting: 0.35 },
    audioFile: "/music/lib-04.mp3",
  },
  {
    id: "lib-05", name: "Minimalist Phase", artist: "Repetitions", genre: "Neo-Classical",
    bpm: 120, key: "A", mode: "minor", durationSec: 240, dominantFamily: "Architects",
    audioFeatures: { energy: 0.3, valence: 0.2, tempo: 120, danceability: 0.15, acousticness: 0.85, harmonicComplexity: 0.55, timbralBrightness: 0.4 },
    r3Profile: { roughness: 0.04, spectralFlux: 0.12, loudness: 0.28, keyClarity: 0.88, onsetStrength: 0.35, melodicClarity: 0.75, brightness: 0.4, tempoStability: 0.85, tonalness: 0.93, grooveStrength: 0.15 },
    c3Profile: { harmonicConsonance: 0.88, rhythmicSync: 0.55, patternPredictability: 0.85, memoryRecognition: 0.7, wanting: 0.3 },
    audioFile: "/music/lib-05.mp3",
  },
  {
    id: "lib-06", name: "Tides of War", artist: "Magnus Score", genre: "Cinematic",
    bpm: 85, key: "F", mode: "minor", durationSec: 200, dominantFamily: "Architects",
    audioFeatures: { energy: 0.75, valence: 0.1, tempo: 85, danceability: 0.08, acousticness: 0.55, harmonicComplexity: 0.85, timbralBrightness: 0.55 },
    r3Profile: { roughness: 0.2, spectralFlux: 0.5, loudness: 0.7, keyClarity: 0.7, onsetStrength: 0.55, melodicClarity: 0.65, brightness: 0.55, tempoStability: 0.65, tonalness: 0.8, grooveStrength: 0.15 },
    c3Profile: { harmonicConsonance: 0.6, rhythmicSync: 0.45, patternPredictability: 0.4, memoryRecognition: 0.35, wanting: 0.8 },
    audioFile: "/music/lib-06.mp3",
  },

  // ═══ ELECTRONIC / IDM / PROGRESSIVE HOUSE (8) ═══════════════
  {
    id: "lib-07", name: "Neon Pulse", artist: "Synthwave Collective", genre: "Electronic",
    bpm: 128, key: "F", mode: "minor", durationSec: 190, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.85, valence: 0.6, tempo: 128, danceability: 0.85, acousticness: 0.02, harmonicComplexity: 0.4, timbralBrightness: 0.8 },
    r3Profile: { roughness: 0.3, spectralFlux: 0.55, loudness: 0.8, keyClarity: 0.6, onsetStrength: 0.7, melodicClarity: 0.45, brightness: 0.8, tempoStability: 0.95, tonalness: 0.6, grooveStrength: 0.9 },
    c3Profile: { harmonicConsonance: 0.5, rhythmicSync: 0.9, patternPredictability: 0.7, memoryRecognition: 0.4, wanting: 0.8 },
    audioFile: "/music/lib-07.mp3",
  },
  {
    id: "lib-08", name: "Fractal Geometry", artist: "Algo", genre: "IDM",
    bpm: 140, key: "Bb", mode: "minor", durationSec: 225, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.7, valence: 0.4, tempo: 140, danceability: 0.5, acousticness: 0.05, harmonicComplexity: 0.85, timbralBrightness: 0.65 },
    r3Profile: { roughness: 0.45, spectralFlux: 0.7, loudness: 0.65, keyClarity: 0.35, onsetStrength: 0.6, melodicClarity: 0.4, brightness: 0.65, tempoStability: 0.5, tonalness: 0.5, grooveStrength: 0.55 },
    c3Profile: { harmonicConsonance: 0.35, rhythmicSync: 0.55, patternPredictability: 0.2, memoryRecognition: 0.2, wanting: 0.6 },
    audioFile: "/music/lib-08.mp3",
  },
  {
    id: "lib-09", name: "Solar Flare", artist: "Deep Transit", genre: "Progressive House",
    bpm: 124, key: "G", mode: "minor", durationSec: 210, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.8, valence: 0.55, tempo: 124, danceability: 0.9, acousticness: 0.05, harmonicComplexity: 0.5, timbralBrightness: 0.7 },
    r3Profile: { roughness: 0.2, spectralFlux: 0.4, loudness: 0.75, keyClarity: 0.65, onsetStrength: 0.65, melodicClarity: 0.55, brightness: 0.7, tempoStability: 0.95, tonalness: 0.7, grooveStrength: 0.92 },
    c3Profile: { harmonicConsonance: 0.6, rhythmicSync: 0.92, patternPredictability: 0.75, memoryRecognition: 0.5, wanting: 0.85 },
    audioFile: "/music/lib-09.mp3",
  },
  {
    id: "lib-10", name: "Digital Rain", artist: "Cipher", genre: "Electronic",
    bpm: 135, key: "D", mode: "minor", durationSec: 175, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.75, valence: 0.35, tempo: 135, danceability: 0.7, acousticness: 0.03, harmonicComplexity: 0.6, timbralBrightness: 0.75 },
    r3Profile: { roughness: 0.35, spectralFlux: 0.6, loudness: 0.7, keyClarity: 0.5, onsetStrength: 0.55, melodicClarity: 0.5, brightness: 0.75, tempoStability: 0.85, tonalness: 0.55, grooveStrength: 0.8 },
    c3Profile: { harmonicConsonance: 0.45, rhythmicSync: 0.8, patternPredictability: 0.5, memoryRecognition: 0.3, wanting: 0.7 },
    audioFile: "/music/lib-10.mp3",
  },
  {
    id: "lib-11", name: "Crystal Lattice", artist: "Resonance Lab", genre: "IDM",
    bpm: 155, key: "E", mode: "minor", durationSec: 200, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.6, valence: 0.3, tempo: 155, danceability: 0.4, acousticness: 0.1, harmonicComplexity: 0.9, timbralBrightness: 0.6 },
    r3Profile: { roughness: 0.4, spectralFlux: 0.75, loudness: 0.55, keyClarity: 0.3, onsetStrength: 0.5, melodicClarity: 0.35, brightness: 0.6, tempoStability: 0.4, tonalness: 0.45, grooveStrength: 0.4 },
    c3Profile: { harmonicConsonance: 0.3, rhythmicSync: 0.4, patternPredictability: 0.15, memoryRecognition: 0.15, wanting: 0.5 },
    audioFile: "/music/lib-11.mp3",
  },
  {
    id: "lib-12", name: "Midnight Drive", artist: "Retro Synth", genre: "Synthwave",
    bpm: 110, key: "A", mode: "minor", durationSec: 185, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.7, valence: 0.5, tempo: 110, danceability: 0.75, acousticness: 0.05, harmonicComplexity: 0.45, timbralBrightness: 0.65 },
    r3Profile: { roughness: 0.15, spectralFlux: 0.35, loudness: 0.65, keyClarity: 0.7, onsetStrength: 0.5, melodicClarity: 0.6, brightness: 0.65, tempoStability: 0.9, tonalness: 0.75, grooveStrength: 0.8 },
    c3Profile: { harmonicConsonance: 0.65, rhythmicSync: 0.85, patternPredictability: 0.7, memoryRecognition: 0.55, wanting: 0.75 },
    audioFile: "/music/lib-12.mp3",
  },
  {
    id: "lib-13", name: "Sub Zero", artist: "Bass Theory", genre: "Drum & Bass",
    bpm: 174, key: "C", mode: "minor", durationSec: 195, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.9, valence: 0.45, tempo: 174, danceability: 0.8, acousticness: 0.02, harmonicComplexity: 0.35, timbralBrightness: 0.85 },
    r3Profile: { roughness: 0.4, spectralFlux: 0.65, loudness: 0.85, keyClarity: 0.4, onsetStrength: 0.85, melodicClarity: 0.3, brightness: 0.85, tempoStability: 0.9, tonalness: 0.45, grooveStrength: 0.95 },
    c3Profile: { harmonicConsonance: 0.3, rhythmicSync: 0.95, patternPredictability: 0.6, memoryRecognition: 0.3, wanting: 0.85 },
    audioFile: "/music/lib-13.mp3",
  },
  {
    id: "lib-14", name: "Quantum Drift", artist: "Trance Union", genre: "Trance",
    bpm: 138, key: "Ab", mode: "minor", durationSec: 220, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.82, valence: 0.6, tempo: 138, danceability: 0.82, acousticness: 0.03, harmonicComplexity: 0.5, timbralBrightness: 0.72 },
    r3Profile: { roughness: 0.18, spectralFlux: 0.4, loudness: 0.78, keyClarity: 0.72, onsetStrength: 0.6, melodicClarity: 0.6, brightness: 0.72, tempoStability: 0.95, tonalness: 0.72, grooveStrength: 0.88 },
    c3Profile: { harmonicConsonance: 0.65, rhythmicSync: 0.9, patternPredictability: 0.8, memoryRecognition: 0.45, wanting: 0.9 },
    audioFile: "/music/lib-14.mp3",
  },

  // ═══ AMBIENT / POST-ROCK / TRIP-HOP (6) ═════════════════════
  {
    id: "lib-15", name: "Submerged", artist: "Deep Oceans", genre: "Ambient",
    bpm: 70, key: "F", mode: "minor", durationSec: 240, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.1, valence: 0.2, tempo: 70, danceability: 0.02, acousticness: 0.6, harmonicComplexity: 0.5, timbralBrightness: 0.2 },
    r3Profile: { roughness: 0.02, spectralFlux: 0.08, loudness: 0.1, keyClarity: 0.45, onsetStrength: 0.05, melodicClarity: 0.3, brightness: 0.2, tempoStability: 0.2, tonalness: 0.6, grooveStrength: 0.02 },
    c3Profile: { harmonicConsonance: 0.75, rhythmicSync: 0.1, patternPredictability: 0.6, memoryRecognition: 0.4, wanting: 0.25 },
    audioFile: "/music/lib-15.mp3",
  },
  {
    id: "lib-16", name: "Memory Palace", artist: "Haze Collective", genre: "Ambient",
    bpm: 80, key: "Eb", mode: "minor", durationSec: 200, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.15, valence: 0.25, tempo: 80, danceability: 0.05, acousticness: 0.7, harmonicComplexity: 0.55, timbralBrightness: 0.3 },
    r3Profile: { roughness: 0.03, spectralFlux: 0.12, loudness: 0.15, keyClarity: 0.55, onsetStrength: 0.08, melodicClarity: 0.4, brightness: 0.3, tempoStability: 0.3, tonalness: 0.7, grooveStrength: 0.05 },
    c3Profile: { harmonicConsonance: 0.8, rhythmicSync: 0.15, patternPredictability: 0.55, memoryRecognition: 0.75, wanting: 0.3 },
    audioFile: "/music/lib-16.mp3",
  },
  {
    id: "lib-17", name: "After the Storm", artist: "Crescendo", genre: "Post-Rock",
    bpm: 90, key: "C", mode: "minor", durationSec: 260, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.5, valence: 0.15, tempo: 90, danceability: 0.1, acousticness: 0.4, harmonicComplexity: 0.65, timbralBrightness: 0.45 },
    r3Profile: { roughness: 0.2, spectralFlux: 0.4, loudness: 0.45, keyClarity: 0.6, onsetStrength: 0.3, melodicClarity: 0.55, brightness: 0.45, tempoStability: 0.55, tonalness: 0.75, grooveStrength: 0.15 },
    c3Profile: { harmonicConsonance: 0.6, rhythmicSync: 0.35, patternPredictability: 0.35, memoryRecognition: 0.45, wanting: 0.65 },
    audioFile: "/music/lib-17.mp3",
  },
  {
    id: "lib-18", name: "Shadow Walk", artist: "Noir Trip", genre: "Trip-Hop",
    bpm: 82, key: "G", mode: "minor", durationSec: 195, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.45, valence: 0.25, tempo: 82, danceability: 0.4, acousticness: 0.25, harmonicComplexity: 0.6, timbralBrightness: 0.4 },
    r3Profile: { roughness: 0.12, spectralFlux: 0.25, loudness: 0.4, keyClarity: 0.6, onsetStrength: 0.35, melodicClarity: 0.5, brightness: 0.4, tempoStability: 0.75, tonalness: 0.7, grooveStrength: 0.55 },
    c3Profile: { harmonicConsonance: 0.65, rhythmicSync: 0.6, patternPredictability: 0.55, memoryRecognition: 0.5, wanting: 0.55 },
    audioFile: "/music/lib-18.mp3",
  },
  {
    id: "lib-19", name: "Glacial Drift", artist: "Polar Ambient", genre: "Dark Ambient",
    bpm: 55, key: "D", mode: "minor", durationSec: 270, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.08, valence: 0.05, tempo: 55, danceability: 0.01, acousticness: 0.5, harmonicComplexity: 0.45, timbralBrightness: 0.15 },
    r3Profile: { roughness: 0.1, spectralFlux: 0.06, loudness: 0.08, keyClarity: 0.3, onsetStrength: 0.03, melodicClarity: 0.15, brightness: 0.15, tempoStability: 0.15, tonalness: 0.5, grooveStrength: 0.01 },
    c3Profile: { harmonicConsonance: 0.55, rhythmicSync: 0.05, patternPredictability: 0.7, memoryRecognition: 0.3, wanting: 0.2 },
    audioFile: "/music/lib-19.mp3",
  },
  {
    id: "lib-20", name: "Constellations", artist: "Slow Burn", genre: "Post-Rock",
    bpm: 95, key: "E", mode: "minor", durationSec: 230, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.55, valence: 0.2, tempo: 95, danceability: 0.08, acousticness: 0.35, harmonicComplexity: 0.7, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.25, spectralFlux: 0.45, loudness: 0.5, keyClarity: 0.55, onsetStrength: 0.35, melodicClarity: 0.5, brightness: 0.5, tempoStability: 0.5, tonalness: 0.7, grooveStrength: 0.1 },
    c3Profile: { harmonicConsonance: 0.55, rhythmicSync: 0.3, patternPredictability: 0.3, memoryRecognition: 0.4, wanting: 0.7 },
    audioFile: "/music/lib-20.mp3",
  },

  // ═══ JAZZ / FUSION (4) ══════════════════════════════════════
  {
    id: "lib-21", name: "Blue Smoke", artist: "Midnight Quintet", genre: "Jazz",
    bpm: 105, key: "Bb", mode: "minor", durationSec: 185, dominantFamily: "Architects",
    audioFeatures: { energy: 0.4, valence: 0.35, tempo: 105, danceability: 0.35, acousticness: 0.8, harmonicComplexity: 0.85, timbralBrightness: 0.45 },
    r3Profile: { roughness: 0.1, spectralFlux: 0.35, loudness: 0.35, keyClarity: 0.6, onsetStrength: 0.4, melodicClarity: 0.7, brightness: 0.45, tempoStability: 0.55, tonalness: 0.85, grooveStrength: 0.5 },
    c3Profile: { harmonicConsonance: 0.7, rhythmicSync: 0.5, patternPredictability: 0.3, memoryRecognition: 0.55, wanting: 0.5 },
    audioFile: "/music/lib-21.mp3",
  },
  {
    id: "lib-22", name: "Tectonic Shift", artist: "Fusion Engine", genre: "Jazz Fusion",
    bpm: 130, key: "E", mode: "minor", durationSec: 210, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.65, valence: 0.4, tempo: 130, danceability: 0.5, acousticness: 0.45, harmonicComplexity: 0.9, timbralBrightness: 0.55 },
    r3Profile: { roughness: 0.2, spectralFlux: 0.5, loudness: 0.6, keyClarity: 0.45, onsetStrength: 0.55, melodicClarity: 0.65, brightness: 0.55, tempoStability: 0.5, tonalness: 0.8, grooveStrength: 0.6 },
    c3Profile: { harmonicConsonance: 0.5, rhythmicSync: 0.5, patternPredictability: 0.2, memoryRecognition: 0.35, wanting: 0.6 },
    audioFile: "/music/lib-22.mp3",
  },
  {
    id: "lib-23", name: "Velvet Night", artist: "Smooth Curves", genre: "Smooth Jazz",
    bpm: 88, key: "Ab", mode: "major", durationSec: 195, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.35, valence: 0.55, tempo: 88, danceability: 0.4, acousticness: 0.75, harmonicComplexity: 0.65, timbralBrightness: 0.4 },
    r3Profile: { roughness: 0.05, spectralFlux: 0.2, loudness: 0.3, keyClarity: 0.75, onsetStrength: 0.25, melodicClarity: 0.75, brightness: 0.4, tempoStability: 0.7, tonalness: 0.9, grooveStrength: 0.45 },
    c3Profile: { harmonicConsonance: 0.85, rhythmicSync: 0.55, patternPredictability: 0.6, memoryRecognition: 0.65, wanting: 0.45 },
    audioFile: "/music/lib-23.mp3",
  },
  {
    id: "lib-24", name: "Free Fall", artist: "Open Form", genre: "Free Jazz",
    bpm: 160, key: "C", mode: "minor", durationSec: 175, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.7, valence: 0.25, tempo: 160, danceability: 0.2, acousticness: 0.65, harmonicComplexity: 0.95, timbralBrightness: 0.6 },
    r3Profile: { roughness: 0.5, spectralFlux: 0.8, loudness: 0.65, keyClarity: 0.15, onsetStrength: 0.65, melodicClarity: 0.4, brightness: 0.6, tempoStability: 0.2, tonalness: 0.55, grooveStrength: 0.25 },
    c3Profile: { harmonicConsonance: 0.2, rhythmicSync: 0.2, patternPredictability: 0.1, memoryRecognition: 0.15, wanting: 0.45 },
    audioFile: "/music/lib-24.mp3",
  },

  // ═══ ROCK / ART ROCK / PROGRESSIVE (6) ══════════════════════
  {
    id: "lib-25", name: "Voltage", artist: "Iron Signal", genre: "Rock",
    bpm: 140, key: "E", mode: "minor", durationSec: 185, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.9, valence: 0.5, tempo: 140, danceability: 0.55, acousticness: 0.1, harmonicComplexity: 0.4, timbralBrightness: 0.85 },
    r3Profile: { roughness: 0.55, spectralFlux: 0.5, loudness: 0.85, keyClarity: 0.55, onsetStrength: 0.8, melodicClarity: 0.5, brightness: 0.85, tempoStability: 0.85, tonalness: 0.6, grooveStrength: 0.8 },
    c3Profile: { harmonicConsonance: 0.4, rhythmicSync: 0.85, patternPredictability: 0.65, memoryRecognition: 0.45, wanting: 0.75 },
    audioFile: "/music/lib-25.mp3",
  },
  {
    id: "lib-26", name: "Prism", artist: "Art Collapse", genre: "Art Rock",
    bpm: 115, key: "F#", mode: "minor", durationSec: 230, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.6, valence: 0.3, tempo: 115, danceability: 0.35, acousticness: 0.25, harmonicComplexity: 0.8, timbralBrightness: 0.6 },
    r3Profile: { roughness: 0.3, spectralFlux: 0.55, loudness: 0.55, keyClarity: 0.5, onsetStrength: 0.5, melodicClarity: 0.55, brightness: 0.6, tempoStability: 0.55, tonalness: 0.65, grooveStrength: 0.4 },
    c3Profile: { harmonicConsonance: 0.45, rhythmicSync: 0.5, patternPredictability: 0.25, memoryRecognition: 0.3, wanting: 0.6 },
    audioFile: "/music/lib-26.mp3",
  },
  {
    id: "lib-27", name: "Temporal Rift", artist: "Prog Collective", genre: "Progressive Rock",
    bpm: 108, key: "B", mode: "minor", durationSec: 280, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.65, valence: 0.35, tempo: 108, danceability: 0.3, acousticness: 0.2, harmonicComplexity: 0.85, timbralBrightness: 0.55 },
    r3Profile: { roughness: 0.25, spectralFlux: 0.5, loudness: 0.6, keyClarity: 0.55, onsetStrength: 0.55, melodicClarity: 0.6, brightness: 0.55, tempoStability: 0.6, tonalness: 0.7, grooveStrength: 0.45 },
    c3Profile: { harmonicConsonance: 0.5, rhythmicSync: 0.55, patternPredictability: 0.2, memoryRecognition: 0.35, wanting: 0.65 },
    audioFile: "/music/lib-27.mp3",
  },
  {
    id: "lib-28", name: "Psyche Garden", artist: "Kaleidoscope", genre: "Psychedelic Rock",
    bpm: 100, key: "D", mode: "minor", durationSec: 245, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.55, valence: 0.4, tempo: 100, danceability: 0.35, acousticness: 0.3, harmonicComplexity: 0.7, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.2, spectralFlux: 0.4, loudness: 0.5, keyClarity: 0.5, onsetStrength: 0.35, melodicClarity: 0.5, brightness: 0.5, tempoStability: 0.6, tonalness: 0.7, grooveStrength: 0.4 },
    c3Profile: { harmonicConsonance: 0.55, rhythmicSync: 0.45, patternPredictability: 0.35, memoryRecognition: 0.5, wanting: 0.6 },
    audioFile: "/music/lib-28.mp3",
  },
  {
    id: "lib-29", name: "Iron Meridian", artist: "Heavy Theory", genre: "Progressive Metal",
    bpm: 155, key: "C", mode: "minor", durationSec: 210, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.92, valence: 0.3, tempo: 155, danceability: 0.4, acousticness: 0.05, harmonicComplexity: 0.75, timbralBrightness: 0.9 },
    r3Profile: { roughness: 0.65, spectralFlux: 0.6, loudness: 0.9, keyClarity: 0.45, onsetStrength: 0.85, melodicClarity: 0.45, brightness: 0.9, tempoStability: 0.75, tonalness: 0.5, grooveStrength: 0.7 },
    c3Profile: { harmonicConsonance: 0.25, rhythmicSync: 0.8, patternPredictability: 0.45, memoryRecognition: 0.3, wanting: 0.7 },
    audioFile: "/music/lib-29.mp3",
  },
  {
    id: "lib-30", name: "Monolith", artist: "Post Earth", genre: "Post-Metal",
    bpm: 78, key: "D", mode: "minor", durationSec: 300, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.6, valence: 0.1, tempo: 78, danceability: 0.1, acousticness: 0.15, harmonicComplexity: 0.6, timbralBrightness: 0.45 },
    r3Profile: { roughness: 0.5, spectralFlux: 0.35, loudness: 0.55, keyClarity: 0.4, onsetStrength: 0.3, melodicClarity: 0.3, brightness: 0.45, tempoStability: 0.55, tonalness: 0.55, grooveStrength: 0.2 },
    c3Profile: { harmonicConsonance: 0.35, rhythmicSync: 0.3, patternPredictability: 0.4, memoryRecognition: 0.25, wanting: 0.55 },
    audioFile: "/music/lib-30.mp3",
  },

  // ═══ HIP-HOP / R&B / NEO-SOUL (6) ══════════════════════════
  {
    id: "lib-31", name: "Lo-Fi Sunrise", artist: "Beat Garden", genre: "Lo-Fi Hip-Hop",
    bpm: 85, key: "F", mode: "major", durationSec: 165, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.3, valence: 0.5, tempo: 85, danceability: 0.55, acousticness: 0.45, harmonicComplexity: 0.45, timbralBrightness: 0.35 },
    r3Profile: { roughness: 0.08, spectralFlux: 0.15, loudness: 0.28, keyClarity: 0.7, onsetStrength: 0.3, melodicClarity: 0.5, brightness: 0.35, tempoStability: 0.85, tonalness: 0.8, grooveStrength: 0.65 },
    c3Profile: { harmonicConsonance: 0.75, rhythmicSync: 0.7, patternPredictability: 0.75, memoryRecognition: 0.7, wanting: 0.45 },
    audioFile: "/music/lib-31.mp3",
  },
  {
    id: "lib-32", name: "Concrete Flow", artist: "Block Poets", genre: "Boom Bap",
    bpm: 92, key: "Eb", mode: "minor", durationSec: 180, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.65, valence: 0.4, tempo: 92, danceability: 0.7, acousticness: 0.2, harmonicComplexity: 0.4, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.15, spectralFlux: 0.3, loudness: 0.6, keyClarity: 0.55, onsetStrength: 0.7, melodicClarity: 0.4, brightness: 0.5, tempoStability: 0.9, tonalness: 0.65, grooveStrength: 0.85 },
    c3Profile: { harmonicConsonance: 0.55, rhythmicSync: 0.85, patternPredictability: 0.7, memoryRecognition: 0.5, wanting: 0.65 },
    audioFile: "/music/lib-32.mp3",
  },
  {
    id: "lib-33", name: "Golden Hour", artist: "Soul Circuit", genre: "Neo-Soul",
    bpm: 95, key: "Ab", mode: "major", durationSec: 200, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.45, valence: 0.65, tempo: 95, danceability: 0.6, acousticness: 0.5, harmonicComplexity: 0.6, timbralBrightness: 0.45 },
    r3Profile: { roughness: 0.06, spectralFlux: 0.2, loudness: 0.4, keyClarity: 0.8, onsetStrength: 0.3, melodicClarity: 0.7, brightness: 0.45, tempoStability: 0.8, tonalness: 0.88, grooveStrength: 0.7 },
    c3Profile: { harmonicConsonance: 0.82, rhythmicSync: 0.7, patternPredictability: 0.65, memoryRecognition: 0.7, wanting: 0.6 },
    audioFile: "/music/lib-33.mp3",
  },
  {
    id: "lib-34", name: "808 Dreams", artist: "Trap Architect", genre: "Trap",
    bpm: 145, key: "C", mode: "minor", durationSec: 175, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.8, valence: 0.35, tempo: 145, danceability: 0.75, acousticness: 0.05, harmonicComplexity: 0.3, timbralBrightness: 0.7 },
    r3Profile: { roughness: 0.25, spectralFlux: 0.4, loudness: 0.75, keyClarity: 0.5, onsetStrength: 0.75, melodicClarity: 0.35, brightness: 0.7, tempoStability: 0.85, tonalness: 0.55, grooveStrength: 0.88 },
    c3Profile: { harmonicConsonance: 0.4, rhythmicSync: 0.88, patternPredictability: 0.7, memoryRecognition: 0.35, wanting: 0.78 },
    audioFile: "/music/lib-34.mp3",
  },
  {
    id: "lib-35", name: "Silk Road", artist: "Velour", genre: "R&B",
    bpm: 100, key: "D", mode: "minor", durationSec: 190, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.5, valence: 0.55, tempo: 100, danceability: 0.65, acousticness: 0.35, harmonicComplexity: 0.55, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.08, spectralFlux: 0.22, loudness: 0.45, keyClarity: 0.72, onsetStrength: 0.35, melodicClarity: 0.65, brightness: 0.5, tempoStability: 0.82, tonalness: 0.82, grooveStrength: 0.72 },
    c3Profile: { harmonicConsonance: 0.75, rhythmicSync: 0.72, patternPredictability: 0.6, memoryRecognition: 0.6, wanting: 0.55 },
    audioFile: "/music/lib-35.mp3",
  },
  {
    id: "lib-36", name: "Funky Transmission", artist: "Groove Lab", genre: "Funk",
    bpm: 112, key: "E", mode: "major", durationSec: 180, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.75, valence: 0.7, tempo: 112, danceability: 0.9, acousticness: 0.35, harmonicComplexity: 0.5, timbralBrightness: 0.65 },
    r3Profile: { roughness: 0.12, spectralFlux: 0.35, loudness: 0.7, keyClarity: 0.7, onsetStrength: 0.65, melodicClarity: 0.6, brightness: 0.65, tempoStability: 0.92, tonalness: 0.78, grooveStrength: 0.95 },
    c3Profile: { harmonicConsonance: 0.65, rhythmicSync: 0.95, patternPredictability: 0.7, memoryRecognition: 0.55, wanting: 0.8 },
    audioFile: "/music/lib-36.mp3",
  },

  // ═══ INDIE FOLK / SINGER-SONGWRITER / BOSSA NOVA (4) ════════
  {
    id: "lib-37", name: "Wooden Heart", artist: "Field Notes", genre: "Indie Folk",
    bpm: 95, key: "G", mode: "major", durationSec: 195, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.3, valence: 0.55, tempo: 95, danceability: 0.3, acousticness: 0.9, harmonicComplexity: 0.45, timbralBrightness: 0.4 },
    r3Profile: { roughness: 0.04, spectralFlux: 0.15, loudness: 0.25, keyClarity: 0.85, onsetStrength: 0.25, melodicClarity: 0.8, brightness: 0.4, tempoStability: 0.7, tonalness: 0.92, grooveStrength: 0.3 },
    c3Profile: { harmonicConsonance: 0.88, rhythmicSync: 0.5, patternPredictability: 0.7, memoryRecognition: 0.75, wanting: 0.4 },
    audioFile: "/music/lib-37.mp3",
  },
  {
    id: "lib-38", name: "Letters Home", artist: "Quiet Streets", genre: "Singer-Songwriter",
    bpm: 78, key: "C", mode: "major", durationSec: 210, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.2, valence: 0.4, tempo: 78, danceability: 0.15, acousticness: 0.95, harmonicComplexity: 0.4, timbralBrightness: 0.35 },
    r3Profile: { roughness: 0.03, spectralFlux: 0.1, loudness: 0.18, keyClarity: 0.9, onsetStrength: 0.2, melodicClarity: 0.85, brightness: 0.35, tempoStability: 0.6, tonalness: 0.95, grooveStrength: 0.15 },
    c3Profile: { harmonicConsonance: 0.92, rhythmicSync: 0.35, patternPredictability: 0.75, memoryRecognition: 0.8, wanting: 0.35 },
    audioFile: "/music/lib-38.mp3",
  },
  {
    id: "lib-39", name: "Saudade", artist: "Rio Dreams", genre: "Bossa Nova",
    bpm: 108, key: "A", mode: "major", durationSec: 185, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.3, valence: 0.6, tempo: 108, danceability: 0.55, acousticness: 0.85, harmonicComplexity: 0.65, timbralBrightness: 0.4 },
    r3Profile: { roughness: 0.04, spectralFlux: 0.18, loudness: 0.25, keyClarity: 0.8, onsetStrength: 0.3, melodicClarity: 0.75, brightness: 0.4, tempoStability: 0.8, tonalness: 0.9, grooveStrength: 0.6 },
    c3Profile: { harmonicConsonance: 0.85, rhythmicSync: 0.65, patternPredictability: 0.65, memoryRecognition: 0.6, wanting: 0.45 },
    audioFile: "/music/lib-39.mp3",
  },
  {
    id: "lib-40", name: "Mountain Song", artist: "Appalachian Echoes", genre: "Bluegrass",
    bpm: 125, key: "D", mode: "major", durationSec: 170, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.55, valence: 0.65, tempo: 125, danceability: 0.5, acousticness: 0.92, harmonicComplexity: 0.5, timbralBrightness: 0.55 },
    r3Profile: { roughness: 0.06, spectralFlux: 0.3, loudness: 0.5, keyClarity: 0.85, onsetStrength: 0.5, melodicClarity: 0.8, brightness: 0.55, tempoStability: 0.85, tonalness: 0.9, grooveStrength: 0.6 },
    c3Profile: { harmonicConsonance: 0.82, rhythmicSync: 0.7, patternPredictability: 0.7, memoryRecognition: 0.6, wanting: 0.5 },
    audioFile: "/music/lib-40.mp3",
  },

  // ═══ EXPERIMENTAL / DRONE / GLITCH (4) ══════════════════════
  {
    id: "lib-41", name: "Static Field", artist: "Noise Theory", genre: "Noise",
    bpm: 0, key: "C", mode: "minor", durationSec: 180, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.7, valence: 0.1, tempo: 0, danceability: 0.02, acousticness: 0.1, harmonicComplexity: 0.2, timbralBrightness: 0.8 },
    r3Profile: { roughness: 0.9, spectralFlux: 0.85, loudness: 0.65, keyClarity: 0.05, onsetStrength: 0.4, melodicClarity: 0.05, brightness: 0.8, tempoStability: 0.05, tonalness: 0.1, grooveStrength: 0.02 },
    c3Profile: { harmonicConsonance: 0.05, rhythmicSync: 0.05, patternPredictability: 0.05, memoryRecognition: 0.05, wanting: 0.3 },
    audioFile: "/music/lib-41.mp3",
  },
  {
    id: "lib-42", name: "Earth Resonance", artist: "Drone Works", genre: "Drone",
    bpm: 0, key: "A", mode: "minor", durationSec: 300, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.2, valence: 0.1, tempo: 0, danceability: 0.01, acousticness: 0.4, harmonicComplexity: 0.35, timbralBrightness: 0.2 },
    r3Profile: { roughness: 0.15, spectralFlux: 0.03, loudness: 0.2, keyClarity: 0.5, onsetStrength: 0.02, melodicClarity: 0.2, brightness: 0.2, tempoStability: 0.05, tonalness: 0.65, grooveStrength: 0.01 },
    c3Profile: { harmonicConsonance: 0.6, rhythmicSync: 0.02, patternPredictability: 0.85, memoryRecognition: 0.2, wanting: 0.15 },
    audioFile: "/music/lib-42.mp3",
  },
  {
    id: "lib-43", name: "Data Corruption", artist: "Glitch Lab", genre: "Glitch",
    bpm: 130, key: "C", mode: "minor", durationSec: 165, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.6, valence: 0.2, tempo: 130, danceability: 0.45, acousticness: 0.05, harmonicComplexity: 0.7, timbralBrightness: 0.7 },
    r3Profile: { roughness: 0.5, spectralFlux: 0.9, loudness: 0.55, keyClarity: 0.2, onsetStrength: 0.7, melodicClarity: 0.2, brightness: 0.7, tempoStability: 0.35, tonalness: 0.3, grooveStrength: 0.5 },
    c3Profile: { harmonicConsonance: 0.15, rhythmicSync: 0.4, patternPredictability: 0.1, memoryRecognition: 0.1, wanting: 0.45 },
    audioFile: "/music/lib-43.mp3",
  },
  {
    id: "lib-44", name: "Musique Concrète No. 7", artist: "Found Sound", genre: "Musique Concrète",
    bpm: 0, key: "C", mode: "minor", durationSec: 200, dominantFamily: "Explorers",
    audioFeatures: { energy: 0.4, valence: 0.15, tempo: 0, danceability: 0.05, acousticness: 0.6, harmonicComplexity: 0.5, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.35, spectralFlux: 0.7, loudness: 0.35, keyClarity: 0.1, onsetStrength: 0.5, melodicClarity: 0.1, brightness: 0.5, tempoStability: 0.1, tonalness: 0.2, grooveStrength: 0.05 },
    c3Profile: { harmonicConsonance: 0.15, rhythmicSync: 0.08, patternPredictability: 0.08, memoryRecognition: 0.1, wanting: 0.35 },
    audioFile: "/music/lib-44.mp3",
  },

  // ═══ WORLD / AFROBEAT / FLAMENCO (4) ════════════════════════
  {
    id: "lib-45", name: "Lagos Night", artist: "Afro Pulse", genre: "Afrobeat",
    bpm: 115, key: "G", mode: "major", durationSec: 200, dominantFamily: "Kineticists",
    audioFeatures: { energy: 0.75, valence: 0.7, tempo: 115, danceability: 0.85, acousticness: 0.4, harmonicComplexity: 0.5, timbralBrightness: 0.6 },
    r3Profile: { roughness: 0.1, spectralFlux: 0.35, loudness: 0.7, keyClarity: 0.7, onsetStrength: 0.65, melodicClarity: 0.6, brightness: 0.6, tempoStability: 0.9, tonalness: 0.8, grooveStrength: 0.92 },
    c3Profile: { harmonicConsonance: 0.7, rhythmicSync: 0.92, patternPredictability: 0.7, memoryRecognition: 0.45, wanting: 0.8 },
    audioFile: "/music/lib-45.mp3",
  },
  {
    id: "lib-46", name: "Duende", artist: "Andalusia Dreams", genre: "Flamenco",
    bpm: 120, key: "E", mode: "minor", durationSec: 190, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.65, valence: 0.3, tempo: 120, danceability: 0.55, acousticness: 0.75, harmonicComplexity: 0.7, timbralBrightness: 0.5 },
    r3Profile: { roughness: 0.12, spectralFlux: 0.4, loudness: 0.6, keyClarity: 0.75, onsetStrength: 0.7, melodicClarity: 0.7, brightness: 0.5, tempoStability: 0.6, tonalness: 0.85, grooveStrength: 0.75 },
    c3Profile: { harmonicConsonance: 0.65, rhythmicSync: 0.7, patternPredictability: 0.4, memoryRecognition: 0.45, wanting: 0.7 },
    audioFile: "/music/lib-46.mp3",
  },
  {
    id: "lib-47", name: "Raga Dawn", artist: "Tabla & Sitar", genre: "Indian Classical",
    bpm: 80, key: "D", mode: "minor", durationSec: 250, dominantFamily: "Alchemists",
    audioFeatures: { energy: 0.4, valence: 0.3, tempo: 80, danceability: 0.2, acousticness: 0.85, harmonicComplexity: 0.8, timbralBrightness: 0.45 },
    r3Profile: { roughness: 0.08, spectralFlux: 0.25, loudness: 0.35, keyClarity: 0.65, onsetStrength: 0.45, melodicClarity: 0.8, brightness: 0.45, tempoStability: 0.45, tonalness: 0.85, grooveStrength: 0.55 },
    c3Profile: { harmonicConsonance: 0.7, rhythmicSync: 0.55, patternPredictability: 0.35, memoryRecognition: 0.35, wanting: 0.55 },
    audioFile: "/music/lib-47.mp3",
  },
  {
    id: "lib-48", name: "Sakura Wind", artist: "Koto Garden", genre: "Japanese Ambient",
    bpm: 68, key: "F", mode: "minor", durationSec: 215, dominantFamily: "Anchors",
    audioFeatures: { energy: 0.15, valence: 0.35, tempo: 68, danceability: 0.05, acousticness: 0.9, harmonicComplexity: 0.5, timbralBrightness: 0.35 },
    r3Profile: { roughness: 0.03, spectralFlux: 0.1, loudness: 0.12, keyClarity: 0.7, onsetStrength: 0.15, melodicClarity: 0.7, brightness: 0.35, tempoStability: 0.35, tonalness: 0.88, grooveStrength: 0.08 },
    c3Profile: { harmonicConsonance: 0.85, rhythmicSync: 0.2, patternPredictability: 0.55, memoryRecognition: 0.65, wanting: 0.3 },
    audioFile: "/music/lib-48.mp3",
  },
];

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

/** All unique genres in the library */
export const LIBRARY_GENRES = [...new Set(LIBRARY_TRACKS.map((t) => t.genre))];
