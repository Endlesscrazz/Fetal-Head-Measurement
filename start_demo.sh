#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

RUN_ID="${RUN_ID:-attention_unet_local_baseline}"
SPLIT="${SPLIT:-test}"

if [[ ! -f "outputs/demo_samples/manifest.json" ]]; then
  echo "outputs/demo_samples/manifest.json not found; exporting curated demo artifacts..."
  if [[ ! -x ".venv/bin/python" ]]; then
    echo "Missing .venv/bin/python. Create the Python environment before exporting artifacts." >&2
    exit 1
  fi
  ".venv/bin/python" scripts/export_demo_artifacts.py --run-id "$RUN_ID" --split "$SPLIT"
fi

mkdir -p frontend/public/samples
cp -R outputs/demo_samples/. frontend/public/samples/

cd frontend
npm install
npm run dev
