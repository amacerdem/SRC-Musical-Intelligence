/* ── 24 Persona → Character Part Configurations ─────────────────────── */
import type { CharacterConfig } from "./types";

export const CHARACTER_CONFIGS: Record<number, CharacterConfig> = {
  /* ═══ ALCHEMISTS ═══ */
  1:  { hair: "flames", eyes: "intense", mouth: "smirk", clothing: "cloak-hoodie", accessory: "lightning" },
  6:  { hair: "spikes", eyes: "intense", mouth: "smirk", clothing: "long-cloak", accessory: "blueprint" },
  7:  { hair: "split", eyes: "intense", mouth: "smirk", clothing: "half-contrast", accessory: "yin-yang" },
  18: { hair: "dramatic-wave", eyes: "intense", mouth: "focused", clothing: "theater-cloak", accessory: "mask" },

  /* ═══ ARCHITECTS ═══ */
  2:  { hair: "slick", eyes: "calm", mouth: "neutral-precise", clothing: "collar-shirt", accessory: "tuning-fork" },
  4:  { hair: "buzzcut", eyes: "calm", mouth: "gentle-smile", clothing: "plain-tee", accessory: "none" },
  5:  { hair: "structured", eyes: "determined", mouth: "focused", clothing: "formal-jacket", accessory: "metronome" },
  9:  { hair: "analytical", eyes: "curious", mouth: "neutral-precise", clothing: "argyle-sweater", accessory: "magnifier" },
  20: { hair: "precise", eyes: "determined", mouth: "neutral-precise", clothing: "lab-coat", accessory: "ruler" },

  /* ═══ EXPLORERS ═══ */
  3:  { hair: "wild", eyes: "wide", mouth: "open-smile", clothing: "hoodie-backpack", accessory: "compass" },
  10: { hair: "windswept", eyes: "wide", mouth: "open-smile", clothing: "travel-cloak", accessory: "map" },
  19: { hair: "curly-free", eyes: "curious", mouth: "open-smile", clothing: "explorer-jacket", accessory: "binoculars" },
  23: { hair: "mohawk", eyes: "wide", mouth: "open-smile", clothing: "leather-jacket", accessory: "thorns" },
  24: { hair: "flowing", eyes: "curious", mouth: "open-smile", clothing: "layered-bohemian", accessory: "palette" },

  /* ═══ ANCHORS ═══ */
  8:  { hair: "wavy-warm", eyes: "warm", mouth: "gentle-smile", clothing: "vintage-jacket", accessory: "rose" },
  11: { hair: "soft-long", eyes: "warm", mouth: "gentle-smile", clothing: "soft-sweater", accessory: "heart" },
  13: { hair: "dreamy", eyes: "dreamy", mouth: "gentle-smile", clothing: "flowing-dress", accessory: "cloud" },
  15: { hair: "neat-bob", eyes: "calm", mouth: "gentle-smile", clothing: "cardigan", accessory: "headphones" },
  17: { hair: "ethereal", eyes: "dreamy", mouth: "gentle-smile", clothing: "long-skirt", accessory: "wind" },
  22: { hair: "vintage", eyes: "warm", mouth: "gentle-smile", clothing: "retro-jacket", accessory: "cassette" },

  /* ═══ KINETICISTS ═══ */
  12: { hair: "dreadlocks", eyes: "sharp", mouth: "grin", clothing: "tank-top", accessory: "drumstick" },
  14: { hair: "electric", eyes: "sharp", mouth: "grin", clothing: "torn-tee", accessory: "lightning-pair" },
  16: { hair: "fade", eyes: "sharp", mouth: "grin", clothing: "mechanic-apron", accessory: "wrench" },
  21: { hair: "raw-spikes", eyes: "sharp", mouth: "grin", clothing: "sleeveless-hoodie", accessory: "fire" },
};
