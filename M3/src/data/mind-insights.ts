/* ── Psychoacoustic Insight Engine ─────────────────────────────────
 *  Generates neuroscience-grounded commentary as if your brain is
 *  speaking to you through music. Every sentence maps to real C³
 *  belief dynamics, R³ perceptual features, or H³ temporal morphology.
 *  ──────────────────────────────────────────────────────────────── */

import type { MindAxes } from "@/types/mind";
import type { Persona } from "@/types/mind";
import { lastWeekDays, weeklyStats, monthlyEvolution, recentTracks } from "./mock-listening";

/* ── Neurochemical language map ───────────────────────────────── */
const NEUROCHEMICALS = {
  dopamine: { name: "Dopamine", role: "prediction error signal", emoji: "DA", color: "#FBBF24" },
  norepinephrine: { name: "Norepinephrine", role: "exploration drive", emoji: "NE", color: "#84CC16" },
  opioids: { name: "Endogenous opioids", role: "consonance pleasure", emoji: "μ-OPI", color: "#C084FC" },
  serotonin: { name: "Serotonin", role: "patience & repetition tolerance", emoji: "5-HT", color: "#38BDF8" },
} as const;

/* ── Belief commentary generators ─────────────────────────────── */

interface InsightBlock {
  title: string;
  body: string;
  belief: "consonance" | "tempo" | "salience" | "familiarity" | "reward" | null;
  neuroChem?: keyof typeof NEUROCHEMICALS;
  intensity: number; // 0-1, how significant this insight is
}

/** Generate the "Your Brain This Week" opening monologue */
export function generateWeeklyMonologue(persona: Persona, axes: MindAxes): string {
  const deltas = weeklyStats.beliefDeltas;
  const dominantDelta = Math.max(...deltas.map(Math.abs));
  const dominantIdx = deltas.findIndex(d => Math.abs(d) === dominantDelta);
  const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
  const dominant = beliefs[dominantIdx];

  const lines: string[] = [];

  // Opening — intimate, first-person brain voice
  if (dominant === "reward") {
    lines.push(`Your reward circuitry shifted +${(deltas[4] * 100).toFixed(0)}% this week. That's not noise — your striatal prediction-error system is recalibrating what "good" means to you.`);
  } else if (dominant === "familiarity") {
    lines.push(`Something changed in your temporal cortex this week. Your familiarity tolerance climbed +${(deltas[3] * 100).toFixed(0)}% — you're building deeper pattern models, letting repetition become depth instead of boredom.`);
  } else if (dominant === "tempo") {
    lines.push(`Your supplementary motor area lit up differently this week. Tempo engagement surged +${(deltas[1] * 100).toFixed(0)}% — your internal clock is syncing to more complex rhythmic structures.`);
  } else if (dominant === "salience") {
    lines.push(`Your anterior insula went quiet this week. Salience dropped ${(deltas[2] * 100).toFixed(0)}% — you were processing inward, not reacting to drama. That's depth.`);
  } else {
    lines.push(`Your auditory cortex reconfigured this week. Consonance perception shifted ${(deltas[0] * 100).toFixed(0)}% — your harmonic templates are updating, hearing intervals differently than 7 days ago.`);
  }

  // Persona-specific observation
  if (axes.tensionAppetite > 0.7) {
    lines.push(`With your tension appetite at ${Math.round(axes.tensionAppetite * 100)}%, every unresolved suspension is fuel for your dopaminergic system. The Electronic → Post-Rock ratio shift this week fed that engine directly.`);
  } else if (axes.monotonyTolerance > 0.6) {
    lines.push(`Your high monotony tolerance (${Math.round(axes.monotonyTolerance * 100)}%) means your serotonin-mediated patience system is unusually strong. This week's ambient listening deepened your recurrence models without triggering habituation.`);
  } else if (axes.entropyTolerance > 0.7) {
    lines.push(`Entropy tolerance at ${Math.round(axes.entropyTolerance * 100)}% — your norepinephrine-driven exploration system runs hot. The genre diversity this week kept your novelty-detection circuits engaged without saturation.`);
  } else {
    lines.push(`Your resolution craving (${Math.round(axes.resolutionCraving * 100)}%) shaped this week's trajectory. Every V-I cadence, every resolved suspension — your brain's prediction system marked each one as a micro-reward.`);
  }

  return lines.join(" ");
}

