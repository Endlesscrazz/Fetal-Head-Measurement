"""Streamlit saved-output explorer for the fetal HC18 pipeline."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from demo.adapters.saved_output import load_manifest, load_sample
from demo.components.pipeline_views import (
    render_geometry_snapshot,
    render_metrics,
    render_pipeline_stages,
    render_sample_header,
)
from demo.components.sample_selector import render_sample_selector


DEFAULT_MANIFEST = Path("outputs/demo_samples/manifest.json")


@st.cache_data(show_spinner=False)
def _load_manifest_cached(path: str):
    return load_manifest(path)


@st.cache_data(show_spinner=False)
def _load_sample_cached(path: str, sample_id: str):
    manifest = load_manifest(path)
    return load_sample(manifest, sample_id)


def main() -> None:
    st.set_page_config(
        page_title="Fetal HC Pipeline Explorer",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    manifest_path = st.sidebar.text_input("Manifest", value=str(DEFAULT_MANIFEST))
    try:
        manifest = _load_manifest_cached(manifest_path)
    except FileNotFoundError:
        st.error(
            "Demo artifacts are missing. Run "
            "`.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`."
        )
        st.stop()
    except Exception as exc:  # pragma: no cover - Streamlit-facing guardrail.
        st.error(f"Could not load demo manifest: {exc}")
        st.stop()

    st.title("Fetal HC Pipeline Explorer")
    st.warning(manifest.safety_text)
    st.caption(
        f"Saved-output mode | {manifest.created_from_run_id or 'unknown run'} | "
        f"{len(manifest.samples)} curated samples"
    )

    sample_id = render_sample_selector(manifest)
    try:
        sample = _load_sample_cached(manifest_path, sample_id)
    except Exception as exc:  # pragma: no cover - Streamlit-facing guardrail.
        st.error(f"Could not load sample `{sample_id}`: {exc}")
        st.stop()

    render_sample_header(sample)
    render_metrics(sample)
    render_pipeline_stages(sample)
    render_geometry_snapshot(sample)


if __name__ == "__main__":
    main()
