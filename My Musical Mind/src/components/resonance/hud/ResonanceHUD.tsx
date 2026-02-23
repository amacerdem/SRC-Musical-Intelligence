/* ── ResonanceHUD — Top-level overlay container ──────────────────── */

import { useState, useEffect } from "react";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { FieldHeader } from "./FieldHeader";
import { SelfStatePanel } from "./SelfStatePanel";
import { SelectedUserPanel } from "./SelectedUserPanel";
import { CommunicationPanel } from "./CommunicationPanel";
import { SignalOverlay } from "./SignalOverlay";

export function ResonanceHUD() {
  const selectedUserId = useResonanceStore(s => s.selectedUserId);
  const [showComm, setShowComm] = useState(false);

  // Close communication panel when deselecting
  useEffect(() => {
    if (!selectedUserId) setShowComm(false);
  }, [selectedUserId]);

  return (
    <div className="fixed inset-0 z-[44] pointer-events-none [&>*]:pointer-events-auto">
      <FieldHeader />
      <SelfStatePanel />
      <SelectedUserPanel onOpenComm={() => setShowComm(true)} />
      <SignalOverlay />
      {showComm && selectedUserId && (
        <CommunicationPanel
          targetUserId={selectedUserId}
          onClose={() => setShowComm(false)}
        />
      )}
    </div>
  );
}
