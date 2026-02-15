import React from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const TEXT_SEC = "#8b8b9e";
const BORDER = "#252538";
const FONT_DATA = "'JetBrains Mono', 'Fira Code', monospace";

const TIER_COLORS: Record<string, string> = {
  alpha: "#22c55e",
  beta: "#f59e0b",
  gamma: "#ef4444",
};

/**
 * CitationPanel - Evidence table and metadata for selected nucleus (detail drawer).
 * Shows evidence tier badge, confidence range, version, paper count,
 * citation table (Author | Year | Finding | Effect Size), and falsification criteria.
 */
export default function CitationPanel(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const meta = nd?.metadata ?? null;

  const noData = !selectedNucleus || !nd || !meta;

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
        Evidence &amp; Citations
      </div>
      <div style={{ flex: 1, overflow: "auto", padding: 12 }}>
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
            {!selectedNucleus ? "Select a nucleus" : "Loading\u2026"}
          </div>
        ) : (
          <>
            {/* Top metadata row */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                marginBottom: 12,
                flexWrap: "wrap",
              }}
            >
              {/* Evidence tier badge */}
              <span
                style={{
                  display: "inline-block",
                  padding: "2px 8px",
                  borderRadius: 4,
                  fontSize: 11,
                  fontWeight: 700,
                  fontFamily: FONT_DATA,
                  color: BG,
                  background: TIER_COLORS[meta.evidence_tier] ?? TEXT,
                  textTransform: "uppercase",
                  letterSpacing: 0.5,
                }}
              >
                {meta.evidence_tier}
              </span>

              {/* Confidence range bar */}
              <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <span style={{ fontSize: 10, color: TEXT_SEC, fontFamily: FONT_DATA }}>
                  conf:
                </span>
                <div
                  style={{
                    width: 80,
                    height: 8,
                    background: BORDER,
                    borderRadius: 4,
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: `${meta.confidence_range[0] * 100}%`,
                      width: `${(meta.confidence_range[1] - meta.confidence_range[0]) * 100}%`,
                      height: "100%",
                      background: TIER_COLORS[meta.evidence_tier] ?? TEXT,
                      borderRadius: 4,
                      opacity: 0.8,
                    }}
                  />
                </div>
                <span style={{ fontSize: 9, color: TEXT_SEC, fontFamily: FONT_DATA }}>
                  [{meta.confidence_range[0].toFixed(2)}, {meta.confidence_range[1].toFixed(2)}]
                </span>
              </div>

              {/* Version */}
              <span style={{ fontSize: 10, color: TEXT_SEC, fontFamily: FONT_DATA }}>
                v{meta.version}
              </span>

              {/* Paper count */}
              <span style={{ fontSize: 10, color: TEXT_SEC, fontFamily: FONT_DATA }}>
                {meta.paper_count} paper{meta.paper_count !== 1 ? "s" : ""}
              </span>
            </div>

            {/* Citation table */}
            {meta.citations.length > 0 && (
              <table
                style={{
                  borderCollapse: "collapse",
                  width: "100%",
                  fontFamily: FONT_DATA,
                  fontSize: 10,
                  marginBottom: 12,
                }}
              >
                <thead>
                  <tr>
                    {["Author", "Year", "Finding", "Effect Size"].map((h) => (
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
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {meta.citations.map((c, i) => (
                    <tr key={i}>
                      <td
                        style={{
                          padding: "3px 6px",
                          color: TEXT,
                          borderBottom: `1px solid ${BORDER}`,
                          whiteSpace: "nowrap",
                        }}
                      >
                        {c.author}
                      </td>
                      <td
                        style={{
                          padding: "3px 6px",
                          color: TEXT,
                          borderBottom: `1px solid ${BORDER}`,
                          whiteSpace: "nowrap",
                        }}
                      >
                        {c.year}
                      </td>
                      <td
                        style={{
                          padding: "3px 6px",
                          color: TEXT,
                          borderBottom: `1px solid ${BORDER}`,
                          maxWidth: 300,
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                        }}
                      >
                        {c.finding}
                      </td>
                      <td
                        style={{
                          padding: "3px 6px",
                          color: TEXT,
                          borderBottom: `1px solid ${BORDER}`,
                          whiteSpace: "nowrap",
                        }}
                      >
                        {c.effect_size}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            {/* Falsification criteria */}
            {meta.falsification_criteria.length > 0 && (
              <div
                style={{
                  background: "rgba(239, 68, 68, 0.08)",
                  border: "1px solid rgba(239, 68, 68, 0.25)",
                  borderRadius: 4,
                  padding: "8px 10px",
                }}
              >
                <div
                  style={{
                    fontSize: 10,
                    fontWeight: 600,
                    color: "#ef4444",
                    marginBottom: 6,
                    fontFamily: "Inter, sans-serif",
                  }}
                >
                  Falsification Criteria
                </div>
                <ol
                  style={{
                    margin: 0,
                    paddingLeft: 18,
                    fontFamily: FONT_DATA,
                    fontSize: 10,
                    color: TEXT,
                    lineHeight: 1.6,
                  }}
                >
                  {meta.falsification_criteria.map((fc, i) => (
                    <li key={i} style={{ marginBottom: 2 }}>
                      {fc}
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
