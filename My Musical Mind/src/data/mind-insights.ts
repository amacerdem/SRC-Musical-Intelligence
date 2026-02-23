/* ── Psychoacoustic Insight Engine ─────────────────────────────────
 *  Generates commentary as if your mind is speaking to you through
 *  music. Grounded in real cognitive science, but written so anyone
 *  can understand what's happening.
 *  ──────────────────────────────────────────────────────────────── */

import type { TFunction } from "i18next";
import type { MindAxes } from "@/types/mind";
import type { Persona } from "@/types/mind";
import { lastWeekDays, weeklyStats, monthlyEvolution, recentTracks } from "./mock-listening";

/* ── Neurochemical language map ───────────────────────────────── */
const NEUROCHEMICALS = {
  dopamine: { name: "Dopamine", role: "the thrill of surprise", emoji: "DA", color: "#FBBF24" },
  norepinephrine: { name: "Norepinephrine", role: "your curiosity engine", emoji: "NE", color: "#84CC16" },
  opioids: { name: "Endogenous opioids", role: "the warmth of beauty", emoji: "μ-OPI", color: "#C084FC" },
  serotonin: { name: "Serotonin", role: "patience & comfort", emoji: "5-HT", color: "#38BDF8" },
} as const;

/* ── Belief commentary generators ─────────────────────────────── */

interface InsightBlock {
  title: string;
  body: string;
  belief: "consonance" | "tempo" | "salience" | "familiarity" | "reward" | null;
  neuroChem?: keyof typeof NEUROCHEMICALS;
  intensity: number; // 0-1, how significant this insight is
}

/** Generate the "Your Week in Music" opening monologue */
export function generateWeeklyMonologue(persona: Persona, axes: MindAxes, t: TFunction): string {
  const deltas = weeklyStats.beliefDeltas;
  const dominantDelta = Math.max(...deltas.map(Math.abs));
  const dominantIdx = deltas.findIndex(d => Math.abs(d) === dominantDelta);
  const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
  const dominant = beliefs[dominantIdx];

  const lines: string[] = [];

  // Opening — intimate, first-person mind voice
  const deltaPercents = deltas.map(d => (d * 100).toFixed(0));
  const deltaMap: Record<string, string> = {
    reward: t("insights.monologue.reward", { delta: deltaPercents[4] }),
    familiarity: t("insights.monologue.familiarity", { delta: deltaPercents[3] }),
    tempo: t("insights.monologue.tempo", { delta: deltaPercents[1] }),
    salience: t("insights.monologue.salience", { delta: deltaPercents[2] }),
    consonance: t("insights.monologue.consonance", { delta: deltaPercents[0] }),
  };
  lines.push(deltaMap[dominant]);

  // Persona-specific observation
  if (axes.tensionAppetite > 0.7) {
    lines.push(t("insights.monologue.tensionHigh", { pct: Math.round(axes.tensionAppetite * 100) }));
  } else if (axes.monotonyTolerance > 0.6) {
    lines.push(t("insights.monologue.monotonyHigh", { pct: Math.round(axes.monotonyTolerance * 100) }));
  } else if (axes.entropyTolerance > 0.7) {
    lines.push(t("insights.monologue.entropyHigh", { pct: Math.round(axes.entropyTolerance * 100) }));
  } else {
    lines.push(t("insights.monologue.resolutionDefault", { pct: Math.round(axes.resolutionCraving * 100) }));
  }

  return lines.join(" ");
}

