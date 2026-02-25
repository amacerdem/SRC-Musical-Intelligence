import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play, Square, Shield, Sprout, Users, Target, Trophy, X,
  Heart, Sparkles, Layers, RotateCcw, Gauge, Activity, BarChart3, LayoutGrid,
} from "lucide-react";
import { MindOrganismCanvas, type OrganismHandle } from "@/components/mind/MindOrganismCanvas";
import { DuoOrganismCanvas, type DuoOrganismHandle } from "@/components/mind/DuoOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { mockUsers } from "@/data/mock-users";
import { pageTransition, staggerChildren, slideUp, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useAnalysisData } from "@/components/viz/hooks/useAnalysisData";
import { getFrameInterp, sampleTrace } from "@/components/viz/hooks/useAudioSync";
import type { AnalysisFrame } from "@/canvas/duo-organism";
import type { MindAxes, NeuralFamily } from "@/types/mind";
import type { UserProfile } from "@/types/social";
import type { GameEvent } from "@/game/duo-game-engine";

type Mode = "solo" | "duo";
type SessionState = "idle" | "performing" | "finished";

/* ── Axis training metadata ──────────────────────────────────── */
const AXIS_KEYS: (keyof MindAxes)[] = [
  "entropyTolerance", "resolutionCraving", "monotonyTolerance",
  "salienceSensitivity", "tensionAppetite",
];

const AXIS_META: Record<keyof MindAxes, {
  belief: keyof typeof beliefColors;
}> = {
  entropyTolerance: { belief: "consonance" },
  resolutionCraving: { belief: "tempo" },
  monotonyTolerance: { belief: "familiarity" },
  salienceSensitivity: { belief: "salience" },
  tensionAppetite: { belief: "reward" },
};

function splitAxes(axes: MindAxes): { strong: (keyof MindAxes)[]; weak: (keyof MindAxes)[] } {
  const sorted = AXIS_KEYS.slice().sort((a, b) => axes[b] - axes[a]);
  return { strong: sorted.slice(0, 3), weak: sorted.slice(3) };
}

/* ── Duo session game conditions ──────────────────────────────── */

interface DuoConditions {
  taskAxisKey: keyof MindAxes;
  goalType: "sameFamily" | "crossFamily";
  myFamily: string;
  friendFamily: string;
  xpReward: number;
  difficulty: "Easy" | "Medium" | "Hard" | "Legendary";
}

const DIFFICULTY_COLORS: Record<DuoConditions["difficulty"], string> = {
  Easy: "#10B981",
  Medium: "#F59E0B",
  Hard: "#EF4444",
  Legendary: "#A855F7",
};

/* ── Controllers ─────────────────────────────────────────────── */

const EMOTIONAL_CONTROLLERS = [
  { id: "valence", Icon: Heart, color: "#EC4899" },
  { id: "arousal", Icon: Sparkles, color: "#F59E0B" },
  { id: "depth", Icon: Layers, color: "#8B5CF6" },
  { id: "nostalgia", Icon: RotateCcw, color: "#38BDF8" },
];

const PHYSICAL_CONTROLLERS = [
  { id: "tempo", Icon: Gauge, color: "#F97316" },
  { id: "energy", Icon: Activity, color: "#EF4444" },
  { id: "dynamics", Icon: BarChart3, color: "#84CC16" },
  { id: "density", Icon: LayoutGrid, color: "#06B6D4" },
];

function generateDuoConditions(
  myAxes: MindAxes,
  friendAxes: MindAxes,
  myFamily: NeuralFamily,
  friendFamily: NeuralFamily,
): DuoConditions {
  const gaps = AXIS_KEYS.map((k) => ({ key: k, gap: Math.abs(myAxes[k] - friendAxes[k]) }));
  gaps.sort((a, b) => b.gap - a.gap);

  const totalDist = gaps.reduce((s, g) => s + g.gap, 0);
  const difficulty: DuoConditions["difficulty"] =
    totalDist > 2.5 ? "Legendary" : totalDist > 1.8 ? "Hard" : totalDist > 1.0 ? "Medium" : "Easy";

  return {
    taskAxisKey: gaps[0].key,
    goalType: myFamily === friendFamily ? "sameFamily" : "crossFamily",
    myFamily,
    friendFamily,
    xpReward: Math.round(200 + totalDist * 400),
    difficulty,
  };
}

function formatSessionTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

export function LivePerformance() {
  const { t } = useTranslation();
  const [mode, setMode] = useState<Mode>("solo");
  const [sessionState, setSessionState] = useState<SessionState>("idle");
  const [sessionTime, setSessionTime] = useState(0);
  const [beliefStates, setBeliefStates] = useState([0.5, 0.5, 0.5, 0.5, 0.5]);
  const [peakReward, setPeakReward] = useState(0);

  const [axisEmphasis, setAxisEmphasis] = useState<Record<string, number>>({});
  const [selectedFriend, setSelectedFriend] = useState<UserProfile | null>(null);
  const [activeControllers, setActiveControllers] = useState<Set<string>>(new Set());
  const [duoWaiting, setDuoWaiting] = useState(false);

  // Game state
  const [gameScore, setGameScore] = useState(0);
  const [gameCombo, setGameCombo] = useState(1);
  const [gameToasts, setGameToasts] = useState<{ id: string; icon: string; name: string; xp: number; ts: number }[]>([]);
  const [activeGameTask, setActiveGameTask] = useState<{ name: string; description: string; progress: number; xp: number; remaining: number } | null>(null);
  const [finalScore, setFinalScore] = useState(0);
  const [achievementCount, setAchievementCount] = useState(0);
  const [duoStarted, setDuoStarted] = useState(false);

  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const identity = useActiveIdentity();
  const color = identity.color;
  const family = identity.family;
  const organismRef = useRef<OrganismHandle>(null);
  const duoOrganismRef = useRef<DuoOrganismHandle>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // ── Analysis data for data-driven duo animation ──
  const { data: analysisData } = useAnalysisData();

  // Precompute min/max for normalization of each trace to [0,1]
  const traceRanges = useMemo(() => {
    if (!analysisData) return null;
    const range = (arr: number[]) => {
      let mn = Infinity, mx = -Infinity;
      for (const v of arr) { if (v < mn) mn = v; if (v > mx) mx = v; }
      return { min: mn, max: mx, span: Math.max(mx - mn, 0.001) };
    };
    return {
      // Beliefs
      consonance: range(analysisData.beliefs.consonance),
      tempo: range(analysisData.beliefs.tempo),
      salience: range(analysisData.beliefs.salience),
      familiarity: range(analysisData.beliefs.familiarity),
      reward: range(analysisData.beliefs.reward),
      // R3 groups
      r3: Object.keys(analysisData.r3_groups).filter(k => k !== "time_s")
        .map(k => range((analysisData.r3_groups as Record<string, number[]>)[k])),
      // Prediction errors
      pe: ["consonance", "tempo", "salience", "familiarity"].map(
        k => range(analysisData.prediction_errors[k as keyof typeof analysisData.prediction_errors])
      ),
      // Precision
      prec: ["consonance", "tempo", "salience", "familiarity"].map(
        k => range(analysisData.precision[k as keyof typeof analysisData.precision])
      ),
      // RAM (per region)
      ram: analysisData.ram.regions.map(
        r => range(analysisData.ram.traces[r])
      ),
      // Relays
      relays: [
        range(analysisData.relays.bch_consonance_signal),
        range(analysisData.relays.hmce_a1_encoding),
        range(analysisData.relays.snem_entrainment),
        range(analysisData.relays.mmp_familiarity),
        range(analysisData.relays.daed_wanting),
        range(analysisData.relays.daed_liking),
        range(analysisData.relays.mpg_onset),
      ],
    };
  }, [analysisData]);

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

  // Duo 3-second delay — organism canvas mounts immediately but animation + audio start after 3s
  useEffect(() => {
    if (sessionState !== "performing" || mode !== "duo") {
      setDuoStarted(false);
      return;
    }
    const timeout = setTimeout(() => {
      setDuoStarted(true);
      // Start audio
      if (!audioRef.current) {
        audioRef.current = new Audio("/music/Shifting Rooms.mp3");
        audioRef.current.loop = true;
      }
      audioRef.current.currentTime = 0;
      audioRef.current.play().catch(() => {});
    }, 3000);
    return () => clearTimeout(timeout);
  }, [sessionState, mode]);

  // Duo animation — driven by analysis JSON synced to audio
  useEffect(() => {
    if (!duoStarted || sessionState !== "performing" || mode !== "duo") return;
    let alive = true;

    const norm = (value: number, r: { min: number; span: number }) =>
      Math.max(0, Math.min(1, (value - r.min) / r.span));

    // R3 group keys in order
    const r3Keys = [
      "A_consonance", "B_energy", "C_timbre", "D_change",
      "F_pitch", "G_rhythm", "H_harmony", "J_ext_timbre", "K_modulation",
    ];
    const relayKeys: (keyof NonNullable<typeof analysisData>["relays"])[] = [
      "bch_consonance_signal", "hmce_a1_encoding", "snem_entrainment",
      "mmp_familiarity", "daed_wanting", "daed_liking", "mpg_onset",
    ];

    const tick = () => {
      if (!alive) return;

      if (analysisData && traceRanges && audioRef.current) {
        const currentTime = audioRef.current.currentTime;
        const duration = analysisData.meta.duration_s;
        const tp = analysisData.meta.trace_points;
        const { index, frac, nextIndex } = getFrameInterp(currentTime, duration, tp);

        // Sample & normalize all traces into a full AnalysisFrame
        const frame: AnalysisFrame = {
          beliefs: {
            consonance: norm(sampleTrace(analysisData.beliefs.consonance, index, frac, nextIndex), traceRanges.consonance),
            tempo: norm(sampleTrace(analysisData.beliefs.tempo, index, frac, nextIndex), traceRanges.tempo),
            salience: norm(sampleTrace(analysisData.beliefs.salience, index, frac, nextIndex), traceRanges.salience),
            familiarity: norm(sampleTrace(analysisData.beliefs.familiarity, index, frac, nextIndex), traceRanges.familiarity),
            reward: norm(sampleTrace(analysisData.beliefs.reward, index, frac, nextIndex), traceRanges.reward),
          },
          r3: r3Keys.map((k, i) =>
            norm(sampleTrace((analysisData.r3_groups as Record<string, number[]>)[k], index, frac, nextIndex), traceRanges.r3[i])
          ),
          pe: [0, 1, 2, 3].map(i => {
            const k = (["consonance", "tempo", "salience", "familiarity"] as const)[i];
            return norm(sampleTrace(analysisData.prediction_errors[k], index, frac, nextIndex), traceRanges.pe[i]);
          }),
          precision: [0, 1, 2, 3].map(i => {
            const k = (["consonance", "tempo", "salience", "familiarity"] as const)[i];
            return norm(sampleTrace(analysisData.precision[k], index, frac, nextIndex), traceRanges.prec[i]);
          }),
          ram: analysisData.ram.regions.map((r, i) =>
            norm(sampleTrace(analysisData.ram.traces[r], index, frac, nextIndex), traceRanges.ram[i])
          ),
          relays: relayKeys.map((k, i) =>
            norm(sampleTrace(analysisData.relays[k], index, frac, nextIndex), traceRanges.relays[i])
          ),
        };

        // Push full frame to DuoOrganism — drives all data-driven visuals
        duoOrganismRef.current?.setAnalysisFrame(frame);

        // Update belief bar display
        setBeliefStates([
          frame.beliefs.consonance,
          frame.beliefs.tempo,
          frame.beliefs.salience,
          frame.beliefs.familiarity,
          frame.beliefs.reward,
        ]);
        if (frame.beliefs.reward > peakReward) setPeakReward(frame.beliefs.reward);
      } else {
        // Fallback: simple sine simulation when JSON not loaded
        const t = performance.now() / 1000;
        const noiseish = (time: number, seed: number) =>
          0.5 + 0.35 * Math.sin(time * (0.3 + seed * 0.2)) + 0.15 * Math.sin(time * 0.7 + seed * 3.7);
        const emo = [0, 1, 2, 3].map(i => Math.max(0, Math.min(1, noiseish(t, i))));
        const phys = [0, 1, 2, 3].map(i => Math.max(0, Math.min(1, noiseish(t, i + 10))));
        duoOrganismRef.current?.updateParams(emo, phys);
      }

      // Update game state from engine
      const gs = duoOrganismRef.current?.getGameState();
      if (gs) {
        setGameScore(Math.round(gs.score));
        setGameCombo(gs.combo);
        if (gs.activeTask) {
          setActiveGameTask({
            name: gs.activeTask.task.name,
            description: gs.activeTask.task.description,
            progress: gs.activeTask.progress,
            xp: gs.activeTask.task.xp,
            remaining: Math.max(0, gs.activeTask.task.durationSec - (gs.sessionTime - gs.activeTask.startTime)),
          });
        } else {
          setActiveGameTask(null);
        }
      }

      requestAnimationFrame(tick);
    };
    const id = requestAnimationFrame(tick);
    return () => { alive = false; cancelAnimationFrame(id); };
  }, [duoStarted, sessionState, mode, analysisData, traceRanges]);

  // Handle game events from DuoOrganismCanvas
  const handleGameEvent = useCallback((events: GameEvent[]) => {
    for (const ev of events) {
      if (ev.type === "achievement" && ev.achievement) {
        const a = ev.achievement;
        setGameToasts(prev => [...prev.slice(-4), { id: a.id, icon: a.icon, name: a.name, xp: ev.xp ?? a.xp, ts: Date.now() }]);
        setAchievementCount(prev => prev + 1);
      }
      if (ev.type === "task_complete" && ev.task) {
        setGameToasts(prev => [...prev.slice(-4), { id: ev.task!.id + "_done", icon: "✓", name: ev.task!.name, xp: ev.xp ?? ev.task!.xp, ts: Date.now() }]);
      }
    }
  }, []);

  // Auto-remove toasts after 3s
  useEffect(() => {
    if (gameToasts.length === 0) return;
    const timeout = setTimeout(() => {
      setGameToasts(prev => prev.filter(t => Date.now() - t.ts < 3000));
    }, 3000);
    return () => clearTimeout(timeout);
  }, [gameToasts]);

  // Store final score when session ends
  const handleDuoStop = useCallback(() => {
    const gs = duoOrganismRef.current?.getGameState();
    if (gs) {
      setFinalScore(Math.round(gs.score));
      setAchievementCount(gs.achievements.size);
    }
    // Stop audio
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setDuoStarted(false);
    setSessionState("finished");
    setDuoWaiting(false);
    organismRef.current?.pulse(0.3);
  }, []);

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
                  <span className="hud-label text-[9px]">{t("live.strengthenEdge")}</span>
                </div>
                {persona && (
                  <p className="text-[9px] text-slate-600 font-body font-light mb-2">
                    <span style={{ color }} className="font-medium">{persona.name}</span>, {t("live.leanIntoPower")}
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
                            <span className="text-[11px] font-display text-slate-300">{t(`live.axes.${axisKey}`)}</span>
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: axisColor }}>{val}%</span>
                        </div>
                        <input type="range" min={0} max={100} value={val}
                          onChange={(e) => setEmphasis(axisKey, Number(e.target.value))}
                          className="w-full h-[3px] rounded-full appearance-none cursor-pointer mb-0.5"
                          style={{ background: `linear-gradient(90deg, ${axisColor} ${val}%, rgba(255,255,255,0.05) ${val}%)`, accentColor: axisColor }}
                        />
                        <p className="text-[8px] text-slate-600 font-body font-light leading-relaxed">
                          {t(`live.strengthen.${axisKey}.${family}`)}
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
                  <span className="hud-label text-[9px]">{t("live.developGround")}</span>
                </div>
                {persona && (
                  <p className="text-[9px] text-slate-600 font-body font-light mb-2">
                    {t("live.expandTerritory", { family })}
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
                            <span className="text-[11px] font-display text-slate-300">{t(`live.axes.${axisKey}`)}</span>
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: axisColor }}>{val}%</span>
                        </div>
                        <input type="range" min={0} max={100} value={val}
                          onChange={(e) => setEmphasis(axisKey, Number(e.target.value))}
                          className="w-full h-[3px] rounded-full appearance-none cursor-pointer mb-0.5"
                          style={{ background: `linear-gradient(90deg, ${axisColor} ${val}%, rgba(255,255,255,0.05) ${val}%)`, accentColor: axisColor }}
                        />
                        <p className="text-[8px] text-slate-600 font-body font-light leading-relaxed">
                          {t(`live.develop.${axisKey}.${family}`)}
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
                          <span className="text-[13px] font-display font-bold text-slate-200 tracking-wide">{t("live.title")}</span>
                          <div className="mt-2">
                            <div className="flex rounded-full p-0.5" style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.08)" }}>
                              {(["solo", "duo"] as const).map((m) => (
                                <button key={m} onClick={() => setMode(m)}
                                  className="px-3 py-0.5 rounded-full text-[9px] font-display font-medium transition-all duration-300 disabled:opacity-50"
                                  style={{
                                    background: mode === m ? `${color}20` : "transparent",
                                    color: mode === m ? "#E2E8F0" : "#64748B",
                                    border: mode === m ? `1px solid ${color}30` : "1px solid transparent",
                                  }}
                                >
                                  {m === "solo" ? t("live.solo") : t("live.duo")}
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
                          <span className="text-[11px] font-display text-slate-300 mt-4">{t("live.sendingInvite")}</span>
                          <span className="text-[9px] font-mono mt-2" style={{ color: `${color}60` }}>{t("live.waitingMind")}</span>
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
                        mode === "duo" ? (
                          <>
                            <span className="text-sm font-display text-slate-500 mt-4 mb-2">{t("live.duoSessionComplete")}</span>
                            <span className="hud-value text-3xl" style={{ color: beliefColors.reward.primary }}>{finalScore}</span>
                            <span className="text-[9px] font-mono text-slate-600 mt-1">{t("live.totalScore")}</span>
                            <div className="flex items-center gap-3 mt-3">
                              <div className="text-center">
                                <span className="text-[13px] font-display font-bold" style={{ color: beliefColors.salience.primary }}>{achievementCount}</span>
                                <span className="text-[7px] font-mono text-slate-600 block">{t("live.achievements")}</span>
                              </div>
                              <div className="w-px h-5 bg-white/5" />
                              <div className="text-center">
                                <span className="text-[13px] font-display font-bold text-slate-300">{formatSessionTime(sessionTime)}</span>
                                <span className="text-[7px] font-mono text-slate-600 block">{t("live.duration")}</span>
                              </div>
                            </div>
                            <button onClick={() => { setSessionState("idle"); setGameScore(0); setGameCombo(1); setFinalScore(0); setAchievementCount(0); setGameToasts([]); setActiveGameTask(null); }} className="mt-4 px-5 py-2 rounded-full text-[11px] font-display text-slate-300 transition-all"
                              style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)" }}>
                              {t("live.newSession")}
                            </button>
                          </>
                        ) : (
                          <>
                            <span className="text-sm font-display text-slate-500 mt-6 mb-2">{t("live.sessionComplete")}</span>
                            <span className="hud-value text-3xl" style={{ color: beliefColors.reward.primary }}>{(peakReward * 100).toFixed(0)}</span>
                            <span className="text-[9px] font-mono text-slate-600 mt-1">{t("live.peakReward")}</span>
                            <button onClick={() => { setSessionState("idle"); }} className="mt-4 px-5 py-2 rounded-full text-[11px] font-display text-slate-300 transition-all"
                              style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)" }}>
                              {t("live.newSession")}
                            </button>
                          </>
                        )
                      ) : mode === "solo" ? (
                        <>
                          <div className="mt-5"><NucleusDot color={color} size={14} active pulsing /></div>
                          <span className="text-sm font-display text-slate-400 mt-3">{persona?.name ?? t("live.ready")}</span>
                          <span className="text-[10px] font-mono mt-1" style={{ color: `${color}80` }}>{family}</span>
                          <button onClick={handleStart} className="mt-5 px-6 py-2.5 rounded-full text-[12px] font-display font-medium text-white transition-all"
                            style={{ background: `linear-gradient(135deg, ${color}, ${beliefColors.reward.primary})`, boxShadow: `0 0 20px ${color}30` }}>
                            <Play size={14} className="inline mr-1.5 -mt-px" /> {t("live.startSolo")}
                          </button>
                        </>
                      ) : (
                        <div className="mt-4 w-full overflow-y-auto" style={{ maxHeight: "60%" }}>
                          {!selectedFriend ? (
                            /* ── Friends list ── */
                            <div className="space-y-1.5">
                              <div className="flex items-center gap-1.5 mb-1.5">
                                <Users size={10} className="text-slate-500" />
                                <span className="text-[8px] font-display text-slate-500 uppercase tracking-wider">{t("live.choosePartner")}</span>
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
                                            <span className="text-[8px] font-display text-slate-400">{t(`live.duoTasks.${duoConditions.taskAxisKey}.task`)}</span>
                                          </div>
                                          <span className="text-[7px] font-mono px-1.5 py-0.5 rounded-full" style={{ color: diffColor, background: `${diffColor}15` }}>
                                            {t(`live.difficulty.${duoConditions.difficulty}`)}
                                          </span>
                                        </div>
                                        <p className="text-[7px] text-slate-600 font-body leading-relaxed">{t(`live.duoTasks.${duoConditions.taskAxisKey}.detail`)}</p>
                                      </div>
                                      <div className="flex items-center justify-between px-2">
                                        <div className="flex items-center gap-1">
                                          <Trophy size={8} style={{ color: beliefColors.reward.primary }} />
                                          <span className="text-[8px] font-mono" style={{ color: beliefColors.reward.primary }}>{duoConditions.xpReward} XP</span>
                                        </div>
                                        <span className="text-[7px] font-mono text-slate-600">{t(`live.duoGoalMetric.${duoConditions.goalType}`)}</span>
                                      </div>
                                    </>
                                  )}

                                  {/* Start button */}
                                  <button onClick={handleStart} className="w-full mt-1 px-4 py-2 rounded-full text-[10px] font-display font-medium text-white transition-all"
                                    style={{ background: `linear-gradient(135deg, ${color}, ${beliefColors.reward.primary})`, boxShadow: `0 0 15px ${color}30` }}>
                                    <Play size={12} className="inline mr-1.5 -mt-px" /> {t("live.startDuo")}
                                  </button>
                                </div>
                              );
                            })()
                          )}
                        </div>
                      )}
                    </div>

                    {/* ── Duo Generative Organism — fills phone during performing ── */}
                    {mode === "duo" && sessionState === "performing" && (
                      <>
                        {/* Full-screen dual organism canvas */}
                        <motion.div
                          className="absolute inset-[3px] rounded-[53px] overflow-hidden z-10"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ duration: 1.5 }}
                        >
                          <DuoOrganismCanvas ref={duoOrganismRef} onGameEvent={handleGameEvent} />
                        </motion.div>

                        {/* Duo session videos — top-left & bottom-right corners */}
                        <motion.div
                          className="absolute inset-0 z-20 pointer-events-none"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ duration: 1.5, delay: 0.5 }}
                        >
                          {/* Top-left video */}
                          <div className="absolute top-[52px] left-3 rounded-xl overflow-hidden shadow-lg pointer-events-auto"
                            style={{ width: "47%", maxWidth: 160, border: "1px solid rgba(255,255,255,0.12)", boxShadow: "0 0 30px rgba(0,0,0,0.6)" }}>
                            <LoopingVideo src="/Duo/Gen-4 Turbo having so much fun hareketli ve heyecanli 2494731309.mp4" className="w-full h-auto block" />
                          </div>
                          {/* Bottom-right video */}
                          <div className="absolute bottom-[72px] right-3 rounded-xl overflow-hidden shadow-lg pointer-events-auto"
                            style={{ width: "47%", maxWidth: 160, border: "1px solid rgba(255,255,255,0.12)", boxShadow: "0 0 30px rgba(0,0,0,0.6)" }}>
                            <LoopingVideo src="/Duo/Gen-4 Turbo having so much fun 1052318284.mp4" className="w-full h-auto block" />
                          </div>
                        </motion.div>

                        {/* Game HUD — top bar (appears after 3s delay) */}
                        {duoStarted && <motion.div
                          className="absolute top-[52px] left-5 right-5 z-30"
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.5 }}
                        >
                          <div className="flex items-center justify-between px-2 py-1 rounded-lg"
                            style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(8px)", border: "1px solid rgba(255,255,255,0.06)" }}>
                            <div className="flex items-center gap-1">
                              <span className="text-[8px] font-mono text-slate-500">⏱</span>
                              <span className="text-[9px] font-mono text-slate-300">{formatSessionTime(sessionTime)}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <span className="text-[8px] font-mono" style={{ color: beliefColors.reward.primary }}>⚡</span>
                              <span className="text-[9px] font-mono font-medium" style={{ color: beliefColors.reward.primary }}>{gameScore}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <span className="text-[8px] font-mono text-orange-400">🔥</span>
                              <span className="text-[9px] font-mono font-medium text-orange-400">x{gameCombo.toFixed(1)}</span>
                            </div>
                          </div>
                        </motion.div>}

                        {/* Active Task Card — bottom-left (after 3s delay) */}
                        {duoStarted && <AnimatePresence>
                          {activeGameTask && (
                            <motion.div
                              key="task"
                              className="absolute bottom-[80px] left-4 z-30"
                              style={{ maxWidth: "55%" }}
                              initial={{ opacity: 0, x: -20, scale: 0.9 }}
                              animate={{ opacity: 1, x: 0, scale: activeGameTask.progress > 0.9 ? [1, 1.02, 1] : 1 }}
                              exit={{ opacity: 0, x: -20, scale: 0.9 }}
                              transition={{ duration: 0.3 }}
                            >
                              <div className="px-2.5 py-2 rounded-xl"
                                style={{ background: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)", border: "1px solid rgba(255,255,255,0.08)" }}>
                                <div className="flex items-center gap-1 mb-1">
                                  <Target size={7} style={{ color: beliefColors.salience.primary }} />
                                  <span className="text-[8px] font-display text-slate-300">{activeGameTask.name}</span>
                                </div>
                                <div className="w-full h-[3px] rounded-full mb-1" style={{ background: "rgba(255,255,255,0.08)" }}>
                                  <motion.div
                                    className="h-full rounded-full"
                                    style={{ background: activeGameTask.progress > 0.9 ? beliefColors.reward.primary : beliefColors.salience.primary }}
                                    animate={{ width: `${activeGameTask.progress * 100}%` }}
                                    transition={{ duration: 0.3 }}
                                  />
                                </div>
                                <div className="flex items-center justify-between">
                                  <span className="text-[7px] font-mono" style={{ color: beliefColors.reward.primary }}>+{activeGameTask.xp} XP</span>
                                  <span className="text-[7px] font-mono text-slate-600">{Math.ceil(activeGameTask.remaining)}s</span>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>}

                        {/* Achievement Toasts (after 3s delay) */}
                        {duoStarted && <div className="absolute top-[90px] left-0 right-0 z-40 flex flex-col items-center gap-1.5 pointer-events-none">
                          <AnimatePresence>
                            {gameToasts.map((toast) => (
                              <motion.div
                                key={toast.id + toast.ts}
                                initial={{ opacity: 0, scale: 0.8, y: 10 }}
                                animate={{ opacity: 1, scale: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                                transition={{ duration: 0.4 }}
                                className="px-3 py-1.5 rounded-xl"
                                style={{
                                  background: "rgba(0,0,0,0.7)",
                                  backdropFilter: "blur(12px)",
                                  border: `1px solid ${beliefColors.reward.primary}30`,
                                  boxShadow: `0 0 20px ${beliefColors.reward.primary}15`,
                                }}
                              >
                                <div className="flex items-center gap-2">
                                  <span className="text-[11px]">{toast.icon}</span>
                                  <div>
                                    <span className="text-[9px] font-display font-medium text-slate-200 block">{toast.name}</span>
                                    <span className="text-[8px] font-mono" style={{ color: beliefColors.reward.primary }}>+{toast.xp} XP</span>
                                  </div>
                                </div>
                              </motion.div>
                            ))}
                          </AnimatePresence>
                        </div>}

                        {/* End Session button — bottom center (after 3s delay) */}
                        {duoStarted && <motion.div
                          className="absolute bottom-[40px] left-0 right-0 z-30 flex justify-center"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 1 }}
                        >
                          <button onClick={handleDuoStop} className="px-4 py-1.5 rounded-full text-[9px] font-display text-slate-400 transition-all hover:text-slate-200"
                            style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(8px)", border: "1px solid rgba(255,255,255,0.08)" }}>
                            <Square size={8} className="inline mr-1 -mt-px" /> {t("live.endSession")}
                          </button>
                        </motion.div>}
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
                        {activeControllers.size > 0 ? t("live.activeCount", { count: activeControllers.size }) : t("live.noControllers")}
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
                  <span className="hud-label text-[9px]">{t("live.emotional")}</span>
                </div>
                <div className="space-y-2">
                  {EMOTIONAL_CONTROLLERS.map(({ id, Icon, color: cColor }) => {
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
                          <div className="text-[11px] font-display" style={{ color: isActive ? "#E2E8F0" : "#64748B" }}>{t(`live.controllers.${id}.label`)}</div>
                          <div className="text-[8px] font-mono text-slate-700">{t(`live.controllers.${id}.description`)}</div>
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
                  <span className="hud-label text-[9px]">{t("live.physical")}</span>
                </div>
                <div className="space-y-2">
                  {PHYSICAL_CONTROLLERS.map(({ id, Icon, color: cColor }) => {
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
                          <div className="text-[11px] font-display" style={{ color: isActive ? "#E2E8F0" : "#64748B" }}>{t(`live.controllers.${id}.label`)}</div>
                          <div className="text-[8px] font-mono text-slate-700">{t(`live.controllers.${id}.description`)}</div>
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

    const tick = (ts: number) => {
      if (!alive) return;
      if (!prev.current) prev.current = ts;
      const dt = (ts - prev.current) / 1000;
      prev.current = ts;
      const t = v.currentTime - dt;
      if (t <= 0) {
        v.currentTime = 0;
        dir.current = 1;
        prev.current = 0;
        v.play().catch(() => {});
        return;
      }
      v.currentTime = t;
      raf.current = requestAnimationFrame(tick);
    };

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