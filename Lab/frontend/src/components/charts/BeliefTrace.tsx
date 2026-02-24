import { useRef, useEffect, useCallback, useMemo } from 'react'
import { StatsSummary } from './StatsSummary'

interface BeliefTraceProps {
  /** Time-series trace data for this belief */
  data: number[]
  /** Belief name */
  name: string
  /** Belief type for color coding */
  type: 'core' | 'appraisal' | 'anticipation'
  /** Accent color */
  color?: string
  /** Optional baseline value to draw as reference line */
  baseline?: number | null
  /** Canvas height */
  height?: number
  /** Current playback frame for cursor sync */
  cursorFrame?: number
  /** Total frames for cursor position */
  totalFrames?: number
  className?: string
}

const TYPE_COLORS: Record<string, string> = {
  core: '#10b981',
  appraisal: '#3b82f6',
  anticipation: '#f59e0b',
}

export function BeliefTrace({
  data,
  name,
  type,
  color,
  baseline,
  height = 160,
  cursorFrame,
  totalFrames,
  className = '',
}: BeliefTraceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const traceColor = color ?? TYPE_COLORS[type] ?? '#60a5fa'

  const stats = useMemo(() => {
    if (data.length === 0) return { mean: 0, std: 0, min: 0, max: 0, current: 0 }
    const sum = data.reduce((a, b) => a + b, 0)
    const mean = sum / data.length
    const variance = data.reduce((a, v) => a + (v - mean) ** 2, 0) / data.length
    return {
      mean,
      std: Math.sqrt(variance),
      min: Math.min(...data),
      max: Math.max(...data),
      current: data[data.length - 1],
    }
  }, [data])

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const width = container.clientWidth
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    // Background
    ctx.fillStyle = 'rgba(255,255,255,0.015)'
    ctx.fillRect(0, 0, width, height)

    if (data.length < 2) {
      ctx.fillStyle = 'rgba(255,255,255,0.08)'
      ctx.font = '10px var(--font-mono)'
      ctx.textAlign = 'center'
      ctx.fillText('awaiting experiment data', width / 2, height / 2 + 3)
      return
    }

    const pad = { top: 12, bottom: 8, left: 2, right: 2 }
    const plotW = width - pad.left - pad.right
    const plotH = height - pad.top - pad.bottom
    const yMin = stats.min
    const yMax = stats.max
    const range = yMax - yMin || 1

    const toY = (v: number) => pad.top + (1 - (v - yMin) / range) * plotH
    const toX = (i: number) => pad.left + (i / (data.length - 1)) * plotW

    // Grid lines
    ctx.strokeStyle = 'rgba(255,255,255,0.04)'
    ctx.lineWidth = 0.5
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (i / 4) * plotH
      ctx.beginPath()
      ctx.moveTo(pad.left, y)
      ctx.lineTo(pad.left + plotW, y)
      ctx.stroke()
    }

    // Baseline reference
    if (baseline != null && isFinite(baseline)) {
      const by = toY(baseline)
      ctx.setLineDash([4, 4])
      ctx.strokeStyle = 'rgba(255,255,255,0.15)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(pad.left, by)
      ctx.lineTo(pad.left + plotW, by)
      ctx.stroke()
      ctx.setLineDash([])

      ctx.fillStyle = 'rgba(255,255,255,0.25)'
      ctx.font = '8px var(--font-mono)'
      ctx.textAlign = 'right'
      ctx.fillText(`\u03b2\u2080=${baseline}`, width - 4, by - 3)
    }

    // Mean line
    const meanY = toY(stats.mean)
    ctx.setLineDash([2, 3])
    ctx.strokeStyle = 'rgba(255,255,255,0.1)'
    ctx.lineWidth = 0.5
    ctx.beginPath()
    ctx.moveTo(pad.left, meanY)
    ctx.lineTo(pad.left + plotW, meanY)
    ctx.stroke()
    ctx.setLineDash([])

    // Fill area under curve
    ctx.beginPath()
    ctx.moveTo(toX(0), toY(data[0]))
    for (let i = 1; i < data.length; i++) {
      ctx.lineTo(toX(i), toY(data[i]))
    }
    ctx.lineTo(toX(data.length - 1), pad.top + plotH)
    ctx.lineTo(toX(0), pad.top + plotH)
    ctx.closePath()
    ctx.fillStyle = traceColor
    ctx.globalAlpha = 0.08
    ctx.fill()
    ctx.globalAlpha = 1

    // Main trace
    ctx.beginPath()
    ctx.strokeStyle = traceColor
    ctx.lineWidth = 1.5
    ctx.lineJoin = 'round'
    for (let i = 0; i < data.length; i++) {
      const x = toX(i)
      const y = toY(data[i])
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Endpoint dot
    const lastX = toX(data.length - 1)
    const lastY = toY(data[data.length - 1])
    ctx.beginPath()
    ctx.arc(lastX, lastY, 3, 0, Math.PI * 2)
    ctx.fillStyle = traceColor
    ctx.fill()

    // Name label
    ctx.fillStyle = traceColor
    ctx.globalAlpha = 0.6
    ctx.font = '10px var(--font-mono)'
    ctx.textAlign = 'left'
    ctx.fillText(name, pad.left + 4, pad.top + 10)
    ctx.globalAlpha = 1

    // Y-axis labels
    ctx.fillStyle = 'rgba(255,255,255,0.25)'
    ctx.font = '8px var(--font-mono)'
    ctx.textAlign = 'right'
    ctx.fillText(yMax.toFixed(3), width - 2, pad.top + 8)
    ctx.fillText(yMin.toFixed(3), width - 2, pad.top + plotH)

    // Playback cursor
    if (cursorFrame != null && totalFrames && totalFrames > 0 && data.length > 1) {
      // Map cursorFrame (in audio frames) to data index
      const dataIdx = (cursorFrame / totalFrames) * (data.length - 1)
      const cx = toX(dataIdx)
      ctx.beginPath()
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'
      ctx.lineWidth = 1
      ctx.moveTo(cx, pad.top)
      ctx.lineTo(cx, pad.top + plotH)
      ctx.stroke()

      // Value dot at cursor position
      const idx = Math.min(Math.round(dataIdx), data.length - 1)
      const cy = toY(data[idx])
      ctx.beginPath()
      ctx.arc(cx, cy, 3, 0, Math.PI * 2)
      ctx.fillStyle = traceColor
      ctx.fill()
      ctx.beginPath()
      ctx.arc(cx, cy, 5, 0, Math.PI * 2)
      ctx.strokeStyle = traceColor
      ctx.lineWidth = 1
      ctx.globalAlpha = 0.4
      ctx.stroke()
      ctx.globalAlpha = 1

      // Value label
      ctx.fillStyle = traceColor
      ctx.font = '9px var(--font-mono)'
      ctx.textAlign = cx > width / 2 ? 'right' : 'left'
      ctx.fillText(data[idx].toFixed(4), cx + (cx > width / 2 ? -8 : 8), cy - 6)
    }
  }, [data, height, stats, baseline, traceColor, name, cursorFrame, totalFrames])

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(draw)
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  return (
    <div className={`space-y-2 ${className}`}>
      <div ref={containerRef} className="w-full rounded-lg overflow-hidden">
        <canvas
          ref={canvasRef}
          className="block w-full"
          style={{ height }}
        />
      </div>
      {data.length > 0 && <StatsSummary {...stats} />}
    </div>
  )
}
