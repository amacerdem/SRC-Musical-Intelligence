import { create } from "zustand";
import type {
  ExperimentMeta,
  NucleusData,
  PsiData,
  R3Group,
  RegionInfo,
  H3Features,
} from "./types/experiment";
import * as api from "./api/client";

export type TabId = "r3" | "nucleus" | "brain" | "neuro" | "psi" | "h3" | "evidence";

interface WebLabState {
  // Playback
  isPlaying: boolean;
  currentTime: number;
  frameIndex: number;
  lodFrameIndex: number;
  duration: number;

  // Navigation
  activeTab: TabId;

  // Selection
  selectedNucleus: string | null;

  // Experiment data
  experimentSlug: string | null;
  experiment: ExperimentMeta | null;
  r3Data: number[][] | null;
  nucleusData: Record<string, NucleusData>;
  ramData: number[][] | null;
  neuroData: number[][] | null;
  psiData: PsiData | null;
  h3Data: H3Features | null;

  // Registry (static, loaded once)
  r3Groups: R3Group[];
  r3FeatureNames: string[];
  regions: RegionInfo[];
  experimentList: string[];

  // Actions
  setPlayback: (isPlaying: boolean) => void;
  updateTime: (currentTime: number) => void;
  seek: (time: number) => void;
  setActiveTab: (tab: TabId) => void;
  selectNucleus: (name: string | null) => void;
  loadRegistry: () => Promise<void>;
  loadExperimentList: () => Promise<void>;
  loadExperiment: (slug: string) => Promise<void>;
  loadNucleus: (name: string) => Promise<void>;
}

export const useStore = create<WebLabState>((set, get) => ({
  // Initial state
  isPlaying: false,
  currentTime: 0,
  frameIndex: 0,
  lodFrameIndex: 0,
  duration: 0,
  activeTab: "r3",
  selectedNucleus: null,
  experimentSlug: null,
  experiment: null,
  r3Data: null,
  nucleusData: {},
  ramData: null,
  neuroData: null,
  psiData: null,
  h3Data: null,
  r3Groups: [],
  r3FeatureNames: [],
  regions: [],
  experimentList: [],

  setPlayback: (isPlaying) => set({ isPlaying }),

  updateTime: (currentTime) => {
    const exp = get().experiment;
    if (!exp) return;
    const frameIndex = Math.round(currentTime * exp.frame_rate);
    const lodFrameIndex = Math.min(
      Math.round(frameIndex / exp.lod_stride),
      exp.lod_frames - 1,
    );
    set({ currentTime, frameIndex, lodFrameIndex });
  },

  seek: (time) => {
    get().updateTime(time);
  },

  setActiveTab: (tab) => set({ activeTab: tab }),

  selectNucleus: (name) => {
    set({ selectedNucleus: name });
    if (name && !get().nucleusData[name]) {
      get().loadNucleus(name);
    }
  },

  loadRegistry: async () => {
    const [r3Reg, regionsData] = await Promise.all([
      api.fetchR3Registry(),
      api.fetchRegions(),
    ]);
    set({
      r3Groups: r3Reg.groups,
      r3FeatureNames: r3Reg.feature_names,
      regions: regionsData,
    });
  },

  loadExperimentList: async () => {
    const list = await api.fetchExperimentList();
    set({ experimentList: list });
  },

  loadExperiment: async (slug) => {
    set({
      experimentSlug: slug,
      experiment: null,
      r3Data: null,
      nucleusData: {},
      ramData: null,
      neuroData: null,
      psiData: null,
      h3Data: null,
      selectedNucleus: null,
      currentTime: 0,
      frameIndex: 0,
      lodFrameIndex: 0,
      isPlaying: false,
    });

    const [meta, r3, ram, neuro, psi, h3] = await Promise.all([
      api.fetchMeta(slug),
      api.fetchR3(slug),
      api.fetchRam(slug),
      api.fetchNeuro(slug),
      api.fetchPsi(slug),
      api.fetchH3(slug),
    ]);

    set({
      experiment: meta,
      duration: meta.duration_s,
      r3Data: r3,
      ramData: ram,
      neuroData: neuro,
      psiData: psi,
      h3Data: h3,
    });

    // Auto-select first nucleus
    if (meta.nuclei.length > 0) {
      const firstName = meta.nuclei[0]!;
      const nd = await api.fetchNucleus(slug, firstName);
      set({
        selectedNucleus: firstName,
        nucleusData: { [firstName]: nd },
      });
    }
  },

  loadNucleus: async (name) => {
    const slug = get().experimentSlug;
    if (!slug) return;
    const nd = await api.fetchNucleus(slug, name);
    set((s) => ({
      nucleusData: { ...s.nucleusData, [name]: nd },
    }));
  },
}));
