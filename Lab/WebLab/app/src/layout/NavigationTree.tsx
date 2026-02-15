import { useMemo } from "react";
import { useStore } from "../store";
import { colors, fonts, sizes } from "../theme/tokens";
import type { NucleusData } from "../types/experiment";

interface NucleusByUnit {
  unit: string;
  nuclei: {
    name: string;
    role: string;
    outputDim: number;
  }[];
}

export function NavigationTree() {
  const experiment = useStore((s) => s.experiment);
  const nucleusData = useStore((s) => s.nucleusData);
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const selectNucleus = useStore((s) => s.selectNucleus);

  // Group nuclei by unit
  const unitGroups = useMemo<NucleusByUnit[]>(() => {
    if (!experiment) return [];

    const groupMap = new Map<string, NucleusByUnit>();

    for (const name of experiment.nuclei) {
      const nd: NucleusData | undefined = nucleusData[name];
      const unit = nd?.unit ?? "unknown";
      const role = nd?.role ?? "---";
      const outputDim = nd?.output_dim ?? 0;

      if (!groupMap.has(unit)) {
        groupMap.set(unit, { unit, nuclei: [] });
      }
      groupMap.get(unit)!.nuclei.push({ name, role, outputDim });
    }

    // Sort units alphabetically
    return Array.from(groupMap.values()).sort((a, b) =>
      a.unit.localeCompare(b.unit),
    );
  }, [experiment, nucleusData]);

  return (
    <div
      style={{
        width: sizes.sidebarWidth,
        height: "100%",
        background: colors.bg.primary,
        borderRight: `1px solid ${colors.border}`,
        overflowY: "auto",
        overflowX: "hidden",
      }}
    >
      {/* Sidebar header */}
      <div
        style={{
          padding: "8px 12px",
          fontSize: 10,
          fontWeight: 700,
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          color: colors.text.muted,
          borderBottom: `1px solid ${colors.border}`,
        }}
      >
        Nuclei
      </div>

      {unitGroups.length === 0 && (
        <div
          style={{
            padding: "16px 12px",
            fontSize: 11,
            color: colors.text.muted,
            fontStyle: "italic",
          }}
        >
          No experiment loaded
        </div>
      )}

      {unitGroups.map((group) => (
        <div key={group.unit}>
          {/* Unit header */}
          <div
            style={{
              padding: "6px 12px 4px",
              fontSize: 10,
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.06em",
              color: colors.text.secondary,
              background: colors.bg.surface,
              borderBottom: `1px solid ${colors.border}`,
              borderTop: `1px solid ${colors.border}`,
            }}
          >
            {group.unit}
          </div>

          {/* Nucleus items */}
          {group.nuclei.map((nuc) => {
            const isSelected = selectedNucleus === nuc.name;
            const roleColor =
              colors.roles[nuc.role as keyof typeof colors.roles] ??
              colors.text.muted;

            return (
              <div
                key={nuc.name}
                onClick={() => selectNucleus(nuc.name)}
                style={{
                  padding: "5px 10px 5px 12px",
                  cursor: "pointer",
                  borderLeft: isSelected
                    ? `3px solid ${colors.accent}`
                    : "3px solid transparent",
                  background: isSelected ? colors.bg.hover : "transparent",
                  display: "flex",
                  flexDirection: "column",
                  gap: 2,
                  transition: "background 0.1s",
                }}
                onMouseEnter={(e) => {
                  if (!isSelected)
                    (e.currentTarget as HTMLDivElement).style.background =
                      colors.bg.hover;
                }}
                onMouseLeave={(e) => {
                  if (!isSelected)
                    (e.currentTarget as HTMLDivElement).style.background =
                      "transparent";
                }}
              >
                {/* Nucleus name */}
                <div
                  style={{
                    fontSize: 11,
                    fontWeight: 600,
                    fontFamily: fonts.data,
                    color: isSelected
                      ? colors.text.primary
                      : colors.text.secondary,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {nuc.name}
                </div>

                {/* Role badge + output dim */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span
                    style={{
                      fontSize: 9,
                      fontWeight: 600,
                      fontFamily: fonts.data,
                      textTransform: "uppercase",
                      color: roleColor,
                      background: `${roleColor}18`,
                      padding: "0 4px",
                      borderRadius: 2,
                    }}
                  >
                    {nuc.role}
                  </span>
                  <span
                    style={{
                      fontSize: 9,
                      fontFamily: fonts.data,
                      color: colors.text.muted,
                    }}
                  >
                    {nuc.outputDim}D
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
