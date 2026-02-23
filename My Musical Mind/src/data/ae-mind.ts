import type { MindProfile, BeliefTrace } from "@/types/mind";
import type { UserProfile } from "@/types/social";

/** Amac Erdem's reference mind profile */
export const aeMind: MindProfile = {
  personaId: 6,  // Tension Architect
  axes: {
    entropyTolerance: 0.52,
    resolutionCraving: 0.68,
    monotonyTolerance: 0.18,
    salienceSensitivity: 0.87,
    tensionAppetite: 0.91,
  },
  stage: 3,
  subTrait: "creative",
};

export const aeProfile: UserProfile = {
  id: "ae-001",
  displayName: "Amac Erdem",
  avatarUrl: "",
  country: "TR",
  level: 50,
  xp: 240000,
  mind: aeMind,
  joinedAt: "2024-01-01",
  tracksAnalyzed: 12847,
  achievements: [
    "mind-awakened", "deep-listener", "creator-spark", "contender",
    "devoted", "soulmate-found", "mind-collector", "evolved",
    "transcendent", "elite-mind", "social-butterfly",
  ],
  streak: 365,
};

/** Mock Swan Lake belief trace for AE's mind */
export const aeSwanLakeTrace: BeliefTrace[] = Array.from({ length: 200 }, (_, i) => {
  const t = i / 200;
  const phase = t < 0.3 ? "intro" : t < 0.6 ? "development" : t < 0.85 ? "climax" : "resolution";
  const noise = () => (Math.random() - 0.5) * 0.06;

  const climaxMod = phase === "climax" ? 0.25 : 0;
  const introMod = phase === "intro" ? -0.1 : 0;

  return {
    time: t * 182.6,
    consonance: 0.65 + 0.1 * Math.sin(t * 12) + introMod + noise(),
    tempo: 0.5 + 0.15 * Math.sin(t * 8) + climaxMod * 0.3 + noise(),
    salience: 0.35 + climaxMod * 0.4 + 0.08 * Math.sin(t * 15) + noise(),
    familiarity: 0.4 + t * 0.4 + noise(),
    reward: 0.06 + climaxMod * 0.12 + 0.04 * Math.sin(t * 20) + noise(),
  };
});
