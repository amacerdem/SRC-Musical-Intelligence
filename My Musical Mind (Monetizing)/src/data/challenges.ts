import type { Challenge } from "@/types/game";

export const challenges: Challenge[] = [
  {
    id: "ch1",
    title: "Prediction Duel",
    description: "Two minds, one track. Who predicts the next musical moment better?",
    type: "prediction",
    xpReward: 75,
    endsAt: "2026-02-19T23:59:00Z",
    participants: 1247,
  },
  {
    id: "ch2",
    title: "Entropy Gauntlet",
    description: "Listen to increasingly chaotic music — how far can your mind handle?",
    type: "entropy",
    xpReward: 100,
    endsAt: "2026-02-20T23:59:00Z",
    participants: 892,
  },
  {
    id: "ch3",
    title: "Resolution Race",
    description: "Spot the exact moment of harmonic resolution. Fastest mind wins.",
    type: "resolution",
    xpReward: 75,
    endsAt: "2026-02-21T23:59:00Z",
    participants: 1534,
  },
  {
    id: "ch4",
    title: "Mind Fusion",
    description: "Combine your mind with a stranger to create a hybrid persona.",
    type: "fusion",
    xpReward: 50,
    endsAt: "2026-02-22T23:59:00Z",
    participants: 673,
  },
];
