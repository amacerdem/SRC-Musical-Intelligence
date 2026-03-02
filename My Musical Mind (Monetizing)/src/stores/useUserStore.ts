import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { MindProfile, EvolutionStage, SubTrait } from "@/types/mind";
import type { SpotifyMIProfile } from "@/services/SpotifyProfileService";

interface UserState {
  /* identity */
  displayName: string;
  avatarUrl: string;

  /* mind */
  mind: MindProfile | null;
  hasCompletedOnboarding: boolean;

  /* spotify */
  spotifyConnected: boolean;
  spotifyProfile: SpotifyMIProfile | null;

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
  setSpotifyProfile: (profile: SpotifyMIProfile | null) => void;
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
  spotifyProfile: null as SpotifyMIProfile | null,
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
      setSpotifyProfile: (spotifyProfile) => set({ spotifyProfile }),

      completeOnboarding: (mind, displayName) =>
        set((s) => {
          // Prefer Spotify profile stats if available, else fall back to MI dataset
          let realTracks = 138, realHours = 10;
          const sp = s.spotifyProfile;
          if (sp && sp.stats.total_tracks > 0) {
            realTracks = sp.stats.total_tracks;
            realHours = Math.round(sp.stats.total_minutes / 60 * 10) / 10;
          } else {
            try {
              const { miDataService } = require("@/services/MIDataService");
              if (miDataService.isReady()) {
                const tracks = miDataService.getAllTracks();
                realTracks = tracks.length;
                const realMinutes = Math.round(tracks.reduce((sum: number, t: { duration_s: number }) => sum + t.duration_s, 0) / 60);
                realHours = Math.round(realMinutes / 60 * 10) / 10;
              }
            } catch { /* fallback to defaults */ }
          }
          return {
            mind,
            hasCompletedOnboarding: true,
            displayName: displayName || s.displayName || "You",
            level: 12,
            xp: 14200,
            streak: 23,
            tracksAnalyzed: realTracks,
            totalListeningHours: realHours,
            songsScanned: realTracks,
            listeningYears: 8,
            joinedAt: new Date().toISOString(),
            achievements: ["mind-awakened", "deep-listener", "curious-ears"],
          };
        }),

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
        spotifyProfile: state.spotifyProfile,
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
