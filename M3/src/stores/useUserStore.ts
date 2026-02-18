import { create } from "zustand";
import type { MindProfile, EvolutionStage, SubTrait } from "@/types/mind";

interface UserState {
  /* identity */
  displayName: string;
  avatarUrl: string;

  /* mind */
  mind: MindProfile | null;
  hasCompletedOnboarding: boolean;

  /* progression */
  level: number;
  xp: number;
  streak: number;
  tracksAnalyzed: number;
  achievements: string[];

  /* actions */
  setMind: (mind: MindProfile) => void;
  setDisplayName: (name: string) => void;
  completeOnboarding: (mind: MindProfile, displayName?: string) => void;
  addXP: (amount: number) => void;
  evolve: (stage: EvolutionStage, subTrait?: SubTrait) => void;
  addAchievement: (id: string) => void;
}

export const useUserStore = create<UserState>((set) => ({
  displayName: "",
  avatarUrl: "",
  mind: null,
  hasCompletedOnboarding: false,
  level: 1,
  xp: 0,
  streak: 0,
  tracksAnalyzed: 0,
  achievements: [],

  setMind: (mind) => set({ mind }),
  setDisplayName: (displayName) => set({ displayName }),

  completeOnboarding: (mind, displayName) =>
    set((s) => ({
      mind,
      hasCompletedOnboarding: true,
      displayName: displayName || s.displayName || "You",
      level: 1,
      xp: 50,
      achievements: ["mind-awakened"],
    })),

  addXP: (amount) =>
    set((s) => {
      const newXP = s.xp + amount;
      /* simple level calc: each level = level * 200 XP */
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
      s.mind ? { mind: { ...s.mind, stage, subTrait } } : {}
    ),

  addAchievement: (id) =>
    set((s) => ({
      achievements: s.achievements.includes(id)
        ? s.achievements
        : [...s.achievements, id],
    })),
}));
