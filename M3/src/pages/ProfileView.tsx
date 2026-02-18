import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, Headphones, Flame, TrendingUp, Trophy } from "lucide-react";
import { mockUsers } from "@/data/mock-users";
import { getPersona } from "@/data/personas";
import { achievements as allAchievements } from "@/data/levels";
import { useUserStore } from "@/stores/useUserStore";
import { getCompatibilityLabel, beliefColors } from "@/design/tokens";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Avatar } from "@/components/ui/Avatar";
import { LevelBadge } from "@/components/mind/LevelBadge";
import { pageTransition, staggerChildren, slideUp, cinematicReveal } from "@/design/animations";
import { STAGE_NAMES } from "@/types/mind";
import type { MindAxes } from "@/types/mind";

const AXIS_LABELS: { key: keyof MindAxes; label: string; short: string; belief: keyof typeof beliefColors }[] = [
  { key: "entropyTolerance", label: "Entropy", short: "ENT", belief: "consonance" },
  { key: "resolutionCraving", label: "Resolution", short: "RES", belief: "tempo" },
  { key: "monotonyTolerance", label: "Monotony", short: "MON", belief: "familiarity" },
  { key: "salienceSensitivity", label: "Salience", short: "SAL", belief: "salience" },
  { key: "tensionAppetite", label: "Tension", short: "TEN", belief: "reward" },
];

function computeCompatibility(a: MindAxes, b: MindAxes): number {
  const keys: (keyof MindAxes)[] = [
    "entropyTolerance", "resolutionCraving", "monotonyTolerance",
    "salienceSensitivity", "tensionAppetite",
  ];
  const totalDist = keys.reduce((sum, k) => sum + Math.abs(a[k] - b[k]), 0);
  return Math.round(Math.max(0, 100 - (totalDist / keys.length) * 100));
}

