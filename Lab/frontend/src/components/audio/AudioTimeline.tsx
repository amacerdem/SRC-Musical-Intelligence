import { useRef, useEffect, useCallback } from 'react'
import { useAudioStore, useAudioCursor, useAudioSamples } from '../../stores/audioStore'

interface AudioTimelineProps {
  /** Accent color for cursor */
  color?: string
  className?: string
}

/**
 * Compact waveform strip (35px) that syncs with global audioStore.
 * Placed per-page (e.g. in FunctionPage) — all instances share the same playback.
 */
export function AudioTimeline({
  color = '#3b82f6',
  className = '',
}: AudioTimelineProps) {
  const samples = useAudioSamples()
  const { currentTime, duration, playing } = useAudioCursor()
  const seek = useAudioStore((s) => s.seek)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const cursor = duration > 0 ? currentTime / duration : 0

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const width = container.clientWidth
    const height = 35
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
      // Draw waveform
      const samplesPerPx = Math.max(1, Math.floor(samples.length / width))
      const midY = height / 2
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
        const yTop = midY - max * midY * 0.9
        const yBot = midY - min * midY * 0.9

        ctx.beginPath()
        ctx.strokeStyle = px <= cursorPx ? color : 'rgba(255,255,255,0.2)'
        ctx.globalAlpha = px <= cursorPx ? 0.8 : 0.4
        ctx.lineWidth = 1
        ctx.moveTo(px, yTop)
        ctx.lineTo(px, yBot)
        ctx.stroke()
      }
      ctx.globalAlpha = 1

      // Cursor line
      if (cursorPx > 0) {
        ctx.beginPath()
        ctx.strokeStyle = color
        ctx.lineWidth = 1.5
        ctx.moveTo(cursorPx, 0)
        ctx.lineTo(cursorPx, height)
        ctx.stroke()

        ctx.beginPath()
        ctx.arc(cursorPx, 3, 3, 0, Math.PI * 2)
        ctx.fillStyle = color
        ctx.fill()
      }

      // Frame counter
      ctx.fillStyle = 'rgba(255,255,255,0.3)'
      ctx.font = '9px var(--font-mono)'
      ctx.textAlign = 'left'
      ctx.fillText(`F${Math.floor(currentTime * 172.27)}`, 4, height - 4)
    } else {
      ctx.fillStyle = 'rgba(255,255,255,0.06)'
      ctx.font = '10px var(--font-mono)'
      ctx.textAlign = 'center'
      ctx.fillText('load audio in transport bar \u2193', width / 2, height / 2 + 3)
    }

    // Duration label
    if (duration > 0) {
      ctx.fillStyle = 'rgba(255,255,255,0.3)'
      ctx.font = '9px var(--font-mono)'
      ctx.textAlign = 'right'
      const mins = Math.floor(duration / 60)
      const secs = (duration % 60).toFixed(1)
      ctx.fillText(`${mins}:${secs.padStart(4, '0')}`, width - 4, height - 4)
    }
  }, [samples, cursor, duration, color, currentTime])

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(draw)
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  // Continuous redraw during playback
  useEffect(() => {
    if (!playing) return
    let raf: number
    const tick = () => { draw(); raf = requestAnimationFrame(tick) }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [playing, draw])

  const handleClick = (e: React.MouseEvent) => {
    if (!containerRef.current || !samples) return
    const rect = containerRef.current.getBoundingClientRect()
    const pos = (e.clientX - rect.left) / rect.width
    seek(Math.max(0, Math.min(1, pos)))
  }

  return (
    <div
      ref={containerRef}
      className={`w-full rounded-lg overflow-hidden cursor-pointer ${className}`}
      onClick={handleClick}
    >
      <canvas
        ref={canvasRef}
        className="block w-full"
        style={{ height: 35 }}
      />
    </div>
  )
}