/** Generate daily micro-insights for each day of the week */
export function generateDailyInsights(persona: Persona): InsightBlock[] {
  return lastWeekDays.map((day) => {
    const snap = day.beliefSnapshot;
    const dominantIdx = snap.indexOf(Math.max(...snap));
    const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
    const dominant = beliefs[dominantIdx];

    const insightMap: Record<string, () => InsightBlock> = {
      consonance: () => ({
        title: `${day.topGenre} shaped your harmonic perception`,
        body: `Consonance peaked at ${snap[0].toFixed(2)} — your superior temporal gyrus was mapping interval hierarchies. ${day.tracksPlayed} tracks through your ${persona.family} architecture.`,
        belief: "consonance",
        neuroChem: "opioids",
        intensity: snap[0],
      }),
      tempo: () => ({
        title: `Your motor cortex locked onto ${day.topGenre} rhythms`,
        body: `Tempo state hit ${snap[1].toFixed(2)} across ${day.minutesListened} minutes. Your basal ganglia-supplementary motor loop was entraining to beat structures stronger than usual.`,
        belief: "tempo",
        intensity: snap[1],
      }),
      salience: () => ({
        title: `High-attention listening session`,
        body: `Salience at ${snap[2].toFixed(2)} — your anterior cingulate cortex flagged ${day.tracksPlayed} moments of musical significance. ${day.topGenre} tends to trigger your ${persona.name} salience filters.`,
        belief: "salience",
        neuroChem: "norepinephrine",
        intensity: snap[2],
      }),
      familiarity: () => ({
        title: `Pattern recognition deepened`,
        body: `Familiarity climbed to ${snap[3].toFixed(2)}. Your hippocampal recurrence detector is building stronger models — you're hearing structure where you used to hear surface.`,
        belief: "familiarity",
        neuroChem: "serotonin",
        intensity: snap[3],
      }),
      reward: () => ({
        title: `Peak reward state — your striatum fired`,
        body: `Reward valence reached ${snap[4].toFixed(2)}. The prediction-error cascade aligned perfectly: enough surprise to trigger DA release, enough familiarity for opioid-mediated pleasure. This is what flow sounds like.`,
        belief: "reward",
        neuroChem: "dopamine",
        intensity: snap[4],
      }),
    };

    return insightMap[dominant]();
  });
}

/** Generate evolution narrative (monthly trajectory) */
export function generateEvolutionNarrative(axes: MindAxes): string[] {
  const evo = monthlyEvolution;
  const snapshots = evo.weeklySnapshots;
  const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

  const lines: string[] = [];

  // Overall trajectory
  lines.push(`Over 4 weeks, your ${evo.mostChangedBelief} belief shifted +${(evo.mostChangedDelta * 100).toFixed(0)}%. ${evo.driftDescription}`);

  // Per-belief micro-narratives
  beliefs.forEach((b, i) => {
    const start = snapshots[0][i];
    const end = snapshots[3][i];
    const delta = end - start;
    if (Math.abs(delta) > 0.05) {
      const direction = delta > 0 ? "ascending" : "descending";
      const mapping: Record<string, string> = {
        consonance: `Your harmonic perception is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your Plomp-Levelt roughness sensitivity is recalibrating — intervals that once felt neutral now carry emotional weight.`,
        tempo: `Temporal processing ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your supplementary motor area is building richer internal metronome models, anticipating beat deviations before they land.`,
        salience: `Attentional gating ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your anterior insula is sharpening its filter — fewer false alarms, stronger response to genuinely novel events.`,
        familiarity: `Recurrence modeling ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your hippocampal-cortical loop is consolidating patterns more efficiently. What took 3 listens before now registers in 1.`,
        reward: `Reward geometry ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your ventral tegmental area is recalibrating — the inverted-U curve is shifting, requiring more nuanced prediction errors to trigger the same pleasure response.`,
      };
      lines.push(mapping[b]);
    }
  });

  return lines;
}

