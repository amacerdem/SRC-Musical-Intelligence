import type { ReactNode } from 'react'

interface PageShellProps {
  title: string
  subtitle?: string
  accent?: string
  children?: ReactNode
}

export function PageShell({ title, subtitle, accent, children }: PageShellProps) {
  return (
    <div className="flex flex-col h-full min-h-0">
      <header className="shrink-0 px-8 pt-6 pb-4">
        <h1
          className="text-2xl font-semibold tracking-tight"
          style={accent ? { color: accent } : undefined}
        >
          {title}
        </h1>
        {subtitle && (
          <p className="mt-1 text-sm text-text-secondary">{subtitle}</p>
        )}
      </header>
      <div className="flex-1 overflow-y-auto px-8 pb-8">{children}</div>
    </div>
  )
}
