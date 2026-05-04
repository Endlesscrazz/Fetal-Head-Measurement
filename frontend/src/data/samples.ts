import type { Manifest, Sample } from "../types/sample";

const DEFAULT_MANIFEST_PATH = "/samples/manifest.json";
const PUBLIC_PREVIEW_MANIFEST_PATH = "/demo-samples/manifest.json";

export function preferredManifestPath(): string {
  return DEFAULT_MANIFEST_PATH;
}

export async function loadManifest(path = preferredManifestPath()): Promise<Manifest> {
  const response = await fetch(path);
  if (!response.ok) {
    if (path === DEFAULT_MANIFEST_PATH) {
      return loadManifest(PUBLIC_PREVIEW_MANIFEST_PATH);
    }
    if (path === PUBLIC_PREVIEW_MANIFEST_PATH) {
      return loadManifest(DEFAULT_MANIFEST_PATH);
    }
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

export function sampleAssetPath(sample: Sample, filename: "ultrasound" | "target" | "pred" | "prob"): string {
  const base = sample.assetBasePath ?? `/samples/${sample.id}`;
  const extension = sample.assetExtension ?? "png";
  return `${base}/${filename}.${extension}`;
}
