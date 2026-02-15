import React, { useMemo, useState } from "react";
import { useStore } from "../store";
import { viridisCSS } from "../canvas/colormap";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const TEXT_SEC = "#8b8b9e";
const BORDER = "#252538";

interface TooltipInfo {
  x: number;
  y: number;
  purpose: string;
  citation: string;
  r3Name: string;
  horizonLabel: string;
  morphName: string;
  lawName: string;
}

/**
 * H3HorizonGridPanel - Grid showing H3 features for selected nucleus.
 * Rows = unique R3 features demanded, Columns = horizons demanded.
 * Cell color by viridis of H3 value at current frame.
 * Tooltip on hover with full demand info.
 */
export default function H3HorizonGridPanel(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const h3Data = useStore((s) => s.h3Data);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const [tooltip, setTooltip] = useState<TooltipInfo | null>(null);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const demands = nd?.h3_demands ?? [];

  // Build unique rows (r3 features) and columns (horizons)
  const { rows, cols, cellMap } = useMemo(() => {
    if (demands.length === 0) {
      return { rows: [] as string[], cols: [] as string[], cellMap: new Map<string, typeof demands[0]>() };
    }
    const rowSet = new Map<number, string>();
    const colSet = new Map<number, string>();
    const cMap = new Map<string, typeof demands[0]>();

    for (const d of demands) {
      rowSet.set(d.r3_idx, d.r3_name);
      colSet.set(d.horizon, d.horizon_label);
      cMap.set(`${d.r3_idx}_${d.horizon}`, d);
    }

    const sortedRows = Array.from(rowSet.entries()).sort((a, b) => a[0] - b[0]);
    const sortedCols = Array.from(colSet.entries()).sort((a, b) => a[0] - b[0]);

    return {
      rows: sortedRows.map(([idx, name]) => ({ idx, name })),
      cols: sortedCols.map(([horizon, label]) => ({ horizon, label })),
      cellMap: cMap,
    };
  }, [demands]);

  const noData = !selectedNucleus || !nd || demands.length === 0;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: BG,
        border: `1px solid ${BORDER}`,
        borderRadius: 6,
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div
        style={{
          padding: "6px 12px",
          fontSize: 12,
          fontWeight: 600,
          color: TEXT,
          borderBottom: `1px solid ${BORDER}`,
          flexShrink: 0,
        }}
      >
        H&sup3; Temporal Demands
      </div>
      <div style={{ flex: 1, overflow: "auto", padding: 8 }}>
        {noData ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              color: TEXT_SEC,
              fontSize: 13,
              fontFamily: "Inter, sans-serif",
            }}
          >
            {!selectedNucleus
              ? "Select a nucleus"
              : demands.length === 0
                ? "No H\u00b3 demands for this nucleus"
                : "Loading\u2026"}
          </div>
        ) : (
          <table
            style={{
              borderCollapse: "collapse",
              width: "100%",
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    padding: "3px 6px",
                    textAlign: "left",
                    color: TEXT_SEC,
                    fontWeight: 500,
                    borderBottom: `1px solid ${BORDER}`,
                    position: "sticky",
                    top: 0,
                    background: BG,
                  }}
                >
                  R&sup3; Feature
                </th>
                {cols.map((c) => (
                  <th
                    key={c.horizon}
                    style={{
                      padding: "3px 6px",
                      textAlign: "center",
                      color: TEXT_SEC,
                      fontWeight: 500,
                      borderBottom: `1px solid ${BORDER}`,
                      position: "sticky",
                      top: 0,
                      background: BG,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {c.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.idx}>
                  <td
                    style={{
                      padding: "3px 6px",
                      color: TEXT,
                      borderBottom: `1px solid ${BORDER}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {r.name}
                  </td>
                  {cols.map((c) => {
                    const demand = cellMap.get(`${r.idx}_${c.horizon}`);
                    if (!demand) {
                      return (
                        <td
                          key={c.horizon}
                          style={{
                            padding: "3px 6px",
                            borderBottom: `1px solid ${BORDER}`,
                            background: "transparent",
                          }}
                        />
                      );
                    }
                    // Look up H3 value: key is "r3_h_m_l"
                    const h3Key = `${demand.r3_idx}_${demand.horizon}_${demand.morph}_${demand.law}`;
                    const timeSeries = h3Data?.[h3Key];
                    const value = timeSeries?.[lodFrameIndex] ?? 0;
                    const clamped = Math.max(0, Math.min(1, value));
                    const bgColor = viridisCSS(clamped);

                    return (
                      <td
                        key={c.horizon}
                        style={{
                          padding: "3px 6px",
                          borderBottom: `1px solid ${BORDER}`,
                          background: bgColor,
                          color: clamped > 0.6 ? "#000" : TEXT,
                          textAlign: "center",
                          cursor: "pointer",
                          minWidth: 40,
                        }}
                        onMouseEnter={(e) => {
                          const rect = (e.target as HTMLElement).getBoundingClientRect();
                          setTooltip({
                            x: rect.left + rect.width / 2,
                            y: rect.top,
                            purpose: demand.purpose,
                            citation: demand.citation,
                            r3Name: demand.r3_name,
                            horizonLabel: demand.horizon_label,
                            morphName: demand.morph_name,
                            lawName: demand.law_name,
                          });
                        }}
                        onMouseLeave={() => setTooltip(null)}
                      >
                        {clamped.toFixed(2)}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Tooltip overlay */}
      {tooltip && (
        <div
          style={{
            position: "fixed",
            left: tooltip.x,
            top: tooltip.y - 8,
            transform: "translate(-50%, -100%)",
            background: "#1a1a24",
            border: `1px solid ${BORDER}`,
            borderRadius: 4,
            padding: "8px 10px",
            fontSize: 10,
            fontFamily: "'JetBrains Mono', monospace",
            color: TEXT,
            zIndex: 1000,
            maxWidth: 280,
            pointerEvents: "none",
            boxShadow: "0 4px 12px rgba(0,0,0,0.5)",
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: 4 }}>
            {tooltip.r3Name} / {tooltip.horizonLabel}
          </div>
          <div style={{ color: TEXT_SEC, marginBottom: 2 }}>
            Morph: {tooltip.morphName} | Law: {tooltip.lawName}
          </div>
          <div style={{ marginBottom: 2 }}>{tooltip.purpose}</div>
          <div style={{ color: TEXT_SEC, fontStyle: "italic" }}>{tooltip.citation}</div>
        </div>
      )}
    </div>
  );
}
