#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_ROOT}"

PYTHON="${PYTHON:-.venv/bin/python}"
MODE="report-only"
RUN_TESTS=1

usage() {
  cat <<'EOF'
Fetal HC18 project runner

Usage:
  bash Myproject.sh [--report-only|--full-local] [--skip-tests]

Modes:
  --report-only  Rebuild report tables/figures from saved local run artifacts.
                 This is the default and is intended for fast course review.
  --full-local   Regenerate splits, train/evaluate the local v1 experiment set,
                 then rebuild report artifacts. This can take a while.

Environment:
  PYTHON=/path/to/python  Override Python executable. Default: .venv/bin/python
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --report-only)
      MODE="report-only"
      shift
      ;;
    --full-local)
      MODE="full-local"
      shift
      ;;
    --skip-tests)
      RUN_TESTS=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing required file: $1" >&2
    return 1
  fi
}

require_python() {
  if [[ ! -x "${PYTHON}" ]]; then
    echo "Python executable not found: ${PYTHON}" >&2
    echo "Create the environment with:" >&2
    echo "  UV_CACHE_DIR=.uv-cache uv venv .venv" >&2
    echo "  UV_CACHE_DIR=.uv-cache uv pip install -r requirements.txt" >&2
    exit 1
  fi
}

run_tests() {
  if [[ "${RUN_TESTS}" -eq 1 ]]; then
    "${PYTHON}" -m pytest tests
  fi
}

make_splits() {
  "${PYTHON}" -m src.data.make_splits --config configs/data.yaml
}

train_run() {
  local config="$1"
  "${PYTHON}" -m src.training.train --config "${config}"
}

evaluate_run() {
  local run_id="$1"
  local split="$2"
  "${PYTHON}" -m src.evaluation.evaluate \
    --config "outputs/runs/${run_id}/config.json" \
    --checkpoint "outputs/runs/${run_id}/best_model.pt" \
    --split "${split}"
}

make_figures() {
  local run_id="$1"
  local split="$2"
  "${PYTHON}" scripts/make_report_figures.py --run-id "${run_id}" --split "${split}"
}

evaluate_and_plot_run() {
  local run_id="$1"
  for split in val test; do
    evaluate_run "${run_id}" "${split}"
    make_figures "${run_id}" "${split}"
  done
}

build_comparison_tables() {
  "${PYTHON}" scripts/compare_runs.py \
    --runs \
      unet_local_baseline \
      attention_unet_local_baseline \
      attention_unet_dice_loss \
      attention_unet_aug \
    --splits val test \
    --output outputs/tables/local_ablation_summary.csv

  for split in val test; do
    "${PYTHON}" scripts/postprocess_ablation.py \
      --run-id attention_unet_local_baseline \
      --split "${split}"
  done

  "${PYTHON}" -c "import pandas as pd; from pathlib import Path; run='attention_unet_local_baseline'; frames=[pd.read_csv(f'outputs/tables/{run}_{split}_postprocess_ablation.csv') for split in ['val','test']]; out=Path('outputs/tables/local_postprocess_ablation_summary.csv'); out.parent.mkdir(parents=True, exist_ok=True); pd.concat(frames, ignore_index=True).to_csv(out, index=False); print(f'Saved {out}')"
}

build_report() {
  build_comparison_tables
  "${PYTHON}" scripts/build_report_artifacts.py
}

require_saved_artifacts() {
  require_file outputs/runs/unet_local_baseline/config.json
  require_file outputs/runs/unet_local_baseline/evaluation/val/aggregate_metrics.csv
  require_file outputs/runs/unet_local_baseline/evaluation/test/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_local_baseline/config.json
  require_file outputs/runs/attention_unet_local_baseline/evaluation/val/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_local_baseline/evaluation/test/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_local_baseline/predictions/val/predictions.csv
  require_file outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv
  require_file outputs/runs/attention_unet_dice_loss/config.json
  require_file outputs/runs/attention_unet_dice_loss/evaluation/val/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_dice_loss/evaluation/test/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_aug/config.json
  require_file outputs/runs/attention_unet_aug/evaluation/val/aggregate_metrics.csv
  require_file outputs/runs/attention_unet_aug/evaluation/test/aggregate_metrics.csv
}

run_full_local() {
  make_splits

  train_run configs/unet_local_baseline.yaml
  train_run configs/attention_unet.yaml
  train_run configs/attention_unet_dice_loss.yaml
  train_run configs/attention_unet_aug.yaml

  evaluate_and_plot_run unet_local_baseline
  evaluate_and_plot_run attention_unet_local_baseline
  evaluate_and_plot_run attention_unet_dice_loss
  evaluate_and_plot_run attention_unet_aug

  build_report
}

require_python

echo "Fetal HC18 project runner"
echo "Mode: ${MODE}"
echo "Python: ${PYTHON}"

if [[ "${MODE}" == "full-local" ]]; then
  run_full_local
else
  require_saved_artifacts
  build_report
fi

run_tests

echo
echo "Done."
echo "Report summary: report/report-results-summary.md"
echo "Main results:   report/tables/main_test_results.csv"
