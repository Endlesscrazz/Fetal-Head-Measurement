export interface MetricCopy {
  label: string;
  description: string;
  interpret: (value: number) => string;
}

export const METRIC_COPY: Record<string, MetricCopy> = {
  dice: {
    label: "Dice",
    description: "Overlap between predicted and true masks. 1.0 is identical.",
    interpret: (value: number) => {
      if (value >= 0.97) return "Practically pixel-perfect.";
      if (value >= 0.92) return "Strong overlap with minor edge slip.";
      if (value >= 0.85) return "Recognizable, with visible drift.";
      return "Significant disagreement.";
    },
  },
  iou: {
    label: "IoU",
    description: "Intersection over Union: how much of the masks coincide.",
    interpret: (value: number) => {
      if (value >= 0.95) return "Near-identical regions.";
      if (value >= 0.85) return "High overlap with edge noise.";
      if (value >= 0.7) return "Workable but imperfect.";
      return "Geometric drift.";
    },
  },
  hcErr: {
    label: "HC error",
    description: "Difference between predicted and target circumference, in mm.",
    interpret: (value: number) => {
      if (value < 0.1) return "Below one tenth of a millimeter.";
      if (value < 0.5) return "Below pencil-tip width.";
      if (value < 2) return "About a grain of rice.";
      if (value < 5) return "A few visible millimeters.";
      return "Several millimeters off.";
    },
  },
  hd95_mm: {
    label: "HD95",
    description: "95th-percentile boundary error, ignoring outliers.",
    interpret: (value: number) => {
      if (value < 1) return "Boundary lines almost overlap.";
      if (value < 3) return "Boundary slip visible when zoomed in.";
      if (value < 6) return "Visible boundary drift on the source image.";
      return "Boundary drift visible at thumbnail size.";
    },
  },
};
