import { useCallback, useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Check, Crown, Sparkles, Zap, Music, Brain, Radio, Users, Star, Shield, Headphones, Eye } from "lucide-react";
import { useOnboardingStore } from "@/stores/useOnboardingStore";
import { useUserStore } from "@/stores/useUserStore";
import { useM3Store } from "@/stores/useM3Store";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { personas, getPersona } from "@/data/personas";
import { beliefColors } from "@/design/tokens";
import { LanguageToggle } from "@/components/layout/LanguageToggle";
import { SpotifySimulator } from "@/services/SpotifySimulator";

/* ── Platform SVG logos (inline, no dependencies) ────────────────── */
function SpotifyLogo({ size = 28 }: { size?: number }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="#1DB954">
      <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
    </svg>
  );
}

function SoundCloudLogo({ size = 28 }: { size?: number }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="#FF5500">
      <path d="M1.175 12.225c-.051 0-.094.046-.101.1l-.233 2.154.233 2.105c.007.058.05.098.101.098.05 0 .09-.04.099-.098l.255-2.105-.27-2.154c-.009-.06-.05-.1-.1-.1m-.899.828c-.06 0-.091.037-.104.094L0 14.479l.172 1.308c.013.06.045.094.104.094.057 0 .09-.037.104-.093l.2-1.31-.2-1.322c-.014-.06-.047-.095-.104-.095M2.26 12.06c-.063 0-.1.044-.107.105l-.212 2.314.212 2.213c.007.062.044.107.106.107.064 0 .1-.045.108-.107l.24-2.213-.24-2.314c-.007-.06-.044-.105-.107-.105m.895-.398c-.07 0-.112.05-.118.116l-.195 2.701.195 2.569c.006.068.049.116.118.116.069 0 .112-.048.119-.116l.22-2.569-.22-2.7c-.007-.067-.05-.116-.119-.116m.9-.054c-.072 0-.119.057-.125.128l-.178 2.753.178 2.612c.006.07.053.127.125.127.073 0 .119-.056.127-.127l.202-2.612-.202-2.753c-.008-.07-.054-.128-.127-.128m.899-.108c-.065 0-.124.062-.131.137l-.16 2.862.16 2.63c.007.076.066.138.13.138.065 0 .124-.062.132-.138l.183-2.63-.183-2.862c-.008-.075-.067-.137-.131-.137m.934.046c-.083 0-.138.065-.145.148l-.145 2.808.145 2.647c.007.083.062.148.145.148.082 0 .137-.065.145-.148l.165-2.647-.165-2.808c-.008-.083-.063-.148-.145-.148m.93-.283c-.09 0-.148.075-.155.158l-.128 3.091.128 2.659c.007.084.065.157.155.157.09 0 .149-.073.157-.157l.144-2.659-.144-3.091c-.008-.083-.067-.158-.157-.158m.94.134c-.098 0-.155.077-.162.168l-.112 2.957.112 2.672c.007.09.064.167.162.167.097 0 .154-.077.162-.167l.127-2.672-.127-2.957c-.008-.091-.065-.168-.162-.168m.954-.288c-.1 0-.164.083-.17.178l-.095 3.245.095 2.675c.006.095.07.178.17.178.1 0 .164-.083.172-.178l.107-2.675-.107-3.245c-.008-.095-.072-.178-.172-.178m.953.177c-.107 0-.173.09-.18.19l-.079 3.068.079 2.682c.007.1.073.189.18.189.107 0 .173-.089.181-.189l.089-2.682-.089-3.068c-.008-.1-.074-.19-.181-.19m.942-.213c-.115 0-.183.098-.19.2l-.062 3.28.062 2.682c.007.103.075.2.19.2.114 0 .182-.097.19-.2l.071-2.682-.071-3.28c-.008-.102-.076-.2-.19-.2m.972-.039c-.116 0-.192.105-.199.21l-.047 3.32.047 2.688c.007.11.083.21.2.21.115 0 .191-.1.199-.21l.053-2.688-.053-3.32c-.008-.104-.084-.21-.2-.21m1.52-1.058c-.504 0-.97.09-1.407.258-.19-2.1-1.964-3.737-4.126-3.737-.563 0-1.103.12-1.597.333-.186.081-.236.163-.238.323v8.637c.002.167.133.305.3.32h7.068a2.623 2.623 0 002.627-2.619c0-1.45-1.178-2.63-2.627-2.63" />
    </svg>
  );
}

