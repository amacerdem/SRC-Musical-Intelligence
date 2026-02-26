/* ── Character Avatar Types ──────────────────────────────────────────── */

import type { NeuralFamily } from "../../types/mind";
import type { PersonaLevel } from "../../types/m3";

/* ── Part Identifiers ────────────────────────────────────────────────── */

export type HeadShape = "angular" | "geometric" | "fluid" | "round" | "athletic";

export type HairStyle =
  | "flames" | "spikes" | "split" | "dramatic-wave"
  | "slick" | "buzzcut" | "structured" | "analytical" | "precise"
  | "wild" | "windswept" | "curly-free" | "mohawk" | "flowing"
  | "wavy-warm" | "soft-long" | "dreamy" | "neat-bob" | "ethereal" | "vintage"
  | "dreadlocks" | "electric" | "fade" | "raw-spikes";

export type EyeStyle =
  | "intense" | "wide" | "calm" | "warm"
  | "sharp" | "dreamy" | "determined" | "curious";

export type MouthStyle =
  | "smirk" | "neutral-precise" | "open-smile"
  | "gentle-smile" | "grin" | "focused";

export type ClothingStyle =
  | "cloak-hoodie" | "long-cloak" | "half-contrast" | "theater-cloak"
  | "collar-shirt" | "plain-tee" | "formal-jacket" | "argyle-sweater" | "lab-coat"
  | "hoodie-backpack" | "travel-cloak" | "explorer-jacket" | "leather-jacket" | "layered-bohemian"
  | "soft-sweater" | "flowing-dress" | "cardigan" | "long-skirt" | "vintage-jacket" | "retro-jacket"
  | "tank-top" | "torn-tee" | "mechanic-apron" | "sleeveless-hoodie";

export type AccessoryType =
  | "lightning" | "tuning-fork" | "compass" | "metronome" | "blueprint"
  | "yin-yang" | "rose" | "magnifier" | "map" | "heart"
  | "drumstick" | "cloud" | "lightning-pair" | "headphones" | "wrench"
  | "wind" | "mask" | "binoculars" | "ruler" | "fire"
  | "cassette" | "thorns" | "palette" | "none";

/* ── Character Configuration ─────────────────────────────────────────── */

export interface CharacterConfig {
  hair: HairStyle;
  eyes: EyeStyle;
  mouth: MouthStyle;
  clothing: ClothingStyle;
  accessory: AccessoryType;
}

/* ── Component Props ─────────────────────────────────────────────────── */

export interface CharacterAvatarProps {
  personaId: number;
  color: string;
  family: NeuralFamily;
  size?: number;
  level?: PersonaLevel;
  showAura?: boolean;
  className?: string;
}

/* ── Family → Head Shape Mapping ─────────────────────────────────────── */

export const FAMILY_HEAD: Record<NeuralFamily, HeadShape> = {
  Alchemists: "angular",
  Architects: "geometric",
  Explorers: "fluid",
  Anchors: "round",
  Kineticists: "athletic",
};
