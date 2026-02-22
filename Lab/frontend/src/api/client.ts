/** API client for MI-Lab backend. */

const BASE = '/api';

export async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function fetchBinary(path: string): Promise<{ data: ArrayBuffer; headers: Headers }> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return { data: await res.arrayBuffer(), headers: res.headers };
}

export async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return res.json();
}

export function audioStreamUrl(name: string): string {
  return `${BASE}/audio/stream/${encodeURIComponent(name)}`;
}
