import type { Level, Achievement } from "../types/game";

export const levels: Level[] = [
  { level: 1, title: "Listener", xpRequired: 0, unlocks: "Basic profile" },
  { level: 2, title: "Listener", xpRequired: 200, unlocks: "" },
  { level: 3, title: "Listener", xpRequired: 600, unlocks: "" },
  { level: 4, title: "Listener", xpRequired: 1200, unlocks: "" },
  { level: 5, title: "Listener", xpRequired: 2000, unlocks: "Profile sharing" },
  { level: 6, title: "Explorer", xpRequired: 3000, unlocks: "Social features" },
  { level: 7, title: "Explorer", xpRequired: 4200, unlocks: "" },
  { level: 8, title: "Explorer", xpRequired: 5600, unlocks: "" },
  { level: 9, title: "Explorer", xpRequired: 7200, unlocks: "" },
  { level: 10, title: "Explorer", xpRequired: 9000, unlocks: "Persona gallery" },
  { level: 11, title: "Seeker", xpRequired: 11000, unlocks: "Arena access" },
  { level: 12, title: "Seeker", xpRequired: 13200, unlocks: "" },
  { level: 13, title: "Seeker", xpRequired: 15600, unlocks: "" },
  { level: 14, title: "Seeker", xpRequired: 18200, unlocks: "" },
  { level: 15, title: "Seeker", xpRequired: 21000, unlocks: "Daily challenges" },
  { level: 16, title: "Resonator", xpRequired: 24000, unlocks: "Stage 2 Evolution" },
  { level: 17, title: "Resonator", xpRequired: 27200, unlocks: "" },
  { level: 18, title: "Resonator", xpRequired: 30600, unlocks: "" },
  { level: 19, title: "Resonator", xpRequired: 34200, unlocks: "" },
  { level: 20, title: "Resonator", xpRequired: 38000, unlocks: "Sub-trait unlock" },
  { level: 21, title: "Architect", xpRequired: 42000, unlocks: "Create Studio" },
  { level: 25, title: "Architect", xpRequired: 58000, unlocks: "5 analyses/day" },
  { level: 26, title: "Conductor", xpRequired: 63000, unlocks: "Custom mind tuning" },
  { level: 30, title: "Conductor", xpRequired: 83000, unlocks: "Leaderboard" },
  { level: 31, title: "Virtuoso", xpRequired: 89000, unlocks: "Mind Fusion" },
  { level: 35, title: "Virtuoso", xpRequired: 113000, unlocks: "Unlimited analyses" },
  { level: 36, title: "Visionary", xpRequired: 120000, unlocks: "Stage 3 Evolution" },
  { level: 40, title: "Visionary", xpRequired: 148000, unlocks: "Unique aura" },
  { level: 41, title: "Oracle", xpRequired: 156000, unlocks: "Mentor status" },
  { level: 45, title: "Oracle", xpRequired: 188000, unlocks: "Create challenges" },
  { level: 46, title: "Transcendent", xpRequired: 196000, unlocks: "Golden profile" },
  { level: 50, title: "Transcendent", xpRequired: 240000, unlocks: "Mind Legacy" },
];

export const achievements: Achievement[] = [
  { id: "mind-awakened", name: "Mind Awakened", description: "Complete onboarding and discover your persona", icon: "Sparkles", condition: "Complete onboarding", xpReward: 50, rarity: "common" },
  { id: "curious-ears", name: "Curious Ears", description: "Analyze your first 10 tracks", icon: "Headphones", condition: "Analyze 10 tracks", xpReward: 100, rarity: "common" },
  { id: "deep-listener", name: "Deep Listener", description: "Analyze 100 tracks through your mind", icon: "Brain", condition: "Analyze 100 tracks", xpReward: 500, rarity: "rare" },
  { id: "creator-spark", name: "Creator Spark", description: "Generate your first piece of music", icon: "Music", condition: "Create first piece", xpReward: 200, rarity: "common" },
  { id: "contender", name: "Contender", description: "Win 3 arena matches", icon: "Gamepad2", condition: "Win 3 arena matches", xpReward: 300, rarity: "rare" },
  { id: "devoted", name: "Devoted", description: "Maintain a 30-day listening streak", icon: "Flame", condition: "30-day streak", xpReward: 1000, rarity: "epic" },
  { id: "soulmate-found", name: "Soulmate Found", description: "Achieve 95%+ compatibility with another mind", icon: "Heart", condition: "95%+ compatibility", xpReward: 500, rarity: "rare" },
  { id: "mind-collector", name: "Mind Collector", description: "View all 24 persona types", icon: "Grid3x3", condition: "View all personas", xpReward: 200, rarity: "common" },
  { id: "evolved", name: "Resonant", description: "Reach Stage 2 evolution", icon: "TrendingUp", condition: "Reach Stage 2", xpReward: 750, rarity: "rare" },
  { id: "transcendent", name: "Transcendent", description: "Reach Stage 3 — your mind has achieved rare depth", icon: "Crown", condition: "Reach Stage 3", xpReward: 2000, rarity: "legendary" },
  { id: "elite-mind", name: "Elite Mind", description: "Reach the global top 100", icon: "Trophy", condition: "Global top 100", xpReward: 5000, rarity: "legendary" },
  { id: "social-butterfly", name: "Social Butterfly", description: "Visit 50 different mind profiles", icon: "Users", condition: "Visit 50 profiles", xpReward: 300, rarity: "rare" },
];

export function getLevelTitle(level: number): string {
  const found = [...levels].reverse().find((l) => l.level <= level);
  return found?.title ?? "Listener";
}
