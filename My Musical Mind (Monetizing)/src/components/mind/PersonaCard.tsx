import { useMemo } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { PersonaAvatar } from "@/components/mind/PersonaAvatar";
import type { Persona } from "@/types/mind";
import { getPersonaDimensions } from "@/data/persona-dimensions";
import { DIMENSION_KEYS_6D } from "@/types/dimensions";
import { ALL_PSYCHOLOGY } from "@/data/dimensions";

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
            <PersonaAvatar
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
      {/* Character Avatar */}
      <div className="flex justify-center mb-3 -mt-1">
        <PersonaAvatar
          personaId={persona.id}
          color={persona.color}
          family={persona.family}
          size={90}
          showAura
        />
      </div>

      {/* Header row */}
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
      <p className="text-xs text-slate-600 mb-3 font-light">{t(`personas.${persona.id}.tagline`)}</p>

      {/* 6D Mini Radar */}
      <div className="flex justify-center">
        <MiniRadar personaId={persona.id} color={persona.color} size={140} />
      </div>
    </motion.div>
  );
}

/* ── MiniRadar — Compact 6D hexagonal radar for persona cards ──────── */

const MINI_ANGLES = Array.from(
  { length: 6 },
  (_, i) => (-90 + i * 60) * (Math.PI / 180),
);

function MiniRadar({ personaId, color, size }: { personaId: number; color: string; size: number }) {
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.36;
  const labelR = maxR + 14;

  const profile = getPersonaDimensions(personaId);
  const vals = DIMENSION_KEYS_6D.map((k) => profile[k]);

  const pts = useMemo(
    () =>
      MINI_ANGLES.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, vals[i]));
        return `${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r}`;
      }),
    [vals, cx, cy, maxR],
  );

  const gridPath = (scale: number) => {
    const gp = MINI_ANGLES.map(
      (a) => `${cx + Math.cos(a) * maxR * scale} ${cy + Math.sin(a) * maxR * scale}`,
    );
    return `M ${gp.join(" L ")} Z`;
  };

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="overflow-visible">
      {/* Grid */}
      {[0.33, 0.66, 1].map((s) => (
        <path key={s} d={gridPath(s)} fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth={0.5} />
      ))}
      {/* Axes */}
      {MINI_ANGLES.map((a, i) => (
        <line key={i} x1={cx} y1={cy} x2={cx + Math.cos(a) * maxR} y2={cy + Math.sin(a) * maxR}
          stroke="rgba(255,255,255,0.04)" strokeWidth={0.5} />
      ))}
      {/* Filled polygon */}
      <path d={`M ${pts.join(" L ")} Z`} fill={`${color}18`} stroke={color} strokeWidth={1.2}
        strokeLinejoin="round" opacity={0.9} />
      {/* Dots */}
      {MINI_ANGLES.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, vals[i]));
        return (
          <circle key={i} cx={cx + Math.cos(a) * r} cy={cy + Math.sin(a) * r}
            r={2} fill={color} stroke="#0a0a0f" strokeWidth={0.6} />
        );
      })}
      {/* Labels */}
      {ALL_PSYCHOLOGY.map((dim, i) => {
        const x = cx + Math.cos(MINI_ANGLES[i]) * labelR;
        const y = cy + Math.sin(MINI_ANGLES[i]) * labelR;
        return (
          <text key={dim.key} x={x} y={y} textAnchor="middle" dominantBaseline="middle"
            fill={dim.color} fontSize={7} fontWeight="500" fontFamily="Inter"
            style={{ pointerEvents: "none" }}>
            {dim.name}
          </text>
        );
      })}
    </svg>
  );
}
