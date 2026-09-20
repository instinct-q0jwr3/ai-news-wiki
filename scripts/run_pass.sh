#!/usr/bin/env bash
set -u
python3 src/update_feed.py || status=$?
# Exit 1 from ingest means an empty filtered pass; derived/site still rebuild.
if [[ ${status:-0} -gt 1 ]]; then exit "$status"; fi
python3 scripts/derive.py
python3 scripts/build_site.py