function AppleMusicLogo({ size = 28 }: { size?: number }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="#FC3C44">
      <path d="M23.994 6.124a9.23 9.23 0 00-.24-2.19c-.317-1.31-1.062-2.31-2.18-3.043A5.022 5.022 0 0019.7.165 10.56 10.56 0 0018.104.02L17.748 0H6.242l-.356.02A10.72 10.72 0 004.3.164a5.022 5.022 0 00-1.874.726C1.31 1.616.566 2.616.248 3.925a9.23 9.23 0 00-.24 2.19c-.01.2-.01.38-.01.57v10.63c0 .19 0 .37.01.57a9.23 9.23 0 00.24 2.19c.318 1.31 1.062 2.31 2.18 3.043a5.022 5.022 0 001.874.727 10.56 10.56 0 001.592.144L6.252 24h11.496l.356-.02a10.56 10.56 0 001.593-.144 5.022 5.022 0 001.874-.727c1.118-.733 1.862-1.733 2.18-3.043a9.23 9.23 0 00.24-2.19c.01-.2.01-.38.01-.57V6.694c0-.19 0-.37-.01-.57zM17.892 10.7l.01 5.28c.002.58-.16 1.103-.5 1.525a2.2 2.2 0 01-1.264.813c-.378.09-.755.12-1.128.054a1.7 1.7 0 01-1.26-.958c-.218-.45-.254-.926-.122-1.404.197-.72.693-1.185 1.38-1.443.298-.11.608-.19.91-.27.38-.1.625-.32.709-.712.023-.11.034-.222.034-.334l-.002-4.6a.84.84 0 00-.066-.302c-.08-.197-.253-.297-.462-.268-.12.016-.24.042-.356.072l-4.058 1.017a.96.96 0 00-.567.372.92.92 0 00-.154.434c-.01.093-.013.186-.012.28l.005 6.874c.003.542-.14 1.033-.448 1.467a2.26 2.26 0 01-1.24.87c-.402.1-.802.13-1.2.044a1.65 1.65 0 01-1.188-.914 1.85 1.85 0 01-.143-1.296c.167-.723.63-1.2 1.31-1.472.316-.125.643-.213.97-.3.312-.084.528-.282.62-.596a1.2 1.2 0 00.043-.296l-.003-8.4c0-.23.037-.455.138-.664.14-.287.38-.462.68-.535.127-.03.258-.054.388-.076l5.014-1.215c.27-.065.544-.122.824-.142a1.17 1.17 0 01.724.174c.26.158.4.392.44.692.014.1.018.2.018.3z" />
    </svg>
  );
}

/* ── Mock listening stats ────────────────────────────────────────── */
const MOCK_STATS = {
  songCount: 2847,
  totalMinutes: 186420,
  topGenres: ["Electronic", "Jazz", "Ambient", "Post-Rock", "Neo-Classical"],
  topArtists: ["Nils Frahm", "Aphex Twin", "Radiohead", "Max Richter"],
  listeningYears: 8,
};

/* ── Conversational analysis phases — more descriptive ───────────── */
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

/* ── Membership Plans ────────────────────────────────────────────── */
const PLANS = [
  {
    id: "pulse",
    name: "Pulse",
    price: "$9.99",
    period: "/mo",
    tagline: "Feel the rhythm of your mind",
    description: "The perfect starting point for your musical self-discovery. Begin to understand the hidden patterns in how you listen.",
    icon: Headphones,
    color: "#6366F1",
    features: [
      { text: "Musical Mind persona discovery", key: "onboarding.plans.features.personaDiscovery", icon: Brain },
      { text: "5-axis mind radar visualization", key: "onboarding.plans.features.fiveAxis", icon: Radio },
      { text: "Weekly evolution reports", key: "onboarding.plans.features.weeklyReports", icon: Zap },
      { text: "Basic listening analytics", key: "onboarding.plans.features.basicAnalytics", icon: Music },
      { text: "Community forum access", key: "onboarding.plans.features.communityAccess", icon: Users },
      { text: "50 track analyses / month", key: "onboarding.plans.features.fiftyAnalyses", icon: Star },
    ],
  },
  {
    id: "resonance",
    name: "Resonance",
    price: "$19.99",
    period: "/mo",
    tagline: "Amplify your musical identity",
    description: "For the curious soul who craves depth. Unlock the full spectrum of your listening DNA and connect with minds like yours.",
    icon: Sparkles,
    color: "#A855F7",
    popular: true,
    features: [
      { text: "Everything in Pulse", key: "onboarding.plans.features.everythingPulse", icon: Check },
      { text: "Live Performance neural mode", key: "onboarding.plans.features.livePerformance", icon: Radio },
      { text: "Advanced 97D perceptual map", key: "onboarding.plans.features.advanced97D", icon: Brain },
      { text: "Mind compatibility matching", key: "onboarding.plans.features.compatibility", icon: Users },
      { text: "Unlimited track analyses", key: "onboarding.plans.features.unlimitedAnalyses", icon: Zap },
      { text: "Custom evolution paths", key: "onboarding.plans.features.customPaths", icon: Star },
      { text: "Priority community badge", key: "onboarding.plans.features.priorityBadge", icon: Shield },
    ],
  },
  {
    id: "transcendence",
    name: "Transcendence",
    price: "$49.99",
    period: "/mo",
    tagline: "Unlock the full spectrum",
    description: "The ultimate experience. Real-time neural mapping, AI insights, and an exclusive community of visionary listeners who hear what others can't.",
    icon: Crown,
    color: "#FBBF24",
    features: [
      { text: "Everything in Resonance", key: "onboarding.plans.features.everythingResonance", icon: Check },
      { text: "Real-time brain region activation", key: "onboarding.plans.features.brainActivation", icon: Brain },
      { text: "AI-powered mind insights", key: "onboarding.plans.features.aiInsights", icon: Sparkles },
      { text: "Exclusive Visionary sessions", key: "onboarding.plans.features.visionarySessions", icon: Crown },
      { text: "Early access to all features", key: "onboarding.plans.features.earlyAccess", icon: Zap },
      { text: "Personal sound signature", key: "onboarding.plans.features.soundSignature", icon: Music },
      { text: "1-on-1 mind coaching", key: "onboarding.plans.features.coaching", icon: Eye },
      { text: "Founding member status", key: "onboarding.plans.features.foundingMember", icon: Shield },
    ],
  },
];

/* ── Typewriter hook ─────────────────────────────────────────────── */
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

/* ── Ticker animation hook ───────────────────────────────────────── */
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

