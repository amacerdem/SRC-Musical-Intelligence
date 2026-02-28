/**
 * Spotify OAuth Callback Page
 *
 * Spotify redirects here after the user authorizes.
 * Exchanges the authorization code via Repetuare backend,
 * stores tokens in localStorage, then navigates back to the app.
 */
import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";

const STORAGE_KEYS = {
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expiresAt: "spotify_expires_at",
  preAuthPath: "spotify_pre_auth_path",
  preAuthUserName: "spotify_pre_auth_username",
};

export function Callback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [errorMsg, setErrorMsg] = useState("");
  const setSpotifyConnected = useUserStore((s) => s.setSpotifyConnected);
  const exchanged = useRef(false);

  useEffect(() => {
    if (exchanged.current) return;
    exchanged.current = true;

    async function process() {
      const code = searchParams.get("code");
      const error = searchParams.get("error");

      if (error) {
        setStatus("error");
        setErrorMsg(`Spotify auth error: ${error}`);
        return;
      }

      if (!code) {
        setStatus("error");
        setErrorMsg("No authorization code received");
        return;
      }

      try {
        const res = await fetch("/api/spotify/exchange", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        });

        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: "Token exchange failed" }));
          throw new Error(err.detail || "Token exchange failed");
        }

        const data = await res.json();

        // Store tokens in localStorage for client-side API calls
        const expiresAt = Date.now() + (data.expires_in ?? 3600) * 1000;
        localStorage.setItem(STORAGE_KEYS.accessToken, data.access_token);
        localStorage.setItem(STORAGE_KEYS.refreshToken, data.refresh_token ?? "");
        localStorage.setItem(STORAGE_KEYS.expiresAt, String(expiresAt));

        // Retrieve pre-auth context
        const fromPath = sessionStorage.getItem(STORAGE_KEYS.preAuthPath) ?? "/onboarding";
        const userName = sessionStorage.getItem(STORAGE_KEYS.preAuthUserName) ?? "";

        // Clean up
        sessionStorage.removeItem(STORAGE_KEYS.preAuthPath);
        sessionStorage.removeItem(STORAGE_KEYS.preAuthUserName);

        setSpotifyConnected(true);
        setStatus("success");

        setTimeout(() => {
          navigate(fromPath, {
            replace: true,
            state: { spotifyConnected: true, userName },
          });
        }, 1200);
      } catch (err: any) {
        setStatus("error");
        setErrorMsg(err.message || "Authentication failed");
      }
    }

    process();
  }, [searchParams, navigate, setSpotifyConnected]);

  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        {status === "loading" && (
          <>
            <Loader2 size={40} className="animate-spin mx-auto mb-4" style={{ color: "#1DB954" }} />
            <p className="text-lg font-display font-medium text-slate-300">
              Connecting to Spotify...
            </p>
            <p className="text-sm text-slate-600 font-display font-light mt-2">
              Exchanging authorization
            </p>
          </>
        )}

        {status === "success" && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }}
          >
            <CheckCircle2 size={48} className="mx-auto mb-4" style={{ color: "#1DB954" }} />
            <p className="text-xl font-display font-bold" style={{ color: "#1DB954" }}>
              Connected!
            </p>
            <p className="text-sm text-slate-500 font-display font-light mt-2">
              Redirecting...
            </p>
          </motion.div>
        )}

        {status === "error" && (
          <>
            <XCircle size={48} className="mx-auto mb-4 text-red-500" />
            <p className="text-xl font-display font-bold text-red-400">
              Connection Failed
            </p>
            <p className="text-sm text-slate-500 font-display font-light mt-2 max-w-xs">
              {errorMsg}
            </p>
            <button
              onClick={() => navigate("/")}
              className="mt-6 px-6 py-2 rounded-xl text-sm font-display font-medium text-slate-300 transition-all duration-300 hover:text-white"
              style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)" }}
            >
              Back to Home
            </button>
          </>
        )}
      </motion.div>
    </div>
  );
}
