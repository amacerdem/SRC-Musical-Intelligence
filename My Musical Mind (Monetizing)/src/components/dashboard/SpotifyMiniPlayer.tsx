/* ── SpotifyMiniPlayer — Compact floating now-playing card ────────────
 *  Shows current track with album art, Spotify branding, animated
 *  equalizer bars. Designed for the Dashboard top-right corner.
 *  ──────────────────────────────────────────────────────────────────── */

import { motion } from "framer-motion";
import type { MockTrack } from "@/services/SpotifySimulator";

const SPOTIFY_GREEN = "#1DB954";

interface Props {
  track: MockTrack;
  isDemo?: boolean;
  accentColor?: string;
}

export function SpotifyMiniPlayer({ track, isDemo }: Props) {
  return (
    <div
      className="flex items-center gap-3 pl-2.5 pr-3.5 py-2.5 rounded-2xl max-w-[300px]"
      style={{
        background: "rgba(0, 0, 0, 0.6)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        border: "1px solid rgba(255,255,255,0.07)",
        boxShadow: `0 8px 32px rgba(0,0,0,0.4), 0 0 40px ${SPOTIFY_GREEN}06`,
      }}
    >
      {/* Album art */}
      {track.albumArt ? (
        <motion.img
          src={track.albumArt}
          alt=""
          className="w-10 h-10 rounded-lg object-cover shrink-0"
          animate={{
            boxShadow: [
              `0 0 8px ${SPOTIFY_GREEN}15`,
              `0 0 16px ${SPOTIFY_GREEN}25`,
              `0 0 8px ${SPOTIFY_GREEN}15`,
            ],
          }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        />
      ) : (
        <div
          className="w-10 h-10 rounded-lg shrink-0 flex items-center justify-center"
          style={{ background: `${SPOTIFY_GREEN}15` }}
        >
          <SpotifyLogo size={20} />
        </div>
      )}

      {/* Track info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-1.5 mb-0.5">
          {/* Equalizer bars */}
          <div className="flex gap-[2px] items-end">
            {[0, 1, 2, 3].map((i) => (
              <motion.div
                key={i}
                className="w-[2.5px] rounded-full"
                style={{ backgroundColor: SPOTIFY_GREEN, originY: 1 }}
                animate={{ scaleY: [0.3, 1, 0.3] }}
                transition={{
                  duration: 0.6 + i * 0.1,
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: i * 0.15,
                }}
              >
                <div className="h-2.5" />
              </motion.div>
            ))}
          </div>
          <span
            className="text-[8px] uppercase tracking-[0.15em] font-display font-medium"
            style={{ color: SPOTIFY_GREEN }}
          >
            Now Playing
          </span>
          {isDemo && (
            <span className="text-[7px] uppercase tracking-[0.1em] font-mono px-1.5 py-0.5 rounded-full bg-white/[0.06] text-slate-500">
              Demo
            </span>
          )}
        </div>
        <p className="text-[12px] font-display font-medium text-white/90 truncate leading-tight">
          {track.name}
        </p>
        <p className="text-[10px] font-mono text-slate-500 truncate leading-tight">
          {track.artist}
        </p>
      </div>

      {/* Spotify logo */}
      <div className="shrink-0 opacity-60">
        <SpotifyLogo size={18} />
      </div>
    </div>
  );
}

/* ── Inline Spotify SVG Logo ─────────────────────────────────────── */

function SpotifyLogo({ size = 20 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill={SPOTIFY_GREEN}
    >
      <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
    </svg>
  );
}