export function Onboarding() {
  const navigate = useNavigate();
  const { step, setStep, setPersona, setProgress, setSelectedPlan, analysisProgress, analysisPhase, selectedPersonaId, selectedTier } =
    useOnboardingStore();
  const { completeOnboarding, displayName, setDisplayName, mind } = useUserStore();
  const birthM3 = useM3Store((s) => s.birthM3);
  const [userName, setUserName] = useState(displayName || "");

  const startEvolution = useCallback((name: string) => {
    setDisplayName(name);
    setStep("evolving");

    let phaseIdx = 0;
    let progress = 0;

    const interval = setInterval(() => {
      progress += 1;
      phaseIdx = Math.min(
        Math.floor((progress / 100) * ANALYSIS_PHASES.length),
        ANALYSIS_PHASES.length - 1
      );
      setProgress(progress, ANALYSIS_PHASES[phaseIdx].key);

      if (progress >= 100) {
        clearInterval(interval);
        const randomPersona = personas[Math.floor(Math.random() * personas.length)];
        setPersona(randomPersona.id);

        completeOnboarding({
          personaId: randomPersona.id,
          axes: randomPersona.axes,
          stage: 1,
          subTrait: null,
        }, name);

        // M³ birth: use the assigned persona for initial family affinity
        birthM3(randomPersona, selectedTier);

        setTimeout(() => {
          setStep("reveal");
        }, 1200);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [setStep, setProgress, setPersona, completeOnboarding, setDisplayName, birthM3, selectedTier]);

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      <div className="cinematic-vignette" />

      {/* Language toggle */}
      <div className="fixed top-6 right-6 z-50">
        <LanguageToggle />
      </div>

      <AnimatePresence mode="wait">
        {step === "plans" && (
          <PlanStep
            key="plans"
            onSelect={(planId) => {
              setSelectedPlan(planId);
              setStep("signup");
            }}
          />
        )}
        {step === "signup" && (
          <SignupStep
            key="signup"
            onComplete={() => setStep("connect")}
          />
        )}
        {step === "connect" && (
          <ConnectStep key="connect" userName={userName} onNameChange={setUserName} onConnect={() => startEvolution(userName)} />
        )}
        {step === "evolving" && (
          <EvolvingStep key="evolving" progress={analysisProgress} phase={analysisPhase} userName={userName} />
        )}
        {step === "reveal" && selectedPersonaId && mind && (
          <RevealStep key="reveal" personaId={selectedPersonaId} mind={mind} displayName={userName} onEnter={() => navigate("/m3")} />
        )}
      </AnimatePresence>
    </div>
  );
}

/* ── Plan Selection Step ─────────────────────────────────────────── */
function PlanStep({ onSelect }: { onSelect: (planId: string) => void }) {
  const { t } = useTranslation();
  const [hoveredPlan, setHoveredPlan] = useState<string | null>(null);
  const [entered, setEntered] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 300);
    return () => clearTimeout(t);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: entered ? 1 : 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 1 }}
      className="h-full flex flex-col items-center relative overflow-y-auto"
    >
      {/* Ambient organism background */}
      <div className="fixed inset-0 opacity-[0.06]">
        <MindOrganismCanvas color="#6366F1" secondaryColor="#A855F7" stage={1} intensity={0.2} className="w-full h-full" interactive={false} />
      </div>

      <div className="relative z-10 w-full max-w-5xl mx-auto px-6 py-12 md:py-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 1, ease: [0.22, 1, 0.36, 1] }}
          className="text-center mb-4"
        >
          <p className="hud-label mb-4">{t("onboarding.plans.chooseJourney")}</p>
          <h1 className="text-3xl md:text-5xl font-display font-bold text-slate-200 mb-4">
            {t("onboarding.plans.mindDeserved")}{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #A855F7, #EC4899)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              {t("onboarding.plans.heard")}
            </span>
          </h1>
          <p className="text-base md:text-lg text-slate-500 font-display font-light max-w-2xl mx-auto leading-relaxed">
            {t("onboarding.plans.description")}
          </p>
        </motion.div>

        {/* Community note */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="text-center text-sm text-slate-600 font-display font-light mb-10 md:mb-14"
        >
          {t("onboarding.plans.communityNote")}
        </motion.p>

        {/* Plans grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6 mb-12">
          {PLANS.map((plan, idx) => {
            const Icon = plan.icon;
            const isHovered = hoveredPlan === plan.id;
            const isPopular = plan.popular;

            return (
              <motion.div
                key={plan.id}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + idx * 0.15, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                onMouseEnter={() => setHoveredPlan(plan.id)}
                onMouseLeave={() => setHoveredPlan(null)}
                className="relative group"
              >
                {/* Popular badge */}
                {isPopular && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.2, duration: 0.5 }}
                    className="absolute -top-3.5 left-1/2 -translate-x-1/2 z-20"
                  >
                    <div
                      className="px-4 py-1 rounded-full text-[10px] font-display font-semibold uppercase tracking-[0.15em]"
                      style={{
                        background: `linear-gradient(135deg, ${plan.color}, #EC4899)`,
                        color: "#000",
                        boxShadow: `0 0 20px ${plan.color}40`,
                      }}
                    >
                      {t("onboarding.plans.mostPopular")}
                    </div>
                  </motion.div>
                )}

                {/* Card */}
                <div
                  className="relative rounded-2xl p-6 md:p-7 transition-all duration-500 cursor-pointer h-full flex flex-col"
                  style={{
                    background: isHovered
                      ? `rgba(255,255,255,0.04)`
                      : "rgba(0,0,0,0.5)",
                    backdropFilter: "blur(16px)",
                    border: `1px solid ${isHovered || isPopular ? `${plan.color}30` : "rgba(255,255,255,0.05)"}`,
                    boxShadow: isHovered
                      ? `0 0 60px ${plan.color}12, 0 20px 60px -20px rgba(0,0,0,0.5)`
                      : isPopular
                        ? `0 0 40px ${plan.color}08`
                        : "none",
                    transform: isHovered ? "translateY(-4px)" : "translateY(0)",
                  }}
                  onClick={() => onSelect(plan.id)}
                >
                  {/* Icon + name */}
                  <div className="flex items-center gap-3 mb-4">
                    <div
                      className="w-10 h-10 rounded-xl flex items-center justify-center"
                      style={{ background: `${plan.color}12`, border: `1px solid ${plan.color}20` }}
                    >
                      <Icon size={20} style={{ color: plan.color }} />
                    </div>
                    <div>
                      <h3 className="text-lg font-display font-bold text-slate-200">{plan.name}</h3>
                      <p className="text-xs text-slate-600 font-display font-light italic">{t(`onboarding.plans.${plan.id}.tagline`)}</p>
                    </div>
                  </div>

                  {/* Price */}
                  <div className="mb-4">
                    <span className="text-4xl font-display font-bold" style={{ color: plan.color }}>
                      {plan.price}
                    </span>
                    <span className="text-sm text-slate-600 font-display font-light">{plan.period}</span>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-slate-500 font-display font-light leading-relaxed mb-6">
                    {t(`onboarding.plans.${plan.id}.description`)}
                  </p>

                  {/* Features */}
                  <div className="space-y-2.5 mb-7 flex-1">
                    {plan.features.map((feature, fi) => {
                      const FIcon = feature.icon;
                      return (
                        <div key={fi} className="flex items-start gap-2.5">
                          <FIcon size={14} className="mt-0.5 flex-shrink-0" style={{ color: `${plan.color}90` }} />
                          <span className="text-sm text-slate-400 font-display font-light">{t(feature.key)}</span>
                        </div>
                      );
                    })}
                  </div>

                  {/* CTA button */}
                  <button
                    className="w-full py-3.5 rounded-xl text-sm font-display font-semibold transition-all duration-500 tracking-wide"
                    style={{
                      background: isPopular || isHovered
                        ? `linear-gradient(135deg, ${plan.color}, ${plan.color}CC)`
                        : `${plan.color}10`,
                      color: isPopular || isHovered ? "#000" : plan.color,
                      border: `1px solid ${plan.color}${isPopular || isHovered ? "60" : "20"}`,
                      boxShadow: isPopular || isHovered ? `0 0 30px ${plan.color}25` : "none",
                    }}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelect(plan.id);
                    }}
                  >
                    {isPopular ? t("onboarding.plans.startJourney") : t("onboarding.plans.choose", { name: plan.name })}
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Bottom trust text */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="text-center pb-8"
        >
          <p className="text-xs text-slate-700 font-display font-light">
            {t("onboarding.plans.cancelAnytime")}
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
}

