import React from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const TEXT_SEC = "#8b8b9e";
const BORDER = "#252538";
const FONT_DATA = "'JetBrains Mono', 'Fira Code', monospace";

const SCOPE_BADGE_STYLES: Record<string, { bg: string; color: string }> = {
  internal: { bg: "rgba(59, 130, 246, 0.2)", color: "#3b82f6" },
  external: { bg: "rgba(34, 197, 94, 0.2)", color: "#22c55e" },
  hybrid: { bg: "rgba(245, 158, 11, 0.2)", color: "#f59e0b" },
};

/**
 * LayerInspectorPanel - E/M/P/F layer table with live values for selected nucleus.
 * One row per layer: Code | Name | Scope (badge) | Dim Count | Dim Names | Current Values.
 */
export default function LayerInspectorPanel(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const layers = nd?.layers ?? [];

  // Current output frame values
  const frameValues = nd?.output?.[lodFrameIndex] ?? null;

  const noData = !selectedNucleus || !nd || layers.length === 0;

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
        Layer Inspector
      </div>
      <div style={{ flex: 1, overflow: "auto" }}>
        {noData ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              padding: 12,
              color: TEXT_SEC,
              fontSize: 13,
              fontFamily: "Inter, sans-serif",
            }}
          >
            {!selectedNucleus ? "Select a nucleus" : "Loading\u2026"}
          </div>
        ) : (
          <table
            style={{
              borderCollapse: "collapse",
              width: "100%",
              fontSize: 10,
              fontFamily: FONT_DATA,
            }}
          >
            <thead>
              <tr>
                {["Code", "Name", "Scope", "Dims", "Dim Names", "Current Values"].map(
                  (h) => (
                    <th
                      key={h}
                      style={{
                        padding: "4px 6px",
                        textAlign: "left",
                        color: TEXT_SEC,
                        fontWeight: 500,
                        borderBottom: `1px solid ${BORDER}`,
                        position: "sticky",
                        top: 0,
                        background: BG,
                        whiteSpace: "nowrap",
                      }}
                    >
                      {h}
                    </th>
                  ),
                )}
              </tr>
            </thead>
            <tbody>
              {layers.map((layer) => {
                const dimCount = layer.end - layer.start;
                const badge = SCOPE_BADGE_STYLES[layer.scope] ?? {
                  bg: BORDER,
                  color: TEXT,
                };

                // Extract current values for this layer
                const values: number[] = [];
                if (frameValues) {
                  for (let i = layer.start; i < layer.end; i++) {
                    values.push(frameValues[i] ?? 0);
                  }
                }

                return (
                  <tr key={layer.code}>
                    {/* Code */}
                    <td
                      style={{
                        padding: "3px 6px",
                        color: TEXT,
                        borderBottom: `1px solid ${BORDER}`,
                        fontWeight: 600,
                        whiteSpace: "nowrap",
                      }}
                    >
                      {layer.code}
                    </td>

                    {/* Name */}
                    <td
                      style={{
                        padding: "3px 6px",
                        color: TEXT,
                        borderBottom: `1px solid ${BORDER}`,
                        whiteSpace: "nowrap",
                        maxWidth: 120,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      }}
                    >
                      {layer.name}
                    </td>

                    {/* Scope badge */}
                    <td
                      style={{
                        padding: "3px 6px",
                        borderBottom: `1px solid ${BORDER}`,
                      }}
                    >
                      <span
                        style={{
                          display: "inline-block",
                          padding: "1px 6px",
                          borderRadius: 3,
                          fontSize: 9,
                          fontWeight: 600,
                          color: badge.color,
                          background: badge.bg,
                          textTransform: "uppercase",
                          letterSpacing: 0.3,
                        }}
                      >
                        {layer.scope}
                      </span>
                    </td>

                    {/* Dim count */}
                    <td
                      style={{
                        padding: "3px 6px",
                        color: TEXT,
                        borderBottom: `1px solid ${BORDER}`,
                        textAlign: "center",
                      }}
                    >
                      {dimCount}
                    </td>

                    {/* Dim names */}
                    <td
                      style={{
                        padding: "3px 6px",
                        color: TEXT_SEC,
                        borderBottom: `1px solid ${BORDER}`,
                        fontSize: 9,
                        maxWidth: 200,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                      title={layer.dim_names.join(", ")}
                    >
                      {layer.dim_names.join(", ")}
                    </td>

                    {/* Current values */}
                    <td
                      style={{
                        padding: "3px 6px",
                        color: badge.color,
                        borderBottom: `1px solid ${BORDER}`,
                        fontFamily: FONT_DATA,
                        fontSize: 9,
                        maxWidth: 260,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                      title={values.map((v) => v.toFixed(4)).join(", ")}
                    >
                      {frameValues
                        ? values.map((v) => v.toFixed(4)).join("  ")
                        : "\u2014"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
