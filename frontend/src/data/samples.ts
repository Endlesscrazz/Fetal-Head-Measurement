import type { Manifest } from "../types/sample";

const DEFAULT_MANIFEST_PATH = "/samples/manifest.json";

export async function loadManifest(path = DEFAULT_MANIFEST_PATH): Promise<Manifest> {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Could not load manifest at ${path}: ${response.status} ${response.statusText}`);
  }

  const manifest = (await response.json()) as Manifest;
  if (manifest.schema_version !== 2) {
    throw new Error(`Expected manifest schema_version 2, got ${manifest.schema_version}`);
  }
  if (!Array.isArray(manifest.samples) || manifest.samples.length === 0) {
    throw new Error("Manifest has no samples");
  }
  return manifest;
}

export function sampleAssetPath(sampleId: string, filename: "ultrasound" | "target" | "pred" | "prob"): string {
  return `/samples/${sampleId}/${filename}.png`;
}