/* ── Signup Step (Email + Password) ──────────────────────────────── */
function SignupStep({ onComplete }: { onComplete: () => void }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [entered, setEntered] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { selectedPlan } = useOnboardingStore();

  const plan = PLANS.find((p) => p.id === selectedPlan);
  const canProceed = email.trim().length > 0 && password.trim().length > 0;

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 200);
    return () => clearTimeout(t);
  }, []);

  const handleSubmit = () => {
    if (canProceed) onComplete();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: entered ? 1 : 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.8 }}
      className="h-full flex items-center justify-center relative"
    >
      {/* Ambient organism background */}
      <div className="fixed inset-0 opacity-[0.06]">
        <MindOrganismCanvas
          color={plan?.color || "#A855F7"}
          stage={1}
          intensity={0.2}
          className="w-full h-full"
          interactive={false}
        />
      </div>

      <div className="relative z-10 w-full max-w-md mx-auto px-6">
        {/* Selected plan badge */}
        {plan && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="flex justify-center mb-8"
          >
            <div
              className="flex items-center gap-2 px-4 py-2 rounded-full"
              style={{
                background: `${plan.color}08`,
                border: `1px solid ${plan.color}20`,
              }}
            >
              <plan.icon size={14} style={{ color: plan.color }} />
              <span className="text-xs font-display font-medium" style={{ color: plan.color }}>
                {plan.name}
              </span>
              <span className="text-xs text-slate-600 font-display font-light">
                {plan.price}{plan.period}
              </span>
            </div>
          </motion.div>
        )}

        {/* Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="text-center mb-10"
        >
          <p className="hud-label mb-4">{t("onboarding.signup.almostThere")}</p>
          <h1 className="text-2xl md:text-3xl font-display font-bold text-slate-200 mb-3">
            {t("onboarding.signup.createAccount")}{" "}
            <span
              style={{
                background: `linear-gradient(135deg, ${plan?.color || "#A855F7"}, #EC4899)`,
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              M³
            </span>
            {" "}{t("onboarding.signup.account")}
          </h1>
          <p className="text-sm text-slate-500 font-display font-light">
            {t("onboarding.signup.fewKeystrokes")}
          </p>
        </motion.div>

        {/* Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.8 }}
          className="space-y-4 mb-8"
        >
          {/* Email */}
          <div>
            <label className="block text-[11px] uppercase tracking-[0.15em] text-slate-600 font-display font-medium mb-2">
              {t("onboarding.signup.email")}
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={t("onboarding.signup.emailPlaceholder")}
              autoFocus
              className="w-full text-base font-display text-slate-200 bg-transparent rounded-xl px-4 py-3.5 outline-none transition-all duration-500 placeholder:text-slate-700"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: `1px solid ${email ? `${plan?.color || "#A855F7"}30` : "rgba(255,255,255,0.06)"}`,
              }}
              onFocus={(e) => { e.currentTarget.style.borderColor = `${plan?.color || "#A855F7"}50`; }}
              onBlur={(e) => { e.currentTarget.style.borderColor = email ? `${plan?.color || "#A855F7"}30` : "rgba(255,255,255,0.06)"; }}
              onKeyDown={(e) => { if (e.key === "Enter") { const pw = document.getElementById("pw-input"); pw?.focus(); } }}
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-[11px] uppercase tracking-[0.15em] text-slate-600 font-display font-medium mb-2">
              {t("onboarding.signup.password")}
            </label>
            <div className="relative">
              <input
                id="pw-input"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={t("onboarding.signup.passwordPlaceholder")}
                className="w-full text-base font-display text-slate-200 bg-transparent rounded-xl px-4 py-3.5 pr-12 outline-none transition-all duration-500 placeholder:text-slate-700"
                style={{
                  background: "rgba(255,255,255,0.03)",
                  border: `1px solid ${password ? `${plan?.color || "#A855F7"}30` : "rgba(255,255,255,0.06)"}`,
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = `${plan?.color || "#A855F7"}50`; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = password ? `${plan?.color || "#A855F7"}30` : "rgba(255,255,255,0.06)"; }}
                onKeyDown={(e) => { if (e.key === "Enter" && canProceed) handleSubmit(); }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-400 transition-colors"
              >
                <Eye size={18} />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Submit button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: canProceed ? 1 : 0.3, y: 0 }}
          transition={{ delay: 1, duration: 0.8 }}
        >
          <button
            onClick={handleSubmit}
            disabled={!canProceed}
            className="w-full py-4 rounded-xl text-base font-display font-semibold transition-all duration-500 tracking-wide"
            style={{
              background: canProceed
                ? `linear-gradient(135deg, ${plan?.color || "#A855F7"}, ${plan?.color || "#A855F7"}CC)`
                : "rgba(255,255,255,0.03)",
              color: canProceed ? "#000" : "rgba(255,255,255,0.2)",
              border: `1px solid ${canProceed ? `${plan?.color || "#A855F7"}60` : "rgba(255,255,255,0.05)"}`,
              boxShadow: canProceed ? `0 0 40px ${plan?.color || "#A855F7"}20` : "none",
              cursor: canProceed ? "pointer" : "not-allowed",
            }}
          >
            {t("onboarding.signup.continue")}
            <ArrowRight size={16} className="inline ml-2" />
          </button>
        </motion.div>

        {/* Terms */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.3, duration: 1 }}
          className="text-center text-[11px] text-slate-700 font-display font-light mt-5 leading-relaxed"
        >
          {t("onboarding.signup.terms")}
          <br />
          {t("onboarding.signup.respectData")}
        </motion.p>
      </div>
    </motion.div>
  );
}

