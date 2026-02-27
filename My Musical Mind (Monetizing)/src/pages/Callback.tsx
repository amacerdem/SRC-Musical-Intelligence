/**
 * Spotify OAuth Callback Page
 *
 * Spotify redirects here after the user authorizes.
 * Exchanges the authorization code for tokens, then navigates
 * back to the onboarding/landing flow to continue evolution.
 */
import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { SpotifyService } from "@/services/spotify";
import { useUserStore } from "@/stores/useUserStore";

export function Callback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [errorMsg, setErrorMsg] = useState("");
  const setSpotifyConnected = useUserStore((s) => s.setSpotifyConnected);

  useEffect(() => {
    let cancelled = false;

    async function process() {
      try {
        const result = await SpotifyService.handleCallback(searchParams);

        if (cancelled) return;

        setSpotifyConnected(true);
        setStatus("success");

        // Navigate back to the originating page with spotify-connected state
        setTimeout(() => {
          if (cancelled) return;
          const target = result.fromPath || "/onboarding";
          navigate(target, {
            replace: true,
            state: {
              spotifyConnected: true,
              userName: result.userName,
              platform: result.platform,
            },
          });
        }, 1200);
      } catch (err: any) {
        if (cancelled) return;
        setStatus("error");
        setErrorMsg(err.message || "Authentication failed");
      }
    }

    process();
    return () => { cancelled = true; };
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
