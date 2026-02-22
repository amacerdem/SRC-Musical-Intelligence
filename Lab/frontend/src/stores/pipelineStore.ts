/** Pipeline execution state + experiment results cache. */

import { create } from 'zustand';

interface ExperimentMeta {
  experiment_id: string;
  audio_name: string;
  timestamp: string;
  duration: number;
  n_frames: number;
  fps: number;
  reward_mean: number;
  reward_positive_pct: number;
  kernel_version: string;
}

interface PipelineState {
  // Current run
  isRunning: boolean;
  runPhase: string;
  runProgress: number;

  // Results cache
  experiments: ExperimentMeta[];
  currentExperimentId: string | null;

  // R³ data (loaded from backend)
  r3Features: Float32Array | null;
  r3Names: string[];
  r3Frames: number;

  // H³ data
  h3Tuples: Int32Array | null;
  h3Values: Float32Array | null;
  h3NTuples: number;

  // Reward
  rewardData: Float32Array | null;

  // RAM
  ramData: Float32Array | null;

  // Actions
  setRunning: (r: boolean) => void;
  setRunPhase: (p: string) => void;
  setRunProgress: (p: number) => void;
  setExperiments: (e: ExperimentMeta[]) => void;
  setCurrentExperimentId: (id: string | null) => void;
  setR3Data: (features: Float32Array, names: string[], frames: number) => void;
  setH3Data: (tuples: Int32Array, values: Float32Array, nTuples: number) => void;
  setRewardData: (data: Float32Array) => void;
  setRamData: (data: Float32Array) => void;
  clearResults: () => void;
}

export const usePipelineStore = create<PipelineState>((set) => ({
  isRunning: false,
  runPhase: '',
  runProgress: 0,
  experiments: [],
  currentExperimentId: null,
  r3Features: null,
  r3Names: [],
  r3Frames: 0,
  h3Tuples: null,
  h3Values: null,
  h3NTuples: 0,
  rewardData: null,
  ramData: null,

  setRunning: (r) => set({ isRunning: r }),
  setRunPhase: (p) => set({ runPhase: p }),
  setRunProgress: (p) => set({ runProgress: p }),
  setExperiments: (e) => set({ experiments: e }),
  setCurrentExperimentId: (id) => set({ currentExperimentId: id }),
  setR3Data: (features, names, frames) => set({ r3Features: features, r3Names: names, r3Frames: frames }),
  setH3Data: (tuples, values, nTuples) => set({ h3Tuples: tuples, h3Values: values, h3NTuples: nTuples }),
  setRewardData: (data) => set({ rewardData: data }),
  setRamData: (data) => set({ ramData: data }),
  clearResults: () => set({
    r3Features: null,
    r3Names: [],
    r3Frames: 0,
    h3Tuples: null,
    h3Values: null,
    h3NTuples: 0,
    rewardData: null,
    ramData: null,
  }),
}));
