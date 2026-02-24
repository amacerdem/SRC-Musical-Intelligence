import { useRef, useEffect, useCallback } from 'react'

interface WaveformProps {
  /** Mono PCM samples, normalized -1..1 */
  samples: Float32Array | null
  /** Current position 0..1 */
  cursor?: number
  /** Accent color for played portion */
  color?: string
  height?: number
  className?: string
}

export function Waveform({
  samples,
  cursor = 0,
  color = '#3b82f6',
  height = 80,
  className = '',
}: WaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

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

    if (!samples || samples.length === 0) {
      ctx.fillStyle = 'rgba(255,255,255,0.04)'
      ctx.fillRect(0, 0, width, height)
      return
    }

    const midY = height / 2
    const samplesPerPx = Math.max(1, Math.floor(samples.length / width))
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
      ctx.strokeStyle = px <= cursorPx ? color : 'rgba(255,255,255,0.2)'
      ctx.globalAlpha = px <= cursorPx ? 0.8 : 0.5
      ctx.lineWidth = 1
      ctx.moveTo(px, yTop)
      ctx.lineTo(px, yBot)
      ctx.stroke()
    }

    ctx.globalAlpha = 1

    // Center line
    ctx.beginPath()
    ctx.strokeStyle = 'rgba(255,255,255,0.06)'
    ctx.lineWidth = 0.5
    ctx.moveTo(0, midY)
    ctx.lineTo(width, midY)
    ctx.stroke()
  }, [samples, cursor, color, height])

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(draw)
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

  return (
    <div ref={containerRef} className={`w-full ${className}`}>
      <canvas
        ref={canvasRef}
        className="block w-full"
        style={{ height }}
      />
    </div>
  )
}
