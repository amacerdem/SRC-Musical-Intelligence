/* ── useLabStore — Lab page state management ─────────────────────────
 *  Manages audio source selection, analysis results, depth level,
 *  and loading state for the Lab analysis studio.
 *  ──────────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { DimensionState } from "@/types/dimensions";
import { computeDimensions } from "@/data/dimensions";

export type AudioSource = "dataset" | "upload" | "mic";
export type DepthLevel = 6 | 12 | 24;
export type AnalysisPhase = "idle" | "loading" | "analyzing" | "done" | "error";

export interface TemporalDimensions {
  /** Per-segment dimension states (8 segments) */
  segments: DimensionState[];
  /** Overall (mean) dimension state */
  overall: DimensionState;
}

export interface LabState {
  /* ── Audio Source ────────────────────────────────── */
  audioSource: AudioSource;
  activeTab: AudioSource;

  /* ── Track Data ─────────────────────────────────── */
  trackDetail: MITrackDetail | null;
  trackId: string | null;

  /* ── Analysis ───────────────────────────────────── */
  phase: AnalysisPhase;
  experimentId: string | null;
  progress: number; // 0-100

  /* ── Dimensions ─────────────────────────────────── */
  depth: DepthLevel;
  temporal: TemporalDimensions | null;

  /* ── Actions ────────────────────────────────────── */
  setActiveTab: (tab: AudioSource) => void;
  setDepth: (depth: DepthLevel) => void;
  selectTrack: (detail: MITrackDetail) => void;
  setPhase: (phase: AnalysisPhase) => void;
  setExperimentId: (id: string) => void;
  setProgress: (pct: number) => void;
  reset: () => void;
}

function computeTemporalDimensions(detail: MITrackDetail): TemporalDimensions {
  const segments = detail.temporal_profile.belief_means_per_segment.map(
    (beliefs) => computeDimensions(beliefs)
  );
  const overall = computeDimensions(detail.beliefs.means);
  return { segments, overall };
}

export const useLabStore = create<LabState>((set) => ({
  audioSource: "dataset",
  activeTab: "dataset",
  trackDetail: null,
  trackId: null,
  phase: "idle",
  experimentId: null,
  progress: 0,
  depth: 6,
  temporal: null,

  setActiveTab: (tab) => set({ activeTab: tab, audioSource: tab }),

  setDepth: (depth) => set({ depth }),

  selectTrack: (detail) =>
    set({
      trackDetail: detail,
      trackId: detail.id,
      audioSource: "dataset",
      phase: "done",
      progress: 100,
      temporal: computeTemporalDimensions(detail),
    }),

  setPhase: (phase) => set({ phase }),

  setExperimentId: (id) => set({ experimentId: id }),

  setProgress: (pct) => set({ progress: pct }),

  reset: () =>
    set({
      trackDetail: null,
      trackId: null,
      phase: "idle",
      experimentId: null,
      progress: 0,
      temporal: null,
    }),
}));
