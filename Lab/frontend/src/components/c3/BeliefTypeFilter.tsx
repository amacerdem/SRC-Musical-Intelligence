import type { BeliefType } from '../../data/beliefs'

interface BeliefTypeFilterProps {
  active: BeliefType | 'all'
  onChange: (type: BeliefType | 'all') => void
  counts: { core: number; appraisal: number; anticipation: number; total: number }
}

const FILTER_OPTIONS: { key: BeliefType | 'all'; label: string; className: string }[] = [
  { key: 'all', label: 'All', className: '' },
  { key: 'core', label: 'Core', className: 'text-core' },
  { key: 'appraisal', label: 'Appraisal', className: 'text-appraisal' },
  { key: 'anticipation', label: 'Anticipation', className: 'text-anticipation' },
]

export function BeliefTypeFilter({ active, onChange, counts }: BeliefTypeFilterProps) {
  const getCount = (key: BeliefType | 'all') =>
    key === 'all' ? counts.total : counts[key]

  return (
    <div className="flex gap-1">
      {FILTER_OPTIONS.map((opt) => (
        <button
          key={opt.key}
          onClick={() => onChange(opt.key)}
          className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
            active === opt.key
              ? 'bg-white/8 text-text-primary'
              : 'text-text-secondary hover:text-text-primary hover:bg-white/4'
          } ${opt.className}`}
        >
          {opt.label}
          <span className="ml-1 mono text-text-tertiary">{getCount(opt.key)}</span>
        </button>
      ))}
    </div>
  )
}
