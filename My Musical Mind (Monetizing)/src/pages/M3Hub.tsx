/* ── M³ Hub — "Zihnim" (My Mind) ─ Living Identity ──────────────────
 *  WHO your mind IS right now. Experiential, immersive, organism-centered.
 *  Full-screen organism hero + persona identity + mind genes +
 *  observations (3-layer) + learn button + growth timeline.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Sparkles, Lock, Zap, Clock, ChevronRight,
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
import type { M3Tier } from "@/types/m3";
import { pageTransition, cinematicReveal } from "@/design/animations";
import type { PresentationLayer } from "@/types/m3";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";

const LAYERS: PresentationLayer[] = ["surface", "narrative", "deep"];

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

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">
      {/* ── Full-screen organism hero ─────────────────────────────── */}
      <div className="absolute inset-0 z-0" style={{ transform: "scale(1.3)", transformOrigin: "center center" }}>
        <MindOrganismCanvas
          color={accentColor}
          stage={organismStage}
          intensity={0.5 + m3Mind.stageProgress * 0.4}
          breathRate={5 - m3Mind.stageProgress * 2}
          familyMorphology={morphology}
          className="w-full h-full"
          variant="hero"
          interactive
        />
      </div>
      <div
        className="absolute inset-0 z-[1] pointer-events-none"
        style={{ background: `radial-gradient(ellipse 60% 60% at 50% 45%, transparent 15%, rgba(0,0,0,0.7) 55%, rgba(0,0,0,0.92) 100%)` }}
      />
      <div className="cinematic-vignette z-[2]" />

      {/* ── Frozen Overlay ────────────────────────────────────────── */}
      <AnimatePresence>
        {m3Mind.frozen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-40 flex items-center justify-center bg-black/60 backdrop-blur-sm"
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

      {/* ═══ MAIN LAYOUT ══════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-10 pb-24">

        {/* ── TOP: Persona Identity ────────────────────────────── */}
        <motion.div {...cinematicReveal} className="text-center py-1">
          <div className="flex items-center justify-center gap-2 mb-1">
            <NucleusDot color={accentColor} size={4} active pulsing />
            <span className="text-[10px] font-display font-light tracking-[0.2em] uppercase text-slate-600">
              {mindType} · L{m3Mind.level}/12
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-display font-bold tracking-tight" style={{ color: accentColor }}>
            {activePersona ? t(`personas.${activePersona.id}.name`) : t("m3.hub.title")}
          </h1>
          <p className="text-sm text-slate-500 font-display font-light mt-1 italic">
            {activePersona ? t(`personas.${activePersona.id}.tagline`) : ""}
          </p>
          <div className="max-w-xs mx-auto mt-3">
            <PersonaLevelTrack currentLevel={m3Mind.level} color={accentColor} />
          </div>
        </motion.div>

        {/* ── MAIN GRID ────────────────────────────────────────── */}
        <div className="flex-1 grid grid-cols-12 gap-4 min-h-0 overflow-hidden mt-3">

          {/* ═ LEFT COLUMN (3 cols): Mind Type + Functions + Timeline */}
          <div className="col-span-3 flex flex-col gap-3 min-h-0">

            {/* Mind Type Ring */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="spatial-card p-3 flex-shrink-0 flex flex-col items-center"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2 w-full">
                {t("m3.hub.mindType")}
              </span>
              <MindTypeRing genes={m3Mind.genes} size={100} />
            </motion.div>

            {/* Active Functions Grid */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="spatial-card p-3 flex-shrink-0"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-3">
                {t("m3.hub.activeFunctions")}
              </span>
              <div className="grid grid-cols-3 gap-2">
                {C3_FUNCTIONS.map((fn) => {
                  const isActive = m3Mind.activeFunctions.includes(fn.id);
                  return (
                    <div
                      key={fn.id}
                      className="relative flex flex-col items-center gap-1 py-2 rounded-lg transition-all duration-500"
                      style={{
                        background: isActive ? `${fn.color}12` : "rgba(255,255,255,0.02)",
                        border: `1px solid ${isActive ? `${fn.color}25` : "rgba(255,255,255,0.04)"}`,
                        opacity: isActive ? 1 : 0.3,
                      }}
                    >
                      <span className="text-xs font-mono font-bold" style={{ color: isActive ? fn.color : "#475569" }}>
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
                    </div>
                  );
                })}
              </div>
            </motion.div>

            {/* Growth Timeline */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="spatial-card p-3 flex-1 min-h-0 overflow-y-auto"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-3">
                {t("m3.hub.growthTimeline")}
              </span>
              <div className="space-y-2">
                {[...milestones].reverse().slice(0, 20).map((ms, i) => {
                  const milestoneColor =
                    ms.type === "birth" ? "#FBBF24" :
                    ms.type === "level_up" ? "#22D3EE" :
                    ms.type === "stage_up" ? "#A855F7" :
                    ms.type === "persona_shift" ? "#EC4899" :
                    ms.type === "function_unlock" ? "#84CC16" :
                    ms.type === "type_change" ? "#EF4444" : "#475569";
                  return (
                    <div key={i} className="flex items-start gap-2">
                      <div
                        className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0"
                        style={{ background: milestoneColor, boxShadow: `0 0 6px ${milestoneColor}40` }}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-[11px] text-slate-400 font-display leading-tight truncate">
                          {ms.detail}
                        </p>
                        <p className="text-[9px] font-mono text-slate-700">
                          {new Date(ms.timestamp).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>

          {/* ═ CENTER COLUMN (5 cols): Observations + Learn ═══════ */}
          <div className="col-span-5 flex flex-col items-center justify-center gap-4 min-h-0">

            {/* Stage + progress */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="w-full max-w-md"
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg" style={{ color: stageColor }}>{stageDef?.icon}</span>
                  <span className="text-[10px] font-display font-light tracking-[0.15em] uppercase" style={{ color: stageColor }}>
                    {t(`m3.stage.${m3Mind.stage}`)}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-slate-600">
                  {Math.round(m3Mind.stageProgress * 100)}%
                </span>
              </div>
              <div className="w-full h-[3px] rounded-full bg-white/[0.04] overflow-hidden">
                <motion.div
                  className="h-full rounded-full"
                  style={{ background: `linear-gradient(90deg, ${stageColor}80, ${stageColor})`, boxShadow: `0 0 16px ${stageColor}40` }}
                  initial={{ width: 0 }}
                  animate={{ width: `${m3Mind.stageProgress * 100}%` }}
                  transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
                />
              </div>
            </motion.div>

            {/* Layer Toggle */}
            <div className="flex items-center gap-1 p-1 rounded-full" style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.05)" }}>
              {LAYERS.map((layer) => {
                const isActive = activeLayer === layer;
                const canSee = gate.canSeeLayer(layer);
                return (
                  <button
                    key={layer}
                    onClick={() => handleLayerChange(layer)}
                    disabled={!canSee}
                    className="relative px-4 py-1.5 rounded-full text-[11px] font-display transition-all duration-300"
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

            {/* Observations */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="w-full max-w-lg"
            >
              <div className="spatial-card p-5 glow-border" style={{ "--glow-color": accentColor } as React.CSSProperties}>
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles size={14} style={{ color: accentColor }} />
                  <span className="text-[11px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${accentColor}90` }}>
                    {t("m3.hub.currentObservation")}
                  </span>
                  <span className="text-[9px] font-mono text-slate-700 ml-auto">
                    {unlockedTypes.length}/{9} {t("m3.hub.typesUnlocked")}
                  </span>
                </div>
                <div className="space-y-3 max-h-40 overflow-y-auto">
                  {observations.length > 0 ? observations.map((obs) => (
                    <div key={obs.id} className="flex items-start gap-2">
                      <div
                        className="w-1 h-1 rounded-full mt-2 flex-shrink-0"
                        style={{ background: accentColor, opacity: obs.intensity }}
                      />
                      <p className="text-[13px] text-slate-400 font-body font-light leading-relaxed">
                        {obs.text}
                      </p>
                    </div>
                  )) : (
                    <p className="text-[12px] text-slate-600 font-body font-light italic">
                      {t("m3.hub.noObservations")}
                    </p>
                  )}
                </div>
              </div>
            </motion.div>

            {/* Learn Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7, duration: 0.8 }}
            >
              <button
                onClick={m3Mind.frozen ? () => setShowPricing(true) : handleLearn}
                disabled={learning}
                className="group relative px-8 py-3.5 rounded-xl text-sm font-display font-semibold transition-all duration-500"
                style={{
                  background: m3Mind.frozen
                    ? "rgba(255,255,255,0.03)"
                    : learning
                      ? `${accentColor}10`
                      : `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                  color: m3Mind.frozen ? "#475569" : learning ? accentColor : "#000",
                  border: `1px solid ${m3Mind.frozen ? "rgba(255,255,255,0.05)" : `${accentColor}60`}`,
                  boxShadow: !m3Mind.frozen && !learning ? `0 0 30px ${accentColor}25` : "none",
                  cursor: learning ? "wait" : "pointer",
                }}
              >
                {learning ? (
                  <span className="flex items-center gap-2">
                    <motion.span animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}>
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

            <AnimatePresence>
              {learnResult && (
                <motion.p
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -5 }}
                  className="text-xs font-display font-light text-center"
                  style={{ color: accentColor }}
                >
                  {learnResult}
                </motion.p>
              )}
            </AnimatePresence>

            {/* Stats row */}
            <div className="flex items-center gap-6 text-center">
              <div>
                <span className="text-xs font-mono text-slate-400">{m3Mind.totalListens}</span>
                <p className="text-[9px] font-display text-slate-600">{t("m3.hub.listens")}</p>
              </div>
              <div>
                <span className="text-xs font-mono text-slate-400">{m3Mind.totalMinutes}</span>
                <p className="text-[9px] font-display text-slate-600">{t("m3.hub.minutes")}</p>
              </div>
              <div>
                <span className="text-xs font-mono text-slate-400">{m3Mind.previousPersonaIds.length}</span>
                <p className="text-[9px] font-display text-slate-600">{t("m3.hub.shifts")}</p>
              </div>
            </div>
          </div>

          {/* ═ RIGHT COLUMN (4 cols): Gene Bars + Parameters + Tier ═══════ */}
          <div className="col-span-4 flex flex-col gap-3 min-h-0">

            {/* Gene Bars */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="spatial-card p-3 flex-shrink-0"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2">
                {t("m3.hub.geneProfile")}
              </span>
              <div className="space-y-2">
                {GENE_NAMES.map((gene, i) => {
                  const value = m3Mind.genes[gene];
                  const pct = Math.round(value * 100);
                  const color = GENE_COLORS[gene];
                  return (
                    <div key={gene} className="flex items-center gap-2">
                      <span className="text-[10px] font-display text-slate-500 w-20 truncate">
                        {t(`m3.gene.${gene}`)}
                      </span>
                      <div className="flex-1 h-[3px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: color, opacity: 0.7 }}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: i * 0.06 }}
                        />
                      </div>
                      <span className="text-[10px] font-mono w-10 text-right" style={{ color: `${color}90` }}>
                        {pct}
                      </span>
                    </div>
                  );
                })}
              </div>
            </motion.div>

            {/* Persona card (link to detail page) */}
            {activePersona && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
              >
                <button
                  onClick={() => navigate(`/info/${activePersona.id}`)}
                  className="w-full spatial-card p-3 text-left transition-all duration-500 hover:scale-[1.01] group"
                  style={{ border: `1px solid ${accentColor}15` }}
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
              </motion.div>
            )}

            {/* Tier Info */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
              className="spatial-card p-3 flex-shrink-0"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2">
                {t("m3.hub.tierInfo")}
              </span>
              <div className="flex items-center gap-2 mb-2">
                <div
                  className="px-3 py-1 rounded-full text-xs font-display font-medium"
                  style={{ background: `${tierDef?.color}15`, color: tierDef?.color, border: `1px solid ${tierDef?.color}20` }}
                >
                  {t(`m3.tier.${m3Mind.tier}.name`)}
                </div>
              </div>
              <div className="space-y-1">
                {tierDef?.features.map((fKey) => (
                  <div key={fKey} className="flex items-center gap-1.5">
                    <Zap size={10} style={{ color: tierDef.color }} />
                    <span className="text-[11px] text-slate-400 font-display font-light">{t(fKey)}</span>
                  </div>
                ))}
              </div>
              {gate.needsUpgrade && (
                <button
                  onClick={() => setShowPricing(true)}
                  className="mt-3 w-full py-2 rounded-lg text-xs font-display font-medium transition-all duration-500"
                  style={{
                    background: `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                    color: "#000",
                    border: `1px solid ${accentColor}50`,
                  }}
                >
                  {t("m3.hub.upgradeCta")} <ChevronRight size={12} className="inline" />
                </button>
              )}
            </motion.div>

            {/* Last updated */}
            {m3Mind.lastUpdated && (
              <div className="flex items-center gap-1.5 px-3">
                <Clock size={10} className="text-slate-700" />
                <span className="text-[10px] font-mono text-slate-700">
                  {new Date(m3Mind.lastUpdated).toLocaleString()}
                </span>
              </div>
            )}
          </div>

        </div>
      </div>

      {/* ── Pricing Overlay ─────────────────────────────────────────── */}
      <TrainingPricingOverlay
        isOpen={showPricing}
        onClose={() => setShowPricing(false)}
        onSelect={handleTierSelect}
        accentColor={accentColor}
      />

      {/* ── Congrats Animation ──────────────────────────────────────── */}
      <CongratsAnimation
        tier={congratsTier}
        accentColor={accentColor}
        isVisible={showCongrats}
        onDismiss={() => setShowCongrats(false)}
      />

      {/* ── Type Change Animation ───────────────────────────────────── */}
      <TypeChangeAnimation
        isVisible={showTypeChange}
        typeName={typeChangeName}
        typeColor={typeChangeColor}
        onDismiss={() => setShowTypeChange(false)}
      />
    </motion.div>
  );
}
