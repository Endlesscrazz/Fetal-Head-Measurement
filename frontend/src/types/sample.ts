export interface SampleMetrics {
  dice: number;
  iou: number;
  hd95_mm: number;
  hcErr: number;
  predHC: number;
  targetHC: number;
}

export interface Ellipse {
  cx: number;
  cy: number;
  rx: number;
  ry: number;
  rot: number;
}

export type SampleCategory = "strong" | "typical" | "failure";

export interface Sample {
  id: string;
  label: string;
  cat: SampleCategory;
  split: string;
  summary: string;
  metrics: SampleMetrics;
  predEllipse: Ellipse;
  contourHC: number;
  confidence: number;
  spacingXMm: number;
  spacingYMm: number;
  resolution: { w: number; h: number };
  notes?: string;
}

export interface Manifest {
  schema_version: number;
  created_from_run_id: string;
  created_from_split?: string;
  safety_text: string;
  samples: Sample[];
}
