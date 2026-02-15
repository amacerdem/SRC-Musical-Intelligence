import { useCallback, useEffect, useRef, useState } from "react";
import { useStore } from "../store";
import { colors, fonts, sizes } from "../theme/tokens";
import { PlaybackEngine } from "../audio/PlaybackEngine";
import { useCanvasResize } from "../hooks/useCanvasResize";
import { drawPlayhead } from "../canvas/colormap";

/** Format seconds as mm:ss */
function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function AudioTransport() {
  const experimentSlug = useStore((s) => s.experimentSlug);
  const isPlaying = useStore((s) => s.isPlaying);
  const currentTime = useStore((s) => s.currentTime);
  const duration = useStore((s) => s.duration);
  const setPlayback = useStore((s) => s.setPlayback);
  const updateTime = useStore((s) => s.updateTime);
  const seek = useStore((s) => s.seek);

  const engineRef = useRef<PlaybackEngine | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const envelopeRef = useRef<Float32Array | null>(null);
  const [volume, setVolume] = useState(0.8);
  const [canvasSize, setCanvasSize] = useState({ w: 0, h: 0 });

  // Initialize engine
  useEffect(() => {
    const engine = new PlaybackEngine((time: number) => {
      updateTime(time);
    });
    engineRef.current = engine;
    return () => engine.dispose();
  }, [updateTime]);

  // Load audio when experiment changes
  useEffect(() => {
    const engine = engineRef.current;
    if (!engine || !experimentSlug) return;
    engine.load(experimentSlug).then(() => {
      envelopeRef.current = engine.getWaveformEnvelope(2000);
    });
  }, [experimentSlug]);

  // Sync play/pause state
  useEffect(() => {
    const engine = engineRef.current;
    if (!engine) return;
    if (isPlaying && !engine.isPlaying) {
      engine.play();
    } else if (!isPlaying && engine.isPlaying) {
      engine.pause();
    }
  }, [isPlaying]);

  // Sync volume
  useEffect(() => {
    engineRef.current?.setVolume(volume);
  }, [volume]);

  // Spacebar shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.code === "Space" && e.target === document.body) {
        e.preventDefault();
        setPlayback(!isPlaying);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isPlaying, setPlayback]);

  // Canvas resize
  const onResize = useCallback((w: number, h: number) => {
    setCanvasSize({ w, h });
  }, []);
  useCanvasResize(canvasRef, onResize);

  // Draw waveform + playhead
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const { w, h } = canvasSize;
    if (w === 0 || h === 0) return;

    const dpr = window.devicePixelRatio || 1;
    ctx.save();
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Clear
    ctx.clearRect(0, 0, w, h);

    // Draw waveform envelope — bin to ~1 bar per 3px for smooth look
    const envelope = envelopeRef.current;
    if (envelope && envelope.length > 0) {
      const targetBars = Math.max(1, Math.round(w / 3));
      const binSize = envelope.length / targetBars;
      const barWidth = w / targetBars;

      ctx.fillStyle = colors.accent;
      ctx.globalAlpha = 0.6;

      for (let i = 0; i < targetBars; i++) {
        const binStart = Math.floor(i * binSize);
        const binEnd = Math.min(envelope.length, Math.floor((i + 1) * binSize));
        let sum = 0;
        for (let j = binStart; j < binEnd; j++) {
          sum += envelope[j]!;
        }
        const avg = sum / (binEnd - binStart);
        const barHeight = Math.min(avg * 3, 1.0) * h;
        const x = i * barWidth;
        const y = (h - barHeight) / 2;
        ctx.fillRect(x, y, Math.max(barWidth - 0.5, 1), barHeight);
      }

      ctx.globalAlpha = 1.0;
    }

    // Draw playhead
    if (duration > 0) {
      const playheadX = (currentTime / duration) * w;
      drawPlayhead(ctx, playheadX, h, colors.playhead);
    }

    ctx.restore();
  }, [canvasSize, currentTime, duration]);

  // Click to seek on canvas
  const handleCanvasClick = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas || duration === 0) return;
      const rect = canvas.getBoundingClientRect();
      const fraction = (e.clientX - rect.left) / rect.width;
      const seekTime = fraction * duration;
      seek(seekTime);
      engineRef.current?.seek(seekTime);
    },
    [duration, seek],
  );

  const togglePlay = useCallback(() => {
    setPlayback(!isPlaying);
  }, [isPlaying, setPlayback]);

  return (
    <div
      style={{
        height: sizes.transportHeight,
        background: colors.bg.panel,
        borderBottom: `1px solid ${colors.border}`,
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "0 16px",
      }}
    >
      {/* Play/Pause button */}
      <button
        onClick={togglePlay}
        style={{
          width: 36,
          height: 36,
          borderRadius: 6,
          border: `1px solid ${colors.border}`,
          background: colors.bg.surface,
          color: colors.text.primary,
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 16,
          flexShrink: 0,
        }}
        title={isPlaying ? "Pause (Space)" : "Play (Space)"}
      >
        {isPlaying ? "\u275A\u275A" : "\u25B6"}
      </button>

      {/* Time display */}
      <div
        style={{
          fontFamily: fonts.data,
          fontSize: 13,
          color: colors.text.primary,
          whiteSpace: "nowrap",
          minWidth: 100,
          textAlign: "center",
          flexShrink: 0,
        }}
      >
        <span>{formatTime(currentTime)}</span>
        <span style={{ color: colors.text.muted, margin: "0 4px" }}>/</span>
        <span style={{ color: colors.text.secondary }}>
          {formatTime(duration)}
        </span>
      </div>

      {/* Waveform canvas */}
      <canvas
        ref={canvasRef}
        onClick={handleCanvasClick}
        style={{
          flex: 1,
          height: sizes.transportHeight - 24,
          borderRadius: 4,
          background: colors.bg.surface,
          cursor: "crosshair",
          display: "block",
        }}
      />

      {/* Volume slider */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontSize: 10,
            color: colors.text.muted,
            textTransform: "uppercase",
          }}
        >
          Vol
        </span>
        <input
          type="range"
          min={0}
          max={1}
          step={0.01}
          value={volume}
          onChange={(e) => setVolume(parseFloat(e.target.value))}
          style={{
            width: 60,
            accentColor: colors.accent,
            cursor: "pointer",
          }}
        />
      </div>
    </div>
  );
}
