import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { MiniOrganism } from "./MiniOrganism";
import type { Persona } from "@/types/mind";

interface Props {
  persona: Persona;
  compact?: boolean;
}

export function PersonaCard({ persona, compact = false }: Props) {
  const navigate = useNavigate();
  const { t } = useTranslation();

  if (compact) {
    return (
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="spatial-card cursor-pointer p-4"
        onClick={() => navigate(`/info/${persona.id}`)}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center font-display font-bold text-xs"
            style={{
              background: `${persona.color}10`,
              color: persona.color,
              border: `1px solid ${persona.color}15`,
            }}
          >
            {persona.id}
          </div>
          <div>
            <div className="text-sm font-medium text-slate-300">{t(`personas.${persona.id}.name`)}</div>
            <div className="text-[10px] text-slate-600">{t(`personas.${persona.id}.tagline`)}</div>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      whileHover={{ scale: 1.01, y: -3 }}
      className="group cursor-pointer rounded-2xl p-5 transition-all duration-500"
      style={{
        background: `rgba(14, 14, 22, 0.4)`,
        border: `1px solid rgba(255, 255, 255, 0.03)`,
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = `${persona.color}08`;
        e.currentTarget.style.borderColor = `${persona.color}15`;
        e.currentTarget.style.boxShadow = `0 8px 40px -12px ${persona.color}15`;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = `rgba(14, 14, 22, 0.4)`;
        e.currentTarget.style.borderColor = `rgba(255, 255, 255, 0.03)`;
        e.currentTarget.style.boxShadow = "none";
      }}
      onClick={() => navigate(`/info/${persona.id}`)}
    >
      {/* Header with MiniOrganism badge */}
      <div className="flex items-start justify-between mb-4">
        <div className="relative w-10 h-10 rounded-xl flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 opacity-60 group-hover:opacity-100 transition-opacity duration-500">
            <MiniOrganism color={persona.color} stage={1} size={40} />
          </div>
          <span
            className="relative z-10 font-display font-bold text-sm"
            style={{ color: persona.color }}
          >
            {persona.id}
          </span>
        </div>
        <span className="text-[10px] font-mono text-slate-700">
          {persona.populationPct}%
        </span>
      </div>

      {/* Name */}
      <h3 className="text-base font-display font-bold text-slate-200 mb-1 group-hover:text-white transition-colors">
        {t(`personas.${persona.id}.name`)}
      </h3>
      <p className="text-xs text-slate-600 mb-4 font-light">{t(`personas.${persona.id}.tagline`)}</p>

      {/* Mini axes — thin bars */}
      <div className="space-y-1.5">
        {Object.entries(persona.axes).map(([key, val]) => (
          <div key={key} className="flex items-center gap-2">
            <div className="w-14 text-[9px] text-slate-700 capitalize truncate">
              {t(`axes.${key}`)}
            </div>
            <div className="flex-1 h-[2px] rounded-full bg-white/[0.03] overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{
                  width: `${val * 100}%`,
                  backgroundColor: persona.color,
                  opacity: 0.4,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
