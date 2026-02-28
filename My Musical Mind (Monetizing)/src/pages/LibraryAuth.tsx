/**
 * Library Auth Bridge
 *
 * Catches /library?auth=ok redirects and continues the My Musical Mind flow.
 * Checks if Spotify tokens exist in localStorage (from PKCE flow).
 */
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useUserStore } from "@/stores/useUserStore";
import { SpotifyService } from "@/services/spotify";

export function LibraryAuth() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const setSpotifyConnected = useUserStore((s) => s.setSpotifyConnected);
  const hasCompletedOnboarding = useUserStore((s) => s.hasCompletedOnboarding);

  useEffect(() => {
    const authOk = searchParams.get("auth") === "ok";

    if (authOk && SpotifyService.isConnected()) {
      setSpotifyConnected(true);
      navigate(hasCompletedOnboarding ? "/spotify" : "/onboarding", {
        replace: true,
        state: { spotifyConnected: true },
      });
    } else {
      navigate(hasCompletedOnboarding ? "/my-mind" : "/", { replace: true });
    }
  }, [searchParams, navigate, setSpotifyConnected, hasCompletedOnboarding]);

  return null;
}
