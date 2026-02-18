import { useCallback, useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useOnboardingStore } from "@/stores/useOnboardingStore";
import { useUserStore } from "@/stores/useUserStore";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { personas } from "@/data/personas";
import { beliefColors } from "@/design/tokens";

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

/* ── Conversational analysis phases ──────────────────────────────── */
const ANALYSIS_PHASES = [
  { text: "Connecting to your music...", belief: null },
  { text: "Interesting... 2,847 tracks. Let me look deeper.", belief: null },
  { text: "Your harmony choices reveal something unusual...", belief: "consonance" as const },
  { text: "I see tension in your playlists. You like the build-up.", belief: "consonance" as const },
  { text: "Your tempo patterns are fascinating. Not what I expected.", belief: "tempo" as const },
  { text: "You notice everything, don't you? High salience.", belief: "salience" as const },
  { text: "The contrasts... you live for the dynamic shifts.", belief: "salience" as const },
  { text: "Repetition doesn't bore you. It deepens.", belief: "familiarity" as const },
  { text: "Your reward geometry is... complex. I like it.", belief: "reward" as const },
  { text: "I know who you are now.", belief: "reward" as const },
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
  const { step, setStep, setPersona, setProgress, analysisProgress, analysisPhase } =
    useOnboardingStore();
  const { completeOnboarding, displayName, setDisplayName } = useUserStore();
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
      setProgress(progress, ANALYSIS_PHASES[phaseIdx].text);

      if (progress >= 100) {
        clearInterval(interval);
        const randomPersona = personas[Math.floor(Math.random() * personas.length)];
        setPersona(randomPersona.id);

        setTimeout(() => {
          completeOnboarding({
            personaId: randomPersona.id,
            axes: randomPersona.axes,
            stage: 1,
            subTrait: null,
          }, name);
          navigate("/reveal");
        }, 800);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [setStep, setProgress, setPersona, completeOnboarding, navigate, setDisplayName]);

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      <div className="cinematic-vignette" />

      <AnimatePresence mode="wait">
        {step === "connect" && (
          <ConnectStep key="connect" userName={userName} onNameChange={setUserName} onConnect={() => startEvolution(userName)} />
        )}
        {step === "evolving" && (
          <EvolvingStep key="evolving" progress={analysisProgress} phase={analysisPhase} userName={userName} />
        )}
      </AnimatePresence>
    </div>
  );
}

function ConnectStep({ userName, onNameChange, onConnect }: { userName: string; onNameChange: (n: string) => void; onConnect: () => void }) {
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
          Welcome
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="text-2xl font-display font-bold text-slate-200 mb-3"
        >
          What should we call you?
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
            placeholder="Your name"
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
          Connect your music
        </motion.p>

        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: canProceed ? 1 : 0 }}
          transition={{ duration: 0.5 }}
          className="text-lg font-display font-medium text-slate-400 mb-8"
        >
          Where does your music live?
        </motion.h2>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: canProceed ? 1 : 0, y: canProceed ? 0 : 20 }}
          transition={{ duration: 0.6 }}
          className="space-y-3"
          style={{ pointerEvents: canProceed ? "auto" : "none" }}
        >
          <ConnectButton logo={<SpotifyLogo />} name="Spotify" sub="Connect your playlists" color="#1DB954" onClick={onConnect} delay={0} />
          <ConnectButton logo={<SoundCloudLogo />} name="SoundCloud" sub="Connect your likes" color="#FF5500" onClick={onConnect} delay={0.1} />
          <ConnectButton logo={<AppleMusicLogo />} name="Apple Music" sub="Connect your library" color="#FC3C44" onClick={onConnect} delay={0.2} />
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

