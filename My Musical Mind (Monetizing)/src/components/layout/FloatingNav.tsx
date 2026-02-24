import { NavLink, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Brain,
  LayoutGrid,
  Radio,
  BookOpen,
  Search,
} from "lucide-react";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useUserStore } from "@/stores/useUserStore";
import { useM3Store } from "@/stores/useM3Store";
import { personas } from "@/data/personas";
import { beliefColors } from "@/design/tokens";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { useDesktop } from "@/hooks/useMediaQuery";
import { LanguageToggle } from "./LanguageToggle";

/* 4 main pages */
const mainNav = [
  { to: "/m3",        icon: Brain,      labelKey: "nav.mind",      belief: "reward" as const },
  { to: "/dashboard", icon: LayoutGrid, labelKey: "nav.home",      belief: "consonance" as const },
  { to: "/live",      icon: Radio,      labelKey: "nav.field",     belief: "tempo" as const },
  { to: "/info",      icon: BookOpen,   labelKey: "nav.info",      belief: "salience" as const },
];

export function FloatingNav() {
  const { t } = useTranslation();
  const location = useLocation();
  const { mind, level } = useUserStore();
  const m3Mind = useM3Store((s) => s.mind);
  const identity = useActiveIdentity();
  const accentColor = identity.color;
  const persona = mind ? personas.find(p => p.id === mind.personaId) : null;
  const [showSearch, setShowSearch] = useState(false);
  const isDesktop = useDesktop();

  const itemHeight = isDesktop ? 44 : 38;
  const iconSize = isDesktop ? 18 : 16;
  const personaLevel = m3Mind?.level ?? 1;

  return (
    <>
      <motion.nav
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
        className="fixed bottom-5 right-6 z-50"
      >
        <div className={`nav-dock flex items-center ${isDesktop ? "px-2.5 py-2 gap-1" : "px-2 py-1.5 gap-0.5"}`}>
          {mainNav.map(({ to, icon: Icon, labelKey, belief }) => {
            const isActive = location.pathname === to || (to === "/info" && location.pathname.startsWith("/info"));
            const navColor = isActive ? accentColor : beliefColors[belief].primary;
            return (
              <NavLink key={to} to={to} className="relative group">
                <div
                  className="flex items-center gap-1.5 rounded-full px-3 transition-all duration-300"
                  style={{
                    height: itemHeight,
                    background: isActive ? `${accentColor}15` : "transparent",
                    border: isActive ? `1px solid ${accentColor}25` : "1px solid transparent",
                    boxShadow: isActive ? `0 0 20px ${accentColor}10, inset 0 0 12px ${accentColor}05` : "none",
                  }}
                >
                  <Icon
                    size={iconSize}
                    className={`transition-all duration-300 ${isActive ? "" : "text-slate-600 group-hover:text-slate-300"}`}
                    style={{
                      color: isActive ? accentColor : undefined,
                      filter: isActive ? `drop-shadow(0 0 6px ${accentColor})` : undefined,
                    }}
                  />
                  <span
                    className={`font-display font-medium transition-all duration-300 ${isDesktop ? "text-[11px]" : "text-[10px]"} ${isActive ? "" : "text-slate-600 group-hover:text-slate-300"}`}
                    style={{
                      color: isActive ? accentColor : undefined,
                      textShadow: isActive ? `0 0 8px ${accentColor}60` : undefined,
                    }}
                  >
                    {t(labelKey)}
                  </span>
                </div>

                {isActive && (
                  <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2">
                    <NucleusDot color={accentColor} size={isDesktop ? 4 : 3} active pulsing />
                  </div>
                )}
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
        <NavLink to="/m3" className="group flex items-center gap-2.5">
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
        <LanguageToggle />

        <button
          onClick={() => setShowSearch(!showSearch)}
          className="w-8 h-8 rounded-full flex items-center justify-center text-slate-700 hover:text-slate-400 transition-colors duration-300"
        >
          <Search size={14} />
        </button>

        {persona && (
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono text-slate-700">L{personaLevel}/12</span>
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
              placeholder={t("nav.search")}
              autoFocus
              onBlur={() => setShowSearch(false)}
              className="w-full px-4 py-2.5 bg-transparent text-sm text-slate-300 placeholder:text-slate-700 outline-none font-body"
            />
          </div>
        </motion.div>
      )}
    </>
  );
}
