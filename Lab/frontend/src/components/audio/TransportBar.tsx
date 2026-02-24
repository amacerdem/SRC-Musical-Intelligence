import { useRef, useCallback, useEffect } from 'react'
import { Play, Pause, SkipBack, Upload, X } from 'lucide-react'
import { useAudioStore, useAudioCursor, useAudioSamples } from '../../stores/audioStore'

/**
 * Persistent transport bar — lives at the bottom of AppLayout.
 * Shows waveform, playback controls, frame counter, and file loader.
 * All pages share this single audio source.
 */
export function TransportBar() {
  const { src, fileName, play, pause, seek, unload, loadAudio } = useAudioStore()
  const { currentFrame, totalFrames, currentTime, duration, playing } = useAudioCursor()
  const samples = useAudioSamples()
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const width = container.clientWidth
    const height = 32
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    // Background
    ctx.fillStyle = 'rgba(255,255,255,0.02)'
    ctx.fillRect(0, 0, width, height)

    if (samples && samples.length > 0) {
      const midY = height / 2
      const samplesPerPx = Math.max(1, Math.floor(samples.length / width))
      const cursor = duration > 0 ? currentTime / duration : 0
      const cursorPx = cursor * width

      for (let px = 0; px < width; px++) {
        const start = Math.floor((px / width) * samples.length)
        const end = Math.min(start + samplesPerPx, samples.length)
        let min = 0
        let max = 0
        for (let i = start; i < end; i++) {
          const v = samples[i]
          if (v < min) min = v
          if (v > max) max = v
        }
        const yTop = midY - max * midY * 0.85
        const yBot = midY - min * midY * 0.85

        ctx.beginPath()
        ctx.strokeStyle = px <= cursorPx ? '#3b82f6' : 'rgba(255,255,255,0.18)'
        ctx.globalAlpha = px <= cursorPx ? 0.85 : 0.5
        ctx.lineWidth = 1
        ctx.moveTo(px, yTop)
        ctx.lineTo(px, yBot)
        ctx.stroke()
      }
      ctx.globalAlpha = 1

      // Cursor line
      if (cursorPx > 0) {
        ctx.beginPath()
        ctx.strokeStyle = '#3b82f6'
        ctx.lineWidth = 1.5
        ctx.moveTo(cursorPx, 0)
        ctx.lineTo(cursorPx, height)
        ctx.stroke()
      }
    } else if (!src) {
      ctx.fillStyle = 'rgba(255,255,255,0.06)'
      ctx.font = '10px var(--font-mono)'
      ctx.textAlign = 'center'
      ctx.fillText('load audio file to begin experiment', width / 2, height / 2 + 3)
    }
  }, [samples, currentTime, duration, src])

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(draw)
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  // Also redraw on every frame during playback
  useEffect(() => {
    if (!playing) return
    let raf: number
    const tick = () => {
      draw()
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [playing, draw])

  const handleSeek = (e: React.MouseEvent) => {
    if (!containerRef.current || !src) return
    const rect = containerRef.current.getBoundingClientRect()
    const pos = (e.clientX - rect.left) / rect.width
    seek(pos)
  }

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const url = URL.createObjectURL(file)
    loadAudio(url, file.name)
  }

  return (
    <div className="h-14 border-t border-border-subtle bg-bg-elevated flex items-center gap-3 px-4 shrink-0">
      {/* File input (hidden) */}
      <input
        ref={fileRef}
        type="file"
        accept="audio/*"
        className="hidden"
        onChange={handleFile}
      />

      {/* Controls */}
      <div className="flex items-center gap-1 shrink-0">
        <button
          onClick={() => fileRef.current?.click()}
          className="p-1.5 rounded hover:bg-white/5 text-text-tertiary hover:text-text-secondary transition-colors"
          title="Load audio file"
        >
          <Upload size={14} />
        </button>
        <button
          onClick={() => { if (src) seek(0) }}
          className="p-1.5 rounded hover:bg-white/5 text-text-tertiary hover:text-text-secondary transition-colors"
          title="Restart"
          disabled={!src}
        >
          <SkipBack size={14} />
        </button>
        <button
          onClick={() => { if (playing) pause(); else play() }}
          className="p-2 rounded hover:bg-white/5 text-text-primary transition-colors"
          title={playing ? 'Pause' : 'Play'}
          disabled={!src}
        >
          {playing ? <Pause size={16} /> : <Play size={16} />}
        </button>
      </div>

      {/* Waveform timeline */}
      <div
        ref={containerRef}
        className="flex-1 h-8 rounded cursor-pointer overflow-hidden"
        onClick={handleSeek}
      >
        <canvas
          ref={canvasRef}
          className="block w-full"
          style={{ height: 32 }}
        />
      </div>

      {/* Time + Frame display */}
      <div className="shrink-0 text-right space-y-0.5">
        <div className="mono text-[11px] text-text-secondary">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
        <div className="mono text-[9px] text-text-tertiary">
          F{currentFrame} / {totalFrames}
        </div>
      </div>

      {/* File name + close */}
      {fileName && (
        <div className="flex items-center gap-1.5 shrink-0 max-w-[160px]">
          <span className="mono text-[10px] text-text-tertiary truncate">{fileName}</span>
          <button
            onClick={unload}
            className="p-1 rounded hover:bg-white/5 text-text-tertiary hover:text-text-secondary"
            title="Unload"
          >
            <X size={10} />
          </button>
        </div>
      )}
    </div>
  )
}

function formatTime(s: number): string {
  if (!s || !isFinite(s)) return '0:00.0'
  const m = Math.floor(s / 60)
  const sec = (s % 60).toFixed(1)
  return `${m}:${sec.padStart(4, '0')}`
}
