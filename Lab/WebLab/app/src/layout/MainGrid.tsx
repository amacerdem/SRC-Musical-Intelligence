import { colors, sizes } from "../theme/tokens";

// Panel placeholders — each will be replaced by a real visualization component.
// Importing from ../panels/ when those files are implemented.

function PanelSlot({ label }: { label: string }) {
  return (
    <div
      className="panel"
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: 120,
      }}
    >
      <span
        style={{
          fontSize: 11,
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

export function MainGrid() {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: sizes.panelGap,
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "auto auto 1fr 1fr",
        gap: sizes.panelGap,
        overflow: "auto",
      }}
    >
      {/* Row 1: R3 Heatmap — full width */}
      <div style={{ gridColumn: "1 / -1" }}>
        <PanelSlot label="R3 Heatmap" />
      </div>

      {/* Row 2: Nucleus Output — full width */}
      <div style={{ gridColumn: "1 / -1" }}>
        <PanelSlot label="Nucleus Output" />
      </div>

      {/* Row 3: Brain Region Map (left) + Neurochemical Timeline (right) */}
      <div>
        <PanelSlot label="Brain Region Map" />
      </div>
      <div>
        <PanelSlot label="Neurochemical Timeline" />
      </div>

      {/* Row 4: Psi State (left) + H3 Horizon Grid (right) */}
      <div>
        <PanelSlot label="Psi State" />
      </div>
      <div>
        <PanelSlot label="H3 Horizon Grid" />
      </div>
    </div>
  );
}
