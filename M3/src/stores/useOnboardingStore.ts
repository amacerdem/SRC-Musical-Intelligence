import { create } from "zustand";

type OnboardingStep = "plans" | "signup" | "connect" | "evolving" | "reveal" | "done";

interface OnboardingState {
  step: OnboardingStep;
  selectedPersonaId: number | null;
  analysisProgress: number;   // 0-100
  analysisPhase: string;
  selectedPlan: string | null; // "pulse" | "resonance" | "transcendence"

  setStep: (step: OnboardingStep) => void;
  setPersona: (id: number) => void;
  setProgress: (p: number, phase: string) => void;
  setSelectedPlan: (plan: string) => void;
  reset: () => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
  step: "plans",
  selectedPersonaId: null,
  analysisProgress: 0,
  analysisPhase: "",
  selectedPlan: null,

  setStep: (step) => set({ step }),
  setPersona: (id) => set({ selectedPersonaId: id }),
  setProgress: (analysisProgress, analysisPhase) =>
    set({ analysisProgress, analysisPhase }),
  setSelectedPlan: (selectedPlan) => set({ selectedPlan }),
  reset: () =>
    set({
      step: "plans",
      selectedPersonaId: null,
      analysisProgress: 0,
      analysisPhase: "",
      selectedPlan: null,
    }),
}));
