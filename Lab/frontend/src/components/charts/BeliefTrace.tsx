import { useRef, useEffect, useMemo } from 'react'
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

/** Max display points for overview — prevents overdraw */
const MAX_POINTS = 600

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

  // Zoom state (refs to avoid re-binding event listeners)
  const zoomRef = useRef({ start: 0, end: 1 })
  const panRef = useRef({ active: false, startX: 0, startZoom: { start: 0, end: 1 } })
  const drawRef = useRef<() => void>(() => {})

  // Store cursor in ref so draw doesn't need it as a dep
  const cursorRef = useRef({ frame: cursorFrame, total: totalFrames })
  cursorRef.current = { frame: cursorFrame, total: totalFrames }

  // Reset zoom when data changes
  useEffect(() => {
    zoomRef.current = { start: 0, end: 1 }
  }, [data.length])

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

  // Draw function — reads zoom from ref
  const draw = () => {
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

    const { start: zs, end: ze } = zoomRef.current
    const startIdx = Math.floor(zs * (data.length - 1))
    const endIdx = Math.ceil(ze * (data.length - 1))
    const viewLen = endIdx - startIdx + 1

    const pad = { top: 12, bottom: 8, left: 2, right: 2 }
    const plotW = width - pad.left - pad.right
    const plotH = height - pad.top - pad.bottom

    // Y range on visible data
    let yMin = Infinity
    let yMax = -Infinity
    for (let i = startIdx; i <= endIdx; i++) {
      if (data[i] < yMin) yMin = data[i]
      if (data[i] > yMax) yMax = data[i]
    }
    const range = yMax - yMin || 1

    const toY = (v: number) => pad.top + (1 - (v - yMin) / range) * plotH

    // Downsample visible range
    const step = Math.max(1, Math.floor(viewLen / MAX_POINTS))
    const indices: number[] = []
    for (let i = startIdx; i <= endIdx; i += step) {
      indices.push(i)
    }
    if (indices[indices.length - 1] !== endIdx) indices.push(endIdx)

    const toX = (arrIdx: number) => {
      const frac = (indices[arrIdx] - startIdx) / Math.max(1, endIdx - startIdx)
      return pad.left + frac * plotW
    }

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
    ctx.moveTo(toX(0), toY(data[indices[0]]))
    for (let i = 1; i < indices.length; i++) {
      ctx.lineTo(toX(i), toY(data[indices[i]]))
    }
    ctx.lineTo(toX(indices.length - 1), pad.top + plotH)
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
    for (let i = 0; i < indices.length; i++) {
      const x = toX(i)
      const y = toY(data[indices[i]])
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Endpoint dot
    const lastX = toX(indices.length - 1)
    const lastY = toY(data[indices[indices.length - 1]])
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

    // Playback cursor — read from ref for stable draw fn
    const cf = cursorRef.current.frame
    const tf = cursorRef.current.total
    if (cf != null && tf && tf > 0 && data.length > 1) {
      const dataFrac = cf / tf
      if (dataFrac >= zs && dataFrac <= ze) {
        const cx = pad.left + ((dataFrac - zs) / (ze - zs)) * plotW
        ctx.beginPath()
        ctx.strokeStyle = 'rgba(255,255,255,0.7)'
        ctx.lineWidth = 1
        ctx.moveTo(cx, pad.top)
        ctx.lineTo(cx, pad.top + plotH)
        ctx.stroke()

        const idx = Math.min(Math.round(dataFrac * (data.length - 1)), data.length - 1)
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

        ctx.fillStyle = traceColor
        ctx.font = '9px var(--font-mono)'
        ctx.textAlign = cx > width / 2 ? 'right' : 'left'
        ctx.fillText(data[idx].toFixed(4), cx + (cx > width / 2 ? -8 : 8), cy - 6)
      }
    }

    // Zoom indicator bar
    if (ze - zs < 0.99) {
      const barY = height - 3
      ctx.fillStyle = 'rgba(255,255,255,0.06)'
      ctx.fillRect(pad.left, barY, plotW, 2)
      ctx.fillStyle = traceColor
      ctx.globalAlpha = 0.4
      ctx.fillRect(pad.left + zs * plotW, barY, (ze - zs) * plotW, 2)
      ctx.globalAlpha = 1
    }
  }

  // Keep drawRef current
  drawRef.current = draw

  // Initial draw + resize observer (stable — no cursor in deps)
  useEffect(() => {
    draw()
    const observer = new ResizeObserver(() => drawRef.current())
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [data, height, stats, baseline, traceColor, name])

  // Lightweight cursor redraw — no observer teardown
  useEffect(() => {
    drawRef.current()
  }, [cursorFrame])

  // Wheel zoom
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault()
      if (data.length < 2) return

      const rect = canvas.getBoundingClientRect()
      const mouseXFrac = (e.clientX - rect.left) / rect.width
      const { start: zs, end: ze } = zoomRef.current
      const currentRange = ze - zs
      const factor = e.deltaY > 0 ? 1.3 : 0.7
      let newRange = Math.min(1, Math.max(0.005, currentRange * factor))

      if (newRange >= 0.99) {
        zoomRef.current = { start: 0, end: 1 }
        drawRef.current()
        return
      }

      const center = zs + mouseXFrac * currentRange
      let ns = center - mouseXFrac * newRange
      let ne = ns + newRange
      if (ns < 0) { ne -= ns; ns = 0 }
      if (ne > 1) { ns -= (ne - 1); ne = 1 }

      zoomRef.current = { start: Math.max(0, ns), end: Math.min(1, ne) }
      drawRef.current()
    }

    canvas.addEventListener('wheel', handleWheel, { passive: false })
    return () => canvas.removeEventListener('wheel', handleWheel)
  }, [data.length])

  // Drag to pan
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleDown = (e: MouseEvent) => {
      const z = zoomRef.current
      if (z.end - z.start >= 0.99) return
      panRef.current = { active: true, startX: e.clientX, startZoom: { ...z } }
      canvas.style.cursor = 'grabbing'
    }

    const handleMove = (e: MouseEvent) => {
      if (!panRef.current.active) return
      const rect = canvas.getBoundingClientRect()
      const dx = (e.clientX - panRef.current.startX) / rect.width
      const { start: ps, end: pe } = panRef.current.startZoom
      const range = pe - ps
      let ns = ps - dx * range
      let ne = ns + range
      if (ns < 0) { ne -= ns; ns = 0 }
      if (ne > 1) { ns -= (ne - 1); ne = 1 }
      zoomRef.current = { start: Math.max(0, ns), end: Math.min(1, ne) }
      drawRef.current()
    }

    const handleUp = () => {
      if (panRef.current.active) {
        panRef.current.active = false
        canvas.style.cursor = ''
      }
    }

    canvas.addEventListener('mousedown', handleDown)
    window.addEventListener('mousemove', handleMove)
    window.addEventListener('mouseup', handleUp)
    return () => {
      canvas.removeEventListener('mousedown', handleDown)
      window.removeEventListener('mousemove', handleMove)
      window.removeEventListener('mouseup', handleUp)
    }
  }, [])

  // Double-click to reset zoom
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const handleDbl = () => {
      zoomRef.current = { start: 0, end: 1 }
      drawRef.current()
    }
    canvas.addEventListener('dblclick', handleDbl)
    return () => canvas.removeEventListener('dblclick', handleDbl)
  }, [])

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
