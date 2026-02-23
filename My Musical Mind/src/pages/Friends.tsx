import { useMemo, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Radio } from "lucide-react";
import { mockUsers, mockActivity } from "@/data/mock-users";
import { getPersona } from "@/data/personas";
import { getCompatibilityLabel } from "@/design/tokens";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { LevelBadge } from "@/components/mind/LevelBadge";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { beliefColors } from "@/design/tokens";
import { pageTransition, staggerChildren, slideUp, fadeIn } from "@/design/animations";
import { useScrollBatch } from "@/hooks/useScrollTrigger";

/** Stable seeded pseudo-random compatibility per user */
function seededCompatibility(userId: string): number {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = (hash * 31 + userId.charCodeAt(i)) | 0;
  }
  return 40 + Math.abs(hash % 59); // range 40-98
}

const ACTIVITY_ICON_COLOR: Record<string, string> = {
  evolution: "#A855F7",
  creation: "#6366F1",
  compatibility: "#EC4899",
  achievement: "#FBBF24",
  challenge: "#10B981",
  performance: "#EF4444",
  composition: "#A855F7",
  listening: "#38BDF8",
};

export function Friends() {
  const navigate = useNavigate();
  const cardGridRef = useRef<HTMLDivElement>(null);
  const feedRef = useRef<HTMLDivElement>(null);
  useScrollBatch(".scroll-card", cardGridRef, { stagger: 0.06 });
  useScrollBatch(".scroll-feed-item", feedRef, { stagger: 0.06 });

  const usersWithCompat = useMemo(
    () =>
      mockUsers.map((u) => ({
        ...u,
        compatibility: seededCompatibility(u.id),
        persona: getPersona(u.mind.personaId),
      })),
    [],
  );

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Organism background — social/connection energy */}
      <div className="absolute inset-0 z-0 opacity-[0.08] pointer-events-none">
        <MindOrganismCanvas
          color={beliefColors.familiarity.primary}
          secondaryColor={beliefColors.consonance.primary}
          stage={2}
          intensity={0.2}
          breathRate={7}
          variant="ambient"
          constellations
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-14 pt-8">
        <span className="hud-label mb-3 block">Community</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
          Friends
        </h1>
        <p className="hud-label text-xs">See what your friends' minds are creating</p>
      </motion.div>

      {/* User cards — staggered scroll entry */}
      <div
        ref={cardGridRef}
        className="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 mb-16 px-2"
      >
        {usersWithCompat.map((user) => {
          const compatLabel = getCompatibilityLabel(user.compatibility);
          return (
            <div key={user.id} className="scroll-card">
              <div
                className="spatial-card p-6 cursor-pointer group transition-all duration-500"
                onClick={() => navigate(`/friends/${user.id}`)}
                style={{ "--glow-color": user.persona.color } as React.CSSProperties}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.boxShadow = `0 4px 40px ${user.persona.color}12, 0 0 60px ${user.persona.color}06`;
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.boxShadow = "none";
                }}
              >
                <div className="flex items-center gap-3 mb-5">
                  {/* Avatar with MiniOrganism ring */}
                  <div className="relative">
                    <div className="absolute -inset-1 opacity-40 pointer-events-none">
                      <MiniOrganism color={user.persona.color} stage={1} size={56} />
                    </div>
                    <div className="relative z-10">
                      <Avatar
                        src={user.avatarUrl || undefined}
                        name={user.displayName}
                        size={48}
                        borderColor={user.persona.color}
                      />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-body font-semibold text-slate-300 truncate group-hover:text-slate-200 transition-colors">
                      {user.displayName}
                    </h4>
                    <p className="text-xs truncate font-body font-light" style={{ color: user.persona.color }}>
                      {user.persona.name}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <LevelBadge level={user.level} size="sm" />
                  <span className="hud-label">{user.country}</span>
                </div>

                {/* Compatibility — glass panel */}
                <div className="p-4 rounded-xl"
                  style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="hud-label">Compatibility</span>
                    <span className="hud-value text-lg" style={{ color: compatLabel.color }}>
                      {user.compatibility}%
                    </span>
                  </div>
                  <div className="h-[2px] rounded-full bg-white/5 overflow-hidden">
                    <motion.div
                      className="h-full rounded-full"
                      style={{ backgroundColor: compatLabel.color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${user.compatibility}%` }}
                      transition={{ duration: 0.8, ease: "easeOut", delay: 0.2 }}
                    />
                  </div>
                  <span className="text-[10px] mt-1.5 block font-body font-light" style={{ color: compatLabel.color }}>
                    {compatLabel.label}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Activity feed — glass panel with NucleusDot indicators */}
      <div ref={feedRef} className="relative z-10 max-w-3xl xl:max-w-4xl 2xl:max-w-5xl mx-auto px-2">
        <div className="spatial-card p-8">
          <div className="flex items-center gap-2 mb-8">
            <NucleusDot color={beliefColors.salience.primary} size={5} active pulsing />
            <span className="hud-label">Community Feed</span>
          </div>
          <div className="space-y-5">
            {mockActivity.map((item) => {
              const iconColor = ACTIVITY_ICON_COLOR[item.type] || "#94A3B8";
              const timeSince = getTimeSince(item.timestamp);

              return (
                <div key={item.id} className="scroll-feed-item flex items-start gap-3">
                  <div className="mt-1.5 shrink-0">
                    <NucleusDot color={iconColor} size={4} active />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm">
                      <span className="text-slate-300 font-body font-medium">{item.userName}</span>
                      <span className="text-slate-600 ml-1 font-body font-light">{item.message}</span>
                    </p>
                    <span className="text-[10px] text-slate-700 font-mono">{timeSince}</span>
                  </div>
                  <Badge label={item.type} color={iconColor} />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function getTimeSince(isoDate: string): string {
  const diff = Date.now() - new Date(isoDate).getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  if (hours < 1) return "Just now";
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}