function EvolvingStep({ progress, phase, userName }: { progress: number; phase: string; userName: string }) {
  const hue = 260 + progress * 0.6;
  const color = `hsl(${hue}, 60%, 55%)`;
  const orgStage = progress > 70 ? 2 : 1 as const;
  const orgIntensity = 0.1 + progress * 0.005;

  const typedPhase = useTypewriter(phase, 25);
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
    <div className="h-full flex flex-col items-center justify-center relative">
      <motion.div
        initial={{ scale: 0.2, opacity: 0 }}
        animate={{ scale: 0.5 + progress * 0.005, opacity: 0.3 + progress * 0.005 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0"
      >
        <MindOrganismCanvas color={color} stage={orgStage} intensity={orgIntensity} breathRate={6 - progress * 0.03} className="w-full h-full" interactive={false} />
      </motion.div>

      {/* Orbital trails */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        {uniqueBeliefs.map((belief, i) => {
          const bColor = beliefColors[belief].primary;
          const radius = 100 + i * 35;
          return (
            <motion.div
              key={belief}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 0.4, scale: 1 }}
              transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
              className="absolute rounded-full"
              style={{
                width: radius * 2, height: radius * 2,
                border: `1px solid ${bColor}10`,
                animation: `orbit ${24 + i * 4}s linear infinite`,
              }}
            >
              <div className="absolute w-2 h-2 rounded-full" style={{ top: -4, left: radius - 4, background: bColor, boxShadow: `0 0 12px ${bColor}60` }} />
            </motion.div>
          );
        })}
      </div>

      <div className="relative z-10 text-center max-w-lg mx-auto px-6">
        <motion.h2
          initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 1 }}
          className="text-xl font-display font-bold text-slate-300 mb-8"
        >
          {userName ? `${userName}'s Mind is Forming` : "Your Mind is Forming"}
        </motion.h2>

        {/* Belief indicators */}
        <div className="flex justify-center gap-4 mb-8">
          {(["consonance", "tempo", "salience", "familiarity", "reward"] as const).map((b) => {
            const isActive = uniqueBeliefs.includes(b);
            const bColor = beliefColors[b].primary;
            return (
              <motion.div key={b} initial={{ opacity: 0.1 }} animate={{ opacity: isActive ? 0.8 : 0.1 }} transition={{ duration: 0.5 }} className="flex flex-col items-center gap-1">
                <div className="w-2 h-2 rounded-full transition-all duration-500" style={{ background: bColor, boxShadow: isActive ? `0 0 10px ${bColor}60` : "none" }} />
                <span className="text-[8px] font-mono uppercase tracking-wider" style={{ color: isActive ? `${bColor}80` : "#1E293B" }}>{b.slice(0, 4)}</span>
              </motion.div>
            );
          })}
        </div>

        {/* Phase text — typewriter effect */}
        <div className="h-6 mb-6">
          <p className="text-sm text-slate-400 font-body font-light italic">
            {typedPhase}
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ repeat: Infinity, duration: 0.6 }}
              className="inline-block w-[2px] h-3.5 bg-slate-500 ml-0.5 align-text-bottom"
            />
          </p>
        </div>

        {/* Stats panel — appears during analysis */}
        <AnimatePresence>
          {progress > 10 && (
            <motion.div
              initial={{ opacity: 0, y: 15, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
              className="mb-8 mx-auto max-w-sm"
            >
              <div className="rounded-2xl p-5" style={{ background: "rgba(0,0,0,0.6)", backdropFilter: "blur(16px)", border: "1px solid rgba(255,255,255,0.05)" }}>
                {/* Track & Hours counters */}
                <div className="flex justify-center gap-8 mb-4">
                  <div className="text-center">
                    <div className="text-lg font-mono font-medium text-slate-200">
                      {songCount.toLocaleString()}
                    </div>
                    <div className="text-[9px] uppercase tracking-widest text-slate-600">tracks scanned</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-mono font-medium text-slate-200">
                      {totalHours.toLocaleString()}
                    </div>
                    <div className="text-[9px] uppercase tracking-widest text-slate-600">hours of listening</div>
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
                      className="flex flex-wrap justify-center gap-1.5 mb-3"
                    >
                      {MOCK_STATS.topGenres.map((genre, i) => (
                        <motion.span
                          key={genre}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: i * 0.15, duration: 0.4 }}
                          className="px-2.5 py-1 rounded-full text-[10px] font-mono text-slate-400"
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
                      <span className="text-[9px] uppercase tracking-widest text-slate-700 block mb-1.5">Top Artists</span>
                      <p className="text-xs text-slate-500 font-body font-light">
                        {MOCK_STATS.topArtists.map((artist, i) => (
                          <motion.span
                            key={artist}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: i * 0.2, duration: 0.4 }}
                          >
                            {i > 0 && <span className="text-slate-700 mx-1">&middot;</span>}
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

        {/* Progress bar */}
        <div className="w-64 mx-auto">
          <div className="w-full h-[2px] rounded-full bg-white/[0.04] overflow-hidden">
            <motion.div className="h-full rounded-full" style={{ background: `linear-gradient(90deg, ${color}80, ${color})`, boxShadow: `0 0 20px ${color}30` }} animate={{ width: `${progress}%` }} transition={{ duration: 0.3 }} />
          </div>
          <div className="mt-3 text-[10px] font-mono text-slate-700 tracking-wider">{progress}%</div>
        </div>
      </div>
    </div>
  );
}
