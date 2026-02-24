/* ── M3Playlist — Glass panel with track list + now playing bar ──── */

import { motion } from "framer-motion";
import { Music } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useM3AudioStore } from "@/stores/useM3AudioStore";
import { M3PlaylistTrackRow } from "./M3PlaylistTrackRow";
import { M3NowPlayingBar } from "./M3NowPlayingBar";

const ease = [0.22, 1, 0.36, 1] as const;

interface Props {
  accentColor: string;
  onStop: () => void;
}

export function M3Playlist({ accentColor, onStop }: Props) {
  const { t } = useTranslation();
  const playlist = useM3AudioStore((s) => s.playlist);
  const currentTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);

  const handleTrackClick = (idx: number) => {
    const store = useM3AudioStore.getState();
    store.setCurrentTrack(idx);
    store.setIsPlaying(true);
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -40, filter: "blur(16px)" }}
      animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
      exit={{ opacity: 0, x: -40, filter: "blur(16px)" }}
      transition={{ duration: 0.6, ease }}
      className="flex flex-col h-full rounded-2xl backdrop-blur-xl overflow-hidden"
      style={{
        background: "linear-gradient(160deg, rgba(0,0,0,0.4), rgba(0,0,0,0.18))",
        border: "1px solid rgba(255,255,255,0.05)",
        boxShadow: `inset 0 1px 0 rgba(255,255,255,0.03), 0 4px 20px rgba(0,0,0,0.3), 0 0 30px ${accentColor}04`,
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-4 pt-3 pb-2">
        <motion.div
          animate={{ rotate: [0, 8, -8, 0] }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        >
          <Music size={11} style={{ color: accentColor }} />
        </motion.div>
        <span
          className="text-[9px] font-display font-light tracking-[0.25em] uppercase"
          style={{ color: `${accentColor}80` }}
        >
          {t("m3.hub.resonancePlaylist", "Resonance Playlist")}
        </span>
        <span className="text-[8px] font-mono text-slate-700 ml-auto">
          {playlist.length} {t("m3.hub.tracks", "tracks")}
        </span>
      </div>

      {/* Track list — scrollable */}
      <div
        className="flex-1 overflow-y-auto px-1 min-h-0"
        style={{ scrollbarWidth: "none" }}
      >
        {playlist.map((track, i) => (
          <M3PlaylistTrackRow
            key={track.id}
            track={track}
            index={i}
            isActive={i === currentTrackIdx}
            isPlaying={i === currentTrackIdx && isPlaying}
            accentColor={accentColor}
            onClick={() => handleTrackClick(i)}
          />
        ))}
      </div>

      {/* Divider */}
      <div
        className="mx-3 h-px"
        style={{ background: `linear-gradient(90deg, transparent, ${accentColor}15, transparent)` }}
      />

      {/* Now Playing Bar */}
      <M3NowPlayingBar accentColor={accentColor} onStop={onStop} />
    </motion.div>
  );
}
