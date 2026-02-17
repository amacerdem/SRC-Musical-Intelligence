import React, { useMemo } from "react";
import { useStore } from "../store";
import { colors, fonts } from "../theme/tokens";

/* ------------------------------------------------------------------ */
/*  Style constants                                                    */
/* ------------------------------------------------------------------ */

const SCOPE_BADGE: Record<string, { bg: string; fg: string }> = {
  internal: { bg: "rgba(59, 130, 246, 0.18)", fg: colors.scope.internal },
  external: { bg: "rgba(34, 197, 94, 0.18)", fg: colors.scope.external },
  hybrid: { bg: "rgba(245, 158, 11, 0.18)", fg: colors.scope.hybrid },
};

const EFFECT_COLORS: Record<string, string> = {
  produce: "#22c55e",
  amplify: "#3b82f6",
  inhibit: "#ef4444",
};

const REGION_GROUP_COLORS: Record<string, string> = {
  cortical: colors.regions.cortical,
  subcortical: colors.regions.subcortical,
  brainstem: colors.regions.brainstem,
};

/* ------------------------------------------------------------------ */
/*  Reusable Section wrapper                                           */
/* ------------------------------------------------------------------ */

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <div
      style={{
        background: colors.bg.panel,
        border: `1px solid ${colors.border}`,
        borderRadius: 6,
        marginBottom: 16,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "8px 14px",
          fontSize: 12,
          fontWeight: 700,
          color: colors.text.primary,
          background: colors.bg.surface,
          borderBottom: `1px solid ${colors.border}`,
          fontFamily: fonts.ui,
          letterSpacing: 0.3,
        }}
      >
        {title}
      </div>
      <div style={{ padding: 14 }}>{children}</div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Shared table header helper                                         */
/* ------------------------------------------------------------------ */