/** Generate daily micro-insights for each day of the week */
export function generateDailyInsights(persona: Persona, t: TFunction): InsightBlock[] {
  return lastWeekDays.map((day) => {
    const snap = day.beliefSnapshot;
    const dominantIdx = snap.indexOf(Math.max(...snap));
    const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
    const dominant = beliefs[dominantIdx];

    const insightMap: Record<string, () => InsightBlock> = {
      consonance: () => ({
        title: t("insights.daily.consonance.title", { genre: day.topGenre }),
        body: t("insights.daily.consonance.body", { val: snap[0].toFixed(2), tracks: day.tracksPlayed, family: persona.family }),
        belief: "consonance",
        neuroChem: "opioids",
        intensity: snap[0],
      }),
      tempo: () => ({
        title: t("insights.daily.tempo.title", { genre: day.topGenre }),
        body: t("insights.daily.tempo.body", { val: snap[1].toFixed(2), mins: day.minutesListened }),
        belief: "tempo",
        intensity: snap[1],
      }),
      salience: () => ({
        title: t("insights.daily.salience.title"),
        body: t("insights.daily.salience.body", { val: snap[2].toFixed(2), tracks: day.tracksPlayed, genre: day.topGenre, persona: t(`personas.${persona.id}.name`) }),
        belief: "salience",
        neuroChem: "norepinephrine",
        intensity: snap[2],
      }),
      familiarity: () => ({
        title: t("insights.daily.familiarity.title"),
        body: t("insights.daily.familiarity.body", { val: snap[3].toFixed(2) }),
        belief: "familiarity",
        neuroChem: "serotonin",
        intensity: snap[3],
      }),
      reward: () => ({
        title: t("insights.daily.reward.title"),
        body: t("insights.daily.reward.body", { val: snap[4].toFixed(2) }),
        belief: "reward",
        neuroChem: "dopamine",
        intensity: snap[4],
      }),
    };

    return insightMap[dominant]();
  });
}

/** Generate evolution narrative (monthly trajectory) */
export function generateEvolutionNarrative(axes: MindAxes, t: TFunction): string[] {
  const evo = monthlyEvolution;
  const snapshots = evo.weeklySnapshots;
  const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

  const lines: string[] = [];

  // Overall trajectory
  lines.push(t("insights.evolution.overall", {
    belief: evo.mostChangedBelief,
    delta: (evo.mostChangedDelta * 100).toFixed(0),
    drift: t("insights.mockDrift"),
  }));

  // Per-belief micro-narratives
  beliefs.forEach((b, i) => {
    const start = snapshots[0][i];
    const end = snapshots[3][i];
    const delta = end - start;
    if (Math.abs(delta) > 0.05) {
      const direction = delta > 0 ? t("insights.evolution.growing") : t("insights.evolution.softening");
      lines.push(t(`insights.evolution.${b}`, { dir: direction, start: start.toFixed(2), end: end.toFixed(2) }));
    }
  });

  return lines;
}

/** Generate PE (Prediction Error) event commentary */
export function generatePEInsight(t: TFunction): InsightBlock {
  const pe = weeklyStats.peakPE;
  return {
    title: t("insights.pe.title", { mag: pe.magnitude.toFixed(2) }),
    body: t("insights.mockPE"),
    belief: pe.belief as InsightBlock["belief"],
    neuroChem: "dopamine",
    intensity: Math.min(1, pe.magnitude),
  };
}

/** Generate music recommendations based on your profile */
export function generateRecommendations(persona: Persona, axes: MindAxes, t: TFunction): {
  title: string;
  artist: string;
  reason: string;
  belief: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  peOptimization: string;
}[] {
  const recs: ReturnType<typeof generateRecommendations> = [];

  if (axes.resolutionCraving > 0.6) {
    recs.push({
      title: "Nuvole Bianche",
      artist: "Ludovico Einaudi",
      reason: t("insights.recommendations.resolutionReason"),
      belief: "consonance",
      peOptimization: t("insights.recommendations.resolutionPE"),
    });
  }

  if (axes.tensionAppetite > 0.5) {
    recs.push({
      title: "Luminous Beings",
      artist: "Jon Hopkins",
      reason: t("insights.recommendations.tensionReason"),
      belief: "reward",
      peOptimization: t("insights.recommendations.tensionPE"),
    });
  }

  if (axes.entropyTolerance > 0.5) {
    recs.push({
      title: "Ageispolis",
      artist: "Aphex Twin",
      reason: t("insights.recommendations.entropyReason"),
      belief: "tempo",
      peOptimization: t("insights.recommendations.entropyPE"),
    });
  }

  if (axes.monotonyTolerance > 0.3) {
    recs.push({
      title: "Music for 18 Musicians",
      artist: "Steve Reich",
      reason: t("insights.recommendations.monotonyReason", { pct: Math.round(axes.monotonyTolerance * 100) }),
      belief: "familiarity",
      peOptimization: t("insights.recommendations.monotonyPE"),
    });
  }

  recs.push({
    title: "On The Nature of Daylight",
    artist: "Max Richter",
    reason: t("insights.recommendations.salienceReason"),
    belief: "salience",
    peOptimization: t("insights.recommendations.saliencePE"),
  });

  return recs.slice(0, 4);
}

