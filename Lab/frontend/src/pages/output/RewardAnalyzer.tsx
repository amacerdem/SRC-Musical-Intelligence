import { PageShell } from '../../components/layout/PageShell'

export function RewardAnalyzer() {
  return (
    <PageShell title="Reward Analyzer" subtitle="SRP reward decomposition \u2014 wanting, liking, pleasure, tension-resolution dynamics">
      <div className="glass-card p-6 mt-4">
        <p className="text-sm text-text-secondary">
          Reward analyzer will display the SRP 19D output with P-layer reward signals
          (wanting, liking, pleasure) and global reward formula components
          (surprise, resolution, exploration, monotony).
        </p>
      </div>
    </PageShell>
  )
}
