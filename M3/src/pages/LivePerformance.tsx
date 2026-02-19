import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play, Square, Shield, Sprout, Users, Target, Trophy, Zap, X,
  Heart, Sparkles, Layers, RotateCcw, Gauge, Activity, BarChart3, LayoutGrid,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { MindOrganismCanvas, type OrganismHandle } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { mockUsers } from "@/data/mock-users";
import { pageTransition, staggerChildren, slideUp, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import type { MindAxes, NeuralFamily } from "@/types/mind";
import type { UserProfile } from "@/types/social";

type Mode = "solo" | "duo";
type SessionState = "idle" | "performing" | "finished";

/* ── Axis training metadata ──────────────────────────────────── */
const AXIS_KEYS: (keyof MindAxes)[] = [
  "entropyTolerance", "resolutionCraving", "monotonyTolerance",
  "salienceSensitivity", "tensionAppetite",
];

const AXIS_META: Record<keyof MindAxes, {
  label: string;
  belief: keyof typeof beliefColors;
  strengthen: Record<NeuralFamily, string>;
  develop: Record<NeuralFamily, string>;
}> = {
  entropyTolerance: {
    label: "Chaos Tolerance",
    belief: "consonance",
    strengthen: {
      Alchemists: "Channel chaos into transformation — let dissonance fuel your alchemy",
      Architects: "Use controlled chaos to stress-test your structures",
      Explorers: "Push deeper into the noise — your edge is where others retreat",
      Anchors: "Let chaotic textures color your emotional palette",
      Kineticists: "Layer polyrhythmic chaos over your groove foundation",
    },
    develop: {
      Alchemists: "Sit with unresolved chaos longer before seeking the drop",
      Architects: "Try free-form listening without seeking patterns",
      Explorers: "You already thrive here — explore chaos in unfamiliar genres",
      Anchors: "Gradually introduce noisy textures into your comfort zone",
      Kineticists: "Listen to broken-beat and glitch to expand rhythmic chaos",
    },
  },
  resolutionCraving: {
    label: "Need for Closure",
    belief: "tempo",
    strengthen: {
      Alchemists: "Maximize the payoff — build longer arcs before resolution",
      Architects: "Perfect your cadence sensitivity with complex harmonic progressions",
      Explorers: "Use resolution as a surprise tool in unexpected contexts",
      Anchors: "Deepen emotional satisfaction through delayed gratification",
      Kineticists: "Find rhythmic resolution in polymetric convergence points",
    },
    develop: {
      Alchemists: "Practice leaving tension unresolved — embrace the open ending",
      Architects: "Try ambient pieces that avoid traditional cadences",
      Explorers: "Let go of needing an ending — some journeys don't close",
      Anchors: "Explore music that fades rather than resolves",
      Kineticists: "Listen to asymmetric rhythms that never fully land",
    },
  },
  monotonyTolerance: {
    label: "Repetition Comfort",
    belief: "familiarity",
    strengthen: {
      Alchemists: "Find transformation within repetition — the loop evolves you",
      Architects: "Hear the micro-variations that hide inside repetition",
      Explorers: "Discover how repetition creates its own kind of novelty",
      Anchors: "Let familiar patterns anchor you deeper into feeling",
      Kineticists: "Lock into the groove — repetition is where pocket lives",
    },
    develop: {
      Alchemists: "Build patience with minimal techno and loop-based music",
      Architects: "Study Steve Reich — repetition as architectural material",
      Explorers: "Challenge yourself with long drone pieces",
      Anchors: "Sit with a single repeated melody and notice what shifts",
      Kineticists: "Try meditative drum loops to build rhythmic patience",
    },
  },
  salienceSensitivity: {
    label: "Attention Sensitivity",
    belief: "salience",
    strengthen: {
      Alchemists: "Amplify your sensitivity to dramatic peaks and drops",
      Architects: "Sharpen your detection of structural turning points",
      Explorers: "Train your ear to catch the most novel moments instantly",
      Anchors: "Attune to the emotional weight of key musical moments",
      Kineticists: "Push your sensitivity with dense polyrhythmic passages",
    },
    develop: {
      Alchemists: "Practice noticing subtle shifts, not just the obvious peaks",
      Architects: "Listen for quiet structural changes in ambient music",
      Explorers: "Slow down and attend to detail within familiar territory",
      Anchors: "Expand your attention beyond emotional peaks to texture",
      Kineticists: "Train with dynamic pieces that reward patient attention",
    },
  },
  tensionAppetite: {
    label: "Tension Appetite",
    belief: "reward",
    strengthen: {
      Alchemists: "You are the master of tension — push build-ups even further",
      Architects: "Engineer longer suspension arcs with more complex layering",
      Explorers: "Seek tension in unfamiliar harmonic territories",
      Anchors: "Let tension deepen your emotional investment in the music",
      Kineticists: "Build rhythmic tension through accelerating density",
    },
    develop: {
      Alchemists: "Explore music with slow, gentle tension curves",
      Architects: "Try pieces that build tension subtly over long durations",
      Explorers: "Let tension accumulate naturally instead of seeking it",
      Anchors: "Gradually increase tolerance with cinematic build-ups",
      Kineticists: "Listen to progressive pieces that build energy slowly",
    },
  },
};

function splitAxes(axes: MindAxes): { strong: (keyof MindAxes)[]; weak: (keyof MindAxes)[] } {
  const sorted = AXIS_KEYS.slice().sort((a, b) => axes[b] - axes[a]);
  return { strong: sorted.slice(0, 3), weak: sorted.slice(3) };
}

/* ── Duo session game conditions ──────────────────────────────── */

interface DuoConditions {
  task: string;
  taskDetail: string;
  goal: string;
  goalMetric: string;
  xpReward: number;
  difficulty: "Easy" | "Medium" | "Hard" | "Legendary";
  complementaryAxis: string;
}

const DUO_TASKS: Record<keyof MindAxes, { task: string; detail: string }> = {
  entropyTolerance: {
    task: "Chaos Sync",
    detail: "One embraces chaos, the other seeks order. Find the shared frequency where both minds resonate.",
  },
  resolutionCraving: {
    task: "Resolution Negotiation",
    detail: "One craves closure, the other resists. Navigate the tension and find where both feel complete.",
  },
  monotonyTolerance: {
    task: "Repetition Bridge",
    detail: "One thrives in loops, the other needs novelty. Build a bridge between patience and exploration.",
  },
  salienceSensitivity: {
    task: "Attention Fusion",
    detail: "Your attention peaks differ. Synchronize your salience — notice the same moments together.",
  },
  tensionAppetite: {
    task: "Tension Alchemy",
    detail: "One builds tension higher, the other seeks release sooner. Find the alchemical balance point.",
  },
};

const DIFFICULTY_COLORS: Record<DuoConditions["difficulty"], string> = {
  Easy: "#10B981",
  Medium: "#F59E0B",
  Hard: "#EF4444",
  Legendary: "#A855F7",
};

/* ── Controllers ─────────────────────────────────────────────── */

const EMOTIONAL_CONTROLLERS = [
  { id: "valence", label: "Valence", description: "Mood polarity", Icon: Heart, color: "#EC4899" },
  { id: "arousal", label: "Arousal", description: "Calm ↔ Excited", Icon: Sparkles, color: "#F59E0B" },
  { id: "depth", label: "Depth", description: "Surface ↔ Deep", Icon: Layers, color: "#8B5CF6" },
  { id: "nostalgia", label: "Nostalgia", description: "Present ↔ Memory", Icon: RotateCcw, color: "#38BDF8" },
];

const PHYSICAL_CONTROLLERS = [
  { id: "tempo", label: "Tempo", description: "Rhythm speed", Icon: Gauge, color: "#F97316" },
  { id: "energy", label: "Energy", description: "Intensity level", Icon: Activity, color: "#EF4444" },
  { id: "dynamics", label: "Dynamics", description: "Contrast range", Icon: BarChart3, color: "#84CC16" },
  { id: "density", label: "Density", description: "Note density", Icon: LayoutGrid, color: "#06B6D4" },
];

function generateDuoConditions(
  myAxes: MindAxes,
  friendAxes: MindAxes,
  myFamily: NeuralFamily,
  friendFamily: NeuralFamily,
): DuoConditions {
  const gaps = AXIS_KEYS.map((k) => ({
    key: k,
    gap: Math.abs(myAxes[k] - friendAxes[k]),
    label: AXIS_META[k].label,
  }));
  gaps.sort((a, b) => b.gap - a.gap);
  const topGap = gaps[0];

  const totalDist = gaps.reduce((s, g) => s + g.gap, 0);
  const difficulty: DuoConditions["difficulty"] =
    totalDist > 2.5 ? "Legendary" : totalDist > 1.8 ? "Hard" : totalDist > 1.0 ? "Medium" : "Easy";

  const baseXP = Math.round(200 + totalDist * 400);
  const sameFamily = myFamily === friendFamily;
  const goal = sameFamily
    ? `Push your shared ${myFamily} strengths to the limit — synchronized peak above 85%`
    : `Fuse ${myFamily} × ${friendFamily} perspectives — achieve belief alignment within 15%`;
  const goalMetric = sameFamily ? "Combined Peak > 85%" : "Belief Delta < 15%";

  return {
    task: DUO_TASKS[topGap.key].task,
    taskDetail: DUO_TASKS[topGap.key].detail,
    goal,
    goalMetric,
    xpReward: baseXP,
    difficulty,
    complementaryAxis: topGap.label,
  };
}

function formatSessionTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

export function LivePerformance() {
  const [mode, setMode] = useState<Mode>("solo");
  const [sessionState, setSessionState] = useState<SessionState>("idle");
  const [sessionTime, setSessionTime] = useState(0);
  const [beliefStates, setBeliefStates] = useState([0.5, 0.5, 0.5, 0.5, 0.5]);
  const [peakReward, setPeakReward] = useState(0);
  const [sessionCount] = useState(17);
  const [axisEmphasis, setAxisEmphasis] = useState<Record<string, number>>({});
  const [selectedFriend, setSelectedFriend] = useState<UserProfile | null>(null);
  const [activeControllers, setActiveControllers] = useState<Set<string>>(new Set());
  const [duoWaiting, setDuoWaiting] = useState(false);

  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const color = persona?.color ?? beliefColors.tempo.primary;
  const family = persona?.family ?? "Explorers";
  const organismRef = useRef<OrganismHandle>(null);

  const { strong, weak } = useMemo(
    () => mind ? splitAxes(mind.axes) : { strong: AXIS_KEYS.slice(0, 3), weak: AXIS_KEYS.slice(3) },
    [mind],
  );

  // Generate duo conditions when a friend is selected
  const duoConditions = useMemo(() => {
    if (!selectedFriend || !mind) return null;
    const friendPersona = getPersona(selectedFriend.mind.personaId);
    return generateDuoConditions(mind.axes, selectedFriend.mind.axes, family, friendPersona.family);
  }, [selectedFriend, mind, family]);

  // Clear friend selection when switching back to solo
  useEffect(() => {
    if (mode === "solo") setSelectedFriend(null);
  }, [mode]);

  // Initialize axis emphasis from persona axes
  useEffect(() => {
    if (!mind) return;
    const init: Record<string, number> = {};
    for (const k of AXIS_KEYS) init[k] = Math.round(mind.axes[k] * 100);
    setAxisEmphasis(init);
  }, [mind]);

  const setEmphasis = useCallback((key: string, val: number) => {
    setAxisEmphasis((prev) => ({ ...prev, [key]: val }));
  }, []);

  const toggleController = useCallback((id: string) => {
    setActiveControllers((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }, []);

  // Compute average emphasis for organism animation
  const avgEmphasis = useMemo(() => {
    const vals = Object.values(axisEmphasis);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length / 100 : 0.5;
  }, [axisEmphasis]);

  // Session timer + belief state simulation
  useEffect(() => {
    if (sessionState !== "performing") return;

    const interval = setInterval(() => {
      setSessionTime((t) => t + 1);

      setBeliefStates((prev) => {
        const t = Date.now() / 1000;
        const e = axisEmphasis;
        const ef = (k: string) => (e[k] ?? 50) / 100;

        const newStates = [
          Math.max(0, Math.min(1, prev[0] + (ef("entropyTolerance") - 0.5) * 0.02 + Math.sin(t * 0.3) * 0.01)),
          Math.max(0, Math.min(1, prev[1] + (ef("resolutionCraving") - 0.5) * 0.02 + Math.sin(t * 0.5) * 0.015)),
          Math.max(0, Math.min(1, prev[2] + (ef("salienceSensitivity") - 0.5) * 0.025 + Math.sin(t * 0.7) * 0.012)),
          Math.max(0, Math.min(1, prev[3] + (ef("monotonyTolerance") - 0.5) * 0.015 + Math.sin(t * 0.2) * 0.008)),
          Math.max(0, Math.min(1, prev[4] + (ef("tensionAppetite") * 0.01 + avgEmphasis * 0.005 - 0.005) + Math.sin(t * 0.4) * 0.02)),
        ];

        if (newStates[4] > peakReward) setPeakReward(newStates[4]);
        return newStates;
      });

      if (Math.random() > 0.92) organismRef.current?.pulse(0.5);
    }, 1000);

    return () => clearInterval(interval);
  }, [sessionState, axisEmphasis, avgEmphasis, peakReward]);

  const handleStart = useCallback(() => {
    if (mode === "duo" && selectedFriend) {
      setDuoWaiting(true);
      organismRef.current?.pulse(0.5);
    } else {
      setSessionState("performing");
      setSessionTime(0);
      setBeliefStates([0.5, 0.5, 0.5, 0.5, 0.3]);
      setPeakReward(0.3);
      organismRef.current?.pulse(0.8);
    }
  }, [mode, selectedFriend]);

  const handleStop = useCallback(() => {
    setSessionState("finished");
    setDuoWaiting(false);
    organismRef.current?.pulse(0.3);
  }, []);

  // Duo waiting → performing after 5 seconds
  useEffect(() => {
    if (!duoWaiting) return;
    const timeout = setTimeout(() => {
      setDuoWaiting(false);
      setSessionState("performing");
      setSessionTime(0);
      setBeliefStates([0.5, 0.5, 0.5, 0.5, 0.3]);
      setPeakReward(0.3);
      organismRef.current?.pulse(0.8);
    }, 5000);
    return () => clearTimeout(timeout);
  }, [duoWaiting]);

  const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

  return (
    <motion.div {...pageTransition} className="h-screen bg-black relative overflow-hidden flex flex-col">
      <div className="cinematic-vignette" />

      {/* Organism — responsive to session state */}
      <div className="absolute inset-0 z-0 opacity-[0.12] pointer-events-none">
        <MindOrganismCanvas
          ref={organismRef}
          color={sessionState === "performing" ? beliefColors.reward.primary : beliefColors.tempo.primary}
          secondaryColor={beliefColors.reward.primary}
          stage={sessionState === "performing" ? 2 : 1}
          intensity={sessionState === "performing" ? 0.5 + avgEmphasis * 0.4 : 0.3}
          breathRate={sessionState === "performing" ? 2 + avgEmphasis * 3 : 5}
          variant="hero"
          constellations
          className="w-full h-full"
          interactive={false}
        />
      </div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10 w-full px-3 flex-1 min-h-0 flex flex-col pt-0 pb-1">
        {/* ── Main layout ──────────────────────────────────── */}
        <div className="grid grid-cols-12 gap-2 flex-1 min-h-0">

          {/* ═ LEFT: Axis bars ═══════════════════════════════ */}
          <div className="col-span-3 flex flex-col gap-2 overflow-y-auto scrollbar-thin">
              {/* Strengthen Your Edge */}
              <motion.div variants={slideUp} className="spatial-card p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Shield size={14} style={{ color }} />
                  <span className="hud-label text-[9px]">Strengthen Your Edge</span>
                </div>
                {persona && (
                  <p className="text-[9px] text-slate-600 font-body font-light mb-2">
                    As a <span style={{ color }} className="font-medium">{persona.name}</span>, lean into what makes you powerful.
                  </p>
                )}
                <div className="space-y-2.5">
                  {strong.map((axisKey) => {
                    const meta = AXIS_META[axisKey];
                    const axisColor = beliefColors[meta.belief].primary;
                    const val = axisEmphasis[axisKey] ?? 50;
                    return (
                      <div key={axisKey}>
                        <div className="flex items-center justify-between mb-0.5">
                          <div className="flex items-center gap-1.5">
                            <NucleusDot color={axisColor} size={2} active />
                            <span className="text-[11px] font-display text-slate-300">{meta.label}</span>
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: axisColor }}>{val}%</span>
                        </div>
                        <input type="range" min={0} max={100} value={val}
                          onChange={(e) => setEmphasis(axisKey, Number(e.target.value))}
                          className="w-full h-[3px] rounded-full appearance-none cursor-pointer mb-0.5"
                          style={{ background: `linear-gradient(90deg, ${axisColor} ${val}%, rgba(255,255,255,0.05) ${val}%)`, accentColor: axisColor }}
                        />
                        <p className="text-[8px] text-slate-600 font-body font-light leading-relaxed">
                          {meta.strengthen[family]}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </motion.div>

              {/* Develop New Ground */}
              <motion.div variants={slideUp} className="spatial-card p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Sprout size={14} style={{ color: beliefColors.salience.primary }} />
                  <span className="hud-label text-[9px]">Develop New Ground</span>
                </div>
                {persona && (
                  <p className="text-[9px] text-slate-600 font-body font-light mb-2">
                    Expand your <span style={{ color: beliefColors.salience.primary }} className="font-medium">{persona.family}</span> mind into new territory.
                  </p>
                )}
                <div className="space-y-2.5">
                  {weak.map((axisKey) => {
                    const meta = AXIS_META[axisKey];
                    const axisColor = beliefColors[meta.belief].primary;
                    const val = axisEmphasis[axisKey] ?? 50;
                    return (
                      <div key={axisKey}>
                        <div className="flex items-center justify-between mb-0.5">
                          <div className="flex items-center gap-1.5">
                            <NucleusDot color={axisColor} size={2} active />
                            <span className="text-[11px] font-display text-slate-300">{meta.label}</span>
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: axisColor }}>{val}%</span>
                        </div>
                        <input type="range" min={0} max={100} value={val}
                          onChange={(e) => setEmphasis(axisKey, Number(e.target.value))}
                          className="w-full h-[3px] rounded-full appearance-none cursor-pointer mb-0.5"
                          style={{ background: `linear-gradient(90deg, ${axisColor} ${val}%, rgba(255,255,255,0.05) ${val}%)`, accentColor: axisColor }}
                        />
                        <p className="text-[8px] text-slate-600 font-body font-light leading-relaxed">
                          {meta.develop[family]}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </motion.div>
            </div>

          {/* ═ CENTER: iPhone mockup + controls ══════════════ */}
          <div className="col-span-6 flex flex-col items-center gap-2 min-h-0">
              {/* Phone wrapper — fills available height, phone derives width from aspect-ratio */}
              <div className="flex-1 min-h-0 flex items-start justify-center w-full">
              <motion.div
                variants={fadeIn}
                initial="initial"
                animate="animate"
                className="relative h-full"
                style={{ aspectRatio: "9 / 19.5", maxWidth: 618, maxHeight: "100%" }}
              >
                {/* Outer bezel */}
                <div
                  className="absolute inset-0 rounded-[56px] overflow-hidden"
                  style={{ border: "3px solid rgba(255,255,255,0.08)", background: "#050505" }}
                >
                  {/* Dynamic Island */}
                  <div className="absolute top-[14px] left-1/2 -translate-x-1/2 w-[100px] h-[28px] bg-black rounded-full z-20" style={{ border: "1px solid rgba(255,255,255,0.06)" }} />

                  {/* Screen area */}
                  <div className="absolute inset-[3px] rounded-[53px] overflow-hidden">
                    {/* Ambient glow background */}
                    <motion.div
                      className="absolute inset-0"
                      animate={{
                        background: sessionState === "performing"
                          ? [`radial-gradient(circle at 50% 40%, ${beliefColors.reward.primary}20, ${color}08, transparent 70%)`,
                             `radial-gradient(circle at 50% 60%, ${color}20, ${beliefColors.reward.primary}08, transparent 70%)`,
                             `radial-gradient(circle at 50% 40%, ${beliefColors.reward.primary}20, ${color}08, transparent 70%)`]
                          : `radial-gradient(circle at 50% 45%, ${color}12, transparent 65%)`,
                      }}
                      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                    />

                    {/* Mini belief bars */}
                    <div className="absolute top-[52px] left-5 right-5 z-10">
                      <div className="flex gap-1.5">
                        {BELIEF_NAMES.map((b, i) => (
                          <div key={b} className="flex-1">
                            <div className="h-[3px] rounded-full" style={{ background: `${beliefColors[b].primary}20` }}>
                              <motion.div
                                className="h-full rounded-full"
                                style={{ background: beliefColors[b].primary }}
                                animate={{ width: `${beliefStates[i] * 100}%` }}
                                transition={{ duration: 0.5 }}
                              />
                            </div>
                            <span className="text-[7px] font-mono block text-center mt-0.5" style={{ color: `${beliefColors[b].primary}60` }}>{b.slice(0, 3)}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Center content */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center px-4">
                      {/* Title + toggle — hidden during performing */}
                      {sessionState !== "performing" && (
                        <>
                          <span className="text-[13px] font-display font-bold text-slate-200 tracking-wide">Live Performance</span>
                          <div className="mt-2">
                            <div className="flex rounded-full p-0.5" style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.08)" }}>
                              {(["solo", "duo"] as const).map((m) => (
                                <button key={m} onClick={() => setMode(m)} disabled={sessionState === "performing"}
                                  className="px-3 py-0.5 rounded-full text-[9px] font-display font-medium transition-all duration-300 disabled:opacity-50"
                                  style={{
                                    background: mode === m ? `${color}20` : "transparent",
                                    color: mode === m ? "#E2E8F0" : "#64748B",
                                    border: mode === m ? `1px solid ${color}30` : "1px solid transparent",
                                  }}
                                >
                                  {m === "solo" ? "Solo" : "Duo"}
                                </button>
                              ))}
                            </div>
                          </div>
                        </>
                      )}

                      {/* State-specific content */}
                      {duoWaiting ? (
                        <>
                          <motion.div
                            className="mt-6"
                            animate={{ scale: [1, 1.3, 1], opacity: [0.4, 1, 0.4] }}
                            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                          >
                            <NucleusDot color={color} size={18} active pulsing />
                          </motion.div>
                          <span className="text-[11px] font-display text-slate-300 mt-4">Sending performance invite...</span>
                          <span className="text-[9px] font-mono mt-2" style={{ color: `${color}60` }}>Waiting for the other Mind</span>
                          <motion.div
                            className="w-16 h-[2px] mt-4 rounded-full"
                            style={{ background: color }}
                            animate={{ scaleX: [0, 1, 0], opacity: [0.3, 0.8, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                          />
                        </>
                      ) : sessionState === "performing" ? (
                        null
                      ) : sessionState === "finished" ? (
                        <>
                          <span className="text-sm font-display text-slate-500 mt-6 mb-2">Session Complete</span>
                          <span className="hud-value text-3xl" style={{ color: beliefColors.reward.primary }}>{(peakReward * 100).toFixed(0)}</span>
                          <span className="text-[9px] font-mono text-slate-600 mt-1">Peak Reward</span>
                          <button onClick={() => { setSessionState("idle"); }} className="mt-4 px-5 py-2 rounded-full text-[11px] font-display text-slate-300 transition-all"
                            style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)" }}>
                            New Session
                          </button>
                        </>
                      ) : mode === "solo" ? (
                        <>
                          <div className="mt-5"><NucleusDot color={color} size={14} active pulsing /></div>
                          <span className="text-sm font-display text-slate-400 mt-3">{persona?.name ?? "Ready"}</span>
                          <span className="text-[10px] font-mono mt-1" style={{ color: `${color}80` }}>{persona?.family}</span>
                          <button onClick={handleStart} className="mt-5 px-6 py-2.5 rounded-full text-[12px] font-display font-medium text-white transition-all"
                            style={{ background: `linear-gradient(135deg, ${color}, ${beliefColors.reward.primary})`, boxShadow: `0 0 20px ${color}30` }}>
                            <Play size={14} className="inline mr-1.5 -mt-px" /> Start Solo
                          </button>
                        </>
                      ) : (
                        <div className="mt-4 w-full overflow-y-auto" style={{ maxHeight: "60%" }}>
                          {!selectedFriend ? (
                            /* ── Friends list ── */
                            <div className="space-y-1.5">
                              <div className="flex items-center gap-1.5 mb-1.5">
                                <Users size={10} className="text-slate-500" />
                                <span className="text-[8px] font-display text-slate-500 uppercase tracking-wider">Choose Partner</span>
                              </div>
                              {mockUsers.slice(0, 3).map((friend) => {
                                const fp = getPersona(friend.mind.personaId);
                                return (
                                  <button key={friend.id} onClick={() => setSelectedFriend(friend)}
                                    className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg transition-all"
                                    style={{
                                      background: "rgba(255,255,255,0.03)",
                                      border: "1px solid rgba(255,255,255,0.06)",
                                    }}>
                                    <img src={friend.avatarUrl} alt={friend.displayName}
                                      className="w-7 h-7 rounded-full object-cover flex-shrink-0"
                                      style={{ border: `1.5px solid ${fp.color}40` }}
                                      onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
                                    />
                                    <div className="text-left flex-1 min-w-0">
                                      <div className="text-[9px] font-display text-slate-300 truncate">{friend.displayName}</div>
                                      <div className="text-[7px] font-mono truncate" style={{ color: fp.color }}>{fp.name}</div>
                                    </div>
                                    <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: `${fp.color}40` }} />
                                  </button>
                                );
                              })}
                            </div>
                          ) : (
                            /* ── Selected friend + game conditions ── */
                            (() => {
                              const fp = getPersona(selectedFriend.mind.personaId);
                              const diffColor = duoConditions ? DIFFICULTY_COLORS[duoConditions.difficulty] : color;
                              return (
                                <div className="space-y-2">
                                  {/* Selected friend header */}
                                  <div className="flex items-center gap-2.5 px-2 py-1.5 rounded-lg"
                                    style={{ background: `${fp.color}12`, border: `1px solid ${fp.color}25` }}>
                                    <img src={selectedFriend.avatarUrl} alt={selectedFriend.displayName}
                                      className="w-7 h-7 rounded-full object-cover flex-shrink-0"
                                      style={{ border: `1.5px solid ${fp.color}50` }}
                                      onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
                                    />
                                    <div className="flex-1 min-w-0">
                                      <div className="text-[9px] font-display text-slate-200 truncate">{selectedFriend.displayName}</div>
                                      <div className="text-[7px] font-mono truncate" style={{ color: fp.color }}>{fp.name} · {fp.family}</div>
                                    </div>
                                    <button onClick={() => setSelectedFriend(null)} className="text-slate-600 hover:text-slate-400 transition-colors">
                                      <X size={10} />
                                    </button>
                                  </div>

                                  {/* Compact game conditions */}
                                  {duoConditions && (
                                    <>
                                      <div className="px-2 py-1.5 rounded-lg" style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}>
                                        <div className="flex items-center justify-between mb-1">
                                          <div className="flex items-center gap-1">
                                            <Target size={8} style={{ color: beliefColors.salience.primary }} />
                                            <span className="text-[8px] font-display text-slate-400">{duoConditions.task}</span>
                                          </div>
                                          <span className="text-[7px] font-mono px-1.5 py-0.5 rounded-full" style={{ color: diffColor, background: `${diffColor}15` }}>
                                            {duoConditions.difficulty}
                                          </span>
                                        </div>
                                        <p className="text-[7px] text-slate-600 font-body leading-relaxed">{duoConditions.taskDetail}</p>
                                      </div>
                                      <div className="flex items-center justify-between px-2">
                                        <div className="flex items-center gap-1">
                                          <Trophy size={8} style={{ color: beliefColors.reward.primary }} />
                                          <span className="text-[8px] font-mono" style={{ color: beliefColors.reward.primary }}>{duoConditions.xpReward} XP</span>
                                        </div>
                                        <span className="text-[7px] font-mono text-slate-600">{duoConditions.goalMetric}</span>
                                      </div>
                                    </>
                                  )}

                                  {/* Start button */}
                                  <button onClick={handleStart} className="w-full mt-1 px-4 py-2 rounded-full text-[10px] font-display font-medium text-white transition-all"
                                    style={{ background: `linear-gradient(135deg, ${color}, ${beliefColors.reward.primary})`, boxShadow: `0 0 15px ${color}30` }}>
                                    <Play size={12} className="inline mr-1.5 -mt-px" /> Start Duo
                                  </button>
                                </div>
                              );
                            })()
                          )}
                        </div>
                      )}
                    </div>

                    {/* Duo session videos — appear during performing */}
                    {mode === "duo" && sessionState === "performing" && (
                      <>
                        <motion.div
                          className="absolute bottom-[70px] right-3 z-20 rounded-xl overflow-hidden shadow-lg"
                          style={{ width: "52%", maxWidth: 150, border: "1px solid rgba(255,255,255,0.1)" }}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.5 }}
                        >
                          <LoopingVideo src="/Duo/Gen-4 Turbo having so much fun 1052318284.mp4" className="w-full object-cover rounded-xl" />
                        </motion.div>
                        <motion.div
                          className="absolute top-[70px] left-3 z-20 rounded-xl overflow-hidden shadow-lg"
                          style={{ width: "52%", maxWidth: 150, border: "1px solid rgba(255,255,255,0.1)" }}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.5, delay: 0.3 }}
                        >
                          <LoopingVideo src="/Duo/Gen-4 Turbo having so much fun hareketli ve heyecanli 2494731309.mp4" className="w-full object-cover rounded-xl" />
                        </motion.div>
                      </>
                    )}

                    {/* Bottom: active controllers indicator */}
                    <div className="absolute bottom-7 left-5 right-5 z-10">
                      <div className="flex justify-center gap-2">
                        {[...EMOTIONAL_CONTROLLERS, ...PHYSICAL_CONTROLLERS].map((c) => (
                          <motion.div
                            key={c.id}
                            className="w-2 h-2 rounded-full"
                            style={{ background: activeControllers.has(c.id) ? c.color : "rgba(255,255,255,0.06)" }}
                            animate={{ opacity: activeControllers.has(c.id) ? [0.6, 1, 0.6] : 0.3 }}
                            transition={{ duration: 2, repeat: Infinity }}
                          />
                        ))}
                      </div>
                      <span className="text-[8px] font-mono text-slate-700 block text-center mt-1.5">
                        {activeControllers.size > 0 ? `${activeControllers.size} active` : "No controllers"}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Side buttons */}
                <div className="absolute -left-[2px] top-[28%] w-[3px] h-[5%] rounded-l bg-slate-800" />
                <div className="absolute -left-[2px] top-[36%] w-[3px] h-[8%] rounded-l bg-slate-800" />
                <div className="absolute -left-[2px] top-[47%] w-[3px] h-[8%] rounded-l bg-slate-800" />
                <div className="absolute -right-[2px] top-[34%] w-[3px] h-[10%] rounded-r bg-slate-800" />
              </motion.div>
              </div>
            </div>

          {/* ═ RIGHT: Controllers ════════════════════════════ */}
          <div className="col-span-3 flex flex-col gap-2 overflow-y-auto scrollbar-thin">
              {/* Emotional Controllers */}
              <motion.div variants={slideUp} className="spatial-card p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Heart size={14} className="text-pink-400" />
                  <span className="hud-label text-[9px]">Emotional</span>
                </div>
                <div className="space-y-2">
                  {EMOTIONAL_CONTROLLERS.map(({ id, label, description, Icon, color: cColor }) => {
                    const isActive = activeControllers.has(id);
                    return (
                      <button
                        key={id}
                        onClick={() => toggleController(id)}
                        className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg transition-all duration-300"
                        style={{
                          background: isActive ? `${cColor}12` : "rgba(255,255,255,0.02)",
                          border: `1px solid ${isActive ? `${cColor}30` : "rgba(255,255,255,0.04)"}`,
                        }}
                      >
                        <Icon size={14} style={{ color: isActive ? cColor : "#475569" }} />
                        <div className="flex-1 text-left">
                          <div className="text-[11px] font-display" style={{ color: isActive ? "#E2E8F0" : "#64748B" }}>{label}</div>
                          <div className="text-[8px] font-mono text-slate-700">{description}</div>
                        </div>
                        <motion.div
                          className="w-2 h-2 rounded-full flex-shrink-0"
                          style={{ background: isActive ? cColor : "rgba(255,255,255,0.06)" }}
                          animate={{ opacity: isActive ? [0.5, 1, 0.5] : 0.3 }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                      </button>
                    );
                  })}
                </div>
              </motion.div>

              {/* Physical Controllers */}
              <motion.div variants={slideUp} className="spatial-card p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Activity size={14} className="text-red-400" />
                  <span className="hud-label text-[9px]">Physical</span>
                </div>
                <div className="space-y-2">
                  {PHYSICAL_CONTROLLERS.map(({ id, label, description, Icon, color: cColor }) => {
                    const isActive = activeControllers.has(id);
                    return (
                      <button
                        key={id}
                        onClick={() => toggleController(id)}
                        className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg transition-all duration-300"
                        style={{
                          background: isActive ? `${cColor}12` : "rgba(255,255,255,0.02)",
                          border: `1px solid ${isActive ? `${cColor}30` : "rgba(255,255,255,0.04)"}`,
                        }}
                      >
                        <Icon size={14} style={{ color: isActive ? cColor : "#475569" }} />
                        <div className="flex-1 text-left">
                          <div className="text-[11px] font-display" style={{ color: isActive ? "#E2E8F0" : "#64748B" }}>{label}</div>
                          <div className="text-[8px] font-mono text-slate-700">{description}</div>
                        </div>
                        <motion.div
                          className="w-2 h-2 rounded-full flex-shrink-0"
                          style={{ background: isActive ? cColor : "rgba(255,255,255,0.06)" }}
                          animate={{ opacity: isActive ? [0.5, 1, 0.5] : 0.3 }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                      </button>
                    );
                  })}
                </div>
              </motion.div>
          </div>
        </div>



      </motion.div>
    </motion.div>
  );
}

/* ── Ping-pong video: forward → reverse → forward, never stops ── */
function LoopingVideo({ src, className }: { src: string; className?: string }) {
  const ref = useRef<HTMLVideoElement>(null);
  const dir = useRef<1 | -1>(1);
  const raf = useRef(0);
  const prev = useRef(0);

  useEffect(() => {
    const v = ref.current;
    if (!v) return;
    let alive = true;

    /* reverse tick: step currentTime backward each frame */
    const tick = (ts: number) => {
      if (!alive) return;
      if (!prev.current) prev.current = ts;
      const dt = (ts - prev.current) / 1000;
      prev.current = ts;
      const t = v.currentTime - dt;
      if (t <= 0) {
        /* reached start → play forward */
        v.currentTime = 0;
        dir.current = 1;
        prev.current = 0;
        v.play().catch(() => {});
        return;
      }
      v.currentTime = t;
      raf.current = requestAnimationFrame(tick);
    };

    /* detect near-end while playing forward */
    const onUpdate = () => {
      if (dir.current !== 1 || !v.duration) return;
      if (v.currentTime >= v.duration - 0.15) {
        v.pause();
        dir.current = -1;
        prev.current = 0;
        raf.current = requestAnimationFrame(tick);
      }
    };

    v.addEventListener("timeupdate", onUpdate);
    /* also catch ended as safety net */
    v.addEventListener("ended", () => {
      if (dir.current === 1) { v.pause(); dir.current = -1; prev.current = 0; raf.current = requestAnimationFrame(tick); }
    });
    v.muted = true;
    v.playsInline = true;
    dir.current = 1;
    v.play().catch(() => {});

    return () => { alive = false; v.removeEventListener("timeupdate", onUpdate); cancelAnimationFrame(raf.current); };
  }, []);

  return <video ref={ref} src={src} muted playsInline preload="auto" className={className} />;
}
