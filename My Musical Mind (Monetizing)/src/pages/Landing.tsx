import { useState, useCallback, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { ArrowRight, Check, CheckCircle2, Loader2, Brain } from "lucide-react";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { OrbitalBeliefs } from "@/components/landing/OrbitalBeliefs";
import { MindRadar } from "@/components/mind/MindRadar";
import { LanguageToggle } from "@/components/layout/LanguageToggle";
import { useUserStore } from "@/stores/useUserStore";
import { useM3Store } from "@/stores/useM3Store";
import { personas, getPersona } from "@/data/personas";
import { beliefColors } from "@/design/tokens";

const INSTITUTIONS = [
  { name: "MIT", dept: "Media Lab" },
  { name: "Stanford", dept: "CCRMA" },
  { name: "CMU", dept: "School of Music" },
];

/* ── Analysis phases (from Onboarding) ────────────────────────────── */
const ANALYSIS_PHASES = [
  { key: "onboarding.evolving.phases.p1", belief: null },
  { key: "onboarding.evolving.phases.p2", belief: null },
  { key: "onboarding.evolving.phases.p3", belief: "consonance" as const },
  { key: "onboarding.evolving.phases.p4", belief: "consonance" as const },
  { key: "onboarding.evolving.phases.p5", belief: "tempo" as const },
  { key: "onboarding.evolving.phases.p6", belief: "salience" as const },
  { key: "onboarding.evolving.phases.p7", belief: "salience" as const },
  { key: "m3.birth.determining", belief: "familiarity" as const },
  { key: "m3.birth.forming", belief: "reward" as const },
  { key: "m3.birth.firstConnections", belief: "reward" as const },
];

const MOCK_STATS = {
  songCount: 2847,
  totalMinutes: 186420,
  topGenres: ["Electronic", "Jazz", "Ambient", "Post-Rock", "Neo-Classical"],
  topArtists: ["Nils Frahm", "Aphex Twin", "Radiohead", "Max Richter"],
};

/* ── OAuth permissions ────────────────────────────────────────────── */
const OAUTH_PERMISSIONS = [
  "onboarding.connect.oauth.permPlaylists",
  "onboarding.connect.oauth.permHistory",
  "onboarding.connect.oauth.permActivity",
  "onboarding.connect.oauth.permProfile",
] as const;

/* ── Typewriter hook ──────────────────────────────────────────────── */
function useTypewriter(text: string, speed = 30) {
  const [displayed, setDisplayed] = useState("");
  const prevText = useRef("");
  useEffect(() => {
    if (text === prevText.current) return;
    prevText.current = text;
    setDisplayed("");
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));
      if (i >= text.length) clearInterval(interval);
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);
  return displayed;
}

/* ── Ticker hook ──────────────────────────────────────────────────── */
function useTicker(target: number, duration: number, active: boolean) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!active) return;
    const start = Date.now();
    const tick = () => {
      const elapsed = Date.now() - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.floor(eased * target));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [target, duration, active]);
  return value;
}

type OAuthPhase = "opening" | "authorize" | "connecting" | "connected";
type RevealPhase = "void" | "birth" | "name" | "radar" | "ready";

