/* ── Framer Motion Variants — Cinematic ──────────────────────── */

const ease = [0.22, 1, 0.36, 1] as const;

export const pageTransition = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.8, ease } },
  exit: { opacity: 0, transition: { duration: 0.4 } },
};

export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 1, ease: "easeOut" } },
  exit: { opacity: 0 },
};

export const fadeInSlow = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 2, ease: "easeOut" } },
};

export const staggerChildren = {
  animate: {
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

export const slideUp = {
  initial: { opacity: 0, y: 40 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, ease },
  },
};

export const slideDown = {
  initial: { opacity: 0, y: -20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease },
  },
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.85 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.6, ease },
  },
};

export const expandIn = {
  initial: { opacity: 0, scale: 0.3 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 1.5, ease },
  },
};

export const glowPulse = {
  animate: {
    boxShadow: [
      "0 0 20px rgba(99, 102, 241, 0.1)",
      "0 0 60px rgba(168, 85, 247, 0.2)",
      "0 0 20px rgba(99, 102, 241, 0.1)",
    ],
    transition: { duration: 3, repeat: Infinity, ease: "easeInOut" },
  },
};

export const floatGentle = {
  animate: {
    y: [0, -6, 0],
    transition: { duration: 6, repeat: Infinity, ease: "easeInOut" },
  },
};

export const breathe = {
  animate: {
    scale: [1, 1.02, 1],
    opacity: [0.5, 0.8, 0.5],
    transition: { duration: 4, repeat: Infinity, ease: "easeInOut" },
  },
};

export const typewriter = (text: string, speed = 0.04) => ({
  initial: { width: 0 },
  animate: {
    width: "auto",
    transition: { duration: text.length * speed, ease: "linear" },
  },
});

/* ── Cinematic entrance sequences ────────────────────────────── */

export const cinematicReveal = {
  initial: { opacity: 0, y: 60, filter: "blur(10px)" },
  animate: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 1.2, ease },
  },
};

export const cinematicScale = {
  initial: { opacity: 0, scale: 0.5, filter: "blur(20px)" },
  animate: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px)",
    transition: { duration: 1.5, ease },
  },
};

/* ── Kinetic text — character-by-character ────────────────────── */

export const kineticContainer = {
  initial: {},
  animate: {
    transition: { staggerChildren: 0.03, delayChildren: 0.2 },
  },
};

export const kineticChar = {
  initial: { opacity: 0, y: 40, scale: 0.5, filter: "blur(12px)" },
  animate: {
    opacity: 1,
    y: 0,
    scale: 1,
    filter: "blur(0px)",
    transition: { duration: 0.8, ease },
  },
};

/* ── Scroll-synced (for GSAP ScrollTrigger) ──────────────────── */

export const scrollReveal = {
  initial: { opacity: 0, y: 80 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 1, ease },
  },
};

export const scrollScale = {
  initial: { opacity: 0, scale: 0.8, filter: "blur(8px)" },
  animate: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px)",
    transition: { duration: 1.2, ease },
  },
};
