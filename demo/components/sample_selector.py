"""Sample selection controls for the saved-output demo."""

from __future__ import annotations

import streamlit as st

from demo.types import DemoManifest


def render_sample_selector(manifest: DemoManifest) -> str:
    """Render a sample selector and return the selected sample id."""

    entries = list(manifest.samples)
    if not entries:
        st.error("No demo samples are listed in the manifest.")
        st.stop()

    categories = ["All"] + sorted({entry.category for entry in entries})
    selected_category = st.sidebar.selectbox("Category", categories, index=0)
    if selected_category != "All":
        entries = [entry for entry in entries if entry.category == selected_category]

    options = [entry.sample_id for entry in entries]
    labels = {
        entry.sample_id: f"{entry.label} ({entry.sample_id})"
        for entry in entries
    }
    return st.sidebar.selectbox(
        "Sample",
        options,
        format_func=lambda sample_id: labels.get(sample_id, sample_id),
    )
