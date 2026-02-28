/* ── M³ Hub — "The Interior" ─ Inside Your Musical Brain ────────────
 *  Single-screen immersive neural landscape.
 *  Organism canvas fills the viewport; glass membrane panels float.
 *  Synaptic particles drift between cortical regions.
 *
 *  Modes: "idle" (genes/learn/observations) ↔ "playing" (playlist/visualizer/observations)
 *
 *  Key emotion: EPIPHANY — moments of realization about who you are.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo, useCallback, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Sparkles, Lock, Zap, Clock, ChevronRight, Music,
} from "lucide-react";
import { useM3Store } from "@/stores/useM3Store";
import { useM3Gate } from "@/hooks/useM3Gate";
import { personas } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MindTypeRing } from "@/components/mind/MindTypeRing";
import { TypeChangeAnimation } from "@/components/mind/TypeChangeAnimation";
import { CongratsAnimation } from "@/components/mind/CongratsAnimation";
import { TrainingPricingOverlay } from "@/components/mind/TrainingPricingOverlay";
import { PersonaLevelTrack } from "@/components/persona/PersonaLevelTrack";
import { C3_FUNCTIONS, M3_STAGES, M3_TIERS } from "@/data/m3-stages";
import { generateObservations, getUnlockedObservationTypes } from "@/data/m3-observations";
import { SpotifySimulator, trackToM3Signal } from "@/services/SpotifySimulator";
import { miDataService } from "@/services/MIDataService";
import { GENE_COLORS, GENE_NAMES, getDominantType, levelToOrganismStage } from "@/types/m3";
import type { M3Tier, PresentationLayer, MindGenes } from "@/types/m3";
import { pageTransition } from "@/design/animations";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import type { MockTrack } from "@/services/SpotifySimulator";
import { useM3AudioStore } from "@/stores/useM3AudioStore";
import { AudioPlayer } from "@/services/AudioPlayer";
import { AudioAnalyzer } from "@/services/AudioAnalyzer";
import { generateWeeklyPlaylist } from "@/hooks/usePlaylistGenerator";
import { LIBRARY_TRACKS } from "@/data/track-library";
import { M3Playlist } from "@/components/m3hub/M3Playlist";
import { MindVisualizer } from "@/components/m3hub/MindVisualizer";

const LAYERS: PresentationLayer[] = ["surface", "narrative", "deep"];
const ease = [0.22, 1, 0.36, 1] as const;

export function M3Hub() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const m3Mind = useM3Store((s) => s.mind);
  const learnFromListening = useM3Store((s) => s.learnFromListening);
  const setTier = useM3Store((s) => s.setTier);
  const preferredLayer = useM3Store((s) => s.preferredLayer);
  const setPreferredLayer = useM3Store((s) => s.setPreferredLayer);
  const gate = useM3Gate();

  const [activeLayer, setActiveLayer] = useState<PresentationLayer>(preferredLayer);
  const [learning, setLearning] = useState(false);
  const [learnResult, setLearnResult] = useState<string | null>(null);
  const [showPricing, setShowPricing] = useState(false);
  const [showCongrats, setShowCongrats] = useState(false);
  const [congratsTier, setCongratsTier] = useState<"basic" | "premium" | "ultimate" | null>(null);
  const [showTypeChange, setShowTypeChange] = useState(false);
  const [typeChangeName, setTypeChangeName] = useState("");
  const [typeChangeColor, setTypeChangeColor] = useState("#A855F7");

  // Neural Memory Stream
  const [neuralMemories, setNeuralMemories] = useState<MockTrack[]>([]);
  useEffect(() => {
    setNeuralMemories(SpotifySimulator.getRecentHistory());
  }, []);

  // ── Audio Engine ──────────────────────────────────────────────────
  const audioMode = useM3AudioStore((s) => s.mode);
  const audioIsPlaying = useM3AudioStore((s) => s.isPlaying);
  const audioTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const audioPlaylist = useM3AudioStore((s) => s.playlist);
  const playerRef = useRef<AudioPlayer | null>(null);
  const analyzerRef = useRef<AudioAnalyzer | null>(null);
  const rafRef = useRef<number>(0);

  // Initialize AudioPlayer lazily
  const getPlayer = useCallback(() => {
    if (!playerRef.current) {
      playerRef.current = new AudioPlayer();
    }
    return playerRef.current;
  }, []);

  // Play track when index changes or playback starts
  useEffect(() => {
    if (audioMode !== "playing" || audioPlaylist.length === 0) return;
    const track = audioPlaylist[audioTrackIdx];
    if (!track) return;

    const player = getPlayer();

    if (audioIsPlaying) {
      player.play(track.audioFile).then(() => {
        // Create analyzer from the player's AnalyserNode
        const node = player.getAnalyser();
        if (node && !analyzerRef.current) {
          analyzerRef.current = new AudioAnalyzer(node);
        }
        // Set track profiles for C³ blending
        analyzerRef.current?.setTrackProfile(track.r3Profile, track.c3Profile);

        useM3AudioStore.getState().setDuration(track.durationSec);
      });
    } else {
      player.pause();
    }
  }, [audioMode, audioTrackIdx, audioIsPlaying, audioPlaylist, getPlayer]);

  // 60fps analysis loop — feed vizParams to store
  useEffect(() => {
    if (audioMode !== "playing") return;
    let running = true;
    const tick = () => {
      if (!running) return;
      const player = playerRef.current;
      const analyzer = analyzerRef.current;
      if (player && analyzer && !player.isPaused()) {
        const params = analyzer.getParameters();
        useM3AudioStore.getState().setVizParams(params);
        useM3AudioStore.getState().setCurrentTime(player.getCurrentTime());
      }
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => { running = false; cancelAnimationFrame(rafRef.current); };
  }, [audioMode]);

  // Auto-advance to next track on end
  useEffect(() => {
    const player = playerRef.current;
    if (!player || audioMode !== "playing") return;
    return player.onEnded(() => {
      useM3AudioStore.getState().skipTrack();
    });
  }, [audioMode, audioTrackIdx]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      playerRef.current?.dispose();
      playerRef.current = null;
      analyzerRef.current = null;
      cancelAnimationFrame(rafRef.current);
      useM3AudioStore.getState().cleanup();
    };
  }, []);

  // Stop handler — return to idle
  const handleStopPlayback = useCallback(() => {
    playerRef.current?.stop();
    analyzerRef.current?.reset();
    useM3AudioStore.getState().stopPlayback();
  }, []);

  // Identity
  const identity = useActiveIdentity();
  const accentColor = identity.color;
  const morphology = identity.morphology;
  const activePersona = m3Mind ? personas.find(p => p.id === m3Mind.activePersonaId) : null;
  const organismStage = m3Mind ? levelToOrganismStage(m3Mind.level) : 1;
  const stageDef = m3Mind ? M3_STAGES[m3Mind.stage] : null;
  const stageColor = stageDef?.color ?? "#94A3B8";
  const tierDef = m3Mind ? M3_TIERS[m3Mind.tier] : null;
  const mindType = m3Mind ? getDominantType(m3Mind.genes) : "Alchemists";

  // Observations
  const observations = useMemo(() => {
    if (!m3Mind) return [];
    return generateObservations(m3Mind, activeLayer, t);
  }, [m3Mind, activeLayer, t]);

  const unlockedTypes = useMemo(() => {
    if (!m3Mind) return [];
    return getUnlockedObservationTypes(m3Mind.level);
  }, [m3Mind]);

  // Learn
  const handleLearn = useCallback(() => {
    if (!m3Mind || m3Mind.frozen || learning) return;
    setLearning(true);
    setLearnResult(null);

    const oldType = getDominantType(m3Mind.genes);
    const session = SpotifySimulator.getListeningSession();

    setTimeout(() => {
      for (const entry of session) {
        const signal = trackToM3Signal(entry.track, {
          wasSkipped: entry.wasSkipped,
          isRepeat: false,
        });
        // Pass real genes from MI dataset when available
        const catalogTrack = miDataService.findTrack(entry.track.id);
        const realGenes: MindGenes | undefined = catalogTrack
          ? catalogTrack.genes as MindGenes
          : undefined;
        learnFromListening(signal, realGenes);
      }

      const currentMind = useM3Store.getState().mind;
      if (currentMind) {
        const newType = getDominantType(currentMind.genes);
        if (oldType !== newType) {
          const geneKey = GENE_NAMES.find(g => currentMind.genes[g] === Math.max(...GENE_NAMES.map(g2 => currentMind.genes[g2])));
          setTypeChangeName(newType);
          setTypeChangeColor(geneKey ? GENE_COLORS[geneKey] : accentColor);
          setShowTypeChange(true);
        }
      }

      setNeuralMemories(SpotifySimulator.getRecentHistory());
      setLearning(false);
      setLearnResult(t("m3.hub.learnSuccess", { count: session.length }));

      // Generate personalized playlist from updated genes and switch to playing mode
      const updatedMind = useM3Store.getState().mind;
      if (updatedMind && !updatedMind.frozen) {
        const playlist = generateWeeklyPlaylist(LIBRARY_TRACKS, updatedMind.genes, 12);
        const audioStore = useM3AudioStore.getState();
        audioStore.setPlaylist(playlist);
        audioStore.setMode("playing");
        audioStore.setIsPlaying(true);
      }

      setTimeout(() => setLearnResult(null), 4000);
    }, 1500);
  }, [m3Mind, learning, learnFromListening, t, accentColor]);

  const handleTierSelect = useCallback((tier: M3Tier) => {
    setTier(tier);
    setCongratsTier(tier === "free" ? "basic" : tier);
    setShowCongrats(true);
  }, [setTier]);

  const handleLayerChange = useCallback((layer: PresentationLayer) => {
    if (!gate.canSeeLayer(layer)) return;
    setActiveLayer(layer);
    setPreferredLayer(layer);
  }, [gate, setPreferredLayer]);

  // ── Empty state ──────────────────────────────────────────────────
  if (!m3Mind) {
    return (
      <motion.div {...pageTransition} className="relative h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Brain size={48} className="mx-auto mb-4 text-slate-700" />
          <h2 className="text-xl font-display font-bold text-slate-400 mb-2">{t("m3.hub.title")}</h2>
          <p className="text-sm text-slate-600 font-display font-light">{t("m3.frozen.description")}</p>
        </div>
      </motion.div>
    );
  }

  const dominantGene = GENE_NAMES.reduce((a, b) => m3Mind.genes[a] > m3Mind.genes[b] ? a : b);

  const familyToGeneColor = (fam: string) =>
    GENE_COLORS[
      fam === "Alchemists" ? "tension" :
      fam === "Architects" ? "resolution" :
      fam === "Explorers" ? "entropy" :
      fam === "Anchors" ? "resonance" : "plasticity"
    ];

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden bg-black">

      {/* ── Living organism background ──────────────────────────── */}
      <div className="absolute inset-0 z-0" style={{ transform: "scale(1.5)", transformOrigin: "center 40%" }}>
        <MindOrganismCanvas
          color={accentColor}
          stage={organismStage}
          intensity={0.35 + m3Mind.stageProgress * 0.25}
          breathRate={6 - m3Mind.stageProgress * 2}
          familyMorphology={morphology}
          className="w-full h-full"
          variant="hero"
          interactive
        />
      </div>

      {/* Depth vignette — radial fade to black */}
      <div
        className="absolute inset-0 z-[1] pointer-events-none"
        style={{
          background: "radial-gradient(ellipse 65% 50% at 50% 40%, transparent 0%, rgba(0,0,0,0.5) 35%, rgba(0,0,0,0.92) 100%)",
        }}
      />
      <div className="cinematic-vignette absolute inset-0 z-[2] pointer-events-none" />

      {/* ── Synaptic particles — ambient neural activity ────────── */}
      {Array.from({ length: 10 }).map((_, i) => (
        <motion.div
          key={`syn-${i}`}
          className="absolute rounded-full pointer-events-none z-[3]"
          style={{
            width: 1.5 + (i % 3),
            height: 1.5 + (i % 3),
            background: `radial-gradient(circle, ${accentColor}60, transparent)`,
            left: `${8 + i * 9}%`,
            top: `${12 + (i % 5) * 18}%`,
          }}
          animate={{
            y: [0, -18 - i * 2, 0],
            x: [0, 6 - i * 1.5, 0],
            opacity: [0.08, 0.45, 0.08],
            scale: [1, 1.5, 1],
          }}
          transition={{
            duration: 7 + i * 1.4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: i * 0.6,
          }}
        />
      ))}

      {/* ── Frozen Overlay ──────────────────────────────────────── */}
      <AnimatePresence>
        {m3Mind.frozen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          >
            <div className="text-center max-w-sm px-6">
              <Lock size={40} className="mx-auto mb-4 text-slate-500" />
              <h2 className="text-xl font-display font-bold text-slate-300 mb-2">{t("m3.frozen.title")}</h2>
              <p className="text-sm text-slate-500 font-display font-light mb-6">{t("m3.frozen.description")}</p>
              <button
                onClick={() => setShowPricing(true)}
                className="px-6 py-3 rounded-xl text-sm font-display font-semibold transition-all duration-500"
                style={{
                  background: `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                  color: "#000",
                  border: `1px solid ${accentColor}60`,
                  boxShadow: `0 0 30px ${accentColor}25`,
                }}
              >
                {t("m3.frozen.cta")}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ SINGLE-SCREEN NEURAL LANDSCAPE ═══════════════════════ */}
      <div className="relative z-10 h-full flex flex-col pb-20">

        {/* ── MEMBRANE: Identity Header ─────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: -30, filter: "blur(16px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 1.2, ease }}
          className="flex-shrink-0 mx-4 mt-4 px-5 py-4 rounded-2xl backdrop-blur-xl"
          style={{
            background: "linear-gradient(135deg, rgba(0,0,0,0.4), rgba(0,0,0,0.2))",
            border: "1px solid rgba(255,255,255,0.06)",
            boxShadow: `0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04), inset 0 0 30px ${accentColor}04`,
          }}
        >
          <div className="flex items-center gap-4">
            {/* Breathing MindTypeRing */}
            <motion.div
              animate={{ scale: [1, 1.04, 1] }}
              transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
            >
              <MindTypeRing genes={m3Mind.genes} size={56} />
            </motion.div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-0.5">
                <NucleusDot color={accentColor} size={4} active pulsing />
                <span className="text-[9px] font-display font-light tracking-[0.2em] uppercase text-slate-500">
                  {mindType} · L{m3Mind.level}/12
                </span>
              </div>
              <h1
                className="text-xl md:text-2xl font-display font-bold tracking-tight truncate"
                style={{ color: accentColor }}
              >
                {activePersona ? t(`personas.${activePersona.id}.name`) : t("m3.hub.title")}
              </h1>
              {activePersona && (
                <p className="text-[10px] text-slate-600 font-display font-light italic truncate mt-0.5">
                  {t(`personas.${activePersona.id}.tagline`)}
                </p>
              )}
            </div>

            {/* Stage orb — breathing glow */}
            <div className="flex-shrink-0 text-center relative">
              <motion.div
                className="absolute rounded-full pointer-events-none"
                style={{ inset: "-10px" }}
                animate={{
                  boxShadow: [
                    `0 0 0px ${stageColor}00`,
                    `0 0 25px ${stageColor}18`,
                    `0 0 0px ${stageColor}00`,
                  ],
                }}
                transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
              />
              <span className="text-2xl block">{stageDef?.icon}</span>
              <span
                className="text-[8px] font-display tracking-[0.1em] uppercase block mt-0.5"
                style={{ color: stageColor }}
              >
                {t(`m3.stage.${m3Mind.stage}`)}
              </span>
              <span className="text-[8px] font-mono text-slate-600">
                {Math.round(m3Mind.stageProgress * 100)}%
              </span>
            </div>
          </div>

          {/* Level track */}
          <div className="mt-3 max-w-[280px]">
            <PersonaLevelTrack currentLevel={m3Mind.level} color={accentColor} />
          </div>
        </motion.div>

        {/* ── CORTEX: Three-Column Neural Landscape ─────────────── */}
        <div className="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-12 gap-3 px-4 mt-3 overflow-y-auto md:overflow-hidden" style={{ scrollbarWidth: "none" }}>

          {/* ── LEFT HEMISPHERE: Mode-Switched ──── */}
          <div className="md:col-span-3 order-2 md:order-1 flex flex-col h-full min-h-0">
            <AnimatePresence mode="wait">
              {audioMode === "playing" ? (
                /* ── PLAYING: Playlist Panel ──── */
                <M3Playlist
                  key="playlist"
                  accentColor={accentColor}
                  onStop={handleStopPlayback}
                />
              ) : (
                /* ── IDLE: Gene Strands + Neural Memory ──── */
                <motion.div
                  key="idle-left"
                  initial={{ opacity: 0, x: -50, filter: "blur(12px)" }}
                  animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
                  exit={{ opacity: 0, x: -30, filter: "blur(12px)" }}
                  transition={{ duration: 0.6, ease }}
                  className="flex flex-col gap-3 overflow-y-auto h-full"
                  style={{ scrollbarWidth: "none" }}
                >
                  {/* Gene Strands — neural DNA panel */}
                  <div
                    className="rounded-2xl p-4 backdrop-blur-xl"
                    style={{
                      background: "linear-gradient(160deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15))",
                      border: "1px solid rgba(255,255,255,0.05)",
                      boxShadow: "inset 0 1px 0 rgba(255,255,255,0.03), 0 4px 20px rgba(0,0,0,0.3)",
                    }}
                  >
                    <span className="text-[9px] font-display font-light tracking-[0.3em] uppercase text-slate-600 block mb-3">
                      {t("m3.hub.geneProfile")}
                    </span>
                    <div className="space-y-3">
                      {GENE_NAMES.map((gene, i) => {
                        const value = m3Mind.genes[gene];
                        const pct = Math.round(value * 100);
                        const color = GENE_COLORS[gene];
                        const isDominant = gene === dominantGene;
                        return (
                          <motion.div
                            key={gene}
                            initial={{ opacity: 0, x: -25 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, delay: 0.5 + i * 0.08, ease }}
                          >
                            <div className="flex items-center justify-between mb-1">
                              <div className="flex items-center gap-1.5">
                                <motion.div
                                  className="w-1.5 h-1.5 rounded-full"
                                  style={{
                                    background: color,
                                    boxShadow: isDominant ? `0 0 10px ${color}80` : "none",
                                  }}
                                  animate={isDominant ? {
                                    scale: [1, 1.6, 1],
                                    boxShadow: [`0 0 4px ${color}40`, `0 0 14px ${color}90`, `0 0 4px ${color}40`],
                                  } : {}}
                                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                                />
                                <span
                                  className="text-[10px] font-display font-medium tracking-wide"
                                  style={{ color: isDominant ? color : "#64748B" }}
                                >
                                  {t(`m3.gene.${gene}`)}
                                </span>
                              </div>
                              <span className="text-[10px] font-mono tabular-nums" style={{ color: `${color}90` }}>
                                {pct}%
                              </span>
                            </div>
                            <div
                              className="relative h-[5px] rounded-full overflow-hidden"
                              style={{ background: "rgba(255,255,255,0.03)" }}
                            >
                              <motion.div
                                className="absolute inset-y-0 left-0 rounded-full"
                                style={{
                                  background: isDominant
                                    ? `linear-gradient(90deg, ${color}50, ${color})`
                                    : `${color}35`,
                                  boxShadow: isDominant
                                    ? `0 0 20px ${color}50, 0 0 40px ${color}20`
                                    : "none",
                                }}
                                initial={{ width: 0 }}
                                animate={{ width: `${pct}%` }}
                                transition={{ duration: 1.4, ease, delay: 0.5 + i * 0.08 }}
                              />
                              {isDominant && (
                                <motion.div
                                  className="absolute inset-y-0 w-10 rounded-full"
                                  style={{
                                    background: `linear-gradient(90deg, transparent, ${color}35, transparent)`,
                                  }}
                                  animate={{ x: ["-40px", `${pct * 3}px`] }}
                                  transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", repeatDelay: 1 }}
                                />
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Neural Memory — absorbed track fragments */}
                  <div
                    className="rounded-2xl p-3 backdrop-blur-xl"
                    style={{
                      background: "linear-gradient(160deg, rgba(0,0,0,0.3), rgba(0,0,0,0.12))",
                      border: "1px solid rgba(255,255,255,0.04)",
                      boxShadow: "inset 0 1px 0 rgba(255,255,255,0.02)",
                    }}
                  >
                    <span className="text-[9px] font-display font-light tracking-[0.3em] uppercase text-slate-600 block mb-2">
                      {t("m3.hub.neuralStream")}
                    </span>
                    {neuralMemories.length > 0 ? (
                      <div className="flex gap-2 overflow-x-auto pb-1" style={{ scrollbarWidth: "none" }}>
                        {neuralMemories.slice(0, 5).map((track, i) => {
                          const trackColor = familyToGeneColor(track.dominantFamily);
                          return (
                            <motion.div
                              key={`${track.id}-${i}`}
                              initial={{ opacity: 0, scale: 0.5, filter: "blur(4px)" }}
                              animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
                              transition={{ delay: 1 + i * 0.1, duration: 0.6, ease }}
                              className="flex-shrink-0 w-16 group"
                            >
                              <div
                                className="relative h-16 w-16 rounded-xl overflow-hidden mb-1 transition-all duration-700 group-hover:scale-110"
                                style={{
                                  background: `radial-gradient(circle at 50% 35%, ${trackColor}22, rgba(0,0,0,0.85))`,
                                  border: `1px solid ${trackColor}15`,
                                  boxShadow: `inset 0 0 15px ${trackColor}08, 0 0 12px ${trackColor}06`,
                                }}
                              >
                                <motion.div
                                  className="absolute inset-0 rounded-xl"
                                  animate={{
                                    boxShadow: [
                                      `inset 0 0 6px ${trackColor}05`,
                                      `inset 0 0 18px ${trackColor}15`,
                                      `inset 0 0 6px ${trackColor}05`,
                                    ],
                                  }}
                                  transition={{ duration: 3 + i * 0.4, repeat: Infinity, ease: "easeInOut" }}
                                />
                                <div className="absolute inset-0 flex items-center justify-center">
                                  <Music size={12} style={{ color: `${trackColor}45` }} />
                                </div>
                              </div>
                              <p className="text-[8px] text-slate-400 font-display truncate">{track.name}</p>
                            </motion.div>
                          );
                        })}
                      </div>
                    ) : (
                      <p className="text-[9px] text-slate-600 font-display font-light italic">
                        {t("m3.hub.feedYourMind")}
                      </p>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* ── CENTER: Learn Button always visible, Visualizer behind when playing ──── */}
          <div className="md:col-span-6 order-1 md:order-2 flex flex-col items-center justify-center relative h-full min-h-0">
            {/* MindVisualizer renders behind when playing */}
            <AnimatePresence>
              {audioMode === "playing" && (
                <motion.div
                  key="visualizer-bg"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.8, ease }}
                  className="absolute inset-0 z-0"
                >
                  <MindVisualizer accentColor={accentColor} />
                </motion.div>
              )}
            </AnimatePresence>

            {/* Neural Nexus — Learn Button (always visible) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.6, filter: "blur(20px)" }}
              animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
              transition={{ duration: 0.6, ease }}
              className="flex flex-col items-center justify-center relative w-full h-full z-10"
            >
              {/* Concentric neural rings — only when idle */}
              {audioMode !== "playing" && [90, 140, 200, 270].map((size, i) => (
                <motion.div
                  key={`ring-${i}`}
                  className="absolute rounded-full pointer-events-none top-1/2 left-1/2"
                  style={{
                    width: size,
                    height: size,
                    marginTop: -size / 2,
                    marginLeft: -size / 2,
                    border: `1px solid ${accentColor}${(8 - i * 2).toString(16).padStart(2, "0")}`,
                  }}
                  animate={{
                    scale: [1, 1.04 - i * 0.005, 1],
                    opacity: [0.2 + i * 0.05, 0.6 - i * 0.08, 0.2 + i * 0.05],
                  }}
                  transition={{
                    duration: 5 + i * 1.8,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: i * 0.5,
                  }}
                />
              ))}

              {/* Ambient radial glow — only when idle */}
              {audioMode !== "playing" && (
                <motion.div
                  className="absolute w-48 h-48 rounded-full pointer-events-none top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                  style={{
                    background: `radial-gradient(circle, ${accentColor}0A, transparent 70%)`,
                  }}
                  animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.3, 0.6, 0.3],
                  }}
                  transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
                />
              )}

              {/* Learn Button — the beating heart of the mind */}
              <motion.div
                className="relative z-10"
                animate={learning ? {} : { scale: [1, 1.025, 1] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
              >
                {/* Glow aura */}
                {!m3Mind.frozen && !learning && (
                  <motion.div
                    className="absolute rounded-full pointer-events-none"
                    style={{
                      inset: "-28px",
                      background: `radial-gradient(circle, ${accentColor}0C, transparent 65%)`,
                    }}
                    animate={{
                      scale: [1, 1.25, 1],
                      opacity: [0.3, 0.7, 0.3],
                    }}
                    transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut" }}
                  />
                )}

                <button
                  onClick={m3Mind.frozen ? () => setShowPricing(true) : handleLearn}
                  disabled={learning}
                  className="relative px-10 py-4 rounded-full text-sm font-display font-semibold transition-all duration-500"
                  style={{
                    background: m3Mind.frozen
                      ? "rgba(255,255,255,0.03)"
                      : learning
                        ? `${accentColor}10`
                        : `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                    color: m3Mind.frozen ? "#475569" : learning ? accentColor : "#000",
                    border: `1px solid ${m3Mind.frozen ? "rgba(255,255,255,0.05)" : `${accentColor}60`}`,
                    boxShadow: !m3Mind.frozen && !learning
                      ? `0 0 50px ${accentColor}30, 0 0 100px ${accentColor}10, inset 0 1px 0 rgba(255,255,255,0.2)`
                      : "none",
                    cursor: learning ? "wait" : "pointer",
                  }}
                >
                  {learning ? (
                    <span className="flex items-center gap-2">
                      <motion.span
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      >
                        <Zap size={14} />
                      </motion.span>
                      {t("m3.hub.learnButton")}...
                    </span>
                  ) : m3Mind.frozen ? (
                    <span className="flex items-center gap-2">
                      <Lock size={14} />
                      {t("m3.hub.learnFrozen")}
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      <Brain size={14} />
                      {t("m3.hub.learnButton")}
                    </span>
                  )}
                </button>
              </motion.div>

              {/* Epiphany result */}
              <AnimatePresence>
                {learnResult && (
                  <motion.p
                    initial={{ opacity: 0, y: 12, scale: 0.9 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.9 }}
                    transition={{ duration: 0.5, ease }}
                    className="text-xs font-display font-light mt-5"
                    style={{ color: accentColor }}
                  >
                    {learnResult}
                  </motion.p>
                )}
              </AnimatePresence>

              {/* Vital Signs — breathing numbers */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.1, duration: 0.8 }}
                className="flex items-center gap-10 mt-6"
              >
                {[
                  { value: m3Mind.totalListens, label: t("m3.hub.listens") },
                  { value: m3Mind.totalMinutes, label: t("m3.hub.minutes") },
                  { value: m3Mind.previousPersonaIds.length, label: t("m3.hub.shifts") },
                ].map((stat, i) => (
                  <div key={i} className="text-center">
                    <motion.span
                      className="text-lg font-mono text-slate-300 block tabular-nums"
                      animate={{ opacity: [0.65, 1, 0.65] }}
                      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: i * 0.6 }}
                    >
                      {stat.value}
                    </motion.span>
                    <span className="text-[7px] font-display text-slate-600 tracking-[0.2em] uppercase">
                      {stat.label}
                    </span>
                  </div>
                ))}
              </motion.div>
            </motion.div>
          </div>

          {/* ── RIGHT HEMISPHERE: Consciousness + Cortex Map ────── */}
          <motion.div
            initial={{ opacity: 0, x: 50, filter: "blur(12px)" }}
            animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            transition={{ duration: 1, delay: 0.4, ease }}
            className="md:col-span-3 order-3 flex flex-col gap-3 overflow-y-auto"
            style={{ scrollbarWidth: "none" }}
          >
            {/* Consciousness Chamber — Observations */}
            <div
              className="rounded-2xl p-4 backdrop-blur-xl"
              style={{
                background: "linear-gradient(160deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15))",
                border: "1px solid rgba(255,255,255,0.05)",
                boxShadow: `inset 0 1px 0 rgba(255,255,255,0.03), 0 4px 20px rgba(0,0,0,0.3), 0 0 25px ${accentColor}03`,
              }}
            >
              <div className="flex items-center gap-2 mb-2">
                <motion.div
                  animate={{ rotate: [0, 12, -12, 0], scale: [1, 1.15, 1] }}
                  transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
                >
                  <Sparkles size={11} style={{ color: accentColor }} />
                </motion.div>
                <span
                  className="text-[11px] font-display font-light tracking-[0.15em] uppercase"
                  style={{ color: `${accentColor}80` }}
                >
                  {t("m3.hub.currentObservation")}
                </span>
                <span className="text-[9px] font-mono text-slate-700 ml-auto">
                  {unlockedTypes.length}/{9}
                </span>
              </div>

              {/* Layer Toggle — glass pills */}
              <div
                className="flex items-center gap-0.5 p-0.5 rounded-full mb-3 w-fit"
                style={{
                  background: "rgba(255,255,255,0.02)",
                  border: "1px solid rgba(255,255,255,0.04)",
                }}
              >
                {LAYERS.map((layer) => {
                  const isActive = activeLayer === layer;
                  const canSee = gate.canSeeLayer(layer);
                  return (
                    <button
                      key={layer}
                      onClick={() => handleLayerChange(layer)}
                      disabled={!canSee}
                      className="relative px-3 py-1 rounded-full text-[8px] font-display transition-all duration-300"
                      style={{
                        background: isActive ? `${accentColor}15` : "transparent",
                        color: isActive ? accentColor : canSee ? "#64748B" : "#1E293B",
                        border: isActive ? `1px solid ${accentColor}25` : "1px solid transparent",
                        boxShadow: isActive ? `0 0 12px ${accentColor}10` : "none",
                        cursor: canSee ? "pointer" : "not-allowed",
                      }}
                    >
                      {t(`m3.layer.${layer}`)}
                      {!canSee && <Lock size={6} className="inline ml-0.5" />}
                    </button>
                  );
                })}
              </div>

              {/* Observations — thoughts emerging */}
              <div className="space-y-2.5">
                {observations.length > 0 ? observations.slice(0, 4).map((obs, i) => (
                  <motion.div
                    key={obs.id}
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.7 + i * 0.1, duration: 0.5, ease }}
                    className="relative pl-3"
                  >
                    <motion.div
                      className="absolute left-0 top-0 bottom-0 w-[2px] rounded-full"
                      style={{
                        background: `linear-gradient(180deg, ${accentColor}${Math.round(obs.intensity * 99).toString(16).padStart(2, "0")}, transparent)`,
                      }}
                      animate={{ opacity: [0.4, 1, 0.4] }}
                      transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: i * 0.5 }}
                    />
                    <p className="text-[13px] text-slate-400 font-body font-light leading-relaxed">
                      {obs.text}
                    </p>
                  </motion.div>
                )) : (
                  <p className="text-[12px] text-slate-600 font-body font-light italic">
                    {t("m3.hub.noObservations")}
                  </p>
                )}
              </div>
            </div>

            {/* Cortex Map — 9 Functions */}
            <div
              className="rounded-2xl p-3 backdrop-blur-xl"
              style={{
                background: "linear-gradient(160deg, rgba(0,0,0,0.3), rgba(0,0,0,0.12))",
                border: "1px solid rgba(255,255,255,0.04)",
                boxShadow: "inset 0 1px 0 rgba(255,255,255,0.02)",
              }}
            >
              <span className="text-[9px] font-display font-light tracking-[0.3em] uppercase text-slate-600 block mb-2">
                {t("m3.hub.activeFunctions")}
              </span>
              <div className="grid grid-cols-3 gap-1.5">
                {C3_FUNCTIONS.map((fn, i) => {
                  const isActive = m3Mind.activeFunctions.includes(fn.id);
                  return (
                    <motion.div
                      key={fn.id}
                      initial={{ opacity: 0, scale: 0.3, filter: "blur(4px)" }}
                      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
                      transition={{ delay: 0.9 + i * 0.05, duration: 0.5, ease }}
                      className="relative flex flex-col items-center gap-0.5 py-2 rounded-xl transition-all duration-500"
                      style={{
                        background: isActive ? `${fn.color}08` : "rgba(255,255,255,0.01)",
                        border: `1px solid ${isActive ? `${fn.color}20` : "rgba(255,255,255,0.02)"}`,
                        opacity: isActive ? 1 : 0.15,
                      }}
                    >
                      {isActive && (
                        <motion.div
                          className="absolute inset-0 rounded-xl"
                          animate={{
                            boxShadow: [
                              `0 0 0px ${fn.color}00`,
                              `0 0 18px ${fn.color}12`,
                              `0 0 0px ${fn.color}00`,
                            ],
                          }}
                          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: i * 0.25 }}
                        />
                      )}
                      <span
                        className="text-[9px] font-mono font-bold"
                        style={{ color: isActive ? fn.color : "#334155" }}
                      >
                        {fn.abbr}
                      </span>
                      <span className="text-[6px] font-display text-slate-500 text-center leading-tight px-0.5">
                        {fn.name}
                      </span>
                      {isActive && (
                        <div className="absolute -top-0.5 -right-0.5">
                          <NucleusDot color={fn.color} size={2} active pulsing />
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </motion.div>
        </div>

        {/* ── SUBSTRATE: Bottom Membrane ─────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 20, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ delay: 1.1, duration: 0.7, ease }}
          className="flex-shrink-0 mx-4 mb-1 px-5 py-2.5 rounded-2xl backdrop-blur-xl flex items-center gap-3"
          style={{
            background: "linear-gradient(135deg, rgba(0,0,0,0.35), rgba(0,0,0,0.18))",
            border: "1px solid rgba(255,255,255,0.05)",
            boxShadow: "inset 0 1px 0 rgba(255,255,255,0.03), 0 -4px 20px rgba(0,0,0,0.2)",
          }}
        >
          {/* Tier badge */}
          <div
            className="px-3 py-1 rounded-full text-[9px] font-display font-medium"
            style={{
              background: `${tierDef?.color}12`,
              color: tierDef?.color,
              border: `1px solid ${tierDef?.color}20`,
              boxShadow: `0 0 10px ${tierDef?.color}08`,
            }}
          >
            {t(`m3.tier.${m3Mind.tier}.name`)}
          </div>

          {/* Upgrade */}
          {gate.needsUpgrade && (
            <button
              onClick={() => setShowPricing(true)}
              className="px-4 py-1 rounded-full text-[9px] font-display font-medium transition-all duration-500 hover:scale-105"
              style={{
                background: `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                color: "#000",
                border: `1px solid ${accentColor}40`,
                boxShadow: `0 0 20px ${accentColor}15`,
              }}
            >
              {t("m3.hub.upgradeCta")} <ChevronRight size={9} className="inline" />
            </button>
          )}

          <div className="flex-1" />

          {/* Persona link */}
          {activePersona && (
            <button
              onClick={() => navigate(`/info/${activePersona.id}`)}
              className="group flex items-center gap-1 text-[9px] font-display text-slate-600 hover:text-slate-400 transition-colors"
            >
              <span className="border-b border-slate-800 group-hover:border-slate-600 pb-0.5 tracking-wide">
                {t("dashboard.viewPersona")}
              </span>
              <ChevronRight size={9} className="group-hover:translate-x-0.5 transition-transform" />
            </button>
          )}

          {/* Last updated */}
          {m3Mind.lastUpdated && (
            <div className="flex items-center gap-1">
              <Clock size={8} className="text-slate-700" />
              <span className="text-[8px] font-mono text-slate-700">
                {new Date(m3Mind.lastUpdated).toLocaleDateString()}
              </span>
            </div>
          )}
        </motion.div>
      </div>

      {/* ── Overlays ───────────────────────────────────────────── */}
      <TrainingPricingOverlay
        isOpen={showPricing}
        onClose={() => setShowPricing(false)}
        onSelect={handleTierSelect}
        accentColor={accentColor}
      />
      <CongratsAnimation
        tier={congratsTier}
        accentColor={accentColor}
        isVisible={showCongrats}
        onDismiss={() => setShowCongrats(false)}
      />
      <TypeChangeAnimation
        isVisible={showTypeChange}
        typeName={typeChangeName}
        typeColor={typeChangeColor}
        onDismiss={() => setShowTypeChange(false)}
      />
    </motion.div>
  );
}