/* ── Connect Step (Spotify + Name) ───────────────────────────────── */
function ConnectStep({ userName, onNameChange, onConnect }: { userName: string; onNameChange: (n: string) => void; onConnect: () => void }) {
  const { t } = useTranslation();
  const [entered, setEntered] = useState(false);
  const canProceed = userName.trim().length >= 2;

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 300);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="h-full flex items-center justify-center relative">
      <div className="absolute inset-0 opacity-[0.08]">
        <MindOrganismCanvas color="#6366F1" stage={1} intensity={0.2} className="w-full h-full" interactive={false} />
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: entered ? 1 : 0 }}
        transition={{ duration: 1.5 }}
        className="relative z-10 text-center max-w-md mx-auto px-6"
      >
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="hud-label mb-6"
        >
          {t("onboarding.connect.welcome")}
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="text-2xl font-display font-bold text-slate-200 mb-3"
        >
          {t("onboarding.connect.whatName")}
        </motion.h1>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.8 }}
          className="mb-10"
        >
          <input
            type="text"
            value={userName}
            onChange={(e) => onNameChange(e.target.value)}
            placeholder={t("onboarding.connect.namePlaceholder")}
            autoFocus
            className="w-full max-w-xs mx-auto block text-center text-xl font-display font-medium text-slate-200 bg-transparent border-b-2 border-white/10 focus:border-indigo-500/50 outline-none py-3 px-4 placeholder:text-slate-700 transition-colors duration-500"
            onKeyDown={(e) => { if (e.key === "Enter" && canProceed) onConnect(); }}
          />
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: canProceed ? 1 : 0 }}
          transition={{ duration: 0.5 }}
          className="hud-label mb-4"
        >
          {t("onboarding.connect.connectMusic")}
        </motion.p>

        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: canProceed ? 1 : 0 }}
          transition={{ duration: 0.5 }}
          className="text-lg font-display font-medium text-slate-400 mb-8"
        >
          {t("onboarding.connect.whereMusic")}
        </motion.h2>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: canProceed ? 1 : 0, y: canProceed ? 0 : 20 }}
          transition={{ duration: 0.6 }}
          className="space-y-3"
          style={{ pointerEvents: canProceed ? "auto" : "none" }}
        >
          <ConnectButton logo={<SpotifyLogo />} name="Spotify" sub={t("onboarding.connect.spotifySub")} color="#1DB954" onClick={onConnect} delay={0} />
          <ConnectButton logo={<SoundCloudLogo />} name="SoundCloud" sub={t("onboarding.connect.soundcloudSub")} color="#FF5500" onClick={onConnect} delay={0.1} />
          <ConnectButton logo={<AppleMusicLogo />} name="Apple Music" sub={t("onboarding.connect.appleSub")} color="#FC3C44" onClick={onConnect} delay={0.2} />
        </motion.div>
      </motion.div>
    </div>
  );
}

