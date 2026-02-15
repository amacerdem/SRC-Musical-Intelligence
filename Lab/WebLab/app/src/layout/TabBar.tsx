import { useStore, type TabId } from "../store";
import { colors, fonts } from "../theme/tokens";

const TABS: { id: TabId; label: string }[] = [
  { id: "r3", label: "R\u00b3 Spectral" },
  { id: "nucleus", label: "Nucleus Output" },
  { id: "brain", label: "Brain Regions" },
  { id: "neuro", label: "Neurochemicals" },
  { id: "psi", label: "\u03a8\u00b3 Cognitive" },
  { id: "h3", label: "H\u00b3 Temporal" },
  { id: "evidence", label: "Evidence" },
];

export function TabBar() {
  const activeTab = useStore((s) => s.activeTab);
  const setActiveTab = useStore((s) => s.setActiveTab);
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;

  return (
    <div
      style={{
        height: 36,
        display: "flex",
        alignItems: "stretch",
        gap: 0,
        background: colors.bg.panel,
        borderBottom: `1px solid ${colors.border}`,
        overflow: "hidden",
        flexShrink: 0,
      }}
    >
      {TABS.map((tab) => {
        const isActive = activeTab === tab.id;
        // Show nucleus name in nucleus tab label
        let label = tab.label;
        if (tab.id === "nucleus" && nd) {
          label = `${nd.name} \u2014 ${nd.output_dim}D`;
        }

        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              flex: "0 0 auto",
              padding: "0 16px",
              height: "100%",
              background: "transparent",
              border: "none",
              borderBottom: isActive
                ? `2px solid ${colors.accent}`
                : "2px solid transparent",
              color: isActive ? colors.text.primary : colors.text.secondary,
              fontSize: 11,
              fontWeight: isActive ? 600 : 400,
              fontFamily: fonts.ui,
              letterSpacing: "0.02em",
              cursor: "pointer",
              whiteSpace: "nowrap",
              transition: "color 0.15s, border-color 0.15s",
            }}
            onMouseEnter={(e) => {
              if (!isActive)
                (e.currentTarget as HTMLButtonElement).style.color =
                  colors.text.primary;
            }}
            onMouseLeave={(e) => {
              if (!isActive)
                (e.currentTarget as HTMLButtonElement).style.color =
                  colors.text.secondary;
            }}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
