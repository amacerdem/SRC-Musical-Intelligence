/* ── M³ Audio Store — Zustand (ephemeral, no persist) ────────────────
 *  State machine: "idle" ↔ "playing".
 *  Owns playlist, playback state, and visualization parameters.
 *  Audio engine (AudioPlayer + AudioAnalyzer) are imperative singletons
 *  managed outside React via refs stored here.
 *  ──────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import type { LibraryTrack } from "@/data/track-library";
import type { MindVisualizerParams } from "@/services/AudioAnalyzer";

export type AudioMode = "idle" | "playing";

interface M3AudioState {
  /* ── State ──────────────────────────────────── */
  mode: AudioMode;
  playlist: LibraryTrack[];
  currentTrackIdx: number;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  vizParams: MindVisualizerParams;

  /* ── Actions ────────────────────────────────── */
  setPlaylist: (tracks: LibraryTrack[]) => void;
  setMode: (mode: AudioMode) => void;
  setCurrentTrack: (idx: number) => void;
  setIsPlaying: (playing: boolean) => void;
  togglePlay: () => void;
  skipTrack: () => void;
  prevTrack: () => void;
  setCurrentTime: (time: number) => void;
  setDuration: (dur: number) => void;
  setVolume: (vol: number) => void;
  setVizParams: (params: MindVisualizerParams) => void;
  stopPlayback: () => void;
  cleanup: () => void;
}

export const DEFAULT_VIZ_PARAMS: MindVisualizerParams = {
  // R³ musical
  roughness: 0,
  spectralFlux: 0,
  loudness: 0,
  keyClarity: 0,
  onsetStrength: 0,
  melodicClarity: 0,
  brightness: 0,
  tempoStability: 0,
  tonalness: 0,
  grooveStrength: 0,
  // C³ cognitive
  harmonicConsonance: 0,
  rhythmicSync: 0,
  patternPredictability: 0,
  memoryRecognition: 0,
  wanting: 0,
};

export const useM3AudioStore = create<M3AudioState>((set, get) => ({
  mode: "idle",
  playlist: [],
  currentTrackIdx: 0,
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  volume: 0.75,
  vizParams: { ...DEFAULT_VIZ_PARAMS },

  setPlaylist: (tracks) => set({ playlist: tracks, currentTrackIdx: 0 }),
  setMode: (mode) => set({ mode }),
  setCurrentTrack: (idx) => set({ currentTrackIdx: idx, currentTime: 0 }),
  setIsPlaying: (playing) => set({ isPlaying: playing }),
  togglePlay: () => set((s) => ({ isPlaying: !s.isPlaying })),

  skipTrack: () => {
    const { playlist, currentTrackIdx } = get();
    if (playlist.length === 0) return;
    set({
      currentTrackIdx: (currentTrackIdx + 1) % playlist.length,
      currentTime: 0,
    });
  },

  prevTrack: () => {
    const { playlist, currentTrackIdx, currentTime } = get();
    if (playlist.length === 0) return;
    // If > 3s into track, restart; otherwise go previous
    if (currentTime > 3) {
      set({ currentTime: 0 });
    } else {
      set({
        currentTrackIdx: (currentTrackIdx - 1 + playlist.length) % playlist.length,
        currentTime: 0,
      });
    }
  },

  setCurrentTime: (time) => set({ currentTime: time }),
  setDuration: (dur) => set({ duration: dur }),
  setVolume: (vol) => set({ volume: Math.max(0, Math.min(1, vol)) }),
  setVizParams: (params) => set({ vizParams: params }),

  stopPlayback: () =>
    set({
      mode: "idle",
      isPlaying: false,
      currentTime: 0,
      vizParams: { ...DEFAULT_VIZ_PARAMS },
    }),

  cleanup: () =>
    set({
      mode: "idle",
      playlist: [],
      currentTrackIdx: 0,
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      vizParams: { ...DEFAULT_VIZ_PARAMS },
    }),
}));
