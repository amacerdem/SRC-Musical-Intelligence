interface Tab {
  key: string
  label: string
  count?: number
}

interface GlassTabsProps {
  tabs: Tab[]
  active: string
  onChange: (key: string) => void
  accent?: string
}

export function GlassTabs({ tabs, active, onChange, accent }: GlassTabsProps) {
  return (
    <div className="glass-tabs">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          className={`glass-tab ${tab.key === active ? 'active' : ''}`}
          onClick={() => onChange(tab.key)}
          style={tab.key === active && accent ? { color: accent } : undefined}
        >
          {tab.label}
          {tab.count !== undefined && (
            <span className="ml-1.5 mono text-text-tertiary text-[11px]">{tab.count}</span>
          )}
        </button>
      ))}
    </div>
  )
}
