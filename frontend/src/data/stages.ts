export type StageKind = "image" | "mask" | "prob" | "ellipse" | "hc";

export interface PipelineStage {
  id: string;
  short: string;
  title: string;
  blurb: string;
  detail: string;
  kind: StageKind;
}

export const STAGES: PipelineStage[] = [
  {
    id: "input",
    short: "Input",
    title: "Ultrasound input",
    blurb: "A grayscale 2D ultrasound of the fetal head, captured in the transthalamic plane.",
    detail: "The model receives a single-channel image. No metadata, no patient context, just pixels.",
    kind: "image",
  },
  {
    id: "target",
    short: "Target",
    title: "Annotation-derived mask",
    blurb: "A radiologist-annotated outline, rendered as a binary mask. This is the ground truth.",
    detail:
      "During training the model tries to reproduce this mask. At inference, we use it only to score how well the prediction matches reality.",
    kind: "mask",
  },
  {
    id: "prob",
    short: "CNN",
    title: "CNN probability map",
    blurb: "For every pixel, the network outputs P(skull). Bright means confident; dark means uncertain.",
    detail:
      "This is a U-Net-style segmentation head with attention gates. The map is continuous, so the model expresses belief before thresholding.",
    kind: "prob",
  },
  {
    id: "mask",
    short: "Mask",
    title: "Threshold and cleanup",
    blurb: "A threshold converts probabilities to a binary mask. Small holes are filled and stray blobs are removed.",
    detail: "This is where the model commits. Choosing the threshold is a design decision for the next UI session.",
    kind: "mask",
  },
  {
    id: "ellipse",
    short: "Ellipse",
    title: "Ellipse fitting",
    blurb: "A least-squares ellipse is fit to the mask boundary.",
    detail:
      "Fitting an ellipse instead of measuring the raw contour makes the final measurement more robust to noisy segmentation edges.",
    kind: "ellipse",
  },
  {
    id: "hc",
    short: "HC",
    title: "Head circumference",
    blurb: "The ellipse perimeter, scaled by pixel size, gives head circumference in millimeters.",
    detail: "This is the clinically meaningful number a sonographer would otherwise measure by hand.",
    kind: "hc",
  },
];
