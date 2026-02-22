import { NavLink } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/',          label: 'Dashboard',  icon: '◈' },
  { to: '/atlas',     label: 'Atlas',      icon: '⬡' },
  { to: '/pipeline',  label: 'Pipeline',   icon: '▶' },
  { to: '/r3',        label: 'R³ Explorer', icon: '◉' },
  { to: '/h3',        label: 'H³ Explorer', icon: '◎' },
  { to: '/c3',        label: 'C³ Explorer', icon: '◍' },
  { to: '/reward',    label: 'Reward',      icon: '◆' },
  { to: '/compare',   label: 'Compare',     icon: '⊞' },
  { to: '/docs',      label: 'Docs',        icon: '☰' },
];

export default function Sidebar() {
  return (
    <aside
      className="glass-panel flex flex-col gap-1 p-3"
      style={{ width: 220, minHeight: '100%', borderRadius: '0 16px 16px 0' }}
    >
      {/* Logo */}
      <div className="px-3 py-4 mb-2">
        <h1 className="text-lg font-semibold tracking-tight" style={{ color: 'var(--text-primary)' }}>
          MI-Lab
        </h1>
        <p className="text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
          Musical Intelligence
        </p>
      </div>

      {/* Nav */}
      <nav className="flex flex-col gap-0.5">
        {NAV_ITEMS.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-150 no-underline ${
                isActive
                  ? 'text-white'
                  : 'hover:text-white'
              }`
            }
            style={({ isActive }) => ({
              color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
              background: isActive ? 'rgba(255,255,255,0.06)' : 'transparent',
            })}
          >
            <span className="text-base w-5 text-center">{icon}</span>
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Bottom */}
      <div className="mt-auto px-3 py-3">
        <div className="text-xs font-data" style={{ color: 'var(--text-muted)' }}>
          v0.1.0 · Kernel v4.0
        </div>
      </div>
    </aside>
  );
}
