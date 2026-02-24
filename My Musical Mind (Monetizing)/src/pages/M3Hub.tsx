/* ── M³ Hub — The Living Mind ──────────────────────────────────────
 *  Central page for the M³ personal musical mind.
 *  Shows stage, temperament, active functions, observations,
 *  growth timeline, and the feed mechanism.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, ChevronRight, Sparkles, Lock,
  Activity, Zap, Clock,
} from "lucide-react";
import { useM3Store } from "@/stores/useM3Store";
import { useM3Gate } from "@/hooks/useM3Gate";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { C3_FUNCTIONS, M3_STAGES, M3_TEMPERAMENTS, M3_TIERS } from "@/data/m3-stages";
import { generateObservations, getPrimaryObservation } from "@/data/m3-observations";
import { SpotifySimulator, trackToM3Signal } from "@/services/SpotifySimulator";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import type { PresentationLayer } from "@/types/m3";

const LAYERS: PresentationLayer[] = ["surface", "narrative", "deep"];

export function M3Hub() {
  const { t } = useTranslation();
  const m3Mind = useM3Store((s) => s.mind);
  const milestones = useM3Store((s) => s.milestones);
  const feedListening = useM3Store((s) => s.feedListening);
  const preferredLayer = useM3Store((s) => s.preferredLayer);
  const setPreferredLayer = useM3Store((s) => s.setPreferredLayer);
  const gate = useM3Gate();
  const { mind: userMind } = useUserStore();
  const persona = userMind ? getPersona(userMind.personaId) : null;
  const accentColor = persona?.color ?? "#A855F7";

  const [activeLayer, setActiveLayer] = useState<PresentationLayer>(preferredLayer);
  const [feeding, setFeeding] = useState(false);
  const [feedResult, setFeedResult] = useState<string | null>(null);

  // Stage data
  const stageDef = m3Mind ? M3_STAGES[m3Mind.stage] : null;
  const stageColor = stageDef?.color ?? "#94A3B8";
  const temperamentDef = m3Mind ? M3_TEMPERAMENTS[m3Mind.temperament] : null;
  const tierDef = m3Mind ? M3_TIERS[m3Mind.tier] : null;

  // Observations
  const observations = useMemo(() => {
    if (!m3Mind) return [];
    return generateObservations(m3Mind, activeLayer, t);
  }, [m3Mind, activeLayer, t]);

  const primaryObs = useMemo(() => {
    if (!m3Mind) return null;
    return getPrimaryObservation(m3Mind, t);
  }, [m3Mind, t]);

  // Feed M³
  const handleFeed = useCallback(() => {
    if (!m3Mind || m3Mind.frozen || feeding) return;
    setFeeding(true);
    setFeedResult(null);

    const session = SpotifySimulator.getListeningSession();
    let newMilestones: ReturnType<typeof feedListening>[] = [];

    // Simulate feeding tracks one by one with a delay
    setTimeout(() => {
      for (const entry of session) {
        const signal = trackToM3Signal(entry.track, {
          wasSkipped: entry.wasSkipped,
          isRepeat: false,
        });
        const ms = feedListening(signal);
        newMilestones.push(ms);
      }
      setFeeding(false);
      setFeedResult(t("m3.hub.feedSuccess", { count: session.length }));
      setTimeout(() => setFeedResult(null), 4000);
    }, 1500);
  }, [m3Mind, feeding, feedListening, t]);

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
      {/* Organism background */}
      <div className="absolute inset-0 z-0" style={{ transform: "scale(1.3)", transformOrigin: "center center" }}>
        <MindOrganismCanvas
          color={stageColor}
          secondaryColor={temperamentDef?.color ?? stageColor}
          stage={stageDef?.organismStage ?? 1}
          intensity={0.5 + m3Mind.stageProgress * 0.4}
          breathRate={5 - m3Mind.stageProgress * 2}
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

      {/* ── Frozen Overlay ─────────────────────────────────────────── */}
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
                className="px-6 py-3 rounded-xl text-sm font-display font-semibold transition-all duration-500"
                style={{
                  background: `linear-gradient(135deg, ${stageColor}, ${stageColor}CC)`,
                  color: "#000",
                  border: `1px solid ${stageColor}60`,
                  boxShadow: `0 0 30px ${stageColor}25`,
                }}
              >
                {t("m3.frozen.cta")}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── TOP HUD ────────────────────────────────────────────────── */}
      <motion.div
        variants={fadeIn}
        initial="initial"
        animate="animate"
        className="fixed top-10 left-6 z-30 flex items-center gap-4"
      >
        {/* Stage badge */}
        <div className="flex items-center gap-2">
          <span className="text-lg" style={{ color: stageColor }}>{stageDef?.icon}</span>
          <div>
            <span className="text-xs font-display font-medium" style={{ color: stageColor }}>
              {t(`m3.stage.${m3Mind.stage}`)}
            </span>
            <span className="text-[10px] font-mono text-slate-600 ml-2">
              {Math.round(m3Mind.stageProgress * 100)}%
            </span>
          </div>
        </div>

        {/* Temperament */}
        <div className="flex items-center gap-1.5">
          <span style={{ color: temperamentDef?.color }}>{temperamentDef?.icon}</span>
          <span className="text-[11px] font-display text-slate-500">
            {t(`m3.temperament.${m3Mind.temperament}`)}
          </span>
        </div>

        {/* Tier */}
        <div
          className="px-2 py-0.5 rounded-full text-[10px] font-display font-medium"
          style={{ background: `${tierDef?.color ?? "#94A3B8"}15`, color: tierDef?.color, border: `1px solid ${tierDef?.color ?? "#94A3B8"}20` }}
        >
          {t(`m3.tier.${m3Mind.tier}.name`)}
        </div>

        {/* Listen counter */}
        <div className="flex items-center gap-1.5">
          <Activity size={12} className="text-slate-600" />
          <span className="text-xs font-mono text-slate-500">{m3Mind.totalListens} listens</span>
        </div>
      </motion.div>

      {/* ═══ MAIN LAYOUT ══════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-10 pb-24">

        {/* ── TOP: Title ─────────────────────────────────────────── */}
        <motion.div {...cinematicReveal} className="text-center py-0.5">
          <h1 className="text-3xl md:text-4xl font-display font-bold tracking-tight" style={{ color: stageColor }}>
            {t("m3.hub.title")}
          </h1>
          <p className="text-sm text-slate-500 font-display font-light mt-1">
            {t("m3.hub.subtitle")}
          </p>
        </motion.div>

        {/* ── MAIN GRID ─────────────────────────────────────────── */}
        <div className="flex-1 grid grid-cols-12 gap-4 min-h-0 overflow-hidden mt-3">

          {/* ═ LEFT COLUMN (3 cols): Active Functions + Timeline ═ */}
          <div className="col-span-3 flex flex-col gap-3 min-h-0">

            {/* Active Functions Grid */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
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
                      <span
                        className="text-xs font-mono font-bold"
                        style={{ color: isActive ? fn.color : "#475569" }}
                      >
                        {fn.abbr}
                      </span>
                      <span className="text-[9px] font-display text-slate-500 text-center leading-tight px-1">
                        {t(`m3.functions.f${fn.id}.name`)}
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
                {[...milestones].reverse().slice(0, 15).map((ms, i) => {
                  const isStageUp = ms.type === "stage_up";
                  const isBirth = ms.type === "birth";
                  return (
                    <div key={i} className="flex items-start gap-2">
                      <div
                        className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0"
                        style={{
                          background: isBirth ? "#FBBF24" : isStageUp ? "#A855F7" : "#475569",
                          boxShadow: isStageUp ? "0 0 8px #A855F740" : undefined,
                        }}
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

          {/* ═ CENTER COLUMN (5 cols): Observation + Feed ═══════ */}
          <div className="col-span-5 flex flex-col items-center justify-center gap-5 min-h-0">

            {/* Stage progress bar */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="w-full max-w-md"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-display font-light tracking-[0.15em] uppercase" style={{ color: stageColor }}>
                  {t(`m3.stage.${m3Mind.stage}`)}
                </span>
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
              <p className="text-[10px] text-slate-600 font-display font-light mt-1 text-center">
                {t(`m3.stage.description.${m3Mind.stage}`)}
              </p>
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
                      background: isActive ? `${stageColor}15` : "transparent",
                      color: isActive ? stageColor : canSee ? "#64748B" : "#1E293B",
                      border: isActive ? `1px solid ${stageColor}20` : "1px solid transparent",
                      cursor: canSee ? "pointer" : "not-allowed",
                    }}
                  >
                    {t(`m3.layer.${layer}`)}
                    {!canSee && <Lock size={8} className="inline ml-1" />}
                  </button>
                );
              })}
            </div>

            {/* Current Observations */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="w-full max-w-lg"
            >
              <div className="spatial-card p-5 glow-border" style={{ "--glow-color": stageColor } as React.CSSProperties}>
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles size={14} style={{ color: stageColor }} />
                  <span className="text-[11px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${stageColor}90` }}>
                    {t("m3.hub.currentObservation")}
                  </span>
                </div>
                <div className="space-y-3">
                  {observations.map((obs) => (
                    <div key={obs.id} className="flex items-start gap-2">
                      <div
                        className="w-1 h-1 rounded-full mt-2 flex-shrink-0"
                        style={{ background: stageColor, opacity: obs.intensity }}
                      />
                      <p className="text-[13px] text-slate-400 font-body font-light leading-relaxed">
                        {obs.text}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Convince me note */}
            <p className="text-[11px] text-slate-600 font-display font-light italic text-center max-w-sm">
              {t("m3.hub.convinceMe")}
            </p>

            {/* Feed M³ Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7, duration: 0.8 }}
            >
              <button
                onClick={handleFeed}
                disabled={m3Mind.frozen || feeding}
                className="group relative px-8 py-3.5 rounded-xl text-sm font-display font-semibold transition-all duration-500"
                style={{
                  background: m3Mind.frozen
                    ? "rgba(255,255,255,0.03)"
                    : feeding
                      ? `${stageColor}10`
                      : `linear-gradient(135deg, ${stageColor}, ${stageColor}CC)`,
                  color: m3Mind.frozen ? "#475569" : feeding ? stageColor : "#000",
                  border: `1px solid ${m3Mind.frozen ? "rgba(255,255,255,0.05)" : `${stageColor}60`}`,
                  boxShadow: !m3Mind.frozen && !feeding ? `0 0 30px ${stageColor}25` : "none",
                  cursor: m3Mind.frozen ? "not-allowed" : "pointer",
                }}
              >
                {feeding ? (
                  <span className="flex items-center gap-2">
                    <motion.span
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Zap size={14} />
                    </motion.span>
                    {t("m3.hub.feedButton")}...
                  </span>
                ) : m3Mind.frozen ? (
                  <span className="flex items-center gap-2">
                    <Lock size={14} />
                    {t("m3.hub.feedFrozen")}
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Brain size={14} />
                    {t("m3.hub.feedButton")}
                  </span>
                )}
              </button>
            </motion.div>

            {/* Feed result message */}
            <AnimatePresence>
              {feedResult && (
                <motion.p
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -5 }}
                  className="text-xs font-display font-light text-center"
                  style={{ color: stageColor }}
                >
                  {feedResult}
                </motion.p>
              )}
            </AnimatePresence>
          </div>

          {/* ═ RIGHT COLUMN (4 cols): Parameters + Temperament + Tier ═ */}
          <div className="col-span-4 flex flex-col gap-3 min-h-0">

            {/* Parameter Activity */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="spatial-card p-3 flex-shrink-0"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2">
                {t("m3.hub.parameterActivity")}
              </span>
              <div className="space-y-2">
                {[
                  { label: "Reward", arr: m3Mind.parameters.rewardWeights, color: "#FBBF24" },
                  { label: "Precision", arr: m3Mind.parameters.precisionWeights, color: "#A855F7" },
                  { label: "Temporal", arr: m3Mind.parameters.temporalPrefs, color: "#F97316" },
                  { label: "Timbral", arr: m3Mind.parameters.timbralMap, color: "#22D3EE" },
                  { label: "Attention", arr: m3Mind.parameters.attentionBiases, color: "#84CC16" },
                ].map(({ label, arr, color }) => {
                  const mean = arr.reduce((s, v) => s + Math.abs(v), 0) / arr.length;
                  const pct = Math.min(100, mean * 1000);
                  return (
                    <div key={label} className="flex items-center gap-2">
                      <span className="text-[10px] font-display text-slate-500 w-16 truncate">{label}</span>
                      <div className="flex-1 h-[3px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: color, opacity: 0.7 }}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                        />
                      </div>
                      <span className="text-[10px] font-mono w-10 text-right" style={{ color: `${color}90` }}>
                        {(mean * 1000).toFixed(1)}
                      </span>
                    </div>
                  );
                })}
              </div>
            </motion.div>

            {/* Temperament Profile */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="spatial-card p-3 flex-shrink-0"
            >
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2">
                {t("m3.hub.temperamentProfile")}
              </span>
              <div className="flex items-center gap-3 mb-2">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-lg"
                  style={{ background: `${temperamentDef?.color}15`, border: `1px solid ${temperamentDef?.color}20` }}
                >
                  {temperamentDef?.icon}
                </div>
                <div>
                  <span className="text-sm font-display font-medium" style={{ color: temperamentDef?.color }}>
                    {t(`m3.temperament.${m3Mind.temperament}`)}
                  </span>
                  <p className="text-[11px] text-slate-500 font-display font-light leading-tight mt-0.5">
                    {t(`m3.temperament.description.${m3Mind.temperament}`)}
                  </p>
                </div>
              </div>
            </motion.div>

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
                <span className="text-[10px] text-slate-600 font-display font-light italic">
                  {t(`m3.tier.${m3Mind.tier}.tagline`)}
                </span>
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
                  className="mt-3 w-full py-2 rounded-lg text-xs font-display font-medium transition-all duration-500"
                  style={{
                    background: `linear-gradient(135deg, ${stageColor}, ${stageColor}CC)`,
                    color: "#000",
                    border: `1px solid ${stageColor}50`,
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
    </motion.div>
  );
}
