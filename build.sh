#!/usr/bin/env bash
# Build the Legend of the Technomancers rulebook with tectonic.
#
# Always cleans aux/log/out/toc files first: a stale .toc (or a chapter
# .aux left over from a previous run) has silently produced wrong page
# counts/numbers in this project before. The book is small enough that
# a full clean build is fast, so there's no reason to risk it.
set -euo pipefail
cd "$(dirname "$0")"
rm -f rulebook.aux rulebook.log rulebook.out rulebook.toc chapters/*.aux
tectonic -X compile rulebook.tex "$@"
echo "Built rulebook.pdf"
