import { NavLink, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Compass,
  LayoutGrid,
  PenTool,
  Radio,
  Trophy,
  Users,
  BookOpen,
  Search,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useUserStore } from "@/stores/useUserStore";
import { personas } from "@/data/personas";
import { beliefColors } from "@/design/tokens";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { useDesktop } from "@/hooks/useMediaQuery";

const mainNav = [
  { to: "/dashboard", icon: LayoutGrid, label: "Home" },
  { to: "/live", icon: Radio, label: "Live" },
  { to: "/compose", icon: PenTool, label: "Compose" },
  { to: "/discover", icon: Compass, label: "Discover" },
];

const secondaryNav = [
  { to: "/friends", icon: Users, label: "Friends" },
  { to: "/leaderboard", icon: Trophy, label: "Ranks" },
  { to: "/info", icon: BookOpen, label: "Info" },
];

export function FloatingNav() {
  const location = useLocation();
  const { mind, level } = useUserStore();
  const persona = mind ? personas.find(p => p.id === mind.personaId) : null;
  const accentColor = persona?.color ?? "#A855F7";
  const [showSearch, setShowSearch] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);
  const isDesktop = useDesktop();

  const itemSize = isDesktop ? 48 : 40;
  const iconSize = isDesktop ? 22 : 18;
  const secondaryIconSize = isDesktop ? 18 : 16;

  useEffect(() => {
    const handleScroll = () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      setScrollProgress(h > 0 ? window.scrollY / h : 0);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <motion.nav
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
        className="fixed bottom-5 left-1/2 -translate-x-1/2 z-50"
      >
        {/* Scroll progress — belief-colored trace */}
        <div className="absolute -top-[2px] left-4 right-4 h-[2px] rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-150"
            style={{
              background: `linear-gradient(90deg, ${beliefColors.consonance.primary}, ${beliefColors.tempo.primary}, ${beliefColors.salience.primary}, ${beliefColors.familiarity.primary}, ${beliefColors.reward.primary})`,
              width: `${scrollProgress * 100}%`,
              opacity: scrollProgress > 0.01 ? 0.7 : 0,
              boxShadow: scrollProgress > 0.01
                ? `0 0 8px ${beliefColors.consonance.primary}40, 0 0 16px ${beliefColors.reward.primary}20`
                : "none",
            }}
          />
        </div>

        <div className={`nav-dock flex items-center ${isDesktop ? "px-3 py-2.5 gap-1.5" : "px-2 py-2 gap-1"}`}>
          {mainNav.map(({ to, icon: Icon, label }) => {
            const isActive = location.pathname === to;
            return (
              <NavLink key={to} to={to} className="relative group" title={label}>
                <div
                  className={`nav-dock-item ${isActive ? "active" : ""}`}
                  style={{
                    width: itemSize,
                    height: itemSize,
                    ...(isActive ? { "--accent-color": accentColor } as React.CSSProperties : {}),
                  }}
                >
                  <Icon
                    size={iconSize}
                    className={`transition-all duration-300 ${isActive ? "text-white" : "text-slate-600 group-hover:text-slate-300"}`}
                    style={isActive ? { filter: `drop-shadow(0 0 6px ${accentColor})` } : undefined}
                  />
                </div>

                {/* NucleusDot active indicator */}
                {isActive && (
                  <div className="absolute -bottom-1 left-1/2 -translate-x-1/2">
                    <NucleusDot color={accentColor} size={isDesktop ? 5 : 4} active pulsing />
                  </div>
                )}

                {/* Hover glow */}
                {!isActive && (
                  <div
                    className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                    style={{
                      background: `radial-gradient(circle, ${accentColor}08 0%, transparent 70%)`,
                    }}
                  />
                )}

                <div className="absolute -top-9 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-300 pointer-events-none translate-y-1 group-hover:translate-y-0">
                  <div className={`px-2.5 py-1 rounded-lg glass-subtle font-display font-medium text-slate-300 whitespace-nowrap ${isDesktop ? "text-xs" : "text-[10px]"}`}>
                    {label}
                  </div>
                </div>
              </NavLink>
            );
          })}

          <div className={`w-px bg-white/[0.04] mx-1 ${isDesktop ? "h-6" : "h-5"}`} />

          {secondaryNav.map(({ to, icon: Icon, label }) => {
            const isActive = location.pathname === to;
            return (
              <NavLink key={to} to={to} className="relative group" title={label}>
                <div
                  className={`nav-dock-item ${isActive ? "active" : ""}`}
                  style={{
                    width: itemSize,
                    height: itemSize,
                    ...(isActive ? { "--accent-color": accentColor } as React.CSSProperties : {}),
                  }}
                >
                  <Icon
                    size={secondaryIconSize}
                    className={`transition-all duration-300 ${isActive ? "text-slate-200" : "text-slate-700 group-hover:text-slate-400"}`}
                  />
                </div>
                {isActive && (
                  <div className="absolute -bottom-1 left-1/2 -translate-x-1/2">
                    <NucleusDot color={accentColor} size={isDesktop ? 4 : 3} active pulsing />
                  </div>
                )}
                <div className="absolute -top-9 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-300 pointer-events-none translate-y-1 group-hover:translate-y-0">
                  <div className={`px-2.5 py-1 rounded-lg glass-subtle font-display font-medium text-slate-300 whitespace-nowrap ${isDesktop ? "text-xs" : "text-[10px]"}`}>
                    {label}
                  </div>
                </div>
              </NavLink>
            );
          })}
        </div>
      </motion.nav>

      {/* Top-left: M³ identity with MiniOrganism */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="fixed top-5 left-6 z-40"
      >
        <NavLink to="/" className="group flex items-center gap-2.5">
          <div className="relative">
            <div className="absolute -inset-1 opacity-60 group-hover:opacity-100 transition-opacity duration-500">
              <MiniOrganism color={accentColor} stage={1} size={32} />
            </div>
            <div
              className="relative z-10 w-7 h-7 rounded-lg flex items-center justify-center text-[10px] font-display font-bold text-white/80 group-hover:text-white transition-all duration-300"
              style={{
                background: `linear-gradient(135deg, ${accentColor}30, ${accentColor}10)`,
                border: `1px solid ${accentColor}15`,
              }}
            >
              M³
            </div>
          </div>
        </NavLink>
      </motion.div>

      {/* Top-right: Level + Search */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="fixed top-5 right-6 z-40 flex items-center gap-3"
      >
        <button
          onClick={() => setShowSearch(!showSearch)}
          className="w-8 h-8 rounded-full flex items-center justify-center text-slate-700 hover:text-slate-400 transition-colors duration-300"
        >
          <Search size={14} />
        </button>

        {persona && (
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono text-slate-700">LV.{level}</span>
            <div className="relative">
              <div
                className="w-6 h-6 rounded-full flex items-center justify-center text-[8px] font-display font-bold"
                style={{ background: `${accentColor}15`, color: accentColor, border: `1px solid ${accentColor}20` }}
              >
                {persona.name.charAt(0)}
              </div>
              <div className="absolute -inset-0.5">
                <NucleusDot color={accentColor} size={3} active className="absolute -top-0.5 -right-0.5" />
              </div>
            </div>
          </div>
        )}
      </motion.div>

      <AnimatePresence>
        {showSearch && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="fixed top-16 right-6 z-50"
          >
            <div className="glass p-1 w-72 lg:w-80">
              <input
                type="text"
                placeholder="Search minds, personas..."
                autoFocus
                onBlur={() => setShowSearch(false)}
                className="w-full px-4 py-2.5 bg-transparent text-sm text-slate-300 placeholder:text-slate-700 outline-none font-body"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
