/* ── M³ Hub — "The Interior" ─ Inside Your Musical Brain ────────────
 *  A vertical journey through layers of consciousness.
 *  Each scroll takes you deeper: Nucleus → Gene Flow → Neural Memory →
 *  Consciousness → Cortex → Pulse → Substrate.
 *
 *  Key emotion: EPIPHANY — moments of realization about who you are.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo, useCallback, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Sparkles, Lock, Zap, Clock, ChevronRight, ChevronDown, Music,
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
import { GENE_COLORS, GENE_NAMES, getDominantType, levelToOrganismStage } from "@/types/m3";
import type { M3Tier, PresentationLayer } from "@/types/m3";
import { pageTransition } from "@/design/animations";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import type { MockTrack } from "@/services/SpotifySimulator";

const LAYERS: PresentationLayer[] = ["surface", "narrative", "deep"];
const ease = [0.22, 1, 0.36, 1] as const;

export function M3Hub() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const m3Mind = useM3Store((s) => s.mind);
  const milestones = useM3Store((s) => s.milestones);
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

  // Neural Memory Stream — cached recent tracks
  const [neuralMemories, setNeuralMemories] = useState<MockTrack[]>([]);
  useEffect(() => {
    setNeuralMemories(SpotifySimulator.getRecentHistory());
  }, []);

  // Identity from dominant gene (reactive to training)
  const identity = useActiveIdentity();
  const accentColor = identity.color;
  const family = identity.family;
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

  // Learn from listening
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
        learnFromListening(signal);
      }

      // Check for type change
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

      // Refresh neural memories after learning
      setNeuralMemories(SpotifySimulator.getRecentHistory());

      setLearning(false);
      setLearnResult(t("m3.hub.learnSuccess", { count: session.length }));
      setTimeout(() => setLearnResult(null), 4000);
    }, 1500);
  }, [m3Mind, learning, learnFromListening, t, accentColor]);

  // Tier selection from pricing overlay
  const handleTierSelect = useCallback((tier: M3Tier) => {
    setTier(tier);
    setCongratsTier(tier === "free" ? "basic" : tier);
    setShowCongrats(true);
  }, [setTier]);

  // Layer change
  const handleLayerChange = useCallback((layer: PresentationLayer) => {
    if (!gate.canSeeLayer(layer)) return;
    setActiveLayer(layer);
    setPreferredLayer(layer);
  }, [gate, setPreferredLayer]);

  // ── Empty state ──────────────────────────────────────────────────
  if (!m3Mind) {
    return (
      <motion.div {...pageTransition} className="relative h-screen flex items-center justify-center">
        <div className="text-center">
          <Brain size={48} className="mx-auto mb-4 text-slate-700" />
          <h2 className="text-xl font-display font-bold text-slate-400 mb-2">{t("m3.hub.title")}</h2>
          <p className="text-sm text-slate-600 font-display font-light">{t("m3.frozen.description")}</p>
        </div>
      </motion.div>
    );
  }

  // Gene dominance check
  const dominantGene = GENE_NAMES.reduce((a, b) => m3Mind.genes[a] > m3Mind.genes[b] ? a : b);

  // Track family → gene color mapping
  const familyToGeneColor = (fam: string) =>
    GENE_COLORS[
      fam === "Alchemists" ? "tension" :
      fam === "Architects" ? "resolution" :
      fam === "Explorers" ? "entropy" :
      fam === "Anchors" ? "resonance" : "plasticity"
    ];

  return (
    <motion.div {...pageTransition} className="relative min-h-screen bg-black">

      {/* ── Fixed organism background ─────────────────────────────── */}
      <div className="fixed inset-0 z-0" style={{ transform: "scale(1.4)", transformOrigin: "center center" }}>
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
      <div
        className="fixed inset-0 z-[1] pointer-events-none"
        style={{
          background: "radial-gradient(ellipse 70% 55% at 50% 35%, transparent 5%, rgba(0,0,0,0.6) 45%, rgba(0,0,0,0.95) 100%)",
        }}
      />
      <div className="cinematic-vignette fixed inset-0 z-[2] pointer-events-none" />

      {/* ── Frozen Overlay ────────────────────────────────────────── */}
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

      {/* ═══ SCROLLABLE LAYERS — The Interior ══════════════════════ */}
      <div className="relative z-10">

        {/* ── LAYER 0: THE NUCLEUS ─ Hero Identity ─────────────── */}
        <section className="min-h-screen flex flex-col items-center justify-center relative px-6 py-20">

          {/* Mind Type Ring — floating, breathing */}
          <motion.div
            initial={{ opacity: 0, scale: 0.4, filter: "blur(24px)" }}
            animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
            transition={{ duration: 1.8, ease }}
          >
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
            >
              <MindTypeRing genes={m3Mind.genes} size={160} />
            </motion.div>
          </motion.div>

          {/* Identity */}
          <motion.div
            initial={{ opacity: 0, y: 50, filter: "blur(12px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 1.2, delay: 0.4, ease }}
            className="text-center mt-8"
          >
            <div className="flex items-center justify-center gap-2 mb-2">
              <NucleusDot color={accentColor} size={4} active pulsing />
              <span className="text-[10px] font-display font-light tracking-[0.25em] uppercase text-slate-600">
                {mindType} · L{m3Mind.level}/12
              </span>
            </div>

            <h1
              className="text-4xl md:text-5xl lg:text-6xl font-display font-bold tracking-tight"
              style={{ color: accentColor }}
            >
              {activePersona ? t(`personas.${activePersona.id}.name`) : t("m3.hub.title")}
            </h1>

            <p className="text-sm text-slate-500 font-display font-light mt-2 italic max-w-sm mx-auto">
              {activePersona ? t(`personas.${activePersona.id}.tagline`) : ""}
            </p>
          </motion.div>

          {/* Stage + Level Track */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8, ease }}
            className="mt-8 w-full max-w-xs"
          >
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="text-lg" style={{ color: stageColor }}>{stageDef?.icon}</span>
              <span className="text-[10px] font-display font-light tracking-[0.15em] uppercase" style={{ color: stageColor }}>
                {t(`m3.stage.${m3Mind.stage}`)}
              </span>
              <span className="text-[10px] font-mono text-slate-600 ml-2">
                {Math.round(m3Mind.stageProgress * 100)}%
              </span>
            </div>
            <PersonaLevelTrack currentLevel={m3Mind.level} color={accentColor} />
          </motion.div>

          {/* Persona link */}
          {activePersona && (
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.4, duration: 0.8 }}
              onClick={() => navigate(`/info/${activePersona.id}`)}
              className="mt-6 group flex items-center gap-2 text-xs font-display text-slate-600 hover:text-slate-400 transition-colors"
            >
              <span className="border-b border-slate-800 group-hover:border-slate-600 pb-0.5 transition-colors tracking-wide">
                {t("dashboard.viewPersona")}
              </span>
              <ChevronRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
            </motion.button>
          )}

          {/* Scroll hint */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.3 }}
            transition={{ delay: 2.5, duration: 1 }}
            className="absolute bottom-10"
          >
            <motion.div
              animate={{ y: [0, 8, 0] }}
              transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
            >
              <ChevronDown size={20} className="text-slate-600" />
            </motion.div>
          </motion.div>
        </section>

        {/* ── LAYER 1: GENE FLOW ─ Your Neural DNA ────────────── */}
        <section className="py-20 px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.9, ease }}
            className="max-w-xl mx-auto"
          >
            <span className="text-[10px] font-display font-light tracking-[0.25em] uppercase text-slate-600 block mb-8">
              {t("m3.hub.geneProfile")}
            </span>

            <div className="space-y-6">
              {GENE_NAMES.map((gene, i) => {
                const value = m3Mind.genes[gene];
                const pct = Math.round(value * 100);
                const color = GENE_COLORS[gene];
                const isDominant = gene === dominantGene;

                return (
                  <motion.div
                    key={gene}
                    initial={{ opacity: 0, x: -40 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.7, delay: i * 0.08, ease }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span
                        className="text-xs font-display font-medium tracking-wide"
                        style={{ color: isDominant ? color : "#64748B" }}
                      >
                        {t(`m3.gene.${gene}`)}
                      </span>
                      <span
                        className="text-xs font-mono tabular-nums"
                        style={{ color: `${color}90` }}
                      >
                        {pct}%
                      </span>
                    </div>

                    <div
                      className="relative h-[6px] rounded-full overflow-hidden"
                      style={{ background: "rgba(255,255,255,0.04)" }}
                    >
                      {/* Main bar */}
                      <motion.div
                        className="absolute inset-y-0 left-0 rounded-full"
                        style={{
                          background: isDominant
                            ? `linear-gradient(90deg, ${color}80, ${color})`
                            : `${color}50`,
                          boxShadow: isDominant
                            ? `0 0 24px ${color}35, 0 2px 8px ${color}20`
                            : "none",
                        }}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${pct}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1.4, ease, delay: i * 0.08 + 0.2 }}
                      />

                      {/* Breathing shimmer on dominant gene */}
                      {isDominant && (
                        <motion.div
                          className="absolute inset-y-0 w-16 rounded-full"
                          style={{
                            background: `linear-gradient(90deg, transparent, ${color}25, transparent)`,
                          }}
                          animate={{ x: ["-64px", `${pct * 4}px`] }}
                          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", repeatDelay: 1.5 }}
                        />
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        </section>

        {/* ── LAYER 2: NEURAL MEMORY STREAM ─ Absorbed Tracks ─── */}
        <section className="py-16 px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.9, ease }}
            className="max-w-3xl mx-auto"
          >
            <span className="text-[10px] font-display font-light tracking-[0.25em] uppercase text-slate-600 block mb-8">
              {t("m3.hub.neuralStream")}
            </span>

            {neuralMemories.length > 0 ? (
              <div
                className="flex gap-5 overflow-x-auto pb-4"
                style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
              >
                {neuralMemories.map((track, i) => {
                  const trackColor = familyToGeneColor(track.dominantFamily);
                  return (
                    <motion.div
                      key={`${track.id}-${i}`}
                      initial={{ opacity: 0, scale: 0.7, y: 30 }}
                      whileInView={{ opacity: 1, scale: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: i * 0.1, duration: 0.7, ease }}
                      className="flex-shrink-0 w-40 group"
                    >
                      {/* Track orb */}
                      <div
                        className="relative h-40 w-40 rounded-2xl overflow-hidden mb-3 transition-all duration-500 group-hover:scale-[1.04]"
                        style={{
                          background: `radial-gradient(circle at 50% 45%, ${trackColor}18, rgba(0,0,0,0.85))`,
                          border: `1px solid ${trackColor}12`,
                        }}
                      >
                        {/* Neural pulse */}
                        <motion.div
                          className="absolute inset-0 rounded-2xl"
                          animate={{
                            boxShadow: [
                              `inset 0 0 20px ${trackColor}05`,
                              `inset 0 0 40px ${trackColor}12`,
                              `inset 0 0 20px ${trackColor}05`,
                            ],
                          }}
                          transition={{ duration: 3 + i * 0.4, repeat: Infinity, ease: "easeInOut" }}
                        />

                        <div className="absolute inset-0 flex items-center justify-center">
                          <Music size={22} style={{ color: `${trackColor}35` }} />
                        </div>

                        {/* Genre tag */}
                        <div className="absolute bottom-2 left-2">
                          <span
                            className="text-[8px] font-display font-light px-2 py-0.5 rounded-full"
                            style={{ background: `${trackColor}12`, color: `${trackColor}80` }}
                          >
                            {track.genre}
                          </span>
                        </div>
                      </div>

                      <p className="text-[12px] text-slate-300 font-display font-medium truncate">
                        {track.name}
                      </p>
                      <p className="text-[10px] text-slate-600 font-display font-light truncate">
                        {track.artist}
                      </p>
                    </motion.div>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-slate-600 font-display font-light italic text-center py-8">
                {t("m3.hub.feedYourMind")}
              </p>
            )}
          </motion.div>
        </section>

        {/* ── LAYER 3: CONSCIOUSNESS CHAMBER ─ Observations ────── */}
        <section className="py-20 px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.9, ease }}
            className="max-w-lg mx-auto"
          >
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
              <Sparkles size={14} style={{ color: accentColor }} />
              <span
                className="text-[10px] font-display font-light tracking-[0.2em] uppercase"
                style={{ color: `${accentColor}80` }}
              >
                {t("m3.hub.currentObservation")}
              </span>
              <span className="text-[9px] font-mono text-slate-700 ml-auto">
                {unlockedTypes.length}/{9} {t("m3.hub.typesUnlocked")}
              </span>
            </div>

            {/* Layer Toggle */}
            <div
              className="flex items-center gap-1 p-1 rounded-full mb-8 w-fit mx-auto"
              style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.05)" }}
            >
              {LAYERS.map((layer) => {
                const isActive = activeLayer === layer;
                const canSee = gate.canSeeLayer(layer);
                return (
                  <button
                    key={layer}
                    onClick={() => handleLayerChange(layer)}
                    disabled={!canSee}
                    className="relative px-5 py-2 rounded-full text-[11px] font-display transition-all duration-300"
                    style={{
                      background: isActive ? `${accentColor}15` : "transparent",
                      color: isActive ? accentColor : canSee ? "#64748B" : "#1E293B",
                      border: isActive ? `1px solid ${accentColor}20` : "1px solid transparent",
                      cursor: canSee ? "pointer" : "not-allowed",
                    }}
                  >
                    {t(`m3.layer.${layer}`)}
                    {!canSee && <Lock size={8} className="inline ml-1" />}
                  </button>
                );
              })}
            </div>

            {/* Observations — thoughts emerging from the subconscious */}
            <div className="space-y-5">
              {observations.length > 0 ? observations.map((obs, i) => (
                <motion.div
                  key={obs.id}
                  initial={{ opacity: 0, x: -15 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1, duration: 0.6, ease }}
                  className="relative pl-5"
                >
                  {/* Accent line — intensity mapped */}
                  <div
                    className="absolute left-0 top-0.5 bottom-0.5 w-[2px] rounded-full"
                    style={{
                      background: `linear-gradient(180deg, ${accentColor}${Math.round(obs.intensity * 99).toString(16).padStart(2, "0")}, transparent)`,
                    }}
                  />
                  <p className="text-[13px] text-slate-400 font-body font-light leading-relaxed">
                    {obs.text}
                  </p>
                </motion.div>
              )) : (
                <p className="text-[12px] text-slate-600 font-body font-light italic text-center py-4">
                  {t("m3.hub.noObservations")}
                </p>
              )}
            </div>
          </motion.div>
        </section>

        {/* ── LAYER 4: THE CORTEX ─ Functions & Growth ──────────── */}
        <section className="py-20 px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.9, ease }}
            className="max-w-2xl mx-auto"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">

              {/* Functions Constellation */}
              <div>
                <span className="text-[10px] font-display font-light tracking-[0.25em] uppercase text-slate-600 block mb-6">
                  {t("m3.hub.activeFunctions")}
                </span>
                <div className="grid grid-cols-3 gap-3">
                  {C3_FUNCTIONS.map((fn, i) => {
                    const isActive = m3Mind.activeFunctions.includes(fn.id);
                    return (
                      <motion.div
                        key={fn.id}
                        initial={{ opacity: 0, scale: 0.4 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: i * 0.05, duration: 0.5, ease }}
                        className="relative flex flex-col items-center gap-1.5 py-3 rounded-xl transition-all duration-500"
                        style={{
                          background: isActive ? `${fn.color}08` : "rgba(255,255,255,0.01)",
                          border: `1px solid ${isActive ? `${fn.color}18` : "rgba(255,255,255,0.03)"}`,
                          opacity: isActive ? 1 : 0.2,
                        }}
                      >
                        {/* Breathing glow */}
                        {isActive && (
                          <motion.div
                            className="absolute inset-0 rounded-xl"
                            animate={{
                              boxShadow: [
                                `0 0 0px ${fn.color}00`,
                                `0 0 20px ${fn.color}0D`,
                                `0 0 0px ${fn.color}00`,
                              ],
                            }}
                            transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: i * 0.3 }}
                          />
                        )}
                        <span
                          className="text-xs font-mono font-bold"
                          style={{ color: isActive ? fn.color : "#334155" }}
                        >
                          {fn.abbr}
                        </span>
                        <span className="text-[9px] font-display text-slate-500 text-center leading-tight px-1">
                          {fn.name}
                        </span>
                        {isActive && (
                          <div className="absolute -top-1 -right-1">
                            <NucleusDot color={fn.color} size={3} active pulsing />
                          </div>
                        )}
                      </motion.div>
                    );
                  })}
                </div>
              </div>

              {/* Growth Timeline */}
              <div>
                <span className="text-[10px] font-display font-light tracking-[0.25em] uppercase text-slate-600 block mb-6">
                  {t("m3.hub.growthTimeline")}
                </span>
                <div className="space-y-3 max-h-72 overflow-y-auto pr-2" style={{ scrollbarWidth: "thin" }}>
                  {[...milestones].reverse().slice(0, 15).map((ms, i) => {
                    const milestoneColor =
                      ms.type === "birth" ? "#FBBF24" :
                      ms.type === "level_up" ? "#22D3EE" :
                      ms.type === "stage_up" ? "#A855F7" :
                      ms.type === "persona_shift" ? "#EC4899" :
                      ms.type === "function_unlock" ? "#84CC16" :
                      ms.type === "type_change" ? "#EF4444" : "#475569";
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: i * 0.03, duration: 0.4, ease }}
                        className="flex items-start gap-3"
                      >
                        <div className="relative mt-1.5 flex-shrink-0">
                          <div
                            className="w-2 h-2 rounded-full"
                            style={{ background: milestoneColor, boxShadow: `0 0 8px ${milestoneColor}40` }}
                          />
                          {i < Math.min(milestones.length - 1, 14) && (
                            <div
                              className="absolute top-3 left-[3px] w-[1px] h-5"
                              style={{ background: `${milestoneColor}15` }}
                            />
                          )}
                        </div>
                        <div className="flex-1 min-w-0 pb-1">
                          <p className="text-[11px] text-slate-400 font-display leading-tight">
                            {ms.detail}
                          </p>
                          <p className="text-[9px] font-mono text-slate-700 mt-0.5">
                            {new Date(ms.timestamp).toLocaleDateString()}
                          </p>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* ── LAYER 5: THE PULSE ─ Learn & Transformation ──────── */}
        <section className="py-28 px-6 flex flex-col items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, margin: "-50px" }}
            transition={{ duration: 1, ease }}
            className="text-center"
          >
            {/* Learn Button — the breathing heart of the mind */}
            <motion.div
              className="relative inline-block mb-10"
              animate={learning ? {} : { scale: [1, 1.03, 1] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            >
              {/* Outer glow rings */}
              {!m3Mind.frozen && !learning && (
                <>
                  <motion.div
                    className="absolute rounded-full pointer-events-none"
                    style={{
                      inset: "-20px",
                      border: `1px solid ${accentColor}10`,
                    }}
                    animate={{
                      scale: [1, 1.1, 1],
                      opacity: [0.3, 0.6, 0.3],
                    }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  />
                  <motion.div
                    className="absolute rounded-full pointer-events-none"
                    style={{
                      inset: "-40px",
                      border: `1px solid ${accentColor}06`,
                    }}
                    animate={{
                      scale: [1, 1.05, 1],
                      opacity: [0.15, 0.35, 0.15],
                    }}
                    transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
                  />
                </>
              )}

              <button
                onClick={m3Mind.frozen ? () => setShowPricing(true) : handleLearn}
                disabled={learning}
                className="relative px-14 py-5 rounded-full text-base font-display font-semibold transition-all duration-500"
                style={{
                  background: m3Mind.frozen
                    ? "rgba(255,255,255,0.03)"
                    : learning
                      ? `${accentColor}10`
                      : `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                  color: m3Mind.frozen ? "#475569" : learning ? accentColor : "#000",
                  border: `1px solid ${m3Mind.frozen ? "rgba(255,255,255,0.05)" : `${accentColor}60`}`,
                  boxShadow: !m3Mind.frozen && !learning
                    ? `0 0 50px ${accentColor}25, 0 0 100px ${accentColor}10`
                    : "none",
                  cursor: learning ? "wait" : "pointer",
                }}
              >
                {learning ? (
                  <span className="flex items-center gap-3">
                    <motion.span
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Zap size={16} />
                    </motion.span>
                    {t("m3.hub.learnButton")}...
                  </span>
                ) : m3Mind.frozen ? (
                  <span className="flex items-center gap-3">
                    <Lock size={16} />
                    {t("m3.hub.learnFrozen")}
                  </span>
                ) : (
                  <span className="flex items-center gap-3">
                    <Brain size={16} />
                    {t("m3.hub.learnButton")}
                  </span>
                )}
              </button>
            </motion.div>

            {/* Epiphany result */}
            <AnimatePresence>
              {learnResult && (
                <motion.div
                  initial={{ opacity: 0, y: 15, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.95 }}
                  transition={{ duration: 0.6, ease }}
                  className="mb-8"
                >
                  <p
                    className="text-sm font-display font-light"
                    style={{ color: accentColor }}
                  >
                    {learnResult}
                  </p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Stats — vital signs */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="flex items-center justify-center gap-12 mt-2"
            >
              {[
                { value: m3Mind.totalListens, label: t("m3.hub.listens") },
                { value: m3Mind.totalMinutes, label: t("m3.hub.minutes") },
                { value: m3Mind.previousPersonaIds.length, label: t("m3.hub.shifts") },
              ].map((stat, i) => (
                <div key={i} className="text-center">
                  <span className="text-xl font-mono text-slate-300 block tabular-nums">{stat.value}</span>
                  <span className="text-[9px] font-display text-slate-600 tracking-widest uppercase">{stat.label}</span>
                </div>
              ))}
            </motion.div>
          </motion.div>
        </section>

        {/* ── LAYER 6: SUBSTRATE ─ Tier & Footer ───────────────── */}
        <section className="py-16 px-6 md:px-12 border-t border-white/[0.03]">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, ease }}
            className="max-w-md mx-auto"
          >
            {/* Tier header */}
            <div className="flex items-center justify-between mb-5">
              <span className="text-[10px] font-display font-light tracking-[0.2em] uppercase text-slate-600">
                {t("m3.hub.tierInfo")}
              </span>
              <div
                className="px-3 py-1 rounded-full text-[10px] font-display font-medium"
                style={{
                  background: `${tierDef?.color}15`,
                  color: tierDef?.color,
                  border: `1px solid ${tierDef?.color}20`,
                }}
              >
                {t(`m3.tier.${m3Mind.tier}.name`)}
              </div>
            </div>

            {/* Features */}
            <div className="space-y-2 mb-6">
              {tierDef?.features.map((fKey) => (
                <div key={fKey} className="flex items-center gap-2">
                  <Zap size={10} style={{ color: tierDef.color }} />
                  <span className="text-[11px] text-slate-500 font-display font-light">{t(fKey)}</span>
                </div>
              ))}
            </div>

            {/* Upgrade CTA */}
            {gate.needsUpgrade && (
              <button
                onClick={() => setShowPricing(true)}
                className="w-full py-3 rounded-xl text-sm font-display font-medium transition-all duration-500 mb-6"
                style={{
                  background: `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                  color: "#000",
                  border: `1px solid ${accentColor}50`,
                  boxShadow: `0 0 30px ${accentColor}15`,
                }}
              >
                {t("m3.hub.upgradeCta")} <ChevronRight size={12} className="inline" />
              </button>
            )}

            {/* Persona card */}
            {activePersona && (
              <button
                onClick={() => navigate(`/info/${activePersona.id}`)}
                className="w-full spatial-card p-3 text-left transition-all duration-500 hover:scale-[1.01] group mb-6"
                style={{ border: `1px solid ${accentColor}10` }}
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-display font-bold"
                    style={{ background: `${accentColor}15`, color: accentColor, border: `1px solid ${accentColor}20` }}
                  >
                    {activePersona.id}
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-xs font-display font-medium" style={{ color: accentColor }}>
                      {t(`personas.${activePersona.id}.name`)}
                    </span>
                    <p className="text-[10px] text-slate-600 font-display font-light truncate">
                      {mindType} · {t("common.ofListeners", { pct: activePersona.populationPct })}
                    </p>
                  </div>
                  <ChevronRight size={14} className="text-slate-700 group-hover:text-slate-400 transition-colors" />
                </div>
              </button>
            )}

            {/* Last updated */}
            {m3Mind.lastUpdated && (
              <div className="flex items-center justify-center gap-1.5">
                <Clock size={10} className="text-slate-700" />
                <span className="text-[10px] font-mono text-slate-700">
                  {new Date(m3Mind.lastUpdated).toLocaleString()}
                </span>
              </div>
            )}
          </motion.div>
        </section>

        {/* Bottom spacer for FloatingNav */}
        <div className="h-24" />
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
