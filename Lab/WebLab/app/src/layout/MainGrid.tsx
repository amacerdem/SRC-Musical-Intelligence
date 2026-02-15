import { sizes } from "../theme/tokens";
import R3HeatmapPanel from "../panels/R3HeatmapPanel";
import NucleusOutputPanel from "../panels/NucleusOutputPanel";
import BrainRegionMapPanel from "../panels/BrainRegionMapPanel";
import NeurochemicalTimelinePanel from "../panels/NeurochemicalTimelinePanel";
import PsiStatePanel from "../panels/PsiStatePanel";
import H3HorizonGridPanel from "../panels/H3HorizonGridPanel";

export function MainGrid() {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: sizes.panelGap,
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "minmax(200px, 2fr) minmax(180px, 2fr) minmax(280px, 3fr) minmax(280px, 3fr)",
        gap: sizes.panelGap,
        overflow: "auto",
      }}
    >
      {/* Row 1: R3 Heatmap — full width */}
      <div style={{ gridColumn: "1 / -1", minHeight: 0, height: "100%" }}>
        <R3HeatmapPanel />
      </div>

      {/* Row 2: Nucleus Output — full width */}
      <div style={{ gridColumn: "1 / -1", minHeight: 0, height: "100%" }}>
        <NucleusOutputPanel />
      </div>

      {/* Row 3: Brain Region Map (left) + Neurochemical Timeline (right) */}
      <div style={{ minHeight: 0, height: "100%" }}>
        <BrainRegionMapPanel />
      </div>
      <div style={{ minHeight: 0, height: "100%" }}>
        <NeurochemicalTimelinePanel />
      </div>

      {/* Row 4: Psi State (left) + H3 Horizon Grid (right) */}
      <div style={{ minHeight: 0, height: "100%" }}>
        <PsiStatePanel />
      </div>
      <div style={{ minHeight: 0, height: "100%" }}>
        <H3HorizonGridPanel />
      </div>
    </div>
  );
}
