#!/usr/bin/env bash
# Build the Legend of the Technomancers rulebook with tectonic.
set -euo pipefail
cd "$(dirname "$0")"
tectonic -X compile rulebook.tex "$@"
echo "Built rulebook.pdf"
