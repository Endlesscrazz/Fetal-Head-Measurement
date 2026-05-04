import { sampleAssetPath } from "../data/samples";
import type { Sample } from "../types/sample";

export type SampleAssetKey = "ultrasound" | "target" | "pred" | "prob";

export interface SampleAssets {
  ultrasound: string;
  target: string;
  pred: string;
  prob: string;
}

export function getSampleAssets(
  sample: Sample,
  overrides?: Partial<SampleAssets> | null,
): SampleAssets {
  return {
    ultrasound: overrides?.ultrasound ?? sampleAssetPath(sample, "ultrasound"),
    target: overrides?.target ?? sampleAssetPath(sample, "target"),
    pred: overrides?.pred ?? sampleAssetPath(sample, "pred"),
    prob: overrides?.prob ?? sampleAssetPath(sample, "prob"),
  };
}
