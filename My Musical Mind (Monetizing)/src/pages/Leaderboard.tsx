import { useState, useMemo, useRef } from "react";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { Crown, Medal } from "lucide-react";
import { mockUsers } from "@/data/mock-users";
import { getPersona } from "@/data/personas";
import { aeProfile } from "@/data/ae-mind";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Tag } from "@/components/ui/Tag";
import { LevelBadge } from "@/components/mind/LevelBadge";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { pageTransition, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useScrollBatch } from "@/hooks/useScrollTrigger";
import type { UserProfile } from "@/types/social";

type FilterTab = "all" | "weekly" | "persona";

const RANK_DECORATION: Record<number, { color: string; icon: React.ReactNode }> = {
  1: { color: beliefColors.reward.primary, icon: <Crown size={16} /> },
  2: { color: "#C0C0C0", icon: <Medal size={16} /> },
  3: { color: "#CD7F32", icon: <Medal size={16} /> },
};

/** Combine AE + mock users into a full leaderboard */
function buildLeaderboard(filter: FilterTab): (UserProfile & { rank: number })[] {
  const allUsers: UserProfile[] = [aeProfile, ...mockUsers];

  let sorted: UserProfile[];
  if (filter === "weekly") {
    sorted = [...allUsers].sort((a, b) => (b.streak * 100 + b.xp * 0.01) - (a.streak * 100 + a.xp * 0.01));
  } else {
    sorted = [...allUsers].sort((a, b) => b.xp - a.xp);
  }

  return sorted.map((u, i) => ({ ...u, rank: i + 1 }));
}

