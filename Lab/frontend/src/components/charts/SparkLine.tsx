import { useRef, useEffect } from 'react'

interface SparkLineProps {
  data: number[]
  width?: number
  height?: number
  color?: string
  className?: string
}

export function SparkLine({
  data,
  width = 80,
  height = 24,
  color = 'rgba(255,255,255,0.5)',
  className = '',
}: SparkLineProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || data.length < 2) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    const min = Math.min(...data)
    const max = Math.max(...data)
    const range = max - min || 1
    const pad = 2

    ctx.beginPath()
    ctx.strokeStyle = color
    ctx.lineWidth = 1.2
    ctx.lineJoin = 'round'
    ctx.lineCap = 'round'

    // Downsample to max width pixels
    const step = Math.max(1, Math.floor(data.length / width))
    for (let i = 0; i < data.length; i += step) {
      const x = (i / (data.length - 1)) * width
      const y = pad + (1 - (data[i] - min) / range) * (height - pad * 2)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Current value dot
    const lastY = pad + (1 - (data[data.length - 1] - min) / range) * (height - pad * 2)
    ctx.beginPath()
    ctx.arc(width, lastY, 2, 0, Math.PI * 2)
    ctx.fillStyle = color
    ctx.fill()
  }, [data, width, height, color])

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      className={`block ${className}`}
      style={{ width, height }}
    />
  )
}
