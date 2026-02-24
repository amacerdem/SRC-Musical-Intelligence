import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, AudioWaveform, Clock, Brain,
  Award, MapPin, Play, Globe,
} from 'lucide-react'
import { useUiStore } from '../../stores/uiStore'
import { FUNCTIONS } from '../../data/functions'

const NAV_SECTIONS = [
  {
    items: [
      { to: '/', label: 'Overview', icon: LayoutDashboard },
    ],
  },
  {
    title: 'EAR',
    items: [
      { to: '/r3', label: 'R\u00b3 Features', icon: AudioWaveform },
      { to: '/h3', label: 'H\u00b3 Morphology', icon: Clock },
    ],
  },
  {
    title: 'BRAIN',
    items: FUNCTIONS.map((fn) => ({
      to: `/brain/${fn.id}`,
      label: `F${fn.index} ${fn.name}`,
      badge: fn.beliefCounts.total,
      dotColor: fn.color,
    })),
  },
  {
    title: 'OUTPUT',
    items: [
      { to: '/reward', label: 'Reward', icon: Award },
      { to: '/ram', label: 'RAM', icon: MapPin },
    ],
  },
  {
    title: 'TOOLS',
    items: [
      { to: '/pipeline', label: 'Pipeline', icon: Play },
      { to: '/atlas', label: 'Atlas', icon: Globe },
    ],
  },
]

interface NavItemDef {
  to: string
  label: string
  icon?: React.ComponentType<{ size?: number }>
  badge?: number
  dotColor?: string
}

function NavItem({ item, collapsed }: { item: NavItemDef; collapsed: boolean }) {
  const Icon = item.icon ?? Brain

  return (
    <NavLink
      to={item.to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-3 py-1.5 rounded-lg text-[13px] transition-colors ${
          isActive
            ? 'bg-white/8 text-text-primary'
            : 'text-text-secondary hover:text-text-primary hover:bg-white/4'
        }`
      }
    >
      {item.dotColor ? (
        <span
          className="w-2 h-2 rounded-full shrink-0"
          style={{ backgroundColor: item.dotColor }}
        />
      ) : (
        <Icon size={16} />
      )}
      {!collapsed && (
        <>
          <span className="truncate flex-1">{item.label}</span>
          {item.badge !== undefined && (
            <span className="mono text-[11px] text-text-tertiary">{item.badge}</span>
          )}
        </>
      )}
    </NavLink>
  )
}

export function Sidebar() {
  const collapsed = useUiStore((s) => s.sidebarCollapsed)

  return (
    <aside
      className={`shrink-0 h-full flex flex-col border-r border-border-subtle bg-bg-elevated/60 backdrop-blur-sm transition-all duration-200 ${
        collapsed ? 'w-14' : 'w-60'
      }`}
    >
      {/* Header */}
      <div className="px-4 pt-4 pb-2">
        {!collapsed && (
          <>
            <div className="text-sm font-semibold tracking-tight text-text-primary">MI-Lab</div>
            <div className="text-[10px] text-text-tertiary mono">v0.2.0 &middot; Kernel v4.0</div>
          </>
        )}
        {collapsed && (
          <div className="text-xs font-bold text-text-secondary text-center">MI</div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-2 py-1 space-y-4">
        {NAV_SECTIONS.map((section, si) => (
          <div key={si}>
            {section.title && !collapsed && (
              <div className="px-3 py-1 text-[10px] font-semibold tracking-widest uppercase text-text-tertiary">
                {section.title}
              </div>
            )}
            {section.title && collapsed && (
              <div className="h-px bg-border-subtle mx-2 my-1" />
            )}
            <div className="space-y-0.5">
              {section.items.map((item) => (
                <NavItem key={item.to} item={item} collapsed={collapsed} />
              ))}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  )
}
