import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "@/stores/useUserStore";

/* Reveal is now handled inside Onboarding. This redirects legacy /reveal URLs. */
export function MindReveal() {
  const navigate = useNavigate();
  const { hasCompletedOnboarding } = useUserStore();

  useEffect(() => {
    navigate(hasCompletedOnboarding ? "/my-mind" : "/onboarding", { replace: true });
  }, [hasCompletedOnboarding, navigate]);

  return null;
}
