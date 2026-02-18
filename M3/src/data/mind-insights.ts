/* ── Psychoacoustic Insight Engine ─────────────────────────────────
 *  Generates commentary as if your mind is speaking to you through
 *  music. Grounded in real cognitive science, but written so anyone
 *  can understand what's happening.
 *  ──────────────────────────────────────────────────────────────── */

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
export function generateWeeklyMonologue(persona: Persona, axes: MindAxes): string {
  const deltas = weeklyStats.beliefDeltas;
  const dominantDelta = Math.max(...deltas.map(Math.abs));
  const dominantIdx = deltas.findIndex(d => Math.abs(d) === dominantDelta);
  const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
  const dominant = beliefs[dominantIdx];

  const lines: string[] = [];

  // Opening — intimate, first-person mind voice
  if (dominant === "reward") {
    lines.push(`Your sense of musical pleasure shifted +${(deltas[4] * 100).toFixed(0)}% this week. That's significant — your mind is recalibrating what "good music" means to you. The songs that moved you last month might not hit the same way next month.`);
  } else if (dominant === "familiarity") {
    lines.push(`Something shifted in how you recognize music this week. Your memory response climbed +${(deltas[3] * 100).toFixed(0)}% — you're building deeper connections with the music you hear, finding new layers in songs you already know.`);
  } else if (dominant === "tempo") {
    lines.push(`You felt rhythm differently this week. Your rhythmic engagement surged +${(deltas[1] * 100).toFixed(0)}% — your body is locking into more complex beats, anticipating groove patterns before they drop.`);
  } else if (dominant === "salience") {
    lines.push(`Your attention to musical detail went quiet this week. Surprise sensitivity dropped ${(deltas[2] * 100).toFixed(0)}% — you were listening inward, soaking things in rather than reacting to every twist. That's depth, not disengagement.`);
  } else {
    lines.push(`Your sense of harmony shifted ${(deltas[0] * 100).toFixed(0)}% this week. The way you hear chords and intervals is changing — melodies that once felt neutral are starting to carry emotional weight.`);
  }

  // Persona-specific observation
  if (axes.tensionAppetite > 0.7) {
    lines.push(`With your love of tension at ${Math.round(axes.tensionAppetite * 100)}%, you live for that moment right before the music resolves. This week's mix of Electronic and Post-Rock fed that craving perfectly — long builds, delayed payoffs, maximum anticipation.`);
  } else if (axes.monotonyTolerance > 0.6) {
    lines.push(`Your comfort with repetition (${Math.round(axes.monotonyTolerance * 100)}%) is a superpower most listeners don't have. This week's ambient sessions let you sink deeper into patterns without getting bored — each loop revealed something new.`);
  } else if (axes.entropyTolerance > 0.7) {
    lines.push(`Chaos appetite at ${Math.round(axes.entropyTolerance * 100)}% — you thrive on the unexpected. The genre diversity this week kept your curiosity satisfied without burning you out. You need variety like breathing.`);
  } else {
    lines.push(`Your need for closure (${Math.round(axes.resolutionCraving * 100)}%) shaped your week. Every resolved chord, every satisfying ending — your mind marked each one as a small victory. You hear music as a series of promises kept.`);
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
        title: `${day.topGenre} shaped how you hear harmony`,
        body: `Your sense of harmony peaked at ${snap[0].toFixed(2)} — you were deeply tuned into chord progressions and intervals. ${day.tracksPlayed} tracks through your ${persona.family} ears.`,
        belief: "consonance",
        neuroChem: "opioids",
        intensity: snap[0],
      }),
      tempo: () => ({
        title: `Your body locked onto ${day.topGenre} rhythms`,
        body: `Rhythmic engagement hit ${snap[1].toFixed(2)} across ${day.minutesListened} minutes. You were moving with the music more than usual — anticipating beats before they landed.`,
        belief: "tempo",
        intensity: snap[1],
      }),
      salience: () => ({
        title: `A high-attention listening session`,
        body: `Your attention peaked at ${snap[2].toFixed(2)} — ${day.tracksPlayed} moments grabbed you. ${day.topGenre} tends to hit your ${persona.name} mind's surprise triggers hard.`,
        belief: "salience",
        neuroChem: "norepinephrine",
        intensity: snap[2],
      }),
      familiarity: () => ({
        title: `You went deeper into what you know`,
        body: `Memory response climbed to ${snap[3].toFixed(2)}. You're building stronger connections with familiar sounds — hearing structure where you used to hear surface.`,
        belief: "familiarity",
        neuroChem: "serotonin",
        intensity: snap[3],
      }),
      reward: () => ({
        title: `Peak pleasure — this is what flow sounds like`,
        body: `Musical pleasure reached ${snap[4].toFixed(2)}. Everything aligned: enough surprise to keep you engaged, enough familiarity to feel right. Your mind was in the zone.`,
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
  lines.push(`Over 4 weeks, your ${evo.mostChangedBelief} response shifted +${(evo.mostChangedDelta * 100).toFixed(0)}%. ${evo.driftDescription}`);

  // Per-belief micro-narratives
  beliefs.forEach((b, i) => {
    const start = snapshots[0][i];
    const end = snapshots[3][i];
    const delta = end - start;
    if (Math.abs(delta) > 0.05) {
      const direction = delta > 0 ? "growing" : "softening";
      const mapping: Record<string, string> = {
        consonance: `Your sense of harmony is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Chords and intervals that once felt neutral are starting to carry more emotional weight for you.`,
        tempo: `Your rhythmic feel is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). You're building richer internal timing — anticipating groove changes before they happen.`,
        salience: `Your surprise sensitivity is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). You're getting better at filtering noise from signal — responding to genuinely important musical moments.`,
        familiarity: `Your musical memory is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Patterns click faster now — what took 3 listens before registers on the first play.`,
        reward: `Your pleasure response is ${direction} (${start.toFixed(2)} → ${end.toFixed(2)}). Your mind is getting more selective — it takes more nuanced music to produce the same rush.`,
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
    title: `Biggest Surprise: ${pe.magnitude.toFixed(2)}x intensity`,
    body: pe.description,
    belief: pe.belief as InsightBlock["belief"],
    neuroChem: "dopamine",
    intensity: Math.min(1, pe.magnitude),
  };
}

/** Generate music recommendations based on your profile */
export function generateRecommendations(persona: Persona, axes: MindAxes): {
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
      reason: "You love when music resolves beautifully. This piece teases you with delayed endings — building anticipation then delivering exactly the closure your mind craves.",
      belief: "consonance",
      peOptimization: "Delayed resolution → deeper satisfaction when it arrives",
    });
  }

  if (axes.tensionAppetite > 0.5) {
    recs.push({
      title: "Luminous Beings",
      artist: "Jon Hopkins",
      reason: "7 minutes of slowly building intensity before the release at 4:32. Your love of tension means you'll ride the anticipation like a wave — and the payoff is worth every second.",
      belief: "reward",
      peOptimization: "Long build → massive release at the climax",
    });
  }

  if (axes.entropyTolerance > 0.5) {
    recs.push({
      title: "Ageispolis",
      artist: "Aphex Twin",
      reason: "Your chaos appetite can handle the unexpected rhythms. Each micro-disruption will spark your curiosity without overwhelming you — the perfect edge between confusion and discovery.",
      belief: "tempo",
      peOptimization: "Rhythmic surprises → exploration and discovery",
    });
  }

  if (axes.monotonyTolerance > 0.3) {
    recs.push({
      title: "Music for 18 Musicians",
      artist: "Steve Reich",
      reason: `Phase-shifting patterns that evolve so slowly you barely notice — until you realize you're somewhere completely new. With your repetition comfort at ${Math.round(axes.monotonyTolerance * 100)}%, this will feel like a meditation, not a loop.`,
      belief: "familiarity",
      peOptimization: "Gradual evolution → deep immersion without boredom",
    });
  }

  recs.push({
    title: "On The Nature of Daylight",
    artist: "Max Richter",
    reason: "The viola entry at 4:05 cuts through 3 minutes of quiet tension. Your mind will flag it as THE moment — the one event in the whole piece that redefines everything before it.",
    belief: "salience",
    peOptimization: "One unforgettable moment → lasting impact",
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
    ["entropyTolerance", "chaos appetite"],
    ["resolutionCraving", "need for closure"],
    ["monotonyTolerance", "repetition comfort"],
    ["salienceSensitivity", "surprise sensitivity"],
    ["tensionAppetite", "tension love"],
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

  // Connection insight — human-friendly
  const connectionInsights = [
    `You and ${best.user.displayName} hear music through remarkably similar ears. When they hear an unexpected chord change, their reaction is nearly identical to yours — same surprise, same satisfaction.`,
    `Both minds share a ${currentPersona.family} love for ${traits[0] || "musical complexity"}. You pick up on the same details in a song — the same moments grab both of you.`,
    `Your musical minds are so aligned that you'd probably love each other's playlists. You reach the emotional peak at the same moments in a piece.`,
    `You both experience time in music the same way — short moments feel equally intense, long passages build the same way. Shared listening would feel natural.`,
  ];

  return {
    user: best.user,
    similarity: best.similarity,
    sharedTraits: traits.slice(0, 3),
    divergence: `${maxDivAxis} is where you differ most — that's what makes shared listening interesting, not boring.`,
    connectionInsight: connectionInsights[Math.abs(best.similarity) % connectionInsights.length],
  };
}

/** Generate the closing insight — one powerful sentence */
export function generateBrainQuote(persona: Persona, axes: MindAxes): string {
  const quotes: Record<string, string[]> = {
    Alchemists: [
      "You're not chasing the drop. You're chasing the moment everything you expected shatters — and something better takes its place.",
      "The tension you crave isn't stress. It's your mind building something complex enough to be worth the resolution.",
      "Every unresolved chord is a question you refuse to leave unanswered. That's not anxiety — that's hunger.",
    ],
    Architects: [
      "You don't just hear music. You hear the blueprint behind it. Every deviation from the pattern is information.",
      "Your mind builds a running model of every song — and the pleasure comes from watching it prove itself right.",
      "Harmony isn't beauty to you. It's confirmation that the universe has structure and you can hear it.",
    ],
    Explorers: [
      "Your curiosity runs hotter than most. You need the unknown like oxygen — silence is just an unexplored frequency.",
      "When you hear something completely new, you don't flinch. You lean in. That's rarer than you think.",
      "Your mind keeps its expectations deliberately loose — so more surprise gets through, more learning happens, more joy arrives.",
    ],
    Anchors: [
      "Your mind wraps sound in memory. Every melody is a key to a room you've already been in — but see differently each time.",
      "Repetition doesn't bore you. It deepens. Each listen carves the groove a little wider, a little richer.",
      "You listen with your entire history. Each note lights up a chain of memories that most people never build.",
    ],
    Kineticists: [
      "Your body doesn't just respond to rhythm — it predicts it. You feel the beat before it lands.",
      "The groove is a precision instrument in your mind. Tiny timing shifts that others miss register as completely different textures.",
      "You lock onto rhythmic structures with unusual speed — you're moving before most people have even found the beat.",
    ],
  };

  const familyQuotes = quotes[persona.family] ?? quotes.Alchemists;
  // Deterministic selection based on persona id
  return familyQuotes[persona.id % familyQuotes.length];
}

/** Recent tracks with context about what your mind experienced */
export function getRecentTracksWithContext() {
  return recentTracks.map((track) => ({
    ...track,
    neuralContext: track.rewardIntensity > 0.85
      ? `Your mind lit up here — the surprise-to-satisfaction ratio was ${(track.rewardIntensity * 3.5).toFixed(1)}x above your baseline. This is one of those rare moments where everything clicks.`
      : track.rewardIntensity > 0.7
      ? `Strong response. Something in this section caught your attention and held it — a sustained wave of enjoyment that built slowly and paid off.`
      : `Steady-state listening. Your mind was comfortable here — familiar territory, low surprise, the kind of music you can sink into without thinking.`,
  }));
}

export { NEUROCHEMICALS };
