import { create } from "zustand";
import type { M3Tier } from "@/types/m3";

type OnboardingStep = "plans" | "signup" | "connect" | "evolving" | "reveal" | "done";

interface OnboardingState {
  step: OnboardingStep;
  selectedPersonaId: number | null;
  analysisProgress: number;   // 0-100
  analysisPhase: string;
  selectedPlan: string | null; // "pulse" | "resonance" | "transcendence"
  selectedTier: M3Tier;       // M³ tier mapped from plan

  setStep: (step: OnboardingStep) => void;
  setPersona: (id: number) => void;
  setProgress: (p: number, phase: string) => void;
  setSelectedPlan: (plan: string) => void;
  reset: () => void;
}

/** Map plan IDs to M³ tiers */
const PLAN_TO_TIER: Record<string, M3Tier> = {
  pulse: "basic",
  resonance: "premium",
  transcendence: "ultimate",
};

export const useOnboardingStore = create<OnboardingState>((set) => ({
  step: "plans",
  selectedPersonaId: null,
  analysisProgress: 0,
  analysisPhase: "",
  selectedPlan: null,
  selectedTier: "free",

  setStep: (step) => set({ step }),
  setPersona: (id) => set({ selectedPersonaId: id }),
  setProgress: (analysisProgress, analysisPhase) =>
    set({ analysisProgress, analysisPhase }),
  setSelectedPlan: (plan) => set({ selectedPlan: plan, selectedTier: PLAN_TO_TIER[plan] ?? "free" }),
  reset: () =>
    set({
      step: "plans",
      selectedPersonaId: null,
      analysisProgress: 0,
      analysisPhase: "",
      selectedPlan: null,
      selectedTier: "free",
    }),
}));
