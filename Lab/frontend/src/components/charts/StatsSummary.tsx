interface StatsSummaryProps {
  mean: number
  std: number
  min: number
  max: number
  current?: number
  className?: string
}

function fmt(v: number): string {
  return v.toFixed(3)
}

export function StatsSummary({ mean, std, min, max, current, className = '' }: StatsSummaryProps) {
  return (
    <div className={`flex items-center gap-4 text-[11px] mono text-text-secondary ${className}`}>
      <span>\u03bc: <span className="text-text-primary">{fmt(mean)}</span></span>
      <span>\u03c3: <span className="text-text-primary">{fmt(std)}</span></span>
      <span>min: <span className="text-text-primary">{fmt(min)}</span></span>
      <span>max: <span className="text-text-primary">{fmt(max)}</span></span>
      {current !== undefined && (
        <span>now: <span className="text-text-primary">{fmt(current)}</span></span>
      )}
    </div>
  )
}
