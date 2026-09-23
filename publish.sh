#!/usr/bin/env bash
# Upload the built rulebook to the `latest-build` release and redeploy
# GitHub Pages (https://qemqemqem.github.io/legend_of_the_technomancers/).
# Asset uploads don't trigger the Pages workflow on their own.
set -euo pipefail
cd "$(dirname "$0")"
gh release upload latest-build rulebook.pdf --clobber
gh workflow run pages.yml
echo "Uploaded rulebook.pdf; Pages deploy started"
