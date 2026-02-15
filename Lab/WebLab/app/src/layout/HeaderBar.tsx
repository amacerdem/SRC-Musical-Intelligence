import { useStore } from "../store";
import { colors, fonts, sizes } from "../theme/tokens";

export function HeaderBar() {
  const experimentList = useStore((s) => s.experimentList);
  const experimentSlug = useStore((s) => s.experimentSlug);
  const experiment = useStore((s) => s.experiment);
  const loadExperiment = useStore((s) => s.loadExperiment);

  const nucleusCount = experiment ? experiment.nuclei.length : 0;

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

      {/* Right: Nucleus count badge */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
        }}
      >
        <span
          style={{
            fontSize: 10,
            color: colors.text.muted,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
          }}
        >
          Nuclei
        </span>
        <span
          style={{
            background: `${colors.accent}20`,
            color: colors.accent,
            fontSize: 11,
            fontWeight: 700,
            fontFamily: fonts.data,
            padding: "2px 8px",
            borderRadius: 3,
            minWidth: 28,
            textAlign: "center",
          }}
        >
          {nucleusCount}
        </span>
      </div>
    </div>
  );
}
