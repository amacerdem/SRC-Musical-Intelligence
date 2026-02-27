import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { MindProfile, EvolutionStage, SubTrait } from "@/types/mind";

interface UserState {
  /* identity */
  displayName: string;
  avatarUrl: string;

  /* mind */
  mind: MindProfile | null;
  hasCompletedOnboarding: boolean;

  /* spotify */
  spotifyConnected: boolean;

  /* progression */
  level: number;
  xp: number;
  streak: number;
  tracksAnalyzed: number;
  achievements: string[];

  /* listening stats (populated at onboarding from "platform import") */
  totalListeningHours: number;
  songsScanned: number;
  listeningYears: number;
  joinedAt: string;

  /* actions */
  setMind: (mind: MindProfile) => void;
  setDisplayName: (name: string) => void;
  setSpotifyConnected: (connected: boolean) => void;
  completeOnboarding: (mind: MindProfile, displayName?: string) => void;
  addXP: (amount: number) => void;
  evolve: (stage: EvolutionStage, subTrait?: SubTrait) => void;
  addAchievement: (id: string) => void;
  analyzeTrack: () => void;
  resetStore: () => void;
}

const INITIAL_STATE = {
  displayName: "",
  avatarUrl: "",
  mind: null as MindProfile | null,
  hasCompletedOnboarding: false,
  spotifyConnected: false,
  level: 1,
  xp: 0,
  streak: 0,
  tracksAnalyzed: 0,
  achievements: [] as string[],
  totalListeningHours: 0,
  songsScanned: 0,
  listeningYears: 0,
  joinedAt: "",
};

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      ...INITIAL_STATE,

      setMind: (mind) => set({ mind }),
      setDisplayName: (displayName) => set({ displayName }),
      setSpotifyConnected: (spotifyConnected) => set({ spotifyConnected }),

      completeOnboarding: (mind, displayName) =>
        set((s) => ({
          mind,
          hasCompletedOnboarding: true,
          displayName: displayName || s.displayName || "You",
          /* Simulate a user who has been listening for years */
          level: 12,
          xp: 14200,
          streak: 23,
          tracksAnalyzed: 847,
          totalListeningHours: 3107,
          songsScanned: 2847,
          listeningYears: 8,
          joinedAt: new Date().toISOString(),
          achievements: ["mind-awakened", "deep-listener", "curious-ears"],
        })),

      addXP: (amount) =>
        set((s) => {
          const newXP = s.xp + amount;
          let lvl = s.level;
          let xpForNext = lvl * 200;
          let remaining = newXP;
          while (remaining >= xpForNext && lvl < 50) {
            remaining -= xpForNext;
            lvl++;
            xpForNext = lvl * 200;
          }
          return { xp: newXP, level: lvl };
        }),

      evolve: (stage, subTrait = null) =>
        set((s) =>
          s.mind ? { mind: { ...s.mind, stage, subTrait } } : {},
        ),

      addAchievement: (id) =>
        set((s) => ({
          achievements: s.achievements.includes(id)
            ? s.achievements
            : [...s.achievements, id],
        })),

      analyzeTrack: () =>
        set((s) => {
          const newCount = s.tracksAnalyzed + 1;
          const newXP = s.xp + 25;
          let lvl = s.level;
          let xpForNext = lvl * 200;
          let remaining = newXP;
          while (remaining >= xpForNext && lvl < 50) {
            remaining -= xpForNext;
            lvl++;
            xpForNext = lvl * 200;
          }
          return { tracksAnalyzed: newCount, xp: newXP, level: lvl };
        }),

      resetStore: () => set(INITIAL_STATE),
    }),
    {
      name: "m3-user-store",
      partialize: (state) => ({
        displayName: state.displayName,
        avatarUrl: state.avatarUrl,
        mind: state.mind,
        hasCompletedOnboarding: state.hasCompletedOnboarding,
        spotifyConnected: state.spotifyConnected,
        level: state.level,
        xp: state.xp,
        streak: state.streak,
        tracksAnalyzed: state.tracksAnalyzed,
        achievements: state.achievements,
        totalListeningHours: state.totalListeningHours,
        songsScanned: state.songsScanned,
        listeningYears: state.listeningYears,
        joinedAt: state.joinedAt,
      }),
    },
  ),
);
