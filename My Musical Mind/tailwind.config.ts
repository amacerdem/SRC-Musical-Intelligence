import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        m3: {
          bg: "#000000",
          surface: "rgba(255,255,255,0.03)",
          "surface-raised": "rgba(255,255,255,0.05)",
          "surface-hover": "rgba(255,255,255,0.07)",
          border: "rgba(255,255,255,0.06)",
          "border-hover": "rgba(255,255,255,0.10)",

          /* ── Belief domain colors ──────────────────────────── */
          consonance: "#C084FC",    // purple-400
          tempo: "#F97316",         // orange-500
          salience: "#84CC16",      // lime-500
          familiarity: "#38BDF8",   // sky-400
          reward: "#FBBF24",        // amber-400

          accent: {
            indigo: "#6366F1",
            purple: "#A855F7",
            violet: "#8B5CF6",
            pink: "#EC4899",
            rose: "#F43F5E",
            cyan: "#06B6D4",
          },
          success: "#10B981",
          warning: "#F59E0B",
          danger: "#EF4444",
        },
      },
      fontFamily: {
        display: ["Saira", "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "monospace"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "accent-gradient":
          "linear-gradient(135deg, #6366F1, #A855F7, #EC4899)",
        "accent-gradient-h":
          "linear-gradient(90deg, #6366F1, #A855F7, #EC4899)",
        /* ── Belief gradients ──────────────────────────────── */
        "consonance-gradient":
          "linear-gradient(135deg, #C084FC, #F472B6, #EC4899)",
        "tempo-gradient":
          "linear-gradient(135deg, #EF4444, #F97316, #FDE047)",
        "salience-gradient":
          "linear-gradient(135deg, #FDE047, #84CC16, #22C55E)",
        "familiarity-gradient":
          "linear-gradient(135deg, #22D3EE, #3B82F6, #6366F1)",
        "reward-gradient":
          "linear-gradient(135deg, #F59E0B, #FDE047, #FFFFFF)",
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        glow: "glow 2s ease-in-out infinite alternate",
        float: "float 6s ease-in-out infinite",
        "float-slow": "float 8s ease-in-out infinite",
        breathe: "breathe 4s ease-in-out infinite",
        drift: "drift 20s linear infinite",
        "fade-up": "fadeUp 0.8s ease-out forwards",
        "scale-in": "scaleIn 0.6s ease-out forwards",
        orbit: "orbit 30s linear infinite",
        "orbit-slow": "orbit 36s linear infinite",
        "orbit-fast": "orbit 24s linear infinite",
        "orbit-reverse": "orbitReverse 30s linear infinite",
        "grain-shift": "grainShift 0.5s steps(10) infinite",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 20px rgba(99,102,241,0.1)" },
          "100%": { boxShadow: "0 0 50px rgba(168,85,247,0.2)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
        breathe: {
          "0%, 100%": { opacity: "0.4", transform: "scale(1)" },
          "50%": { opacity: "0.7", transform: "scale(1.02)" },
        },
        drift: {
          "0%": { transform: "translate(0, 0) rotate(0deg)" },
          "25%": { transform: "translate(10px, -5px) rotate(1deg)" },
          "50%": { transform: "translate(-5px, 10px) rotate(-0.5deg)" },
          "75%": { transform: "translate(-10px, -3px) rotate(0.5deg)" },
          "100%": { transform: "translate(0, 0) rotate(0deg)" },
        },
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(30px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.85)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        orbit: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        orbitReverse: {
          "0%": { transform: "rotate(360deg)" },
          "100%": { transform: "rotate(0deg)" },
        },
        grainShift: {
          "0%": { transform: "translate(0, 0)" },
          "10%": { transform: "translate(-5%, -10%)" },
          "20%": { transform: "translate(-15%, 5%)" },
          "30%": { transform: "translate(7%, -15%)" },
          "40%": { transform: "translate(-5%, 15%)" },
          "50%": { transform: "translate(-15%, 10%)" },
          "60%": { transform: "translate(15%, 0%)" },
          "70%": { transform: "translate(0%, 10%)" },
          "80%": { transform: "translate(3%, -20%)" },
          "90%": { transform: "translate(-10%, 10%)" },
          "100%": { transform: "translate(0, 0)" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
      borderRadius: {
        "4xl": "2rem",
      },
    },
  },
  plugins: [],
} satisfies Config;
