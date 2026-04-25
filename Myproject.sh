#!/usr/bin/env bash
set -euo pipefail

# Course runner placeholder.
# This script will be expanded as the pipeline is implemented.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_ROOT}"

echo "Fetal HC18 project runner"
echo "Current status: scaffold created; data/model pipeline tasks are pending."
echo
echo "Expected future flow:"
echo "  1. prepare data splits"
echo "  2. train U-Net baseline"
echo "  3. run inference/evaluation"
echo "  4. generate report tables and figures"
echo
echo "See project-tasks.md for the next implementation session."