/** Generate PE (Prediction Error) event commentary */
export function generatePEInsight(): InsightBlock {
  const pe = weeklyStats.peakPE;
  return {
    title: `Peak Prediction Error: ${pe.magnitude.toFixed(2)}σ`,
    body: pe.description,
    belief: pe.belief as InsightBlock["belief"],
    neuroChem: "dopamine",
    intensity: Math.min(1, pe.magnitude),
  };
}

/** Generate neuroscience-backed music recommendations */
export function generateRecommendations(persona: Persona, axes: MindAxes): {
  title: string;
  artist: string;
  reason: string;
  belief: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  peOptimization: string;
}[] {
  const recs: ReturnType<typeof generateRecommendations> = [];

  // Recommendation based on PE optimization
  if (axes.resolutionCraving > 0.6) {
    recs.push({
      title: "Nuvole Bianche",
      artist: "Ludovico Einaudi",
      reason: "Your resolution craving is high — this piece's delayed cadential patterns will maximize your V→I prediction-error-to-resolution reward cycle.",
      belief: "consonance",
      peOptimization: "High PE at deceptive cadences → strong resolution reward",
    });
  }

  if (axes.tensionAppetite > 0.5) {
    recs.push({
      title: "Luminous Beings",
      artist: "Jon Hopkins",
      reason: "Tension builds across 7 minutes before the harmonic shift at 4:32 — your tension appetite will sustain the anticipatory dopamine accumulation.",
      belief: "reward",
      peOptimization: "Sustained PE accumulation → massive resolution at climax",
    });
  }

  if (axes.entropyTolerance > 0.5) {
    recs.push({
      title: "Ageispolis",
      artist: "Aphex Twin",
      reason: "Your entropy tolerance can handle the micro-timing deviations. Your norepinephrine system will fire at each rhythmic disruption without overwhelming your prediction models.",
      belief: "tempo",
      peOptimization: "Moderate PE from rhythmic entropy → exploration reward",
    });
  }

  if (axes.monotonyTolerance > 0.3) {
    recs.push({
      title: "Music for 18 Musicians",
      artist: "Steve Reich",
      reason: "Phase-shifting patterns will engage your recurrence detector. With monotony tolerance at ${Math.round(axes.monotonyTolerance * 100)}%, the gradual transformations will register as deepening familiarity, not habituation.",
      belief: "familiarity",
      peOptimization: "Low PE amplitude + high recurrence = serotonin-mediated depth",
    });
  }

  recs.push({
    title: "On The Nature of Daylight",
    artist: "Max Richter",
    reason: "The viola entry at 4:05 resolves 3 minutes of accumulated tension. Your salience system will flag it as the single most significant event — a textbook prediction error cascade.",
    belief: "salience",
    peOptimization: "Salience-gated PE → reward amplification through attentional focus",
  });

  return recs.slice(0, 4);
}

