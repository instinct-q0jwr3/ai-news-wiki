#!/usr/bin/env bash
set -u
python3 src/update_feed.py || status=$?
# Exit 1 from ingest means an empty filtered pass; derived/site still rebuild.
if [[ ${status:-0} -gt 1 ]]; then exit "$status"; fi
python3 scripts/derive.py
# Pre-publication reviewer: blocks the build if any standing content rule is violated
# (authored day-specific digest sections, no fixed taxonomy, no char-per-line prose,
# digest story ids resolve). See scripts/verify_content.py.
python3 scripts/verify_content.py || exit 3
python3 scripts/build_site.py
