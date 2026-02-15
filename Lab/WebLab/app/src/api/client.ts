import type {
  ExperimentMeta,
  NucleusData,
  PsiData,
  R3Group,
  RegionInfo,
  H3Features,
} from "../types/experiment";

const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

// --- Experiment endpoints ---

export function fetchExperimentList(): Promise<string[]> {
  return get("/experiments");
}

export function fetchMeta(slug: string): Promise<ExperimentMeta> {
  return get(`/experiments/${slug}/meta`);
}

export function audioUrl(slug: string): string {
  return `${BASE}/experiments/${slug}/audio`;
}

export function fetchR3(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/r3`);
}

export function fetchNucleus(slug: string, name: string): Promise<NucleusData> {
  return get(`/experiments/${slug}/nuclei/${name}`);
}

export function fetchRam(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/ram`);
}

export function fetchNeuro(slug: string): Promise<number[][]> {
  return get(`/experiments/${slug}/neuro`);
}

export function fetchPsi(slug: string): Promise<PsiData> {
  return get(`/experiments/${slug}/psi`);
}

export function fetchH3(slug: string): Promise<H3Features> {
  return get(`/experiments/${slug}/h3`);
}

// --- Registry endpoints ---

export function fetchR3Registry(): Promise<{
  groups: R3Group[];
  feature_names: string[];
}> {
  return get("/registry/r3");
}

export function fetchRegions(): Promise<RegionInfo[]> {
  return get("/registry/regions");
}