export function Leaderboard() {
  const { t } = useTranslation();
  const [filter, setFilter] = useState<FilterTab>("all");
  const [personaFilter, setPersonaFilter] = useState<number | null>(null);
  const tableRef = useRef<HTMLDivElement>(null);
  useScrollBatch(".scroll-row", tableRef, { stagger: 0.06 });

  const leaderboard = useMemo(() => {
    const base = buildLeaderboard(filter);
    if (filter === "persona" && personaFilter !== null) {
      return base.filter((u) => u.mind.personaId === personaFilter);
    }
    return base;
  }, [filter, personaFilter]);

  const availablePersonas = useMemo(() => {
    const ids = new Set(mockUsers.map((u) => u.mind.personaId));
    return Array.from(ids).map((id) => getPersona(id)).sort((a, b) => a.id - b.id);
  }, []);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Organism background — reward/achievement energy */}
      <div className="absolute inset-0 z-0 opacity-[0.08] pointer-events-none">
        <MindOrganismCanvas
          color={beliefColors.reward.primary}
          secondaryColor={beliefColors.salience.primary}
          stage={2}
          intensity={0.2}
          breathRate={8}
          variant="ambient"
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-12 pt-8">
        <span className="hud-label mb-3 block">{t("leaderboard.hudLabel")}</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
          {t("leaderboard.title")}
        </h1>
        <p className="hud-label text-xs">{t("leaderboard.subtitle")}</p>
      </motion.div>

      {/* Filter tabs */}
      <div className="relative z-10 flex items-center justify-center gap-2 mb-8 flex-wrap">
        <Tag label={t("leaderboard.allTime")} active={filter === "all"} onClick={() => { setFilter("all"); setPersonaFilter(null); }} />
        <Tag label={t("leaderboard.weekly")} active={filter === "weekly"} onClick={() => { setFilter("weekly"); setPersonaFilter(null); }} />
        <Tag label={t("leaderboard.byPersona")} active={filter === "persona"} onClick={() => setFilter("persona")} />
      </div>

      {/* Persona sub-filter */}
      {filter === "persona" && (
        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="relative z-10 mb-8">
          <div className="flex flex-wrap gap-2 justify-center">
            {availablePersonas.map((p) => (
              <Tag
                key={p.id}
                label={t(`personas.${p.id}.name`)}
                active={personaFilter === p.id}
                onClick={() => setPersonaFilter(personaFilter === p.id ? null : p.id)}
              />
            ))}
          </div>
        </motion.div>
      )}

      {/* Glass panel table */}
      <div ref={tableRef} className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-2">
        <div className="spatial-card overflow-hidden p-0">
          {/* Header row */}
          <div className="grid grid-cols-12 gap-4 px-8 py-4 border-b border-white/5"
            style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)" }}
          >
            <div className="col-span-1">
              <span className="hud-label">{t("leaderboard.rank")}</span>
            </div>
            <div className="col-span-4">
              <span className="hud-label">{t("leaderboard.player")}</span>
            </div>
            <div className="col-span-2">
              <span className="hud-label">{t("leaderboard.persona")}</span>
            </div>
            <div className="col-span-2">
              <span className="hud-label">{t("leaderboard.level")}</span>
            </div>
            <div className="col-span-2 text-right">
              <span className="hud-label">{t("leaderboard.xp")}</span>
            </div>
            <div className="col-span-1 text-right">
              <span className="hud-label">{t("leaderboard.flag")}</span>
            </div>
          </div>

          {/* Rows */}
          {leaderboard.map((user) => {
            const persona = getPersona(user.mind.personaId);
            const decoration = RANK_DECORATION[user.rank];
            const isTopThree = user.rank <= 3;

            return (
              <div
                key={user.id}
                className={`scroll-row grid grid-cols-12 gap-4 px-8 py-5 items-center border-b border-white/[0.03] transition-all duration-300 ${
                  isTopThree ? "" : "hover:bg-white/[0.02]"
                }`}
                style={isTopThree ? {
                  borderLeftWidth: 2,
                  borderLeftColor: `${decoration?.color}40`,
                  background: `linear-gradient(90deg, ${decoration?.color}06, transparent)`,
                } : undefined}
              >
                {/* Rank */}
                <div className="col-span-1">
                  {decoration ? (
                    <div className="flex items-center gap-1.5" style={{ color: decoration.color }}>
                      {decoration.icon}
                      <span className="font-display font-bold text-sm">{user.rank}</span>
                    </div>
                  ) : (
                    <span className="hud-value text-sm text-slate-600">{user.rank}</span>
                  )}
                </div>

                {/* Player — top 3 get MiniOrganism ring */}
                <div className="col-span-4 flex items-center gap-3">
                  <div className="relative">
                    {isTopThree && (
                      <div className="absolute -inset-1 opacity-50 pointer-events-none">
                        <MiniOrganism color={decoration?.color ?? persona.color} stage={1} size={42} />
                      </div>
                    )}
                    <div className="relative z-10">
                      <Avatar
                        src={user.avatarUrl || undefined}
                        name={user.displayName}
                        size={34}
                        borderColor={isTopThree ? decoration?.color : persona.color}
                      />
                    </div>
                  </div>
                  <span className={`font-body font-medium truncate text-sm ${isTopThree ? "text-slate-200" : "text-slate-400"}`}>
                    {user.displayName}
                  </span>
                </div>

                {/* Persona */}
                <div className="col-span-2">
                  <Badge label={t(`personas.${persona.id}.name`)} color={persona.color} />
                </div>

                {/* Level */}
                <div className="col-span-2">
                  <LevelBadge level={user.level} size="sm" />
                </div>

                {/* XP */}
                <div className="col-span-2 text-right">
                  <span className={`hud-value text-sm ${isTopThree ? "text-slate-200" : "text-slate-500"}`}>
                    {user.xp.toLocaleString()}
                  </span>
                </div>

                {/* Country */}
                <div className="col-span-1 text-right">
                  <span className="text-sm">{countryToFlag(user.country)}</span>
                </div>
              </div>
            );
          })}

          {leaderboard.length === 0 && (
            <div className="px-8 py-16 text-center text-slate-600 font-body font-light">
              {t("leaderboard.noMinds")}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

function countryToFlag(code: string): string {
  const codePoints = code
    .toUpperCase()
    .split("")
    .map((char) => 127397 + char.charCodeAt(0));
  return String.fromCodePoint(...codePoints);
}
