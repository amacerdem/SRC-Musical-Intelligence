import { useLocation } from 'react-router-dom'
import { PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import { useUiStore } from '../../stores/uiStore'
import { FUNCTIONS } from '../../data/functions'

const ROUTE_LABELS: Record<string, string> = {
  '/': 'Overview',
  '/r3': 'R\u00b3 Features',
  '/h3': 'H\u00b3 Morphology',
  '/reward': 'Reward Analyzer',
  '/ram': 'Region Activation Map',
  '/pipeline': 'Pipeline Runner',
  '/atlas': 'Neuroacoustic Atlas',
}

function getBreadcrumb(pathname: string): string[] {
  const crumbs: string[] = ['MI-Lab']

  if (ROUTE_LABELS[pathname]) {
    crumbs.push(ROUTE_LABELS[pathname])
    return crumbs
  }

  const brainMatch = pathname.match(/^\/brain\/(f\d)$/)
  if (brainMatch) {
    const fn = FUNCTIONS.find(f => f.id === brainMatch[1])
    crumbs.push('Brain')
    crumbs.push(fn ? `F${fn.index} ${fn.name}` : brainMatch[1].toUpperCase())
    return crumbs
  }

  crumbs.push(pathname.slice(1))
  return crumbs
}

export function TopBar() {
  const { sidebarCollapsed, toggleSidebar } = useUiStore()
  const location = useLocation()
  const crumbs = getBreadcrumb(location.pathname)

  return (
    <header className="h-12 shrink-0 flex items-center gap-3 px-4 border-b border-border-subtle bg-bg-elevated/80 backdrop-blur-sm">
      <button
        onClick={toggleSidebar}
        className="p-1.5 rounded-md hover:bg-white/5 text-text-secondary hover:text-text-primary transition-colors"
        aria-label="Toggle sidebar"
      >
        {sidebarCollapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
      </button>

      <nav className="flex items-center gap-1.5 text-sm">
        {crumbs.map((crumb, i) => (
          <span key={i} className="flex items-center gap-1.5">
            {i > 0 && <span className="text-text-tertiary">/</span>}
            <span className={i === crumbs.length - 1 ? 'text-text-primary' : 'text-text-secondary'}>
              {crumb}
            </span>
          </span>
        ))}
      </nav>
    </header>
  )
}