function TH({ children }: { children: React.ReactNode }): React.ReactElement {
  return (
    <th
      style={{
        padding: "6px 10px",
        textAlign: "left",
        color: colors.text.secondary,
        fontFamily: fonts.ui,
        fontWeight: 600,
        fontSize: 10,
        textTransform: "uppercase",
        letterSpacing: 0.5,
        borderBottom: `1px solid ${colors.border}`,
        background: colors.bg.surface,
        position: "sticky",
        top: 0,
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </th>
  );
}

function TD({
  children,
  style,
  title,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
  title?: string;
}): React.ReactElement {
  return (
    <td
      title={title}
      style={{
        padding: "5px 10px",
        borderBottom: `1px solid ${colors.border}`,
        fontSize: 11,
        color: colors.text.primary,
        fontFamily: fonts.data,
        ...style,
      }}
    >
      {children}
    </td>
  );
}

/* ------------------------------------------------------------------ */
/*  EvidencePage                                                        */
/* ------------------------------------------------------------------ */

export default function EvidencePage(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const regions = useStore((s) => s.regions);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const meta = nd?.metadata ?? null;
  const layers = nd?.layers ?? [];
  const regionLinks = nd?.region_links ?? [];
  const neuroLinks = nd?.neuro_links ?? [];
  const citations = meta?.citations ?? [];
  const falsificationCriteria = meta?.falsification_criteria ?? [];

  // Dim name -> scope mapping (used to color dim names by scope)
  const dimScopeMap = useMemo(() => {
    const m = new Map<string, string>();
    for (const layer of layers) {
      for (const dn of layer.dim_names) {
        m.set(dn, layer.scope);
      }
    }
    return m;
  }, [layers]);

  // Region abbreviation -> group mapping
  const regionGroupMap = useMemo(() => {
    const m = new Map<string, string>();
    for (const r of regions) {
      m.set(r.abbreviation, r.group);
    }
    return m;
  }, [regions]);

  // Citations sorted by year descending
  const sortedCitations = useMemo(
    () => [...citations].sort((a, b) => b.year - a.year),
    [citations],
  );

  // Current frame output values
  const frameValues = nd?.output?.[lodFrameIndex] ?? null;

  // No nucleus selected -- centered message
  if (!selectedNucleus || !nd || !meta) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: colors.bg.primary,
          color: colors.text.secondary,
          fontFamily: fonts.ui,
          fontSize: 14,
        }}
      >
        {!selectedNucleus ? "Select a nucleus to view evidence" : "Loading\u2026"}
      </div>
    );
  }

  const tierColor = colors.tiers[meta.evidence_tier] ?? colors.text.primary;

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
      {/* Scrollable content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px 20px" }}>
        {/* ============================================================ */}
        {/*  Section 1: Metadata Header                                  */}
        {/* ============================================================ */}
        <div style={{ marginBottom: 20 }}>
          {/* Nucleus name */}
          <div
            style={{
              fontSize: 22,
              fontWeight: 700,
              color: colors.text.primary,
              fontFamily: fonts.ui,
              marginBottom: 2,
            }}
          >
            {nd.name}
          </div>
          <div
            style={{
              fontSize: 13,
              color: colors.text.secondary,
              fontFamily: fonts.ui,
              marginBottom: 12,
            }}
          >
            {nd.full_name}
          </div>

          {/* Badge row */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              flexWrap: "wrap",
            }}
          >
            {/* Evidence tier badge */}
            <span
              style={{
                display: "inline-block",
                padding: "3px 10px",
                borderRadius: 4,
                fontSize: 11,
                fontWeight: 700,
                fontFamily: fonts.data,
                color: colors.bg.primary,
                background: tierColor,
                textTransform: "uppercase",
                letterSpacing: 0.6,
              }}
            >
              {meta.evidence_tier}
            </span>

            {/* Version badge */}
            <span
              style={{
                display: "inline-block",
                padding: "3px 10px",
                borderRadius: 4,
                fontSize: 11,
                fontWeight: 600,
                fontFamily: fonts.data,
                color: colors.accent,
                background: "rgba(99, 102, 241, 0.15)",
                letterSpacing: 0.3,
              }}
            >
              v{meta.version}
            </span>

            {/* Paper count badge */}
            <span
              style={{
                display: "inline-block",
                padding: "3px 10px",
                borderRadius: 4,
                fontSize: 11,
                fontWeight: 600,
                fontFamily: fonts.data,
                color: colors.text.secondary,
                background: colors.bg.surface,
                border: `1px solid ${colors.border}`,
              }}
            >
              {meta.paper_count} paper{meta.paper_count !== 1 ? "s" : ""}
            </span>

            {/* Confidence range bar */}
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span
                style={{
                  fontSize: 10,
                  color: colors.text.muted,
                  fontFamily: fonts.data,
                }}
              >
                conf
              </span>
              <div
                style={{
                  width: 120,
                  height: 6,
                  background: colors.border,
                  borderRadius: 3,
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
                    background: tierColor,
                    borderRadius: 3,
                    opacity: 0.85,
                  }}
                />
              </div>
              <span
                style={{
                  fontSize: 10,
                  color: colors.text.muted,
                  fontFamily: fonts.data,
                }}
              >
                [{meta.confidence_range[0].toFixed(2)}, {meta.confidence_range[1].toFixed(2)}]
              </span>
            </div>
          </div>
        </div>

        {/* ============================================================ */}
        {/*  Section 2: Region Links                                     */}
        {/* ============================================================ */}
        {regionLinks.length > 0 && (
          <Section title="Region Links">
            <div style={{ overflow: "auto" }}>
              <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11 }}>
                <thead>
                  <tr>
                    <TH>Dimension Name</TH>
                    <TH>Region</TH>
                    <TH>Weight</TH>
                    <TH>Citation</TH>
                  </tr>
                </thead>
                <tbody>
                  {regionLinks.map((rl, i) => {
                    const scope = dimScopeMap.get(rl.dim_name) ?? "internal";
                    const scopeColor = colors.scope[scope as keyof typeof colors.scope] ?? colors.text.primary;
                    const regionGroup = regionGroupMap.get(rl.region) ?? "cortical";
                    const regionColor = REGION_GROUP_COLORS[regionGroup] ?? colors.text.primary;
                    const absWeight = Math.abs(rl.weight);
                    const maxBarWidth = 80;

                    return (
                      <tr
                        key={`${rl.dim_name}-${rl.region}-${i}`}
                        style={{ background: i % 2 === 0 ? "transparent" : colors.bg.surface }}
                      >
                        <TD style={{ color: scopeColor, fontWeight: 600 }}>
                          {rl.dim_name}
                        </TD>
                        <TD style={{ color: regionColor, fontWeight: 600 }}>
                          {rl.region}
                        </TD>
                        <TD>
                          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                            <div
                              style={{
                                width: maxBarWidth,
                                height: 6,
                                background: colors.border,
                                borderRadius: 3,
                                overflow: "hidden",
                                flexShrink: 0,
                              }}
                            >
                              <div
                                style={{
                                  width: `${Math.min(absWeight, 1) * 100}%`,
                                  height: "100%",
                                  background: scopeColor,
                                  borderRadius: 3,
                                  opacity: 0.8,
                                }}
                              />
                            </div>
                            <span
                              style={{
                                fontFamily: fonts.data,
                                fontSize: 10,
                                color: colors.text.primary,
                                whiteSpace: "nowrap",
                              }}
                            >
                              {rl.weight.toFixed(3)}
                            </span>
                          </div>
                        </TD>
                        <TD
                          style={{
                            color: colors.text.muted,
                            fontFamily: fonts.ui,
                            fontStyle: "italic",
                            fontSize: 10,
                            maxWidth: 240,
                            lineHeight: 1.4,
                          }}
                        >
                          {rl.citation}
                        </TD>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {/* ============================================================ */}
        {/*  Section 3: Neuro Links                                      */}
        {/* ============================================================ */}
        {neuroLinks.length > 0 && (
          <Section title="Neuro Links">
            <div style={{ overflow: "auto" }}>
              <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11 }}>
                <thead>
                  <tr>
                    <TH>Dimension Name</TH>
                    <TH>Channel</TH>
                    <TH>Effect</TH>
                    <TH>Weight</TH>
                    <TH>Citation</TH>
                  </tr>
                </thead>
                <tbody>
                  {neuroLinks.map((nl, i) => {
                    const channelColor =
                      colors.neuro[nl.channel_name as keyof typeof colors.neuro] ??
                      colors.text.primary;
                    const effectColor = EFFECT_COLORS[nl.effect] ?? colors.text.primary;

                    return (
                      <tr
                        key={`${nl.dim_name}-${nl.channel_name}-${nl.effect}-${i}`}
                        style={{ background: i % 2 === 0 ? "transparent" : colors.bg.surface }}
                      >
                        <TD style={{ fontWeight: 600 }}>{nl.dim_name}</TD>
                        <TD style={{ color: channelColor, fontWeight: 700 }}>
                          {nl.channel_name}
                        </TD>
                        <TD
                          style={{
                            color: effectColor,
                            fontWeight: 600,
                            textTransform: "uppercase",
                            fontSize: 10,
                            letterSpacing: 0.4,
                          }}
                        >
                          {nl.effect}
                        </TD>
                        <TD>
                          <span
                            style={{
                              fontFamily: fonts.data,
                              fontSize: 11,
                              color: colors.text.primary,
                            }}
                          >
                            {nl.weight.toFixed(3)}
                          </span>
                        </TD>
                        <TD
                          style={{
                            color: colors.text.muted,
                            fontFamily: fonts.ui,
                            fontStyle: "italic",
                            fontSize: 10,
                            maxWidth: 240,
                            lineHeight: 1.4,
                          }}
                        >
                          {nl.citation}
                        </TD>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {/* ============================================================ */}
        {/*  Section 4: Layer Inspector                                   */}
        {/* ============================================================ */}
        {layers.length > 0 && (
          <Section title="Layer Inspector">
            <div style={{ overflow: "auto" }}>
              <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11 }}>
                <thead>
                  <tr>
                    <TH>Code</TH>
                    <TH>Name</TH>
                    <TH>Scope</TH>
                    <TH>Dims</TH>
                    <TH>Dim Names</TH>
                    <TH>Values at Frame</TH>
                  </tr>
                </thead>
                <tbody>
                  {layers.map((layer, i) => {
                    const dimCount = layer.end - layer.start;
                    const badge = SCOPE_BADGE[layer.scope] ?? {
                      bg: colors.border,
                      fg: colors.text.primary,
                    };

                    // Extract current values for this layer
                    const values: number[] = [];
                    if (frameValues) {
                      for (let j = layer.start; j < layer.end; j++) {
                        values.push(frameValues[j] ?? 0);
                      }
                    }

                    return (
                      <tr
                        key={layer.code}
                        style={{ background: i % 2 === 0 ? "transparent" : colors.bg.surface }}
                      >
                        <TD style={{ fontWeight: 700, whiteSpace: "nowrap" }}>
                          {layer.code}
                        </TD>
                        <TD
                          style={{
                            whiteSpace: "nowrap",
                            maxWidth: 140,
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                          }}
                        >
                          {layer.name}
                        </TD>
                        <TD>
                          <span
                            style={{
                              display: "inline-block",
                              padding: "2px 8px",
                              borderRadius: 10,
                              fontSize: 9,
                              fontWeight: 700,
                              color: badge.fg,
                              background: badge.bg,
                              textTransform: "uppercase",
                              letterSpacing: 0.4,
                            }}
                          >
                            {layer.scope}
                          </span>
                        </TD>
                        <TD style={{ textAlign: "center" }}>{dimCount}</TD>
                        <TD
                          style={{
                            fontSize: 9,
                            color: colors.text.secondary,
                            maxWidth: 220,
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap",
                          }}
                          title={layer.dim_names.join(", ")}
                        >
                          {layer.dim_names.join(", ")}
                        </TD>
                        <TD
                          style={{
                            fontFamily: fonts.data,
                            fontSize: 10,
                            color: badge.fg,
                            maxWidth: 300,
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap",
                          }}
                          title={values.map((v) => v.toFixed(3)).join(", ")}
                        >
                          {frameValues
                            ? values.map((v) => v.toFixed(3)).join("  ")
                            : "\u2014"}
                        </TD>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {/* ============================================================ */}
        {/*  Section 5: Citations                                        */}
        {/* ============================================================ */}
        {sortedCitations.length > 0 && (
          <Section title="Citations">
            <div style={{ overflow: "auto" }}>
              <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11 }}>
                <thead>
                  <tr>
                    <TH>Author</TH>
                    <TH>Year</TH>
                    <TH>Finding</TH>
                    <TH>Effect Size</TH>
                  </tr>
                </thead>
                <tbody>
                  {sortedCitations.map((c, i) => (
                    <tr
                      key={`${c.author}-${c.year}-${i}`}
                      style={{ background: i % 2 === 0 ? "transparent" : colors.bg.surface }}
                    >
                      <TD style={{ whiteSpace: "nowrap", fontWeight: 600 }}>{c.author}</TD>
                      <TD style={{ whiteSpace: "nowrap" }}>{c.year}</TD>
                      <TD
                        style={{
                          fontFamily: fonts.ui,
                          maxWidth: 400,
                          lineHeight: 1.5,
                        }}
                      >
                        {c.finding}
                      </TD>
                      <TD style={{ whiteSpace: "nowrap" }}>{c.effect_size}</TD>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {/* ============================================================ */}
        {/*  Section 6: Falsification Criteria                           */}
        {/* ============================================================ */}
        {falsificationCriteria.length > 0 && (
          <Section title="Falsification Criteria">
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >
              {falsificationCriteria.map((criterion, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    gap: 10,
                    alignItems: "flex-start",
                    padding: "10px 14px",
                    background: "rgba(239, 68, 68, 0.06)",
                    border: "1px solid rgba(239, 68, 68, 0.2)",
                    borderRadius: 6,
                  }}
                >
                  {/* Number badge */}
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      justifyContent: "center",
                      width: 22,
                      height: 22,
                      borderRadius: "50%",
                      background: "rgba(239, 68, 68, 0.15)",
                      color: "#ef4444",
                      fontFamily: fonts.data,
                      fontSize: 11,
                      fontWeight: 700,
                      flexShrink: 0,
                    }}
                  >
                    {i + 1}
                  </span>
                  <span
                    style={{
                      fontFamily: fonts.data,
                      fontSize: 11,
                      color: colors.text.primary,
                      lineHeight: 1.6,
                    }}
                  >
                    {criterion}
                  </span>
                </div>
              ))}
            </div>
          </Section>
        )}
      </div>
    </div>
  );
}
