#!/usr/bin/env bash
# Build the Across the Realms rulebook with tectonic.
set -euo pipefail
cd "$(dirname "$0")"
tectonic -X compile rulebook.tex "$@"
echo "Built rulebook.pdf"
