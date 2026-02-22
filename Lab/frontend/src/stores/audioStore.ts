/** Global audio playback state — shared cursor for all visualizations. */

import { create } from 'zustand';
import { FRAME_RATE } from '../design/tokens';

interface AudioState {
  // Audio metadata
  currentFile: string | null;
  duration: number;       // seconds
  totalFrames: number;    // R³ frame count

  // Playback
  isPlaying: boolean;
  currentTime: number;    // seconds
  currentFrame: number;   // frame index (derived from currentTime)

  // Waveform data
  waveformEnvelope: Float32Array | null;
  spectrogramData: Float32Array | null;
  spectrogramMels: number;
  spectrogramFrames: number;

  // Actions
  setCurrentFile: (name: string | null) => void;
  setDuration: (d: number) => void;
  setPlaying: (p: boolean) => void;
  setCurrentTime: (t: number) => void;
  setWaveformEnvelope: (data: Float32Array) => void;
  setSpectrogramData: (data: Float32Array, mels: number, frames: number) => void;
}

export const useAudioStore = create<AudioState>((set) => ({
  currentFile: null,
  duration: 0,
  totalFrames: 0,
  isPlaying: false,
  currentTime: 0,
  currentFrame: 0,
  waveformEnvelope: null,
  spectrogramData: null,
  spectrogramMels: 128,
  spectrogramFrames: 0,

  setCurrentFile: (name) => set({
    currentFile: name,
    currentTime: 0,
    currentFrame: 0,
    isPlaying: false,
    waveformEnvelope: null,
    spectrogramData: null,
  }),

  setDuration: (d) => set({
    duration: d,
    totalFrames: Math.floor(d * FRAME_RATE),
  }),

  setPlaying: (p) => set({ isPlaying: p }),

  setCurrentTime: (t) => set({
    currentTime: t,
    currentFrame: Math.floor(t * FRAME_RATE),
  }),

  setWaveformEnvelope: (data) => set({ waveformEnvelope: data }),

  setSpectrogramData: (data, mels, frames) => set({
    spectrogramData: data,
    spectrogramMels: mels,
    spectrogramFrames: frames,
  }),
}));
