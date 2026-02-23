import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Brain,
  Compass,
  Gamepad2,
  LayoutDashboard,
  Music,
  Headphones,
  Trophy,
  Users,
  Sparkles,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { ProgressBar } from "@/components/ui/ProgressBar";

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/explorer", icon: Brain, label: "Mind Explorer" },
  { to: "/personas", icon: Sparkles, label: "Personas" },
  { to: "/social", icon: Users, label: "Social" },
  { to: "/arena", icon: Gamepad2, label: "Arena" },
  { to: "/leaderboard", icon: Trophy, label: "Leaderboard" },
  { to: "/create", icon: Music, label: "Create Studio" },
  { to: "/listen", icon: Headphones, label: "Listen Lab" },
];

export function Sidebar() {
  const { level, xp, displayName } = useUserStore();

  /* XP progress within current level */
  const xpForLevel = level * 200;
  const prevLevelXP = ((level - 1) * level) / 2 * 200;  // simplified
  const xpInLevel = xp - prevLevelXP;
  const pct = Math.min(100, (xpInLevel / xpForLevel) * 100);

  return (
    <aside className="w-64 h-screen sticky top-0 flex flex-col border-r border-m3-border bg-m3-surface/50 backdrop-blur-sm">
      {/* Logo */}
      <NavLink to="/" className="px-6 py-5 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-accent-gradient flex items-center justify-center">
          <span className="text-white font-display font-bold text-sm">M³</span>
        </div>
        <span className="font-display font-bold text-lg text-slate-100">
          My Musical Mind
        </span>
      </NavLink>

      {/* Level card */}
      <div className="mx-4 mb-4 p-3 glass rounded-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-400">Level {level}</span>
          <span className="text-xs font-mono text-purple-400">{xp} XP</span>
        </div>
        <ProgressBar value={pct} color="#A855F7" height={4} />
      </div>

      {/* Nav items */}
      <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-m3-accent-purple/15 text-purple-300"
                  : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Explore AE */}
      <div className="p-4 border-t border-m3-border">
        <NavLink
          to="/explore-ae"
          className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-white/5 transition-all"
        >
          <Compass size={18} />
          Amac Erdem's Mind
        </NavLink>
      </div>
    </aside>
  );
}