/** Find the most similar user (mock) and generate comparison */
export function findSimilarMind(
  currentAxes: MindAxes,
  currentPersona: Persona,
  users: { id: string; displayName: string; avatarUrl: string; mind: { personaId: number; axes: MindAxes; stage: number } }[],
  t: TFunction,
): {
  user: typeof users[0];
  similarity: number;
  sharedTraits: string[];
  divergence: string;
  connectionInsight: string;
} | null {
  if (users.length === 0) return null;

  // Compute axis-distance for each user
  const scored = users.map((u) => {
    const axesDiff =
      Math.abs(u.mind.axes.entropyTolerance - currentAxes.entropyTolerance) +
      Math.abs(u.mind.axes.resolutionCraving - currentAxes.resolutionCraving) +
      Math.abs(u.mind.axes.monotonyTolerance - currentAxes.monotonyTolerance) +
      Math.abs(u.mind.axes.salienceSensitivity - currentAxes.salienceSensitivity) +
      Math.abs(u.mind.axes.tensionAppetite - currentAxes.tensionAppetite);
    const similarity = Math.round((1 - axesDiff / 5) * 100);
    return { user: u, similarity };
  });

  scored.sort((a, b) => b.similarity - a.similarity);
  const best = scored[0];
  if (best.similarity < 50) return null;

  // Find shared traits (axes within 0.15 of each other)
  const traits: string[] = [];
  const axisKeys: (keyof MindAxes)[] = [
    "entropyTolerance", "resolutionCraving", "monotonyTolerance",
    "salienceSensitivity", "tensionAppetite",
  ];

  let maxDivKey: keyof MindAxes = "entropyTolerance";
  let maxDivValue = 0;

  for (const key of axisKeys) {
    const diff = Math.abs(best.user.mind.axes[key] - currentAxes[key]);
    if (diff < 0.15) traits.push(t(`axes.traits.${key}`));
    if (diff > maxDivValue) {
      maxDivValue = diff;
      maxDivKey = key;
    }
  }

  // Connection insight — human-friendly
  const connectionInsights = [
    t("insights.similar.connection0", { name: best.user.displayName }),
    t("insights.similar.connection1", { family: currentPersona.family, trait: traits[0] || t("axes.traits.entropyTolerance") }),
    t("insights.similar.connection2"),
    t("insights.similar.connection3"),
  ];

  return {
    user: best.user,
    similarity: best.similarity,
    sharedTraits: traits.slice(0, 3),
    divergence: t("insights.similar.divergence", { axis: t(`axes.traits.${maxDivKey}`) }),
    connectionInsight: connectionInsights[Math.abs(best.similarity) % connectionInsights.length],
  };
}

/** Generate the closing insight — one powerful sentence */
export function generateBrainQuote(persona: Persona, axes: MindAxes, t: TFunction): string {
  const family = persona.family || "Alchemists";
  // Deterministic selection based on persona id
  const idx = persona.id % 3;
  return t(`insights.brainQuotes.${family}.${idx}`);
}

/** Recent tracks with context about what your mind experienced */
export function getRecentTracksWithContext(t: TFunction) {
  return recentTracks.map((track) => ({
    ...track,
    neuralContext: track.rewardIntensity > 0.85
      ? t("insights.trackContext.high", { ratio: (track.rewardIntensity * 3.5).toFixed(1) })
      : track.rewardIntensity > 0.7
      ? t("insights.trackContext.mid")
      : t("insights.trackContext.low"),
  }));
}

export { NEUROCHEMICALS };
