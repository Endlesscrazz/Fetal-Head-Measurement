"""Pipeline visualization components for the saved-output demo."""

from __future__ import annotations

import numpy as np
import streamlit as st

from demo.types import DemoSample


def _fmt_mm(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f} mm"


def _fmt_score(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.4f}"


def _mask_display(mask: np.ndarray | None) -> np.ndarray | None:
    if mask is None:
        return None
    return (mask.astype(np.uint8) * 255)


def render_sample_header(sample: DemoSample) -> None:
    st.subheader(sample.label)
    st.caption(f"{sample.sample_id} | {sample.category or 'uncategorized'} | split: {sample.split}")
    if sample.reason:
        st.caption(sample.reason)


def render_metrics(sample: DemoSample) -> None:
    cols = st.columns(5)
    cols[0].metric("Pred HC", _fmt_mm(sample.hc_pred_mm))
    cols[1].metric("Target HC", _fmt_mm(sample.hc_gt_mm))
    cols[2].metric("HC Error", _fmt_mm(sample.abs_hc_error_mm))
    cols[3].metric("Dice", _fmt_score(sample.dice))
    cols[4].metric("HD95", _fmt_mm(sample.hd95_mm))


def render_pipeline_stages(sample: DemoSample) -> None:
    st.markdown("#### Pipeline Stages")
    top = st.columns(3)
    top[0].image(sample.image, caption="Original ultrasound", width="stretch", clamp=True)
    target = _mask_display(sample.target_mask)
    if target is None:
        top[1].info("Target mask unavailable")
    else:
        top[1].image(target, caption="Annotation-derived target mask", width="stretch", clamp=True)
    top[2].image(_mask_display(sample.raw_mask), caption="Thresholded CNN output", width="stretch", clamp=True)

    bottom = st.columns(2)
    bottom[0].image(_mask_display(sample.cleaned_mask), caption="Cleaned mask", width="stretch", clamp=True)
    bottom[1].image(sample.ellipse_overlay, caption="Ellipse overlay", width="stretch", clamp=True)


def render_geometry_snapshot(sample: DemoSample) -> None:
    st.markdown("#### Measurement")
    cols = st.columns(3)
    cols[0].metric("Ellipse HC", _fmt_mm(sample.hc_pred_mm))
    cols[1].metric("Contour HC", _fmt_mm(sample.contour_hc_mm))
    cols[2].metric("Signed Error", _fmt_mm(sample.signed_hc_error_mm))

    if sample.ellipse_params:
        params = sample.ellipse_params
        st.caption(
            "Ellipse center "
            f"({params.get('center_x', 0.0):.1f}, {params.get('center_y', 0.0):.1f}), "
            f"axes {params.get('semi_axis_a', 0.0):.1f} x {params.get('semi_axis_b', 0.0):.1f} px, "
            f"angle {params.get('angle_deg', 0.0):.1f} deg"
        )
