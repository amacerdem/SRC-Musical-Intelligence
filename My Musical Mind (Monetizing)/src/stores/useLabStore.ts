/* ── useLabStore — Lab page state management ─────────────────────────
 *  Manages audio source selection, analysis results, depth level,
 *  and loading state for the Lab analysis studio.
 *
 *  Dimension computation uses _beliefs_full.json (frame-level beliefs)
 *  for high-resolution temporal curves, falling back to the summary
 *  JSON's belief_means_per_segment if the full file isn't available.
 *  ──────────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { DimensionState } from "@/types/dimensions";
import { computeLabDimensions } from "@/data/dimensions";
import { miDataService, MIDataService } from "@/services/MIDataService";

export type AudioSource = "dataset" | "upload" | "mic";
export type DepthLevel = 6 | 12 | 24;
export type AnalysisPhase = "idle" | "loading" | "analyzing" | "done" | "error";

/** Default number of temporal segments for dimension curves */
const TEMPORAL_SEGMENTS = 200;

export interface TemporalDimensions {
  /** Per-segment dimension states */
  segments: DimensionState[];
  /** Overall (mean) dimension state */
  overall: DimensionState;
  /** Number of raw frames used (for display) */
  frameCount: number;
  /** Source: "full" = _beliefs_full.json, "summary" = main JSON fallback */
  source: "full" | "summary";
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
  setTemporal: (temporal: TemporalDimensions) => void;
  reset: () => void;
}

/** Fallback: compute from the summary JSON's 64-segment belief means */
function computeFromSummary(detail: MITrackDetail): TemporalDimensions {
  const segments = detail.temporal_profile.belief_means_per_segment.map(
    (beliefs) => computeLabDimensions(beliefs)
  );
  const overall = computeLabDimensions(detail.beliefs.means);
  return { segments, overall, frameCount: 0, source: "summary" };
}

/** Async: fetch _beliefs_full.json, downsample, compute dimensions */
async function computeFromFull(
  trackId: string,
): Promise<TemporalDimensions | null> {
  try {
    const full = await miDataService.getTrackBeliefsFull(trackId);
    const matrix = MIDataService.beliefsFullToMatrix(full);
    const numSegs = Math.min(TEMPORAL_SEGMENTS, matrix.length);
    const downsampled = MIDataService.downsampleMatrix(matrix, numSegs);

    const segments = downsampled.map((beliefs) => computeLabDimensions(beliefs));

    // Overall = mean of all frames
    const overallBeliefs = new Array(131).fill(0);
    for (let t = 0; t < matrix.length; t++) {
      for (let b = 0; b < 131; b++) overallBeliefs[b] += matrix[t][b];
    }
    for (let b = 0; b < 131; b++) overallBeliefs[b] /= matrix.length;
    const overall = computeLabDimensions(overallBeliefs);

    return { segments, overall, frameCount: full.n_frames, source: "full" };
  } catch {
    return null;
  }
}

export const useLabStore = create<LabState>((set, get) => ({
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

  selectTrack: (detail) => {
    // Immediately show with summary data (fast)
    const summaryTemporal = computeFromSummary(detail);
    set({
      trackDetail: detail,
      trackId: detail.id,
      audioSource: "dataset",
      phase: "done",
      progress: 100,
      temporal: summaryTemporal,
    });

    // Then upgrade to full beliefs async (31 MB fetch)
    computeFromFull(detail.id).then((fullTemporal) => {
      // Only update if this track is still selected
      if (fullTemporal && get().trackId === detail.id) {
        set({ temporal: fullTemporal });
      }
    });
  },

  setPhase: (phase) => set({ phase }),

  setExperimentId: (id) => set({ experimentId: id }),

  setProgress: (pct) => set({ progress: pct }),

  setTemporal: (temporal) => set({ temporal }),

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
