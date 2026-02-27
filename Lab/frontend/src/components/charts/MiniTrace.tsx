import { useRef, useEffect, useCallback } from 'react'

const MAX_POINTS = 600
const ROW_HEIGHT = 56

export interface MiniTraceProps {
  traceData: number[]
  label: string
  color: string
  height?: number
  cursorFrame?: number
  totalFrames?: number
}

/** Single-trace canvas for stacked decomposition charts. */
export function MiniTrace({
  traceData,
  label,
  color,
  height = ROW_HEIGHT,
  cursorFrame,
  totalFrames,
}: MiniTraceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const drawRef = useRef<() => void>(() => {})

  // Store cursor in ref so draw callback stays stable during playback
  const cursorRef = useRef({ frame: cursorFrame, total: totalFrames })
  cursorRef.current = { frame: cursorFrame, total: totalFrames }

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

    if (traceData.length < 2) return

    const pad = { top: 4, bottom: 4, left: 60, right: 30 }
    const plotW = width - pad.left - pad.right
    const plotH = height - pad.top - pad.bottom

    // Y range
    let yMin = Infinity
    let yMax = -Infinity
    for (const v of traceData) {
      if (v < yMin) yMin = v
      if (v > yMax) yMax = v
    }
    const range = yMax - yMin || 0.001
    const toY = (v: number) => pad.top + (1 - (v - yMin) / range) * plotH

    // Grid — just one mid line
    ctx.strokeStyle = 'rgba(255,255,255,0.03)'
    ctx.lineWidth = 0.5
    ctx.beginPath()
    ctx.moveTo(pad.left, pad.top + plotH / 2)
    ctx.lineTo(pad.left + plotW, pad.top + plotH / 2)
    ctx.stroke()

    // Downsample
    const step = Math.max(1, Math.floor(traceData.length / MAX_POINTS))
    const indices: number[] = []
    for (let i = 0; i < traceData.length; i += step) indices.push(i)
    if (indices[indices.length - 1] !== traceData.length - 1) indices.push(traceData.length - 1)

    const toX = (arrIdx: number) => {
      const frac = indices[arrIdx] / Math.max(1, traceData.length - 1)
      return pad.left + frac * plotW
    }

    // Fill under curve
    ctx.beginPath()
    ctx.moveTo(toX(0), toY(traceData[indices[0]]))
    for (let i = 1; i < indices.length; i++) {
      ctx.lineTo(toX(i), toY(traceData[indices[i]]))
    }
    ctx.lineTo(toX(indices.length - 1), pad.top + plotH)
    ctx.lineTo(toX(0), pad.top + plotH)
    ctx.closePath()
    ctx.fillStyle = color
    ctx.globalAlpha = 0.06
    ctx.fill()
    ctx.globalAlpha = 1

    // Trace line
    ctx.beginPath()
    ctx.strokeStyle = color
    ctx.lineWidth = 1.2
    ctx.lineJoin = 'round'
    for (let i = 0; i < indices.length; i++) {
      const x = toX(i)
      const y = toY(traceData[indices[i]])
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Label on the left
    ctx.fillStyle = color
    ctx.globalAlpha = 0.9
    ctx.font = '10px var(--font-mono)'
    ctx.textAlign = 'left'
    ctx.fillText(label, 2, height / 2 + 3)
    ctx.globalAlpha = 1

    // Y range labels
    ctx.fillStyle = 'rgba(255,255,255,0.2)'
    ctx.font = '8px var(--font-mono)'
    ctx.textAlign = 'right'
    ctx.fillText(yMax.toFixed(2), width - 2, pad.top + 8)
    ctx.fillText(yMin.toFixed(2), width - 2, pad.top + plotH)

    // Playback cursor — read from ref for stable callback
    const cf = cursorRef.current.frame
    const tf = cursorRef.current.total
    if (cf != null && tf && tf > 0) {
      const dataFrac = cf / tf
      const cx = pad.left + dataFrac * plotW
      ctx.beginPath()
      ctx.strokeStyle = 'rgba(255,255,255,0.5)'
      ctx.lineWidth = 1
      ctx.moveTo(cx, pad.top)
      ctx.lineTo(cx, pad.top + plotH)
      ctx.stroke()

      // Value at cursor
      const idx = Math.min(Math.round(dataFrac * (traceData.length - 1)), traceData.length - 1)
      const cy = toY(traceData[idx])
      ctx.beginPath()
      ctx.arc(cx, cy, 2, 0, Math.PI * 2)
      ctx.fillStyle = color
      ctx.fill()
    }
  }, [traceData, label, color, height])

  drawRef.current = draw

  // Setup observer once per trace data change (stable — no cursor in deps)
  useEffect(() => {
    draw()
    const observer = new ResizeObserver(() => drawRef.current())
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  // Lightweight cursor redraw — no observer teardown
  useEffect(() => {
    drawRef.current()
  }, [cursorFrame])

  return (
    <div ref={containerRef} className="w-full">
      <canvas ref={canvasRef} className="block w-full" style={{ height }} />
    </div>
  )
}
