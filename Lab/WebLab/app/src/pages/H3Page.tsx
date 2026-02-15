import React, { useMemo } from "react";
import { useStore } from "../store";
import { viridisCSS } from "../canvas/colormap";
import { colors, fonts } from "../theme/tokens";

/**
 * H3Page -- Full-page H3 temporal demands table for the selected nucleus.
 * Columns: # | R3 Feature | Horizon | Morph | Law | Purpose | Value | Citation
 * Value cell is colored by viridisCSS and shows 3-decimal numeric readout.
 */
export default function H3Page(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const h3Data = useStore((s) => s.h3Data);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const demands = nd?.h3_demands ?? [];

  // Pre-sort demands by r3_idx then horizon for stable ordering
  const sortedDemands = useMemo(
    () =>
      [...demands].sort(
        (a, b) => a.r3_idx - b.r3_idx || a.horizon - b.horizon || a.morph - b.morph || a.law - b.law,
      ),
    [demands],
  );

  const title =
    selectedNucleus && nd
      ? `H\u00b3 Temporal Demands \u2014 ${nd.full_name}`
      : "H\u00b3 Temporal Demands \u2014 Select a nucleus";

  if (!selectedNucleus || !nd || sortedDemands.length === 0) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          background: colors.bg.primary,
          fontFamily: fonts.ui,
        }}
      >
        {/* Title bar */}
        <div
          style={{
            padding: "10px 16px",
            fontSize: 14,
            fontWeight: 600,
            color: colors.text.primary,
            borderBottom: `1px solid ${colors.border}`,
            flexShrink: 0,
          }}
        >
          {title}
        </div>
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: colors.text.secondary,
            fontSize: 14,
          }}
        >
          {!selectedNucleus
            ? "Select a nucleus to view H\u00b3 demands"
            : sortedDemands.length === 0
              ? "No H\u00b3 demands for this nucleus"
              : "Loading\u2026"}
        </div>
      </div>
    );
  }

  const HEADERS = ["#", "R\u00b3 Feature", "Horizon", "Morph", "Law", "Purpose", "Value", "Citation"];

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: colors.bg.primary,
        fontFamily: fonts.ui,
        overflow: "hidden",
      }}
    >
      {/* Title bar */}
      <div
        style={{
          padding: "10px 16px",
          fontSize: 14,
          fontWeight: 600,
          color: colors.text.primary,
          borderBottom: `1px solid ${colors.border}`,
          flexShrink: 0,
        }}
      >
        {title}
      </div>

      {/* Scrollable table */}
      <div style={{ flex: 1, overflow: "auto" }}>
        <table
          style={{
            borderCollapse: "collapse",
            width: "100%",
            fontSize: 12,
          }}
        >
          <thead>
            <tr>
              {HEADERS.map((h) => (
                <th
                  key={h}
                  style={{
                    padding: "8px 10px",
                    textAlign: "left",
                    color: colors.text.secondary,
                    fontFamily: fonts.ui,
                    fontWeight: 600,
                    fontSize: 11,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    borderBottom: `1px solid ${colors.border}`,
                    position: "sticky",
                    top: 0,
                    background: colors.bg.surface,
                    whiteSpace: "nowrap",
                    zIndex: 1,
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedDemands.map((d, i) => {
              const h3Key = `${d.r3_idx}_${d.horizon}_${d.morph}_${d.law}`;
              const timeSeries = h3Data?.[h3Key];
              const rawValue = timeSeries?.[lodFrameIndex] ?? 0;
              const clamped = Math.max(0, Math.min(1, rawValue));
              const bgColor = viridisCSS(clamped);
              const valueFg = clamped > 0.55 ? "#000" : colors.text.primary;
              const rowBg = i % 2 === 0 ? colors.bg.primary : colors.bg.panel;

              return (
                <tr key={h3Key} style={{ background: rowBg }}>
                  {/* # */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.muted,
                      fontFamily: fonts.data,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {i + 1}
                  </td>

                  {/* R3 Feature */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.primary,
                      fontFamily: fonts.data,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span style={{ color: colors.text.muted, marginRight: 4 }}>
                      [{d.r3_idx}]
                    </span>
                    {d.r3_name}
                  </td>

                  {/* Horizon */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.primary,
                      fontFamily: fonts.data,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span style={{ color: colors.text.muted, marginRight: 4 }}>
                      h{d.horizon}
                    </span>
                    {d.horizon_label}
                  </td>

                  {/* Morph */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.primary,
                      fontFamily: fonts.data,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span style={{ color: colors.text.muted, marginRight: 4 }}>
                      m{d.morph}
                    </span>
                    {d.morph_name}
                  </td>

                  {/* Law */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.primary,
                      fontFamily: fonts.data,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span style={{ color: colors.text.muted, marginRight: 4 }}>
                      l{d.law}
                    </span>
                    {d.law_name}
                  </td>

                  {/* Purpose */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.primary,
                      fontFamily: fonts.ui,
                      fontSize: 11,
                      borderBottom: `1px solid ${colors.border}`,
                      maxWidth: 320,
                      lineHeight: 1.4,
                    }}
                  >
                    {d.purpose}
                  </td>

                  {/* Value (viridis-colored) */}
                  <td
                    style={{
                      padding: "6px 10px",
                      fontFamily: fonts.data,
                      fontSize: 12,
                      fontWeight: 600,
                      borderBottom: `1px solid ${colors.border}`,
                      background: bgColor,
                      color: valueFg,
                      textAlign: "center",
                      whiteSpace: "nowrap",
                      minWidth: 72,
                    }}
                  >
                    {rawValue.toFixed(3)}
                  </td>

                  {/* Citation */}
                  <td
                    style={{
                      padding: "6px 10px",
                      color: colors.text.muted,
                      fontFamily: fonts.ui,
                      fontSize: 10,
                      fontStyle: "italic",
                      borderBottom: `1px solid ${colors.border}`,
                      maxWidth: 220,
                      lineHeight: 1.4,
                    }}
                  >
                    {d.citation}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
