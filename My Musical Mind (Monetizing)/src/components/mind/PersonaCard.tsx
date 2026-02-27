import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { MiniOrganism } from "./MiniOrganism";
import { CharacterAvatar } from "@/svg/characters";
import type { Persona } from "@/types/mind";
import { getPersonaDimensions } from "@/data/persona-dimensions";
import { DIMENSION_KEYS_6D } from "@/types/dimensions";
import { PSYCHOLOGY_COLORS } from "@/data/dimensions";

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
          <div className="w-10 h-10 flex-shrink-0">
            <CharacterAvatar
              personaId={persona.id}
              color={persona.color}
              family={persona.family}
              size={28}
            />
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
      {/* Character Avatar — centered visual */}
      <div className="flex justify-center mb-3 -mt-1">
        <CharacterAvatar
          personaId={persona.id}
          color={persona.color}
          family={persona.family}
          size={90}
          showAura
        />
      </div>

      {/* Header row — ID badge + population */}
      <div className="flex items-center justify-between mb-2">
        <div
          className="w-6 h-6 rounded-md flex items-center justify-center font-display font-bold text-[10px]"
          style={{
            background: `${persona.color}10`,
            color: persona.color,
            border: `1px solid ${persona.color}15`,
          }}
        >
          {persona.id}
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

      {/* 6D Dimension bars */}
      <div className="space-y-1.5">
        {DIMENSION_KEYS_6D.map((key) => {
          const dimProfile = getPersonaDimensions(persona.id);
          const val = dimProfile[key];
          return (
            <div key={key} className="flex items-center gap-2">
              <div className="w-14 text-[9px] text-slate-700 capitalize truncate">
                {t(`dimensions.6d.${key}`, key)}
              </div>
              <div className="flex-1 h-[2px] rounded-full bg-white/[0.03] overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${val * 100}%`,
                    backgroundColor: PSYCHOLOGY_COLORS[key],
                    opacity: 0.5,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
