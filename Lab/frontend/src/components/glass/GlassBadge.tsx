import type { BeliefType } from '../../data/beliefs'

interface GlassBadgeProps {
  type: BeliefType
  count?: number
  showLabel?: boolean
}

const TYPE_CONFIG = {
  core: { label: 'Core', className: 'badge-core' },
  appraisal: { label: 'Appraisal', className: 'badge-appraisal' },
  anticipation: { label: 'Anticipation', className: 'badge-anticipation' },
} as const

export function GlassBadge({ type, count, showLabel = true }: GlassBadgeProps) {
  const config = TYPE_CONFIG[type]
  return (
    <span className={`glass-badge ${config.className}`}>
      {count !== undefined && <span className="mono">{count}</span>}
      {showLabel && config.label}
    </span>
  )
}
