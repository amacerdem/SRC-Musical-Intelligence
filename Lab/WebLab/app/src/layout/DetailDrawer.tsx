import { useStore } from "../store";
import { colors, fonts, sizes } from "../theme/tokens";

/** Placeholder for a detail sub-panel. */
function DetailSlot({ label }: { label: string }) {
  return (
    <div
      className="panel"
      style={{
        flex: 1,
        minWidth: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
      }}
    >
      <span
        style={{
          fontSize: 10,
          fontWeight: 600,
          textTransform: "uppercase",
          letterSpacing: "0.05em",
          color: colors.text.muted,
        }}
      >
        {label}
      </span>
    </div>
  );
}

export function DetailDrawer() {
  const drawerOpen = useStore((s) => s.detailDrawerOpen);
  const toggleDrawer = useStore((s) => s.toggleDrawer);

  const totalHeight = drawerOpen ? sizes.drawerHeight : 32;

  return (
    <div
      style={{
        height: totalHeight,
        background: colors.bg.panel,
        borderTop: `1px solid ${colors.border}`,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        transition: "height 0.25s ease-in-out",
      }}
    >
      {/* Toggle bar */}
      <div
        onClick={toggleDrawer}
        style={{
          height: 32,
          minHeight: 32,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 8,
          cursor: "pointer",
          background: colors.bg.surface,
          borderBottom: drawerOpen
            ? `1px solid ${colors.border}`
            : "none",
          userSelect: "none",
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLDivElement).style.background =
            colors.bg.hover;
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLDivElement).style.background =
            colors.bg.surface;
        }}
      >
        {/* Chevron indicator */}
        <span
          style={{
            fontSize: 12,
            color: colors.text.muted,
            transform: drawerOpen ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.25s ease-in-out",
            display: "inline-block",
          }}
        >
          {"\u25B2"}
        </span>
        <span
          style={{
            fontSize: 10,
            fontWeight: 600,
            fontFamily: fonts.ui,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
            color: colors.text.muted,
          }}
        >
          Detail
        </span>
      </div>

      {/* Sub-panels (visible when open) */}
      {drawerOpen && (
        <div
          style={{
            flex: 1,
            display: "flex",
            gap: sizes.panelGap,
            padding: sizes.panelGap,
            minHeight: 0,
          }}
        >
          <DetailSlot label="Region Link Flow" />
          <DetailSlot label="NeuroLink Effects" />
          <DetailSlot label="Citations" />
          <DetailSlot label="Layer Inspector" />
        </div>
      )}
    </div>
  );
}
