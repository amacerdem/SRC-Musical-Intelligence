import { PageShell } from '../../components/layout/PageShell'

export function PipelineRunner() {
  return (
    <PageShell title="Pipeline Runner" subtitle="Run MI pipeline on audio files \u2014 R\u00b3 \u2192 H\u00b3 \u2192 C\u00b3 \u2192 \u03a8\u00b3">
      <div className="glass-card p-6 mt-4">
        <p className="text-sm text-text-secondary">
          Pipeline runner will allow selecting audio files, configuring pipeline parameters,
          and running the full MI processing chain with progress display.
        </p>
      </div>
    </PageShell>
  )
}
