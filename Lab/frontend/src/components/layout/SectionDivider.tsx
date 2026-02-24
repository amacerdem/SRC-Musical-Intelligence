interface SectionDividerProps {
  label?: string
}

export function SectionDivider({ label }: SectionDividerProps) {
  if (!label) {
    return <div className="h-px bg-border-subtle my-2" />
  }
  return (
    <div className="section-divider my-2">
      <span>{label}</span>
    </div>
  )
}
