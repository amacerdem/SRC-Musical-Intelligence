import { useRef, useEffect, useCallback } from 'react'
import type { MidiSegment } from '../../stores/libraryStore'
import { useAudioCursor, useAudioStore } from '../../stores/audioStore'

const CONSONANCE_TYPES: Record<string, string> = {
  P1: '#4ade80', P5: '#4ade80', P4: '#86efac',
  maj: '#60a5fa', min: '#93c5fd', M3: '#60a5fa', m3: '#93c5fd',
  dom7: '#fbbf24', dim: '#f87171', aug: '#fb923c',
  m2: '#ef4444', M7: '#f87171', TT: '#dc2626',
  cluster: '#ef4444',
  rest: '#334155',
}

function getSegmentColor(label: string): string {
  for (const [key, color] of Object.entries(CONSONANCE_TYPES)) {
    if (label.toLowerCase().includes(key.toLowerCase())) return color
  }
  return '#94a3b8'
}

interface MidiTimelineProps {
  segments: MidiSegment[]
  duration: number
  height?: number
}

export function MidiTimeline({ segments, duration, height = 64 }: MidiTimelineProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const drawRef = useRef<() => void>(() => {})
  const { currentTime, playing } = useAudioCursor()
  const seekTo = useAudioStore((s) => s.seek)

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container || duration <= 0) return

    const width = container.clientWidth
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    const pad = { left: 0, right: 0, top: 2, bottom: 18 }
    const plotW = width - pad.left - pad.right
    const barH = height - pad.top - pad.bottom

    const toX = (t: number) => pad.left + (t / duration) * plotW

    // Draw segments as bars
    for (const seg of segments) {
      const x1 = toX(seg.start)
      const x2 = toX(seg.end)
      const w = Math.max(1, x2 - x1 - 1)
      const color = getSegmentColor(seg.label)

      // Bar fill
      ctx.fillStyle = color
      ctx.globalAlpha = 0.15
      ctx.beginPath()
      ctx.roundRect(x1, pad.top, w, barH, 3)
      ctx.fill()

      // Bar border
      ctx.globalAlpha = 0.5
      ctx.strokeStyle = color
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.roundRect(x1, pad.top, w, barH, 3)
      ctx.stroke()
      ctx.globalAlpha = 1

      // Label
      ctx.fillStyle = color
      ctx.font = '10px var(--font-mono)'
      ctx.textAlign = 'center'
      const labelX = x1 + w / 2
      ctx.fillText(seg.label, labelX, pad.top + barH / 2 + 3)
    }

    // Time ticks at bottom
    ctx.fillStyle = 'rgba(255,255,255,0.15)'
    ctx.font = '8px var(--font-mono)'
    ctx.textAlign = 'center'
    const tickInterval = duration <= 10 ? 1 : duration <= 30 ? 2 : 5
    for (let t = 0; t <= duration; t += tickInterval) {
      const x = toX(t)
      ctx.fillText(`${t}s`, x, height - 2)
    }

    // Cursor
    if (currentTime >= 0 && currentTime <= duration) {
      const cx = toX(currentTime)
      ctx.beginPath()
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'
      ctx.lineWidth = 1.5
      ctx.moveTo(cx, pad.top)
      ctx.lineTo(cx, pad.top + barH)
      ctx.stroke()

      // Cursor dot
      ctx.beginPath()
      ctx.arc(cx, pad.top, 3, 0, Math.PI * 2)
      ctx.fillStyle = '#fff'
      ctx.fill()
    }
  }, [segments, duration, height, currentTime])

  drawRef.current = draw

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(() => drawRef.current())
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  // Click to seek
  const handleClick = (e: React.MouseEvent) => {
    const container = containerRef.current
    if (!container || duration <= 0) return
    const rect = container.getBoundingClientRect()
    const frac = (e.clientX - rect.left) / rect.width
    seekTo(Math.max(0, Math.min(1, frac)))
  }

  // Current segment at cursor
  const activeSeg = segments.find(
    (s) => currentTime >= s.start && currentTime < s.end,
  )

  return (
    <div>
      <div
        ref={containerRef}
        className="w-full cursor-pointer"
        onClick={handleClick}
      >
        <canvas
          ref={canvasRef}
          className="block w-full"
          style={{ height }}
        />
      </div>
      {activeSeg && (
        <div className="text-[10px] text-text-tertiary mt-1 mono truncate">
          {activeSeg.detail}
        </div>
      )}
    </div>
  )
}