export function Landing() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { completeOnboarding, setDisplayName } = useUserStore();
  const birthM3 = useM3Store((s) => s.birthM3);
  const mind = useUserStore((s) => s.mind);

  // UI flow state
  const [showAuth, setShowAuth] = useState(false);
  const [showConnect, setShowConnect] = useState(false);
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signup");
  const [userName, setUserName] = useState("");

  // OAuth state
  const [showOAuth, setShowOAuth] = useState(false);
  const [oAuthPlatform, setOAuthPlatform] = useState<"spotify" | "soundcloud" | "apple">("spotify");
  const [oAuthPhase, setOAuthPhase] = useState<OAuthPhase>("opening");

  // Evolution state
  const [evolving, setEvolving] = useState(false);
  const [progress, setProgress] = useState(0);
  const [phaseKey, setPhaseKey] = useState("");

  // Reveal state
  const [selectedPersonaId, setSelectedPersonaId] = useState<number | null>(null);
  const [revealPhase, setRevealPhase] = useState<RevealPhase>("void");

  const active = showAuth || showConnect;
  const typedPhase = useTypewriter(t(phaseKey), 22);
  const songCount = useTicker(MOCK_STATS.songCount, 6000, progress > 5);
  const totalHours = useTicker(Math.floor(MOCK_STATS.totalMinutes / 60), 8000, progress > 5);

  const activeBeliefs = ANALYSIS_PHASES
    .slice(0, Math.floor((progress / 100) * ANALYSIS_PHASES.length) + 1)
    .map(p => p.belief)
    .filter((b): b is keyof typeof beliefColors => b !== null);
  const uniqueBeliefs = [...new Set(activeBeliefs)];

  // Derived background props — evolve organism through flow stages
  const persona = selectedPersonaId ? getPersona(selectedPersonaId) : null;
  const orgColor = persona ? persona.color : evolving ? `hsl(${260 + progress * 0.6}, 60%, 55%)` : "#7C3AED";
  const orgIntensity = revealPhase === "ready" ? 0.95 : revealPhase === "radar" ? 0.7 : evolving ? 0.15 + progress * 0.007 : 0.8;
  const orgStage: 1 | 2 | 3 = revealPhase === "ready" ? 3 : revealPhase === "radar" || revealPhase === "name" ? 2 : evolving && progress > 70 ? 2 : 2;
  const orgScale = revealPhase !== "void" ? 1.8 : evolving ? 0.6 + progress * 0.006 : 2.0;
  const orgBreath = revealPhase === "ready" ? 4 : evolving ? 6 - progress * 0.03 : 5;

  // Start evolution after OAuth completes
  const startEvolution = useCallback((name: string) => {
    setDisplayName(name);
    setShowConnect(false);
    setEvolving(true);

    let phaseIdx = 0;
    let prog = 0;
    const interval = setInterval(() => {
      prog += 1;
      phaseIdx = Math.min(
        Math.floor((prog / 100) * ANALYSIS_PHASES.length),
        ANALYSIS_PHASES.length - 1
      );
      setProgress(prog);
      setPhaseKey(ANALYSIS_PHASES[phaseIdx].key);

      if (prog >= 100) {
        clearInterval(interval);
        const randomPersona = personas[Math.floor(Math.random() * personas.length)];
        setSelectedPersonaId(randomPersona.id);

        completeOnboarding({
          personaId: randomPersona.id,
          axes: randomPersona.axes,
          stage: 1,
          subTrait: null,
        }, name);

        birthM3(randomPersona, "free");

        setTimeout(() => {
          setEvolving(false);
          setRevealPhase("birth");
          setTimeout(() => setRevealPhase("name"), 2300);
          setTimeout(() => setRevealPhase("radar"), 5300);
          setTimeout(() => setRevealPhase("ready"), 7300);
        }, 1200);
      }
    }, 200);
  }, [setDisplayName, completeOnboarding, birthM3]);

  // Platform connect → trigger OAuth
  const handlePlatformConnect = useCallback((platform: "spotify" | "soundcloud" | "apple") => {
    setOAuthPlatform(platform);
    setOAuthPhase("opening");
    setShowOAuth(true);
    setShowConnect(false);
  }, []);

  // OAuth phase progression
  useEffect(() => {
    if (!showOAuth) return;
    if (oAuthPhase === "opening") {
      const timer = setTimeout(() => setOAuthPhase("authorize"), 1800);
      return () => clearTimeout(timer);
    }
    if (oAuthPhase === "connecting") {
      const timer = setTimeout(() => setOAuthPhase("connected"), 2000);
      return () => clearTimeout(timer);
    }
    if (oAuthPhase === "connected") {
      const timer = setTimeout(() => {
        setShowOAuth(false);
        startEvolution(userName);
      }, 1200);
      return () => clearTimeout(timer);
    }
  }, [showOAuth, oAuthPhase, startEvolution, userName]);

  const platformColor = oAuthPlatform === "spotify" ? "#1DB954" : oAuthPlatform === "soundcloud" ? "#FF5500" : "#FC3C44";
  const showGenres = progress > 30 && progress < 85;
  const showArtists = progress > 50 && progress < 90;
  const isPreReveal = !evolving && !selectedPersonaId; // original landing state

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      {/* Living organism background — evolves through flow */}
      <motion.div
        className="absolute inset-0 z-0"
        animate={{ scale: orgScale, opacity: revealPhase === "ready" ? 0.7 : revealPhase !== "void" ? 0.55 : evolving ? 0.35 + progress * 0.005 : 1 }}
        transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
        style={{ transformOrigin: "center center" }}
      >
        <MindOrganismCanvas
          color={orgColor}
          secondaryColor={persona ? `${persona.color}80` : "#6366F1"}
          stage={orgStage}
          intensity={orgIntensity}
          breathRate={orgBreath}
          variant={revealPhase !== "void" ? "hero" : undefined}
          constellations={revealPhase === "radar" || revealPhase === "ready"}
          className="w-full h-full"
          interactive={revealPhase === "ready" || isPreReveal}
        />
      </motion.div>

      {/* Orbital beliefs — ambient decoration, locked to viewport center */}
      <div className="absolute top-1/2 left-1/2 pointer-events-none z-[1]" style={{ transform: "translate(-50%, -50%)" }}>
        <OrbitalBeliefs visible size={Math.min(900, typeof window !== "undefined" ? window.innerWidth * 1.275 : 900)} />
      </div>

      {/* Color wash — appears during reveal */}
      {revealPhase !== "void" && persona && (
        <motion.div
          className="absolute inset-0 pointer-events-none z-[2]"
          initial={{ opacity: 0 }}
          animate={{ opacity: revealPhase === "ready" ? 1 : 0.7 }}
          transition={{ duration: 2 }}
          style={{ background: `radial-gradient(ellipse 70% 60% at 50% 45%, ${persona.color}18, transparent 70%)` }}
        />
      )}

      {/* Language toggle */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 2.5 }}
        className="fixed top-6 right-6 z-20"
      >
        <LanguageToggle />
      </motion.div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Content */}
      <div className="relative z-10 h-full flex flex-col items-center justify-end pb-[22vh] px-6">
        {/* Title group — slides up when auth shown, fades out during evolving/reveal */}
        <motion.div
          className="flex flex-col items-center mb-[16.5rem]"
          animate={
            evolving || revealPhase !== "void"
              ? { y: "-25vh", scale: 0.35, opacity: 0 }
              : active
                ? { y: "-15vh", scale: 0.55, opacity: 1 }
                : { y: 0, scale: 1, opacity: 1 }
          }
          transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
          style={{ pointerEvents: evolving || revealPhase !== "void" ? "none" : "auto" }}
        >
          {/* M³ Title */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, filter: "blur(20px)" }}
            animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
            transition={{ duration: 2, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-visible"
          >
            <h1 className="relative text-center overflow-visible">
              <span
                className="text-[clamp(5rem,14vw,16rem)] font-display font-bold leading-[1.1] tracking-tighter pr-[0.15em]"
                style={{
                  background: "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(139,92,246,0.8) 50%, rgba(99,102,241,0.3) 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                M³
              </span>
              <div
                className="absolute inset-0 pointer-events-none"
                style={{
                  background: "radial-gradient(ellipse at 50% 60%, rgba(139,92,246,0.25) 0%, transparent 60%)",
                  filter: "blur(60px)",
                }}
              />
            </h1>
          </motion.div>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 0.75, y: 0 }}
            transition={{ duration: 1.5, delay: 1, ease: [0.22, 1, 0.36, 1] }}
            className="text-lg md:text-xl text-slate-300 font-display font-light tracking-[0.2em] -mt-2"
          >
            {t("landing.subtitle")}
          </motion.p>
        </motion.div>

        {/* CTA Button */}
        <motion.button
          initial={{ opacity: 0, y: 30 }}
          animate={active || evolving || revealPhase !== "void" ? { opacity: 0, y: 80 } : { opacity: 1, y: 0 }}
          transition={{ duration: active ? 0.8 : 1, delay: active ? 0 : 1.8, ease: [0.22, 1, 0.36, 1] }}
          onClick={() => setShowAuth(true)}
          whileHover={!active ? { scale: 1.06 } : undefined}
          whileTap={!active ? { scale: 0.95 } : undefined}
          style={{ pointerEvents: active || evolving || revealPhase !== "void" ? "none" : "auto" }}
          className="group relative px-16 py-5 rounded-full overflow-visible cursor-pointer"
        >
          {/* Ambient glow — always visible, intensifies on hover */}
          <motion.div
            className="absolute -inset-3 rounded-full pointer-events-none"
            initial={{ opacity: 0.3 }}
            whileHover={{ opacity: 0.5 }}
            style={{
              background: "radial-gradient(ellipse at center, rgba(139,92,246,0.55) 0%, rgba(99,102,241,0.25) 40%, transparent 70%)",
              filter: "blur(20px)",
            }}
          />

          {/* Spinning gradient border */}
          <div
            className="absolute inset-0 rounded-full transition-opacity duration-500 opacity-80 group-hover:opacity-100"
            style={{
              background: "conic-gradient(from var(--organism-border-angle, 0deg), #6366F1, #A855F7, #EC4899, #6366F1)",
              animation: "organismBorderSpin 4s linear infinite",
              padding: "1.5px",
              borderRadius: "9999px",
            }}
          >
            <div className="w-full h-full rounded-full bg-black/85 group-hover:bg-black/75 backdrop-blur-xl transition-colors duration-500" />
          </div>

          {/* Inner shimmer on hover */}
          <div
            className="absolute inset-[1.5px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700 overflow-hidden"
          >
            <div
              className="absolute inset-0"
              style={{
                background: "linear-gradient(105deg, transparent 40%, rgba(168,85,247,0.14) 45%, rgba(99,102,241,0.20) 50%, rgba(168,85,247,0.14) 55%, transparent 60%)",
                animation: "shimmer 2.5s ease-in-out infinite",
              }}
            />
          </div>

          {/* Outer glow ring on hover */}
          <div
            className="absolute -inset-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"
            style={{
              boxShadow: "0 0 40px rgba(139,92,246,0.35), 0 0 80px rgba(99,102,241,0.22), 0 0 120px rgba(236,72,153,0.12)",
            }}
          />

          <span className="relative z-10 text-sm font-display font-medium text-slate-200 group-hover:text-white transition-colors duration-300 tracking-[0.1em]">
            {t("landing.cta")}
          </span>
        </motion.button>

      </div>

      {/* ── Auth Panel ─────────────────────────────────────────────── */}
      <AnimatePresence>
        {showAuth && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.8, delay: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="fixed inset-0 z-30 flex items-center justify-center px-6"
          >
            <div className="w-full max-w-sm space-y-5">
              {/* Tab switcher */}
              <div
                className="flex gap-1 p-1 rounded-full"
                style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
              >
                <button
                  onClick={() => setAuthMode("signup")}
                  className={`flex-1 py-2.5 rounded-full text-sm font-display font-medium transition-all duration-300 ${
                    authMode === "signup" ? "bg-white/10 text-white" : "text-slate-500 hover:text-slate-300"
                  }`}
                >
                  Sign Up
                </button>
                <button
                  onClick={() => setAuthMode("signin")}
                  className={`flex-1 py-2.5 rounded-full text-sm font-display font-medium transition-all duration-300 ${
                    authMode === "signin" ? "bg-white/10 text-white" : "text-slate-500 hover:text-slate-300"
                  }`}
                >
                  Sign In
                </button>
              </div>

              {/* Form */}
              <div className="glass p-6 space-y-4">
                {authMode === "signup" && (
                  <input
                    type="text"
                    placeholder="Full Name"
                    className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-violet-500/40 transition-colors font-body"
                  />
                )}
                <input
                  type="email"
                  placeholder="Email"
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-violet-500/40 transition-colors font-body"
                />
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-violet-500/40 transition-colors font-body"
                />
                <button
                  onClick={() => { setShowAuth(false); setShowConnect(true); }}
                  className="w-full py-3 rounded-xl text-sm font-display font-medium text-white transition-all duration-300 hover:brightness-110"
                  style={{ background: "linear-gradient(135deg, #6366F1, #A855F7)" }}
                >
                  {authMode === "signup" ? "Create Account" : "Sign In"}
                </button>
              </div>

              {/* Divider */}
              <div className="flex items-center gap-3">
                <div className="flex-1 h-px bg-white/10" />
                <span className="text-xs text-slate-600 font-display">or continue with</span>
                <div className="flex-1 h-px bg-white/10" />
              </div>

              {/* Social */}
              <div className="flex gap-3">
                <button className="flex-1 glass-subtle py-3 rounded-xl text-sm font-display text-slate-400 hover:text-white transition-colors duration-300">
                  Google
                </button>
                <button className="flex-1 glass-subtle py-3 rounded-xl text-sm font-display text-slate-400 hover:text-white transition-colors duration-300">
                  Apple
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Connect Panel ──────────────────────────────────────────── */}
      <AnimatePresence>
        {showConnect && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="fixed inset-0 z-30 flex items-center justify-center px-6"
          >
            <div className="w-full max-w-sm text-center space-y-6">
              <p className="hud-label">{t("onboarding.connect.welcome")}</p>
              <h2 className="text-2xl font-display font-bold text-slate-200">
                {t("onboarding.connect.whatName")}
              </h2>

              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                placeholder={t("onboarding.connect.namePlaceholder")}
                autoFocus
                className="w-full max-w-xs mx-auto block text-center text-xl font-display font-medium text-slate-200 bg-transparent border-b-2 border-white/10 focus:border-indigo-500/50 outline-none py-3 px-4 placeholder:text-slate-700 transition-colors duration-500"
              />

              <motion.div
                animate={{ opacity: userName.trim().length >= 2 ? 1 : 0, y: userName.trim().length >= 2 ? 0 : 20 }}
                transition={{ duration: 0.5 }}
                className="space-y-3 pt-4"
                style={{ pointerEvents: userName.trim().length >= 2 ? "auto" : "none" }}
              >
                <p className="hud-label mb-2">{t("onboarding.connect.connectMusic")}</p>
                {/* Spotify */}
                <button
                  onClick={() => handlePlatformConnect("spotify")}
                  className="group w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-500"
                  style={{ background: "#1DB95406", border: "1px solid #1DB95410" }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "#1DB95412"; e.currentTarget.style.borderColor = "#1DB95425"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "#1DB95406"; e.currentTarget.style.borderColor = "#1DB95410"; }}
                >
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: "#1DB95410" }}>
                    <svg viewBox="0 0 24 24" width={22} height={22} fill="#1DB954"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" /></svg>
                  </div>
                  <div className="text-left flex-1">
                    <div className="text-sm font-display font-medium text-slate-300">Spotify</div>
                    <div className="text-xs text-slate-600">{t("onboarding.connect.spotifySub")}</div>
                  </div>
                </button>
                {/* SoundCloud */}
                <button
                  onClick={() => handlePlatformConnect("soundcloud")}
                  className="group w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-500"
                  style={{ background: "#FF550006", border: "1px solid #FF550010" }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "#FF550012"; e.currentTarget.style.borderColor = "#FF550025"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "#FF550006"; e.currentTarget.style.borderColor = "#FF550010"; }}
                >
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: "#FF550010" }}>
                    <svg viewBox="0 0 24 24" width={22} height={22} fill="#FF5500"><path d="M1.175 12.225c-.051 0-.094.046-.101.1l-.233 2.154.233 2.105c.007.058.05.098.101.098.05 0 .09-.04.099-.098l.255-2.105-.27-2.154c-.009-.06-.05-.1-.1-.1m-.899.828c-.06 0-.091.037-.104.094L0 14.479l.172 1.308c.013.06.045.094.104.094.057 0 .09-.037.104-.093l.2-1.31-.2-1.322c-.014-.06-.047-.095-.104-.095M2.26 12.06c-.063 0-.1.044-.107.105l-.212 2.314.212 2.213c.007.062.044.107.106.107.064 0 .1-.045.108-.107l.24-2.213-.24-2.314c-.007-.06-.044-.105-.107-.105m.895-.398c-.07 0-.112.05-.118.116l-.195 2.701.195 2.569c.006.068.049.116.118.116.069 0 .112-.048.119-.116l.22-2.569-.22-2.7c-.007-.067-.05-.116-.119-.116m.9-.054c-.072 0-.119.057-.125.128l-.178 2.753.178 2.612c.006.07.053.127.125.127.073 0 .119-.056.127-.127l.202-2.612-.202-2.753c-.008-.07-.054-.128-.127-.128m.899-.108c-.065 0-.124.062-.131.137l-.16 2.862.16 2.63c.007.076.066.138.13.138.065 0 .124-.062.132-.138l.183-2.63-.183-2.862c-.008-.075-.067-.137-.131-.137m.934.046c-.083 0-.138.065-.145.148l-.145 2.808.145 2.647c.007.083.062.148.145.148.082 0 .137-.065.145-.148l.165-2.647-.165-2.808c-.008-.083-.063-.148-.145-.148m.93-.283c-.09 0-.148.075-.155.158l-.128 3.091.128 2.659c.007.084.065.157.155.157.09 0 .149-.073.157-.157l.144-2.659-.144-3.091c-.008-.083-.067-.158-.157-.158m.94.134c-.098 0-.155.077-.162.168l-.112 2.957.112 2.672c.007.09.064.167.162.167.097 0 .154-.077.162-.167l.127-2.672-.127-2.957c-.008-.091-.065-.168-.162-.168m.954-.288c-.1 0-.164.083-.17.178l-.095 3.245.095 2.675c.006.095.07.178.17.178.1 0 .164-.083.172-.178l.107-2.675-.107-3.245c-.008-.095-.072-.178-.172-.178m.953.177c-.107 0-.173.09-.18.19l-.079 3.068.079 2.682c.007.1.073.189.18.189.107 0 .173-.089.181-.189l.089-2.682-.089-3.068c-.008-.1-.074-.19-.181-.19m.942-.213c-.115 0-.183.098-.19.2l-.062 3.28.062 2.682c.007.103.075.2.19.2.114 0 .182-.097.19-.2l.071-2.682-.071-3.28c-.008-.102-.076-.2-.19-.2m.972-.039c-.116 0-.192.105-.199.21l-.047 3.32.047 2.688c.007.11.083.21.2.21.115 0 .191-.1.199-.21l.053-2.688-.053-3.32c-.008-.104-.084-.21-.2-.21m1.52-1.058c-.504 0-.97.09-1.407.258-.19-2.1-1.964-3.737-4.126-3.737-.563 0-1.103.12-1.597.333-.186.081-.236.163-.238.323v8.637c.002.167.133.305.3.32h7.068a2.623 2.623 0 002.627-2.619c0-1.45-1.178-2.63-2.627-2.63" /></svg>
                  </div>
                  <div className="text-left flex-1">
                    <div className="text-sm font-display font-medium text-slate-300">SoundCloud</div>
                    <div className="text-xs text-slate-600">{t("onboarding.connect.soundcloudSub")}</div>
                  </div>
                </button>
                {/* Apple Music */}
                <button
                  onClick={() => handlePlatformConnect("apple")}
                  className="group w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-500"
                  style={{ background: "#FC3C4406", border: "1px solid #FC3C4410" }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "#FC3C4412"; e.currentTarget.style.borderColor = "#FC3C4425"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "#FC3C4406"; e.currentTarget.style.borderColor = "#FC3C4410"; }}
                >
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: "#FC3C4410" }}>
                    <svg viewBox="0 0 24 24" width={22} height={22} fill="#FC3C44"><path d="M23.994 6.124a9.23 9.23 0 00-.24-2.19c-.317-1.31-1.062-2.31-2.18-3.043A5.022 5.022 0 0019.7.165 10.56 10.56 0 0018.104.02L17.748 0H6.242l-.356.02A10.72 10.72 0 004.3.164a5.022 5.022 0 00-1.874.726C1.31 1.616.566 2.616.248 3.925a9.23 9.23 0 00-.24 2.19c-.01.2-.01.38-.01.57v10.63c0 .19 0 .37.01.57a9.23 9.23 0 00.24 2.19c.318 1.31 1.062 2.31 2.18 3.043a5.022 5.022 0 001.874.727 10.56 10.56 0 001.592.144L6.252 24h11.496l.356-.02a10.56 10.56 0 001.593-.144 5.022 5.022 0 001.874-.727c1.118-.733 1.862-1.733 2.18-3.043a9.23 9.23 0 00.24-2.19c.01-.2.01-.38.01-.57V6.694c0-.19 0-.37-.01-.57zM17.892 10.7l.01 5.28c.002.58-.16 1.103-.5 1.525a2.2 2.2 0 01-1.264.813c-.378.09-.755.12-1.128.054a1.7 1.7 0 01-1.26-.958c-.218-.45-.254-.926-.122-1.404.197-.72.693-1.185 1.38-1.443.298-.11.608-.19.91-.27.38-.1.625-.32.709-.712.023-.11.034-.222.034-.334l-.002-4.6a.84.84 0 00-.066-.302c-.08-.197-.253-.297-.462-.268-.12.016-.24.042-.356.072l-4.058 1.017a.96.96 0 00-.567.372.92.92 0 00-.154.434c-.01.093-.013.186-.012.28l.005 6.874c.003.542-.14 1.033-.448 1.467a2.26 2.26 0 01-1.24.87c-.402.1-.802.13-1.2.044a1.65 1.65 0 01-1.188-.914 1.85 1.85 0 01-.143-1.296c.167-.723.63-1.2 1.31-1.472.316-.125.643-.213.97-.3.312-.084.528-.282.62-.596a1.2 1.2 0 00.043-.296l-.003-8.4c0-.23.037-.455.138-.664.14-.287.38-.462.68-.535.127-.03.258-.054.388-.076l5.014-1.215c.27-.065.544-.122.824-.142a1.17 1.17 0 01.724.174c.26.158.4.392.44.692.014.1.018.2.018.3z" /></svg>
                  </div>
                  <div className="text-left flex-1">
                    <div className="text-sm font-display font-medium text-slate-300">Apple Music</div>
                    <div className="text-xs text-slate-600">{t("onboarding.connect.appleSub")}</div>
                  </div>
                </button>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Bottom bar: compact footer ───────────────────────────── */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.5, duration: 2 }}
        className="absolute bottom-0 left-0 right-0 z-10 px-6 pb-3 pt-2"
      >
        <div className="flex items-center justify-between max-w-2xl mx-auto">
          <span className="text-[10px] font-display font-light text-slate-500 tracking-[0.15em]">
            SRC<sup className="text-[8px]">9</sup> <span className="text-slate-600 mx-1">|</span> {t("landing.copyright")}
          </span>
          <div className="hidden md:flex items-center gap-4">
            {INSTITUTIONS.map((inst) => (
              <span key={inst.name} className="text-[9px] font-display font-light text-slate-600 tracking-[0.15em]">
                {inst.name} <span className="text-slate-700">{inst.dept}</span>
              </span>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