function ConnectButton({ logo, name, sub, color, onClick, delay }: {
  logo: React.ReactNode; name: string; sub: string; color: string; onClick: () => void; delay: number;
}) {
  return (
    <motion.button
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 1.5 + delay, duration: 0.6 }}
      onClick={onClick}
      className="group w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-500"
      style={{ background: `${color}06`, border: `1px solid ${color}10` }}
      onMouseEnter={(e) => { e.currentTarget.style.background = `${color}12`; e.currentTarget.style.borderColor = `${color}25`; }}
      onMouseLeave={(e) => { e.currentTarget.style.background = `${color}06`; e.currentTarget.style.borderColor = `${color}10`; }}
    >
      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${color}10` }}>
        {logo}
      </div>
      <div className="text-left flex-1">
        <div className="text-sm font-display font-medium text-slate-300">{name}</div>
        <div className="text-xs text-slate-600">{sub}</div>
      </div>
      <span className="text-xs font-medium opacity-0 group-hover:opacity-50 transition-opacity" style={{ color }}>Connect</span>
    </motion.button>
  );
}

/* ── Evolving Step — Mind Forming ────────────────────────────────── */
function EvolvingStep({ progress, phase, userName }: { progress: number; phase: string; userName: string }) {
  const { t } = useTranslation();
  const hue = 260 + progress * 0.6;
  const color = `hsl(${hue}, 60%, 55%)`;
  const orgStage = progress > 70 ? 2 : 1 as const;
  const orgIntensity = 0.15 + progress * 0.007;

  const typedPhase = useTypewriter(t(phase), 22);
  const songCount = useTicker(MOCK_STATS.songCount, 6000, progress > 5);
  const totalHours = useTicker(Math.floor(MOCK_STATS.totalMinutes / 60), 8000, progress > 5);

  const showGenres = progress > 30 && progress < 85;
  const showArtists = progress > 50 && progress < 90;

  const activeBeliefs = ANALYSIS_PHASES
    .slice(0, Math.floor((progress / 100) * ANALYSIS_PHASES.length) + 1)
    .map(p => p.belief)
    .filter((b): b is keyof typeof beliefColors => b !== null);
  const uniqueBeliefs = [...new Set(activeBeliefs)];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, scale: 1.05, filter: "blur(10px)" }}
      transition={{ duration: 1 }}
      className="h-full flex flex-col items-center justify-center relative"
    >
      {/* Organism background — large, growing */}
      <motion.div
        initial={{ scale: 0.3, opacity: 0 }}
        animate={{ scale: 0.6 + progress * 0.006, opacity: 0.35 + progress * 0.005 }}
        transition={{ duration: 0.4 }}
        className="absolute inset-0"
        style={{ transform: `scale(${0.6 + progress * 0.006})`, transformOrigin: "center center" }}
      >
        <MindOrganismCanvas color={color} stage={orgStage} intensity={orgIntensity} breathRate={6 - progress * 0.03} className="w-full h-full" interactive={false} />
      </motion.div>

      {/* Orbital trails — larger radii */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        {uniqueBeliefs.map((belief, i) => {
          const bColor = beliefColors[belief].primary;
          const radius = 160 + i * 50;
          return (
            <motion.div
              key={belief}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 0.4, scale: 1 }}
              transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
              className="absolute rounded-full"
              style={{
                width: radius * 2, height: radius * 2,
                background: `conic-gradient(from ${i * 72}deg, ${bColor}25, transparent 20%, transparent 100%)`,
                maskImage: `radial-gradient(transparent ${radius - 3}px, black ${radius - 2}px, black ${radius + 2}px, transparent ${radius + 3}px)`,
                WebkitMaskImage: `radial-gradient(transparent ${radius - 3}px, black ${radius - 2}px, black ${radius + 2}px, transparent ${radius + 3}px)`,
                animation: `orbit ${22 + i * 5}s linear infinite`,
              }}
            >
              <div className="absolute w-3 h-3 rounded-full" style={{ top: -6, left: radius - 6, background: bColor, boxShadow: `0 0 16px ${bColor}70, 0 0 40px ${bColor}25` }} />
            </motion.div>
          );
        })}
      </div>

      <div className="relative z-10 text-center max-w-2xl mx-auto px-6">
        {/* Title */}
        <motion.div
          initial={{ opacity: 0, y: 30, filter: "blur(10px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 1.2 }}
          className="mb-6"
        >
          <p className="text-sm font-display font-light text-slate-600 tracking-[0.2em] uppercase mb-3">
            {t("onboarding.evolving.neuralGenesis")}
          </p>
          <h2 className="text-3xl md:text-4xl font-display font-bold text-slate-200 mb-2">
            {userName ? t("onboarding.evolving.mindForming", { name: userName }) : t("onboarding.evolving.mindFormingDefault")}
          </h2>
          <p className="text-base font-display font-light text-slate-500">
            {t("onboarding.evolving.mapping97")}
          </p>
        </motion.div>

        {/* Belief indicators — bigger */}
        <div className="flex justify-center gap-6 mb-8">
          {(["consonance", "tempo", "salience", "familiarity", "reward"] as const).map((b) => {
            const isActive = uniqueBeliefs.includes(b);
            const bColor = beliefColors[b].primary;
            return (
              <motion.div key={b} initial={{ opacity: 0.1 }} animate={{ opacity: isActive ? 0.9 : 0.1 }} transition={{ duration: 0.6 }} className="flex flex-col items-center gap-2">
                <div className="w-3 h-3 rounded-full transition-all duration-500" style={{ background: bColor, boxShadow: isActive ? `0 0 14px ${bColor}70, 0 0 30px ${bColor}25` : "none" }} />
                <span className="text-[10px] font-display font-light uppercase tracking-[0.15em]" style={{ color: isActive ? `${bColor}CC` : "#1E293B" }}>
                  {b}
                </span>
              </motion.div>
            );
          })}
        </div>

        {/* Phase text — typewriter */}
        <div className="h-8 mb-8">
          <p className="text-base text-slate-400 font-body font-light italic leading-relaxed">
            {typedPhase}
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ repeat: Infinity, duration: 0.6 }}
              className="inline-block w-[2px] h-4 bg-slate-500 ml-1 align-text-bottom"
            />
          </p>
        </div>

        {/* Stats panel */}
        <AnimatePresence>
          {progress > 10 && (
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
              className="mb-10 mx-auto max-w-md"
            >
              <div className="rounded-2xl p-6" style={{ background: "rgba(0,0,0,0.6)", backdropFilter: "blur(16px)", border: "1px solid rgba(255,255,255,0.05)" }}>
                {/* Track & Hours counters */}
                <div className="flex justify-center gap-12 mb-5">
                  <div className="text-center">
                    <div className="text-2xl font-mono font-medium text-slate-200">
                      {songCount.toLocaleString()}
                    </div>
                    <div className="text-[11px] uppercase tracking-widest text-slate-600 font-display">{t("onboarding.evolving.tracksScanned")}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-mono font-medium text-slate-200">
                      {totalHours.toLocaleString()}
                    </div>
                    <div className="text-[11px] uppercase tracking-widest text-slate-600 font-display">{t("onboarding.evolving.hoursListening")}</div>
                  </div>
                </div>

                {/* Genres */}
                <AnimatePresence>
                  {showGenres && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.5 }}
                      className="flex flex-wrap justify-center gap-2 mb-4"
                    >
                      {MOCK_STATS.topGenres.map((genre, i) => (
                        <motion.span
                          key={genre}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: i * 0.15, duration: 0.4 }}
                          className="px-3 py-1.5 rounded-full text-xs font-display font-light text-slate-400"
                          style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}
                        >
                          {genre}
                        </motion.span>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Top artists */}
                <AnimatePresence>
                  {showArtists && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.5 }}
                      className="text-center"
                    >
                      <span className="text-[10px] uppercase tracking-[0.15em] text-slate-700 block mb-2 font-display">{t("onboarding.evolving.topArtists")}</span>
                      <p className="text-sm text-slate-500 font-body font-light">
                        {MOCK_STATS.topArtists.map((artist, i) => (
                          <motion.span
                            key={artist}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: i * 0.2, duration: 0.4 }}
                          >
                            {i > 0 && <span className="text-slate-700 mx-1.5">&middot;</span>}
                            {artist}
                          </motion.span>
                        ))}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Progress bar — wider */}
        <div className="w-80 mx-auto">
          <div className="w-full h-[3px] rounded-full bg-white/[0.04] overflow-hidden">
            <motion.div className="h-full rounded-full" style={{ background: `linear-gradient(90deg, ${color}80, ${color})`, boxShadow: `0 0 24px ${color}40` }} animate={{ width: `${progress}%` }} transition={{ duration: 0.3 }} />
          </div>
          <div className="mt-3 flex justify-between items-center">
            <span className="text-[10px] font-display font-light text-slate-700 tracking-wider uppercase">{t("onboarding.evolving.forming")}</span>
            <span className="text-xs font-mono text-slate-600 tracking-wider">{progress}%</span>
            <span className="text-[10px] font-display font-light text-slate-700 tracking-wider uppercase">{t("onboarding.evolving.complete")}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ── Reveal Step — Persona emerges in-page ───────────────────────── */
type RevealPhase = "void" | "birth" | "name" | "radar" | "ready";

function RevealStep({ personaId, mind, displayName, onEnter }: {
  personaId: number;
  mind: { personaId: number; axes: { entropyTolerance: number; resolutionCraving: number; monotonyTolerance: number; salienceSensitivity: number; tensionAppetite: number }; stage: number; subTrait: string | null };
  displayName: string;
  onEnter: () => void;
}) {
  const { t } = useTranslation();
  const [phase, setPhase] = useState<RevealPhase>("void");
  const persona = getPersona(personaId);
  const m3Mind = useM3Store((s) => s.mind);

  useEffect(() => {
    if (!persona) return;
    const timers = [
      setTimeout(() => setPhase("birth"), 1200),
      setTimeout(() => setPhase("name"), 3500),
      setTimeout(() => setPhase("radar"), 6500),
      setTimeout(() => setPhase("ready"), 8500),
    ];
    return () => timers.forEach(clearTimeout);
  }, [persona]);

  if (!persona) return null;

  const color = persona.color;

  return (
    <motion.div
      initial={{ opacity: 0, filter: "blur(10px)" }}
      animate={{ opacity: 1, filter: "blur(0px)" }}
      transition={{ duration: 1.5 }}
      className="h-full relative"
    >
      {/* Conic gradient trails per belief */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        {phase !== "void" && (["consonance", "tempo", "salience", "familiarity", "reward"] as const).map((b, i) => {
          const bColor = beliefColors[b].primary;
          const radius = 180 + i * 50;
          return (
            <motion.div
              key={b}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 0.2, scale: 1 }}
              transition={{ duration: 2, delay: i * 0.2, ease: [0.22, 1, 0.36, 1] }}
              className="absolute rounded-full"
              style={{
                width: radius * 2, height: radius * 2,
                background: `conic-gradient(from ${i * 72}deg, ${bColor}25, transparent 20%, transparent 100%)`,
                maskImage: `radial-gradient(transparent ${radius - 3}px, black ${radius - 2}px, black ${radius + 2}px, transparent ${radius + 3}px)`,
                WebkitMaskImage: `radial-gradient(transparent ${radius - 3}px, black ${radius - 2}px, black ${radius + 2}px, transparent ${radius + 3}px)`,
                animation: `orbit ${28 + i * 4}s linear infinite`,
              }}
            />
          );
        })}
      </div>

      {/* Organism explodes from center — large, detailed, persona-colored */}
      <AnimatePresence>
        {phase !== "void" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.05 }}
            animate={{
              opacity: phase === "ready" ? 0.7 : phase === "radar" ? 0.55 : 0.35,
              scale: 1,
            }}
            transition={{ duration: 3, ease: [0.22, 1, 0.36, 1] }}
            className="absolute inset-0"
            style={{ transform: "scale(1.8)", transformOrigin: "center center" }}
          >
            <MindOrganismCanvas
              color={color}
              secondaryColor={`${color}80`}
              stage={phase === "ready" ? 3 : phase === "radar" ? 2 : 1}
              intensity={phase === "ready" ? 0.95 : phase === "radar" ? 0.7 : 0.5}
              breathRate={phase === "ready" ? 4 : 3}
              variant="hero"
              constellations={phase === "radar" || phase === "ready"}
              interactive={phase === "ready"}
              className="w-full h-full"
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Color wash — stronger with persona color */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        initial={{ opacity: 0 }}
        animate={{ opacity: phase === "ready" ? 1 : phase !== "void" ? 0.7 : 0 }}
        transition={{ duration: 2 }}
        style={{ background: `radial-gradient(ellipse 70% 60% at 50% 45%, ${color}18, transparent 70%)` }}
      />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-6">
        <AnimatePresence>
          {phase === "void" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 0.4 }} exit={{ opacity: 0 }} transition={{ duration: 0.8 }}>
              <motion.span animate={{ opacity: [0.2, 0.6, 0.2] }} transition={{ duration: 2, repeat: Infinity }} className="text-base text-slate-600 font-display font-light tracking-[0.15em]">
                {t("onboarding.reveal.preparing")}
              </motion.span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Name — character-by-character */}
        <AnimatePresence>
          {(phase === "name" || phase === "radar" || phase === "ready") && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} className="text-center">
              <motion.p initial={{ opacity: 0, y: 10 }} animate={{ opacity: 0.4, y: 0 }} transition={{ duration: 1 }} className="text-sm font-display font-light text-slate-500 tracking-[0.2em] uppercase mb-6">
                {displayName && displayName !== "You" ? `${displayName}, ${t("onboarding.reveal.youAre")}` : t("onboarding.reveal.youAreDefault")}
              </motion.p>

              <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold mb-5 leading-none flex justify-center flex-wrap">
                {persona.name.split("").map((char, i) => (
                  <motion.span
                    key={i}
                    initial={{ opacity: 0, y: 50, scale: 0.3, filter: "blur(15px)" }}
                    animate={{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)" }}
                    transition={{ duration: 0.7, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
                    style={{ color, display: "inline-block" }}
                  >
                    {char === " " ? "\u00A0" : char}
                  </motion.span>
                ))}
              </h1>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.5 }}
                transition={{ delay: persona.name.length * 0.06 + 0.5, duration: 1 }}
                className="text-xl text-slate-500 font-display font-light italic"
              >
                "{persona.tagline}"
              </motion.p>

              {/* M³ Birth Badge */}
              {m3Mind && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: persona.name.length * 0.06 + 1.2, duration: 0.8 }}
                  className="flex items-center gap-3 mt-5 px-5 py-2.5 rounded-full mx-auto"
                  style={{ background: `${color}08`, border: `1px solid ${color}15` }}
                >
                  <Brain size={16} style={{ color }} />
                  <span className="text-sm font-display font-medium" style={{ color }}>
                    L{m3Mind.level}/12 · {persona.family}
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full" style={{ background: `${color}15`, color }}>
                    {t(`m3.stage.${m3Mind.stage}`)}
                  </span>
                  {m3Mind.frozen && (
                    <span className="text-[10px] font-mono text-slate-500 px-2 py-0.5 rounded-full bg-white/[0.04]">
                      {t("m3.frozen.title")}
                    </span>
                  )}
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Radar */}
        <AnimatePresence>
          {(phase === "radar" || phase === "ready") && (
            <motion.div
              initial={{ opacity: 0, scale: 0.6, filter: "blur(15px)" }}
              animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
              transition={{ duration: 1.2, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="mt-10"
            >
              <MindRadar axes={mind.axes} color={color} size={400} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* CTA + Description */}
        <AnimatePresence>
          {phase === "ready" && (
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, delay: 0.5 }} className="mt-10 text-center max-w-lg">
              <p className="text-base text-slate-500 mb-3 leading-relaxed font-light">{persona.description}</p>
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 0.3 }} transition={{ delay: 1, duration: 1.5 }} className="text-xs font-display font-light text-slate-600 tracking-[0.2em] uppercase mb-8">
                {t("onboarding.reveal.thisIsYourMind")}
              </motion.p>
              <button
                onClick={onEnter}
                className="group relative px-10 py-4 rounded-full transition-all duration-500 hover:scale-[1.03]"
                style={{ background: `${color}08`, border: `1px solid ${color}20` }}
                onMouseEnter={(e) => { e.currentTarget.style.background = `${color}18`; e.currentTarget.style.boxShadow = `0 0 50px ${color}20`; }}
                onMouseLeave={(e) => { e.currentTarget.style.background = `${color}08`; e.currentTarget.style.boxShadow = "none"; }}
              >
                <span className="text-base font-display font-medium text-slate-200">{t("onboarding.reveal.enterMind")}</span>
                <ArrowRight size={18} className="inline ml-2 text-slate-400 group-hover:translate-x-1 transition-transform" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
