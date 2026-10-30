#!/usr/bin/env bash
# Durable publish gate: derive, then verify, and ONLY then build.
# A verify_content failure exits non-zero and build/push must not happen.
# Usage: bash scripts/build_verified.sh   (then commit+push only if exit 0)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/derive.py
python3 scripts/verify_content.py
python3 scripts/build_site.py
