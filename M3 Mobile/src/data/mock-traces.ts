import type { BeliefTrace } from "../types/mind";

/** Generate a realistic mock belief trace for a given persona style. */
export function generateTrace(
  durationSec: number,
  style: "calm" | "dramatic" | "chaotic" | "balanced" = "balanced",
  points = 200,
): BeliefTrace[] {
  const traces: BeliefTrace[] = [];

  for (let i = 0; i < points; i++) {
    const t = i / points;
    const time = t * durationSec;
    const noise = () => (Math.random() - 0.5) * 0.05;

    let consonance: number, tempo: number, salience: number, familiarity: number, reward: number;

    if (style === "calm") {
      consonance = 0.7 + 0.05 * Math.sin(t * 6) + noise();
      tempo = 0.4 + 0.03 * Math.sin(t * 4) + noise();
      salience = 0.2 + 0.05 * Math.sin(t * 8) + noise();
      familiarity = 0.5 + t * 0.3 + noise();
      reward = 0.05 + 0.02 * Math.sin(t * 10) + noise();
    } else if (style === "dramatic") {
      const climax = Math.exp(-((t - 0.7) ** 2) / 0.02) * 0.4;
      consonance = 0.55 + 0.15 * Math.sin(t * 10) + climax * 0.2 + noise();
      tempo = 0.5 + 0.2 * t + climax * 0.3 + noise();
      salience = 0.3 + climax * 0.5 + 0.1 * Math.sin(t * 12) + noise();
      familiarity = 0.3 + t * 0.5 + noise();
      reward = 0.04 + climax * 0.2 + 0.03 * Math.sin(t * 15) + noise();
    } else if (style === "chaotic") {
      consonance = 0.4 + 0.2 * Math.sin(t * 20) + noise() * 2;
      tempo = 0.6 + 0.2 * Math.sin(t * 15 + 1) + noise() * 2;
      salience = 0.5 + 0.3 * Math.sin(t * 25) + noise() * 2;
      familiarity = 0.3 + 0.1 * Math.sin(t * 5) + noise();
      reward = 0.08 + 0.1 * Math.sin(t * 30) + noise() * 2;
    } else {
      /* balanced */
      const wave = 0.15 * Math.sin(t * 8);
      consonance = 0.6 + wave + noise();
      tempo = 0.55 + 0.1 * Math.sin(t * 6) + noise();
      salience = 0.4 + 0.15 * Math.sin(t * 10) + noise();
      familiarity = 0.4 + t * 0.35 + noise();
      reward = 0.06 + 0.04 * Math.sin(t * 12) + noise();
    }

    traces.push({
      time,
      consonance: clamp(consonance),
      tempo: clamp(tempo),
      salience: clamp(salience),
      familiarity: clamp(familiarity),
      reward: clamp(reward, -0.5, 0.5),
    });
  }

  return traces;
}

function clamp(v: number, min = 0, max = 1) {
  return Math.max(min, Math.min(max, v));
}