/** Find the most similar user (mock) and generate comparison */
export function findSimilarMind(
  currentAxes: MindAxes,
  currentPersona: Persona,
  users: { id: string; displayName: string; avatarUrl: string; mind: { personaId: number; axes: MindAxes; stage: number } }[],
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
  const axisNames: [keyof MindAxes, string][] = [
    ["entropyTolerance", "entropy processing"],
    ["resolutionCraving", "resolution drive"],
    ["monotonyTolerance", "repetition depth"],
    ["salienceSensitivity", "attentional gating"],
    ["tensionAppetite", "tension architecture"],
  ];

  let maxDivAxis = "";
  let maxDivValue = 0;

  for (const [key, label] of axisNames) {
    const diff = Math.abs(best.user.mind.axes[key] - currentAxes[key]);
    if (diff < 0.15) traits.push(label);
    if (diff > maxDivValue) {
      maxDivValue = diff;
      maxDivAxis = label;
    }
  }

  // Connection insight — neuroscience-grounded
  const connectionInsights = [
    `Your auditory cortices process harmonic information through remarkably similar neural pathways. When ${best.user.displayName} hears a deceptive cadence, their prediction error magnitude is within 0.12σ of yours.`,
    `Both minds share a ${currentPersona.family} affinity for ${traits[0] || "musical complexity"}. Your temporal processing windows overlap — you hear the same structural boundaries in a piece.`,
    `The similarity in your belief architectures means you likely reach peak reward at the same musical moments. Your ventral tegmental areas fire in near-synchrony.`,
    `Your H³ temporal morphology profiles suggest you perceive musical time at similar scales. The micro-meso horizon boundary falls in the same place for both minds.`,
  ];

  return {
    user: best.user,
    similarity: best.similarity,
    sharedTraits: traits.slice(0, 3),
    divergence: `${maxDivAxis} differs most — this creates complementary tension in shared listening.`,
    connectionInsight: connectionInsights[Math.abs(best.similarity) % connectionInsights.length],
  };
}

/** Generate the "Your Brain Says" footer insight — one powerful sentence */
export function generateBrainQuote(persona: Persona, axes: MindAxes): string {
  const quotes: Record<string, string[]> = {
    Alchemists: [
      "Your dopamine system isn't chasing the drop — it's chasing the moment your prediction model breaks and rebuilds itself stronger.",
      "The tension you crave isn't stress. It's your brain's way of building a model complex enough to be worth resolving.",
      "Every unresolved chord is an open question your striatum refuses to leave unanswered.",
    ],
    Architects: [
      "You don't hear music. You hear the blueprint behind it. Every deviation from the template is data.",
      "Your auditory cortex maintains a running structural model — and the pleasure comes from watching it prove itself right.",
      "Consonance isn't beauty to you. It's confirmation that your internal model of harmony matches reality.",
    ],
    Explorers: [
      "Your norepinephrine system runs 2σ hotter than the median listener. You need novelty like oxygen.",
      "When you hear something you've never heard before, your brain doesn't flinch. It leans in. That's rare.",
      "Your prediction models are deliberately loose — they allow more entropy through, which means more surprise, more learning, more reward.",
    ],
    Anchors: [
      "Your temporal cortex wraps sound in memory. Every melody is a key to a room you've already been in.",
      "The familiarity response in your hippocampus is unusually strong — repetition doesn't bore you, it deepens the neural groove.",
      "You listen with your entire history. Each note activates a chain of associations that most minds never build.",
    ],
    Kineticists: [
      "Your motor cortex doesn't just respond to rhythm — it predicts it. You feel the beat before it arrives.",
      "The groove is a precision instrument in your brain. Micro-timing deviations of 10ms register as distinct textures.",
      "Your basal ganglia lock onto rhythmic structures with unusual speed — you're entrained before most people have found the beat.",
    ],
  };

  const familyQuotes = quotes[persona.family] ?? quotes.Alchemists;
  // Deterministic selection based on persona id
  return familyQuotes[persona.id % familyQuotes.length];
}

/** Recent tracks with neuroscience context */
export function getRecentTracksWithContext() {
  return recentTracks.map((track) => ({
    ...track,
    neuralContext: track.rewardIntensity > 0.85
      ? `Your C³ reward system peaked here — prediction error magnitude exceeded baseline by ${(track.rewardIntensity * 3.5).toFixed(1)}×. This is a signature PE event.`
      : track.rewardIntensity > 0.7
      ? `Moderate-high reward activation. Your precision-weighted prediction error created a sustained dopaminergic response through this section.`
      : `Steady-state processing. Your belief trajectories were stable — familiarity-driven listening with low PE amplitude.`,
  }));
}

export { NEUROCHEMICALS };
