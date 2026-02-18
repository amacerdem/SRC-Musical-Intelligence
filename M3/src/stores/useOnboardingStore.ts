import { create } from "zustand";

type OnboardingStep = "connect" | "evolving" | "reveal" | "done";

interface OnboardingState {
  step: OnboardingStep;
  selectedPersonaId: number | null;
  analysisProgress: number;   // 0-100
  analysisPhase: string;

  setStep: (step: OnboardingStep) => void;
  setPersona: (id: number) => void;
  setProgress: (p: number, phase: string) => void;
  reset: () => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
  step: "connect",
  selectedPersonaId: null,
  analysisProgress: 0,
  analysisPhase: "",

  setStep: (step) => set({ step }),
  setPersona: (id) => set({ selectedPersonaId: id }),
  setProgress: (analysisProgress, analysisPhase) =>
    set({ analysisProgress, analysisPhase }),
  reset: () =>
    set({
      step: "connect",
      selectedPersonaId: null,
      analysisProgress: 0,
      analysisPhase: "",
    }),
}));