export function ProfileView() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const { mind: myMind } = useUserStore();

  const user = mockUsers.find((u) => u.id === userId);

  if (!user) {
    return (
      <motion.div {...pageTransition} className="flex flex-col items-center justify-center h-96 gap-4 bg-black">
        <p className="text-2xl font-display font-bold text-slate-500">Mind not found</p>
        <p className="text-slate-600 font-body font-light">This mind does not exist in our network.</p>
        <Button variant="glass" size="sm" onClick={() => navigate("/friends")}>
          <ArrowLeft size={16} className="mr-2" />
          Back to Social
        </Button>
      </motion.div>
    );
  }

  const persona = getPersona(user.mind.personaId);
  const userAchievements = user.achievements
    .map((aid) => allAchievements.find((a) => a.id === aid))
    .filter(Boolean);

  const compatibility = myMind
    ? computeCompatibility(myMind.axes, user.mind.axes)
    : null;
  const compatLabel = compatibility !== null ? getCompatibilityLabel(compatibility) : null;

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      {/* Full-screen organism background */}
      <div className="absolute inset-0 opacity-15 pointer-events-none">
        <MindOrganismCanvas
          color={persona.color}
          stage={user.mind.stage}
          intensity={0.5}
          breathRate={5}
          className="w-full h-full"
        />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Ambient glow */}
      <div
        className="absolute top-20 left-1/2 -translate-x-1/2 w-[500px] h-[400px] rounded-full blur-[180px] opacity-10 pointer-events-none"
        style={{ backgroundColor: persona.color }}
      />

      {/* Back */}
      <div className="relative z-20 mb-8 pt-4">
        <Button variant="ghost" size="sm" onClick={() => navigate("/friends")}>
          <ArrowLeft size={16} className="mr-2" />
          Back to Social
        </Button>
      </div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        {/* Hero — identity floating over organism */}
        <motion.div variants={cinematicReveal} className="mb-14">
          <div className="flex items-start gap-5 mb-6">
            <Avatar
              src={user.avatarUrl || undefined}
              name={user.displayName}
              size={80}
              borderColor={persona.color}
            />
            <div>
              <h1 className="text-3xl md:text-4xl font-display font-bold text-slate-100 tracking-tight">
                {user.displayName}
              </h1>
              <div className="flex items-center gap-3 mt-2">
                <Badge label={persona.name} color={persona.color} size="md" />
                <Badge label={STAGE_NAMES[user.mind.stage]} color={persona.color} />
              </div>
              <p className="text-sm text-slate-600 mt-3 italic font-body font-light">"{persona.tagline}"</p>
            </div>
          </div>

          {/* Stats — HUD row with belief-colored accents */}
          <div className="flex gap-8 text-sm">
            <StatChip icon={<TrendingUp size={13} />} label="Level" value={`${user.level}`} color={beliefColors.reward.primary} />
            <StatChip icon={<Headphones size={13} />} label="Tracks" value={user.tracksAnalyzed.toLocaleString()} color={beliefColors.consonance.primary} />
            <StatChip icon={<Flame size={13} />} label="Streak" value={`${user.streak}d`} color={beliefColors.tempo.primary} />
            <StatChip icon={<Trophy size={13} />} label="Region" value={user.country} color={beliefColors.salience.primary} />
          </div>
        </motion.div>

        <div className="grid grid-cols-12 gap-8 max-w-6xl">
          {/* Radar — glass panel */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-5 space-y-8">
            <div className="rounded-2xl p-8 flex flex-col items-center"
              style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
            >
              <span className="hud-label mb-6">Mind Profile</span>
              <MindRadar
                axes={user.mind.axes}
                color={persona.color}
                compareAxes={myMind?.axes}
                compareColor={myMind ? beliefColors.consonance.primary : undefined}
                size={300}
              />
              {myMind && (
                <div className="flex items-center gap-8 mt-6 text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: persona.color }} />
                    <span className="text-slate-600 font-body font-light">{user.displayName}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: beliefColors.consonance.primary }} />
                    <span className="text-slate-600 font-body font-light">You</span>
                  </div>
                </div>
              )}
            </div>

            {/* Axis bars — HUD style with belief colors */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-6 block">Axes</span>
              <div className="space-y-4">
                {AXIS_LABELS.map(({ key, label, short, belief }) => {
                  const pct = Math.round(user.mind.axes[key] * 100);
                  const barColor = beliefColors[belief].primary;
                  return (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="hud-label w-8">{short}</span>
                          <span className="text-[11px] text-slate-600 font-body">{label}</span>
                        </div>
                        <span className="hud-value text-xs" style={{ color: barColor }}>{pct}</span>
                      </div>
                      <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: barColor }}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </motion.div>

          {/* Right side */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-7 space-y-8">
            {/* Compatibility — glass panel */}
            {compatibility !== null && compatLabel && (
              <div className="spatial-card p-8 glow-border">
                <span className="hud-label mb-6 block">Compatibility with You</span>
                <div className="flex items-center gap-8">
                  <div className="text-center">
                    <span className="text-5xl font-display font-bold" style={{ color: compatLabel.color }}>
                      {compatibility}%
                    </span>
                    <p className="text-sm mt-2 font-body font-light" style={{ color: compatLabel.color }}>
                      {compatLabel.label}
                    </p>
                  </div>
                  <div className="flex-1 space-y-3">
                    {AXIS_LABELS.map(({ key, label, belief }) => {
                      const diff = Math.abs(user.mind.axes[key] - (myMind?.axes[key] ?? 0));
                      const similarity = Math.round((1 - diff) * 100);
                      const barColor = beliefColors[belief].primary;
                      return (
                        <div key={key} className="flex items-center gap-3 text-xs">
                          <span className="w-16 text-slate-600 font-body font-light">{label}</span>
                          <div className="flex-1 h-[2px] rounded-full bg-white/5 overflow-hidden">
                            <div
                              className="h-full rounded-full transition-all"
                              style={{
                                width: `${similarity}%`,
                                backgroundColor: barColor,
                              }}
                            />
                          </div>
                          <span className="hud-value text-[10px] text-slate-500 w-8 text-right">{similarity}%</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* Level — glass panel */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-5 block">Progression</span>
              <div className="flex items-center gap-5">
                <LevelBadge level={user.level} size="lg" />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-slate-600 font-body font-light">Experience</span>
                    <span className="hud-value text-xs text-slate-500">{user.xp.toLocaleString()} XP</span>
                  </div>
                  <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                    <motion.div
                      className="h-full rounded-full"
                      style={{ backgroundColor: beliefColors.reward.primary }}
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(100, (user.xp / 240000) * 100)}%` }}
                      transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Achievements — glass panel */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-5 block">Achievements</span>
              <div className="grid grid-cols-2 gap-3">
                {userAchievements.map((ach) => {
                  if (!ach) return null;
                  const rarityColor =
                    ach.rarity === "legendary" ? beliefColors.reward.primary :
                    ach.rarity === "epic" ? beliefColors.consonance.primary :
                    ach.rarity === "rare" ? beliefColors.familiarity.primary :
                    "#94A3B8";
                  return (
                    <div
                      key={ach.id}
                      className="p-3 rounded-xl flex items-center gap-3"
                      style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
                    >
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold"
                        style={{
                          background: `${rarityColor}12`,
                          color: rarityColor,
                          border: `1px solid ${rarityColor}20`,
                        }}
                      >
                        {ach.name.charAt(0)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-body font-medium text-slate-300 truncate">{ach.name}</div>
                        <div className="text-[10px] text-slate-600 truncate font-body font-light">{ach.description}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}

function StatChip({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
  return (
    <div className="flex flex-col gap-0.5">
      <div className="flex items-center gap-1.5">
        <span style={{ color }} className="opacity-60">{icon}</span>
        <span className="hud-label">{label}</span>
      </div>
      <span className="hud-value text-sm text-slate-300">{value}</span>
    </div>
  );
}
