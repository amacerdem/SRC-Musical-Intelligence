/* ── M3PlaylistTrackRow — Individual track in the playlist ─────────── */

import { motion } from "framer-motion";
import type { LibraryTrack } from "@/data/track-library";
import { GENE_COLORS } from "@/types/m3";

const ease = [0.22, 1, 0.36, 1] as const;

const FAMILY_TO_GENE: Record<string, keyof typeof GENE_COLORS> = {
  Alchemists: "tension",
  Architects: "resolution",
  Explorers: "entropy",
  Anchors: "resonance",
  Kineticists: "plasticity",
};

function formatDuration(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

interface Props {
  track: LibraryTrack;
  index: number;
  isActive: boolean;
  isPlaying: boolean;
  accentColor: string;
  onClick: () => void;
}

export function M3PlaylistTrackRow({ track, index, isActive, isPlaying, accentColor, onClick }: Props) {
  const geneKey = FAMILY_TO_GENE[track.dominantFamily] ?? "tension";
  const dotColor = GENE_COLORS[geneKey];

  return (
    <motion.button
      onClick={onClick}
      initial={{ opacity: 0, x: -16 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4, delay: index * 0.04, ease }}
      className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-left transition-all duration-300 group"
      style={{
        background: isActive ? `${accentColor}0A` : "transparent",
        border: isActive ? `1px solid ${accentColor}18` : "1px solid transparent",
      }}
    >
      {/* Track number / equalizer */}
      <div className="w-5 h-5 flex items-center justify-center shrink-0">
        {isActive && isPlaying ? (
          <div className="flex items-end gap-[1.5px] h-3">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-[2px] rounded-full origin-bottom"
                style={{
                  background: accentColor,
                  animation: "eq 0.8s ease-in-out infinite",
                  animationDelay: `${i * 0.15}s`,
                  height: "100%",
                }}
              />
            ))}
          </div>
        ) : (
          <span
            className="text-[10px] font-mono tabular-nums"
            style={{ color: isActive ? accentColor : "#475569" }}
          >
            {index + 1}
          </span>
        )}
      </div>

      {/* Family dot */}
      <div
        className="w-1.5 h-1.5 rounded-full shrink-0"
        style={{
          background: dotColor,
          boxShadow: isActive ? `0 0 6px ${dotColor}60` : "none",
        }}
      />

      {/* Track info */}
      <div className="flex-1 min-w-0">
        <p
          className="text-[11px] font-display font-medium truncate transition-colors"
          style={{ color: isActive ? accentColor : "#CBD5E1" }}
        >
          {track.name}
        </p>
        <p className="text-[9px] font-mono text-slate-600 truncate">
          {track.artist}
        </p>
      </div>

      {/* Genre tag */}
      <span
        className="text-[7px] font-display tracking-wider uppercase px-1.5 py-0.5 rounded-full shrink-0 hidden sm:block"
        style={{
          color: `${dotColor}90`,
          background: `${dotColor}0A`,
          border: `1px solid ${dotColor}12`,
        }}
      >
        {track.genre}
      </span>

      {/* Duration */}
      <span className="text-[9px] font-mono text-slate-600 tabular-nums shrink-0 w-8 text-right">
        {formatDuration(track.durationSec)}
      </span>
    </motion.button>
  );
}
