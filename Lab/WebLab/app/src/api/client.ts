/**
 * Static JSON data client — no backend server needed.
 * All data is pre-computed and served from Vite's public/ directory.
 */
import type {
  ExperimentMeta,
  NucleusData,
  PsiData,
  R3Group,
  RegionInfo,
  H3Features,
} from "../types/experiment";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Fetch ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

// --- Experiment data (from /experiments/{slug}/) ---

export function fetchExperimentList(): Promise<string[]> {
  return get("/data/experiments-index.json");
}

export function fetchMeta(slug: string): Promise<ExperimentMeta> {
  return get(`/experiments/${slug}/meta.json`);
}

export function audioUrl(slug: string): string {
  return `/experiments/${slug}/audio.wav`;
}

export function fetchR3(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/r3.json`);
}

export function fetchNucleus(slug: string, name: string): Promise<NucleusData> {
  return get(`/experiments/${slug}/nuclei/${name}.json`);
}

export function fetchRam(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/ram.json`);
}

export function fetchNeuro(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/neuro.json`);
}

export function fetchPsi(slug: string): Promise<PsiData> {
  return get(`/experiments/${slug}/psi.json`);
}

export function fetchH3(slug: string): Promise<H3Features> {
  return get(`/experiments/${slug}/h3.json`);
}

// --- Registry data (static, from /data/) ---

export function fetchR3Registry(): Promise<{
  groups: R3Group[];
  feature_names: string[];
}> {
  return get("/data/r3-registry.json");
}

export function fetchRegions(): Promise<RegionInfo[]> {
  return get("/data/regions.json");
}
