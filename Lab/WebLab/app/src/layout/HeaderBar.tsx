import { useStore } from "../store";
import { colors, fonts, sizes } from "../theme/tokens";

export function HeaderBar() {
  const experimentList = useStore((s) => s.experimentList);
  const experimentSlug = useStore((s) => s.experimentSlug);
  const experiment = useStore((s) => s.experiment);
  const loadExperiment = useStore((s) => s.loadExperiment);

  return (
    <div
      style={{
        height: sizes.headerHeight,
        background: colors.bg.panel,
        borderBottom: `1px solid ${colors.border}`,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 16px",
        fontFamily: fonts.ui,
      }}
    >
      {/* Left: Title */}
      <div
        style={{
          fontSize: 15,
          fontWeight: 700,
          color: colors.accent,
          letterSpacing: "0.02em",
          whiteSpace: "nowrap",
        }}
      >
        MI WebLab
      </div>

      {/* Center: Experiment dropdown */}
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <label
          style={{
            fontSize: 11,
            color: colors.text.secondary,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            fontWeight: 600,
          }}
        >
          Experiment
        </label>
        <select
          value={experimentSlug ?? ""}
          onChange={(e) => {
            const slug = e.target.value;
            if (slug) loadExperiment(slug);
          }}
          style={{
            background: colors.bg.surface,
            color: colors.text.primary,
            border: `1px solid ${colors.border}`,
            borderRadius: 4,
            padding: "4px 8px",
            fontSize: 12,
            fontFamily: fonts.data,
            outline: "none",
            cursor: "pointer",
            minWidth: 180,
          }}
        >
          <option value="" disabled>
            Select experiment...
          </option>
          {experimentList.map((slug) => (
            <option key={slug} value={slug}>
              {slug}
            </option>
          ))}
        </select>
      </div>

      {/* Right: Experiment info */}
      {experiment && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            fontSize: 11,
            fontFamily: fonts.data,
            color: colors.text.secondary,
          }}
        >
          <span>{experiment.duration_s.toFixed(1)}s</span>
          <span style={{ color: colors.text.muted }}>&middot;</span>
          <span>{experiment.lod_frames} frames</span>
          <span style={{ color: colors.text.muted }}>&middot;</span>
          <span>
            {experiment.nuclei.length} {experiment.nuclei.length === 1 ? "nucleus" : "nuclei"}
          </span>
        </div>
      )}
    </div>
  );
}
